# ---------- 第 05A 节 · 示例 5A-4：步出（Shift+F11）看返回值 ----------
# 对应知识点：5A.4 步出 Shift+F11 —— 函数内部看够了，一次跳出并把返回值带回调用处
# 操作：在 result = avg_speed(data) 设断点 → F5 → F11 进入函数 →
#      按 Shift+F11 直接跳出，光标回到调用行，result 立刻有了值。

def avg_speed(speeds):
    """平均车速，保留 1 位小数"""
    total = 0
    for s in speeds:
        total = total + s
    return round(total / len(speeds), 1)

data = [62, 45, 78, 51]
result = avg_speed(data)       # ← 断点设在这一行，F11 进入、Shift+F11 跳出
print("平均车速：", result, "km/h")
