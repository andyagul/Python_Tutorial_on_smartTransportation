#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""交付前校验：notebook 中的随堂示例是否「可运行且输出与文档一致」。"""

import glob
import json
import os
import re
import subprocess
import sys

ROOT = "/Users/waiyu/Library/Mobile Documents/com~apple~CloudDocs/Work/系部工作/专项分类/智能网联汽车技术应用/Python/Python_Tutorial_on_smartTransportation"


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
        demos = [c for c in cells if c.get("metadata", {}).get("demo")]
        for i, c in enumerate(cells):
            if not c.get("metadata", {}).get("demo"):
                continue
            kp = c["metadata"]["demo"]
            total += 1
            code = "".join(c["source"])
            nxt = cells[i + 1] if i + 1 < len(cells) else None
            expected = doc_output("".join(nxt["source"])) if nxt and nxt["cell_type"] == "markdown" else None
            if expected is None:
                problems.append("%s 知识点 %s：缺少「预期输出」块" % (os.path.basename(chapter_dir), kp))
                continue
            p = subprocess.run([sys.executable, "-c", code], cwd=chapter_dir,
                               capture_output=True, text=True, timeout=90)
            if p.returncode != 0:
                problems.append("%s 知识点 %s：运行报错 %s" % (os.path.basename(chapter_dir), kp,
                                                              p.stderr.strip().split("\n")[-1][:120]))
                continue
            actual = p.stdout.rstrip("\n")
            if actual != expected:
                problems.append("%s 知识点 %s：输出与文档不一致\n  文档：%r\n  实际：%r"
                                % (os.path.basename(chapter_dir), kp, expected[:200], actual[:200]))
                continue
            ok += 1
    print("随堂示例总数：%d，通过：%d，问题：%d" % (total, ok, len(problems)))
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
