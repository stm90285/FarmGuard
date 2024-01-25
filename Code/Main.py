import notecard
import serial
import time
import json
from huskylib import HuskyLensLibrary
from periphery import I2C

# Initialize HuskyLensLibrary and I2C port
hl = HuskyLensLibrary("SERIAL", "/dev/ttyUSB0")
port = I2C("/dev/i2c-1")

# Open Notecard connection over I2C
nCard = notecard.OpenI2C(port, 0, 0)

# Restore Notecard, set the hub product, and wait for stability
req = {"req": "card.restore"}
req["delete"] = True
rsp = nCard.Transaction(req)
print(rsp)
time.sleep(5)

req = {"req": "hub.set"}
req["product"] = "com.gmail.stm90285:virtualfence"
rsp = nCard.Transaction(req)
print(rsp)
time.sleep(5)

# Function to map detected IDs to animal names using a "switch" dictionary
def ObjectDetect(obj):
    items = obj.__dict__
    detected_id = items['ID']
    
    # Switch-like dictionary to map IDs to animal names
    animal_names = {
        1: "Wild Boar",
        2: "Wild Boar",
        3: "Wild Boar",
        4: "Elephant",
        5: "Elephant",
        6: "Elephant",
        7: "Monkey",
        8: "Monkey",
        9: "Monkey",
    }
    
    return animal_names.get(detected_id, None)

# Function to post data to Notecard and sync with the hub
def PostData(animal_name):
    req = {"req": "note.add"}
    req["body"] = {"customMessage": f"{animal_name} Detected"}
    rsp = nCard.Transaction(req)
    print(rsp)
    time.sleep(5)
    
    req = {"req": "hub.sync"}
    rsp = nCard.Transaction(req)
    print(rsp)
    time.sleep(10)

# Main loop for continuous object detection
while True:
    try:
        # Detect object and get the corresponding animal name
        animal_name = ObjectDetect(hl.learned())
        if animal_name is not None:
            # Post data to Notecard and sync with the hub
            PostData(animal_name)
    except IndexError:
        # Ignore index errors
        pass
