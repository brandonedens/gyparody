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

// Serial port baud rate
#define SERIAL_BAUD_RATE (57600)

// Define Buttons and LEDS
#define BUTTON_1 (2)
#define BUTTON_2 (4)
#define BUTTON_3 (6)

// Button LEDs
#define BUTTON_LED_1 (3)
#define BUTTON_LED_2 (5)
#define BUTTON_LED_3 (7)

// Panel Reset Button
#define BUTTON_PANEL_RESET (8)

// Panel LEDs
#define PANEL_LED_1 (11)
#define PANEL_LED_2 (12)
#define PANEL_LED_3 (13)

// Countdown LEDs
#define GREEN_LED (14)
#define YELLOW_LED (15)
#define RED_LED (16)


// Input buffer ring size.
#define SIZE_OF_INPUT_RING (5)

// Uncomment DEBUG to 1 to get debugging output on the Serial connection
// #define DEBUG


/* ---------------------------------------------------------------------------
  - globals
   ---------------------------------------------------------------------------*/

// button states.
int button_1 = HIGH;
int button_2 = HIGH;
int button_3 = HIGH;
// previous button states.
int last_button_1 = HIGH;
int last_button_2 = HIGH;
int last_button_3 = HIGH;

// serial input ring.
char ring[SIZE_OF_INPUT_RING];


/* ---------------------------------------------------------------------------
  - local functions
   ---------------------------------------------------------------------------*/
static void print_button(int button_value);
static void send_buttons(void);
static void handle_reset(void);


/* ---------------------------------------------------------------------------
 - setup
 - The routine setup is called by the Arduino before main processing has begun.
 - The purpose of setup is to configure the program to use the proper pin outs,
 - initialize variables, and establish serial communication.
   ---------------------------------------------------------------------------*/
void setup()
{

   // Initialize serial connection for possible debugging
   Serial.begin(SERIAL_BAUD_RATE);

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
   digitalWrite(BUTTON_LED_2, LOW);
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
   pinMode(RED_LED, OUTPUT);
   digitalWrite(GREEN_LED, LOW);
   digitalWrite(YELLOW_LED, LOW);
   digitalWrite(RED_LED, LOW);

#ifdef DEBUG
   Serial.println("Testing LEDs");
#endif

   // Power on SELF TEST

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

   // Test Player Panel LEDs
   digitalWrite(PANEL_LED_1, HIGH);
   digitalWrite(PANEL_LED_2, HIGH);
   digitalWrite(PANEL_LED_3, HIGH);
   digitalWrite(BUTTON_LED_1, HIGH);
   digitalWrite(BUTTON_LED_2, HIGH);
   digitalWrite(BUTTON_LED_3, HIGH);

   delay(250);
   digitalWrite(PANEL_LED_1, LOW);
   digitalWrite(PANEL_LED_2, LOW);
   digitalWrite(PANEL_LED_3, LOW);
   digitalWrite(BUTTON_LED_1, LOW);
   digitalWrite(BUTTON_LED_2, LOW);
   digitalWrite(BUTTON_LED_3, LOW);

}

/* ---------------------------------------------------------------------------
 - loop - main loop. will document more later, if need be
   ---------------------------------------------------------------------------*/
void loop()
{
    int transmit_buttons = false;

    /* First check for reset button press. */
    handle_reset();

    // Read the input pins.
    button_1 = digitalRead(BUTTON_1);
    if (button_1 != last_button_1) {
        last_button_1 = button_1;
        transmit_buttons = true;
    }

    button_2 = digitalRead(BUTTON_2);
    if (button_2 != last_button_2) {
        last_button_2 = button_2;
        transmit_buttons = true;
    }

    button_3 = digitalRead(BUTTON_3);
    if (button_3 != last_button_3) {
        last_button_3 = button_3;
        transmit_buttons = true;
    }

    // Transmit those button presses to the computer.
    if (transmit_buttons == true){
        send_buttons();
        transmit_buttons = false;
    }

    // Read incoming button light information from the computer.
    while (Serial.available() > 0) {
        int incoming_byte = Serial.read();
        for (int i = 0; i < (SIZE_OF_INPUT_RING - 1); i++) {
            // Shift all elements in the ring towards the head.
            ring[i] = ring[i+1];
        }
        // Store the incoming_byte as the last element in the ring.
        ring[SIZE_OF_INPUT_RING - 1] = (char)incoming_byte;
    }

    /* Check ring buffer to see we have complete data. */
    if (ring[0] == 'G' && ring[1] == 'Y') {
        // We have complete serial input so light buttons if need be.
        if (ring[2] == '1') {
            digitalWrite(BUTTON_LED_1, HIGH);
            digitalWrite(PANEL_LED_1, HIGH);
        } else {
            digitalWrite(BUTTON_LED_1, LOW);
            digitalWrite(PANEL_LED_1, LOW);
        }

        if (ring[3] == '1') {
            digitalWrite(BUTTON_LED_2, HIGH);
            digitalWrite(PANEL_LED_2, HIGH);
        } else {
            digitalWrite(BUTTON_LED_2, LOW);
            digitalWrite(PANEL_LED_2, LOW);
        }

        if (ring[4] == '1') {
            digitalWrite(BUTTON_LED_3, HIGH);
            digitalWrite(PANEL_LED_3, HIGH);
        } else {
            digitalWrite(BUTTON_LED_3, LOW);
            digitalWrite(PANEL_LED_3, LOW);
        }
        /* Reset ring buffer so that button lighting is not activated again. */
        for (int i = 0; i < SIZE_OF_INPUT_RING; i++) {
            ring[i] = ' ';
        }
    }

    /* Do nothing with the other LEDs for the moment. */
    digitalWrite(GREEN_LED, HIGH);
    digitalWrite(YELLOW_LED, LOW);
    digitalWrite(RED_LED, LOW);
}

/** Print the value of a single button. */
void print_button(int button_value)
{
    if (button_value == LOW) {
        Serial.print("1");
    } else {
        Serial.print("0");
    }
}

/** Send all information about buttons. */
void send_buttons(void)
{
    Serial.print("GY");
    print_button(button_1);
    print_button(button_2);
    print_button(button_3);
}

void handle_reset(void) {
    int val = HIGH;
    val = digitalRead(BUTTON_PANEL_RESET); // read the input pin
    if (val == LOW) {
        digitalWrite(RED_LED, HIGH);
        /* The reset button is pressed. Stop serial receiving and sending. */
        Serial.end();
    }
    while (val == LOW) {
        /* What until reset button is depressed. */
        val = digitalRead(BUTTON_PANEL_RESET);
    }
    digitalWrite(RED_LED, LOW);
    /* Restart normal operation. */
    Serial.begin(SERIAL_BAUD_RATE);
}

