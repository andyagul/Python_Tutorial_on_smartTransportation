#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
把 demos.py 中的 67 个随堂示例写入各章 md：

1. 真实执行每段示例代码，采集 stdout 作为「预期输出」（保证与代码逻辑一致）；
2. 在对应知识点的最后一个三级标题之后、下一个二级标题之前插入
   「### X.Y.4 随堂示例：标题 / 核心要点 / 代码 / 预期输出」；
3. 已插入过的知识点默认跳过；加 --refresh 参数则原地替换为新内容
   （改完 demos.py 后用它刷新，不必手工删除旧块）。

用法：
    python3 insert_demos.py            # 只写入尚未插入的知识点
    python3 insert_demos.py --refresh  # 全部按 demos.py 重建（覆盖已有块）
"""

import os
import re
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from demos import DEMOS  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def run_demo(code, cwd):
    """执行示例代码，返回 (成功, 输出或错误信息)"""
    proc = subprocess.run(
        [sys.executable, "-c", code],
        cwd=cwd, capture_output=True, text=True, timeout=60,
    )
    if proc.returncode != 0:
        return False, proc.stderr.strip()
    return True, proc.stdout.rstrip("\n")


def build_block(demo, output):
    fence_id = "demo" + demo["kp"].replace(".", "-")
    head = [
        "### %s.4 随堂示例：%s" % (demo["sec"], demo["title"]),
        "",
        "**核心要点**：%s" % demo["point"],
        "",
        "```python " + fence_id,
    ]
    body = demo["code"].rstrip("\n").split("\n")
    tail = ["```", "", "**预期输出**：", "", "```text"]
    out = output.split("\n")
    return head + body + tail + out + ["```"]


def insert(md_path, demo, block, refresh=False):
    with open(md_path, encoding="utf-8") as f:
        lines = f.read().split("\n")

    head_pat = "## %s 知识点 %s" % (demo["sec"], demo["kp"])
    idx = next((i for i, l in enumerate(lines) if l.startswith(head_pat)), None)
    if idx is None:
        return False, "未找到知识点标题：" + head_pat

    # 该知识点所在的二级标题范围：[idx, section_end)，围栏内的 "#" 注释不算标题
    section_end = idx + 1
    in_fence = False
    while section_end < len(lines):
        line = lines[section_end]
        if line.startswith("```"):
            in_fence = not in_fence
        elif not in_fence and re.match(r"^#{1,2} ", line):
            break
        section_end += 1

    demo_pat = "### %s.4 随堂示例" % demo["sec"]
    old_start = next((i for i in range(idx, section_end)
                      if lines[i].startswith(demo_pat)), None)

    if old_start is not None:
        if not refresh:
            return False, "已存在随堂示例，跳过"
        old_end = old_start + 1
        in_fence = False
        while old_end < len(lines):
            line = lines[old_end]
            if line.startswith("```"):
                in_fence = not in_fence
            elif not in_fence and re.match(r"^#{1,3} ", line):
                break
            old_end += 1
        new = lines[:old_start] + block + [""] + lines[old_end:]
        with open(md_path, "w", encoding="utf-8") as f:
            f.write("\n".join(new))
        return True, "已刷新"

    # 插入点：段末（回退掉尾部空行）
    k = section_end
    while k - 1 > idx and lines[k - 1].strip() == "":
        k -= 1
    new = lines[:k] + [""] + block + [""] + lines[section_end:]
    with open(md_path, "w", encoding="utf-8") as f:
        f.write("\n".join(new))
    return True, "ok"


def main():
    refresh = "--refresh" in sys.argv
    stats = {}
    failures = []
    created = set()

    for demo in DEMOS:
        folder = demo["ch"]
        cwd = os.path.join(ROOT, folder)
        ok, output = run_demo(demo["code"], cwd)
        if not ok:
            failures.append((demo["ch"], demo["kp"], output))
            continue

        # 记录示例运行产生的临时文件，跑完统一清理
        for f in os.listdir(cwd):
            if f.startswith("demo8"):
                created.add(os.path.join(cwd, f))

        block = build_block(demo, output)
        md = os.path.join(cwd, "案例与练习.md")
        inserted, msg = insert(md, demo, block, refresh=refresh)
        stats.setdefault(folder, {"ok": 0, "skip": 0})
        stats[folder]["ok" if inserted else "skip"] += 1
        if not inserted and msg != "已存在随堂示例，跳过":
            failures.append((folder, demo["kp"], msg))

    print("=" * 60)
    for folder, s in stats.items():
        print("%-24s 写入 %d 个 / 跳过 %d 个" % (folder, s["ok"], s["skip"]))

    total = sum(s["ok"] for s in stats.values())
    print("合计写入：%d 个随堂示例%s" % (total, "（refresh 模式）" if refresh else ""))

    for f in sorted(created):
        os.remove(f)
    if created:
        print("已清理示例产生的临时文件 %d 个" % len(created))

    if failures:
        print("\n失败项：")
        for ch, kp, msg in failures:
            print("  %s 知识点 %s：%s" % (ch, kp, msg[:300]))
        sys.exit(1)


if __name__ == "__main__":
    main()
