/* ---------------------------------------------------------------------------
 * Jeopardy Buttons
 * Created by John Duksta <john@duksta.org>
 * Updated by Brandon Edens <brandon@as220.org>
 *
 --------------------------------------------------------------------------- */


/* ---------------------------------------------------------------------------
  - includes
   ---------------------------------------------------------------------------*/

#include <stdio.h>
#include <stdlib.h>


/* ---------------------------------------------------------------------------
  - defines
   ---------------------------------------------------------------------------*/

// Define Buttons and LEDS
#define BUTTON_1 2
#define BUTTON_2 4
#define BUTTON_3 6

// Button LEDs
#define BUTTON_LED_1 3
#define BUTTON_LED_2 5
#define BUTTON_LED_3 7

// Panel Reset Button
#define BUTTON_PANEL_RESET 8

// Panel LEDs
#define PANEL_LED_1 11
#define PANEL_LED_2 12
#define PANEL_LED_3 13

// Countdown LEDs
#define GREEN_LED 14
#define YELLOW_LED 15
#define RED_LED 16

// Uncomment DEBUG to 1 to get debugging output on the Serial connection
// #define DEBUG


/* ---------------------------------------------------------------------------
  - globals
   ---------------------------------------------------------------------------*/

// game status variables
int waitingForAnswer = 0;
int currentPlayer = 0;
int timeToAnswer = 20000; // Number of milliseconds players have to answer


/* ---------------------------------------------------------------------------
 - setup
 - The routine setup is called by the Arduino before main processing has begun.
 - The purpose of setup is to configure the program to use the proper pin outs,
 - initialize variables, and establish serial communication.
   ---------------------------------------------------------------------------*/
void setup()
{

   // Initialize serial connection for possible debugging
   Serial.begin(9600);

   // Initialize buttons
   pinMode(BUTTON_1, INPUT);     // sets pushbutton pins to input
   digitalWrite(BUTTON_1, HIGH); // set pullup resistor to high
   pinMode(BUTTON_2, INPUT);     // sets pushbutton pins to input
   digitalWrite(BUTTON_2, HIGH); // set pullup resistor to high
   pinMode(BUTTON_3, INPUT);     // sets pushbutton pins to input
   digitalWrite(BUTTON_3, HIGH); // set pullup resistor to high
   pinMode(BUTTON_PANEL_RESET, INPUT);     // sets pushbutton pins to input
   digitalWrite(BUTTON_PANEL_RESET, HIGH); // set pullup resistor to high

   // Initialize Button LEDs
   pinMode(BUTTON_LED_1, OUTPUT);
   pinMode(BUTTON_LED_2, OUTPUT);
   pinMode(BUTTON_LED_3, OUTPUT);
   digitalWrite(BUTTON_LED_1, LOW);
   digitalWrite(BUTTON_LED_3, LOW);
   digitalWrite(BUTTON_LED_3, LOW);

   // Initialize Player Panel LEDs
   pinMode(PANEL_LED_1, OUTPUT);
   pinMode(PANEL_LED_2, OUTPUT);
   pinMode(PANEL_LED_3, OUTPUT);
   digitalWrite(PANEL_LED_1, LOW);
   digitalWrite(PANEL_LED_2, LOW);
   digitalWrite(PANEL_LED_3, LOW);

   // Initialize Timer LEDs
   pinMode(GREEN_LED, OUTPUT);
   pinMode(YELLOW_LED, OUTPUT);
   pinMode(RED_LED, OUTPUT );
   digitalWrite(GREEN_LED, LOW);
   digitalWrite(YELLOW_LED, LOW);
   digitalWrite(RED_LED, LOW);

#ifdef DEBUG
   Serial.println("Testing LEDs");
#endif

   // Test Timer LEDs
   digitalWrite(GREEN_LED, HIGH);
   delay(250);
   digitalWrite(GREEN_LED, LOW);
   digitalWrite(YELLOW_LED, HIGH);
   delay(250);
   digitalWrite(YELLOW_LED, LOW);
   digitalWrite(RED_LED, HIGH);
   delay(250);
   digitalWrite(RED_LED, LOW);
   delay(250);

#if 0
   // Test Player Panel LEDs
   digitalWrite(PANEL_LED_1, HIGH);
   delay(250);
   digitalWrite(PANEL_LED_1, LOW);
   digitalWrite(PANEL_LED_2, HIGH);
   delay(250);
   digitalWrite(PANEL_LED_2, LOW);
   digitalWrite(PANEL_LED_3, HIGH);
   delay(250);
   digitalWrite(PANEL_LED_3, LOW);
   delay(250);

   // Test Button LEDs
   digitalWrite(BUTTON_LED_1, HIGH);
   delay(250);
   digitalWrite(BUTTON_LED_1, LOW);
   digitalWrite(BUTTON_LED_2, HIGH);
   delay(250);
   digitalWrite(BUTTON_LED_2, LOW);
   digitalWrite(BUTTON_LED_3, HIGH);
   delay(250);
   digitalWrite(BUTTON_LED_3, LOW);
   delay(250);
#endif

}

