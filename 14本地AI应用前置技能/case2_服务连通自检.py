# -*- coding: utf-8 -*-
"""案例 14-2：本地 Ollama 服务的请求构造与结构化返回解析（离线演示版）。

主程序不发起真实网络请求，输出在任何机器上一致，便于课堂统一校对；
check_service() 供本机部署完成后调用，步骤见讲义 14.8。
"""
import json
from urllib.error import URLError
from urllib.request import Request, urlopen

BASE = "http://127.0.0.1:11434"


def build_request(model, prompt):
    """构造 /api/chat 的 POST 请求，并用 format 约定返回结构。"""
    payload = {
        "model": model,
        "messages": [{"role": "user", "content": prompt}],
        "stream": False,
        "format": {
            "type": "object",
            "properties": {
                "level": {"type": "string"},
                "road": {"type": "string"},
            },
            "required": ["level", "road"],
        },
    }
    body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    return Request(BASE + "/api/chat", data=body,
                   headers={"Content-Type": "application/json"}, method="POST")


def check_service(timeout=2):
    """真实连通性自检：返回 (是否连通, 说明)。本机部署后再调用。"""
    try:
        with urlopen(BASE + "/api/version", timeout=timeout) as resp:
            return True, "HTTP %d" % resp.status
    except URLError as e:
        return False, "服务未启动或端口不通：%s" % e.reason
    except Exception as e:
        return False, "未知错误：%s" % e


def parse_label(content):
    """把模型返回的 content 解析成标注字典，并做字段与取值校验。"""
    data = json.loads(content)
    missing = [k for k in ("level", "road") if k not in data]
    if missing:
        return None, "缺字段：" + "、".join(missing)
    if data["level"] not in ("畅通", "缓行", "拥堵"):
        return None, "level 取值非法：" + str(data["level"])
    return data, "校验通过"


req = build_request("qwen2.5:3b", "判读：机场北平均车速 35.5km/h")
print("请求方法：", req.get_method())
print("请求地址：", req.full_url)
print("请求体字节数：", len(req.data))
print("format.required：", json.loads(req.data)["format"]["required"])

# 模拟三条模型返回：一条正常、一条缺字段、一条不是合法 JSON
samples = [
    '{"road": "机场北", "level": "拥堵"}',
    '{"road": "京开"}',
    '{"road": "机场南", "level": "拥堵",',
]
print("—— 结构化返回校验 ——")
for i, content in enumerate(samples, 1):
    try:
        label, msg = parse_label(content)
        print("样本", i, "：", msg, "|", label)
    except json.JSONDecodeError as e:
        print("样本", i, "：JSON 解析失败 →", e.msg)
print("提示：连通性自检函数 check_service() 需本机部署 Ollama 后调用")
