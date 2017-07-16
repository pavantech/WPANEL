from distutils.dir_util import copy_tree
from connect import connect
import os
import shutil



class runplaybooks(object):

    def __init__(self):
        self._rolelist = []
        self._groupname=[]

    def runplaybookgroup(self, groupname, rolelist):
           if not os.path.exists('rundir'):
                  os.makedirs('rundir')
           if  os.path.exists('rundir/hosts'):
                  os.remove("rundir/hosts")
           if  os.path.exists('rundir/hosts'):
                  os.remove("rundir/main.yml")
           if  os.path.exists('rundir/roles'):
                 shutil.rmtree('rundir/hosts/roles')
           if  os.path.exists('rundir/ansible.cfg''):
                 os.remove("rundir/ansible.cfg'")
           conn,cur=connect()
           srcfile = 'external/plugins/Ansible_Playbook/ansible.cfg'
           dstroot = 'rundir'
           shutil.copy(srcfile, dstroot)
           for role in rolelist:
              if not os.path.exists('rundir/roles/'+role):
                       os.makedirs('rundir/roles/'+role)
              src = 'external/plugins/Ansible_Playbook/'+role
              dst = 'rundir/roles/'+role
              copy_tree(src,dst)
           f = open('rundir/hosts', 'a')
           f.write("["+groupname[0]+"]\n")
           
           f.write("xxx.xxx.xx ansible.ssh.username=pavan ansible.ssh.pavan=pavan \n")
           f.close()
           f = open('rundir/main.yml', 'a')
           f.write("- hosts: "+groupname[0]+"\n")
           f.write("  roles: \n")
           for rolename in rolelist:
               f.write("    - {role: "+ rolename +", become: true} \n")
           f.close()

