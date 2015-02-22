#!/usr/bin/python
# -*- coding: utf-8 -*-

# IRC server params
nickname = "rebot"
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

# Reevo servers
hosts = {
    'ergaster' : {
        'IP' : '88.80.186.30',
        'Descripción' : 'Servidor de pruebas',
        'Dominio' : 'peervox.org',
        'Localización' : 'London, England, UK', },
    'raddad' : {
        'IP' : '37.187.37.53',
        'Descripción' : 'Servidor de produccion',
        'Dominio' : 'reevo.org',
        'Localización' : 'Strasbourg, Francia', }
}
