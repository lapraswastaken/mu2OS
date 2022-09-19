
from dataclasses import dataclass, fields
from typing import ClassVar, get_type_hints

@dataclass
class APIType:

    @classmethod
    def names_for_fields(cls):
        return [field.name for field in fields(cls)]
    
    @classmethod
    def type_for_field(cls, name: str) -> type:
        for field in fields(cls):
            if field.name == name:
                return get_type_hints(cls)[field.name]
        raise KeyError()

@dataclass
class HasEndpoint(APIType):
    endpoint: ClassVar[str]
    id: int

@dataclass
class HasName(HasEndpoint):
    name: str