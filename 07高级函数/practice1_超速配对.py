# ---------- 第 07 章 高级函数 · 练习 7-1 参考答案：车牌与车速配对筛选 ----------
# 对应知识点：7.4 zip() 配对、7.2 filter() 与 map()、7.1 lambda
# 功能说明：把车牌列表与车速列表配对，筛出超速记录并提取对应车牌，计算超速占比

plates = ["京A12345", "京B67890", "津C24680", "冀D11223", "京E55667"]
speeds = [62, 118, 132, 78, 150]

pairs = list(zip(plates, speeds))
print("配对结果：", pairs)

over = list(filter(lambda p: p[1] > 120, pairs))
print("超速记录：", over)
print("超速数量：", len(over))

over_plates = list(map(lambda p: p[0], over))
print("超速车牌：", over_plates)

print("超速占比：", round(len(over) / len(pairs) * 100, 1), "%")
print("车牌数校验一致：", len(plates) == len(speeds))
