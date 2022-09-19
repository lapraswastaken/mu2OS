
from flask import Flask

import discordsecrets
from dubious.discord import api
from dubious import pory

app = Flask(__name__)

Pory = pory.Pory(
    discordsecrets.DISCORD_CLIENT_ID,
    discordsecrets.DISCORD_PUBLIC_KEY,
    discordsecrets.DISCORD_CLIENT_SECRET,
)

@Pory.command
def ping():
    """ Responds with "Pong!" """
    return api.InteractionCallbackMessages(
        content="Pong!"
    )

pory.hook(app, Pory)