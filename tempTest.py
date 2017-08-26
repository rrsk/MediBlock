import cv2
import numpy as np

WINDOW_NAME = 'MedicBox' 
capture = cv2.VideoCapture(0)
image_hsv = None
# pixel = (20,60,80)
#center x,y 
windowCenter = np.array([340,242])
lower_pointer_color= np.array([10,110,120])
upper_pointer_color = np.array([90,190,200])

# def calculateSlope(marker):
#     return (marker[1]-windowCenter[1])/((marker[0]-windowCenter[0])*1.0)
# mouse callback function will be required while adjusting for colours tho isko katna mat
# def pick_color(event,x,y,flags,param):
#     if event == cv2.EVENT_LBUTTONDOWN:
#         print(x,y)
#         _, frame = capture.read()
#         pixel = frame[x,y]
#         print(pixel)
# def getY(lenght,slope,centroid_y):
#     if(slope==0):
#         return lenght+centroid_y
#     y = (lenght**(2))/( 1+1/(slope**(2)) )
#     y = y**(0.5)
#     if(centroid_y<windowCenter[1]):
#         y = y*-1
#     return centroid_y+y
# def getX(lenght,slope,centroid_x):
#     x = (lenght**(2))/( 1+(slope**(2)) )
#     x = x**(0.5)
#     if(centroid_x<windowCenter[0]):
#         x = x*-1
#     return centroid_x+x

# code to get center for first time of whole body
def setTheCenterOfImage(image):
    lower_pointer_color= np.array([10,110,120])
    upper_pointer_color = np.array([90,190,200])
    blur = cv2.GaussianBlur(image, (5,5),0)
    hsv = cv2.cvtColor(blur, cv2.COLOR_BGR2HSV)
    maskForPointer = cv2.inRange(hsv, lower_pointer_color, upper_pointer_color)
    bmaskForPointer = cv2.GaussianBlur(maskForPointer, (5,5),0)
    res = cv2.bitwise_and(image,image,mask = bmaskForPointer)
    moments = cv2.moments(bmaskForPointer)
    m00 = moments['m00']
    centroid_x, centroid_y = None, None
    if m00 != 0:
        centroid_x = int(moments['m10']/m00)
        centroid_y = int(moments['m01']/m00)
    windowCenter[0] = centroid_x
    windowCenter[1] = centroid_y


def track(image):
    blur = cv2.GaussianBlur(image, (5,5),0)
    hsv = cv2.cvtColor(blur, cv2.COLOR_BGR2HSV)
    maskForPointer = cv2.inRange(hsv, lower_pointer_color, upper_pointer_color)
    bmaskForPointer = cv2.GaussianBlur(maskForPointer, (5,5),0)
    res = cv2.bitwise_and(image,image,mask = bmaskForPointer)
    moments = cv2.moments(bmaskForPointer)
    m00 = moments['m00']
    centroid_x, centroid_y = None, None
    if m00 != 0:
        centroid_x = int(moments['m10']/m00)
        centroid_y = int(moments['m01']/m00)
    ctr = (-1,-1)
    if centroid_x != None and centroid_y != None:
        # slope = calculateSlope(np.array([centroid_x,centroid_y]))
        # length  = 100;
        # y = int(getY(length,slope,centroid_y))
        # x = int(getX(length,slope,centroid_x))
        # lines can be deleted
        # point = (x,y)
        ctr = (centroid_x, centroid_y)
        cv2.circle(image, ctr, 4, (44,23,232))
        # cv2.circle(image, point, 4, (44,23,232))    
    # cv2.circle(image, (340,242), 4, (0,0,0))
    cv2.imshow(WINDOW_NAME, image)
    # line that can be deleated ends
    if cv2.waitKey(2) & 0xFF == 27:
        ctr = None
    return ctr

if __name__ == '__main__':
    cv2.namedWindow(WINDOW_NAME)
    cv2.setMouseCallback(WINDOW_NAME, pick_color)
    okay, image = capture.read()
    setTheCenterOfImage(image)
    firstInput = None
    print(windowCenter[0],windowCenter[1])
    while True:
        okay, image = capture.read()
        if okay:
            if not track(image):
                break
            if cv2.waitKey(1) & 0xFF == 27:
                break
        else:
           print('Capture failed')
           break