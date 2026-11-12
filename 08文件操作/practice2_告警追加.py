# ---------- 第 08 章 文件操作 · 练习 8-2 参考答案：告警记录追加写入 ----------
# 对应知识点：8.1 a 追加模式（不覆盖）、8.3 写入与换行、8.2 读回统计
# 功能说明：分两批把告警记录追加写入同一文件，读回校验旧数据未被覆盖并统计最高车速

# 第一批告警
batch1 = [
    "2026-10-29 08:16:32,津C24680,132",
    "2026-10-29 08:17:32,京E55667,150",
    "2026-10-29 09:05:10,冀D11223,128",
]
with open("alarm.txt", "a", encoding="utf-8") as f:
    for item in batch1:
        f.write(item + "\n")

# 第二批告警（追加，不覆盖）
batch2 = [
    "2026-10-29 18:22:05,京A12345,135",
    "2026-10-29 18:30:44,京B67890,142",
]
with open("alarm.txt", "a", encoding="utf-8") as f:
    for item in batch2:
        f.write(item + "\n")

# 读回统计
count = 0
max_speed = 0
with open("alarm.txt", "r", encoding="utf-8") as f:
    for line in f:
        line = line.strip()
        if line == "":
            continue
        count += 1
        parts = line.split(",")
        speed = int(parts[2])
        if speed > max_speed:
            max_speed = speed
        print("第" + str(count) + "条：", line)

print("告警总数：", count, "条")
print("最高车速：", max_speed, "km/h")
