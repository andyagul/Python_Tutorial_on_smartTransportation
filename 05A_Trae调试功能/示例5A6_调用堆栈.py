# ---------- 第 05A 节 · 示例 5A-6：调用堆栈，看清"谁调用了谁" ----------
# 对应知识点：5A.6 调用堆栈 Call Stack —— 顺着调用链找到出问题的那一层
# 操作：在 lane_density 的 return 行设断点 → F5 暂停 →
#      「调用堆栈」面板自上而下依次是 lane_density ← judge ← report ← <module>，
#      点任意一帧，编辑器跳到对应代码行，变量面板切换成该层的局部变量。

def lane_density(flow, lanes):
    """单车道车流密度（辆/车道）"""
    return round(flow / lanes)      # ← 断点设在这一行

def judge(flow, lanes):
    """按单车道密度判定服务水平"""
    d = lane_density(flow, lanes)
    if d > 400:
        return "拥堵"
    if d > 250:
        return "缓行"
    return "畅通"

def report(name, flow, lanes):
    print(name, "单车道", round(flow / lanes), "辆 →", judge(flow, lanes))

report("京港澳", 1650, 3)
report("京开", 900, 3)
