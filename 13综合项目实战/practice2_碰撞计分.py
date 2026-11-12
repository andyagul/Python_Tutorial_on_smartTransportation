# ---------- 第 13 章 综合项目实战 · 练习 13-2 参考答案：给车流仿真加碰撞检测与计分 ----------
# 对应知识点：13.5 pygame.Rect 与 colliderect() 碰撞检测、13.4 主循环改造、7.3 sorted(key=)
# 功能说明：同车道前后车矩形重叠即判定追尾并扣分，车辆通过路口加分，界面实时显示得分

import pygame
import sys

W, H = 800, 400
FPS = 60
LANES = [175, 225]                       # 两条车道的中心 y 坐标

pygame.init()
screen = pygame.display.set_mode((W, H))
pygame.display.set_caption("智慧路口车流仿真 · 碰撞检测")
clock = pygame.time.Clock()
font = pygame.font.SysFont("microsoftyahei", 20)

cars = []
for i, y in enumerate(LANES):
    for k in range(3):
        # 每条车道 3 辆车，初始 x 互相错开 150 像素，避免开局就重叠
        cars.append({"x": -k * 150.0 - i * 40, "y": y, "v": 3.0})

score = 0
crashes = 0


def rect_of(car):
    """把车辆字典转成 pygame.Rect，用于碰撞检测（x, y, 宽, 高）"""
    return pygame.Rect(int(car["x"]), car["y"] - 15, 40, 30)


running = True
while running:
    dt = clock.tick(FPS) / 1000.0
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    for car in cars:
        car["x"] += car["v"] * 60 * dt
        if car["x"] > W:
            car["x"] = -60
            score += 1

    # 同车道碰撞检测：先按车道分组，再按 x 排序，只有相邻两车才可能追尾
    for y in LANES:
        same = [c for c in cars if c["y"] == y]
        same.sort(key=lambda c: c["x"])
        for i in range(len(same) - 1):
            if rect_of(same[i]).colliderect(rect_of(same[i + 1])):
                # 矩形重叠 → 判定追尾：后车停住、扣分、并退到前车之后
                same[i + 1]["v"] = 0
                crashes += 1
                score -= 5
                same[i + 1]["x"] = same[i]["x"] - 42   # 回退，避免下一帧重复计数
            else:
                same[i + 1]["v"] = 3.0                 # 未碰撞则恢复正常速度

    screen.fill("#eef1f5")
    pygame.draw.rect(screen, "#5b5b5b", (0, 150, W, 100))
    for y in LANES:
        pygame.draw.line(screen, "white", (0, y + 25), (W, y + 25), 1)

    for car in cars:
        pygame.draw.rect(screen, "#2980b9", rect_of(car), border_radius=6)

    screen.blit(font.render("得分：" + str(score) + "   碰撞：" + str(crashes), True, "#2c3e50"), (20, 20))
    pygame.display.flip()

pygame.quit()
sys.exit()
