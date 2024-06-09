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




# got = ugot.UGOT()
# # 初始化设备
# got.initialize('192.168.96.221')

# 打开夹手
got.mechanical_clamp_release()
print('-----1:',got.mechanical_get_clamp_status())
time.sleep(1)



# # 机械臂复位
# got.mechanical_arms_restory()

# 关节角度控制
# got.mechanical_joint_control(0, 0, 0, 500)#控制三个关节的角度
# got.mechanical_single_joint_control(2,60,2000)
# 移动位置
# got.mechanical_joint_control(0, 0, 0, 500)
# got.mechanical_move_axis(20, 12, 0, 1000)
# got.mechanical_move_axis(20, 10, 30, 1000)## 移动位置
# while True:
# got.mechanical_single_joint_control(2,120,4000)#控制一个关节的角度
# got.mechanical_single_joint_control(3,90,4000)#控制一个关节的角度
# got.mechanical_single_joint_control(1,-90,5000)#控制一个关节的角度
# time.sleep(3)
i=1
while i<2:
    got.mechanical_single_joint_control(2,120,4000)#控制一个关节的角度
    time.sleep(1)
    i=i+1
# got.mechanical_single_joint_control(2,130,2000)#控制一个关节的角度
# got.mechanical_single_joint_control(2,130,2000)#控制一个关节的角度
# got.mechanical_joint_control(20, 60, 80, 2000)

#关节2是110
# 闭合夹手
got.mechanical_clamp_close()
print('-----2:',got.mechanical_get_clamp_status())
# time.sleep(1)
got.mechanical_single_joint_control(2,90,5000)#控制一个关节的角度
time.sleep(3.5)
# got.mechanical_arms_restory()

# got.mechanical_move_axis(20, -5, 1, 2000)
# got.mechanical_single_joint_control(2,60,2000)
