from socket import *
from RSA import *
from system_student import *
from DES import *
import pickle
from client_dingzhen import main
IP = '127.0.0.1'
SERVER_PORT = 1233
BUFLEN = 1024
flag = 0
#实例化一个socket对象，指明协议
dataSocket = socket(AF_INET, SOCK_STREAM)
#连接服务端socket
dataSocket.connect((IP, SERVER_PORT))
while True:
    #从终端读入用户输入的字符串
    print('--------------------------------------------------------')
    print('客户端操作：')
    print('1.getkey从服务端获得密钥')
    print('2.登录学生管理系统')
    print('3.RSA生成公私钥对，将公钥给服务端')
    print('4.获得会话密钥')
    print('5.利用会话密钥进行通信')
    print('6.退出')
    print('--------------------------------------------------------')
    toSend = input('请输入对应的序号')
    dataSocket.send(toSend.encode())
    if toSend == '5':
        main()
    elif toSend == '6':
        break
    elif toSend == '4':
        if flag == 1:
            #将bytes转换为str形式
            s_pub = dataSocket.recv(BUFLEN)
            s_pub = pickle.loads(s_pub)
            print('接收到servers的公钥：')
            print(s_pub)
            DS = dataSocket.recv(BUFLEN)
            print('DS数字签名：')
            print(DS)
            wk_en = dataSocket.recv(BUFLEN)
            print('数字信封：')
            print(wk_en)
            DE = dataSocket.recv(BUFLEN)
            print('DE：')
            print(DE)

            #签名认证
            DPK = rsaDecrypt(DE, c_priv)
            wk = DesDecrypt(wk_en, DPK)
            print(wk)

            if verify_sign(wk, DS, s_pub) == 'SHA-256':
                print('验签成功')
        else:
            print('请先进行步骤3')
    elif toSend == '3':
        #1.先生成client的RSA公私钥
        c_pub, c_priv = createkey_rsa()
        print(c_pub)
        print(c_priv)
        Message = pickle.dumps(c_pub)
        dataSocket.send(Message)
        crypt = dataSocket.recv(BUFLEN)
        cleartxt = rsaDecrypt(crypt, c_priv)
        print(cleartxt)
        flag = 1
    elif toSend == '1':

        #发送信息，也要编码为bytes
        # dataSocket.send(tmp_pub.encode())
        #等待接收服务端的消息
        recved = dataSocket.recv(BUFLEN)
        print(recved.decode())
        #如果返回的是空bytes，表示对方关闭了连接
    elif toSend == '2':
        recved = dataSocket.recv(BUFLEN)
        print(recved.decode())
        secr = input('请输入密码')
        dataSocket.send(secr.encode())
        retxt= dataSocket.recv(BUFLEN)
        retxt = retxt.decode()
        print(retxt)
        if retxt == '欢迎进入学生系统':
            main()
        else:
            print("进入学生系统失败")

    else:
        # 发送信息，也要编码为bytes
        dataSocket.send(toSend.encode())
        # 等待接收服务端的消息
        recved = dataSocket.recv(BUFLEN)
        print(recved.decode())
        # 如果返回的是空bytes，表示对方关闭了连接

    # recved = dataSocket.recv(BUFLEN)
    # print(recved)
    # if not recved:
    #     break
    # print(recved.decode())

dataSocket.close()