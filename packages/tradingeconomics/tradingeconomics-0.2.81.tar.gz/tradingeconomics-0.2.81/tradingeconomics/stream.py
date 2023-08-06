import websocket
#import thread
import time
import sys
import json
from pprint import pprint
from time import sleep
import datetime as dt
import threading
from . import glob

  

te_url = "ws://stream.tradingeconomics.com/"

reconnect_timeout = 60


def on_error(ws, error):
    print error

def on_close(ws):
    print "### closed ### reconnect in " + str(reconnect_timeout) + " seconds"
    sleep(reconnect_timeout)
    start_socket(on_message_client)   


def on_open(ws):
    print "+++ Socket is open!"
    print "+++ Subscribe to {0}".format(glob._event)
    ws.send(json.dumps({'topic': 'subscribe', 'to': glob._event}) )



def build_url():
    return te_url + "?client=" + glob.apikey


def start_socket(on_message_client):    
    def _on_message(web_sock, message):
        """ 
            made so we do not have to reinitialize connection
        """
        t = threading.Thread(target=on_message_client, args=(web_sock, message))
        t.start()

    ws = websocket.WebSocketApp(build_url(),
                              on_message = _on_message,
                              on_error = on_error,
                              on_close = on_close)
    
    ws.on_open = on_open
    ws.run_forever()
    ws.close()


def run(on_message_client):
    websocket.enableTrace(True)
    start_socket(on_message_client)
