#!/usr/bin/python
"""rBot (reebot) sends information to IRC channel"""

import irclib
import feedparser
import sys
import threading
import time
from config import *

def main():
    try:
        c = rBot()
    except irclib.ServerConnectionError, e:
        print( "Error: %s" % e )
        exit()
        
class rBot:
    def __init__(self):
        self.irc = irclib.IRC()
        self.server = self.irc.server()
        self.server.connect( IRC_SERVER, IRC_PORT, NICK )
 
        for c in CHANNEL_LIST:
            self.server.join( c )
            self.server.privmsg( c, "Che, I am here" ) # Welcome message

        self.irc.process_forever()
        
    def getsources(self):
        self.feed_list = FEED_LIST

    def sendmsgqueue(self, message):    
        # self.msgqueue = []
        # self.msgqueue.append(message)
        # self.msg = msgqueue.pop()

        # for c in self.channel_list:
        #      self.server.privmsg( c, self.msg )
        # self.irc.process_once()
        pass
        
    def feed_refresh():
        pass
            
if __name__ == "__main__":
    main()
