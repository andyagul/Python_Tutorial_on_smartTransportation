# -*- coding: utf-8 -*-
CHAPTER = "11面向对象编程上"
ITEMS = [
    dict(
        anchor="## 11.2 知识点 11.1　类与对象、实例化",
        sec="11.2",
        demo="demo11-1b",
        principle="""`class` 语句执行时会在内存里创建一个类对象，它本身也是对象；而 `类名()` 才是实例化：解释器先分配一块空实例，再调用 `__init__` 初始化，最后返回其引用。每个实例默认携带自己的 `__dict__` 属性字典，这正是各对象属性互不影响的内存依据——`v1.plate = ...` 只是往 `v1.__dict__` 里塞一个键，丝毫不会动 `v2.__dict__`。`is` 比较的是对象身份（可理解为内存中的同一块），`==` 比较值；`type(obj).__name__` 读的是类对象的名字而非实例数据。常见误解是把 `v1 = Vehicle`（没写括号）当成实例化，那其实只是给类对象又绑了一个名字，后续访问实例属性必然 `AttributeError`。另外，类体在定义时就会执行一次，所以类属性此刻已建立，而实例属性要等 `__init__` 被调用才出现。""",
        variant="""把 demo11-1 的打印 `plate` 值改为打印两个实例的 `__dict__` 与 `is` 身份，验证每个实例各持一份属性字典、动态挂属性互不干扰。""",
        code="""# 类是模板：两个卡口对象各有独立属性字典，给 g1 挂属性不影响 g2
class Gate:
    pass
g1 = Gate()
g2 = Gate()
g1.plate = "京A12345"
print("g1 属性表：", g1.__dict__)
print("g2 属性表：", g2.__dict__)
print("不同实例：", g1 is not g2, "| 类型：", type(g1).__name__)
print("g2 是否已有 plate：", hasattr(g2, "plate"))
""",
        steps=[
            "运行代码，核对 g1 属性表： {'plate': '京A12345'}，`g1.plate = ...` 只往 `g1.__dict__` 写键。",
            "核对 g2 属性表： {}，`g2` 没有继承到 `g1` 动态挂的属性，验证两份 `__dict__` 相互独立。",
            "核对不同实例： True | 类型： Gate，`is not` 比较身份、`type().__name__` 读类名。",
            "核对 g2 是否已有 plate： False，`hasattr` 在 `g2.__dict__` 里找不到该键。",
            "把 `g1 = Gate()` 改成漏写括号的 `g1 = Gate` 重跑，会变成给类对象挂属性、属性表不再是实例属性表，反证实例化必须写括号。",
        ],
        faq=[
            ("漏写括号、把类对象赋值给变量后访问实例属性报 `AttributeError`", "这只是给类对象又绑了名字，并未创建实例", "实例化必须写 `Vehicle()`"),
            ("类名写成小写 `class vehicle:` 被提醒不规范", "类名约定用大驼峰", "改为 `Vehicle`、`TrafficLight` 这类大驼峰"),
            ("实例化参数个数与 `__init__` 不符报 `TypeError`", "实参会整体传给构造签名，个数必须对齐", "对照 `__init__` 的形参考传参"),
        ],
    ),
    dict(
        anchor="## 11.3 知识点 11.2　`__init__` 与 `self`",
        sec="11.3",
        demo="demo11-2b",
        principle="""`v = Vehicle(...)` 实际分两步：`__new__` 造出空实例，再以该实例为第一个实参调用 `__init__`。所谓 `self` 并不是关键字，只是约定俗成的形参名，Python 通过绑定方法机制在调用 `v.info()` 时自动把 `v` 塞进首位，所以定义必须写 `self`、调用却绝不手写——漏写会让自动传入的实例与你写的参数个数对不上，报 `takes 0 positional arguments but 1 was given`。`self.x = 值` 是往实例 `__dict__` 写键，而方法内不加 `self.` 的局部变量只是栈帧上的临时量，方法返回即随帧销毁，从 `hasattr` 和 `__dict__` 都查不到。另一个易错点是拼写：`__init__` 前后各两个下划线，写成 `__int__` 就成了普通方法，构造时不会被调用、属性也就没初始化。默认参数在定义时求值一次，放在构造签名里可让省略实参的对象也有初值。""",
        variant="""把 demo11-2 的打印属性表加深为故意在 `__init__` 里写一个不带 `self.` 的局部变量，验证它不会进入 `__dict__`、且默认参数照常生效。""",
        code="""# 验证 __init__ 自动执行与 self 含义：不加 self. 的变量只是局部变量
class Vehicle:
    def __init__(self, plate, speed=0):
        self.plate = plate
        self.speed = speed
        local = "临时值"                  # 无 self. 前缀，方法结束即消失
v = Vehicle("京A12345", 62)
print("属性表只含带 self 的两个：", v.__dict__)
print("local 没有成为属性：", hasattr(v, "local"))
print("默认参数生效：", Vehicle("京B67890").speed)
""",
        steps=[
            "运行代码，核对属性表只含带 self 的两个： {'plate': '京A12345', 'speed': 62}，`__init__` 在实例化时自动执行。",
            "核对 local 没有成为属性： False，方法内不带 `self.` 的 `local` 只是局部变量、方法返回即销毁。",
            "核对默认参数生效： 0，不传车速实参创建对象时取默认值 0。",
            "把不带前缀的 `local` 赋值改成 `self.local` 赋值重跑，属性表会多出 `local` 键，体会 `self.` 前缀的作用。",
            "把 `def __init__` 故意拼成 `def __int__` 重跑，构造时不再初始化属性、访问 `v.plate` 会抛 `AttributeError`。",
        ],
        faq=[
            ("方法里写了不带 `self.` 的赋值，之后读不到属性", "那只是局部变量，方法结束即随栈帧销毁", "写成 `self.speed = speed`"),
            ("定义带了 `self`，调用时还手写 `v.info(self)` 报 `TypeError`", "`self` 由绑定方法自动传入，调用不手写", "调用写 `v.info()`，定义才保留 `self`"),
            ("把 `__init__` 拼成 `__int__`，属性没初始化", "构造方法名写错，实例化时不会被调用", "前后各两个下划线，仔细核对拼写"),
        ],
    ),
    dict(
        anchor="## 11.4 知识点 11.3　实例属性与类属性",
        sec="11.4",
        demo="demo11-3b",
        principle="""属性读取遵循先实例 `__dict__`、再类 `__dict__`、再沿继承链的查找顺序，这正是 `obj.total` 能读到类属性的原因；但写入永远只作用于点号左边的那一个。`self.total += 1` 会被拆成读 `self.total`、加 1、写回 `self.total` 三步：读时因实例无此键而回退到类拿到 0，写时却直接在实例 `__dict__` 新建一个 `total` 键，类属性纹丝不动——于是每个对象各有一个计数器、`Vehicle.total` 恒为 0，这是本章最隐蔽的错误。要真正改类属性必须写 `类名.属性 += 1`。另一层风险是类属性若为可变对象（如列表），所有实例共享同一份引用，一处 `append` 会污染全部对象；因此每个对象各自的数据应放实例属性，类属性只放计数、常量表这类共享且通常不可变的值。误以为 `obj.total` 一定读到类属性，也会在对象已有同名实例属性时算错。""",
        variant="""把 demo11-3 的类名正确累加故意改成 `self.total += 1`，验证实例属性会遮蔽类属性、`Vehicle.total` 恒为 0 这一最隐蔽错误。""",
        code="""# 验证遮蔽：self.total += 1 只新建实例属性，类属性不受影响
class Vehicle:
    total = 0
    def __init__(self, plate):
        self.plate = plate
        self.total += 1                # 错误写法：实例属性遮蔽类属性
v = Vehicle("京A12345")
print("类属性仍是 0：", Vehicle.total)
print("实例读到自己的 1：", v.total)
print("实例属性表：", v.__dict__)
""",
        steps=[
            "运行代码，核对类属性仍是 0： 0，说明 `Vehicle.total` 没有被 `self.total += 1` 改动。",
            "核对实例读到自己的 1： 1，`v.total` 优先命中实例 `__dict__` 里的同名键。",
            "核对实例属性表： {'plate': '京A12345', 'total': 1}，确实多出一个 `total` 实例属性、遮蔽了类属性。",
            "把 `self.total += 1` 改回 `Vehicle.total += 1` 重跑，`Vehicle.total` 变为 1、`v.__dict__` 不再有 `total` 键。",
            "连续造两辆车再打印 `Vehicle.total`：错误写法下它恒为 0，正确写法下等于造车数，验证修改类属性必须用类名。",
        ],
        faq=[
            ("`self.total += 1` 后 `Vehicle.total` 恒为 0", "`+=` 的写回在实例 `__dict__` 新建同名属性、遮蔽类属性", "改类属性必须写 `Vehicle.total += 1`"),
            ("类属性放列表，一个对象 `append` 后所有实例都变了", "可变类属性被所有实例共享同一份引用", "各对象自持的数据放实例属性"),
            ("以为 `obj.total` 一定读到类属性", "若该对象已有同名实例属性，读取会先命中实例", "用 `类名.total` 读取最稳妥"),
        ],
    ),
    dict(
        anchor="## 11.5 知识点 11.4　实例方法与自描述",
        sec="11.5",
        demo="demo11-4b",
        principle="""`print(obj)` 与 `str(obj)` 并不是把对象直接变成文字，而是解释器去查该类是否有 `__str__`，有则调用它并打印返回的字符串；没有才回退到 `__repr__`，默认实现给出带内存地址的 `<模块.类 object at 0x…>` 表示，这就是不要打印对象默认 `repr` 的由来。`__str__` 必须返回 `str`，返回数字会抛 `TypeError`，所以拼接时要用 `str()` 把车速等数值显式转文本。`__repr__` 面向调试、追求无歧义，`__str__` 面向用户、追求可读，两者用途不同常被混淆。实例方法的第一个形参 `self` 由绑定机制自动传入，方法内部要调用同类其它方法必须写 `self.cycle()`；写成 `cycle()` 会在局部与全局命名空间都找不到名字而报 `NameError`。让 `info()`、`__str__` 都 `return` 字符串而非就地 `print`，结果才能被继续拼接、写日志或参与比较。""",
        variant="""把 demo11-4 的 `info` 与 `__str__` 并列改为让 `__str__` 内部用 `self.cycle()` 复用同类方法，验证方法互调必须带 `self.`、且 `print` 与 `str` 都触发 `__str__`。""",
        code="""# __str__ 必须返回字符串；方法内互调带 self.，print 与 str 都触发它
class Signal:
    def cycle(self):
        return self.green * 2 + 3
    def __str__(self):
        return "绿灯 " + str(self.green) + "s / 周期 " + str(self.cycle()) + "s"
s = Signal()
s.green = 35
print("print(对象) 自动调用 __str__：", s)
print("str(对象) 结果一致：", str(s))
""",
        steps=[
            "运行代码，核对两行分别以 print(对象) 自动调用 __str__ 与 str(对象) 结果一致开头，文本完全相同。",
            "核对文本为绿灯 35s / 周期 73s，其中 73 = 35 * 2 + 3 来自 `self.cycle()`，验证方法互调生效。",
            "确认打印 `s` 没有出现带内存地址的 object at 0x 默认表示，说明自定义 `__str__` 覆盖了默认 `repr`。",
            "把 `__str__` 的返回值改成整数 `self.cycle()` 重跑，会抛 `TypeError`，验证它必须返回字符串。",
            "把 `self.cycle()` 改成 `cycle()` 重跑，会报 `NameError`，验证同类方法互调必须带 `self.`。",
        ],
        faq=[
            ("`__str__` 返回数字时打印对象报 `TypeError`", "`__str__` 必须返回 `str`，返回其他类型不合法", "用 `str()` 把数值拼接成字符串再返回"),
            ("方法里写 `cycle()` 报 `NameError`", "同类方法互调必须经 `self.` 走绑定方法", "写成 `self.cycle()`"),
            ("`print(对象)` 显示带内存地址的默认表示", "没有 `__str__`，回退到默认 `__repr__`", "定义 `__str__` 返回可读文本"),
        ],
    ),
    dict(
        anchor="## 11.6 知识点 11.5　私有属性与受控访问",
        sec="11.6",
        demo="demo11-5b",
        principle="""Python 的私有不是权限隔离，而是编译期的名称改写：类体内以双下划线开头且不以双下划线结尾的名字，会被改写成 `_类名__名字`，例如 `self.__green` 实际存成 `_TrafficLight__green`。因此用 `hasattr` 查 `__green` 返回 `False` 并非属性不存在，而是它换了名字；理论上仍可用改写名访问，故私有是约定与防护、不是绝对隔离。改写只发生在 `class` 语句内部，类外写 `light.__green = 0` 不会触发改写，只会新建一个同名普通属性，真正的私有值丝毫未变——这与讲义易错表一致。封装的价值在于把校验收进唯一入口 `set_xxx()`：`__init__` 末尾调用私有 `__check()` 可纠正非法初值，`get` 与 `set` 成对提供保证读写都经过同一段逻辑。若外部能绕过入口直接赋值，绿灯 0 秒这类误操作就无人拦截，封装形同虚设。""",
        variant="""把 demo11-5 的验证 `hasattr` 为假推进到看 `__dict__` 里的真实键名，验证 `__green` 被改写成 `_TrafficLight__green`、且越界值被 `set_green` 拒绝。""",
        code="""# 验证名称改写：__green 在 __dict__ 里存为 _TrafficLight__green，故 hasattr 为 False
class TrafficLight:
    def __init__(self, green): self.__green = green
    def get_green(self): return self.__green
    def set_green(self, s): self.__green = s if 5 <= s <= 120 else self.__green
light = TrafficLight(35)
light.set_green(45)
light.set_green(200)                   # 越界被拒，私有值仍为 45
print("属性表键名：", list(light.__dict__.keys()))
print("读数/改写名：", light.get_green(), light._TrafficLight__green, "| hasattr：", hasattr(light, "__green"))
""",
        steps=[
            "运行代码，核对属性表键名： ['_TrafficLight__green']，私有属性被改写成 `_类名__属性` 而非 `__green`。",
            "核对读数/改写名一行里 `hasattr` 为 False，`hasattr` 为假是因为名字已改写、不是属性不存在。",
            "核对 `light.set_green(200)` 被拒绝后 `get_green()` 仍为 45，验证越界值没有通过唯一入口写入。",
            "核对同行两个 45 分别是 `get_green()` 与改写名 `_TrafficLight__green` 的值，证明私有是名称改写、理论仍可访问，并非绝对隔离。",
            "在类外加一句 `light.__green = 0` 再打印属性表，会多出一个普通 `__green` 键而 `get_green()` 仍是 45，验证类外同名赋值不影响私有值。",
        ],
        faq=[
            ("用 `hasattr` 查 `__green` 返回 `False`，以为属性丢了", "双下划线被改写成 `_类名__green`，不是不存在", "知道名称改写机制，用 `get_green()` 读取"),
            ("类外写 `light.__green = 0` 后绿灯值没变", "类外不触发改写，只是新建了一个普通同名属性", "一律用 `set_green()` 这个唯一入口修改"),
            ("初始值非法也能创建成功", "`__init__` 末尾没调用校验", "在 `__init__` 里调用私有 `__check()` 纠正初值"),
        ],
    ),
]
