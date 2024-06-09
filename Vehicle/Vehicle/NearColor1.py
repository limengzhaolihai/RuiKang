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
u.load_models(["color_recognition"])
u.show_light_rgb_effect(255, 100, 100, 0)

max_forward_speed = 40




#创建PID控制器
pid_forward_speed = u.create_pid_controller()
#设置PID控制参数
pid_forward_speed.set_pid(0.9, 0, 0.001)

# 计算前进速度（负数就表示后退速度）
def get_forward_speed(target_color):
    #获取传感器数据
    distance = u.read_distance_data(21)#传感器读取数据
    print("distance:", distance)
    dis=8 - distance
    #调用PID
    forward_speed = round(pid_forward_speed.update(dis))
    if forward_speed > max_forward_speed:
        forward_speed = max_forward_speed
    if forward_speed < -max_forward_speed:
        forward_speed = -max_forward_speed
    print("forward_speed:", forward_speed)
    return distance

# 靠近目标
def reach_target(target_color):
    forward_speed =40
    i=1
    falg=True
    while True:
        color_info = u.get_color_total_info()
        print(color_info)
        [color, type, target_center_x, target_center_y, height, width, area] = color_info
        i=i+1
        if i>10:
             break
        if color == target_color:
                i=0
                print("1111")
                u.mecanum_move_speed(0, abs(forward_speed))
                    
                #获取小车前进速度
                a = get_forward_speed(target_color)
                if  width>180:
                      u.mecanum_stop()
                      break
                forward_speed=30
      
            
        else:
            # if (
            #     len(color) == 0
            #     or len(type) == 0
            #     or target_center_x == -1
            #     or str(target_color) != color
            #     ):
                # u.mecanum_move_turn(30, 40, 3, 100)
                u.mecanum_stop()
                # u.mecanum_move_turn(30, 40, 3, 100)
            # break
       # 加一些逻辑旋转一定的角度去抓块

     
    # while abs(forward_speed) > 1:
    #     direction = 0 if forward_speed > 0 else 1
    #     print("direction:", direction)
    #     u.mecanum_move_speed(direction, abs(forward_speed))
    #     #获取小车前进速度
    #     forward_speed = get_forward_speed(target_color)

    u.mecanum_stop()

if __name__ == "__main__":
    # u.mecanum_move_turn(45, 20, 2, 40)
    # time.sleep(2)
    # u.mecanum_move_turn(2, 40, 3, 100)
    u.mecanum_turn_speed_times(3, 10, 1, 0)
    # u.mecanum_turn_speed_times(2, 40, 200, 2)#掉头
    # time.sleep(2)
    target_color=Color.RED
    print(target_color)
    reach_target(target_color)
