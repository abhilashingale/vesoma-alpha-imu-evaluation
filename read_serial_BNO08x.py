import serial
import struct
import csv
import time
import sys

# Config
PORT = '/dev/ttyUSB0'  # Update to your port
BAUD = 1000000  # 1 Mbps for faster data transfer
PACKET_SIZE = 20  # 4 + (4 * 4)
HEADER = b'\xaa\xaa'

def run_logger():
    try:
        ser = serial.Serial(PORT, BAUD, timeout=1)
        print("Connected. Syncing with BNO08x...")
        
        # Give the Arduino time to reset
        time.sleep(2) 
        ser.reset_input_buffer() # Throw away any garbage bootloader text

        with open("data/BAUD_1M_I2C_FREQ_400kHZ_UPDATE_FREQ_400Hz_BNO085_exp_09_500us_wait_I2C_game_Rotation_vector_no_Gyro_no_Accel.csv", "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["Timestamp", "QI", "QJ", "QK", "QR"])  # Header

            while True:
                # Synchronize with Header
                if ser.read(1) == b'\xaa':
                    if ser.read(1) == b'\xaa':
                        raw_payload = ser.read(PACKET_SIZE)
                        
                        if len(raw_payload) == PACKET_SIZE:
                            # < = Little Endian
                            # I = uint32 (Timestamp)
                            # 4f = Four 4-byte floats (QI, QJ, QK, QR)
                            data = struct.unpack('<I4f', raw_payload)
                            writer.writerow(data)
                            
                            # Console update every 100 samples
                            if data[0] % 100 == 0:
                                print(f"Logged Time: {data[0]}ms | AccelX: {data[5]:.2f}")

    except Exception as e:
        print(f"Error: {e}")
    finally:
        ser.close()

if __name__ == "__main__":
    run_logger()