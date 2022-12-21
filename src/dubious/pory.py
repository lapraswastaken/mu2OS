
from __future__ import annotations

import dataclasses as dc
import json
import multiprocessing as mp
import typing as t
from pprint import pprint

from flask import Flask, abort, jsonify, request
from nacl.exceptions import BadSignatureError
from nacl.signing import VerifyKey

from dubious import callback as cb
from dubious.discord import api, disc, req


def _match_response_type(response: api.InteractionCallbackData | None, ixn_type: api.InteractionType) -> api.InteractionCallbackType:
    match response:
        case api.ResponseMessage():
            return api.InteractionCallbackType.CHANNEL_MESSAGE_WITH_SOURCE
        case api.ResponseModal():
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

    on_command: cb.CommandGroup = dc.field(default_factory=cb.CommandGroup.new, init=False)
    on_message: cb.CommandGroup = dc.field(default_factory=cb.CommandGroup.new, init=False)
    on_user: cb.CommandGroup = dc.field(default_factory=cb.CommandGroup.new, init=False)
    on_modal: cb.Group = dc.field(default_factory=cb.Group, init=False)
    on_component: cb.Group = dc.field(default_factory=cb.Group, init=False)
    
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
                return abort(405, "Bad request")
            ixn_json = request.json
            ixn = disc.cast(api.Interaction, ixn_json)
            res = self.handle(ixn)
            return jsonify(dc.asdict(res))

        return app

    def sync_commands(self):
        prepared_on_command = self.on_command.get_commands(as_type=api.ApplicationCommandType.CHAT_INPUT)
        prepared_on_message = self.on_message.get_commands(as_type=api.ApplicationCommandType.MESSAGE)
        prepared_on_user = self.on_user.get_commands(as_type=api.ApplicationCommandType.USER)

        registered_commands: list[api.ApplicationCommand] = []
        guilds = req.GetCurrentUserGuilds().do_with(self.token)
        for guild in guilds:
            registered_commands += req.GetGuildApplicationCommands(self.id, guild.id).do_with(self.token)
        registered_commands += req.GetGlobalApplicationCommands(self.id).do_with(self.token)

        for registered in registered_commands:
            match registered.type:
                case api.ApplicationCommandType.CHAT_INPUT:
                    prepared = prepared_on_command
                case api.ApplicationCommandType.MESSAGE:
                    prepared = prepared_on_message
                case api.ApplicationCommandType.USER:
                    prepared = prepared_on_user
                case _:
                    raise Exception()
            self.compare_if_exists(registered, prepared)

        for to_register in (
            list(prepared_on_command.values()) +
            list(prepared_on_message.values()) +
            list(prepared_on_user.values())
        ):
            self.create_command(to_register)

    def compare_if_exists(self, registered: api.ApplicationCommand, prepared: dict[str, cb.Command]):
        if not registered.name in prepared:
            if not registered.guild_id:
                print(f"Deleting registered command: {registered.name}")
                req.DeleteGlobalApplicationCommand(self.id, registered.id).do_with(self.token)
            else:
                print(f"Deleting registered command in guild {registered.guild_id}: {registered.name}")
                req.DeleteGuildApplicationCommand(self.id, registered.guild_id, registered.id).do_with(self.token)
        elif registered.guild_id == prepared[registered.name].guild_id:
            if not prepared[registered.name].compare_with(registered):
                pprint(prepared[registered.name].options)
                pprint(registered.options)
                if not registered.guild_id:
                    print(f"Updating registered command: {registered.name}")
                    req.EditGlobalApplicationCommand(self.id, registered.id, disc.cast(req.EditGlobalApplicationCommand.Form, registered))
                else:
                    print(f"Updating registered command in guild {registered.guild_id}: {registered.name}")
                    req.EditGuildApplicationCommand(self.id, registered.guild_id, registered.id, disc.cast(req.EditGuildApplicationCommand.Form, registered))
            prepared.pop(registered.name)

    def create_command(self, to_register: cb.Command):
        if not to_register.guild_id:
            print(f"Creating new command: {to_register.name}")
            req.CreateGlobalApplicationCommand(self.id, form=disc.cast(req.CreateGlobalApplicationCommand.Form, to_register)).do_with(self.token)
        else:
            print(f"Creating new command in guild {to_register.guild_id}: {to_register.name}")
            req.CreateGuildApplicationCommand(self.id, to_register.guild_id, form=disc.cast(req.CreateGuildApplicationCommand.Form, to_register)).do_with(self.token)

    def handle(self, ixn: api.Interaction):
        match ixn:
            case api.Interaction(
                type=api.InteractionType.PING as ixn_type,
                data=None as data
            ):
                callback = self.get_callback_for_ping()

            case api.Interaction(
                type=api.InteractionType.APPLICATION_COMMAND as ixn_type,
                data=api.ApplicationCommandData(name=command_name) as data
            ):
                callback = self.get_callback_for_command(command_name)

            case api.Interaction(
                type=api.InteractionType.MODAL_SUBMIT as ixn_type,
                data=api.ModalSubmitData(custom_id=modal_id) as data
            ):
                callback = self.get_callback_for_modal(modal_id)

            case api.Interaction(
                type=api.InteractionType.MESSAGE_COMPONENT as ixn_type,
                data=api.MessageComponentData(custom_id=component_id) as data
            ):
                callback = self.get_callback_for_component(component_id)

            case _:
                raise Exception()

        response = callback.do(ixn, data) if isinstance(callback, cb.Callback) else None
        return api.InteractionResponse(_match_response_type(response, ixn_type), data=response)
    
    def get_callback_for_ping(self):
        return None
    
    def get_callback_for_command(self, command_name: str):
        return next(filter(
            lambda on: command_name in on._options,
            (self.on_command, self.on_message, self.on_user)
        ))._options[command_name]
    
    def get_callback_for_modal(self, modal_id: str):
        return self.on_modal._options[modal_id]
    
    def get_callback_for_component(self, component_id: str):
        return self.on_component._options[component_id]

    def create_cancel_button(self, ixn_id: api.Snowflake, token: str, process_message: str, button_text: str):
        lock = mp.Event()
        @self.on_component(
            name=ixn_id
        )
        def _():
            lock.set()
            self.delete_response(token)
            self.on_component._options.pop(ixn_id)

        return api.ResponseMessage(
            content=process_message,
            components=[api.ActionRow([
                api.Button(
                    api.ButtonStyle.DANGER,
                    label=button_text,
                    custom_id=ixn_id
                )
            ])]
        ), lock
    
    def send_response(self, token: str, followup: req.ExecuteWebhook.Form):
        return req.ExecuteWebhook(self.id, token, form=followup).do_with(self.token)

    def edit_response(self, token: str, edit: req.EditWebhookMessage.Form, response_id: str="@original"):
        return req.EditWebhookMessage(self.id, token, response_id, form=edit).do_with(self.token)

    def delete_response(self, token: str, response_id: str="@original"):
        req.DeleteWebhookMessage(self.id, token, response_id).do_with(self.token)
    
    def send(self, channel_id: api.Snowflake, message: req.CreateMessage.Form):
        return req.CreateMessage(channel_id, message).do_with(self.token)
    
    def edit(self, channel_id: api.Snowflake, message_id: api.Snowflake, message: req.EditMessage.Form):
        return req.EditMessage(channel_id, message_id, message).do_with(self.token)
    
    def delete(self, channel_id: api.Snowflake, message_id: api.Snowflake):
        req.DeleteMessage(channel_id, message_id).do_with(self.token)

    def history(self, channel_id: api.Snowflake, limit: int=200, chunk_size: int=50):
        message: api.Message | None = None
        while limit:
            chunk = limit
            if chunk > chunk_size:
                chunk = chunk_size
            messages = req.GetChannelMessages(channel_id, req.GetChannelMessages.Query(
                before = message.id if message else None,
                limit = chunk
            )).do_with(self.token)
            while messages:
                message = messages.pop(0)
                yield message
                limit -= 1
                chunk -= 1
            if chunk:
                limit = 0

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

        config = self.on_command.group(
            "config",
            "Configures a channel to do something related to this bot.",
            [api.Permission.MANAGE_CHANNELS]
        )
        
        for field in dc.fields(config_model):
            type_field = field.type if not t.get_origin(field.type) else t.get_origin(field.type)
            if not type_field is api.Snowflake: continue
            setters = config.group(
                f"{field.name}",
                f"Configure a {'list of channels' if t.get_origin(field.type) else 'channel'} to be related to {field.name}."
            )
            if t.get_origin(field.type):
                @setters
                def add(channel: api.Channel, *, guild_id: api.Snowflake | None):
                    if not guild_id:
                        return api.ResponseMessage(content="You can't use this command outside of a guild.")
                    channel_list: list[api.Snowflake] = getattr(self.guilds[guild_id], field.name)
                    channel_list.append(channel.id)
                    return api.ResponseMessage(
                        content=f"Channel {channel.name} added to {field.name}."
                    )
                @setters
                def remove(channel: api.Channel, *, guild_id: api.Snowflake | None):
                    if not guild_id:
                        return api.ResponseMessage(content="You can't use this command outside of a guild.")
                    channel_list: list[api.Snowflake] = getattr(self.guilds[guild_id], field.name)
                    if not channel.id in channel_list:
                        return api.ResponseMessage(content=f"That channel isn't a part of {field.name}.")
                    channel_list.remove(channel.id)
                    return api.ResponseMessage(content=f"Channel {channel.name} removed from {field.name}.")
            else:
                @setters
                def set(channel: api.Channel, *, guild_id: api.Snowflake | None):
                    pass
