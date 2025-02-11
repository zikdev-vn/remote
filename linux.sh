#!/bin/bash

# Lấy địa chỉ IP của máy
IP=$(ip addr show eth0 | grep 'inet ' | awk '{print $2}' | cut -d/ -f1)
DEVICE_NAME=$(hostname)
USER_NAME=$(whoami)

# Thông tin bot Telegram
bot_token="7318734370:AAGCyDSFwsb4Ln3DHn9y9FnzDfPWiq_1YxA"
chat_id="7447164672"

# Gửi thông tin qua Telegram
curl -s -X POST "https://api.telegram.org/bot$bot_token/sendMessage" \
     -d chat_id=$chat_id \
     -d text="Tên thiết bị: $DEVICE_NAME\n:  Tên người dùng: $USER_NAME\n:   Địa chỉ IP: $IP"

# Tạo và cài đặt service systemd để tự động chạy script khi khởi động lại
SERVICE_FILE="/etc/systemd/system/ip_notify.service"

# Kiểm tra xem file service đã tồn tại chưa
if [ ! -f "$SERVICE_FILE" ]; then
    echo "[Unit]" | sudo tee $SERVICE_FILE > /dev/null
    echo "Description=Send IP to Telegram on boot" | sudo tee -a $SERVICE_FILE > /dev/null
    echo "After=network.target" | sudo tee -a $SERVICE_FILE > /dev/null
    echo "" | sudo tee -a $SERVICE_FILE > /dev/null
    echo "[Service]" | sudo tee -a $SERVICE_FILE > /dev/null
    echo "ExecStart=$(realpath $0)" | sudo tee -a $SERVICE_FILE > /dev/null
    echo "Type=oneshot" | sudo tee -a $SERVICE_FILE > /dev/null
    echo "RemainAfterExit=true" | sudo tee -a $SERVICE_FILE > /dev/null
    echo "User=root" | sudo tee -a $SERVICE_FILE > /dev/null
    echo "" | sudo tee -a $SERVICE_FILE > /dev/null
    echo "[Install]" | sudo tee -a $SERVICE_FILE > /dev/null
    echo "WantedBy=multi-user.target" | sudo tee -a $SERVICE_FILE > /dev/null

    # Kích hoạt service
    sudo systemctl daemon-reload
    sudo systemctl enable ip_notify.service
    echo "Service systemd đã được cài đặt và kích hoạt."
else
    echo "Service systemd đã tồn tại, không cần cài đặt lại."
fi
