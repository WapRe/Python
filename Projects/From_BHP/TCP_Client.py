

import socket

# Set the target host and port
target_host = '127.0.0.1'
target_port = 9998

# Create a socket object
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect the client
client.connect((target_host, target_port))

# Send some data
message = "Hello, Server!"
client.send(message.encode())

# Receive some data
response = client.recv(4096)

print(response.decode())
client.close()
