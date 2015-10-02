import urllib2
import xml.etree.ElementTree as ET
import argparse
import os

array_tweets = []

def obtener_tweets(file):
    count = 0
    """lee el xml y agrega el tweet leido en nuestro arreglo de tweets"""
    tree = ET.parse(file)
    root = tree.getroot()
    for document in root.iter('document'):
        url = document.attrib['url']
        response = urllib2.urlopen(url)
        tweet = response.read()
        count += 1
        print count
        array_tweets.append(tweet)

def write_json(name):
    """Escribe el archivo json"""
    with open(name, "w") as json_file :
        json.dump(array_tweets, json_file)
        json_file.close()
        
# Creation of the actual interface, using authentication
#api = tweepy.API(auth,wait_on_rate_limit=True,wait_on_rate_limit_notify=True)

 
if __name__ == "__main__":
    # Command line options
    p = argparse.ArgumentParser("transform-tweets")
    p.add_argument("DIR",default=None,
        action="store", help="Directory with corpus")
#    p.add_argument("KEYS",default=None,
#        action="store", help="Twitter screet keys")
    p.add_argument("-v", "--verbose",
        action="store_true", dest="verbose",
        help="Verbose mode [Off]")
    opts = p.parse_args()
    count  = 0
    for root, dirs, files in os.walk(opts.DIR):
        for filename in files:
            if filename.endswith('.xml') and count < 1:
                count += 1
                obtener_tweets(os.path.join(root,filename))
    write_json(opts.DIR)