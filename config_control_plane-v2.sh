#!/bin/bash

{

sudo apt update
sudo apt install -y docker.io apt-transport-https curl gnupg
curl -s https://packages.cloud.google.com/apt/doc/apt-key.gpg | sudo apt-key add -

#sudo sh -c "echo deb https://apt.kubernetes.io/ kubernetes-xenial main > /etc/apt/sources.list.d/kubernetes.list"
#cat /etc/apt/sources.list.d/kubernetes.list

sudo mkdir /etc/apt/keyrings
curl -fsSL https://pkgs.k8s.io/core:/stable:/v1.28/deb/Release.key | sudo gpg --dearmor -o /etc/apt/keyrings/kubernetes-apt-keyring.gpg
echo 'deb [signed-by=/etc/apt/keyrings/kubernetes-apt-keyring.gpg] https://pkgs.k8s.io/core:/stable:/v1.28/deb/ /' | sudo tee /etc/apt/sources.list.d/kubernetes.list


sudo apt-get update
sudo apt-get install -y kubelet=1.28.4-1.1 kubeadm=1.28.4-1.1 kubectl=1.28.4-1.1
sudo apt-mark hold kubelet kubeadm kubectl

sudo swapoff -a
sudo sed -i '/ swap / s/^\(.*\)$/#\1/g' /etc/fstab

sudo modprobe overlay
sudo modprobe br_netfilter

sudo tee /etc/sysctl.d/kubernetes.conf <<EOF
net.bridge.bridge-nf-call-iptables = 1
net.ipv4.ip_forward = 1
net.ipv4.conf.all.forwarding = 1
net.ipv6.conf.default.forwarding = 1
net.ipv6.conf.all.forwarding=1
EOF

sudo sysctl --system

sudo sh -c "echo {                                                  >  /etc/docker/daemon.json"
sudo sh -c 'echo \"exec-opts\": [\"native.cgroupdriver=systemd\"]  >>  /etc/docker/daemon.json'
sudo sh -c "echo }                                                 >>  /etc/docker/daemon.json"


sudo systemctl enable docker
sudo systemctl daemon-reload
sudo systemctl restart docker

}   2>&1 | tee -a config_control_plane.log
