# שירות ההצפנה
class Encryptor:
    def __init__(self, key: str):
        self.key = key

    def xor_encrypt(self, data: str) -> str:
        return ''.join(chr(ord(c) ^ ord(self.key[i % len(self.key)])) for i, c in enumerate(data))
