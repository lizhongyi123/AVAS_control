import subprocess
import uuid
import os
from utils.tool import format_output
def stop_job(**item):
    job_id = item['jobId']

    result = subprocess.run(["scancel", job_id], capture_output=True, text=True)


    kwargs = {}
    kwargs.update({"jobStatus": []})

    output = format_output(**kwargs)

    return output