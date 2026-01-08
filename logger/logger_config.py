# logger_config.py
# import logging
#
# def setup_logger(level=logging.INFO):
#     logging.basicConfig(
#         level=level,
#         format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
#         datefmt="%Y-%m-%d %H:%M:%S"
#     )
#
# DEBUG    ❌（被过滤）
# INFO     ✅
# WARNING  ✅
# ERROR    ✅
# CRITICAL ✅

import logging
import os

def setup_logger(
    level=logging.INFO,
    log_file="app.log"
):
    # 1️⃣ 获取 root logger
    root = logging.getLogger()
    root.setLevel(level)

    # 2️⃣ 防止重复添加 handler（非常重要）
    if root.handlers:
        return

    # 3️⃣ 日志格式
    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    # 4️⃣ 终端 handler（INFO 及以上）
    console_handler = logging.StreamHandler()
    console_handler.setLevel(level)
    console_handler.setFormatter(formatter)

    # 5️⃣ 文件 handler（DEBUG 全量）
    file_handler = logging.FileHandler(
        log_file,
        mode="a",
        encoding="utf-8"
    )
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)

    # 6️⃣ 加到 root logger
    root.addHandler(console_handler)
    root.addHandler(file_handler)


# import logging
# from logger_config import setup_logger
#
# setup_logger(level=logging.INFO, log_file="run.log")
#
# logger = logging.getLogger(__name__)
#
# logger.info("Program started")