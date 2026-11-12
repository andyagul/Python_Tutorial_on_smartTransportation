# ---------- 第 11 章 面向对象编程（上）· 练习 11-1 参考答案：停车场类 ParkingLot ----------
# 对应知识点：11.1—11.5（构造方法、私有列表、方法约束、使用率计算）
# 功能说明：实现入场、出场、余位查询与使用率统计，处理满位与重复入场两种情况

class ParkingLot:
    """智慧停车场"""

    def __init__(self, name, capacity):
        self.name = name
        self.capacity = capacity
        self.__cars = []                 # 私有：已停车辆

    def park(self, plate):
        if plate in self.__cars:
            print("[提示]", plate, "已在场内")
            return False
        if len(self.__cars) >= self.capacity:
            print("[拒绝]", self.name, "车位已满，无法驶入")
            return False
        self.__cars.append(plate)
        print("[驶入]", plate, "剩余车位", self.free())
        return True

    def leave(self, plate):
        if plate not in self.__cars:
            print("[提示]", plate, "不在本停车场")
            return False
        self.__cars.remove(plate)
        print("[驶出]", plate, "剩余车位", self.free())
        return True

    def free(self):
        return self.capacity - len(self.__cars)

    def usage(self):
        if self.capacity == 0:
            return 0
        return round(len(self.__cars) / self.capacity * 100, 1)

    def info(self):
        return (self.name + "：车位 " + str(self.capacity)
                + "，已停 " + str(len(self.__cars))
                + "，使用率 " + str(self.usage()) + "%")


lot = ParkingLot("B 区智慧停车场", 4)
lot.park("京A12345")
lot.park("京B67890")
lot.park("津C24680")
lot.park("冀D11223")
lot.park("京E55667")          # 满位
lot.park("京A12345")          # 重复入场
print(lot.info())

lot.leave("京B67890")
lot.leave("京X99999")         # 不在场
print(lot.info())
