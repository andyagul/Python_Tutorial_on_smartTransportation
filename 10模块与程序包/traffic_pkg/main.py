# ---------- 第 10 章 模块与程序包 · 练习 10-2 配套程序包：包入口 ----------
# 对应知识点：10.5 相对导入、10.3 __main__ 保护；运行方式 python -m traffic_pkg.main
# 功能说明：以模块方式运行包入口，打印包版本并调用包内计算接口

"""包入口程序：需在 traffic_pkg 的上一级目录执行 python -m traffic_pkg.main"""

from . import capacity, density, __version__

if __name__ == "__main__":
    print("包版本：", __version__)
    print("3 车道通行能力：", capacity(3))
    print("车流密度：", density(96, 2.5, 3))
