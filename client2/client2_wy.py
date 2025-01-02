from tkinter.messagebox import showinfo
from threading import Thread
from time import sleep
import sys
from request_protocol import RequestProtocol
from window_login import WindowLogin
from window_chat import WindowChat
from client_socket import ClientSocket
from config import *
from DES import *
import base64
class Client(object):
    """客户端"""

    def __init__(self):
        # 创建登录窗口
        self.window = WindowLogin()
        # 创建聊天室窗口并隐藏
        self.room = WindowChat()
        self.room.withdraw()
        # 服务器连接对象
        self.conn = ClientSocket()
        # 存储响应处理函数
        self.response_handle_functions = dict()
        # 处理服务器响应线程是否正在运行
        self.is_running = True
        # 当前登录用户, 未登录之前为None
        self.username = None

        # 登录窗口按钮绑定点击处理方法
        self.window.on_reset_button_click(lambda: self.clear_inputs())
        self.window.on_login_button_click(lambda: self.send_login_data())
        self.window.on_window_closed(lambda: self.exit())

        # 聊天室窗口发送按钮绑定处理函数
        self.room.on_send_button_click(lambda:self.send_chat_data())
        self.room.on_window_closed(lambda:self.exit())

        # 注册响应处理函数
        self.register(RESPONSE_LOGIN_RESULT,lambda data:self.response_login_handle(data))
        self.register(RESPONSE_CHAT,lambda data:self.response_chat_handle(data))

    def register(self, response_id, handle_function):
        """注册响应处理函数"""

        self.response_handle_functions[response_id] = handle_function


    def exit(self):
        """退出程序"""

        self.is_running = False
        self.conn.close()
        sys.exit(0)

    def clear_inputs(self):
        """清空输入框内容"""

        self.window.clear_username()
        self.window.clear_password()

    def send_login_data(self):
        """发送登录数据到服务器"""

        # 获得用户输入内容
        username = self.window.get_username()
        passowrd = self.window.get_password()
        # 构造登录请求
        request_text = RequestProtocol.request_login(username, passowrd)
        print('发送的聊天内容:', request_text)
        # 发送请求
        self.conn.send_data(request_text)

    def send_chat_data(self):
        """发送聊天数据到服务器"""

        # 获得聊天内容
        chat_contents = self.room.get_inputs()



        # 清空输入内容
        self.room.clear_inputs()
        # 显示聊天内容
        self.room.append_message("我",chat_contents)
        # 加密聊天内容
        with open('client2_key.txt', 'r') as fw:
            key_s = fw.read()
        print('原文：')
        print(chat_contents)
        chat_en = DesEncrypt(chat_contents, key_s)
        print('密文：')
        print(chat_en)
        chat_en = base64.b64encode(chat_en)
        chat_en = chat_en.decode('utf-8')
        # 生成聊天协议内容
        request_text = RequestProtocol.request_chat(self.username, chat_en)
        print('发送给服务端的内容')
        print(request_text)
        # 向服务器端发送聊天数据
        self.conn.send_data(request_text)

    def startup(self):
        """启动客户端"""

        # 连接服务器
        self.conn.connect_server()
        # 创建线程处理服务器返回的响应
        Thread(target=lambda:self.response_handle()).start()
        # 窗口主循环
        self.window.mainloop()

    def response_handle(self):
        while self.is_running:

            response_text = None
            try:
                # 接受服务器端返回的数据
                response_text = self.conn.recv_data()
            except BlockingIOError:
                sleep(0.1)
                continue
            # 响应编号和响应内容
            response_data = self.parsing_response_text(response_text)
            # 获取对应处理函数
            handle_function = self.response_handle_functions[response_data['response_id']]

            if handle_function:
                handle_function(response_data)

    def response_login_handle(self,response_data):
        """登录响应处理"""

        result = response_data["result"]
        nickname = response_data["nickname"]
        if result == "0":
            showinfo("提示","用户名或密码错误") #参数1，标题。参数2，提示内容
            return

        # 登录成功处理
        self.username = response_data["username"]
        showinfo("提示","登陆成功!")
        # 显示聊天窗口
        self.room.set_title(nickname)
        self.room.update()
        self.room.deiconify()
        # 隐藏登录窗口
        self.window.withdraw()

    def response_chat_handle(self,response_data):
        """聊天响应处理"""

        nickname = response_data['nickname']
        messages = response_data['messages']


        self.room.append_message(nickname,messages)


    @staticmethod
    def parsing_response_text(response_text):
        """解析服务器返回的字符串"""

        # 响应编号
        response_text_list = response_text.split(DELIMITER)
        # 保存解析后的数据
        response_data = dict()
        response_data["response_id"] = response_text_list[0]

        # 如果响应的是登录结果
        if response_text_list[0] == RESPONSE_LOGIN_RESULT:
            response_data["result"] = response_text_list[1]
            response_data["nickname"] = response_text_list[2]
            response_data["username"] = response_text_list[3]

        # 如果响应的是聊天内容
        if response_text_list[0] == RESPONSE_CHAT:
            response_data['nickname'] = response_text_list[1]
            response_data['messages'] = response_text_list[2]

        return response_data

def main():
    client = Client()
    client.startup()

if __name__ == '__main__':
    main()