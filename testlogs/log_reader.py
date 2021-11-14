r"""
    Read and format the logs to be transported or whatever.
"""

from log_writer import FILE_PATH, LOG_REGEX_FORMAT
from log_generator import NUMBER_OF_INTERFACES
from time import sleep
import re

SLEEP_TIME = 4 # 4 seconds

CHECK_PATTERN = re.compile(LOG_REGEX_FORMAT)

def read_logs():
    r"""
        Read set of logs and format them. Read will be done every 4 seconds.

        Will skip formatting for now.
        @TODO: Do formatting -> will eventually wanna do prometheus integration
    """

    while 1:
        sleep(SLEEP_TIME)
        retrieved_logs = _read_method_bytes()
        print(retrieved_logs)


def get_logs():
    r"""
        Retrieves a single set of logs and returns them.
    """
    return _read_method_bytes()

def _read_end_of_file():
    r"""
        Utilize the file.seek() method to to go the end of file and read the last
        two lines of the log files.
    """

    with open(FILE_PATH, "r") as readFile:
        # set the position to the 2nd to las line of the file
        readFile.seek(0, 2) # 2 lines up from the end of the file
        readFile.seek(-2,1)

        # read the last couple of lines (based on number of interfaces)
        # will append the lines to single string with '\n' as separator
        retrieved_log = ""
        for i in range(NUMBER_OF_INTERFACES):
            retrieved_log += readFile.readline() + "\n"
    
    return retrieved_log


def _read_method_bytes():
    r"""
        Will read the last two lines of logs. The read will first ahve the
        logs be converted to bytes. Will start at end and go up from there,
        seeking out NUMBER_OF_INTERFACES '\n' 's.
    """

    log_string = ""
    log_string_final = ""

    with open(FILE_PATH, "rb+") as r_file:
        
        reverse_count = -1
        line_break_count = 0
        while True:
            r_file.seek(reverse_count, 2) # go backward from end of the file
            decoded_string = (r_file.read(1)).decode("utf-8")
            
            if decoded_string == "\n":
                reverse_count = reverse_count - 1
                continue

            check_result = _check_log_pattern(log_string)
            if check_result:
                log_string_final = "\n" + check_result + log_string_final
                log_string = ""
                line_break_count = line_break_count + 1
            else:
                log_string = decoded_string + log_string
            
            if line_break_count == NUMBER_OF_INTERFACES:
                break

            reverse_count = reverse_count - 1
    
    return log_string_final

def _check_log_pattern(log_to_check):
    r"""
        Helper method to be used with _read_method_butes(). Will check obtained bytes
        to see if a log line has been obtained.
    """
    
    matchedObj = re.search(CHECK_PATTERN, log_to_check)
    if matchedObj:
        return matchedObj.group(0)
    
    return False


if __name__ == "__main__":
    read_logs()

