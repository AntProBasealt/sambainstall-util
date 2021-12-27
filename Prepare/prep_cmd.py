#! /usr/bin/env python3
# -*- coding: utf-8 -*-
import sys 
import shutil
import os

def prep_update(prepare_list):
	prepare_list = ['apt-get update && sudo apt-get dist-upgrade', 'apt-get install task-samba-dc krb5-kinit bind', 'apt-get remove nss-ldapd nscd', 'systemctl disable --now smb nmb krb5kdc kadmin kpropd slapd', 'systemctl stop samba bind']
	for i in prepare_list:
		shellcmd = os.popen(i)	
#print(shellcmd.read())
#sys.stdout.flush()

# обдумываю как подставить домен при установке
def set_hostname(prepare_list):
	prepare_list = ['hostnamectl set-hostname %name_dc + '.custom.alt'', 'control bind-chroot disabled']
	for i in prepare_list:
		shellcmd = os.popen(i)	
# или так
	d = {'var1'="%name_dc + '.custom.alt", 'var2'="disabled", 'var3'="all"}
	s = "hostnamectl set-hostname {var1}, control bind-chroot {var2}, update_chrooted {var3}"
		shellcmd = os.popen(i)	


#
def prep_dir(prepare_list):
    prepare_list = ['rm -rf /var/lib/samba /etc/samba/smb.conf', 'mkdir /var/lib/samba', 'systemctl restart systemd-resolved', 'mkdir -p /usr/local/samba/private']
	for i in prepare_list:
		shellcmd = os.popen(i)	    
	#run_commands(cmdlist)
# или так
	d = { 'var1': "/var/lib/samba /etc/samba/smb.conf", 'var2': "/var/lib/samba", 'var3': "systemd-resolved", 'var4': "/usr/local/samba/private" }
	s = "rm -rf {var1}, mkdir {var2}, systemctl restart {var3}, mkdir -p {var4}"
		shellcmd = os.popen(s.format(**d))

