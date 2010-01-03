from config import SLEEP_DURATION
from lib.wiimote import Wiimote
from lib.base import find_wiimotes
from time import sleep
import sys, os


class Server :

    def __init__(self):
        # self.wiimotes = [('00:19:1D:B7:43:0D', 'Nintendo RVL-CNT-01')] # for debug 
        self.wiimotes = []
        self.clients = []        
        self.wiimote_threads = []

        self.clients = self.listen_for_connections()
        self.wiimotes = self.listen_for_wiimotes()

        self.proceed()
        

    def listen_for_wiimotes(self):
        wiimotes = []
        attempts = 5 # for inifinite loop, set this to True
        
        while attempts :
            wiimotes = find_wiimotes()
            attempts -= 1
            if len (wiimotes) :
                break
            else :
                sleep (SLEEP_DURATION)

        return wiimotes

    
    def proceed(self):

        if len(self.wiimotes) == 0 :
            print ("No Wiimote found")
            exit (128)
        elif len(self.wiimotes) > 4 :
            print ("Cannot handle more than 4 Wiimotes. Truncating to 4 first entries")
            self.wiimotes = self.wiimotes[0:4]
        
        idx = 1
        for wm in wiimotes:
            wiimote = Wiimote(str(wm[0]), str(wm[1]), idx)
            wiimote.start()
            self.wiimote_threads.append(wiimote)
            idx += 1
        
        for wm in self.wiimote_threads :
            wm.join()


            
class Daemon :
    """
    Daemonize class based on Daemonizer, in Python for Unix Administration, Gift & Noah
    """

    instance = None
    startmsg = 'started with pid %s'
    
    def __init__(self, instance):
        """
        Initiating the instance
        """
        self.instance = instance
        instance.run()

    def fork(self):
        """
        Fork procedure
        """
        try:
            pid = os.fork() 
            if pid > 0 :
                exit(0)
        except OSError, e: 
            sys.stderr.write("Fork failed (%d) %s\n" % (e.errno, e.strerror))
            exit(1)
            
        return pid

    def deamonize(self):
        """
        Set the process as a daemon
        """
        
        # first fork
        pid = self.fork()
        
        # detach from parent environment
        os.chdir('/')
        os.umask(0)
        os.setsid()
        
        # second fork
        pid = self.fork()
           
        for stream in sys.stdout, sys.stderr:
            stream.flush()
    
        si = file(self.instance.stdin, 'r')
        so = file(self.instance.stdout, 'a+')
        se = file(self.instance.stderr, 'a+', 0)
    
        pid = str(os.getpid())
    
        sys.stderr.write("\n%s\n" % self.startmsg % pid)
        sys.stderr.flush()
    
        if self.instance.pidfile:
            file(self.instance.pidfile,'w+').write("%s\n" % pid)

        # dup-ing std input/outputs
        os.dup2(si.fileno(), sys.stdin.fileno())
        os.dup2(so.fileno(), sys.stdout.fileno())
        os.dup2(se.fileno(), sys.stderr.fileno())
           
