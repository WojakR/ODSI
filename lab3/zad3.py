import math
import string
from collections import Counter
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

def decrypt_ecb(key, data):
    d = Cipher(algorithms.AES(key), modes.ECB()).decryptor()
    return d.update(data) + d.finalize()

def entropy(data):
    n = len(data)
    return -sum(c / n * math.log2(c / n) for c in Counter(data).values())


with open("slaby_ecb.bin", "rb") as f:
    ct = f.read()

sample = ct[:4096]
results = []
for ch in string.ascii_lowercase + string.digits:
    key = (ch * 16).encode()
    results.append((entropy(decrypt_ecb(key, sample)), ch))

results.sort()
print("top 5:")
for h, ch in results[:5]:
    print(f"{ch}: {h:.4f}")

best = results[0][1]
pt = decrypt_ecb((best * 16).encode(), ct)
unpadder = padding.PKCS7(128).unpadder()
pt = unpadder.update(pt) + unpadder.finalize()
text = pt.decode("utf-8")
print("klucz:", best)
print("pierwszy wiersz:", text.splitlines()[0])
