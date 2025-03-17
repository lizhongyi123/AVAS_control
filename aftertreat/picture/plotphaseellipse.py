import matplotlib.pyplot as plt
import numpy as np
class PlotPhaseEllipse():
    def __init__(self, ):
        self.fig_size = (6.4, 4.8)
        pass

    def run(self, show_, fig=None):
        alpha = -0.6044328
        beta = 0.81006911
        gamma = (1 + alpha **2) / beta
        emit = 0.1534267

        # print(self.x, self.y)
        # print(fig)
        if not fig:
            fig, ax1 = plt.subplots(figsize=self.fig_size)
        else:
            ax1 = fig.add_subplot(111)

        x = np.linspace(-2.5, 2.5, 40)
        xp = np.linspace(-2.5, 2.5, 40)


        # ax.set_ylim([-60, 60])
        # ax.set_xlim([-40, 40])
        x, xp = np.meshgrid(x, xp)
        ax1.contour(x, xp, gamma * x ** 2 + 2 * alpha * x * xp + beta * xp ** 2,
                   [emit], colors='r')
        plt.show()


        # 添加标题和标签
        # plt.title('Bar Chart Example')

        ax1.set_xlabel(self.xlabel, fontsize=self.fontsize)
        ax1.set_ylabel(self.ylabel, fontsize=self.fontsize)

        if len(self.xlim) == 2:
            ax1.set_xlim(self.xlim[0], self.xlim[1])


        if len(self.ylim) == 2:
            ax1.set_ylim(self.ylim[0], self.ylim[1])


        if self.set_legend == 1:
            ax1.legend()


        if self.patch_list:
            for shapes in self.patch_list:
                for shape in shapes:
                    ax1.gca().add_patch(shape)

        # ax1.grid()
        if show_:
            plt.show()
            return None

        else:
            return None

if __name__ == '__main__':
    obj = PlotPhaseEllipse()
    obj.run(show_=1)

