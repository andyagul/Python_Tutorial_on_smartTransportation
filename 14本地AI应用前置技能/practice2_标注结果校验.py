# -*- coding: utf-8 -*-
"""练习 14-2：模型标注结果的解析、字段校验与落盘。

当前代码可以运行，但有 2 处统计口径问题，请按《案例与练习.md》练习 14-2
的题目要求修正，使输出与第四部分参考答案一致。
"""
import json

RAW = [
    '{"road": "机场北", "level": "拥堵", "avg_speed": 35.5}',
    '{"road": "京开", "level": "畅通", "avg_speed": 60.0}',
    '{"road": "机场南", "avg_speed": 30.0}',
    '{"road": "机场北", "level": "严重拥堵", "avg_speed": 25.0}',
    '{"road": "机场北", "level": "缓行",',
]
REQUIRED = ["road", "level", "avg_speed"]
LEVELS = ["畅通", "缓行", "拥堵"]

valid, invalid = [], []
for i, text in enumerate(RAW, 1):
    try:
        data = json.loads(text)
    except json.JSONDecodeError:
        print("样本", i, "：JSON 解析失败，已跳过")
        # 口径问题 1：不合格样本没有记入 invalid
        continue
    missing = [k for k in REQUIRED if k not in data]
    if missing:
        print("样本", i, "：缺字段", missing)
        # 口径问题 1：不合格样本没有记入 invalid
        continue
    if data["level"] not in LEVELS:
        print("样本", i, "：level 非法", data["level"])
        # 口径问题 1：不合格样本没有记入 invalid
        continue
    valid.append(data)

print("合格条数：", len(valid))
print("不合格条数：", len(invalid))
# 口径问题 2：分母用了合格条数，而不是样本总数
print("合格率：", round(len(valid) / len(valid) * 100, 1), "%")
