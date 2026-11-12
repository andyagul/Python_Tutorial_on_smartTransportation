# ---------- 第 06 章 函数 · 练习 6-1 参考答案：可变参数与关键字参数计费 ----------
# 对应知识点：6.2 *args 可变参数、默认参数、关键字调用、6.3 返回值
# 功能说明：用可变参数合计任意多个路段的车流，用关键字参数控制费率与折扣计算通行费

def total_flow(*flows):
    """任意多个路段的车流总量"""
    if len(flows) == 0:
        return 0
    return sum(flows)


def avg_flow(*flows):
    """任意多个路段的平均流量"""
    if len(flows) == 0:
        return 0
    return round(sum(flows) / len(flows), 1)


def fee(km, rate=0.5, discount=1.0):
    """通行费 = 里程 × 费率 × 折扣"""
    return round(km * rate * discount, 2)


print("三路段总量：", total_flow(820, 1100, 760))
print("无参数总量：", total_flow())
print("四路段均值：", avg_flow(820, 1100, 760, 690))
print("默认费率：", fee(120))
print("指定费率：", fee(120, 0.6))
print("关键字调用：", fee(km=120, discount=0.95))
print("全部关键字：", fee(km=200, rate=0.45, discount=0.9))
