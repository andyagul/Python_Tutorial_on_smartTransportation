# ---------- 第 10 章 模块与程序包 · 案例 10-2：用标准库生成模拟车流数据 ----------
# 对应知识点：10.4 标准库 random 与 datetime、10.1 import、3.2 条件表达式
# 功能说明：用随机数与时间函数生成带时间戳的模拟车流，并做拥堵概率抽样与日期推算

import random
import datetime

random.seed(20261029)               # 固定种子：每次运行结果一致，便于批改

roads = ["京港澳 K12", "京开 K8", "机场高速 K3", "京承 K20"]

print("=== 模拟车流数据（5 条） ===")
for i in range(5):
    road = random.choice(roads)
    flow = random.randint(600, 1800)          # 整数流量
    speed = round(random.uniform(15, 85), 1)  # 浮点车速
    now = datetime.datetime.now()
    stamp = now.strftime("%Y-%m-%d %H:%M:%S")  # 格式化时间

    print(str(i + 1) + ".", stamp, "|", road, "| 流量", flow, "| 车速", speed)

print()
print("=== 随机拥堵概率 ===")
for i in range(3):
    p = random.random()                        # 0~1 之间
    print("第" + str(i + 1) + "次抽样拥堵概率：", round(p, 3), "->", "拥堵" if p > 0.6 else "不拥堵")

print()
print("=== 时间计算 ===")
today = datetime.date.today()
print("今天：", today)
print("明天：", today + datetime.timedelta(days=1))
