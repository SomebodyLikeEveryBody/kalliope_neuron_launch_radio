import logging
import subprocess
import os
import sys
import psutil
import threading
from time import sleep
from kalliope.core.Utils import Utils
from kalliope.core.NeuronModule import NeuronModule, InvalidParameterException

logging.basicConfig()
logger = logging.getLogger("kalliope")

pid_file_path = "pid.txt"

class Launch_radio(NeuronModule):
    """
    Launch radio neuron
	Play the stream from an url (Radio Néo url for example: http://stream.radioneo.org:8000/;stream/1)
	Play a sound passed as arg radio_url in the synapse
    """
    def __init__(self, **kwargs):
        super(Launch_radio, self).__init__(**kwargs)

        self.state = kwargs.get('state', None)
        self.radio_url = kwargs.get('radio_url', None)
        self.radio_name = kwargs.get('radio_name', None)
        self.mplayer_path = kwargs.get('mplayer_path', "/usr/bin/mplayer")
        self.auto_stop_minutes = kwargs.get('auto_stop_minutes', None)

        # this is the target AmbientSound object if the user gave a sound_name to play.
        # this object will be loaded by the _is_parameters_ok function durring the check if the sound exist
        self.target_ambient_sound = None

        # message dict that will be passed to the neuron template
        self.message = dict()

        # check if sent parameters are in good state
        if self._is_parameters_ok():
            if self.state == "off":
                self.stop_last_process()
                self.clean_pid_file()
            else:
                # we stop the last process if exist
                self.stop_last_process()

                # then we can start a new process
                self.start_new_process(self.radio_url)

                # give the current file name played to the neuron template
                self.message["radio_url"] = self.radio_url
                self.message["radio_name"] = self.radio_name

                # run auto stop thread
                if self.auto_stop_minutes:
                    thread_auto_stop = threading.Thread(target=self.wait_before_stop)
                    thread_auto_stop.start()

            # give the message dict to the neuron template
            self.say(self.message)

    def is_playable_url(radio_url):
        """
        Checks if the url is playable in mplayer.
        Not done yet.
        return: True if playable, False if it isn't
        """
        return True


    def wait_before_stop(self):
        logger.debug("[Launch_radio] Wait %s minutes before checking if the thread is alive" % self.auto_stop_minutes)
        Utils.print_info("[Launch_radio] Wait %s minutes before stopping the ambient sound" % self.auto_stop_minutes)
        sleep(self.auto_stop_minutes*60)  # *60 to convert received minutes into seconds
        logger.debug("[Launch_radio] Time is over, Stop player")
        Utils.print_info("[Launch_radio] Time is over, stopping the ambient sound")
        self.stop_last_process()

    def _is_parameters_ok(self):
        """
        Check that all given parameter are valid
        :return: True if all given parameter are ok
        """

        if self.state not in ["on", "off"]:
            raise InvalidParameterException("[Launch_radio] State must be 'on' or 'off'")

        if self.state == "ok":
            if self.radio_url is None:
                raise InvalidParameterException("[Launch_radio] You have to specify a radio_url parameter")
            if self.is_playable_url(self.radio_url) is not True:
                raise InvalidParameterException("[Launch_radio] The radio_url parameter you specified is not a valid playable url")
            if self.radio_name is None:
                raise InvalidParameterException("[Launch_radio] You have to specify a radio_name parameter")

        # if wait auto_stop_minutes is set, must be an integer or string convertible to integer
        if self.auto_stop_minutes is not None:
            if not isinstance(self.auto_stop_minutes, int):
                try:
                    self.auto_stop_minutes = int(self.auto_stop_minutes)
                except ValueError:
                    raise InvalidParameterException("[Launch_radio] auto_stop_minutes must be an integer")
            # check auto_stop_minutes is positive
            if self.auto_stop_minutes < 1:
                raise InvalidParameterException("[Launch_radio] auto_stop_minutes must be set at least to 1 minute")
        return True

    @staticmethod
    def store_pid(pid):
        """
        Store a PID number into a file
        :param pid: pid number to save
        :return:
        """

        content = str(pid)
        absolute_pid_file_path = os.path.dirname(os.path.abspath( __file__ )) + os.sep + pid_file_path
        try:
            with open(absolute_pid_file_path, "wb") as file_open:
                if sys.version_info[0] == 2:
                    file_open.write(content)
                else:
                    file_open.write(content.encode())
                file_open.close()

        except IOError as e:
            logger.error("[Launch_radio] I/O error(%s): %s", e.errno, e.strerror)
            return False

    @classmethod
    def get_scriptdir_absolute_path(cls):
        return os.path.dirname(os.path.abspath( __file__ ))

    @staticmethod
    def load_pid():
        """
        Load a PID number from the pid.txt file
        :return:
        """
        absolute_pid_file_path = Launch_radio.get_scriptdir_absolute_path() + os.sep + pid_file_path

        if os.path.isfile(absolute_pid_file_path):
            try:
                with open(absolute_pid_file_path, "r") as file_open:
                    pid_str = file_open.readline()
                    if pid_str:
                        return int(pid_str)

            except IOError as e:
                logger.debug("[Launch_radio] I/O error(%s): %s", e.errno, e.strerror)
                return False
        return False

    def stop_last_process(self):
        """
        stop the last mplayer process launched by this neuron
        :return:
        """
        pid = self.load_pid()

        if pid is not None:
            logger.debug("[Launch_radio] loaded pid: %s" % pid)
            try:
                p = psutil.Process(pid)
                p.kill()
                logger.debug("[Launch_radio] mplayer process with pid %s killed" % pid)
            except psutil.NoSuchProcess:
                logger.debug("[Launch_radio] the process PID %s does not exist" % pid)
        else:
            logger.debug("[Launch_radio] pid is null. Process already stopped")

    def start_new_process(self, radio_url):
        """
        Start mplayer process with the given radio_url
        :param radio_url:
        :type radio_url: str
        :return:
        """
        mplayer_exec_path = [self.mplayer_path]
        mplayer_options = ['-slave', '-quiet', '-loop', '0', '-af', 'volume=-15']
        mplayer_command = list()
        mplayer_command.extend(mplayer_exec_path)
        mplayer_command.extend(mplayer_options)

        mplayer_command.append(radio_url)
        logger.debug("[Launch_radio] Mplayer cmd: %s" % str(mplayer_command))

        # run mplayer in background inside a new process
        fnull = open(os.devnull, 'w')
        pid = subprocess.Popen(mplayer_command, stdout=fnull, stderr=fnull).pid

        # store the pid in a file to be killed later
        self.store_pid(pid)

        logger.debug("[Launch_radio] Mplayer started, pid: %s" % pid)

    @staticmethod
    def clean_pid_file():
        """
        Clean up all data stored in the pid.txt file
        """

        absolute_pid_file_path = Launch_radio.get_scriptdir_absolute_path() + os.sep + pid_file_path
        try:
            with open(absolute_pid_file_path, "w") as file_open:
                file_open.close()
                logger.debug("[Launch_radio] pid file cleaned")

        except IOError as e:
            logger.error("I/O error(%s): %s", e.errno, e.strerror)
            return False
