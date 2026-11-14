# -*- coding: utf-8 -*-
"""案例 15-2：基于本地 Ollama 的交通事件文本结构化抽取与分类（RTX 3050 适配）。

用法：
  python3 case2_交通事件NLP.py                    # 离线演示模式（默认）
  python3 case2_交通事件NLP.py --live             # 真实调用本机 Ollama
  python3 case2_交通事件NLP.py --live --vram 4    # 4GB/6GB 显存档位

输入：events_sample.txt（5 条交通事件自由文本）
输出：output/nlp_results.json、output/nlp_report.csv
"""
import json
import re
import sys
from collections import Counter
from pathlib import Path

from ai_common import (check_service, post_chat, save_csv, save_json,
                       select_model, summary, validate)

HERE = Path(__file__).resolve().parent
OUT = HERE / "output"
EVENTS_FILE = HERE / "events_sample.txt"

PLATE = re.compile(r"[\u4e00-\u9fa5][A-Z]\d{5}")
ROAD = re.compile(r"机场北|机场南|京开|京港澳")
TIME = re.compile(r"\d{2}:\d{2}")
SPEED = re.compile(r"(\d+)\s*km/h")

SCHEMA = {
    "type": "object",
    "properties": {
        "event_type": {"type": "string"},
        "road": {"type": "string"},
        "severity": {"type": "string"},
        "time": {"type": "string"},
        "summary": {"type": "string"},
    },
    "required": ["event_type", "road", "severity", "time", "summary"],
}
REQUIRED = SCHEMA["required"]
ENUMS = {
    "event_type": ["事故", "拥堵", "施工", "通行正常"],
    "severity": ["低", "中", "高"],
}
FIELDS = ["time", "road", "event_type", "severity", "speed", "summary", "model"]
PROMPT = (
    "你是交通事件分类员。只输出一个 JSON 对象，不要解释。"
    "字段：event_type（事故/拥堵/施工/通行正常四选一）、road（路段名）、"
    "severity（低/中/高三选一）、time（HH:MM）、summary（一句中文摘要）。"
)
TRUTH = {
    "08:12": "事故",
    "09:05": "拥堵",
    "10:30": "事故",
    "14:20": "施工",
    "17:45": "通行正常",
}


def preprocess(line):
    """正则预清洗：车牌脱敏 + 抽出时间 / 路段 / 车速，减少模型负担。"""
    plates = len(PLATE.findall(line))
    clean = PLATE.sub("【车牌】", line)
    t, road, sp = TIME.search(clean), ROAD.search(clean), SPEED.search(clean)
    return {
        "time": t.group() if t else "",
        "road": road.group() if road else "",
        "speed": int(sp.group(1)) if sp else 0,
        "text": clean,
        "plates": plates,
    }


def demo_answer(item):
    """离线演示桩：按关键词规则给出确定性分类，走与真实模型相同的校验链路。"""
    text = item["text"]
    if "追尾" in text or "撞" in text:
        et, sev = "事故", "高"
    elif "施工" in text:
        et, sev = "施工", "中"
    elif "缓行" in text or "通行缓慢" in text:
        et, sev = "拥堵", "中"
    else:
        et, sev = "通行正常", "低"
    return json.dumps({
        "event_type": et,
        "road": item["road"],
        "severity": sev,
        "time": item["time"],
        "summary": text[:18],
    }, ensure_ascii=False)


def infer_content(item, model, live, strict=False):
    if not live:
        return demo_answer(item)
    prompt = PROMPT + "\n待分类文本：" + item["text"]
    if strict:
        prompt += "\n请严格只输出 JSON，不要任何前后缀。"
    return post_chat(model, prompt, SCHEMA)


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


def main(argv=None):
    argv = sys.argv[1:] if argv is None else argv
    live, vram = parse_args(argv)
    vram_key, model = select_model("text", vram)
    mode = "真实调用" if live else "离线演示"

    if live:
        ok, info = check_service()
        if not ok:
            print("本机 Ollama 未就绪（%s），自动降级为离线演示模式" % info)
            live = False
            mode = "离线演示（自动降级）"

    lines = [l.strip() for l in EVENTS_FILE.read_text(encoding="utf-8").splitlines() if l.strip()]
    items = [preprocess(l) for l in lines]
    print("运行模式：", mode, "| 显存档位：", vram_key, "GB | 模型：", model)
    print("读入事件：", len(items), "条 | 脱敏车牌：", sum(it["plates"] for it in items), "处")

    rows, failed, retries = [], [], 0
    for i, item in enumerate(items, 1):
        content = infer_content(item, model, live)
        data, msg = validate(content, REQUIRED, ENUMS)
        if data is None and live:
            content = infer_content(item, model, live, strict=True)
            data, msg = validate(content, REQUIRED, ENUMS)
            retries += 1
        if data is None:
            failed.append(i)
            print("  事件", i, "→", msg, "（记入失败日志）")
            continue
        row = dict(data)
        row["speed"] = item["speed"]
        row["model"] = model
        rows.append(row)
        print("  事件", i, "→", row["event_type"], "/", row["severity"], "/", row["road"])

    dist = Counter(r["event_type"] for r in rows)
    print("事件类型分布：", dict(dist))
    hits = sum(1 for r in rows if TRUTH.get(r["time"]) == r["event_type"])
    print("已知答案样本： %d 条 | 命中： %d | 准确率： %.1f %%"
          % (len(TRUTH), hits, hits / len(TRUTH) * 100))
    save_json(rows, OUT / "nlp_results.json")
    save_csv(rows, OUT / "nlp_report.csv", FIELDS)
    print("已写入 output/nlp_results.json（%d 条）" % len(rows))
    print("已写入 output/nlp_report.csv（%d 条）" % len(rows))

    summary(len(rows), len(items), retries, mode, model, vram_key)


if __name__ == "__main__":
    main()
