#!/usr/bin/env python
# coding=utf-8

from flask import Flask, redirect, url_for
from flask import render_template
import os
from main import convert_timestamp, return_img_stream, monitor_screen

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def show_img():
    """
    首页展示所有截图
    """
    img_list = []
    img_timestamp_list = []
    for filename in os.listdir('static/images'):
        img_timestamp_list.append(int(os.path.basename(filename).split(".")[0]))
        img_list.append('static/images/' + filename)
    img_timestamp_list.sort(reverse=True)
    img_list.sort(reverse=True)
    img_time_list = convert_timestamp(img_timestamp_list)
    return render_template('index.html',
                           img_time_list=img_time_list,
                           img_list=img_list)


@app.route("/delete_all_files", methods=['GET', 'POST'])
def delete_all_files():
    """
    删除指定img文件夹目录下的所有文件
    """
    del_list = os.listdir('static/images')
    for f in del_list:
        file_path = os.path.join('static/images', f)
        if os.path.isfile(file_path):
            os.remove(file_path)
    return redirect(url_for('show_img'))


if __name__ == '__main__':
    app.run(debug=True, port=8080)