# ---------- 第 02 章 变量与数据类型 · 案例 2-2：信号配时周期拆分 ----------
# 对应知识点：2.3 str() 类型转换、2.4 // 与 % 及复合赋值、2.5 比较与逻辑运算、2.6 输出拼接
# 功能说明：把信号周期按相位平均分配，余数补给主干道，并判断周期是否落在 60~180 秒合理区间

# 信号周期按相位平均分配，余数补给主干道
cycle = eval(input("信号周期总时长(s)："))
phases = eval(input("相位数："))

base = cycle // phases        # 每相位基础绿灯
rest = cycle % phases         # 不能整除的余数

print("每相位基础绿灯：", base, "s")
print("余数：", rest, "s")

base += rest                  # 复合赋值：主干道多拿余数
print("主干道绿灯：", base, "s")
print("支路绿灯：", cycle // phases, "s")

# 比较运算 + 逻辑运算，结果为 bool
print("周期是否合理(60~180s)：", cycle >= 60 and cycle <= 180)
print("是否严重超长(>180s)：", cycle > 180)

# str() 把数字转换成字符串才能与文本拼接
print("本周期设定为 " + str(cycle) + " 秒，共 " + str(phases) + " 个相位")
