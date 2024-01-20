import socket

class Client():
    def send_message(self, host, port, message):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.connect((host, port))
            sock.sendall(bytes(message, "utf-8"))
            response = sock.recv(2048)
            return response.decode("utf-8")