#!/usr/bin/env python
import cmd, os, sys, socket, logging, datetime

class cmdSSG(cmd.Cmd):
    """This is a terminal for the LUSTRO BEXUS experiment. \nIt allows the operator to set all of the experiment's\nconfigureable parametres, like motor's speed and measurements\nfrequency."""
    #variables & mechanics of cmd
    speed1 = 0
    speed2 = 0
    port = 0
    ip = ""
    TIMEOUT = 2.0  # in sec
    BUFFER_SIZE = 1024
    configfilename = "config.cfg"
    command_dict = {}
    results_file = "readings.txt"

    def send(self, msg):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((self.ip, int(self.port)))
        sock.send(msg.encode("utf-8"))
        sock.close()


    def streamDown(self):
        # TODO: write to file
        try:
            sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
            sock.bind((self.ip, int(self.port)))
            print("Waiting for data...")
            if os.path.exists(self.results_file):
                aw = 'a'
            else:
                aw = 'w'
            f = open(self.results_file, aw)
            while True:
                logging.debug('debug msg')
                sock.settimeout(self.TIMEOUT)
                data, address = sock.recvfrom(self.BUFFER_SIZE)
                # TODO: check recvfromto
                f.write(data.decode("utf-8"))

        except OSError as err:
            print("OS error: {0}".format(err))
        except ValueError:
            print("Could not convert data to an integer.")
        except socket.timeout:
            print("Socket timeout. Data not received")
        except:
            print("Unexpected error:", sys.exc_info()[0])
            raise
        finally:
            print("Closing connection...")
            #sock.shutdown(socket.SHUT_RDWR)
            sock.close()
            f.close()

    def sendrec(self, msg):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((self.ip, int(self.port)))
        sock.send(msg.encode("utf-8"))
        try:
            sock.settimeout(self.TIMEOUT)
            data = sock.recv(self.BUFFER_SIZE)
        except socket.timeout:
            print("socket timeout. Data not received")
        else:
            sock.close()
            return data.decode("utf-8")

    def save_results(self, data):
        if os.path.exists(self.results_file):
            aw = 'a'
            print("appending to file")
        else:
            aw = 'w'
            print("file for result will be created")
        f = open(self.results_file, aw)
        f.write(data)
        f.close()

    # def do_tmp(self, msg):
    #     #self.send(msg)
    #     self.streamDown()
        
    # def configure(conf_file, ip, port):
    #     try:
    #         f=open(conf_file)
    #         line = f.readline()
    #         port, ip = line.split()
    #     except OSError:
    #         print("file ",conf_file," cannot be found. File will be created now.\nPlease pass the ip:")
    #         try:
    #             fo=open(conf_file, "w+")
    #             fo.write(self.port," ",self.ip)
    #         except OSError as e:
    #             print("OS error: ",e)
    #         else:
    #             fo.close()
    #         ip = input("abc")
    #         print("Pass the port:")
    #         port = int(sys.stdin)
    #         print(ip," ",port)
    #
    #     else:
    #         f.close()

    def preloop(self):
        # setting up logger
        # TODO: poprawic printy i logi (osobna funkcja do printowania i jednoczesnego logowania)
        log_name = datetime.datetime.now().strftime("%y%m%d") + ".log"
        log_formatter = logging.Formatter(fmt="%(asctime)s %(levelname)s: %(message)s",
                                          datefmt='%Y/%m/%d %H:%M:%S'
                                          )
        root_logger = logging.getLogger()
        root_logger.setLevel(logging.DEBUG)

        # handler for logging to file
        file_handler = logging.FileHandler(log_name)
        file_handler.setFormatter(log_formatter)
        root_logger.addHandler(file_handler)

        # handler for logging into stream
        # console_handler = logging.StreamHandler()
        # #console_handler = logging.StreamHandler(sys.stdout)
        # root_logger.addHandler(console_handler)

        self.speed1 = 0
        self.speed2 = 0
        self.port = 0
        self.ip = ""
        self.TIMEOUT = 2.0
        
        #configure
        logging.info("setting networking parameters...")
        try:
            f=open(self.configfilename, "r+")
            line = f.readline()
            ip_tmp, port_tmp = line.split()
            try:
                self.port = int(port_tmp)
                if not (self.port <= 65535 and self.port >= 0):
                    # TODO: tu skończyłem
                    msg = 'port value in configure file outside of range.'
                    logging.error(msg)
                    print(msg)
                    self.port = input()
                    f.seek(0)
                    f.write(ip_tmp + " " + self.port)
            except ValueError as e:
                logging.error('Configure file error: ' + str(e))
                self.port = input("Pass correct value now:\n")
            try:
                socket.inet_aton(ip_tmp)
            except socket.error:
                logging.error('Ip address error in configuration file.')
                self.ip = input("Pass correct value now:\n")
            else:
                self.ip = ip_tmp
        except OSError:  # no config file
            print("file ",self.configfilename, " cannot be found. File will be created now.")
            try:
                fo=open(self.configfilename, "w+")
                self.ip = input("Please pass the ip:\n")
                self.port = int(input("Pass the port:\n"))
                msg = self.ip + " " + str(self.port)
                fo.write(msg)
            except OSError as e:
                logging.error("OS error: ", e)
                raise SystemExit
            finally:
                fo.close()

            print(self.ip," ",self.port)
        except ValueError as e:
            print("OS error: ", e, "\nPlease review how config.cfg file looks like")
            f.close()
            raise SystemExit
        else:
            logging.info("port: " + str(self.port))
            logging.info("ip: " + str(self.ip))
            f.close()
        
        #setting commands codes
        try:
            f=open("command.dict", "r")
            for line in f:
                tmp1,tmp2 = line.split()
                self.command_dict[tmp2] = tmp1
        except KeyError as e:
            print("key is not in the map. Original message: " + e)
        except OSError as e:
            print("OS error: ", e)
            raise SystemExit
        finally:
            f.close()

    def do_shell(self, line):
        """Run a shell command"""
        print ("running shell command:", line)
        output = os.popen(line).read()
        print (output)
        self.last_output = output

    # Commands
    # *operational:
    def do_strem_cont(self):
        """Continuous reading data from OBC"""
        # TODO: dodac do helpa
        self.streamDown()

    def do_stopm(self, args):
        """Stop motors"""
        self.send(self.command_dict["sudo_stopm"])

    def do_go_idle(self, a):
        """Turn off the motors and data gathering"""
        self.send(self.command_dict["sudo_set_status"]+"0")

    def do_status(self, args):
        """Check experiment's status"""
        self.send(self.command_dict["get_status"])

    def do_go_scanning(self, args):
        """Turn the scanning mode on"""
        self.send(self.command_dict["sudo_set_status"] + "1")
        self.streamDown()

    def do_send_nth(self, args):
        """Send every N-th set of measurements to Ground Station"""
        self.send(self.command_dict["send_nth"] + str(args))
        self.streamDown()
    
    def do_get_htp(self, args):
        """Get humidity, temperature and pressure data"""
        data = self.sendrec(self.command_dict["get_htp"])
        self.save_results(data)

    def do_get_photo(self, args):
        """Get data from set of photodetectors"""
        data = self.sendrec(self.command_dict["get_photo"])
        self.save_results(data)

    def do_get_speed(self, args):
        """Get actual motor's speed"""
        # TODO: brakuje komendy
        data = self.sendrec(self.command_dict["get_speed"])
        self.save_results(data)

    def do_get_speed_fast(self, args):
        """Display last motors' speeds set by set-speed command"""
        print("speed motor1: {0}\nspeed motor2: {1}".format(self.speed1, self.speed2))

    def do_get_uc_temp(self, args):
        """Check the microcontroller's temperature"""
        data = self.sendrecv(self.command_dict["get_uc_temp"])
        self.save_results(data)

    def do_go_manual(self, args):
        """Enable additional commands: set_speed, set_frequency, mknlog, save_htp"""
        self.send(self.command_dict["sudo_set_status"] + " 2")

    def do_set_speed(self, args):
        #TODO: usunac speed2 po rozmowie z Mikolajem
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
            return
        else:
            print("Second argument must be from 0-255!")
            return
        self.send(self.command_dict["set_speed"] + " " + self.speed1)
    
    def do_set_frequency(self, args):
        """set measurements' frequency according to arg value"""
        # TODO: brak komendy
        # TODO: check weather amount of parameters is right and if they are correct
        self.send(self.command_dict["set_frequency"] + args)

    def do_mknlog(self, args):
        """make new logfile on SD card"""
        self.send(self.command_dict["mknlog"])

    def do_save_htp(self, args):
        """Save humidity, temperature and pressure data on SD card"""
        # TODO: brak komendy
        self.send(self.command_dict["save_htp"])
    
    # *networking:
    def do_set_ip(self, args):
        """set destination's ip as arg and save it in configfile"""
        self.ip = args
        try:
            f=open(self.configfilename, "r+")
            line = self.ip + " " + str(self.port)
            f.seek(0)
            f.write(line)
            print("ip set to: ",self.ip)
        except ValueError as e:
            print("OS error: ",e,"\nPlease review how config.cfg file looks like")
            raise SystemExit
        else:
            f.close()

    def do_set_port(self, args):
        """set destination's targeted port as arg and save it in """
        self.port = args
        try:
            f=open(self.configfilename, "r+")
            line = self.ip + " " + str(self.port)
            f.seek(0)
            f.write(line)
            print("port set to: ", self.port)
        except ValueError as e:
            print("OS error: ", e, "\nPlease review how config.cfg file looks like")
            raise SystemExit
        else:
            f.close()

    def do_set_address(self, args):
        """set destination's ip as arg1 and port as arg2 and save them in configile"""
        self.ip,self.port = args.split()
        try:
            f=open(self.configfilename, "r+")
            line = self.ip + " " + str(self.port)
            f.seek(0)
            f.write(line)
            print("ip set to: ",self.ip)
            print("port set to: ",self.port)
        except ValueError as e:
            print("OS error: ", e, "\nPlease review how config.cfg file looks like")
            raise SystemExit
        else:
            f.close()

    def do_show_address(self, args):
        """display current destination's ip and port from configfile"""
        print("Current address: " + self.ip + "/" + str(self.port))

    def do_set_timeout(self, args):
        """set timeout time in seconds for UDP receiving socket"""
        try:
            self.TIMEOUT = float(args)
        except ValueError:
            logging.error("Wrong value. It should be number")
        else:
            logging.info("Timeout value changed to " + str(self.TIMEOUT))
        # TODO: add to help

    # *other
    def do_help(self, args):
        """help command"""
        f = open('help.info', 'r')
        print (f.read())
        f.close()
    
    def do_exit(self, args):
        """close the program"""
        logging.info("Exiting")
        raise SystemExit


if __name__ == "__main__":
    # execute only if run as a script
    prompt = cmdSSG()
    prompt.prompt = '> '
    prompt.cmdloop('GSS waiting for commands')
