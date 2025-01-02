from config import *


class ResponseProtocol(object):
    """响应拼接"""

    @staticmethod
    def response_login_result(result, nickname, username):
        """
        拼接登录响应, 数据格式为:  "响应协议编号|登录结果|登录用户昵称|登录用户用户名"
        :param result: 登录结果, 0或者1, 0表示登录失败, 1表示登录成功
        :param nickname: 登录用户昵称, 如登录失败, 则该值为空字符串
        :param username: 登录用户名, 如登录失败, 该值为空字符串
        :return: 登录结果响应格式字符串
        """

        return DELIMITER.join([RESPONSE_LOGIN_RESULT, result, nickname, username])

    @staticmethod
    def response_chat(nickname,messages):
        """
        拼接聊天响应, 数据格式为: "响应协议编号|聊天发送者昵称|聊天信息"
        :param nickname: 聊天内容发送者的昵称
        :param messages: 聊天内容
        :return: 聊天响应协议格式字符串
        """

        return DELIMITER.join([RESPONSE_CHAT,nickname,messages])