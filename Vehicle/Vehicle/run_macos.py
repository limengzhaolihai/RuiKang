# import os
# import signal
# import time
# os.system('python3 ./FindLine.py')#寻线
# time.sleep(30)
# os.kill(os.getpid(), signal.SIGINT)
# # os.system('python ./NearColor.py')



import subprocess
import time
import signal
import os

# 使用绝对路径
find_line_script = '/Users/mac/Desktop/Vehicle/FindLine.py'
RotationFindColor = '/Users/mac/Desktop/Vehicle/RotationFindColor.py'
near_color_script = '/Users/mac/Desktop/Vehicle/NearColor1 2.py'
ArmTake = '/Users/mac/Desktop/Vehicle/ArmTake.py'
TagLocal = '/Users/mac/Desktop/Vehicle/TagLocal.py'
HighDesk1 = '/Users/mac/Desktop/Vehicle/HighDesk1.py'
HighDesk2 = '/Users/mac/Desktop/Vehicle/HighDesk2.py'
ArmPut = '/Users/mac/Desktop/Vehicle/ArmPut.py'
# 启动子进程
process = subprocess.Popen(['python3', find_line_script])
retcode = process.wait()
process.kill()
# # 等待一段时间（例如10秒）
# time.sleep(20)

# # 发送终止信号
# os.kill(process.pid, signal.SIGINT)  # 等价于按下 Ctrl+C

# 等待子进程处理信号并终止
# try:
#     process.wait(timeout=5)  # 给子进程一些时间来处理信号
# except subprocess.TimeoutExpired:
#     print("Process did not terminate in time, killing it")
#     process.kill()

# print("Subprocess has been terminated")
# process = subprocess.Popen(['python3', RotationFindColor])
# process.kill()
# 启动下一个子进程

# process.kill()
# time.sleep(7)
# 启动下一个子进程
process = subprocess.Popen(['python3', RotationFindColor])
retcode = process.wait()
process.kill()

process = subprocess.Popen(['python3', near_color_script])
retcode = process.wait()
process.kill()


process = subprocess.Popen(['python3', ArmTake])
retcode = process.wait()
process.kill()

process = subprocess.Popen(['python3', TagLocal])
retcode = process.wait()
process.kill()

process = subprocess.Popen(['python3', HighDesk1])
retcode = process.wait()
process.kill()

process = subprocess.Popen(['python3', ArmPut])
retcode = process.wait()
process.kill()