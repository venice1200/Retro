# Microtronic Phoenix Uploader  
  
A Python script for transferring MIC code files from the PC to the Microtronic Phoenix via an Arduino connected via USB.  
The Arduino Uno or Nano executes a program that can be accessed via the Python library on the PC.  
The Arduino itself acts as external GPIO pins for the PC, which are connected to the Phoenix DIN pins.
  
**Technical Important Note**  
The Nano wants its digital outputs to be loaded with a maximum of 40 mA, typically only 20 mA.  
The inputs of the Microtronic each have 100 ohms against GND.  
This would then allow 50 mA of current to flow through the Arduino outputs at 5V. Ouch.  
Therefore—to be on the safe side—use 1 kOhm resistors in front of the Microtronic inputs!  
I found the Note in German here:  
https://github.com/rab-berlin/Monarch2090/tree/main/program/2090undArduino#monarch2090-mit-arduino-nano
  
  
The Python Uploader Code is based on the 2095 Emulation of Martin Sauter & Michael Wessel.  
Further information can be found here:  
https://blog.wirelessmoves.com/2017/06/emulating-a-busch-2090-tape-interface-part-1.html  
https://github.com/lambdamikel/microtronic-2095-arduino-emulator/tree/master  
  
The originally used USB-GPIO Python Library and the Arduiono Sketch can be found here:  
https://github.com/ltspicer/usb_gpio  
Available digital pins on Uno/Nano are D2 to D13, configure and use them as input or output.  
I think you need the python library "serial" as well.  
  
**Updated Arduino Sketch 2025-09-07**  
I have updated and enhanced the USB-GPIO Arduino Sketch and added code from here:  
https://github.com/rab-berlin/Monarch2090/tree/main/program/2090undArduino  
to add an RND generator for the Games Monarch and maybe Kniffel & Co.  
  
The Microtronics RND System is not really random so the above programmer has created an  
external Random Generator based on an Arduino which transfers the RND Data via IOs to the Busch 2090.  
The RND Generator uses the same IO Pins as used by the Phoenix Uploader.  
  
Using the Arduino Input Pins D11 and D12 you are able to choose the Aruino Mode during Start or Reset of the Arduino.  
**Mode 0:** D11 open, D12 open, Standard GPIO Mode (default)  
  
**Mode 1:** D11 GND, D12 open,  Random Number Generator 1..6 at D2..D5 maybe for Kniffel ???  
This Mode transfers data without handshake one by one.  
If you like to test this Mode with the Microtronic Kniffel Game from here https://github.com/rab-berlin/Kniffel2090  
replace `F05` in line **0xC9** with `FDD` to use the external generated Values.  

**Mode 2:** D11 open, D12 GND,  Random Number Generator 0..9 at D2..D5 for Microtronic Monarch Game  
Code is copied nearly 1:1 except the IO assigment.  
  
**Mode 3:** D11 GND, D12 GND,   Random Number Generator 0..15 at D2..D5 for ???  
This Mode transfers data without handshake one by one.  
  
See the Arduino Sketch `pgm1_gpio_and_rnd_generator.ino` for Details.  
  
<img src="https://github.com/venice1200/Retro/blob/main/Microtronic_Phoenix/pic/connection.jpg" width="800" />
  
Used IOs:  
Phoenix Inputs <=> Arduino Output  
BUSCH_DIN1 <-> D2  
BUSCH_DIN2 <-> D3  
BUSCH_DIN3 <-> D4  
BUSCH_DIN4 <-> D5  
  
Phoenix Outputs <=> Arduino Input  
BUSCH_DOT3 <-> D6  
BUSCH_DOT4 <-> D7  
D6/D7 are used for the RND Generator.
  
**!! Important !!**  
A GND connection is also needed!  
  
Usage: `2095_pgm1.py [Filename] [ComPort]`  
  
## Example (Windows 11):  
```
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
```
