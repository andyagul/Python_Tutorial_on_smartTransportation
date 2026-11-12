# ---------- 第 07 章 高级函数 · 案例 7-2：用装饰器给采集函数加统一日志 ----------
# 对应知识点：7.5 装饰器与 @ 语法糖、嵌套函数与闭包、*args / **kwargs 透传
# 功能说明：为多个采集函数统一加上调用日志与调用次数统计，不修改原函数体内部代码

def log_call(func):
    """装饰器：记录被装饰函数的调用次数与参数"""
    def wrapper(*args, **kwargs):
        wrapper.calls += 1
        print("[日志] 第 " + str(wrapper.calls) + " 次调用 " + func.__name__
              + " 参数=" + str(args) + str(kwargs))
        return func(*args, **kwargs)
    wrapper.calls = 0          # 给 wrapper 挂一个计数器属性
    return wrapper


@log_call
def calc_density(cars, length_km, lanes):
    return round(cars / (length_km * lanes), 2)


@log_call
def calc_fee(km, rate=0.5, discount=1.0):
    return round(km * rate * discount, 2)


print("密度结果：", calc_density(96, 2.5, 3))
print("密度结果：", calc_density(120, 3.0, 2))
print("费用结果：", calc_fee(120, discount=0.95))
print("累计调用 calc_density：", calc_density.calls)
print("累计调用 calc_fee：", calc_fee.calls)
