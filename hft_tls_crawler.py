"""
This module starts all required worker processes in the correct order.
"""

import os
import sys
import signal
import time
import subprocess
from threading import Thread
from Queue import Queue

#: the path to your python executable
PYTHON_PATH = ""

#: all modules in this list will be started in separate process
MODULE_LIST = ["queue_manager.py", "input_worker.py", "sslyze_worker.py", "result_worker.py"]

#: the output of the modules in this list will be logged to console or to file
LOG_MODULES = MODULE_LIST

#: holds the running processes
RUNNING_PROCESSES = []


def enqueue_out(stream, module, q):
    """
    iterate over each line in stdout and put line to queue.

    :param stream: the stream of stdout
    :param module: the name of the module to keep track of stdout
    :param q: the queue to put each line
    :return:
    """
    for line in iter(stream.readline, b''):
        q.put((module, "stdout", line.rstrip(b'\r\n')))


def enqueue_err(stream, module, q):
    """
    iterate over each line in stderr and put line to queue.

    :param stream: the stream of stderr
    :param module: the name of the module to keep track of stderr
    :param q: the queue to put each line
    :return:
    """
    for line in iter(stream.readline, b''):
        q.put((module, "stderr", line.rstrip(b'\r\n')))


def sigint_handler(signum, frame):
    """
    handles keyboard interrupt
    :param signum:
    :param frame:
    :return:
    """
    print("### TERMINATION ###")
    for p, module in RUNNING_PROCESSES:
        print("terminating %s with PID %s)" % (module, p.pid))
        p.terminate()
        p.wait()
    sys.exit()


def main():

    signal.signal(signal.SIGINT, sigint_handler)

    q = Queue()

    print("Starting modules ...")

    for module in MODULE_LIST:

        p = subprocess.Popen([os.path.join(PYTHON_PATH, "python"), "-u", module], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        RUNNING_PROCESSES.append([p, module])

        print("%s is running with PID %s" % (module, p.pid))

        t = Thread(target=enqueue_out, args=(p.stdout, module, q))
        t.daemon = True  # thread dies with the program
        t.start()

        t = Thread(target=enqueue_err, args=(p.stderr, module, q))
        t.daemon = True  # thread dies with the program
        t.start()

    print("")

    while True:
        line = q.get()

        if line[0] in LOG_MODULES:

            if line[1] == "stderr":
                color = 95

            elif line[0] == "queue_manager.py":
                color = 91

            elif line[0] == "input_worker.py":
                color = 94

            elif line[0] == "sslyze_worker.py":
                color = 92

            elif line[0] == "result_worker.py":
                color = 93

            msg = "\033[%sm%s [%s]:    %s\033[0m\n" % (color, time.time(), line[0], line[2])
            sys.stdout.write(msg)


if __name__ == "__main__":
    main()
