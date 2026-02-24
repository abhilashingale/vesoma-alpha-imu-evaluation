#include <Wire.h>
#include "SparkFun_BNO080_Arduino_Library.h"

// Instantiate the two sensor objects
BNO080 imuA;
BNO080 imuB;

// Pin Definitions
#define PIN_RST_A 18
#define PIN_RST_B 3

// Accuracy threshold for logging
const uint8_t threshold = 0; 
const uint16_t update_frequency = 200; // 500Hz update rate means new data every 2ms

// Declare all variables at the start
float imuA_quatI = 0, imuA_quatJ = 0, imuA_quatK = 0, imuA_quatReal = 0, imuA_quatAccuracy = 0;
float imuA_accelX = 0, imuA_accelY = 0, imuA_accelZ = 0, imuA_accelAccuracy = 0;
float imuA_gyroX = 0, imuA_gyroY = 0, imuA_gyroZ = 0, imuA_gyroAccuracy = 0;

float imuB_quatI = 0, imuB_quatJ = 0, imuB_quatK = 0, imuB_quatReal = 0, imuB_quatAccuracy = 0;
float imuB_accelX = 0, imuB_accelY = 0, imuB_accelZ = 0, imuB_accelAccuracy = 0;
float imuB_gyroX = 0, imuB_gyroY = 0, imuB_gyroZ = 0, imuB_gyroAccuracy = 0;

bool newDataA = false; // Flag to track new data from Sensor A
bool newDataB = false; // Flag to track new data from Sensor B

const uint32_t baud_rate = 1000000; // Baud rate for serial communication

struct DataPacket {
uint32_t timestamp;
float a_quat[4];
float b_quat[4];
float a_accel[3];
float b_accel[3];
float a_gyro[3];
float b_gyro[3];
} packet;


void setup() {
  Serial.begin(baud_rate);

  while (!Serial)
  {
    delay(10);
  } 
     

  Serial.println(F("--- Dual BNO08x Polling System ---"));

  // 1. Hardware Reset Sequence to ensure clean start
  pinMode(PIN_RST_A, OUTPUT);
  pinMode(PIN_RST_B, OUTPUT);
  digitalWrite(PIN_RST_A, LOW);
  digitalWrite(PIN_RST_B, LOW);
  delay(600);
  digitalWrite(PIN_RST_A, HIGH);
  digitalWrite(PIN_RST_B, HIGH);
  delay(600); 

  // 2. I2C Initialization
  Wire.begin();
  Wire.setClock(400000); // 400kHz for stability

  // 3. Initialize Sensor A (0x4A)

  // We pass 'Wire' but NO interrupt pin to force polling mode
  Serial.print(F("STATUS: Initializing BNO085 (0x4A)... "));
  if (imuA.begin(0x4A, Wire) == false) 
  {
    Serial.println(F("STATUS: Failed. Check wiring/Address."));
  } 
  else 
  {
    imuA.enableRotationVector(1.0 / update_frequency * 1000); // Send data every 5ms
    imuA.enableAccelerometer(1.0 / update_frequency * 1000); // Send data every 5ms
    imuA.enableGyro(1.0 / update_frequency * 1000); // Send data every 5ms
    Serial.println(F("STATUS: ONLINE"));
  }

  delay(200); // Gap to prevent bus contention


  // 4. Initialize Sensor B (0x4B)
  Serial.print(F("STATUS: Initializing BNO086 (0x4B)... "));
  if (imuB.begin(0x4B, Wire) == false) 
  {
    Serial.println(F("STATUS:  Failed. Check wiring/Address."));
  } 
  else 
  {
    imuB.enableRotationVector(1.0 / update_frequency * 1000); // Send data every 5ms
    imuB.enableAccelerometer(1.0 / update_frequency * 1000); // Send data every 5ms
    imuB.enableGyro(1.0 / update_frequency * 1000); // Send data every 5ms
    Serial.println(F("STATUS: ONLINE"));
  }

  // Print CSV Header for your Python script
  Serial.println(F("Time(milliseconds), IMUA_quatI, IMUA_quatJ, IMUA_quatK, IMUA_quatReal, IMUB_quatI, IMUB_quatJ, IMUB_quatK, IMUB_quatReal, IMUA_accelX, IMUA_accelY, IMUA_accelZ, IMUB_accelX, IMUB_accelY, IMUB_accelZ, IMUA_gyroX, IMUA_gyroY, IMUA_gyroZ, IMUB_gyroX, IMUB_gyroY, IMUB_gyroZ"));
}


void loop() 
{
  bool newDataA = imuA.dataAvailable();
  bool newDataB = imuB.dataAvailable();

  if (newDataA || newDataB) {
    // Update packet with latest values
    packet.timestamp = millis();
    
    packet.a_quat[0] = imuA.getQuatI();
    packet.a_quat[1] = imuA.getQuatJ();
    packet.a_quat[2] = imuA.getQuatK();
    packet.a_quat[3] = imuA.getQuatReal();

    packet.b_quat[0] = imuB.getQuatI();
    packet.b_quat[1] = imuB.getQuatJ();
    packet.b_quat[2] = imuB.getQuatK();
    packet.b_quat[3] = imuB.getQuatReal();

    packet.a_accel[0] = imuA.getAccelX();
    packet.a_accel[1] = imuA.getAccelY();
    packet.a_accel[2] = imuA.getAccelZ();

    packet.b_accel[0] = imuB.getAccelX();
    packet.b_accel[1] = imuB.getAccelY();
    packet.b_accel[2] = imuB.getAccelZ();

    packet.a_gyro[0] = imuA.getGyroX();
    packet.a_gyro[1] = imuA.getGyroY();
    packet.a_gyro[2] = imuA.getGyroZ();

    packet.b_gyro[0] = imuB.getGyroX();
    packet.b_gyro[1] = imuB.getGyroY();
    packet.b_gyro[2] = imuB.getGyroZ();

    // 1. Send Start-of-Frame Header (0xAAAA)
    Serial.write(0xAA);
    Serial.write(0xAA);

    // 2. Send the raw bytes of the struct
    Serial.write((byte*)&packet, sizeof(packet));
  }

}


