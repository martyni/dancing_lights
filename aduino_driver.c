#include <FastLED.h>

// How many leds in your strip?
#define NUM_LEDS 50
// What delay do you want between updates?
#define DELAY 4
// Which pin is the Data pin for you lights?
#define DATA_PIN 12
// Which pin is the Data pin for you lights?
#define CLOCK_PIN 13
// Do you want debug information to come out of the serial port?
#define DEBUG false
// Create the leds object
CRGB leds[NUM_LEDS];
// Create the empty input string
String inputString = "";      
// Variable 
bool stringComplete = false;  // whether the string is complete
String mode = "random";

void setup() {                                   
  // initialize serial:
  Serial.begin(9600);
  // reserve 1000 bytes for the inputString:
  inputString.reserve(1000);
  FastLED.addLeds<WS2812, DATA_PIN, RGB>(leds, NUM_LEDS);
  Serial.println("");
  pinMode(9, OUTPUT);
  digitalWrite(9, HIGH);
}

void loop() {
  // print the string when a newline arrives:
  if (stringComplete) {
    if ( isAlpha(inputString[0]) ) {
       if (inputString.indexOf("random") != -1 ) {
          inputString = randomColours();
          mode = "random";
       }
    } else {
       inputString = checkColour(inputString);
       mode = "not random";
    }
  Serial.println(inputString);  
  inputString = "";
  stringComplete = false;  
  } 
  if (mode == "random") {
     randomColours();
  }
}


/*
  SerialEvent occurs whenever a new data comes in the hardware serial RX. This
  routine is run between each time loop() runs, so using delay inside loop can
  delay response. Multiple bytes of data may be available.
*/
void serialEvent() {
  while (Serial.available()) {
    // get the new byte:
    char inChar = (char)Serial.read();
    // add it to the inputString:
    inputString += inChar;
    // if the incoming character is a newline, set a flag so the main loop can
    // do something about it:
    if (inChar == '\n') {
      stringComplete = true;
    }  
  }
}

String randomColours() {
  // create 3 random numbers with a low value, medium value and high value
  int LMH[] = {random(0,10), random(10,100), random(150,255)};
  //each colour is chosen at random from the low, medium and high values
  int colour1[] = { LMH[random(0,3)], LMH[random(0,3)], LMH[random(0,3)]};
  int colour2[] = { LMH[random(0,3)], LMH[random(0,3)], LMH[random(0,3)]};
  moveColoursToLEDS(colour1, colour2, DELAY, DEBUG);
  return  String(colour1[0]) + String(colour1[1]) + String(colour1[2]) + String(colour2[0]) + String(colour2[1]) + String(colour2[2]) + "\n";
}

String checkColour(String colour) {
  //Colour string expected to be 18 characters long.
  //Each 3 characters corresponds to a number between 000 and 255
  String red1 = colour.substring(0,3);
  String green1 = colour.substring(3, 6);
  String blue1 = colour.substring(6, 9);
  String red2 = colour.substring(9,12);
  String green2 = colour.substring(12, 15);
  String blue2 = colour.substring(15, 18);
  int coulour1[] = {red1.toInt(), green1.toInt(), blue1.toInt()};
  int coulour2[] = {red2.toInt(), green2.toInt(), blue2.toInt()};
  //Send colours to the LEDs setting the delay to 0 so they update
  //Straight away
  moveColoursToLEDS(coulour1, coulour2, 0, DEBUG);
  return  red1 + green1 + blue1 + red2 + green2 + blue2 + "\n";
}

void moveColoursToLEDS(int colour1[3], int colour2[3] ,int wait, bool debug) {

  int red1 = colour1[0];
  int green1 = colour1[1];
  int blue1 = colour1[2];
  int red2 = colour2[0];
  int green2 = colour2[1];
  int blue2 = colour2[2];  

  //work out the difference between each element of colour then 
  //divide by total number of LEDs
  int red_diff =  (red2 - red1) / NUM_LEDS;
  int green_diff =  (green2 - green1) / NUM_LEDS;
  int blue_diff =  (blue2 - blue1) / NUM_LEDS;
  // Check if the diff is 0 then set anyway to provide more dynamic differences
  // in colour
  /*
  if ( red_diff == 0 or green_diff == 0 or blue_diff == 0 ) {
    if ( red_diff == 0 ) {
       red_diff = (red2 > red1) ? +1 : -1;
    }
    if ( green_diff == 0 ) {
       green_diff = (green2 > green1) ? +1 : -1;
    }
    if ( blue_diff == 0 ) {
       blue_diff = (blue2 > blue1) ? +1 : -1;
    }
  }
  */
  if (debug) {
  //Debug serial output to show contents of every LED
    Serial.print(red1);
    Serial.print(" ");
    Serial.print(green1);
    Serial.print(" ");
    Serial.print(blue1);
    Serial.print(" ");
    Serial.print(red2);
    Serial.print(" ");
    Serial.print(green2);
    Serial.print(" ");
    Serial.print(blue2);
    Serial.println("");
  }
  for (int led = 0 ; led < NUM_LEDS  ; led += 1) {
    int green = (green_diff * led) + green1;
    int rd = (red_diff * led) + red1;
    int blue = (blue_diff * led) + blue1;
    leds[led ].red = rd;
    leds[led ].green = green;
    leds[led ].blue = blue;
    if ( wait != 0 ) {
       FastLED.show();
       delay(wait);
       if (debug) {
         String no = String (led);
         String red = String (leds[led ].red);
         String grn = String (leds[led ].green); 
         String blu = String (leds[led ].blue);
         Serial.println(no + "  :" + red + ":" + grn + ":" + blu);
       }
    }    
    FastLED.show();
  }  
}
