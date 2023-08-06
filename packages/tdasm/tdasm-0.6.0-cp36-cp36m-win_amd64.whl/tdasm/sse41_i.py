

PMULLD = {
    "xmmxmm": {"mod": "/r", "opcode": "660F3840"},
    "xmmmem128": {"mod": "/r", "opcode": "660F3840"},
}

PMULDQ = {
    "xmmxmm": {"mod": "/r", "opcode": "660F3828"},
    "xmmmem128": {"mod": "/r", "opcode": "660F3828"},
}

DPPD = {
    "xmmxmmimm8": {"mod": "/r", "opcode": "660F3A41", "imm": "ib"},
    "xmmmem128imm8": {"mod": "/r", "opcode": "660F3A41", "imm": "ib"},
}

DPPS = {
    "xmmxmmimm8": {"mod": "/r", "opcode": "660F3A40", "imm": "ib"},
    "xmmmem128imm8": {"mod": "/r", "opcode": "660F3A40", "imm": "ib"},
}

MOVNTDQA = {"xmmmem128": {"mod": "/r", "opcode": "660F382A"}}

BLENDPD = {
    "xmmxmmimm8": {"mod": "/r", "opcode": "660F3A0D", "imm": "ib"},
    "xmmmem128imm8": {"mod": "/r", "opcode": "660F3A0D", "imm": "ib"},
}

BLENDPS = {
    "xmmxmmimm8": {"mod": "/r", "opcode": "660F3A0C", "imm": "ib"},
    "xmmmem128imm8": {"mod": "/r", "opcode": "660F3A0C", "imm": "ib"},
}

BLENDVPD = {
    "xmmxmm": {"mod": "/r", "opcode": "660F3815"},
    "xmmmem128": {"mod": "/r", "opcode": "660F3815"},
}

BLENDVPS = {
    "xmmxmm": {"mod": "/r", "opcode": "660F3814"},
    "xmmmem128": {"mod": "/r", "opcode": "660F3814"},
}

PBLENDVB = {
    "xmmxmm": {"mod": "/r", "opcode": "660F3810"},
    "xmmmem128": {"mod": "/r", "opcode": "660F3810"},
}

PBLENDW = {
    "xmmxmmimm8": {"mod": "/r", "opcode": "660F3A0E", "imm": "ib"},
    "xmmmem128imm8": {"mod": "/r", "opcode": "660F3A0E", "imm": "ib"},
}

PMINUW = {
    "xmmxmm": {"mod": "/r", "opcode": "660F383A"},
    "xmmmem128": {"mod": "/r", "opcode": "660F383A"},
}

PMINUD = {
    "xmmxmm": {"mod": "/r", "opcode": "660F383B"},
    "xmmmem128": {"mod": "/r", "opcode": "660F383B"},
}

PMINSB = {
    "xmmxmm": {"mod": "/r", "opcode": "660F3838"},
    "xmmmem128": {"mod": "/r", "opcode": "660F3838"},
}

PMINSD = {
    "xmmxmm": {"mod": "/r", "opcode": "660F3839"},
    "xmmmem128": {"mod": "/r", "opcode": "660F3839"},
}

PMAXUW = {
    "xmmxmm": {"mod": "/r", "opcode": "660F383E"},
    "xmmmem128": {"mod": "/r", "opcode": "660F383E"},
}

PMAXUD = {
    "xmmxmm": {"mod": "/r", "opcode": "660F383F"},
    "xmmmem128": {"mod": "/r", "opcode": "660F383F"},
}

PMAXSB = {
    "xmmxmm": {"mod": "/r", "opcode": "660F383C"},
    "xmmmem128": {"mod": "/r", "opcode": "660F383C"},
}

PMAXSD = {
    "xmmxmm": {"mod": "/r", "opcode": "660F383D"},
    "xmmmem128": {"mod": "/r", "opcode": "660F383D"},
}

ROUNDPS = {
    "xmmxmmimm8": {"mod": "/r", "opcode": "660F3A08", "imm": "ib"},
    "xmmmem128imm8": {"mod": "/r", "opcode": "660F3A08", "imm": "ib"},
}

ROUNDPD = {
    "xmmxmmimm8": {"mod": "/r", "opcode": "660F3A09", "imm": "ib"},
    "xmmmem128imm8": {"mod": "/r", "opcode": "660F3A09", "imm": "ib"},
}

ROUNDSS = {
    "xmmxmmimm8": {"mod": "/r", "opcode": "660F3A0A", "imm": "ib"},
    "xmmmem32imm8": {"mod": "/r", "opcode": "660F3A0A", "imm": "ib"},
}

ROUNDSD = {
    "xmmxmmimm8": {"mod": "/r", "opcode": "660F3A0B", "imm": "ib"},
    "xmmmem64imm8": {"mod": "/r", "opcode": "660F3A0B", "imm": "ib"},
}

EXTRACTPS = {
    "r32xmmimm8": {"mod": "/r", "opcode": "660F3A17", "imm": "ib"},
    "r64xmmimm8": {"mod": "/r", "opcode": "660F3A17", "prefix": "REX.W", "imm": "ib"},
    "mem32xmmimm8": {"mod": "/r", "opcode": "660F3A17", "imm": "ib"},
}

