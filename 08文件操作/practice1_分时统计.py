# ---------- 第 08 章 文件操作 · 练习 8-1 参考答案：分时段过车记录统计 ----------
# 对应知识点：8.1 w / r 模式、8.2 逐行解析、5.5 字典按键累加
# 功能说明：把过车记录按小时累加写入并读回，统计分时车流量、峰值小时与小时均值

# 1) 生成样例数据（同一小时故意重复两条，用于验证累加）
sample = [
    (6, 420), (6, 400), (8, 1100), (10, 760),
    (12, 690), (14, 720), (16, 980), (18, 1650), (20, 1320),
]
with open("flow_log.txt", "w", encoding="utf-8") as f:
    for hour, flow in sample:
        f.write(str(hour) + "," + str(flow) + "\n")

# 2) 读取并按小时累加
hourly = {}
with open("flow_log.txt", "r", encoding="utf-8") as f:
    for line in f:
        line = line.strip()
        if line == "":
            continue
        parts = line.split(",")
        hour = int(parts[0])
        flow = int(parts[1])
        hourly[hour] = hourly.get(hour, 0) + flow

# 3) 统计
total = sum(hourly.values())
peak_hour = max(hourly, key=lambda h: hourly[h])
print("参与统计的小时数：", len(hourly))
print("全天总流量：", total, "辆")
print("峰值小时：", peak_hour, "时，流量", hourly[peak_hour], "辆")
print("小时均值：", round(total / len(hourly), 1), "辆")
