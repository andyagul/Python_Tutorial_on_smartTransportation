# ---------- 第 03 章 流程控制 · 练习 3-1 参考答案：车辆排队放行仿真 ----------
# 对应知识点：3.4 while 循环、break 跳出、循环 else 子句
# 功能说明：模拟排队车辆按每分钟放行数逐渐清空；等待超过 30 分钟则转人工疏导

queue = eval(input("排队车辆数："))
per_min = eval(input("每分钟放行车辆数："))
minute = 0

while queue > 0:              # 队列未清空就一直放行
    minute += 1               # 计数写在循环体首行，避免从 0 分钟开始
    if minute > 30:
        print("等待超过 30 分钟，转人工疏导")
        break
    queue -= per_min          # 本分钟放行后剩余排队
    if queue < 0:
        queue = 0             # 防止出现负数排队
    print("第 " + str(minute) + " 分钟，剩余排队", queue, "辆")
else:
    print("排队已清空，共耗时", minute, "分钟")
