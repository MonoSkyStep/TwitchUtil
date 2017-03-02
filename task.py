from utils import Enumeration



class Task(Enumeration):

    _types = 'PRIV_MSG WHISPER TIMEOUT BAN'

    def __init__(self, tasktype):
        global _types

        super().__init__(_types)

        self.type = tasktype
