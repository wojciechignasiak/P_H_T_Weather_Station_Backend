# if install.sh not working try adding +x parameter:
# $ chmod +x install.sh
apt install git
apt install python3-pip
echo "++++Python3 with pip installation complete++++"
apt install curl
echo "++++Curl installation complete++++"
echo "++++Docker set up++++"
apt-get install \
    ca-certificates \
    curl \
    gnupg \
    lsb-release
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu \
  $(lsb_release -cs) stable" | tee /etc/apt/sources.list.d/docker.list > /dev/null
apt-get install docker-ce docker-ce-cli containerd.io
groupadd docker
usermod -aG docker $USER
curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
chmod +x /usr/local/bin/docker-compose
chmod 777 *
echo "++++Docker and Docker-Compose installation complete.++++"
echo "++++System has been prepared for PHT deployment++++"
echo "++++Please reboot your device to update users group”
