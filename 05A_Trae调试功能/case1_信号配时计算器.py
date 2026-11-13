# ---------- 第 05A 节 · 案例 5A-1：信号配时计算器（含 3 个预设 bug）----------
# 对应知识点：5A.2 逐过程、5A.3 步入、5A.5 变量与监视
# 功能说明：按两个相位的流量比，把 90 秒周期内的有效绿灯时间分配给各相位，
#           并输出绿信比，用于核对分配是否合理。
# 使用方式：先 Ctrl+F5 直接跑一遍，记下"错的输出"；再按提示设断点逐行定位。
# 判定标准：绿灯合计 = 有效绿灯时间；两个相位绿信比之和 ≈ 1。

CYCLE = 90                 # 信号周期（秒）
LOST_PER_PHASE = 3         # 每相位损失时间（秒）
SATURATION = 1650          # 单车道饱和流量（pcu/h）

flows = {"南北直行": 720, "东西直行": 480}      # 各相位车流量（辆/小时）


def phase_green(y_phase, y_total, cycle_eff):
    """按流量比把有效绿灯时间分配给一个相位"""
    return round(cycle_eff * y_phase / y_total)


# 1) 总流量比 Y = Σ(q / S)
y_total = 0
for name in flows:
    y_total = 0
    y_total = y_total + flows[name] / SATURATION
print("总流量比 Y =", round(y_total, 3))

# 2) 有效绿灯时间 = 周期 − 总损失时间
lost = LOST_PER_PHASE * len(flows)
cycle_eff = CYCLE - lost
print("总损失", lost, "秒，有效绿灯", cycle_eff, "秒")
print()

# 3) 分配各相位绿灯时间
greens = {}
for name in flows:
    y = flows[name] / SATURATION
    g = phase_green(cycle_eff, y, y_total)
    greens[name] = g
    print("  ", name, "流量比", round(y, 3), "→ 绿灯", g, "秒")

# 4) 校核：绿灯合计应等于有效绿灯
total_green = 0
for name in greens:
    total_green = total_green + greens[name]
print("绿灯合计", total_green, "秒（应等于", cycle_eff, "秒）")
print()

# 5) 绿信比 λ = g / C
for name in greens:
    lam = greens[name] / cycle_eff
    print("  ", name, "绿信比 λ =", round(lam, 3))
