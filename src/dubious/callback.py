
import dataclasses as dc
import inspect
import re
import traceback as tb
import typing as t
from pprint import pprint

from dubious.discord import api, disc, req

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

def prepare_option(opt: inspect.Parameter):
    if not pat_discord_name.search(opt.name):
        # https://discord.com/developers/docs/interactions/application-commands#application-command-object-application-command-naming
        raise ValueError(f"Option '{opt.name}' has an invalid name.")
    desc = "No description."
    choices = None
    if t.get_origin(opt.annotation) == t.Annotated:
        anns = t.get_args(opt.annotation)
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
        required=opt.default == inspect._empty,
        choices=choices
    )

ta_Callback = t.Callable[..., api.InteractionCallbackData | None]

def do_callback(callback: ta_Callback, ixn: api.Interaction, data: api.InteractionData | api.ApplicationCommandInteractionDataOption | None):
    wants: dict[str, t.Any] = {}
    for paramname, param in inspect.signature(callback).parameters.items():
        match param.kind:
            case inspect.Parameter.POSITIONAL_OR_KEYWORD:
                assert isinstance(data, api.ApplicationCommandData)
                if not param.default == inspect._empty: continue
                assert data.options

                found = False
                for opt in data.options:
                    found = opt.name == paramname
                    if found:
                        wants[paramname] = opt.value
                        break
                assert found
            case inspect.Parameter.KEYWORD_ONLY:
                if hasattr(ixn, paramname):
                    wants[paramname] = getattr(ixn, paramname)
                elif hasattr(ixn.data, paramname):
                    wants[paramname] = getattr(ixn.data, paramname)
                else:
                    raise Exception()
            case _:
                raise Exception()

    return callback(**wants)

ps_CallbackArgs = t.ParamSpec("ps_CallbackArgs")
t_CallbackRet = t.TypeVar("t_CallbackRet", bound=api.InteractionCallbackData | None)
@dc.dataclass(frozen=True)
class Callback(api.ApplicationCommandOption, t.Generic[ps_CallbackArgs, t_CallbackRet]):
    __func__: t.Callable[ps_CallbackArgs, t_CallbackRet]
    _options: dict[str, api.ApplicationCommandOption] = dc.field(default_factory=dict, init=False)
    
    @property
    def options(self):
        return list(self._options.values())
    @options.setter
    def options(self, val: list[api.ApplicationCommandOption] | None):
        pass

    def __post_init__(self):
        assert pat_discord_name.search(self.name), f"Command '{self.name}' has an invalid name."
        assert len(self.description) <= 100, f"The description on command '{self.name}' is too long. Should be 100 or less; got {len(self.description)}."

        for opt in inspect.signature(self.__func__).parameters.values():
            if opt.kind == inspect.Parameter.POSITIONAL_OR_KEYWORD:
                try:
                    self._options[opt.name] = prepare_option(opt)
                except Exception as e:
                    raise ValueError(f"In command '{self.name}': {''.join(tb.format_exception(e))}")
        if len(self.options) > 25: raise ValueError(f"There are too many options for command \"{self.name}\". Should be 25 or less; got {len(self.options)}.")

    def __call__(self, *args: ps_CallbackArgs.args, **kwargs: ps_CallbackArgs.kwargs):
        return self.__func__(*args, **kwargs)

    def cast_to_form_as_type(self, as_type: api.ApplicationCommandType):
        prepared_commands: list[req.CreateGlobalApplicationCommand.Form] = []
        for command in self.options:
            to_cast = dc.asdict(dc.replace(command, type=as_type))
            if command.options: to_cast["options"] = [dc.asdict(option) for option in command.options]
            prepared_commands.append(disc.cast(req.CreateGlobalApplicationCommand.Form, to_cast))
            print(f"prepared command:")
            pprint(prepared_commands[-1])
        return prepared_commands

    def do(self, ixn: api.Interaction, data: api.InteractionData | api.ApplicationCommandInteractionDataOption | None):
        if (
            isinstance(data, (api.ApplicationCommandData, api.ApplicationCommandInteractionDataOption)) and
            data.options and
            len(data.options) == 1
        ):
            option, = data.options
            subcommand = self._options[option.name]
            assert isinstance(subcommand, Callback)
            return subcommand.do(ixn, option)
        return do_callback(self.__func__, ixn, data)

@dc.dataclass(frozen=True)
class Group(Callback[[], None]):

    @classmethod
    def new(cls):
        return cls(
            api.ApplicationCommandOptionType.SUB_COMMAND_GROUP,
            "_",
            "_",
            lambda: None
        )

    def __call__(self, callback: t.Callable[ps_CallbackArgs, t_CallbackRet]) -> Callback[ps_CallbackArgs, t_CallbackRet]:
        assert callback.__doc__
        command = self._options[callback.__name__] = Callback(
            api.ApplicationCommandOptionType.SUB_COMMAND,
            callback.__name__,
            callback.__doc__,
            callback
        )
        return command

    def group(self, name: str, desc: str):
        group = self._options[name] = self.__class__(
            api.ApplicationCommandOptionType.SUB_COMMAND_GROUP,
            name,
            desc,
            lambda: None
        )
        return group
