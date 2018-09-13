import os
import cv2
import google_drive
import data_processing

class Screenshot:

    def get_crop(self, video, time_shot, instance, position):
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
                a = list(position[0])
                b = list(position[1])
                position = [a ,b]
                instance_image = frame[position[0][1]:position[1][1],position[0][0]:position[1][0]]
                cv2.imwrite('crop/{}/{}.jpg'.format(instance,sec),instance_image)
            c = c + 1
            cv2.waitKey(1)

        vc.release()