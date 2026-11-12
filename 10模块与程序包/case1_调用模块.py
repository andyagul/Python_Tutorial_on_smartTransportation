# ---------- 第 10 章 模块与程序包 · 案例 10-1：抽出第一个自定义模块并调用 ----------
# 对应知识点：10.1 import ... as 导入形式、10.2 读取模块文档 __doc__、模块级常量
# 功能说明：以「导入并起别名」的方式调用 traffic_utils 中的函数，演示模块复用

import traffic_utils as tu          # 导入自定义模块并起别名

print("模块说明：", tu.__doc__.strip().splitlines()[0])
print("默认单车道能力：", tu.DEFAULT_CAPACITY)

print("3 车道通行能力：", tu.capacity(3))
print("2 车道(匝道 1800)：", tu.capacity(2, 1800))
print("车流密度：", tu.density(96, 2.5, 3))

speeds = [66, 45, 28, 15]
densities = [8, 12, 22, 45]
for i in range(len(speeds)):
    print("车速", speeds[i], "密度", densities[i], "->", tu.judge(speeds[i], densities[i]))
