import os
import cv2
import google_drive
import data_processing


def screenshot(video, time_shot):
    vc = cv2.VideoCapture(video) 

    fps = vc.get(cv2.CAP_PROP_FPS)      # OpenCV2 version 2 used "CV_CAP_PROP_FPS"
    frameCount = int(vc.get(cv2.CAP_PROP_FRAME_COUNT))
    duration = frameCount/fps


    if vc.isOpened(): 
        rval , frame = vc.read()
    else:
        rval = False
        
    shot = (int(fps) + 1) * time_shot
    c = 1

    while rval:   
        rval, frame = vc.read()
        if c % shot == 0:
            sec = int(c/1800)
            CO2_image = frame[191:245,181:330]
            PM25_image = frame[320:410,650:750]
            cv2.imwrite('input/CO2/{}.jpg'.format(sec),CO2_image)
            cv2.imwrite('input/PM25/{}.jpg'.format(sec),PM25_image) 
            cv2.imwrite('input/raw/{}.jpg'.format(sec),frame)
        c = c + 1
        cv2.waitKey(1)

    vc.release()

def main():
    need_dir = ['input', 'output', 'input/raw', 'input/CO2', 'input/PM25', 'output/CO2', 'output/PM25' ]
    [os.mkdir(dir) for dir in need_dir]

    video = input("Video:")
    time_shot = int(input("Time(s) :"))

    print('Start screenshot..............')
    screenshot(video, time_shot)
    print('Finish screenshot')

    print('Start upload and download..............')
    drive = google_drive.Drive()
    drive.upload_download()
    print('Finish upload and download')

    print('Start analysis..............')
    data = data_processing.Analysis()
    data.get_figure()
    print('Finish analysis')

if __name__ == '__main__':
    main()