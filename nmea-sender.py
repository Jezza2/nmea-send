import serial
from serial.tools import list_ports
import argparse
import time

# Get a list of available serial ports
def get_port_list():
	ports = list_ports.comports(include_links=True)
	return [p.device for p in ports ]

def get_ports_string(ports):
	return ', '.join(ports)

# Get the checksum of a bytes object as an integer
def get_checksum(sentence):
	cks = 0
	for c in sentence:
		cks ^= c
	return cks

# Get the checksum of a bytes object as a 2 nibble hex string (big endian)
def get_checksum_str(sentence):
	return f'{get_checksum(sentence):0>2X}'

available_ports = get_port_list()

parser = argparse.ArgumentParser(
		description="Send NMEA sentences on a serial port",
		epilog="Available serial ports: " + get_ports_string(available_ports))
parser.add_argument("-c", action='store_true', help="Print checksum field and exit")
parser.add_argument('-b', type=int, default=9600, help="Port baud rate (default: 9600)")
parser.add_argument('-n', type=int, default=10, help="Send sentence n times (default: 10)")
parser.add_argument('-s', type=int, default=100, help="Sleep time between sends in milliseconds")
parser.add_argument("-p", default='', help="Serial port full path")
parser.add_argument("sentence", help="NMEA sentence to send (excluding leading $, trailing * and checksum)")

args = parser.parse_args()

# Check baud rate is supported
if args.b not in serial.Serial.BAUDRATES:
	print(args.b, "is not a supported baud rate.")
	print("Supported baud rates:")
	print(serial.Serial.BAUDRATES)
	exit(1)

# Calculate checksum
cksum = get_checksum_str(args.sentence.encode('utf-8'))
if args.c:
	print(cksum)
	exit(0)

if args.p == '':
	print("Please provide a port")
	exit(1)

# Complete the sentence
message_string = '$' + args.sentence + '*' + cksum + '\r\n'
message_bytes = message_string.encode('utf-8')

# Open port and send
try:
	with serial.Serial(port=args.p, baudrate=args.b) as ser:
		for i in range(0, args.n):
			ser.write(message_bytes)
			time.sleep(args.s / 1000.0)
except serial.serialutil.SerialException as e:
	print(e)
