import cv2
import numpy as np

def color_isolate(hsv, lower, upper) :
	mask = cv2.inRange(hsv,lower,upper)
	res = cv2.bitwise_and(img,img, mask= mask)

	median = cv2.medianBlur(mask,15)
	# cv2.imshow('Median Blur',mask)

	kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(5,5))
	opening = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
	median_2 = cv2.medianBlur(opening,15)


	return median_2

def choose_colour(x):
	if x == 0:
		lower = np.array([0,80,40])
		upper = np.array([15,255,255])
		text_colour=(0,0,255)
	elif x == 1:
		lower = np.array([35,80,40])
		upper = np.array([85,255,255])
		text_colour=(0,255,0)
	elif x == 2:
		lower = np.array([95,80,40])
		upper = np.array([130,255,255])
		text_colour=(255,0,0)
	return lower, upper, text_colour


cap = cv2.VideoCapture(0)

cv2.namedWindow('img')
cv2.createTrackbar('RGB', 'img', 0, 2, choose_colour)

i = 0

colour_dict = {0:"Red", 1:"Green", 2:"Blue"}

while(True):
	ret, frame = cap.read()
	img = cv2.flip(frame, 1)
	hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)


	a_pos = cv2.getTrackbarPos('RGB', 'img')
	text = colour_dict[a_pos]


	lower, upper, text_colour = choose_colour(a_pos)
	fnres = color_isolate(hsv, lower, upper)


	_,contours,_ = cv2.findContours(fnres, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
	try:
		c = max(contours, key = cv2.contourArea)
		# cv2.drawContours(img, c, -1, (50,255,50), 5)
		area = cv2.contourArea(c)
		if area >= 150:
				rect = cv2.minAreaRect(c)
				box = cv2.boxPoints(rect)
				box = np.int0(box)
				cv2.drawContours(img,[box],0,(0,0,255),2)
		
		pass
	except Exception:
		cv2.putText(img,"No contours in frame",(10,60),cv2.FONT_HERSHEY_SIMPLEX,0.9,(0,0,0),1,cv2.LINE_AA)
	

	cv2.putText(img,text,(10,40),cv2.FONT_HERSHEY_SIMPLEX,1.2,text_colour,2,cv2.LINE_AA)

	cv2.imshow("img", img)

	key = cv2.waitKey(1)
	if key == 113:
		break
	elif key == 32:
		cv2.imwrite("colourTrack%d.png"%i,img)
		i += 1
cap.release()
cv2.destroyAllWindows()
