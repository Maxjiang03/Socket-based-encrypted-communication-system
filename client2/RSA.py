import rsa
# rsa加密
def rsaEncrypt(str1, pubkey):
    # 明文编码格式
    content = str1.encode("utf-8")
    # 公钥加密
    crypto = rsa.encrypt(content, pubkey)
    return crypto

# rsa解密
def rsaDecrypt(str, pk):
    # 私钥解密
    content = rsa.decrypt(str, pk)
    con = content.decode("utf-8")
    return con

def createkey_rsa():
    (pubkey, privkey) = rsa.newkeys(512)
    return pubkey, privkey

def signature(str, private_key):
    sign = rsa.sign(str, private_key, "SHA-256")  # 使用私钥进行'sha256'签名
    return sign

def verify_sign(str, sign, public_key):
    verify = rsa.verify(str, sign, public_key)  # 使用公钥验证签名
    # print(verify)  # 签名正确则返回SHA-256
    return verify

if __name__ == "__main__":
    pubkey, privkey = createkey_rsa()
    print("公钥:\n%s\n私钥:\n%s" % (pubkey, privkey))
    str = rsaEncrypt("password", pubkey)
    print("加密后密文：\n%s" % str)
    content = rsaDecrypt(str, privkey)
    print("解密后明文：\n%s" % content)
    signature(str, privkey, pubkey)