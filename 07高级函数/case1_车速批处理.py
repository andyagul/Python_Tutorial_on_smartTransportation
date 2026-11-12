# ---------- 第 07 章 高级函数 · 案例 7-1：车载车速数据批处理 ----------
# 对应知识点：7.1 lambda 匿名函数、7.2 map() 与 filter()、7.3 sorted(key=) 排序
# 功能说明：批量把车速换算为 m/s、筛出超速车辆、按车速降序排名并计算超速率

speeds = [62, 118, 45, 132, 78, 95, 150]

# 1) map：把 km/h 换算成 m/s（除以 3.6）
ms = list(map(lambda v: round(v / 3.6, 1), speeds))
print("换算 m/s：", ms)

# 2) filter：保留大于 120 的超速车辆
over = list(filter(lambda v: v > 120, speeds))
print("超速车速：", over)
print("超速车辆数：", len(over))

# 3) sorted + key：按车速降序排名（原列表不变）
ranked = sorted(speeds, key=lambda v: v, reverse=True)
print("降序排名：", ranked)
print("原列表未被修改：", speeds)

# 4) 组合计算超速率
rate = len(over) / len(speeds) * 100
print("超速率：", round(rate, 1), "%")

# 5) 等价写法对照：map 也可直接传内置函数
print("全部转字符串：", list(map(str, speeds)))
