import cv2
import numpy as np
import math


class ShapeDetector:
    def __init__(self):
        pass

    def detect(self, c):
        # initialize the shape name and approximate the contour
        shape = "unidentified"
        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.04 * peri, True)
        # if the shape is a triangle, it will have 3 vertices
        if len(approx) == 3:
            shape = "triangle"

        # if the shape has 4 vertices, it is either a square or
        # a rectangle
        elif len(approx) == 4:
            # compute the bounding box of the contour and use the
            # bounding box to compute the aspect ratio
            (x, y, w, h) = cv2.boundingRect(approx)
            ar = w / float(h)

            # a square will have an aspect ratio that is approximately
            # equal to one, otherwise, the shape is a rectangle
            shape = "square" if ar >= 0.95 and ar <= 1.05 else "rectangle"

        # if the shape is a pentagon, it will have 5 vertices
        elif len(approx) == 5:
            shape = "pentagon"

        # otherwise, we assume the shape is a circle
        else:
            shape = "circle"

        # return the name of the shape
        return shape


def getInput():
    try:
        sd = ShapeDetector()

        face_cascade = cv2.CascadeClassifier('face.xml')
        video = cv2.VideoCapture(cv2.CAP_DSHOW)
        hueLower = 3
        hueUpper = 33
        mask = np.zeros((720, 1280), np.uint8)
        bg = np.zeros((1, 65), np.float64)
        fg = np.zeros((1, 65), np.float64)
        fgbg = cv2.createBackgroundSubtractorMOG2()

        while video.isOpened():
            ret, img2 = video.read()

            img = cv2.GaussianBlur(img2, (11, 11), 0)
            faces = face_cascade.detectMultiScale(img2, 1.3, 5)
            img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
            img = cv2.inRange(img, (3, 50, 50), (15, 255, 255))
            img = cv2.medianBlur(img, 11)
            img = cv2.erode(img, None, iterations=1)
            if faces != ():
                for face in faces:
                    (x, y, w, h) = face
                    img[y - 50:y + h, x:x + w] = 0

            img3 = np.zeros(img.shape)

            contours, hierarchy = cv2.findContours(img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
            if contours:
                c = max(contours, key=cv2.contourArea)
                x, y, w, h = cv2.boundingRect(c)
                img3[y:y + h, x:x + w] = cv2.medianBlur(img[y:y + h, x:x + w], 11)
                cv2.rectangle(img2, (x, y), (x + w, y + h), 255)

                hull = cv2.convexHull(c, returnPoints=False)
                defects = cv2.convexityDefects(c, hull)
                cnt = 0

                for i in range(defects.shape[0]):
                    s, e, f, d = defects[i, 0]
                    start = tuple(c[s][0])
                    end = tuple(c[e][0])
                    far = tuple(c[f][0])
                    cv2.line(img2, start, end, 255, 2)
                    # cv2.circle(img3, far, 5, [0, 0, 255], -1)
                    a = math.sqrt((end[0] - start[0]) ** 2 + (end[1] - start[1]) ** 2)
                    b = math.sqrt((far[0] - start[0]) ** 2 + (far[1] - start[1]) ** 2)
                    ci = math.sqrt((end[0] - far[0]) ** 2 + (end[1] - far[1]) ** 2)
                    angle = math.acos((b ** 2 + ci ** 2 - a ** 2) / (2 * b * ci))
                    if angle <= math.pi / 2:
                        cnt += 1
                        cv2.circle(img2, far, 8, 255, -1)

                cnt = 0 if not cnt else cnt + 1

                st = "Paper"
                if cnt >= 4:
                    st = "Paper"
                elif cnt >= 2:
                    st = "Scissor"
                else:
                    st = "Stone"

                cv2.putText(img2, st, (x, y - 50), cv2.FONT_HERSHEY_SIMPLEX, 3, 255)

            cv2.drawContours(img2, contours, -1, (255, 255, 0), 3)

            cv2.imshow('hand', img2)
            tempLst = {'Stone': 1, 'Paper': 2, 'Scissor': 3}
            if cv2.waitKey(30) & 0xFF == ord('q'):
                video.release()
                cv2.destroyAllWindows()
                return str(tempLst[st])
    except:
        pass


