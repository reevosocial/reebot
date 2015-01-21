#!/usr/bin/python
""" rBot: Reevo IRC client 2nd generation"""

import irclib
irclib.DEBUG = False
import feedparser
import sys
import threading
import time
import os

from config import *
from messages import messages
from reemongo import reemongo

# Set default encoding
reload(sys)
sys.setdefaultencoding("utf-8")

def main():
    try:
        db = reemongo()
        c = rBot(db)
    except irclib.ServerConnectionError, e:
        exit()
    
class rBot:
    def __init__(self, db):
        """ IRC objects constructor """
        # MongoDB connection
        self.db = db

        # Create IRC object and connect to the network
        self.irc = irclib.IRC()
        self.server = self.irc.server()
        self.server.connect( irc_server, irc_port, nickname )

        # Join channels and send welcome message
        for channel in channels_list:
            self.server.join( channel )
	    self.sendmessage( channel, messages['che'] )

        # Register handlers
        self.irc.add_global_handler( 'ping', self.ponger, -42 )
        self.irc.add_global_handler( 'privmsg', self.handleprivmessage )
        self.irc.add_global_handler( 'pubmsg', self.handlepubmessage )
        self.irc.add_global_handler( 'join', self.handlejoin )

        # Server connection checker
        if self.server.is_connected():
            # Execute feed_refresh()
            self.feed_refresh()
        
        # Go into an infinite loop
        self.irc.process_forever()

    def sendmessage(self, channel, message):
        """ Send messages function"""
        self.server.privmsg(channel, message)
        
    def ponger(self, connection, event):
        """ Send pong command """
        connection.pong(event.target())

    def handleprivmessage (self, connection, event):
        """Handle private messages function
        
        argument -- message
        source -- origin of the message (nickname)
        """
        argument = event.arguments() [0].lower()
        source = event.source().split( '!' ) [0]
        
        if argument.find ( 'hola ' + nickname ) == 0:
            self.sendmessage( source, messages['hello'] + source )
             
    def handlepubmessage (self, connection, event):
        """ Handle public messages function
        
        argument -- message
        source -- origin of the message (nickname)
        target -- target of the command (channel)
        """
        argument = event.arguments() [0].lower()
        source = event.source().split( '!' ) [0]
        target = event.target()
        
        if argument.find ( 'hola ' + nickname ) == 0:
            self.sendmessage( target, messages['hello'] + source )

    def handlejoin(self, connection, event):
	""" Handle channel join

	source -- user who joined the channel
	"""
	source = event.source().split( '!' ) [0]
	self.sendmessage( source, messages['welcome'] )

    def feed_refresh(self):
        
        msgqueue = []

        # Get feeds list from mongo
        feed_list = self.db.feed_list.find()

        # Loop over feeds list
        for feed in feed_list:
            feeds = feedparser.parse( feed['url'] )

            # Loop over feeds entries
            for entry in feeds.entries:
                if self.db.log.find_one( { "url" : entry.link } ) is None:
                    msgqueue.append( feed['name']
                        + " | " + feeds.feed.title
                        + " > " + entry.title
                        + " : " + entry.link )
                    self.db.log.insert( { "url" : entry.link } )
                        
        while len( msgqueue ) > 0:
            msgq = msgqueue.pop()
            for channel in channels_list:
                self.sendmessage( channel, msgq )
                
        time.sleep(3)
        threading.Timer( 60, self.feed_refresh ).start()

if __name__ == "__main__":
    main()
