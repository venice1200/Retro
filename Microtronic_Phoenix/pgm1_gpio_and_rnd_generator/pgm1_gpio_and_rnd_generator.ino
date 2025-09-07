//
// 2025-09-07 venice1200
// 
// Modified Arduino Sketch from here https://github.com/ltspicer/usb_gpio
// 
// Use D11 and D12 during start/reset of the arduino to choose the Mode
//
// Mode 0: D11 open, D12 open, Standard GPIO Mode
// Mode 1: D11 GND, D12 open,  Random Number Generator 1..6 at D2..D5 maybe for Kniffel ???
//         This Mode transfers data without handshake one by one
//         Replace F05 in line C9 with FDD in Kniffel Program to use the DIN1..DIN4 RND Values
// Mode 2: D11 open, D12 GND,  Random Number Generator 0..9 at D2..D5 for Microtronic Monarch Game
//         see https://github.com/rab-berlin/Monarch2090
//         Code is copied nearly 1:1 except the IO assigment, see below.
// Mode 3: D11 GND, D12 GND,   Random Number Generator 0..15 at D2..D5 for ???
//         This Mode transfers data without handshake oine by one (untested)
// 
// IOs:
// Arduino <---------> Busch
// --------------------------
// D2 (out)    <->     DIN1
// D3 (out)    <->     DIN2  
// D4 (out)    <->     DIN3
// D5 (out)    <->     DIN4
// D6 (in)     <->     DOT3
// D7 (in)     <->     DOT4
// D8 (in Pullup) <->  Switch against GND (Monarch Re-Start)
//
// If you like to enable debuging to see the RND values via serial with 115200 baud
// uncomment the #define XDEBUG statement below.
//

#include <Servo.h>

#define MAX_SERVOS 8
const int servo_pins[MAX_SERVOS] = {2, 3, 4, 5, 6, 7, 8, 9};
Servo servos[MAX_SERVOS];
bool servo_attached[MAX_SERVOS] = {false, false, false, false, false, false, false, false};

// Debug output via serial? 
// Uncomment the following line.
//#define XDEBUG

// Mode 0..3
int mode = 0;

unsigned int z;
unsigned int taste;
unsigned int m2090Out4;
unsigned int m2090Out3;

int get_servo_index(int pin) {
  for (int i = 0; i < MAX_SERVOS; i++) {
    if (servo_pins[i] == pin) return i;
  }
  return -1;
}

void setup() {
  Serial.begin(115200);
  // Mode Inputs
  pinMode(11, INPUT_PULLUP);
  pinMode(12, INPUT_PULLUP);
  delay(500);

  // Get Modes, 0=GPIO Mode (default), 1=RND6 Mode, 2=RND10 Mode, 3=RND16 Mode
  if (!digitalRead(11) and digitalRead(12)) mode = 1;
  if (digitalRead(11) and !digitalRead(12)) mode = 2;
  if (!digitalRead(11) and !digitalRead(12)) mode = 3;
  
#ifdef XDEBUG
  // Which mode?
  Serial.print("Mode: ");
  Serial.println(mode);
#endif // XDEBUG

  // Random Modes, I/O Setup
  if (mode > 0) {
    pinMode(2, OUTPUT);           // m2090In1
    pinMode(3, OUTPUT);           // m2090In2
    pinMode(4, OUTPUT);           // m2090In3
    pinMode(5, OUTPUT);           // m2090In4
    pinMode(6, INPUT);            // m2090Out3
    pinMode(7, INPUT);            // m2090Out4
    pinMode(8, INPUT_PULLUP);     // taste
    randomSeed(analogRead(A0));
  }
}

