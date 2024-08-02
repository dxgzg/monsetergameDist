from pathlib import Path
import subprocess
import os
import const
import re
from go_helper_template import *


# from go_helper_template import res_field_content


def run_command(command):
    result = subprocess.run(command, cwd=const.target_work_path, capture_output=True, text=True, encoding='utf-8')

    print(f"run command result:{result.stdout}")


class Meta:
    def __init__(self, path, export_type):
        self.path = Path(path)
        self.export_type = export_type

    def read_meta(self):
        for file_path in self.path.rglob("*.xlsx"):
            if '~$' in file_path.name:
                continue

            # file_name = file_path.name
            if self.export_type == "server":
                self.export_server(file_path)
                self.export_server_helper_gen(file_path)

        self.export_server_helper_file_create()

    def export_server_helper_file_create(self):
        file_name = "Helper.go"
        helper_content = go_helper_template.replace("${res_field_content}", res_field_content). \
            replace("${res_field_init_content}", res_field_init_content).replace("${res_load}", res_load). \
            replace("${res_load_funcs}", res_load_funcs)

        with open(os.path.join(const.server_helper_out_path, file_name), "w",encoding='utf-8') as file:
            file.write(helper_content)

    def export_server_helper_gen(self, file_path):
        file_base_name = file_path.stem
        file_base_name_without_meta = re.sub(r'meta', '', file_base_name, flags=re.IGNORECASE)
        file_base_name_first_upper = file_base_name_without_meta[0].upper() + file_base_name_without_meta[1:]
        file_base_name_first_lower = file_base_name_without_meta[0].lower() + file_base_name_without_meta[1:]

        self.proc_server_helper_field_content(file_base_name_first_upper)
        self.proc_server_helper_init_content(file_base_name_first_upper)
        self.proc_server_helper_load(file_base_name_first_upper)
        self.proc_server_helper_load_funcs(file_base_name_first_lower)

    def proc_server_helper_field_content(self, file_base_name_title_case):
        global res_field_content
        res_field_content += f"{file_base_name_title_case} *Table\n"

    def proc_server_helper_init_content(self, file_base_name_title_case):
        global res_field_init_content
        res_field_init_content += f"helper.{file_base_name_title_case} = NewTable()\n"

    def proc_server_helper_load(self, file_base_name_title_case):
        global res_load
        res_load_proc = go_load_err_template.replace(code_template_replace_str, file_base_name_title_case)
        res_load += f"{res_load_proc}\n"

    def proc_server_helper_load_funcs(self, file_base_name_first_lower):
        global res_load_funcs
        file_base_name_first_upper = file_base_name_first_lower[0].upper() + file_base_name_first_lower[1:]

        res_func = go_load_funcs_template.replace(code_template_replace_str, file_base_name_first_lower)
        res_func = res_func.replace(res_first_upper, file_base_name_first_upper)
        res_load_funcs += f"{res_func}\n"

    def export_server(self, file_path):
        file_base_name = file_path.stem
        print(f"file_name:{file_base_name}")

        file_base_name_without_meta = re.sub(r'meta', '', file_base_name, flags=re.IGNORECASE)
        go_out = os.path.join(const.server_go_out_path,
                              file_base_name_without_meta[0].upper() + file_base_name_without_meta[1:] + ".go")
        json_out = os.path.join(const.server_conf_out_path,
                                file_base_name_without_meta[0].lower() + file_base_name_without_meta[1:] + ".json")
        command = [
            'tabtoy.exe',
            '-mode=v3',
            f'-index={file_path}',
            '-package=conf',
            f'-go_out={go_out}',
            '--tag_action=nogenfield_json:client',
            f'-json_out={json_out}'
        ]

        run_command(command)


# 值得注意的是在哪里运行的tabtoy,他的工作目录就在哪里，所以读取type表或者资源表都需要../来表示上级目录
def main():
    m = Meta(const.meta_path, "server")
    m.read_meta()


if __name__ == "__main__":
    main()
