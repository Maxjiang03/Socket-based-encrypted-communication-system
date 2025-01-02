def input_info():
    infile_info = open('infile.txt', 'a')  # 以追加的方式向文件中写入数据，如果文件不存在就创建一个文件
    flag = 'y'
    # 向文件中录入学生信息，每一个学生的信息单独占一行
    while flag == 'y' or flag == 'Y':
        stu_id = input("请输入学生学号（如2020001）：")
        stu_name = input("请输入学生姓名：")
        stu_score_eng = input("请输入学生英语成绩：")
        stu_score_py = input("请输入学生Python成绩：")
        stu_score_math = input("请输入学生数学成绩：")
        stu_sum_score = int(stu_score_eng) + int(stu_score_py) + int(stu_score_math)
        stu_info = stu_id + '\t' + stu_name + '\t' + stu_score_eng + '\t' + stu_score_py + '\t' + \
                   stu_score_math + '\t' + str(stu_sum_score) + '\n'
        infile_info.write(stu_info)
        flag = input("是否继续添加学生信息？y/n")
    print("信息录入完毕！！！")
    infile_info.close()


# 查询学生信息
# 查询时分为按学号和按姓名查找两种
def find_info():
    flag = 'y'
    while flag == 'y' or flag == 'Y':
        n = 0
        m = 0  # 定义m，n是为了用作判断文件中是否有此人信息的标记
        findfile_info = open('infile.txt', 'r')  # 以可读方式打开文件
        line_info = findfile_info.readlines()
        find_nid = input("按学号查找请输入1，按姓名查找请输入2：")  # 查询方式分为按学号和按姓名
        if find_nid == '1':
            find_id = input('请输入学生学号：')
            for line in line_info:
                if find_id in line:
                    print(line)
                    n = n + 1
            if n == 0:
                print("没有查询到学生信息，无数据显示！！！")
        if find_nid == '2':
            find_name = input('请输入学生姓名：')
            for line in line_info:
                if find_name in line:
                    print(line)
                    m = m + 1
            if m == 0:
                print("没有查询到学生信息，无数据显示！！！")
        findfile_info.close()
        flag = input("是否继续查询学生信息？y/n")


# 删除学生信息
# 输入学号进行查找，查找到学生信息之后，对学生信息进行删除
def del_info():
    flag = 'y'
    while flag == 'y' or flag == 'Y':
        n = 0  # 用以查无此人时的标记
        defile_info1 = open('infile.txt', 'r')  # 以可读方式打开文件
        line_info = defile_info1.readlines()  # 将文件的信息按行全部读取出来，此时line_info是一个列表，每一行是一个元素
        defile_info2 = open('infile.txt', 'w')  # 以可写方式打开文件，用来将删除后的信息写入文件
        del_id = input("请输入要删除的学生的学号：")
        for line in line_info:  # 如果要删除的学生学号在文件存储的信息中，就将后面的信息向前移动覆盖这条信息
            if del_id in line:
                continue
            defile_info2.write(line)
            n = n + 1
        if n == len(line_info):
            print("无此学生信息，请核对后再操作！！！")
        else:
            print("学号为{0}的学生信息已被删除！！！".format(del_id))
        defile_info1.close()
        defile_info2.close()
        flag = input("是否继续删除学习信息？y/n")


# 修改学生信息
# 输入学号后，查询到学生信息之后，对学生信息进行修改
def mod_info():
    flag = 'y'
    while flag == 'y' or flag == 'Y':
        n = 0  # 用以查无此人时的标记
        mod_id = input("请输入要修改的学生学号：")
        modfile_file1 = open('infile.txt', 'r')  # 以可读方式打开文件，读取到line_info中，每一行就是一个列表的元素
        line_info = modfile_file1.readlines()
        modfile_file2 = open('infile.txt', 'w')  # 用以写入修改后的数据
        for line in line_info:  # 遍历列表
            if mod_id in line:  # 如果修改的学生信息存在，就重新写入学生信息
                print("已找到学生，请修改信息！")
                mod_name = input("请输入姓名：")
                mod_score_eng = input("请输入英语成绩：")
                mod_score_py = input("请输入python成绩：")
                mod_score_math = input("请输入数学成绩：")
                mod_sum_score = int(mod_score_eng) + int(mod_score_py) + int(mod_score_math)
                mod_stu_info = mod_id + '\t' + mod_name + '\t' + mod_score_eng + '\t' + mod_score_py + '\t' + \
                               mod_score_math + '\t' + str(mod_sum_score) + '\n'
                modfile_file2.write(mod_stu_info)
                print("修改成功！！！")
                continue
            modfile_file2.write(line)  # 由于w方式打开的文件重新后会覆盖原有数据，所以需要将原有数据写入
            n = n + 1
        if n == len(line_info):
            print("无此学生信息，请核对后再操作！！！")
        else:
            print("学号为{0}的学生信息已修改！！！".format(mod_id))
        modfile_file1.close()
        modfile_file2.close()
        flag = input("是否继续修改学习信息？y/n")


