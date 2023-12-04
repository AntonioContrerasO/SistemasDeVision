
import cv2
import easyocr
import numpy as np

reader = easyocr.Reader(["es"],gpu=False)


image = cv2.imread("Prueba3.png")
frameHSV = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)


result = reader.readtext(image,rotation_info=[90, 180 ,270])
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) 
gray_blurred = cv2.blur(gray, (3, 3)) 

result = reader.readtext(gray)

detected_circles = cv2.HoughCircles(gray_blurred,  
                   cv2.HOUGH_GRADIENT, 1, 100, param1 = 200, 
               param2 = 30, minRadius = 200, maxRadius = 600) 

if detected_circles is not None:
    # Convert the circle parameters a, b and r to integers. 
    detected_circles = np.uint16(np.around(detected_circles))
    print("Hubo circulos") 
  
    for x in detected_circles[0, :]: 
        a, b, r = x[0], x[1], x[2] 
  
        # Draw the circumference of the circle. 
        cv2.circle(image, (a, b), r, (0, 255, 0), 4)

for res in result:

	pt0 = [int(x) for x in res[0][0]]
	pt1 = [int(x) for x in res[0][2]]

	cv2.rectangle(image,pt0,pt1,(255,0,0),3)
	cv2.putText(image,res[1],(pt0[0],pt0[1] -3), 2, 1, (255,255,255), 1)

cv2.imwrite('./public/img/copia11.png', image)