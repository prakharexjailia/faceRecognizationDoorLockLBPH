Project Description ===
			Face recognization based door lock .
				door will be controlled by raspberrypi's GPIO pins specificaly for this project is pin 18.
				
1. capture face and update ID,name,age in sqlite database by running PC -> creat_database.py.
2. train and creat yml database by running PC -> trainer.py.
3. to test this recognizer run PC -> facerecogGUI.py .

4. copy PI -> piServer.py to raspberrypi. 
5. run piServer.py on raspberrypi.
6. open PC -> facerecog_clientCammandPC.py and replace IP form 192.168.43.160 to your ip at which PI is connected. 
7. run PC -> facerecog_clientCammandPC.py on PC.


note - 1.install all lib opneCV, PIL, numpy, sqlite ect. All scripts are written for python2.
       2.process of running LBPH scripts and Eigen scripts are same. 	
       3.for more information refer documantation but LBPH works better.  	

        