# ---------- 第 09 章 异常处理 · 练习 9-1 参考答案：日志行解析的多异常捕获 ----------
# 对应知识点：9.2 try / except / else、9.3 except ... as e 与多异常、9.5 容错跳过
# 功能说明：解析日志行；字段不足抛 IndexError、车速非数字抛 ValueError，均返回空值继续处理

def parse_line(line):
    """返回 (车牌, 车速)，解析失败返回 (None, None)"""
    try:
        parts = line.split("|")
        plate = parts[1]              # 字段不足时抛 IndexError
        speed = int(parts[2])         # 非数字时抛 ValueError
    except IndexError:
        print("  [错误] 字段数不足：", line)
        return None, None
    except ValueError:
        print("  [错误] 车速不是整数：", line)
        return None, None
    else:
        return plate, speed


logs = [
    "08:15:32|京A12345|62",
    "08:16:02|京B67890",              # 缺字段
    "08:16:32|津C24680|快",           # 车速非数字
    "08:17:02|冀D11223|78",
    "08:17:32|京E55667|150",
]

ok = 0
fail = 0
for line in logs:
    plate, speed = parse_line(line)
    if plate is None:
        fail += 1
    else:
        ok += 1
        print("  解析成功：", plate, speed, "km/h")
    print("-" * 30)

print("成功", ok, "条，失败", fail, "条")
