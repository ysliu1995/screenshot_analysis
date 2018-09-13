import tkinter as tk
import cv2
import os
import crop, screenshot, google_drive, data_processing

pos_dict = {}

def add(root, instance):
    cp = crop.Crop()
    pos_dict[instance] = cp.get_position()
    show_list(root)

def start():
    
    for path in ['crop', 'output']:
        if not os.path.isdir(path):
            os.mkdir(path)

    print('----start screenshot -----')
    flow_1 = screenshot.Screenshot()
    for idx, item in enumerate(pos_dict):
        if not os.path.isdir('crop/{}'.format(item)):
            os.mkdir('crop/{}'.format(item))
        if not os.path.isdir('output/{}'.format(item)):
            os.mkdir('output/{}'.format(item))
        flow_1.get_crop('test.mp4', 60, item, pos_dict[item])
    print('----end----')
    
    print('----start upload and download -----')
    flow_2 = google_drive.Drive()
    for idx, item in enumerate(pos_dict):
        flow_2.upload_download(item)
    print('----end----')

    print('----start analysis -----')
    flow_3 = data_processing.Analysis()
    for idx, item in enumerate(pos_dict):
        flow_3.get_figure(item)
    print('----end----')

def show_list(root):
    for idx, item in enumerate(pos_dict):
        tk.Label(root, text='{} : {}'.format(item, pos_dict[item])).grid(row=idx+2, column=0, padx=10, pady=10)

def main():

    root = tk.Tk()
    root.title('Analysis')
    root.geometry('500x500')
    
    v = tk.StringVar()

    entry = tk.Entry(root, textvariable=v).grid(row=0, column=0, padx=10, pady=10)
    tk.Button(root, text='Add', width=15, height=2, command=lambda : add(root,v.get())).grid(row=0, column=1, padx=10, pady=10)
    tk.Button(root, text='Start', width=15, height=2, command=start).grid(row=0, column=2, padx=10, pady=10)

    root.mainloop()


if __name__ == '__main__':
    main()