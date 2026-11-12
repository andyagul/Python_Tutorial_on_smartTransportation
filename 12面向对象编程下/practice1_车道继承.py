# ---------- 第 12 章 面向对象编程（下）· 练习 12-1 参考答案：ETC 车道与人工车道 ----------
# 对应知识点：12.2 继承与 super().__init__、12.3 重写（通行能力 / 计费 / 信息追加）
# 功能说明：由车道基类派生 ETC 车道与人工车道，分别重写通行能力与收费规则

class Lane:
    """车道基类"""

    def __init__(self, code):
        self.code = code

    def capacity(self):
        return 400

    def fee(self, km, rate=0.5):
        return round(km * rate, 2)

    def info(self):
        return self.code + " 通行能力 " + str(self.capacity()) + " 辆/h"


class EtcLane(Lane):
    """ETC 车道"""

    def __init__(self, code, device_ok=True):
        super().__init__(code)
        self.device_ok = device_ok

    def capacity(self):
        return 1500

    def fee(self, km, rate=0.5):
        return round(super().fee(km, rate) * 0.95, 2)

    def info(self):
        state = "正常" if self.device_ok else "故障"
        return super().info() + "，设备" + state


class ManualLane(Lane):
    """人工车道"""

    def capacity(self):
        return 400

    def info(self):
        return super().info() + "，人工发卡"


lanes = [EtcLane("E-01"), EtcLane("E-02", device_ok=False), ManualLane("M-01")]

for lane in lanes:
    print(lane.info(), "| 200km 费用", lane.fee(200), "元")

print()
print("ETC 与人工通行能力比：", round(EtcLane("X").capacity() / ManualLane("Y").capacity(), 2))
print("是否车道子类：", isinstance(lanes[0], Lane))
