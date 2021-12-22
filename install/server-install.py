import sys 
import shutil
import os
import yaml
import argparse


# for templates
from jinja2 import Environment, FileSystemLoader
template_dir, template_file = os.path.split(sys.argv[1])
vars_file = sys.argv[2]
env = Environment(loader=FileSystemLoader('./'))
env.trim_blocks = True
env.lstrip_blocks = True
env.rstrip_blocks = True


# запихал все команды преднастройки системы в один массив, и далее в цикле из выполняю 
prepare_list = ['apt-get update && sudo apt-get dist-upgrade', 'apt-get install task-samba-dc krb5-kinit bind', 'apt-get remove nss-ldapd nscd', 'systemctl disable --now smb nmb krb5kdc kadmin kpropd slapd', 'systemctl stop samba bind']
	for i in prepare_list:
		cmd + i
shellcmd = os.popen(cmd) #
print(shellcmd.read())

# можно объединить в один блок
prepare_list = ['hostnamectl set-hostname %name_dc + '.custom.alt'', 'update_chrooted all', 'control bind-chroot disabled']
import os
	for i in prepare_list:
		cmd + i
shellcmd = os.popen(cmd) #
print(shellcmd.read())

# можно объединить в один блок
prepare_list = ['rm -rf /var/lib/samba /etc/samba/smb.conf', 'mkdir /var/lib/samba', 'systemctl restart systemd-resolved', 'mkdir -p /usr/local/samba/private']
import os
	for i in prepare_list:
		cmd + i
shellcmd = os.popen(cmd) #
print(shellcmd.read())

# можно объединить в один блок
with open('/etc/bind/named.conf', 'w') as file:
    file.write('include /'/etc/bind/options.conf/';\n include /'/etc/bind/rndc.conf/';\n include /'/etc/bind/local.conf/'; include /'/var/lib/samba/bind-dns/named.conf/';')

'''
# а это макароны, которые заменил ниже
# Config kdc.conf
template = env.get_template('template/kdc.conf.j2')
with open(vars_file) as f:
    vars_dict = yaml.safe_load(f)
output_from_parsed_template = template.render(vars_dict)
with open("res/kdc.conf", "w") as fh:
    fh.write(output_from_parsed_template)

# Config smb.conf
template = env.get_template('template/smb.conf.j2')
with open(vars_file) as f:
    vars_dict = yaml.safe_load(f)
output_from_parsed_template = template.render(vars_dict)
with open("res/smb.conf", "w") as fh:
    fh.write(output_from_parsed_template)

# Config options.conf
template = env.get_template('template/options.conf.j2')
with open(vars_file) as f:
    vars_dict = yaml.safe_load(f)
output_from_parsed_template = template.render(vars_dict)
with open("res/options.conf", "w") as fh:
    fh.write(output_from_parsed_template)

'''
# Здесь генерит конфиги (те что всерху)
class file_config ()
	
	def __init__(self):
		self.templ_name = ('kdc.conf.j2', 'smb.conf.j2', 'options.conf.j2')
		self.out_file = ('kdc.conf', 'smb.conf', 'options.conf')
	
	def configure(self, templ_name, out_file):
		for i in self.templ_name():
			for j in self.out_file():
				template = env.get_template('template/%s' % i)
				with open(vars_file) as f:
    				vars_dict = yaml.safe_load(f)
					output_from_parsed_template = template.render(vars_dict)
				with open('res/%s' % j, 'w') as fh:
    				fh.write(output_from_parsed_template)
-------------------------------------------------------------------
'''
# это тож макароны, заменил ниже потом                                                                
print("Please enter ip_dns: ")                                    
ip_dns = sys.stdin.readline()                                     
#user_value = str(input("Please enter ip_dns: "))
#ip_dns = getattr(ureg, user_value)
with open("/etc/systemd/resolved.conf", "w") as f:
		f.write("DNS=%s" % ip_dns)

#
print("Please enter name_domain: ")
name_domain = sys.stdin.readline() 
with open("/etc/systemd/resolved.conf", "w") as f:
		f.write("Domains=%s" % name_domain)
with open("/etc/hosts", "w") as f:
		f.write( ip_dns + "localhost.localdomain localhost")

print("Please enter name_dc: ")
name_dc = sys.stdin.readline() 
with open("/etc/systemd/resolved.conf", "w") as f:
		f.write("Domains=%s" % name_domain)

# Config krb5.conf.j2
template = env.get_template('template/krb5.conf.j2')
with open(vars_file) as f:
    vars_dict = yaml.safe_load(f)
output_from_parsed_template = template.render(vars_dict)
with open("res/krb5.conf", "w") as fh:                            
    fh.write(output_from_parsed_template)    
'''                     
-------------------------------------------------------------------

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

---------------------------------------------------------

os.system('samba-tool domain provision --realm=custom.alt --domain custom --adminpass='Pa$$word' --dns-backend=BIND9_DLZ --backend-store=mdb --server-role=dc --use-rfc2307 --host-ip=10.64.66.17')


