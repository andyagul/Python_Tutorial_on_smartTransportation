# -*- coding: utf-8 -*-
"""练习 14-2 参考答案：模型标注结果的解析、字段校验与落盘（口径修正版）。

修正点：
1. 三类不合格样本（解析失败 / 缺字段 / 取值非法）统一记入 invalid；
2. 合格率分母改为样本总数 len(RAW)，并把合格记录序列化为 JSON 供落盘。
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
        invalid.append(i)
        continue
    missing = [k for k in REQUIRED if k not in data]
    if missing:
        print("样本", i, "：缺字段", missing)
        invalid.append(i)
        continue
    if data["level"] not in LEVELS:
        print("样本", i, "：level 非法", data["level"])
        invalid.append(i)
        continue
    valid.append(data)

print("合格条数：", len(valid))
print("不合格条数：", len(invalid))
print("合格率：", round(len(valid) / len(RAW) * 100, 1), "%")
saved = json.dumps(valid, ensure_ascii=False)
print("落盘 JSON 条数：", len(json.loads(saved)))
print("合格记录：", [(d["road"], d["level"], d["avg_speed"]) for d in valid])
