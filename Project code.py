#NOTE: The "Check" prints are scattered through the code for debugging, they should all
# run if the code is working 

#Libraries to import
import smbus
import sys
import requests
from smbus import SMBus
from gpiozero import MotionSensor, LED
from picamera import PiCamera 
from signal import pause 
from filestack import Client
from guizero import App, Text, PushButton

#Global Vairables to declare 
client = Client("ACf97urbvR1OZ71NezZspz")
print("Check1")
camera = PiCamera()
print("Check2")
TestLED = LED(17)
camera.resolution = (1920, 1080)
addr = 0x8
bus = SMBus(1)
##GUI DEFINITIONS
app = App()

# code which initiates the capture and the send event 
def send_alert():
       camera.capture("image.jpg") 
       new_filelink = client.upload(filepath="image.jpg") 
       print(new_filelink.url)
       r = requests.post("https://maker.ifttt.com/trigger/trigger/with/key/q8lCFRu1JJ6--Hac8Ga-0", json={"value1" : new_filelink.url}) 
       if r.status_code == 200: 
        print("Alert Sent") 
       else: 
        print("Error")
		camera.capture('/home/pi/capture.jpg')        
       DisArmSys.when_pressed = DisArmSystem
       print("Check3")
           
#Function to arm the system and allow the device to start taking captures         
def ArmSystem():
    bus.write_byte(addr, 0x1)
    sleep(100)
    bus.write_byte(addr, 0x0)
    valid = True
    TestLED.on()
    while valid == True: #Runs code continuously while system is armed, only stops code if system has been disarmed
        print("system armed")
        pir = MotionSensor(4)
        pir.when_motion = send_alert 
        if DisArmSys.is_pressed:
            valid = False
        sleep(10) # Delay so the function doesnt send multiple captures to the user
        print("Check4")


#Function used to disarm the system when the Disarm button has been pressed 
def DisArmSystem():
    TestLED.off()
    print("system Disarmed")
    while ArmSys.when_pressed != True: ##conditional loop fault tolerance measure to ensure the system does not take any more readings while the diarm has been pressed
        sleep(0.1)
    print("Check5")

           
 ## CONTROLLERS (BUTTONS)
ArmSys = PushButton(app, text = "Arm System", command=ArmSystem, height = 1, width = 24)
ArmSys.when_pressed = ArmSystem
ArmSys.bg = "red"
DisArmSys = PushButton(app, text = "Disarm System", command=DisArmSystem, height = 1, width = 24)
DisArmSys.when_pressed = DisArmSystem
DisArmSys.bg = "green"
##Exit function
def Exit():
    sys.exit()

##Exit Button
ExtButton = PushButton(app, text = "Exit", command = Exit, height = 1, width = 10)
ExtButton.bg = "grey"
ExtButton.when_pressed = Exit
app.display()
print("Check6")
pause()


