# -*- coding: utf-8 -*-
"""练习 14-1 参考答案：交通事件文本清洗与词频统计（口径修正版）。

修正点：
1. 涉及路段数改为对「路段」字段去重后计数（set）；
2. 低速车辆阈值由 <= 35 改为 < 35，边界车速 35km/h 不计入。
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

# 修正 1：先取出去重的路段集合，再计数
roads = [r["路段"] for r in rows if r["路段"]]
print("涉及路段数（去重）：", len(set(roads)), sorted(set(roads)))

# 修正 2：严格小于 35
slow = [r["车牌"] for r in rows if r["车速"] < 35]
print("低速车辆（<35）：", slow)
