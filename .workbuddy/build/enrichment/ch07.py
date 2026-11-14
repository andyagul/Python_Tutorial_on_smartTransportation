# -*- coding: utf-8 -*-
CHAPTER = "07高级函数"
ITEMS = [
    dict(
        anchor="## 7.2 知识点 7.1　`lambda` 匿名函数",
        sec="7.2",
        demo="demo7-1b",
        principle="""`lambda` 是表达式而不是语句：解释器执行到它就现场创建一个函数对象并把它作为结果返回，所以能直接写在参数位置（如 `key=lambda...`）；它和 `def` 编译出的都是同一种函数对象，区别只在 `lambda` 体被语法限定为「单个表达式」，表达式的值自动成为返回值，因此既不需要也不能写 `return`。为什么不能写语句？赋值、`print` 语句、`if` 块都不产生值，而 lambda 体内只允许求值表达式；想表达分支只能用三元式 `a if cond else b`。`lambda` 不是「更快的函数」也不更高级，它只是「没有名字、用完即弃」的简写：其 `__name__` 恒为 `<lambda>`，出错回溯里看不出用途。常见误解是把它赋给变量 `f = lambda x: ...` 就算「起了名」，其实反而丢掉了可读性这一唯一优势；一旦逻辑需要复用、命名或调试，就该写具名 `def`。""",
        variant="相对随堂示例用 lambda 做数值换算，本变式在 lambda 体内用三元表达式表达分支，并直接作为 `sorted` 的 `key` 就地使用，验证「单表达式」边界与匿名函数 `__name__` 恒为 `<lambda>`。",
        code="""# lambda 体内用三元表达式实现分支，仍是单个表达式
level = lambda v: "超速" if v > 120 else "正常"
print("单次调用：", level(132), level(78))
speeds = [62, 132, 78, 150]
# lambda 作为 sorted 的 key 就地使用：超速(0)排前，组内再按车速
ranked = sorted(speeds, key=lambda v: (0 if v > 120 else 1, v))
print("超速优先的排名：", ranked)
print("匿名函数名：", level.__name__)""",
        steps=[
            "`level(132)` 返回 `超速`、`level(78)` 返回 `正常`，说明三元表达式 `a if 条件 else b` 是表达式、可放进 lambda",
            "`key=lambda v: (0 if v > 120 else 1, v)` 把超速车映射到 `(0, v)`、其余映射到 `(1, v)`，输出 `[132, 150, 62, 78]`",
            "打印 `level.__name__` 得到 `<lambda>`，验证 lambda 没有有意义的名字",
            "试着在 lambda 里写 `x = v + 1` 语句，预期 `SyntaxError`，说明体内只能是表达式",
            "把三元分支改写为等价 `def`，结果与 lambda 一致，说明二者是同一种函数对象",
        ],
        faq=[
            ("lambda 里写赋值/语句报 `SyntaxError`", "lambda 体只允许单个表达式，语句不产生值", "分支改用三元表达式 `a if cond else b`，复杂逻辑改 `def`"),
            ("在 lambda 里加 `return` 报 `invalid syntax`", "表达式的值自动作为返回值，不能写 `return`", "直接写表达式，冒号后不出现 `return`"),
            ("回溯里函数名叫 `<lambda>`，看不出用途", "lambda 的 `__name__` 恒为 `<lambda>`", "需要命名、复用、调试时改写具名 `def`"),
            ("`f = lambda v: print(v)` 调用后拿到 `None`", "`print` 表达式返回 `None`，被当作 lambda 的返回值", "要可见输出应在外部 `print(f(v))`，调试别用 lambda"),
        ],
    ),
    dict(
        anchor="## 7.3 知识点 7.2　`map()` 与 `filter()`",
        sec="7.3",
        demo="demo7-2b",
        principle="""`map` 与 `filter` 返回的都不是列表，而是惰性迭代器：对象内部只保存「函数 + 输入迭代器」的引用，每次 `next()` 才对下一个元素应用 `f`、产出一个结果。这既省内存（不必先生成完整中间列表），也解释了「只能遍历一次」——迭代器有单向游标，走到末尾就耗尽，第二次 `list()` 得到空表。参数顺序为何是函数在前？`map(f, seq)` 把「做什么」放前、「对谁做」放后，与 `filter(f, seq)` 保持一致；二者语义正交：`map` 逐元素变换、个数不变，`filter` 用 `f` 的真值决定去留、个数可能减少。常见误解是以为 `map(...)` 已经「算完了」，其实直接 `print` 只显示 `<map object ...>` 这样的对象描述；要复用结果必须先 `list(...)` 固化成列表。迭代器惰性也意味着 `f` 里对外部状态的副作用会延迟到真正遍历时才发生。""",
        variant="相对随堂示例分别对全量车速做 map 与 filter，本变式迁移为「filter 的结果再喂给 map」的链式处理，并用同一 map 对象遍历两次验证迭代器只能消费一次。",
        code="""# 用一批检测器上报车速演示 filter 筛选与 map 变换
speeds = [62, 132, 78, 150, 95, 118]
over = list(filter(lambda v: v > 120, speeds))        # 筛选：个数减少
labels = list(map(lambda v: str(v) + "限速提醒", over))  # 变换：个数不变
print("超速车速：", over, "共", len(over), "条")
print("提醒文本：", labels)
lazy = map(lambda v: round(v / 3.6, 1), speeds)
first = list(lazy)                         # 迭代器第一次遍历即耗尽
print("首次遍历：", first, "| 原对象类型：", type(lazy).__name__)
print("二次遍历：", list(lazy))""",
        steps=[
            "`filter(lambda v: v > 120, ...)` 只保留 132、150，输出 `共 2 条`，验证筛选会减少元素个数",
            "把 `over` 再传给 `map` 得到 `['132限速提醒', '150限速提醒']`，个数仍为 2，验证变换不改变数量",
            "`lazy = map(...)` 不套 `list()` 时 `type` 为 `map`，此时没有任何元素被真正计算",
            "`first = list(lazy)` 得到 6 个换算值，是第一次也是唯一一次有效遍历",
            "再次 `list(lazy)` 输出 `[]`，验证迭代器游标已到末尾、不能重复消费",
        ],
        faq=[
            ("打印出 `<map object at 0x…>`", "map/filter 返回惰性迭代器，尚未计算", "套 `list(map(...))` 固化后再打印"),
            ("同一个迭代器第二次用变成空列表", "迭代器单向游标走到底即耗尽", "把第一次结果 `list()` 存成列表再复用"),
            ("筛选后结果个数没变", "把 `filter` 误写成 `map`，map 会保留全部元素", "筛选条件用 `filter`，变换用 `map`"),
            ("`TypeError` 或结果全错", "把参数写成 `map(序列, 函数)`，顺序反了", "固定为 `map(函数, 序列)`、`filter(函数, 序列)`"),
        ],
    ),
    dict(
        anchor="## 7.4 知识点 7.3　`sorted(key=)` 与多级排序",
        sec="7.4",
        demo="demo7-3b",
        principle="""`sorted` 采用 DSU（装饰—排序—去装饰）：先对序列每个元素调用一次 `key` 函数得到「比较键」并与原元素配对，再只按键排序，最后剥掉键还原元素。因此 `key` 必须传「函数本身」（`key=len`），写成 `key=len()` 等于先调用一次、把返回值当参数，自然报 `TypeError`；每个元素的键只算一次，这也比两两比较的 `cmp` 更高效。元组 key 能做多级排序，是因为 Python 对元组按字典序比较：先比第 0 项，相等再比第 1 项。想让「某列降序、另一列升序」混排时不能整体 `reverse`（会把两列一起翻），于是对数值列取负号 `-r[2]`，把降序折算进升序比较。`sorted` 还是稳定排序，键相等的元素保持原相对次序，这是「两次 sorted 分主次键」可行的原因；它永远返回新列表，原列表不变，别与原地方法 `lst.sort()`（返回 `None`）混淆。""",
        variant="相对随堂示例用二元组 key 混排车速与排队，本变式迁移为「等级分 + 排队」的三字段元组 key，并追加 `key=len`（函数本身）与「原列表不变」的校验，验证 DSU 机制与 key 不能带括号。",
        code="""# 三字段路段：(名称, 拥堵等级分, 排队长度)，等级分越小越优先
roads = [("京港澳", 3, 320), ("京开", 1, 80), ("机场", 3, 40), ("京承", 1, 120)]
# 元组 key：先按等级升序，同级按排队降序（负号折算）
ranked = sorted(roads, key=lambda r: (r[1], -r[2]))
print("等级优先+排队降序：", ranked)
names = [r[0] for r in ranked]            # 只取排序后的路段名
print("处置顺序：", names)
print("按名称长度排：", sorted(names, key=len))
print("原列表未变：", roads[0])""",
        steps=[
            "`key=lambda r: (r[1], -r[2])` 先比等级分（1 在前），同级用 `-r[2]` 把排队降序折算进升序，得到京承、京开、京港澳、机场",
            "等级分同为 1 时，京承排队 120 大于京开 80，因 `-120 < -80` 而排前，验证负号取反",
            "`sorted(names, key=len)` 得到 `['京承', '京开', '机场', '京港澳']`，注意 `key` 传函数本身 `len` 而非 `len()`",
            "把 `key` 改成 `key=len()` 运行，预期 `TypeError`，验证 key 必须是可调用对象",
            "最后打印 `roads[0]` 仍是 `('京港澳', 3, 320)`，验证 `sorted` 返回新列表、不改原列表",
        ],
        faq=[
            ("`key=len()` 报 `TypeError`", "key 被写成「调用一次的结果」，而不是函数对象", "去掉括号写 `key=len`，让 sorted 对每个元素调用"),
            ("第二列仍是升序、混排失败", "元组 key 里没对降序列取负号", "数值列写 `-r[2]`，或分两次稳定 `sorted`"),
            ("`TypeError: bad operand type for unary -`", "对字符串字段用了负号", "负号只用于数值；字符串列降序改两次稳定排序"),
            ("排序后原列表也被改了", "误用 `lst.sort()`（原地、返回 `None`）", "需要新列表就用 `sorted()`"),
        ],
    ),
    dict(
        anchor="## 7.5 知识点 7.4　`zip()` 配对",
        sec="7.5",
        demo="demo7-4b",
        principle="""`zip(a, b)` 返回一个迭代器，内部持有对各输入序列的迭代器；每次 `next()` 从每个序列各取一个元素组装成元组，只要任一序列耗尽就立即抛 `StopIteration` 结束。可见「以最短为准」并非容错设计，而是迭代协议的必然结果：长序列多出的元素根本没机会被取用，Python 也不会报错提示丢弃，所以这是最隐蔽的数据丢失来源，配对前务必 `len()` 校验。`dict(zip(k, v))` 之所以成立，是因为 `dict()` 接受「可迭代的键值对」，而 zip 恰好产出二元组序列，键列表与值列表便自然拼成字典。内存视角上，只有 `list(zip(...))` 才一次性物化全部元组，在此之前 zip 对象只占固定小空间。常见误解是把 zip 当成「两两组合/笛卡尔积」，其实它只做「对齐配对」，要组合得用嵌套循环。""",
        variant="相对随堂示例用两个等长序列配对，本变式迁移为三序列 zip、`dict(zip(...))` 成字典，并故意让第二序列变短，验证「以最短为准静默截断」及配对前长度校验的必要性。",
        code="""plates = ["京A12345", "京B67890", "津C24680", "冀D11223"]
speeds = [62, 132, 78, 150]
lanes = [2, 3, 1, 2]
# 三序列 zip：按下标组装成 (车牌, 车速, 车道)
records = list(zip(plates, speeds, lanes))
print("配对记录：", records)
print("车牌→车速字典：", dict(zip(plates, speeds)))
print("长度校验：", len(plates) == len(speeds) == len(lanes))
short = list(zip(plates, speeds[:2]))     # 第二个序列只有 2 个
print("最短截断后：", short, "共", len(short), "条")""",
        steps=[
            "`list(zip(plates, speeds, lanes))` 得到 4 个三元组，每个按下标把车牌、车速、车道对齐",
            "`dict(zip(plates, speeds))` 得到 4 个键值对的字典，验证 zip 产物可直接喂给 `dict()`",
            "`len(plates) == len(speeds) == len(lanes)` 输出 `True`，这是防止静默截断的前置校验",
            "把 `speeds[:2]` 传入 zip，只得到 2 条记录且无任何报错，验证以最短序列为准",
            "直接 `print(zip(...))` 会显示 `<zip object …>`，必须 `list()` 才能看到内容",
        ],
        faq=[
            ("记录少了几条却没有任何报错", "两序列长度不一致，zip 以最短为准静默截断", "配对前先 `len(a) == len(b)` 校验"),
            ("打印出 `<zip object at 0x…>`", "zip 返回迭代器，未物化", "用 `list(zip(...))` 或 `dict(zip(...))` 转换"),
            ("复用同一个 zip 对象第二次为空", "迭代器一次性消费", "转成列表保存后再多次使用"),
            ("以为是两两组合，结果只有 4 条", "zip 是对齐配对，不是笛卡尔积", "要组合用嵌套 `for`"),
        ],
    ),
    dict(
        anchor="## 7.6 知识点 7.5　装饰器与高阶函数",
        sec="7.6",
        demo="demo7-5b",
        principle="""装饰器能「不改原函数加行为」，根源是函数为一等对象：`def` 把函数对象绑定到名字，而 `@log_call` 在定义完成后立刻执行 `calc_density = log_call(calc_density)`，把名字重新绑定到装饰器返回的新函数 `wrapper`。闭包让 `wrapper` 记住外层的 `func`，即便 `log_call` 已返回，原函数仍被引用着；此后调用 `calc_density(...)` 实际是在调 `wrapper`，先做前置处理再 `func(*args, **kwargs)` 转交。`wrapper` 必须用可变参数原样「打包再拆包透传」，才能适配任意被装饰函数的签名；且必须 `return func(...)`，否则原函数结果在 wrapper 里被丢弃、调用方拿到 `None`。常见误解是以为 `@` 有什么魔法，它只是赋值语法糖；被装饰后 `func.__name__` 变成 `wrapper`，也正说明「函数名」只是引用，不是函数对象的固有身份。""",
        variant="相对随堂示例的计数型装饰器，本变式迁移为「打印透传参数与被装饰后函数名」的观察型装饰器，验证 `*args/**kwargs` 原样透传、必须 `return func(...)`、以及 `@` 把名字重绑到 wrapper 后 `__name__` 变为 `wrapper`。",
        code="""def deco(func):                                  # 高阶函数：接收原函数
    def wrapper(*a, **kw):                       # 新函数，包住原函数
        print("前置：", func.__name__, a, kw)
        return func(*a, **kw)                    # 必须返回原函数结果
    return wrapper
@deco                                            # 语法糖：等价于 fee = deco(fee)
def fee(km, rate=0.5, discount=1.0):
    return round(km * rate * discount, 2)
print("费用：", fee(120, discount=0.9))
print("被装饰后名字：", fee.__name__)""",
        steps=[
            "调用 `fee(120, discount=0.9)` 先打印 `前置： fee (120,) {'discount': 0.9}`，说明位置实参进 `a`、关键字实参进 `kw`",
            "wrapper 内 `return func(*a, **kw)` 拆包转交原函数，输出 `费用： 54.0`，验证返回值没被吞掉",
            "打印 `fee.__name__` 得到 `wrapper`，验证 `@deco` 等价于 `fee = deco(fee)`、名字已指向新函数",
            "把 `return func(*a, **kw)` 改成只写 `func(*a, **kw)`，调用会得到 `None`，验证必须返回原函数结果",
            "把 `wrapper(*a, **kw)` 写死成 `wrapper(km)`，再用 `discount=` 调用会报 `TypeError`，验证必须用可变参数透传",
        ],
        faq=[
            ("调用被装饰函数得到 `None`", "wrapper 里漏了 `return func(...)`，结果被丢弃", "在 wrapper 内 `return func(*args, **kwargs)`"),
            ("`TypeError: got an unexpected keyword argument`", "wrapper 参数写死，无法接收关键字实参", "用 `wrapper(*args, **kwargs)` 原样透传"),
            ("被装饰后 `__name__` 变成 `wrapper`", "`@` 已把名字重绑到新函数对象", "知道名字只是引用即可；保留元信息可用 `functools.wraps`（进阶）"),
            ("多个被装饰函数计数互相串味", "计数器用了全局变量，被所有 wrapper 共享", "把计数挂在各自的 `wrapper.calls` 上"),
            ("被装饰函数变成 `None`、调用报 `TypeError`", "装饰器末尾忘记 `return wrapper`", "装饰器必须返回新函数对象"),
        ],
    ),
]
