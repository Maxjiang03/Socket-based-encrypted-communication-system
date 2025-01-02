import random


n = 6


def v_code(n=32):
    """
        Returns:
            ret:random six num and letter
    """
    ret = ""
    for i in range(n):
        num = random.randint(0, 9)
        # num = chr(random.randint(48,57))#ASCII表示数字
        letter = chr(random.randint(97, 122))  # 取小写字母
        Letter = chr(random.randint(65, 90))  # 取大写字母
        s = str(random.choice([num, letter, Letter]))
        ret += s
    return ret


print("v_code_nums_letters result: " + v_code())