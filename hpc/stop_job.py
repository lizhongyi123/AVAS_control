import subprocess
import uuid
import os
from utils.tool import format_output
def stop_job(**item):
    job_id = item['jobId']

    result = subprocess.run(["scancel", job_id], capture_output=True, text=True)

    # print(f"? STDOUT:\n{result.stdout}")
    # print(f"? STDERR:\n{result.stderr}")

    # # ���в�������ȥ�����У�
    # lines = [line.strip() for line in result.stdout.strip().split("\n") if line.strip()]
    #
    # # ���зָ�ÿһ�У����ɶ�ά�б�
    # rows = [line.split() for line in lines]
    #

    kwargs = {}
    kwargs.update({"jobStatus": []})

    output = format_output(**kwargs)

    return output