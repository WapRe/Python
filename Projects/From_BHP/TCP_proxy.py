
import sys
import socket
import threading

# Hexfilter string, that contains ASCII-printable characters, or a '.' if it doesn't exist any. 
HEX_FILTER = ''.join([(len(repr(chr(i))) == 3) and chr(i) or '.' for i in range(256)])

# hexdump function, takes some input as bytes or a string, and prints a hexdump to the console.
# It will output the packet details in hexadecimal and ASCII-printable characters.
# For analysing protocols, plain text communication.. etc. 
def hexdump(src, lenght=16, show=True):
    # We pass a string to decode
    if isinstance(src, bytes):
        src = src.decode()
    
    results = list()
    for i in range(0, len(src), lenght):
        # We grab a piece of the string to dump, and assign it to the variable word
        word = str(src[i:i+lenght])

        # We use the filter created to create a printable version
        printable = word.translate(HEX_FILTER)

        # Same for a hexadecimal version
        hexa = ' '.join([f'{ord(c):02X}' for c in word])
        hexwidth = lenght*3
        # We create a new array to hold the strings, contains the hex value of the first byte, the hex value of word and its printable representation.
        results.append(f'{i:04x} {hexa:<{hexwidth}} {printable}')
    
    if show:
        for line in results:
            print(line)
        
    else: 
        return results
    
# This function provides a way for the 2 ends of the proxy will use to receive data.
def receive_from(connection):
    buffer = b""
    # buffer will acumulate responses from the socket, that we passed in to be used.
    connection.settimeout(5) # Default timeout, personalize it if need. 
    try:
        while True:
            # Loop to read response data into the buffer.
            data = connection.recv(4096)
            if not data:
                break

            buffer += data
    except Exception as e:
        pass
    # We return the buffer byte str to the caller
    return buffer

# Use this 2 functions to create any modifications we want with the requests or responses
# We can modify the packets, fuzzing content, test for auth, store it in a log, whatever.
def request_handler(buffer):
   # Perform packet modifications
    return buffer

def response_handler(buffer):
     # Perform packet modifications
    return buffer


def proxy_handler(client_socket, remote_host, remote_port, receive_first):
    # We start a TCP server, so we can connect to the remote host. 
    remote_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    remote_socket.connect((remote_host, remote_port))

    # We check that we don't need to first initiate a connection to the remote side and request data before going into the main loop
    if receive_first:
        remote_buffer = receive_from(remote_socket)    # We use the receive from function to communicate
        hexdump(remote_buffer)


    remote_buffer = response_handler(remote_buffer)
    if len(remote_buffer):
        print("[<==] Sending %d bytes to localhost." % len(remote_buffer))
        client_socket.send(remote_buffer)

# We start to hand data fromm both sides.
    while True:
        local_buffer = receive_from(client_socket)
        if len(local_buffer):
            line = print("[==>] Received %d bytes to localhost." % len(local_buffer))
            print(line)
            hexdump(local_buffer)
        
            local_buffer = request_handler(local_buffer)
            remote_socket.send(local_buffer)
            print("[==>] Sent to remote.")
    
        remote_buffer = receive_from(remote_socket)
        if len(remote_buffer):
            print("[<==] Received %d bytes from remote." % len(remote_buffer))
            hexdump(remote_buffer)

            remote_buffer = response_handler(remote_buffer)
            client_socket.send(remote_buffer)
            print("[<==] Sent to localhost. ")

# No more data, that means we close the socket
        if not len(local_buffer) or not len(remote_buffer):
            client_socket.close()
            remote_socket.close()
            print("[*] No more data. Closing connections.")
            break

def server_loop(local_host, local_port, remote_host, remote_port, receive_first):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        server.bind((local_host, local_port))
    except Exception as e:
        print('Problem on bind: %r' % e)

        print("[!!] Failed to listen on %s: %d" % (local_host, local_port))
        print("[!!] Check for other listening sockets or correct permissions.")
        sys.exit(0)
    
    print("[*] Listening on %s: %d" % (local_host, local_port))
    server.listen(5)
    
    while True: # Main loop, when a fresh connection request comes in, we hand it off to the proxy_handler in a new thread. 
        client_socket, addr = server.accept()
        # print out the local connection information
        line = "> Received incoming connection from %s:%d" % (addr[0], addr[1])
        print(line)
        # start a thread to talk to the remote host
        proxy_thread = threading.Thread(
            target=proxy_handler,
            args=(client_socket, remote_host, remote_port, receive_first)
        )
        proxy_thread.start()
    
def main():
    if len(sys.argv[1:]) != 5:
        print("Usage: ./TCP_proxy.py [localhost] [localport]", end='')
        print("[remotehost] [remoteport] [receive_first]")
        print("Exemple: ./TCP_proxy.py 127.0.0.1 9000 10.12.132.1 9000 True")
        sys.exit(0)

    local_host = sys.argv[1]
    local_port = int(sys.argv[2])
    remote_host = sys.argv[3]
    remote_port = int(sys.argv[4])
    receive_first = sys.argv[5]

    if 'True' in receive_first:
        receive_first = True
    else:
        receive_first = False
    
    server_loop(local_host, local_port, remote_host, remote_port, receive_first)

if __name__ == '__main__':
    main()