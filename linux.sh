#!/bin/bash

# Script gửi IP lên Telegram khi máy khởi động, chỉ gửi nếu IP thay đổi

# Lấy địa chỉ IPv4
IP=$(ip addr show eth0 | grep 'inet ' | awk '{print $2}' | cut -d/ -f1)
DEVICE_NAME=$(hostname)
USER_NAME=$(whoami)

# File lưu IP cũ để kiểm tra thay đổi
IP_FILE="/tmp/last_ip.txt"

# Kiểm tra nếu IP đã thay đổi mới gửi
if [ ! -f "$IP_FILE" ] || [ "$IP" != "$(cat $IP_FILE)" ]; then
    # Lưu IP mới vào file
    echo "$IP" > "$IP_FILE"

    # Thông tin bot và chat_id
    bot_token="7318734370:AAGCyDSFwsb4Ln3DHn9y9FnzDfPWiq_1YxA"
    chat_id="7447164672"

    # Gửi thông tin qua Telegram
    curl -s -X POST "https://api.telegram.org/bot$bot_token/sendMessage" \
         -d chat_id=$chat_id \
         -d text="Tên thiết bị: $DEVICE_NAME\nTên người dùng: $USER_NAME\nĐịa chỉ IP: $IP"
fi

# Tạo systemd service để chạy script khi khởi động (chỉ chạy một lần)
SERVICE_FILE="/etc/systemd/system/ip_notify.service"
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

    # Kích hoạt service nếu chưa được kích hoạt
    if ! systemctl is-enabled ip_notify.service > /dev/null 2>&1; then
        sudo systemctl daemon-reload
        sudo systemctl enable ip_notify.service
    fi
fi
