from utils.readfile import read_txt
import os
import matplotlib.pyplot as plt

class EaAnalysis():
    def __init__(self, project_path):
        self.project_path = project_path
        self.input_path = os.path.join(self.project_path, 'InputFile')
        self.output_path = os.path.join(self.project_path, 'OutputFile')

        self.EA_errors_par_tot_path = os.path.join( self.output_path, "EA_errors_par_tot.txt")


    def get_para(self):
        errors_par_tot = read_txt(self.EA_errors_par_tot_path)
        v = errors_par_tot.pop("step_err")


        errors_par_tot = {int(k): [float(i) for i in v] for k, v in errors_par_tot.items()}
        # print(errors_par_tot)
        # print(errors_par_tot[-1])

        v1 = []
        v2 = []
        for i in range(0, 205, 7):
            v = errors_par_tot.get(i)
            if v:
                v1.append(i)
                v2.append(v)
        v1 = [i/7 for i in v1]
        v2 = [i[4] * 1000 for i in v2]
        plt.plot(v1, v2)


        v3 = [i for i in range(len(v1))]
        v4 = [i for i in v3 if i not in v1]
        print(v1)
        print(v4)

        plt.show()


if __name__ == "__main__":
    path =r"C:\Users\anxin\Desktop\test_mulp"
    obj = EaAnalysis(path)
    obj.get_para()
