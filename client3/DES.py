import pyDes
import random

Des_IV = b"\x00\x00\x00\x00\x00\x00\x00\x00"

def RandomDesKey():
    SmallLetter = [chr(i) for i in range(97, 123)]
    return ''.join(random.sample(SmallLetter, 8)).encode('utf-8')

def DesEncrypt(str, Key):
    k = pyDes.des(Key, pyDes.CBC, Des_IV, pad = None, padmode = pyDes.PAD_PKCS5)
    Encrypt_Str = k.encrypt(str)
    return Encrypt_Str

def DesDecrypt(str, Key):
    k = pyDes.des(Key, pyDes.CBC, Des_IV, pad = None, padmode = pyDes.PAD_PKCS5)
    Decrypt_Str = k.decrypt(str)
    return Decrypt_Str