
from ast import arg
from dataclasses import dataclass, field
import os
import re

import inflect
from docparse.parser import Parser, parse, do_steps

p = inflect.engine()

Root = Parser(r"\n")

def make_singular(match: str):
    singular = p.singular_noun(match)
    if isinstance(singular, str): return singular
    return match
def namify(match: str):
    return "".join([w[0].upper() + w[1:] for w in match.split()])
def prepend_lines(prep: str, lines: str):
    return "\n".join([f"{prep}{line}" for line in lines.split("\n") if line])

class AppendBracketParser(Parser):
    def out(self, parser: Parser):
        return "}"

Disc = Root.copyto(AppendBracketParser)

@Root.hook(r"###### (.+?) Structure")
def create_disc_class(m: re.Match[str]):
    name, = m.groups()
    return f"interface {namify(name)} "+"{", Disc

def unfuck_type(typ: str):
    return do_steps(typ, {
        r"\[(.+?)\].*": lambda match: (
            namify(match.group(1))
        ),
        #r"string": "str",
        r"integer": "number",
        #r"number": "int",
        r"double": "number",
        #r"boolean": "bool",
        r"snowflake": "Snowflake",
        r"ISO8601 timestamp": "string",
        r"file contents": "any",

        r"`?20\d`? and an? ": "",
        r"`?20\d`? \w+ with ": "",
        r".+No Content.+": "void",
        r".+on success.*": "void",
        r".+[E|e]mpty [R|r]esponse.*": "void",

        r"\(default.*\)": "",
        r",(?: or)?": " |",
        r" or ": " | ",
        r"one of": "",
        r"\bthe (?:new|modified|created|updated|deleted|bot's) ": "",
        r"\\?\*": "",
        r"partial ": "",
        r"^an? ": "",
        r"^that ": "",
        r"^the ": "",
        r"up to \d+ ": "",
        
        r".*?(?:[a|A]rray|[l|L]ist) of (.+)": lambda match: (
            f"{make_singular(match.group(1))}[]"
        ),
        r".*?[m|M]ap of (.+) to (.+)": lambda match: (
            "{"+f"{make_singular(match.group(1))}: {make_singular(match.group(2))}"+"}"
        ),

        r"^\?(.+)": r"\1?",
        #r"(.+)\?$": r"\1 | None",
        r" for (.+?) options": "",
        r"dictionary with keys in AvailableLocales": r"{string: string}",
        r"^mixed.*": "any",
        r"binary": "any",
        r"thread-specific ": "",
        r"\(can be null only in reaction emoji objects\)": "",
        r"two ints \(shard_id \| num_shards\)": "[number, number]",
        r"Unsigned ": "",
        r" \(big endian\)": "",
        r"(?:Message)?Component": "MessageComponent",
        r"\bMember": "GuildMember",
        r"\bTag\b": "ForumTag",
        r"\bChoice\b": "ApplicationCommandOptionChoice",
        r"\b((?:ActionType)|(?:ActionMetadata)|(?:Action))\b": r"AutoModeration\1",
        r"\b(?:Event)?((?:EntityMetadata)|(?:PrivacyLevel)|(?:EntityType))\b": r"GuildScheduledEvent\1",
        r"\b(?:Event)?Status(?:Type)?\b": r"GuildScheduledEventStatusType",
        r"\b((?:Account))\b": r"Integration\1",
        r"channel Webhook": "Webhook",
        r"guild Webhook": "Webhook",
        r"(?:guild |DM)Channel": "Channel",
        r"all of the guild's ": "",
        r"object with .+": "any",
        r"PNG image widget for the guild": "any",
        r"GuildApplicationCommandPermission\b": "GuildApplicationCommandPermissions",
        r"Object$": "",
        r"AllowedMention\b": "AllowedMentions",
        r"\bImageData\b": "string",
        r"\bLevel\b": "number",
        r"\bWidget\b": "GuildWidget",
        r"\bGuildMembershipStateType\b": "MembershipStateType",
    })

def unfuck_desc(desc: str):
    return do_steps(desc, {
        r"\[(.+?)\]\(.+\)": r"`\1`"
    })

pat_field = r"^\| ([a-zA-Z?_]+?)[ \\\*]+\| (.+?) +\| (.+?) \|"
@Disc.hook(pat_field)
def format_field(m: re.Match[str]):
    name, typ, desc = m.groups()
    if name == "Field": return ""

    typ = unfuck_type(typ)

    desc = unfuck_desc(desc)

    if name.endswith("?"):
        if not typ.endswith("?"):
            typ += "?"
        #typ += " = field(kw_only=True, default=None)"
        name = name[:-1]
    
    match = re.search(r"`(\d+)`", desc)
    if match and "number" in typ and not re.search(r"min|max|version", name):
        #typ += f" = field(kw_only=True, default={match.group(1)})"
        typ += f" = {match.group(1)}"

    return f"    // {desc}\n    {name}: {typ}"

