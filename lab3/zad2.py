import os
from cryptography.hazmat.primitives import hashes, padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

PASSWORD = "haslo123"

def derive_key(password, salt):
    kdf = PBKDF2HMAC(algorithm=hashes.SHA256(), length=32, salt=salt, iterations=200000)
    return kdf.derive(password.encode("utf-8"))

def encrypt(data, password):
    salt = os.urandom(16)
    iv = os.urandom(16)
    key = derive_key(password, salt)
    padder = padding.PKCS7(128).padder()
    padded = padder.update(data) + padder.finalize()
    e = Cipher(algorithms.AES(key), modes.CBC(iv)).encryptor()
    return salt + iv + e.update(padded) + e.finalize()

def decrypt(data, password):
    salt, iv, ct = blob[:16], blob[16:32], blob[32:]
    key = derive_key(password, salt)
    d = Cipher(algorithms.AES(key), modes.CBC(iv)).decryptor()
    padded = d.update(ct) + d.finalize()
    unpadder = padding.PKCS7(128).unpadder()
    return unpadder.update(padded) + unpadder.finalize()

with open("wiadomosc.txt", "rb") as f:
    msg = f.read()

# testy: puste dane, 16 B, wiadomosc.txt
tests = [("puste", b""), ("16 B", b"A" * 16), ("wiadomosc.txt", msg)]
for name, data in tests:
    blob = encrypt(data, PASSWORD)
    ct_len = len(blob) - 32
    assert decrypt(blob, PASSWORD) == data
    assert ct_len == (len(data) // 16 + 1) * 16
    print(f"{name}: {len(data)} B -> kryptogram {ct_len} B, OK")

# zapis do pliku i odczyt
blob = encrypt(msg, PASSWORD)
with open("wiadomosc.enc", "wb") as f:
    f.write(blob)
with open("wiadomosc.enc", "rb") as f:
    assert decrypt(f.read(), PASSWORD) == msg
print("Plik wiadomosc.enc odszyfrowany bez zmian, OK")

blob2 = encrypt(msg, PASSWORD)
print("rozna sol:", blob[:16] != blob2[:16])
print("rozne IV:", blob[16:32] != blob2[16:32])
print("rozne kryptogramy:", blob[32:] != blob2[32:])