import serial
import struct
import csv
import time

# Config
PORT = '/dev/ttyUSB0'  # Update to your port
BAUD = 500000
PACKET_SIZE = 44  # 4 + (10 * 4)
HEADER = b'\xaa\xaa'

def run_logger():
    try:
        ser = serial.Serial(PORT, BAUD, timeout=1)
        print("Connected. Syncing with BNO086...")
        
        # Give the Arduino time to reset
        time.sleep(2) 
        ser.reset_input_buffer() # Throw away any garbage bootloader text

        with open("data/BAUD_500K_I2C_FREQ_100kHZ_UPDATE_FREQ_50Hz_BNO085.csv", "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["Timestamp", "QI", "QJ", "QK", "QR", "AX", "AY", "AZ", "GX", "GY", "GZ"])

            while True:
                # Synchronize with Header
                if ser.read(1) == b'\xaa':
                    if ser.read(1) == b'\xaa':
                        raw_payload = ser.read(PACKET_SIZE)
                        
                        if len(raw_payload) == PACKET_SIZE:
                            # < = Little Endian
                            # I = uint32 (Timestamp)
                            # 10f = Ten 4-byte floats
                            data = struct.unpack('<I10f', raw_payload)
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