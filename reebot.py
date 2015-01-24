#!/usr/bin/python
#
# ReeBot informs updated in RSS/Atom channels
#
# based in IRC b0t by Akarsh Simha
#
# Licensed under the GNU General Public License v3


import irclib
import feedparser
import os
import threading
import time


nick = "reebot" # Name of the creature
channel_list = [ "#reevo" ] # Put in a list of channels


sources = os.path.dirname(os.path.realpath(__file__)) + "/sources.txt"
f = open(sources)
feed_list = f.readlines()
f.close()

old_entries_file = os.path.dirname(os.path.realpath(__file__)) + "/feeds.log"
if not os.path.exists(old_entries_file):
    open(old_entries_file, 'w').close() 


irc = irclib.IRC()
server = irc.server()

server.connect( "irc.freenode.org", 6667, nick ) # TODO: Make this general
# server.privmsg( "NickServ", "identify " )

msgqueue = []

def feed_refresh():
 #print "Test"
 FILE = open( old_entries_file, "r" )
 filetext = FILE.read()
 FILE.close()
 for feed in feed_list:
  NextFeed = False
  name,url = feed.split("|")
  d = feedparser.parse( url )
  for entry in d.entries:
   id = entry.link.encode('utf-8')+entry.title.encode('utf-8')
   if id in filetext:
    NextFeed = True
   else:
    FILE = open( old_entries_file, "a" )
    #print entry.title + "\n"
    FILE.write( id + "\n" )
    FILE.close()
    msgqueue.append( name + " | " + d.feed.title.encode('utf-8') + " > " + entry.title.encode('utf-8') + " : " + entry.link.encode('utf-8') )
   if NextFeed:
    break;

 t = threading.Timer( 10.0, feed_refresh ) # TODO: make this static
 t.start()

for channel in channel_list:
  server.join( channel )

feed_refresh()

while 1:
 while len(msgqueue) > 0:
  msg = msgqueue.pop()
  for channel in channel_list:
   # server.notice( channel, msg )
   server.privmsg( channel, msg )
 time.sleep(3) # TODO: Fix bad code
 irc.process_once()
 time.sleep(3) # So that we don't hog the CPU!
