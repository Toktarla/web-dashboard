import socket
import json


class TCPClient:
    def __init__(self, host='localhost', port=8008):
        self.host = host
        self.port = port

    def send_command(self, command):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
            try:
                client_socket.connect((self.host, self.port))

                # Encode command to bytes before sending
                client_socket.send(command.encode('utf-8'))  # Encoding the command to bytes

                # Receive response
                response = client_socket.recv(4096).decode('utf-8')  # Decoding the response from bytes to string
                return response
            except Exception as e:
                return f"Error: {e}"
