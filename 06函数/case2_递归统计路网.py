# ---------- 第 06 章 函数 · 案例 6-2：递归统计路网节点 ----------
# 对应知识点：6.5 递归三要素（终止条件 / 递推 / 回归）、6.3 返回累计值、5.5 嵌套字典遍历
# 功能说明：递归遍历「干道—支路—路口」树结构，统计节点总数、末端路口数与层级深度

# 路网树：干道 -> 支路 -> 路口
road_net = {
    "type": "干道", "name": "京港澳高速",
    "children": [
        {"type": "支路", "name": "杜家坎", "children": [
            {"type": "路口", "name": "A1", "children": []},
            {"type": "路口", "name": "A2", "children": []},
        ]},
        {"type": "支路", "name": "岳各庄", "children": [
            {"type": "路口", "name": "B1", "children": []},
        ]},
    ],
}


def count_nodes(node):
    """统计本节点及其所有下级节点总数"""
    total = 1                       # 自己算 1 个
    for child in node["children"]:
        total += count_nodes(child)  # 递归处理每个子节点
    return total


def count_leaves(node):
    """统计末端路口数：没有子节点即为路口"""
    if len(node["children"]) == 0:   # 终止条件
        return 1
    total = 0
    for child in node["children"]:
        total += count_leaves(child)  # 递推
    return total


def max_depth(node, depth=1):
    """统计路网层级深度"""
    if len(node["children"]) == 0:
        return depth
    best = depth
    for child in node["children"]:
        d = max_depth(child, depth + 1)
        if d > best:
            best = d
    return best


print("路网节点总数：", count_nodes(road_net))
print("末端路口总数：", count_leaves(road_net))
print("层级深度：", max_depth(road_net))
print("干道直属支路数：", len(road_net["children"]))
