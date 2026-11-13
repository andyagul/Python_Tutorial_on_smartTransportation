# ---------- 第 05A 节 · 练习 5A-1 参考答案：ETC 计费核对（3 处 bug 已修复）----------
# 对应知识点：5A.2 逐过程（F10）、5A.5 变量与监视、5A.7 条件断点
# 修复点：
#   ① 累加器 total = 0 原本写在循环内，导致合计只剩最后一笔 → 移到循环外；
#   ② 折扣取值 DISCOUNT.get(level, 0) → get(level, 1.0)，普通卡不再打 0 折；
#   ③ 分段计费基数 rate * 0.8 * km → rate * 0.8 * (km - 100)，只对超出部分打折。
# 校验结果：4 笔金额 32.90 / 158.40 / 46.31 / 84.60，合计 322.21 元。

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

total = 0                                    # 修复 ①：累加器初始化放在循环外
for i in range(len(trips)):
    plate = trips[i][0]
    kind = trips[i][1]
    km = trips[i][2]
    level = trips[i][3]

    rate = RATES[kind]
    if km > 100:
        fee = rate * 100 + rate * 0.8 * (km - 100)  # 修复 ③：只对超出 100 km 的部分打折
    else:
        fee = rate * km

    fee = fee * DISCOUNT.get(level, 1.0)      # 修复 ②：普通卡默认值为 1.0（不打折）
    total = total + fee                       # 修复 ①：累加器已在循环外初始化，这里只做加法

    print(plate, kind, str(km) + " km", "→", "{:.2f} 元".format(fee))

print("-" * 40)
print("合计：{:.2f} 元".format(total))
