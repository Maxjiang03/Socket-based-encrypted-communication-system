# Socket-based-encrypted-communication-system
Using digital envelope technology to enable multi-person chat

用户信息（users）存储格式

CREATE TABLE users (

user_id int(11) NOT NULL AUTO_INCREMENT,

user_name varchar(30) CHARACTER SET utf8 NOT NULL,

user_password varchar(30) CHARACTER SET utf8 NOT NULL,

user_nickname varchar(20) CHARACTER SET utf8 NOT NULL,

PRIMARY KEY (user_id)

) ;

插入三个用户信息，user_name用于登录，user_nickname用于通信时显示名字

insert into users values(0,'user1','111111','wang_yuan');

insert into users values(0,'user2','111111','ding_zhen');

insert into users values(0,'user3','111111','cxk');

2、密码库和图形界面库选择：

（1）对称密码算法选择：DES，库文件pyDes

Des_IV使得算法可以输入任意长度的明文和输出任意长度的密文

```
Des_IV = b"\x00\x00\x00\x00\x00\x00\x00\x00"
生成随机密钥函数：
def RandomDesKey():
     SmallLetter = [chr(i) for i in range(97, 123)]
     return ''.join(random.sample(SmallLetter, 8)).encode('utf-8')
 
Des加密函数：
def DesEncrypt(str, Key):
     k = pyDes.des(Key, pyDes.CBC, Des_IV, pad = None, padmode = pyDes.PAD_PKCS5)
     Encrypt_Str = k.encrypt(str)
     return Encrypt_Str
 
Des解密函数：
def DesDecrypt(str, Key):
     k = pyDes.des(Key, pyDes.CBC, Des_IV, pad = None, padmode = pyDes.PAD_PKCS5)
     Decrypt_Str = k.decrypt(str)
     return Decrypt_Str
```

（2）公钥密码算法和签名算法选择：RSA，库文件rsa

生成公私钥对函数：

def createkey_rsa():

   (pubkey, privkey) = rsa.newkeys(512)

   return pubkey, privkey

 

RSA加密函数：

```
def rsaEncrypt(str1, pubkey):
     # 明文编码格式
     content = str1.encode("utf-8")
     # 公钥加密
     crypto = rsa.encrypt(content, pubkey)
     return crypto
 
RSA解密函数：
def rsaDecrypt(str, pk):
     # 私钥解密
     content = rsa.decrypt(str, pk)
     con = content.decode("utf-8")
     return con
 
RSA私钥签名：
def signature(str, private_key):
     s ign = rsa.sign(str, private_key, "SHA-256")  # 使用私钥进行'sha256'签名
     return sign
RSA公钥验签：
def verify_sign(str, sign, public_key):
     verify = rsa.verify(str, sign, public_key)  # 使用公钥验证签名
     # print(verify)  # 签名正确则返回SHA-256
     return verify
```

（3）哈希算法使用sha_256

（4）图形界面库选择python自带的tkinter

Tkinter 是 Python 的标准 GUI 库（GUI：图形化用户界面，即通过鼠标对菜单、按钮等图形化元素触发指令,并从标签、对话框等图型化显示容器中获取人机对话信息。）Python 使用 Tkinter 可以快速的创建 GUI 应用程序。由于 Tkinter 是内置到 python 的安装包中、只要安装好 Python 之后就能 import Tkinter 库、而且 IDLE 也是用 Tkinter 编写而成、对于简单的图形界面 Tkinter 还是能应付自如。

3、设置基本属性：

```
# ----服务器相关配置----
SERVER_IP = '127.0.0.1'  # 服务器IP地址
SERVER_PORT = 8090  # 服务器端口
# ----数据协议相关配置----
REQUEST_LOGIN = '0001'  # 登录请求
REQUEST_CHAT = '0002'  # 聊天请求
RESPONSE_LOGIN_RESULT = '1001'  # 登录结果响应
RESPONSE_CHAT = '1002'  # 聊天响应
DELIMITER = '|'  # 自定义协议数据分隔符
 
```

\# ----数据库相关配置----

DB_HOST = '127.0.0.1' # 数据库连接地址

DB_USER = 'root' # 数据库登录用户名

DB_PASS = '6573jm65' # 数据库登录密码

DB_PORT = 3306 # 数据库端口

DB_NAME = 'mini_chat' # 数据库名

4、设计思路：

（1）客户端为三个，服务端固定一个，需要时可再增加，每个客户端对应一个文件夹，方便之后在不同计算机之间移植。

（2）服务端和客户端均分为两大模块：

servers_key用来和client_key相互配合实现相对完全的密钥安全分发过程（包括数字信封、加密、数字签名），将成功验证的密钥存储在txt文件中，方便后续通信加密的操作。

server负责连接各个客户端（client_wy)，实现接受解密和加密发送的过程。

（3）先实现密钥安全分发，再登录验证（和事先在数据库中存好的账号密码认证）
