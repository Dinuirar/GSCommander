#!/usr/bin/env python
import cmd
import os
import socket
import logging
import obccom
from logmod import *
# TODO: check weather amount of parameters is right and if they are correct? how much work would it be?


class cmdSSG(cmd.Cmd):
    """This is a terminal for the LUSTRO BEXUS experiment. \nIt allows the operator to set all of the experiment's\nconfigureable parametres, like motor's speed and measurements\nfrequency."""
    # variables & mechanics of cmd
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

    def preloop(self):
        log_init()
        logging.info("Starting new session")

        # configure
        logging.info("Setting networking parameters...")
        try:
            f = open(self.configfilename, "r+")
            line = f.readline()
            ip_tmp, port_tmp = line.split()
            try:
                self.port = int(port_tmp)
                if not (self.port <= 65535 and self.port >= 0):
                    # TODO: should ask for input always if last input was wrong?
                    msg = 'port value in configure file outside of range.'
                    log_error(msg)
                    self.port = input()
                    f.seek(0)
                    f.write(ip_tmp + " " + self.port)
            except ValueError as e:
                log_info('Configure file error: ' + str(e))
                self.port = input("Pass correct value now:\n")
            try:
                socket.inet_aton(ip_tmp)
            except socket.error:
                log_error('Ip address error in configuration file.')
                self.ip = input("Pass correct value now:\n")
            else:
                self.ip = ip_tmp
        except OSError:  # no config file
            log_warning("file " + self.configfilename + " cannot be found. File will be created now.")
            try:
                fo = open(self.configfilename, "w+")
                self.ip = input("Please pass the ip:\n")
                self.port = int(input("Pass the port:\n"))
                msg = self.ip + " " + str(self.port)
                fo.write(msg)
            except OSError as e:
                log_exception("OS error: " + str(e))
                raise SystemExit
            finally:
                fo.close()

                log_info("Address parameters: " + self.ip + " " + str(self.port))
        except ValueError as e:
            log_error("OS error: " + str(e) + "\nPlease review how config.cfg file looks like")
            f.close()
            raise SystemExit
        else:
            log_info("Address parameters: " + self.ip + " " + str(self.port))
            f.close()

        # setting commands codes
        try:
            f = open("command.dict", "r")
            for line in f:
                tmp1, tmp2 = line.split()
                self.command_dict[tmp2] = tmp1
        except KeyError as e:
            log_error("key is not in the map. Original message: " + str(e))
        except OSError as e:
            log_exception("OS error: " + str(e))
            raise SystemExit
        finally:
            f.close()

    def do_shell(self, line):
        """Run a shell command"""
        # TODO: add to help
        log_info("running shell command:" + line)
        output = os.popen(line).read()
        log_info(output)
        self.last_output = output

    # Commands
    # *operational:
    def do_stream_cont(self, args):
        """Continuous reading data from OBC"""
        # TODO: add to help
        obccom.streamDown(self)

    def do_downstream_on(self, args):
        """Send command to start downstream and start downstream"""
        msg = "FFFFFF"
        obccom.send(self, msg)
        obccom.streamDown(self)

    def do_downstream_off(self, args):
        """Stop downstream"""
        msg = "FFFFFF"
        obccom.send(self, msg)

    def do_stopm(self, args):
        """Stop motors"""
        try:
            obccom.send(self, self.command_dict["sudo_stopm"])
        except KeyError:
            log_exception("Wrong key. Check dictionary")

    def do_go_idle(self, args):
        """Turn off the motors and data gathering"""
        try:
            obccom.send(self, self.command_dict["sudo_set_status"] + "0")
        except KeyError:
            log_exception("Wrong key. Check dictionary")

    def do_status(self, args):
        """Check experiment's status"""
        try:
            data = obccom.sendrec(self, self.command_dict["get_status"])
        except KeyError:
            log_exception("Wrong key. Check dictionary")
            return
        else:
            obccom.save_results(self, data)

    def do_go_scanning(self, args):
        """Turn the scanning mode on"""
        try:
            obccom.send(self, self.command_dict["sudo_set_status"] + "1")
        except KeyError:
            log_exception("Wrong key. Check dictionary")
            return
        else:
            obccom.streamDown(self)

    def do_send_nth(self, args):
        """Send every N-th set of measurements to Ground Station"""
        try:
            data = obccom.sendrec(self, self.command_dict["send_nth"] + str(args))
        except KeyError:
            log_exception("Wrong key. Check dictionary")
            return
        else:
            obccom.streamDown(self)

    def do_get_htp(self, args):
        """Get humidity, temperature and pressure data"""
        try:
            data = obccom.sendrec(self, self.command_dict["get_htp"])
        except KeyError:
            log_exception("Wrong key. Check dictionary")
            return
        else:
            obccom.save_results(self, data)

    def do_get_photo(self, args):
        """Get data from set of photodetectors"""
        try:
            data = obccom.sendrec(self, self.command_dict["get_photo"])
        except KeyError:
            log_exception("Wrong key. Check dictionary")
            return
        else:
            obccom.save_results(self, data)

    def do_get_speed(self, args):
        """Get actual motor's speed"""
        # TODO: no command in dict
        try:
            data = obccom.sendrec(self, self.command_dict["get_speed"])
        except KeyError:
            log_exception("Wrong key. Check dictionary")
            return
        else:
            obccom.save_results(self, data)

    def do_get_speed_fast(self, args):
        """Display last motors' speeds set by set-speed command"""
        try:
            log_info("speed motor1: {0}\nspeed motor2: {1}".format(self.speed1, self.speed2))
        except KeyError:
            log_exception("Wrong key. Check dictionary")

    def do_get_uc_temp(self, args):
        """Check the microcontroller's temperature"""
        try:
            data = obccom.sendrec(self, self.command_dict["get_uc_temp"])
        except KeyError:
            log_exception("Wrong key. Check dictionary")
            return
        else:
            obccom.save_results(self, data)

    def do_go_manual(self, args):
        """Enable additional commands: set_speed, set_frequency, mknlog, save_htp"""
        try:
            obccom.send(self, self.command_dict["sudo_set_status"] + "2")
        except KeyError:
            log_exception("Wrong key. Check dictionary")

    def do_set_speed(self, args):
        # TODO: usunac speed2?
        """set selected (arg1 [1-2]) motor's speed (arg2 [0-255])"""
        arg1, arg2 = args.split()
        arg1 = int(arg1)
        arg2 = int(arg2)
        if (arg1 == 1 or arg1 == 2) and (arg2 > 0 and arg2 < 256):
            if arg1 == 1:
                self.speed1 = arg2
                log_info("speed of motor no 1 is set to {0}".format(arg2))
            elif arg1 == 2:
                self.speed2 = arg2
                log_info("speed of motor no 2 is set to {0}".format(arg2))
        elif not (arg1 == 1 or arg1 == 2):
            log_warning("First argument must be 1 or 2! Enter 'help' for more info")
            return
        else:
            log_warning("Second argument must be from 0-255!")
            return
        try:
            obccom.send(self, self.command_dict["set_speed"] + self.speed1)
        except KeyError:
            log_exception("Wrong key. Check dictionary")

    def do_set_frequency(self, args):
        """set measurements' frequency according to arg value"""
        # TODO: no command in dict
        try:
            obccom.send(self, self.command_dict["set_frequency"] + args)
        except KeyError:
            log_exception("Wrong key. Check dictionary")

    def do_mknlog(self, args):
        """make new logfile on SD card"""
        try:
            obccom.send(self, self.command_dict["mknlog"])
        except KeyError:
            log_exception("Wrong key. Check dictionary")

    def do_save_htp(self, args):
        """Save humidity, temperature and pressure data on SD card"""
        # TODO: no command in dict
        try:
            obccom.send(self, self.command_dict["save_htp"])
        except KeyError:
            log_exception("Wrong key. Check dictionary")

    # *networking:
    def do_set_ip(self, args):
        """set destination's ip as arg and save it in configfile"""
        self.ip = args
        try:
            f = open(self.configfilename, "r+")
            line = self.ip + " " + str(self.port)
            f.seek(0)
            f.write(line)
            log_info("ip set to: " + self.ip)
        except ValueError as e:
            log_exception("OS error: " + str(e) + "\nPlease review how config.cfg file looks like")
            raise SystemExit
        else:
            f.close()

    def do_set_port(self, args):
        """set destination's targeted port as arg and save it in """
        self.port = args
        try:
            f = open(self.configfilename, "r+")
            line = self.ip + " " + str(self.port)
            f.seek(0)
            f.write(line)
            log_info("port set to: " + self.port)
        except ValueError as e:
            log_exception("OS error: " + str(e) + "\nPlease review how config.cfg file looks like")
            raise SystemExit
        else:
            f.close()

    def do_set_address(self, args):
        """set destination's ip as arg1 and port as arg2 and save them in configile"""
        self.ip, self.port = args.split()
        try:
            f = open(self.configfilename, "r+")
            line = self.ip + " " + str(self.port)
            f.seek(0)
            f.write(line)
            log_info("ip set to: " + self.ip)
            log_info("port set to: " + self.port)
        except ValueError as e:
            log_exception("OS error: " + str(e) + "\nPlease review how config.cfg file looks like")
            raise SystemExit
        else:
            f.close()

    def do_show_address(self, args):
        """display current destination's ip and port from configfile"""
        try:
            log_info("Current address: " + self.ip + "/" + str(self.port))
        except KeyError:
            log_exception("Wrong key. Check dictionary")

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
        print(f.read())
        f.close()

    def do_exit(self, args):
        """close the program"""
        logging.info("Exiting")
        raise SystemExit

