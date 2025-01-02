from socket import socket
from socket import AF_INET
from socket import SOCK_STREAM
from config import SERVER_IP
from config import SERVER_PORT

class ClientSocket(socket):

    def __init__(self):
        """初始化套接字"""
        super(ClientSocket,self).__init__(AF_INET,SOCK_STREAM)

    def connect_server(self):
        """连接服务器"""
        self.connect((SERVER_IP,SERVER_PORT))
        # 设置当前套接字为非阻塞模式
        self.setblocking(0)

    def recv_data(self):
        """获得服务器返回数据"""
        return self.recv(512).decode("utf-8")

    def send_data(self,messages):
        """向服务器发送数据"""
        self.send(messages.encode("utf-8"))

if __name__ == '__main__':
    cs = ClientSocket()
    cs.connect_server()