Enums = Root.copyto(AppendBracketParser)

@Root.hook(r"###### (.+? Flag)s?$")
@Root.hook(r"###### (.+? Type)s?$")
@Root.hook(r"###### (.+? Style)s?$")
@Root.hook(r"###### (.+? Level)s?$")
@Root.hook(r"###### (.+? Feature)s?$")
@Root.hook(r"###### (.+? Behavior)s?$")
@Root.hook(r"###### (.+? Scope)s?$")
#@Root.hook(r"###### (.+? Option)s?$")
def create_enum(m: re.Match[str]):
    name, = m.groups()
    if re.search(r"\bBy\b", name):
        return ""
    # typ = "int"
    # if name in [
    #     "Embed Type",
    #     "Allowed Mention Type",
    #     "Guild Feature",
    #     "OAuth2 Scope",
    #     "Mutable Guild Feature"
    # ]:
    #     typ = "str"
    return f"enum {namify(name)} "+"{", Enums

@Enums.hook(r"^\| (.+?)(?:[\\\* ])+\| (?:(.+?)(?:[\\\* ])+\|(?: (.*?) +\|)?)?$")
def format_flag_value(m: re.Match[str]):
    name, value, desc = m.groups()
    if "--" in name:
        return ""

    if value in (
        "Type",
        "Value",
        "Description",
        "Name",
        "ID",
        "Integer",
        "Required Permissions", # case for Guild -> Mutable Guild Features
    ):
        return ""

    if not re.match(r"[\d`x()< ]+", value):
        if re.match(r"^[A-Z_]+$", value): # case for backwards flag definitions (i.e. value in first column)
            _ = name
            name = value
            value = _
        else:
            if value and not desc:
                desc = value
            value = f'"{name}"'

    match_bitwise_value = re.search(r"\((\d+ << \d+)\)", value) # case for bitwise flags
    if match_bitwise_value:
        value, = match_bitwise_value.groups()
    name = do_steps(name.upper(), {
        r" ": "_", # case for Webhook -> Webhook Type
        r"\.": "_", # case for dotted enums
        r"\*": "", # case for Guild -> Mutable Guild Features
    })
    if desc:
        desc = unfuck_desc(desc)
        return f"    // {desc}\n    {name} = {value},"
    else:
        return f"    {name} = {value},"

@dataclass
class HttpReqData:
    name: str
    type_req: str
    endpoint: str
    type_ret = "void"
    type_query: list[str] = field(init=False, default_factory=list)
    type_form: list[str] = field(init=False, default_factory=list)

    inner: list[str] = field(default_factory=list, init=False)
    response: list[str] = field(default_factory=list, init=False)
    nullable: bool = field(default=True, init=False)

    def format(self):
        ep_parts = [arg for arg in self.endpoint.split("/") if arg]
        ep_args = [arg[1:] for arg in ep_parts if arg.startswith("!")]
        endpointargsstr = f", {', '.join([f'{arg}: string' for arg in ep_args])}" if ep_args else ""
        endpointformat = "\"/" + f"/".join(arg if not arg.startswith("!") else "{"+arg[1:]+"}" for arg in ep_parts) + "\""
        return (
            ((f"\n".join(self.response) + "\n") if self.response else "") +
            #f"@dataclass\n"
            f"interface {self.name} extends HttpReq<{self.type_ret}> " + "{\n" +
            "\n".join(line for line in self.inner if line) + (
            "\n" if self.type_ret.endswith("Response") or self.type_query or self.type_form else "") +
            #"\n".join([f"    {arg}: InitVar[str]" for arg in ep_args]) + ("\n" if ep_args else "") +
            (f"    query: {'|'.join(self.type_query)}?\n" if self.type_query else '') +
            (f"    form: {'|'.join(self.type_form)}?\n" if self.type_form else '') +
            f"\n"
            f"    method = Http.{self.type_req}\n"
            f"    endpoint"+(f" = {endpointformat}" if not ep_args else (": str = field(init=False)" + "\n\n"
            f"    def __post_init__(self{endpointargsstr}):\n"
            f"        self.endpoint = f{endpointformat}"
            )) + "\n\n"
            f"    def cast(self, data: Any):\n"
            f"        return "+(f"cast({self.type_ret}, data)" if self.type_ret != "None" else "None")
        )

@dataclass
class HttpParser(Parser):
    data: HttpReqData = field(init=False)
    complete: list[HttpReqData] = field(init=False, default_factory=list)
    
    def out(self, into: Parser):
        if into == Root:
            self.complete.append(self.data)

