import sys 
import os
import yaml
import argparse


# здесь заменяю макароны сверху на опциии утилиты
def options():
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
