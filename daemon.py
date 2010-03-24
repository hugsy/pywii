from time import sleep
import sys, os  

            
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
           
