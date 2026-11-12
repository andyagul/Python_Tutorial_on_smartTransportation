# ---------- 第 05 章 列表、元组、集合与字典 · 案例 5-1：进口道车辆队列管理 ----------
# 对应知识点：5.1 列表增删改查（append / insert / pop / remove）、5.2 sort() 与统计、5.6 列表推导式
# 功能说明：模拟进口道队列的入队、应急车辆插队、绿灯放行与异常剔除，并对车速排序统计

# 1) 建立队列并查看状态
queue = ["京A12345", "京B67890", "津C24680", "京A13579"]
print("初始队列：", queue, "共", len(queue), "辆")
print("队首：", queue[0], "| 队尾：", queue[-1])
print("前两辆：", queue[:2])

# 2) 入队与插队
queue.append("冀D11223")          # 队尾加入
print("新车入队后：", queue)
queue.insert(1, "京E55667")       # 插到第 2 位（应急车辆优先）
print("应急车辆插入后：", queue)

# 3) 放行与剔除
left = queue.pop(0)               # 取出并删除队首
print("绿灯放行：", left)
queue.remove("津C24680")          # 按车牌剔除异常车辆
print("剔除后队列：", queue, "共", len(queue), "辆")

# 4) 车速排序与统计
speeds = [62, 45, 78, 51, 66]
speeds.sort()                     # 原地升序
print("车速升序：", speeds)
print("最高：", max(speeds), "最低：", min(speeds))
print("平均：", round(sum(speeds) / len(speeds), 1))

speeds.sort(reverse=True)         # 原地降序
print("车速降序：", speeds)
print("前三快：", speeds[:3])
