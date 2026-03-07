#include <Wire.h>
#include "SparkFun_BNO080_Arduino_Library.h"

BNO080 imu;

#define BNO_RST 18
#define BNO_ADDR 0x4A

uint8_t update_rate = 2.5; // ms (400Hz)
uint8_t update_rate_quat = update_rate; // ms (400Hz)

// Packet size: 4 bytes (timestamp) + 4*4 bytes (quaternions) + 3*4 bytes (accel) = 32 bytes
struct DataPacket {
  uint32_t timestamp;
  float quatI, quatJ, quatK, quatReal;
  // float accelX, accelY, accelZ;
  // float gyroX, gyroY, gyroZ;
} packet;

void setup() {

  Serial.begin(1000000); // 1 Mbps

  delay(1000);

  // Hardware Reset
  pinMode(BNO_RST, OUTPUT);
  digitalWrite(BNO_RST, LOW);
  delay(600);
  digitalWrite(BNO_RST, HIGH);
  delay(600);

  Wire.begin();
  Wire.setClock(400000); // 400kHz I2C

  // Initialize (Polling mode)
  if (imu.begin(BNO_ADDR, Wire) == false) {
    delay (10); // Stop if sensor not found
  }
  
  // Enable reports at 2.5ms intervals (400Hz)
  imu.enableGameRotationVector(update_rate_quat); 
  // imu.enableAccelerometer(update_rate);
  // imu.enableGyro(update_rate);
}

void loop() {
  if (imu.dataAvailable()) {

    packet.timestamp = micros();
    packet.quatI     = imu.getQuatI();
    packet.quatJ     = imu.getQuatJ();
    packet.quatK     = imu.getQuatK();
    packet.quatReal  = imu.getQuatReal();
    // packet.accelX    = imu.getAccelX();
    // packet.accelY    = imu.getAccelY();
    // packet.accelZ    = imu.getAccelZ();
    // packet.gyroX     = imu.getGyroX();
    // packet.gyroY     = imu.getGyroY();
    // packet.gyroZ     = imu.getGyroZ();

    // Send Start-of-Frame Header

    Serial.write(0xAA);
    Serial.write(0xAA);
    
    // Send raw bytes of the struct
    Serial.write((byte*)&packet, sizeof(packet));


  }
}