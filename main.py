
#from dataClasses import ticket
from dataClasses import batch
from dataClasses import machine
from dataClasses import myUSB
import dataServices as ds
import keyboard
import time
import json
import usb.core
import usb.backend.libusb1
import os
from urllib.request import urlopen
import RPi.GPIO as GPIO
import sys
sys.path
def internet_on():
   try:
        response = urlopen('https://www.google.com/', timeout=10)
        
        return True
   except: 
        return False


myMachine=ds.getmachineInfo()
myBatch = ds.getBatchInfo(myMachine)
currentUSB = myUSB(None,None,None,None,None,None,None)
released=1


GPIO.output(ds.PowerPin,1)
#print (str((ds.get_mount_points())[0]))
while True:

    x=keyboard.read_hotkey(False)
    xx=1
    
    if(x=='0'):
        if(xx==1):
            GPIO.output(ds.OperationPin,1)
            myTicket = ds.getTicketInfo(myMachine, myBatch, myMachine.militaryPrice,'عسكرى')
            time.sleep(0.1)
            GPIO.output(ds.OperationPin,0)
            while keyboard.is_pressed('0'):
                xx=0
    elif(x=='.'):
        if (xx == 1):
            GPIO.output(ds.OperationPin,1)
            myTicket = ds.getTicketInfo(myMachine, myBatch, myMachine.civilianPrice,'مدنى')
            time.sleep(0.1)
            GPIO.output(ds.OperationPin,0)
            while keyboard.is_pressed('0'):
                xx = 0
    elif(x=='5+enter'):
        
        if (xx == 1):
           
                devices = usb.core.find(find_all=True)
                for dev in devices:
                    if dev != None:
                        try:
                            
                            
                            print(str(usb.util.get_string( dev, dev.iSerialNumber )))
                            currentUSB=ds.USBRole(dev.idVendor,dev.idProduct,usb.util.get_string(dev, dev.iSerialNumber))
                            
                            #print(dev.idProduct)
                            print(currentUSB.securityLevel)
                            if( currentUSB.securityLevel=='closing' or currentUSB.securityLevel=='admin'):
                                GPIO.output(ds.OperationPin,1)
                                GPIO.output(ds.PrinterError,0)
                                myBatch = ds.closeBatchInfo(myMachine,currentUSB)
                                #ds.printZreport(myBatch,myMachine,currentUSB)
                                myBatch = ds.getBatchInfo(myMachine)
                                time.sleep(0.5)
                                GPIO.output(ds.OperationPin,0)
                                break
                            else:
                                GPIO.output(ds.PrinterError, 1)
                                             
                        except:
                            GPIO.output(ds.PrinterError,1)
                            
                
    elif(x=='8+enter'):
        if(xx==1):
                
                devices = usb.core.find(find_all=True)
                for dev in devices:
                    
                    if dev != None:
                        try:
                            GPIO.output(ds.OperationPin,1)
                            GPIO.output(ds.PrinterError,0)
                            currentUSB=ds.USBRole(dev.idVendor,dev.idProduct,usb.util.get_string( dev, dev.iSerialNumber ))

                             #print(currentUSB.bus , currentUSB.device)
                            if( currentUSB.securityLevel=='update' or currentUSB.securityLevel=='admin'):
                                if(os.path.exists((str((ds.get_mount_points())[0]))+"/BackUp/")==False):
                                   os.mkdir((str((ds.get_mount_points())[0]))+"/BackUp/")
                                   
                                if(os.path.exists((str((ds.get_mount_points())[0]))+"/update/")==False):
                                   os.mkdir((str((ds.get_mount_points())[0]))+"/update/")
                                
                                #print("I found your usb"+(str((ds.get_mount_points())[0])))
                                #os.system("sudo cp -r /home/pi/Desktop/ticketSystemFolder/* /media/pi/NOZOM/BackUp ")
                                os.system("sudo cp -r /home/pi/Desktop/ticketSystemFolder/* "+(str((ds.get_mount_points())[0]))+"/BackUp ")
                                os.system("sudo cp -r "+(str((ds.get_mount_points())[0]))+"/update/* /home/pi/Desktop/ticketSystemFolder")
                                GPIO.output(ds.PowerPin, 0)
                                time.sleep(3)
                                GPIO.output(ds.OperationPin,0)
                                time.sleep(3)
                                GPIO.output(ds.PrinterError, 1)
                                time.sleep(3)
                                GPIO.output(ds.PowerPin, 1)
                                time.sleep(3)
                                GPIO.output(ds.PrinterError, 0)
                                time.sleep(3)

                                break
                            else:
                                GPIO.output(ds.PrinterError, 1)

                            
                        except:
                            GPIO.output(ds.PrinterError, 1)
                            
                            GPIO.output(ds.OperationPin,0)
            
    elif(x=='7+enter'):
        if(xx==1):
            
                devices = usb.core.find(find_all=True)
                for dev in devices:
                    if dev != None:
                        try:
                            GPIO.output(ds.OperationPin,1)
                            currentUSB=ds.USBRole(dev.idVendor,dev.idProduct,usb.util.get_string( dev, dev.iSerialNumber ))
                            print(currentUSB.securityLevel)
                            if( currentUSB.securityLevel=='watch' or currentUSB.securityLevel=='admin'):
                                print("watchxxxxxxx")
                                GPIO.output(ds.PrinterError, 0)
                                TimeCounter=0
                                while(not(internet_on())):
                                    TimeCounter = TimeCounter +1 
                                    GPIO.output(ds.OperationPin,0)
                                    time.sleep(1)
                                    GPIO.output(ds.OperationPin,1)
                                    time.sleep(1)
                                    if(TimeCounter == 5):
                                        GPIO.output(ds.PrinterError, 1)
                                        GPIO.output(ds.OperationPin,0)
                                        break
                                if(TimeCounter != 5):
                                    time.sleep(10)
                                    os.system("sudo hwclock -w")
                                    GPIO.output(ds.OperationPin,0)
                                
                                    
                                break
                            GPIO.output(ds.OperationPin,0)
                        except:
                            GPIO.output(ds.OperationPin,0)
            
    elif(x=='1+enter'):
        
        if (xx == 1):
           
                devices = usb.core.find(find_all=True)
                for dev in devices:
                    if dev != None:
                        try:
                            
                            
                            
                            currentUSB=ds.USBRole(dev.idVendor,dev.idProduct,usb.util.get_string(dev, dev.iSerialNumber))
                            
                            #print(dev.idProduct)
                           
                            if( currentUSB.securityLevel=='admin'):
                                GPIO.output(ds.OperationPin,1)
                                ds.printLastBatches(myMachine,currentUSB)
                                GPIO.output(ds.OperationPin,0)
                                break
                            else:
                                GPIO.output(ds.PrinterError, 1)
                                             
                        except:
                            GPIO.output(ds.PrinterError,1)
                            
               
                    
            #print Report for time here