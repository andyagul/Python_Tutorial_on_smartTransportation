# ---------- 第 10 章 模块与程序包 · 练习 10-1 配套模块：车流量统计 ----------
# 对应知识点：10.2 自定义模块、10.3 if __name__ == "__main__" 保护
# 功能说明：提供总量、均值、峰值下标三个统计函数，并带只在直接运行时才执行的模块自测

"""车流量统计模块"""


def total(flows):
    """车流总量"""
    return sum(flows)


def average(flows):
    """平均流量，保留 1 位小数；空列表返回 0"""
    if len(flows) == 0:
        return 0
    return round(sum(flows) / len(flows), 1)


def peak_index(flows):
    """峰值所在下标（从 0 开始）"""
    return flows.index(max(flows))


if __name__ == "__main__":
    demo = [820, 1100, 760, 690]
    print("[模块自测] 总量", total(demo), "均值", average(demo), "峰值下标", peak_index(demo))
