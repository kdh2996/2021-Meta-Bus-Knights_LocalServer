# Python UDP server

#import sys, os
# sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

import UdpCommunications as U
import time

# test.py learning test set
#from testHandModel import send_action
#curaction = send_action


# Create UDP socket to use for sending (and receiving)
sock = U.UdpCommunications(udpIP="127.0.0.1", portTX=8000, portRX=8001,
                           enableRX=True, suppressWarnings=True)

i = 0

while True:
    # sock.SendData(curaction) : send string to other app
    sock.SendData('Sent from Python: ' + str(i))

    i += 1

    # raed data
    data = sock.ReadReceivedData()

    # if NEW data has been received since last ReadReceivedData function call
    if data != None:
        # print new received data
        print(data)

    time.sleep(1)
