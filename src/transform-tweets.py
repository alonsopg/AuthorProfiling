#!/usr/bin/env python
# -*- coding: utf-8

import xml.etree.ElementTree as ET
import argparse
import os
import twitter
import secret_keys

def process_xml(xmlfile):
    """lee el xml y hace append en nuestro arreglo que se escribirá como json"""
    tree = ET.parse(xmlfile)
    root = tree.getroot()
   
    print "Connecting to api"
    api = twitter.Api(consumer_key=secret_keys.APISECRET,
                    consumer_secret=secret_keys.APIKEY,
                    access_token_key=secret_keys.TOKENACCES,
                    access_token_secret=secret_keys.TOKENSECRET
                    )

    print api.VerifyCredentials()
    sys.exit()
    for document in root.iter('document'):
        print document.get('url')


if __name__ == "__main__":
    # Command line options
    p = argparse.ArgumentParser("transform-tweets")
    p.add_argument("DIR",default=None,
        action="store", help="Directory with corpus")
    p.add_argument("KEYS",default=None,
        action="store", help="Twitter screet keys")
    p.add_argument("-v", "--verbose",
        action="store_true", dest="verbose",
        help="Verbose mode [Off]")
    opts = p.parse_args()

    for root, dirs, files in os.walk(opts.DIR):
        for filename in files:
            if filename.endswith('.xml'):
               process_xml(os.path.join(root,filename))
                

