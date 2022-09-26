
import re
from dataclasses import dataclass, field
from typing import Collection

from dubious import pory
from dubious.discord import api, req

import mu2OS.discordsecrets as discordsecrets


@dataclass
class RPConfig:
    rp_channels: list[api.Snowflake] = field(default_factory=list)

@dataclass
class LogConfig:
    log_channel: api.Snowflake | None

Pory = pory.Pory(
    discordsecrets.DISCORD_CLIENT_ID,
    discordsecrets.DISCORD_PUBLIC_KEY,
    discordsecrets.DISCORD_USER_TOKEN
)

@Pory.on_command
def ping():
    """ Responds with "Pong!" """
    return api.InteractionCallbackMessage(
        content="Pong!"
    )

scene = Pory.on_command.group("scene", "Adds a scene separator to a finished/paused scene.")

str_break = "<><><><><><><><>"
str_pause = "(Scene paused)"
str_unpause = "(Scene unpaused)"

@scene
@pory.name("break")
def _(*, token: str, channel_id: api.Snowflake | None):
    """ Adds a scene break. """
    return separator(str_break, (str_break, str_pause, str_unpause), token, channel_id)

@scene
def pause(*, token: str, channel_id: api.Snowflake | None):
    """ Pauses a scene. The scene can be continued later with `unpause`. """
    return separator(str_pause, (str_break,), token, channel_id)

@scene
def unpause(*, token: str, channel_id: api.Snowflake | None):
    """ Unpauses the most recently paused scene. If used immediately after a pause, deletes that pause. """
    for hist in Pory.history(channel_id, limit=2) if channel_id else []:
        if re.search(str_pause, hist.content):
            Pory.delete(hist.channel_id, hist.id)
            Pory.delete_response(Pory.id, token)
            return
    return separator(str_unpause, (str_pause,), token, channel_id)

def separator(content: str, patterns: Collection[str], token: str, channel_id: api.Snowflake | None):

    if not channel_id:
        return api.InteractionCallbackMessage(
            content="You can't use this command outside of a guild.",
            flags=api.MessageFlag.EPHEMERAL
        )

    @pory.do_after
    def _():
        if not channel_id: return

        last: api.Message | None = None

        for hist in Pory.history(channel_id, limit=10000):
            if any(re.search(pat, hist.content) for pat in patterns):
                last = hist
                break

        Pory.send(channel_id, req.CreateMessage.Form(
            content=content,
            message_reference=api.MessageReference(
                message_id=last.id
            ) if last else None
        ))

        Pory.delete_response(Pory.id, token)

    return None

app = Pory.flask()
