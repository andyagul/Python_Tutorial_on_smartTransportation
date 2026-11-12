# ---------- 第 06 章 函数 · 练习 6-2 参考答案：函数拆分重构拥堵播报 ----------
# 对应知识点：6.1 定义与调用、6.3 返回值、6.4 不依赖全局变量、3.1 分支
# 功能说明：把「判定等级—给出建议—拼装播报」拆成三个函数，循环批量生成 5 条路段播报

def judge_level(speed):
    if speed >= 60:
        return "畅通"
    elif speed >= 40:
        return "缓行"
    elif speed >= 20:
        return "拥堵"
    return "严重拥堵"


def advice(level):
    if level == "畅通":
        return "保持当前配时"
    elif level == "缓行":
        return "绿灯延长 5 秒"
    elif level == "拥堵":
        return "启动绿波协调，发布绕行提示"
    return "发布一级诱导，通知警力现场疏导"


def build_report(road, speed):
    level = judge_level(speed)
    return road + " | " + level + " | " + advice(level)


roads = ["京港澳 K12", "京开 K8", "机场高速 K3", "京承 K20", "五环西段"]
speeds = [66, 45, 28, 15, 52]

for i in range(len(roads)):
    print(build_report(roads[i], speeds[i]))
