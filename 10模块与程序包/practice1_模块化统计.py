# ---------- 第 10 章 模块与程序包 · 练习 10-1 参考答案：把统计逻辑模块化 ----------
# 对应知识点：10.1 from ... import 与 import ... as 两种导入形式、10.2 自定义模块
# 功能说明：从 flow_stats 导入统计函数，汇总 8 个时段的车流量，并对照别名调用

from flow_stats import total, average, peak_index
import flow_stats as fs

flows = [820, 1100, 760, 690, 720, 980, 1650, 1320]

print("总流量：", total(flows))
print("平均：", average(flows))
print("峰值下标：", peak_index(flows), "（第", peak_index(flows) + 1, "个时段）")

# 别名调用方式，结果一致
print("别名调用总量：", fs.total(flows))