INSERTPS = {
    "xmmxmmimm8": {"mod": "/r", "opcode": "660F3A21", "imm": "ib"},
    "xmmmem32imm8": {"mod": "/r", "opcode": "660F3A21", "imm": "ib"},
}

PINSRB = {
    "xmmr32imm8": {"mod": "/r", "opcode": "660F3A20", "imm": "ib"},
    "xmmmem8imm8": {"mod": "/r", "opcode": "660F3A20", "imm": "ib"},
}

PINSRD = {
    "xmmr32imm8": {"mod": "/r", "opcode": "660F3A22", "imm": "ib"},
    "xmmmem32imm8": {"mod": "/r", "opcode": "660F3A22", "imm": "ib"},
}

PINSRQ = {
    "xmmr64imm8": {"mod": "/r", "opcode": "660F3A22", "prefix": "REX.W", "imm": "ib"},
    "xmmmem64imm8": {"mod": "/r", "opcode": "660F3A22", "prefix": "REX.W", "imm": "ib"},
}

PEXTRB = {
    "r32xmmimm8": {"mod": "/r", "opcode": "660F3A14", "imm": "ib", "rm": "1"},
    "r64xmmimm8": {"mod": "/r", "opcode": "660F3A14", "prefix": "REX.W", "imm": "ib", "rm": "1"},
    "mem8xmmimm8": {"mod": "/r", "opcode": "660F3A14", "imm": "ib"},
}

PEXTRD = {
    "r32xmmimm8": {"mod": "/r", "opcode": "660F3A16", "imm": "ib", "rm": "1"},
    "mem32xmmimm8": {"mod": "/r", "opcode": "660F3A16", "imm": "ib"},
}

PEXTRQ = {
    "r64xmmimm8": {"mod": "/r", "opcode": "660F3A16", "prefix": "REX.W", "imm": "ib", "rm": "1"},
    "mem64xmmimm8": {"mod": "/r", "opcode": "660F3A16", "prefix": "REX.W", "imm": "ib"},
}

PMOVSXBW = {
    "xmmxmm": {"mod": "/r", "opcode": "660F3820"},
    "xmmmem64": {"mod": "/r", "opcode": "660F3820"},
}

PMOVSXBD = {
    "xmmxmm": {"mod": "/r", "opcode": "660F3821"},
    "xmmmem32": {"mod": "/r", "opcode": "660F3821"},
}

PMOVSXBQ = {
    "xmmxmm": {"mod": "/r", "opcode": "660F3822"},
    "xmmmem16": {"mod": "/r", "opcode": "660F3822"},
}

PMOVSXWD = {
    "xmmxmm": {"mod": "/r", "opcode": "660F3823"},
    "xmmmem64": {"mod": "/r", "opcode": "660F3823"},
}

PMOVSXWQ = {
    "xmmxmm": {"mod": "/r", "opcode": "660F3824"},
    "xmmmem32": {"mod": "/r", "opcode": "660F3824"},
}

PMOVSXDQ = {
    "xmmxmm": {"mod": "/r", "opcode": "660F3825"},
    "xmmmem64": {"mod": "/r", "opcode": "660F3825"},
}

PMOVZXBW = {
    "xmmxmm": {"mod": "/r", "opcode": "660F3830"},
    "xmmmem64": {"mod": "/r", "opcode": "660F3830"},
}

PMOVZXBD = {
    "xmmxmm": {"mod": "/r", "opcode": "660F3831"},
    "xmmmem32": {"mod": "/r", "opcode": "660F3831"},
}

PMOVZXBQ = {
    "xmmxmm": {"mod": "/r", "opcode": "660F3832"},
    "xmmmem16": {"mod": "/r", "opcode": "660F3832"},
}

PMOVZXWD = {
    "xmmxmm": {"mod": "/r", "opcode": "660F3833"},
    "xmmmem64": {"mod": "/r", "opcode": "660F3833"},
}

PMOVZXWQ = {
    "xmmxmm": {"mod": "/r", "opcode": "660F3834"},
    "xmmmem32": {"mod": "/r", "opcode": "660F3834"},
}

PMOVZXDQ = {
    "xmmxmm": {"mod": "/r", "opcode": "660F3835"},
    "xmmmem64": {"mod": "/r", "opcode": "660F3835"},
}

MPSADBW = {
    "xmmxmmimm8": {"mod": "/r", "opcode": "660F3A42", "imm": "ib"},
    "xmmmem128imm8": {"mod": "/r", "opcode": "660F3A42", "imm": "ib"},
}

PHMINPOSUW = {
    "xmmxmm": {"mod": "/r", "opcode": "660F3841"},
    "xmmmem128": {"mod": "/r", "opcode": "660F3841"},
}

PTEST = {
    "xmmxmm": {"mod": "/r", "opcode": "660F3817"},
    "xmmmem128": {"mod": "/r", "opcode": "660F3817"},
}

PCMPEQQ = {
    "xmmxmm": {"mod": "/r", "opcode": "660F3829"},
    "xmmmem128": {"mod": "/r", "opcode": "660F3829"},
}

PACKUSDW = {
    "xmmxmm": {"mod": "/r", "opcode": "660F382B"},
    "xmmmem128": {"mod": "/r", "opcode": "660F382B"},
}
