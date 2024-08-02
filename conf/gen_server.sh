#!/bin/bash

#tabtoy.exe -mode=v3 -index=Index.xlsx -package=main -go_out=../dist/server/code/table_gen.go --tag_action=nogenfield_binary:server -json_out=../dist/server/conf/table_gen.json
#tabtoy.exe -mode=v3 -index=meta/Item.xlsx -package=conf -go_out=table_gen.go --tag_action=nogenfield_json:client -json_out=table_gen.json
# todo 应该在golang生成文件中也不该导入client的字段。
#tabtoy.exe -mode=v3 -index=Index.xlsx -package=main -go_out=table_gen.go --tag_action=nogenfield_json:client|nogenfield_go -json_out=table_gen.json

# todo 
#python bin/gen_code.py
echo 生成OK
echo 按任意键继续...
read -n 1
