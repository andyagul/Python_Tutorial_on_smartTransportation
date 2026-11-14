#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
课件构建脚本：把各章的「案例与练习.md」统一转成同构 Jupyter Notebook。

约定（写 md 时必须遵守）：
1. 代码块围栏写 ```python 文件名.py  → 生成一个 code cell，且与同名 .py 文件内容一致；
2. 若文件名写作 ```python %%writefile 路径 → 生成带 %%writefile 魔术命令的 code cell（第 10 章用）；
3. 其他围栏（```text、```、```csv）原样留在 markdown cell 内，作为「运行结果」等示例；
4. markdown cell 在 # / ## / ### / #### 标题处切分，便于逐节讲解。

用法：python3 build_notebooks.py [章节目录名...]
"""

import hashlib
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

CHAPTERS = [
    ("01初识Python世界", "01_初识Python世界.ipynb"),
    ("02变量与数据类型", "02_变量与数据类型.ipynb"),
    ("03流程控制", "03_流程控制.ipynb"),
    ("04字符串与输入输出", "04_字符串与输入输出.ipynb"),
    ("05列表元组集合与字典", "05_列表元组集合与字典.ipynb"),
    ("05A_Trae调试功能", "05A_Trae调试功能.ipynb"),
    ("06函数", "06_函数.ipynb"),
    ("07高级函数", "07_高级函数.ipynb"),
    ("08文件操作", "08_文件操作.ipynb"),
    ("09异常处理", "09_异常处理.ipynb"),
    ("10模块与程序包", "10_模块与程序包.ipynb"),
    ("11面向对象编程上", "11_面向对象编程上.ipynb"),
    ("12面向对象编程下", "12_面向对象编程下.ipynb"),
    ("13综合项目实战", "13_综合项目实战.ipynb"),
    ("14本地AI应用前置技能", "14_本地AI应用前置技能.ipynb"),
    ("15本地AI综合实战", "15_本地AI综合实战.ipynb"),
    ("99终结性考核", "99_终结性考核.ipynb"),
]

CODE_FENCE = re.compile(r"^```python\s+(.+?)\s*$")
HEADING = re.compile(r"^#{1,4} ")


def md_cell(text):
    lines = text.strip("\n").split("\n")
    if not lines or (len(lines) == 1 and lines[0].strip() == ""):
        return None
    src = [l + "\n" for l in lines[:-1]] + [lines[-1]]
    return {"cell_type": "markdown", "metadata": {}, "source": src}


def code_cell(src, filename):
    lines = src.rstrip("\n").split("\n")
    cell_src = [l + "\n" for l in lines[:-1]] + [lines[-1]]
    cell = {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": cell_src,
    }
    cell["metadata"]["source_file"] = filename
    return cell


def parse(md_text, out_cells, problems):
    lines = md_text.split("\n")
    i = 0
    buf = []
    in_fence = False

    def flush(force=False):
        if not buf:
            return
        # 结尾的孤立围栏（未闭合）需报错
        cell = md_cell("\n".join(buf))
        if cell:
            out_cells.append(cell)
        buf.clear()

    while i < len(lines):
        line = lines[i]

        if not in_fence:
            m = CODE_FENCE.match(line)
            if m:
                flush()
                filename = m.group(1).strip()
                body = []
                i += 1
                while i < len(lines) and not lines[i].startswith("```"):
                    body.append(lines[i])
                    i += 1
                if i >= len(lines):
                    problems.append("代码块未闭合：%s" % filename)
                if filename.startswith("%%writefile "):
                    path = filename[len("%%writefile "):].strip()
                    cell = code_cell("%%writefile " + path + "\n" + "\n".join(body), path)
                    cell["metadata"]["writefile"] = True
                elif filename.startswith("demo"):
                    # 随堂示例：围栏标注 demo<知识点号>，只作为可直接运行的单元，
                    # 不对应磁盘文件，因此不做「与 .py 一致」校验。
                    cell = code_cell("\n".join(body), filename)
                    cell["metadata"].pop("source_file", None)
                    cell["metadata"]["demo"] = filename[len("demo"):].replace("-", ".")
                else:
                    cell = code_cell("\n".join(body), filename)
                out_cells.append(cell)
                i += 1  # 跳过闭合围栏
                continue

            # 普通围栏（非 python 文件名）：整体留在 markdown
            if line.startswith("```"):
                buf.append(line)
                i += 1
                while i < len(lines):
                    buf.append(lines[i])
                    if lines[i].startswith("```"):
                        i += 1
                        break
                    i += 1
                continue

            if HEADING.match(line):
                flush()
                buf.append(line)
                i += 1
                continue

            buf.append(line)
            i += 1
        else:
            buf.append(line)
            i += 1

    flush()


def title_of(folder):
    """文件夹名 -> 章节标题：01初识Python世界 -> 初识Python世界，05A_Trae调试功能 -> Trae调试功能"""
    return re.sub(r"^\d+[A-Za-z]?_?", "", folder)


