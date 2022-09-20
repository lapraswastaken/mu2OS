
from flask import Flask

import discordsecrets
from dubious.discord import api
from dubious import pory

app = Flask(__name__)

Pory = pory.Pory(
    discordsecrets.DISCORD_CLIENT_ID,
    discordsecrets.DISCORD_PUBLIC_KEY,
    discordsecrets.DISCORD_CLIENT_SECRET
)

@Pory.command
def ping():
    """ Responds with "Pong!" """
    return api.InteractionCallbackMessages(
        content="Pong!"
    )

@Pory.command
def echo(message: str):
    """ Responds with the message given. """
    return api.InteractionCallbackMessages(
        content=message
    )

@Pory.command
def button(count: int=0):
    """ Creates a button that you can click to increase a count! """
    return api.InteractionCallbackMessages(
        content = f"{count}",
        components = [
            api.ActionRow([
                api.Button(api.ButtonStyle.PRIMARY,
                    label = "+",
                    custom_id = on_increment.__name__
                )
            ])
        ]
    )

@Pory.component
def on_increment(*, message: api.Message):
    return button(int(message.content) + 1)

pory.hook(app, Pory)