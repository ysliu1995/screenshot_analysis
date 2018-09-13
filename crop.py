import cv2


class Crop:

    ref_point = []
    cropping = False
    image = cv2.imread('test.jpg')

    def get_position(self):
        clone = self.image.copy()
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
            cropping = True

        elif event == cv2.EVENT_LBUTTONUP:
            self.ref_point.append((x, y))
            cropping = False

            cv2.rectangle(self.image, self.ref_point[0], self.ref_point[1], (0, 255, 0), 2)
            cv2.imshow("image", self.image)



