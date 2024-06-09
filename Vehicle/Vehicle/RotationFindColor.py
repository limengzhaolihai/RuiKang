from ugot import ugot

camera_center_x = 320
camera_center_y = 240
max_rotate_speed = 60
max_forward_speed = 60
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
u.load_models([ "color_recognition"])

class GrabObject():

    def __init__(self) -> None:
        #创建PID控制器
        self.pid_rotate_speed = u.create_pid_controller()
        #设置PID控制器参数
        self.pid_rotate_speed.set_pid(0.3, 0, 0.01)

        self.pid_forward_speed = u.create_pid_controller()
        self.pid_forward_speed.set_pid(0.9, 0, 0.001)

        self.gap = 0

    #
    def go_and_grap_object(self, target_color):
        start_y_speed = 0
        # 调整小车朝向
        self.adjust_direction(start_y_speed, target_color)

    # 计算小车原地转动的速度
    def get_rotate_speed(self, target_color):
        color_info = u.get_color_total_info()
        [color, type, target_center_x, target_center_y, height, width, area] = color_info
        if (
                len(color) == 0
                or len(type) == 0
                or target_center_x == -1
                or str(target_color) != color
        ):
            target_center_x = 460  #！
            return -60

        gap = target_center_x - camera_center_x
        #调用PID
        rotate_speed = round(self.pid_rotate_speed.update(gap))
        if rotate_speed > max_rotate_speed:
            rotate_speed = max_rotate_speed
        if rotate_speed < -max_rotate_speed:
            rotate_speed = -max_rotate_speed
        return rotate_speed

    # 调整小车朝向
    def adjust_direction(self, forward_speed, target_color):
        #获取小车旋速度
        rotate_speed = self.get_rotate_speed(target_color)
        while abs(rotate_speed) > 3:
            u.mecanum_move_xyz(0, forward_speed, int(rotate_speed))
            # 计算小车原地转动的速度
            rotate_speed = self.get_rotate_speed(target_color)


if __name__ == "__main__":

    u.mecanum_move_speed_times(0, 20, 40, 1)
    grab_object = GrabObject()
    target_color="蓝色"
    grab_object.go_and_grap_object(target_color)
