import json
import sys
import os
import datetime
import arabic_reshaper
import usb
from escpos import printer
from bidi.algorithm import get_display
from wand.image import Image as wImage
from wand.drawing import Drawing as wDrawing
from wand.color import Color as wColor

from dataClasses import ticket
from dataClasses import batch
from dataClasses import machine
from dataClasses import myUSB
import RPi.GPIO as GPIO

from glob import glob
from subprocess import check_output, CalledProcessError
def get_usb_devices():
    sdb_devices = map(os.path.realpath, glob('/sys/block/sd*'))
    usb_devices = (dev for dev in sdb_devices
        if 'usb' in dev.split('/')[5])
    return dict((os.path.basename(dev), dev) for dev in usb_devices)
    #return dict((dev) for dev in usb_devices)


def get_mount_points(devices=None):
    devices = devices or get_usb_devices()  # if devices are None: get_usb_devices
    #print (devices)
    output = check_output(['mount']).splitlines()
    output = [tmp.decode('UTF-8') for tmp in output]

    def is_usb(path):
        return any(dev in path for dev in devices)
    usb_info = (line for line in output if is_usb(line.split()[0]))
    #return [(info.split()[0], info.split()[2]) for info in usb_info]
    return [(info.split()[2]) for info in usb_info]


GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
PrinterError = 13
PowerPin= 19
OperationPin=26
GPIO.setup(PrinterError,GPIO.OUT)
GPIO.setup(PowerPin,GPIO.OUT)
GPIO.setup(OperationPin,GPIO.OUT)
GPIO.output(PowerPin,0)
GPIO.output(OperationPin,0)
GPIO.output(PrinterError,0)
originalPath=os.path.dirname(os.path.realpath(__file__))+'/'
def getUSBInfo():
    with open(originalPath+'USB.json','r') as json_file:
        data = json.load(json_file)
        USB = data['USB']
        USB_arr = []
        for i in USB:
            myUS = myUSB(i["vendorId"],i["productId"],i["securityLevel"],i["userId"],None,None,i["iSerialNumber"])
            USB_arr.append(myUS)
    return USB_arr

USBs = getUSBInfo()
#currentUSB = myUSB(None,None,None,None)
def write_json(data, filename):
    with open(originalPath+filename, 'w') as f:
        json.dump(data, f, indent=2)
    return
def USBRole(vendorId,productId,iSerialNumber):
    
    for i in USBs:
        if(i.vendorId==str(vendorId) and i.productId==str(productId) and i.iSerialNumber==str(iSerialNumber)):
            
            
            return i
    return None    
             

def getmachineInfo():

    "this method get the machineId and destination"
    with open(originalPath+'Machine/machine.json', 'r') as f:

        array = json.load(f)

        myMachine = machine(array['machine'][0]['machineId'],array['machine'][0]['destination'],array['machine'][0]['militaryPrice'],array['machine'][0]['civilianPrice'])
    return myMachine

def getBatchInfo(machine):
    myBatch=batch(None,None,None,None,None,None,None,None)


    with open(originalPath+'Batch/batch.json','r') as json_file:
        data = json.load(json_file)
        temp = data['batch']
        arrayLength = len(data['batch'])
        if(arrayLength==0):
            y = {
                  'batchNumber': 1,
                  'machineId': machine.machineId,
                  'startDate': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                  'endDate': None,
                  'numberOfTickets': 0,
                  'numberOfCivilTickets': 0,
                  'numberOfMilTickets': 0,
                  'closingTotal': 0
                }
            temp.append(y)
            write_json(data,'Batch/batch.json')
            myBatch.batchNumber=1
            myBatch.machineId = machine.machineId
            myBatch.startDate = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            myBatch.endDate = None
            myBatch.numberOfTickets = 0
            myBatch.closingTotal = 0
        else:
            if(data['batch'][arrayLength-1]['endDate']==None):
                myBatch.batchNumber = data['batch'][arrayLength-1]['batchNumber']
                myBatch.machineId = machine.machineId
                myBatch.startDate = data['batch'][arrayLength-1]['startDate']
                myBatch.endDate = None
                myBatch.numberOfTickets = 0
                myBatch.closingTotal = 0
            else:
                y = {
                    'batchNumber': data['batch'][arrayLength - 1]['batchNumber']+1,
                    'machineId': machine.machineId,
                    'startDate': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    'endDate': None,
                    'numberOfTickets': 0,
                    'numberOfCivilTickets': 0,
                    'numberOfMilTickets': 0,
                    'closingTotal': 0
                }
                temp.append(y)
                write_json(data,'Batch/batch.json')
                myBatch.batchNumber = data['batch'][arrayLength - 1]['batchNumber']+1
                myBatch.machineId = machine.machineId
                myBatch.startDate = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                myBatch.endDate = None
                myBatch.numberOfTickets = 0
                myBatch.closingTotal = 0

    return myBatch
