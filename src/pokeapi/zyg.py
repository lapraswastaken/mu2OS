
from __future__ import annotations

import dataclasses as dc
import json
import os
import re
import typing as t
from pprint import pprint
from time import perf_counter

import requests

from pokeapi import api

t_Getall = t.TypeVar("t_Getall", bound=api.HasEndpoint)
t_Any = t.TypeVar("t_Any")

def cast(data: t.Any, typ: type[t_Any]) -> t_Any:
    if typ in (int, str, bool):
        return data
    elif t.get_origin(typ) == list:
        castreplacements: list[t_Any] = []
        for subobject in data if data else []:
            castreplacements.append(cast(subobject, *t.get_args(typ)))
        return castreplacements # type: ignore
    else:
        if t.get_origin(typ):
            typ = t.get_origin(typ) # type: ignore
        assert issubclass(typ, api.APIType)
        return cast_dataclass(data, typ)

def cast_dataclass(data: dict, apitype: type[api.t_API]) -> api.t_API:
    if not data: return apitype()
    
    orig = t.get_origin(apitype)
    if orig: apitype = orig

    types = t.get_type_hints(apitype)
    newdata = {}
    
    for field in dc.fields(apitype):
        subdata = data[field.name]
        typ = types[field.name]
        newdata[field.name] = cast(subdata, typ)
        
    return apitype(**newdata)

def get(apitype: type[api.t_API], url: str, args: dict[str, str | int] | None=None) -> api.t_API:
    itemres = requests.get(url, args if args else {})
    data = json.loads(itemres.text)

    return cast_dataclass(data, apitype)

# def getall(endpoint: type[t_Getall]) -> list[t_Getall]:
#     arbitrarilyLargeNumber = 100000
#     resources: list[t_Getall] = []
#     listtyp = api.NamedAPIResourceList if issubclass(endpoint, api.HasName) else api.APIResourceList
#     got = get(listtyp, endpoint.endpoint, {"limit": arbitrarilyLargeNumber})
#     for item in got.results:
#         resource = _binch(lambda: get(endpoint, item.url), item.url, 1)
#         resources.append(resource)
#     return resources
    

t_Ret = t.TypeVar("t_Ret")
def _binch(call: t.Callable[..., t_Ret], name: str, tab: int) -> t_Ret:
    entab = tab * "  "
    print(f"{entab}Getting {name}... ", end="")
    tic = perf_counter()
    ret = call()
    toc = perf_counter()
    print(f"{entab}Got in {round(toc - tic, 2)}s")
    return ret

# def get_dex(apitype: type[t_Getall]):
#     dex = {}
#     if os.path.exists(f"dexes/{apitype.__name__}.json"):
#         return
#     for item in getall(apitype):
#         key = item.name if isinstance(item, api.HasName) else item.id
#         dex[key] = asdict(item)
#     with open(f"dexes/{apitype.__name__}.json", "w") as f:
#         json.dump(dex, f)

# def getall_dexes():
#     for apitype in api.HasEndpoint.__subclasses__():
#         if apitype == api.HasName: continue
#         _binch(lambda: get_dex(apitype), f"{apitype.__name__}.json", 0)
#     for apitype in api.HasName.__subclasses__():
#         _binch(lambda: get_dex(apitype), f"{apitype.__name__}.json", 0)

@dc.dataclass
class Dex(t.Generic[t_Getall]):

    apitype: type[t_Getall]
    data: dict[str, t_Getall] = dc.field(init=False)

    def __post_init__(self):
        with open(f"src/pokeapi/dexes/{self.apitype.__name__}.json", "r") as f:
            self.data = json.load(f)
            # for itemname in self.data:
            #     self.data[itemname] = cast_dataclass(self.data[itemname], self.apitype)

    def search_by_name(self, value: str):
        return cast(self.data.get(value), self.apitype)

pattern = re.compile(r'(?<!^)(?=[A-Z])')

def collect_subclasses(superclass: type[api.HasEndpoint]):
    dexes: dict[str, Dex] = {}
    for endpointclass in superclass.__subclasses__():
        if endpointclass.__subclasses__():
            dexes = {**dexes, **collect_subclasses(endpointclass)}
        else:
            dexes[re.sub(pattern, "_", endpointclass.__name__).lower()] = Dex(endpointclass)
    return dexes

dexes = collect_subclasses(api.HasName)

def get_dex_for(cls: type[t_Getall]) -> Dex[t_Getall]:
    return dexes[cls.__name__.lower()]
