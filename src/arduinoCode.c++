#include <Serial.h>

int receivedMoney;  // Declare variable outside loop for persistence

void setup() {
  Serial.begin(9600);
}

void loop() {
  if (Serial.available()) {
    if (Serial.parseInt() > 0) {  // Check for successful parsing
      receivedMoney = Serial.parseInt();
      // Use the receivedMoney value in your Arduino project
    } else {
      // Handle parsing error
    }
  }

  // ... rest of your Arduino code ...
}