def closeBatchInfo(machine,myUSB):
    myBatch=batch(None,None,None,None,None,None,None,None)


    with open(originalPath+'Batch/batch.json','r') as json_file:
        data = json.load(json_file)
        temp = data['batch']
        arrayLength = len(data['batch'])
        if(arrayLength==0):
            y = {
                  'batchNumber': 1,
                  'machineId': machine.machineId,
                  'startDate': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                  'endDate': None,
                  'numberOfTickets': 0,
                  'numberOfCivilTickets': 0,
                  'numberOfMilTickets': 0,
                  'closingTotal': 0
                }
            temp.append(y)
            write_json(data,'Batch/batch.json')

        else:
            if(data['batch'][arrayLength-1]['endDate']==None ):
                if(os.path.exists(originalPath+'Batch/'+str(data['batch'][arrayLength-1]['batchNumber'])+'.json')):
                    data['batch'][arrayLength-1]['endDate'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    myBatch.batchNumber = data['batch'][arrayLength-1]['batchNumber']
                    myBatch.machineId = machine.machineId
                    myBatch.startDate = data['batch'][arrayLength-1]['startDate']
                    myBatch.endDate = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    

                    with open(originalPath+'Batch/' +str(myBatch.batchNumber) +'.json', 'r') as json_file_batch:
                        batchData = json.load(json_file_batch)
                        tempTickets = batchData['ticket']
                        arrayLengthTickets = len(batchData['ticket'])
                        TotalPrice = 0
                        numberOfCivilTickets=0
                        numberOfMilTickets=0
                        for i in tempTickets:
                            TotalPrice += i["price"]
                            if(i['type']=='مدنى'):
                                numberOfCivilTickets=numberOfCivilTickets+1
                            else:
                                numberOfMilTickets=numberOfMilTickets+1
                                    
                                
                            
                    json_file_batch.close()
                    myBatch.numberOfTickets = arrayLengthTickets
                    myBatch.numberOfCivilTickets=numberOfCivilTickets
                    myBatch.numberOfMilTickets=numberOfMilTickets
                    myBatch.closingTotal = TotalPrice
                    data['batch'][arrayLength-1]['numberOfTickets'] = arrayLengthTickets
                    data['batch'][arrayLength-1]['numberOfCivilTickets'] = numberOfCivilTickets
                    data['batch'][arrayLength-1]['numberOfMilTickets'] = numberOfMilTickets
                    data['batch'][arrayLength-1]['closingTotal'] = TotalPrice
                    
                    y = {
                        'batchNumber': data['batch'][arrayLength - 1]['batchNumber'] + 1,
                        'machineId': machine.machineId,
                        'startDate': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        'endDate': None,
                        'numberOfTickets': 0,
                        'numberOfCivilTickets': 0,
                        'numberOfMilTickets': 0,
                        'closingTotal': 0
                    }
                    temp.append(y)
                    try:
                        printZreport(myBatch,machine,myUSB)
                        write_json(data, 'Batch/batch.json')
                    except:
                        GPIO.output(ds.PrinterError, 1)
                    
            else:
                y = {
                    'batchNumber': data['batch'][arrayLength - 1]['batchNumber']+1,
                    'machineId': machine.machineId,
                    'startDate': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    'endDate': None,
                    'numberOfTickets': 0,
                    'numberOfCivilTickets': 0,
                    'numberOfMilTickets': 0,
                    'closingTotal': 0
                }
                temp.append(y)
                write_json(data,'Batch/batch.json')


    return myBatch
def printZreport(batch,machine,myUSB):
    if(batch.batchNumber != None):
        batchNum = batch.batchNumber
        startDate = batch.startDate
        closingDate  = batch.endDate
        numOfTickets = batch.numberOfTickets
        numberOfCivilTickets=batch.numberOfCivilTickets
        numberOfMilTickets=batch.numberOfMilTickets
        closingTotal = batch.closingTotal

        fontPath = originalPath + "CourierNewPS-BoldMT.ttf"
        tmpImage = originalPath + 'my-text.png'
        printFile = "/dev/usb/lp0"
        printWidth = 550

        im = wImage(filename=originalPath + 'ZBack.png')
        draw = wDrawing()
        draw.text_alignment = 'right'
        draw.text_antialias = False
        draw.text_encoding = 'utf-8'
        draw.text_kerning = -1
        draw.font = fontPath
        tn = (batch.machineId) +'_'+ '%04d' % (batch.batchNumber)
        draw.font_size = 30
        draw.text_alignment = 'center'
        draw.text((int)(printWidth / 2), 30, get_display(arabic_reshaper.reshape(tn)))

        draw.font_size = 35
        draw.text_alignment = 'center'
        draw.text((int)(printWidth / 2), 60, get_display(arabic_reshaper.reshape('Company Name')))
        tn = u"الاتجاه  " + machine.destination
        draw.font_size = 28
        draw.text_alignment = 'center'
        draw.text((int)(printWidth / 2), 90, get_display(arabic_reshaper.reshape(tn)))

        tn = u"تاريخ الفتح : " + batch.startDate
        draw.font_size = 28
        draw.text_alignment = 'center'
        draw.text((int)(printWidth / 2), 120, get_display(arabic_reshaper.reshape(tn)))
        tn = u"تاريخ الإغلاق : " + batch.endDate
        draw.font_size = 28
        draw.text_alignment = 'center'
        draw.text((int)(printWidth / 2), 150, get_display(arabic_reshaper.reshape(tn)))

        tn = u"عدد التذاكر : " + str(batch.numberOfTickets)+' عسكرى:'+str(batch.numberOfMilTickets)+' مدنى:'+str(batch.numberOfCivilTickets)
        draw.font_size = 28
        draw.text_alignment = 'center'
        draw.text((int)(printWidth / 2), 180, get_display(arabic_reshaper.reshape(tn)))
        tn = u"الإيراد " +'%.2f'%(batch.closingTotal)
        draw.font_size = 28
        draw.text_alignment = 'center'
        draw.text((int)(printWidth / 2), 210, get_display(arabic_reshaper.reshape(tn)))
        
        tn = u"ر.ت المستخدم " +str(myUSB.userId)
        draw.font_size = 28
        draw.text_alignment = 'center'
        draw.text((int)(printWidth / 2), 240, get_display(arabic_reshaper.reshape(tn)))
        draw(im)
        im.save(filename=tmpImage)

        # Print an image with your printer library

        printerx = printer.File(printFile)
        printerx.set(align="center")
        printerx.image(tmpImage)
        printerx.cut()

def printTicketInfo(ticket):
    tnp=u'مسلسل:'
    tn=ticket.machineId+'_'+'%04d'%(ticket.batchNumber)+'%04d'%(ticket.ticketNumber)
    print(tnp+tn)
    dtp=u'التاريخ:'
    dt=ticket.date
    print(dtp+dt)
    destp='الإتجاه:'
    dest=ticket.destination
    print(destp+dest)
    pricep='السعر '
    #price=str(ticket.price)
    price='%.2f'%(ticket.price)
    print(pricep+price)
    # Some variables
    #fontPath = "/usr/share/fonts/opentype/fonts-hosny-thabit/Thabit.ttf"
    fontPath=originalPath+"CourierNewPS-BoldMT.ttf"
    textUtf8 = tnp+tn
    tmpImage = originalPath+'my-text.png'
    printFile = "/dev/usb/lp0"
    printWidth = 550

# Get the characters in order
    textReshaped = arabic_reshaper.reshape(textUtf8)
    textDisplay = get_display(textReshaped)

    
    #im = wImage(width=printWidth, height=130, background=wColor('#ffffff'))
    im= wImage(filename=originalPath+'back.png')
    draw = wDrawing()
    draw.text_alignment = 'right'
    draw.text_antialias = False
    draw.text_encoding = 'utf-8'
    draw.text_kerning = -2
    draw.font = fontPath
   
    draw.font_size = 35
    draw.text_alignment = 'center'
    draw.text((int)(printWidth/2),30 , get_display(arabic_reshaper.reshape('Company Name')))
    draw.text((int)(printWidth/2),30 , get_display(arabic_reshaper.reshape('______________________')))
   
    draw.font_size = 30
    draw.text_alignment = 'right'
    draw.text(550,65 , get_display(arabic_reshaper.reshape(tnp)))
    
    draw.font_size = 30
    draw.text_alignment = 'right'
    draw.text(350,65 , get_display(arabic_reshaper.reshape(tn)))
    
    draw.font_size = 28
    draw.text_alignment = 'right'
    draw.text(550,90 , get_display(arabic_reshaper.reshape('الخط:')))
    
    draw.font_size = 28
    draw.text_alignment = 'right'
    draw.text(350,90 , get_display(arabic_reshaper.reshape(dest)))
    
    draw.font_size = 28
    draw.text_alignment = 'right'
    draw.text(550,120 , get_display(arabic_reshaper.reshape(dtp)))
    
    draw.font_size = 28
    draw.text_alignment = 'right'
    draw.text(350,120 , get_display(arabic_reshaper.reshape(dt)))
    
    draw.font_size = 30
    draw.text_alignment = 'right'
    draw.text(550,150 , get_display(arabic_reshaper.reshape('سعر التذكرة:')))
    
    draw.font_size = 30
    draw.text_alignment = 'right'
    draw.text(350,150 , get_display(arabic_reshaper.reshape(price+'ج.م'+'  '+ticket.type)))
    
    draw(im)
    im.save(filename=tmpImage)

    # Print an image with your printer library
    
    printerx = printer.File(printFile)
    printerx.set(align="center")
    
    printerx.image(tmpImage)
    printerx.cut("PART",b"\n\n\n\n")
    return
def getTicketInfo(machine,batch,price,type):
    myTicket=ticket(None,None,None,None,None,None,None)
    if(os.path.exists(originalPath+'Batch/'+str(batch.batchNumber)+'.json')):
        with open(originalPath+'Batch/'+str(batch.batchNumber)+'.json', 'r') as json_file:
            data = json.load(json_file)
            temp = data['ticket']
            arrayLength = len(data['ticket'])
            y = {
                'ticketNumber': data['ticket'][arrayLength - 1]['ticketNumber'] + 1,
                'batchNumber': batch.batchNumber,
                'destination': machine.destination,
                'date': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                'price': price,
                'machineId': machine.machineId,
                'type': type

            }
            temp.append(y)
            try:
                
                
                
                myTicket = ticket(data['ticket'][arrayLength - 1]['ticketNumber'] + 1, batch.batchNumber, machine.destination,
                              datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), price, machine.machineId,type)
                printTicketInfo(myTicket)
                write_json(data,'Batch/'+str(batch.batchNumber)+'.json')
                GPIO.output(PrinterError,0)
            except:
                GPIO.output(PrinterError,1)

    else:
        data={}
        data['ticket']=[]
        data['ticket'].append({
            'ticketNumber':1,
           'batchNumber':batch.batchNumber,
            'destination':machine.destination,
            'date':datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'price':price,
            'machineId':machine.machineId,
            'type': type

        })
        myTicket = ticket(1, batch.batchNumber,machine.destination,datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),price,machine.machineId,type )
        try:
            
            printTicketInfo(myTicket)
            write_json(data,'Batch/'+str(batch.batchNumber)+'.json')
            GPIO.output(PrinterError,0)
            
        except:
            GPIO.output(PrinterError,1)
        #with open(str(batch.batchNumber)+'.json','w') as outfile:
            #json.dump(data,outfile,indent=2)
    
    return myTicket




