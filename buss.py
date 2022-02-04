#week 4
from readerwriterlock import rwlock

class buss(object):
    def __init__(self):
        self.lock = rwlock.RWLockWriteD ()
        self.message = default

    def write(self):
        with self.lock.gen_wlock ():
            self.message = message

    def read(self):
        with self.lock.gen_rlock ():
            message = self.message
        return message
