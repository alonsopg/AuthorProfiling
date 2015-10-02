#!/usr/bin/python
from parser import parse, json_name
from sys import argv

if len(argv) < 2:
    raise Exception("Especifica la ruta del corpus ")
    
script, path = argv


parse(path)

print json_name()