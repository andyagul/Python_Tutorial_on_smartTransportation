# ---------- 第 06 章 函数 · 案例 6-1：交通计算函数库 ----------
# 对应知识点：6.1 定义与调用、6.2 位置参数与默认参数、6.3 返回值与多返回值、6.4 不使用全局变量
# 功能说明：把通行能力、车流密度、拥堵判定封装为函数，由主程序组合调用并解包多返回值

# ---------- 函数定义 ----------
def capacity(lanes, per_lane=2200):
    """理论通行能力（辆/h），per_lane 默认 2200"""
    return lanes * per_lane


def density(cars, length_km, lanes):
    """车流密度（辆/(km·车道)）"""
    return cars / (length_km * lanes)


def judge(speed, dens):
    """按车速与密度判定拥堵等级"""
    if speed >= 60 and dens < 10:
        return "畅通"
    elif speed >= 40:
        return "缓行"
    elif speed >= 20:
        return "拥堵"
    return "严重拥堵"


def report(road, speed, cars, length_km, lanes):
    """生成站点简报，返回三个值"""
    d = density(cars, length_km, lanes)
    level = judge(speed, d)
    return road, round(d, 2), level


# ---------- 主程序 ----------
print("3 车道通行能力：", capacity(3))          # 使用默认 per_lane
print("2 车道(匝道 1800)：", capacity(2, 1800))  # 覆盖默认值
print("密度：", round(density(96, 2.5, 3), 2))
print("判定(35km/h, 18)：", judge(35, 18))
print("判定(15km/h, 45)：", judge(15, 45))

# 多返回值：按位置解包
site, dens, level = report("京港澳 K12", 35, 96, 2.5, 3)
print("站点：", site)
print("密度：", dens)
print("等级：", level)