void loop() {

  // Part 1 GPIO Extender via Python Script
  if (mode == 0) {
    if (Serial.available() > 0) {
      char data = Serial.read();

      // --- SERVO COMMANDS ---
      if (data == 'A') { // Attach Servo
        while (!Serial.available());
        int pin = Serial.read() - '0';
        int idx = get_servo_index(pin);
        if (idx != -1 && !servo_attached[idx]) {
            servos[idx].attach(pin);
            servo_attached[idx] = true;
        }
      }
      else if (data == 'B') { // Servo auf Winkel stellen
        while (Serial.available() < 2); // Warten auf Pin und mindestens 1 Ziffer
        int pin = Serial.read() - '0';
        int idx = get_servo_index(pin);
        delay(2);
        char winkel_str[4] = {0};

        int i = 0;
        // Bis zu 3 Ziffern für Winkel einlesen (z.B. 180)
        while (i < 3 && Serial.available()) {
            char c = Serial.peek();
            if (c >= '0' && c <= '9') {
              winkel_str[i++] = Serial.read();
            } else {
              break;
            }
        }
        int winkel = atoi(winkel_str);

        if (idx != -1 && servo_attached[idx]) {
            servos[idx].write(winkel);
        }
      }
      else if (data == 'C') { // Detach Servo
        while (!Serial.available());
        int pin = Serial.read() - '0';
        int idx = get_servo_index(pin);
        if (idx != -1 && servo_attached[idx]) {
            servos[idx].detach();
            servo_attached[idx] = false;
        }
      }
      // --- END SERVO COMMANDS ---

      else if (data == 'a') {
        pinMode(2, INPUT);
      } else if (data == 'b') {
        pinMode(3, INPUT);
      } else if (data == 'c') {
        pinMode(4, INPUT);
      } else if (data == 'd') {
        pinMode(5, INPUT);
      } else if (data == 'e') {
        pinMode(6, INPUT);
      } else if (data == 'f') {
        pinMode(7, INPUT);
      } else if (data == 'g') {
        pinMode(8, INPUT);
      } else if (data == 'h') {
        pinMode(9, INPUT);
      } else if (data == 'i') {
        pinMode(10, INPUT);
      } else if (data == 'j') {
        pinMode(11, INPUT);
      } else if (data == 'N') {
        pinMode(12, INPUT);
      } else if (data == 'I') {
        pinMode(13, INPUT);
      }

      else if (data == 'k') {
        pinMode(2, OUTPUT);
      } else if (data == 'l') {
        pinMode(3, OUTPUT);
      } else if (data == 'm') {
        pinMode(4, OUTPUT);
      } else if (data == 'n') {
        pinMode(5, OUTPUT);
      } else if (data == 'o') {
        pinMode(6, OUTPUT);
      } else if (data == 'p') {
        pinMode(7, OUTPUT);
      } else if (data == 'q') {
        pinMode(8, OUTPUT);
      } else if (data == 'r') {
        pinMode(9, OUTPUT);
      } else if (data == 's') {
        pinMode(10, OUTPUT);
      } else if (data == 't') {
        pinMode(11, OUTPUT);
      } else if (data == 'O') {
        pinMode(12, OUTPUT);
      } else if (data == 'L') {
        pinMode(13, OUTPUT);
      }

      else if (data == 'u') {
        digitalWrite(2, HIGH);
      } else if (data == 'v') {
        digitalWrite(3, HIGH);
      } else if (data == 'w') {
        digitalWrite(4, HIGH);
      } else if (data == 'x') {
        digitalWrite(5, HIGH);
      } else if (data == 'y') {
        digitalWrite(6, HIGH);
      } else if (data == 'z') {
        digitalWrite(7, HIGH);
      } else if (data == '0') {
        digitalWrite(8, HIGH);
      } else if (data == '1') {
        digitalWrite(9, HIGH);
      } else if (data == '2') {
        digitalWrite(10, HIGH);
      } else if (data == '3') {
        digitalWrite(11, HIGH);
      } else if (data == 'P') {
        digitalWrite(12, HIGH);
      } else if (data == 'H') {
        digitalWrite(13, HIGH);
      }

      else if (data == '4') {
        digitalWrite(2, LOW);
      } else if (data == '5') {
        digitalWrite(3, LOW);
      } else if (data == '6') {
        digitalWrite(4, LOW);
      } else if (data == '7') {
        digitalWrite(5, LOW);
      } else if (data == '8') {
        digitalWrite(6, LOW);
      } else if (data == '9') {
        digitalWrite(7, LOW);
      } else if (data == '!') {
        digitalWrite(8, LOW);
      } else if (data == '@') {
        digitalWrite(9, LOW);
      } else if (data == '#') {
        digitalWrite(10, LOW);
      } else if (data == '$') {
        digitalWrite(11, LOW);
      } else if (data == 'Q') {
        digitalWrite(12, LOW);
      } else if (data == 'M') {
        digitalWrite(13, LOW);
      }

      else if (data == '%') {
        Serial.write(digitalRead(2));
      } else if (data == '^') {
        Serial.write(digitalRead(3));
      } else if (data == '&') {
        Serial.write(digitalRead(4));
      } else if (data == '*') {
        Serial.write(digitalRead(5));
      } else if (data == '(') {
        Serial.write(digitalRead(6));
      } else if (data == ')') {
        Serial.write(digitalRead(7));
      } else if (data == '-') {
        Serial.write(digitalRead(8));
      } else if (data == '=') {
        Serial.write(digitalRead(9));
      } else if (data == ',') {
        Serial.write(digitalRead(10));
      } else if (data == '.') {
        Serial.write(digitalRead(11));
      } else if (data == '.') {
        Serial.write(digitalRead(12));
      } else if (data == 'R') {
        Serial.write(digitalRead(13));
      }
    }
  }

  // Part 2 RND Generator
  else {
    switch (mode) {
      case 1:   // 1..6 Kniffel ?? Generate and Transfer without Handshake
        z = random(1,7);
#ifdef  XDEBUG
        Serial.print("RND Value: ");
        Serial.println(z);
#endif // XDEBUG
        setOutputs();
      break;
      case 2:  // 0..9 Monarch
        z = random(10);
        taste = 0;
        z = 0;
        setOutputs();
  
        m2090Out3 = 0;
        m2090Out4 = 0;
        while (!(m2090Out4 || m2090Out3)) {
          m2090Out3 = digitalRead(6);
          m2090Out4 = digitalRead(7);
        }
        if (m2090Out4) {
          z = random(10);   // 0..9 Monarch
#ifdef  XDEBUG
          Serial.print("RND Value: ");
          Serial.println(z);
#endif // XDEBUG
          setOutputs();
          while (m2090Out4) {
            m2090Out4 = digitalRead(7);
          }
        }
        if (m2090Out3) {
          while (m2090Out3) {
            m2090Out3 = digitalRead(6);
            taste = digitalRead(8);
            if (!taste) {
              z = 1;
              setOutputs();
            }
          } 
        }
      break;
      case 3:  // 0..15 ???
        z = random(16);
#ifdef  XDEBUG
        Serial.print("RND Value: ");
        Serial.println(z);
#endif // XDEBUG
        setOutputs();
      break;
    }
  }
}

void setOutputs() {
  // an Ausgänge binär legen
  digitalWrite(2,z&1);
  z = z >> 1;
  digitalWrite(3,z&1);
  z = z >> 1;
  digitalWrite(4,z&1);
  z = z >> 1;
  digitalWrite(5,z&1);
}