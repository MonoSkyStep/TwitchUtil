from utils import switch


class Debug:

    verbose = True

    INFO = 0x1#this is some stupid inconsitency errors old me
    ERROR = 0x2


    @staticmethod
    def __init__(verbose=True, log_file_='log.txt'):
        global log_file
        Debug.verbose = verbose
        log_file = log_file_


    @staticmethod
    def log(message, type_=INFO, received=False):
        global log_file
        with open(log_file, 'a') as tmpfile:
            tmpfile.write('[{}] '.format(Debug.getType(type_)) + ('<' if received else '>') + message + '\n')
        if Debug.verbose:
            print('[{}] '.format(Debug.getType(type_)) + ('<' if received else '>') + message)


    @staticmethod
    def getType(data):
        for case in switch(data):
            if case(Debug.INFO):
                return 'INFO'
            elif case(Debug.ERROR):
                return 'ERROR'