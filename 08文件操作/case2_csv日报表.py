# ---------- 第 08 章 文件操作 · 案例 8-2：交通流量日报表（CSV）生成与汇总 ----------
# 对应知识点：8.5 CSV 手工写入与解析、8.1 w / a / r 三种模式、8.2 readlines()
# 功能说明：生成日报 CSV，读回按流量加权求平均车速，追加合计行后验证文件行数

# ---------- 1) 生成 CSV 报表 ----------
rows = [
    ("时段", "车流量", "平均车速"),
    ("06:00-08:00", 820, 68),
    ("08:00-10:00", 1100, 42),
    ("10:00-12:00", 760, 58),
    ("12:00-14:00", 690, 62),
    ("14:00-16:00", 720, 60),
    ("16:00-18:00", 980, 48),
    ("18:00-20:00", 1650, 32),
]

with open("flow_daily.csv", "w", encoding="utf-8") as f:
    for r in rows:
        f.write(",".join(map(str, r)) + "\n")
print("报表已生成，共", len(rows), "行")

# ---------- 2) 读回并汇总 ----------
total_flow = 0
weighted = 0
first = True

with open("flow_daily.csv", "r", encoding="utf-8") as f:
    for line in f:
        line = line.strip()
        if line == "":
            continue
        if first:                 # 跳过表头
            first = False
            continue
        parts = line.split(",")
        flow = int(parts[1])
        speed = int(parts[2])
        total_flow += flow
        weighted += flow * speed

avg_speed = round(weighted / total_flow, 1)
print("全天总流量：", total_flow, "辆")
print("加权平均车速：", avg_speed, "km/h")

# ---------- 3) 追加汇总行 ----------
with open("flow_daily.csv", "a", encoding="utf-8") as f:
    f.write("合计," + str(total_flow) + "," + str(avg_speed) + "\n")
print("汇总行已追加")

# ---------- 4) 验证追加结果 ----------
with open("flow_daily.csv", "r", encoding="utf-8") as f:
    lines = f.readlines()
print("当前文件行数：", len(lines))
print("最后一行：", lines[-1].strip())
