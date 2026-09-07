#
# "send2a1.py" Python Script 2026 by lm/venice
# Read HEX/Text file and send the Data to an Apple-1 using a connected Serial-Port
#
# This script uses:
# pySerial, progressbar
#
# Usage
# python send2a1_v0.2.py [Filename] [COM-Port] [Baudrate(optional)]
#
# Example (Windows)
# python send2a1_v0.2.py mandelbrot65_v1.0_LF.txt COM18 or
# python send2a1_v0.2.py mandelbrot65_v1.0_LF.txt COM18 2400
#
# Baudrate is set to 9600 by default but can be changed using last command line parameter
#
# Version 
# 0.1 Intial Version, write all sent values on Desktop
# 0.2 Use a Progressbar as Progress-Indikator instead of Text
#

# Libs
import time, serial, sys, progressbar

# Version
version="v0.2"

# Set Start Time
start_time = time.time()

# Vars
cdelay = 0.020 # 20-50ms, 0.01 NOK, 0.015 OK, 0.02 Safe
ldelay = 0.200 # 100-300ms
brate  = 9600  # Baurate
idelay = 3     # Serial Init Delay, wait for rebooted Arduino (Appledore Nano direct Connection)
cc = 0         # Char-Counter
lc = 0         # Line Counter

# Progressbar Object
bar = progressbar.ProgressBar(maxval=100)

# Check Command Line
if len(sys.argv) < 3:
    print("Error! Not enough Command Parameter given!")
    print("Usage: {} [Filename] [Port] [Baudrate(optional)]".format(sys.argv[0]))
    print("Example: {} TEXT.txt COM16 2400".format(sys.argv[0]))
    sys.exit()

# Baudrate override using Command Line Parameter
if len(sys.argv) == 4:
    brate=sys.argv[3]

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

# Show Infos
print("\n{} {}".format(sys.argv[0], version))
print("----------------------------------------------------------------")
print("Usage:")
print("{} [Filename] [Port] [Baudrate(optional)]".format(sys.argv[0]))
print("----------------------------------------------------------------")
print("Settings:")
print("Char-Delay: {} sec".format(cdelay))
print("Line-Delay: {} sec".format(ldelay))
print("Serial Speeed: {} baud".format(brate))
print("")

# Get No. of lines in File
with open(sys.argv[1], "rb") as file:
    fnolines = sum(1 for _ in file)

# Wait a moment
# If there is an Arduino on the other site it will be reseted after Opening the Port
print("Wait for Serial Port", sys.argv[2], end='', flush = True)
for x in range(idelay,0,-1):
    print(".", end='', flush = True)
    time.sleep(1.0)
print ("\nSending \"{}\" with {} lines.\n".format(sys.argv[1],fnolines))
time.sleep(1.0)

# Open File
with open(sys.argv[1]) as file:
    print("Progress:")
    # Init Progressbar
    bar.start()
    # Loop
    while True:
        # Read Char
        c = file.read(1)
        # No more chars?
        if not c:
#            print("\nEnd of file.")
            break
        # Newline
        if "\n" in c:
            ser.write(bytes('\r', encoding='utf8'))
            time.sleep(ldelay)
            # Increase Line Counter
            lc+=1
        # New Character
        else :
            ser.write(bytes(c, encoding='utf8'))
            time.sleep(cdelay)
        # Increase Character Counter
        cc+=1
        bar.update(lc*100/fnolines)
    # End While
        
# Cleanup and show Transfer Statistics
bar.finish()
file.close()
runtime=time.time() - start_time
print("\nDone.")
print("Transferred \"{}\" with {} Chars in {} Lines in {:3.2f} Seconds = {:3.2f} cps.".format(sys.argv[1], cc, lc, runtime, cc/runtime))

#############
#    END    #
#############
