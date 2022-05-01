import hashlib
import random
import socket
import threading

from prime_generator import generate_prime


class Client:
    def __init__(self, server_ip: str, port: int) -> None:
        self.server_ip = server_ip
        self.port = port
        self.socket = None
        self.partner_modulo = 0
        self.__generate_keys()

    def __generate_keys(self):
        ready = False
        while not ready:
            print(f"Generating keys...")
            p, q = 1, 1
            while (p - 1) % 65537 == 0:
                p = generate_prime(1024)
            while (q - 1) % 65537 == 0 or p == q:
                q = generate_prime(1024)
            self.modulo = p * q
            self.encrypt_key = 65537 % ((p - 1) * (q - 1))
            self.__set_decrypt_key((p - 1) * (q - 1))
            ready = self.check_keys()

    def __set_decrypt_key(self, modulo):
        t = 0
        new_t = 1
        rem = modulo
        new_rem = self.encrypt_key % modulo

        while new_rem != 0:
            quotient = rem // new_rem
            t, new_t = new_t, t - quotient * new_t
            rem, new_rem = new_rem, rem - quotient * new_rem

        if rem > 1:
            raise ValueError('Public keys are not relatively prime')
        if t < 0:
            t = t + modulo
        self.decrypt_key = t

    def check_keys(self):
        test_val = random.randint(2, self.modulo)
        result = self.modulo_power(test_val, self.encrypt_key, self.modulo)
        result = self.modulo_power(result, self.decrypt_key, self.modulo)
        return test_val == result

    def init_connection(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.socket.connect((self.server_ip, self.port))
        except Exception as e:
            print("[client]: could not connect to server: ", e)
            return
        print('Sending public key...')
        self.socket.send(int.to_bytes(self.modulo, byteorder='big',
                                      length=256))
        print("Waiting partner's public key...")
        self.partner_modulo = int.from_bytes(self.socket.recv(1024),
                                             byteorder='big')
        print("Key received. Ready!")
        message_handler = threading.Thread(target=self.read_handler, args=())
        message_handler.start()
        input_handler = threading.Thread(target=self.write_handler, args=())
        input_handler.start()

    def read_handler(self):
        while True:
            encrypted_text = int.from_bytes(self.socket.recv(1024),
                                            byteorder='big')

            decrypted_text = 0
            while encrypted_text:
                encrypted_text, rem = divmod(encrypted_text, self.modulo)
                block = self.modulo_power(rem, self.decrypt_key, self.modulo)
                decrypted_text *= self.modulo
                decrypted_text += block

            text = ''
            while decrypted_text:
                decrypted_text, char = divmod(decrypted_text, 256)
                text += chr(char)

            idx = text.find(':')
            if idx == -1:
                print('Corrupted unreadable message received')
            else:
                msg_hash, msg = text[:idx], text[idx + 1:]
                if msg_hash == hashlib.sha256(msg.encode()).hexdigest():
                    print(msg)
                else:
                    print(f"Corrupted: {msg}")

    def write_handler(self):
        while True:
            text = input()

            text_hash = hashlib.sha256(text.encode()).hexdigest()
            text = f'{text_hash}:{text}'
            print(text_hash)

            if not text.isascii():
                print('It supports only ascii symbols')
                continue

            decrypted_text = 0
            for char in text[::-1]:
                decrypted_text *= 256
                decrypted_text += ord(char)

            encrypted_text = 0
            while decrypted_text:
                decrypted_text, rem = divmod(decrypted_text, self.partner_modulo)
                block = self.modulo_power(rem, self.encrypt_key,
                                          self.partner_modulo)
                encrypted_text *= self.partner_modulo
                encrypted_text += block

            self.socket.send(int.to_bytes(
                encrypted_text,
                byteorder='big',
                length=1024
            ))

    @staticmethod
    def modulo_power(value, power, modulo) -> int:
        if modulo == 1:
            return 0
        else:
            ans = 1
            value %= modulo
            while power > 0:
                if power % 2 == 1:
                    ans = (ans * value) % modulo
                value = (value * value) % modulo
                power >>= 1
            return ans


if __name__ == "__main__":
    cl = Client("127.0.0.1", 9001)
    cl.init_connection()
