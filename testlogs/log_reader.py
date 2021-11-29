r"""
    Read and format the logs to be transported or whatever.
"""

from datetime import datetime
from .log_writer import FILE_PATH, LOG_REGEX_FORMAT
from .log_generator import NUMBER_OF_INTERFACES
from time import sleep, time
import re

SLEEP_TIME = 4 # 4 seconds

CHECK_PATTERN = re.compile(LOG_REGEX_FORMAT)

METRIC_NAME = "rando"

# regex and strings based on specific log format to be able to parse it. this will be different based on log.
## see format_logs() method for how the below are used.
TIME_REGEX = re.compile("([0-9]{4})-([0-9]{2})-([0-9]{2}) ([0-9]{2}):([0-9]{2}):([0-9]{2}).([0-9]{3})")
MERIC_NAME_REGEX = re.compile("(?<=\[)\w+(?=\])")
LOG_SPLITTER = " : " # splits the log metadata from the actual value; the value comes right after this string in the whole log string

# line break option
LINE_BREAK = "\n"

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
    
    # get the raw logs; will come with 2 lines
    raw_logs = _read_method_bytes()

    # split lines
    lines = re.split("\n", raw_logs)

    # format each log and concatenate them
    metric_total = ""
    for line in lines:
        metric_total += format_logs(line)

    return metric_total

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
                continue
            else:
                log_string = decoded_string + log_string
            
            if line_break_count == NUMBER_OF_INTERFACES:
                log_string_final = log_string_final[1:] # due to op under check_result there is an extra \n at the begining which will be gotten rid of here
                break

            reverse_count = reverse_count - 1
    
    return log_string_final

def _check_log_pattern(log_to_check):
    r"""
        Helper method to be used with _read_method_bytes(). Will check obtained bytes
        to see if a log line has been obtained.
    """
    
    matchedObj = re.search(CHECK_PATTERN, log_to_check)
    if matchedObj:
        return matchedObj.group(0)
    
    return False



def format_logs(log:str):
    r"""
        Convert from raw logs to prometheus compatible metrics.
        Format:
        
        ```
        #TYPE <name> gauge
        <name> <val> <time>
        ```

        Time will have to be prometheus compatible.
    """

    # get the timestamp section of the log
    timestampstr = get_UTC_timestamp(log)

    # get metric name
    interface_name_match = re.search(MERIC_NAME_REGEX, log)
    if interface_name_match:
        interface_name = interface_name_match.group(0)
    
    # get value of metric
    value_start_index = log.index(LOG_SPLITTER) + len(LOG_SPLITTER)
    value = log[value_start_index:]

    # create formatted string:
    metric_string_total = ""
    metric_string = METRIC_NAME + "{" \
        + "interface=\"" +  interface_name + "\""\
        + "} " + value #\
        #+ " " + timestampstr
    metric_string_total += metric_string + LINE_BREAK

    return metric_string_total


def get_metric_typedef():
    metric_typedef = "# TYPE " + METRIC_NAME + " gauge"
    return metric_typedef

   


def get_UTC_timestamp(log:str):
    r"""
        Parse a log and return the utc int timestamp as a string.

        ---
        param(s):
        - log: a str formatted like the following example: 2021-11-27 18:18:30.006 [Dumb] : 51

        ---
        returns: an int as a str representing the timestamp from log (as utc); from the above example one would get: 1638055110
    """

    times = re.search(TIME_REGEX, log)
    if times:
        times_parts = times.groups()
        year = int(times_parts[0])
        month = int(times_parts[1])
        day = int(times_parts[2])
        hour = int(times_parts[3])
        minute = int(times_parts[4])
        second = int(times_parts[5])
        millisecond = int(times_parts[6])
    else: # if a bad timestamp is given(?)
        raise ValueError("Log doesn't have time or has bad time.")
    
    dtobj = datetime(year, month, day, hour, minute, second)
    timestamp_int = int(dtobj.timestamp())
    timestamp_str = str(timestamp_int)
    return timestamp_str



if __name__ == "__main__":
    read_logs()

