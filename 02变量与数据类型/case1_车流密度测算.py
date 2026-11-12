# ---------- 第 02 章 变量与数据类型 · 案例 2-1：车流密度测算 ----------
# 对应知识点：2.1 变量与赋值、2.2 四种基本数据类型、2.3 input() 与 eval()、2.4 算术运算符、2.6 round() 精度
# 功能说明：由路段长度、车道数与本段车辆数测算车流密度、平均车头间距与理论通行能力

# 路段车流参数测算
# 输入：路段长度(km)、车道数、当前车辆数

length = eval(input("观测路段长度(km)："))   # float
lanes = eval(input("车道数："))              # int
cars = eval(input("该路段车辆数："))         # int

# 车流密度：辆 /(km·车道)
density = cars / (length * lanes)

# 平均车头间距：米
avg_gap = length * 1000 / cars

# 理论通行能力：2200 辆/(h·车道)
capacity = 2200 * lanes

print("车流密度：", round(density, 2), "辆/(km·车道)")
print("平均车头间距：", round(avg_gap, 1), "m")
print("理论通行能力：", capacity, "辆/h")
print("density 类型：", type(density))
print("cars 类型：", type(cars))