Http = Root.copyto(HttpParser)

pat_http = r"## (.+?) % ([A-Z]+) (/.+)"

@Root.hook(pat_http)
def create_httpreq_class(m: re.Match[str]):
    name, reqtype, endpoint = m.groups()
    if (
        ("Interaction" in name and not "Create" in name) or
        "Followup Message" in name or
        "Batch Edit" in name
    ):
        return "", Root
    name = do_steps(namify(name), {
        r"/": "Or",
        r"-": "",
    })
    endpoint = do_steps(endpoint, {
        r"{(\S+?)#.+?}": r"!\1",
        r"\.": "_",
    })
    Http.data = HttpReqData(name, reqtype, endpoint)
    return "", Http

@Http.hook(r"^(\w.+)")
def add_http_req_desc(m: re.Match[str]):
    desc, = m.groups()
    match = re.findall(r"Returns ([^\.]+)", desc)
    if match:
        Http.data.type_ret = unfuck_type(match[-1])
    match = re.findall(r"Body is ([^\.]+)", desc)
    if match:
        Http.data.type_form.append(unfuck_type(match[-1]))
    return ""

@Http.hook(r"^> (.+)")
def make_http_req_nullable(m: re.Match[str]):
    content, = m.groups()
    if re.match(r"All parameters to this endpoint are optional and nullable\.", content):
        Http.data.nullable = True
    return ""

@Http.hook(r"###### (Response) (?:Structure|Body)")
def create_http_response_disc(m: re.Match[str]):
    Http.data.type_ret = f"Response_{Http.data.name}"
    Http.data.response.append(f"@dataclass\nclass {Http.data.type_ret}(Disc):")
    return ""

@Http.hook(r"###### (.+?) Params(.*)")
def create_http_input_disc(m: re.Match[str]):
    name, subname = m.groups()
    if "Structure" in subname: return Root
    if subname:
        match = re.search(r"\((.+)\)", subname)
        if match:
            subname, = match.groups()
            subname = f"_{namify(subname)}"
    if re.search(r"JSON|Form", name):
        name = f"Form{subname}"
        Http.data.type_form.append(f"{Http.data.name}.{name}")
    elif re.search(r"Query", name):
        name = f"Query{subname}"
        Http.data.type_query.append(f"{Http.data.name}.{name}")
    Http.data.inner.append(f"    @dataclass\n    class {name}(Disc):")
    return ""

@Http.hook(pat_field)
def format_response_field(m: re.Match[str]):
    line = format_field(m)
    if line:
        if Http.data.nullable and not line.endswith(" | None = field(kw_only=True, default=None)"):
            line += " | None = field(kw_only=True, default=None)"
        if Http.data.response:
            Http.data.response.append(line)
        else:
            Http.data.inner.append(prepend_lines("    ", line))
    return ""

@Http.hook("###### Limitations")
def skip_limitations_exit(_):
    return ""

@Disc.hook(r"^#")
@Enums.hook(r"^#")
@Http.hook(r"^#")
def to_root(_):
    return Root

if __name__ == "__main__":

    inp: list[str] = []
    path_root = os.path.join("src/docparse/discord-api-docs", "docs")
    for folder in ["interactions", "resources"]:
        path_folder = os.path.join(path_root, folder)
        for file in os.listdir(path_folder):
            path_file = os.path.join(path_folder, file)
            with open(path_file, "r") as f:
                inp.append(f.read())
    path_topics_folder = os.path.join(path_root, "topics")
    for specific in ["OAuth2.md", "Permissions.md", "Teams.md"]:
        path_file = os.path.join(path_topics_folder, specific)
        with open(path_file, "r") as f:
            inp.append(f.read())
    newline = "\n"

    api = f"""
{newline.join([parse(Root, content) for content in inp])}

type InteractionData = ApplicationCommandData | MessageComponentData | ModalSubmitData
type InteractionCallbackData = InteractionCallbackMessage | InteractionCallbackAutocomplete | InteractionCallbackModal
type MessageComponent = ActionRow | Button | SelectMenu | TextInput
"""
    req = f"""
{(newline+newline).join([req.format() for req in Http.complete])}
"""

    req, api = [do_steps(content, {
        r"\bBitwisePermissionFlag\b": "Permission",
        r"\bInteractionCallbackMessage\b": "ResponseMessage",
        r"\bInteractionCallbackAutocomplete\b": "ResponseAutocomplete",
        r"\bInteractionCallbackModal\b": "ResponseModal",
    }) for content in [req, api]]
    with open("api.ts", "w") as f:
        f.write(api)
    with open("req.ts", "w") as f:
        f.write(req)