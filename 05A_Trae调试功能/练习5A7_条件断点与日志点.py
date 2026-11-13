# ---------- 第 05A 节 · 练习 5A-7：用条件断点揪出异常值 ----------
# 现象：8 个样本的平均车速只有 62.1 km/h，与肉眼看到的 60~82 明显不符
# 任务：
#   1) 在 total = total + speeds[i] 设普通断点，看要停几次；
#   2) 改成条件断点 speeds[i] < 10，只停那一次，看 i 与 speeds[i]；
#   3) 用日志点输出每一轮的 i 与 speeds[i]，确认是哪一条数据有问题；
#   4) 说清这条数据该怎么处理（提示：第 4 章清洗、第 5 章筛选取值）
# 提示：条件断点的表达式用当前作用域里的变量写，不要把 print 写进去

speeds = [78, 65, 71, 0, 82, 69, 74, 58]
total = 0
for i in range(len(speeds)):
    total = total + speeds[i]        # ← 先设普通断点，再改条件断点 speeds[i] < 10

avg = total / len(speeds)
print("样本数：", len(speeds))
print("平均车速：", round(avg, 1), "km/h")
