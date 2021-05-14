from serial.serialutil import SerialException
from threading import Thread
from django_redis import get_redis_connection
from app.utils.tools import create_lighting_usage_record

import time
import serial
import logging


redis_conn = get_redis_connection('default')  # 获取redis连接

receive_flag = True    # 串口数据接收标志


connect = serial.Serial()  # 串口连接对象
connect.port = 'COM3'
connect.baudrate = 9600
connect.timeout = 0.5


def receive():
    while receive_flag:
        size = connect.in_waiting
        if size:
            recv_byte = connect.read(size)
            print("Receive data：", recv_byte)
            save_data(recv_byte)
            continue
        time.sleep(0.4)


def save_data(recv_byte):
    # 设备名称
    device_name = 'ILD001'

    head_list, data_list = list(), list()
    receive_string = bytes.decode(recv_byte)
    receive_list = receive_string.split('+')
    receive_list.remove('')
    receive_list.reverse()

    for index, value in enumerate(receive_list):
        value_list = value.split('|')
        head_list.insert(index, value_list[0])
        data_list.insert(index, value_list[1])

    # 处理接收过来的数据并存入redis缓存
    if 'all_status' in head_list:
        index = head_list.index('all_status')
        redis_conn.set('LORA_RECEIVE_ALL_STATUS_DATA', data_list[index])

    if 'switch_status' in head_list:
        moment = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
        index = head_list.index('switch_status')

        if int(data_list[index]):
            redis_conn.set('LORA_RECEIVE_SWITCH_OPEN_STATUS_DATA', moment)
        else:
            open_time = redis_conn.get('LORA_RECEIVE_SWITCH_OPEN_STATUS_DATA')

            # 开启时刻
            open_time = time.strptime(open_time, '%Y-%m-%d %H:%M:%S')
            # 关闭时刻
            close_time = time.strptime(moment, '%Y-%m-%d %H:%M:%S')
            # 历时秒数
            duration = int(time.mktime(close_time) - time.mktime(open_time))

            open_time = time.strftime('%Y-%m-%d %H:%M:%S', open_time)
            close_time = moment

            create_dict = {'DeviceName': device_name, 'OpenTime': open_time,
                           'CloseTime': close_time, 'Duration': duration}
            create_lighting_usage_record(create_dict)


def open_uart():
    if not connect.is_open:
        connect.open()


def close_uart():
    if connect.is_open:
        connect.close()


def send(method, explain, value):
    if method == 'post':
        value = f'+{explain}|{value}\n'
    elif method == 'get':
        value = f'-{explain}|{value}\n'
    else:
        return
    connect.write(value.encode('utf-8'))


logger = logging.getLogger('uart')
handler = logging.StreamHandler()
handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(levelname)s：%(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)


try:
    connect.open()
    logger.warn('UART module started successfully.')
    # 创建Uart线程
    uart_thread = Thread(target=receive, daemon=True)
    uart_thread.start()
except SerialException as e:
    logger.error('UART module failed to start !!!')


if __name__ == '__main__':
    receive()
