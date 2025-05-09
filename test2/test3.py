import sys
sys.path.append('/LustreData7/home/lizhongyi/yun3/AVAS_control')
from AVAS_control.utils.treat_directory import list_files_in_directory
import os
from AVAS_control.hpc.submit_job import submit_job
if __name__ == '__main__':
    path = r"/LustreData7/home/lizhongyi/yun3"
    project_path = os.path.join(path, "cafe_avas")
    all_files = list_files_in_directory(project_path)
    print(all_files)
    item = {
        "projectPath": project_path,
    }
    #submit_job(**item)

#