import tkinter as tk
from tkinter import filedialog, messagebox
import cv2
import os
import crop, screenshot, google_drive, data_processing

class App:

    def __init__(self):
        self.pos_dict = {}
        self.fname = ''

    def add(self, root, instance):
        cp = crop.Crop(self.fname)
        self.pos_dict[instance] = cp.get_position()
        self.show_list(root)

    def start(self):
        for path in ['crop', 'output']:
            if not os.path.isdir(path):
                os.mkdir(path)

        print('----start-----')

        flow_1 = screenshot.Screenshot()
        flow_2 = google_drive.Drive()
        flow_3 = data_processing.Analysis()

        for idx, item in enumerate(self.pos_dict):

            if not os.path.isdir('crop/{}'.format(item)):
                os.mkdir('crop/{}'.format(item))
            if not os.path.isdir('output/{}'.format(item)):
                os.mkdir('output/{}'.format(item))

            flow_1.get_crop(self.fname, 30, item, self.pos_dict[item])
            flow_2.upload_download(item)
            flow_3.get_figure(item)

        print('----end----')

    def show_list(self, root):
        for idx, item in enumerate(self.pos_dict):
            tk.Label(root, text='{} : {}'.format(item, self.pos_dict[item])).grid(row=idx+3, column=0, padx=10, pady=10)

    def get_file(self, root):
        self.fname = filedialog.askopenfilename(title=u"choose the file")
        tk.Label(root, text='path : {}'.format(self.fname), height=2).grid(row=0, column=1, columnspan=2, padx=10, pady=10)
        cp = crop.Crop(self.fname)
        cp.get_screenshot()

    def main(self):

        root = tk.Tk()
        root.title('Analysis')
        root.geometry('550x500')

        category = tk.StringVar()
        path = tk.StringVar()

        tk.Button(root, text='open file', width=15, height=2, command=lambda : self.get_file(root)).grid(row=0, column=0, padx=10, pady=10)
        entry = tk.Entry(root, textvariable=category).grid(row=2, column=0, padx=10, pady=10)
        tk.Button(root, text='Add', width=15, height=2, command=lambda : self.add(root,category.get())).grid(row=2, column=1, padx=10, pady=10)
        tk.Button(root, text='Start', width=15, height=2, command=self.start).grid(row=2, column=2, padx=10, pady=10)

        root.mainloop()


if __name__ == '__main__':
    app = App()
    app.main()
