# -*- coding: utf-8 -*-
"""案例 14-1：待标注图片目录清点与 base64 预检（纯标准库，可离线运行）。

本例用 tempfile 临时造一批演示文件，避免依赖真实图片。
实际使用时把 root 改成 Path("images") 即可，其余代码不用动。
"""
import base64
import json
from pathlib import Path
from tempfile import TemporaryDirectory

MIME = {
    ".jpg": "image/jpeg",
    ".jpeg": "image/jpeg",
    ".png": "image/png",
    ".webp": "image/webp",
}


def scan(root):
    """遍历目录，返回图片清单；非图片文件与子目录自动跳过。"""
    items = []
    for p in sorted(root.glob("*")):
        if not p.is_file():
            continue
        mime = MIME.get(p.suffix.lower())
        if mime is None:
            continue
        data = p.read_bytes()
        items.append({
            "file": p.name,
            "mime": mime,
            "bytes": len(data),
            "b64_len": len(base64.b64encode(data)),
        })
    return items


with TemporaryDirectory() as tmp:
    root = Path(tmp)
    (root / "cam01.jpg").write_bytes(b"\xff\xd8" + b"IMG-01" + b"\xff\xd9")
    (root / "cam02.png").write_bytes(b"\x89PNG\r\n\x1a\n" + b"IMG-02")
    (root / "cam03.jpg").write_bytes(b"\xff\xd8" + b"IMG-03-LONG" + b"\xff\xd9")
    (root / "notes.txt").write_text("课堂记录", encoding="utf-8")
    (root / "labels").mkdir()

    items = scan(root)
    print("发现图片：", len(items), "张（notes.txt 与 labels/ 已跳过）")
    for it in items:
        print(" ", it["file"], "|", it["mime"], "|", it["bytes"], "字节 | base64", it["b64_len"], "字符")
    print("base64 总长度：", sum(it["b64_len"] for it in items), "字符")
    manifest = json.dumps({"count": len(items), "items": items}, ensure_ascii=False)
    print("清单 JSON 长度：", len(manifest), "字符")
