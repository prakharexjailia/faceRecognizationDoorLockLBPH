import socket
import RPi.GPIO as gpio
import time

host = ''
port = 5560                                                                             #this specified port should be same as PC
BUFFER_SIZE = 1024                           
pin = 18                                                                                #pin at which door's lock will be connected  
gpio.setmode(gpio.BCM)
gpio.setup(pin, gpio.OUT)

storedValue = "hello I am server"

def setupServer():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print("socket created")
    try:
        s.bind((host,port))
    except socket.error as msg:
        print(msg)
    print("socket bind complete")
    return s
def setupConnection():
    s.listen(1)                                                                             #allow one connection
    conn,address = s.accept()
    print("Connected to : " + str(address))
    return conn

def door():                                                                                 #door function can be changed from here as your wish
        gpio.output(pin, gpio.LOW)       
        print("door is now Opening")
        gpio.output(pin, gpio.HIGH)
        print("door will be opened for 10 sec")
        time.sleep(10)
        gpio.output(pin, gpio.LOW)
        print("door has been closed")                


def dataTransfer(conn):
    #loop send receive  data
    while True:
        #receive the data
        data = conn.recv(1024)                                                               #reveive the data
        data = data.decode('utf-8')
                                                                                             #split data such that you separate the cammand from rest of data 
        dataMessage = data.split(' ',1)
        cammand = dataMessage[0]
        if cammand == 'True':
            print("door open request")
            reply = door();            
        elif cammand == 'EXIT':
            print("cilent left")
            break
        elif cammand == 'KILL':
            print ("our server sutting down.")
            s.close()
            break
        else:
            reply = 'Unknown Cammand'

        conn.sendall(str.encode(str(reply)))
        print("data has been sent")
    conn.colse()          


s = setupServer()

while True:
    try:
        conn = setupConnection()
        dataTransfer(conn)
    except socket.error as msg:
        print(msg)
        break
s.close()
    
