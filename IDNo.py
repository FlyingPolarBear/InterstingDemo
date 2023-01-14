'''
Author: Derry
Date: 2023-01-14 16:28:52
LastEditors: Derry
Email: drlv@mail.ustc.edu.cn
LastEditTime: 2023-01-14 16:47:37
Description: None
'''


def fillIDNo(IDNo):
    if len(IDNo) < 17:
        raise ValueError("你输入的身份证号码的长度不足17位！")
    for c in IDNo:
        if not c.isdigit():
            raise ValueError("你输入的身份证号码的前17位不全是数字！")

    table1 = [7, 9, 10, 5, 8, 4, 2, 1, 6, 3, 7, 9, 10, 5, 8, 4, 2]
    table2 = [1, 0, 'X', 9, 8, 7, 6, 5, 4, 3, 2]
    s = sum([int(IDNo[i])*table1[i] for i in range(17)])
    print(f"17位数字加权和：{s}\t余数：{s % 11}\t校验码：{table2[s % 11]}")
    print(f"你输入的身份证号码为：{IDNo}{table2[s % 11]}")


if __name__ == "__main__":
    IDNo = input("请输入你的身份证号码的前17位：")
    fillIDNo(IDNo)
