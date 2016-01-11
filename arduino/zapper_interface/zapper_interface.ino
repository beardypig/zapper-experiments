#define TRIGGER_PIN 3
#define DETECT_PIN 2

volatile int trigger_state = LOW;
volatile int detect_state = LOW;

/*
 * Set the interrupts up, TRIGGER is connect to that it
 * will trigger on a falling edge, and DETECT will 
 * trigger on a rising edge. 
 */
void setup() {
  Serial.begin(9600);
  
  attachInterrupt(digitalPinToInterrupt(TRIGGER_PIN), trigger_handle, FALLING);
  attachInterrupt(digitalPinToInterrupt(DETECT_PIN), detect_handle, RISING);
  reset_state();
}

/* 
 * Latch TRIGGER state  
 */
void trigger_handle() {
  trigger_state = HIGH;
}

/* 
 * Latch DETECT state 
 */
void detect_handle() {
  detect_state = HIGH;
}

/* 
 * Reset the state of TRIGGER and DETECT 
 */
inline void reset_state() {
  trigger_state = LOW;
  detect_state = LOW;
}

/*
 * Read the state of the Zapper and reset the state
 * The state of the TRIGGER and DETECT pins are latched
 * when there is a event for TRIGGER/DETECT and only 
 * reset when the latched state is read.
 * To read the state any character can be sent to the 
 * serial port, the state will then be written back 
 * over the serial port.
 * 
 * The state is stored in a single byte
 * +----+----+----+----+----+----+---------+--------+
 * | 7  | 6  | 5  | 4  | 3  | 2  | 1       | 0      |
 * +----+----+----+----+----+----+---------+--------+
 * | NA | NA | NA | NA | NA | NA | TRIGGER | DETECT |
 * +----+----+----+----+----+----+---------+--------+
 */
void loop() {
  if (Serial.available()) {
    uint8_t in = (uint8_t)Serial.read();
    Serial.write((trigger_state<<1) | detect_state);
    reset_state();
  }
}


