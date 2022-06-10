import cv2
import numpy as np
from imutils import perspective, rotate
from deskew import determine_skew


def refactor_image(image: np.array, max_width: int = 1500):
    h, w, _ = image.shape
    if h > w:
        k = max_width / h
        w = int(h * k)
        image = cv2.resize(image, (w, max_width))
        return image
    else:
        k = max_width / w
        h = int(h * k)
        image = cv2.resize(image, (max_width, h))
        return image


def reorder(counter):
    myPoints = counter.reshape((4, 2))
    myPointsNew = np.zeros((4, 1, 2), dtype=np.int32)
    add = myPoints.sum(1)

    myPointsNew[0] = myPoints[np.argmin(add)]
    myPointsNew[3] = myPoints[np.argmax(add)]
    diff = np.diff(myPoints, axis=1)
    myPointsNew[1] = myPoints[np.argmin(diff)]
    myPointsNew[2] = myPoints[np.argmax(diff)]

    return myPointsNew


def get_documents_from_image(image: np.array, size_width: int = 1500,
                             k: int = 5, delete_border: int = 20) -> list[np.array]:
    # heightImg = 640
    # widthImg = 480
    # kk = int(size_width / widthImg)
    # widthImg = size_width
    # heightImg = int(heightImg * kk)
    # img = refactor_image(image, size_width)
    # # img = cv2.resize(image, (widthImg, heightImg))  # RESIZE IMAGE
    # img = img[delete_border: heightImg - delete_border, delete_border: widthImg - delete_border]
    # img = cv2.resize(img, (widthImg, heightImg))  # RESIZE IMAGE
    # imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  # CONVERT IMAGE TO GRAY SCALE
    # intensity = np.sum(imgGray) / (imgGray.shape[0] * imgGray.shape[1])
    # imgBlur = cv2.GaussianBlur(imgGray, (kk * 5, kk * 5), 1)  # ADD GAUSSIAN BLUR
    # if intensity < 200:
    #     thres = 100
    # else:
    #     thres = 90652 * np.exp(-0.033 * intensity)
    #
    # imgThreshold = cv2.Canny(imgBlur, thres / 2, thres)
    # kernel = np.ones((kk * 5, kk * 5))
    # imgDial = cv2.dilate(imgThreshold, kernel, iterations=2)  # APPLY DILATION
    # imgThreshold = cv2.erode(imgDial, kernel, iterations=1)  # APPLY EROSION
    # contours, hierarchy = cv2.findContours(imgThreshold, cv2.RETR_EXTERNAL,
    #                                        cv2.CHAIN_APPROX_SIMPLE)  # FIND ALL CONTOURS
    #
    # # FIND THE BIGGEST COUNTOUR # FIND THE BIGGEST CONTOUR
    # docs = []
    # for contour in contours:
    #     rect = (x, y), (w, h), a = cv2.minAreaRect(contour)
    #     contour = np.int0(cv2.boxPoints(rect))
    #     peri = cv2.arcLength(contour, True)
    #     contour = cv2.approxPolyDP(contour, 0.02 * peri, True)
    #     if w > widthImg / k and h > heightImg / (2 * k) and len(contour) == 4:
    #         contour = reorder(contour)
    #         points = np.array([tuple(*p) for p in contour])
    #         wrap = perspective.four_point_transform(img, points)
    #         docs.append(refactor_image(wrap))
    # return docs

    angle = determine_skew(image)
    image = rotate(image, angle)
    return [image]
