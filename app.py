#!/usr/bin/env python
# coding=utf-8

from flask import Flask, redirect, url_for
from flask import render_template
import os
import time

app = Flask(__name__)


def return_img_stream(img_path_list):
    """
    工具函数:
    获取本地图片流
    :param img_local_path:文件单张图片的本地绝对路径
    :return: 图片流
    """
    import base64
    img_stream_list = []
    for img_path in img_path_list:
        with open(img_path, 'rb') as img_f:
            stream_temp = img_f.read()
            img_stream_list.append(base64.b64encode(stream_temp).decode())
    return img_stream_list


def convert_timestamp(timestamp_list):
    customize_style_time_list = []
    for timestamp in timestamp_list:
        localtime = time.localtime(timestamp)
        customize_style_time_list.append(time.strftime("%Y-%m-%d %H:%M:%S", localtime))
    return customize_style_time_list


@app.route('/', methods=['GET', 'POST'])
def show_img():
    img_list = []
    img_timestam_list = []
    for filename in os.listdir('img'):
        img_timestam_list.append(int(os.path.basename(filename).split(".")[0]))
        img_list.append('img/' + filename)
    img_timestam_list.sort(reverse=True)
    img_list.sort(reverse=True)
    img_time_list = convert_timestamp(img_timestam_list)
    img_stream_list = return_img_stream(img_list)
    return render_template('index.html',
                           img_stream_list=img_stream_list,
                           img_time_list=img_time_list)


@app.route("/delete_all_files", methods=['GET', 'POST'])
def delete_all_files():
    """
    删除指定img文件夹目录下的所有文件
    """
    del_list = os.listdir('img')
    for f in del_list:
        file_path = os.path.join('img', f)
        if os.path.isfile(file_path):
            os.remove(file_path)
    return redirect(url_for('show_img'))


if __name__ == '__main__':
    app.run(debug=True, port=8080)
