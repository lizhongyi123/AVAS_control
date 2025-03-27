import math
import copy
import global_varible

def write_to_txt(path, lis):
    with open(path, 'w') as f:
        for i in lis:
            f.write(' '.join(map(str, i)) + '\n')

def add_to_txt(path, lis):
    with open(path, 'a') as f:
        for i in lis:
            f.write(' '.join(map(str, i)) + '\n')


def calculate_rms(data):
    if not data:
        raise ValueError("The input list cannot be empty.")
    x_mean = calculate_mean(data)
    square_sum = sum((x-x_mean) ** 2 for x in data)
    mean_square = square_sum / len(data)
    rms = math.sqrt(mean_square)

    return rms

def calculate_mean(data):
    if not data:
        raise ValueError("The input list cannot be empty.")

    total_sum = sum(data)
    mean = total_sum / len(data)

    return mean

def convert_dic2lis(dic):
    res = []
    for k, v in dic.items():
        v_lis = []
        if isinstance(v, list):
            v_lis.append(k)
            v_lis.extend(v)
        else:
            v_lis.append(k)
            v_lis.append(v)
        res.append(v_lis)

    return res

def format_output(code=0, msg="success", **kwargs):

    return {
        "code": code,
        "data": {
            "msg": msg,
            **kwargs
        }
    }


def judge_command_on_element(lattice, command):
    # 返回一个命令对应的是哪个元件
    lattice = copy.deepcopy(lattice)

    command_index = lattice.index(command)
    command_on_element = None
    for i in range(command_index, len(lattice)):
        if lattice[i][0] in global_varible.long_element:
            command_on_element = int(lattice[i][-1].split("_")[1])
            break
    return command_on_element

def delete_element_end_index(error_lattice):
    error_lattice_copy = copy.deepcopy(error_lattice)
    for i in error_lattice_copy:
        if i[0] in global_varible.long_element:
            i.pop()
    return error_lattice_copy

def add_element_end_index(error_lattice):
    error_lattice = copy.deepcopy(error_lattice)
    index = 0
    for i in error_lattice:
        if i[0] in global_varible.long_element:
            add_name = f'element_{index}'
            i.append(add_name)
            index += 1
    return error_lattice


#判断一个数能否转化成其他类型
def can_convert_to_othertype(s: str, target_type) -> bool:
    try:
        if target_type == int:
            v1 = float(s)
            if not v1.is_integer():  # 用 `is_integer()` 避免浮点数精度问题
                raise ValueError("Cannot convert to an integer")
        elif target_type == float:
            float(s)
        elif target_type == str:
            str(s)
        return True
    except ValueError:
        return False

def convert_to_othertype(s: str, target_type) -> bool:
    if target_type == int:
        v1 = int(float(s))
    elif target_type == float:
        v1 = float(s)
    if target_type == str:
        v1 = str(s)
    return v1

def safe_to_float(text, default=0.0):
    try:
        return float(text)
    except ValueError:
        return 0


if __name__ == '__main__':
    # code = 1
    # msg = "s"
    # kwargs = {"x": [1, 2, 3],
    #           "y": [1, 2, 3]}
    # value = format_output(msg ="dad")
    # print(value)
    v = "10.0"
    print(can_convert_to_othertype(v, float))