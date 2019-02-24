#!/usr/bin/env python3

class jail():
    def __init__(self):
        self.blacklist = []
    def run_file(self, filename):
        f = open(filename, 'r')
        src = f.read()
        self.run_code(src)
        f.close()
    def run_code(self, src):
        if not self.is_safe(src):
            print("Bad character was found! Go away!")
            return
        exec(src)
    def is_safe(self, src):
        if list(filter(lambda bad: bad in src, self.blacklist)):
            return False
        return True
    def add_blacklist(self, blacklist):
        if type(blacklist) == "list":
            self.blacklist.extend(blacklist)
        elif type(blacklist) == "str":
            self.blacklist.extend(list(blacklist))


r = jail()
r.add_blacklist('()=')
opt = raw_input("run file (f) / run code (c) : ")
if opt == 'c':
    r.run_code(raw_input("your src : "))
elif opt == 'f':
    r.run_file(raw_input("your filename : "))
