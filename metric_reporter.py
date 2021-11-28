import multiprocessing
from multiprocessing import Manager
import queue
from flask import Flask
from multiprocessing import queues
from concurrent.futures.process import ProcessPoolExecutor
from concurrent.futures.thread import ThreadPoolExecutor
import threading
from typing import Tuple
import time
from testlogs.log_suite_runner import read_loop, write_loop, Log


def flask_app() -> Flask:

    manager = Manager()

    # queues to control and share data
    control_queue = manager.Queue(1)
    read_queue = manager.Queue(10)

    # set up read_queue
    log_obj = Log()
    #read_queue.put(log_obj)

    # set up process pool executor
    ppe = ProcessPoolExecutor(max_workers=2)

    # submit the methods to ppe and get them started
    # writer
    ppe.submit(write_loop, control_queue)
    # reader
    ppe.submit(read_loop, control_queue, read_queue)

    # initialize flask application
    metric_app = Flask(__name__)

    # route to gather metrics
    @metric_app.route('/metrics', methods=['GET'])
    def get_metrics():
        r"""
            Provide metrics to prometheus.
        """
        
        r"""
        # get metrics or return prev 
        try:
            inner_log_obj:Log = read_queue.get_nowait()
            tobereturned = inner_log_obj.get_metrics()
            return tobereturned
        except queue.Empty as e:
            return ""
        """

        try:
            return read_queue.get_nowait()
        except queue.Empty:
            return "queue empty (?)"
    

    # return application
    return metric_app

