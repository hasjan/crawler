#!/usr/bin/env python
"""
This worker analyzes hosts similarly to how SSLyze does.
"""

__author__ = ["David Hoeyng", "Adrian Zapletal"]
__license__ = ""  # TODO ?
__version__ = "0.1"

import sys
from multiprocessing import Process, JoinableQueue
import settings
from queue_manager import QueueClient
from sslyze.plugins import PluginsFinder

try:
    from utils.ServersConnectivityTester import ServersConnectivityTester, InvalidTargetError
except ImportError as e:
    print str(e) + '\nERROR: Could not import nassl Python module. Did you clone SSLyze\'s repo ? \n' +\
    'Please download the right pre-compiled package as described in the README.\n'
    sys.exit()


class WorkerProcess(Process):
    """
    This class checks hosts from the host_queue with the settings specified in settings.py.
    """
    def __init__(self, host_queue, result_queue, available_commands):
        Process.__init__(self)

        self.host_queue = host_queue
        self.result_queue = result_queue
        self.available_commands = available_commands

    def run(self):
        # Plugin classes are unpickled by the multiprocessing module
        # without state info. Need to assign shared_settings here
        for plugin_class in self.available_commands.itervalues():
            plugin_class._shared_settings = settings.SHARED_SETTINGS

        while True:
            try:
                hostname = self.host_queue.get(timeout=settings.HOST_QUEUE_TIMEOUT)
            except:  # If a timeout happens, an exception will always be thrown, hence why we just break here
                break

            target = self._test_server(hostname)
            if target:
                result_dict = dict(target=target, result=[])

                for command in settings.COMMAND_LIST:
                    result = self._process_command(target, command)
                    result_dict["result"].append(result.get_raw_result())

            self.result_queue.put(result_dict)

    def _process_command(self, target, command):
            plugin_instance = self.available_commands[command]()
            try:  # Process the task
                result = plugin_instance.process_task(target, command, True)
            except Exception as e:  # Generate txt and xml results
                result = e  # TODO format exception
            return result

    def _test_server(self, hostname):
        try:
            target = ServersConnectivityTester._test_server(hostname, settings.SHARED_SETTINGS)
        except InvalidTargetError as e:
            self.result_queue.put(((hostname, None, None, None), None, e.get_error_txt()))
            return
        return target


def main():
    ##########################
    # PLUGINS INITIALIZATION #
    ##########################

    sslyze_plugins = PluginsFinder()
    available_plugins = sslyze_plugins.get_plugins()
    available_commands = sslyze_plugins.get_commands()

    ########################
    # QUEUE INITIALIZATION #
    ########################
    # TODO use queue from remote queue manager, this is just for testing purposes

    c = QueueClient()
    host_queue = c.host_queue()
    result_queue = c.result_queue()

    # host_queue = JoinableQueue()
    # result_queue = JoinableQueue()
    # host_queue.put("google.com")

    ##########################
    # PROCESS INITIALIZATION #
    ##########################

    process_list = []

    for _ in xrange(settings.NUMBER_PROCESSES):
        p = WorkerProcess(host_queue, result_queue, available_commands)
        p.start()
        process_list.append(p)

    # Wait for all processes to terminate
    for p in process_list:
        p.join()


if __name__ == "__main__":
    main()
