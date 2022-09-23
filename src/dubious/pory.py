
from dataclasses import InitVar, asdict, dataclass, field
from inspect import Parameter, signature
import inspect
from pprint import pprint
import re
import time
from typing import Annotated, Any, Callable, TypeVar, get_args, get_origin

import requests
from flask import Flask, abort, jsonify, request
from nacl.exceptions import BadSignatureError
from nacl.signing import VerifyKey

from dubious.discord import api, disc, req

def hook(app: Flask, actor: "Pory"):
    actor.sync_commands()
    VERIFY = VerifyKey(bytes.fromhex(actor.public_key))

    @app.route("/interactions", methods=["POST"])
    def _():
        signature = request.headers["X-Signature-Ed25519"]
        timestamp = request.headers["X-Signature-Timestamp"]
        body = request.data.decode("utf-8")

        try:
            VERIFY.verify(f"{timestamp}{body}".encode(), bytes.fromhex(signature))
        except BadSignatureError:
            abort(401, "Invalid request signature")

        if not request.json:
            return abort(405)
        ixn_json = request.json
        ixn = disc.cast(api.Interaction, ixn_json)
        return jsonify(actor.handle(ixn))

    return app

option_types = {
    str: api.ApplicationCommandOptionType.STRING,
    int: api.ApplicationCommandOptionType.INTEGER,
    bool: api.ApplicationCommandOptionType.BOOLEAN,
    api.User: api.ApplicationCommandOptionType.USER,
    api.Channel: api.ApplicationCommandOptionType.CHANNEL,
    api.Role: api.ApplicationCommandOptionType.ROLE,
    api.User: api.ApplicationCommandOptionType.USER,
    float: api.ApplicationCommandOptionType.NUMBER,
    api.Attachment: api.ApplicationCommandOptionType.ATTACHMENT,
}

pat_discord_name = re.compile(r"^[-_a-z]{1,32}$")

def _format_option(opt: Parameter):
    if not pat_discord_name.search(opt.name):
        # https://discord.com/developers/docs/interactions/application-commands#application-command-object-application-command-naming
        raise ValueError(f"Option '{opt.name}' has an incorrect name.")
    desc = "No description."
    choices = None
    if get_origin(opt.annotation) == Annotated:
        anns = get_args(opt.annotation)
        typ = option_types[anns[0]]
        if len(anns) > 1:
            if len(anns[1]) > 100:
                raise ValueError(f"The description for option '{opt.name}' is too long. Should be 100 or less; got {len(anns[1])}.")
            desc = anns[1]
        if len(anns) > 2: choices = anns[2]
    else:
        typ = option_types[opt.annotation]

    return api.ApplicationCommandOption(
        typ,
        opt.name,
        desc,
        required=opt.default == Parameter.empty,
        choices=choices
    )

ta_CommandCallback = Callable[..., api.InteractionCallbackMessages | api.InteractionCallbackModal]
ta_ComponentCallback = Callable[..., api.InteractionCallbackMessages | api.InteractionCallbackModal]
ta_ModalCallback = Callable[..., api.InteractionCallbackMessages]

