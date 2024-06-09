from ugot import ugot
import time
import math
import threading
import cv2
import numpy as np
camera_center_x = 320
#定义一个的类
class FaceAprilTag():
    #类的构造函数（init方法），用于初始化类的实例
    def __init__(self, ugot) -> None:
        self.u = ugot
        pass
      #找到标签，并且靠近它
    def find_apriltag_and_face_it(self, tagid):
        #获取标签信息
        tag = self.find_april_tag(tagid)
        #靠近标签
        self.approach_apriltag(tagid, tag)
        #获取标签信息
    def get_apriltag_total_info_by_id(self, tagid=0):
        a = self.u.get_apriltag_total_info()
        for info in a:
            id = info[0]
            if id == tagid:
                return info
        return None
       #检查并修正传入的角度值 degreey
    def check_degreey(self, degreey):
        if degreey < 90 and degreey > 0:
            degreey = 180 - degreey
        if degreey < 0 and degreey > -90:
            degreey = -180 - degreey

        if degreey < 0:
            degreey = -180 - degreey
        if degreey > 0:
            degreey = 180 - degreey
        return degreey
        #找到标签
    def find_april_tag(self, tagid=0):
        while True:
            #获取标签信息
            tag = self.get_apriltag_total_info_by_id(tagid)
            if tag is not None and tag[0] == tagid:
                id, center_x, center_y, height, width, area, distance5, distance7, distance10, x, y, z ,h,v= tag
                gap = camera_center_x - center_x
                print(f"gap to center is {gap}")
                if abs(gap) < 100:
                    self.u.mecanum_stop()
                    return tag
            self.u.mecanum_turn_speed(2, 20)
    #靠进标签
    def approach_apriltag(self, tagid, info):
        id, center_x, center_y, height, width, area, distance5, distance7, distance10, x, y, z ,h,v= info
        #距离*0.6是为了让小车靠进标签时，始终保持一段距离（避免考太进），round保留整数 abs求绝对值
        b=abs(round(distance5 * 100*0.6))
        if b>20:
            fd=round(b)
            #*100 是为了化单位 cm
            self.u.mecanum_move_speed_times(0, 20, b, 1)
            self.u.mecanum_stop()
            #获取标签信息
            info = self.get_apriltag_total_info_by_id(tagid)
            if info is None:
                #面对标签
                info = self.find_april_tag(tagid)
            id, center_x, center_y, height, width, area, distance5, distance7, distance10, x, y, z,h,v = info
        # 弧度转角度
        degreey = math.degrees(y)
        # 检查并修正角度值 degreey
        degreey = self.check_degreey(degreey)
        print("approach_apriltag", id, distance5, degreey)

        direct = 3 if degreey > 0 else 2
        direct_str = "右转" if degreey >0 else "左转"
        #计算变量y的正弦值
        siny = math.sin(y)
         #计算小车与标签的偏移量
        dist_offset = abs(int(siny * distance5 * 100))
        d = abs(int(degreey))
        #左转、右转操作
        if d > 0:
            print(f"approach_apriltag {direct_str}:{degreey}")
            self.u.mecanum_turn_speed_times(direct, 60, d, 2)
            self.u.mecanum_stop()
        
        left_right_flag = 90 if degreey < 0 else -90
        left_right_flag_str = "右移" if degreey < 0 else "左移"
        total_offset_dist = dist_offset
        #平移操作
        if abs(total_offset_dist) > 0:
            print(f"approach_apriltag {left_right_flag_str}:{total_offset_dist}")
            self.u.mecanum_translate_speed_times(left_right_flag, 30, total_offset_dist, 1)


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
u.load_models(["apriltag_qrcode"])
time.sleep(2)
base_angle2 = 90
base_angle3 = -80
# u.mechanical_joint_control(0, base_angle2, base_angle3, 200)
camera_stopped = False
#打开相机
def camera_test():
    u.open_camera()

    while not camera_stopped:
        #读取相机数据
        frame = u.read_camera_data()
        if frame is not None:
            nparr = np.frombuffer(frame, np.uint8)
            data = cv2.imdecode(nparr,cv2.IMREAD_COLOR)
            cv2.imshow('camera', data)
            cv2.waitKey(1)

def main():
    try:
        #创建线程
        t1 = threading.Thread(target=camera_test)
        t1.start()
        #实例化对象
        apriltag_tool = FaceAprilTag(u)
        apriltag_tool.find_apriltag_and_face_it(4)
    finally:
        global camera_stopped
        camera_stopped = True
        u.mecanum_stop()

if __name__ == "__main__":
    main()
