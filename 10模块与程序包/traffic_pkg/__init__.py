# ---------- 第 10 章 模块与程序包 · 练习 10-2 配套程序包：包声明 ----------
# 对应知识点：10.5 包结构与 __init__.py、__all__ 导出、包版本号
# 功能说明：声明 traffic_pkg 包，把 calc 中的接口对外暴露，并给出 __all__ 与 __version__

"""智慧交通计算包：对外暴露常用计算接口"""

from .calc import capacity, density

__all__ = ["capacity", "density"]
__version__ = "1.0.0"
