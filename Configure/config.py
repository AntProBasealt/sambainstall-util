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



# можно объединить в один блок
# Config (replace -  /etc/bind/named.conf)
def conf_template():
	
	with open('named.conf', 'w') as f:
		x='''
		include \'/etc/bind/options.conf\';
		include \'/etc/bind/rndc.conf\';
		include \'/etc/bind/local.conf\'; 
		include \'/var/lib/samba/bind-dns/named.conf\';
		'''
		f.write(x)

# Здесь генерит конфиги 
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
