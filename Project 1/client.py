# Client File
# Student ID: 1001173911
# Name: Ritesh Deshmukh
# Class: CSE 5344-002

import socket
import threading
import sys
from timeit import default_timer
import datetime


class Client:
    def __init__(self, a, hostname, port):
        try:
            # Initializing the socket
            self.clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_TCP)

            # Running the client listener on a thread
            self.t = threading.Thread(name='ClientThread', target=self.ClientListener)
            self.t.daemon = True
            self.message = a
            self.address = hostname
            self.port = port
            self.clientsocket.connect((self.address, self.port))
            self.initValues()
            if a == 'cdet':
                self.message = 'Client Socket details = Hostname: ' + self.Hostname + ', HostIP: ' + self.HostIP + ', TimeOut: ' + str(
                    self.TimeOut) + '\nFamily: ' + self.Family + ', Type: ' + self.Type + ', Protocol: ' + self.Protocol + ', PeerName' + str(
                    self.Peername)
            elif a == 'RTT Obtained':
                self.start = default_timer()
            self.clientsocket.send((self.message).encode())
            self.t.start()
        except socket.error as e:
            print('Exception' + str(e))

    # Generating Client details
    def initValues(self):
        self.families = self.get_constants('AF_')
        self.types = self.get_constants('SOCK_')
        self.protocols = self.get_constants('IPPROTO_')
        self.HostIP = socket.gethostbyname(socket.gethostname())
        self.Hostname = socket.gethostname()
        self.TimeOut = str(socket.getdefaulttimeout())
        self.Family = str(self.families[self.clientsocket.family])
        self.Type = str(self.types[self.clientsocket.type])
        self.Protocol = str(self.protocols[self.clientsocket.proto])
        self.Peername = self.clientsocket.getpeername()

    # Client Listener
    def ClientListener(self):
        try:
            a = self.clientsocket.recv(1024).decode()
            if 'RTT' in a:
                duration = default_timer() - self.start
                print('RTT = ' + str(duration))
                self.clientsocket.close()
            # print()
            print(str(datetime.datetime.now()) + ' : ' + a)
        except socket.error as e:
            print('Exception' + str(e))

    # Function to store various socket codes and using a dictionary to store socket details with its names
    def get_constants(self, prefix):
        return dict((getattr(socket, n), n)
                    for n in dir(socket)
                    if n.startswith(prefix)
                    )


if len(sys.argv) == 3:
    print('Client')
    print('Type "cdet" to send the Client details to Server')
    print('Type "sdet" to retrieve the Server details from server')
    print('Type "files" to see the list of files on the server')
    print('Type "req" to Request File from server')
    print('Type "rtt" to calculate the RTT')
    print('Type "quit" to Shutdown')
    while 1:
        cmd = input()
        if cmd == 'sdet':
            message = 'Server Details sent to Client'
        elif cmd == 'rtt':
            message = 'RTT Obtained'
        elif cmd == 'files':
            message = 'File list sent to Client'
        elif cmd == 'req':
            message = ('GET /' + input('Enter the File Name : '))
        elif cmd == 'cdet':
            message = 'cdet'
        elif cmd == 'quit':
            print('Client Shutdown!')
            quit()
        else:
            print('Please enter a valid input')
            message = 'invalid'
        if message != 'invalid':
            c = Client(message, sys.argv[1], int(sys.argv[2]))
else:
    print('Enter client.py/server.py with the host and port number')
    quit()
