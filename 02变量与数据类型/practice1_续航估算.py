# ---------- 第 02 章 变量与数据类型 · 练习 2-1 参考答案：新能源车续航估算 ----------
# 对应知识点：2.1—2.6 全章综合（类型转换、乘法链、比较运算、精度控制）
# 功能说明：由剩余电量、电池容量与百公里电耗估算可用电量与可行驶里程，并判断能否到达充电站

soc = eval(input("剩余电量(%)："))
capacity = eval(input("电池容量(kWh)："))
consume = eval(input("百公里电耗(kWh/100km)："))

energy = capacity * soc / 100          # 可用电量
range_km = energy / consume * 100      # 预计续航

print("可用电量：", round(energy, 2), "kWh")      # 保留两位
print("预计续航：", round(range_km), "km")        # 保留整数
print("能否到达 200km 外充电站：", range_km >= 200)  # 布尔结论
print("电量百分比类型：", type(soc))               # 检查类型
