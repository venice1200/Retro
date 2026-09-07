# Binary File Uploader send2a1  
  
"send2a1.py" Python Script  
Tested using Python 3.14.7, the P-LAB Appledore Adapter v1.1a and the Briel Replica 1 TE Rev.3.  
  
The Scripts reads a HEX/Text file and send the Data to an Apple-1 using a connected Terminal/Serial-Port.  
The Text file must have "LF" Line Endings.  
The Baudrate is set to 9600 by default but can be changed using an optional command line parameter.  
  
This script uses the Python Add-Ons: pySerial, progressbar  
  
```  
Usage:  
python send2a1_v0.2.py [Filename] [COM-Port] [Baudrate(optional)]  
  
Examples (Windows):  
python send2a1_v0.2.py mandelbrot65_v1.0_LF.txt COM18 or  
python send2a1_v0.2.py mandelbrot65_v1.0_LF.txt COM18 2400  
```  
  

  
