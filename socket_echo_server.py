import socket
import sys
import subprocess
import ast

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the port
server_address = ('localhost', 10000)
print >>sys.stderr, 'starting up on %s port %s' % server_address
sock.bind(server_address)


# Listen for incoming connections
sock.listen(1)

while True:
    # Wait for a connection
    print >>sys.stderr, 'waiting for a connection'
    connection, client_address = sock.accept()
    try:
        print >>sys.stderr, 'connection from', client_address

        # Receive the data in small chunks and retransmit it
        msg = ""
        while True:
            data = connection.recv(256)
            print >>sys.stderr, 'received "%s"' % data
            msg += data
            if "CLIENT_DONE_RECEIVING" in data:
                break
            if "MY_END_OF_MESSAGE_STRING" in  data:
                print >>sys.stderr, 'no more data from', client_address
                print >>sys.stderr, 'sending data back to the client: ' + msg
                msg = msg.replace("MY_END_OF_MESSAGE_STRING", "")
                p = subprocess.Popen(ast.literal_eval(msg), stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                (out, _) = p.communicate()
                print ("sendall" + out + "ENDIT")
                connection.sendall(out + "MY_END_OF_MESSAGE_STRING")
    finally:
        # Clean up the connection
        connection.close()