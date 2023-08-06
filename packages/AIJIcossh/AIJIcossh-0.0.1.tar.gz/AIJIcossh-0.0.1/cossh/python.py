'''
Use python version 3.4
'''

__all__ = ['python']

class Python:

    name = ''
    pip = None

    def __init__(self, telecontrol):
        self.tc = telecontrol
        self._ensure_python(self.tc.yum)
        self.pip = _Pip(self)

    
    def _is_ok(self):
        names = ['python3', 'python3.4', 'python3.5', 'python3.6']
        for name in names:
            self.tc.sendline(' '.join(['type', name]), stdout=False)
            self.tc.prompt()
            if not self.tc.show():
                self.name = name
                return True
        else:
            return False

    def _ensure_python(self, yum):
        if self._is_ok():
            return
        yum.install('epel-release')
        _, msg = yum.install('python34')
        if self._is_ok():
            return
        raise Exception('\n'.join([
                'Cannot found python.',
                'Messgae from yum:',
                msg]))

class _Pip:

    name = ''

    def __init__(self, python):
        self.python = python
        self.tc = python.tc 

    def __bool__(self):
        return bool(self.name)

    def list(self):
        self._ensure_pip()
        self.tc.sendline(' '.join([self.name, 'list',
                '--format=legacy']), stderr=False)
        self.tc.prompt()
        foo = self.tc.show()
        foo = foo.split('\n')
        foo = filter(lambda x:x, foo)
        foo = [i.split(' ')[0].strip() for i in foo]
        return foo    
        
    def install(self, packs):
        if not isinstance(packs, list):
            packs = [packs]
        self._ensure_pip()
        for p in packs:
            self.tc.sendline(' '.join([self.name, 'install', name, '-U']), 
                    stdout=False, stderr=False)
            self.tc.prompt()
        foo = self.list()
        for p in packs:
            if p not in foo:
                return False, p
        else:
            return True, None

        

    def _is_ok(self):
        name = ' '.join(self.python.name, '-m', 'pip')
        self.tc.sendline(name, stdout=False)
        self.tc.prompt()
        if not self.tc.show()
            self.name = name
            return True
        return False

    def _ensure_pip(self):
        if self or self._is_ok():
            return
        self.tc.sendline(' '.join([
                self.python.name, '-m', 'ensurepip']), stdout=False)
        self.tc.prompt()
        msg = self.tc.show()
        if not msg:
            self.tc.sendline(' '.join([
                self.python.name, '-m', 'pip',
                'install', '--upgrade', 'pip']), stdout=False)
            self.tc.prompt()
            msg = self.tc.show()
        if not self._is_ok():
            raise Exception('Pip Error:\n' + msg)

    

