# Socket-based-encrypted-communication-system
Using digital envelope technology to enable multi-person chat

�û���Ϣ��users���洢��ʽ

CREATE TABLE users (

user_id int(11) NOT NULL AUTO_INCREMENT,

user_name varchar(30) CHARACTER SET utf8 NOT NULL,

user_password varchar(30) CHARACTER SET utf8 NOT NULL,

user_nickname varchar(20) CHARACTER SET utf8 NOT NULL,

PRIMARY KEY (user_id)

) ;

���������û���Ϣ��user_name���ڵ�¼��user_nickname����ͨ��ʱ��ʾ����

insert into users values(0,'user1','111111','wang_yuan');

insert into users values(0,'user2','111111','ding_zhen');

insert into users values(0,'user3','111111','cxk');

2��������ͼ�ν����ѡ��

��1���Գ������㷨ѡ��DES�����ļ�pyDes

Des_IVʹ���㷨�����������ⳤ�ȵ����ĺ�������ⳤ�ȵ�����

```
Des_IV = b"\x00\x00\x00\x00\x00\x00\x00\x00"
���������Կ������
def RandomDesKey():
     SmallLetter = [chr(i) for i in range(97, 123)]
     return ''.join(random.sample(SmallLetter, 8)).encode('utf-8')
 
Des���ܺ�����
def DesEncrypt(str, Key):
     k = pyDes.des(Key, pyDes.CBC, Des_IV, pad = None, padmode = pyDes.PAD_PKCS5)
     Encrypt_Str = k.encrypt(str)
     return Encrypt_Str
 
Des���ܺ�����
def DesDecrypt(str, Key):
     k = pyDes.des(Key, pyDes.CBC, Des_IV, pad = None, padmode = pyDes.PAD_PKCS5)
     Decrypt_Str = k.decrypt(str)
     return Decrypt_Str
```

��2����Կ�����㷨��ǩ���㷨ѡ��RSA�����ļ�rsa

���ɹ�˽Կ�Ժ�����

def createkey_rsa():

   (pubkey, privkey) = rsa.newkeys(512)

   return pubkey, privkey

 

RSA���ܺ�����

```
def rsaEncrypt(str1, pubkey):
     # ���ı����ʽ
     content = str1.encode("utf-8")
     # ��Կ����
     crypto = rsa.encrypt(content, pubkey)
     return crypto
 
RSA���ܺ�����
def rsaDecrypt(str, pk):
     # ˽Կ����
     content = rsa.decrypt(str, pk)
     con = content.decode("utf-8")
     return con
 
RSA˽Կǩ����
def signature(str, private_key):
     s ign = rsa.sign(str, private_key, "SHA-256")  # ʹ��˽Կ����'sha256'ǩ��
     return sign
RSA��Կ��ǩ��
def verify_sign(str, sign, public_key):
     verify = rsa.verify(str, sign, public_key)  # ʹ�ù�Կ��֤ǩ��
     # print(verify)  # ǩ����ȷ�򷵻�SHA-256
     return verify
```

��3����ϣ�㷨ʹ��sha_256

��4��ͼ�ν����ѡ��python�Դ���tkinter

Tkinter �� Python �ı�׼ GUI �⣨GUI��ͼ�λ��û����棬��ͨ�����Բ˵�����ť��ͼ�λ�Ԫ�ش���ָ��,���ӱ�ǩ���Ի����ͼ�ͻ���ʾ�����л�ȡ�˻��Ի���Ϣ����Python ʹ�� Tkinter ���Կ��ٵĴ��� GUI Ӧ�ó������� Tkinter �����õ� python �İ�װ���С�ֻҪ��װ�� Python ֮����� import Tkinter �⡢���� IDLE Ҳ���� Tkinter ��д���ɡ����ڼ򵥵�ͼ�ν��� Tkinter ������Ӧ�����硣

3�����û������ԣ�

```
# ----�������������----
SERVER_IP = '127.0.0.1'  # ������IP��ַ
SERVER_PORT = 8090  # �������˿�
# ----����Э���������----
REQUEST_LOGIN = '0001'  # ��¼����
REQUEST_CHAT = '0002'  # ��������
RESPONSE_LOGIN_RESULT = '1001'  # ��¼�����Ӧ
RESPONSE_CHAT = '1002'  # ������Ӧ
DELIMITER = '|'  # �Զ���Э�����ݷָ���
 
```

\# ----���ݿ��������----

DB_HOST = '127.0.0.1' # ���ݿ����ӵ�ַ

DB_USER = 'root' # ���ݿ��¼�û���

DB_PASS = '6573jm65' # ���ݿ��¼����

DB_PORT = 3306 # ���ݿ�˿�

DB_NAME = 'mini_chat' # ���ݿ���

4�����˼·��

��1���ͻ���Ϊ����������˹̶�һ������Ҫʱ�������ӣ�ÿ���ͻ��˶�Ӧһ���ļ��У�����֮���ڲ�ͬ�����֮����ֲ��

��2������˺Ϳͻ��˾���Ϊ����ģ�飺

servers_key������client_key�໥���ʵ�������ȫ����Կ��ȫ�ַ����̣����������ŷ⡢���ܡ�����ǩ���������ɹ���֤����Կ�洢��txt�ļ��У��������ͨ�ż��ܵĲ�����

server�������Ӹ����ͻ��ˣ�client_wy)��ʵ�ֽ��ܽ��ܺͼ��ܷ��͵Ĺ��̡�

��3����ʵ����Կ��ȫ�ַ����ٵ�¼��֤�������������ݿ��д�õ��˺�������֤��
