"""
    second run this code to make yml training database.  
"""

import cv2
import os
import numpy as np
from PIL import Image                                                       

recognizer = cv2.createLBPHFaceRecognizer()                                                     #initialize local binary pattern histograms Face recognizer
filepath = 'database'

def getImagesWithID(path):
    imagePaths=[os.path.join(path,f) for f in os.listdir(path)]                                 #get image path 
    faces = []
    IDs = []
    for imagePath in imagePaths:
        faceImg = Image.open(imagePath).convert('L')
        faceNp  = np.array(faceImg,'uint8')
        ID = int(os.path.split(imagePath)[-1].split('.')[1])                                    #get ID of image
        faces.append(faceNp)
        IDs.append(ID)
        cv2.imshow("training",faceNp)
        cv2.waitKey(10)
    return np.array(IDs),faces        
        
Idss,facess = getImagesWithID(filepath)
print ("data found")
recognizer.train(facess,Idss)                                                                   #train recognizer with image and their ID's
print("training is going on")
recognizer.save('ymlDatabase/trainingData.yml')                                                 #save yml database
print("saving database")
cv2.destroyAllWindows()                                                                         #destroy all variables
