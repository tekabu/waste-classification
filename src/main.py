from dotenv import load_dotenv
from ultralytics import YOLO
from pathlib import Path
import threading as th
import numpy as np
import serial
import time
import cv2
import os

load_dotenv()

serial_port = os.getenv('SERIAL_PORT')
print("serial port:", serial_port)

ser = serial.Serial(port=serial_port, 
                    baudrate=9600, 
                    parity=serial.PARITY_NONE, 
                    stopbits=serial.STOPBITS_ONE, 
                    bytesize=serial.EIGHTBITS, 
                    timeout=1)

# Constants
apppath = Path(__file__)
model = YOLO(os.path.join(apppath.parent, 'models', 'best.pt'))

# Global variables
last_name = None
last_time = 0
lock = th.Lock()

def wait_for_arduino_ready():
    print("waiting arduino ready")
    try:        
        ser.flushInput()
        buffer = b''
        
        while True:
            try:
                # Read available bytes
                if ser.in_waiting > 0:
                    new_data = ser.read(ser.in_waiting)
                    buffer += new_data
                    
                    # Look for complete lines in buffer
                    while b'\n' in buffer:
                        line, buffer = buffer.split(b'\n', 1)
                        
                        try:
                            decoded_line = line.decode('utf-8').strip()
                            print(f"Received: '{decoded_line}'")
                            
                            if decoded_line == "ready":
                                print("Arduino is ready!")
                                return True
                                
                        except UnicodeDecodeError:
                            # Skip non-UTF-8 data (likely bootloader noise)
                            print(f"Skipping non-UTF-8 data: {line}")
                            continue
                            
                time.sleep(0.1)  # Small delay to prevent busy waiting
                
            except Exception as e:
                print(f"Error during reading: {e}")
                continue
        
        print("Timeout waiting for 'ready' message")
        return False
        
    except serial.SerialException as e:
        print(f"Serial connection error: {e}")
        return False

    except Exception as e:
        print(f"Unexpected error: {e}")
        return False

def send_arduino(name):
    channels = {
        'glass': 1,
        'paper': 2,
        'plastic': 3,
        'metal': 4,
    }

    command_with_newline = str(channels[name]) + '\n'
    ser.write(command_with_newline.encode('utf-8'))

    wait_for_arduino_ready()

def classify(frame):
    global last_name, last_time
    results = model(frame, verbose=False, conf=0.9)
    names_dict = results[0].names
    probs = results[0].probs.data.tolist()
    prob = probs[np.argmax(probs)]
    boxes = results[0].boxes

    if boxes is not None and len(boxes) > 0 and prob >= 0.9:
        name = names_dict[np.argmax(probs)]
        current_time = time.time()

        with lock:
            if last_name != name:
                last_name = name
                last_time = current_time
                print(f"Recognized new object {name} at {time.ctime(current_time)}")
            elif last_name == name and (current_time - last_time) >= 10:
                print(last_name)
                print(f"OK - Recognized same object {name} for 10 seconds")
                send_arduino(name)
                last_time = current_time

def main():
    wait_for_arduino_ready()

    camera = os.getenv('CAMERA')
    cap1 = cv2.VideoCapture(int(camera))

    cap1.set(3, 640)
    cap1.set(4, 480)

    fps = cap1.get(cv2.CAP_PROP_FPS)
    if not cap1.isOpened():
        print("Error: Camera not found.")
        return

    proc = None

    try:
        while True:
            ret, frame = cap1.read()

            if ret and frame is not None:
                frame = cv2.rotate(frame, cv2.ROTATE_90_CLOCKWISE)
                # if proc is None or not proc.is_alive():
                #     proc = th.Thread(target=classify, args=(frame,))
                #     proc.daemon = True
                #     proc.start()
                classify(frame)

            cv2.imshow(f'Camera', frame)

            time.sleep(1 / fps)

            if cv2.waitKey(1) == ord('q'):
                break

    except KeyboardInterrupt:
        print("Keyboard Interrupt")

    finally:
        cap1.release()
        cv2.destroyAllWindows()
        print("Cleaned up resources.")

    ser.close()

if __name__ == "__main__":
    main()
