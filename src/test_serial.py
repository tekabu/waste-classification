from dotenv import load_dotenv
import serial
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

if ser.isOpen():
    print("arduino open")

    try:
        while True:
            if ser.in_waiting > 0:
                responses = ser.readlines()
                ready = False
                for response in responses:
                    try:
                        response = response.decode('utf-8').strip()
                        print("response:", response)
                        if "ready" in response:
                            ready = True
                            break
                    except UnicodeDecodeError:
                        print("error decoding", response)
                if ready:
                    break
                
    except KeyboardInterrupt:
        print('keyboard interrupted')

    print("arduino ok")
    arduino_ready = True