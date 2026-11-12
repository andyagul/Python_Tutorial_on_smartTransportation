# ---------- 第 09 章 异常处理 · 练习 9-2 参考答案：批量录入中的异常跳过 ----------
# 对应知识点：9.4 raise 主动抛出、9.5 用 continue 跳过坏数据、9.2 多异常捕获
# 功能说明：批量校验 6 条车速数据，非数字或超范围的记录跳过，汇总有效数据与平均值

raw = ["62", "abc", "-5", "118", "999", "78"]

valid = []
total = 0

for item in raw:
    try:
        speed = int(item)
        if speed < 0:
            raise ValueError("车速不能为负数")
        if speed > 300:
            raise ValueError("车速超过 300，疑似单位错误")
    except ValueError as e:
        print("[跳过]", item, "->", e)
        continue
    valid.append(speed)
    total += speed

print("有效数据：", valid)
print("有效条数：", len(valid), "| 无效条数：", len(raw) - len(valid))
if len(valid) > 0:
    print("有效平均车速：", round(total / len(valid), 1), "km/h")
else:
    print("无有效数据，无法计算平均值")
