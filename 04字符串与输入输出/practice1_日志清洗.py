# ---------- 第 04 章 字符串与输入输出 · 练习 4-1 参考答案：车载日志行清洗与字段提取 ----------
# 对应知识点：4.2 strip() 清洗、4.4 count() 与 split()、4.3 replace()
# 功能说明：清洗一条车载日志，按竖线切分字段，校验分隔符数量并输出英文化文本

line = "  2026-10-29 08:15:32 | 京A12345 | 车速 62 | 车道 2  "

clean = line.strip()                 # 去首尾空白
print("清洗后：", clean)
print("分隔符个数：", clean.count("|"))

parts = clean.split("|")             # 按竖线切分
print("字段个数：", len(parts))
print("分隔符校验通过：", clean.count("|") == len(parts) - 1)

for i in range(len(parts)):
    print("字段" + str(i) + "：", parts[i].strip())

print("英文化输出：", clean.replace("车速", "speed").replace("车道", "lane"))
