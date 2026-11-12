#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
67 个知识点的「随堂示例」代码库。

字段说明：
- ch    章节目录名
- sec   章节内的节号（用于定位插入位置，如 "1.2"）
- kp    知识点编号（如 "1.1"）
- title 示例标题（写入小标题）
- point 核心要点（一两句话说明本示例验证什么）
- code  可直接运行的示例代码（含中文注释，不依赖输入、不依赖图形界面、结果确定）
"""

DEMOS = [
    # ==================== 第 01 章 ====================
    dict(ch="01初识Python世界", sec="1.2", kp="1.1",
         title="四种 print 写法一次跑通",
         point="验证 `print()` 的四种基本写法：单引号、双引号、多参数（自动补空格）、空参数（输出空行），并确认引号本身不会出现在输出里。",
         code='''\
# 单引号与双引号等价，引号本身不会输出
print('限速 60')
print("车道 2 畅通")

# 多参数用逗号分隔，输出时自动补一个空格
print("京A12345", "62", "km/h")

# 空参数：只输出一个空行
print()

# 空字符串：同样输出一个空行
print("")
print("（上面第 4、5 条 print 各产生一个空行）")'''),

    dict(ch="01初识Python世界", sec="1.3", kp="1.2",
         title="注释不参与运行",
         point="验证三类注释的实际效果：独立成行的注释、行尾注释、被注释掉的语句都不产生输出，只有未被注释的 `print` 才输出。",
         code='''\
# 这是独立成行的注释，Python 直接跳过
print("提示：前方施工，请减速")      # 行尾注释：说明本行含义
# print("这行被注释掉了，不会输出")
print("注释不影响程序结果")          # 三条 print 只生效两条'''),

    dict(ch="01初识Python世界", sec="1.4", kp="1.3",
         title="转义字符与多行字符串",
         point="验证 `\\n`（换行）、`\\t`（制表）、`\\\\`（一个反斜杠）与三引号多行字符串的输出差异，重点是路径中的反斜杠必须写两个。",
         code=r'''# \n：在一条 print 内换行
print("自检完成\n系统正常")

# \t：制表位，让三列起点对齐
print("车牌\t时间\t车道")
print("京A12345\t08:15\t2")

# \\：输出一个反斜杠；若只写一个 \t，路径会被"吃掉"
print("日志路径：D:\\traffic\\log.csv")

# 三引号：源码换行即输出换行，收尾引号紧贴文字
print("""【入场须知】
一、限速 5 km/h
二、限高 2.1 m""")'''),

    dict(ch="01初识Python世界", sec="1.5", kp="1.4",
         title="分隔线与两列对齐",
         point="验证手工排版的三条规则：上下分隔线字符数相同、标题两侧补空格居中、表头与数据行的 `\\t` 数量一致。",
         code='''\
# 上下分隔线用相同数量的等号，版式才不歪
print("==============================")
print("        智慧交通出行提示")
print("==============================")

# 表头与数据行都用一个 \t 分隔两列
print("车牌号码\t车位编号")
print("京A12345\tB-013")
print("京B67890\tA-042")

# 换一种字符做次级分隔，形成视觉层次
print("------------------------------")
print("发布单位：市交通运行监测中心")'''),

    dict(ch="01初识Python世界", sec="1.6", kp="1.5",
         title="最小可运行程序的结构",
         point="验证一个 `.py` 文件的最小结构：文件头注释说明用途、若干 `print` 产生可见输出、末尾给出完成提示。能看到这几行输出，就说明文件保存、编码与运行三步都正确。",
         code='''\
# 文件名：hello.py（UTF-8 编码）
# 运行方式：在本文件所在目录执行  python hello.py
print("程序开始运行")          # 第 1 行输出：证明文件确实被执行
print("Hello, 智慧交通")       # 第 2 行输出：程序主体
print("运行结束，无报错")      # 第 3 行输出：程序正常走完'''),

    # ==================== 第 02 章 ====================
    dict(ch="02变量与数据类型", sec="2.2", kp="2.1",
         title="变量是贴了标签的盒子",
         point="验证变量的三件事：用 `=` 赋值、用变量名取值、重新赋值会覆盖旧值；同时观察变量的命名要能看出含义。",
         code='''\
road = "京港澳 K12"      # 字符串变量：路段名
lanes = 3                # 整数变量：车道数
speed = 62.5             # 浮点变量：平均车速

print(road, "|", lanes, "车道 |", speed, "km/h")

lanes = 4                # 重新赋值：变量改指向新值 4
print("调整后车道数：", lanes)
print("通行能力：", lanes * 2200, "辆/h")'''),

    dict(ch="02变量与数据类型", sec="2.3", kp="2.2",
         title="四种基本类型与 type()",
         point="用 `type()` 逐个确认 `str` / `int` / `float` / `bool` 四种类型，并验证同一运算符在不同类型上的行为差异（数字相加是求和，字符串相加是拼接）。",
         code='''\
plate = "京A12345"       # str
lanes = 3                # int
speed = 62.5             # float
jam = True               # bool

print(type(plate), type(lanes), type(speed), type(jam))

# 同样的 + 号，类型不同结果完全不同
print("3 + 2 =", 3 + 2)
print("3.0 + 2 =", 3.0 + 2)
print("『京A』+『12345』=", "京A" + "12345")'''),

    dict(ch="02变量与数据类型", sec="2.4", kp="2.3",
         title="input() 拿到的是字符串",
         point="验证 `input()` 的返回值恒为 `str`，必须用 `int()` / `float()` / `eval()` 转换后才能参与算术；这里用字面量模拟用户输入，避免课堂上等待输入。",
         code='''\
raw = "62"                    # 模拟 input() 收到的内容
print(raw, type(raw))         # 是字符串，不是数字

speed = int(raw)              # 转成整数
print(speed, type(speed))

length = eval("2.5")          # eval 按字面量转换：带小数点就是 float
print(length, type(length))

# 转换为数字后才能计算
print("两倍路段长：", round(length * 2, 1), "km")'''),

    dict(ch="02变量与数据类型", sec="2.5", kp="2.4",
         title="// 与 % 拆分信号周期",
         point="验证整除 `//`（取商的整数部分）与取余 `%`（取不够一份的余数）的配合用法，这是「平均分配 + 余数补给」这类业务的通用写法。",
         code='''\
cycle = 130          # 信号周期总时长（秒）
share = 4            # 主干道 : 支路 = 3 : 1，共 4 份

print("普通除法：", cycle / share)
print("整除：", cycle // share)
print("取余：", cycle % share)

base = cycle // share        # 每份基础时长：向下取整
rest = cycle % share         # 除不尽的余数：单独补给主干道
main_green = base * 3 + rest # 主干道拿 3 份，再吃下余数
side_green = base            # 支路拿 1 份
print("主干道绿灯：", main_green, "秒")
print("支路绿灯：", side_green, "秒")
print("合计：", main_green + side_green, "秒（正好等于周期）")'''),

    dict(ch="02变量与数据类型", sec="2.6", kp="2.5",
         title="比较与逻辑运算产出布尔值",
         point="验证比较运算返回 `bool`，再用 `and` / `or` / `not` 组合成复合条件——这正是第 3 章 `if` 语句的判断依据。",
         code='''\
speed = 45           # 车速（km/h）
density = 8          # 车流密度（辆/(km·车道)）

print("车速 ≥ 60：", speed >= 60)              # False
print("密度 < 10：", density < 10)              # True
print("两个条件同时满足：", speed >= 60 and density < 10)   # False
print("任一条件满足：", speed >= 60 or density < 10)        # True
print("对结果取反：", not (speed >= 60))        # True
print("类型是：", type(speed >= 60))'''),

    dict(ch="02变量与数据类型", sec="2.7", kp="2.6",
         title="round() 控制有效位数",
         point="验证 `round(x, n)` 的第二参数可以是正数（保留小数位）、0（取整）、负数（对整数位取整），并注意浮点误差导致个别结果与直觉不同。",
         code='''\
density = 96 / (2.5 * 3)
print("原始值：", density)
print("保留 2 位：", round(density, 2))
print("保留 0 位：", round(density))
print("对十位取整：", round(density, -1))

# 浮点误差：2.675 在内存中略小于 2.675
print("round(2.675, 2) =", round(2.675, 2))'''),

    # ==================== 第 03 章 ====================
    dict(ch="03流程控制", sec="3.2", kp="3.1",
         title="四档拥堵分级",
         point="验证 `if-elif-else` 自顶向下逐条判断、命中即跳出：同一份数据只会落进一个分支，`else` 兜住所有剩余情况。",
         code='''\
speed = 35

if speed >= 60:
    level = "畅通"
elif speed >= 40:
    level = "缓行"
elif speed >= 20:
    level = "拥堵"
else:
    level = "严重拥堵"

print("车速", speed, "km/h →", level)
print("提示：elif 的顺序决定结果，改动顺序会改变分级")'''),

    dict(ch="03流程控制", sec="3.3", kp="3.2",
         title="用三元写法一行定等级",
         point="验证条件表达式 `A if 条件 else B` 的求值方式：条件为真取前者，为假取后者；适合「二选一」的赋值，不适合三个以上分支。",
         code='''\
speed = 72

level = "畅通" if speed >= 60 else "非畅通"
print("等级：", level)

# 三元写法也可以直接嵌在计算里
green = 30 if level == "畅通" else 50
print("绿灯时长：", green, "秒")

# 两个分支都要求值一次，因此适合简单判断
print("是否超速：", "是" if speed > 120 else "否")'''),

    dict(ch="03流程控制", sec="3.4", kp="3.3",
         title="range() 的三个参数",
         point="验证 `range(start, stop, step)` 的左闭右开特性（不含 `stop`）、步长作用，以及用循环变量参与计算得到逐行结果。",
         code='''\
total = 0
for hour in range(6, 13, 2):        # 6,8,10,12：不含 13
    flow = hour * 100               # 用循环变量算出一个"车流量"
    total += flow
    print(hour, "时 车流", flow, "辆")

print("合计：", total, "辆")
print("循环次数：", len(range(6, 13, 2)))'''),

    dict(ch="03流程控制", sec="3.5", kp="3.4",
         title="while + break + 循环 else",
         point="验证三件事：`while` 由条件控制次数、`break` 立即跳出整个循环、循环 `else` 只在「未被 `break` 中断」时执行。",
         code='''\
def dispatch(queue, limit, per_min):
    """每分钟放行 per_min 辆；超过 limit 分钟则转人工"""
    minute = 0
    while queue > 0:                 # 条件为真才继续循环
        minute += 1
        queue = max(queue - per_min, 0)      # 不会减成负数
        print("  第", minute, "分钟，剩余", queue, "辆")
        if minute >= limit:
            print("  等待超时，转人工疏导")
            break                    # 立即跳出整个循环
    else:                            # 只有「未被 break 中断」才执行
        print("  排队已清空，共耗时", minute, "分钟")

print("【情形一】排队 6 辆，限 3 分钟：")
dispatch(6, 3, 3)                    # 2 分钟清空 → 走 else

print("【情形二】排队 10 辆，限 3 分钟：")
dispatch(10, 3, 3)                   # 3 分钟未清空 → 走 break'''),

    dict(ch="03流程控制", sec="3.6", kp="3.5",
         title="嵌套循环打印车道占用网格",
         point="验证「外层管行、内层管列」的嵌套结构，并强调两个易错点：每行开始要重置拼接变量，整行拼完再输出一次。",
         code='''\
lanes = 3
slots = 4
occupied = 2                 # 每车道前 2 个车位已占用

for lane in range(1, lanes + 1):        # 外层：逐条车道
    line = ""                           # 每行开始必须重置
    for slot in range(1, slots + 1):    # 内层：逐个车位
        if slot <= occupied:
            line += "[X]"
        else:
            line += "[ ]"
    print("第", lane, "车道：", line)    # 整行拼完再输出'''),

    # ==================== 第 04 章 ====================
    dict(ch="04字符串与输入输出", sec="4.2", kp="4.1",
         title="用索引与切片拆车牌",
         point="验证字符串下标从 0 开始、负数下标从末尾数、切片 `[start:stop]` 不含 `stop`，并用 `len()` 判断长度。",
         code='''\
plate = "京A12345"

print("长度：", len(plate))
print("第 1 位（下标 0）：", plate[0])
print("最后 1 位（下标 -1）：", plate[-1])
print("发牌机关（下标 1）：", plate[1])
print("号牌序号（2 到末尾）：", plate[2:])
print("前 3 位：", plate[:3])
print("后 3 位：", plate[-3:])'''),

    dict(ch="04字符串与输入输出", sec="4.3", kp="4.2",
         title="清洗一条带空白的车牌",
         point="验证 `strip()` 只去首尾空白、`upper()` 统一大小写、`replace()` 替换内容；三者可以链式调用，且都不改变原字符串。",
         code='''\
raw = "  京a12345  "          # 设备上报时带空格、字母小写
clean = raw.strip().upper()   # 先清洗再去大小写差异

print("原始：[" + raw + "]")
print("清洗：[" + clean + "]")
print("长度：", len(raw), "→", len(clean))
print("替换后：", clean.replace("京A", "京B"))
print("原字符串是否被改动：[" + raw + "]")     # 仍是原样，字符串不可变'''),

    dict(ch="04字符串与输入输出", sec="4.4", kp="4.3",
         title="判断关键词是否存在",
         point="验证 `in` 返回布尔、`find()` 返回位置（找不到返回 -1 而不是报错）、`startswith()` / `endswith()` 判断首尾，这四者是字符串检索的基本组合。",
         code='''\
name = "京港澳高速 K12"

print("包含『高速』：", "高速" in name)
print("『K12』的位置：", name.find("K12"))
print("查找不存在的词：", name.find("隧道"))
print("以『京』开头：", name.startswith("京"))
print("以『高速』结尾：", name.endswith("高速"))
print("『高速』出现次数：", name.count("高速"))'''),

    dict(ch="04字符串与输入输出", sec="4.5", kp="4.4",
         title="split() 拆字段、join() 拼回去",
         point="验证 `split(分隔符)` 得到列表（分隔符本身不保留）、`join()` 用指定字符把列表拼成字符串，二者互为逆操作。",
         code='''\
line = "08:15:32|京A12345|62|2"

parts = line.split("|")
print("切分结果：", parts)
print("字段数：", len(parts))
print("第 2 个字段（下标 1）：", parts[1])

print("前两段用 - 连接：", "-".join(parts[0:2]))
print("全部用逗号连接：", ",".join(parts))'''),

    dict(ch="04字符串与输入输出", sec="4.6", kp="4.5",
         title="三种格式化写法的对齐效果",
         point="验证同一张两列表格用 `f-string`、`%`、`format()` 三种写法都能实现；其中 `:<n` 左对齐补空格、`:>n` 右对齐、`:.1f` 控制小数位。",
         code='''\
road = "京开"
speed = 43.5

# 1) f-string：宽度与精度都写在花括号里
print(f"{'路段':<8}{'车速':>8}")
print(f"{road:<8}{speed:>8.1f}")

# 2) 百分号写法：类型符 %s / %.1f
print("百分号：%s / %.1f km/h" % (road, speed))

# 3) format() 写法：用 {} 占位
print("format：{} / {:.1f} km/h".format(road, speed))'''),

    # ==================== 第 05 章 ====================
    dict(ch="05列表元组集合与字典", sec="5.2", kp="5.1",
         title="队列的入队、插队与放行",
         point="验证列表四个高频方法的分工：`append()` 尾部追加、`insert(i, x)` 指定位置插入、`pop()` 取出并删除、`remove(x)` 按值删除。",
         code='''\
queue = ["京A12345", "京B67890"]
print("初始队列：", queue)

queue.append("津C24680")          # 队尾加入
queue.insert(0, "冀D11223")       # 插到队首（应急车辆优先）
print("插入后：", queue, "| 共", len(queue), "辆")

left = queue.pop(0)               # 放行队首
print("放行：", left, "| 剩余：", queue)

queue.remove("京B67890")          # 按车牌剔除异常车辆
print("剔除后：", queue)'''),

    dict(ch="05列表元组集合与字典", sec="5.3", kp="5.2",
         title="sort() 与 sorted() 的区别",
         point="验证 `sort()` 原地排序且返回 `None`、`sorted()` 返回新列表不动原列表；同时用 `sum` / `max` / `min` 做统计。",
         code='''\
flows = [820, 1100, 760]

print("总量：", sum(flows), "| 最大：", max(flows), "| 最小：", min(flows))
print("峰值下标：", flows.index(max(flows)))

flows.sort()                      # 原地升序，返回 None
print("sort 后原列表：", flows)
print("sort 的返回值：", flows.sort())

ranked = sorted(flows, reverse=True)   # 返回新列表
print("sorted 降序：", ranked)
print("原列表仍是：", flows)'''),

    dict(ch="05列表元组集合与字典", sec="5.4", kp="5.3",
         title="元组：不可变的固定参数",
         point="验证元组用下标访问与切片读取，但**不能修改元素**；单元素元组必须写逗号，否则只是加了括号的普通值。",
         code='''\
cross = ("京港澳 K12", 39.9042, 116.4074)
print("点位：", cross[0])
print("纬度：", cross[1], "| 经度：", cross[2])
print("字段数：", len(cross))

# 元组不可改：下面这行一旦取消注释就会报 TypeError
# cross[0] = "京开 K8"

single = (62,)            # 有逗号才是元组
not_tuple = (62)          # 没有逗号只是整数
print("单元素元组：", single, type(single))
print("加括号的整数：", not_tuple, type(not_tuple))'''),

    dict(ch="05列表元组集合与字典", sec="5.5", kp="5.4",
         title="集合去重与交并差",
         point="验证集合自动去重（无序、不重复），以及交集 `&`、并集 `|`、差集 `-` 的语义——这是比对两个时段过车记录的标准写法。",
         code='''\
this_hour = ["京A12345", "京B67890", "京A12345"]
a = set(this_hour)
print("原始条数：", len(this_hour), "→ 去重后：", len(a))

b = {"京B67890", "津C24680"}
print("本时段车辆：", sorted(a))
print("上时段车辆：", sorted(b))
print("两时段都出现（交集）：", sorted(a & b))
print("任一时段出现（并集）：", sorted(a | b))
print("仅本时段新增（差集）：", sorted(a - b))'''),

    dict(ch="05列表元组集合与字典", sec="5.6", kp="5.5",
         title="字典：按路段查路况",
         point="验证字典「键—值」的增、查、默认值 `get()` 与遍历 `items()`；重点体会 `[]` 取不到键会报错，而 `get()` 可以给默认值。",
         code='''\
status = {"京开": "缓行", "机场": "畅通"}

status["京港澳"] = "拥堵"            # 新增键值对
print("路段数：", len(status))
print("京开的状态：", status["京开"])

# get()：键不存在时返回默认值，不报错
print("京承（get）：", status.get("京承", "无数据"))

print("逐条遍历：")
for road, level in status.items():
    print("  ", road, "→", level)'''),

    dict(ch="05列表元组集合与字典", sec="5.7", kp="5.6",
         title="列表推导式一行完成筛选与换算",
         point="验证推导式 `[表达式 for 变量 in 序列 if 条件]` 的三个位置各自的作用：表达式决定元素形态、`if` 决定保留哪些元素。",
         code='''\
flows = [820, 1100, 760, 1650]

over = [f for f in flows if f > 1000]
print("超 1000 的时段：", over, "| 共", len(over), "个")

half = [f // 100 for f in flows]
print("折合百辆：", half)

labels = ["高" if f > 1500 else "平" for f in flows]
print("等级标记：", labels)'''),

    # ==================== 第 06 章 ====================
    dict(ch="06函数", sec="6.2", kp="6.1",
         title="从定义到调用的最小函数",
         point="验证 `def` 定义、按位置传参、默认参数生效，以及文档字符串可通过 `函数名.__doc__` 读回。",
         code='''\
def capacity(lanes, per_lane=2200):
    """计算理论通行能力：车道数 × 单车道能力"""
    return lanes * per_lane

print("3 车道：", capacity(3))                 # 使用默认 per_lane
print("2 车道（匝道 1800）：", capacity(2, 1800))  # 覆盖默认值
print("函数说明：", capacity.__doc__)'''),

    dict(ch="06函数", sec="6.3", kp="6.2",
         title="四类参数放在同一个函数里",
         point="验证位置参数、默认参数、可变参数 `*extra`、关键字参数 `discount=` 一次协作：`*extra` 把多余的位置实参收成元组，关键字实参必须写在最后。",
         code='''\
def fee(km, rate=0.5, *extra, discount=1.0):
    """位置 + 默认 + 可变 + 关键字，四类参数一次演示"""
    print("里程：", km, "| 费率：", rate)
    print("额外标记：", extra, "| 折扣：", discount)
    return round(km * rate * discount, 2)

print("默认调用：", fee(120))
print("完整调用：", fee(120, 0.6, "夜间", "ETC", discount=0.95))'''),

    dict(ch="06函数", sec="6.4", kp="6.3",
         title="返回多个值并按位置解包",
         point="验证 `return a, b, c` 实际返回一个元组，调用方可用三个变量一次解包；也可用下标只取其中一个。",
         code='''\
def report(road, cars, length_km, lanes):
    """返回三个值：站点、密度、等级"""
    d = round(cars / (length_km * lanes), 2)
    level = "畅通" if d < 10 else "缓行"
    return road, d, level

site, dens, level = report("京港澳 K12", 96, 2.5, 3)
print("站点：", site)
print("密度：", dens, "辆/(km·车道)")
print("等级：", level)

print("只取密度：", report("京开 K8", 30, 2, 2)[1])'''),

    dict(ch="06函数", sec="6.5", kp="6.4",
         title="局部变量与全局变量互不干扰",
         point="验证函数内部的变量是局部的，函数结束后即消失；函数外定义的同名变量不会被函数内部修改（除非显式声明 `global`，本章不使用）。",
         code='''\
total = 0                     # 全局变量

def calc(n):
    total = n * 2             # 这里是新的局部变量，与全局同名但无关
    inner = "函数内可见"
    return total, inner

value, note = calc(5)
print("函数返回：", value, note)
print("全局 total 仍为：", total)

# 局部变量在函数外不存在，取消下一行注释会报 NameError
# print(inner)'''),

    dict(ch="06函数", sec="6.6", kp="6.5",
         title="递归统计路网末端节点",
         point="验证递归三要素：终止条件（没有子节点即返回 1）、递推（对每个子节点调用自身）、回归（累加子结果）。",
         code='''\
net = {
    "name": "京港澳干道",
    "children": [
        {"name": "杜家坎", "children": [
            {"name": "A1", "children": []},
            {"name": "A2", "children": []},
        ]},
        {"name": "岳各庄", "children": [
            {"name": "B1", "children": []},
        ]},
    ],
}

def count_leaves(node):
    """递归统计末端路口数"""
    if len(node["children"]) == 0:      # 终止条件
        return 1
    total = 0
    for child in node["children"]:
        total += count_leaves(child)    # 递推
    return total

print("末端路口数：", count_leaves(net))
print("干道直属支路：", len(net["children"]))'''),

    # ==================== 第 07 章 ====================
    dict(ch="07高级函数", sec="7.2", kp="7.1",
         title="lambda 就是没有名字的小函数",
         point="验证 `lambda 参数: 表达式` 只能写一个表达式、自动返回结果，常作为 `key=` 或 `map()` 的参数就地使用。",
         code='''\
to_ms = lambda v: round(v / 3.6, 1)
print("72 km/h →", to_ms(72), "m/s")
print("108 km/h →", to_ms(108), "m/s")

pairs = [("京A", 62), ("京B", 132), ("津C", 78)]
print("按车速降序：", sorted(pairs, key=lambda p: p[1], reverse=True))

# 等价的 def 写法，对比可读性
def to_ms2(v):
    return round(v / 3.6, 1)

print("两种写法结果一致：", to_ms(72) == to_ms2(72))'''),

    dict(ch="07高级函数", sec="7.3", kp="7.2",
         title="map 转换、filter 筛选",
         point="验证 `map()` 对每个元素做同一变换、`filter()` 只保留条件为真的元素；两者都返回迭代器，必须套 `list()` 才能看到内容。",
         code='''\
speeds = [62, 118, 132, 78]

ms = list(map(lambda v: round(v / 3.6, 1), speeds))
print("换算 m/s：", ms)

over = list(filter(lambda v: v > 120, speeds))
print("超速车速：", over, "| 辆数：", len(over))
print("超速率：", round(len(over) / len(speeds) * 100, 1), "%")

# 不套 list() 时拿到的是迭代器：只占位置、还没算
lazy = map(str, speeds)
print("不套 list() 的类型：", type(lazy))
print("套上 list() 才有内容：", list(lazy))'''),

    dict(ch="07高级函数", sec="7.4", kp="7.3",
         title="多关键字排序：元组 key 与负号",
         point="验证 `sorted(key=...)` 的 key 返回元组时按元组顺序逐级比较，以及用 `-` 取反实现「某一列降序、另一列升序」的混排。",
         code='''\
roads = [("京港澳", 45, 320), ("京开", 62, 80), ("机场", 45, 40)]

by_queue = sorted(roads, key=lambda r: r[2], reverse=True)
print("按排队降序：", by_queue)

# 车速升序；车速相同时排队长的在前
by_speed = sorted(roads, key=lambda r: (r[1], -r[2]))
print("车速升序+排队降序：", by_speed)

print("最拥堵：", by_queue[0][0], by_queue[0][2], "m")
print("原列表未被修改：", roads)'''),

    dict(ch="07高级函数", sec="7.5", kp="7.4",
         title="zip 把两个列表配对",
         point="验证 `zip()` 按位置把多个序列打包成元组，长度以最短的为准；配合 `for` 可同时取出车牌与车速。",
         code='''\
plates = ["京A12345", "京B67890", "津C24680"]
speeds = [62, 132, 78]

pairs = list(zip(plates, speeds))
print("配对结果：", pairs)
print("配对数：", len(pairs))

for plate, speed in pairs:
    if speed > 120:                  # 两个分支各自输出，不带多余空格
        print(plate, "→", speed, "km/h（超速）")
    else:
        print(plate, "→", speed, "km/h")'''),

    dict(ch="07高级函数", sec="7.6", kp="7.5",
         title="装饰器：不改原函数就加日志",
         point="验证装饰器的工作方式：`@log_call` 把函数替换为 `wrapper`，调用时先执行附加逻辑再执行原函数；计数器挂在 `wrapper` 属性上，因此能跨多次调用累计。",
         code='''\
def log_call(func):
    """记录被装饰函数被调用的次数"""
    def wrapper(*args, **kwargs):
        wrapper.calls += 1
        print("[日志] 第", wrapper.calls, "次调用", func.__name__, "参数", args)
        return func(*args, **kwargs)
    wrapper.calls = 0
    return wrapper

@log_call
def density(cars, length_km, lanes):
    return round(cars / (length_km * lanes), 2)

print("结果：", density(96, 2.5, 3))
print("结果：", density(120, 3, 2))
print("累计调用次数：", density.calls)'''),

    # ==================== 第 08 章 ====================
    dict(ch="08文件操作", sec="8.2", kp="8.1",
         title="w / a / r 三种模式的实际差别",
         point="用同一文件连续演示三种模式：`w` 清空后写入、`a` 追加到末尾、`r` 读取；关键在于 `w` 会覆盖原内容，`a` 不会。",
         code='''\
with open("demo8_mode.txt", "w", encoding="utf-8") as f:   # w：新建或清空
    f.write("820\\n")

with open("demo8_mode.txt", "a", encoding="utf-8") as f:   # a：末尾追加
    f.write("1100\\n")

with open("demo8_mode.txt", "r", encoding="utf-8") as f:   # r：读取
    print("文件内容：")
    print(f.read(), end="")'''),

    dict(ch="08文件操作", sec="8.3", kp="8.2",
         title="read / readline / readlines 三种读法",
         point="验证三种读取方式的返回形态：`read()` 得到整段字符串、`readline()` 得到一行、`readlines()` 得到按行切分的列表；文件指针只前进不回退。",
         code='''\
with open("demo8_read.txt", "w", encoding="utf-8") as f:
    f.write("06:00,820\\n08:00,1100\\n10:00,760\\n")

with open("demo8_read.txt", encoding="utf-8") as f:
    print("read() 全文：")
    print(f.read(), end="")

with open("demo8_read.txt", encoding="utf-8") as f:
    print("readline() 首行：", f.readline().strip())
    print("readline() 次行：", f.readline().strip())

with open("demo8_read.txt", encoding="utf-8") as f:
    lines = f.readlines()
print("readlines() 共", len(lines), "行；末行：", lines[-1].strip())'''),

    dict(ch="08文件操作", sec="8.4", kp="8.3",
         title="写入必须自己补换行",
         point="验证 `write()` 不会自动换行：不写 `\\n` 时多行会粘连成一行；写完后读回校验行数，是最直接的确认手段。",
         code='''\
rows = ["06:00,820", "08:00,1100", "10:00,760"]

with open("demo8_write.txt", "w", encoding="utf-8") as f:
    for r in rows:
        f.write(r + "\\n")        # 每行自己补换行

with open("demo8_write.txt", encoding="utf-8") as f:
    lines = f.readlines()
print("行数：", len(lines))
print("首行：", lines[0].strip())
print("末行：", lines[-1].strip())'''),

    dict(ch="08文件操作", sec="8.5", kp="8.4",
         title="with 自动关闭与 encoding 防乱码",
         point="验证 `with` 语句块结束时自动关闭文件（`f.closed` 变为 `True`），以及 `encoding=「utf-8」` 保证中文读写一致。",
         code='''\
with open("demo8_with.txt", "w", encoding="utf-8") as f:
    f.write("路段,流量\\n京开,1100\\n")
    print("块内是否关闭：", f.closed)

print("块外是否关闭：", f.closed)          # with 结束自动关闭

with open("demo8_with.txt", encoding="utf-8") as f:
    print(f.read(), end="")'''),

    dict(ch="08文件操作", sec="8.6", kp="8.5",
         title="手工拼 CSV 并逐行解析",
         point="验证 CSV 的本质：用逗号连接字段、每行一条记录。写出时 `join()` 拼行，读回时 `split(\「,\」)` 拆字段，无需第三方库。",
         code='''\
rows = [("时段", "流量"), ("06:00", 820), ("08:00", 1100)]

with open("demo8_csv.csv", "w", encoding="utf-8") as f:
    for r in rows:
        f.write(",".join(map(str, r)) + "\\n")

total = 0
with open("demo8_csv.csv", encoding="utf-8") as f:
    for line in f:
        parts = line.strip().split(",")
        print("字段：", parts)
        if parts[1].isdigit():        # 跳过表头
            total += int(parts[1])

print("流量合计：", total)'''),

    # ==================== 第 09 章 ====================
    dict(ch="09异常处理", sec="9.2", kp="9.1",
         title="四类常见异常分别是什么样",
         point="逐个触发 `ValueError` / `ZeroDivisionError` / `IndexError` / `KeyError`，用 `as e` 打印异常自带的说明，建立「按类型捕获」的直觉。",
         code='''\
try:
    int("abc")                     # 字符串转不成数字
except ValueError as e:
    print("ValueError：", e)

try:
    1 / 0                          # 除数为零
except ZeroDivisionError as e:
    print("ZeroDivisionError：", e)

try:
    [1, 2][5]                      # 下标越界
except IndexError as e:
    print("IndexError：", e)

try:
    {"a": 1}["b"]                  # 键不存在
except KeyError as e:
    print("KeyError：", e)'''),

    dict(ch="09异常处理", sec="9.3", kp="9.2",
         title="try / except / else / finally 的执行次序",
         point="验证四个子句的分工：`try` 放可能出错的代码、`except` 只在出错时执行、`else` 只在**没出错**时执行、`finally` 无论成败都执行。",
         code='''\
def divide(a, b):
    try:
        result = a / b
    except ZeroDivisionError:
        print("[出错] 除数不能为 0")
        return None
    else:
        print("[成功] 结果 =", result)
        return result
    finally:
        print("—— 本次计算结束 ——")

divide(10, 4)
print()
divide(10, 0)'''),

    dict(ch="09异常处理", sec="9.4", kp="9.3",
         title="一个 except 捕获多种异常",
         point="验证 `except (A, B) as e` 的写法可同时捕获多类异常，并用 `type(e).__name__` 区分实际发生的类型；`else` 用于「没出错时」的正常处理。",
         code='''\
def parse(item):
    try:
        speed = int(item)
        if speed > 300:
            raise ValueError("车速超出 0~300")
    except (ValueError, TypeError) as e:
        print("跳过", item, "→", type(e).__name__, ":", e)
        return None
    else:
        print("录入成功：", speed)
        return speed

for v in ["62", "abc", "999"]:
    parse(v)'''),

    dict(ch="09异常处理", sec="9.5", kp="9.4",
         title="assert 断言与 raise 主动抛出",
         point="验证两者差别：`assert` 用于「必须成立的前提」，失败抛 `AssertionError`；`raise` 用于「业务规则不允许的情况」，可指定异常类型与提示。",
         code='''\
def check_speed(speed):
    assert isinstance(speed, (int, float)), "车速必须是数字"
    if speed < 0 or speed > 300:
        raise ValueError("车速超出 0~300：" + str(speed))
    return "通过"

for v in [62, 320, "快"]:
    try:
        print(v, "→", check_speed(v))
    except AssertionError as e:
        print(v, "→ 断言失败：", e)
    except ValueError as e:
        print(v, "→ 数值非法：", e)'''),

    dict(ch="09异常处理", sec="9.6", kp="9.5",
         title="坏数据跳过、好数据继续",
         point="验证容错模式的标准骨架：`try` 内解析、`except` 内记录原因并用 `continue` 跳过，循环不中断，最终只汇总有效数据。",
         code='''\
raw = ["62", "abc", "-5", "118"]

valid = []
for item in raw:
    try:
        speed = int(item)
        if speed < 0:
            raise ValueError("车速不能为负数")
    except ValueError as e:
        print("[跳过]", item, "原因：", e)
        continue                    # 跳过本条，继续下一条
    valid.append(speed)

print("有效数据：", valid)
print("有效", len(valid), "条，无效", len(raw) - len(valid), "条")
print("有效平均车速：", round(sum(valid) / len(valid), 1), "km/h")'''),

    # ==================== 第 10 章 ====================
    dict(ch="10模块与程序包", sec="10.2", kp="10.1",
         title="三种导入形式与调用写法",
         point="验证三种导入写法的差别：`import 模块` 要加模块名前缀、`from 模块 import 名称` 可直接用、`import 模块 as 别名` 可简化长名字。",
         code='''\
import math                        # 形式一：导入整个模块
from math import sqrt              # 形式二：只导入一个函数
import random as rd                # 形式三：导入并起别名

print("math.ceil(3.2)：", math.ceil(3.2))
print("sqrt(16)：", sqrt(16))       # 不需要写 math.

rd.seed(2026)                      # 固定种子，结果可复现
print("rd.randint(1, 10)：", rd.randint(1, 10))'''),

    dict(ch="10模块与程序包", sec="10.3", kp="10.2",
         title="用 __doc__ 读取模块说明",
         point="验证模块开头的三引号字符串就是模块文档，可用 `模块.__doc__` 读取；自定义模块与标准库遵循完全相同的规则（案例 10-1 会新建 `traffic_utils.py` 验证）。",
         code='''\
import math

print("模块全名：", math.__name__)
print("文档首行：", math.__doc__.strip().splitlines()[0])
print("模块内常量 pi：", round(math.pi, 4))

# dir() 会把 __doc__ 这类内部名称一并列出，需过滤掉下划线开头的
public = [n for n in dir(math) if not n.startswith("_")]
print("按字母序的前 6 个公开名称：", public[:6])'''),

    dict(ch="10模块与程序包", sec="10.4", kp="10.3",
         title="看 __name__ 判断运行方式",
         point="验证 `__name__` 的取值规律：直接运行（含 Notebook 单元格）时为 `\「__main__\」`，被其他文件导入时才是模块名。这就是「自测代码只在直接运行时执行」的原理。",
         code='''\
print("当前 __name__ 的值：", __name__)

if __name__ == "__main__":
    print("→ 直接运行：以下自测代码会执行")
else:
    print("→ 被导入：以下自测代码不会执行")

print("—— 自测开始 ——")
print("通行能力 3 车道：", 3 * 2200, "辆/h")'''),

    dict(ch="10模块与程序包", sec="10.5", kp="10.4",
         title="random 与 datetime 的常用组合",
         point="验证标准库的两类高频用法：`random` 生成模拟数据（固定 `seed` 便于批改）、`datetime` 做日期推算与格式化，都不需要安装第三方包。",
         code='''\
import random
import datetime

random.seed(20261029)              # 固定种子：每次运行结果一致
roads = ["京港澳", "京开", "机场高速"]
print("随机路段：", random.choice(roads))
print("随机流量：", random.randint(600, 1800))
print("随机车速：", round(random.uniform(15, 85), 1))

d = datetime.date(2026, 11, 12)
print("日期：", d, "| 明天：", d + datetime.timedelta(days=1))
print("格式化：", d.strftime("%Y年%m月%d日"))'''),

    dict(ch="10模块与程序包", sec="10.6", kp="10.5",
         title="包与模块的层级命名",
         point="验证「包是带 `__init__.py` 的目录，模块全名用点号表示层级」；包内 `from . import calc` 中的 `.` 就指当前包，因此包必须用 `python -m` 方式运行。",
         code='''\
import xml.etree.ElementTree as ET      # 标准库中的三层结构：包.子包.模块

print("模块全名：", ET.__name__)
print("所属包：", ET.__package__)
print("名称层级数：", ET.__name__.count(".") + 1)
print("说明：包内 from . import calc 的 . 即当前包")'''),

    # ==================== 第 11 章 ====================
    dict(ch="11面向对象编程上", sec="11.2", kp="11.1",
         title="先造对象，再挂属性",
         point="验证「类是模板、对象是实例」：`Vehicle()` 每次实例化都产生独立对象，给其中一个挂属性不会影响另一个。",
         code='''\
class Vehicle:
    """车辆类：暂时只是个空模板"""

v1 = Vehicle()
v1.plate = "京A12345"
v2 = Vehicle()
v2.plate = "京B67890"

print("v1：", v1.plate)
print("v2：", v2.plate)
print("类型：", type(v1).__name__)
print("两个是不同对象：", v1 is not v2)'''),

    dict(ch="11面向对象编程上", sec="11.3", kp="11.2",
         title="__init__ 在实例化时自动执行",
         point="验证 `__init__` 的调用时机（`Vehicle(...)` 时自动执行）与 `self` 的含义（指代刚创建的那个对象）；`实例.__dict__` 可看到属性表。",
         code='''\
class Vehicle:
    def __init__(self, plate, speed=0):
        self.plate = plate          # self 指向当前实例
        self.speed = speed

v = Vehicle("京A12345", 62)
print("车牌：", v.plate, "| 车速：", v.speed)
print("属性表：", v.__dict__)

default = Vehicle("京B67890")       # 使用默认 speed=0
print("默认车速：", default.speed)'''),

    dict(ch="11面向对象编程上", sec="11.4", kp="11.3",
         title="类属性共享、实例属性独立",
         point="验证类属性由所有实例共享（用于计数最典型）、实例属性各自独立；通过类名或实例都能读到类属性。",
         code='''\
class Vehicle:
    total = 0                       # 类属性：所有实例共享

    def __init__(self, plate):
        self.plate = plate          # 实例属性：各自独立
        Vehicle.total += 1          # 每造一辆车，计数加一

a = Vehicle("京A12345")
b = Vehicle("京B67890")

print("a.plate：", a.plate, "| b.plate：", b.plate)
print("Vehicle.total：", Vehicle.total)
print("通过实例读取类属性：", a.total)
print("a 的属性表只有 plate：", a.__dict__)'''),

    dict(ch="11面向对象编程上", sec="11.5", kp="11.4",
         title="方法返回值与 __str__ 的区别",
         point="验证三种输出路径：普通方法返回字符串需自己 `print`、`__str__` 决定 `print(对象)` 的显示、`str(对象)` 与 `print` 等价。",
         code='''\
class Vehicle:
    def __init__(self, plate, speed):
        self.plate = plate
        self.speed = speed

    def info(self):
        return self.plate + " " + str(self.speed) + " km/h"

    def __str__(self):
        return "Vehicle<" + self.plate + ">"

v = Vehicle("京A12345", 62)
print(v.info())            # 普通方法返回字符串：必须自己 print
print(v)                   # print 对象 → 自动调用 __str__
print(str(v))              # 显式 str() → 同样走 __str__，结果一致'''),

    dict(ch="11面向对象编程上", sec="11.6", kp="11.5",
         title="私有属性只经受控方法修改",
         point="验证 `__green` 这类双下划线属性在类外不可直接访问（`hasattr` 为 `False`），只能通过公有的 `get` / `set` 方法读写，从而把校验逻辑收进类内。",
         code='''\
class TrafficLight:
    def __init__(self, green):
        self.__green = green        # 私有属性

    def get_green(self):
        return self.__green

    def set_green(self, seconds):
        if 5 <= seconds <= 120:
            self.__green = seconds
            return True
        print("[拒绝] 绿灯时长必须在 5~120 秒")
        return False

light = TrafficLight(35)
print("当前绿灯：", light.get_green())
print("改为 45：", light.set_green(45), "→", light.get_green())
print("改为 200：", light.set_green(200), "→", light.get_green())
print("类外能直接访问吗：", hasattr(light, "__green"))'''),

    # ==================== 第 12 章 ====================
    dict(ch="12面向对象编程下", sec="12.2", kp="12.1",
         title="封装：把约束放进方法里",
         point="验证封装的价值：外部只调方法、不碰属性，区间约束（0~120）只在类内写一次，任何调用方都无法绕过。",
         code='''\
class Vehicle:
    def __init__(self, plate, speed=0):
        self.plate = plate
        self.__speed = speed

    def accelerate(self, delta):
        self.__speed = min(self.__speed + delta, 120)   # 上限约束在类内
        return self.__speed

    def get_speed(self):
        return self.__speed

v = Vehicle("京A12345", 100)
print("初始车速：", v.get_speed())
print("加速 50：", v.accelerate(50), "（被限制在 120）")
print("再加速 30：", v.accelerate(30))'''),

    dict(ch="12面向对象编程下", sec="12.3", kp="12.2",
         title="继承：子类复用父类能力",
         point="验证 `class 子类(父类)` 自动获得父类方法，`super().__init__()` 复用父类初始化；`isinstance()` 认定子类对象同时属于父类。",
         code='''\
class Vehicle:
    def __init__(self, plate):
        self.plate = plate

    def limit(self):
        return 120

    def info(self):
        return self.plate + " 限速 " + str(self.limit()) + " km/h"

class Truck(Vehicle):
    def __init__(self, plate, load):
        super().__init__(plate)         # 复用父类初始化
        self.load = load

    def limit(self):
        return 80                       # 重写：货车限速更低

t = Truck("京B67890", 18)
print(t.info())
print("载重：", t.load, "吨")
print("是 Vehicle 的实例吗：", isinstance(t, Vehicle))'''),

    dict(ch="12面向对象编程下", sec="12.4", kp="12.3",
         title="方法重写：替换与扩展",
         point="验证重写的两种形态：完全替换（直接给新实现）与扩展（先 `super()` 取父类结果再加工），二者对外接口保持一致。",
         code='''\
class Vehicle:
    def fee(self, km, rate=0.5):
        return round(km * rate, 2)

class Bus(Vehicle):
    def fee(self, km, rate=0.5):
        return round(km * rate * 1.2, 2)     # 替换：直接新实现

class Truck(Vehicle):
    def fee(self, km, rate=0.5):
        base = super().fee(km, rate)         # 扩展：先取父类结果
        return round(base * 1.8, 2)

print("小客车 120km：", Vehicle().fee(120))
print("客车   120km：", Bus().fee(120))
print("货车   120km：", Truck().fee(120))'''),

    dict(ch="12面向对象编程下", sec="12.5", kp="12.4",
         title="多态：同一接口，不同实现",
         point="验证多态：调用方只写 `device.run()`，具体执行哪段代码由对象类型决定，因此新增设备时主循环无需改动。",
         code='''\
class Device:
    def run(self):
        raise NotImplementedError("子类必须实现 run()")

class Light(Device):
    def run(self):
        return "信号灯：切换相位"

class Board(Device):
    def run(self):
        return "情报板：刷新提示"

class Barrier(Device):
    def run(self):
        return "道闸：抬杆放行"

for d in [Light(), Board(), Barrier()]:
    print(d.run())          # 同一句调用，各自执行

try:
    Device().run()          # 基类未实现，直接调用会报错
except NotImplementedError as e:
    print("基类直接调用：", e)'''),

    dict(ch="12面向对象编程下", sec="12.6", kp="12.5",
         title="isinstance 与 type 的取舍",
         point="验证二者差异：`isinstance()` 沿继承链判断（子类对象也算父类），`type()` 只认精确类型；接口判断用前者更安全。",
         code='''\
class Vehicle:
    pass

class Truck(Vehicle):
    pass

t = Truck()
print("type(t).__name__：", type(t).__name__)
print("isinstance(t, Truck)：", isinstance(t, Truck))
print("isinstance(t, Vehicle)：", isinstance(t, Vehicle))
print("type(t) is Vehicle：", type(t) is Vehicle)

items = [Vehicle(), Truck()]
for x in items:
    print(type(x).__name__, "是 Vehicle 吗：", isinstance(x, Vehicle))'''),

    # ==================== 第 13 章 ====================
    dict(ch="13综合项目实战", sec="13.2", kp="13.1",
         title="屏幕坐标 ↔ turtle 坐标换算",
         point="验证两套坐标系的差别：屏幕以左上角为原点、y 向下；turtle 以窗口中心为原点、y 向上。示例用纯计算演示换算，不弹窗即可看到结果。",
         code='''\
W, H = 640, 480

def to_turtle(px, py):
    """把"左上角原点、y 向下"的像素坐标换算为 turtle 坐标"""
    return px - W / 2, H / 2 - py

print("屏幕中心 (320, 240) →", to_turtle(320, 240))
print("屏幕左上 (0, 0)     →", to_turtle(0, 0))
print("屏幕右下 (640, 480) →", to_turtle(640, 480))
print("道路中线 y=240 的 turtle y：", to_turtle(0, 240)[1])'''),

    dict(ch="13综合项目实战", sec="13.3", kp="13.2",
         title="矩形的四个顶点与填充路径",
         point="验证 `rect()` 的填充路径怎么给：4 个顶点按顺时针排列，坐标规律是「x 加宽、y 加高」，中心点等于两组对角的平均值；列出的 4 个点尚未回到起点，最后那条边由 `end_fill()` 自动闭合。",
         code='''\
def rect_corners(x, y, w, h):
    """以 (x, y) 为左下角，按顺时针返回填充路径的 4 个顶点"""
    return [(x, y), (x + w, y), (x + w, y + h), (x, y + h)]

corners = rect_corners(-100, -50, 200, 100)
for i, p in enumerate(corners, start=1):
    print("顶点", i, "：", p)

# 4 个点只走完一圈，末点还没回到起点：最后那条边由 end_fill() 自动闭合
print("末点与起点重合吗：", corners[-1] == corners[0])
print("缺的那条边：从", corners[-1], "回到", corners[0])
print("中心坐标：", ((corners[0][0] + corners[2][0]) / 2,
                    (corners[0][1] + corners[2][1]) / 2))'''),

    dict(ch="13综合项目实战", sec="13.4", kp="13.3",
         title="tracer(0) + update() 的刷新节奏",
         point="验证动画原理：关闭自动刷新后，每次改完内容只调用一次 `update()`，一秒一帧；若忘记 `clear()`，上一帧的数字会与新的叠加。",
         code='''\
# 对应 screen.tracer(0)：先关掉自动刷新
frame = 0
for s in range(3, 0, -1):
    frame += 1
    # 对应 text.clear() + text.write(str(s))
    print("第", frame, "帧：重画数字", s, "→ 调用 update() 刷新")
print("倒计时结束：重画提示「绿灯放行」→ 调用 update()")

# 若不清屏，数字会叠加：这里用字符串模拟"叠加"效果
overlay = ""
for s in range(3, 0, -1):
    overlay += str(s)
print("忘记 clear() 的结果：", overlay)'''),

    dict(ch="13综合项目实战", sec="13.5", kp="13.4",
         title="用 dt 让位移与帧率解耦",
         point="验证时间驱动位移：每帧位移 = 速度 × `dt`，而 `dt` 来自 `clock.tick(FPS)`；这样换机器、掉帧都不会改变实际行驶速度。示例用固定 `dt` 演算，不打开窗口。",
         code='''\
FPS = 60
GREEN_T = 0.05                 # 为便于演示，把绿灯压缩到 3 帧
dt = 1 / FPS                   # 每帧时长（秒）

speed = 3.0                    # 像素/帧
timer = 0.0
state = "green"
x = 0.0

for frame in range(1, 7):
    timer += dt
    if timer >= GREEN_T:
        timer = 0
        state = "yellow" if state == "green" else "green"
    x += speed * 60 * dt       # 位移 = 速度 × 60 × dt
    print("第", frame, "帧  相位", state, "  x =", round(x, 2))'''),

    dict(ch="13综合项目实战", sec="13.6", kp="13.5",
         title="矩形重叠判定与计分",
         point="验证碰撞检测的本质是两组区间同时重叠，等价于 `pygame.Rect.colliderect()`；碰撞后扣分、未碰撞不加分，与案例的计分逻辑一致（示例不依赖 pygame）。",
         code='''\
def overlap(a, b):
    """两个矩形是否重叠：a、b 均为 (x, y, w, h)，等价于 colliderect()"""
    ax, ay, aw, ah = a
    bx, by, bw, bh = b
    return ax < bx + bw and bx < ax + aw and ay < by + bh and by < ay + ah

car1 = (100, 175, 40, 30)      # 前车
car2 = (120, 175, 40, 30)      # 后车：与 car1 重叠 → 追尾
car3 = (200, 175, 40, 30)      # 第三辆：与前车有间距

score = 0
if overlap(car1, car2):
    print("car1 与 car2 重叠 → 判定追尾，扣 5 分")
    score -= 5
else:
    print("car1 与 car2 未重叠 → 正常通行")

if overlap(car1, car3):
    print("car1 与 car3 重叠 → 扣 5 分")
    score -= 5
else:
    print("car1 与 car3 未重叠 → 得分不变")

print("最终得分：", score)'''),
]
