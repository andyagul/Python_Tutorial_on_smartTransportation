# ---------- 第 05A 节 · 示例 5A-2：逐过程（F10）观察累加 ----------
# 对应知识点：5A.2 逐过程 F10 —— 一行一行执行，不进入函数内部
# 操作：在 total = total + f 设断点 → F5 启动 → 连按 3 次 F10，
#      每次停顿都看一眼「变量」面板里的 total，把数值记下来。

flows = [820, 1100, 760]
total = 0
for f in flows:
    total = total + f          # ← 断点设在这一行，按 F10 走完这一行
    print("本轮 f =", f, "累计 total =", total)
print("总流量：", total)
print("平均流量：", round(total / len(flows), 1))
