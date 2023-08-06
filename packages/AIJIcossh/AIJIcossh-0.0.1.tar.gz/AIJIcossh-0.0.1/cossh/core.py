import re
import configparser
from time import sleep
import os.path as op
from threading import Thread

from telecontrol import Telecontrol as TC

dirpath = op.dirname(op.abspath(__file__))
dirpath = re.match('.*/CMDB', dirpath).group()
filepath = op.join(dirpath, 'distri.ini')
config = configparser.ConfigParser()
config.read(filepath)
PACKAGE_LIST = config['python']['packages'].strip().split(' ')

                

def install_cmdb(tc):
    tc.upload('/home/aiji/CMDB', '/opt', timeout=9999)
    
    


 

def start_monitor(tc):
    tc.sendline('python3.4 /opt/CMDB/client/main.py start monitor')
    tc.prompt()


def deploy(port):
    s = TC('root', port=port)
    python_env(s)
    install_cmdb(s)
    start_monitor(s)
    s.logout()
    
def start_client(port):
    s = TC('root', port=port)
    start_monitor(s)
    s.logout()
    


if  __name__ == '__main__':
    port = [i + 12042 for i in range(4)]
    for p in port:
        t = Thread(target=deploy, args=(p,), daemon=True)
        t.start()
        t.join()
    
    # for p in port:
    #   t = Thread(target=start_client, args=(p,), daemon=True)
    #   t.start()
    #   t.join()


