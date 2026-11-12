# ---------- 第 11 章 面向对象编程（上）· 练习 11-2 参考答案：路口类 Intersection ----------
# 对应知识点：11.2 __init__、11.3 类属性计数、11.4 方法互调、11.5 私有累计量
# 功能说明：统计路口通过车辆数与平均车速，非法车速拒绝计入，并统计创建的路口对象数

class Intersection:
    """路口：通行统计"""

    total = 0                          # 类属性：路口对象总数

    def __init__(self, name, lanes):
        self.name = name
        self.lanes = lanes
        self.__count = 0
        self.__speed_sum = 0
        Intersection.total += 1

    def pass_car(self, speed):
        if speed < 0 or speed > 300:
            print("[拒绝] 车速异常：", speed)
            return False
        self.__count += 1
        self.__speed_sum += speed
        return True

    def avg_speed(self):
        if self.__count == 0:
            return 0
        return round(self.__speed_sum / self.__count, 1)

    def capacity(self):
        return self.lanes * 2200

    def info(self):
        return (self.name + "：" + str(self.lanes) + " 车道，已通过 "
                + str(self.__count) + " 辆，平均车速 " + str(self.avg_speed())
                + " km/h，通行能力 " + str(self.capacity()) + " 辆/h")


a = Intersection("京港澳 K12", 3)
b = Intersection("京开 K8", 2)

for s in [62, 118, 45, 132, 78]:
    a.pass_car(s)
a.pass_car(400)                        # 非法车速

print(a.info())
print(b.info(), "（尚未通车）")
print("平均车速：", a.avg_speed(), "km/h")
print("创建路口对象：", Intersection.total, "个")
