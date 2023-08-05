import oauth2
import json


def authentication(consumer_key, consumer_secret, access_token, access_secret):
    consumer = oauth2.Consumer(key = consumer_key, secret = consumer_secret)
    token = oauth2.Token(key = access_token, secret = access_secret)
    client = oauth2.Client(consumer, token)

    return client

def get_tweets(client, qry):
    qry = " OR ".join(qry)
    url = "https://api.twitter.com/1.1/search/tweets.json?count=100&q=" + qry
    
    fulldata = []
    while True:
    	try:
            resp, content = client.request( url, method="GET", body=b"", headers=None )
            content = json.loads(content)
            #print(content)

            fulldata += content["statuses"]

            temp = []
            for t in content["statuses"]:
                temp.append(t["id"])

            max_id = str(min(temp)-1)

            url = "https://api.twitter.com/1.1/search/tweets.json?count=100&max_id=" + max_id + "&q=" + qry
            print(url)
        except:
            print("break")
            break

    return fulldata










	