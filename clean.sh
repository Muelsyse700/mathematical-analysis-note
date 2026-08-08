#!/bin/zsh

# 获取脚本所在的当前目录绝对路径
SCRIPT_DIR="$( cd "$( dirname "${(%):-%x}" )" && pwd )"

echo "开始清理目录下的 LaTeX 辅助文件："
echo "$SCRIPT_DIR"
echo "--------------------------------"

# 查找并删除常见的 LaTeX 编译中间文件，同时打印被删除的文件路径
find "$SCRIPT_DIR" -type f \( \
    -name "*.aux" -o \
    -name "*.log" -o \
    -name "*.toc" -o \
    -name "*.out" -o \
    -name "*.bbl" -o \
    -name "*.blg" -o \
    -name "*.synctex.gz" -o \
    -name "*.fdb_latexmk" -o \
    -name "*.fls" -o \
    -name "*.nav" -o \
    -name "*.snm" -o \
    -name "*.vrb" -o \
    -name "*.bcf" -o \
    -name "*.run.xml" \
\) -print -delete

echo "--------------------------------"
echo "清理完成！"