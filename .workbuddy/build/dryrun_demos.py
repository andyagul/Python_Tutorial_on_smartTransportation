#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""试运行 demos.py 中全部示例，打印输出并标注可疑之处（不写任何文件）。"""

import os
import re
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from demos import DEMOS  # noqa: E402

ROOT = "/Users/waiyu/Library/Mobile Documents/com~apple~CloudDocs/Work/系部工作/专项分类/智能网联汽车技术应用/Python/Python_Tutorial_on_smartTransportation"


def flags(out):
    f = []
    if not out.strip():
        f.append("空输出")
    if re.search(r"0x[0-9a-fA-F]{6,}", out):
        f.append("含内存地址")
    for ln in out.split("\n"):
        if ln != ln.rstrip():
            f.append("行尾空格:" + repr(ln))
            break
    if re.search(r"at 0x", out):
        f.append("对象表示")
    return f


def main():
    bad = 0
    for d in DEMOS:
        cwd = os.path.join(ROOT, d["ch"])
        p = subprocess.run([sys.executable, "-c", d["code"]], cwd=cwd,
                           capture_output=True, text=True, timeout=90)
        print("=" * 70)
        print("[%s] %s | %s" % (d["kp"], d["ch"], d["title"]))
        if p.returncode != 0:
            bad += 1
            print("!! 运行失败")
            print(p.stderr.strip()[:800])
            continue
        out = p.stdout.rstrip("\n")
        print("---- 输出 ----")
        print(out)
        fl = flags(out)
        if fl:
            bad += 1
            print("---- 标记 ----")
            print(" | ".join(fl))
    print("=" * 70)
    print("示例总数 %d，待关注 %d" % (len(DEMOS), bad))


if __name__ == "__main__":
    main()
