#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
把教材 md 中的 ```python 文件名.py 代码块内容同步为磁盘 .py 文件的真实内容。

用途：先改 .py（补注释、调格式），再一键同步到 md，避免"文档代码"与"可运行代码"两处不一致。
说明：
- 只处理 ```python <文件名> 形式的围栏，其余围栏（text / csv / 无标注）原样保留；
- 第 10 章的 ```python %%writefile 路径 形式，会保留首行魔术命令，其余内容取自同名文件；
- 找不到对应 .py 的代码块会跳过并提示。
"""

import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

CHAPTERS = [
    "01初识Python世界", "02变量与数据类型", "03流程控制", "04字符串与输入输出",
    "05列表元组集合与字典", "05A_Trae调试功能", "06函数", "07高级函数", "08文件操作",
    "09异常处理", "10模块与程序包", "11面向对象编程上", "12面向对象编程下", "13综合项目实战",
]

FENCE_OPEN = re.compile(r"^```python\s+(\S.*?)\s*$")


def sync_md(md_path, folder):
    with open(md_path, encoding="utf-8") as f:
        lines = f.read().split("\n")

    out, i, changed, missing = [], 0, 0, []
    while i < len(lines):
        m = FENCE_OPEN.match(lines[i])
        if not m:
            out.append(lines[i])
            i += 1
            continue

        target = m.group(1)
        if target.startswith("demo"):            # 随堂示例：不是磁盘文件，原样保留
            j = i + 1
            while j < len(lines) and not lines[j].startswith("```"):
                j += 1
            out.extend(lines[i:j + 1])
            i = j + 1
            continue

        # 收集原代码块（用于比较与容错）
        j = i + 1
        old_body = []
        while j < len(lines) and not lines[j].startswith("```"):
            old_body.append(lines[j])
            j += 1
        if j >= len(lines):                      # 未闭合，原样保留
            out.extend(lines[i:])
            break

        if target.startswith("%%writefile "):
            rel = target[len("%%writefile "):].strip()
        else:
            rel = target

        path = os.path.join(ROOT, folder, rel)
        if not os.path.exists(path):
            missing.append(rel)
            out.extend(lines[i:j + 1])
            i = j + 1
            continue

        with open(path, encoding="utf-8") as f:
            code = f.read().rstrip("\n")

        # 注意：md 代码块内不写 %%writefile 魔术行，该行由 build_notebooks.py 在生成
        # notebook 时自动补上；若此处重复写入，notebook 中会出现两行魔术命令。
        new_body = code.split("\n")
        if new_body != old_body:
            changed += 1
            out.append(lines[i])
            out.extend(new_body)
            out.append("```")
        else:
            out.extend(lines[i:j + 1])
        i = j + 1

    with open(md_path, "w", encoding="utf-8") as f:
        f.write("\n".join(out))

    tag = "已同步 %d 个代码块" % changed
    if missing:
        tag += "；⚠️ 缺少文件：" + "、".join(missing)
    print("%-22s %s" % (folder, tag))


def main():
    for folder in CHAPTERS:
        md = os.path.join(ROOT, folder, "案例与练习.md")
        if os.path.exists(md):
            sync_md(md, folder)


if __name__ == "__main__":
    main()
