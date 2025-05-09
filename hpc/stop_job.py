import subprocess
import uuid
import os
from utils.tool import format_output
def stop_job(**item):
    job_id = item['jobId']

    result = subprocess.run(["scancel", job_id], capture_output=True, text=True)

    # print(f"? STDOUT:\n{result.stdout}")
    # print(f"? STDERR:\n{result.stderr}")

    # # 按行拆分输出（去除空行）
    # lines = [line.strip() for line in result.stdout.strip().split("\n") if line.strip()]
    #
    # # 按列分割每一行，生成二维列表
    # rows = [line.split() for line in lines]
    #

    kwargs = {}
    kwargs.update({"jobStatus": []})

    output = format_output(**kwargs)

    return output