# -*- coding: utf-8 -*-
"""练习 15-1：标注结果置信度过滤。

当前代码可以运行，但有 2 处统计口径问题，请按《案例与练习.md》练习 15-1
的题目要求修正，使输出与第四部分参考答案一致。
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
# 口径问题 1：题目要求「>= 阈值」，代码写成了严格大于
print("过滤阈值： >", THRESHOLD)
kept = [r for r in ROWS if r["confidence"] > THRESHOLD]
dropped = [r["file"] for r in ROWS if r["confidence"] <= THRESHOLD]
print("保留记录：", len(kept))
print("剔除记录：", dropped)
print("保留等级分布：", dict(Counter(r["level"] for r in kept)))
# 口径问题 2：合格率分母用了保留条数，而不是总记录数
print("合格率：", round(len(kept) / len(kept) * 100, 1), "%")
