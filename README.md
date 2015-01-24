# ReeBot

ReeBot es un bot utilizado para enviar notificaciones de las diferentes herramientas al canal de IRC de #reevo.


## Configuración

El archivo *sources.txt* debe contener el listado de feeds de la siguiente forma:
```
Nombre del feed|<URL DEL FEED>
```

Se incluye un script para obtener los feeds de repositorios gestionados con CGit.


## Ejecucion

Se incluye un script para iniciar el script como un servicio. Para configurarlo:

```
ln -s /ruta/a/reebot.sh /etc/init.d/reebot
```

Luego lo iniciamos como un servicio normal:

```
/etc/init.d/reebot start|stop|restart|status
```

## Licencia

ReeBot se publica bajo AGPLv3. Creado por el equipo de Reevo.

Moriras
