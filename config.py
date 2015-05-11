#!/usr/bin/python
# -*- coding: utf-8 -*-

# IRC server params
nickname = "reebot"
channels_list = [ "#reevo" ]
irc_server = "irc.freenode.org"
irc_port = 6667

# Database params
db_params = {
    'uri' : 'mongodb://127.0.0.1:27017',
    'database' : 'reevo',
    'feed_list' : 'feed_list',
    'log' : 'log',
    'users' : 'users',
}
