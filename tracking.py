from cv2 import cv

camcapture = cv.CreateCameraCapture(0)

TPL_WIDTH= 15 # template width
TPL_HEIGHT= 15 # template height
WINDOW_WIDTH = 24 # search window width
WINDOW_HEIGHT = 24 # search window height
THRESHOLD= 0.2

object_x0 = 60
object_y0 = 70
is_tracking = False


frame = cv.QueryFrame(camcapture)

gray = cv.CreateImage(cv.GetSize(frame), cv.IPL_DEPTH_8U, 1)
cv.CvtColor(frame, gray, cv.CV_RGB2GRAY)

tpl = cv.CreateImage((TPL_WIDTH,TPL_HEIGHT), cv.IPL_DEPTH_8U, 1)

# create image to store template matching result in
tm = cv.CreateImage((WINDOW_WIDTH-TPL_WIDTH+1, WINDOW_HEIGHT-TPL_HEIGHT+1),
                    cv.IPL_DEPTH_32F, 1)

def get_rect(img, rect):
    w = img.width
    h = img.height
    if rect[0] + rect[2] > w:
        rect = (w - rect[2], rect[1], rect[2], rect[3])
    elif rect[0] < 0:
        rect = (0, rect[1], rect[2] - rect[0], rect[3])
    if rect[1] + rect[3] > h:
        rect = (rect[0], h - rect[3], rect[2], rect[3])
    elif rect[1] < 0:
        rect = (rect[0], 0, rect[2], rect[3] - rect[1])
    return rect

def trackobject(img, frame):
    global object_x0, object_y0, is_tracking
    window = cv.GetSubRect(img, (object_x0, object_y0, WINDOW_WIDTH, WINDOW_HEIGHT))
    cv.MatchTemplate(window, tpl, tm, cv.CV_TM_SQDIFF_NORMED)
    minval, maxval, minloc, maxloc = cv.MinMaxLoc(tm)
    if minval <= THRESHOLD:
        rect = get_rect(img, (minloc[0] + object_x0 - TPL_WIDTH // 2,
                              minloc[1] + object_y0 - TPL_HEIGHT // 2,
                              WINDOW_WIDTH, WINDOW_HEIGHT))
        object_x0 = rect[0]
        object_y0 = rect[1]

        cv.Rectangle(frame, (object_x0, object_y0),
                     (object_x0+TPL_WIDTH, object_y0+TPL_HEIGHT),
                     (0,0,1,0),3,8,0)
    else:
        #if not found
        print "Lost object"
        is_tracking = False


def mousecallback(event, x, y, flags, param):
    global gray, is_tracking, object_x0, object_y0, tpl
    if event == cv.CV_EVENT_LBUTTONUP:
        object_x0 = x - TPL_WIDTH // 2
        object_y0 = y - TPL_HEIGHT // 2
        rect = get_rect(gray, (x - TPL_WIDTH // 2, y - TPL_HEIGHT // 2,
                               WINDOW_WIDTH, WINDOW_HEIGHT))
        object_x0 = rect[0]
        object_y0 = rect[1]
        sub = cv.GetSubRect(gray, (rect[0], rect[1], TPL_WIDTH, TPL_HEIGHT))
        cv.Copy(sub, tpl)
        print "Template selected. Start tracking"
        is_tracking = True

cv.ShowImage("video", gray)
cv.SetMouseCallback("video", mousecallback)

while True:
    frame = cv.QueryFrame(camcapture)
    if frame is None:
        break
    cv.Flip(frame, frame, cv.CV_CVTIMG_FLIP)
    cv.CvtColor(frame, gray, cv.CV_RGB2GRAY)

    if is_tracking:
        trackobject(gray, frame)

    cv.ShowImage("video", frame)
    k=cv.WaitKey(10)
    if k == 27:
        break

cv.DestroyWindow("video")
del camcapture
