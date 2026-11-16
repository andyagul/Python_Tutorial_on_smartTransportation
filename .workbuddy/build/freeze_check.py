#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""只读基线工具：采集/比对讲义中的冻结对象。

冻结对象：
1. 全部围栏行（``` 开头，含 info string），按出现顺序；
2. 每个 python 围栏体的 SHA-256，按出现顺序；
3. 代码围栏外的花括号 token 多重集合；
4. 代码围栏外的全角方括号槽位多重集合；
5. 知识点节号、案例/练习/答案编号清单。

用法：
  python3 freeze_check.py --capture --out .workbuddy/build/freeze_baseline.json
  python3 freeze_check.py --compare --baseline .workbuddy/build/freeze_baseline.json
"""

import argparse
import hashlib
import json
import os
import re
import sys
from collections import Counter

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

CHAPTERS = [
    "01初识Python世界", "02变量与数据类型", "03流程控制", "04字符串与输入输出",
    "05列表元组集合与字典", "05A_Trae调试功能", "06函数", "07高级函数", "08文件操作",
    "09异常处理", "10模块与程序包", "11面向对象编程上", "12面向对象编程下", "13综合项目实战",
    "14本地AI应用前置技能", "15本地AI综合实战",
]

BRACE = re.compile(r"\{[^{}\n]{0,80}\}")
FULLWIDTH = re.compile(r"【[^】\n]{0,40}】")
HEAD_NUM = re.compile(r"^(#{2,3}) ((?:[\dA-Z]+\.)+[\dA-Z]+|案例 [\dA-Z]+-\d+|练习 [\dA-Z]+-\d+|答案 [\dA-Z]+-\d+)")


def scan(md_path):
    with open(md_path, encoding="utf-8") as f:
        lines = f.read().split("\n")

    fences, bodies, braces, fullwidth, numbers = [], [], [], [], []
    inside = False
    info = ""
    body = []

    for line in lines:
        if not inside:
            if line.startswith("```"):
                fences.append(line)
                info = line[3:].strip()
                body = []
                inside = True
            else:
                braces.extend(BRACE.findall(line))
                fullwidth.extend(FULLWIDTH.findall(line))
                m = HEAD_NUM.match(line)
                if m:
                    numbers.append(m.group(2))
        else:
            if line.startswith("```"):
                inside = False
                if info.split(" ")[0] == "python":
                    bodies.append(hashlib.sha256("\n".join(body).encode("utf-8")).hexdigest())
            else:
                body.append(line)

    return {
        "fences": fences,
        "python_body_sha256": bodies,
        "braces": dict(sorted(Counter(braces).items())),
        "fullwidth": dict(sorted(Counter(fullwidth).items())),
        "numbers": numbers,
    }


def capture(out_path):
    data = {}
    for folder in CHAPTERS:
        md = os.path.join(ROOT, folder, "案例与练习.md")
        data[folder] = scan(md)
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=1, sort_keys=True)
        f.write("\n")
    print("已采集 %d 份讲义 → %s" % (len(data), out_path))


def compare(baseline_path):
    with open(baseline_path, encoding="utf-8") as f:
        base = json.load(f)

    diffs = []
    for folder in CHAPTERS:
        md = os.path.join(ROOT, folder, "案例与练习.md")
        now = scan(md)
        old = base.get(folder)
        if old is None:
            diffs.append("%s：基线缺失" % folder)
            continue
        for key in ("fences", "python_body_sha256", "numbers"):
            old_c, new_c = Counter(old[key]), Counter(now[key])
            if old_c != new_c:
                added = sorted((new_c - old_c).elements())
                removed = sorted((old_c - new_c).elements())
                diffs.append("%s：%s 变化，新增 %s，缺失 %s"
                             % (folder, key, added[:20], removed[:20]))
        for key in ("braces", "fullwidth"):
            if now[key] != old[key]:
                old_set, new_set = set(old[key]), set(now[key])
                added = sorted(new_set - old_set)
                removed = sorted(old_set - new_set)
                diffs.append("%s：%s 变化，新增 %s，缺失 %s"
                             % (folder, key, added[:20], removed[:20]))
    if diffs:
        print("冻结对象差异：%d 项" % len(diffs))
        for d in diffs:
            print(" -", d)
        return 1
    print("冻结对象无差异：%d 份讲义全部一致" % len(CHAPTERS))
    return 0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--capture", action="store_true")
    ap.add_argument("--compare", action="store_true")
    ap.add_argument("--out", default=os.path.join(ROOT, ".workbuddy", "build", "freeze_baseline.json"))
    ap.add_argument("--baseline", default=os.path.join(ROOT, ".workbuddy", "build", "freeze_baseline.json"))
    args = ap.parse_args()

    if args.capture:
        capture(args.out)
    elif args.compare:
        sys.exit(compare(args.baseline))
    else:
        ap.print_help()


if __name__ == "__main__":
    main()
