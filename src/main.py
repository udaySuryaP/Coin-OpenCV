import cv2
import cvzone
import numpy as np
from cvzone.ColorModule import ColorFinder
import serial

ser = serial.Serial('COM4', 9600)  # Replace 'COM4' with your Arduino's port
deviceId = 'iriunv0'

capture = cv2.VideoCapture(deviceId)
capture.set(3, 640)
capture.set(4, 480)

totalMoney = 0
myColorFinder = ColorFinder(False)
hsvVals = {'hmin': 0, 'smin': 0, 'vmin': 145,
           'hmax': 63, 'smax': 91, 'vmax': 255}

minArea2 = [19000, 20001]
# minArea1 = [100, 300]
minArea5 = [1900, 20100]
minArea10 = [22000, 24000]
pixelCount1 = [13000, 14500]
pixelCount5 = [6000, 11000]


def empty(a):
    pass


cv2.namedWindow("Settings")
cv2.resizeWindow("Settings", 640, 240)
cv2.createTrackbar("Threshold1", "Settings", 0, 255, empty)
cv2.createTrackbar("Threshold2", "Settings", 200, 255, empty)


def preProcessing(img):
    imgPre = cv2.GaussianBlur(img, (5, 5), 3)
    thresh1 = cv2.getTrackbarPos("Threshold1", "Settings")
    thresh2 = cv2.getTrackbarPos("Threshold2", "Settings")
    imgPre = cv2.Canny(imgPre, thresh1, thresh2)
    kernal = np.ones((3, 3), np.uint8)
    imgPre = cv2.dilate(imgPre, kernal, iterations=1)
    imgPre = cv2.morphologyEx(imgPre, cv2.MORPH_CROSS, kernal)
    return imgPre


while True:
    success, img = capture.read()
    imgPre = preProcessing(img)
    imgContours, conFound = cvzone.findContours(img, imgPre, minArea=20)
    totalMoney = 0
    imgCount = np.zeros((480, 640, 3), np.uint8)

    if conFound:
        for count, contour in enumerate(conFound):
            peri = cv2.arcLength(contour['cnt'], True)
            approx = cv2.approxPolyDP(contour['cnt'], 0.02*peri, True)
            if len(approx) > 7:
                area = contour['area']
                x, y, w, h = contour['bbox']
                imgCrop = img[y:y+h, x:x+w]
                imgColor, mask = myColorFinder.update(imgCrop, hsvVals)
                whitePixelCount = cv2.countNonZero(mask)
                print(area, whitePixelCount)
                if minArea10[0] < area < minArea10[1]:
                    totalMoney += 10
                elif pixelCount5[0] < whitePixelCount < pixelCount5[1]:
                    totalMoney += 5
                elif minArea2[0] < area < minArea2[1]:
                    totalMoney += 2
                # elif minArea1[0] < area < minArea1[1]:
                #     totalMoney += 1
                else:
                    totalMoney += 1

    cvzone.putTextRect(
        imgCount, f'Rs.{totalMoney}', (100, 200), scale=10, offset=30, thickness=7)
    imgStacked = cvzone.stackImages([img, imgPre, imgContours], 2, 1)
    cvzone.putTextRect(imgStacked, f'Rs.{totalMoney}', (50, 50))
    cv2.imshow("Image", imgStacked)

    ser.write(str(totalMoney).encode())
    cv2.waitKey(1)
