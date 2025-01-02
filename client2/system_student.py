# 定义全局变量
info_list = [{"name": '张三', "gender": '男', "age": 27}]
admin_id = "python"
password = "123456"


def add_info_name():  # 输入姓名
    name = str(input("请输入姓名："))
    return name


def add_info_gender():  # 输入性别
    while True:
        gender = str(input("请输入性别："))
        if gender in "男女":
            return gender
        else:
            print("【ERROR_1】：性别输入有误，请输入男或女！")


def add_info_age():  # 输入年龄
    while True:
        age = str(input("请输入年龄："))
        if age.isdigit() is True:
            return age
        else:
            print("【ERROR_2】：年龄输入有误，请输入纯数字！")


def search():  # 按姓名查找
    name = add_info_name()
    for i in info_list:
        if name in i.values():
            print(i)
            return
    else:
        print("【ERROR_3】：查无此人，请重新输入！")


def remove():  # 删除函数
    name = add_info_name()
    for i in info_list:
        if name in i.values():
            info_list.remove(i)
            print("【INFO_1】:删除成功！")
            return
    else:
        print("【ERROR_3】：查无此人，请重新输入！")


def alter():  # 修改函数
    name = add_info_name()
    for i in info_list:
        if name in i.values():
            info_list[info_list.index(i)] = {"name": name, "gender": add_info_gender(), "age": add_info_age()}
            print("【INFO_2】:修改成功！")
            return
    else:
        print("【ERROR_5】：查无此人，请重新输入！")


def verify():
    ad = str(input("请输入管理员账号："))
    pd = str(input("请输入管理员密码："))
    if ad == admin_id and pd == password:
        return True
    else:
        print("【ERROR_6】：管理员账号或密码错误，请重新输入！")


def main():
    while True:
        print("************************** 名片管理器 **************************")
        print("-------------------------- 1.添加名片 --------------------------")
        print("-------------------------- 2.删除名片 --------------------------")
        print("-------------------------- 3.修改名片 --------------------------")
        print("-------------------------- 4.查询名片 --------------------------")
        print("-------------------------- 5.查询所有 --------------------------")
        print("-------------------------- 6.退出系统 --------------------------")
        print("************************** 名片管理器 **************************")
        command = str(input("请输入对应数字进行操作："))  # 采用字符串形式，避免用户输入时报错
        print("-" * 30)  # 分隔线
        if command == "1":  # 采用字符串形式，避免用户输入时报错
            dic = {"name": add_info_name(), "gender": add_info_gender(), "age": add_info_age()}
            info_list.append(dic)
            print("【INFO_3】:添加成功！")
        elif command == "2":
            if verify():
                remove()
            else:
                pass
        elif command == "3":
            if verify():
                alter()
            else:
                pass
        elif command == "4":
            if verify():
                search()
            else:
                pass
        elif command == "5":
            if verify():
                print("【INFO_4】：所有员工信息为：")
                print(info_list)
            else:
                pass
        elif command == "6":
            print("【INFO_5】：谢谢使用，您已成功退出系统！")
            exit()
        else:
            print("【ERROR_7】：输入有误，请重新输入相应数字进行操作！")

