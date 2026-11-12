# ---------- 第 12 章 面向对象编程（下）· 练习 12-2 参考答案：充电设施的多态计费 ----------
# 对应知识点：12.4 多态与基类统一实现、12.3 方法重写、6.x 模板方法思想
# 功能说明：由充电桩基类派生快充与慢充，用统一接口按不同电价与功率计算充电费用

class Charger:
    """充电桩基类"""

    def __init__(self, code):
        self.code = code

    def power(self):
        return 7

    def price(self):
        return 0.6

    def overtime_fee(self, minutes):
        return 0

    def settle(self, kwh, minutes):
        energy_fee = round(kwh * self.price(), 2)
        service = round(energy_fee * 0.1, 2)
        ot = self.overtime_fee(minutes)
        return round(energy_fee + service + ot, 2)

    def info(self):
        return self.code + " " + str(self.power()) + "kW 单价 " + str(self.price()) + " 元/kWh"


class SlowCharger(Charger):
    def power(self):
        return 7

    def price(self):
        return 0.6


class FastCharger(Charger):
    def power(self):
        return 60

    def price(self):
        return 1.0


class SuperCharger(Charger):
    def power(self):
        return 250

    def price(self):
        return 1.6

    def overtime_fee(self, minutes):
        if minutes > 60:
            return (minutes - 60) * 2
        return 0


chargers = [SlowCharger("C-01"), FastCharger("C-02"), SuperCharger("C-03")]

for c in chargers:
    total = c.settle(35, 85)
    print(c.info(), "| 35kWh/85min 应收", total, "元")

print()
print("超充超时费：", SuperCharger("C-03").overtime_fee(85), "元")
print("慢充超时费：", SlowCharger("C-01").overtime_fee(85), "元")
