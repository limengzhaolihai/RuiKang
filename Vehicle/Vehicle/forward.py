from ugot import ugot
import time
class Color:
    GREEN = "绿色"
    BLUE = "蓝色"
    PURPLE = "紫色"
    RED = "红色"
    UN_SET = "未设置"

def read_config(filename):
    config = {}
    with open(filename, 'r') as file:
        for line in file:
            key, value = line.strip().split('=')
            config[key] = value
    return config

config = read_config('config.txt')
# print(config['ip_address'])

u = ugot.UGOT()
u.initialize(config['ip_address'])

u.mecanum_move_speed_times(1,20,10,1)