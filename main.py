#!/usr/bin/env python
import cmd
import os
import sys
import socket

class cmdSSG(cmd.Cmd):
    """This is a terminal for the LUSTRO BEXUS experiment. \nIt allows the operator to set all of the experiment's\nconfigureable parametres, like motor's speed and measurements\nfrequency."""
    #variables & mechanics of cmd
    speed1 = 0
    speed2 = 0
    port = 0
    ip = ""
    timeout = 0

    def handshake():
        """check weather connection with OBC is possible"""
        sock = socket.socket(socket.AF_INET, soclet.SOCK_DGRAM)
        sock.connect("localhost", 12000)

    def send(self, msg):
        try:
            sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
            sock.connect((self.ip, self.port))
            msg=bytes(msg, 'utf-8')
            sock.send(msg)
            sock.shutdown(socket.SHUT_RDWR)
            sock.close()
        except OSError as err:
            print("OS error: {0}".format(err))
            sock.shutdown(socket.SHUT_RDWR)
            sock.close()
        except ValueError:
            print("Could not convert data to an integer.")
            sock.shutdown(socket.SHUT_RDWR)
            sock.close()
        except:
            print("Unexpected error:", sys.exc_info()[0])
            sock.shutdown(socket.SHUT_RDWR)
            sock.close()
            raise
            
    def do_tmp(self, msg):
        self.send(msg)
        
    def configure(conf_file, ip, port):
        #TODO: czy wszystkie wyjatki obsluzone? co jezeli nie ma pliku?
        try:
            f=open(conf_file)
            line = f.readline()
            port, ip = line.split()
        except OSError:
            print("file ",conf_file," cannot be found. File will be created now.\nPlease pass the ip:")
            try:
                fo=open(conf_file, "w+")
                fo.write(self.port," ",self.ip)
            except OSError as e:
                print("OS error: ",e)
            else:
                fo.close()
            ip = input("abc")
            print("Pass the port:")
            port = int(sys.stdin)
            print(ip," ",port)
            
        else:
            f.close()

    def preloop(self):
        print("Starting GSS...")
        configfilename = "config.cfg"
        self.speed1 = 0
        self.speed2 = 0
        self.port = 0
        self.ip = ""
        self.timeout = 0
        
        #configure
        print("setting networking parameters...")
        try:
            f=open(configfilename)
            line = f.readline()
            self.port, self.ip = line.split()
            self.ip = int(self.ip)
            print("port: ",self.port)
            print("ip: ",self.ip)
        except OSError:
            print("file ",configfilename," cannot be found. File will be created now.")
            try:
                fo=open(configfilename, "w+")
                self.ip = input("Please pass the ip:\n")
                self.port = int(input("Pass the port:\n"))
                tmp = self.ip + " " + str(self.port)
                fo.write(tmp)
            except OSError as e:
                print("OS error: ",e)
                raise SystemExit
            else:
                fo.close()
                
            print(self.ip," ",self.port)
        except ValueError as e:
            print("OS error: ",e,"\nPlease review how config.cfg file looks like")
            raise SystemExit
        else:
            f.close()
        #TODO: handshake

    def do_shell(self, line):
        """Run a shell command"""
        print ("running shell command:", line)
        output = os.popen(line).read()
        print (output)
        self.last_output = output

    
    # Commands
    # *operational:
    def do_stopm(self, args):
        """Stop motors"""
        pass
        
    def do_go_idle(self, a):
        """Turn off the motors and data gathering"""
        pass

    def do_status(self, args):
        """Check experiment's status"""
        pass

    def do_go_scanning(self, args):
        """Turn the scanning mode on"""
        pass

    def do_send_nth(self, args):
        """Send every N-th set of measurements to Ground Station"""
        pass
    
    def do_get_htp(self, args):
        """Get humidity, temperature and pressure data"""
        pass

    def do_get_photo(self, args):
        """Get data from set of photodetectors"""
        pass

    def do_get_speed(self, args):
        """Get actual motor's speed"""
        pass

    def do_get_speed_fast(self, args):
        """Display last motors' speeds set by set-speed command"""
        print("speed motor1: {0}\nspeed motor2: {1}".format(self.speed1, self.speed2))

    def do_get_uc_temp(self, args):
        """Check the microcontroller's temperature"""
        pass

    def do_go_manual(self, args):
        """Check the microcontroller's temperature"""
        pass

    def do_set_speed(self, args):
        #TODO: przekazac speed1 i speed2
        """set selected (arg1 [1-2]) motor's speed (arg2 [0-255])"""
        arg1,arg2 = args.split()
        arg1 = int(arg1)
        arg2 = int(arg2)
        if (arg1 == 1 or arg1 == 2) and (arg2 > 0 and arg2 < 256):
            if arg1 ==1:
                self.speed1 = arg2;
                print("speed of motor no 1 is set to {0}".format(arg2))
            elif arg1 == 2:
                self.speed2 = arg2;
                print("speed of motor no 2 is set to {0}".format(arg2))
        elif not (arg1 == 1 or arg1 == 2):
            print("First argument must be 1 or 2! Enter 'help' for more info")
        else:
            print("Second argument must be from 0-255!")
    
    def do_set_frequency(self, args):
        """set measurements' frequency according to arg value"""
        pass

    def do_mknlog(self, args):
        """make new logfile on SD card"""
        pass

    def do_save_htp(self, args):
        """Save humidity, temperature and pressure data on SD card"""
        pass
    
    # *networking:
    def do_set_ip(self, args):
        """set destination's ip as arg and save it in configfile"""
        pass

    def do_set_port(self, args):
        """set destination's targeted port as arg and save it in """
        pass

    def do_set_address(self, args):
        """set destination's ip as arg1 and port as arg2 and save them in configile"""
        pass

    def do_show_address(self, args):
        """display current destination's ip and port from configfile"""
        pass

    # *other
    def do_help(self, args):
        """help command"""
        f = open('help.info', 'r')
        print (f.read())
        f.close()
    
    def do_exit(self, args):
        """close the program"""
        print ("Exiting")
        raise SystemExit

    

    

    

    

    

if __name__ == "__main__":
    # execute only if run as a script
    prompt = cmdSSG()
    prompt.prompt = '> '
    prompt.cmdloop('GSS waiting for commands')
