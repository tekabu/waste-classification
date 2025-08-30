from ultralytics import YOLO
import cv2
import os
from pathlib import Path
import time
import numpy as np
import threading as th
from adafruit_servokit import ServoKit

# Constants
apppath = Path(__file__)
model = YOLO(os.path.join(apppath.parent, 'models', 'best.pt'))
servo = ServoKit(channels=16)

# Global variables
last_name = None
last_time = 0
lock = th.Lock()

for index in range(0, 5):
    servo.servo[index].angle = 100

def activate_servo(name):
    channels = {
        'glass': 0,
        'paper': 1,
        'plastic': 2,
        'metal': 3,
    }
    servo.servo[channels.get(name, 16)].angle = 180
    time.sleep(15)
    servo.servo[channels.get(name, 16)].angle = 100

def classify(frame):
    global last_name, last_time
    results = model(frame, verbose=False, conf=0.9)
    names_dict = results[0].names
    probs = results[0].probs.data.tolist()
    prob = probs[np.argmax(probs)]

    if prob >= 0.9:
        name = names_dict[np.argmax(probs)]
        current_time = time.time()

        with lock:
            if last_name != name:
                last_name = name
                last_time = current_time
                print(f"Recognized new object: {name} at {time.ctime(current_time)}")
            elif last_name == name and (current_time - last_time) >= 10:
                print("OK - Recognized same object for 10 seconds")
                activate_servo(name)
                last_time = current_time

def main():
    cap1 = cv2.VideoCapture(0)

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
                if proc is None or not proc.is_alive():
                    proc = th.Thread(target=classify, args=(frame,))
                    proc.daemon = True
                    proc.start()

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

if __name__ == "__main__":
    main()
