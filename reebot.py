#!/usr/bin/python
# -*- coding: utf-8 -*-
""" Reebot: Reevo IRC client 2nd generation"""

import irclib
irclib.DEBUG = False
import feedparser
import sys
import threading
import time
import os
import re

from config import *
from messages import messages
from reemongo import reemongo
from reefuncs import *

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
        self.irc.add_global_handler( 'privmsg', self.handlemessage )
        self.irc.add_global_handler( 'pubmsg', self.handlemessage )
        self.irc.add_global_handler( 'join', self.handlejoin )

        # Reefunc instance
        self.rf = reefuncs()
        
        # Server connection checker
        if self.server.is_connected():
            self.feed_refresh()
        
        # Go into an infinite loop
        self.irc.process_forever()

    def sendmessage(self, channel, message):
        """ Send messages function"""
        self.server.privmsg(channel, message)
        
    def ponger(self, connection, event):
        """ Send pong command """
        connection.pong(event.target())

    def reegex(self, argument):
        """ Check arguments """
        r = re.compile('(^reebot (.*))')
        m = re.match(r, argument)
        if m:
            return m.group(2)
            
    def handlemessage (self, connection, event):
        """ Handle public messages function
        
        argument -- message
        source -- origin of the message (nickname)
        target -- target of the command (channel)
        """
        argument = event.arguments() [0].lower()
        source = event.source().split( '!' ) [0]
        target = channels_list[0]
        
        if self.reegex(argument):
            try:
                for lines in self.rf.argparser(self.reegex(argument)).splitlines():
                    self.sendmessage( target, lines )
                    time.sleep(1) # Prevent floods
            except:
                # Avoid stdout messages
                # TODO: Reebot hangs when argparse prints help message (-h/--help)
                pass
        elif argument.find ( 'hola ' + nickname ) == 0:
            self.sendmessage( target, messages['hello'] + source )

    def handlejoin(self, connection, event):
        """ Handle channel join

        source -- user who has joined the channel
        target -- target of the command (channel)
        """
        source = event.source().split( '!' ) [0]
        target = event.target()

        # Check if user has been accessed before
        if self.db.users.find_one( { "user" : source } ) is None:
            # If not insert the nickname into the database
            self.db.users.insert( {
                "user" : source,
                "join_date" : time.strftime("%Y-%m-%d %H:%M:%S"),
                "channel" : [ target ]
            } )
            # Send welcome message to user
            for m in messages['welcome']:
                self.sendmessage( source, m )
                time.sleep(3)
            
    def feed_refresh(self):
        """ Read feeds and sends the news to the channel """
        
        msgqueue = []
        
        # Strip html tags regex
        r = re.compile('<.*?>')

        # Get feeds list from mongo
        feed_list = self.db.feed_list.find()

        # Loop over feeds list
        for feed in feed_list:
            feeds = feedparser.parse( feed['url'] )

            # Loop over entries
            for entry in feeds.entries:
                if self.db.log.find_one( { "url" : entry.link } ) is None:
                    msgqueue.append( feed['name'] + " ( " + feed['site'] + " ) | "
                        + " > " . join(map(lambda tag : re.sub(r, '', entry[tag]), feed['tags'])) )
                    # Insert link into log database
                    self.db.log.insert( { "url" : entry.link } )
                    
        # Send newer entries to the channel
        while len( msgqueue ) > 0:
            msgq = msgqueue.pop()
            for channel in channels_list:
                self.sendmessage( channel, msgq )

        time.sleep(2)
        # Refresh interval (every X seconds)
        threading.Timer( 10, self.feed_refresh ).start()

if __name__ == "__main__":
    main()
