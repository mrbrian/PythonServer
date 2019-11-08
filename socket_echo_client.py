import socket
import sys
import shlex 
# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect the socket to the port where the server is listening
server_address = ('localhost', 10000)
print >>sys.stderr, 'connecting to %s port %s' % server_address
sock.connect(server_address)
# todo: wait until connection made
try:
    
    # Send data
    message = str(sys.argv[1:])
    print >>sys.stderr, 'sending "%s"' % message
    sock.sendall(message)
    sock.sendall("MY_END_OF_MESSAGE_STRING")

    response = ""
    while True:
        data = sock.recv(256)
        response += data
        if "MY_END_OF_MESSAGE_STRING" in data:
            response = response.replace("MY_END_OF_MESSAGE_STRING", '')
            print >>sys.stderr, 'received "%s"' % response
            sock.sendall("CLIENT_DONE_RECEIVING")
            break;

finally:
    print >>sys.stderr, 'closing socket'
    sock.close()