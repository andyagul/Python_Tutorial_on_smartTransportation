# -*- coding: utf-8 -*-
"""练习 15-1 参考答案：标注结果置信度过滤（口径修正版）。

修正点：
1. 阈值改为 >= 0.70，边界样本 f.png 应保留；剔除清单同步改为 < 阈值；
2. 合格率分母改为总记录数 len(ROWS)。
"""
from collections import Counter

ROWS = [
    {"file": "a.png", "level": "拥堵", "confidence": 0.93},
    {"file": "b.png", "level": "缓行", "confidence": 0.80},
    {"file": "c.png", "level": "拥堵", "confidence": 0.55},
    {"file": "d.png", "level": "畅通", "confidence": 0.72},
    {"file": "e.png", "level": "拥堵", "confidence": 0.41},
    {"file": "f.png", "level": "缓行", "confidence": 0.70},
]
THRESHOLD = 0.70

print("总记录：", len(ROWS))
print("过滤阈值： >=", THRESHOLD)
kept = [r for r in ROWS if r["confidence"] >= THRESHOLD]
dropped = [r["file"] for r in ROWS if r["confidence"] < THRESHOLD]
print("保留记录：", len(kept))
print("剔除记录：", dropped)
print("保留等级分布：", dict(Counter(r["level"] for r in kept)))
print("合格率：", round(len(kept) / len(ROWS) * 100, 1), "%")
