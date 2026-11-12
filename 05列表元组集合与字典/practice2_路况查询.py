# ---------- 第 05 章 列表、元组、集合与字典 · 练习 5-2 参考答案：路段拥堵状态查询与汇总 ----------
# 对应知识点：5.5 字典遍历 / get() / values()、5.1 列表收集、5.4 集合去重
# 功能说明：按路段查询路况（含缺失路段的默认值），汇总拥堵路段并统计出现过的状态种类

status = {
    "京港澳高速": "拥堵",
    "京开高速": "缓行",
    "机场高速": "畅通",
}

for road in status:
    print(road, "->", status[road])

print("京开高速状态：", status["京开高速"])
print("机场高速状态：", status.get("机场高速", "无数据"))
print("京承高速状态：", status.get("京承高速", "无数据"))

crowded = []
for road in status:
    if status[road] == "拥堵":
        crowded.append(road)
print("拥堵路段：", crowded, "共", len(crowded), "条")

print("全部畅通：", "拥堵" not in status.values() and "缓行" not in status.values())  # values() 取出所有状态值
print("状态种类：", sorted(set(status.values())))
