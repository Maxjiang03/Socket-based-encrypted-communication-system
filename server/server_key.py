import json
from socket import *
from DES import *
from system_student import *
from RSA import *
import pickle
#主机地址位0.0.0.0，表示绑定本机所有网络接口ip地址
#等待客户端来连接
IP = '0.0.0.0'
#端口号
PORT = 1233
#定义一次从socket缓存区最多读入512个字节数据
BUFLEN = 1024

#socket 是一个类，实例化一个socket对象
#参数AF_INET表示使用socket网络层使用ip协议   ，后者表示使用的TCP协议
listenSocket = socket(AF_INET, SOCK_STREAM)
#socket绑定地址和端口
listenSocket.bind((IP, PORT))
#使socket处于监听状态，等待客户端的连接请求，参数5表示最多接受5个等待连接的客户端
listenSocket.listen(5)
print(f"服务端启动成功，在{PORT}端口等待客户端连接...")
dataSocket, addr = listenSocket.accept()
print('接受一个客户端连接：', addr)


while True:
    #读取对方发送的消息
    #BUFLEN 指从接收缓存里最多读取多少个字节
    recved = dataSocket.recv(BUFLEN)
    #如果返回空bytes，表示对方关闭了连接
    if not recved:
        break

    #读取的字节数据是bytes类型，需要解码为字符串
    #可以根据什么样的数据类型进行相应的处理
    info = recved.decode()
    if info == '5':
        print('已经打开servers')

    elif info == '6':
        while True:
            en_chat = dataSocket.recv(BUFLEN)
            print('对方说：')
            re_chat = DesDecrypt(en_chat, wk)

            print(re_chat)
            if re_chat == b'exit':
                break
            chat = input('说点啥')
            chaten = DesEncrypt(chat, wk)
            dataSocket.send(chaten)

    elif info == '3':
        recv = dataSocket.recv(BUFLEN)
        recv = pickle.loads(recv)
        print('成功接收到客户端公钥')
        print(recv)
        str = 'test'
        crypt = rsaEncrypt(str, recv)
        print(crypt)
        dataSocket.send(crypt)
    elif info == '4':
        wk = RandomDesKey()
        print('生成会话密钥：')
        print(wk)
        with open('client2_key.txt', 'w') as fw:
            fw.write(wk.decode())
        # WK_hash = hash(wk)
        # print('wk的哈希值：')
        # print(WK_hash)
        s_pub, s_priv = createkey_rsa()
        #签名
        print('生成服务端公私钥对：')
        print(s_pub)
        print(s_priv)
        #将公钥转换为bytes的格式
        Message2 = pickle.dumps(s_pub)
        dataSocket.send(Message2)
        #RSA签名DS
        wk_sign = signature(wk, s_priv)
        print('会话密钥wk的签名：')
        print(wk_sign)
        dataSocket.send(wk_sign)
        #生成随机密钥E(wk)
        key = RandomDesKey()
        print('随机密钥:')
        print(key)
        # 将wk工作密钥进行DES加密
        wk_en = DesEncrypt(wk, key)
        print('加密后的wk：')
        print(wk_en)
        dataSocket.send(wk_en)
        #DE
        DE = rsaEncrypt(key.decode(), recv)
        print('加密随机密钥：')
        print(DE)
        dataSocket.send(DE)


    elif info == '1':
        # p_client = dataSocket.recv(BUFLEN)
        # p_client = p_client.decode()
        # print(p_client)
        # e_client = rsaEncrypt("password", str(p_client))
        # dataSocket.send(f'加密结果{e_client}'.encode())
        print("服务器随机生成一个工作密钥（WK）,使用DES...")
        WK1 = RandomDesKey()
        print(WK1.decode())
        dataSocket.send(f'输入操作in用密码{WK1.decode()}进入系统'.encode())

    elif info == '2':
        dataSocket.send(f'服务端接收到了信息{info}'.encode())
        if WK1 == dataSocket.recv(BUFLEN):
            dataSocket.send('欢迎进入学生系统'.encode())
        else:
            dataSocket.send('密码错误'.encode())

    else:
        print(f'收到对方的信息:{info}')
        #发送的数据类型必须是bytes，所以要编码
        dataSocket.send(f'服务端接收到了信息{info}'.encode())
dataSocket.close()
listenSocket.close()
