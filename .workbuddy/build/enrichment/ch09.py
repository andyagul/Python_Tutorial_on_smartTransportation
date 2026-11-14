# -*- coding: utf-8 -*-
CHAPTER = "09异常处理"
ITEMS = [
    dict(
        anchor="## 9.2 知识点 9.1　异常概念与六种常见类型",
        sec="9.2",
        demo="demo9-1b",
        principle="""Python 把异常实现为类，所有内置异常都继承自 `BaseException`，日常捕获的 `ValueError`、`IndexError` 等又继承自 `Exception`。`except 类型` 的匹配本质是按 `isinstance` 的子类关系自外向内比对，所以把父类写在前面会吞掉后面的子类分支，这是 `except Exception` 必须垫底的原因。异常抛出后解释器做栈展开：沿调用链逐层回退，寻找能匹配的处理块，一找到就停止；若一路没人接，最外层解释器打印 `Traceback` 并以非零码退出。对空字段调用 `int` 抛 `ValueError` 而非 `TypeError`，是因为参数类型合法、只是值无法解析——类型检查发生在转换逻辑之前。理解「异常是一个带类型与信息的对象」而非「一段报错文字」，才能明白为何能用 `as e` 把它接住、读取 `str(e)` 并写进日志，而 `AttributeError`、`NameError` 这类编码缺陷不该靠捕获掩盖。""",
        variant="""把 demo9-1 的四条独立 try 逐个触发收进一个解析函数与一条循环，对一批卡口日志逐条分类，验证异常类型可用 `type(e).__name__` 区分、且单条失败不会中断整批。""",
        code="""# 卡口日志 时间|车牌|车速：把逐个触发改为逐条分类诊断
def parse(line):
    try:
        speed = int(line.split("|")[2])     # 缺字段抛 IndexError，空字段抛 ValueError
        return "录入 " + str(speed) + " km/h"
    except (IndexError, ValueError) as e:
        return type(e).__name__ + "：" + str(e)
for line in ["08:15|京A|62", "08:16|京B", "08:17|津C|", "08:18|冀D|78"]:
    print(line, "->", parse(line))
print("四条均返回结果，异常未逃逸、程序未中断")
""",
        steps=[
            "运行代码，核对首行 `08:15|京A|62 -> 录入 62 km/h`，说明该条日志三个字段齐全、转换成功。",
            "核对第二条 `08:16|京B` 的输出以 `IndexError` 开头，因为切分后只有两个字段、取下标 2 越界。",
            "核对第三条 `08:17|津C|` 的输出以 `ValueError` 开头且信息里带空串标记，验证空字段触发的是值错误而非类型错误。",
            "核对第四条 `08:18|冀D|78 -> 录入 78 km/h`，说明坏数据之后的好数据仍被处理、循环未中断。",
            "把 `except (IndexError, ValueError)` 改成只留 `ValueError` 重跑，`08:16|京B` 的 `IndexError` 将逃逸并导致非零退出码，体会按类型列全的必要性。",
        ],
        faq=[
            ("对空串调用 `int` 却想靠 `TypeError` 兜住，异常仍逃逸", "空串类型合法、只是值无法解析，抛的是 `ValueError`", "改捕获 `ValueError`；类型不匹配才用 `TypeError`"),
            ("列表取 `parts[2]` 越界却写了 `except KeyError`", "`IndexError` 归序列下标、`KeyError` 归字典键，二者不互换", "列表用 `IndexError`、字典用 `KeyError`，按容器选类型"),
            ("写了 `except Exception` 后具体分支不再执行", "父类按子类关系先匹配，会吞掉后面的具体类型", "具体类型在前、`Exception` 垫底，避免一把抓"),
        ],
    ),
    dict(
        anchor="## 9.3 知识点 9.2　`try` / `except` / `else` / `finally`",
        sec="9.3",
        demo="demo9-2b",
        principle="""`try` 并非把代码包起来就安全：解释器为它维护一张异常处理表，一旦块内抛错就跳到表中登记的第一个匹配 `except`；`else` 只在无异常时执行，是因为它被编译成正常路径尾部的续接块，异常路径会直接绕过它。`finally` 最特殊，编译器会把它的代码复制到正常、异常、`return`、`break` 等每一条出口之前，因此无论中途是否返回、是否抛错都必然执行——这正是收尾用 `finally`、成功逻辑用 `else` 的底层原因。一个常见误解是以为 `return` 能跳过 `finally`：实际返回值会先被暂存，`finally` 执行完才真正交还调用者；若 `finally` 里自己写了 `return`，还会覆盖暂存值。把 `try` 范围收小，本质是让异常表更精确，出错时 `Traceback` 才能指到真正的语句，而不是笼统地指向整个程序。""",
        variant="""把 demo9-2 的两次调用看打印改为用列表 `seq` 记录子句命中顺序，验证正常只走 `else`、异常只走 `except`、两种情况都追加 `finally`。""",
        code="""# 记录四个子句的执行时机：正常走 else，异常走 except，两者都走 finally
seq = []
def calc(a, b):
    try:
        r = a / b
    except ZeroDivisionError: seq.append("except")
    else: seq.append("else")
    finally: seq.append("finally")
    return 0 if b == 0 else round(r, 1)
print("结果：", calc(96, 2.5), calc(96, 0), "| 子句序列：", seq)
""",
        steps=[
            "运行后核对结果一行为 `38.4 0`：96/2.5 保留一位是 38.4，除零那次按 `b == 0` 返回 0。",
            "核对子句序列为 `['else', 'finally', 'except', 'finally']`，第一次调用命中 `else`、第二次命中 `except`。",
            "数出 `finally` 共出现 2 次，与调用次数相等，验证它无论成功失败都执行。",
            "把 `96 / 0` 换成 `96 / 2` 重跑，序列会变成两次 `['else', 'finally']`，`except` 一次也不出现。",
            "把 `return 0 if b == 0 else round(r, 1)` 改成无条件 `round(r, 1)`，除零那次会因 `r` 未赋值抛 `NameError`，反证条件表达式的惰性求值保护了异常分支。",
        ],
        faq=[
            ("把成功后的输出写进 `try`，出错路径也跟着执行", "成功逻辑与监控代码混在一起，异常时行为难控", "把成功逻辑移到 `else`，`try` 只放可能出错的语句"),
            ("用 `else` 代替 `finally` 做收尾，异常时收尾没执行", "`else` 只在无异常时执行，异常路径会绕过它", "收尾一律放 `finally`，它才保证始终执行"),
            ("把 `try-else` 当成 `for-else` 理解", "两者的否则含义不同：`for-else` 是未被 `break` 才执行", "记住 `try-else` 是 `try` 内无异常才执行"),
        ],
    ),
    dict(
        anchor="## 9.4 知识点 9.3　`except ... as e` 与多异常捕获",
        sec="9.4",
        demo="demo9-3b",
        principle="""`except 类型 as e` 里的 `e` 只在 `except` 块内有效：Python 3 在块结束时会主动 `del e`，目的是断开异常对象到回溯对象、再到栈帧与局部变量的引用环，让内存及时回收，否则 `Traceback` 会一直拽着整条调用栈不放。因此想把诊断留到后面，应存 `str(e)` 或 `type(e).__name__` 这样的值，而不是保存 `e` 本身。`except (A, B) as e` 的括号不是列表而是异常元组，解释器逐个做类型匹配；写成 `except A, B:` 在 Python 3 会被当作旧语法而报错。另一层误解是捕获即消失：不写 `raise` 时异常确实被消化、流程继续，但它携带的栈信息也随之丢弃，所以关键日志应在 `except` 内当场记录，而不是等块外再补。""",
        variant="""把 demo9-3 的元组合并捕获改为两条 `except` 按类型分别给不同诊断语，验证 `as e` 取出的信息可用于分类提示、两类异常各走各的分支。""",
        code="""# 同样的坏数据改用两个 except 分别处理，验证按类型给不同提示语
def parse(rec):
    try:
        return "通过 " + str(int(rec.split("|")[1]))
    except IndexError:
        return "字段不足：缺少车速列"
    except ValueError as e:
        return "车速非数字：" + str(e)
for rec in ["京A|62", "京B|快", "京C", "冀D|78"]:
    print(rec, "->", parse(rec))
""",
        steps=[
            "运行代码，核对 `京A|62 -> 通过 62`，说明两段字段且车速为整数时走成功返回。",
            "核对 `京B|快` 输出以车速非数字开头，命中 `except ValueError as e`，`str(e)` 里含 `invalid literal`。",
            "核对 `京C` 输出为字段不足：缺少车速列，命中前面的 `except IndexError`，证明两条分支按类型分流。",
            "核对 `冀D|78 -> 通过 78`，坏数据之后流程继续，未因异常中断。",
            "把两个 `except` 合并成 `except (IndexError, ValueError):` 重跑，两类坏数据会共用同一句提示，验证分开写才能给不同诊断语。",
        ],
        faq=[
            ("`except ValueError, IndexError:` 报语法错", "元组漏了圆括号，Python 3 不再支持 Python 2 的逗号写法", "写成 `except (ValueError, IndexError) as e:`"),
            ("只捕获一种异常，另一种一来程序就中断", "未列出的异常类型没有匹配分支，继续向上抛出", "按实际可能列出全部预期类型"),
            ("`as e` 接了却没用，日志只有笼统一句", "未读取 `e` 的信息，丢失了具体诊断文本", "打印 `type(e).__name__` 与 `str(e)` 写进日志"),
        ],
    ),
    dict(
        anchor="## 9.5 知识点 9.4　`raise` 与 `assert`",
        sec="9.5",
        demo="demo9-4b",
        principle="""`assert 条件, 提示` 在字节码层面大致等价于条件不成立时 `raise AssertionError(提示)`，但关键差别是它受 `__debug__` 开关控制：以 `python -O` 运行时编译器会整段丢弃 `assert`，连条件都不求值。所以断言适合表达代码内部必然成立的前提（如入口参数类型），绝不能用来挡文件、网络、用户输入带来的脏数据——生产校验必须写成 `if + raise ValueError(...)`，它是不可被优化掉的普通控制流。`raise` 后既可跟异常类（解释器自动实例化）也可跟实例；一旦执行，当前块后续语句全部不可达，控制流立刻转入栈展开。讲义强调的内层抛、外层接，本质是把发现问题与决定处置解耦：校验函数只管抛，调用方才决定拒绝、跳过还是记日志，同一套校验因此能被不同流程复用。""",
        variant="""把 demo9-4 的单函数内 try 加多分支拆成内层 check 只抛、外层循环里的 try 按类型接的分层结构，验证 `assert` 抛 `AssertionError`、`raise` 抛指定类型且都不逃逸。""",
        code="""# 分层校验：内层 assert 守类型、raise 守范围，外层按类型分别接住
def check(v):
    assert isinstance(v, int), "车速必须是整数"
    if v < 0 or v > 300: raise ValueError("车速越界：" + str(v))
    return "通过 " + str(v)
for v in [62, 320, "快"]:
    try: print(v, "->", check(v))
    except AssertionError as e: print(v, "-> AssertionError：", e)
    except ValueError as e: print(v, "-> ValueError：", e)
""",
        steps=[
            "运行代码，核对 `62 -> 通过 62`，说明 `assert` 与 `raise` 两条防线都未触发。",
            "核对 `320` 走 `ValueError` 分支并带车速越界：320，是 `if + raise` 主动抛出后被循环内的 `except` 接住。",
            "核对 `快` 走 `AssertionError` 分支、提示车速必须是整数，抛出类型与上一行不同。",
            "核对三行输入都打印了结果、没有 `Traceback`，说明内层 `check` 抛出的异常都在外层被消化、循环未中断。",
            "把 `assert` 那行改成类型不符时 `raise TypeError` 并重跑，`快` 会改走 `TypeError` 分支，体会断言与主动抛出在类型及 `-O` 下的差别。",
        ],
        faq=[
            ("用 `assert` 挡用户输入，加了 `-O` 后校验消失", "`assert` 受 `__debug__` 控制，优化模式下被整段丢弃", "生产校验用 `if + raise ValueError(...)`，不用断言"),
            ("抛 `Exception` 且提示语笼统，调用方无法精确捕获", "抛出类型过于宽泛，调用方只能一把抓", "抛具体类型并带上具体值与期望范围"),
            ("`raise` 后面还写了赋值语句却从不生效", "`raise` 立刻转入栈展开，同一块后续语句不可达", "把代码删掉或移到 `else` 与函数外"),
        ],
    ),
    dict(
        anchor="## 9.6 知识点 9.5　容错模式：跳过坏数据、继续处理",
        sec="9.6",
        demo="demo9-5b",
        principle="""容错模式的要害不在 `except` 怎么写，而在 `try` 放在循环的哪一层。若把整个 `for` 包进一个 `try`，任何一条坏数据抛错都会跳出整个循环，后续数据全部丢失，正是一条坏数据毁掉整批的由来；正确骨架是循环在外、`try` 在内，让每条数据拥有独立的异常处理表。`continue` 必须放在 `except` 末尾，否则坏数据会掉进后面的 `append` 或求和语句，甚至因变量未重新赋值而沿用上一轮旧值，酿成比崩溃更隐蔽的统计污染。内存视角看，`valid` 列表只累积成功解析出的对象，失败项从未进入，故 `len(raw) - len(valid)` 天然等于失败条数。最后一个易错点是零有效数据：算平均值前先判断 `len(valid)`，用条件表达式兜底，避免分母为 0 触发 `ZeroDivisionError`，这与前面章节先判断再计算一脉相承。""",
        variant="""把 demo9-5 的 raise 判负加打印跳过原因改为靠 `int()` 自然抛错、`valid` 列表配合 `len` 统计成败，并加条件表达式兜底，验证零有效数据不触发除零。""",
        code="""# 容错骨架：坏数据 continue 跳过，好数据进列表；空集用条件表达式兜底防除零
raw = ["62", "abc", "118", "快"]
valid = []
for item in raw:
    try: valid.append(int(item))       # 非数字抛 ValueError 并跳过
    except ValueError: continue        # 坏数据不进入统计
print("有效", valid, "共", len(valid), "条，无效", len(raw) - len(valid), "条")
print("平均车速：", round(sum(valid) / len(valid), 1) if valid else "无有效数据")
""",
        steps=[
            "运行代码，核对首行有效 [62, 118] 共 2 条、无效 2 条，`abc` 与 `快` 因 `int()` 抛 `ValueError` 被跳过。",
            "核对第二行平均车速： 90.0，即 `(62+118)/2`，被跳过的数据没有进入分子分母。",
            "把 `except ValueError: continue` 里的 `continue` 删掉重跑，`valid` 会沿用上一轮旧值而被污染，观察统计如何失真。",
            "把 `raw` 全部换成非法字符串（如 `abc`、`快`、空串）重跑，核对走兜底分支打印无有效数据，验证零有效数据不抛 `ZeroDivisionError`。",
            "把 `try` 缩进移到 `for` 外面重跑，第一条坏数据就会终止整批，验证 `try` 必须在循环内。",
        ],
        faq=[
            ("第一条坏数据就终止了整批处理", "`try` 包住了整个 `for`，异常跳出循环", "把 `try` 移到循环内，让每条数据独立处理"),
            ("`except` 后忘写 `continue`，坏数据混进了统计", "坏数据掉进后续 `append` 与求和，甚至沿用上一轮旧值", "在 `except` 末尾加 `continue` 跳过本条"),
            ("全部数据非法时算平均值报 `ZeroDivisionError`", "`len(valid)` 为 0 时做了除法", "先判断有效条数，用条件表达式兜底"),
        ],
    ),
]
