# ---------- 第 11 章 面向对象编程（上）· 案例 11-2：信号灯类 TrafficLight ----------
# 对应知识点：11.5 私有属性与受控访问、11.3 类属性 PHASES、11.4 方法互调
# 功能说明：模拟信号灯相位轮转与配时；绿灯时长只能通过带校验的公有方法修改

class TrafficLight:
    """路口信号灯：相位轮转与配时"""

    PHASES = ("红灯", "绿灯", "黄灯")        # 类属性：相位顺序固定

    def __init__(self, name, green=30, yellow=3, red=30):
        self.name = name
        self.__green = green                 # 私有属性：外部不可直接改
        self.__yellow = yellow
        self.__red = red
        self.index = 0                       # 当前相位下标
        self.__check()

    # ---------- 内部校验（私有方法） ----------
    def __check(self):
        if self.__green < 5 or self.__green > 120:
            print("[警告] 绿灯时长异常：", self.__green, "秒，已重置为 30 秒")
            self.__green = 30

    # ---------- 公有方法 ----------
    def get_cycle(self):
        """信号周期总时长"""
        return self.__green + self.__yellow + self.__red

    def get_green(self):
        return self.__green

    def set_green(self, seconds):
        """设置绿灯时长，带合法性校验"""
        if seconds < 5 or seconds > 120:
            print("[拒绝] 绿灯时长必须在 5~120 秒之间")
            return False
        self.__green = seconds
        return True

    def current(self):
        return TrafficLight.PHASES[self.index]

    def switch(self):
        """切换到下一相位"""
        self.index = (self.index + 1) % len(TrafficLight.PHASES)
        return self.current()

    def info(self):
        return (self.name + "：" + self.current()
                + "，绿灯 " + str(self.__green) + "s / 黄灯 " + str(self.__yellow)
                + "s / 红灯 " + str(self.__red) + "s，周期 " + str(self.get_cycle()) + "s")


# ---------- 使用 ----------
light = TrafficLight("京港澳K12 东进口", green=35, yellow=3, red=30)
print(light.info())
print("当前相位：", light.current())
print("切换 ->", light.switch())
print("切换 ->", light.switch())
print("切换 ->", light.switch())

print("设置绿灯 45 秒：", light.set_green(45), "->", light.get_green(), "秒")
print("设置绿灯 200 秒：", light.set_green(200))

print("周期总长：", light.get_cycle(), "秒")

light2 = TrafficLight("异常测试", green=0)
print(light2.info())

# 尝试直接访问私有属性（会报 AttributeError，已注释）
# print(light.__green)
print("私有属性是否被隐藏：", hasattr(light, "__green"))
