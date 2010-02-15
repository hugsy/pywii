from config import SLEEP_DURATION
from lib.wiimote import Wiimote
from lib.base import find_wiimotes
from time import sleep
import sys, os


class Server :
    """
    Server class for wiimote administration
    """

    PORT = 4321
    HOST = ''
    
    def __init__(self):
        self.clients = []        
        self.wiimote_threads = []
        self.nb_wiimote = 0

        # listen for client connection
        # self.listen_for_connections()

        # listen for wiimote
        self.listen_for_wiimotes()

        self.stop_all()

        
    def listen_for_connections (self):
        """
        Listen for clients connection on 4321/TCP 
        """
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        except socket.error, msg:
            sys.stderr.write (msg)
            s = None
            exit(1)

        try:
            s.bind((HOST, PORT))
            s.listen(1)
            if s is None: raise socket.error("Socket is None")
        except socket.error, msg:
            sys.stderr.write(msg)
            s.close()
            s = None
            exit(1)

        while True:
            rdy_r, rdy_w, rdy_x = select([s], [], [])

            if s in rdy_r:
                conn, addr = s.accept()
                # too late to continue ...

    
    def listen_for_wiimotes(self):
        """
        Listen for new wiimotes
        """
        attempts = 5 # for inifinite loop, set this to True
        
        while attempts :
            new_wiimotes = []
            new_wiimotes = find_wiimotes()
            
            for new_wiimote in new_wiimotes :
                self.start(new_wiimote)
                
            attempts -= 1
            if len (new_wiimotes) :
                break
            else :
                sleep(SLEEP_DURATION)

    
    def start(self, wiimote):
        """
        Start wiimote
        """
        if self.nb_wiimote > 4 :
            print ("Cannot handle more than 4 Wiimotes.")
            return

        self.nb_wiimote += 1
        wiimote_o = Wiimote(str(wiimote[0]), str(wiimote[1]), self.nb_wiimote)
        wiimote_o.start()
        self.wiimote_threads.append(wiimote_o)
                

    def stop(self, wiimote):
        """
        Stop wiimote
        """
        wiimote.join()
        
        
    def stop_all(self):
        """
        Stop all wiimotes
        """
        for wm in self.wiimote_threads :
            self.stop(wm)
    


            
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
           
