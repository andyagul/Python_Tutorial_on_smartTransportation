# ---------- 第 10 章 模块与程序包 · 案例 10-1 配套模块：交通计算工具 ----------
# 对应知识点：10.2 自定义模块与模块文档 __doc__、6.2 默认参数、模块级常量
# 功能说明：提供通行能力、车流密度、拥堵判定的通用计算，供其他程序导入复用

"""
交通计算工具模块
作者：智慧交通教研组
说明：提供通行能力、车流密度、拥堵判定的通用计算，供各业务程序复用
"""

DEFAULT_CAPACITY = 2200        # 单车道理论通行能力（辆/h）


def capacity(lanes, per_lane=DEFAULT_CAPACITY):
    """理论通行能力（辆/h）"""
    return lanes * per_lane


def density(cars, length_km, lanes):
    """车流密度（辆/(km·车道)），保留 2 位小数"""
    return round(cars / (length_km * lanes), 2)


def judge(speed, dens):
    """拥堵等级判定"""
    if speed >= 60 and dens < 10:
        return "畅通"
    elif speed >= 40:
        return "缓行"
    elif speed >= 20:
        return "拥堵"
    return "严重拥堵"
