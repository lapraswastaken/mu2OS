
from pprint import pprint
import re
import datetime as dt
import dataclasses as dc
import typing as t

import dubious.pory as pory
import dubious.callback as cb
from dubious.discord import api, req

from pokeapi import api as pkapi, zyg

import mu2OS.discordsecrets as discordsecrets

header_prepend_title = r"Query: `\query_tokens([, ])`"
header_allowed_anyone = "Anyone"
header_append_allowed = r"\allowed_users(Anyone?[]|[<@\_>, ]) can use this query."
header_allowed_join = ", "
header_footer = "Use the buttons below to add to this query."

dexes_prev = "dexes_prev"
dexes_prev_label = "<"
dexes_next = "dexes_next"
dexes_next_label = ">"

add = "add_"

rm = "rm"
rm_label = "Delete last token"

@dc.dataclass
class Query:
    tokens: list[str]
    timestamp: dt.datetime
    allowed_users: set[api.Snowflake] | t.Literal[True] = dc.field(default_factory=set)
    dex_index: int = 0

    @classmethod
    def from_message(cls, message: api.Message):
        if not message.embeds: return
        header = message.embeds[0]
        if not header.title: return
        if not header.title.startswith(header_prepend_title): return
        if not header.description: return
        if not header.description.endswith(header_append_allowed): return
        if not header.footer: return
        if not header.footer.text == header_footer: return
        q = cls(
            (
                header
                    .title[len(header_prepend_title):]
                    .strip("`")
                    .split()
            ),
            dt.datetime.fromisoformat(message.timestamp),
            set(
                api.Snowflake(user_id.strip("<>@")) for user_id in
                    header
                        .description[:-len(header_append_allowed)]
                        .split(header_allowed_join)
            ) if header.description[:-len(header_append_allowed)] != header_allowed_anyone else True,
            cls.get_dex_index(message),
        )
        return q
    
    @classmethod
    def get_dex_index(cls, message: api.Message):
        for row in message.components if message.components else []:
            assert isinstance(row, api.ActionRow)
            if isinstance(row.components[0], api.Button):
                btn = row.components[0]
                if not btn.custom_id == dexes_prev: continue
                assert btn.label
                if not btn.label.startswith(dexes_prev_label): continue

        return 0

    def add_token(self, text: str):
        self.tokens.append(text)
    def remove_token(self):
        self.tokens.pop()

    def add_user(self, user_id: api.Snowflake):
        if self.allowed_users is True: return
        self.allowed_users.add(user_id)

    def can_inc_dex(self):
        return self.dex_index < len(zyg.dexes) - 3
    def inc_dex(self):
        if self.can_inc_dex():
            self.dex_index += 1

    def can_dec_dex(self):
        return self.dex_index > 0
    def dec_dex(self):
        if self.can_dec_dex:
            self.dex_index -= 1
    
    def collect(self):
        return {
            "embeds": [self.header_embed()],
            "components": self.parse()
        }

    def header_embed(self):
        return api.Embed(
            title = f"{header_prepend_title}" + (f" `{' '.join(self.tokens)}`" if self.tokens else ""),
            description = (
                header_allowed_join.join(
                    f"<@{user_id}>" for user_id in self.allowed_users
                ) if self.allowed_users !=  True else header_allowed_anyone
            ) + header_append_allowed,
            footer = api.EmbedFooter(header_footer)
        )

    def parse(self):
        rows: list[api.ActionRow] = []
        if not self.tokens:
            rows += [self.collect_dexes()]
        for token in self.tokens:
            rows += self.parse_token(token)
        rows += [api.ActionRow([
            api.Button(api.ButtonStyle.DANGER, label=rm_label, custom_id=rm, disabled=not bool(self.tokens))
        ])]
        return rows

    def parse_token(self, token: str):
        match token:
            case _: pass    
        return []

    def collect_dexes(self):
        return api.ActionRow([
            api.Button(api.ButtonStyle.SECONDARY, label=dexes_prev_label, custom_id=dexes_prev, disabled=not self.can_dec_dex()),
            *[
                api.Button(api.ButtonStyle.PRIMARY, label=dexname.replace("_", " ").title(), custom_id=f"{add}{dexname}")
                    for dexname in list(zyg.dexes.keys())[self.dex_index:self.dex_index+3]
            ],
            api.Button(api.ButtonStyle.SECONDARY, label=dexes_next_label, custom_id=dexes_next, disabled=not self.can_inc_dex()),
        ])

