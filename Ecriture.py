#!/usr/bin/env python
# -*- coding: utf8 -*-
# Version modifiee de la librairie https://github.com/mxgxw/MFRC522-python

import RPi.GPIO as GPIO
import MFRC522
import signal

continue_reading = True

# Fonction qui arrete la lecture proprement 
def end_read(signal,frame):
    global continue_reading
    print ("Lecture terminée")
    continue_reading = False
    GPIO.cleanup()

signal.signal(signal.SIGINT, end_read)
MIFAREReader = MFRC522.MFRC522()

data = []
texte = raw_input("Entrez une chaine de caractère :\n")
for c in texte:
    if (len(data)<16):
        data.append(int(ord(c)))
while(len(data)!=16):
    data.append(0)
print ("Placez votre carte RFID")

while continue_reading:
      
    # Detecter les tags
    (status,TagType) = MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL)

    # Une carte est detectee
    if status == MIFAREReader.MI_OK:
        print ("Carte detectee")
    
    # Recuperation UID
    (status,uid) = MIFAREReader.MFRC522_Anticoll()

    if status == MIFAREReader.MI_OK:

        # Print UID
        print ("UID de la carte : "+str(uid[0])+"."+str(uid[1])+"."+str(uid[2])+"."+str(uid[3]))
    
        # Clee d authentification par defaut
        key = [0xFF,0xFF,0xFF,0xFF,0xFF,0xFF]
        
        # Selection du tag
        MIFAREReader.MFRC522_SelectTag(uid)

        # Authentification
        status = MIFAREReader.MFRC522_Auth(MIFAREReader.PICC_AUTHENT1A, 8, key, uid)

        if status == MIFAREReader.MI_OK:
            print ("Le secteur 8 contient actuellement : ")
            MIFAREReader.MFRC522_Read(8)

            print ("Ecriture ...")
            MIFAREReader.MFRC522_Write(8, data)

            print ("Le secteur 8 contient maintenant : ")
            MIFAREReader.MFRC522_Read(8)

            # Stop
            MIFAREReader.MFRC522_StopCrypto1()
            continue_reading = False

        else:
            print ("Erreur d authentication")
