import subprocess
import os

# 定义脚本的绝对路径
scripts = [
    # r'C:\Users\lenovo\Desktop\Vehicle\Vehicle\FindLine.py',
    r'C:\Users\lenovo\Desktop\Vehicle\Vehicle\RotationFindColor.py',
    r'C:\Users\lenovo\Desktop\Vehicle\Vehicle\NearColorDemo.py',
    r'C:\Users\lenovo\Desktop\Vehicle\Vehicle\ArmTake.py',
    r'C:\Users\lenovo\Desktop\Vehicle\Vehicle\TagLocal.py',
    r'C:\Users\lenovo\Desktop\Vehicle\Vehicle\HighDesk1.py',
    # r'C:\Users\lenovo\Desktop\Vehicle\Vehicle\HighDesk2.py',
    r'C:\Users\lenovo\Desktop\Vehicle\Vehicle\ArmPut.py',
]

# 配置文件的目录
config_directory = r'C:\Users\lenovo\Desktop\Vehicle\Vehicle'

# 运行脚本的函数
def run_script(script_path):
    process = subprocess.Popen(
        ['python', script_path],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        cwd=config_directory  # 设置工作目录
    )
    try:
        stdout, stderr = process.communicate()
        print(f"Output from {script_path}:\n{stdout}")
        if stderr:
            print(f"Errors from {script_path}:\n{stderr}")
        if process.returncode != 0:
            print(f"Script {script_path} exited with code {process.returncode}")
    except Exception as e:
        print(f"An error occurred while running the script {script_path}: {e}")
    finally:
        process.kill()

# 依次运行每个脚本
for script in scripts:
    run_script(script)

print("All scripts have been run.")
