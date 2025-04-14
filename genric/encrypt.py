import os

from cryptography.fernet import Fernet, InvalidToken

key = os.getenv("SECRET_KEY").encode()


class PasswordCipher:
    fernet = Fernet(key=key)

    @staticmethod
    def encrypt_password(password: str) -> bytes:
        """
        The function `encrypt_password` takes a string password, encrypts it using Fernet encryption,
        and returns the encrypted password as bytes.

        :param password: The `encrypt_password` function takes a string `password` as input and encrypts
        it using the Fernet encryption algorithm. The encrypted password is then returned as bytes
        :type password: str
        :return: The function `encrypt_password` returns the encrypted password as bytes after
        encrypting the input password using the Fernet encryption algorithm.
        """
        if not isinstance(password, str):
            raise TypeError("Password must be a string")
        try:
            encrypted_password = PasswordCipher.fernet.encrypt(password.encode())
            return encrypted_password
        except Exception as e:
            raise EncryptionError("Encryption failed") from e

    @staticmethod
    def decrypt_password(encrypted_password: bytes) -> str:
        """
        The function `decrypt_password` decrypts an encrypted password using Fernet encryption and
        returns the decrypted password as a string.

        :param encrypted_password: The `decrypt_password` function takes an `encrypted_password`
        parameter, which should be a bytes object containing the encrypted password that needs to be
        decrypted. The function decrypts the password using a Fernet cipher and returns the decrypted
        password as a string
        :type encrypted_password: bytes
        :return: The `decrypt_password` function returns the decrypted password as a string if the
        decryption is successful. If an `InvalidToken` exception is raised during decryption, it raises
        a `DecryptionError` with the message "Invalid token". If any other exception occurs during
        decryption, it raises a `DecryptionError` with the message "Decryption failed".
        """
        if not isinstance(encrypted_password, bytes):
            raise TypeError("Encrypted password must be a bytes object")
        try:
            decrypted_password = PasswordCipher.fernet.decrypt(encrypted_password).decode()
            return decrypted_password
        except InvalidToken:
            raise DecryptionError("Invalid token")
        except Exception as e:
            raise DecryptionError("Decryption failed") from e


class EncryptionError(Exception):
    pass


class DecryptionError(Exception):
    pass
