# -*- encoding: utf-8 -*-
from mm_client import MattermostClient
import re
from requests import request

URL = 'http://mattermost.example.org:8080/api/v1'
LOGIN = 'mattermostbot@ing.nl'
PASSWORD = 'bot-password'
TEAM = 'CDAAS'


class MattermostBot(object):
    def __init__(self):
        self.mm_cli = MattermostClient(URL)
        self.msg = None

    def get_message(self):
        return self.msg['props']['post']['message']

    def send(self, msg, ch_id=None):
        self.mm_cli.send_message(ch_id or self.msg['channel_id'], msg)

    def process_message(self):
        message = self.get_message()

        if re.match("list.*sergeant.*", message):
            r = request.get("http://sotdapi.herokuapp.com/sergeant/list")
            if r.status_code == 200:
                res = r.json()
                for n in res['names']:
                   self.send(n)

        if re.match("who.*sergeant.*", message):
            self.send(">  is Maurits, next sargent will be .... Maurits again")
            return

        self.send("I don't get it...")

    def run(self):
        self.mm_cli.login(TEAM, LOGIN, PASSWORD)
        for self.msg in self.mm_cli.recv_messages():
            if self.msg.get('action') == 'posted':
                self.process_message()


if __name__ == '__main__':
    try:
        MattermostBot().run()
    except KeyboardInterrupt:
        pass
