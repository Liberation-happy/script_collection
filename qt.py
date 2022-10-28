# coding = utf-8
# author: happy
import os
import shutil
from tkinter import *
from tkinter import filedialog

from tkinter.messagebox import *
import numpy as np
import tkinter.messagebox as msgbox


class First:

    def get_txt(self, path) -> list:
        file_list = []
        for filename in os.listdir(path):
            file_list.append(os.path.join(path, filename))
        return file_list

    # 读取文件夹中的txt文件，获取所有的数据，并存入data数组中
    def get_data(self, file_list) -> list:
        data_list = []
        for file in file_list:
            file = open(file, 'r', encoding="utf-8")
            # 读取每一列
            lines = file.readlines()
            for idx, line in enumerate(lines):
                if idx >= 8:
                    # 对每行数据进行处理，将所有数据变为float类型
                    line_data = line.split()
                    line_data = [float(i) for i in line_data]
                    data_list.append(line_data)
                else:
                    continue
        return data_list

    # 将数据装换为ndarray的格式，然后进行排序
    def sort_data(self, data_list) -> list:
        data = np.array(data_list)
        data = data[data[:, 2].argsort()]
        a = np.min(data, axis=0)
        four = []
        for i in range(len(data)):
            data[i][0] *= 1000
            data[i][1] = (float(data[:, 1][i]) - float(a[1])) / 1000
            data[i][2] = float(data[:, 2][i]) - float(a[2])
            four.append((data[i][0] / (0.05 ** 2)) / 1000000)
        four = np.array(four)
        data = np.c_[data, four]
        return data

    # 将数据存储到新的txt文件中，命名为new
    def save_data(self, path, data):
        new_file = open(os.path.join(path, 'new.txt'), mode='w')
        for i in data:
            str_data = "{}\t{}\t{}\t{}\n".format(i[0], i[1], i[2], i[3])
            new_file.write(str_data)

    def work_data(self, path):
        try:
            file_list = self.get_txt(path)
            data_list = self.get_data(file_list)
            data = self.sort_data(data_list)
            self.save_data(path, data)
            return True
        except:
            return False


class FirstFrame(Frame):  # 继承Frame类
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.root = master  # 定义内部变量root
        self.select_path = StringVar()
        self.path = None
        self.createPage()

    def select_folder(self):
        # 文件夹选择
        selected_folder = filedialog.askdirectory()  # 使用askdirectory函数选择文件夹
        self.select_path.set(selected_folder)
        self.path = selected_folder

    def work_data(self):
        worker = First()
        num = worker.work_data(path=self.path)
        if num:
            msgbox.showinfo("提示", '完成')
        else:
            msgbox.showwarning('提示', '已处理过')

    def createPage(self):
        Label(self, text="文件路径：").grid(column=0, row=0, rowspan=3)
        Entry(self, textvariable=self.select_path).grid(column=1, row=0, rowspan=3)
        Button(self, text="选择文件夹", command=self.select_folder).grid(row=2, column=2)
        Button(self, text='处理', command=self.work_data).grid(row=6, column=1, stick=E, pady=10)


class QueryFrame(Frame):  # 继承Frame类
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.root = master  # 定义内部变量root
        self.select_img_path = StringVar()
        self.old_path = None
        self.selected_img_path = StringVar()
        self.new_path = None
        self.interval = StringVar()
        self.createPage()

    def select_old_folder(self):
        # 文件夹选择
        selected_folder = filedialog.askdirectory()  # 使用askdirectory函数选择文件夹
        self.select_img_path.set(selected_folder)
        self.old_path = selected_folder

    def select_new_folder(self):
        # 文件夹选择
        selected_folder = filedialog.askdirectory()  # 使用askdirectory函数选择文件夹
        self.selected_img_path.set(selected_folder)
        self.new_path = selected_folder

    def work_data(self):
        try:
            interval = int(self.interval.get())
            old_pictures = []
            new_pictures = []
            for filename in os.listdir(self.old_path):
                old_pictures.append(os.path.join(self.old_path, filename))
                new_pictures.append(os.path.join(self.new_path, filename))

            old_picture = old_pictures[interval - 1::interval]
            new_picture = new_pictures[interval - 1::interval]
            for idx, pic in enumerate(old_picture):
                shutil.copy(pic, new_picture[idx])
            msgbox.showinfo("提示", '完成')
        except:
            msgbox.showwarning('提示', '未完成，出现问题')

    def createPage(self):
        Label(self, text="图片文件路径：").grid(column=0, row=0, rowspan=3)
        Entry(self, textvariable=self.select_img_path).grid(column=1, row=0, rowspan=3)
        Button(self, text="选择文件夹", command=self.select_old_folder).grid(row=1, column=2)
        Label(self, text="目标文件路径：").grid(column=0, row=3, rowspan=3)
        Entry(self, textvariable=self.selected_img_path).grid(column=1, row=3, rowspan=3)
        Button(self, text="选择文件夹", command=self.select_new_folder).grid(row=3, column=2)
        Label(self, text='间隔: ').grid(row=7, stick=W, pady=10)
        Entry(self, textvariable=self.interval).grid(row=7, column=1, stick=E)
        Button(self, text='处理', command=self.work_data).grid(row=9, column=1, stick=E, pady=10)


