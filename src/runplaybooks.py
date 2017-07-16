from distutils.dir_util import copy_tree
from connect import connect
import os
import shutil
import time

class runplaybooks(object):

    def __init__(self):
        self._rolelist = []
        self._groupname=[]
        self._consolelist=[]

    def runplaybookgroup(self, groupname, rolelist):
           owd = os.getcwd()
           dir="rundir"+str(time.strftime("%Y-%m-%d%H:%M:%S"))
           if not os.path.exists(dir):
                  os.makedirs(dir)
           if not os.path.exists('log'):
                  os.makedirs('log')
           if not os.path.exists(dir+'/roles/'):
                  os.makedirs(dir+'/roles/')
           conn,cur=connect()
           cur.execute("SELECT * FROM hostlist where groupname='%s'"%groupname[0])
           srcfile = 'external/plugins/Ansible_Playbook/ansible.cfg'
           dstroot = dir
           shutil.copy(srcfile, dstroot)
           #for list1 in cur.fetchall():
           #   print("biglist"+list1[1]+""+list1[2])
           for role in rolelist:
              if not os.path.exists(dir+'/roles/'+role):
                       os.makedirs(dir+'/roles/'+role)
              src = 'external/plugins/Ansible_Playbook/'+role
              dst = dir+'/roles/'+role
              copy_tree(src,dst)
           f = open(dir+'/hosts', 'a')
           f.write("["+groupname[0]+"]\n")
           for list1 in cur.fetchall():      
               f.write(""+ list1[1] +"  ansible_ssh_user="+ list1[2] +"  ansible_ssh_pass="+ list1[3] +"\n")
           f.close()
           f = open(dir+'/main.yml', 'a')
           f.write("- hosts: "+groupname[0]+"\n")
           f.write("  roles: \n")
           for rolename in rolelist:
               f.write("    - {role: "+ rolename +", become: true} \n")
           f.close()
           return dir

    def runplaybookhost(self, hostname, rolelist):
           owd = os.getcwd()
           dir="rundir"+str(time.strftime("%Y-%m-%d%H:%M:%S"))
           if not os.path.exists(dir):
                  os.makedirs(dir)
           if not os.path.exists('log'):
                  os.makedirs('log')
           if not os.path.exists(dir+'/roles/'):
                  os.makedirs(dir+'/roles/')
           conn,cur=connect()
           cur.execute("SELECT * FROM hostlist where hostip='%s'"%hostname[0])
           srcfile = 'external/plugins/Ansible_Playbook/ansible.cfg'
           dstroot = dir
           shutil.copy(srcfile, dstroot)
           for role in rolelist:
              if not os.path.exists(dir+'/roles/'+role):
                       os.makedirs(dir+'/roles/'+role)
              src = 'external/plugins/Ansible_Playbook/'+role
              dst = dir+'/roles/'+role
              copy_tree(src,dst)
           f = open(dir+'/hosts', 'a')
           f.write("[demo]\n")
           for list1 in cur.fetchall():
               f.write(""+ list1[1] +"  ansible_ssh_user="+ list1[2] +"  ansible_ssh_pass="+ list1[3] +"\n")
           f.close()
           f = open(dir+'/main.yml', 'a')
           f.write("- hosts: demo \n")
           f.write("  roles: \n")
           for rolename in rolelist:
               f.write("    - {role: "+ rolename +", become: true} \n")
           f.close()
           return dir
    def runplaybookhostnoregister(self, hostname, username, password, rolelist):
           owd = os.getcwd()
           dir="rundir"+str(time.strftime("%Y-%m-%d%H:%M:%S"))
           if not os.path.exists(dir):
                  os.makedirs(dir)
           if not os.path.exists('log'):
                  os.makedirs('log')
           if not os.path.exists(dir+'/roles/'):
                  os.makedirs(dir+'/roles/')
           srcfile = 'external/plugins/Ansible_Playbook/ansible.cfg'
           dstroot = dir
           shutil.copy(srcfile, dstroot)
           for role in rolelist:
              if not os.path.exists(dir+'/roles/'+role):
                       os.makedirs(dir+'/roles/'+role)
              src = 'external/plugins/Ansible_Playbook/'+role
              dst = dir+'/roles/'+role
              copy_tree(src,dst)
           f = open(dir+'/hosts', 'a')
           f.write("[demo]\n")
           f.write(""+ hostname +"  ansible_ssh_user="+ username +"  ansible_ssh_pass="+ password +"\n")
           f.close()
           f = open(dir+'/main.yml', 'a')
           f.write("- hosts: demo \n")
           f.write("  roles: \n")
           for rolename in rolelist:
               f.write("    - {role: "+ rolename +", become: true} \n")
           f.close()
           return dir
      

           

