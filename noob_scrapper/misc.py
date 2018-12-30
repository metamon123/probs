#!/usr/bin/env python3
import random, string, argparse

def argcheck():
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", help="port of the server", type=int)
    args = parser.parse_args()
    return args

def random_string_generator(length):
    return ''.join([random.choice(string.ascii_letters + string.digits) for n in range(length)])


