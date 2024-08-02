from pathlib import Path
import subprocess
import os
import const


def run_command(command):
    result = subprocess.run(command, capture_output=True, text=True, encoding='utf-8')

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

    def export_server(self, file_path):
        file_base_name = file_path.stem
        print(f"file_name:{file_base_name}")

        go_out = os.path.join( const.server_go_out_path, file_base_name[0].upper() + file_base_name[1:] + ".go")
        json_out = os.path.join(const.server_conf_out_path, file_base_name[0].lower() + file_base_name[1:] + ".json")
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
    #  todo 需要很多个变量表
    m = Meta(const.meta_path, "server")
    m.read_meta()


if __name__ == "__main__":
    main()
