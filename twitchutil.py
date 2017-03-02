__author__ = 'monoskystep'

from threading import Thread
from utils import switch
import requests
import socket
import debug



'''
the following special forms using leading or trailing underscores are recognized (these can generally be combined with any case convention):

_single_leading_underscore: weak "internal use" indicator. E.g. "from M import *" does not import objects whose name starts with an underscore.
single_trailing_underscore_: used by convention to avoid conflicts with Python keyword, e.g.

Tkinter.Toplevel(master, class_='ClassName')
__double_leading_underscore: when naming a class attribute, invokes name mangling (inside class FooBar, __boo becomes _FooBar__boo; see below).
__double_leading_and_trailing_underscore__: "magic" objects or attributes that live in user-controlled namespaces. E.g. __init__, __import__ or __file__. Never invent such names; only use them as documented.
'''







class TwitchIrcConnection:

    MEMBERSHIP_CAP = 1
    COMMANDS_CAP   = 2
    TAGS_CAP       = 3
    ALL_CAP        = 4


    class Event:

        def __init__(self, raw_text):
            text = str(raw_text)

            self.raw_msg    = text
            self.tag_data   = None
            self.type       = None
            self.chan       = None
            self.usr        = None
            self.msg        = None
            self.cmd        = None
            self.args       = None
            self.op         = None
            #if it's a ping then
            if 'PING' == text[0:4]:
                self.type = 'ping'
                return

            tag_data = {}
            message_data = None

            if (text.find(';') is not -1) and text.find(';') < text.find(':'):
                tmp_data, message_data = text.split(':', 1)
                tmp_data = tmp_data.split(';')

                for tmp in tmp_data:
                    str_split = tmp.split('=')
                    tag_data[str_split[0]] = str_split[1]
            else:
                message_data = text.split(':', 1)
                message_data.pop(0)
                message_data = message_data[0]

            if tag_data != {}:
                self.tag_data = tag_data

            meta_data = None
            message = None

            if message_data.find(':') is -1:
                meta_data = message_data.split(' ')
            else:
                tmp_data = message_data.split(':', 1)
                meta_data = tmp_data[0].split(' ')
                message = tmp_data[1]


            self.type = meta_data[1].lower()

            for case in switch(self.type.lower()):

                if case('join'):
                    self.usr = meta_data[0].split('!')[0]
                    self.chan = meta_data[2].replace('#', '')

                elif case('part'):
                    self.usr = meta_data[0].split('!')[0]
                    self.chan = meta_data[2].replace('#', '')

                elif case('privmsg'):
                    self.usr = meta_data[0].split('!')[0]
                    self.chan = meta_data[2].replace('#', '')
                    self.msg = message

                elif case('userstate'):
                    pass

                elif case('roomstate'):
                    pass

                elif case('cap'):
                    pass

                elif case('mode'):
                    self.chan = meta_data[2].replace('#', '')
                    self.op   = meta_data[3]
                    self.usr  = meta_data[4]
                    pass

                elif case('notice'):
                    self.chan = meta_data[2].replace('#', '')
                    pass

                elif case('376'):
                    self.type = 'connection'

                elif case('421'):
                    self.type = 'invalid'
                    pass
















    def __init__(self, user, oath, *caps):
        self.user = user
        self.oath = oath
        self.host = 'irc.twitch.tv'
        self.port = 6667
        self.cap_requests = []

        #takes all extra args and puts them into caps
        for arg in caps:
            self.cap_requests.append(arg)

        #tracking what channels this connection is in, and the people in it
        self.joined_channels = []
        self.joined_channel_users = []
        self.s_thread = Thread(target=self.run)
        self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        #all the message type handlers
        self.on_ping            = None

        self.on_connection      = None
        self.on_invalid_command = None

        self.on_join_chan       = None
        self.on_part_chan       = None
        self.on_privmsg_msg     = None

        self.on_mode            = None
        self.on_userstate       = None
        self.on_roomstate       = None
        self.on_mod             = None
        self.on_notice          = None
        self.on_hosttarget      = None
        self.on_clearchat       = None





    def init_connection(self):

        self.connection.settimeout(10)
        self.connection.connect((self.host, self.port))

        self.connection.sendall(bytes('PASS {}\r\n'.format(self.oath), 'UTF-8'))
        self.connection.sendall(bytes('NICK {}\r\n'.format(self.user), 'UTF-8'))



    def run(self):

        self.send_cap_request()
        self.connection.settimeout(2)

        while True:
            messages = self.read()

            for tmp_msg in messages:
                debug.Debug.log(tmp_msg, received=True)
                message = TwitchIrcConnection.Event(tmp_msg)

                for case in switch(message.type.lower()):

                    if case('connection'):
                        if self.on_connection is not None:
                            self.on_connection(message)

                    elif case('ping'):
                        if self.on_ping is not None:
                            self.on_ping(message)

                    elif case('privmsg'):
                        if self.privmsg is not None:
                            self.on_ping(message)

                    elif case('join'):
                        if self.on_join_chan is not None:
                            self.on_join_chan(message)

                    elif case('part'):
                        if self.on_part_chan is not None:
                            self.on_part_chan(message)

                    elif case('mode'):
                        if message.op[0] == '+':
                            if self.on_usr_mod is not None:
                                self.on_usr_mod(message)


                        if message.op[0] == '-':
                            if self.on_usr_demod is not None:
                                self.on_usr_demod(message)
                    else:
                        print('UNHANDLED EVENT:' + message.type)



                        # privmsg
                        # servmsg
                        # on_join_chan
                        # on_part_chan
                        # on_usr_part_chan
                        # on_usr_join_chan
                        # on_usr_mod
                        # on_usr_demod







    def read(self, buffer_=1024):
        messages = []

        try:

            while True:
                data = self.connection.recv(buffer_).decode('utf-8').split('\r\n')

                for tmp_data in data:
                    if len(tmp_data) > 1:
                        messages.append(tmp_data)
                    else:
                        pass

        except socket.timeout:
            return messages




    '''
    handle setter, just here to create sections
    '''
    def set_handler(self, handler, function):

        for case in switch(handler.lower()):
            if case('PRIVMSG'):
                self.on_chan_msg = function

            elif case('JOIN'):
                self.on_join_chan = function

            elif case('LEAVE'):
                self.on_part_chan = function

            elif case('USRJOIN'):
                self.on_usr_join_chan = function

            elif case('USRPART'):
                self.on_usr_part_chan = function

            elif case('USRMOD'):
                self.on_usr_mod = function

            elif case('USRDEMOD'):
                self.on_usr_demod = function









    '''
    section of raw messages
    '''
    def _send_raw(self, data):
        debug.Debug.log(data)
        self.connection.sendall(bytes(data + '\r\n', 'utf-8'))



    def send_cap_request(self):

        for cap in self.cap_requests:
            if cap is TwitchIrcConnection.ALL_CAP:
                self._send_raw('CAP REQ :twitch.tv/membership')
                self._send_raw('CAP REQ :twitch.tv/commands')
                self._send_raw('CAP REQ :twitch.tv/tags')
                return

            elif cap is TwitchIrcConnection.MEMBERSHIP_CAP:
                self._send_raw('CAP REQ :twitch.tv/membership')

            elif cap is TwitchIrcConnection.COMMANDS_CAP:
                self._send_raw('CAP REQ :twitch.tv/commands')

            elif cap is TwitchIrcConnection.TAGS_CAP:
                self._send_raw('CAP REQ :twitch.tv/tags')



    def join_chan(self, channel):
        self._send_raw('JOIN #{}'.format(channel))

    def leave_chan(self, channel):
        self._send_raw('PART #{}'.format(channel))

    def send_chan_message(self, channel, message):
        self._send_raw('PRIVMSG #{} :{}'.format(channel, message))



    def start(self):
        self.s_thread.start()













class TwitchWhisperConnection(TwitchIrcConnection):#i think this was finished


    def __init__(self, user, oath, host, port, **caps):
        super().__init__(user, oath, caps)
        self.host = host
        self.port = port

    def send_whisper(self, user, message):
        self._send_raw('PRIVMSG #jtv :/w {} {}'.format(user, message))


# class TwitchGroupServerConnection(TwitchIrcConnection):#unfinished

#         def __init__(self, user, oath, host, port, **caps):
#             super().__init__(user, oath, caps)
#             self.host = host
#             self.port = port