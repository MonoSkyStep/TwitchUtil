from time import sleep
import twitchutil

class Bot:

    def __init__(self):
        self.connections=[]


    def getConnections(self):
        return self.connections


    def start(self):
        while True:
            self.update()
            sleep(0.1)

    def update(self):
        pass



    #event handlers
    def onConnection(self):
        pass

    def onServerMessage(self, event):
        pass

    def onChanMessage(self, event):
        pass





    def onPing(self, message):
        print('sending message ->' + message.get_msg().replace('PING','PONG'))
        self.IRC.send_message(message.get_msg().replace('PING','PONG'))

# self.on_connection      = None
# self.on_privmsg         = None
# self.on_servmsg         = None
# self.on_join_chan       = None
# self.on_part_chan       = None
# self.on_usr_part_chan   = None
# self.on_usr_join_chan   = None
# self.on_usr_mod         = None
# self.on_usr_demod       = None