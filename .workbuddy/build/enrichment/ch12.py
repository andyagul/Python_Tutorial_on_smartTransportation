# -*- coding: utf-8 -*-
CHAPTER = "12面向对象编程下"
ITEMS = [
    dict(
        anchor="## 12.2 知识点 12.1　封装回顾",
        sec="12.2",
        demo="demo12-1b",
        principle="""「私有」并不是加密：双下划线属性在类定义时被解释器改名成「下划线加类名加原名」的形式，外部仍可用改名后的名字或对象字典看到它。改名的真正作用是避免子类意外覆盖父类的同名属性。内存里每个实例只有一张属性字典，父类的共性数据与子类的扩展属性平铺其中，并不存在两层对象。区间约束必须写进唯一的写入入口（构造方法与设值方法），否则构造时直接赋值就绕过校验，非法车速会悄悄进入仿真。类外直接给同名属性赋值并不报错，只新建一个普通键，与改名后的私有项是两码事——这正是初学者觉得「改了却没生效」的根因。""",
        variant="""把随堂示例的单向上限约束迁移为"双向区间夹逼 + 名称改写验证"：新增构造期校验与类外直改对照，验证私有属性被改名后外部同名赋值动不了真实值。""",
        code="""\
class Gantry:  # 门架测速：车速私有，区间约束只在类内写一次
    def __init__(self, road, v):
        self.road = road
        self.__v = max(0, min(v, 120))  # 写入前把 150 夹到 120
g = Gantry("G15 门架", 150)
print("对象字典：", g.__dict__)  # 私有 __v 被改名为 _Gantry__v
g.__v = 999  # 类外不改名，只是新建一个键，动不了私有值
print("真实车速仍是：", g._Gantry__v)
print("外部直改产生的键：", "__v" in g.__dict__)
""",
        steps=[
            "运行后观察首行 `对象字典` 中私有键已被写成 `_Gantry__v`，而不是 `__v`。",
            "核对构造参数 150 打印出的车速是 120，说明 `min(v, 120)` 在写入 `__v` 之前就生效。",
            "观察末行 `外部直改产生的键： True`，确认类外的 `g.__v = 999` 新建了一个普通键。",
            "核对第二行 `真实车速仍是： 120`，证明改写后的 `_Gantry__v` 没有被那行外部赋值改变。",
            "试着把 `g._Gantry__v` 直接改成 60 再打印第二行，观察车速真的变 60，理解「私有只是改名、不是加密」。",
        ],
        faq=[
            ("`AttributeError: 'Gantry' object has no attribute '__v'`", "私有名已被改写为 `_Gantry__v`，类外用原名访问不到", "通过类内方法读取，或用改写后的名字 `g._Gantry__v`"),
            ("外部写 `g.__v = 999` 后读到的车速仍是原值", "类外不触发名称改写，这行只新建一个普通属性 `__v`", "一律通过 `set_speed()` 修改，不要直接赋值"),
            ("构造时传入 150，车速却没被限制", "校验只写在 `set_speed()`，构造时直接赋给 `self.__v` 绕过了校验", "构造末尾也调用统一的校验入口"),
            ("子类里改 `self.__v` 对父类数据不起作用", "私有名按定义它的类名改写，子类的 `self.__v` 是 `_子类名__v`，与父类不是同一项", "父类提供共有的 `get/set` 方法供子类调用"),
            ("打印 `g` 出现 `<... object at 0x...>`", "未定义 `__str__`，打印的是含内存地址的对象默认 repr", "自定义 `__str__` 或打印具体属性"),
        ],
    ),
    dict(
        anchor="## 12.3 知识点 12.2　继承与 `super()`",
        sec="12.3",
        demo="demo12-2b",
        principle="""继承不是把父类代码复制一份，而是查找：每个类都带一张 MRO 表，调用方法时按「子类、父类、object」依次找，找到即停，父类方法始终只存一份。内存里子类实例只有一张属性字典，父、子属性平铺其中；super 语句只是以这个实例为 self 去执行父类初始化，把车牌写进同一张字典。所以 super 不是调用父类对象，而是沿 MRO 从下一站继续找方法，必须放在子类构造方法的首行，否则父类用到的属性还没写入就会报错。isinstance 返回真也不是类型转换，而是沿继承链比对。""",
        variant="""把随堂示例的"货车重写 limit"迁移为"救护车只继承不重写 + 打印 MRO 链"，验证继承是按查找链复用父类方法而非复制代码，且父、子属性共存于同一实例字典。""",
        code="""\
class Vehicle:  # 车辆基类：共性数据与限速写在父类
    def __init__(self, plate): self.plate = plate   # 一行方法体
    def limit(self): return 120
class Ambulance(Vehicle):  # 子类：括号写父类，方法靠"查找"而非复制
    def __init__(self, plate, level):
        super().__init__(plate)  # 首行复用构造，plate 才有值
        self.level = level
a = Ambulance("京A急救01", 1)
print("车牌：", a.plate, "；限速：", a.limit(), "；等级：", a.level)
print("继承链：", [c.__name__ for c in Ambulance.__mro__], "；是 Vehicle 吗：", isinstance(a, Vehicle))
""",
        steps=[
            "运行后观察 `继承链` 打印为 `['Ambulance', 'Vehicle', 'object']`，确认查找顺序是子类在前、父类在后。",
            "观察 `限速： 120`：子类没写 `limit()` 却拿到父类返回值，证明是「查找」而非复制代码。",
            "观察 `车牌： 京A急救01`，说明 `super().__init__(plate)` 把 `plate` 写进了实例字典。",
            "观察 `等级： 1` 与车牌同时存在，说明父、子属性都在同一个 `a.__dict__` 里。",
            "把 `super().__init__(plate)` 注释掉再运行，观察报错行正是访问 `a.plate` 的那行 `print`。",
            "观察 `是 Vehicle 吗： True`，确认子类实例同时被认定为父类实例。",
        ],
        faq=[
            ("`AttributeError: 'Ambulance' object has no attribute 'plate'`", "子类 `__init__` 忘了 `super().__init__(plate)`，父类初始化没执行", "在子类 `__init__` 首行补 `super().__init__(...)`"),
            ("`super()` 放在赋值之后，父类值把已设的属性覆盖", "父类初始化后执行会重写同名字段，逻辑混乱", "把 `super().__init__` 放到首行"),
            ("改父类名后多处报 `NameError`", "硬编码了 `Vehicle.__init__(self, ...)`，父类名写死在多处", "改用 `super()`，不写死父类名"),
            ("以为子类「复制」了父类方法，改父类后子类行为不变", "实际是运行时沿 MRO 查找，父类方法只有一份", "理解方法解析顺序，改动父类会即时影响所有子类"),
            ("`isinstance(a, Vehicle)` 期望 `False` 却是 `True`", "`isinstance` 沿继承链判断，子类实例也算父类实例", "需要精确类型时改用 `type(a) is Vehicle`"),
        ],
    ),
    dict(
        anchor="## 12.4 知识点 12.3　方法重写",
        sec="12.4",
        demo="demo12-3b",
        principle="""重写是同名方法在子类 MRO 中排在前面：解释器先命中子类版本，父类版本并未删除，只是被遮蔽，仍可用 super 取回。super 从 MRO 的下一站开始查找，只取一次父类结果，不会绕回子类导致无限递归，所以「先拿父类结果再乘系数」的扩展写法是安全的。方法名与参数表须与父类一致，否则按父类签名传参会报 `TypeError`，或变成新方法让父类版本仍被调用。最容易埋雷的是漏写 `return`：函数会隐式返回 `None`，调用方拿它参与运算才报错，排查很晚。""",
        variant="""把随堂示例的单一费率重写迁移为"替换 / 扩展 / 追加信息"三种形态同场对比，验证 `super()` 取父类结果不递归，且三种写法对外接口 `fee` / `info` 完全一致。""",
        code="""\
class Toll:  # 通行费基类：给出基准实现
    def fee(self, km): return round(km * 0.5, 2)
    def info(self): return "基准费率 0.5"
class Etc(Toll):  # 完全替换：直接给新实现，不调父类
    def fee(self, km): return round(km * 0.5 * 0.95, 2)
class Truck(Toll):  # 扩展：先 super 取父类结果再加工
    def fee(self, km): return round(super().fee(km) * 1.8, 2)
    def info(self): return super().info() + "，货车上浮"  # 追加信息且不会递归
for label, t in [("基准", Toll()), ("ETC", Etc()), ("货车", Truck())]:
    print(label, "120km 费：", t.fee(120), "；", t.info())
""",
        steps=[
            "运行观察三行费用依次是 60.0、57.0、108.0，分别对应基准、完全替换、扩展三种重写。",
            "核对 `ETC` 的 57.0 = 120 × 0.5 × 0.95，说明它没调父类 `fee`，是全新实现。",
            "核对 `货车` 的 108.0 = 父类 60.0 × 1.8，说明 `super().fee(km)` 只取一次父类结果、没有递归。",
            "观察 `货车` 行的 `info()` 是「基准费率 0.5，货车上浮」，验证追加信息 = `super().info() + 后缀`。",
            "把 `Truck.info()` 里的 `return` 删掉再运行，观察该行变成 `None`，确认重写漏返回值的后果。",
            "把 `Etc.fee` 改名为 `fee2`，观察费用退回 60.0（父类版本被调用），验证方法名必须一致。",
        ],
        faq=[
            ("子类方法名拼错，父类版本仍被调用", "拼错的名字成了新方法，未构成重写", "对照父类签名逐个核对方法名"),
            ("`super().fee(km)` 报 `TypeError` 缺参数", "漏传父类要求的参数，或参数顺序改动", "参数表与父类保持一致"),
            ("调用重写方法得到 `None`", "某个分支漏写 `return`，函数隐式返回 `None`", "每个分支都显式 `return`"),
            ("担心 `super().info()` 会无限递归", "误以为 super 会重新调用子类方法", "`super()` 从 MRO 下一站取父类实现，不会绕回子类"),
            ("在 `__str__` 里调 `self.info()` 逻辑绕、易递归", "`self.info()` 可能再次触发相关链路", "直接用 `super().info()` 拼字符串"),
        ],
    ),
    dict(
        anchor="## 12.5 知识点 12.4　多态与接口约定",
        sec="12.5",
        demo="demo12-4b",
        principle="""多态不靠类型分支，而靠「所有对象都实现同名方法」这份接口约定：那句状态调用在运行前并不知道对象是什么，解释器运行时才按对象实际类型的方法表动态分派。因此新增设备只要也有同名方法，主循环一个字都不用改。基类为何要抛出未实现异常而非返回空值？因为空值是合法返回值，子类漏实现时会被静默打印、错误极晚才暴露；抛异常则第一次调用就拦截。反模式是在循环里写 isinstance 分支，那等于退回第 3 章，每加一种设备都要改调用方。接口名也必须统一，写成别的名字就会分派失败。""",
        variant="""把随堂示例的三类设备替换为"信号灯 + 新增毫米波雷达"，验证新增设备只需加一个子类、统一调度循环 `d.status()` 一行不改，并用基类直接调用验证 `raise NotImplementedError` 的强制拦截。""",
        code="""\
class Device:  # 基类用 raise 约定接口：漏实现立刻报错
    def status(self): raise NotImplementedError("子类必须实现 status()")
class Light(Device):  # 信号灯
    def status(self): return "信号灯：绿灯放行"
class Radar(Device):  # 新增设备：接入时主循环一行不改
    def status(self): return "毫米波雷达：测流量"
for d in [Light(), Radar()]: print("[巡检]", d.status())  # 同一句调用
try: Device().status()
except NotImplementedError as e: print("基类直接调用：", e)
""",
        steps=[
            "运行观察两行 `[巡检]` 分别来自 `Light` 与 `Radar`，同一句 `d.status()` 打印出不同内容。",
            "核对 `Radar` 只是新增一个子类，主循环那个 `for` 没有任何改动，验证多态的可扩展性。",
            "观察末行 `基类直接调用： 子类必须实现 status()`，确认基类方法确实抛出了 `NotImplementedError`。",
            "把 `Radar.status` 改名为 `get_status` 再运行，观察轮询到雷达时抛出 `NotImplementedError`（父类版本被调用）。",
            "在设备清单里再加一个 `Light()`，观察 `[巡检]` 变成三行而循环仍不变。",
        ],
        faq=[
            ("新增设备后主循环报 `NotImplementedError`", "子类漏实现基类约定的方法", "补齐同名方法实现"),
            ("子类写了 `get_status`，多态失效", "方法名与接口约定不一致，`d.status()` 找不到子类实现", "统一命名为 `status`"),
            ("基类方法返回 `None`，漏实现被静默忽略", "用 `return None` 代替抛异常，错误被吞掉", "基类 `raise NotImplementedError`"),
            ("`poll()` 里堆满 `isinstance` 分支，新增类型要改多处", "退化成第 3 章分支写法，失去多态", "只依赖共同方法名 `d.status()`"),
            ("调用 `Device().status()` 得到 `None` 而不是报错", "基类给了可运行的默认实现", "基类只做约定、不提供可运行实现"),
        ],
    ),
    dict(
        anchor="## 12.6 知识点 12.5　`isinstance()` 与 `type()`",
        sec="12.6",
        demo="demo12-5b",
        principle="""差别不在「宽松还是严格」，而在判断路径：isinstance 沿实例类型的 MRO 链逐个比对，链上任一环节命中即为真，所以三级链里的特种车实例也会被判为货车；type 加 is 只做确切类型对象的身份比较，差一个子类就为假。这也解释了第二参数可用元组——本质是对每项各做一次链上比对，写成列表会报类型错误。取类型名得到的是类的名字字符串，适合日志；直接打印对象会得到含内存地址的默认表示，每次运行都变、无法核对。更要紧的是：能不用类型判断就不用，一旦按类型写分支，新增车型就得改分支，与多态相悖。""",
        variant="""把随堂示例的两级继承迁移为三级继承链（新增 `Ambulance(Truck)`）并统计判定数量，验证 `isinstance` 沿整条继承链命中、`type() is` 只认精确类型，并演示第二参数用元组的写法。""",
        code="""\
class Vehicle: pass  # 车辆基类
class Truck(Vehicle): pass  # 货车
class Ambulance(Truck): pass  # 特种货车：继承链更长
fleet = [Vehicle(), Truck(), Ambulance(), Vehicle()]
print("isinstance 判为 Truck：", len([v for v in fleet if isinstance(v, Truck)]))  # 含子类
print("type 精确判为 Truck：", len([v for v in fleet if type(v) is Truck]))  # 只认自己
print("元组参数 (Truck, int)：", [isinstance(v, (Truck, int)) for v in fleet])
print("精确类型名：", [type(v).__name__ for v in fleet])
""",
        steps=[
            "运行观察 `isinstance 判为 Truck： 2`，其中 `Truck()` 与 `Ambulance()` 都被计入。",
            "观察 `type 精确判为 Truck： 1`，只有 `Truck()` 命中，`Ambulance()` 被排除。",
            "观察 `元组参数` 打印 `[False, True, True, False]`，确认 `(Truck, int)` 对链上子类同样返回 `True`。",
            "观察 `精确类型名` 为 `['Vehicle', 'Truck', 'Ambulance', 'Vehicle']`，核对每个对象的确切类型。",
            "把第二参数从元组 `(Truck, int)` 改成列表 `[Truck, int]` 再运行，观察抛出 `TypeError`。",
            "用 `print(fleet[1])` 替换打印类型名，观察输出含 `0x` 内存地址且每次不同，理解为何要打印属性。",
        ],
        faq=[
            ("子类对象用 `type(x) == Vehicle` 判成「不是车辆」", "`type` 只做精确类型比较，不含子类", "改用 `isinstance(x, Vehicle)`"),
            ("`isinstance(x, [int, float])` 报 `TypeError`", "第二参数传了列表而非类型元组", "改为元组 `(int, float)`"),
            ("新增车型后按类型写的分支要改多处", "过度使用类型判断，代码僵硬", "优先用多态，类型判断只用于边界/日志"),
            ("打印对象出现 `<... object at 0x...>`", "未自定义 `__str__`，用了含内存地址的默认 repr", "打印 `type(x).__name__` 或具体属性"),
            ("以为 `isinstance(v, (Truck, int))` 会把字符串也判成数值", "混淆了「任一命中即可」与类型层级", "元组表示对每一项做链上比对，与继承无关的类型仍为 `False`"),
        ],
    ),
]
