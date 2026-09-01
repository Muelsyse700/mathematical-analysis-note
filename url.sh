#!/bin/bash

read -r -p "URL: " url

escaped=$(printf '%s' "$url" | sed \
    -e 's/\\/\\textbackslash{}/g' \
    -e 's/\([#$%&_{}]\)/\\\1/g' \
    -e 's/~/\\textasciitilde{}/g' \
    -e 's/\^/\\textasciicircum{}/g')

printf '%s' "$escaped" | pbcopy

printf '\n已复制到剪贴板：\n%s\n' "$escaped"