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
    except:
        e = sys.exc_info()[0]
        print( "Error: %s" % e )
        exit()
    # main()
    
class rBot:
    def __init__(self):
        # Set server variables from config
        self.nick = NICK
        self.channel_list = CHANNEL_LIST
        self.irc_server = IRC_SERVER
        # self.port = SERVER_PORT

        # Connecting to IRC server
        self.irc = irclib.IRC()
        self.server = self.irc.server()
        self.server.connect( self.irc_server, self.port, self.nick )

        # Join IRC channel
        for c in self.channel_list:
            self.server.join( c )

    def getsources(self):
        self.feed_list = FEED_LIST
        
    def sendmessage(self, message):    
        self.msgqueue = []
        self.msgqueue.append(message)
        self.msg = msgqueue.pop()

        for c in self.channel_list:
             self.server.privmsg( c, self.msg )
        self.irc.process_once()
        
    def feed_refresh():
        pass
            
if __name__ == "__main__":
    main()
