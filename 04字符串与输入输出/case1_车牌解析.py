# ---------- 第 04 章 字符串与输入输出 · 案例 4-1：车牌号解析与合法性初筛 ----------
# 对应知识点：4.1 索引 / 切片 / len()、4.2 strip() 与 upper()、4.3 isalnum() / isascii()、3.1 分支判定
# 功能说明：解析车牌字符串，取出省份简称、发牌机关与号牌序号，并按长度初筛车牌类型

# 车牌号解析与合法性初筛
raw = input("请输入车牌号：")
plate = raw.strip().upper()          # 去空白 + 统一大写

print("规范化结果：", plate)
print("字符总数：", len(plate))

prov = plate[0]         # 索引 0：省份简称
letter = plate[1]       # 索引 1：发牌机关代号
number = plate[2:]      # 切片：从第 3 位到末尾的序号

print("省份简称：", prov)
print("发牌机关：", letter)
print("号牌序号：", number)

if len(plate) == 7:
    print("车牌类型：普通民用号牌")
elif len(plate) == 8:
    print("车牌类型：新能源号牌")
else:
    print("车牌类型：长度异常，需人工复核")

print("序号是否只含字母数字：", number.isalnum())
print("首字符是否为汉字：", not prov.isascii())
