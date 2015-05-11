#!/usr/bin/python
# -*- coding: utf-8 -*-

import argparse
import subprocess

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
        -k, --matate : restart reebot
    """
    def __init__(self):
        pass

    def argparser(self,arguments):
        # Create parser
        parser = argparse.ArgumentParser(prog='reebot', description='Reebot functions')
        
        # Adding arguments
        parser.add_argument('-t', '--task', type=self.task, help='show task status', action='store', dest='task', nargs='+')
        # parser.add_argument('-p', '--ping', type=self.ping, help='send ping to server', action='store', dest='host', nargs='+')
        parser.add_argument('-m', '--msg', help='send message', action='store', dest='message', nargs='+')
        # parser.add_argument('-i', '--info', type=self.info, help='print host information', action='store', dest='hostname', nargs='+')
        parser.add_argument('-k', '--matate', type=self.matate, help='killing myself', action='store', dest='matate')

        # Parsing arguments
        args = parser.parse_args(arguments.split())
        
        # Put responses in a list (the library may already do this...)
        responses = [args.task, args.message]

        # Return responses
        for r in responses:
            if r:
                return ' ' . join(r)
        
    def task(self, task):
        # return "Print the task number %s" % task
        pass

    def matate(self):
        cmd = ['/etc/init.d/reebot', 'stop']
        killreebot = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = killreebot.communicate()
        rc = killreebot.returncode
        return rc
        
    # def ping(self, host):
    #     """ Send ping to host """        
    #     msg = []
    #     cmd = ['ping', '-c 1', host]
    #     ping = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    #     out, err = ping.communicate()
    #     rc = ping.returncode
    #     msg.append('Host %s is %s\n' % \
    #                    (host, 'up' if rc == 0 else 'down'))
    #     return '\n'.join(msg)
