import tweepy
import re

from ConexionBaseDeDatos import ConexionBaseDeDatos
from SendEmail import SenDMail

def get_auth():
    consumer_key = ''
    consumer_secret = ''
    access_token = 
    access_token_secret = ''
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    return auth


class MyStreamListener(tweepy.StreamListener):
    baseDeDatos = ConexionBaseDeDatos()
    def on_status(self, status):
            #eliminamos @
            if status is not False and status.text is not None:
                try:
                    texto = status.extended_tweet["full_text"]
                    print(texto)
                except AttributeError:
                    texto = status.text
                    # texto= re.sub('@[^\s]+', '', texto)
                    # texto = re.sub(r"http\S+", "", texto)
                # tweetText = unicode(tweetText, errors='ignore')
                # texto = re.sub(r'[^a-zA-Z0-9_\s]+', '', texto)  # on sentence itself.Here I have modified RegEx to include spaces as well
                # When a tweet is published it arrives here.

                try:
                    if self.baseDeDatos.existe_tweet(texto):
                        try:
                            self.baseDeDatos.almacenar_base_de_datos(status.created_at,
                            status.id, texto, status.source, status.truncated,
                            status.in_reply_to_status_id, status.in_reply_to_user_id,
                            status.in_reply_to_screen_name, status.geo, status.coordinates,
                            status.place,status.contributors, status.lang, status.retweeted)
                        except Exception as e:
                            print(e)
                    else:
                        print("Print Repetido")
                except Exception as e:
                    print("merda")
                print("Almacenamos Tweet")
                print("-" * 10)
    def on_error(self, status_code):
        aux = SenDMail()
        aux.send_email_alerta()
        print(status_code)

        return False

if __name__ == '__main__':
    print("===== Captador de tweets =====")

    # Get an API item using tweepy
    auth = get_auth()  # Retrieve an auth object using the function 'get_auth' above
    api = tweepy.API(auth)  # Build an API object.

    # Connect to the stream
    myStreamListener = MyStreamListener()
    while True:
        try:
            myStream = tweepy.Stream(auth=api.auth, listener=myStreamListener)

            print(">> Listening to tweets about #bitcoin en ingles:")
            myStream.filter(track=['bitcoin'], languages=['en'])

        except:
            continue

    



