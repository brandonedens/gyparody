/* ---------------------------------------------------------------------------
 * Jeopardy Buttons
 * Created by John Duksta <john@duksta.org>
 *
 --------------------------------------------------------------------------- */

#include <stdio.h>
#include <stdlib.h>

// Define Buttons and LEDS
#define P1BUTTON 2
#define P2BUTTON 4
#define P3BUTTON 6

// Button LEDs
#define P1LED 3
#define P2LED 5
#define P3LED 7

// Panel Reset Button
#define PRESET 8

// Panel LEDs
#define P1PLED 11
#define P2PLED 12
#define P3PLED 13

// Countdown LEDs
#define GREENLED 14
#define YELLOWLED 15
#define REDLED 16

// Uncomment DEBUG to 1 to get debugging output on the Serial connection
// #define DEBUG



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
   pinMode(P1BUTTON, INPUT ) ;     // sets pushbutton pins to input
   digitalWrite(P1BUTTON, HIGH) ;   // set pullup resistor to high
   pinMode(P2BUTTON, INPUT ) ;     // sets pushbutton pins to input
   digitalWrite(P2BUTTON, HIGH) ;   // set pullup resistor to high
   pinMode(P3BUTTON, INPUT ) ;     // sets pushbutton pins to input
   digitalWrite(P3BUTTON, HIGH) ;   // set pullup resistor to high
   pinMode(PRESET, INPUT ) ;     // sets pushbutton pins to input
   digitalWrite(PRESET, HIGH) ;   // set pullup resistor to high

   // Initialize Button LEDs
   pinMode(P1LED, OUTPUT ) ;
   pinMode(P2LED, OUTPUT ) ;
   pinMode(P3LED, OUTPUT ) ;
   digitalWrite(P1LED, LOW) ;
   digitalWrite(P3LED, LOW) ;
   digitalWrite(P3LED, LOW) ;

   // Initialize Player Panel LEDs
   pinMode(P1PLED, OUTPUT ) ;
   pinMode(P2PLED, OUTPUT ) ;
   pinMode(P3PLED, OUTPUT ) ;
   digitalWrite(P1PLED, LOW) ;
   digitalWrite(P2PLED, LOW) ;
   digitalWrite(P3PLED, LOW) ;

   // Initialize Timer LEDs
   pinMode(GREENLED, OUTPUT ) ;
   pinMode(YELLOWLED, OUTPUT ) ;
   pinMode(REDLED, OUTPUT ) ;
   digitalWrite(GREENLED, LOW) ;
   digitalWrite(YELLOWLED, LOW) ;
   digitalWrite(REDLED, LOW) ;

#ifdef DEBUG
   Serial.println("Testing LEDs");
#endif

   // Test Timer LEDs
   digitalWrite(GREENLED, HIGH);
   delay(250);
   digitalWrite(GREENLED, LOW);
   digitalWrite(YELLOWLED, HIGH);
   delay(250);
   digitalWrite(YELLOWLED, LOW);
   digitalWrite(REDLED, HIGH);
   delay(250);
   digitalWrite(REDLED, LOW);
   delay(250);

   // Test Player Panel LEDs
/*
   digitalWrite(P1PLED, HIGH);
   delay(250);
   digitalWrite(P1PLED, LOW);
   digitalWrite(P2PLED, HIGH);
   delay(250);
   digitalWrite(P2PLED, LOW);
   digitalWrite(P3PLED, HIGH);
   delay(250);
   digitalWrite(P3PLED, LOW);
   delay(250);
*/
   // Test Button LEDs
/*
   digitalWrite(P1LED, HIGH);
   delay(250);
   digitalWrite(P1LED, LOW);
   digitalWrite(P2LED, HIGH);
   delay(250);
   digitalWrite(P2LED, LOW);
   digitalWrite(P3LED, HIGH);
   delay(250);
   digitalWrite(P3LED, LOW);
   delay(250);
*/

}

/* ---------------------------------------------------------------------------
  - globals
   ---------------------------------------------------------------------------*/

// game status variables
int waitingForAnswer = 0;
int currentPlayer = 0;
int timeToAnswer = 20000; // Number of milliseconds players have to answer


/* ---------------------------------------------------------------------------
 - loop - main loop. will document more later, if need be
   ---------------------------------------------------------------------------*/
void loop()
{

   int val = HIGH;

   val = digitalRead(P1BUTTON);   // read the input pin
   digitalWrite(P1LED, !val);    // sets the LED to the button's value
   digitalWrite(P1PLED, !val);    // sets the LED to the button's value
   if (val == LOW) waitForAnswer(1);

   val = digitalRead(P2BUTTON);   // read the input pin
   digitalWrite(P2LED, !val);    // sets the LED to the button's value
   digitalWrite(P2PLED, !val);    // sets the LED to the button's value
   if (val == LOW) waitForAnswer(2);

   val = digitalRead(P3BUTTON);   // read the input pin
   digitalWrite(P3LED, !val);    // sets the LED to the button's value
   digitalWrite(P3PLED, !val);    // sets the LED to the button's value
   if (val == LOW) waitForAnswer(3);

   digitalWrite(GREENLED, LOW);
   digitalWrite(YELLOWLED, LOW);
   digitalWrite(REDLED, LOW);

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
      if (checkForReset() == LOW) return;
      digitalWrite(GREENLED, HIGH);
      delay(blinkInterval);
      if (checkForReset() == LOW) return;
      i = i - blinkInterval;
      digitalWrite(GREENLED, LOW);
      delay(blinkInterval);
      if (checkForReset() == LOW) return;
      i = i - blinkInterval;
   }

   // Blink yellow for 1/3 of timeToAnswer
   #ifdef DEBUG
   Serial.println("Blinking Yellow");
   #endif
   i = timeToAnswer / 3;
   while(i > 0) {
      #ifdef DEBUG
      Serial.println(i);
      #endif
      if (checkForReset() == LOW) return;
      digitalWrite(YELLOWLED, HIGH);
      delay(blinkInterval);
      if (checkForReset() == LOW) return;
      i = i - blinkInterval;
      digitalWrite(YELLOWLED, LOW);
      delay(blinkInterval);
      if (checkForReset() == LOW) return;
      i = i - blinkInterval;
   }


   // Blink yellow for 1/3 of timeToAnswer
   #ifdef DEBUG
   Serial.println("Blinking Red");
   #endif

   i = timeToAnswer / 3;
   while(i > 0) {
      #ifdef DEBUG
      Serial.println(i);
      #endif
      if (checkForReset() == LOW) return;
      digitalWrite(REDLED, HIGH);
      delay(blinkInterval);
      if (checkForReset() == LOW) return;
      i = i - blinkInterval;
      digitalWrite(REDLED, LOW);
      delay(blinkInterval);
      if (checkForReset() == LOW) return;
      i = i - blinkInterval;
   }

}

int checkForReset() {

   int val = HIGH;
   val = digitalRead(PRESET);   // read the input pin
   return val;


}

