#!/bin/bash

printf "Starting Installation"

printf "\n\nAdd deb repo for tailscale..."
curl -fsSL https://pkgs.tailscale.com/stable/debian/bookworm.noarmor.gpg | sudo tee /usr/share/keyrings/tailscale-archive-keyring.gpg > /dev/null
curl -fsSL https://pkgs.tailscale.com/stable/debian/bookworm.tailscale-keyring.list | sudo tee /etc/apt/sources.list.d/tailscale.list > /dev/null
printf "complete"

printf "\n\nAdd deb repo for docker..."
curl -fsSL https://download.docker.com/linux/debian/gpg | sudo gpg --yes --dearmor -o /etc/apt/keyrings/docker.gpg
curl -fsSL https://download.docker.com/linux/debian/gpg | sudo gpg --yes --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/debian bullseye stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
printf "complete"

printf "\n\nInstall packages..."
sudo apt update
sudo apt install -y curl cron openssh-server tailscale docker-ce docker-compose

printf "\n\nDocker user setup..."
sudo usermod -aG docker mobian
printf "complete"

printf "\n\nAdd cron job to increase charging limit..."
cat <(echo "* * * * * echo 1500000 > /sys/class/power_supply/rk818-usb/input_current_limit") | sudo crontab -
printf "complete"

printf "\n\nTailscale setup started\n"
sudo tailscale up
printf "Tailscale setup complete"

printf "\n\nInstallation Complete!"
printf "\n\nLog out/in to complete docker user setup.\n\n"