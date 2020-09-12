import socket
import sys
import requests
import requests_oauthlib
import json
import bleach
from bs4 import BeautifulSoup

import credentials


my_auth = requests_oauthlib.OAuth1(credentials.consumer_key, credentials.consumer_secret,credentials.access_token, credentials.access_token_secret)


def ReadTweets():
    url = 'https://stream.twitter.com/1.1/statuses/filter.json'	
    query_data = [('language', 'en'), ('locations', '-130,-20,100,50'),('track','covid')]
    query_url = url + '?' + '&'.join([str(t[0]) + '=' + str(t[1]) for t in query_data])
    response = requests.get(query_url, auth=my_auth, stream=True)
    print(query_url, response)
    return response




def TweetsToSpark(http_resp, tcp_connection):
	for line in http_resp.iter_lines():
		try:

			full_tweet = json.loads(line)

			tweet_text = full_tweet['text']
			print("Tweet Text: " + tweet_text)
			print ("------------------------------------------")
			     
		
			tweet_country_code = "CC"+full_tweet['place']['country_code']
			print("COUNTRY CODE IS : " + tweet_country_code)
			print ("------------------------------------------")

			tcp_connection.send((tweet_text +' '+ tweet_country_code + '\n').encode())
			
		except Exception as e:
			print('Mensaje', e)



TCP_IP = 'localhost'
TCP_PORT = 5556
conn = None
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

s.bind((TCP_IP, TCP_PORT))
s.listen(1)

print("Esperando por la conexion")
conn, addr = s.accept()
print('------------------------')
print("Conectados, busquemos los paises que más hablan sobre el coronavirus")

resp = ReadTweets()
TweetsToSpark(resp, conn)