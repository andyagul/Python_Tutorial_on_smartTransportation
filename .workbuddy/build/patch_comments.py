#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""为个别语句补充行内注释（不改动任何逻辑）。

每条替换都必须精确命中一次，否则脚本报错退出，便于发现教材与代码不同步。
"""

import os

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

PATCHES = [
    ("03流程控制/practice1_排队放行仿真.py",
     "while queue > 0:\n    minute += 1\n",
     "while queue > 0:              # 队列未清空就一直放行\n    minute += 1               # 计数写在循环体首行，避免从 0 分钟开始\n"),
    ("03流程控制/practice1_排队放行仿真.py",
     "    queue -= per_min\n    if queue < 0:\n        queue = 0\n",
     "    queue -= per_min          # 本分钟放行后剩余排队\n    if queue < 0:\n        queue = 0             # 防止出现负数排队\n"),
    ("03流程控制/practice2_车道占用网格.py",
     "for lane in range(1, lanes + 1):\n    line = \"\"\n    for slot in range(1, slots + 1):\n        if slot <= occupied:\n            line = line + \"[X]\"\n        else:\n            line = line + \"[ ]\"\n    print(\"第 \" + str(lane) + \" 车道：\" + line)\n",
     "for lane in range(1, lanes + 1):        # 外层：逐条车道\n    line = \"\"                           # 每换一条车道必须重置，否则上一行会累积进来\n    for slot in range(1, slots + 1):     # 内层：逐个车位拼接\n        if slot <= occupied:\n            line = line + \"[X]\"         # 已占用\n        else:\n            line = line + \"[ ]\"         # 空位\n    print(\"第 \" + str(lane) + \" 车道：\" + line)   # 内层结束后整行输出一次\n"),
    ("04字符串与输入输出/practice2_路段名检索.py",
     "if name.find(keyword) == -1:\n",
     "if name.find(keyword) == -1:      # find() 找不到时返回 -1，而不是抛异常\n"),
    ("05列表元组集合与字典/practice1_车流量统计.py",
     "morning = sum(flows[:4])\nevening = sum(flows[4:])\n",
     "morning = sum(flows[:4])          # 切片取前 4 个时段：早高峰\nevening = sum(flows[4:])          # 后 4 个时段：晚高峰\n"),
    ("05列表元组集合与字典/practice2_路况查询.py",
     "print(\"全部畅通：\", \"拥堵\" not in status.values() and \"缓行\" not in status.values())\n",
     "print(\"全部畅通：\", \"拥堵\" not in status.values() and \"缓行\" not in status.values())  # values() 取出所有状态值\n"),
    ("10模块与程序包/flow_stats.py",
     "def total(flows):\n    return sum(flows)\n",
     "def total(flows):\n    \"\"\"车流总量\"\"\"\n    return sum(flows)\n"),
    ("10模块与程序包/flow_stats.py",
     "def average(flows):\n",
     "def average(flows):\n    \"\"\"平均流量，保留 1 位小数；空列表返回 0\"\"\"\n"),
    ("10模块与程序包/flow_stats.py",
     "def peak_index(flows):\n",
     "def peak_index(flows):\n    \"\"\"峰值所在下标（从 0 开始）\"\"\"\n"),
    ("10模块与程序包/traffic_pkg/calc.py",
     "def capacity(lanes, per_lane=2200):\n",
     "def capacity(lanes, per_lane=2200):\n    \"\"\"理论通行能力（辆/h）\"\"\"\n"),
    ("10模块与程序包/traffic_pkg/calc.py",
     "def density(cars, length_km, lanes):\n",
     "def density(cars, length_km, lanes):\n    \"\"\"车流密度（辆/(km·车道)），保留 2 位小数\"\"\"\n"),
]


def main():
    ok = 0
    for rel, old, new in PATCHES:
        path = os.path.join(ROOT, rel)
        with open(path, encoding="utf-8") as f:
            text = f.read()
        n = text.count(old)
        if n != 1:
            print("⚠️ 命中 %d 次，跳过：%s" % (n, rel))
            continue
        with open(path, "w", encoding="utf-8") as f:
            f.write(text.replace(old, new, 1))
        ok += 1
    print("已补注释：%d 处" % ok)


if __name__ == "__main__":
    main()
