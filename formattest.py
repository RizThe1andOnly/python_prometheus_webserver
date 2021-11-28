from testlogs.log_reader import format_logs
import datetime

if __name__ == "__main__":
    dummyLog = "2021-11-27 18:18:30.006 [Dumb] : 51"
    print(format_logs(dummyLog))