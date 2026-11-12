# ---------- 第 05 章 列表、元组、集合与字典 · 案例 5-2：车牌台账与过车记录去重 ----------
# 对应知识点：5.3 元组（不可变）、5.5 字典增删改查与遍历、5.4 集合去重与交并差
# 功能说明：用元组存路口坐标、字典存车辆台账、集合对两个时段的过车记录去重与比对

# 1) 元组：路口坐标一经确定不允许修改
cross = ("京港澳高速 K12 路口", 39.9042, 116.4074)
print("监测点位：", cross[0])
print("纬度：", cross[1], "经度：", cross[2])
print("坐标字段数：", len(cross))

# 2) 字典：车牌 -> (车型, 车速)
ledger = {
    "京A12345": ("小型车", 62),
    "京B67890": ("大型车", 48),
    "津C24680": ("小型车", 75),
}
print("台账车辆数：", len(ledger))
print("京A12345 档案：", ledger["京A12345"])
print("车型：", ledger["京A12345"][0], "车速：", ledger["京A12345"][1])

ledger["冀D11223"] = ("新能源", 55)     # 新增
ledger["京B67890"] = ("大型车", 51)     # 修改
del ledger["津C24680"]                  # 删除
print("更新后台账：")
for plate in ledger:
    print("   ", plate, "->", ledger[plate])

print("是否已注销津C24680：", "津C24680" not in ledger)

# 3) 集合：过车记录去重
records = ["京A12345", "京B67890", "京A12345", "冀D11223", "京B67890", "京A12345"]
print("原始记录：", len(records), "条")
unique = set(records)
print("去重车牌：", sorted(unique))
print("实际车辆：", len(unique), "辆")
print("重复上报：", len(records) - len(unique), "条")

# 集合运算：本时段与上时段都出现的车辆
last_hour = {"京A12345", "津C24680"}
print("两时段均出现：", sorted(unique & last_hour))
print("本时段新增：", sorted(unique - last_hour))
