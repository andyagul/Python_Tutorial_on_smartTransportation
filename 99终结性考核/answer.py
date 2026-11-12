"""
终结性考核参考答案
课程：Python 编程基础（智慧交通）
功能：读入路口车流数据 -> 清洗 -> 统计 -> 配时决策 -> 输出报表
"""


# ============ 任务一：读入与清洗 ============
def load_data(filename):
    """读取 CSV 并清洗，返回 (有效记录列表, 异常计数字典)"""
    valid = []
    errors = {"格式异常": 0, "数值异常": 0, "越界异常": 0}

    with open(filename, "r", encoding="utf-8") as f:
        lines = f.readlines()

    for i in range(1, len(lines)):          # 跳过表头
        line = lines[i].strip()
        if line == "":
            continue
        parts = line.split(",")

        if len(parts) != 4:
            errors["格式异常"] += 1
            print("  第" + str(i + 1) + "行 格式异常：字段数为 " + str(len(parts)))
            continue

        try:
            flow = int(parts[2])
            speed = int(parts[3])
        except ValueError:
            errors["数值异常"] += 1
            print("  第" + str(i + 1) + "行 数值异常：" + parts[2] + " / " + parts[3])
            continue

        if flow < 0 or flow > 3000 or speed < 0 or speed > 300:
            errors["越界异常"] += 1
            print("  第" + str(i + 1) + "行 越界异常：流量 " + str(flow) + "，车速 " + str(speed))
            continue

        valid.append((parts[0], parts[1], flow, speed))

    print("有效记录：", len(valid), "条")
    for k in errors:
        print("  " + k + "：", errors[k], "条")
    return valid, errors


# ============ 任务二：统计与判定 ============
def judge(flow, speed):
    """拥堵等级判定"""
    if speed >= 55 and flow < 1500:
        return "畅通"
    elif speed >= 40:
        return "缓行"
    elif speed >= 25:
        return "拥堵"
    return "严重拥堵"


def summarize(records):
    """按时间汇总流量、计算平均车速，返回 (时段流量字典, 时段车速字典, 总量, 均速)"""
    flow_by_period = {}
    speed_list = []
    speed_by_period = {}

    for period, lane, flow, speed in records:
        flow_by_period[period] = flow_by_period.get(period, 0) + flow
        speed_list.append(speed)
        speed_by_period.setdefault(period, []).append(speed)

    total_flow = sum(flow_by_period.values())
    avg_speed = round(sum(speed_list) / len(speed_list), 1)

    for p in speed_by_period:
        vals = speed_by_period[p]
        speed_by_period[p] = round(sum(vals) / len(vals), 1)

    return flow_by_period, speed_by_period, total_flow, avg_speed


# ============ 任务三：配时决策 ============
class SignalPlan:
    """单个时段的信号配时方案"""

    GREEN_MAP = {"畅通": 30, "缓行": 50, "拥堵": 70, "严重拥堵": 90}
    YELLOW = 3
    RED = 40
    MAX_CYCLE = 120

    def __init__(self, period, flow, level):
        self.period = period
        self.flow = flow
        self.level = level

    def green_time(self):
        """按等级查表得到绿灯时长"""
        return SignalPlan.GREEN_MAP[self.level]

    def cycle(self):
        """周期 = 绿 + 黄 + 红；超过 120 秒则红灯被压缩，周期取 120"""
        raw = self.green_time() + SignalPlan.YELLOW + SignalPlan.RED
        return min(raw, SignalPlan.MAX_CYCLE)

    def __str__(self):
        return (self.period + " 流量 " + str(self.flow) + " " + self.level
                + " 绿灯 " + str(self.green_time()) + "s 周期 " + str(self.cycle()) + "s")


class EmergencyPlan(SignalPlan):
    """应急方案：严重拥堵时绿灯再加 5 秒"""

    def green_time(self):
        base = super().green_time()
        if self.level == "严重拥堵":
            return base + 5
        return base


# ============ 任务四：报表输出 ============
def write_report(filename, plans, total_flow):
    """写出配时报表"""
    with open(filename, "w", encoding="utf-8") as f:
        f.write("时段,流量,等级,绿灯,周期\n")
        for p in plans:
            row = [p.period, str(p.flow), p.level, str(p.green_time()), str(p.cycle())]
            f.write(",".join(row) + "\n")
        f.write("合计," + str(total_flow) + ",,,\n")

    with open(filename, "r", encoding="utf-8") as f:
        count = len(f.readlines())
    print("报表已写入 " + filename + "，共 " + str(count) + " 行")


# ============ 主程序 ============
if __name__ == "__main__":
    print("=== 任务一：数据读入与清洗 ===")
    records, errors = load_data("traffic_data.csv")

    print()
    print("=== 任务二：分时段统计与等级判定 ===")
    flow_by_period, speed_by_period, total_flow, avg_speed = summarize(records)
    print("全天总流量：", total_flow, "辆 | 平均车速：", avg_speed, "km/h")

    peak_period = max(flow_by_period, key=lambda p: flow_by_period[p])
    slow_period = min(speed_by_period, key=lambda p: speed_by_period[p])
    print("流量最大时段：", peak_period, flow_by_period[peak_period], "辆")
    print("车速最低时段：", slow_period, speed_by_period[slow_period], "km/h")
    print()
    print(f"{'时段':<14}{'流量':>8}{'车速':>8}{'等级':>10}")
    for p in flow_by_period:
        lv = judge(flow_by_period[p], speed_by_period[p])
        print(f"{p:<14}{flow_by_period[p]:>8}{speed_by_period[p]:>8}{lv:>10}")

    print()
    print("=== 任务三：信号配时决策 ===")
    plans = []
    for p in flow_by_period:
        lv = judge(flow_by_period[p], speed_by_period[p])
        plans.append(SignalPlan(p, flow_by_period[p], lv))
    for plan in plans:
        print(plan)

    print()
    print("--- 应急方案（继承演示）---")
    emergency = EmergencyPlan("16:00-18:00", 3230, "严重拥堵")
    print(emergency)

    print()
    print("=== 任务四：报表输出 ===")
    write_report("signal_plan.csv", plans, total_flow)
