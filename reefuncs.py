#!/usr/bin/python
# -*- coding: utf-8 -*-

import argparse
import subprocess
from config import hosts

class reefuncs:
    """ Parse arguments and execute functions

        usage: reebot [-h] [-t TASK] [-p SERVER] [-m MESSAGE] [-i HOSTNAME]

        Reebot functions

        optional arguments:
        -h, --help : show this help message and exit
        -t TASK [TASK ...], --task TASK [TASK ...] : show task status
        -p SERVER [SERVER ...], --ping SERVER [SERVER ...] : send ping to server
        -m MESSAGE [MESSAGE ...], --msg MESSAGE [MESSAGE ...] : send message
        -i HOSTNAME [HOSTNAME ...], --info HOSTNAME [HOSTNAME ...] : show host info

    """
    def __init__(self):
        pass

    def argparser(self,arguments):
        # Create parser
        parser = argparse.ArgumentParser(prog='reebot', description='Reebot functions')
        
        # Adding arguments
        parser.add_argument('-t', '--task', type=self.task, help='show task status', action='store', dest='task', nargs='+')
        parser.add_argument('-p', '--ping', type=self.ping, help='send ping to server', action='store', dest='host', nargs='+')
        parser.add_argument('-m', '--msg', help='send message', action='store', dest='message', nargs='+')
        parser.add_argument('-i', '--info', type=self.info, help='print host information', action='store', dest='hostname', nargs='+')
                            
        # Parsing arguments
        args = parser.parse_args(arguments.split())
        
        # Put responses in a list (the library may already do this...)
        responses = [args.task, args.host, args.hostname, args.message]

        # Return responses
        for r in responses:
            if r:
                return ' ' . join(r)
        
    def task(self, task):
        # return "Print the task number %s" % task
        pass

    def ping(self, host):
        """ Send ping to host """        
        msg = []
        if host in hosts.keys():
            cmd = ['ping', '-c 1', hosts[host]['IP']]
            ping = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            out, err = ping.communicate()
            rc = ping.returncode
            msg.append('Host %s (%s) is %s\n' % \
                       (host, hosts[host]['IP'], 'up' if rc == 0 else 'down'))
        return '\n'.join(msg)
    
    def info(self, host):
        """ Print hosts info """
        i = []
        for hostname, data in hosts.iteritems():
            if host == hostname:
                i.append('Nombre del servidor: %c%s%c' % (2, hostname, 2))
                for key, value in data.iteritems():
                    i.append('%s: %s' % (key, value))
                return '\n' . join(i)


