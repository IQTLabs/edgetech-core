#!/bin/bash

# Fetch current username
CURRENT_USER=$(whoami)

printf "Starting Installation"
sudo apt-get update
sudo apt-get install ca-certificates curl gnupg cron openssh-server 

printf "\n\nAdd deb repo and install tailscale..."
curl -fsSL https://pkgs.tailscale.com/stable/raspbian/bookworm.noarmor.gpg | sudo tee /usr/share/keyrings/tailscale-archive-keyring.gpg > /dev/null
curl -fsSL https://pkgs.tailscale.com/stable/raspbian/bookworm.tailscale-keyring.list | sudo tee /etc/apt/sources.list.d/tailscale.list
sudo apt update
sudo apt install -y tailscale 
printf "complete"


printf "\n\nDocker install and setup..."
curl -sSL https://get.docker.com | sh
sudo usermod -aG docker $CURRENT_USER
printf "complete"

printf "\n\nTailscale setup started\n"
sudo tailscale up
printf "Tailscale setup complete"

printf "\n\nInstallation Complete!"
printf "\n\nLog out/in to complete docker user setup.\n\n"
