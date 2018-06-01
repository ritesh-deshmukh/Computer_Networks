# Server File
# Student ID: 1001173911
# Name: Ritesh Deshmukh
# Class: CSE 5344-002

import socket
import threading
import sys
import datetime


class Server:
    def __init__(self, hostname, port):
        try:
            # Initializing the socket
            self.address = hostname
            self.port = port
            self.serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_TCP)
            self.serversocket.bind((self.address, self.port))
            self.serversocket.listen(5)

            # Running the server listener on a thread
            self.t = threading.Thread(name='ServerThread', target=self.ServerListener)
            self.t.daemon = True
            self.t.start()
            self.initValues()
            self.ClientDetails = 'Nothing to display'
            self.fileList = ['webpage.html', 'test.txt']
        except socket.error as e:
            self.serversocket.close()
            print('Could not open socket: ' + str(e))
            quit()

    # Generating Server Details
    def initValues(self):
        self.families = self.get_constants('AF_')
        self.types = self.get_constants('SOCK_')
        self.protocols = self.get_constants('IPPROTO_')
        self.HostIP = socket.gethostbyname(socket.gethostname())
        self.Hostname = socket.gethostname()
        self.TimeOut = str(socket.getdefaulttimeout())
        self.Family = str(self.families[self.serversocket.family])
        self.Type = str(self.types[self.serversocket.type])
        self.Protocol = str(self.protocols[self.serversocket.proto])

    # Server Listener functioning in a thread for requests from all clients
    def ServerListener(self):
        while 1:
            print('Server is Listening:')
            (clientsocket, address) = self.serversocket.accept()
            Peername = clientsocket.getpeername()
            try:
                new = clientsocket.recv(1024).decode('utf-8')
                # Sending particular message according to the client request
                if new == 'RTT Obtained':
                    clientsocket.send(('RTT').encode())
                elif 'GET' in new:
                    print('Sending File to Client')
                    filename = new.split(' /')[1].split(' ')[0]
                    if filename in self.fileList:
                        filedisplay = open("C:/Users/rites/Desktop/example/" + filename.strip()).read()
                        clientsocket.send(
                            ('HTTP/1.1 200 OK Content-Type: text/html\nFile contents:\n\n ' + filedisplay).encode())
                    else:
                        clientsocket.send(
                            "HTTP/1.0 404 Not Found\r\n" + "Content-type: text/html\r\n\r\n" + "<html><head></head><body>" + filename + " not found</body></html>\n").encode()
                elif new == 'File list sent to Client':
                    # sending list of available files to the client from the server
                    clientsocket.send((self.fileList[0] + ',' + self.fileList[1]).encode())
                elif new == 'Server Details sent to Client':
                    clientsocket.send((
                                      'Server Socket details = Hostname: ' + self.Hostname + ', HostIP: ' + self.HostIP + ', TimeOut: ' + str(
                                          self.TimeOut) + ', Family: ' + self.Family + ', Type: ' + self.Type + ', Protocol: ' + self.Protocol + ', PeerName' + str(
                                          Peername)).encode())
                elif 'Client Socket details' in new:
                    self.ClientDetails = new;
                    clientsocket.send(('Client details sent to Server').encode())
                # Details of client
                print('Client details ' + address[0] + ':' + str(address[1]))
                # printing the message received from client
                print(new)
                clientsocket.close()
            except socket.error as e:
                print('Socket Exception' + str(e))
                clientsocket.close()
            except IOError as e:
                clientsocket.send(
                    "HTTP/1.0 404 Not Found\r\n" + "Content-type: text/html\r\n\r\n" + "<html><head></head><body>" + filename + " not found</body></html>\n")
                print('I/O error({0}): {1}'.format(e.errno, e.strerror))
                clientsocket.close()
            except:
                print("Unexpected error:", sys.exc_info()[0])
                clientsocket.close()

    # Function to store various socket codes and using a dictionary to store socket details with its names
    def get_constants(self, prefix):
        return dict((getattr(socket, n), n)
                    for n in dir(socket)
                    if n.startswith(prefix)
                    )


if len(sys.argv) == 3:
    print('Server')
    print('Type "cdet" to display Client details')
    print('Type "quit" to shutdown')
    s = Server(sys.argv[1], int(sys.argv[2]))
    while 1:
        cmd = input()
        if cmd == 'cdet':
            print(s.ClientDetails)
        elif cmd == 'quit':
            print('Server Shutdown!')
            s.serversocket.close()
            quit()
else:
    print('Enter client.py/server.py with the desired host and port number')
    quit()
