

import socket

# Set the target host and port
target_host = "localhost"
target_port = 12345

# Create a socket object
client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Send some data
message = "Hello, Server!"
client.sendto(message.encode(), (target_host, target_port))

# Receive some data
data, addr = client.recvfrom(4096)

print(data.decode())
client.close()
