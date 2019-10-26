import cv2
import numpy as np
import serial
import time
import math


print("Start")
port="/dev/tty.HC-05-SPPDev" #This will be different for various devices and on windows it will probably be a COM port.
bluetooth=serial.Serial(port, 9600)#Start communications with the bluetooth unit
print("Connected")
bluetooth.flushInput() #This gives the bluetooth a little kick

#img = cv2.namedWindow('output', cv2.WINDOW_AUTOSIZE)
err_pitch = 0
err_yaw = 0
i=0
check = 0
yaw = 0
s_check = 0
pitch1 = 0
pitch2 = 0
yaw1 = 0
yaw2 = 0
prev_pitch = 0
prev_yaw = 0
pitch3 = 0
prev_input_data = 0
cap = cv2.VideoCapture(0)
ret, frame = cap.read()
img = cv2.flip(frame, 1)
level = input("Please select the level as 1 2 3 4 and 5 : ")
error = 0
while 1:

    if (s_check == 0) :
        bluetooth.flushInput()  # This gives the bluetooth a little kick
        i = '100'
        bluetooth.write(str.encode(i))
    ret, frame = cap.read()
    img = cv2.flip(frame, 1)
    img = cv2.resize(img, (720, 720))
    overlay = img.copy()
    # (2) draw shapes:
    cv2.circle(overlay, (320, 320), 700, (0, 0, 0), -1)
    # cv2.circle(overlay, (320, 320), 720, (255, 255, 255), -1)
    opacity = 0.5
    cv2.addWeighted(overlay, opacity, img, 1 - opacity, 0, img)
    cv2.circle(img, (360, 360), 70, (0, 125, 255), 5)
    cv2.circle(img, (360, 360), 180, (0, 25, 255), 5)
    cv2.circle(img, (360, 360), 255, (25, 0, 255), 5)
    cv2.circle(img, (360, 360), 300, (125, 0, 255), 5)
    cv2.circle(img, (360, 360), 355, (125, 25, 255), 5)
    yaw1 = int((720*yaw)/255)
    cv2.circle(img, (yaw1,360), 10, (0, 255, 255), -1)
    #img = np.zeros((720, 720, 3), np.uint8)
    #cv2.circle(img, (360, yaw1), 5, (0, 0, 255), -1)
    cv2.imshow('tp', img)
    if level == 1:
        error += (math.sqrt((yaw-360)*(yaw - 360)) - 70)
    if level == 2:
        error += (math.sqrt((yaw-360)*(yaw - 360)) - 180)
    if level == 3:
        error += (math.sqrt((yaw-360)*(yaw - 360)) - 255)
    if level == 4:
        error += (math.sqrt((yaw-360)*(yaw - 360)) - 300)
    if level == 5:
        error += (math.sqrt((yaw-360)*(yaw - 360)) - 355)

    input_data1 = bluetooth.readline()  # This reads the incoming data. In this particular example it will be the "Hello from Blue" line
    input_data1 = input_data1.decode()  # These are bytes coming in so a decode is needed
    input_data = str(input_data1)
    #input_data = int(input_data)
    #input_data = int(input_data)
    input_data = input_data.rstrip()
    if (input_data != ''):
        input_data = np.uint8(input_data)
        if(input_data == 0):
            input_data = prev_input_data
    else:
        input_data = prev_input_data
    input_data = 45
    yaw = input_data
    s_check = 0

    err_yaw = err_yaw + np.uint(yaw) - np.uint(prev_yaw)
    prev_yaw = yaw
    print(error)

    #img = cv2.imread('/Users/soofiyanatar/Desktop/blank.jpg',cv2.IMREAD_COLOR)
    #img = cv2.resize(img, (720, 720))
    #print(err_pitch)
    if cv2.waitKey(1) == ord('q'):
        break
bluetooth.close() #Otherwise the connection will remain open until a timeout which ties up the /dev/thingamabob
print("Done")
cv2.destroyAllWindows()
