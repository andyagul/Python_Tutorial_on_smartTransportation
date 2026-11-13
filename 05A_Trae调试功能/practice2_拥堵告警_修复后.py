# ---------- 第 05A 节 · 练习 5A-2 参考答案：分断面告警报表（4 处 bug 已修复）----------
# 对应知识点：5A.5 变量与监视、5A.6 调用堆栈、5A.7 条件断点、第 5 章字典与集合去重
# 修复点：
#   ① 分组键 records[i][1][:2] 截断了断面名 → 改用完整名称 records[i][1]；
#   ② 平均车速分母写成常数 3 → 改为 len(speed_list)；
#   ③ 分支顺序宽条件在前 → 改为先判 avg < 40 再判 avg < 60；
#   ④ 低速清单边界 <= 35 → 改为 < 35（业务口径为"低于 35"）。
# 校验结果：4 个断面平均车速 47.0 / 60.0 / 35.5 / 30.0，判定 缓行 / 畅通 / 拥堵 / 拥堵。

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
    road = records[i][1]                       # 修复 ①：断面名完整保留，不做切片
    if road not in roads:
        roads[road] = []
    roads[road].append(records[i][2])

print("-" * 40)

for road in roads:
    speed_list = roads[road]
    avg = round(sum(speed_list) / len(speed_list), 1)   # 修复 ②：分母用本断面条数
    if avg < 40:                             # 修复 ③：窄条件在前
        level = "拥堵"
    elif avg < 60:
        level = "缓行"
    else:
        level = "畅通"
    print(road, "→ 平均", avg, "km/h |", len(speed_list), "条 |", level)

print("-" * 40)
slow = []
for i in range(len(records)):
    if records[i][2] < 35:                     # 修复 ④：严格小于，不含 35
        slow.append(records[i][0])
print("低速车辆（< 35 km/h）：", slow, "共", len(slow), "辆")

print("涉及断面：", list(roads.keys()))
