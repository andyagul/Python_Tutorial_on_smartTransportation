# ---------- 第 05 章 列表、元组、集合与字典 · 练习 5-1 参考答案：分时段车流量统计 ----------
# 对应知识点：5.2 sum / max / min / index 统计、5.1 切片、5.6 列表推导式
# 功能说明：统计 8 个时段车流量的总量、均值、峰谷位置与早晚高峰合计，并折算百辆

flows = [820, 1100, 760, 690, 720, 980, 1650, 1320]

print("时段数：", len(flows))
print("总流量：", sum(flows), "辆")
print("平均：", round(sum(flows) / len(flows), 1), "辆")
print("最大：", max(flows), "出现在第", flows.index(max(flows)) + 1, "个时段")
print("最小：", min(flows), "出现在第", flows.index(min(flows)) + 1, "个时段")

morning = sum(flows[:4])          # 切片取前 4 个时段：早高峰
evening = sum(flows[4:])          # 后 4 个时段：晚高峰
print("早高峰合计：", morning, "| 晚高峰合计：", evening)
print("晚高峰是否更高：", evening > morning)

over = [x for x in flows if x > 1500]
print("超 1500 的时段流量：", over, "共", len(over), "个")

hundreds = [x // 100 for x in flows]
print("折合百辆：", hundreds)
