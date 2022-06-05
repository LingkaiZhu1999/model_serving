#! /bin/bash

repository="https://github.com/onuryuxcodes/openstack-client.git"

echo Cloning git repo of Ansible Client
git clone "$repository"

KEY_DESTINATION="/home/ubuntu/cluster-keys"
ssh-keygen -t rsa -f $KEY_DESTINATION

sudo apt-get update -y
sudo apt-get upgrade -y
sudo apt-add-repository ppa:ansible/ansible -y
sudo apt-get update -y
sudo apt install ansible -y