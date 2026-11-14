# -*- coding: utf-8 -*-
"""用纯标准库生成 4 张交通场景示意 PNG，供案例 15-1 开箱演示。

不需要联网下载素材，也不需要 Pillow。
真实教学时，把学生自己拍的路口照片放进 sample_images/ 即可覆盖本示意图。

用法：
  python3 make_sample_images.py                 # 生成到 ./sample_images
  python3 make_sample_images.py 指定目录        # 生成到指定目录
"""
import struct
import sys
import zlib
from pathlib import Path


def make_png(width, height, painter):
    """按 painter(x, y) -> (r, g, b) 逐像素生成 PNG 字节（8bit RGB）。"""
    raw = bytearray()
    for y in range(height):
        raw.append(0)                         # PNG 每行的 filter type：0 = None
        for x in range(width):
            raw.extend(painter(x, y))

    def chunk(tag, data):
        return (struct.pack(">I", len(data)) + tag + data +
                struct.pack(">I", zlib.crc32(tag + data) & 0xffffffff))

    ihdr = struct.pack(">IIBBBBB", width, height, 8, 2, 0, 0, 0)
    return (b"\x89PNG\r\n\x1a\n" +
            chunk(b"IHDR", ihdr) +
            chunk(b"IDAT", zlib.compress(bytes(raw), 9)) +
            chunk(b"IEND", b""))


def clear_scene(x, y):
    """畅通：绿灯 + 一辆车 + 车道虚线。"""
    if (x - 48) ** 2 + (y - 12) ** 2 <= 64:
        return (60, 205, 95)
    if 30 <= y < 33 and (x // 8) % 2 == 0:
        return (238, 238, 238)
    if 20 <= x < 28 and 38 <= y < 54:
        return (45, 115, 225)
    return (72, 76, 82)


def jam_scene(x, y):
    """拥堵：同一车道密集排了 6 辆车。"""
    for i in range(6):
        if 6 + i * 9 <= x < 12 + i * 9 and 22 <= y < 42:
            return (200 - i * 12, 80 + i * 10, 60 + i * 15)
    for i in range(5):
        if 8 + i * 11 <= x < 15 + i * 11 and 46 <= y < 62:
            return (60 + i * 18, 120, 200 - i * 14)
    return (72, 76, 82)


def incident_scene(x, y):
    """事故：两车相接 + 黄色警示块。"""
    if 10 <= x < 28 and 26 <= y < 42:
        return (215, 70, 60)
    if 28 <= x < 44 and 28 <= y < 44:
        return (55, 110, 215)
    if 50 <= x < 60 and 8 <= y < 18:
        return (240, 200, 50)
    return (72, 76, 82)


def foggy_scene(x, y):
    """雾天：整体低对比度，用于演示「模型未按格式输出」的容错分支。"""
    v = 140 + ((x + y) // 8) % 4 * 3
    if 26 <= x < 38 and 28 <= y < 40:
        return (v - 8, v - 8, v - 8)
    return (v, v, v)


SCENES = {
    "road_clear": clear_scene,
    "road_jam": jam_scene,
    "road_incident": incident_scene,
    "road_foggy": foggy_scene,
}


def build(target):
    """在 target 目录生成 4 张 64x64 示意 PNG，返回排序后的文件名列表。"""
    root = Path(target)
    root.mkdir(parents=True, exist_ok=True)
    made = []
    for name, painter in SCENES.items():
        p = root / (name + ".png")
        p.write_bytes(make_png(64, 64, painter))
        made.append(p.name)
    return sorted(made)


if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else "sample_images"
    names = build(out)
    print("已生成示意图片：", len(names), "张 →", out)
    for n in names:
        print(" ", n, (Path(out) / n).stat().st_size, "字节")
