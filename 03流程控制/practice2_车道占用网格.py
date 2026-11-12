# ---------- 第 03 章 流程控制 · 练习 3-2 参考答案：打印路口车道占用网格 ----------
# 对应知识点：3.5 循环三要素与嵌套循环、3.1 内层分支、字符串累加拼接
# 功能说明：按车道数与每车道车位数打印占用网格：[X] 表示已占用、[ ] 表示空位

lanes = eval(input("车道数："))
slots = eval(input("每车道车位数："))
occupied = eval(input("每车道已停车数："))

for lane in range(1, lanes + 1):        # 外层：逐条车道
    line = ""                           # 每换一条车道必须重置，否则上一行会累积进来
    for slot in range(1, slots + 1):     # 内层：逐个车位拼接
        if slot <= occupied:
            line = line + "[X]"         # 已占用
        else:
            line = line + "[ ]"         # 空位
    print("第 " + str(lane) + " 车道：" + line)   # 内层结束后整行输出一次
