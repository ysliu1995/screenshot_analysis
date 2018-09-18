# %matplotlib inline
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

class Analysis:

    def get_figure(self, instance):

        instance_name = self.get_file_name(instance)

        instance_df = self.get_data(instance,instance_name)

        label = []
        for index , num in enumerate(instance_df.values):
            t = tuple([(index+1)*30,int(num)])
            label.append(t)

        self.plotData(plt, label, instance)
        instance_df[0].to_csv('output/{}/{}.csv'.format(instance, instance), index = 0)
        plt.savefig('output/{}/{}.png'.format(instance, instance))
        # plt.show()
        


    def get_file_name(self, dir):
        all_file = os.listdir('output/{}'.format(dir))
        s = sorted([int(f.strip('.txt')) for f in all_file])
        return s
    
    def check_digit(self, str):
        num = ''
        for i in str:
            if i.isdigit():
                num += i
        return num

    def get_data(self, dir, name):
        total = []
        for item in name:
            fp = open('output/{}/{}.txt'.format(dir, item), "r")
            next(fp)
            next(fp)
            raw = fp.read()                           
            fp.close()
            t = self.check_digit(raw)    
            total.append(t)

        df = pd.DataFrame(total)
        return df

    def plotData(self, plt, data, title):
        x = [p[0] for p in data]
        y = [p[1] for p in data]
        plt.plot(x, y, '-o')
        plt.title(title)