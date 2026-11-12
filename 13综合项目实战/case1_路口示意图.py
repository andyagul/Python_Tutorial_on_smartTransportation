# ---------- 第 13 章 综合项目实战 · 案例 13-1：turtle 绘制智慧路口与信号灯倒计时 ----------
# 对应知识点：13.1 turtle 坐标系与画笔、13.2 矩形 / 圆点 / 文字 / 填充、13.3 tracer(0) + update() 动画刷新
# 功能说明：绘制路口平面图（道路、中心区、斑马线），并播放「红灯 3 秒 → 绿灯 5 秒」倒计时动画

import turtle
import time

# 画布尺寸：turtle 以窗口中心为原点，故所有坐标都落在 ±W/2、±H/2 之内
W, H = 640, 480


def rect(t, x, y, w, h, color):
    """以 (x, y) 为左下角画填充矩形"""
    t.penup()
    t.goto(x, y)
    t.pendown()
    t.color(color)
    t.fillcolor(color)
    t.begin_fill()
    for _ in range(2):
        t.forward(w)
        t.left(90)
        t.forward(h)
        t.left(90)
    t.end_fill()


def draw_scene(t):
    """绘制路口：两条道路 + 中心区 + 四处斑马线"""
    rect(t, -W / 2, -50, W, 100, "#5b5b5b")      # 横向主干道
    rect(t, -50, -H / 2, 100, H, "#5b5b5b")      # 纵向支路
    rect(t, -50, -50, 100, 100, "#8a6d0b")       # 路口中心区

    # 左右两侧斑马线（竖条纹）
    for i in range(6):
        rect(t, 62 + i * 16, -45, 9, 90, "white")
        rect(t, -62 - i * 16 - 9, -45, 9, 90, "white")

    # 上下两侧斑马线（横条纹）
    for i in range(6):
        rect(t, -45, 62 + i * 16, 90, 9, "white")
        rect(t, -45, -62 - i * 16 - 9, 90, 9, "white")

    t.penup()
    t.goto(-W / 2 + 12, 58)
    t.color("white")
    t.write("智慧路口平面示意图", font=("Microsoft YaHei", 14, "bold"))


def draw_lamp(t, x, y, color):
    """在 (x, y) 画一个信号灯"""
    t.clear()
    t.penup()
    t.goto(x, y)
    t.dot(30, color)


def countdown(text, screen, seconds, tip):
    """倒计时文字动画：每秒刷新一个数字，结束后显示提示语"""
    for s in range(seconds, 0, -1):       # 倒序循环：seconds → 1
        text.clear()                      # 先擦掉上一个数字，避免叠加
        text.write(str(s), align="center", font=("Arial", 30, "bold"))
        screen.update()                   # 手动刷新一帧，数字才会出现
        time.sleep(1)                     # 停 1 秒，形成"1 秒一跳"的节奏
    text.clear()
    text.write(tip, align="center", font=("Microsoft YaHei", 18, "bold"))
    screen.update()


def main():
    # 1) 屏幕对象：负责标题、窗口尺寸与背景色，不参与绘图
    screen = turtle.Screen()
    screen.title("智慧路口示意图 - turtle")
    screen.setup(W + 40, H + 40)
    screen.bgcolor("#eef1f5")
    screen.tracer(0)                      # 关闭自动刷新，手动 update

    # 2) 画笔一：只画静态场景（道路、斑马线、标题），画完不再改动
    pen = turtle.Turtle()
    pen.hideturtle()
    pen.speed(0)
    draw_scene(pen)

    # 3) 画笔二：只画信号灯圆点；切换相位时 clear() 不会擦掉场景
    lamp = turtle.Turtle()
    lamp.hideturtle()
    lamp.speed(0)

    # 4) 画笔三：只写倒计时数字与提示文字，位置固定在路口上方
    text = turtle.Turtle()
    text.hideturtle()
    text.speed(0)
    text.color("#c0392b")
    text.penup()
    text.goto(0, 150)

    # 阶段一：红灯 3 秒
    draw_lamp(lamp, 0, 105, "#c0392b")
    countdown(text, screen, 3, "红灯")

    # 阶段二：绿灯 5 秒
    draw_lamp(lamp, 0, 105, "#27ae60")
    text.color("#1e8449")
    countdown(text, screen, 5, "绿灯放行")

    screen.update()
    print("示意图绘制完成，点击窗口关闭")
    screen.exitonclick()


if __name__ == "__main__":
    main()
