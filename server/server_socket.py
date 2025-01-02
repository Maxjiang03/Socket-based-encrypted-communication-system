from socket import socket
from socket import AF_INET
from socket import SOCK_STREAM
from config import SERVER_IP,SERVER_PORT

class ServerSocket(socket):

    def __init__(self):
        # 初始化套接字
        super(ServerSocket,self).__init__(AF_INET,SOCK_STREAM)

        # 绑定IP和PORT
        self.bind((SERVER_IP,SERVER_PORT))

        # 设置为被动监听套接字
        self.listen(128)

if __name__ == '__main__':
    server = ServerSocket()
    