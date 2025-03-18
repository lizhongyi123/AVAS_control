import matplotlib.pyplot as plt
import numpy as np
import matplotlib
matplotlib.use("TkAgg")
class PlotPhaseEllipse():
    def __init__(self, ):
        self.fig_size = (6.4, 4.8)
        pass

    # def get_x_y(self, x, y, picture_type):
    #     self.x = x
    #     self.y = y



    def run(self, show_=1, fig= None):




        alpha_x = -0.46109213
        beta_x = 0.38656878
        gamma_x = (1 + alpha_x **2) / beta_x
        emit = 0.2 * 4 ** 2

        # print(19, emit)
        # print(self.x, self.y)
        # print(fig)
        if not fig:
            fig, ax1 = plt.subplots(figsize=self.fig_size)
        else:
            ax1 = fig.add_subplot(111)

        x = np.linspace(-2, 2, 40)
        xp = np.linspace(-4.5, 4.5, 40)


        # ax.set_ylim([-60, 60])
        # ax.set_xlim([-40, 40])
        x, xp = np.meshgrid(x, xp)
        ax1.contour(x, xp, gamma_x * x ** 2 + 2 * alpha_x * x * xp + beta_x * xp ** 2,
                   [emit], colors='r')
        plt.show()


        # 添加标题和标签
        # plt.title('Bar Chart Example')

        ax1.set_xlabel(self.xlabel, fontsize=self.fontsize)
        # ax1.set_ylabel(self.ylabel, fontsize=self.fontsize)

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

