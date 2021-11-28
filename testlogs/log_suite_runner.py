from multiprocessing.queues import Queue
import threading
from concurrent.futures import ThreadPoolExecutor
import time
import os
from .log_reader import read_logs, get_logs
from .log_writer import write_logs

WRITE_SLEEP_TIME = 0
READ_SLEEP_TIME = 0

class Log:
    def __init__(self) -> None:
        self.read_log = ""
    
    def update_log(self, new_log:str):
        self.read_log += new_log
    
    def get_metrics(self):
        tobereturned = self.read_log
        self.read_log = ""
        return tobereturned


def read_loop(control_queue:Queue, shared_obj:Queue):
    r"""
        Continuously reads from file and returns the content
    """
    while control_queue.qsize() == 0:
        #print(os.getpid())
        shared_obj.put(get_logs())
        time.sleep(READ_SLEEP_TIME)


def write_loop(control_queue:Queue):
    r"""
        Continusouly write to file.
    """
    while control_queue.qsize() == 0:
        #print(os.getpid())
        write_logs()
        time.sleep(WRITE_SLEEP_TIME)


    
