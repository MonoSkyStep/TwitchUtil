from simplecrypt import encrypt, decrypt
import requests
import os

_accounts = {}

server_link = 'http://chatdepot.twitch.tv/room_memberships?oauth_token='


def load_accounts():
    global _accounts
    with open('.config', 'rb') as tmp_file:
        tmp_line = tmp_file.readline()

        if len(tmp_line) > 0:

            data = str(decrypt(os.environ['cryptkey'], tmp_line).decode('utf-8')).split('~')
            data.pop(0)

            for tmp_data in data:

                username, oath = tmp_data.split(':', 1)
                _accounts[username] = oath


def get_user_oath(username):
    global _accounts
    return _accounts[username]

def get_user_server():
    print(_accounts)

def add(username, oath):
    global _accounts
    current_usernames = {}

    with open('.config', 'rb') as tmp_file:
        tmp_data = tmp_file.readline()

        if len(tmp_data) > 0:
            data = str(decrypt(os.environ['cryptkey'], tmp_data).decode('utf-8')).split('~')
            print('data: ' + repr(data))
            for tmp_line in data:
                tmp_str = str(decrypt(os.environ['cryptkey'], tmp_line).decode('utf-8'))
                tmp_username, tmp_oath = tmp_str.split(':', 1)
                current_usernames[tmp_username] = tmp_oath

    current_usernames[username] = oath
    _accounts = current_usernames
    save_accounts()

def save_accounts():
    global _accounts
    f_string = ''
    if len(_accounts.keys()) > 0:
        pass
    for num, username in enumerate(_accounts):
        f_string += '~' + username + ':' + _accounts[username]
    print(f_string)
    #don't tab it josh
    with open('.config', 'wb') as tmpfile:
        tmpfile.write(encrypt(os.environ['cryptkey'], f_string))










def __init__():
    os.environ['cryptkey'] = 'senpai'