#!/usr/bin/env python
import cmd, os, sys, socket, logging, datetime, traceback

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

    def precmd(self, line):
        try:
            logging.info("Executing {0} method".format(line.split()[0]))
        except IndexError:
            logging.info("Exception omitted in case of empty line")
        return line

    # def send(self, msg):
    #     try:
    #         sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #         sock.connect((self.ip, int(self.port)))
    #         sock.settimeout(self.TIMEOUT)
    #         sock.send(msg.encode("utf-8"))
    #         sock.close()
    #     except socket.timeout:
    #         msg = "Socket timeout. Data not received"
    #         self.log_error(msg)
    #     except OSError:
    #         msg = "OS error. Trace in log."
    #         self.log_exception(msg)
    #     except KeyboardInterrupt:
    #         self.log_info("Method manually interrupted. Back to main loop")
    def send(self, msg):
        if len(msg) %2:
            msg = '0' + msg
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect((self.ip, int(self.port)))
            sock.settimeout(self.TIMEOUT)
            sock.send(bytes.fromhex(msg))
            sock.close()
        except socket.timeout:
            msg = "Socket timeout. Data not received"
            self.log_error(msg)
        except OSError:
            msg = "OS error. Trace in log."
            self.log_exception(msg)
        except KeyboardInterrupt:
            self.log_info("Method manually interrupted. Back to main loop")

    def log_exception(self, msg):
        logging.exception(msg=msg)
        print(msg)

    def log_error(self, msg):
        logging.error(msg=msg)
        print(msg)

    def log_warning(self, msg):
        logging.warning(msg=msg)
        print(msg)

    def log_info(self, msg):
        logging.info(msg=msg)
        print(msg)

    def streamDown(self):
        # TODO: keyboardinterrupt
        logging.info("streamDown method used")
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.connect((self.ip, int(self.port)))
            self.log_info("Waiting for data...")
            if os.path.exists(self.results_file):
                aw = 'a'
            else:
                aw = 'w'
            try:
                f = open(self.results_file, aw)
                while True:
                    # if timeout show message and continue, else save data to file
                    try:
                        sock.settimeout(self.TIMEOUT)
                    except socket.timeout:
                        msg = "Socket timeout. Data not received"
                        self.log_error(msg)
                    except KeyboardInterrupt:
                        self.log_info("Method manually interrupted. Back to main loop")
                    else:
                        data, address = sock.recvfrom(self.BUFFER_SIZE)
                        f.write(data.decode("utf-8"))
            except OSError:
                msg = "OS error. Trace in log."
                self.log_exception(msg)
        except OSError:
            msg = "OS error. Trace in log."
            self.log_exception(msg)

        except ValueError:
            msg = "Could not convert data to an integer."
            self.log_exception(msg)

        except KeyboardInterrupt:
            self.log_info("Method manually interrupted. Back to main loop")

        except:
            msg = "Unexpected error:", sys.exc_info()[0]
            self.log_exception(msg)
            raise

        finally:
            self.log_info("Closing connection...")
            #sock.shutdown(socket.SHUT_RDWR)
            sock.close()
            f.close()
            return

    def sendrec(self, msg):
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect((self.ip, int(self.port)))
            sock.send(msg.encode("utf-8"))
            sock.settimeout(self.TIMEOUT)
            data = sock.recv(self.BUFFER_SIZE)
        except socket.timeout:
            self.log_warning("Socket timeout. Data not received")
            return None
        except socket.error:
            self.log_error("Could not connect to chosen address")
            return None
        else:
            sock.close()
            return data.decode("utf-8")

    def save_results(self, data):
        if data is not None:
            if os.path.exists(self.results_file):
                aw = 'a'
                self.log_info("appending to file {0}".format(self.results_file))
            else:
                aw = 'w'
                self.log_info("file for result will be created")
            f = open(self.results_file, aw)
            f.write(data)
            f.close()
        else:
            self.log_info("Data = None - no data saved")

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

        logging.info("Starting new session")
        self.speed1 = 0
        self.speed2 = 0
        self.port = 0
        self.ip = ""
        self.TIMEOUT = 2.0
        
        #configure
        logging.info("Setting networking parameters...")
        try:
            f=open(self.configfilename, "r+")
            line = f.readline()
            ip_tmp, port_tmp = line.split()
            try:
                self.port = int(port_tmp)
                if not (self.port <= 65535 and self.port >= 0):
                    # TODO: poprawić tak żeby był pętla
                    msg = 'port value in configure file outside of range.'
                    self.log_error(msg)
                    self.port = input()
                    f.seek(0)
                    f.write(ip_tmp + " " + self.port)
            except ValueError as e:
                self.log_info('Configure file error: ' + str(e))
                self.port = input("Pass correct value now:\n")
            try:
                socket.inet_aton(ip_tmp)
            except socket.error:
                self.log_error('Ip address error in configuration file.')
                self.ip = input("Pass correct value now:\n")
            else:
                self.ip = ip_tmp
        except OSError:  # no config file
            self.log_warning("file " + self.configfilename + " cannot be found. File will be created now.")
            try:
                fo=open(self.configfilename, "w+")
                self.ip = input("Please pass the ip:\n")
                self.port = int(input("Pass the port:\n"))
                msg = self.ip + " " + str(self.port)
                fo.write(msg)
            except OSError as e:
                self.log_exception("OS error: " + e)
                raise SystemExit
            finally:
                fo.close()

                self.log_info("Address parameters: " + self.ip + " " + str(self.port))
        except ValueError as e:
            self.log_error("OS error: " + e + "\nPlease review how config.cfg file looks like")
            f.close()
            raise SystemExit
        else:
            self.log_info("Address parameters: " + self.ip + " " + str(self.port))
            f.close()
        
        #setting commands codes
        try:
            f=open("command.dict", "r")
            for line in f:
                tmp1,tmp2 = line.split()
                self.command_dict[tmp2] = tmp1
        except KeyError as e:
            self.log_error("key is not in the map. Original message: " + e)
        except OSError as e:
            self.log_exception("OS error: " + e)
            raise SystemExit
        finally:
            f.close()

    def do_shell(self, line):
        """Run a shell command"""
        # TODO: add to help
        self.log_info("running shell command:" + line)
        output = os.popen(line).read()
        self.log_info(output)
        self.last_output = output

    # Commands
    # *operational:
    def do_stream_cont(self, args):
        """Continuous reading data from OBC"""
        # TODO: dodac do helpa
        self.streamDown()

    def do_downstream_on(self, args):
        """Start downstream"""

    def do_downstream_off(self, args):
        """Stop downstream"""

    def do_stopm(self, args):
        """Stop motors"""
        try:
            self.send(self.command_dict["sudo_stopm"])
        except KeyError:
            self.log_exception("Wrong key. Check dictionary")

    def do_go_idle(self, args):
        """Turn off the motors and data gathering"""
        try:
            self.send(self.command_dict["sudo_set_status"]+"0")
        except KeyError:
            self.log_exception("Wrong key. Check dictionary")

    def do_status(self, args):
        """Check experiment's status"""
        try:
            data = self.sendrec(self.command_dict["get_status"])
        except KeyError:
            self.log_exception("Wrong key. Check dictionary")
            return
        self.save_results(data)

    def do_go_scanning(self, args):
        """Turn the scanning mode on"""
        try:
            self.send(self.command_dict["sudo_set_status"] + "1")
        except KeyError:
            self.log_exception("Wrong key. Check dictionary")
            return
        self.streamDown()

    def do_send_nth(self, args):
        """Send every N-th set of measurements to Ground Station"""
        try:
            data = self.sendrec(self.command_dict["send_nth"] + str(args))
        except KeyError:
            self.log_exception("Wrong key. Check dictionary")
            return
        self.streamDown()
    
    def do_get_htp(self, args):
        """Get humidity, temperature and pressure data"""
        try:
            data = self.sendrec(self.command_dict["get_htp"])
        except KeyError:
            self.log_exception("Wrong key. Check dictionary")
            return
        self.save_results(data)

    def do_get_photo(self, args):
        """Get data from set of photodetectors"""
        try:
            data = self.sendrec(self.command_dict["get_photo"])
        except KeyError:
            self.log_exception("Wrong key. Check dictionary")
            return
        self.save_results(data)

    def do_get_speed(self, args):
        """Get actual motor's speed"""
        # TODO: brakuje komendy
        try:
            data = self.sendrec(self.command_dict["get_speed"])
        except KeyError:
            self.log_exception("Wrong key. Check dictionary")
            return
        self.save_results(data)

    def do_get_speed_fast(self, args):
        """Display last motors' speeds set by set-speed command"""
        try:
            self.log_info("speed motor1: {0}\nspeed motor2: {1}".format(self.speed1, self.speed2))
        except KeyError:
            self.log_exception("Wrong key. Check dictionary")

    def do_get_uc_temp(self, args):
        """Check the microcontroller's temperature"""
        try:
            data = self.sendrecv(self.command_dict["get_uc_temp"])
        except KeyError:
            self.log_exception("Wrong key. Check dictionary")
            return
        self.save_results(data)

    def do_go_manual(self, args):
        """Enable additional commands: set_speed, set_frequency, mknlog, save_htp"""
        try:
            self.send(self.command_dict["sudo_set_status"] + "2")
        except KeyError:
            self.log_exception("Wrong key. Check dictionary")

    def do_set_speed(self, args):
        #TODO: usunac speed2 po rozmowie z Mikolajem
        """set selected (arg1 [1-2]) motor's speed (arg2 [0-255])"""
        arg1,arg2 = args.split()
        arg1 = int(arg1)
        arg2 = int(arg2)
        if (arg1 == 1 or arg1 == 2) and (arg2 > 0 and arg2 < 256):
            if arg1 ==1:
                self.speed1 = arg2;
                self.log_info("speed of motor no 1 is set to {0}".format(arg2))
            elif arg1 == 2:
                self.speed2 = arg2;
                self.log_info("speed of motor no 2 is set to {0}".format(arg2))
        elif not (arg1 == 1 or arg1 == 2):
            self.log_warning("First argument must be 1 or 2! Enter 'help' for more info")
            return
        else:
            self.log_warning("Second argument must be from 0-255!")
            return
        try:
            self.send(self.command_dict["set_speed"] + self.speed1)
        except KeyError:
            self.log_exception("Wrong key. Check dictionary")

    def do_set_frequency(self, args):
        """set measurements' frequency according to arg value"""
        # TODO: brak komendy
        # TODO: check weather amount of parameters is right and if they are correct
        try:
            self.send(self.command_dict["set_frequency"] + args)
        except KeyError:
            self.log_exception("Wrong key. Check dictionary")

    def do_mknlog(self, args):
        """make new logfile on SD card"""
        try:
            self.send(self.command_dict["mknlog"])
        except KeyError:
            self.log_exception("Wrong key. Check dictionary")

    def do_save_htp(self, args):
        """Save humidity, temperature and pressure data on SD card"""
        # TODO: brak komendy
        try:
            self.send(self.command_dict["save_htp"])
        except KeyError:
            self.log_exception("Wrong key. Check dictionary")

    # *networking:
    def do_set_ip(self, args):
        """set destination's ip as arg and save it in configfile"""
        self.ip = args
        try:
            f=open(self.configfilename, "r+")
            line = self.ip + " " + str(self.port)
            f.seek(0)
            f.write(line)
            self.log_info("ip set to: " + self.ip)
        except ValueError as e:
            self.log_exception("OS error: " + e + "\nPlease review how config.cfg file looks like")
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
            self.log_info("port set to: " + self.port)
        except ValueError as e:
            self.log_exception("OS error: " + e + "\nPlease review how config.cfg file looks like")
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
            self.log_info("ip set to: " + self.ip)
            self.log_info("port set to: " + self.port)
        except ValueError as e:
            self.log_exception("OS error: " + e + "\nPlease review how config.cfg file looks like")
            raise SystemExit
        else:
            f.close()

    def do_show_address(self, args):
        """display current destination's ip and port from configfile"""
        try:
            self.log_info("Current address: " + self.ip + "/" + str(self.port))
        except KeyError:
            self.log_exception("Wrong key. Check dictionary")

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