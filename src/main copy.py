from ultralytics import YOLO
import cv2
import os
from pathlib import Path
import time
import numpy as np
import threading as th
import imutils
from adafruit_servokit import ServoKit

apppath = Path(__file__)

model = YOLO(os.path.join(apppath.parent, 'models', 'best.pt'))

last_name = None

def classify(frame):
    results = model(frame, verbose=False, conf=0.9)
    names_dict = results[0].names
    probs = results[0].probs.data.tolist()
    prob = probs[np.argmax(probs)]

    if prob >= 0.9:
        name = names_dict[np.argmax(probs)]
        print(name, prob)

        # todo:
        # if last_name != name then save current time
        # if last_name == name and from previous time vs current time is 10 seconds then print ok
        # else set last_name = name and reset previous time to current time

def main():
    cap1 = cv2.VideoCapture(0)

    cap1.set(3, 640)
    cap1.set(4, 480)

    fps = cap1.get(cv2.CAP_PROP_FPS)

    proc = th.Thread(target=classify, args=(None,))

    try:
        while True:
            _, frame = cap1.read()

            if _ and frame is not None:
                frame = cv2.rotate(frame, cv2.ROTATE_90_CLOCKWISE)
                if proc.is_alive() == False:
                    proc = th.Thread(target=classify, args=(frame,))
                    proc.daemon = True
                    proc.start()

            cv2.imshow(f'Camera', frame)

            time.sleep(1 / fps)

            if cv2.waitKey(1) == ord('q'):
                break

    except KeyboardInterrupt:
        print("Keyboard Interrupt")

    cap1.release()
    cv2.destroyAllWindows()

if __name__=="__main__":
	main()
