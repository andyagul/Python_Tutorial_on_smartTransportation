# ---------- 第 12 章 面向对象编程（下）· 案例 12-2：多态——统一调度不同路侧设备 ----------
# 对应知识点：12.4 多态与 NotImplementedError 接口约定、12.2 super().__init__、12.3 重写
# 功能说明：用基类约定统一接口，循环调度信号灯、情报板、道闸等设备，各自实现自身行为

class SignalDevice:
    """路侧设备基类：约定接口"""

    def __init__(self, code):
        self.code = code

    def status(self):
        raise NotImplementedError("子类必须实现 status()")

    def refresh(self):
        raise NotImplementedError("子类必须实现 refresh()")


class Light(SignalDevice):
    """信号灯"""

    def __init__(self, code, phase="红灯"):
        super().__init__(code)
        self.phase = phase

    def status(self):
        return "信号灯 " + self.code + " 当前相位 " + self.phase

    def refresh(self):
        return "信号灯 " + self.code + " 已同步配时方案"


class VariableSign(SignalDevice):
    """可变情报板"""

    def __init__(self, code, text="限速 60"):
        super().__init__(code)
        self.text = text

    def status(self):
        return "情报板 " + self.code + " 显示 <" + self.text + ">"

    def refresh(self):
        return "情报板 " + self.code + " 已刷新显示内容"


class Barrier(SignalDevice):
    """道闸"""

    def __init__(self, code, opened=False):
        super().__init__(code)
        self.opened = opened

    def status(self):
        state = "抬起" if self.opened else "落下"
        return "道闸 " + self.code + " 当前" + state

    def refresh(self):
        self.opened = not self.opened
        return "道闸 " + self.code + " 已切换为" + ("抬起" if self.opened else "落下")


def poll(devices):
    """统一巡检：不判断具体类型"""
    print("=== 设备巡检开始，共 " + str(len(devices)) + " 台 ===")
    for d in devices:
        print("[状态]", d.status())
        print("[指令]", d.refresh())
    print("=== 巡检结束 ===")


devices = [
    Light("L-01", "绿灯"),
    VariableSign("V-07", "前方事故，减速慢行"),
    Barrier("B-03"),
    Light("L-02", "黄灯"),
]

poll(devices)
print()
print("第二轮巡检（道闸状态已翻转）：")
poll(devices)
