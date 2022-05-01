import socket
import threading


class Server:

    def __init__(self, port: int) -> None:
        self.host = '127.0.0.1'
        self.port = port
        self.clients = []
        self.keys_lookup = {}
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def start(self):
        self.s.bind((self.host, self.port))
        self.s.listen(100)

        while True:
            conn, _ = self.s.accept()
            if len(self.clients) >= 2:
                conn.close()
                continue
            bytes_key = conn.recv(1024)
            key = int.from_bytes(bytes_key, byteorder='big')
            print(f"Someone tries to connect")
            self.keys_lookup[conn] = key
            if self.clients:
                self.clients[0][0].send(int.to_bytes(key, byteorder='big',
                                                     length=256))
                conn.send(int.to_bytes(self.clients[0][1], byteorder='big',
                                       length=256))
            self.clients.append((conn, key))
            threading.Thread(target=self.handle_client,
                             args=(conn, )).start()

    def handle_client(self, conn: socket):
        while True:
            msg = conn.recv(1024)

            for client in self.clients:
                if client[0] != conn:
                    client[0].send(msg)


if __name__ == "__main__":
    s = Server(9001)
    s.start()
