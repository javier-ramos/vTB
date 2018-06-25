


from cmd import Cmd
from os import isatty
from select import poll, POLLIN
import sys
import time
import os
import atexit
import subprocess
from time import sleep
from resource import getrlimit, setrlimit, RLIMIT_NPROC, RLIMIT_NOFILE
from select import poll, POLLIN, POLLHUP
from subprocess import call, check_call, Popen, PIPE, STDOUT
import re
from fcntl import fcntl, F_GETFL, F_SETFL
from os import O_NONBLOCK
import os
from functools import partial


class shell( Cmd ):
    

    prompt = 'vTB> '
    def __init__( self, vTB, stdin=sys.stdin):
       
        self.vtb = vTB
        # Attempt to handle input
        self.stdin = stdin
        self.inPoller = poll()
        self.inPoller.register( stdin )
        Cmd.__init__( self )
        print( '*** Starting Shell:\n' )
        self.initReadline()
        self.run()

       
    readlineInited = False

    @classmethod
    def initReadline( cls ):
        "Set up history if readline is available"
        # Only set up readline once to prevent multiplying the history file
        if cls.readlineInited:
            return
        cls.readlineInited = True
        try:
            from readline import ( read_history_file, write_history_file,
                                   set_history_length )
        except ImportError:
            pass
        else:
            history_path = os.path.expanduser( '~/.vtb_history' )
            if os.path.isfile( history_path ):
                read_history_file( history_path )
                set_history_length( 1000 )
            atexit.register( lambda: write_history_file( history_path ) )

    def run( self ):
        "Run our cmdloop(), catching KeyboardInterrupt"
        while True:
            try:
                self.cmdloop()
                break
            except KeyboardInterrupt:
                # Output a message - unless it's also interrupted
                # pylint: disable=broad-except
                try:
                    output( '\nInterrupt\n' )
                except Exception:
                    pass
                # pylint: enable=broad-except

    def emptyline( self ):
        "Don't repeat last command when you hit return."
        pass

    def getLocals( self ):
        "Local variable bindings for py command"
        self.locals.update( self.mn )
        return self.locals

    def do_sh( self, line ):
        """Run an external shell command
           Usage: sh [cmd args]"""
        assert self  # satisfy pylint and allow override
        call( line, shell=True )

   
    def do_xterm( self, line, term='xterm' ):
        """Spawn xterm(s) for the given node(s).
           Usage: xterm node1 node2 ..."""
        args = line.split()
        if not args:
            error( 'usage: %s node1 node2 ...\n' % term )
        else:
            for arg in args:
                #if arg not in self.mn:
                #   error( "node '%s' not in network\n" % arg )
                #else:

                pid = subprocess.Popen(args=["xterm","-e"," python getCMD.py %s"%arg]).pid
                    #node = self.mn[ arg ]
                    #self.mn.terms += makeTerms( [ node ], term = term )
    def do_gterm( self, line, term='gterm' ):
        """Spawn xterm(s) for the given node(s).
           Usage: xterm node1 node2 ..."""
        args = line.split()
        if not args:
            error( 'usage: %s node1 node2 ...\n' % term )
        else:
            for arg in args:
                #if arg not in self.mn:
                #   error( "node '%s' not in network\n" % arg )
                #else:

            
                pid = subprocess.Popen(args=["gnome-terminal","-e" ,"python getCMD.py %s"%arg]).pid

#                pid = subprocess.Popen(args=["gnome-terminal -x","python getCMD.py %s"%arg]).pid
                    #node = self.mn[ arg ]
                    #self.mn.terms += makeTerms( [ node ], term = term )
    def do_exit( self, _line ):
        "Exit"
        assert self  # satisfy pylint and allow override
        return 'exited by user command'

    def do_quit( self, line ):
        "Exit"
        return self.do_exit( line )

    def do_EOF( self, line ):
        "Exit"
        output( '\n' )
        return self.do_exit( line )

    def isatty( self ):
        "Is our standard input a tty?"
        return isatty( self.stdin.fileno() )


    def default( self, line ):
        """Called on an input line when the command prefix is not recognized.
           Overridden to run shell commands when a node is the first
           CLI argument.  Past the first CLI argument, node names are
           automatically replaced with corresponding IP addrs."""

      

       
        error( '*** Unknown command: %s\n' % line )

    def precmd( self, line ):
        "allow for comments in the cli"
        if '#' in line:
            line = line.split( '#' )[ 0 ]
        return line


# Helper functions

def isReadable( poller ):
    "Check whether a Poll object has a readable fd."
    for fdmask in poller.poll( 0 ):
        mask = fdmask[ 1 ]
        if mask & POLLIN:
            return True
