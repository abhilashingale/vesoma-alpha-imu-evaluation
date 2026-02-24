import serial
import struct
import csv
import time

# Configuration
PORT = '/dev/ttyUSB0' 
BAUD = 1000000
PACKET_SIZE = 84 # 4 (uint32) + 20*4 (floats)
HEADER = b'\xaa\xaa'

def run_binary_logger():
    ser = serial.Serial(PORT, BAUD)
    print("Connected. Waiting for binary sync...")

    with open("data/BAUD_1M_I2C_FREQ_400kHz_ASYNC_UPDATE_BNO085_BNO086_DATA.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Timestamp", "A_QI", "A_QJ", "A_QK", "A_QR", "B_QI", "B_QJ", "B_QK", "B_QR", 
                         "A_AX", "A_AY", "A_AZ", "B_AX", "B_AY", "B_AZ", 
                         "A_GX", "A_GY", "A_GZ", "B_GX", "B_GY", "B_GZ"])

        while True:
            # Look for Header
            if ser.read(1) == b'\xaa':
                if ser.read(1) == b'\xaa':
                    # Read the full packet
                    raw_data = ser.read(PACKET_SIZE)
                    if len(raw_data) == PACKET_SIZE:
                        # Unpack: I (uint32), 20f (20 floats)
                        data = struct.unpack('<I20f', raw_data)
                        writer.writerow(data)
                        
                        # Print every 50th packet to console to save CPU
                        if data[0] % 50 == 0:
                            print(f"Sync - Time: {data[0]}ms")

if __name__ == "__main__":
    run_binary_logger()