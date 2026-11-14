# -*- coding: utf-8 -*-
"""练习 15-2 参考答案：事件分类分布与准确率统计（口径修正版）。

修正点：
1. 用 collections.Counter 按事件类型去重计数，并给出分布；
2. 准确率分母改为样本总数 len(PRED)。
"""
from collections import Counter

PRED = ["事故", "拥堵", "事故", "施工", "通行正常"]
TRUTH = ["事故", "拥堵", "事故", "施工", "拥堵"]

hits = sum(1 for p, t in zip(PRED, TRUTH) if p == t)
dist = Counter(PRED)
print("样本数：", len(PRED))
print("命中数：", hits)
print("事件类型数：", len(dist))
print("分布：", dist.most_common())
print("准确率：", round(hits / len(PRED) * 100, 1), "%")
