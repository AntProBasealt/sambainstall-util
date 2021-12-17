import sys 
import shutil
import os

loader = FileSystemLoader('/project1/templates', encoding='utf-8')
# запихал все команды преднастройки системы в один массив, и далее в цикле из выполняю 
prepare_list = ["apt-get update && sudo apt-get dist-upgrade", "apt-get install task-samba-dc krb5-kinit bind", "apt-get remove nss-ldapd nscd", "systemctl disable --now smb nmb krb5kdc kadmin kpropd slapd", "systemctl stop samba bind"]
	for i in prepare_list:
		cmd + i
shellcmd = os.popen(cmd) #
print(shellcmd.read())

#
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

#
prepare_list = ["hostnamectl set-hostname %name_dc + '.custom.alt'", "update_chrooted all", "control bind-chroot disabled"]
import os
	for i in prepare_list:
		cmd + i
shellcmd = os.popen(cmd) #
print(shellcmd.read())

#
with open("/etc/bind/named.conf", "w") as file:
    file.write("include "/etc/bind/options.conf";\n include "/etc/bind/rndc.conf";\n include "/etc/bind/local.conf"; include "/var/lib/samba/bind-dns/named.conf";")

#
prepare_list = ["rm -rf /var/lib/samba /etc/samba/smb.conf", "mkdir /var/lib/samba", "systemctl restart systemd-resolved", "mkdir -p /usr/local/samba/private"]
import os
	for i in prepare_list:
		cmd + i
shellcmd = os.popen(cmd) #
print(shellcmd.read())


#
from jinja2 import Environment, FileSystemLoader
loader = FileSystemLoader('/projects/jinja2/krb5.conf.j2')
env = Environment(loader, trim_blocks=True, lstrip_blocks=True)
template = env.get_template('krb5.conf.j2')
data = {'samba_realm':'custom.domain,alt'}
with open("krb5.conf", "w") as f:
    f.write(template.render(data))
#config krb5.conf
shutil.copy(r'krb5.conf.j2', r'/etc/krb5t.conf')


#
from jinja2 import Environment, FileSystemLoader
loader = FileSystemLoader('/projects/jinja2/kdc.conf.j2')
env = Environment(loader, trim_blocks=True, lstrip_blocks=True)
template = env.get_template('skdc.conf.j2')
data = {'samba_realm':'doamin.alt'}
with open("kdc.conf.j2", "w") as f:
    f.write(template.render(data))
#config kdc.conf
shutil.copy(r'kdc.conf.j2', r'/usr/local/samba/private/kdc.conf')


#
from jinja2 import Environment, FileSystemLoader
loader = FileSystemLoader('/projects/jinja2/smb.conf.master.j2')
env = Environment(loader, trim_blocks=True, lstrip_blocks=True)
template = env.get_template('smb.conf.master.j2')
data = {'dc_short_name':'dc0', 'samba_realm':'doamin.alt', 'samba_domain':'domain', 'samba_dns_forward':'8.8.8.8'}
with open("smb.conf.master.j2", "w") as f:
    f.write(template.render(data))
#config smb.conf
shutil.copy(r'smb.conf.master.j2', r'/etc/samba/smb.conf.master.j2')


#
from jinja2 import Environment, FileSystemLoader
loader = FileSystemLoader('/projects/jinja2/options.conf.j2')
env = Environment(loader, trim_blocks=True, lstrip_blocks=True)
template = env.get_template('options.conf.j2')
data = {'samba_network':'10.0.0.0', 'samba_dns_forward':'8.8.8.8'}
with open("options.conf", "w") as f:
    f.write(template.render(data))
#config options.conf
shutil.copy(r'options.conf.j2', r'/etc/bind/options.conf')

os.system('samba-tool domain provision --realm=custom.alt --domain custom --adminpass='Pa$$word' --dns-backend=BIND9_DLZ --backend-store=mdb --server-role=dc --use-rfc2307 --host-ip=10.64.66.17')


