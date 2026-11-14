# -*- coding: utf-8 -*-
"""第 15 章共享工具模块：本地 Ollama 调用、模型选择、结果校验与落盘。

两个实战案例共用本模块，对应第 10 章「模块与程序包」的组织方式。

设计原则：
1. 只依赖 Python 标准库，不装任何第三方包；
2. 真实调用只走 127.0.0.1:11434，不访问任何外部在线 API；
3. 模型返回一律「先解析、再校验、后使用」，坏数据记日志不伪造默认值。
"""
import base64
import csv
import json
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

BASE = "http://127.0.0.1:11434"
TIMEOUT = 120                       # 首次加载模型较慢，给出足够超时

# RTX 3050 双档位：8GB 台式 / 4GB·6GB 笔记本
PROFILES = {
    8: {"vision": "gemma3:4b", "text": "qwen2.5:3b"},
    4: {"vision": "moondream", "text": "qwen2.5:3b"},
}


def select_model(kind, vram_gb=8):
    """按显存容量选档位与模型，返回 (档位, 模型名)。"""
    key = 8 if vram_gb >= 8 else 4
    return key, PROFILES[key][kind]


def check_service(timeout=2):
    """本机服务连通性自检，返回 (是否连通, 说明)。"""
    try:
        with urlopen(BASE + "/api/version", timeout=timeout) as resp:
            return True, "HTTP %d" % resp.status
    except (HTTPError, URLError) as e:
        return False, "服务不可达：%s" % e
    except Exception as e:
        return False, "未知错误：%s" % e


def image_to_b64(path):
    """图片 -> 纯 base64 字符串（Ollama 的 images 字段只收载荷，不要 data URL 前缀）。"""
    return base64.b64encode(Path(path).read_bytes()).decode("ascii")


def post_chat(model, prompt, schema, images=None, timeout=TIMEOUT):
    """向本机 /api/chat 发一次 POST，返回模型输出的 content 字符串。"""
    payload = {
        "model": model,
        "messages": [{"role": "user", "content": prompt}],
        "stream": False,
        "format": schema,                  # 语法约束：只保证 JSON 可解析
        "options": {"temperature": 0},     # 降低随机性，便于课堂复现
    }
    if images:
        payload["messages"][0]["images"] = images
    body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    req = Request(BASE + "/api/chat", data=body,
                  headers={"Content-Type": "application/json"}, method="POST")
    with urlopen(req, timeout=timeout) as resp:
        return json.loads(resp.read().decode("utf-8"))["message"]["content"]


def validate(content, required, enums=None):
    """解析 + 语义校验，返回 (数据, 说明)；任何一环失败都返回 (None, 原因)。"""
    try:
        data = json.loads(content)
    except json.JSONDecodeError as e:
        return None, "JSON 解析失败：" + e.msg
    if not isinstance(data, dict):
        return None, "返回不是 JSON 对象"
    missing = [k for k in required if k not in data]
    if missing:
        return None, "缺字段：" + "、".join(missing)
    for key, allowed in (enums or {}).items():
        if data.get(key) not in allowed:
            return None, "%s 取值非法：%s" % (key, data.get(key))
    return data, "校验通过"


def save_json(rows, path):
    """结构化结果落盘为 UTF-8 JSON。"""
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(rows, ensure_ascii=False, indent=2), encoding="utf-8")
    return p


def save_csv(rows, path, fields):
    """同一批结果另存 CSV，utf-8-sig 让 Excel 打开中文不乱码。"""
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    with p.open("w", encoding="utf-8-sig", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields, lineterminator="\n")
        w.writeheader()
        for r in rows:
            w.writerow({k: r.get(k, "") for k in fields})
    return p


def summary(ok, total, retries, mode, model, vram_key):
    """统一汇总输出；不含耗时等随机器变化的值，便于当堂逐字校对。"""
    print("—— 运行汇总 ——")
    print("运行模式：", mode, "| 显存档位：", vram_key, "GB | 模型：", model)
    print("处理条数：", total, "| 合格：", ok, "| 重试：", retries)
    print("合格率：", round(ok / total * 100, 1) if total else 0.0, "%")
    print("服务地址： 127.0.0.1:11434（仅本机）| 外部在线 API： 无")
