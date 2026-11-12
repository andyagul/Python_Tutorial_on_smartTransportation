# ---------- 第 13 章 综合项目实战 · 练习 13-1 参考答案：turtle 绘制智慧停车场 ----------
# 对应知识点：13.1 坐标与画笔、13.2 矩形与文字、13.3 tracer(0) + update()
# 功能说明：绘制 3×6 车位矩阵并整体居中，已占用车位标注车牌尾号、空位标注 FREE

import turtle

ROWS, COLS = 3, 6                        # 车位矩阵：3 行 6 列，共 18 个车位
SLOT_W, SLOT_H, GAP = 60, 100, 8         # 单车位宽、高与车位间距（像素）

# 已占用车位用（行, 列）表示，下标从 0 开始；plates 与之一一对应
occupied = [(0, 0), (0, 2), (1, 1), (1, 4), (2, 5)]
plates = ["2345", "7890", "4680", "1122", "5667"]


def rect(t, x, y, w, h, color, text="", text_color="#2c3e50"):
    """以 (x, y) 为左下角画填充矩形，可选在中心写一行文字"""
    t.penup()
    t.goto(x, y)
    t.pendown()
    t.color("#34495e")
    t.fillcolor(color)
    t.begin_fill()
    for _ in range(2):
        t.forward(w)
        t.left(90)
        t.forward(h)
        t.left(90)
    t.end_fill()
    if text != "":
        t.penup()
        t.goto(x + w / 2, y + h / 2 - 8)
        t.color(text_color)
        t.write(text, align="center", font=("Arial", 12, "bold"))


def main():
    screen = turtle.Screen()
    screen.title("智慧停车场平面图")
    screen.setup(760, 560)
    screen.bgcolor("#f4f6f8")
    screen.tracer(0)

    t = turtle.Turtle()
    t.hideturtle()
    t.speed(0)

    # 先算出停车场总宽高，再由左下角起点反推每个车位的坐标，整体才能居中
    total_w = COLS * SLOT_W + (COLS - 1) * GAP
    total_h = ROWS * SLOT_H + (ROWS - 1) * GAP
    start_x = -total_w / 2
    start_y = -total_h / 2

    idx = 0
    for r in range(ROWS):
        for c in range(COLS):
            x = start_x + c * (SLOT_W + GAP)
            # 行号自上而下，而 turtle 的 y 向上为正，故用 (ROWS - 1 - r) 反向取行
            y = start_y + (ROWS - 1 - r) * (SLOT_H + GAP)
            if (r, c) in occupied:
                label = "京A" + plates[idx % len(plates)][-4:]
                idx += 1
                rect(t, x, y, SLOT_W, SLOT_H, "#aed6f1", label, "#1a5276")
            else:
                rect(t, x, y, SLOT_W, SLOT_H, "white", "FREE", "#7f8c8d")

    t.penup()
    t.goto(0, total_h / 2 + 40)
    t.color("#2c3e50")
    t.write("智慧停车场 · 已用 " + str(len(occupied)) + " / " + str(ROWS * COLS),
            align="center", font=("Microsoft YaHei", 18, "bold"))

    screen.update()
    screen.exitonclick()


if __name__ == "__main__":
    main()
