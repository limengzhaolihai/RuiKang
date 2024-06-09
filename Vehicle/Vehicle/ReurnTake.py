#左转 寻线 左转
from ugot import ugot
import time

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
u.load_models(["line_recognition"])
time.sleep(2)
u.set_track_recognition_line(0)
#创建PID控制器。
pid_turn = u.create_pid_controller()
#设置PID参数
pid_turn.set_pid(0.2, 0.001, 0)
offset=0

def main():

    control = MoveControl()
    try:
        #控制小车前进
        control.forward()
            
    finally:
        control.mecanum_stop()

class MoveControl:
    def __init__(self) -> None:
         #前进速度
        self.forward_speed = 26
         #索引
        self.intersection_index = -1
         #路口标志
        self.is_cross = False
        # u.mechanical_joint_control(0, base_angle2, base_angle3, 200)#这块会导致机械臂复位
        
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
        #调用PID
        rotate_speed = round(pid_turn.update(offset))
        print("offset=",offset)
        if rotate_speed > max_rotate_speed:
            rotate_speed = max_rotate_speed
        if rotate_speed < -max_rotate_speed:
            rotate_speed = -max_rotate_speed
        return rotate_speed, line_type, x, y

    #控制小车前进
    def forward(self):
        i=1
        while True:
            old_is_cross = self.is_cross
            #获取旋转速度
            speed_info = self.get_rotate_speed()

            rotate_speed, line_type, x, y = speed_info
            new_is_cross = self.is_cross

            if old_is_cross and not new_is_cross:
                i=1
                if self.intersection_index==1:
                    u.mecanum_move_speed_times(0, 10, 10, 1)  # 直线行驶距离20cm
                    print("终止运行")
                    break
                u.mecanum_move_speed_times(0, 20, 20, 1)
                # u.mecanum_move_speed(0, 10)
                # time.sleep(1)
                u.mecanum_turn_speed_times(2,100,90,2)
                self.intersection_index = self.intersection_index + 1
                print(f"------------------------路口计数增加，序号：{self.intersection_index + 1}, 坐标x:{x}, y:{y}------------------------")
                if  self.intersection_index >= 5:
                    u.mecanum_stop()
                    s = f"识别到第{str(self.intersection_index+1)}个路口，没有定义控制逻辑，停止"

                    u.play_audio_tts(s, 0, True)
                    break

                print(f"已顺利通过第{str(self.intersection_index + 1)}个路口")

            if self.intersection_index == 5 - 1 :
                self.mecanum_stop()
                s = f"已经处理完{str(self.intersection_index+1)}个路口，终止本次巡线"
                u.play_audio_tts(s, 0, True)
                return
            
            if line_type == 0:
                # 没有识别到线,停止
                # u.mecanum_move_xyz(0, 3, -int(rotate_speed))
                u.mecanum_stop()
                i=i+1
                if i>10:
                    break
                print("没有识别到线,停止")
                continue
            # 巡线前进
            u.mecanum_move_xyz(0, self.forward_speed, -int(rotate_speed))
            
if __name__ == "__main__":
    u.mecanum_move_speed_times(1,20,40,1)
    u.mecanum_turn_speed_times(2, 40, 200, 2)#掉头
    main()
    
