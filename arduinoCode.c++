#include <Serial.h>

Serial.begin(9600);

void loop() {
    if (Serial.available()) {
        int receivedMoney = Serial.parseInt();
        // Use the receivedMoney value in your Arduino project
    }

    // ... rest of your Arduino code ...
}
