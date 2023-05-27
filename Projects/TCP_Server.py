

import socket
import threading

# Set the server IP and port
bind_ip = "0.0.0.0"
bind_port = 9998

def start_server(bind_ip, bind_port):
    # Create the server socket
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((bind_ip, bind_port))

    # Start listening with a max backlog of connections set to 5
    server.listen(5)
    print(f"Listening on {bind_ip}:{bind_port}")

    while True:
        # When a client connects we receive the client socket into the client variable,
        # and the remote connection details into the addr variable
        client, addr = server.accept()
        print(f"Accepted connection from {addr[0]}:{addr[1]}")

        # Start a thread to handle incoming data from the client
        client_handler = threading.Thread(target=handle_client, args=(client,))
        client_handler.start()

def handle_client(client_socket):
    # Print out what the client sends
    request = client_socket.recv(1024)
    print(f"Received: {request.decode()}")
    
    # Send back a packet
    response = "ACK!"
    client_socket.send(response.encode())
    client_socket.close()

start_server(bind_ip, bind_port)
