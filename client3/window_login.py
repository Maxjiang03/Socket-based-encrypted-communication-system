from tkinter import Tk
from tkinter import Label
from tkinter import Entry
from tkinter import Button
from tkinter import Frame
from tkinter import LEFT
from tkinter import END


class WindowLogin(Tk):
    """登录窗口"""

    def __init__(self):

        # 调用父类初始化方法
        super(WindowLogin, self).__init__()
        # 设置窗体属性
        self.window_init()
        # 创建控件
        self.add_widgets()

    def window_init(self):
        """窗口属性初始化"""

        # 设置窗体标题
        self.title("登录窗口")
        # 设置窗体大小不能修改
        self.resizable(False,False)
        # 窗口宽高
        window_width = 255
        window_height = 95
        # 屏幕宽高
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        # 屏幕中心位置坐标
        pos_x = (screen_width - window_width) / 2
        pos_y = (screen_height - window_height) / 2
        # 设置屏幕宽、高、x位置、y位置
        self.geometry('%dx%d+%d+%d' % (window_width, window_height, pos_x, pos_y))

    def add_widgets(self):
        """创建所需控件"""

        # 用户名提示标签
        username_label = Label(self)
        username_label['text'] = '用户名:'
        username_label.grid(row=0, column=0, padx=10, pady=5)
        # 用户名输入文本框
        username_entry = Entry(self, name='username_entry')
        username_entry['width'] = 25
        username_entry.grid(row=0, column=1)

        # 密码提示标签
        password_label = Label(self)
        password_label['text'] = '密   码:'
        password_label.grid(row=1, column=0)
        # 密码输入文本框
        password_entry = Entry(self, name='password_entry')
        password_entry['show'] = '*'
        password_entry['width'] = 25
        password_entry.grid(row=1, column=1)

        # 创建Frame
        button_frame = Frame(self, name='button_frame')
        # 重置按钮
        reset_button = Button(button_frame, name='reset_button')
        reset_button['text'] = ' 重置 '
        reset_button.pack(side=LEFT, padx=20)
        # 登录按钮
        login_button = Button(button_frame, name='login_button')
        login_button['text'] = ' 登录 '
        login_button.pack(side=LEFT)
        button_frame.grid(row=2, columnspan=2, pady=5)

    def get_username(self):
        """获得用户名"""

        return self.children['username_entry'].get()

    def clear_username(self):
        """清除输入的用户名"""

        self.children['username_entry'].delete(0, END)

    def clear_password(self):
        """清除输入的密码"""

        self.children['password_entry'].delete(0, END)

    def get_password(self):
        """获得密码"""

        return self.children['password_entry'].get()

    def on_login_button_click(self, command):
        """登录按钮绑定点击事件处理方法"""

        self.children['button_frame'].children['login_button']['command'] = command

    def on_reset_button_click(self, command):
        """重置按钮点击事件处理方法"""

        self.children['button_frame'].children['reset_button']['command'] = command

    def on_window_closed(self, command):
        """窗口关闭事件处理方法"""

        # 设置窗口关闭事件
        self.protocol('WM_DELETE_WINDOW', command)


if __name__ == '__main__':
    login_window = WindowLogin()
    login_window.mainloop()