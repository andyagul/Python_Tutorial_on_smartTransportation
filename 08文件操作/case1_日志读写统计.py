# ---------- 第 08 章 文件操作 · 案例 8-1：车载日志写入与逐行统计 ----------
# 对应知识点：8.1 w / r 模式、8.3 write() 与换行、8.2 逐行遍历与 strip() / split()、8.4 with + encoding
# 功能说明：写入 6 条样例车载日志，再逐行读回统计记录数、平均车速并打印超速记录

# ---------- 1) 写入样例日志 ----------
records = [
    "2026-10-29 08:15:32|京A12345|62|2",
    "2026-10-29 08:16:02|京B67890|118|1",
    "2026-10-29 08:16:32|津C24680|132|3",
    "2026-10-29 08:17:02|冀D11223|78|2",
    "2026-10-29 08:17:32|京E55667|150|1",
    "2026-10-29 08:18:02|京A13579|95|3",
]

with open("vehicle_log.txt", "w", encoding="utf-8") as f:
    for line in records:
        f.write(line + "\n")          # 每行必须以换行结尾
print("已写入", len(records), "条记录")

# ---------- 2) 读取并统计 ----------
total = 0
over = 0
speed_sum = 0

with open("vehicle_log.txt", "r", encoding="utf-8") as f:
    for line in f:                    # 逐行读取，内存占用最小
        line = line.strip()
        if line == "":                # 跳过空行，防止解析越界
            continue
        parts = line.split("|")
        speed = int(parts[2])         # 字符串转整数
        total += 1
        speed_sum += speed
        if speed > 120:
            over += 1
            print("  超速：", parts[1], speed, "km/h")

print("总记录数：", total, "条")
print("超速记录：", over, "条")
print("平均车速：", round(speed_sum / total, 1), "km/h")
