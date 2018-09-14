import cv2


class Crop:

    def __init__(self,fname):
        self.ref_point = []
        self.cropping = False
        self.fname = fname
        self.image = cv2.imread('screenshot.jpg')

    def get_screenshot(self):
        video = self.fname
        vc = cv2.VideoCapture(video)

        if vc.isOpened(): 
            rval , frame = vc.read()

        cv2.imwrite('screenshot.jpg', frame)


    def get_position(self):
        cv2.namedWindow("image")
        cv2.setMouseCallback("image", self.shape_selection)

        while True:
            cv2.imshow("image", self.image)
            key = cv2.waitKey(1) & 0xFF

            if key == ord("c"):
                break

        cv2.destroyAllWindows()

        return self.ref_point


    def shape_selection(self, event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN:
            self.ref_point = [(x, y)]
            self.cropping = True

        elif event == cv2.EVENT_LBUTTONUP:
            self.ref_point.append((x, y))
            self.cropping = False

            cv2.rectangle(self.image, self.ref_point[0], self.ref_point[1], (0, 255, 0), 2)
            cv2.imshow("image", self.image)



