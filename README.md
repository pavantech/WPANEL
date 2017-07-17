# WPANEL
# WPANEL IS THE ANSIBLE GUI. Using WPANAL you can run the playbooks as group or single meachine.
# How to test this code
# this code will working only redhat family
# Before test the code make sure python, ansible, flask and git are need. If these softwares are not avilable on source meachine.
# follow the below steps
# yum install git
# git clone https://github.com/pavantech/Ansible_setup.git
# cd Ansible_setup
# sh setup.sh
# ansible --version
# git --version 
# python --V
# git clone https://github.com/pavantech/Ansible_Postgres.git
# cd Ansible_Postgres/centos/
# vi main.yml
# change  - host: localhost
# save
# create database in database name as ansible
# ansible-playbook main.yml
# git clone https://github.com/pavantech/WPANEL.git
# cd WPANEL
# python setup.py //this will install flask, request, postgres git using pip
# 