def printZreportDuplicate(batch,machine,myUSB):
    if(batch.batchNumber != None):
        batchNum = batch.batchNumber
        startDate = batch.startDate
        closingDate  = batch.endDate
        numOfTickets = batch.numberOfTickets
        numberOfCivilTickets=batch.numberOfCivilTickets
        numberOfMilTickets=batch.numberOfMilTickets
        closingTotal = batch.closingTotal

        fontPath = originalPath + "CourierNewPS-BoldMT.ttf"
        tmpImage = originalPath + 'my-text.png'
        printFile = "/dev/usb/lp0"
        printWidth = 550

        im = wImage(filename=originalPath + 'ZBack.png')
        draw = wDrawing()
        draw.text_alignment = 'right'
        draw.text_antialias = False
        draw.text_encoding = 'utf-8'
        draw.text_kerning = -1
        draw.font = fontPath
        tn = (batch.machineId) +'_'+ '%04d' % (batch.batchNumber) + '(م)'
        draw.font_size = 30
        draw.text_alignment = 'center'
        draw.text((int)(printWidth / 2), 30, get_display(arabic_reshaper.reshape("--------")))

        draw.font_size = 35
        draw.text_alignment = 'center'
        draw.text((int)(printWidth / 2), 60, get_display(arabic_reshaper.reshape(tn)))
        tn = u"الاتجاه  " + machine.destination
        draw.font_size = 28
        draw.text_alignment = 'center'
        draw.text((int)(printWidth / 2), 90, get_display(arabic_reshaper.reshape(tn)))

        tn = u"تاريخ الفتح : " + batch.startDate
        draw.font_size = 28
        draw.text_alignment = 'center'
        draw.text((int)(printWidth / 2), 120, get_display(arabic_reshaper.reshape(tn)))
        tn = u"تاريخ الإغلاق : " + batch.endDate
        draw.font_size = 28
        draw.text_alignment = 'center'
        draw.text((int)(printWidth / 2), 150, get_display(arabic_reshaper.reshape(tn)))

        tn = u"عدد التذاكر : " + str(batch.numberOfTickets)+' عسكرى:'+str(batch.numberOfMilTickets)+' مدنى:'+str(batch.numberOfCivilTickets)
        draw.font_size = 28
        draw.text_alignment = 'center'
        draw.text((int)(printWidth / 2), 180, get_display(arabic_reshaper.reshape(tn)))
        tn = u"الإيراد " +'%.2f'%(batch.closingTotal)
        draw.font_size = 28
        draw.text_alignment = 'center'
        draw.text((int)(printWidth / 2), 210, get_display(arabic_reshaper.reshape(tn)))
        
        tn = u"ر.ت المستخدم " +str(myUSB.userId)
        draw.font_size = 28
        draw.text_alignment = 'center'
        draw.text((int)(printWidth / 2), 240, get_display(arabic_reshaper.reshape(tn)))
        draw(im)
        im.save(filename=tmpImage)

        # Print an image with your printer library

        printerx = printer.File(printFile)
        printerx.set(align="center")
        printerx.image(tmpImage)
        
