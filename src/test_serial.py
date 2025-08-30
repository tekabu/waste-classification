from dotenv import load_dotenv
import serial
import time
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

def main():
    wait_for_arduino_ready()
    command = input("bin:")
    print(command)

    command_with_newline = command + '\n'
    ser.write(command_with_newline.encode('utf-8'))

    wait_for_arduino_ready()
    ser.close()

if __name__ == '__main__':
    main()