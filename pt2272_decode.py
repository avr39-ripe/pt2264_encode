#!/usr/bin/env python

#(c) 2014 Alexander V. Ribchansky
#based on code from http://thomasolson.com/PROJECTS/SC2262/
from wiringpi2 import *

INPUT = 0
OUTPUT = 1
LOW = 0
HIGH = 1

recvPin = 2
# ledPin = 1

FoscCshort = 500
FoscClong = 1500
FoscTol = 200

SHORTMAX = FoscCshort + FoscTol
SHORTMIN = FoscCshort - FoscTol
LONGMAX = FoscClong + FoscTol
LONGMIN = FoscClong - FoscTol
SAMPLES = 120

edges = [0, ] * SAMPLES
pulses = [0, ] * SAMPLES
polarity = [0, ] * SAMPLES
pulsePair = ['0', ] * SAMPLES
addressData = ['\0', ] * SAMPLES

wiringPiSetup()

pinMode(recvPin, INPUT)
# pinMode(ledPin, OUTPUT)


def pt2272_decode():

    for x in range(0, SAMPLES):
        pulsePair[x] = '0'
        addressData[x] = '\0'

    for x in range(0, SAMPLES, 2):
        while not digitalRead(recvPin):
            #low to high edge detected
            edges[x] = micros()
            polarity[x] = 1
            print("0>1 ")
        while digitalRead(recvPin):
            #high to low edge detected
            edges[x+1] = micros()
            polarity[x+1] = 0
            print("1>0 ")

#    digitalWrite(ledPin, HIGH)  # LED ON after edges samples detected

    for x in range(1, SAMPLES):
        pulses[x-1] = edges[x] - edges[x-1]
        #pulse widths

    # NOTE: array position 0 should be a high polarity pulse
    # So assuming so, then all odd values are low.
    for x in range(0, SAMPLES, 2):
        # Assuming nominal short pulse are 500uS and long are 1500uS
        if pulses[x] > pulses[x+1]:  # Hi longer Lo might be ONE
            if pulses[x] > LONGMIN and pulses[x] < LONGMAX:  # LongHigh valid
                if pulses[x+1] > SHORTMIN and pulses[x+1] < SHORTMAX:  # ShortLow valid
                    # valid interim digit 1
                    pulsePair[x/2] = '1'
        elif pulses[x] < pulses[x+1]:  # Hi shorter than Lo- ZERO? or SYNC?
            if pulses[x] > SHORTMIN and pulses[x] < SHORTMAX:  # ShortHigh valid
                if pulses[x+1] > LONGMIN and pulses[x+1] < LONGMAX:  # LongLo valid
                    # valid interim digit 0
                    pulsePair[x/2] = '0'
            elif pulses[x+1] > 14400 and pulses[x+1] < 17600:  # Sync valid
                # valid interim digit S(ync)
                pulsePair[x/2] = 'S'
    # Analyse to get actual security CODES
    x = 0
    y = 0

    # Find the first S
    while pulsePair[x] != 'S' and x < SAMPLES/2:
        x += 1

    # Found S so start converting until next S
    x += 1

    while pulsePair[x] != 'S' and x < SAMPLES/2:
        if pulsePair[x] == '0' and pulsePair[x+1] == '0':
            print('0')  # ZERO LO (00)
            addressData[y] = '0'
        elif pulsePair[x] == '1' and pulsePair[x+1] == '1':
            print('1')  # ONE HI (11)
            addressData[y] = '1'
        elif pulsePair[x] == '0' and pulsePair[x+1] == '1':
            print('F')  # Float TriState (01)
            addressData[y] = 'F'
        else:
            print('U')  # Undefined (10)
            addressData[y] = 'U'
        x += 2
        y += 1

    if pulsePair[x] == 'S':
        addressData[y] = '\0'  # NULL ends string

        print(addressData)  # Print if not empty
        return addressData
#    digitalWrite(ledPin, LOW)  # LED off after edge samples detected

if __name__ == "__main__":
    while True:
        pt2272_decode()