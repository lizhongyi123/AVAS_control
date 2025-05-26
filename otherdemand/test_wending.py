import pyautogui
import keyboard   # ⇽ 需要先：pip install keyboard
import time
import sys

pyautogui.FAILSAFE = False      # 仍然禁用左上角紧急停止

def main():
    time.sleep(2)               # 启动前缓冲 2 秒

    target_start = (24, 82)     # “启动”按钮
    target_stop  = (76, 81)     # “结束”按钮

    for i in range(10_000):
        # ── 1. 每次循环先检测是否按下 Esc ──
        if keyboard.is_pressed('esc'):
            print("检测到 Esc，安全退出脚本")
            safe_exit()

        print("循环", i, "→ 点击启动")
        pyautogui.moveTo(*target_start, duration=0.5)
        pyautogui.click()

        # ── 2. 在 sleep 里也检测 Esc，避免休眠期间无法终止 ──
        wait_or_abort(2)        # 等待 5 秒（可中断）

        print("循环", i, "→ 点击结束")
        pyautogui.moveTo(*target_stop, duration=0.5)
        pyautogui.click()

        wait_or_abort(0.1)        # 等待 1 秒（可中断）

def wait_or_abort(seconds: float):
    """按 Esc 可以随时终止的可中断 sleep。"""
    end = time.time() + seconds
    while time.time() < end:
        if keyboard.is_pressed('esc'):
            print("检测到 Esc，安全退出脚本")
            safe_exit()
        time.sleep(0.05)        # 50 ms 检查一次键盘

def safe_exit():
    """确保鼠标先移回安全位置，然后退出。"""
    pyautogui.moveTo(0, 0)      # 可选：移动到屏幕角落
    sys.exit(0)

if __name__ == "__main__":
    if 1:
        print("请在5秒内把鼠标移动到你想获取的位置...")

        time.sleep(3)

        # 获取并打印当前鼠标位置
        x, y = pyautogui.position()
        print(f"鼠标当前位置：({x}, {y})")

    # try:
    #     main()
    # except KeyboardInterrupt:
    #     # 兼容在终端里 Ctrl+C
    #     safe_exit()
