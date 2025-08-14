# Microtronic Phoenix  
..
Direct 2095 Transfer from PC to the Microtronic Phoenix using an Arduino Uno or Nano as Serial IO Gateway.  
  
The Arduino runs a gateway sketch which can be accessed by the python library from the PC side.  
  
Python Code based on 2095 Emulator Code of Martin Sauter & Michael Wessel from here:  
https://blog.wirelessmoves.com/2017/06/emulating-a-busch-2090-tape-interface-part-1.html  
https://github.com/lambdamikel/microtronic-2095-arduino-emulator/tree/master  
  
The used USB-GPIO Python Lib and the Arduiono Skecth can be found here:  
https://github.com/ltspicer/usb_gpio  
Available digital pins on Uno/Nano are D2 to D13, configure and use them as input or output.  
I think you need the "serial" library installed.  
  
Used IOs:  
Phoenix Inputs <=> Arduino Output  
BUSCH_DIN1 <-> D2  
BUSCH_DIN2 <-> D3  
BUSCH_DIN3 <-> D4  
BUSCH_DIN4 <-> D5  
  
Phoenix Outputs <=> Arduino Input  
BUSCH_DOT1 <-> D6  
BUSCH_DOT2 <-> D7  
BUSCH_DOT3 <-> D8  
  
!! Important !!  
The GND connection is also needed!  
  
Usage 2095_pgm1.py [Filename] [ComPort]  
Example: 2095_pgm1.py kniffel.mic com16  
  
