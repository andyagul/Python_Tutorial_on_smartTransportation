# ---------- 第 03 章 流程控制 · 案例 3-2：全天分时段车流统计 ----------
# 对应知识点：3.3 for 与 range() 的步长、3.5 累加器与极值维护、3.1 循环体内的分支
# 功能说明：采集 8 个时段的车流量，统计总量、峰值与峰值时段，并对超 1500 辆的时段告警

# 全天分时段车流采集与统计
total = 0        # 全天总量
peak = 0         # 峰值流量
peak_hour = 0    # 峰值所在时段

for hour in range(6, 22, 2):          # 6,8,10,12,14,16,18,20
    flow = eval(input("第 " + str(hour) + " 时段车流量(辆/2h)："))
    total += flow
    if flow > peak:
        peak = flow
        peak_hour = hour
    if flow > 1500:
        print("  [告警] " + str(hour) + " 时段流量偏高：" + str(flow) + " 辆")

print("全天总流量：", total, "辆")
print("平均每时段：", round(total / 8, 1), "辆")
print("峰值时段：", peak_hour, "时，流量", peak, "辆")
print("峰值是否超过 1500：", peak > 1500)
