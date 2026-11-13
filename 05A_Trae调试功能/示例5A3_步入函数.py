# ---------- 第 05A 节 · 示例 5A-3：步入（F11）进入函数内部 ----------
# 对应知识点：5A.3 步入 F11 —— 光标停在函数调用处，按 F11 进入函数体
# 操作：在 print(s, "→", classify(s)) 设断点 → F5 → 按 F11，
#      光标跳到 def classify(speed) 内部，此时「变量」面板能看到形参 speed 的值。

def classify(speed):
    """按车速判定等级（km/h）"""
    if speed >= 80:
        return "超速"
    if speed >= 60:
        return "正常"
    return "偏慢"

speeds = [92, 58, 74]
for s in speeds:
    print(s, "→", classify(s))     # ← 断点设在这一行，然后按 F11
