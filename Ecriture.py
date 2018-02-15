#!/usr/bin/env python

import RPi.GPIO as GPIO
import SimpleMFRC522

reader = SimpleMFRC522.SimpleMFRC522()

try:
    text = raw_input('Donnée :')
    print("Placer le tag RFID ...")
    reader.write(text)
    print("OK")
finally:
    GPIO.cleanup()
