"""
    first run this code to capture image and store into image databse for training
"""


import cv2      
import numpy as np
import sqlite3
import time

faceDetect = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')                #faceDtector classifier 

                                                                                         #insert data into database  
def insertOrUpdate(Id,Name,Age):
    conn = sqlite3.connect("SQLFace.db")
    data = (Id,Name,Age)
    cmd = "SELECT * FROM People WHERE ID="+str(Id)
    cursor = conn.execute(cmd)
    isRecordExist = 0
    for row in cursor:
        isRecordExist=1
    if(isRecordExist==1):
        cmd = "UPDATE People SET Name=?,Age=? WHERE ID=?"
        conn.execute(cmd,(Name,Age,Id))
    else:
        cmd = "INSERT INTO People Values(?,?,?)"
        conn.execute(cmd,data)
    conn.commit()
    conn.close()


id = raw_input("enter id : ")
name = str(raw_input("enter name : "))
age = raw_input("enter age : ")

insertOrUpdate(id,name,age)

                                                                                        #initilize camera
cam = cv2.VideoCapture(0)

                                                                                        #read image from camera
ret,img = cam.read()

                                                                                        #wait to make yourself infront of camera 
print("wait 5 sec")
time.sleep(5)

                                                                                        #no. of samples you want to take
smapleCount = 50

imageNo=0
try:
    while(True):
        ret,img = cam.read()
        gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)                                       #convert color image into gray
        faces = faceDetect.detectMultiScale(gray,1.3,5)                                   #tuning face detection variables and o/p position,height and width  
         
        for (x,y,w,h) in faces:
            imageNo=imageNo+1
            image = gray[y:y+h,x:x+w]                                                     #crop image
            resized = cv2.resize(image,(200,150))                                         #resize image
            cv2.imwrite("database/User."+str(id)+"."+str(imageNo)+".jpg",resized)         #save image into database folder      
            cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),2)                                #draw ractangle on the face 
            cv2.waitKey(100)                                                              #dealy between each face captured       
            
        cv2.imshow("faces",img)                                                           #show image  
        cv2.waitKey(1)                                          
        if(imageNo>smapleCount):                                                          #sample count logic   
            break
        if(cv2.waitKey(1)==ord('q')):                                                     # to interrupt press button q      
            break

finally:
    cam.release()                                                                        #destroy all image window       
    cv2.destroyAllWindows()
            
