import os
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

# klucz i wejscie
key = bytes.fromhex("000102030405060708090a0b0c0d0e0f")
data = b"ABCDEFGHIJKLMNOP" * 4
iv = os.urandom(16)


def encrypt(mode, d):
    # trzeba dodac dopelnienie
    e = Cipher(algorithms.AES(key), mode).encryptor()
    return e.update(d) + e.finalize()


def decrypt(mode, d):
    x = Cipher(algorithms.AES(key), mode).decryptor()
    return x.update(d) + x.finalize()


ecb = encrypt(modes.ECB(), data)
cbc = encrypt(modes.CBC(iv), data)

print("IV:", iv.hex())
for name, c in [("ECB", ecb), ("CBC", cbc)]:
    blocks = [c[i:i + 16] for i in range(0, len(c), 16)]
    print(f"\n{name} ({len(c)} B)")
    for i, b in enumerate(blocks):
        print(f"C[{i}] = {b.hex()}")
    pairs = [(i, j) for i in range(4) for j in range(i + 1, 4) if blocks[i] == blocks[j]]
    print("rowne bloki:", pairs if pairs else "brak")

print("\nECB odszyfrowane == wejscie:", decrypt(modes.ECB(), ecb) == data)
print("CBC odszyfrowane == wejscie:", decrypt(modes.CBC(iv), cbc) == data)