
from docparse.parser import do_steps

apitype_classname = r"APIType"
hasendpoint_classname = r"HasEndpoint"
hasname_classname = r"HasName"
apitypevar_name = r"t_API"

endpoint_regexflag = r"!ENDPOINT "
doc_regexflag = r"!DOC "

steps = {
    # clear out JSON examples; prepare endpoint urls
    r"GET (.+){[\w\W]+?View raw JSON.+":
        endpoint_regexflag+r"\1",
    # clear out groupings
    r".+ \(group\)":
        r"",
    # create divider for Common Models
    r"Common Models":
        r"#\n"+
        r"# Common Models\n"+
        r"#\n",
    # prepare endpoint class docstrings
    r".+ \(endpoint\)\n\n(.+)\n":
        doc_regexflag+r"\1",
    # create a class for each type and clear type infotable headers
    r"(.+) \(type\)\nName\tDescription\tType\n":
        r"class \1("+apitype_classname+r"):\n",
    # insert endpoint url and docstring into endpoint classes
    doc_regexflag+r"(.+)\n"+endpoint_regexflag+r"(.+)\nclass (.+)\("+apitype_classname+r"\):":
        r'class \3('+hasendpoint_classname+r'):\n'+
        r'    """ \1 """\n'+
        r'\n'+
        r'    endpoint: ClassVar[str] = "\2"\n',
    # special case for APIResource
    r"class APIResource\("+apitype_classname+r"\):":
        apitypevar_name+r' = TypeVar("'+apitypevar_name+r'", bound='+apitype_classname+r')\n'+
        r"class APIResource("+apitype_classname+r", Generic["+apitypevar_name+r"]):",
    # special case for NamedAPIResource
    r"class NamedAPIResource\("+apitype_classname+r"\):":
        r"class NamedAPIResource(APIResource["+apitypevar_name+r"]):",
    # prepend dataclass to all classes
    r"class (.+):":
        r"@dataclass\n"+
        r"class \1:",
    # preformat each field
    r"(\w+)\t\n\s+(.+)\n\s+(.+)":
        r"    # \2\n"+
        r"    \1: \3\n",
    # format APIResource subtypes
    r"(Named)?APIResource \((\w+)\)":
        r"\1APIResource[\2]",
    # clean up other subtype things
    r" \((.+)\)":
        r"",
    # format list subtypes
    r": list (.+)":
        r": list[\1]",
    # replace types with python types
    r"integer":
        r"int",
    r"string":
        r"str",
    r"boolean":
        r"bool",
    r"class (\w+)\(HasEndpoint\):(\n.+\n\n.+\n\n.+\n.+\n\n.+\n    name:)":
        r"class \1(HasName):\2",
}

if __name__ == "__main__":
    with open("docs_pokeapi.txt", "r") as f:
        inp = f.read()

    with open("pokeapi/api.py", "w") as f:
        f.write(f"""

from __future__ import annotations

from dataclasses import dataclass
from typing import ClassVar, Generic, TypeVar

from pokeapi.typ import APIType, HasEndpoint, HasName
{do_steps(inp, steps)} """)
