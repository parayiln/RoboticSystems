#week 4
from readerwriterlock import rwlock
import sys
sys.path.append(r'/home/nidhi/.local/lib/python3.7/site-packages')
class buss(object):
    def __init__(self,message):
        self.lock = rwlock.RWLockWriteD ()
        self.message = message

    def write(self,message):
        with self.lock.gen_wlock ():
            self.message = message

    def read(self):
        with self.lock.gen_rlock ():
            message = self.message
        return message
