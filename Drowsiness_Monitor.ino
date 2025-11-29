#include <Wire.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>

#define SCREEN_WIDTH 128
#define SCREEN_HEIGHT 64
#define SCREEN_ADDRESS 0x3C   

Adafruit_SSD1306 display(SCREEN_WIDTH, SCREEN_HEIGHT, &Wire, -1);

const int buzzer_Pin = 8;
const int led_Pin    = 9;

char sleep_status = 'b';  

void setup() {
  Serial.begin(9600);

  pinMode(buzzer_Pin, OUTPUT);
  pinMode(led_Pin, OUTPUT);
  digitalWrite(buzzer_Pin, LOW);
  digitalWrite(led_Pin, LOW);

  if (!display.begin(SSD1306_SWITCHCAPVCC, SCREEN_ADDRESS)) {
    for (;;);  
  }

  display.clearDisplay();
  display.setTextSize(1);
  display.setTextColor(SSD1306_WHITE);
  display.setCursor(0, 0);
  display.println("Driver Sleep");
  display.setCursor(0, 16);
  display.println("Detection SYSTEM");
  display.display();
}

void loop() {
  if (Serial.available() > 0) {
    sleep_status = Serial.read();
  }

  if (sleep_status == 'a') {
    digitalWrite(buzzer_Pin, HIGH);
    digitalWrite(led_Pin, HIGH);

    display.clearDisplay();
    display.setCursor(0, 0);
    display.println("Driver Drowsiness");
    display.setCursor(0, 16);
    display.println("Detected");
    display.setCursor(0, 32);
    display.println("Please Wake Up");
    display.display();

  } else { 
    digitalWrite(buzzer_Pin, LOW);
    digitalWrite(led_Pin, LOW);

    display.clearDisplay();
    display.setCursor(0, 0);
    display.println("All Ok");
    display.setCursor(0, 16);
    display.println("Drive Safe");
    display.display();
  }

  delay(50);
}