#!/usr/bin/python  # 指定Python解释器路径
# author Yu  # 作者信息
# 2023年06月24日  # 代码编写日期
import sys  # 导入sys模块，用于访问与Python解释器紧密相关的变量和函数
import os  # 导入os模块，提供了与操作系统进行交互的功能
import re  # 导入re模块，用于支持正则表达式操作

my_list = []  # 初始化一个空列表，用于存储符合条件的文件路径

# 定义一个递归函数，用于遍历指定目录及其子目录
def recursion_dir(dir, width):
    file_list = os.listdir(dir)  # 获取指定目录下的所有文件和文件夹列表
    for file1 in file_list:  # 遍历文件和文件夹列表
        data = re.search(r'.py$|.ipynb$', file1)  # 使用正则表达式查找以.py或.ipynb结尾的文件
        # 使用正则表达式，在空格前面加上反斜杠
        # file = re.sub(r'\s', r'\ ', file)
        path = os.path.join(dir, file1)  # 拼接当前文件或文件夹的完整路径
        if data:  # 如果当前文件是.py或.ipynb文件
            my_list.append(path)  # 将拼接后的路径添加到列表中
        if os.path.isdir(path):  # 如果当前路径是一个目录
            recursion_dir(path, width + 4)  # 递归调用该函数，继续遍历子目录

recursion_dir('.', 0)  # 从当前目录开始调用递归函数进行遍历
name = '刘杰.tar.gz '  # 拼接压缩文件的名称，使用命令行参数
# os.system是Python调用bash shell的函数
print(name)  # 打印压缩文件的名称
print(my_list)  # 打印存储符合条件文件路径的列表
os.system('tar czf ' + name + " ".join(my_list))  # 调用系统命令进行文件压缩
str_scp = 'scp ' + name + ' py11@8.155.27.170:~/day' + sys.argv[1]  # 拼接scp命令字符串
os.system(str_scp)  # 调用系统命令进行文件传输
print('提交成功')  # 打印提交成功的提示信息