@dc.dataclass
class QueriedPory(pory.Pory):
    def get_latest_query(self, channel_id: api.Snowflake, as_user: api.Snowflake):
        for message in self.history(channel_id, limit=25):
            if message.author.id == self.id:
                print(f"matched IDs")
                q = Query.from_message(message)
                if q:
                    return q, message.id
        q = Query([], dt.datetime.now(), {as_user})
        message = self.send(channel_id, req.CreateMessage.Form(**q.collect()))
        return q, message.id

    def get_callback_for_component(self, component_id: str):
        match component_id.split("_", 1):
            case "add", rest:
                return self.create_query_callback(Query.add_token, rest)
            case "next", "dexes":
                return self.create_query_callback(Query.inc_dex)
            case "prev", "dexes":
                return self.create_query_callback(Query.dec_dex)
            case "rm",:
                return self.create_query_callback(Query.remove_token)
        return super().get_callback_for_component(component_id)

    def create_query_callback(self, do: t.Callable[t.Concatenate[Query, cb.ps_CallbackArgs], cb.t_CommandRet], *args: cb.ps_CallbackArgs.args, **kwargs: cb.ps_CallbackArgs.kwargs):
        def callback(*, channel_id: api.Snowflake, message: api.Message | None, user: api.User):
            if message:
                q, message_id = Query.from_message(message), message.id
                if not q: raise Exception()
            else:
                q, message_id = self.get_latest_query(channel_id, user.id)
            if (q.allowed_users is True) or (user.id in q.allowed_users):
                do(q, *args, **kwargs)
                self.edit(channel_id, message_id, req.EditMessage.Form(**q.collect()))
        return cb.Callback("", callback)

Pory = QueriedPory(
    discordsecrets.DISCORD_CLIENT_ID,
    discordsecrets.DISCORD_PUBLIC_KEY,
    discordsecrets.DISCORD_USER_TOKEN
)

@Pory.on_command
def query(query_input: str="", *, ixn: api.Interaction):
    yield api.ResponseMessage(content="Hold on...", flags=api.MessageFlag.EPHEMERAL)
    callback = Pory.create_query_callback(Query.add_token, query_input)
    callback.do(ixn, ixn.data)
    return api.ResponseMessage(content="Done.", flags=api.MessageFlag.EPHEMERAL)

@Pory.on_command
def ping():
    """ Responds with "Pong!" """
    return api.ResponseMessage(
        content="Pong!"
    )

@Pory.on_command(perms=[api.Permission.MANAGE_MESSAGES])
def ping_special():
    """ Responds with "Pong!" Only usable by members with the Manage Messages permission. """
    return api.ResponseMessage(
        content="Pong!"
    )

scene = Pory.on_command.group("scene", "Adds a scene separator to a finished/paused scene.")

str_break = "<><><><><><><><>"
str_pause = "(Scene paused)"
str_unpause = "(Scene unpaused)"

@scene(name="break")
def _(*, id: api.Snowflake, token: str, channel_id: api.Snowflake):
    """ Adds a scene break. """
    return separator(str_break, (str_break, str_pause, str_unpause), id, token, channel_id)

@scene
def pause(*, id: api.Snowflake, token: str, channel_id: api.Snowflake):
    """ Pauses a scene. The scene can be continued later with `unpause`. """
    return separator(str_pause, (str_break,), id, token, channel_id)

@scene
def unpause(*, id: api.Snowflake, token: str, channel_id: api.Snowflake):
    """ Unpauses the most recently paused scene. If used immediately after a pause, deletes that pause. """
    for hist in Pory.history(channel_id, limit=2) if channel_id else []:
        if re.search(str_pause, hist.content):
            Pory.delete(hist.channel_id, hist.id)
            Pory.delete_response(Pory.id, token)
            return
    return separator(str_unpause, (str_pause,), id, token, channel_id)

def separator(content: str, patterns: t.Collection[str], ixn_id: api.Snowflake, token: str, channel_id: api.Snowflake):

    response, lock = Pory.create_cancel_button(ixn_id, token, "Finding last separator...", "Stop")

    yield response

    if not channel_id: return

    last: api.Message | None = None

    limit = 3000

    for hist in Pory.history(channel_id, limit=limit):
        if lock.is_set():
            break
        if any(re.search(pat, hist.content) for pat in patterns):
            last = hist
            break

    if not last:
        status = f"Couldn't find a separator in the last {limit} messages" if not lock.is_set() else "Cancelled"
        Pory.send_response(token, req.ExecuteWebhook.Form(
            content=f"{status}. Creating a new separator without a link.",
            flags=api.MessageFlag.EPHEMERAL
        ))

    Pory.send(channel_id, req.CreateMessage.Form(
        content=content,
        message_reference=api.MessageReference(
            message_id=last.id,
            fail_if_not_exists=False,
        ) if last else None
    ))

    if not lock.is_set():
        Pory.delete_response(token)

if __name__ == "__main__":
    app = Pory.flask()
    app.run()
