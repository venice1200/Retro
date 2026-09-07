# Binary File Uploader send2a1  
  
"send2a1.py" Python Script
Read HEX/Text file and send the Data to an Apple-1 using a connected Terminal/Serial-Port  
  
This script uses:  
pySerial, progressbar  
  
```  
Usage  
python send2a1_v0.2.py [Filename] [COM-Port] [Baudrate(optional)]  
  
Example (Windows)  
 python send2a1_v0.2.py mandelbrot65_v1.0_LF.txt COM18 or  
 python send2a1_v0.2.py mandelbrot65_v1.0_LF.txt COM18 2400  
  
 Baudrate is set to 9600 by default but can be changed using last command line parameter   
```   
