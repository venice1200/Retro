#
# 2026 by lm/venice
# Read text file and send to Apple I using the Appledores-Nano-Serial-Port
#
# This script uses:
# pySerial
#
# Version 0.1
#

# Libs
import time, serial, sys

# Version
version="v0.1"

# Set Start Time
start_time = time.time()

# Vars
cdelay = 0.020 # 20-50ms, 0.01 NOK
ldelay = 0.200 # 100-300ms
brate  = 9600  # Baurate
idelay = 3     # Serial Init Delay
cc = 0         # Char-Counter
lc = 1         # Line Counter
newline = True # Newline Flag

# Check Command Line
if len(sys.argv) < 3:
    print("Error! Not enough Arguments given!")
    print("Usage: {} [Filename] [Port]".format(sys.argv[0]))
    print("Example: {} file.txt COM16".format(sys.argv[0]))
    sys.exit()

#Set and Open Serial Port
ser = serial.Serial(
    port=sys.argv[2],
    baudrate=brate,
    bytesize=8,
    parity='N',
    stopbits=1,
    timeout=None,
    xonxoff=0,
    rtscts=0
)

print("\nPlease wait!")
print("Char-Delay: {} sec".format(cdelay))
print("Line-Delay: {} sec".format(ldelay))
print("Serial Speeed: {} baud".format(brate))
print("")

# Get No. of lines
with open(sys.argv[1], "rb") as file:
    fnolines = sum(1 for _ in file)

# Wait for Serial
# If there is an Arduino on the other site it will be Reseted after Opening the Port
print("Wait for Serial Port", sys.argv[2], end='', flush = True)
for x in range(idelay,0,-1):
    print(".", end='', flush = True)
    time.sleep(1.0)
print ("\nSending \"{}\" with {} lines.\n".format(sys.argv[1],fnolines))
time.sleep(1.0)

# Open File
with open(sys.argv[1]) as file:
    # Loop
    while True:
        # Read Char
        c = file.read(1)
        # No more chars?
        if not c:
            print("\nEnd of file.")
            break
        # Newline
        if "\n" in c:
            newline = True
            print(c, end='')
            ser.write(bytes('\r', encoding='utf8'))
            time.sleep(ldelay)
            # Increase Line Counter
            lc+=1
        # New Character
        else :
            if newline:
                print("Sending {}/{}> ".format(lc,fnolines), end='', flush = True)
                newline = False
            print(c, end='', flush = True)
            ser.write(bytes(c, encoding='utf8'))
            time.sleep(cdelay)
        # Increase Character Counter
        cc+=1
    # End While
        
# Cleanup and show Transfer Statistics
lc-=1
runtime=time.time() - start_time
file.close()
print("Transferred \"{}\" with {} Lines and {} Characters in {:3.2f} Seconds = {:3.2f} chars/sec.".format(sys.argv[1], lc, cc, runtime, cc/runtime))

#############
#    END    #
#############
