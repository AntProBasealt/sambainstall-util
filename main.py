#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import sys 
import shutil
import os
import yaml
import argparse


from Configure import config
from Prepare import prep_cmd


class Runner:
    __path_to_config = '/etc'

    def __init__(self, arguments):
        self.args = arguments

    def run(self):
        predv()
        configure()
        options()
        return True

    def predv():
        self.__path_to_config = '/tmp/etc'

        prep_cmd.prep_update(self.args)
        prep_cmd.set_hostname()
        prep_cmd.prep_dir()

    def configure():
        x = self.__path_to_config
        config.conf_template

    def options():
        x = self.__path_to_config
        options_conf.options()

def main():
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

    runnner = Runner(args)
    result = runnner.run()

    return result

if __name__ == "__main__":
    main()

# далее еще не дописал как всё это применить, и надо ли это так делать
x='samba-tool domain provision --realm={} --domain {} --adminpass='Pa$$word' --dns-backend=BIND9_DLZ --backend-store=mdb --server-role={} --use-rfc2307 --host-ip={}'
#os.system(x.format('realm', 'domain', 'server-role', 'ip'))

