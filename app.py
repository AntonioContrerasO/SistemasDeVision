import cv2
import numpy as np


"""
    En este caso, 0 quiere decir que queremos acceder
    a la cámara 0. Si hay más cámaras, puedes ir probando
    con 1, 2, 3...
"""
cap = cv2.VideoCapture(1)

leido, frame = cap.read()

if leido == True:
    cv2.imwrite("foto.png", frame)
    print("Foto tomada correctamente")
else:
    print("Error al acceder a la cámara")

"""
    Finalmente liberamos o soltamos la cámara
"""
cap.release()


















# def detectar_color(image_path):
#     color_bajo = np.array([20, 100, 240])
#     color_alto = np.array([35, 255, 255])

#     # Convertir la imagen de BGR a HSV
#     hsv = cv2.cvtColor(imagen, cv2.COLOR_BGR2HSV)

#     # Definir un rango de colores en HSV
#     rango_color = cv2.inRange(hsv, color_bajo, color_alto)

#     # Calcular el área total de píxeles que están dentro del rango de color
#     area_color = cv2.countNonZero(rango_color)

#     # Determinar si el área de color es mayor que un umbral arbitrario
#     umbral_area = 50  # Puedes ajustar este umbral según tus necesidades
#     color_presente = area_color > umbral_area

#     return color_presente


# # Llamar a la función para detectar el color
# color_presente = detectar_color(ruta_imagen, color_bajo, color_alto)










# import cv2
# import easyocr
# import numpy as np

# reader = easyocr.Reader(["es"],gpu=False)


# image = cv2.imread("Prueba3.png")
# frameHSV = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)


# result = reader.readtext(image,rotation_info=[90, 180 ,270])
# gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) 
# gray_blurred = cv2.blur(gray, (3, 3)) 

# result = reader.readtext(gray)

# detected_circles = cv2.HoughCircles(gray_blurred,  
#                    cv2.HOUGH_GRADIENT, 1, 1000, param1 = 50, 
#                param2 = 30, minRadius = 200, maxRadius = 300) 

# if detected_circles is not None: 
#     # Convert the circle parameters a, b and r to integers. 
#     detected_circles = np.uint16(np.around(detected_circles))
  
#     for x in detected_circles[0, :]: 
#         a, b, r = x[0], x[1], x[2] 
  
#         # Draw the circumference of the circle. 
#         cv2.circle(image, (a, b), r, (0, 255, 0), 4)

# for res in result:

# 	pt0 = [int(x) for x in res[0][0]]
# 	pt1 = [int(x) for x in res[0][2]]

# 	cv2.rectangle(image,pt0,pt1,(255,0,0),3)
# 	cv2.putText(image,res[1],(pt0[0],pt0[1] -3), 2, 1, (255,255,255), 1)

# cv2.imwrite('./public/img/copia11.png', image)