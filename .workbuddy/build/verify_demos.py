#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""交付前校验：notebook 中的示例是否「可运行且输出与文档一致」。

两类都校验：
1. 内联示例（围栏 demo<知识点号>，单元格 metadata 带 demo）：比对紧随其后的「预期输出」块；
   - 随堂示例 demoX-Y（81 个）、变式示例 demoX-Yb（88 个，其中 74 个为知识点体系优化新增）；
2. 文件型示例与练习：执行 .py 文件，比对紧随其后的「运行结果」块。
   - 05A 节：文件名形如 示例5A1_xxx.py、练习5A2_xxx.py（14 个）；
   - 第 14/15 章：文件名形如 case1_xxx.py、practice1_xxx.py、practice1_xxx_答案.py（12 个）
     （这两章的主程序默认走离线演示模式，输出可逐字复现，故同样纳入校验）。

当前全量：169 个内联 + 26 个文件型 = 195 条。
"""

import glob
import json
import os
import re
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# 05A 节文件型示例 / 练习
FILE_DEMO = re.compile(r"^(示例|练习)5A\d")
# 第 14/15 章文件型案例、练习与参考答案
AI_CHAPTER = re.compile(r"^1[45]")
AI_FILE_DEMO = re.compile(r"^(case|practice)\d")


def doc_output(md_src):
    m = re.search(r"```text\n(.*?)\n```", md_src, re.S)
    return m.group(1) if m else None


def main():
    total = ok = 0
    problems = []
    for nb_path in sorted(glob.glob(os.path.join(ROOT, "*", "*.ipynb"))):
        nb = json.load(open(nb_path, encoding="utf-8"))
        cells = nb["cells"]
        chapter_dir = os.path.dirname(nb_path)
        is_ai_chapter = bool(AI_CHAPTER.match(os.path.basename(chapter_dir)))
        for i, c in enumerate(cells):
            if c["cell_type"] != "code":
                continue
            meta = c.get("metadata", {})
            kp = meta.get("demo")
            src_file = meta.get("source_file", "")
            is_file_demo = bool(FILE_DEMO.match(src_file)) or (
                is_ai_chapter and bool(AI_FILE_DEMO.match(src_file)))
            if not kp and not is_file_demo:
                continue
            label = "知识点 %s" % kp if kp else src_file
            total += 1
            nxt = cells[i + 1] if i + 1 < len(cells) else None
            expected = doc_output("".join(nxt["source"])) if nxt and nxt["cell_type"] == "markdown" else None
            if expected is None:
                problems.append("%s %s：缺少「预期输出 / 运行结果」块" % (os.path.basename(chapter_dir), label))
                continue

            if is_file_demo:                       # 直接跑磁盘文件，顺带验证讲义与文件同源
                cmd = [sys.executable, src_file]
                code = None
            else:
                cmd = [sys.executable, "-c", "".join(c["source"])]
                code = True
            p = subprocess.run(cmd, cwd=chapter_dir, capture_output=True, text=True, timeout=90)
            if p.returncode != 0:
                problems.append("%s %s：运行报错 %s" % (os.path.basename(chapter_dir), label,
                                                       p.stderr.strip().split("\n")[-1][:120]))
                continue
            actual = p.stdout.rstrip("\n")
            if actual != expected:
                problems.append("%s %s：输出与文档不一致\n  文档：%r\n  实际：%r"
                                % (os.path.basename(chapter_dir), label, expected[:200], actual[:200]))
                continue
            ok += 1
    print("示例总数：%d（含文件型示例/练习），通过：%d，问题：%d" % (total, ok, len(problems)))
    for x in problems:
        print(" -", x)

    # 清理第 8 章示例运行留下的临时文件
    cleaned = 0
    for f in glob.glob(os.path.join(ROOT, "08文件操作", "demo8*")):
        os.remove(f)
        cleaned += 1
    if cleaned:
        print("已清理第 8 章示例临时文件 %d 个" % cleaned)
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
