# ---------- 第 04 章 字符串与输入输出 · 练习 4-2 参考答案：路段名称检索与脱敏 ----------
# 对应知识点：4.3 in / find() / startswith() / endswith() / count()、4.2 replace()
# 功能说明：在路段名中检索敏感关键词，统计出现次数与位置，并输出脱敏后的名称

name = input("路段名称：")
keyword = input("敏感关键词：")

print("是否包含关键词：", keyword in name)
print("首次出现位置：", name.find(keyword))
print("是否以'京'开头：", name.startswith("京"))
print("是否以'高速'结尾：", name.endswith("高速"))
print("关键词出现次数：", name.count(keyword))

masked = name.replace(keyword, "***")
print("脱敏后名称：", masked)

if name.find(keyword) == -1:      # find() 找不到时返回 -1，而不是抛异常
    print("结论：无需脱敏")
else:
    print("结论：已脱敏，可对外发布")
