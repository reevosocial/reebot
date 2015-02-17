#!/usr/bin/python
# -*- coding: utf-8 -*-

import argparse
import subprocess

class reefuncs:
    """ Parse arguments and execute functions

        usage: reebot [-h] [-t TASK [TASK ...]] [-p SERVER [SERVER ...]] [-m MESSAGE [MESSAGE ...]]

        Reebot functions

        optional arguments:
        -h, --help            show this help message and exit
        -t TASK [TASK ...], --task TASK [TASK ...]
                        show task status
        -p SERVER [SERVER ...], --ping SERVER [SERVER ...]
                        send ping to server
        -m MESSAGE [MESSAGE ...], --msg MESSAGE [MESSAGE ...]
                        send message
    """
    def __init__(self):
        pass

    def argparser(self,arguments):
        # Create parser
        parser = argparse.ArgumentParser(prog='reebot', description='Reebot functions')
        
        # Adding arguments
        parser.add_argument('-t', '--task', type=self.task, help='show task status', action='store', dest='task', nargs='+')
        parser.add_argument('-p', '--ping', type=self.ping, help='send ping to server', action='store', dest='server', nargs='+')
        parser.add_argument('-m', '--msg', help='send message', action='store', dest='message', nargs='+')
                            
        # Parsing arguments
        args = parser.parse_args(arguments.split())
        
        # Put responses in a list (the library may already do this...)
        responses = [args.task, args.server, args.message]

        # Return responses
        for r in responses:
            if r:
                return ' ' . join(r)
        
    def task(self, task):
        return "Print the task number %s" % task

    def ping(self, host):
        ping = ['ping','-v', '-c 3', host]
        process = subprocess.Popen(ping, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = process.communicate()
        return out


