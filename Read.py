#!/usr/bin/env python
# -*- coding: utf8 -*-

import RPi.GPIO as GPIO
import MFRC522
import signal

continue_reading = True


# Capture SIGINT for cleanup when the script is aborted
def end_read(signal, frame):
    global continue_reading
    print "Ctrl+C captured, ending read."
    continue_reading = False
    GPIO.cleanup()


# Hook the SIGINT
signal.signal(signal.SIGINT, end_read)

# Create an object of the class MFRC522
MIFAREReader = MFRC522.MFRC522()

# Welcome message
print "Welcome to the MFRC522 data read example"
print "Press Ctrl-C to stop."

# This loop keeps checking for chips. If one is near it will get the UID and authenticate
while continue_reading:

    # Scan for cards    
    (status, TagType) = MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL)

    # If a card is found
    if status == MIFAREReader.MI_OK:
        print "Card detected"

    # Get the UID of the card
    (status, uid) = MIFAREReader.MFRC522_Anticoll()

    # If we have the UID, continue
    if status == MIFAREReader.MI_OK:

        # Print UID
        print "Card read UID: " + str(uid[0]) + "," + str(uid[1]) + "," + str(uid[2]) + "," + str(uid[3])

        # This is the default key for authentication
        key = [0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF]
        keys = [
            [0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF],
            [0x00, 0x00, 0x00, 0x00, 0x00, 0x00],
            [0xa0, 0xa1, 0xa2, 0xa3, 0xa4, 0xa5],
            [0xb0, 0xb1, 0xb2, 0xb3, 0xb4, 0xb5],
            [0xaa, 0xbb, 0xcc, 0xdd, 0xee, 0xFF],
            [0x4d, 0x3a, 0x99, 0xc3, 0x51, 0xdd],
            [0x1a, 0x98, 0x2c, 0x7e, 0x45, 0x9a],
            [0xd3, 0xf7, 0xd3, 0xf7, 0xd3, 0xF7],
            [0x71, 0x4c, 0x5c, 0x88, 0x6e, 0x97],
            [0x58, 0x7e, 0xe5, 0xF9, 0x35, 0x0F],
            [0xa0, 0x47, 0x8c, 0xc3, 0x90, 0x91],
            [0x53, 0x3c, 0xb6, 0xc7, 0x23, 0xF6],
            [0x8F, 0xd0, 0xa4, 0xF2, 0x56, 0xe9],
        ]

        # Select the scanned tag
        MIFAREReader.MFRC522_SelectTag(uid)

        key_len = keys.__len__()
        i = 0
        while i < key_len:
            # Authenticate
            status = MIFAREReader.MFRC522_Auth(MIFAREReader.PICC_AUTHENT1A, 8, keys[i], uid)

            # Check if authenticated
            if status == MIFAREReader.MI_OK:
                MIFAREReader.MFRC522_Read(8)
                MIFAREReader.MFRC522_StopCrypto1()
                break
            else:
                print(keys[i])
                print "Authentication error"
            i += 1
