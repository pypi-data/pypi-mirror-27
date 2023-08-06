
FISTTP = {
    "mem16": {"mod": "/1", "opcode": "DF"},
    "mem32": {"mod": "/1", "opcode": "DB"},
    "mem64": {"mod": "/1", "opcode": "DD"},
}

LDDQU = {
    "xmmmem128": {"mod": "/r", "opcode": "F20FF0"},
}

ADDSUBPS = {
    "xmmxmm": {"mod": "/r", "opcode": "F20FD0"},
    "xmmmem128": {"mod": "/r", "opcode": "F20FD0"},
}

ADDSUBPD = {
    "xmmxmm": {"mod": "/r", "opcode": "660FD0"},
    "xmmmem128": {"mod": "/r", "opcode": "660FD0"},
}

HADDPS = {
    "xmmxmm": {"mod": "/r", "opcode": "F20F7C"},
    "xmmmem128": {"mod": "/r", "opcode": "F20F7C"},
}

HSUBPS = {
    "xmmxmm": {"mod": "/r", "opcode": "F20F7D"},
    "xmmmem128": {"mod": "/r", "opcode": "F20F7D"},
}

HADDPD = {
    "xmmxmm": {"mod": "/r", "opcode": "660F7C"},
    "xmmmem128": {"mod": "/r", "opcode": "660F7C"},
}

HSUBPD = {
    "xmmxmm": {"mod": "/r", "opcode": "660F7D"},
    "xmmmem128": {"mod": "/r", "opcode": "660F7D"},
}

MOVSLDUP = {
    "xmmxmm": {"mod": "/r", "opcode": "F30F12"},
    "xmmmem128": {"mod": "/r", "opcode": "F30F12"},
}

MOVSHDUP = {
    "xmmxmm": {"mod": "/r", "opcode": "F30F16"},
    "xmmmem128": {"mod": "/r", "opcode": "F30F16"},
}

MOVDDUP = {
    "xmmxmm": {"mod": "/r", "opcode": "F20F12"},
    "xmmmem64": {"mod": "/r", "opcode": "F20F12"},
}

MONITOR = {"no_op": {"opcode": "0F01C8"}}
MWAIT = {"no_op": {"opcode": "0F01C9"}}
