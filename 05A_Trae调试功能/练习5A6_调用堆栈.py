# ---------- 第 05A 节 · 练习 5A-6：调用堆栈定位"错在哪一层" ----------
# 现象：京开断面单车道 300 辆，应判"缓行"，实际判成"拥堵"
# 任务：在 lane_density 的 return 行设断点 → F5（会停在京港澳那次）→ F5 继续（停在京开那次）
#      → 在「调用堆栈」里点 judge 那一帧，比较 judge 收到的 lanes 与它转交给 lane_density 的实参
# 提示：错误往往不在"算式"，而在"传参"；堆栈面板能同时看到上下两层的变量

def lane_density(flow, lanes):
    return round(flow / lanes)      # ← 断点设在这一行

def judge(flow, lanes):
    d = lane_density(flow, 2)       # 此处传的车道数与形参不一致
    if d > 400:
        return "拥堵"
    if d > 250:
        return "缓行"
    return "畅通"

def report(name, flow, lanes):
    print(name, "→", judge(flow, lanes))

report("京港澳", 1650, 3)
report("京开", 900, 3)
