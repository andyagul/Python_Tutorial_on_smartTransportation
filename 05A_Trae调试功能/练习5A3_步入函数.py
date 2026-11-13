# ---------- 第 05A 节 · 练习 5A-3：步入（F11）检查形参 ----------
# 现象：5 分钟观测 12 辆车，折成小时流量只有 25 辆，明显偏小（应为 144）
# 任务：在 hourly_flow(...) 调用处按 F11 进入函数，比较「形参」与「实参」的对应关系
# 提示：进入函数后先看 vehicles 与 minutes 各是多少，再回到调用处看传的是什么

def hourly_flow(vehicles, minutes):
    """由 minutes 分钟的观测值折算为小时流量（辆/小时）"""
    return round(vehicles / minutes * 60)

samples = [(12, 5), (8, 4), (20, 6)]
for vehicles, minutes in samples:
    flow = hourly_flow(minutes, vehicles)      # ← 断点设在这一行，按 F11
    print("5 分钟内", vehicles, "辆 → 小时流量", flow, "辆/小时")
