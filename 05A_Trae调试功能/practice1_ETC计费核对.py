# ---------- 第 05A 节 · 练习 5A-1：ETC 计费核对（含 3 个预设 bug，独立完成）----------
# 计费规则：
#   1) 费率：小型车 0.45 元/km，中型车 0.75 元/km，大型车 1.20 元/km；
#   2) 里程超过 100 km 的部分按 8 折计费（100 km 以内原价）；
#   3) 会员折扣：金卡 85 折、银卡 95 折、普通卡不打折；
#   4) 每条输出两位小数的应收金额，最后输出合计。
# 现象：普通卡车辆的应收金额为 0.00 元，合计也是 0.00 元；大型车 140 km 的金额偏低。
# 任务：用断点 + 单步定位 3 处错误，改完后校验合计为 322.21 元。

RATES = {"小型车": 0.45, "中型车": 0.75, "大型车": 1.20}      # 元/km
DISCOUNT = {"金卡": 0.85, "银卡": 0.95}                       # 普通卡不打折

trips = [
    ("京A12345", "小型车", 86, "金卡"),
    ("京B67890", "大型车", 140, "普通"),
    ("津C24680", "中型车", 65, "银卡"),
    ("冀D11223", "小型车", 210, "普通"),
]

print("—— 计费明细 ——")
print("-" * 40)

total = 0
for i in range(len(trips)):
    plate = trips[i][0]
    kind = trips[i][1]
    km = trips[i][2]
    level = trips[i][3]

    rate = RATES[kind]
    if km > 100:
        fee = rate * 100 + rate * 0.8 * km
    else:
        fee = rate * km

    fee = fee * DISCOUNT.get(level, 0)
    total = 0
    total = total + fee

    print(plate, kind, str(km) + " km", "→", "{:.2f} 元".format(fee))

print("-" * 40)
print("合计：{:.2f} 元".format(total))
