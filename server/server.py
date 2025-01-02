from threading import Thread
from server_socket import ServerSocket
from socket_wrapper import SocketWrapper
from db import DB
from config import *
from response_protocol import *
from DES import *
import base64
class Server(object):
    """服务器"""

    def __init__(self):

        # 初始化套接字
        self.server_socket = ServerSocket()
        # 保存客户端连接套接字
        self.clients = dict()
        # 请求处理函数
        self.request_handle_functions = dict()
        # 注册请求处理函数
        self.register(REQUEST_LOGIN, lambda sf,data:self.request_login_handle(sf,data))
        self.register(REQUEST_CHAT,lambda sf,data:self.request_chat_handle(sf,data))

    def remove_offline_user(self, client_sock):
        """移除离线用户连接"""

        username = None
        for uname, csock in self.clients.items():
            if csock['sock'].sock == client_sock.sock:
                username = uname

        # 删除用户信息
        del self.clients[username]

    def register(self, request_id, handle_function):
        """注册请求处理函数"""

        self.request_handle_functions[request_id] = handle_function

    def startup(self):
        """启动服务器"""

        while True:
            # 等待客户端连接
            sock,addr = self.server_socket.accept()
            # 给客户端sock增加额外功能
            client_sock = SocketWrapper(sock)
            # 启动线程处理该用户请求
            Thread(target=lambda:self.request_handle(client_sock)).start()

    def request_handle(self, client_sock):
        """响应处理函数"""

        while True:
            # 读取客户端数据
            request_text = client_sock.recv_data()
            if not request_text:
                print("客户端下线!")
                self.remove_offline_user(client_sock)
                break
            # 解析请求数据
            request_data = self.parse_request_text(request_text)
            # 获取响应处理函数
            handle_function = self.request_handle_functions[request_data["request_id"]]
            if handle_function:
                handle_function(client_sock,request_data)

    def request_login_handle(self,client_sock,request_data):
        """处理用户登录"""

        # 登录用户名和密码
        username = request_data["username"]
        password = request_data["password"]

        # 查询用户名是否合法
        ret, nickname, username = self.check_user_login(username,password)
        # 如果登录成功, 则保存用户连接套接字
        if ret == "1":
            self.clients[username] = {'sock':client_sock,'nickname':nickname}
        # 组装响应结果
        response_text = ResponseProtocol.response_login_result(ret,nickname,username)
        # 发送响应结果
        client_sock.send_data(response_text)


    def check_user_login(self,username,password):
        """用户名和密码验证"""

        # 查询SQL
        sql = "select * from users where user_name='" + username + "'"
        # 创建数据库连接对象
        db_conn = DB()
        results = db_conn.get_one(sql)
        # 未查询到数据
        if not results:
            return "0","",username
        # 用户名和密码不相等
        if results['user_password'] != password:
            return "0","",username

        return "1",results["user_nickname"],username

    def request_chat_handle(self,client_sock,request_data):
        """处理用户聊天"""

        # 获得当前用户名、发送信息、昵称
        username = request_data["username"]
        messages = request_data["messages"]
        nickname = self.clients[username]["nickname"]
        # 对messages采用des解密
        with open('client2_key.txt', 'r') as fw:
            key_s = fw.read()
        if username == 'user1':
            print('原始数据：')
            print(messages)
            print('解密过程：')
            #逆过程
            messages = messages.encode()
            messages = base64.b64decode(messages)
            messages = DesDecrypt(messages, key_s)
            print('解密数据:')
            messages = str(messages)
            messages = messages[2:-1]
            print(messages)
        response_text = ResponseProtocol.response_chat(nickname,messages)
        # 将信息发送到每一个登录客户端
        for uname,csock in self.clients.items():
           # 不用给自己再发信息
            if uname == username:
                continue
            # 给其他用户发送消息
            csock["sock"].send_data(response_text)

    @staticmethod
    def parse_request_text(request_text):
        """解析请求数据"""

        request_text_list = request_text.split(DELIMITER)
        # 保存请求数据
        request_data = dict()

        request_data['request_id'] = request_text_list[0]
        if request_text_list[0] == REQUEST_LOGIN:
            request_data['username'] = request_text_list[1]
            request_data['password'] = request_text_list[2]

        if request_text_list[0] == REQUEST_CHAT:
            request_data['username'] = request_text_list[1]
            request_data['messages'] = request_text_list[2]

        return request_data


if __name__ == "__main__":
    server = Server()
    server.startup()