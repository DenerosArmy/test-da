import cv2
from cv2 import cv

window_name = "Simple Edge Detector"

camcapture = cv.CaptureFromCAM(0)

THRESHOLD = 30

def edges(img):
    gray = cv.CreateImage(cv.GetSize(img), 8, 1)
    cv.CvtColor(img, gray, cv.CV_RGB2GRAY)
    #cv.EqualizeHist(gray, gray)
    canny = cv.CreateImage(cv.GetSize(img), 8, 1)
    cv.Canny(gray, canny, THRESHOLD, THRESHOLD*3)
    combined = cv.CreateImage(cv.GetSize(img), 8, 1)
    cv.Add(gray, canny, combined)
    return combined

while True:
    img = cv.QueryFrame(camcapture)
    edgeimg = edges(img)
    cv.ShowImage(window_name, edgeimg)
    k = cv.WaitKey(10)
    if k == 27: break

cv.DestroyWindow(window_name)
del camcapture
