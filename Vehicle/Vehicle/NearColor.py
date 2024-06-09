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

# 创建PID控制器
pid_forward_speed = u.create_pid_controller()
# 设置PID控制参数
pid_forward_speed.set_pid(0.9, 0, 0.001)

# 计算前进速度（负数就表示后退速度）
def get_forward_speed(dis):
    # 调用PID
    forward_speed = round(pid_forward_speed.update(dis))
    if forward_speed > max_forward_speed:
        forward_speed = max_forward_speed
    if forward_speed < -max_forward_speed:
        forward_speed = -max_forward_speed
    print("forward_speed:", forward_speed)
    return forward_speed

# 靠近目标
def reach_target(target_color):
    
    while True:
        color_info = u.get_color_total_info()
        print(color_info)
        [color, type, target_center_x, target_center_y, height, width, area] = color_info

        if color == target_color:
            print("目标颜色已识别")
            
            

            # 获取当前距离并打印
            initial_distance = u.read_distance_data(21)
            print(f"Initial distance to target color ({target_color}):", initial_distance)

            # 计算目标距离
            target_distance = int(initial_distance-5 )
        #    print(f"Target distance to move: {target_distance}")
            
           # 按里程前进/后退
            u.mecanum_move_speed_times(0, target_distance, target_distance, 1)
            # u.mecanum_move_speed(0, abs(forward_speed))
            print(target_distance)
            final_distance = u.read_distance_data(21)
            
            print(f"Final distance to target color ({target_color}):", final_distance)
            break
        else:
            u.mecanum_stop()

if __name__ == "__main__":
    # u.mecanum_move_speed_times(0, 20, 40, 1)
    target_color = Color.RED
    print(target_color)
    reach_target(target_color)