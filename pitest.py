# import the necessary packages
from picamera.array import PiRGBArray
from picamera import PiCamera
import numpy as np
import time
import cv2
import datetime
import requests
import json
 

base_url="http://192.168.4.29:5000/get_pill_by_user_for_pi?user_id=1"
response = requests.get(base_url)
json_data = json.loads(response.text)
i = int(json_data["size"])
k = 1
medicinList = []
while(k<=i):
	obj = json_data[str(k)]
	timing = None
	if(obj['cycle']=="100"):
		timing = 1
	elif(obj['cycle']=="010"):
		timing = 2
	else:
		timing = 3
	value = [obj["partition_number"],timing,obj["count"],obj["pill_id"]]
	medicinList.append(value)
	k+=1

camera = PiCamera()
camera.resolution = (320, 240)
camera.framerate = 40
rawCapture = PiRGBArray(camera, size=(320, 240))
time.sleep(0.1)

lower_pointer_color= np.array([5,130,100])
upper_pointer_color = np.array([40,180,150])

lastIndexStored = np.array([0,0])
centerOfFrame = np.array([0,0])
# capture_continuous
currentTime = None
medicinTakenForPeriod = []


# mouse callback function will be required while adjusting for colours tho isko katna mat
def pick_color(event,x,y,flags,param):
    if event == cv2.EVENT_LBUTTONDOWN:
        print param[x,y]

def getQuadrant(centroid_x,centroid_y):
	x = centroid_x-centerOfFrame[0]
	y = centroid_y-centerOfFrame[1]
	if(x>=0 and y>=0):
		return 1
	if(x<0 and y>=0):
		return 2
	if(x<0 and y<0):
		return 3
	if(x>=0 and y<0):
		return 4


int haveTakePill = 0
def updateIndex(centroid_x,centroid_y):
	haveTakePill += 1
	if(haveTakePill==20):
		haveTakePill = 0
		return True
	else:
		return False

def findIfAnyInTheBlock(lastQuad):
	for medicin in medicinList:
		if(lastQuad==medicin[0]):
			return True
	return False


def openedTheBox(lastQuad):
	for medicin in medicinTakenForPeriod:
		if(medicin[0]==lastQuad)
			k = 0
			for j in medicinList:
				if(medicin==j):
					if(medicinList[k][2]==0):
						return
					medicinList[k][2] -= 1
				k += 1
			medicinTakenForPeriod.remove(medicin)

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
    	findIfAnyInTheBlock(getQuadrant(centroid_x, centroid_y))
    	if(updateIndex(centroid_x, centroid_y)):
    		q = getQuadrant(centroid_x, centroid_y)
        ctr = (centroid_x, centroid_y)
        cv2.circle(image, ctr, 4, (44,23,232))  
    cv2.imshow('frame', image)
    if cv2.waitKey(2) & 0xFF == 27:
        ctr = None
    return ctr

def getWindowCenter(image):
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
    centerOfFrame[0] = centroid_x
    centerOfFrame[1] = centroid_y

def addIfAnyPillToBeTaken():
	for medicin in medicinList:
		if(medicin[1]!=currentTime):
			next
		if(medicin[1]==currentTime):
			medicinTakenForPeriod.append(medicin)

if __name__ == '__main__':
	notHaveCenter = 1
	for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
		now = datetime.datetime.now()
		if(now.hours()>=8 and now.hours()<2 and currentTime!=1):
			currentTime = 1
			addIfAnyPillToBeTaken()
			buzzerIt(3)
		if(now.hours()>=2 and now.hours()<6 and currentTime!=2):
			currentTime = 2
			addIfAnyPillToBeTaken()
			buzzerIt(3)
		if(now.hours()>=6 and now.hours()<9 and currentTime!=3):
			currentTime = 3
			addIfAnyPillToBeTaken()
			buzzerIt(3)
		cv2.setMouseCallback('frame', pick_color, param = frame)
		image = frame.array
		if(notHaveCenter):
			getWindowCenter(image)
			notHaveCenter = None
			next
		track(image)
		key = cv2.waitKey(1) & 0xFF
		rawCapture.truncate(0)
		if key == ord("q"):
			break