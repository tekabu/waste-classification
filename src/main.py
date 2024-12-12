from ultralytics import YOLO
import cv2
import os
from pathlib import Path
import time
import numpy as np
import threading as th
import imutils

apppath = Path(__file__)

model = YOLO(os.path.join(apppath.parent, 'models', 'best.pt'))

def classify(frame):
    results = model(frame, verbose=False, conf=0.9)
    names_dict = results[0].names
    probs = results[0].probs.data.tolist()
    prob = probs[np.argmax(probs)]

    if prob >= 0.9:
        name = names_dict[np.argmax(probs)]
        print(name, prob)
    else:
        print(names_dict)

proc = th.Thread(target=classify, args=(None,))

def main():
    cap1 = cv2.VideoCapture(0)

    cap1.set(3, 640)
    cap1.set(4, 480)

    fps = cap1.get(cv2.CAP_PROP_FPS)

    try:
        while True:
            _, frame = cap1.read()

            if _ and frame is not None:
                if proc.is_alive == False and False:
                    proc = th.Thread(target=classify, args=(frame,))
                    proc.daemon = True
                    proc.start()

            cv2.imshow(f'Camera {index+1}', frame)

            time.sleep(1 / fps)

            if cv2.waitKey(1) == ord('q'):
                break

    except KeyboardInterrupt:
        print("Keyboard Interrupt")

    cap1.release()
    cv2.destroyAllWindows()

if __name__=="__main__":
	main()
