"""
    third to check recognizer capability to recognize face  
"""

import cv2
import numpy as np
from PIL import Image
import sqlite3


faceDetect = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

cam = cv2.VideoCapture(0)
rec=cv2.createLBPHFaceRecognizer()                                                                             #initilize LBPH function 
rec.load("ymlDatabase\\trainingData.yml")


def getProfile(id):                                                                                            #sql database data fetching
    conn = sqlite3.connect('SQLFace.db')
    cmd = "SELECT * FROM People WHERE ID="+str(id)
    cursor = conn.execute(cmd)
    profile = None
    for row in cursor:
        profile=row
    conn.close()
    return profile

font = cv2.cv.InitFont(cv2.cv.CV_FONT_HERSHEY_COMPLEX_SMALL,1,1,0,1,1)
while(True):
    ret,img = cam.read()
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    faces = faceDetect.detectMultiScale(gray,1.3,5)
    for (x,y,w,h) in faces:
        cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),2)
        image = gray[y:y+h,x:x+w]
        resized = cv2.resize(image,(200,150))
        id,conf = rec.predict(resized)                                                                          #getting ID and confidace value form LBPH function
        profile = getProfile(id)                                                                                
        if profile != None and conf < 100 :
            cv2.cv.PutText(cv2.cv.fromarray(img),str(profile[1]),(x,y+h+30),font,255)
            cv2.cv.PutText(cv2.cv.fromarray(img),str(profile[2]),(x,y+h+60),font,255)
            cv2.cv.PutText(cv2.cv.fromarray(img),str("confidance : "+str(conf)),(x,y+h+90),font,255)
        if conf > 100 :
            cv2.cv.PutText(cv2.cv.fromarray(img),str("Unknown"),(x,y+h+30),font,255)
    cv2.imshow("faces",img)
    if(cv2.waitKey(1)==ord('q')):                                                                               #press q for intrruption
        break
cam.release()
cv2.destroyAllWindows()
