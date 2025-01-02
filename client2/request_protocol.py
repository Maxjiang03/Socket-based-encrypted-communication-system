from config import *


class RequestProtocol(object):
    '''请求协议组装'''

    @staticmethod
    def request_login(username, password):
        """
        拼接登录请求, 数据格式:  "请求协议编号|登录用户名|登录密码"
        :param username: 登录用户名
        :param password: 登录密码
        :return: 登录请求格式字符串
        """
        return DELIMITER.join([REQUEST_LOGIN,username,password])

    @staticmethod
    def request_chat(username,message):
        """
        拼接聊天请, 数据格式:  "请求协议编号|聊天内容发送者用户名|聊天内容"
        :param username: 聊天信息发送者的用户名
        :param messages: 聊天内容
        :return: 聊天请求格式字符串
        """
        return DELIMITER.join([REQUEST_CHAT,username,message])