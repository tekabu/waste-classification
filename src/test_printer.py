import time

import serial
uart = serial.Serial("/dev/serial0", baudrate=19200, timeout=3000)

uart.reset_input_buffer()
uart.reset_output_buffer()

import adafruit_thermal_printer
ThermalPrinter = adafruit_thermal_printer.get_printer_class(2.16)

printer = ThermalPrinter(uart)

# Initialize the printer.  Note this will take a few seconds for the printer
# to warm up and be ready to accept commands (hence calling it explicitly vs.
# automatically in the initializer with the default auto_warm_up=True).
printer.warm_up()

# printer.test_page()

printer.print('Hello from CircuitPython1!')
printer.feed(2)
printer.print('Hello from CircuitPython2!')
printer.feed(2)
printer.print('Hello from CircuitPython3!')
printer.feed(4)

# printer.bold = True   # Turn on bold
# printer.print('This is bold text!')
# printer.bold = False  # Turn off bold
# # Feed lines to make visible:
# printer.feed(2)

# printer.underline = adafruit_thermal_printer.UNDERLINE_THICK
# printer.size = adafruit_thermal_printer.SIZE_MEDIUM
# printer.justify = adafruit_thermal_printer.JUSTIFY_CENTER
# printer.print('Medium center!')
# # Reset back to normal printing:
# printer.underline = None
# printer.size = adafruit_thermal_printer.SIZE_SMALL
# printer.justify = adafruit_thermal_printer.JUSTIFY_LEFT
# # Feed lines to make visible:
# printer.feed(2)