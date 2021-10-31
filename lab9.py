import random
import base64
from math import gcd
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from base64 import b64encode, b64decode

BYTES_QUANTITY = 16


def primesInRange(x, y):
    prime_list = []
    for n in range(x, y):
        isPrime = all(n % num != 0 for num in range(2, n))
        if isPrime:
            prime_list.append(n)
    return prime_list


def xgcd(a, b):
    if b == 0:
        return 0, 1, 0
    u0 = 1
    u1 = 0
    v0 = 0
    v1 = 1
    while b != 0:
        q = a//b
        r = a - b * q
        u = u0 - q * u1
        v = v0 - q * v1
        # Update a,b
        a = b
        b = r
        # Update for next iteration
        u0 = u1
        u1 = u
        v0 = v1
        v1 = v
    return a, u0, v0


def modInv(n, a):
    mcd, u, v = xgcd(n, a)
    if mcd != 1:
        print("No existe inverso")
        return 0
    return u % a


def generator(minn, maxx):
    valido = False
    p = random.choice(primesInRange(minn, maxx))
    q = random.choice(primesInRange(minn, maxx))
    while p == q:
        p = random.choice(primesInRange(minn, maxx))
        q = random.choice(primesInRange(minn, maxx))
    N = p*q
    e = random.randint(2, N) % N
    phi = N - p - q + 1
    while (
        (e % N) == 1
        and (e % N) == ((N - 1) % N)
        and gcd(e, phi) > 1
        and not valido
    ):
        e = random.randint(2, N) % N
    d = modInv(e, phi)
    publicKey = base64.b64encode(
        (str(e) + '.' + str(N)).encode('ascii')).decode('ascii')
    privateKey = base64.b64encode(
        (str(d) + '.' + str(N)).encode('ascii')).decode('ascii')
    return publicKey, privateKey


def encrypt(message: bytes, key: bytes, mode=AES.MODE_CBC):
    cipher = AES.new(key, mode)
    encrypted_bytes: bytes = cipher.encrypt(pad(message, BYTES_QUANTITY))
    with open('CypherMessage.txt') as keys:
        keys.writelines(encrypted_bytes)
        keys.writelines(cipher.iv)
    return encrypted_bytes, cipher.iv


def decrypt(message: bytes, key: bytes, iv: bytes, mode=AES.MODE_CBC) -> bytes:
    cipher = AES.new(key, mode, iv)
    return unpad(cipher.decrypt(message), BYTES_QUANTITY)


def text_to_bytes(text: str, base64=False, encoding='utf-8') -> bytes:
    if base64:
        return b64decode(text)
    else:
        return bytes(text, encoding)


def getFromFile(pathname):
    with open(pathname) as newFile:
        return newFile.readlines()


flag = True
while flag:
    option = input(
        "--------menu -------- \n1. Generar llaves. \n2. Cifrar \n3. Descifrar \n4. salir \n")
    if option == '1':
        pubkey, privkey = generator(200, 1000)
        print("Las llaves se han guardado en el archivo Keys.txt")
    if option == '2':
        msg = input("Ingrese el mensaje a cifrar: ")
        encrypt(msg.encode('utf-8'),
                getFromFile('Keys.txt')[1].encode('utf-8'))
        print("El mensaje ha sido cifrado y guardado en encMSG.txt")
    if option == '3':
        msg, iv, y = getFromFile('CypherMessage.txt')
        decrypt(msg, y, iv)
    if option == '4':
        flag = False
