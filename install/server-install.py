#! /usr/bin/env python3

import sys 
import shutil
import os
import yaml
import argparse

# for templates
from jinja2 import Environment, FileSystemLoader
#template_dir, template_file = os.path.split(sys.argv[1])
#vars_file = sys.argv[2]
env = Environment(loader=FileSystemLoader('./'))
env.trim_blocks = True
env.lstrip_blocks = True
env.rstrip_blocks = True




# запихал все команды преднастройки системы в один массив, и далее в цикле из выполняю 
# можно объединить в один блок, пока не придумал как
def prep_update(prepare_list):
	prepare_list = ['apt-get update && sudo apt-get dist-upgrade', 'apt-get install task-samba-dc krb5-kinit bind', 'apt-get remove nss-ldapd nscd', 'systemctl disable --now smb nmb krb5kdc kadmin kpropd slapd', 'systemctl stop samba bind']
	for i in prepare_list:
		shellcmd = os.popen(i)	
#print(shellcmd.read())
#sys.stdout.flush()

# можно объединить в один блок
def set_hostname(prepare_list):
	prepare_list = ['hostnamectl set-hostname %name_dc + '.custom.alt'', 'update_chrooted all', 'control bind-chroot disabled']
	for i in prepare_list:
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



chmod +x server-install.py


# можно объединить в один блок
# Config (replace -  /etc/bind/named.conf)
with open('named.conf', 'w') as file:
	x='''
	include \'/etc/bind/options.conf\';
	include \'/etc/bind/rndc.conf\';
	include \'/etc/bind/local.conf\'; 
	include \'/var/lib/samba/bind-dns/named.conf\';'''
	file.write(x)

# Здесь генерит конфиги (те что сверху)
templ_name = ('kdc.conf.j2', 'krb5.conf.j2', 'smb.conf.j2', 'options.conf.j2')
out_file = ('kdc.conf', 'krb5.conf', 'smb.conf', 'options.conf')
	
for i in templ_name():
	for j in out_file():
		template = env.get_template('templ/%s' % i)
		with open('varfile.yml') as f:
   			vars_dict = yaml.safe_load(f)
			output_from_parsed_template = template.render(vars_dict)
		with open('res/%s' % j, 'w') as fh:
   			fh.write(output_from_parsed_template)

# здесь заменяю макароны сверху на опциии утилиты
parser = argparse.ArgumentParser()
parser.add_argument('--realm', type=str, help='realm')
parser.add_argument('--domain', type=str, help='domain')
parser.add_argument('--adminpass', type=str, help='At least 8 characters')
parser.add_argument('--dns-backend', type=str, help='BIND9_DLZ or INTERNAL', default='BIND9_DLZ')
parser.add_argument('--backend-store', type=str, help='lndb/mdb', default='mdb')
parser.add_argument('--server-role', type=str, help='dc', default='dc')
parser.add_argument('--host-ip', type=str, help='ip-address')
parser.add_argument('-v', '--verbosity', action='count', default=0)
args = parser.parse_args()

'''
os.system('samba-tool domain provision --realm=custom.alt --domain custom --adminpass='Pa$$word' --dns-backend=BIND9_DLZ --backend-store=mdb --server-role=dc --use-rfc2307 --host-ip=10.64.66.17')
'''
x='samba-tool domain provision --realm={} --domain {} --adminpass='Pa$$word' --dns-backend=BIND9_DLZ --backend-store=mdb --server-role={} --use-rfc2307 --host-ip={}'
os.system(x.format('realm', 'domain', 'server-role', 'ip'))









