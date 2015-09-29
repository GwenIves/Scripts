#!/usr/bin/env python3

#
# Send periodic GPS fixes to an Android emulator
#

import socket
import time
import signal
import sys
import random

TIME_DELTA = 500
LATITUDE_DELTA = 0.0005
LONGITUDE_DELTA = 0.0005

LATITUDE_START = 40.0
LONGITUDE_START = -5.0

def main():
    def quit_emulation(_, _):
        s.close()
        sys.exit(0)

    signal.signal(signal.SIGINT, quit_emulation)

    latitude = LATITUDE_START
    longitude = LONGITUDE_START

    try:
        with socket.socket() as s:
            s.connect(("localhost", 5554))

            while True:
                latitude += LATITUDE_DELTA * random.random()

                if latitude > 90:
                    latitude = -90

                longitude += LONGITUDE_DELTA * random.random()

                if longitude > 180:
                    longitude = -180

                command = "geo fix {1} {0}\n".format(latitude, longitude)
                s.send(command.encode('ascii'))

                time.sleep(TIME_DELTA / 1000.0)
    except ConnectionError as err:
        print(err)

if __name__ == '__main__':
    main()
