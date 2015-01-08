#!/usr/bin/python
"""rBot (reebot) sends information to IRC channel"""

import irclib
irclib.DEBUG = True
import feedparser
import sys
import threading
import time
import json
from config import *

def main():
    try:
        c = rBot()
    except irclib.ServerConnectionError, e:
        print( "Error: %s" % e )
        exit()
        
    c.feed_refresh()
        
class rBot:
    def __init__(self):
        self.irc = irclib.IRC()
        self.server = self.irc.server()
        self.server.connect( IRC_SERVER, IRC_PORT, NICK )
 
        for c in CHANNEL_LIST:
            self.server.join( c )
            self.sendmessage( c, "Che, I am here!" )
        
        self.feed_list = FEED_LIST
        self.irc.process_forever()

    def sendmessage(self, channel, message):
        self.server.privmsg( channel, message )
        
    def feed_refresh(self):
        
        old_feeds = []
        new_feeds = []
        msgqueue = []
        
        with open( 'feeds.log', 'r' ) as f:
            old_feeds = [ line.strip() for line in f ]
            
        for feed in self.feed_list:
            name, source = feed.split( "|" )
            d = feedparser.parse( source )
            
            for entry in d.entries:
                link = [ entry.link.encode('utf-8') ]
                if link[0] not in old_feeds:
                    msgqueue.append( name
                        + " | " + d.feed.title.encode('utf-8')
                        + " > " + entry.title.encode('utf-8')
                        + " : " + entry.link.encode('utf-8') )
                    new_feeds.append(link[0])
                    
        nf = open("feeds.log", "a")
        for item in new_feeds:
            nf.write("%s\n" % item)
        nf.close()
        
        while len( msgqueue ) > 0:
            msgq = msgqueue.pop()
            for c in CHANNEL_LIST:
                self.sendmessage( c, msgq )

            # time.sleep(5)
        threading.Timer( 30, feed_refresh ).start()
            
if __name__ == "__main__":
    main()