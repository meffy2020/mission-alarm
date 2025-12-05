import serial
import threading
import time
import re
from .config import settings

# Global storage for latest sensor data
latest_sensor_data = {
    "distance": 0.0,
    "ldr": 0,
    "is_near": False,
    "is_dark": False,
    "last_updated": None
}

stop_event = threading.Event()

def parse_arduino_line(line: str):
    """
    Parses line like: "Dist(cm): 25.00   LDR: 300   Near: 0   Dark: 0"
    """
    try:
        # Using regex to extract values safely
        # Looking for patterns like "Dist(cm): <float>"
        dist_match = re.search(r"Dist\(cm\):\s*([\d\.\-]+)", line)
        ldr_match = re.search(r"LDR:\s*(\d+)", line)
        near_match = re.search(r"Near:\s*(\d+)", line)
        dark_match = re.search(r"Dark:\s*(\d+)", line)

        if dist_match and ldr_match:
            latest_sensor_data["distance"] = float(dist_match.group(1))
            latest_sensor_data["ldr"] = int(ldr_match.group(1))
            latest_sensor_data["is_near"] = bool(int(near_match.group(1))) if near_match else False
            latest_sensor_data["is_dark"] = bool(int(dark_match.group(1))) if dark_match else False
            latest_sensor_data["last_updated"] = time.time()
            # print(f"[Serial] Updated: {latest_sensor_data}") # Debug logging
    except Exception as e:
        print(f"[Serial Parse Error] Line: {line}, Error: {e}")

def read_serial_loop():
    print(f"Attempting to connect to Arduino at {settings.SERIAL_PORT}...")
    ser = None
    while not stop_event.is_set():
        try:
            if ser is None:
                ser = serial.Serial(settings.SERIAL_PORT, settings.SERIAL_BAUDRATE, timeout=1)
                print(f"Connected to Arduino on {settings.SERIAL_PORT}")
            
            if ser.in_waiting > 0:
                line = ser.readline().decode('utf-8', errors='ignore').strip()
                if line:
                    parse_arduino_line(line)
            else:
                time.sleep(0.05) # Prevent CPU hogging

        except serial.SerialException as e:
            print(f"Serial connection error: {e}. Retrying in 5s...")
            if ser:
                ser.close()
            ser = None
            time.sleep(5)
        except Exception as e:
            print(f"Unexpected serial error: {e}")
            time.sleep(1)

def start_serial_reader():
    t = threading.Thread(target=read_serial_loop, daemon=True)
    t.start()
