#!/usr/bin/env python

#(c) 2014 Alexander V. Ribchansky
#based on code from http://thomasolson.com/PROJECTS/SC2262/
from wiringpi2 import *

INPUT = 0
OUTPUT = 1
LOW = 0
HIGH = 1

xmtrPin = 0

PULSESHORT = 500
PULSELONG = 1500
PULSESYNC = 16000

#PULSESHORT = 160
#PULSELONG = 500
#PULSESYNC = 5333

wiringPiSetup()

pinMode(xmtrPin, OUTPUT)
digitalWrite(xmtrPin, LOW)


def ookPulse(on, off):
    digitalWrite(xmtrPin, HIGH)
    delayMicroseconds(on)
    digitalWrite(xmtrPin, LOW)
    delayMicroseconds(off)


def pt2262Send(packet):
    for repeat in range(0, 4):

        for x in range(0, 12):

            if packet[x] == '0':
#                print '0'
                ookPulse(PULSESHORT, PULSELONG)
                ookPulse(PULSESHORT, PULSELONG)
            elif packet[x] == '1':
#                print '1'
                ookPulse(PULSELONG, PULSESHORT)
                ookPulse(PULSELONG, PULSESHORT)
            elif packet[x] == 'F' or packet[x] == 'f':
#                print 'f'
                ookPulse(PULSESHORT, PULSELONG)
                ookPulse(PULSELONG, PULSESHORT)
            elif packet[x] == 'U' or packet[x] == 'u':
#                print 'u'
                ookPulse(PULSELONG, PULSESHORT)
                ookPulse(PULSESHORT, PULSELONG)

        ookPulse(PULSESHORT, PULSESYNC)
#        print 'sync'

if __name__ == "__main__":
    while True:
        pt2262Send("FFFFF0FF0001")
        pt2262Send("FFFFF0FF0010")

