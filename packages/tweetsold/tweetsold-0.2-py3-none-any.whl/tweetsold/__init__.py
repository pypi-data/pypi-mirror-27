import oauth2
import json
import time


def authentication(consumer_key, consumer_secret, access_token, access_secret):
    consumer = oauth2.Consumer(key = consumer_key, secret = consumer_secret)
    token = oauth2.Token(key = access_token, secret = access_secret)
    client = oauth2.Client(consumer, token)
    return client

def get_tweets(client, qry, until = ""):
    print("Process : Extrction of tweets is running...This will take sometime...")
    qry = " OR ".join(qry)
    if until != "":
        url = "https://api.twitter.com/1.1/search/tweets.json?until=" + until + "&count=100&q=" + qry
    else:
        url = "https://api.twitter.com/1.1/search/tweets.json?count=100&q=" + qry
    
    fulldata = []
    while True:
    	try:
    	    #print("step1")
            resp, content = client.request( url, method="GET", body=b"", headers=None )
            content = json.loads(content)
            #print(content)

            fulldata += content["statuses"]

            temp = []
            for t in content["statuses"]:
                temp.append(t["id"])

            max_id = str(min(temp)-1)

            if until != "": 
                url = "https://api.twitter.com/1.1/search/tweets.json?until=" + until + "&count=100&max_id=" + max_id + "&q=" + qry
            else:
                url = "https://api.twitter.com/1.1/search/tweets.json?count=100&max_id=" + max_id + "&q=" + qry
            
            print("Extracted " + str(len(fulldata)) + " tweets till now.")
            time.sleep(5)
        except:
            #print("break")
            break
    print("\n-------------------------------------------------------------")
    print("Total " + str(len(fulldata)) + " Extracted.")
    print("-------------------------------------------------------------")
    return fulldata










	