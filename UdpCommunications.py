class UdpCommunications():
    # Constructor
    # param udpIP: Must be string e.g. "127.0.0.1"
    # param portTX: integer number e.g. 8000. Port to transmit from i.e From Python to other application
    # param portRX: integer number e.g. 8001. Port to receive on i.e. From other application to Python
    # param enableRX: When False you may only send from Python and not receive. If set to True a thread is created to enable receiving of data
    # param suppressWarnings: Stop printing warnings if not connected to other application
    def __init__(self, udpIP, portTX, portRX, enableRX=False, suppressWarnings=True):

        import socket

        self.udpIP = udpIP
        self.udpSendPort = portTX
        self.udpRcvPort = portRX
        self.enableRX = enableRX

        # when suppressWarnings=true : warnings are suppressed
        self.suppressWarnings = suppressWarnings
        self.isDataReceived = False
        self.dataRX = None

        # Connect using UDP
        # Internet protocol, Udp(DGRAM) socket
        self.udpSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # Allows the address/port to be reused immediately instead of it being stuck in the TIME_WAIT state waiting for late packets to arrive.
        self.udpSock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.udpSock.bind((udpIP, portRX))

        # Create Receiving thread if required
        if enableRX:
            import threading
            self.rxThread = threading.Thread(
                target=self.ReadUdpThreadFunc, daemon=True)
            self.rxThread.start()

    def __del__(self):
        self.CloseSocket()

    def CloseSocket(self):
        # Function : close socket
        self.udpSock.close()

    def SendData(self, strToSend):
        # Function : send string to C#
        self.udpSock.sendto(bytes(strToSend, 'utf-8'),
                            (self.udpIP, self.udpSendPort))

    def ReceiveData(self):
        """
        Should not be called by user
        Function BLOCKS until data is returned from C#. It then attempts to convert it to string and returns on successful conversion.
        An warning/error is raised if:
            - Warning: Not connected to C# application yet. Warning can be suppressed by setting suppressWarning=True in constructor
            - Error: If data receiving procedure or conversion to string goes wrong
            - Error: If user attempts to use this without enabling RX
        :return: returns None on failure or the received string on success
        """
        # if RX is not enabled, raise error
        if not self.enableRX:
            raise ValueError(
                "Attempting to receive data without enabling this setting. Ensure this is enabled from the constructor")

        data = None
        try:
            data, _ = self.udpSock.recvfrom(1024)
            data = data.decode('utf-8')
        except WindowsError as e:
            # An error occurs if you try to receive before connecting to other application
            if e.winerror == 10054:
                if not self.suppressWarnings:
                    print("Are You connected to the other application? Connect to it!")
                else:
                    pass
            else:
                raise ValueError(
                    "Unexpected Error. Are you sure that the received data can be converted to a string")

        return data
    # Should be called from thread

    def ReadUdpThreadFunc(self):
        """
        This function should be called from a thread [Done automatically via constructor]
                (import threading -> e.g. udpReceiveThread = threading.Thread(target=self.ReadUdpNonBlocking, daemon=True))
        This function keeps looping through the BLOCKING ReceiveData function and sets self.dataRX when data is received and sets received flag
        This function runs in the background and updates class variables to read data later
        """
        # Initially nothing received
        self.isDataReceived = False

        while True:
            # Blocks (in thread) until data is returned (OR MAYBE UNTIL SOME TIMEOUT AS WELL)
            data = self.ReceiveData()

            # Populate AFTER new data is received
            self.dataRX = data

            # When it reaches here, data received is available
            self.isDataReceived = True

    # Function : read received data
    # Checks if data has been received SINCE LAST CALL, if so it returns the received string and sets flag to False (to avoid re-reading received data)
    # Data is None if nothing has been received

    def ReadReceivedData(self):

        data = None

        # if data has been received
        if self.isDataReceived:
            self.isDataReceived = False
            data = self.dataRX

            # Empty receive buffer
            self.dataRX = None
        return data
