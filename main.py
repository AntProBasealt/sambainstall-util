#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import sys 
import shutil
import os


from Options import options_conf
from Configure import config
from Prepare import prep_cmd


class Runner:
    __path_to_config = '/etc'

    def __init__(self):
        pass

    def run(self):
        predv()
        configure()
        options()
        return True

    def predv():
        self.__path_to_config = '/tmp/etc'

        prep_cmd.prep_update()
        prep_cmd.set_hostname()
        prep_cmd.prep_dir()

    def configure():
        x = self.__path_to_config
        config.conf_template

    def options():
        x = self.__path_to_config
        options_conf.options()

def main():
    runnner = Runner()
    result = runnner.run()

    return result

if __name__ == "__main__":
    main()

# далее еще не дописал как всё это применить, и надо ли это так делать
x='samba-tool domain provision --realm={} --domain {} --adminpass='Pa$$word' --dns-backend=BIND9_DLZ --backend-store=mdb --server-role={} --use-rfc2307 --host-ip={}'
#os.system(x.format('realm', 'domain', 'server-role', 'ip'))
