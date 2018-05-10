"""
McMaster University IBEHS 1P10

Group 1
Alarm Detection Warning Device for Hearing Impared Individuals
        - Program is able to calculate the average sound intensity,
          and use that to determine whether or not an emergency alarm is ringing.
        - If an alarm is found to be ringing, a vibration motor is triggered, indicating
          to the user that an alarm is ringing
          
February 28, 2018
"""
#Import Modules
import PCF8591 as ADC
import RPi.GPIO as GPIO
import time

#ADC Converter Configuration
def setup():
    ADC.setup(0x48)
setup()

#Vibration Motor Configuration
pin = 19 #pin for vibration motor
GPIO.setmode(GPIO.BCM)
GPIO.setup(pin,GPIO.OUT)

def on():
    GPIO.output(pin,0) #activate vibration motor
def off():
    GPIO.output(pin,1) #decactivate vibration motor

#Functions for Main()
def checkAverage(data): #inputs individual data values, and returns the average of the previous 10 entries
        global listValues
        if data > 100.0: #do not include data below 100
                listValues.append(data) #append data to list of values
                if len(listValues) > 10: #if the list is larger than 10, remove the oldest entry
                        listValues.remove(listValues[0])
        try:
                average = sum(listValues)/len(listValues) #calculate the average of the list
                average = round(average,1) #round the average to 1 decimal place for ease of readability
        except ZeroDivisionError: #if the first data entry is less than 100, the list will be empty
                average = data
        return(average)

def ActivateVibration():
    Vibrate = True
    while Vibrate == True: #loop until keyboard is interupted
        try:
            print("Vibrate")
            on() #turn on vibration motor
            time.sleep(0.5)
            
        except KeyboardInterrupt: #in place of a reset button
            print("\nSensor Reset.\n")
            off() #turn off vibration motor
            Vibrate = False
        
def Main():
    while True: #Run indefinitely when on power
        global listValues
        listValues = [] #reset/initialize average when sensor is reset
        
        try:
                analyseSound = True
                while analyseSound == True:
                        data = ADC.read(0) #runs with individual data entries
                        average = checkAverage(data) #Calculate a running average of the previous 10 data entries
                        print('Average Sound Intensity: '+ str(average))
                        if average > 150: #if the average if over 150, the alarm is ringing
                                analyseSound = False
                                ActivateVibration() #if activate vibration returns false, reset sensor
                        time.sleep(0.5) #only an alarm ringing for more than 5 seconds will be registered (0.5 seconds per entry * 10 entries)
                        
        except KeyboardInterrupt: #if ctrl C is pressed during analysis, program will exit
            print("\nProgram Terminated.")
            break #Break from while True loop
        
Main()