# 排序学生信息
# 排序方式可选择升序和降序
# 可选择按英语、python、数学成绩以及总成绩进行排序
def sort_info():
    flag = 'y'

    # 此方法用来排序，返回列表的2，3，4，5的元素，也就是分别依据英语、python、数学、总成绩进行排序
    # 例如列表[['1','2','3'],['1','2','3'],['1','2','3']]
    # 则take_eng就是以每个列表的第三个元素为依据排序，也就是3，2，1
    def take_eng(elem):
        return int(elem[2])

    def take_py(elem):
        return int(elem[3])

    def take_math(elem):
        return int(elem[4])

    def take_sum(elem):
        return int(elem[5])

    # 此方法用来进行排序后的输出操作
    def output_sort(sort_list):
        for m in sort_list:
            for n in m:
                print("%+10s" % n, end=' ')
            print()

    while flag == 'y' or flag == 'Y':
        sortfile_info = open('infile.txt', 'r')  # 可读方式打开文件，并读取信息line_info中
        line_info = sortfile_info.readlines()
        # 定义列表，用来将读取出来的字符串信息，转化为列表
        # 例如['2020001\t李一一\t75\t86\t89\t250\n', '2020002\t王大伟\t85\t96\t99\t280\n']
        # 转化为[['2020001', '李一一', '75', '86', '89', '250'], ['2020002', '王大伟', '85', '96', '99', '280']]
        lst = []
        for i in range(0, len(line_info)):
            lst.append('lst' + str(i))
        i = 0
        for line in line_info:  # 遍历列表，将信息转化为单独的列表，并去掉\t和\n，方便接下来的排序比较
            line = line.replace('\n', '')
            lst[i] = line.split('\t')
            i = i + 1

        sort_up_down = input("请选择（0升序，1降序）：")
        print("1.按英语成绩排序，2.按python成绩排序")
        print("3.按数学成绩排序，4.按学生总成绩排序")
        sort_term = input("请选择：")
        if sort_up_down == '0':  # 升序
            if sort_term == '1':
                lst.sort(key=take_eng, reverse=False)  # 以英语成绩升序排序
            if sort_term == '2':
                lst.sort(key=take_py, reverse=False)
            if sort_term == '3':
                lst.sort(key=take_math, reverse=False)
            if sort_term == '4':
                lst.sort(key=take_sum, reverse=False)
            output_sort(lst)
        if sort_up_down == '1':  # 降序
            if sort_term == '1':
                lst.sort(key=take_eng, reverse=True)  # 以英语成绩降序排序
            if sort_term == '2':
                lst.sort(key=take_py, reverse=True)
            if sort_term == '3':
                lst.sort(key=take_math, reverse=True)
            if sort_term == '4':
                lst.sort(key=take_sum, reverse=True)
            output_sort(lst)
        flag = input("是否继续排序信息？y/n")


# 统计学生总数
# 输出信息管理系统中有几个学生的信息
def sum_info():
    sumfile_info = open('infile.txt', 'r')
    line_info = sumfile_info.readlines()
    sum_stu = len(line_info)  # 写出列表中的元素个数
    print("一共有{0}名学生。".format(sum_stu))
    sumfile_info.close()


# 显示学生信息
def show_info():
    print("学号", end='\t\t')
    print("姓名", end='\t\t')
    print("英语成绩", end='\t\t')
    print("Python成绩", end='\t\t')
    print("数学成绩", end='\t\t')
    print("总成绩", end='\t\t')
    print('\n')
    showfile_info = open('infile.txt', 'r')
    line_info = showfile_info.readlines()
    for line in line_info:  # 遍历列表，输出各个元素
        print(line)
    showfile_info.close()


def show_choose():
    print("==========================学生信息管理系统==========================")
    print()
    print("-----------------------------功能菜单------------------------------")
    print()
    print("                         1.录入学生信息")
    print("                         2.查找学生信息")
    print("                         3.删除学生信息")
    print("                         4.修改学生信息")
    print("                         5.排序学生信息")
    print("                         6.统计学生总数")
    print("                         7.显示学生信息")
    print("                         0.退出信息管理系统")
    print()
    print("------------------------------------------------------------------")


def main():
    show_choose()
    choose_menu = input("请选择：")
    while choose_menu != '0':
        if choose_menu == '1':
            input_info()
        if choose_menu == '2':
            find_info()
        if choose_menu == '3':
            del_info()
        if choose_menu == '4':
            mod_info()
        if choose_menu == '5':
            sort_info()
        if choose_menu == '6':
            sum_info()
        if choose_menu == '7':
            show_info()
        choose_menu = input("请选择：")

    print("欢迎您再次使用！！！")


main()
