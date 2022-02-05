#week 4

import sys
sys.path.append(r'/home/nidhi/.local/lib/python3.7/site-packages')
from readerwriterlock import rwlock


class buss(object):
    def __init__(self):
        self.lock = rwlock.RWLockWriteD()
        self.message = None

    def write(self, message):
        with self.lock.gen_wlock():
            self.message = message
            print("message write",message)

    def read(self):
        with self.lock.gen_rlock():
            message = self.message
            print("message read",message)
            return message
