# ---------- 第 05A 节 · 示例 5A-5：变量面板、悬停与监视表达式 ----------
# 对应知识点：5A.5 查看变量与方法 —— 变量面板展开、鼠标悬停、监视 Watch
# 操作：
#   1) 在 print(...) 设断点 → F5 暂停；
#   2) 「变量」面板展开 road_flows，看字典 → 列表的层级；
#   3) 鼠标悬停在 len(flows) 上，直接看到结果；
#   4) 在「监视」里添加表达式：len(flows)、sum(flows)、max(flows)。

road_flows = {"京港澳": [820, 1100, 760], "京开": [640, 720]}
for road in road_flows:
    flows = road_flows[road]
    print(road, "断面数：", len(flows), "| 合计：", sum(flows), "| 峰值：", max(flows))
