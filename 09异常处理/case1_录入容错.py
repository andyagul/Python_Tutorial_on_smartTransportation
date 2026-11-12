# ---------- 第 09 章 异常处理 · 案例 9-1：交通参数录入的容错处理 ----------
# 对应知识点：9.1 ValueError / ZeroDivisionError、9.2 try / except / else / finally 完整结构
# 功能说明：用同一段代码演练三种情形：正常录入、路段长度为 0、车道数输入非数字

print("=== 路段参数录入 ===")

try:
    length = eval(input("路段长度(km)："))
    lanes = int(input("车道数："))
    cars = int(input("车辆数："))

    density = cars / (length * lanes)      # 长度为 0 时触发除零
    capacity = 2200 * lanes

except ValueError:
    print("[错误] 输入的不是有效数字，请重新录入")
except ZeroDivisionError:
    print("[错误] 路段长度或车道数不能为 0")
else:
    # 只有 try 内全部成功才会执行
    print("车流密度：", round(density, 2), "辆/(km·车道)")
    print("通行能力：", capacity, "辆/h")
    if density > 25:
        print("提示：密度偏高，建议现场复核")
finally:
    print("=== 本次录入结束 ===")
