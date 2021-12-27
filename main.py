#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import sys 
import shutil
import os


from Options import options_conf
from Configure import config
from Prep_command import prep_cmd

	if __name__ == "__main__"
		
		def prepare():
			prep_cmd.rprep_update()
			prep_cmd.set_hostname()
			prep_cmd.rprep_dir()

		def configure():
			config.conf_template

		def options():
			options_conf.options()

# далее еще не дописал как всё это применить, и надо ли это так делать
x='samba-tool domain provision --realm={} --domain {} --adminpass='Pa$$word' --dns-backend=BIND9_DLZ --backend-store=mdb --server-role={} --use-rfc2307 --host-ip={}'
os.system(x.format('realm', 'domain', 'server-role', 'ip'))
