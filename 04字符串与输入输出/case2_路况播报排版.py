# ---------- 第 04 章 字符串与输入输出 · 案例 4-2：路况播报文本排版 ----------
# 对应知识点：4.5 f-string / % / format() 三种格式化与对齐精度、4.4 字符串重复拼接、3.1 状态判定
# 功能说明：把路段名、平均车速与排队长度排版为三列对齐报表，并按状态给出通行建议

road = input("路段名称：")
speed = eval(input("平均车速(km/h)："))
queue = eval(input("排队长度(m)："))

# 1) 表头三列对齐（左对齐 10、右对齐 10、右对齐 10）
print(f"{'路段':<10}{'车速(km/h)':>14}{'排队(m)':>12}")

# 2) 数据行：同一套宽度，保证纵向对齐
print(f"{road:<10}{speed:>14.1f}{queue:>12}")

# 3) 老式 % 格式化写法（对照用）
print("百分号写法：%s / %.1f km/h / %d m" % (road, speed, queue))

# 4) format() 写法（对照用）
print("format 写法：{0} / {1:.1f} km/h / {2} m".format(road, speed, queue))

if queue >= 300:
    status = "拥堵"
    tip = "建议绕行辅道"
elif queue >= 100:
    status = "缓行"
    tip = "保持车距，谨慎变道"
else:
    status = "畅通"
    tip = "正常通行"

print("=" * 40)
print(f"【路况播报】{road}　当前{status}")
print(f"平均车速 {speed:.1f} km/h，排队长度 {queue} m。{tip}。")
