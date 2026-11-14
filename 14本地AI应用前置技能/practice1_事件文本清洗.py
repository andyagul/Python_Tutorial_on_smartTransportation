# -*- coding: utf-8 -*-
"""练习 14-1：交通事件文本清洗与词频统计。

当前代码可以运行，但有 2 处统计口径问题，请按《案例与练习.md》练习 14-1
的题目要求修正，使输出与第四部分参考答案一致。
"""
import csv
import io
import re
from collections import Counter

EVENTS = [
    "08:12 京A12345 机场北 追尾 车速35km/h",
    "08:15 京B67890 机场北 拥堵 车速30km/h",
    "08:21 京C11122 京开 缓行 车速48km/h",
    "08:33 京D33344 机场南 拥堵 车速25km/h",
    "08:40 京E55566 机场北 畅通 车速62km/h",
]
KEYWORDS = ["追尾", "拥堵", "缓行", "畅通"]
PLATE = re.compile(r"[\u4e00-\u9fa5][A-Z]\d{5}")
ROAD = re.compile(r"机场北|机场南|京开|京港澳")


def clean(lines):
    """把每条自由文本拆成结构化字典。"""
    rows = []
    for line in lines:
        plate = PLATE.search(line)
        time = re.search(r"\d{2}:\d{2}", line)
        speed = re.search(r"(\d+)\s*km/h", line)
        road = ROAD.search(line)
        rows.append({
            "时间": time.group() if time else "",
            "车牌": plate.group() if plate else "",
            "路段": road.group() if road else "",
            "车速": int(speed.group(1)) if speed else 0,
        })
    return rows


rows = clean(EVENTS)
print("清洗记录数：", len(rows))
print("首条：", rows[0]["时间"], rows[0]["车牌"], rows[0]["路段"], rows[0]["车速"])

out = io.StringIO()
w = csv.DictWriter(out, fieldnames=["时间", "车牌", "路段", "车速"], lineterminator="\n")
w.writeheader()
w.writerows(rows)
print("CSV 行数（含表头）：", len(out.getvalue().splitlines()))

counts = Counter()
for line in EVENTS:
    for k in KEYWORDS:
        if k in line:
            counts[k] += 1
print("关键词计数：", dict(counts))
print("关键词命中总数：", sum(counts.values()))

# 口径问题 1：直接拿记录条数当「涉及路段数」，没有按路段去重
print("涉及路段数：", len(rows))

# 口径问题 2：低速阈值写成 <= 35，题目要求是 < 35
slow = [r["车牌"] for r in rows if r["车速"] <= 35]
print("低速车辆（<35）：", slow)
