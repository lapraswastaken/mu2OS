
from __future__ import annotations
from abc import ABC, abstractmethod

import dataclasses as dc
import re
from time import sleep
from types import UnionType
from typing import Any, Generic, TypeVar, ClassVar, get_args, get_origin, get_type_hints
from enum import Enum
from typing_extensions import TypeVarTuple

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

t_Cast = TypeVar("t_Cast")
def cast(t_to: type[t_Cast], raw: Any) -> t_Cast:
    if raw is None: return raw

    t_root = get_origin(t_to)

    if t_root:
        if issubclass(t_root, list):
            t_list, *_ = get_args(t_to)
            return [
                cast(t_list, rawitem) for rawitem in raw
            ] # type: ignore
        elif issubclass(t_root, dict):
            t_key, t_val, *_ = get_args(t_to)
            return {
                cast(t_key, key): cast(t_val, val)
                    for key, val in raw.items()
            } # type: ignore
        elif issubclass(t_root, UnionType):
            t_optionals = [
                t for t in get_args(t_to)
                    if t != type(None)
            ]
            for t_opt in t_optionals:
                try:
                    return cast(t_opt, raw)
                except ValueError:
                    continue
            raise ValueError()

    if issubclass(t_to, Disc):
        fixedraw = {}

        fieldtypes: dict[str, type] = get_type_hints(t_to)
        fixedraw = {
            field.name: cast(
                fieldtypes[field.name], raw[field.name] if field.name in raw else None
            ) for field in dc.fields(t_to)
        }
        return t_to(**fixedraw)
    else:
        return raw

class Http(str, Enum):
    GET = "GET"
    PUT = "PUT"
    PATCH = "PATCH"
    POST = "POST"
    DELETE = "DELETE"

ROOT = "https://discord.com/api"

t_Ret = TypeVar("t_Ret")
class HttpReq(ABC, Generic[t_Ret]):
    query: Disc | None = None
    form: Disc | None = None

    method: Http
    endpoint: str

    @abstractmethod
    def cast(self, data: Any) -> t_Ret:
        ...

    def do_with(self, token: str) -> t_Ret:
        res = request(self.method, ROOT + self.endpoint,
            headers={
                "Authorization": f"Bearer {token}"
            },
            params=dc.asdict(self.query) if self.query else None,
            json=dc.asdict(self.form) if self.form else None
        )
        if not res.status_code in range(200, 300):
            error = res.json()
            if error.get("retry_after"):
                sleep(error["retry_after"])
                return self.do_with(token)
            raise Exception(str(error))
        return self.cast(res.json() if res.text else None)