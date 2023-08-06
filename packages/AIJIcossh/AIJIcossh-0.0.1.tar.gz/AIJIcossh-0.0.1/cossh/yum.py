# util for Telecontrol to interact with yum.

from pexpect import TIMEOUT
import os.path as op
import re
import time


dirpath = op.dirname(op.abspath(__file__))

class Yum:
    def __init__(self, telecontrol):
        self.tc = telecontrol
        boo, msg = self._repair()
        if boo is False:
            raise Exception('Yum is not available.')
        
        
    # Internal, blocking
    def _is_ok(self):
        '''check yum is available or not'''
        # @WARNING: This function will never timeout
        self.tc.sendline('yum list yum', stdout=False)
        possibles = [self.tc.PROMPT, TIMEOUT]
        while True:
            index = self.tc.expect(possibles, timeout=5)
            if index == 0:
                if not self.tc.show():
                    return True, ''
                return False, self.tc.show()
            elif index == 1:
                pass

    # Internal
    def _repair(self):
        '''Try to fix problems on yum'''
        boo, msg = self._is_ok()
        res = 'Unkonw exception when repairing yum.'

        if boo is True:
            return True, ''

        if 'Error: Cannot retrieve metalink for repository: epel.' in msg:
            source = op.join(dirpath, 'epel.repo')
            filepath = '/eself.tc/yum.repos.d/epel.repo' 
            foo, bar = self.upload(source, filepath)
            if foo is False:
                res = 'Upload repo failed'
            elif __debug__: print('Upload repo successfully.')
        else:
            raise Exception('Unknow yum problem\n' + msg + '\n\n')
        
        boo, msg = self._is_ok()
        if boo is not True:
            return False, res
        else:
            return True, '' 

    def has(self, name):
        '''Find a application installed or not'''
        self.tc.sendline('yum list %s' % name, stdout=False)
        self.tc.prompt(5)
        if not self.tc.show():
            return True
        
        name = 'type ' + name

        self.tc.sendline(name, stdout=False)
        self.tc.prompt(5)
    
        foo = self.tc.show()
        if foo:
            return False
        return True

    def install(self, name):
        '''Install packages by yum.'''
        if self.has(name) is True:
            return True, 'exist'

        self.tc.sendline('yum install %s -y' % name, stdout=False)
        while True:
            possibles = [TIMEOUT, self.tc.PROMPT]
            index = self.tc.expect(possibles)

            if index == 0:
                pass
            else index == 1:
                if not self.tc.show():
                    return True, 'complete'
                else:
                    info = '\n'.join(['fail when installing', '='*10, self.tc.show(), '='*10, '']) 
                    return False, info
            
    

