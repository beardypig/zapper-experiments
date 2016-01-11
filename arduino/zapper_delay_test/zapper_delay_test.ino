#include <TVout.h>
#include <video_gen.h>
#include <font6x8.h>

#define TRIGGER_PIN 3
#define DETECT_PIN 2
#define DELAY_TIMEOUT 50

volatile int trigger_state = LOW;
volatile int detect_state = LOW;
volatile int vblank = 0;

TVout TV;

void setup() {
  attachInterrupt(digitalPinToInterrupt(TRIGGER_PIN), trigger_handle, FALLING);
  attachInterrupt(digitalPinToInterrupt(DETECT_PIN), detect_handle, RISING);

  TV.begin(PAL, 120, 96);
  TV.clear_screen();
  TV.select_font(font6x8);
  TV.set_vbi_hook(vbi_hook_flag);
  
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
 * Set flag when vertical blank happens
 */
void vbi_hook_flag() {
  vblank = 1;
}

/*
 * Wait for veritcal blank and reset the flag
 */
inline void wait_for_vblank() {
  while (!vblank);
  vblank = 0;
}

/*
 *
 */
void loop() {
  int delay_count = 0;
  reset_state();
  TV.clear_screen();
  TV.println(0, 0, "Point the Zapper at the TV and pull the trigger");

  while (trigger_state == LOW); // wait for the trigger

  wait_for_vblank(); 
  
  // Set the screen to white for 2 frames
  TV.fill(WHITE);
  wait_for_vblank();
  wait_for_vblank();
    
  TV.clear_screen();
  
  delay_count = 2;
    
  // count the number of frames
  while (detect_state == LOW && delay_count++ < DELAY_TIMEOUT) {
    wait_for_vblank();
  }

  TV.clear_screen();
  if (detect_state == HIGH) {
    TV.print(0, 0, "Zapper triggered DETECT pin with a delay of:");
    TV.print(0, 30, delay_count);
  } else {
    TV.println(0, 0, "Zapper did not trigger the DETECT pin before timeout");
  }
  reset_state();
  while (trigger_state == LOW); // wait for the trigger
}

