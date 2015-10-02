#!/usr/bin/env python
# -*- coding: utf-8
from __future__ import print_function

# Importar librerías requeridas
import argparse
import os

# Variables de configuaración
NAME='train'

if __name__ == "__main__":
    # Las opciones de línea de comando
    p = argparse.ArgumentParser(NAME)
    p.add_argument("DIR",default=None,
        action="store", help="Output directory")
    p.add_argument("-l",type=str,nargs=2,
        action="append", dest="options",default=[],
        help="Mode (gender|age|extroverted|stable|agreeable|conscientious|open) [gender]")
    p.add_argument("--lang",type=str,
        action="store", dest="lang",default="en",
        help="Mode (gender|age|extroverted|stable|agreeable|conscientious|open) [gender]")
    p.add_argument("-v", "--verbose",
        action="store_true", dest="verbose",
        help="Verbose mode [Off]")
    opts = p.parse_args()
  

    # prepara función de verbose
    if opts.verbose:
        def verbose(*args):
            print(*args)
    else:   
        verbose = lambda *a: None 

    labels={}
    for label,filename in opts.options:
        labeling={}
        for line in open(filename):
            line=line.strip().split()
            labeling[line[0]]=line[1]
        labels[label]=labeling
        
    xml_='<author id="{user}"\ntype="twitter"\nlang="{lang}"\n'

    for user in labels['gender'].keys():
        xml=xml_.format(user=user,lang=opts.lang)
        for label,labeling in labels.iteritems():
            if label=="gender":
                if labeling[user].startswith('F'):
                    xml+='gender="female"\n'
                else:
                    xml+='gender="male"\n'
            elif label=="age":
                xml+='age_group="{0}"\n'.format(labeling[user])
            elif label.startswith("ex"):
                xml+='extroverted="{0}"\n'.format(labeling[user])
            elif label.startswith("st"):
                xml+='stable="{0}"\n'.format(labeling[user])
            elif label.startswith("agre"):
                xml+='agreeable="{0}"\n'.format(labeling[user])
            elif label.startswith("co"):
                xml+='conscientious="{0}"\n'.format(labeling[user])
            elif label.startswith("op"):
                xml+='open="{0}"'.format(labeling[user])
        xml=xml+'\n/>'
        with open(os.path.join(opts.DIR,user+'.xml'),'w') as ff:
            ff.write(xml)

