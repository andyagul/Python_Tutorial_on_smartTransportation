#!/bin/zsh
# 双击本文件即可在浏览器中打开智慧交通 Python 课件
cd "$(dirname "$0")" || exit 1

# 清除可能残留的代理变量：JupyterLab 启动时会据此构建 httpx 代理通道，
# 若本机证书文件缺失，会导致 "FileNotFoundError: certifi/cacert.pem" 而无法启动。
unset HTTP_PROXY HTTPS_PROXY http_proxy https_proxy ALL_PROXY all_proxy 2>/dev/null

JUPYTER="$(command -v jupyter)"
if [ -z "$JUPYTER" ]; then
    for p in /opt/homebrew/bin/jupyter /usr/local/bin/jupyter; do
        [ -x "$p" ] && JUPYTER="$p" && break
    done
fi

if [ -z "$JUPYTER" ]; then
    echo "未找到 jupyter 命令。请先安装 JupyterLab："
    echo "    python3 -m pip install jupyterlab"
    echo ""
    read -r "?按回车键退出…"
    exit 1
fi

echo "正在启动 JupyterLab 课件…（关闭本终端窗口即可停止服务）"
exec "$JUPYTER" lab "00_课程索引.ipynb"
