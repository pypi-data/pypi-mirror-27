
PHADDW = {
    "mmmm": {"mod": "/r", "opcode": "0F3801"},
    "mmmem64": {"mod": "/r", "opcode": "0F3801"},
    "xmmxmm": {"mod": "/r", "opcode": "660F3801"},
    "xmmmem128": {"mod": "/r", "opcode": "660F3801"},
}

PHADDSW = {
    "mmmm": {"mod": "/r", "opcode": "0F3803"},
    "mmmem64": {"mod": "/r", "opcode": "0F3803"},
    "xmmxmm": {"mod": "/r", "opcode": "660F3803"},
    "xmmmem128": {"mod": "/r", "opcode": "660F3803"},
}

PHADDD = {
    "mmmm": {"mod": "/r", "opcode": "0F3802"},
    "mmmem64": {"mod": "/r", "opcode": "0F3802"},
    "xmmxmm": {"mod": "/r", "opcode": "660F3802"},
    "xmmmem128": {"mod": "/r", "opcode": "660F3802"},
}

PHSUBW = {
    "mmmm": {"mod": "/r", "opcode": "0F3805"},
    "mmmem64": {"mod": "/r", "opcode": "0F3805"},
    "xmmxmm": {"mod": "/r", "opcode": "660F3805"},
    "xmmmem128": {"mod": "/r", "opcode": "660F3805"},
}

PHSUBSW = {
    "mmmm": {"mod": "/r", "opcode": "0F3807"},
    "mmmem64": {"mod": "/r", "opcode": "0F3807"},
    "xmmxmm": {"mod": "/r", "opcode": "660F3807"},
    "xmmmem128": {"mod": "/r", "opcode": "660F3807"},
}

PHSUBD = {
    "mmmm": {"mod": "/r", "opcode": "0F3806"},
    "mmmem64": {"mod": "/r", "opcode": "0F3806"},
    "xmmxmm": {"mod": "/r", "opcode": "660F3806"},
    "xmmmem128": {"mod": "/r", "opcode": "660F3806"},
}

PABSB = {
    "mmmm": {"mod": "/r", "opcode": "0F381C"},
    "mmmem64": {"mod": "/r", "opcode": "0F381C"},
    "xmmxmm": {"mod": "/r", "opcode": "660F381C"},
    "xmmmem128": {"mod": "/r", "opcode": "660F381C"},
}

PABSW = {
    "mmmm": {"mod": "/r", "opcode": "0F381D"},
    "mmmem64": {"mod": "/r", "opcode": "0F381D"},
    "xmmxmm": {"mod": "/r", "opcode": "660F381D"},
    "xmmmem128": {"mod": "/r", "opcode": "660F381D"},
}

PABSD = {
    "mmmm": {"mod": "/r", "opcode": "0F381E"},
    "mmmem64": {"mod": "/r", "opcode": "0F381E"},
    "xmmxmm": {"mod": "/r", "opcode": "660F381E"},
    "xmmmem128": {"mod": "/r", "opcode": "660F381E"},
}

PMADDUBSW = {
    "mmmm": {"mod": "/r", "opcode": "0F3804"},
    "mmmem64": {"mod": "/r", "opcode": "0F3804"},
    "xmmxmm": {"mod": "/r", "opcode": "660F3804"},
    "xmmmem128": {"mod": "/r", "opcode": "660F3804"},
}

PMULHRSW = {
    "mmmm": {"mod": "/r", "opcode": "0F380B"},
    "mmmem64": {"mod": "/r", "opcode": "0F380B"},
    "xmmxmm": {"mod": "/r", "opcode": "660F380B"},
    "xmmmem128": {"mod": "/r", "opcode": "660F380B"},
}

PSHUFB = {
    "mmmm": {"mod": "/r", "opcode": "0F3800"},
    "mmmem64": {"mod": "/r", "opcode": "0F3800"},
    "xmmxmm": {"mod": "/r", "opcode": "660F3800"},
    "xmmmem128": {"mod": "/r", "opcode": "660F3800"},
}

PSIGNB = {
    "mmmm": {"mod": "/r", "opcode": "0F3808"},
    "mmmem64": {"mod": "/r", "opcode": "0F3808"},
    "xmmxmm": {"mod": "/r", "opcode": "660F3808"},
    "xmmmem128": {"mod": "/r", "opcode": "660F3808"},
}

PSIGNW = {
    "mmmm": {"mod": "/r", "opcode": "0F3809"},
    "mmmem64": {"mod": "/r", "opcode": "0F3809"},
    "xmmxmm": {"mod": "/r", "opcode": "660F3809"},
    "xmmmem128": {"mod": "/r", "opcode": "660F3809"},
}

PSIGND = {
    "mmmm": {"mod": "/r", "opcode": "0F380A"},
    "mmmem64": {"mod": "/r", "opcode": "0F380A"},
    "xmmxmm": {"mod": "/r", "opcode": "660F380A"},
    "xmmmem128": {"mod": "/r", "opcode": "660F380A"},
}

PALIGNR = {
    "mmmmimm8": {"mod": "/r", "opcode": "0F3A0F", "imm": "ib"},
    "mmmem64imm8": {"mod": "/r", "opcode": "0F3A0F", "imm": "ib"},
    "xmmxmmimm8": {"mod": "/r", "opcode": "660F3A0F", "imm": "ib"},
    "xmmmem128imm8": {"mod": "/r", "opcode": "660F3A0F", "imm": "ib"},
}