def printLastBatches(machine,myUSB):
    
    with open(originalPath+'Batch/batch.json','r') as json_file:
        data = json.load(json_file)
        temp = data['batch']
        arrayLength = len(temp)
        
        if(not(arrayLength == 0)):
            
            
            myBatch=batch(None,None,None,None,None,None,None,None)
            r = 10
            if arrayLength < 10:
                r = arrayLength
            for i in range(r):
                        print(i)
                        myBatch.batchNumber = temp[arrayLength-2-i] ['batchNumber']
                        print(myBatch.batchNumber)
                        myBatch.machineId = machine.machineId
                        myBatch.startDate = temp[arrayLength-2-i][ 'startDate']
                        myBatch.endDate = temp[arrayLength-2-i] ['endDate']
                        myBatch.numberOfTickets = temp[arrayLength-2-i] ['numberOfTickets']
                        myBatch.numberOfCivilTickets=temp[arrayLength-2-i] ['numberOfCivilTickets']
                        myBatch.numberOfMilTickets= temp[arrayLength-2-i] ['numberOfMilTickets']
                        myBatch.closingTotal = temp[arrayLength-2-i] ['closingTotal']
                        printZreportDuplicate(myBatch,machine,myUSB)
            
             
            printFile = "/dev/usb/lp0"
            printerx = printer.File(printFile)
            printerx.set(align="center")
            printerx.cut()
                            
                
