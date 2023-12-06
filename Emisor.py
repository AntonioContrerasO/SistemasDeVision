import socketio
import time #Importar modulo para el manejo de tiempo
import serial #Importar modulo para comunicacion con puerto serial
import cv2
import easyocr
import numpy as np
import time

PATH_FOTOS = "./public/img/"
FINALIZAR_PROGRAMA = False;


reader = easyocr.Reader(["es"],gpu=False)
sio = socketio.Client() 


global count
count = 0

@sio.event
def connect():
    print("Conexion establecida")

@sio.event
def disconnect():
    print('disconnected from server')

@sio.on("pythonIniciar")
def Start(data):
    serialArduino.write("Wait_for_Object".encode("ascii"))
    

@sio.on("pythonFinalizar")
def End(data):
	serialArduino.close()


  
def tomarFoto(numeroDeFoto):
    cap = cv2.VideoCapture(0)

    leido, frame = cap.read()

    if leido == True:
        cv2.imwrite(f"foto{numeroDeFoto}.png", frame)
        print("Foto tomada correctamente")
    else:
        print("Error al acceder a la cámara")

    cap.release()
    return procesarImagen(cv2.imread(f"foto{numeroDeFoto}.png"),numeroDeFoto)

def procesarImagen(image,numLata):

    circle_approval = False
    label_approval = False
    color_approval = False

    color_bajo = np.array([15, 120, 50])
    color_alto = np.array([30, 255, 255])

    result = reader.readtext(image,rotation_info=[90, 180 ,270])
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) 
    gray_blurred = cv2.blur(gray, (3, 3))

    #Detectar color
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    rango_color = cv2.inRange(hsv, color_bajo, color_alto)
    area_color = cv2.countNonZero(rango_color)
    print(area_color)
    umbral_area = 10000 
    color_approval = area_color > umbral_area 

    # Modelo OCR
    result = reader.readtext(gray)
    # Modelo Detector de circulos
    detected_circles = cv2.HoughCircles(gray_blurred,  
                   cv2.HOUGH_GRADIENT, 1, 1000, param1 = 200, 
               param2 = 110, minRadius = 200, maxRadius = 300) 

    if detected_circles is not None:
    # Convert the circle parameters a, b and r to integers. 
        detected_circles = np.uint16(np.around(detected_circles))
        circle_approval = True
        for x in detected_circles[0, :]: 
            a, b, r = x[0], x[1], x[2] 
  
        # Draw the circumference of the circle. 
            cv2.circle(image, (a, b), r, (0, 255, 0), 4)

    tempCount = 0;


    for res in result:

        pt0 = [int(x) for x in res[0][0]]
        pt1 = [int(x) for x in res[0][2]]

        if res[1] == "05.11.24" or res[1] == "10.00" or res[1]== "15.11.24" or res[1]== ")5.11.24" or res[1] == "5.11.24":
            tempCount = tempCount + 1
            if tempCount == 2:
                label_approval = True


        cv2.rectangle(image,pt0,pt1,(255,0,0),3)
        cv2.putText(image,res[1],(pt0[0],pt0[1] -3), 2, 1, (255,255,255), 1)

    final_path = f"{PATH_FOTOS}lata{numLata}_T_{label_approval}_C_{circle_approval}_CC_{color_approval}.png"

    cv2.imwrite(final_path, image)
    sio.emit('CambiarImagenPagina', f"./img/lata{numLata}_T_{label_approval}_C_{circle_approval}_CC_{color_approval}.png")
    sio.emit('AprobadoCirculo',f"{circle_approval}")
    sio.emit('AprobadoEtiqueta',f"{label_approval}")
    sio.emit('AprobadoColor',f"{color_approval}")

    return True if circle_approval and color_approval and label_approval else False





#Definicion de las variables necesarias
PUERTOSERIE = "COM7"
BAUDIOS = 9600
IPSERVER = "127.0.0.1" #IP del server
PUERTOSERVER = "5000"

sio.connect('http://' + IPSERVER + ':' + PUERTOSERVER)
serialArduino = serial.Serial(PUERTOSERIE, BAUDIOS) #Creacion del objeto serial para la comunicacion con el arduino emisor
time.sleep(1) #Tiempo de retardo


latas = 0

ListBuenoMalo = []
TotalBuenos = 0
TotalMalos = 0


while True:

    if serialArduino.in_waiting > 0:
        dato = serialArduino.readline().decode().strip()

        if (dato == "INICIADO" and latas == 0):
            print("Poner lata 1")


        if dato == "Object_IR":
            serialArduino.write("Motor_ON".encode("ascii"))
            latas = latas + 1
        if dato == "Magnet_Hall_Motor_OFF":
            if latas >= 1:
                serialArduino.write("ETIQUETADO".encode("ascii"))
                while (serialArduino.in_waiting < 0):
                    pass
                newd = serialArduino.readline().decode().strip()
                if newd == "LISTO":
                    print("Etiquetado")
            if latas >= 2:
                ListBuenoMalo.append(tomarFoto(latas-1))
            if latas >= 3:

                if ListBuenoMalo[latas-3]:
                    TotalBuenos = TotalBuenos + 1

                    if TotalBuenos <= 3:
                        serialArduino.write("Bueno1".encode("ascii"))
                    else:
                        serialArduino.write("Bueno2".encode("ascii"))
                        TotalBuenos = 0

                else:
                    TotalMalos = TotalMalos + 1

                    if TotalMalos <= 3:
                        serialArduino.write("Malo1".encode("ascii"))
                    else:
                        serialArduino.write("Malo2".encode("ascii"))
                        TotalMalos = 0

                while (serialArduino.in_waiting < 0):
                    pass
                newd = serialArduino.readline().decode().strip()
                print(newd)
            serialArduino.write("Wait_for_Object".encode("ascii"))
