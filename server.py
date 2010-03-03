from config import SLEEP_DURATION
from lib.wiimote import Wiimote
from lib.base import find_wiimotes
from time import sleep
import sys, os


class Server :
    """
    PyWii is nothing less than a server that will listen for Wiimote
    actions and responds with system actions    
    """

    
    def __init__(self):
        """ initializes server """
        
        wiimotes_found = self.listen_for_wiimotes()
        
        if not wiimotes_found :
            return
            
        self.nb_wiimote = 0  # nb of running wiimotes
        self.start_all (wiimotes_found)  # fire up
        self.stop_all()  # clean and quit properly

    
    def listen_for_wiimotes(self):
        """ listen for new wiimotes """
        
        attempts = 3 # for inifinite loop, set this to True
        new_wiimotes = []
        
        while attempts :
            new_wiimotes = find_wiimotes()
            if len(new_wiimotes) > 0 :
                break
            else :
                attempts -= 1
            
        return new_wiimotes

    
    def start(self, wiimote):
        """ Start wiimote thread, and add it to the wiimote threads pool"""
        
        if self.nb_wiimote > 4 :
            print ("Cannot handle more than 4 Wiimotes.")
            return

        self.nb_wiimote += 1
        wiimote_o = Wiimote(str(wiimote[0]), str(wiimote[1]), self.nb_wiimote)
        wiimote_o.start()
        self.wiimote_threads.append(wiimote_o)

        
    def start_all(self, wiimotes):
        """ Starts all wiimotes """
        for new_wiimote in wiimotes :
            self.start(new_wiimote)
                

    def stop(self, wiimote):
        """ Stop wiimote """
        wiimote.join()
        
        
    def stop_all(self):
        """ Stop all wiimotes """
        for wm in self.wiimote_threads :
            self.stop(wm)
    


            
class Daemon :
    """
    Daemonize class based on Daemonizer, in Python for Unix Administration,
    by Gift & Noah
    """

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
            if pid > 0 : exit(0)
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
           
