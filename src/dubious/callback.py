
import dataclasses as dc
import inspect
import multiprocessing as mp
import re
import traceback as tb
import typing as t

from dubious.discord import api

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
        required=None if not opt.default == inspect._empty else True,
        choices=choices
    )

ta_CommandRet = api.InteractionCallbackData | None | t.Iterator[api.InteractionCallbackData | None]

ps_CallbackArgs = t.ParamSpec("ps_CallbackArgs")
t_CommandRet = t.TypeVar("t_CommandRet", bound=ta_CommandRet)

def do_callback(
    callback: t.Callable[ps_CallbackArgs, t_CommandRet],
    ixn: api.Interaction,
    data: api.InteractionData | api.ApplicationCommandInteractionDataOption | None
) -> t_CommandRet:
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
                if paramname == "ixn":
                    wants[paramname] = ixn
                elif paramname == "data":
                    wants[paramname] = ixn.data
                elif paramname == "user":
                    if not ixn.user:
                        assert ixn.member
                        wants[paramname] = ixn.member.user
                elif hasattr(ixn, paramname):
                    wants[paramname] = getattr(ixn, paramname)
                elif hasattr(ixn.data, paramname):
                    wants[paramname] = getattr(ixn.data, paramname)
                else:
                    raise Exception()
            case _:
                raise Exception()

    return callback(**wants) # type: ignore


@dc.dataclass
class Callback(t.Generic[ps_CallbackArgs, t_CommandRet]):
    name: str
    __func__: t.Callable[ps_CallbackArgs, t_CommandRet]

    def do(self, ixn: api.Interaction, data: api.InteractionData | api.ApplicationCommandInteractionDataOption | None) -> api.InteractionCallbackData | None:
        done = do_callback(self.__func__, ixn, data)
        if isinstance(done, t.Iterator):
            initial_return = next(done)
            mp.Process(target=list, args=(done,)).start()
            return initial_return
        return done

@dc.dataclass
class Group:
    _options: dict[str, Callback] = dc.field(default_factory=dict, kw_only=True)

    def __call__(self, cb: t.Callable[ps_CallbackArgs, t_CommandRet] | None = None, /, *, name: str | None=None):
        def _(callback: t.Callable[ps_CallbackArgs, t_CommandRet]):
            _name = name if name else callback.__name__
            self._options[_name] = Callback(_name, callback)
            return callback
        if cb: return _(cb)
        else: return _

@dc.dataclass
class Command(api.ApplicationCommandOption, Callback[ps_CallbackArgs, t_CommandRet]):
    __func__: t.Callable[ps_CallbackArgs, t_CommandRet]
    default_member_permissions: str | None = None
    _options: dict[str, api.ApplicationCommandOption] = dc.field(default_factory=dict, kw_only=True)
    guild_id: api.Snowflake | None = None

    @property
    def options(self):
        return list(self._options.values()) if self._options else None
    @options.setter
    def options(self, _: list[api.ApplicationCommandOption] | None):
        # only needed to appease dataclass default __init__
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
        if len(self._options) > 25: raise ValueError(f"There are too many options for command \"{self.name}\". Should be 25 or less; got {len(self._options)}.")

    def compare_with(self, registered: api.ApplicationCommand):
        return (
            self.guild_id == registered.guild_id and
            self.default_member_permissions == registered.default_member_permissions and
            self.compare_with_as_option(registered)
        )
    
    def compare_with_as_option(self, registered: api.ApplicationCommand | api.ApplicationCommandOption):
        return (
            self.name == registered.name and
            self.name_localizations == registered.name_localizations and
            self.description == registered.description and
            self.description_localizations == registered.description_localizations and
            all(
                this_opt.compare_with_as_option(that_opt)
                    if isinstance(this_opt, Command) else
                this_opt == that_opt
                    for this_opt, that_opt in zip(self.options, registered.options)
            ) if self.options and registered.options else self.options == registered.options
        )

    def __call__(self, *args: ps_CallbackArgs.args, **kwargs: ps_CallbackArgs.kwargs):
        return self.__func__(*args, **kwargs)

    def do(self, ixn: api.Interaction, data: api.InteractionData | api.ApplicationCommandInteractionDataOption | None) -> api.InteractionCallbackData | None:
        if (
            isinstance(data, (api.ApplicationCommandData, api.ApplicationCommandInteractionDataOption)) and
            data.options and
            len(data.options) == 1
        ):
            option, = data.options
            subcommand = self._options[option.name]
            assert isinstance(subcommand, Command)
            return subcommand.do(ixn, option)
        return super().do(ixn, data)

@dc.dataclass
class CommandGroup(Group, Command[[], None]):
    _options: dict[str, Command] = dc.field(default_factory=dict, kw_only=True)

    def get_commands(self, *, as_type: api.ApplicationCommandType | None=None):
        prepared_commands: dict[str, Command] = {}
        for opt in self._options.values():
            prepared = opt
            if as_type:
                # below should type error but dc.replace doesn't care
                # api.ApplicationCommandOption.type field can't be type api.ApplicationCommandType
                prepared = dc.replace(prepared, type=as_type)
            if isinstance(prepared, CommandGroup):
                prepared = dc.replace(prepared, _options=prepared.get_commands())
            prepared_commands[opt.name] = prepared
        return prepared_commands

    @classmethod
    def new(cls):
        return cls(
            "_",
            lambda: None,
            api.ApplicationCommandOptionType.SUB_COMMAND_GROUP,
            "_",
        )

    def __call__(self, cb: t.Callable[ps_CallbackArgs, t_CommandRet] | None=None, /, *,
        name: str | None=None,
        desc: str | None=None,
        perms: list[api.Permission] | None=None,
        guild: api.Snowflake | None=None,
    ):
        def _(callback: t.Callable[ps_CallbackArgs, t_CommandRet]) -> t.Callable[ps_CallbackArgs, t_CommandRet]:
            _name = name if name else callback.__name__
            _desc = desc if desc else callback.__doc__ if (not desc) and callback.__doc__ else "No description provided."
            _perms = 0
            for perm in perms if perms else []:
                _perms |= perm
            self._options[_name] = Command(
                _name,
                callback,
                api.ApplicationCommandOptionType.SUB_COMMAND,
                _desc.strip(),
                str(_perms) if perms else None,
                guild,
            )
            return callback
        if cb: return _(cb)
        else: return _

    def group(self,
        name: str,
        desc: str,
        perms: t.Collection[api.Permission] | None=None,
        guild: api.Snowflake | None=None
    ):
        _perms = 0
        for perm in perms if perms else []:
            _perms |= perm
        group = self._options[name] = self.__class__(
            name,
            lambda: None,
            api.ApplicationCommandOptionType.SUB_COMMAND_GROUP,
            desc,
            str(_perms) if perms else None,
            guild
        )
        return group
