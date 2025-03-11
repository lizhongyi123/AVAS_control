import copy
import global_varible

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
