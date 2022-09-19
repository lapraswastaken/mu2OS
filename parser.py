
from abc import abstractmethod
from dataclasses import InitVar, dataclass, field
import re
from typing import Any, Callable, Concatenate, Generic, Mapping, ParamSpec, Protocol, TypeVar, overload
from typing_extensions import TypeVarTuple, Unpack

ta_Steps = Mapping[str, str | Callable[[re.Match[str]], str]]
def do_steps(inp: str, steps: ta_Steps):
    for regex, replacer in steps.items():
        inp = re.sub(regex, replacer, inp)
    return inp

"""
What I want

To be able to parse documentation markdown files
    Take a chunk from a file with regex
    If regex got a chunk, try to match the chunk against a list of regexes
    If a regex in the chunk matches, use an a function associated with that regex to do something to the chunk and continue matching
    Add the processed chunk to a list
    Try to take a chunk again
    If regex didn't get a chunk, join the list and make a file
"""

t_ParserHookRet = TypeVar("t_ParserHookRet", str, "Parser", "tuple[str, Parser]", "str | tuple[str, Parser] | Parser")
ta_ParserHookCallback = Callable[[re.Match[str]], t_ParserHookRet]

@dataclass
class Parser:
    """ Uses a ``chunker`` (a regex to split a string by) to take a
        chunk from a string and passes that chunk to its ``hooks``.
        """

    match_chunk: InitVar[str]
    chunker: re.Pattern[str] = field(init=False)
    hooks: dict[re.Pattern[str], ta_ParserHookCallback] = field(default_factory=dict, init=False)

    def __post_init__(self, match_chunk: str):
        self.chunker = re.compile(match_chunk)
    
    def copy(self):
        return self.__class__(self.chunker.pattern)
    
    t_Parser = TypeVar("t_Parser", bound="Parser")
    def copyto(self, intocls: type[t_Parser]) -> t_Parser:
        return intocls(self.chunker.pattern)

    def hook(self, parse_chunk: str):
        def _(callback: ta_ParserHookCallback[t_ParserHookRet]) -> ta_ParserHookCallback[t_ParserHookRet]:
            self.hooks[re.compile(parse_chunk)] = callback
            return callback
        return _
    
    def do(self, s: str):
        """ Takes a string and takes a chunk from it. That chunk is
            passed to each of its hooks successively.
            
            Returns a processed chunk, the remaining text in the
            string, and a new ``Parser`` if one exists else ``None``.
            
            If a hook returns a string, make that string the chunk
            to pass to subsequent hooks and continue through the
            loop.
            
            If a hook returns a string and a ``Parser``, return and
            pass the new ``Parser`` instead of ``None``.
            
            If a hook returns a ``Parser``, return an empty string
            as the processed chunk, then the entire string that was
            passed into this function, then the new ``Parser``
            instead of ``None``.
            """

        chunk, rest = self.chunker.split(s, maxsplit=1)
        changed = chunk
        for hook_pat in self.hooks:
            hook_match = hook_pat.search(changed)
            if not hook_match: continue

            res = self.hooks[hook_pat](hook_match)
            if isinstance(res, str):
                changed = res
            elif isinstance(res, Parser):
                return "", s, res
            else:
                return res[0], rest, res[1]
        if not changed == chunk:
            return changed, rest, None
        return "", rest, None
    
    def out(self, into: "Parser") -> str | None:
        return None

def parse(parser: Parser, s: str):
    original_parser = parser
    chunks: list[str] = []
    while s:
        chunk, s, new_parser = parser.do(s)
        if chunk:
            chunks.append(chunk)
        if new_parser:
            out = parser.out(new_parser)
            if out is not None: chunks.append(out)
            parser = new_parser
    out = parser.out(original_parser)
    if out is not None: chunks.append(out)
    return "\n".join(chunks)
