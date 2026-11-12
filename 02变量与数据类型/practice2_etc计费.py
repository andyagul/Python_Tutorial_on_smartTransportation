# ---------- 第 02 章 变量与数据类型 · 练习 2-2 参考答案：ETC 通行费核算 ----------
# 对应知识点：2.3 类型转换、2.4 乘法链、2.5 比较运算、2.6 精度控制
# 功能说明：按里程、费率与 ETC 折扣核算通行费与每公里单价，并判断是否超出预算

km = eval(input("行驶里程(km)："))
rate = eval(input("费率(元/km)："))
discount = eval(input("ETC 折扣(如 0.95)："))

fee = km * rate * discount
unit_price = rate * discount

print("应收通行费：", round(fee, 2), "元")          # 两位小数
print("每公里单价：", round(unit_price, 3), "元/km")  # 三位小数
print("是否超出 50 元预算：", fee > 50)              # 布尔判断
print("折扣后是否优惠：", discount < 1)              # 逻辑结论