class CountFrame(Frame):  # 继承Frame类
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.root = master  # 定义内部变量root
        self.createPage()

    def createPage(self):
        Label(self, text='统计界面').pack()


class AboutFrame(Frame):  # 继承Frame类
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.root = master  # 定义内部变量root
        self.createPage()

    def createPage(self):
        Label(self, text='关于界面').pack()


class MainPage(object):
    def __init__(self, master=None):
        self.root = master  # 定义内部变量root
        self.root.geometry('%dx%d' % (600, 400))  # 设置窗口大小
        self.createPage()

    def createPage(self):
        self.inputPage = FirstFrame(self.root)  # 创建不同Frame
        self.queryPage = QueryFrame(self.root)
        self.countPage = CountFrame(self.root)
        self.aboutPage = AboutFrame(self.root)
        self.inputPage.pack()  # 默认显示数据录入界面
        menubar = Menu(self.root)
        menubar.add_command(label='时间整合', command=self.inputData)
        menubar.add_command(label='图片处理', command=self.queryData)
        menubar.add_command(label='统计', command=self.countData)
        menubar.add_command(label='关于', command=self.aboutDisp)
        self.root['menu'] = menubar  # 设置菜单栏

    def inputData(self):
        self.inputPage.pack()
        self.queryPage.pack_forget()
        self.countPage.pack_forget()
        self.aboutPage.pack_forget()

    def queryData(self):
        self.inputPage.pack_forget()
        self.queryPage.pack()
        self.countPage.pack_forget()
        self.aboutPage.pack_forget()

    def countData(self):
        self.inputPage.pack_forget()
        self.queryPage.pack_forget()
        self.countPage.pack()
        self.aboutPage.pack_forget()

    def aboutDisp(self):
        self.inputPage.pack_forget()
        self.queryPage.pack_forget()
        self.countPage.pack_forget()
        self.aboutPage.pack()


class LoginPage(object):
    def __init__(self, master=None):
        self.root = master  # 定义内部变量root
        self.root.geometry('%dx%d' % (300, 180))  # 设置窗口大小
        self.username = StringVar()
        self.password = StringVar()
        self.createPage()

    def createPage(self):
        self.page = Frame(self.root)  # 创建Frame
        self.page.pack()
        Label(self.page).grid(row=0, stick=W)
        Label(self.page, text='账户: ').grid(row=1, stick=W, pady=10)
        Entry(self.page, textvariable=self.username).grid(row=1, column=1, stick=E)
        Label(self.page, text='密码: ').grid(row=2, stick=W, pady=10)
        Entry(self.page, textvariable=self.password, show='*').grid(row=2, column=1, stick=E)
        Button(self.page, text='登陆', command=self.loginCheck).grid(row=3, stick=W, pady=10)
        Button(self.page, text='退出', command=self.page.quit).grid(row=3, column=1, stick=E)

    def loginCheck(self):
        name = self.username.get()
        secret = self.password.get()
        if name == '大创' and secret == '123456':
            self.page.destroy()
            MainPage(self.root)
        else:
            showinfo(title='错误', message='账号或密码错误！')


root = Tk()
root.title('小程序')
LoginPage(root)
# MainPage(root)
root.mainloop()
