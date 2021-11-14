r"""
    Write random log data to a file, making sure to lock it while writing.

    Log format:

    YYYY-MM-DD HH:MM:SS.MS [INTERFACE] : <Random-Number>

    @TODO: Write the random generation code
    @TODO: Do it so that upon getting Ctrl-C it will erase the file it writes to.
"""

from log_generator import generate_log, NUMBER_OF_INTERFACES
from time import sleep


SLEEP_TIME = 3 # 3 seconds inbetween updates to file
FILE_PATH = "./dummy.txt"
LOG_REGEX_FORMAT = "[0-9]{4}-[0-9]{2}-[0-9]{2} [0-9]{2}:[0-9]{2}:[0-9]{2}.[0-9]{3} \[\w+\] : [0-9]{2}"


def update_logs():
    r"""
        Will create the thread that runs the _write_logs() method.
    """

    try:
        while True:
            sleep(SLEEP_TIME)
            _write_logs()
    except KeyboardInterrupt:
        clear_file()
        #print("Ended Program Execution")


def clear_file():
    r"""
        Clears the log file upon the end of program execution.
        Here "end of program execution" means a KeyboardInterrupt
        exception which means a Ctrl+C button press in the terminal
        running this program.

        @TODO: come up with better way to clear file or just outright delete it
    """

    with open(FILE_PATH, "w") as opened_file:
        opened_file.write("")


def _write_logs():
    r"""
        Writes logs to a file continuously, every 3 seconds or so.
    """
    
    #open file and wrie to it; will use the default open() setting for now
    with open(FILE_PATH, "a") as opened_file:
        for i in range(NUMBER_OF_INTERFACES):
            opened_file.write(generate_log())
            opened_file.write("\n")


if __name__ == "__main__":
    update_logs()