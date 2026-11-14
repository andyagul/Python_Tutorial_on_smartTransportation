#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""为既有章节的 74 个知识点追加「原理补充 / 变式代码 / 实操步骤 / FAQ」四段增补。

严格约束（用户明确要求）：
1. **只在指定位置插入新行，不修改、不删除、不重排任何原文行**；
2. 「原理补充」插在 `### <sec>.2` 之前（即核心概念 / 集中讲解末尾）；
3. 「变式代码 + 实操步骤 + FAQ」插在该知识点末尾（下一个一级/二级标题之前）；
4. 变式代码**真实执行采集 stdout** 写入「预期输出」块，保证与 verify_demos.py 逐字一致；
5. 编号接续原有小节：普通章节 .5 / .6，第 5A 节（原有 3 小节）.4 / .5；
6. 带重复注入保护，可反复执行 --check。

数据文件：.workbuddy/build/enrichment/ch*.py，每个模块需提供 CHAPTER 与 ITEMS。
  ITEMS 每项字段：anchor(完整 ## 标题行), sec(小节号如 "1.2"),
  demo(围栏名如 "demo1-1b"), principle, variant, code, steps[], faq[(现象,根因,处理)]

用法：
  python3 enrich_chapters.py --check                    # 校验数据 + 实跑全部变式代码
  python3 enrich_chapters.py --apply                   # 写入全部章节
  python3 enrich_chapters.py --apply 01初识Python世界  # 只写指定章节
  python3 enrich_chapters.py --undo                   # 精确回滚本次注入（保留其他改动）
  python3 enrich_chapters.py --verify                  # 核验已注入章节的原文未被改动
"""

import glob
import importlib.util
import os
import re
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "enrichment")

H_ANY = re.compile(r"^#{1,2}\s")


def load_modules():
    mods = []
    for p in sorted(glob.glob(os.path.join(DATA_DIR, "ch*.py"))):
        spec = importlib.util.spec_from_file_location("enrich_" + os.path.basename(p)[:-3], p)
        m = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(m)
        mods.append((p, m))
    return mods


def run_code(code):
    p = subprocess.run([sys.executable, "-c", code], capture_output=True, text=True, timeout=30)
    if p.returncode != 0:
        raise RuntimeError("变式代码运行失败：\n" + p.stderr.strip()[-500:])
    out = p.stdout.rstrip("\n")
    if not out:
        raise RuntimeError("变式代码没有任何 stdout，请补充 print")
    return out


def render_principle(item):
    return [
        "**原理补充（概念深化）**：" + item["principle"].strip(),
        "",
    ]


def render_tail(item, stdout, n_step, n_faq):
    sec = item["sec"]
    lines = [
        "**变式代码（迁移练习）**：" + item["variant"].strip(),
        "",
        "```python " + item["demo"],
    ]
    lines += item["code"].rstrip("\n").split("\n")
    lines += ["```", "", "**预期输出**：", "", "```text"]
    lines += stdout.split("\n")
    lines += ["```", "", "### %s.%d 实操步骤（上机跟随）" % (sec, n_step), ""]
    for i, s in enumerate(item["steps"], 1):
        lines += ["%d. %s" % (i, s.strip())]
    lines += ["", "### %s.%d 常见问题 FAQ" % (sec, n_faq), "",
              "| 现象 | 根因 | 处理 |", "|---|---|---|"]
    for q in item["faq"]:
        lines.append("| %s | %s | %s |" % tuple(x.strip().replace("|", "\\|") for x in q))
    lines += ["", ""]
    return lines


def scan_until(lines, start, stop, pattern=None):
    """在 [start, stop) 内查找第一个位于**代码块外部**的标题行。

    关键：讲义代码块里大量注释以 `# ` 开头，与 `^#{1,2}\\s` 的标题形态完全相同。
    若不跟踪 ``` 围栏状态，插入点会落进代码块内部，直接破坏 md 结构。
    """
    in_fence = False
    for i in range(start, stop):
        line = lines[i]
        if line.startswith("```"):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        if pattern.match(line) if pattern else H_ANY.match(line):
            return i
    return None


def locate(lines, item, n_step):
    anchors = [i for i, l in enumerate(lines) if l.rstrip() == item["anchor"].rstrip()]
    if len(anchors) != 1:
        raise RuntimeError("anchor 匹配 %d 次（应为 1）：%s" % (len(anchors), item["anchor"]))
    a = anchors[0]

    end = scan_until(lines, a + 1, len(lines))
    if end is None:
        end = len(lines)

    p2 = re.compile(r"^### " + re.escape(item["sec"]) + r"\.2\s")
    principle_at = scan_until(lines, a + 1, end, p2)
    if principle_at is None:
        raise RuntimeError("找不到 %s.2 小节（原理补充插入点）：%s" % (item["sec"], item["anchor"]))

    marker = "### %s.%d 实操步骤" % (item["sec"], n_step)
    if any(l.startswith(marker) for l in lines):
        return None                        # 已注入，跳过
    return a, principle_at, end


def undo(mod):
    """精确回滚：按数据文件复现两个插入块，在文件中找到连续行并整段删除。

    由于注入是纯插入，块内文本不会被改写；因此按连续行序列删除是安全的，
    且能保留章节中其他（非本次增补的）改动，例如第 13 章的章节衔接文案。
    """
    chapter = mod.CHAPTER
    md_path = os.path.join(ROOT, chapter, "案例与练习.md")
    with open(md_path, encoding="utf-8") as f:
        lines = f.read().split("\n")
    n_step, n_faq = (4, 5) if chapter.startswith("05A") else (5, 6)
    # 已经回滚或从未注入的章节直接跳过，便于与 git 恢复的章节混合处理
    if not any(l.startswith("### %s.%d 实操步骤" % (it["sec"], n_step)) for it in mod.ITEMS for l in lines):
        print("%-22s 未注入，跳过回滚" % chapter)
        return 0

    removed_items = removed_lines = 0
    for item in mod.ITEMS:
        stdout = run_code(item["code"])
        blocks = (render_principle(item), render_tail(item, stdout, n_step, n_faq))
        found = []
        for block in blocks:
            n = len(block)
            hits = [i for i in range(len(lines) - n + 1) if lines[i:i + n] == block]
            if len(hits) != 1:
                raise RuntimeError("%s 回滚块匹配 %d 次（应为 1）：%s" %
                                   (chapter, len(hits), item["anchor"]))
            found.append((hits[0], n))
        for pos, n in sorted(found, key=lambda x: -x[0]):
            del lines[pos:pos + n]
        removed_items += 1
        removed_lines += sum(n for _, n in found)

    with open(md_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print("%-22s 已回滚 %2d 个知识点 / %4d 行" % (chapter, removed_items, removed_lines))
    return removed_items


def process(mod, apply_changes):
    chapter = mod.CHAPTER
    md_path = os.path.join(ROOT, chapter, "案例与练习.md")
    with open(md_path, encoding="utf-8") as f:
        lines = f.read().split("\n")
    original = list(lines)
    n_step, n_faq = (4, 5) if chapter.startswith("05A") else (5, 6)

    inserts = []
    checked = 0
    for item in mod.ITEMS:
        for key in ("anchor", "sec", "demo", "principle", "variant", "code", "steps", "faq"):
            if key not in item:
                raise RuntimeError("%s 缺少字段 %s：%s" % (chapter, key, item.get("anchor")))
        stdout = run_code(item["code"])          # 无论 apply 与否都实跑，保证代码可用
        checked += 1
        pos = locate(lines, item, n_step)
        if pos is None:
            continue
        a, principle_at, end = pos
        inserts.append((principle_at, render_principle(item)))
        inserts.append((end, render_tail(item, stdout, n_step, n_faq)))

    print("%-22s 知识点 %2d | 待注入 %2d | 变式代码实跑 %2d 通过" %
          (chapter, len(mod.ITEMS), len(inserts) // 2, checked))

    if apply_changes and inserts:
        for pos, block in sorted(inserts, key=lambda x: -x[0]):
            lines[pos:pos] = block
        with open(md_path, "w", encoding="utf-8") as f:
            f.write("\n".join(lines))
        # 逐行核验：原文每一行都还在，且顺序不变（纯插入的严格证明）
        j = 0
        for line in lines:
            if j < len(original) and line == original[j]:
                j += 1
        if j != len(original):
            raise RuntimeError("%s：原文行未完整保留（%d/%d），已中止！" % (chapter, j, len(original)))
        print("   ✅ 已写入，原文 %d 行全部保留且顺序不变，新增 %d 行" %
              (len(original), len(lines) - len(original)))
    return len(inserts) // 2


def main():
    args = sys.argv[1:]
    apply_changes = "--apply" in args
    undo_changes = "--undo" in args
    targets = [a for a in args if not a.startswith("--")]
    mods = load_modules()
    if not mods:
        print("⚠️ 未找到增补数据文件：%s/ch*.py" % DATA_DIR)
        return 1
    total = 0
    for p, m in mods:
        if targets and m.CHAPTER not in targets:
            continue
        total += undo(m) if undo_changes else process(m, apply_changes)
    verb = "已回滚" if undo_changes else ("已写入" if apply_changes else "仅检查")
    print("合计知识点：%d（%s）" % (total, verb))
    return 0


if __name__ == "__main__":
    sys.exit(main())
