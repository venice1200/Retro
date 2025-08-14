#
# v1.1 by lm/venice
# Direct Transfer from PC to the Microtronic Phoenix
# using an Arduino Uno or Nano as Serial IO Gateway running
# the usb_gpio sketch and the usb_gpio python library on PC side.
#
# Python Code based on 2095 Emulator Code of Martin Sauter & Michael Wessel from here
# https://blog.wirelessmoves.com/2017/06/emulating-a-busch-2090-tape-interface-part-1.html
# https://github.com/lambdamikel/microtronic-2095-arduino-emulator/tree/master
#
# The used USB-GPIO Python Lib and the Arduiono Skecth can be found here
# https://github.com/ltspicer/usb_gpio
# Available digital pins on Uno/Nano are D2 to D13, configure and use them as input or output.
# I think you need the "serial" library installed.
#
# Many Thanks!
# 
# Used IOs:
# Phoenix Inputs <=> Arduino Output
# BUSCH_DIN1 <-> D2
# BUSCH_DIN2 <-> D3
# BUSCH_DIN3 <-> D4
# BUSCH_DIN4 <-> D5
#
# Phoenix Outputs <=> Arduino Input
# BUSCH_DOT1 <-> D6
# BUSCH_DOT2 <-> D7
# BUSCH_DOT3 <-> D8
#
# !! Important !!
# The GND connection is also needed!
#
# Usage 2095_pgm1.py [Filename] [ComPort]
# Example: 2095_pgm1.py kniffel.mic com16
#
# 2025-08-09 v1.0 Initial Version
# 2025-08-09 v1.1 Add ComPort Argument and checking, add Runtime, cosmetics
# 2025-08-14 v1.2 Remove Wrapper "writeDigitalPin" as the statements are included in the library now
#
#

import time, sys
from usbgpio import USBgpio

version="v1.2"

start_time = time.time()
print("\nWait please, initializing...\n")

if len(sys.argv) < 3:
    print("Error! Not enough Arguments given.")
    print("Usage: {} [Filename] [Port]".format(sys.argv[0]))
    print("Example: {} kniffel.mic com16".format(sys.argv[0]))
    sys.exit()

# Establish a serial connection to the device.
comPort = sys.argv[2]
gpio = USBgpio(comPort, 115200)
time.sleep(1)                   # <= Important!!!

# Set Onboard LED Pin 13 as output
ledPIN = 13
gpio.set_output(ledPIN)

# Delays
delay_bit          = 0.01
delay_after_value  = 0.01
transfer_start_delay = 5

# Variables
pc = 0
myFile = ""

# Busch Inputs <=> Arduino Outputs
BUSCH_DIN1 = 2
BUSCH_DIN2 = 3
BUSCH_DIN3 = 4
BUSCH_DIN4 = 5
gpio.set_output(BUSCH_DIN1)
gpio.set_output(BUSCH_DIN2)
gpio.set_output(BUSCH_DIN3)
gpio.set_output(BUSCH_DIN4)

# Busch Outputs <=> Arduino Inputs
BUSCH_DOT1 = 6
BUSCH_DOT2 = 7
BUSCH_DOT3 = 8
gpio.set_input(BUSCH_DOT1)
gpio.set_input(BUSCH_DOT2)
gpio.set_input(BUSCH_DOT3)

# ---- Defines ----

def resetPins():
    gpio.digital_write(BUSCH_DIN1, "LOW")
    gpio.digital_write(BUSCH_DIN2, "LOW")
    gpio.digital_write(BUSCH_DIN3, "LOW")
    gpio.digital_write(BUSCH_DIN4, "LOW")
#end resetPins

def clockSignal (pin, delay):
  gpio.digital_write(pin, "HIGH")     
  time.sleep (delay/2)                
  gpio.digital_write(pin, "LOW")
  time.sleep (delay/2)
  return;
#end clockSignal

def loadInstructionToBusch2090(in_str):
  # Loop over each of the 3 nibbles (4 bits) of the current instruction
  for y in range(0, 3):

    # Set the mask that is used to check if a bit is 0 or 1
    # to the first bit.
    mask = 1
    
    # Loop over each bit of the current nibble
    for z in range(0, 4):
    
      # If the current bit is 1
      if int(in_str[y], 16) & mask > 0:
        # Output a HIGH bit
        gpio.digital_write(BUSCH_DIN1, "HIGH")
      else:
        # Output a LOW bit
        gpio.digital_write(BUSCH_DIN1, "LOW")
    
      # If this is the first bit of the 3 nibble instruction
      if (y == 0 and z == 0):
        # Raise OUT3 to signal start of a new instruction
        gpio.digital_write (BUSCH_DIN3, "HIGH")
        time.sleep(delay_bit)          
      else:
        # All other bits are signaled with a clock tick on OUT2
        clockSignal(BUSCH_DIN2, delay_bit)           
        
      # Move the 'mask' bit one location forward  
      mask = mask << 1
  # End of current 3 x 4 byte transmission

  # Set all OUTs to 0 to signal the end of the current 3 nibble instruction
  gpio.digital_write(BUSCH_DIN3, "LOW")
  gpio.digital_write(BUSCH_DIN2, "LOW")
  gpio.digital_write(BUSCH_DIN1, "LOW")
  
  # Give the 2090 some time to write the received nibbles to memory
  time.sleep(delay_after_value)
#end of loadInstructionToBusch2090()


# -----------------------------
# ---- Main Programm ----
# -----------------------------

resetPins
pc = 0

try:
    myfile = sys.argv[1]
    micfile = open(myfile, 'r')
    
except IOError:
    print("File Error: File \"{}\" not found!".format(myfile))
    sys.exit()

#print("\n")
print("Tiny PC to Microtronic Phoenix MIC-File Uploader {}.".format(version))
print("Your Phoenix is running PGM 1?")
print("Stop transfer with STRG/CTRL-C, if needed.\n")
print("Transfer of \"{}\" starts in {} seconds using Port \"{}\".\n".format(myfile, transfer_start_delay, comPort))

time.sleep(transfer_start_delay)

print("Go!\n")
gpio.digital_write(ledPIN, True)  # On Board LED on

pc = 0

for line in micfile.readlines():
    try:
        if len(line) < 3: continue
        if line[0] == " ": continue
        if line[0].isalpha() != True and line[0].isdigit() != True: continue
        
        # Get data from read line
        data = line[0:3]
        
        # Search/replace OCR code errors,                                                           
        # see https://github.com/lambdamikel/Busch-2090/tree/master/software
        data = data.replace ("I", "1")
        data = data.replace ("l", "1")
        data = data.replace ("Q", "0")
        data = data.replace ("O", "0")
        data = data.replace ("p", "D")
        
        # Some output
        print("PC: {0:#04x}/{0:03d} <=> {1}".format(pc,data))
        
        # Send 3 x 4 Bit Instructions to the 2090/Phoenix
        loadInstructionToBusch2090(data)
        
        # Increase PC
        pc +=1
        
    except KeyboardInterrupt:
        # STRG-C
        break 
        
# IO Cleanup, File close, Power off
runtime=time.time() - start_time
resetPins
micfile.close()
print("\n")
print("Transferred {} Code-Lines in {:3.2f} Seconds.".format(pc, runtime))
gpio.digital_write(ledPIN, False)
print("Now Reset your Phoenix.")
print("Cheers :-)")



