import cv2,os
import numpy as np
from PIL import Image
import sqlite3
import socket

host = '192.168.43.160'                                                      #put your raspberrypi address here 
port = 5560                                                                  #specifie port   
s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)                         #initilize socket
s.connect((host,port))                                                       #connect to that IP and port address to your raspberrypi 

faceDetect = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
confidance = 100

cam = cv2.VideoCapture(0)
rec=cv2.createLBPHFaceRecognizer()
rec.load("ymlDatabase\\trainingData.yml")                                    #All Code Same as GUI               
                                                                                  

def getProfile(id):
    conn = sqlite3.connect('SQLFace.db')
    cmd = "SELECT * FROM People WHERE ID="+str(id)
    cursor = conn.execute(cmd)
    profile = None
    for row in cursor:
        profile=row
    conn.close()
    return profile


def faceRec():
    ret,img = cam.read()
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    faces = faceDetect.detectMultiScale(gray,1.3,5)
    for (x,y,w,h) in faces:
        cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),2)
        image = gray[y:y+h,x:x+w]
        resized = cv2.resize(image,(200,150))
        id,conf = rec.predict(resized)
        profile = getProfile(id)
        if (id == 1 or id == 2) and conf < confidance:
            return True

try:                                            
    trueCount = 0
    maxTrueCount = 5                                                                    # after how much times recogniation of face door open will be sent.
    while True:
        cammand = faceRec()                                                             # sending request to open the door 
        print("command : "+ str(cammand))
        if cammand == True:
            print("processing")
            trueCount = trueCount + 1
        if cammand == True and trueCount > maxTrueCount:
            cammand = str(cammand)
            s.send(str.encode(cammand))
            reply = s.recv(1024)
            print (reply.decode('utf-8'))
            trueCount = 0
finally:
    cam.release()
    cv2.destroyAllWindows()                                                             #destroy all            
    s.close()
