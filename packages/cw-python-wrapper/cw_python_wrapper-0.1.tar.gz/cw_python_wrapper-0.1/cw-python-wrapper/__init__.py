__all__ = [
    'CwPythonWrapper'
]

from socketIO_client_nexus import SocketIO, LoggingNamespace
import json

from .BotControlUpdate import BotControlUpdate
from .IdentificationBot import IdentificationBot

class CwPythonWrapper:
    def __init__(self, botId, botSecret, tick):
        self.botId = botId,
        self.botSecret = botSecret,
        self.tick = tick
        self.socketIO.on("do-identification", self.on_do_identification)
        self.socketIO.on('identification-successful', self.on_identification_successful)
        self.socketIO.on('identification-bot-successful', self.identification_bot_successful)
        self.socketIO.on('identification-bot-failed', self.identification_bot_failed)
        self.socketIO.on('state', self.state)
        self.socketIO.wait()

    socketIO = SocketIO('localhost', 8080, LoggingNamespace)

    def on_do_identification(self, *args):
        print(args)
        self.socketIO.emit("identification", "VALID")

    def on_identification_successful(self, args):
        self.id = args
        print(self.id)
        identificationBot = IdentificationBot(self.botId[0], self.botSecret[0], self.id)
        self.socketIO.emit("identification-bot", json.dumps(identificationBot.__dict__))

    def identification_bot_successful(self, *args):
        print('bot authenticated')

    def identification_bot_failed(self, *args):
        print(args)

    def state(self, args):
        controls = self.tick(args)
        print(controls)
        bot_control_update = BotControlUpdate(self.id, self.botId, controls)
        self.socketIO.emit('bot-control-update', json.dumps(bot_control_update.__dict__))
