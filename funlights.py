"""
Written by Richard Garsthagen - The.anykey@gmail.com

You will need the following 3 python libraries:
- pywinusb

You can install these with pip install [library name]

Feel free to modify and distibute in anyway you like.

This is tested with the Komplete Kontrol S61 keyboard. If you use a different one,
you probably have to change the note offset.

"""

import pywinusb.hid as hid
import time
import math


def Connect():
    global komplete_device
    global reports
    global bufferC
    kompleteVID = 0x17cc
    kompletePID = 0x1360
    all_devices = hid.HidDeviceFilter(vendor_id = kompleteVID, product_id = kompletePID).get_devices()
    found = False
    if len(all_devices) == 0:
        print ("No komplete device found!")
        found = False
    else:
        print ("Komplete found :-)" )
        komplete_device = all_devices[0]
        komplete_device.open()
        found = True
     
        reports = komplete_device.find_output_reports()

        # Initialize else the light control does not seem to work
        bufferI = [0x00] * 249
        bufferI[0] = 0xa0

        reports[3].set_raw_data(bufferI)
        reports[3].send()

        # Set all keys to 0x00 - Black / no light
        bufferC = [0x00] * 249
        bufferC[2] = 0x82

        reports[2].set_raw_data(bufferC)
        reports[2].send()
   
    return found

def CoolDemoSweep(loopcount):
    speed = 0.01
    for loop in range(0,loopcount):
        for x in range(0, 61):
            bufferC = [0x00] * 249
            bufferC[0] = 0x82
            bufferC[x*3-2] = 0xFF
            reports[2].set_raw_data(bufferC)
            reports[2].send()
            time.sleep(speed)
        for x in range(61, 0,-1):
            bufferC = [0x00] * 249
            bufferC[0] = 0x82
            bufferC[x*3-2] = 0xFF
            reports[2].set_raw_data(bufferC)
            reports[2].send()
            time.sleep(speed)
    bufferC = [0x00] * 249
    bufferC[0] = 0x82
    reports[2].set_raw_data(bufferC)
    reports[2].send()
   
def rainbowloop(loopcount):

    frequency  = float(0.1);
    speed = 0.01
    x = 20
    for l in (0,loopcount):
        for k in range (0,61):
            for i in range (0,61):
               red   = math.sin(frequency*i + 0) * x + 128
               green = math.sin(frequency*i + 2) * x + 128
               blue  = math.sin(frequency*i + 4) * x + 128
               sk = i+k
               if sk > 61:
                   sk = sk-61
               bufferC[(sk*3)+1] = int(red)
               bufferC[(sk*3)+2] = int(green)
               bufferC[(sk*3)+3] = int(blue)
            bufferC[0] = 0x82
            reports[2].set_raw_data(bufferC)
            reports[2].send()
            time.sleep(speed)
        for k in range (61,0, -1):
            for i in range (0,61):
               red   = math.sin(frequency*i + 0) * x + 128
               green = math.sin(frequency*i + 2) * x + 128
               blue  = math.sin(frequency*i + 4) * x + 128
               sk = i+k
               if sk > 61:
                   sk = sk-61
               bufferC[(sk*3)+1] = int(red)
               bufferC[(sk*3)+2] = int(green)
               bufferC[(sk*3)+3] = int(blue)
            bufferC[0] = 0x82
            reports[2].set_raw_data(bufferC)
            reports[2].send()
            time.sleep(speed)
       
        

    

if __name__ == '__main__':
    connected = Connect()
    if connected:
        while True:
            CoolDemoSweep(2)
            rainbowloop(10)

        
        




        
    
