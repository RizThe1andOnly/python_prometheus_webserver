r"""
    Create logs to be written. 

    The format is as follows:
    
    YYYY-MM-DD HH:MM:SS.MS [INTERFACE] : <Random-Number>
"""

import random
from datetime import datetime


INTERFACES = ["Dumb","Dumber"]
NUMBER_OF_INTERFACES = 2

# global / cached variables:
interface_index = 0



def generate_log():
    r"""
        Creates a random log to write into the file
    """
    timestamp = _generate_log_date()
    interface = _get_interface()
    logval = _generate_random_int()

    return timestamp + ' [' + str(interface) + '] : ' + str(logval)

def _generate_log_date():
    r"""
        Create and format a date for the log:
    """
    return datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]

def _get_interface():
    r"""
        Picks one of the limited number of interfaces and returns it. If there are
        two interfaces then 1st will be returned and then 2nd and then 1st again,
        so on and so forth.
    """

    global interface_index

    currentIndex = interface_index
    interface_index = (interface_index + 1) % 2

    return INTERFACES[currentIndex]

def _generate_random_int():
    return random.randint(0, 100)


if __name__ == "__main__":
    print("not meant to be used on its own")

