import time
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
StepPins = [12,16,20,21]


for pin in StepPins:
  GPIO.setup(pin,GPIO.OUT)
  GPIO.output(pin,False)

StepCount = 4
TargetAngle = 526

StepCounter = 0
StepAccum = 0
Direction = 0

Seq_1 = [[0,0,0,1],
         [0,0,1,0],
         [0,1,0,0],
         [1,0,0,0]]

Seq_2 = [[1,0,0,0],
         [0,1,0,0],
         [0,0,1,0],
         [0,0,0,1]]
try:
    
    if(Direction == 1):
        while 1:
            for pin in range(0, 4):
                xpin = StepPins[pin]
                if Seq_1[StepCounter][pin]!=0:
                    GPIO.output(xpin, True)
                else:
                    GPIO.output(xpin, False)

            StepCounter += 1
            StepAccum += 1

            if (StepCounter == StepCount):
                StepCounter = 0
            if (StepCounter<0):
                StepCounter = StepCount

            if (StepAccum == TargetAngle):
                StepAccum = 0
                break
            else:
                time.sleep(0.002)

    else:
        while 1:
            for pin in range(0, 4):
                xpin = StepPins[pin]
                if Seq_2[StepCounter][pin]!=0:
                    GPIO.output(xpin, True)
                else:
                    GPIO.output(xpin, False)      

            StepCounter += 1
            StepAccum += 1

            if (StepCounter == StepCount):
                StepCounter = 0
            if (StepCounter<0):
                StepCounter = StepCount

            if (StepAccum == TargetAngle):
                StepAccum = 0
                break
            else:
                time.sleep(0.002)

except KeyboardInterrupt:
    GPIO.clenup()
