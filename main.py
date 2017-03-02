from twitchutil import TwitchIrcConnection
from debug import Debug
from bot import Bot
import setup

class SimpleBot(Bot):

    def __init__(self):
        super().__init__()


        username = 'languagebot'

        self.connection = TwitchIrcConnection(
            username,
            setup.get_user_oath(username),
            TwitchIrcConnection.COMMANDS_CAP, TwitchIrcConnection.MEMBERSHIP_CAP
        )
        self.connection.init_connection()
        self.connection.start()
        self.connection.join_chan('monoskystep')
        self.connection.send_chan_message('monoskystep', 'hiya')



    def onConnection(self):
        print('got connection')
        # self.connection.init_connection()
        # self.connection.start()
        # self.connection.join_chan('monoskystep')
        # self.connection.send_chan_message('monoskystep', 'hiya')






if __name__ == '__main__':
    setup.__init__()
    Debug.__init__(verbose=True)
    setup.load_accounts()
    bot = SimpleBot()
