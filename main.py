import os
import time
import subprocess


def adb_devices():
    """
    查看已连接设备
    """
    return os.system('adb devices')


def screen_cap():
    """
    通过adb命令行截图，并以时间戳命名
    命令行例子:adb exec-out screencap -p > test.png
    """
    current_time = str(int(time.time()))
    result = os.system('adb exec-out screencap -p > img/' + current_time + '.png')
    if result == 0:
        print("截图成功")


def monitor_screen():
    """
    通过adb开启监听屏幕点击事件
    命令行例子:adb shell getevent
    """
    p = subprocess.Popen('adb shell getevent -l', shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    print('开始监听屏幕点击事件')
    while True:
        cmd_output = p.stdout.readline().decode()
        if "ABS_MT_POSITION_X" in cmd_output:
            print("存在屏幕点击事件")
            screen_cap()


# def delete_all_files():
#     """
#     删除指定img文件夹目录下的所有文件
#     """
#     del_list = os.listdir('img')
#     for f in del_list:
#         file_path = os.path.join('img', f)
#         if os.path.isfile(file_path):
#             os.remove(file_path)


if __name__ == '__main__':
    # pass
    print(monitor_screen())
