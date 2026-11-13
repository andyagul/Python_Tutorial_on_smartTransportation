# ---------- 第 05A 节 · 练习 5A-2：逐过程（F10）找累加错误 ----------
# 现象：三个断面 820 + 1100 + 760 应得 2680，程序却只有 760，平均流量 253.3
# 任务：用 F10 逐行执行，在循环里盯住 total 的变化规律，说出它在第几行被"打回原形"
# 操作：在 total = 0 设断点 → F5 → 反复按 F10，注意 total 的取值序列

flows = [820, 1100, 760]
total = 0
for f in flows:
    total = 0
    total = total + f
    print("本轮 f =", f, "累计 total =", total)
print("总流量：", total)
print("平均流量：", round(total / len(flows), 1))
