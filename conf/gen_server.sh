#!/bin/bash

tabtoy.exe -mode=v3 -index=Index.xlsx -package=main -go_out=../dist/server/code/table_gen.go -json_out=../dist/server/conf/table_gen.json

echo 生成OK
echo 按任意键继续...
read -n 1
