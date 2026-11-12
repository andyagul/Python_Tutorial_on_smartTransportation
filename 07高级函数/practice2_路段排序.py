# ---------- 第 07 章 高级函数 · 练习 7-2 参考答案：路段多关键字排序 ----------
# 对应知识点：7.3 sorted(key=) 的多级 key（元组 + 负号取反）、7.1 lambda、7.2 map()
# 功能说明：按排队长度降序排出处置顺序，并按「车速升序、同速排队降序」做多关键字排序

roads = [
    ("京港澳", 45, 320),
    ("京开", 62, 80),
    ("机场", 78, 40),
    ("京承", 45, 120),
]

by_queue = sorted(roads, key=lambda r: r[2], reverse=True)
print("按排队降序：", by_queue)
print("处置顺序：", list(map(lambda r: r[0], by_queue)))

by_speed = sorted(roads, key=lambda r: (r[1], -r[2]))
print("按车速升序、同速排队降序：", by_speed)

print("最拥堵路段：", by_queue[0][0], "排队", by_queue[0][2], "m")
print("平均车速：", round(sum(map(lambda r: r[1], roads)) / len(roads), 1))
