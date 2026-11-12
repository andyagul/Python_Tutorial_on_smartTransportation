# ---------- 第 03 章 流程控制 · 案例 3-1：路口拥堵等级判定 ----------
# 对应知识点：3.1 if / elif / else 与缩进、2.5 逻辑运算符 and
# 功能说明：按平均车速与车流密度判定拥堵等级，并给出对应的配时与诱导处置建议

# 根据平均车速与车流密度判定拥堵等级
speed = eval(input("路段平均车速(km/h)："))
density = eval(input("车流密度(辆/km)："))

if speed >= 60 and density < 10:
    level = "畅通"
    advice = "保持当前配时方案"
elif speed >= 40:
    level = "缓行"
    advice = "主干道绿灯延长 5 秒"
elif speed >= 20:
    level = "拥堵"
    advice = "启动绿波协调，发布绕行提示"
else:
    level = "严重拥堵"
    advice = "发布一级诱导，通知警力现场疏导"

print("平均车速：", speed, "km/h")
print("车流密度：", density, "辆/km")
print("拥堵等级：", level)
print("处置建议：", advice)
