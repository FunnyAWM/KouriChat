import subprocess
import time

import pyautogui


# 尝试导入Linux上的窗口和鼠标控制库

def find_wechat_window():
    """查找微信窗口"""
    try:
        # 使用wmctrl命令查找微信窗口
        result = subprocess.run(['wmctrl', '-l'], capture_output=True, text=True)
        if result.returncode != 0:
            print("未找到wmctrl命令，请安装: sudo apt-get install wmctrl")
            return None
        
        # 在窗口列表中查找微信
        lines = result.stdout.strip().split('\n')
        for line in lines:
            if '微信' in line or 'WeChat' in line:
                # 提取窗口ID（第一列）
                window_id = line.split()[0]
                return window_id
        
        # 如果没找到中文的，尝试查找英文版本
        for line in lines:
            if 'wechat' in line.lower():
                window_id = line.split()[0]
                return window_id
                
        return None
    except Exception as e:
        print(f"查找微信窗口时出错: {str(e)}")
        return None


def get_window_geometry(window_id):
    """获取窗口几何信息"""
    try:
        result = subprocess.run(['xwininfo', '-id', window_id], capture_output=True, text=True)
        if result.returncode != 0:
            return None
        
        lines = result.stdout.split('\n')
        x, y, width, height = 0, 0, 0, 0
        
        for line in lines:
            if 'Absolute upper-left X:' in line:
                x = int(line.split(':')[1].strip())
            elif 'Absolute upper-left Y:' in line:
                y = int(line.split(':')[1].strip())
            elif 'Width:' in line:
                width = int(line.split(':')[1].strip())
            elif 'Height:' in line:
                height = int(line.split(':')[1].strip())
        
        return x, y, width, height
    except Exception as e:
        print(f"获取窗口几何信息时出错: {str(e)}")
        return None


def activate_window(window_id):
    """激活窗口"""
    try:
        # 使用wmctrl激活窗口
        subprocess.run(['wmctrl', '-i', '-a', window_id], check=False)
        time.sleep(0.3)
        
        # 尝试将窗口移到前台
        subprocess.run(['wmctrl', '-i', '-R', window_id], check=False)
        time.sleep(0.2)
        
        return True
    except Exception as e:
        print(f"激活窗口时出错: {str(e)}")
        return False


def click_wechat_buttons():
    """Linux版本的微信登录点击器"""
    # 查找微信窗口
    window_id = find_wechat_window()
    if not window_id:
        print("找不到微信登录窗口")
        print("请确保微信已经启动并且登录窗口可见")
        return False
    
    print(f"找到微信窗口: {window_id}")
    
    # 获取窗口位置和大小
    geometry = get_window_geometry(window_id)
    if not geometry:
        print("无法获取微信窗口的位置信息")
        return False
    
    x, y, width, height = geometry
    print(f"窗口位置: ({x}, {y}), 大小: {width}x{height}")
    
    # 激活窗口
    activated = activate_window(window_id)
    if not activated:
        print("警告: 无法确认微信窗口已成功激活，但将继续尝试点击")
    
    # 设置PyAutoGUI的安全设置
    pyautogui.FAILSAFE = True  # 移动鼠标到屏幕角落可以停止程序
    pyautogui.PAUSE = 0.2  # 每次操作间暂停
    
    try:
        # 点击确认按钮（窗口中心偏下位置）
        confirm_x = x + width // 2
        confirm_y = y + height * 3 // 4
        
        print(f"点击确认按钮位置: ({confirm_x}, {confirm_y})")
        pyautogui.click(confirm_x, confirm_y)
        time.sleep(0.5)  # 等待确定按钮响应
        
        # 再次激活窗口
        activate_window(window_id)
        time.sleep(0.2)
        
        print("微信登录点击操作完成")
        return True
        
    except Exception as e:
        print(f"执行点击操作时出错: {str(e)}")
        return False

if __name__ == "__main__":
    click_wechat_buttons()