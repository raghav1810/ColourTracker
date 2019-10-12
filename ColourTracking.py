import cv2
import numpy as np


# Processing image based on upper and lower bounds passed to function
def color_isolate(hsv, lower, upper) :
    mask = cv2.inRange(hsv,lower,upper)
        res = cv2.bitwise_and(img,img, mask= mask)

        median = cv2.medianBlur(mask,15)

        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(5,5))
        opening = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
        median_2 = cv2.medianBlur(opening,15)


        return median_2


# Defines range of colour to track based on value passed by trackbar 
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


# Use trackbar to switch between tracking a red, blue or green object
cv2.namedWindow('img')
cv2.createTrackbar('RGB', 'img', 0, 2, choose_colour)

# i = 0
colour_dict = {0:"Red", 1:"Green", 2:"Blue"}

while(True):
    ret, frame = cap.read()
        img = cv2.flip(frame, 1)
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)


        # Obtain position of trackbar to pick which colour to track
        a_pos = cv2.getTrackbarPos('RGB', 'img')
        text = colour_dict[a_pos]


        # Use position of trackbar to pick colour and then isolate objects of matching colour
        lower, upper, text_colour = choose_colour(a_pos)
        fnres = color_isolate(hsv, lower, upper)


        # Extract contours from image after processing
        _,contours,_ = cv2.findContours(fnres, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        try:
            # Obtain contour of greatest size
                c = max(contours, key = cv2.contourArea)
                area = cv2.contourArea(c)
                # Use contour only if area greater than 150 to avoid noise
                if area >= 150:
                    rect = cv2.minAreaRect(c)
                                box = cv2.boxPoints(rect)
                                box = np.int0(box)
                                cv2.drawContours(img,[box],0,(0,0,255),2)

                pass
        except Exception:
            # Display message if no object found in image
                cv2.putText(img,"No contours in frame",(10,60),cv2.FONT_HERSHEY_SIMPLEX,0.9,(0,0,0),1,cv2.LINE_AA)


        cv2.putText(img,text,(10,40),cv2.FONT_HERSHEY_SIMPLEX,1.2,text_colour,2,cv2.LINE_AA)

        cv2.imshow("img", img)

        # Save image if spacebar pressed
        # Press Q to close the window
        key = cv2.waitKey(1)
        if key == 113: 
            break
        elif key == 32:
            cv2.imwrite("FINAL_colourTrack%d.png"%i,img)
                i += 1

cap.release()
cv2.destroyAllWindows()
