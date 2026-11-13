# ---------- 第 05A 节 · 练习 5A-2：分断面告警报表（含 4 个预设 bug，独立完成）----------
# 数据结构：records 每条为元组 (车牌, 断面, 行程车速 km/h)
# 判定标准：
#   1) 断面名称必须完整保留（"机场北"与"机场南"是两个断面，不能合并）；
#   2) 平均车速 = 该断面各条记录车速之和 ÷ 该断面记录条数；
#   3) 平均车速 < 40 判"拥堵"，40~59 判"缓行"，≥ 60 判"畅通"；
#   4) 低速清单收录车速 < 35 km/h 的车辆（不含 35）。
# 现象：机场两个断面被合成一条；京开平均车速只有 40.0；机场北、机场南都显示"缓行"；
#       低速清单里多了一辆 35 km/h 的车。请逐个定位。

records = [
    ("京A12345", "京港澳", 48),
    ("京B67890", "京港澳", 41),
    ("津C24680", "京港澳", 52),
    ("京E11223", "京开", 63),
    ("京F33445", "京开", 57),
    ("京G55667", "机场北", 36),
    ("京H77889", "机场北", 35),
    ("京J99001", "机场南", 29),
    ("京K22110", "机场南", 31),
]

roads = {}
for i in range(len(records)):
    road = records[i][1][:2]
    if road not in roads:
        roads[road] = []
    roads[road].append(records[i][2])

print("-" * 40)

for road in roads:
    speed_list = roads[road]
    avg = round(sum(speed_list) / 3, 1)
    if avg < 60:
        level = "缓行"
    elif avg < 40:
        level = "拥堵"
    else:
        level = "畅通"
    print(road, "→ 平均", avg, "km/h |", len(speed_list), "条 |", level)

print("-" * 40)
slow = []
for i in range(len(records)):
    if records[i][2] <= 35:
        slow.append(records[i][0])
print("低速车辆（< 35 km/h）：", slow, "共", len(slow), "辆")

print("涉及断面：", list(roads.keys()))
