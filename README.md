# nmea-send
Send NMEA sentences on a serial port

Give the script a port and an incomplete sentence and it will send the sentence with the
checksum appended 10 times every 100ms.

There are options to set the baud rate, number of repetitions, and sleep time.
Providing the -c option will cause the script to just print the checksum and exit.

Running the script with the -h option will print a list of options and available serial ports.

Install python (at least version 3) from here: https://www.python.org/downloads/
and the pySerial module (instructions: https://pyserial.readthedocs.io/en/latest/pyserial.html)
