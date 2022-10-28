# coding = utf-8
# author: happy
import os
import shutil


def work_data(path, new_path, interval):
    old_pictures = []
    new_pictures = []
    for filename in os.listdir(path):
        old_pictures.append(os.path.join(path, filename))
        new_pictures.append(os.path.join(new_path, filename))

    old_picture = old_pictures[interval-1::interval]
    new_picture = new_pictures[interval-1::interval]
    for idx, pic in enumerate(old_picture):
        shutil.copy(pic, new_picture[idx])


work_data(path=r"D:\code_before", new_path=r"D:\data", interval=300)

