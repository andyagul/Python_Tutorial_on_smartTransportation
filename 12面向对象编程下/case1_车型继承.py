# ---------- 第 12 章 面向对象编程（下）· 案例 12-1：车型继承体系与方法重写 ----------
# 对应知识点：12.2 继承与 super()、12.3 方法重写（替换 / 扩展）、12.5 isinstance() 与 type()
# 功能说明：由车辆基类派生出小客车、货车与客车，重写限速、计费与信息输出方法

class Vehicle:
    """车辆基类"""

    def __init__(self, plate, speed=0):
        self.plate = plate
        self.speed = speed

    def limit(self):
        """限速，默认 120"""
        return 120

    def fee(self, km, rate=0.5):
        """基础通行费"""
        return round(km * rate, 2)

    def info(self):
        return self.plate + " 限速 " + str(self.limit()) + " km/h"


class Car(Vehicle):
    """小客车"""

    def limit(self):
        return 120


class Truck(Vehicle):
    """货车：新增载重，限速更低，费率上浮"""

    def __init__(self, plate, load, speed=0):
        super().__init__(plate, speed)     # 复用父类初始化
        self.load = load

    def limit(self):
        return 80

    def fee(self, km, rate=0.5):
        base = super().fee(km, rate)       # 先算基础费用
        return round(base * 1.8, 2)        # 货车按 1.8 倍计费

    def info(self):
        return super().info() + "，载重 " + str(self.load) + " 吨"


class Bus(Vehicle):
    """客车"""

    def limit(self):
        return 100

    def fee(self, km, rate=0.5):
        return round(km * rate * 1.2, 2)


fleet = [Car("京A12345"), Truck("京B67890", 18), Bus("京C24680"), Car("京D13579")]

for v in fleet:
    print(v.info(), "| 行驶 120km 通行费", v.fee(120), "元")

print()
print("是否货车：", isinstance(fleet[1], Truck))
print("是否车辆：", isinstance(fleet[1], Vehicle))
print("类型：", type(fleet[1]).__name__)
