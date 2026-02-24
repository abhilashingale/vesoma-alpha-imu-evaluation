import serial
import csv
import time

# --- Configuration ---
SERIAL_PORT = '/dev/ttyACM0'  # Change to '/dev/ttyUSB0' or '/dev/ttyACM0' on Linux/Mac
BAUD_RATE = 115200      # Match this to your hardware's Serial.begin()
OUTPUT_FILE = "data/sensor_data.csv"

def run_parser():
    try:
        # Initialize serial connection
        ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
        time.sleep(2) # Give the connection a moment to settle
        print(f"Connected to {SERIAL_PORT}. Press Ctrl+C to stop.")

        # Open CSV file in append mode
        with open(OUTPUT_FILE, "a", newline="") as f:
            writer = csv.writer(f)
            
            # If the file is empty, write a header
            if f.tell() == 0:
                writer.writerow(["Timestamp", "Value1", "Value2"]) # Customize headers

            while True:
                if ser.in_waiting > 0:
                    # Read line and decode to string
                    line = ser.readline().decode('utf-8').strip()
                    
                    if line:
                        # Split data if your hardware sends "val1,val2"
                        data_points = line.split(',')
                        
                        # Add a timestamp for easier offline post-processing
                        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
                        row = [timestamp] + data_points
                        
                        writer.writerow(row)
                        f.flush()  # Force write to disk so data isn't buffered
                        print(f"Saved: {row}")

    except serial.SerialException as e:
        print(f"Error: Could not open serial port: {e}")
    except KeyboardInterrupt:
        print("\nStopping parser and saving file...")
    finally:
        if 'ser' in locals() and ser.is_open:
            ser.close()

if __name__ == "__main__":
    run_parser()