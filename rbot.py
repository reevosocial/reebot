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

def main():
    try:
        c = rBot()
    except irclib.ServerConnectionError, e:
        exit()
    
class rBot:
    def __init__(self, connection_interval=60):
        """ IRC objects constructor """
        # Create IRC object and connect to the network
        self.irc = irclib.IRC()
        self.server = self.irc.server()
        self.server.connect( irc_server, irc_port, nickname )

        # Join channels and send welcome message
        for channel in channels_list:
            self.server.join( channel )
            self.sendmessage( channel, welcome_message )

        # Register handlers
        self.irc.add_global_handler( 'ping', self.ponger, -42 )
        self.irc.add_global_handler( 'privmsg', self.handleprivmessage )
        self.irc.add_global_handler( 'pubmsg', self.handlepubmessage )

        if connection.is_connected() is True:
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
        
        if argument.find ( 'hola r33bot' ) == 0:
            self.sendmessage( source, 'hola ' + source )
             
    def handlepubmessage (self, connection, event):
        """ Handle public messages function
        
        argument -- message
        source -- origin of the message (nickname)
        target -- target of the command (channel)
        """
        argument = event.arguments() [0].lower()
        source = event.source().split( '!' ) [0]
        target = event.target()
        
        if argument.find ( 'hola r33bot' ) == 0:
            self.sendmessage( target, 'hola ' + source )

    def feed_refresh(self):

        old_feeds = []
        new_feeds = []
        msgqueue = []

        # Reading old feeds from feeds.log file
        with open( log_path, 'r' ) as f:
            old_feeds = [ line.strip() for line in f ]

        # Loop over feeds list
        for feed_source in feed_list:
            name, source = feed_source.split( '|' )
            feeds = feedparser.parse( source )

            # Loop over feeds entries
            for entry in feeds.entries:
                link = [ entry.link.encode('utf-8') ]
                # If link doesn't exists in old feeds add it to msgqueue list 
                if link[0] not in old_feeds:
                    msgqueue.append( name
                        + " | " + feeds.feed.title.encode( 'utf-8' )
                        + " > " + entry.title.encode( 'utf-8' )
                        + " : " + entry.link.encode( 'utf-8' ) )
                    new_feeds.append(link[0])

        # Insert new feeds into feeds.log 
        nf = open( log_path, "a" )
        for item in new_feeds:
            nf.write( "%s\n" % item )
        nf.close()

        while len( msgqueue ) > 0:
            msgq = msgqueue.pop()
            for channel in channels_list:
                self.sendmessage( channel, msgq )
                
        time.sleep(3)
        threading.Timer( 60, self.feed_refresh ).start()

if __name__ == "__main__":
    main()
