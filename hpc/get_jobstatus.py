
import subprocess
import uuid
import os
from utils.tool import format_output
def get_jobstatus_in_hpc(**item):
    job_id = item['jobId']
    print("job_id", job_id)
    result = subprocess.run(["squeue", "-j", str(job_id)], capture_output=True, text=True)

    lines = [line.strip() for line in result.stdout.strip().split("\n") if line.strip()]

    rows = [line.split() for line in lines]


    if len(rows) == 0:
        raise Exception("the jobId not exist")
    elif len(rows) == 1:
        if_finish = 2
    elif len(rows) == 2:
        if_finish = 1

    kwargs = {}
    kwargs.update({"jobStatus": rows, "ifFinish": if_finish, })

    output = format_output(**kwargs)
    return output


def get_jobstatus_in_windows(**item):
    rows = [['JOBID', 'PARTITION', 'NAME', 'USER', 'ST', 'TIME', 'NODES', 'NODELIST(REASON)'],
        ['961397', 'cpup8', 'AVAS56', 'lizhongy', 'PD', '0:00', '1', '(Priority)']]

    project_path = item['projectPath']

    signa_path = os.path.join(project_path, "OutputFile", "signal.txt")
    with open(signa_path, 'r') as f:
        text = f.read()

    text = text.strip()
    if text == "1":
        status_list = rows
    elif text == "2":
        status_list = [rows[0]]
    else:
        status_list = [rows[0]]

    if_finish = 1
    if len(status_list) == 1:
        if_finish = 2
    elif len(status_list) == 2:
        if_finish = 1

    kwargs = {'jobStatus': status_list,
              "ifFinish": if_finish,
    }

    output = format_output(**kwargs)
    return output

if __name__ == '__main__':
    project_path = r"C:\Users\shliu\Desktop\test_schedule\cafe_avas_error"
    item = {"projectPath": project_path}
    result = get_jobstatus_in_windows(**item)
    print(result)




