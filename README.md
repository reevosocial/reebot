# rBot (reebot IRC client 2nd generation)

## TODO:
- Optimizar el modo en que el bot chequea los feeds ya leídos:
 - Eliminar fichero feeds.log e implementar MongoDB
 - Usar ETag para reducir el número de peticiones: https://pythonhosted.org/feedparser/http-etag.html
- Implementar algunos register handlers
```
irc.add_global_handler ( 'part' , handlePart ) #handles parts
irc.add_global_handler ( 'quit' , handleQuit ) #handles quits
irc.add_global_handler ( 'kick' , handleKick ) #handles kicks
irc.add_global_handler ( 'mode' , handleMode ) #handles mode changes
irc.add_global_handler ( 'topic' , handleTopic ) #handles topic changes
irc.add_global_handler ( 'privmsg', handlePrivMessage ) #private messages
irc.add_global_handler ( 'pubmsg', handlePubMessage ) #public channel messages
irc.add_global_handler ( 'invite', handleInvite ) #invite
irc.add_global_handler ( 'privnotice', handlePrivNotice ) #Private notice
irc.add_global_handler ( 'welcome', handleEcho ) # Welcome message
irc.add_global_handler ( 'yourhost', handleEcho ) # Host message
irc.add_global_handler ( 'created', handleEcho ) # Server creation message
irc.add_global_handler ( 'myinfo', handleEcho ) # "My info" message
irc.add_global_handler ( 'featurelist', handleEcho ) # Server feature list
irc.add_global_handler ( 'luserclient', handleEcho ) # User count
irc.add_global_handler ( 'luserop', handleEcho ) # Operator count
irc.add_global_handler ( 'luserchannels', handleEcho ) # Channel count
irc.add_global_handler ( 'luserme', handleEcho ) # Server client count
irc.add_global_handler ( 'n_local', handleEcho ) # Server client count/maximum
irc.add_global_handler ( 'n_global', handleEcho ) # Network client count/maximum
irc.add_global_handler ( 'luserconns', handleEcho ) # Record client count
irc.add_global_handler ( 'luserunknown', handleEcho ) # Unknown connections
irc.add_global_handler ( 'motdstart', handleEcho ) # Message of the day ( start )
irc.add_global_handler ( 'motd', handleNoSpace ) # Message of the day
irc.add_global_handler ( 'edofmotd', handleEcho ) # Message of the day ( end )
irc.add_global_handler ( 'join', handleJoin ) # Channel join
irc.add_global_handler ( 'namreply', handleNoSpace ) # Channel name list
irc.add_global_handler ( 'endofnames', handleNoSpace ) # Channel name list ( end )
```
- Crear función que envíe ping a beta.reevo.org y mande aviso al canal IRC si no responde
- Crear módulo con diccionario de funciones de respuesta a argumentos

