from ugot import ugot
import time

def read_config(filename):
    config = {}
    with open(filename, 'r') as file:
        for line in file:
            key, value = line.strip().split('=')
            config[key] = value
    return config

config = read_config('config.txt')
# print(config['ip_address'])
got = ugot.UGOT()
# 初始化设备
got.initialize(config['ip_address'])

# 打开夹手
# got.mechanical_single_joint_control(3,-90,0)#控制一个关节的角度
# got.mechanical_clamp_release()
# got.mechanical_clamp_close()
print('-----1:',got.mechanical_get_clamp_status())
time.sleep(1)