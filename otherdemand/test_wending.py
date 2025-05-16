import pyautogui
import time

if 0:
    print("请在5秒内把鼠标移动到你想获取的位置...")

    time.sleep(3)

    # 获取并打印当前鼠标位置
    x, y = pyautogui.position()
    print(f"鼠标当前位置：({x}, {y})")

time.sleep(2)

#(1350, 82) (1403, 81)
if 1:
    for i in range(10000):
        print(16, i)
        # 设置要点击的目标坐标（屏幕上的位置）
        target_x = 1350
        target_y = 82

        # 将鼠标移动到指定位置（可以加上持续时间实现平滑移动）
        pyautogui.moveTo(target_x, target_y, duration=0.5)

        # 单击鼠标左键
        pyautogui.click()

        print("鼠标已点击启动。")

        time.sleep(5)
        # 设置要点击的目标坐标（屏幕上的位置）
        target_x = 1403
        target_y = 81

        # 将鼠标移动到指定位置（可以加上持续时间实现平滑移动）
        pyautogui.moveTo(target_x, target_y, duration=0.5)

        # 单击鼠标左键
        pyautogui.click()

        print("鼠标已点击结束。")
        time.sleep(1)