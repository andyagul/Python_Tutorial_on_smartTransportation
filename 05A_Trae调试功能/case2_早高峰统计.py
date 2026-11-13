# ---------- 第 05A 节 · 案例 5A-2：早高峰断面统计与告警（含 4 个预设 bug）----------
# 对应知识点：5A.2 逐过程、5A.3 步入、5A.5 变量与监视、5A.7 条件断点
# 数据结构：records 每条为元组 (车牌, 断面, 平均行程车速 km/h)，同一车牌可能被多次检测
# 判定标准：
#   1) 断面平均车速应在 30~60 km/h 之间，与记录里的单车车速同量级；
#   2) 平均车速 < 40 判"拥堵"，40~59 判"缓行"，≥ 60 判"畅通"；
#   3) 涉及车辆数按车牌去重后统计。

records = [
    ("京A12345", "京港澳", 48),
    ("京B67890", "京港澳", 42),
    ("京A12345", "京港澳", 51),
    ("津C24680", "京港澳", 39),
    ("京E11223", "京开", 62),
    ("京F33445", "京开", 58),
    ("京G55667", "机场", 35),
    ("京G55667", "机场", 38),
    ("京H77889", "机场", 33),
]


def avg_speed(speeds):
    """断面平均行程车速（km/h）"""
    return round(sum(speeds) / len(records), 1)


count = {}
speeds = {}
for i in range(len(records)):
    plate = records[i][0]
    road = records[i][1]
    count[road] = count.get(road, 0) + 1
    speeds[road] = [records[i][2]]

print("断面数：", len(count), "| 采样记录：", len(records), "条")
print("-" * 40)

for road in count:
    avg = avg_speed(speeds[road])
    if avg < 60:
        level = "缓行"
    elif avg < 40:
        level = "拥堵"
    else:
        level = "畅通"
    print(road, "→ 平均", avg, "km/h |", count[road], "条记录 |", level)

print("-" * 40)
plates = []
for i in range(len(records)):
    plates.append(records[i][0])
print("涉及车辆数：", len(records), "辆（含重复检测）")

fast = [records[i][0] for i in range(len(records)) if records[i][2] > 60]
print("车速高于 60 km/h 的车辆：", fast, "共", len(fast), "辆")
