# Importing the libraries that we need to replace netcat with python.
# shlex and subprocess to deal with shell-like syntax

import argparse
import socket
import shlex
import subprocess
import sys
import textwrap
import threading

def execute(cmd):
    # cmd is stripped of leading and trailing with whitespaces
    cmd = cmd.strip()
    # checking if there is any empty command, if yes, should return 'None'
    if not cmd:
        return 
    # if the command is not empty, subprocess.check_output executes the command in a specific syntax
    # shlex.split ensure that the command is in that syntax to be executed
    # stderr is used to specify that the standard output and error should be captured
    output = subprocess.check_output(shlex.split(cmd),stderr=subprocess.STDOUT)
    # After everything is captured, is then decoded from bytes to a string.
    return output.decode()


class NetCat:
    # We initialize the NetCat object with the arguments from the command line and the buffer
    def __init__(self, args, buffer = None ):
        self.args = args
        self.buffer = buffer
        # Then we create a socket object
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    def run(self):
        # Setting up the start point, defining if its a listener or a sender.
        if self.args.listen:
            self.listen()
        else:
            self.send()

    def send(self):
        self.socket.connect((self.args.target, self.args.port))
        # We connect to the target and port
        if self.buffer:
            self.socket.send(self.buffer)
        
        # this block is a try/catch block so we can interrupt the connection with CTRL + C
        try:
            while True:
                # We start a loop to receive data from the target
                recv_len = 1 
                response = ''
                while recv_len:
                    data = self.socket.recv(4096)
                    recv_len = len(data)
                    response += data.decode()
                    # If there is no more data we break the loop.
                    if recv_len < 4096:
                        break
                if response:
                    # Otherwise, we print the data received, and pause to get interactive input.
                    print(response)
                    buffer = input('> ')
                    buffer += '\n'
                    self.socket.send(buffer.encode())
    
        except KeyboardInterrupt:
            print('User terminated.')
            self.socket.close()
            sys.exit()

    def listen(self):
        self.socket.bind((self.args.target, self.args.port))
        self.socket.listen(5)

        # After beein bind to a target and a port, it starts listening in a loop. 
        while True:
            client_socket, _ = self.socket.accept()
            client_thread = threading.Thread(
                target = self.handle, args = (client_socket,)
            )
            client_thread.start()
    

    # The handle method executes the task corresponding to the command line argument it receives
    def handle(self, client_socket):
        # If a command has to be executed, the handle method passes that command to the execute function and sends back the output on the socket
        if self.args.execute:
            output = execute(self.args.execute)
            client_socket.send(output.encode())
        
        # If a file should be uploaded, we set up a loop to listen for content and receive data until there is no more.
        # Finnaly we write the accumulated content to the specified file.
        elif self.args.upload:
            file_buffer = b''
            while True:
                data = client_socket.recv(4096)
                
                if data:
                    file_buffer += data
                else:
                    break
            
            with open(self.args.upload, 'wb') as f:
                f.write(file_buffer)

            message = f'Saved file {self.args.upload}'
            client_socket.send(message.encode())
        
        # And if a shell has to be created, we set up a loop, send a prompt to the sender and wait for a command string to come back.
        # We then execute the command by using the execute function and return the output of the command to the sender.
        elif self.args.command:
            cmd_buffer = b''
            while True:
                try:
                    client_socket.send(b'BHP: #> ')
                    while '\n' not in cmd_buffer.decode():
                        cmd_buffer += client_socket.recv(64)
                    response = execute(cmd_buffer.decode())
                    if response:
                        client_socket.send(response.encode())
                    cmd_buffer = b''
                except Exception as e:
                    print(f'server killed {e}')
                    self.socket.close()
                    sys.exit()
                    

# Main block responsible for handling command line arguments and calling the rest of our functions: 

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        # We use the argparse module to create a command line interface, so it can be invoked to perform different actions. 
        description = 'BHP Net Tool',
        formatter_class = argparse.RawDescriptionHelpFormatter,
        epilog = textwrap.dedent(''' Exemple:
        netcat.py -t 192.168.1.203 -p 5555 -l -c #command shell
        netcat.py -t 192.168.1.203 -p 5555 -l -u=somefile.txt #upload to file
        netcat.py -t 192.168.1.203 -p 5555 -l -e=\"cat /etc/passwd\" #execute command
        echo 'WEA' | ./netcat2.py -t 192.168.1.203 -p 135 #echo text to server port 135
        netcat.py -t 192.168.1.203 -p 5555 #connect to the server
        '''))

# Those arguments are the reference of the command, when the user type --help
# and the reference for what are we expecting the arguments to do
parser.add_argument('-c', '--command', action = 'store_true', help = 'Command shell') # Sets up an interactive shell
parser.add_argument('-e', '--execute', help = 'Execute specified command') # Executes 1 specific command
parser.add_argument('-l', '--listen', action = 'store_true', help = 'Listen') # A listener should be set up 
parser.add_argument('-p', '--port', type = int, default ='192.168.1.203', help = 'Specified port') # Which port to communicate
parser.add_argument('-t', '--target', default ='192.168.1.203', help = 'Specified IP') # Target ip
parser.add_argument('-u', '--upload', help = 'Upload file') # Name of the file to upload

args = parser.parse_args()

# Setting it up as a listener
# We invoke the NetCat object with an empty buffer string.
if args.listen:
    buffer = ''
else:
    buffer = sys.stdin.read()
# Otherwise, we send the buffer content from stdin.
nc = NetCat(args, buffer.encode())

# Run method to start it. 
nc.run