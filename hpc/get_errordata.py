import os
from utils.tool import format_output
def get_errordata(**item):
    error_exist = False
    project_path = item['projectPath']
    err_path = os.path.join(project_path, "OutputFile", "tmp", "errordata.log")
    with open(err_path, 'r') as file:
        text = file.read()
        if text.strip():  # 去除空格和换行后仍有内容
            error_exist = True
        else:
            error_exist = False
    if error_exist:
        kwargs = {"errorInfo": text}
    else:
        kwargs = {"errorInfo": ""}

    output = format_output(**kwargs)
    return output


if __name__ == '__main__':
    item = {
        "projectPath": r"C:\Users\shliu\Desktop\test_schedule\cafe_avas"
    }
    res = get_errordata(**item)
    print(res)