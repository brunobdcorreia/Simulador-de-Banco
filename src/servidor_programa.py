import socket

class Servidor:
    def __init__(self) -> None:
        HOST = '127.0.0.1'
        PORT = 65432

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.bind((HOST, PORT))
            sock.listen()
            conn, addr = sock.accept()

            with conn:
                print("Connected by: ", addr)

                while True:
                    data = conn.recv(1024)

                    if not data:
                        break
                    conn.sendall(data)