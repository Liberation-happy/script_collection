# coding = utf-8
# author: happy

# 获取文件夹中所有的txt文件，并按时间排序

"""
力 	位移 	时间
kN	mm	sec
3.07300561523438	-5.38320001214743	15.4499998092651
3.02878564453125	-5.38600003346801	15.5
3.0045126953125	-5.38800004869699	15.5500001907349
2.9830458984375	-5.38920005783439	15.6000003814697
"""
import os

import numpy as np


# 获取文件夹中的txt文件
def get_txt(path) -> list:
    file_list = []
    for filename in os.listdir(path):
        file_list.append(os.path.join(path, filename))
    return file_list


# 读取文件夹中的txt文件，获取所有的数据，并存入data数组中
def get_data(file_list) -> list:
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
def sort_data(data_list) -> list:
    data = np.array(data_list)
    data = data[data[:, 2].argsort()]
    a = np.min(data, axis=0)
    four = []
    for i in range(len(data)):
        data[i][0] *= 1000
        data[i][1] = (float(data[:, 1][i]) - float(a[1])) / 1000
        data[i][2] = float(data[:, 2][i]) - float(a[2])
        four.append((data[i][0] / (0.05**2)) / 1000000)
    four = np.array(four)
    data = np.c_[data, four]
    return data


# 将数据存储到新的txt文件中，命名为new
def save_data(path, data):
    new_file = open(os.path.join(path, 'new.txt'), mode='w')
    for i in data:
        str_data = "{}\t{}\t{}\t{}\n".format(i[0], i[1], i[2], i[3])
        new_file.write(str_data)


if __name__ == "__main__":
    file_list = get_txt(r"D:\实验室\大创数据\力学测试材料-1023-202\23-1试验运行 1 2022-10-23 10 53 18")
    data_list = get_data(file_list)
    data = sort_data(data_list)
    save_data(r"D:\实验室\大创数据\力学测试材料-1023-202\23-1试验运行 1 2022-10-23 10 53 18", data)
