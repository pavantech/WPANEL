# WPANEL
# WPANEL is  ANSIBLE GUI. Using WPANAL you can run the playbooks as group or single meachine.
# How to test this code.
# This code will working only redhat family
# Before test the code make sure python, ansible, flask and git are need. If these softwares are not avilable on source meachine.
# Please follow the below steps
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
# create database in database name as ansible (any name)
# ansible-playbook main.yml
# git clone https://github.com/pavantech/WPANEL.git
# cd WPANEL
# python setup.py //this will install flask, request, postgres git using pip
# Next please update src/database.ini file
# Database credentials are needed.
# python index.py
# http://ipaddress:5000/
# username name as admin and password admin
# please test this code on redhat family
