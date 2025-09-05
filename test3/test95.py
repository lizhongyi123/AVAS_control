import matplotlib.pyplot as plt
import numpy as np

# 生成10个数据点
steps = np.arange(0, 11, 1)

# 左图数据 (Loss)
loss = np.zeros(11)  # 全部为0

# 右图数据 (Average of beam energy change)
energy_change = np.array([-2, -2.5, -3, -4.5, -5, -5.8,
                          -6, -8, -5.2, -14, -16]) +2

# 绘制图像
fig, axes = plt.subplots(1, 2, figsize=(10, 4))

# 左图
axes[0].plot(steps, loss, color='blue')
axes[0].set_xlabel('step')
axes[0].set_ylabel('Loss(%)')

# 右图
axes[1].plot(steps, energy_change, color='red')
axes[1].set_xlabel('step')
axes[1].set_ylabel('Average of beam energy change (keV)')

plt.tight_layout()
plt.show()
