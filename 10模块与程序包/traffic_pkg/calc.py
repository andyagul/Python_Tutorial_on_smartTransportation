# ---------- 第 10 章 模块与程序包 · 练习 10-2 配套程序包：包内计算模块 ----------
# 对应知识点：10.5 程序包内的子模块
# 功能说明：提供通行能力与车流密度两个计算函数，供包入口与其他模块调用

"""包内计算模块"""


def capacity(lanes, per_lane=2200):
    """理论通行能力（辆/h）"""
    return lanes * per_lane


def density(cars, length_km, lanes):
    """车流密度（辆/(km·车道)），保留 2 位小数"""
    return round(cars / (length_km * lanes), 2)