def nav_cell(idx):
    prev_link = "◀ 上一章"
    prev_dir = None
    prev_nb = None
    if idx > 0:
        prev_dir, prev_nb = CHAPTERS[idx - 1]
        prev_link = "◀ 上一章：%s" % title_of(prev_dir)
    nxt = "下一章 ▶"
    nxt_dir = None
    nxt_nb = None
    if idx + 1 < len(CHAPTERS):
        nxt_dir, nxt_nb = CHAPTERS[idx + 1]
        nxt = "下一章：%s ▶" % title_of(nxt_dir)

    parts = ["[🏠 课程首页](../00_课程索引.ipynb)"]
    if prev_dir:
        parts.append("&nbsp;&nbsp;|&nbsp;&nbsp;[%s](../%s/%s)" % (prev_link, prev_dir, prev_nb))
    if nxt_dir:
        parts.append("&nbsp;&nbsp;|&nbsp;&nbsp;[%s](../%s/%s)" % (nxt, nxt_dir, nxt_nb))
    text = "---\n\n" + "".join(parts)
    return md_cell(text)


def old_cell_ids(out):
    """返回 (文件是否存在, 既有单元格 id 列表)。

    既有 notebook 若本来就带 id，重建时按位置复用；若本来没有 id（早期文件），
    保持原样不加，避免重建产生大面积无意义 diff。
    """
    if not os.path.exists(out):
        return False, []
    try:
        with open(out, encoding="utf-8") as f:
            old = json.load(f)
        ids = [c.get("id") for c in old.get("cells", [])]
        return (any(ids), ids)
    except Exception:
        return False, []


def build(idx):
    folder, nb_name = CHAPTERS[idx]
    md_path = os.path.join(ROOT, folder, "案例与练习.md")
    if not os.path.exists(md_path):
        md_path = os.path.join(ROOT, folder, "终结性考核题目与参考答案.md")
    with open(md_path, encoding="utf-8") as f:
        md_text = f.read()

    cells, problems = [], []
    parse(md_text, cells, problems)

    nav = nav_cell(idx)
    if nav:
        cells.append(nav)

    # nbformat 4.5 要求每个单元格有唯一 id：新文件生成，旧文件有则复用、无则不加；
    # id 插在 metadata 之前，与既有 notebook 的键顺序保持一致，避免重建产生无意义 diff
    out = os.path.join(ROOT, folder, nb_name)
    need_id, reused = old_cell_ids(out)
    if not os.path.exists(out):
        need_id = True
    if need_id:
        ordered = []
        for i, c in enumerate(cells):
            cid = reused[i] if i < len(reused) and reused[i] else \
                hashlib.md5(("%s-%d-%s" % (folder, i, c["cell_type"])).encode("utf-8")).hexdigest()[:8]
            new = {}
            for k, v in c.items():
                if k == "metadata":
                    new["id"] = cid
                new[k] = v
            new.setdefault("id", cid)
            ordered.append(new)
        cells = ordered

    nb = {
        "cells": cells,
        "metadata": {
            "kernelspec": {"display_name": "Python 3 (ipykernel)", "language": "python", "name": "python3"},
            "language_info": {
                "name": "python",
                "version": "3.13.12",
                "mimetype": "text/x-python",
                "file_extension": ".py",
                "pygments_lexer": "ipython3",
                "codemirror_mode": {"name": "ipython", "version": 3},
                "nbconvert_exporter": "python",
            },
        },
        "nbformat": 4,
        "nbformat_minor": 5,
    }

    out = os.path.join(ROOT, folder, nb_name)
    with open(out, "w", encoding="utf-8") as f:
        json.dump(nb, f, ensure_ascii=False, indent=1)
        f.write("\n")
    n_md = sum(1 for c in cells if c["cell_type"] == "markdown")
    n_code = sum(1 for c in cells if c["cell_type"] == "code")
    print("✅ %-22s cells=%d (md %d / code %d)%s" % (folder, len(cells), n_md, n_code,
          ("  ⚠️ " + ";".join(problems)) if problems else ""))
    return cells


def check_code(cells):
    """校验 code cell 与磁盘 .py 文件一致，返回不一致清单"""
    bad = []
    for c in cells:
        if c["cell_type"] != "code":
            continue
        if c["metadata"].get("demo"):        # 随堂示例没有对应磁盘文件
            continue
        name = c["metadata"].get("source_file", "")
        src = "".join(c["source"])
        if c["metadata"].get("writefile"):
            path = os.path.join(ROOT, CUR_FOLDER, name)
            src = src.split("\n", 1)[1] if "\n" in src else ""
        else:
            path = os.path.join(ROOT, CUR_FOLDER, name)
        if not os.path.exists(path):
            bad.append("%s 不存在" % name)
            continue
        with open(path, encoding="utf-8") as f:
            disk = f.read()
        if disk.rstrip("\n") != src.rstrip("\n"):
            bad.append("%s 与磁盘内容不一致" % name)
    return bad


if __name__ == "__main__":
    targets = sys.argv[1:]
    idxs = [i for i, (f, _) in enumerate(CHAPTERS) if not targets or f in targets]
    for i in idxs:
        CUR_FOLDER = CHAPTERS[i][0]
        cells = build(i)
        bad = check_code(cells)
        if bad:
            print("   ⚠️ 代码校验：", "; ".join(bad))
