import math


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