
from dataclasses import asdict, dataclass, field
from inspect import Parameter, signature
import time
from typing import Annotated, Callable, get_args, get_origin

import requests
from flask import Flask, abort, jsonify, request
from nacl.exceptions import BadSignatureError
from nacl.signing import VerifyKey

from dubious.discord import api, disc, req

def hook(app: Flask, actor: "Pory"):
    actor.new_token()
    actor._register_commands()
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

def _format_option(opt: Parameter):
    name = opt.name
    req = opt.default != Parameter.empty
    desc = "No description."
    choices = None
    if get_origin(opt.annotation) == Annotated:
        anns = get_args(opt.annotation)
        typ = option_types[anns[0]]
        if len(anns) > 1: desc = anns[1]
        if len(anns) > 2: choices = anns[2]
    else:
        typ = option_types[opt.annotation]
    return api.ApplicationCommandOption(typ, name, desc, required=req, choices=choices)

@dataclass
class Token:
    access_token: str
    expires_in: int
    scope: str
    token_type: str

    now: float = field(init=False)

    def __post_init__(self):
        self.now = time.time()

    def expired(self):
        return (time.time() - self.now) > self.expires_in

    @classmethod
    def get_token(cls, c_id: str, c_secret: str):
        data = {
            'grant_type': 'client_credentials',
            'scope': 'identify connections'
        }
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        r = requests.post(f'{disc.ROOT}/oauth2/token', data=data, headers=headers, auth=(c_id, c_secret))
        r.raise_for_status()
        return cls(**r.json())

@dataclass
class Pory:
    app_id: str
    public_key: str
    secret: str
    guild: disc.Snowflake | None = None

    token: Token = field(init=False)
    on_command: dict[str, Callable] = field(default_factory=dict, init=False)
    on_component: dict[str, Callable] = field(default_factory=dict, init=False)
    on_modal: dict[str, Callable] = field(default_factory=dict, init=False)

    def new_token(self):
        self.token = Token.get_token(self.app_id, self.secret)
    
    def handle(self, ixn: api.Interaction):
        match ixn.type:
            case api.InteractionType.PING:
                return asdict(api.InteractionResponse(api.InteractionCallbackType.PONG))
            case api.InteractionType.APPLICATION_COMMAND:
                if not isinstance(ixn.data, api.ApplicationCommandData): raise Exception()
                if not ixn.data.name in self.on_command: raise Exception()
                return asdict(self.on_command[ixn.data.name](ixn.data))

    def command(self, callback: Callable[..., api.InteractionCallbackMessages]):
        self.on_command[callback.__name__] = callback
        return callback

    def _register_commands(self):
        for name, command in self.on_command.items():
            if not command.__doc__:
                raise ValueError(f"Callback for command \"{name}\" doesn't have a docstring description.")
            options: list[api.ApplicationCommandOption] = []
            for opt in list(signature(command).parameters.values())[1:]:
                if opt.kind == Parameter.POSITIONAL_ONLY:
                    options.append(_format_option(opt))
            if self.guild:
                req.CreateGuildApplicationCommand(
                    self.app_id,
                    self.guild,
                    req.CreateGuildApplicationCommand.Form(
                        name, command.__doc__,
                        options = options if options else None
                    )
                ).do_with(self.token.access_token)
            else:
                req.CreateGlobalApplicationCommand(
                    self.app_id,
                    req.CreateGlobalApplicationCommand.Form(
                        name, command.__doc__,
                        options = options if options else None
                    )
                ).do_with(self.token.access_token)
