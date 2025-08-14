# Microtronic Phoenix Uploader  
  
Direct transfer of MIC Files from PC to the Microtronic Phoenix using Python on PC and an connected Arduino.  
The Arduino Uno or Nano runs a program which can be accessed by the python library on the PC.  
The Arduino himself acts like external GPIO Pins for the PC which are connected to the Phoenix DIN Pins.  
  
The Python Code is based on the 2095 Emulator Code of Martin Sauter & Michael Wessel from here:  
https://blog.wirelessmoves.com/2017/06/emulating-a-busch-2090-tape-interface-part-1.html  
https://github.com/lambdamikel/microtronic-2095-arduino-emulator/tree/master  
  
The used USB-GPIO Python Lib and the Arduiono Skecth can be found here:  
https://github.com/ltspicer/usb_gpio  
Available digital pins on Uno/Nano are D2 to D13, configure and use them as input or output.  
I think you need the "serial" library installed as well.  
  
See: https://github.com/venice1200/Retro/blob/main/Microtronic_Phoenix/pic/connection.jpg  
  
Used IOs:  
Phoenix Inputs <=> Arduino Output  
BUSCH_DIN1 <-> D2  
BUSCH_DIN2 <-> D3  
BUSCH_DIN3 <-> D4  
BUSCH_DIN4 <-> D5  
  
Phoenix Outputs <=> Arduino Input (not in use)  
BUSCH_DOT1 <-> D6  
BUSCH_DOT2 <-> D7  
BUSCH_DOT3 <-> D8  
  
!! Important !!  
A GND connection is also needed!  
  
Usage `2095_pgm1.py [Filename] [ComPort]`  
..
## Example (Windows 11):  
python.exe 2095_pgm1.py kniffel.mic com16  
  
Wait please, initializing...  
  
Tiny PC to Microtronic Phoenix MIC-File Uploader v1.2.  
Your Phoenix is running PGM 1?  
Stop transfer with STRG/CTRL-C, if needed.  
  
Transfer of "kniffel.mic" starts in 5 seconds using Port "com18".  
  
Go!  
  
PC: 0x00/000 <=> 1F8  
PC: 0x01/001 <=> FE8  
PC: 0x02/002 <=> 1F9  
PC: 0x03/003 <=> 1FA  
...  
PC: 0xf7/247 <=> 4D1  
PC: 0xf8/248 <=> FB2  
PC: 0xf9/249 <=> 4E2  
PC: 0xfa/250 <=> CEF  
  
  
Transferred 251 Code-Lines in 42.51 Seconds.  
Now Reset your Phoenix.  
Cheers :-)  
..