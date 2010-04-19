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

// game status variables
int last_button_1 = HIGH;
int last_button_2 = HIGH;
int last_button_3 = HIGH;
// serial input ring.
char ring[SIZE_OF_INPUT_RING] = "     ";


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
    int button_1 = HIGH;
    int button_2 = HIGH;
    int button_3 = HIGH;
    int send_state = false;

    /* First check for reset button press. */
    handle_reset()

    // Read the input pins.
    button_1 = digitalRead(BUTTON_1);
    if (player_1 != last_button_1) {
        last_button_1 = player_1;
        send_state = true;
    }

    button_2 = digitalRead(BUTTON_2);
    if (player_2 != last_button_2) {
        last_button_2 = player_2;
        send_state = true;
    }

    button_3 = digitalRead(BUTTON_3);
    if (player_3 != last_button_3) {
        last_button_3 = player_3;
        send_state = true;
    }

    // Transmit those button presses to the computer.
    if (send_state == true){
        send_buttons();
    }

    // Read incoming button light information from the computer.
    while (Serial.available() > 0) {
        int incoming_byte = Serial.read();
        for (int i = 0; i < (SIZE_OF_INPUT_RING - 1); i++) {
            // Shift all elements in the ring towards the head.
            ring[i] = ring[i+1];
        }
        // Store the incoming_byte as the last element in the ring.
        ring[SIZE_OF_INPUT_RING - 1] = (byte)incoming_byte;
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
        ring[0] = ' ';
        ring[1] = ' ';
    }

    /* Do nothing with the other LEDs for the moment. */
    digitalWrite(GREEN_LED, LOW);
    digitalWrite(YELLOW_LED, LOW);
    digitalWrite(RED_LED, LOW);
}

/** Print the value of a single button. */
void print_button(int button_value)
{
    if (button_value == HIGH) {
        Serial.print("1");
    } else {
        Serial.print("0");
    }
}

/** Send all information about buttons. */
void send_buttons()
{
    Serial.print("GY");
    print_button(button_1);
    print_button(button_2);
    print_button(button_3);
}

int handle_reset() {
    int val = HIGH;
    val = digitalRead(BUTTON_PANEL_RESET); // read the input pin
    if (val == LOW) {
        /* The reset button is pressed. Stop serial receiving and sending. */
        Serial.end();
    }
    while (val == LOW) {
        /* What until reset button is depressed. */
        val = digitalRead(BUTTON_PANEL_RESET);
    }
    /* Restart normal operation. */
    Serial.begin(9600);
}

