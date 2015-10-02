import tweepy
import secret_keys
import xml.etree.ElementTree as ET
import argparse
import os
import json

auth = tweepy.OAuthHandler(secret_keys.APIKEY , secret_keys.APISECRET)
auth.set_access_token(secret_keys.TOKENACCES,secret_keys.TOKENSECRET)

chunk=100

def create_json(data,age=None,gender=None):
    ids,text=zip(*data)
    return {
    'index': ids,
    'columns': ['age','gender','text'],
    'data': [
        [age,gender,t]
            for t in text]
    }

def obtener_tweets(file,truth):
    """lee el xml y agrega el tweet leido en nuestro arreglo de tweets"""
    tree = ET.parse(file)
    root = tree.getroot()
    ids=[]
    b,e=os.path.splitext(file)
    i=0
    array_tweets = []
    for document in root.iter('document'):
        id = document.attrib['id']
        ids.append(id)
    for i in range(len(ids)/chunk):
        ids_=[x for x in ids[i*chunk:(i+1)*chunk] if
            len(x) ]
        try:
            tweets = api.statuses_lookup(ids_,True,True)
            tweets = [(t.id,t.text) for t in tweets]
            array_tweets.extend(tweets)
        except tweepy.error.TweepError:
            print ids_,os.path.basename(b)
    ids_=[x for x in ids[(i+1)*chunk:] if
            len(x) ]
    if len(ids_)>0:
        tweets = api.statuses_lookup(ids_,True,True)
        tweets = [(t.id,t.text) for t in tweets]
        array_tweets.extend(tweets)
    if len(array_tweets)>0:
        gender,age=truth[os.path.basename(b)]
        json_info=create_json(array_tweets,gender=gender,age=age)
        write_json(json_info,b+'.json')
    else:
        print "Warning: Nothing recovered", os.path.basename(b)

def write_json(array_tweets,name):
    """Escribe el archivo json"""
    with open(name, "w") as json_file :
        json.dump(array_tweets, json_file)
        json_file.close()
        
# Creation of the actual interface, using authentication
api = tweepy.API(auth,wait_on_rate_limit=True,wait_on_rate_limit_notify=True)

 
if __name__ == "__main__":
    # Command line options
    p = argparse.ArgumentParser("transform-tweets")
    p.add_argument("DIR",default=None,
        action="store", help="Directory with corpus")
    p.add_argument("-v", "--verbose",
        action="store_true", dest="verbose",
        help="Verbose mode [Off]")
    opts = p.parse_args()

    truth={}
    for line in open(os.path.join(opts.DIR,'truth.txt')):
        bits=line.split(':::')
        truth[bits[0]]=(bits[1],bits[2])

    for root, dirs, files in os.walk(opts.DIR):
        for filename in files:
            if filename.endswith('.xml'):
                obtener_tweets(os.path.join(root,filename),truth)
   
