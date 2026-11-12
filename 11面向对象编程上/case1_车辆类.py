# ---------- 第 11 章 面向对象编程（上）· 案例 11-1：车辆类 Vehicle ----------
# 对应知识点：11.1 类与实例化、11.2 __init__ 与 self、11.3 实例属性与类属性、11.4 方法与 __str__
# 功能说明：定义车辆类并创建三辆车，演示加速 / 减速的上下限约束与类属性累计创建数

class Vehicle:
    """车辆类：描述车辆属性与行驶行为"""

    total = 0                      # 类属性：所有实例共享，累计创建数

    def __init__(self, plate, vtype, speed=0):
        self.plate = plate          # 实例属性：每辆车独立
        self.vtype = vtype
        self.speed = speed
        Vehicle.total += 1          # 通过类名访问类属性

    def accelerate(self, delta):
        """加速，上限 120 km/h"""
        self.speed = min(self.speed + delta, 120)
        return self.speed

    def brake(self, delta):
        """减速，下限 0 km/h"""
        self.speed = max(self.speed - delta, 0)
        return self.speed

    def info(self):
        return self.plate + "（" + self.vtype + "）当前 " + str(self.speed) + " km/h"

    def __str__(self):
        return "Vehicle<" + self.plate + ">"


# ---------- 使用 ----------
v1 = Vehicle("京A12345", "小型车")
v2 = Vehicle("京B67890", "大型车", 45)
v3 = Vehicle("冀D11223", "新能源", 60)

print(v1.info())
print(v2.info())
print(v3.info())

print("v1 加速 80：", v1.accelerate(80), "km/h")
print("v1 继续加速 50：", v1.accelerate(50), "km/h（被限制在 120）")
print("v2 减速 20：", v2.brake(20), "km/h")
print("v2 紧急制动 100：", v2.brake(100), "km/h（被限制在 0）")

print(v1)
print("累计创建车辆：", Vehicle.total, "辆")
print("v1 的类属性视角：", v1.total)
