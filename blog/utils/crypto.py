import base64
import hashlib
from uuid import uuid4
from Crypto import Random
from Crypto.Cipher import AES
from blog.constants import BLOG_CONTENT_KEY


class AESCipher(object):

    def __init__(self, key: str):
        """
        AES encryption utility.

        :param key: Encryption key to be hashed into a 32 byte phrase.
        """
        self.bs = 32
        self.key = hashlib.sha256(key.encode()).digest()

    def encrypt(self, raw: str):
        """
        Encrypt raw content with AES cipher using provided key.

        :param raw: Content to encrypt.
        :type raw: str
        """
        raw = self._pad(raw)
        iv = Random.new().read(AES.block_size)
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return base64.b64encode(iv + cipher.encrypt(raw))

    def decrypt(self, enc: str):
        """
        Decrypt encrypted content with AES cipher using provided key.

        :param raw: Encrypted content to decrypt.
        :type raw: str
        """
        enc = base64.b64decode(enc)
        iv = enc[:AES.block_size]
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return self._unpad(cipher.decrypt(enc[AES.block_size:])).decode('utf-8')

    def _pad(self, s):
        return s + (self.bs - len(s) % self.bs) * chr(self.bs - len(s) % self.bs)

    @staticmethod
    def _unpad(s):
        return s[:-ord(s[len(s)-1:])]


def hash_password(password: str):
    """
    Hashes password with a randomly generated salt value.

    :param password: Plain text password to hash.
    :type password: str
    :return: (hashed_password, salt)
    """
    salt = str(uuid4())
    hashed_password = hashlib.sha256(password + salt).hexdigest()
    return (hashed_password, salt)


def compare_passwords(hashed: str, password: str, salt: str) -> bool:
    """
    Compares hashed password for authentication.

    :param hashed: Hashed password to compare.
    :type hashed: str
    :param password: Plain text password to hash.
    :type password: str
    :param salt: Password salt.
    :type salt: str
    """
    return hashed == hashlib.sha256(password + salt).hexdigest()


def encrypt_content(content: str):
    """
    Encrypt blog post and comment content.

    :param content: Blog content to encrypt.
    :type content: str
    """
    return AESCipher(BLOG_CONTENT_KEY).encrypt(content)


def decrypt_content(content: str):
    """
    Decrypt blog post and comment content.

    :param content: Blog content to decrypt.
    :type content: str
    """
    return AESCipher(BLOG_CONTENT_KEY).encrypt(content)
