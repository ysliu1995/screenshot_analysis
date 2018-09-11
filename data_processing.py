# %matplotlib inline
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

class Analysis:

    def get_figure(self):

        CO2_name = self.get_file_name('CO2')
        PM25_name = self.get_file_name('PM25')

        CO2_df = self.get_data('CO2',CO2_name)
        PM25_df = self.get_data('PM25',PM25_name)

        CO2 = []
        PM25 = []

        for index , num in enumerate(CO2_df.values):
            t = tuple([(index+1)*60,int(num)])
            CO2.append(t)
        for index , num in enumerate(PM25_df.values):
            t = tuple([(index+1)*60,int(num)])
            PM25.append(t)

        plt.subplot(121)
        self.plotData(plt, CO2, 'CO2', 'Time(s)', 'ppm')
        plt.subplot(122)
        self.plotData(plt, PM25, 'PM2.5', 'Time(s)', 'us/m*3')
        plt.show()

    def get_file_name(self, dir):
        all_file = os.listdir('output/{}'.format(dir))
        s = sorted([int(f.strip('.txt')) for f in all_file])
        return s

    def get_data(self, dir, name):
        total = []
        for item in name:
            fp = open('output/{}/{}.txt'.format(dir, item), "r")
            next(fp)
            next(fp)
            lines = fp.readlines()                              # 變數 lines 會儲存 filename.txt 的內容
            fp.close()
            t = [n.strip('\n').strip('.') for n in lines]       #把不是數字的去掉
            total.append(t)

        df = pd.DataFrame(total)
        return df

    def plotData(self, plt, data, title , xl, yl):
        x = [p[0] for p in data]
        y = [p[1] for p in data]
        plt.plot(x, y, '-o')
        plt.title(title)
        plt.xlabel(xl)
        plt.ylabel(yl)
