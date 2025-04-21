
import numpy as np
#计算发射度
def cal_twiss_emitt(self, x, x1):
    average_x = np.mean(x)
    average_x1 = np.mean(x1)
    sigma_x = np.average([(i - average_x) ** 2 for i in x])   #beta
    sigma_x1 = np.average([(i - average_x1) ** 2 for i in x1])    #x1

    sigma_xx1 = np.average([(x[i] - average_x) * (x1[i] - average_x1) for i in range(len(x))])  #

    epsilon_x = math.sqrt(sigma_x * sigma_x1 - sigma_xx1 * sigma_xx1)

    beta_x = sigma_x / epsilon_x
    alpha_x = -sigma_xx1 / epsilon_x
    gamma_x = (1 + alpha_x ** 2) / beta_x

    norm_epsilon_x = self.beta * self.gamma * epsilon_x
    # 如果是z
    #norm_epsilon_x = self.beta * self.gamma**3 * epsilon_x


    return alpha_x, beta_x, gamma_x, epsilon_x, norm_epsilon_x

#计算包络

rms_x = np.sqrt(np.sum([(i - center_x) ** 2 for i in self.x_list]) / self.number)


rms_y = np.sqrt(np.sum([(i - center_y) ** 2 for i in self.y_list]) / self.number)

def cal_twiss_emitt(self, x, x1):

