# ---------- 第 05A 节 · 练习 5A-4：步出（Shift+F11）检查返回值 ----------
# 现象：函数内部明明打印了 2680，函数外面拿到的 total 却是 None
# 任务：在 total = total_flow(flows) 设断点，F11 进入、Shift+F11 跳出，
#      观察跳出瞬间 total 的值，从而判断函数"有没有把结果交回来"
# 提示：函数内部算对了却交不出结果，问题通常不在算，而在最后一行

def total_flow(flows):
    """合计流量"""
    total = 0
    for f in flows:
        total = total + f
    print("函数内部合计：", total)        # 内部算对了
    # 这里少了一行把结果交回去的语句

flows = [820, 1100, 760]
total = total_flow(flows)      # ← 断点设在这一行，F11 进入、Shift+F11 跳出
print("总流量：", total, "辆")