/* ---------------------------------------------------------------------------
 - loop - main loop. will document more later, if need be
   ---------------------------------------------------------------------------*/
void loop()
{

   int val = HIGH;

   val = digitalRead(BUTTON_1);   // read the input pin
   digitalWrite(BUTTON_LED_1, !val);    // sets the LED to the button's value
   digitalWrite(PANEL_LED_1, !val);    // sets the LED to the button's value
   if (val == LOW) {
       waitForAnswer(1);
   }

   val = digitalRead(BUTTON_2);   // read the input pin
   digitalWrite(BUTTON_LED_2, !val);    // sets the LED to the button's value
   digitalWrite(PANEL_LED_2, !val);    // sets the LED to the button's value
   if (val == LOW) {
       waitForAnswer(2);
   }

   val = digitalRead(BUTTON_3);   // read the input pin
   digitalWrite(BUTTON_LED_3, !val);    // sets the LED to the button's value
   digitalWrite(PANEL_LED_3, !val);    // sets the LED to the button's value
   if (val == LOW) {
       waitForAnswer(3);
   }

   digitalWrite(GREEN_LED, LOW);
   digitalWrite(YELLOW_LED, LOW);
   digitalWrite(RED_LED, LOW);

}

void waitForAnswer(int player) {

   int blinkInterval = 250; // On and off time for timer LEDs
   int i;

   // Set Current Player
   currentPlayer = player;
   Serial.print("Player ");
   Serial.print(currentPlayer);
   Serial.println(" Answering");

   // Blink green for 1/3 of timeToAnswer
#ifdef DEBUG
   Serial.println("Blinking Green");
#endif
   i = timeToAnswer / 3;
   while(i > 0) {
#ifdef DEBUG
      Serial.println(i);
#endif
      if (checkForReset() == LOW) {
          return;
      }
      digitalWrite(GREEN_LED, HIGH);
      delay(blinkInterval);
      if (checkForReset() == LOW) {
          return;
      }
      i = i - blinkInterval;
      digitalWrite(GREEN_LED, LOW);
      delay(blinkInterval);
      if (checkForReset() == LOW) {
          return;
      }
      i = i - blinkInterval;
   }

   // Blink yellow for 1/3 of timeToAnswer
#ifdef DEBUG
   Serial.println("Blinking Yellow");
#endif
   i = timeToAnswer / 3;
   while (i > 0) {
#ifdef DEBUG
      Serial.println(i);
#endif
      if (checkForReset() == LOW) {
          return;
      }
      digitalWrite(YELLOW_LED, HIGH);
      delay(blinkInterval);
      if (checkForReset() == LOW) {
          return;
      }
      i = i - blinkInterval;
      digitalWrite(YELLOW_LED, LOW);
      delay(blinkInterval);
      if (checkForReset() == LOW) {
          return;
      }
      i = i - blinkInterval;
   }


   // Blink yellow for 1/3 of timeToAnswer
#ifdef DEBUG
   Serial.println("Blinking Red");
#endif

   i = timeToAnswer / 3;
   while (i > 0) {
#ifdef DEBUG
      Serial.println(i);
#endif
      if (checkForReset() == LOW) {
          return;
      }
      digitalWrite(RED_LED, HIGH);
      delay(blinkInterval);
      if (checkForReset() == LOW) {
          return;
      }
      i = i - blinkInterval;
      digitalWrite(RED_LED, LOW);
      delay(blinkInterval);
      if (checkForReset() == LOW) {
          return;
      }
      i = i - blinkInterval;
   }

}

int checkForReset() {
    int val = HIGH;
    val = digitalRead(BUTTON_PANEL_RESET); // read the input pin
    return val;
}

