from ugot import ugot
import time
import threading
# import cv2
# import numpy as np
camera_center_x = 320
camera_center_y = 240
max_rotate_speed = 60
base_angle2 = 90
base_angle3 = -80

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
u.load_models(["line_recognition"])#这个如果再加载一个颜色识别模型是会报错的 所以需要分开去加载
time.sleep(2)
u.set_track_recognition_line(0)
# 创建PID控制器。
pid_turn = u.create_pid_controller()
# 设置PID参数
pid_turn.set_pid(0.2, 0.001, 0)
offset = 0
# u.load_models(['color_recognition'])
var = 1
camera_stopped = False
def check_time():
    global var
    print("开始检测异常路口")
    while True:
        if var == 0:
            print("正在走曲线")
            # time.sleep(4)
            # time.sleep(4)
            time.sleep(2)
            var = 1
            print("------")
            print("------")
            break

# def camera_test():
#     u.open_camera()
#     while not camera_stopped:
#         frame = u.read_camera_data()
#         if frame is not None:
#               nparr = np.frombuffer(frame, np.uint8)
#               data = cv2.imdecode(nparr,cv2.IMREAD_COLOR)
#               cv2.imshow('camera', data)
#               cv2.waitKey(1)


def main():
    control = MoveControl()
    t2 = threading.Thread(target=check_time)#检测异常路口的线程
    t2.start()
   
    try:
        # 控制小车前进
        t1 = threading.Thread(target=control.forward)
        t1.start()
        t1.join()
        t2.join()
    finally:
        control.mecanum_stop()
    # u.mecanum_move_speed_times(0, 20, 40, 1)
class MoveControl:
    def __init__(self) -> None:
        # 前进速度
        self.forward_speed = 26
        # 索引
        self.intersection_index = -1
        # 路口标志
        self.is_cross = False
        # u.mechanical_joint_control(0, base_angle2, base_angle3, 200)
        
    def mecanum_stop(self):
        u.mecanum_stop()

    # 计算小车原地转动的速度
    def get_rotate_speed(self, check_cross=False):
        line_info = u.get_single_track_total_info()
        print(line_info)

        offset, line_type, x, y = line_info

        old_is_cross = self.is_cross

        self.is_cross = line_type == 2 or line_type == 3

        if line_type == 2 or line_type == 3:
            print(line_info)
        if line_type == 0:
            return 0, line_type, 0, 0
        # 调用PID
        rotate_speed = round(pid_turn.update(offset))
        print("offset=", offset)
        if rotate_speed > max_rotate_speed:
            rotate_speed = max_rotate_speed
        if rotate_speed < -max_rotate_speed:
            rotate_speed = -max_rotate_speed
        return rotate_speed, line_type, x, y

    # 控制小车前进
    def forward(self):
        global var
        i=1
        while True:
            old_is_cross = self.is_cross
            # 获取旋转速度
            speed_info = self.get_rotate_speed()
            
            rotate_speed, line_type, x, y = speed_info
            new_is_cross = self.is_cross

            if old_is_cross and not new_is_cross:
                print(var)
                i=1
                if var == 1:
                    u.mecanum_move_speed_times(0, 14, 14, 1)  # 直线行驶距离20cm
                    u.mecanum_turn_speed_times(3, 100, 90, 2)  # 进行右转
                    if self.intersection_index == -1:
                        var = 0

                    self.intersection_index = self.intersection_index + 1
                    print(f"------------------------路口计数增加，序号：{self.intersection_index + 1}, 坐标x:{x}, y:{y}------------------------")
                    if self.intersection_index >= 5:
                        u.mecanum_stop()
                        s = f"识别到第{str(self.intersection_index+1)}个路口，没有定义控制逻辑，停止"
                        u.play_audio_tts(s, 0, True)
                        break

                    print(f"已顺利通过第{str(self.intersection_index + 1)}个路口")

            if self.intersection_index == 5 - 1:
                self.mecanum_stop()
                s = f"已经处理完{str(self.intersection_index+1)}个路口，终止本次巡线"
                u.play_audio_tts(s, 0, True)
                return
            
            if line_type == 0:
                u.mecanum_stop()
                print("没有识别到线,停止")
                i=i+1
                if i>10:
                    break
                # u.mecanum_move_speed_times(0, 20, 20, 1)  # 直线行驶距离20cm
                continue
            # 巡线前进
            u.mecanum_move_xyz(0, self.forward_speed, -int(rotate_speed))

if __name__ == "__main__":
    main()
