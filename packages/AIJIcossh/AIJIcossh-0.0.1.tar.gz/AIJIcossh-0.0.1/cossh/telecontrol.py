import re
import sys
import os
import time

from pexpect.pxssh import pxssh
import pexpect as pe
from devtools.format import tostr

from yum import Yum

INTERNAL = 0.5

# A wrap for the pxssh Class (which is a wrap of spawn Class).
# Make controlling remote more easily
class Telecontrol(pxssh):
    
    target_addr = ('', 0)

    def __init__(self, user, ip='122.144.139.60', port='12045', passwd='yylc#8888', timeout=3):
        super(Telecontrol, self).__init__(timeout=timeout)
        
        self.login(ip, user, passwd, port=port)
        
        if __debug__ : print('logged in.') 
        self.target_addr = (ip, str(port))
        self.user = user
        self.passwd = passwd
        
        self.yum = Yum(self)

        if __debug__ : print('checked in advance.') 
        if __debug__ : print('Telecontrol created.') 

    # Override, add sleep to avoid some weird bugs
    def prompt(self, timeout=-1, sleep=0.1):
         time.sleep(sleep)
         res = super(Telecontrol, self).prompt(timeout)
         time.sleep(sleep)
         return res

    # Override, add option stdout=False
    def sendline(self, s='', stdout=True, stderr=True):
        if stdout is False:
            s = s + ' 1>/dev/null'
        if stderr is False:
            s = s + ' 2>/dev/null'
        res = super(Telecontrol, self).sendline(s) 
        return s

    # return True:  is a directory
    # return False: is not a directory
    # return None:  no such file or directory
    def isdir(self, filepath):
        self.sendline(filepath + '/')
        self.prompt()
        text = self.show()
        if re.search('(?i)is a directory', text):
            return True
        elif re.search('(?i)not a directory', text):
            return False
        elif re.search('(?i)no such file or directory', text):
            return None
        else:
            raise Exception('Unpredicted output:\n {0} \n\n'.format(text))

    # remove file or directory sliently by force
    def remove(self, filepath):
        foo = self.isdir(filepath)
        if foo is True:
            self.sendline('rm -rf %s' % filepath)
            self.prompt()
        elif foo is False:
            self.sendline('rm -f %s' % filepath)
            self.prompt()
        elif foo is None:
            if __debug__: print('Remove {0}: file or dir not found'.format(filepath))
            return 
        if __debug__ : print('Remove {0}'.format(filepath), self.show(), sep='\n')

    def mkdir(self, dirpath):
        if not dirpath.startswith('/'):
            raise NotImplementedError('mkdir for relative path not supported yet')
            
       
    def show(self):
        foo = self.before.decode()
        foo = re.sub('^.*\r\n', '', foo)

        return foo     
    


    # This function need to be improved
    def upload(self, source_file, target_dir, target_name='', opt='', timeout=10):
        if not os.path.exists(source_file):
            return False, 'file or directory not found'
        if os.path.isdir(source_file):
            opt = '-r'
        elif os.path.isfile(source_file):
            opt = ''
        else:
            raise Exception('Not a dir nor a file')
        if source_file.strip().endswith('/'):
            raise NotImplementedError('"scp source/dir/ target/dir" not implemented.')
        target_dir = target_dir + '/'
        if not target_name:
            target_name = source_file.split('/')[-1]
        target_path = os.path.join(target_dir, target_name)
        self.mkdir(target_dir)
        self.remove(target_path)
        
        target_path = '{0}@{1}:{2}'.format(
                self.user, 
                self.target_addr[0], 
                target_path)
        
         

        cmd = 'scp -P {0} {1} {2} {3}'.format(
                self.target_addr[1],
                opt,
                source_file,
                target_path)

        if __debug__: print('Upload cmd:', cmd)

        child = pe.spawn(cmd, timeout=3)
        time = 0
        
        possibles = [
                '(?i)password: ',  # 0
                '(?i)yes/no',      # 1
                'lost connection', # 2
                pe.EOF,            # 3
                pe.TIMEOUT,        # 4
                'ssh:',            # 5
                '100%']            # 6 
        while True:
            index = child.expect(possibles)
            if __debug__ and index != 6: print('Uploading ... code:', index, str(possibles[index]))
            if index == 0:
                child.sendline(self.passwd)
            elif index == 1:
                child.sendline('yes')
            elif index == 2:
                return False, 'lost connection'
            elif index == 3:
                return True, child.before
            elif index == 4:
                time += child.timeout
                if time > timeout:
                    return False, 'upload timeout'
            elif index == 5:
                return False, 'ssh failed'
            elif index == 6:
                pass 
    def reset(self):
        self.sendcontrol('c')
        self.prompt(0.1)
        time.sleep(0.5)
            

            

        
