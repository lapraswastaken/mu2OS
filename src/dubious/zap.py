
from __future__ import annotations
import dataclasses as dc
from pprint import pprint
import re
import typing as t

eval_name = re.compile(r"\w")

ta_MatchResults = dict[str, "str | list[str] | ta_MatchResults"]
ta_Process = t.Callable[[str, "Trick"], ta_MatchResults]
ta_Instructions = dict[str, list[ta_Process]]

@dc.dataclass
class Step:
    name: str | None = None
    ops: list[str] = dc.field(default_factory=list)
    opname: str | None = None
    inner: str = ""
    nest: int = 0
    done: bool = False

@dc.dataclass
class Trick:
    template: str
    instructions: ta_Instructions = dc.field(default_factory=dict)
    pattern: str = dc.field(init=False, default="")

    def __post_init__(self):
        print(f"trick: {self.template}")
        step = Step()
        for char in self.template:
            print(char)
            match char, step:
                case "$", Step(name=None):
                    print("var start")
                    step.name = ""
                case _, Step(name=None):
                    print("adding to pattern")
                    self.pattern += char
                case _, Step(name=str(some), opname=None, nest=0) if re.match(r"\w", char):
                    print("adding to var name")
                    step.name = some + char
                case ".", Step(name=str(_), opname=None, nest=0):
                    print("op start")
                    step.opname = ""
                case _, Step(name=str(some), opname=None, nest=0) if not re.match(r"\w", char):
                    print("var end")
                    self.create_group(some, [])
                    step.name = None
                case _, Step(name=str(_), opname=str(some), nest=0) if re.match(r"\w", char):
                    print("adding to op")
                    step.opname = some + char
                case "{", Step(name=str(_), opname=str(some), nest=0):
                    print("up nest (new op)")
                    step.ops.append(some)
                    step.opname = None
                    step.nest += 1
                case "{", Step(name=str(_), nest=int(some)) if some > 0:
                    print("up nest")
                    step.nest += 1
                case "}", Step(name=str(name), nest=int(some)) if some > 0:
                    print("down nest")
                    step.nest -= 1
                    if step.nest == 0:
                        self.create_group(name, [op_by_char[opname] for opname in step.ops], step.inner)
                        step.name = None
                case _, Step(name=str(_), nest=int(some)) if some > 0:
                    print("adding to inner")
                    step.inner += char
                case _:
                    raise Exception()
        print(f"trick [[{self.pattern}]] done")

    def create_group(self, name: str, instructions: list[ta_Process], inner: str=""):
        self.pattern += r"(?P<"+name+r">[\w\W]+?)"
        self.instructions[name] = Trick(inner, instructions) if inner else instructions

    def match(self, on: str):
        match = re.match(self.pattern, on)
        if not match: return
        groups = match.groupdict()
        results: ta_MatchResults = {}
        for group in groups:
            inner = self.instructions[group]
            got = groups[group]
            if not inner:
                results[group] = got
            else:
                results[group] = inner.match(got)

if __name__ == "__main__":
    trick = Trick(r"Query: `$query_tokens.sep{, }`")
    pprint(trick)
    print(trick.match("Query: `1, 2, 3, 4`"))
    #trick = Trick(r"$allowed_users?.sep{, }.srnd{<@{}>}|.lit{Anyone} can use this query.")
