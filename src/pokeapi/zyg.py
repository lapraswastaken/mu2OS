
from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field, fields, make_dataclass
import os
import re
from time import perf_counter
from typing import Any, Callable, Generic, TypeVar, get_args, get_origin, get_type_hints

import requests

from pokeapi import api

t_Getall = TypeVar("t_Getall", bound=api.HasEndpoint)

def cast(data: Any, typ: type):
    if typ in (int, str, bool):
        return data
    elif get_origin(typ) == list:
        castreplacements = []
        for subobject in data if data else []:
            castreplacements.append(cast(subobject, *get_args(typ)))
        return castreplacements
    else:
        return cast_dataclass(data, typ)

def cast_dataclass(data: dict, apitype: type[api.t_API]) -> api.t_API:
    if not data: return apitype()
    
    orig = get_origin(apitype)
    if orig: apitype = orig

    types = get_type_hints(apitype)
    newdata = {}
    
    for field in fields(apitype):
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
    

t_Ret = TypeVar("t_Ret")
def _binch(call: Callable[..., t_Ret], name: str, tab: int) -> t_Ret:
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

@dataclass
class Dex(Generic[t_Getall]):

    apitype: type[t_Getall]
    data: dict[str, t_Getall] = field(init=False)

    def __post_init__(self):
        with open(f"dexes/{self.apitype.__name__}.json", "r") as f:
            self.data = json.load(f)
            # for itemname in self.data:
            #     self.data[itemname] = cast_dataclass(self.data[itemname], self.apitype)

pattern = re.compile(r'(?<!^)(?=[A-Z])')

def collect_subclasses(superclass: type[api.HasEndpoint]):
    dexes: dict[str, type[api.HasEndpoint]] = {}
    for endpointclass in superclass.__subclasses__():
        if endpointclass.__subclasses__():
            dexes = {**dexes, **collect_subclasses(endpointclass)}
        else:
            dexes[re.sub(pattern, "_", endpointclass.__name__).lower()] = endpointclass
    return dexes

Dexes: type[api.HasEndpoint] = make_dataclass("Dexes", [
    (key, val) for key, val in collect_subclasses(api.HasEndpoint).items()
], bases=(api.HasEndpoint,)) # type: ignore