@dataclass
class Pory:
    id: str
    public_key: str
    secret: str

    on_command: dict[str, ta_CommandCallback] = field(default_factory=dict, init=False)
    on_component: dict[str, ta_ComponentCallback] = field(default_factory=dict, init=False)
    on_modal: dict[str, ta_ModalCallback] = field(default_factory=dict, init=False)

    _token: disc.Token = field(init=False)
    @property
    def token(self):
        if not hasattr(self, "_token") or self._token.expired():
            self._token = disc.Token.get_token(self.id, self.secret)
        return self._token
    @token.setter
    def token(self, value):
        self._token = value
    @token.deleter
    def token(self):
        del self._token

    t_Callback = TypeVar("t_Callback", bound=ta_CommandCallback | ta_ComponentCallback | ta_ModalCallback)
    def command(self, callback: t_Callback) -> t_Callback:
        self.on_command[callback.__name__] = callback
        return callback
    
    def component(self, callback: t_Callback) -> t_Callback:
        self.on_component[callback.__name__] = callback
        return callback

    def sync_commands(self):
        commands = req.GetGlobalApplicationCommands(self.id).do_with(self.token)
        for command in commands:
            if not command.name in self.on_command:
                req.DeleteGlobalApplicationCommand(self.id, command.id).do_with(self.token)

        for name, command in self.on_command.items():
            if not pat_discord_name.search(name):
                # https://discord.com/developers/docs/interactions/application-commands#application-command-object-application-command-naming
                raise ValueError(f"Command '{name}' has an incorrect name.")
            if not command.__doc__:
                raise ValueError(f"Command '{name}' doesn't have a docstring description.")
            if len(command.__doc__) > 100:
                raise ValueError(f"The docstring on command '{name}' is too long. Should be 100 or less; got {len(command.__doc__)}.")
            
            options: list[api.ApplicationCommandOption] = []
            for opt in signature(command).parameters.values():
                if opt.kind == Parameter.POSITIONAL_OR_KEYWORD:
                    try:
                        options.append(_format_option(opt))
                    except ValueError as e:
                        raise ValueError(f"In command '{name}': {e}")
            if len(options) > 25: raise ValueError(f"There are too many options for command \"{name}\". Should be 25 or less; got {len(options)}.")
            
            req.CreateGlobalApplicationCommand(
                self.id,
                req.CreateGlobalApplicationCommand.Form(
                    name, command.__doc__,
                    options = options if options else None,
                    type=api.ApplicationCommandType.CHAT_INPUT
                )
            ).do_with(self.token)
    
    def perform_callback(self, callback: Callable, ixn: api.Interaction):
        sig = inspect.signature(callback)
        wants: dict[str, Any] = {}
        for paramname, param in sig.parameters.items():
            if param.kind in (param.VAR_POSITIONAL, param.VAR_KEYWORD, param.POSITIONAL_ONLY): raise Exception()
            if param.kind == param.POSITIONAL_OR_KEYWORD:
                if not isinstance(ixn.data, api.ApplicationCommandData): raise Exception()
                if not param.default == param.empty: continue
                if not ixn.data.options: raise Exception()

                found = False
                for opt in ixn.data.options:
                    found = opt.name == paramname
                    if found:
                        wants[paramname] = opt.value
                        break
                if not found: raise Exception()
            elif param.kind == param.KEYWORD_ONLY:
                if hasattr(ixn, paramname):
                    wants[paramname] = getattr(ixn, paramname)
                elif hasattr(ixn.data, paramname):
                    wants[paramname] = getattr(ixn.data, paramname)
                else: raise Exception()
        return callback(**wants)

    def handle(self, ixn: api.Interaction):
        got: api.InteractionCallbackData | None = None
        typ: api.InteractionCallbackType | None = None

        match ixn.type:
            case api.InteractionType.PING:
                typ = api.InteractionCallbackType.PONG
            case api.InteractionType.APPLICATION_COMMAND:
                if not isinstance(ixn.data, api.ApplicationCommandData): raise Exception()
                if not ixn.data.name in self.on_command: raise Exception()
                got = self.perform_callback(self.on_command[ixn.data.name], ixn)
            case api.InteractionType.MODAL_SUBMIT:
                if not isinstance(ixn.data, api.ModalSubmitData): raise Exception()
                if not ixn.data.custom_id in self.on_modal: raise Exception()
                got = self.perform_callback(self.on_modal[ixn.data.custom_id], ixn)
            case api.InteractionType.MESSAGE_COMPONENT:
                if not isinstance(ixn.data, api.MessageComponentData): raise Exception()
                if not ixn.data.custom_id in self.on_component: raise Exception()
                got = self.perform_callback(self.on_component[ixn.data.custom_id], ixn)
        
        if not typ:
            if isinstance(got, api.InteractionCallbackMessages):
                if isinstance(ixn.data, api.MessageComponentData):
                    typ = api.InteractionCallbackType.UPDATE_MESSAGE
                elif isinstance(ixn.data, api.ApplicationCommandData):
                    typ = api.InteractionCallbackType.CHANNEL_MESSAGE_WITH_SOURCE
            elif isinstance(got, api.InteractionCallbackModal):
                typ = api.InteractionCallbackType.MODAL
        if not typ: raise Exception()

        return asdict(api.InteractionResponse(typ, data=got))
    
    def send(self, channel_id: api.Snowflake, message: req.CreateMessage.Form):
        return req.CreateMessage(channel_id, message).do_with(self.token)

    def history(self, channel_id: api.Snowflake, limit: int=200):
        messages: list[api.Message] = []
        while limit:
            chunk = limit
            if chunk > 100:
                chunk = 100
            messages += req.GetChannelMessages(channel_id, req.GetChannelMessages.Query(
                limit = chunk
            )).do_with(self.token)
            for message in messages:
                yield message
            limit -= chunk

