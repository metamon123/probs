#!/usr/bin/env python3
import sys

class Pyjail():
    def __init__(self):
        self.blacklist = []
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


jail = Pyjail()
jail.add_blacklist('()')

print("Give me a python code to execute")
print("Ah! Please make sure there aren't any PARENTHESES... '(', ')'")
print("* To submit code, just ctrl+D")

code = ''.join(sys.stdin.readlines())
del sys
jail.run_code(code)
