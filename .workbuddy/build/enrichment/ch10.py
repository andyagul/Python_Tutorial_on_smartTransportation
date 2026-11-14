# -*- coding: utf-8 -*-
CHAPTER = "10模块与程序包"
ITEMS = [
    dict(
        anchor="## 10.2 知识点 10.1　模块概念与三种导入形式",
        sec="10.2",
        demo="demo10-1b",
        principle="""`import` 不是把源码复制进来，而是三步：按 `sys.path` 顺序找到文件、编译执行其中语句生成一个模块对象、把该对象登记进 `sys.modules` 缓存并绑定到本地名字。因此同一模块无论 `import` 几次都只执行一次，第二次只是把缓存里的同一对象再绑一个名字，这解释了为何 `import math` 与 `import math as m` 之后 `math is m` 为真。`import 模块` 绑定的是整个模块对象，访问成员必须写前缀；`from 模块 import 名称` 则把成员对象直接绑进当前命名空间，省了前缀却也失去来源标识，一旦与本地变量同名便互相覆盖。`from ... import *` 更会把一堆名字灌进来，是命名空间污染的根源。常见误解是以为别名会复制一份模块，实际 `as` 只改本地绑定名，底层仍是同一个对象。""",
        variant="""把 demo10-1 的三种导入各调一次补上 `math is m` 身份判断，验证 `as` 只是给 `sys.modules` 里同一模块对象换个绑定名、模块不会重复创建。""",
        code="""# 用标准库 math 算配时：三种导入形式对比，别名与原名指向同一模块对象
import math
from math import sqrt
import math as m
print("5000 辆/h 需车道数 math.ceil(5000/2200) =", math.ceil(5000 / 2200))
print("from 直接调用 sqrt(64) =", sqrt(64), "（视距系数）")
print("别名调用 m.floor(3.7) =", m.floor(3.7))
print("别名与原名是同一模块对象：", math is m)
print("模块 __name__ =", math.__name__)
""",
        steps=[
            "运行代码，核对 `math.ceil(5000 / 2200)` 输出 3，说明 `import math` 后必须带模块名前缀访问成员。",
            "核对 `sqrt(64) = 8.0`，`from math import sqrt` 把函数直接绑进当前命名空间，调用时不用写前缀。",
            "核对 `m.floor(3.7) = 3`，`import math as m` 用别名调用，结果与写全名一致。",
            "核对别名与原名是同一模块对象： True，验证 `math is m`，即 `as` 没复制模块、只是新增一个绑定。",
            "核对模块 __name__ = math，说明模块对象自带 `__name__`，导入用的是模块名而非文件名。",
        ],
        faq=[
            ("`import 模块` 后直接写 `capacity(3)` 报 `NameError`", "导入绑定的是模块对象，成员要加模块名前缀", "写 `模块.capacity(3)`，或改用 `from ... import`"),
            ("自定义文件名取成 `random.py`，标准库导入错乱", "同名文件优先命中当前目录，遮蔽了标准库", "模块名避开标准库名"),
            ("`from ... import *` 后调用到意外版本的函数", "通配符把大量名字灌入当前命名空间，易与本地变量重名", "改用 `import ... as 别名` 保留命名空间"),
        ],
    ),
    dict(
        anchor="## 10.3 知识点 10.2　自定义模块与 `__doc__`",
        sec="10.3",
        demo="demo10-2b",
        principle="""模块文档字符串必须是文件第一条语句，是因为编译器构造模块代码对象时，只把模块体开头紧邻的第一个字符串字面量收进 `co_consts` 并赋给 `__doc__`；若第一条语句是 `import` 或赋值，这个槽位就是 `None`。注意注释不产生任何字节码，所以文档字符串前写注释并不算一条语句，但把可执行语句放前面就会让 `__doc__` 丢失。`模块.__doc__` 读到的是整段原始字符串，取首行常用 `.strip().splitlines()[0]`；`dir()` 则列出模块命名空间里绑定的所有名字，双下划线开头的多为解释器预置。另一常见误解是改了模块文件就立即生效：进程内已被 `sys.modules` 缓存，不重启内核或 `importlib.reload` 仍是旧对象。以 `python3 -c` 直接执行时 `__name__` 为 `__main__` 且没有文档字符串，恰是 `__doc__ is None` 的直观例子。""",
        variant="""把 demo10-2 只展示有文档的 math 扩展为有文档与无文档对比，用 `-c` 脚本 `__doc__` 为 `None` 反证文档字符串必须是首条语句。""",
        code="""# 借标准库 math 说明 __doc__：文档字符串置顶才有值，当前 -c 脚本为 None
import math
print("交通配时 5000/2200 向上取整需", math.ceil(5000 / 2200), "条车道")
print("直接运行的脚本 __name__ =", __name__, "，__doc__ =", __doc__)
print("math 有文档字符串：", isinstance(math.__doc__, str) and len(math.__doc__) > 0)
print("math.__name__ =", math.__name__, "（导入用的是模块名，不是文件名）")
print("启示：自定义交通模块要把三引号说明放首行，否则 __doc__ 为 None")
""",
        steps=[
            "运行代码，核对首行算出需 3 条车道，确认 `math` 已成功导入且可用。",
            "核对直接运行的脚本 `__name__` = `__main__`、`__doc__` = None，因为 `-c` 代码首条语句是 `import` 而非字符串。",
            "核对 math 有文档字符串： True，标准库模块首行写了三引号说明，`__doc__` 不为空。",
            "核对 `math.__name__ = math`，区分模块名与磁盘文件名。",
            "在 `import math` 之前插入一句可执行语句重跑，`__doc__` 仍为 None，验证文档字符串必须是第一条语句。",
        ],
        faq=[
            ("在文档字符串前写了代码，`__doc__` 变成 `None`", "`__doc__` 只取模块体第一条字符串字面量", "把三引号说明放在文件最开头，注释置于其后"),
            ("改了模块文件，运行中仍是旧版本", "模块已被 `sys.modules` 缓存，不会重新执行", "重启内核或用 `importlib.reload`"),
            ("`dir(模块)` 里一堆下划线名字不知如何处理", "双下划线开头的是解释器预置成员", "用列表推导过滤下划线开头的名字"),
        ],
    ),
    dict(
        anchor='## 10.4 知识点 10.3　`if __name__ == "__main__"`',
        sec="10.4",
        demo="demo10-3b",
        principle="""每个模块对象都有 `__name__` 属性，值由它是怎么被加载的决定：被当作主程序直接执行时解释器把它设成 `__main__`，被 `import` 时则是模块自身名字（包内是带点号的全名）。把代码放进 `if __name__` 与字面量 `__main__` 比较的分支里，只是一次普通的字符串比较，却能把自测代码与可导入的功能隔离在同一文件里。机制上，导入模块会执行其全部顶层语句，所以若把打印测试数据的代码裸露在顶层，调用方一 `import` 就会被刷屏甚至被误执行；加保护后这些语句只在直接运行时触发。两个高频笔误值得留意：把 `__main__` 少写两侧下划线、或漏写引号把它当成变量，都会让条件恒为假或抛 `NameError`。主程序入口同样应加这道保护，便于日后被别的程序当作模块复用。""",
        variant="""把 demo10-3 的打印 `__name__` 并判断改为把自测封装成函数、在保护块内调用，验证直接运行时自测被执行、且少写下划线的写法恒为假。""",
        code="""# 在 -c 中 __name__ 恒为 "__main__"，验证自测块只在直接运行时执行
def selftest():
    print("  [自测] 3 车道通行能力：", 3 * 2200, "辆/h")
print("当前 __name__ =", __name__)
if __name__ == "__main__":
    selftest()
    print("→ 直接运行：自测代码执行")
else:
    print("→ 被导入：自测代码不执行")
print('写成 == "main" 会漏两侧下划线，条件永远为 False')
""",
        steps=[
            "运行代码，核对当前 `__name__` = `__main__`，因为 `python3 -c` 把这段代码当主程序执行。",
            "核对 [自测] 3 车道通行能力： 6600 辆/h 被打印，说明 `if __name__` 比较条件成立、保护块内的 `selftest()` 执行了。",
            "核对出现 → 直接运行：自测代码执行，而 else 分支那句被导入没有出现。",
            "把条件里的 `__main__` 少写两侧下划线重跑，自测行不再打印、`__name__` 仍是 `__main__`，验证笔误让条件恒为假。",
            "设想把这段存成文件再被 `import`（此时 `__name__` 为模块名），`selftest()` 不会执行，体会导入时不打扰调用方。",
        ],
        faq=[
            ("模块被 `import` 时刷出一堆测试输出", "演示代码写在顶层，导入会执行全部顶层语句", "把自测放进 `__name__` 保护块"),
            ("把 `__main__` 少写两侧下划线后自测永不执行", "字符串与实际的 `__name__` 值不相等", "补全两侧下划线再比较"),
            ("条件里漏写引号、把 `__main__` 当变量报 `NameError`", "该名字未定义，应当作字符串而非变量", "给字面量加上引号再比较"),
        ],
    ),
    dict(
        anchor="## 10.5 知识点 10.4　标准库 `random` 与 `datetime`",
        sec="10.5",
        demo="demo10-4b",
        principle="""`random` 生成的是伪随机数：给定相同种子，梅森旋转算法产生完全相同的序列，所以 `seed(n)` 或 `random.Random(n)` 能让仿真结果可复现，便于批改与回归对比；用独立生成器对象而非模块级 `seed()`，好处是不扰动程序里其他依赖全局随机状态的地方，隔离性更好。别把 `randint(a, b)` 与 `range` 混为一谈——前者含两端、后者含头不含尾，这是边界统计出错的常见来源。`datetime.date` 与 `datetime` 对象是不可变的，加减 `timedelta` 返回的是新对象而非原地修改，因此 `d + timedelta(days=1)` 不会改动 `d` 本身；`strftime` 只是按占位符把对象格式化成字符串，`%Y` 是四位年、`%y` 是两位年，大小写敏感。安全或抽奖等场景不能依赖可预测的伪随机，应改用 `secrets`。""",
        variant="""把 demo10-4 的模块级 `random.seed` 换成独立生成器 `random.Random(7)`，并全部使用固定日期，验证伪随机序列可复现且生成器状态与全局隔离。""",
        code="""# 用独立的 Random(7) 生成器造可复现车流，datetime 用固定日期而非当前时间
import random
import datetime
rng = random.Random(7)                 # 独立种子对象，不污染全局随机状态
print("随机路段：", rng.choice(["京港澳", "京开", "机场高速"]))
print("随机流量 randint(600,1800)：", rng.randint(600, 1800))
print("随机车速：", round(rng.uniform(15, 85), 1))
d = datetime.date(2026, 11, 12)
print("固定日期 + 1 天：", d + datetime.timedelta(days=1))
print("格式化 %Y 四位年：", d.strftime("%Y年%m月%d日"))
""",
        steps=[
            "运行代码，核对前三行是固定路段、固定流量、保留 1 位的车速，因为 `random.Random(7)` 的种子固定。",
            "把代码原样再跑一次，核对三行数值完全一致，验证伪随机序列可复现。",
            "核对固定日期 + 1 天： 2026-11-13，确认用的是 `datetime.date(2026, 11, 12)` 固定日期而非当前时间。",
            "核对格式化 %Y 四位年： 2026年11月12日，`%Y` 给出四位年；若误写成 `%y` 会得到两位年。",
            "把 `Random(7)` 换成 `Random(8)` 重跑，随机路段、流量、车速整体变化，但同一新种子下再次运行结果仍一致。",
        ],
        faq=[
            ("每次跑 `random` 结果都不同，没法核对", "没固定种子，伪随机序列随系统状态变化", "用 `seed(n)` 或 `random.Random(n)` 固定"),
            ("以为 `randint(1, 10)` 不含 10", "`randint` 含两端，与 `range` 的含头不含尾不同", "记住边界差异，抽样范围写清楚"),
            ("`import datetime` 后写 `datetime.now()` 报 `AttributeError`", "`now` 在 `datetime.datetime` 类上，模块层没有", "写 `datetime.datetime.now()` 或 `from datetime import datetime`"),
        ],
    ),
    dict(
        anchor="## 10.6 知识点 10.5　程序包与相对导入",
        sec="10.6",
        demo="demo10-5b",
        principle="""包本质是一个带 `__init__.py` 的目录，模块全名用点号表达层级，点号对应磁盘上的目录层级；`__package__` 记录该模块所属的包，全名去掉最后一段便是它。`__init__.py` 在包首次被导入时执行一次，作用是把子模块里的接口提升到包这一层，并用 `__all__` 约束 `from 包 import *` 的导出名单，因此它只应放元信息与导入、不写业务逻辑——导入即执行，放业务会难以测试。相对导入 `from .calc import capacity` 里的点，是以当前 `__package__` 为基准解析的，必须存在包上下文；直接 `python traffic_pkg/main.py` 时该模块被当成顶层脚本、`__package__` 为空，于是报 `attempted relative import with no known parent package`，改用 `python -m traffic_pkg.main` 才会为它建立包身份。""",
        variant="""把 demo10-5 的层级数统计并列上交通包全名，验证模块全名、`__package__` 与点号层级的对应关系，点出相对导入的点所指。""",
        code="""# 借标准库多层包说明层级命名：模块全名用点号，__package__ 是所属包
import xml.etree.ElementTree as ET
print("标准库模块全名：", ET.__name__)
print("所属包 __package__ =", ET.__package__)
print("点号层级数 =", ET.__name__.count(".") + 1)
print("交通包 traffic_pkg.calc.capacity 层级数 =", "traffic_pkg.calc.capacity".count(".") + 1)
print("包内 from . import calc 的 . 即指 __package__ 这一层")
""",
        steps=[
            "运行代码，核对标准库模块全名： xml.etree.ElementTree，点号把包、子包、模块连成层级全名。",
            "核对所属包 __package__ = xml.etree，它是全名去掉最后一段后的部分。",
            "核对点号层级数 = 3，即 xml / etree / ElementTree 三层。",
            "核对交通包 traffic_pkg.calc.capacity 层级数 = 3，自定义包遵循同样的点号规则。",
            "记住包内 `from . import calc` 的点指 `__package__` 这一层，因此入口须在包上一级用 `python -m traffic_pkg.main` 运行，直接按文件路径运行会因缺少包上下文报相对导入错误。",
        ],
        faq=[
            ("按文件路径直接运行包内 main 报 `attempted relative import`", "直接运行使模块失去包上下文，`__package__` 为空", "改用 `python -m traffic_pkg.main`"),
            ("在包内目录运行报 `ModuleNotFoundError: traffic_pkg`", "当前目录不对，解释器找不到包", "回到包的上一级目录执行"),
            ("`__init__.py` 里写了大量计算，导入即执行难测试", "包被导入时 `__init__.py` 会执行其顶层语句", "只放接口暴露与 `__all__` 等元信息，业务移到子模块"),
        ],
    ),
]
