import os
import time
import subprocess
import cv2


def adb_devices():
    """
    查看已连接设备
    """
    return os.system('adb devices')


def monitor_screen():
    """
    通过adb开启监听屏幕点击事件
    命令行例子:adb shell getevent
    """
    p = subprocess.Popen('adb shell getevent -l', shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    print('开始监听屏幕点击事件')
    while True:
        cmd_output = p.stdout.readline().decode()
        # print(cmd_output)
        if "ABS_MT_POSITION_X" in cmd_output:
            x_value = get_coordinate_value(cmd_output)
        if "ABS_MT_POSITION_Y" in cmd_output:
            y_value = get_coordinate_value(cmd_output)
            print("x:", x_value, "y:", y_value)
            print("存在屏幕点击事件")
            screen_cap(x_value, y_value)


def screen_cap(x_value, y_value):
    """
    通过adb命令行截图，并以时间戳命名
    命令行例子:adb exec-out screencap -p > test.png
    """
    current_time = str(int(time.time()))
    img_path = 'img/' + current_time + '.png'
    # result = os.system('adb exec-out screencap -p > img/' + current_time + '.png')
    result = os.system('adb exec-out screencap -p > ' + img_path)
    if result == 0:
        print("截图成功，点击事件坐标x:"+ str(x_value) + "y:" + str(y_value))
    draw_img(img_path, x_value, y_value)


def get_coordinate_value(cmd_output):
    """
    通过命令行返回的字符串中提取点击事件所在的x或y轴坐标点
    命令行例子:adb shell getevent
    """
    cmd_output_split_list = cmd_output.split(' ')
    temp_list = [x for x in cmd_output_split_list if x != '']
    if '\r\n' in temp_list:
        temp_list.remove('\r\n')
    elif '\n' in temp_list:
        temp_list.remove('\n')
    coordinate_value = temp_list[-1]
    coordinate_value = int(coordinate_value, 16)
    return coordinate_value


def return_img_stream(img_path_list):
    """
    工具函数:
    获取本地图片流
    :param img_path_list:文件图片的路径列表
    :return: 图片流列表
    """
    import base64
    img_stream_list = []
    for img_path in img_path_list:
        with open(img_path, 'rb') as img_f:
            stream_temp = img_f.read()
            img_stream_list.append(base64.b64encode(stream_temp).decode())
    return img_stream_list


def convert_timestamp(timestamp_list):
    """
    时间戳转换
    :param timestamp_list:时间戳列表
    :return: 转换后的时间格式列表
    """
    customize_style_time_list = []
    for timestamp in timestamp_list:
        localtime = time.localtime(timestamp)
        customize_style_time_list.append(time.strftime("%Y-%m-%d %H:%M:%S", localtime))
    return customize_style_time_list


def draw_img(img_path, x, y):
    img = cv2.imread(img_path)  # 读取图片
    cv2.circle(img, (x, y), 60, (0, 0, 255), 10)
    # cv2.circle(img, center, radius, color[, thickness[, lineType[, shift]]])
    # cv2.circle(输入的图片data,圆心位置,圆的半径,圆的颜色,圆形轮廓的粗细（如果为正）负数(-1)表示要绘制实心圆,圆边界的类型,中心坐标和半径值中的小数位数)
    cv2.imwrite(img_path, img)


if __name__ == '__main__':
    # pass
    print(monitor_screen())
    # draw_img()
