#!/bin/bash

printf "Starting Installation\n\n"
sudo apt update
sudo apt install -y openssh-server
sudo apt install -y curl cron
curl -fsSL https://pkgs.tailscale.com/stable/debian/bookworm.noarmor.gpg | sudo tee /usr/share/keyrings/tailscale-archive-keyring.gpg >/dev/null
curl -fsSL https://pkgs.tailscale.com/stable/debian/bookworm.tailscale-keyring.list | sudo tee /etc/apt/sources.list.d/tailscale.list
sudo apt-get update
sudo apt-get install tailscale
curl -fsSL https://download.docker.com/linux/debian/gpg | sudo gpg --yes --dearmor -o /etc/apt/keyrings/docker.gpg
curl -fsSL https://download.docker.com/linux/debian/gpg | sudo gpg --yes --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/debian bullseye stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
sudo apt update
sudo apt install -y docker-ce
sudo usermod -aG docker mobian
sudo apt install -y docker-compose
echo "echo 1500000 > /sys/class/power_supply/rk818-usb/input_current_limit" > /home/mobian/powerChange.sh && chmod 755 /home/mobian/powerChange.sh
cat <(sudo crontab -l) <(echo "* * * * * /home/mobian/powerChange.sh") | sudo crontab -
printf "\n\nInstallation Complete!\n\n"
