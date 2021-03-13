# -*- coding: utf-8 -*-

# 主函数

import sys
from PyQt5 import QtGui, QtCore, QtWidgets
import index, alert, bye


def get_relus():
    """
    获取规则库，并将结论和前提分开存储
    :return:P：存储前提
            Q：存储结论
    """
    RD = open("data\RD.txt", "r")       # 打开规则库
    P = []      # 存储前提
    Q = []      # 存储结论
    for line in RD:     # 按行读取文件
        line = line.strip("\n")     # 删除每行开头或结尾的换行
        if line == '':      # 跳过空行
            continue
        line = line.split(' ')      # 把每一行按照空格切片
        Q.append(line[line.__len__() - 1])      # 把除了最后一个元素添加到前提数组中
        del line[line.__len__() - 1]        # 删除前提
        P.append(line)
    RD.close()      # 关闭文件
    return P, Q

def ListInSet(li, se):
    """
    判断前提是否在输入事实的set中
    :param li:前提的列表
    :param se:输入事实的集合
    :return:
    """
    for i in li:
        if i not in se:
            return False
    return True


# 设置退出界面
class Bye_ui(QtWidgets.QMainWindow, bye.Ui_MainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)    # 创建主界面对象
        bye.Ui_MainWindow.__init__(self)    # 主界面对象初始化
        self.setupUi(self)      # 配置主界面对象
        self.pushButton.clicked.connect(self.no)
    def no(self):   # 关闭窗口
        self.close()

# 设置提示界面
class Alert_ui(QtWidgets.QMainWindow, alert.Ui_MainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        alert.Ui_MainWindow.__init__(self)
        self.setupUi(self)


# 设置主界面
class Index_ui(QtWidgets.QMainWindow, index.Ui_MainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        index.Ui_MainWindow.__init__(self)
        self.setupUi(self)
        self.pushButton.clicked.connect(self.add_rule)      # 添加规则
        self.pushButton_2.clicked.connect(self.inference)   # 进行推理
        self.alert_window = Alert_ui()
        for line in open("data\RD.txt", 'r'):
            self.textBrowser.append(line)   # 将规则库放入显示框
        self.pushButton_3.clicked.connect(self.close_window)    # 退出系统


    def add_rule(self):
        """
        添加新规则
        :return:
        """
        new_rule = self.lineEdit.text()     # 获取到添加规则输入框的内容
        if new_rule != " ":
            self.textBrowser.append(new_rule)
            RD = open('data\RD.txt', 'a')
            RD.write(new_rule)
            RD.write('\n')
            RD.close()

    def close_window(self):
        """
        关闭窗口
        :return:
        """
        self.bye_window = Bye_ui()
        self.bye_window.show()
        self.alert_window = Alert_ui()
        self.alert_window.close()
        self.close()
        # self.bye_window.pushButton.clicked.connect(self.bye_window.close())

    def inference(self):
        """
        推理函数
        :return:
        """
        input = self.textEdit.toPlainText() # 获取到输入的事实
        input = input.split('\n')   # 按照回车符进行切片
        DB = set(input)     # 将切片的事实存放到集合中
        [P, Q] = get_relus()    # 获取到规则库中的前提和结论
        self.process = ''       # 存储推理过程
        self.animal = ''        # 存储推理结果
        # 开始推理
        flag = 0    # 设置一个标识，判断能否退出结论，若能推出结论，则置为1
        for premise in P:   # 遍历规则库的前提
            if ListInSet(premise, DB):  # 判断前提是否在输入事实的集合中
                DB.add(Q[P.index(premise)])     # 将前提对应的结论添加到事实集合中
                self.animal = Q[P.index(premise)]   # 更新一下推理结论
                self.process += "%s --> %s" % (premise, Q[P.index(premise)])    # 更新一下推理过程
                flag = 1

        if flag == 0:   # 若一个结论推不出来，弹出提示窗口，询问是否进行补充
            self.alert_window.show()
            self.alert_window.pushButton.clicked.connect(self.alert_window.close)   # 若点是按钮，返回主页面
            self.alert_window.pushButton_2.clicked.connect(self.close_window)   # 若点否按钮，关闭系统

        else:   # 若推出结论，则显示推理过程以及结论
            self.textEdit_2.setText(self.process)
            self.lineEdit_2.setText(self.animal)

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)      # 新建窗体
    index_window = Index_ui()     # 创建系统首页的窗口对象
    index_window.show()     #显示首页
    sys.exit(app.exec_())   # 保持显示