
from __future__ import annotations

import abc
import dataclasses as dc
import enum
import math
import time
import types
import typing as t

from requests import request


class Snowflake(str):
    def __init__(self, r: str|int):
        self.id = int(r) if isinstance(r, str) else r
        self.timestamp = (self.id >> 22) + 1420070400000
        self.workerID = (self.id & 0x3E0000) >> 17
        self.processID = (self.id & 0x1F000) >> 12
        self.increment = self.id & 0xFFF

    def __repr__(self):
        return str(self.id)

    def __str__(self) -> str:
        return repr(self)

    def __hash__(self):
        return self.id

    def __eq__(self, o: object) -> bool:
        if not isinstance(o, self.__class__):
            try:
                return int(o) == self.id # type: ignore
            except TypeError:
                return False
        return o.id == self.id

    def __ne__(self, o: object) -> bool:
        return not self == o

@dc.dataclass
class Disc:
    """ Root class for all Discord objects. """

t_Cast = t.TypeVar("t_Cast")
def cast(t_to: type[t_Cast], raw: t.Any, debug: t.Callable[..., None] = lambda *_, **__: None) -> t_Cast:
    debug(t_to)
    debug(raw)
    if raw is None: return raw
    if dc.is_dataclass(raw): raw = dc.asdict(raw)

    t_root = t.get_origin(t_to)

    if t_root:
        if issubclass(t_root, list):
            t_list, *_ = t.get_args(t_to)
            return [
                cast(t_list, rawitem) for rawitem in raw
            ] # type: ignore
        elif issubclass(t_root, dict):
            t_key, t_val, *_ = t.get_args(t_to)
            return {
                cast(t_key, key): cast(t_val, val)
                    for key, val in raw.items()
            } # type: ignore
        elif issubclass(t_root, types.UnionType):
            t_optionals = [
                t for t in t.get_args(t_to)
                    if t != type(None)
            ]
            best_score = 0
            best_len = math.inf
            best_opt = None
            for t_opt in t_optionals:
                if dc.is_dataclass(t_opt):
                    fields = [field.name for field in dc.fields(t_opt)]
                    score = sum(name in fields for name in raw)
                    if (
                        score > best_score or (
                            score == best_score and 
                            len(fields) < best_len
                        )
                    ):
                        best_score = score
                        best_len = len(fields)
                        best_opt = t_opt
                else:
                    try:
                        return cast(t_opt, raw)
                    except ValueError:
                        continue
            return cast(best_opt, raw) #type: ignore

    if issubclass(t_to, Disc):
        fixedraw = {}

        fieldtypes: dict[str, type] = t.get_type_hints(t_to)
        fixedraw = {
            field.name: cast(
                fieldtypes[field.name], raw[field.name] if field.name in raw else None
            ) for field in dc.fields(t_to)
        }
        return t_to(**fixedraw)
    else:
        try:
            return t_to(raw)
        except ValueError:
            return raw

ROOT = "https://discord.com/api"

class Http(str, enum.Enum):
    GET = "GET"
    PUT = "PUT"
    PATCH = "PATCH"
    POST = "POST"
    DELETE = "DELETE"

t_Ret = t.TypeVar("t_Ret")
class HttpReq(abc.ABC, t.Generic[t_Ret]):
    query: Disc | None = None
    form: Disc | None = None

    method: Http
    endpoint: str

    @abc.abstractmethod
    def cast(self, data: t.Any) -> t_Ret:
        ...

    def do_with(self, token: str) -> t_Ret:
        res = request(self.method, ROOT + self.endpoint,
            headers={
                "Authorization": f"Bot {token}"
            },
            params=dc.asdict(self.query) if self.query else None,
            json=dc.asdict(self.form) if self.form else None
        )
        if not res.status_code in range(200, 300):
            error = res.json()
            if error.get("retry_after"):
                print(f"rate limited, waiting {error['retry_after']/1000} seconds")
                time.sleep(error["retry_after"]/1000)
                return self.do_with(token)
            raise Exception(f"{res.status_code}: {str(error)}")
        return self.cast(res.json() if res.text else None)
