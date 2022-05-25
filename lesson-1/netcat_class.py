import sys
import socket
import threading

import netcat_methods

class NetCat:
    def __init__(self, args, buffer=None):
        self.args = args
        self.buffer = buffer
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    def run(self):
        if self.args.listen:
            print('Start listen...')
            self.listen()
        else:
            print('Sending...')
            self.send()

    def send(self):
        self.socket.connect((self.args.target, self.args.port))

        if self.buffer:
            self.socket.send(self.buffer)

        try:
            while True:
                recv_len = 1
                response = ''

                if recv_len:
                    data = self.socket.recv(4096)
                    recv_len = len(data)
                    response += data.decode()
                    
                    if recv_len < 4096:
                        break

            if response:
                print(f'Response {response}')
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

        print(f'Binding {self.args.target}:{self.args.port}')

        while True:
            client_socket, _ = self.socket.accept()
            client_thread = threading.Thread(
                target=self.handle,
                args=(client_socket,)
            )
            
            client_thread.start()
            

    def handle(self, client_socket):
        if self.args.execute:
            output = netcat_methods.execute(self.args.execute)
            client_socket.send(output.encode())

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

        elif self.args.command:
            cmd_buffer = b''

            while True:
                try:
                    client_socket.send(b'BHP:#>')

                    while '\n' not in cmd_buffer.decode():
                        cmd_buffer += client_socket.recv(64)
                    
                    response = netcat_methods.execute(cmd_buffer.decode())

                    if response:
                        client_socket.send(response.encode())
                    
                    cmd_buffer = b''
                except Exception as e:
                    print(f'server killed {e}')
                    self.socket.close()
                    sys.exit()