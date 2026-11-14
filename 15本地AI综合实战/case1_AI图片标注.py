# -*- coding: utf-8 -*-
"""案例 15-1：基于本地 Ollama 的交通场景图片批量标注（RTX 3050 适配）。

用法：
  python3 case1_AI图片标注.py                    # 离线演示模式（默认，无需 Ollama / GPU）
  python3 case1_AI图片标注.py --live             # 真实调用本机 Ollama
  python3 case1_AI图片标注.py --live --vram 4    # 4GB/6GB 显存档位，自动换 moondream

输出：output/labels.json、output/labels.csv
离线边界：真实调用只连 127.0.0.1:11434；首次 ollama pull 需联网，之后可断网运行。
"""
import json
import sys
from pathlib import Path
from tempfile import TemporaryDirectory

from ai_common import (check_service, image_to_b64, post_chat, save_csv,
                       save_json, select_model, summary, validate)
from make_sample_images import build as build_images

HERE = Path(__file__).resolve().parent
OUT = HERE / "output"

SCHEMA = {
    "type": "object",
    "properties": {
        "scene": {"type": "string"},
        "congestion": {"type": "string"},
        "vehicle_count": {"type": "integer"},
        "risk": {"type": "string"},
        "caption": {"type": "string"},
    },
    "required": ["scene", "congestion", "vehicle_count", "risk", "caption"],
}
REQUIRED = SCHEMA["required"]
ENUMS = {
    "congestion": ["畅通", "缓行", "拥堵"],
    "risk": ["无", "低", "中", "高"],
}
FIELDS = ["file", "scene", "congestion", "vehicle_count", "risk", "caption", "model"]
PROMPT = (
    "你是交通场景标注员。只输出一个 JSON 对象，不要任何解释文字。"
    "字段：scene（场景简述）、congestion（畅通/缓行/拥堵三选一）、"
    "vehicle_count（整数，画面中的车辆数）、risk（无/低/中/高四选一）、"
    "caption（一句中文描述）。"
)

# 离线演示用的确定性桩：前三张是「已知答案样本」，用于效果验证
DEMO_ANSWERS = {
    "road_clear": {"scene": "城市道路", "congestion": "畅通", "vehicle_count": 1,
                   "risk": "无", "caption": "绿灯路口仅一辆车通行"},
    "road_jam": {"scene": "城市道路", "congestion": "拥堵", "vehicle_count": 11,
                 "risk": "低", "caption": "多车密集排队，通行缓慢"},
    "road_incident": {"scene": "事故现场", "congestion": "缓行", "vehicle_count": 2,
                      "risk": "高", "caption": "两车相撞并设有警示标志"},
}
KNOWN = [
    ("road_clear", "congestion", "畅通"),
    ("road_jam", "congestion", "拥堵"),
    ("road_incident", "risk", "高"),
]


def demo_answer(stem):
    """演示桩：road_foggy 故意返回非 JSON 文本，用来走通容错分支。"""
    if stem == "road_foggy":
        return "这张图太模糊了，我无法判断，建议重新拍摄。"
    return json.dumps(DEMO_ANSWERS.get(stem, {}), ensure_ascii=False)


def infer_content(path, model, live, strict=False):
    if not live:
        return demo_answer(path.stem)
    prompt = PROMPT if not strict else PROMPT + " 请严格只输出 JSON，不要任何前后缀。"
    return post_chat(model, prompt, SCHEMA, images=[image_to_b64(path)])


def parse_args(argv):
    live = "--live" in argv
    vram = 8
    if "--vram" in argv:
        i = argv.index("--vram")
        if i + 1 < len(argv):
            try:
                vram = int(argv[i + 1])
            except ValueError:
                vram = 8
    return live, vram


def verify_output(rows, known):
    """已知答案样本核对：真实模型上线后，这个数字就是持续监控的质量指标。"""
    hits = 0
    for stem, field, expect in known:
        row = next((r for r in rows if r["file"] == stem + ".png"), None)
        if row and row[field] == expect:
            hits += 1
    print("已知答案样本： %d 条 | 命中： %d" % (len(known), hits))
    return hits


def main(argv=None):
    argv = sys.argv[1:] if argv is None else argv
    live, vram = parse_args(argv)
    vram_key, model = select_model("vision", vram)
    mode = "真实调用" if live else "离线演示"

    if live:
        ok, info = check_service()
        if not ok:
            print("本机 Ollama 未就绪（%s），自动降级为离线演示模式" % info)
            live = False
            mode = "离线演示（自动降级）"

    print("运行模式：", mode, "| 显存档位：", vram_key, "GB | 模型：", model)

    with TemporaryDirectory() as tmp:
        img_dir = HERE / "sample_images"
        imgs = sorted(img_dir.glob("*.png")) if img_dir.exists() else []
        if not imgs:                       # 没有自备图片时，用标准库造 4 张示意图
            img_dir = Path(tmp)
            build_images(img_dir)
            imgs = sorted(img_dir.glob("*.png"))
        print("待标注图片：", len(imgs), "张")

        rows, failed, retries = [], [], 0
        for p in imgs:
            content = infer_content(p, model, live)
            data, msg = validate(content, REQUIRED, ENUMS)
            if data is None and live:      # 真实调用失败时，收紧提示词重试一次
                content = infer_content(p, model, live, strict=True)
                data, msg = validate(content, REQUIRED, ENUMS)
                retries += 1
            if data is None:
                failed.append(p.name)
                print(" ", p.name, "→", msg, "（记入失败日志）")
                continue
            print(" ", p.name, "→", msg)
            row = dict(data)
            row["file"] = p.name
            row["model"] = model
            rows.append(row)

        if failed:
            print("不合格样本：", failed)
        save_json(rows, OUT / "labels.json")
        save_csv(rows, OUT / "labels.csv", FIELDS)
        print("已写入 output/labels.json（%d 条）" % len(rows))
        print("已写入 output/labels.csv（%d 条）" % len(rows))
        verify_output(rows, KNOWN)

    summary(len(rows), len(imgs), retries, mode, model, vram_key)


if __name__ == "__main__":
    main()
