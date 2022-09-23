
import re
from typing import Annotated
from flask import Flask

import src.mu2OS.discordsecrets as discordsecrets
from dubious.discord import api, req
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
def scene(
    op: Annotated[str, "The separator to use. `break` to end a scene, `pause` to pause, and `unpause` to resume.", [
        api.ApplicationCommandOptionChoice("break", "break"),
        api.ApplicationCommandOptionChoice("pause", "pause"),
        api.ApplicationCommandOptionChoice("unpause", "unpause")
    ]], *, channel_id: api.Snowflake | None
):
    """ Adds scene separators to a finished/paused scene. """

    if not channel_id:
        return api.InteractionCallbackMessages(
            content="You can't use this command outside of a guild.",
            flags=api.MessageFlag.EPHEMERAL
        )

    last: api.Message | None = None
    for hist in Pory.history(channel_id):
        if re.search(r"<>", hist.content):
            last = hist
            break
    
    if op == "break":
        message = Pory.send(channel_id, req.CreateMessage.Form(
            content="<><><><><><><><>",
            message_reference=api.MessageReference(
                message_id=last.id
            ) if last else None
        ))
        return api.InteractionCallbackMessages(
            content="Done!",
            flags = api.MessageFlag.EPHEMERAL
        )
    
    raise Exception()

pory.hook(app, Pory)