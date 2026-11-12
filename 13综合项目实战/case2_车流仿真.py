# ---------- 第 13 章 综合项目实战 · 案例 13-2：pygame 路口车流仿真 ----------
# 对应知识点：13.4 pygame 主循环 / 事件 / clock.tick 帧率 / 时间驱动位移、13.5 停止线判定与通过计数
# 功能说明：车辆按帧率匀速通过路口，红灯时在停止线前等待，信号灯按相位循环并统计通过车数

import pygame
import sys

W, H = 800, 400
FPS = 60
# 道路上下边界：pygame 的 y 轴向下为正，数值越大越靠下
ROAD_TOP, ROAD_BOTTOM = 150, 250
STOP_LINE_X = 620                        # 停止线横坐标（红灯时车头不得越过）

pygame.init()
screen = pygame.display.set_mode((W, H))
pygame.display.set_caption("智慧路口车流仿真")
clock = pygame.time.Clock()              # 帧率控制器：tick() 返回距上一帧的毫秒数
font = pygame.font.SysFont("microsoftyahei", 22)

# 信号灯状态：green / yellow / red
light_state = "green"
light_timer = 0                          # 当前相位已持续的秒数
GREEN_T, YELLOW_T, RED_T = 5, 1, 4

# 车辆列表：每个元素为 [x, 车道y, 速度]
cars = [[i * 120.0, ROAD_TOP + 25, 3.0] for i in range(4)]
passed = 0


def current_phase():
    """返回当前相位应持续的秒数，供计时判断使用"""
    if light_state == "green":
        return GREEN_T
    elif light_state == "yellow":
        return YELLOW_T
    return RED_T


running = True
while running:                           # 主循环：每一轮就是动画的一帧
    dt = clock.tick(FPS) / 1000.0          # 本帧耗时（秒），把帧率差异折算进位移

    # 事件处理：关闭窗口即退出循环，避免程序无法结束
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # ---------- 信号灯计时 ----------
    light_timer += dt
    if light_timer >= current_phase():     # 本相位到时，按 绿→黄→红→绿 轮转
        light_timer = 0
        if light_state == "green":
            light_state = "yellow"
        elif light_state == "yellow":
            light_state = "red"
        else:
            light_state = "green"

    # ---------- 车辆运动 ----------
    for car in cars:
        x, y, speed = car
        front = x + 40
        if light_state == "red" and front < STOP_LINE_X and front + speed * 60 >= STOP_LINE_X - 5:
            pass                            # 接近停止线且红灯：本帧不前进
        else:
            car[0] += speed * 60 * dt

        if car[0] > W:
            car[0] = -60
            passed += 1

    # ---------- 绘制 ----------
    screen.fill("#eef1f5")
    pygame.draw.rect(screen, "#5b5b5b", (0, ROAD_TOP, W, ROAD_BOTTOM - ROAD_TOP))
    pygame.draw.line(screen, "white", (0, 200), (W, 200), 2)
    pygame.draw.line(screen, "white", (STOP_LINE_X, ROAD_TOP), (STOP_LINE_X, ROAD_BOTTOM), 4)
    pygame.draw.line(screen, "white", (300, ROAD_TOP), (340, ROAD_TOP), 6)

    for car in cars:
        pygame.draw.rect(screen, "#2980b9", (int(car[0]), car[1] - 15, 40, 30), border_radius=6)

    color = {"green": "#27ae60", "yellow": "#f1c40f", "red": "#c0392b"}[light_state]
    pygame.draw.circle(screen, color, (60, 70), 26)

    info = "相位：" + light_state + "   已通过：" + str(passed) + " 辆"
    screen.blit(font.render(info, True, "#2c3e50"), (100, 50))

    pygame.display.flip()

pygame.quit()
sys.exit()
