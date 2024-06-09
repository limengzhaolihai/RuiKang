from ugot import ugot
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
    distance = u.read_distance_data(21)
    print("distance:", distance)
    dis=8 - distance
    #调用PID
    forward_speed = round(pid_forward_speed.update(dis))
    if forward_speed > max_forward_speed:
        forward_speed = max_forward_speed
    if forward_speed < -max_forward_speed:
        forward_speed = -max_forward_speed
    print("forward_speed:", forward_speed)
    return forward_speed

# 靠近目标
def reach_target(target_color):
    forward_speed = 10
    falg=True
    while falg:
        color_info = u.get_color_total_info()
        print(color_info)
        [color, type, target_center_x, target_center_y, height, width, area] = color_info
        if (
            len(color) == 0
            or len(type) == 0
            or target_center_x == -1
            or str(target_color) != color
        ):
            u.mecanum_stop()
        else:
            falg=False
    while abs(forward_speed) > 1:
        direction = 0 if forward_speed > 0 else 1
        print("direction:", direction)
        u.mecanum_move_speed(direction, abs(forward_speed))
        #获取小车前进速度
        forward_speed = get_forward_speed(target_color)

    u.mecanum_stop()

if __name__ == "__main__":

    target_color=Color.BLUE
    reach_target(target_color)
