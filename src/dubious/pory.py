
from __future__ import annotations
import json
import multiprocessing as mp
import dataclasses as dc
import typing as t

from flask import Flask, abort, jsonify, request
from nacl.exceptions import BadSignatureError
from nacl.signing import VerifyKey

from dubious.discord import api, disc, req
from dubious import callback as cb

t_Any = t.TypeVar("t_Any")
def add_meta(meta_name: str, s: str):
    def _(obj: t_Any) -> t_Any:
        setattr(obj, meta_name, s)
        return obj
    return _

def name(s: str): return add_meta("__name__", s)
def desc(s: str): return add_meta("__doc__", s)

def do_after(callback: t.Callable[[], None]):
    mp.Process(target=callback).start()

def match_response_type(response: api.InteractionCallbackData | None, ixn_type: api.InteractionType) -> api.InteractionCallbackType:
    match response:
        case api.InteractionCallbackMessage():
            return api.InteractionCallbackType.CHANNEL_MESSAGE_WITH_SOURCE
        case api.InteractionCallbackModal():
            return api.InteractionCallbackType.MODAL
        case None:
            match ixn_type:
                case api.InteractionType.PING:
                    return api.InteractionCallbackType.PONG
                case api.InteractionType.APPLICATION_COMMAND | api.InteractionType.MODAL_SUBMIT:
                    return api.InteractionCallbackType.DEFERRED_CHANNEL_MESSAGE_WITH_SOURCE
                case api.InteractionType.MESSAGE_COMPONENT:
                    return api.InteractionCallbackType.DEFERRED_UPDATE_MESSAGE
                case _:
                    raise Exception()
        case _:
            raise Exception()

@dc.dataclass
class Pory:
    app_id: dc.InitVar[str]
    public_key: str
    token: str

    id: disc.Snowflake = dc.field(init=False)

    def __post_init__(self, app_id: str):
        self.id = disc.Snowflake(app_id)

    on_command: cb.Group = dc.field(default_factory=cb.Group.new, init=False)
    on_message: cb.Group = dc.field(default_factory=cb.Group.new, init=False)
    on_user: cb.Group = dc.field(default_factory=cb.Group.new, init=False)
    on_modal: cb.Group = dc.field(default_factory=cb.Group.new, init=False)
    on_component: cb.Group = dc.field(default_factory=cb.Group.new, init=False)
    
    def flask(self):
        app = Flask(__name__)
        
        self.sync_commands()
        verify_key = VerifyKey(bytes.fromhex(self.public_key))

        @app.route("/interactions", methods=["POST"])
        def _():
            signature = request.headers["X-Signature-Ed25519"]
            timestamp = request.headers["X-Signature-Timestamp"]
            body = request.data.decode("utf-8")

            try:
                verify_key.verify(f"{timestamp}{body}".encode(), bytes.fromhex(signature))
            except BadSignatureError:
                abort(401, "Invalid request signature")

            if not request.json:
                return "Bad request", 405
            ixn_json = request.json
            ixn = disc.cast(api.Interaction, ixn_json)
            res = self.handle(ixn)
            return jsonify(dc.asdict(res))

        return app

    def sync_commands(self):
        prepared_commands: list[req.CreateGlobalApplicationCommand.Form] = (
            self.on_command.cast_to_form_as_type(api.ApplicationCommandType.CHAT_INPUT) +
            self.on_message.cast_to_form_as_type(api.ApplicationCommandType.MESSAGE) +
            self.on_user.cast_to_form_as_type(api.ApplicationCommandType.USER)
        )

        commands = req.GetGlobalApplicationCommands(self.id).do_with(self.token)
        for command in commands:
            if not any(command.name in group.options for group in (
                self.on_command,
                self.on_message,
                self.on_user
            )):
                req.DeleteGlobalApplicationCommand(self.id, command.id).do_with(self.token)

        for to_register in prepared_commands:
            req.CreateGlobalApplicationCommand(self.id, form=to_register).do_with(self.token)

    def handle(self, ixn: api.Interaction):
        match ixn:
            case api.Interaction(
                type=api.InteractionType.PING as ixn_type,
                data=None as data
            ):
                callback = None
            case api.Interaction(
                type=api.InteractionType.APPLICATION_COMMAND as ixn_type,
                data=api.ApplicationCommandData(name=command_name) as data
            ):
                callback = next(filter(
                    lambda on: command_name in on._options,
                    (self.on_command, self.on_message, self.on_user)
                ))._options[command_name]
            case api.Interaction(
                type=api.InteractionType.MODAL_SUBMIT as ixn_type,
                data=api.ModalSubmitData(custom_id=modal_id) as data
            ):
                callback = self.on_modal._options[modal_id]
            case api.Interaction(
                type=api.InteractionType.MESSAGE_COMPONENT as ixn_type,
                data=api.MessageComponentData(custom_id=component_id) as data
            ):
                callback = self.on_component._options[component_id]
            case _:
                raise Exception()
        assert isinstance(callback, cb.Callback)
        response = callback.do(ixn, data)
        return api.InteractionResponse(match_response_type(response, ixn_type), data=response)
    
    def send(self, channel_id: api.Snowflake, message: req.CreateMessage.Form):
        return req.CreateMessage(channel_id, message).do_with(self.token)
    
    def delete(self, channel_id: api.Snowflake, message_id: api.Snowflake):
        req.DeleteMessage(channel_id, message_id).do_with(self.token)
    
    def delete_response(self, id: api.Snowflake, token: str, response_id: str="@original"):
        req.DeleteWebhookMessage(id, token, response_id).do_with(self.token)

    def history(self, channel_id: api.Snowflake, limit: int=200):
        message: api.Message | None = None
        messages: list[api.Message] = []
        while limit:
            chunk = limit
            if chunk > 100:
                chunk = 100
            messages += req.GetChannelMessages(channel_id, req.GetChannelMessages.Query(
                before = message.id if message else None,
                limit = chunk
            )).do_with(self.token)
            for message in messages:
                yield message
            limit -= chunk

t_ConfigType = t.TypeVar("t_ConfigType")
@dc.dataclass
class ConfiguredPory(Pory, t.Generic[t_ConfigType]):
    config_path: str
    config_model: dc.InitVar[type[t_ConfigType]]

    guilds: dict[api.Snowflake, t_ConfigType]

    def __post_init__(self, app_id: str, config_model: type[t_ConfigType]):
        super().__post_init__(app_id)

        with open(self.config_path, "r") as f:
            data = json.load(f)
        for guild_id in data:
            self.guilds[guild_id] = disc.cast(config_model, data[guild_id])
        
        for field in dc.fields(config_model):
            pass
