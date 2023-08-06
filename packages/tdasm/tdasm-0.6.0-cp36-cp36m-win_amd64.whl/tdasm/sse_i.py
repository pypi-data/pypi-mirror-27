

MOVAPS = {
    "xmmxmm": {"mod": "/r", "opcode": "0F28"},
    "xmmmem128": {"mod": "/r", "opcode": "0F28"},
    "mem128xmm": {"mod": "/r", "opcode": "0F29"},
}

MOVUPS = {
    "xmmxmm": {"mod": "/r", "opcode": "0F10"},
    "xmmmem128": {"mod": "/r", "opcode": "0F10"},
    "mem128xmm": {"mod": "/r", "opcode": "0F11"},
}

MOVHPS = {
    "xmmmem64": {"mod": "/r", "opcode": "0F16"},
    "mem64xmm": {"mod": "/r", "opcode": "0F17"},
}

MOVHLPS = {
    "xmmxmm": {"mod": "/r", "opcode": "0F12"},
}

MOVLPS = {
    "xmmmem64": {"mod": "/r", "opcode": "0F12"},
    "mem64xmm": {"mod": "/r", "opcode": "0F13"},
}

MOVLHPS = {
    "xmmxmm": {"mod": "/r", "opcode": "0F16"},
}

MOVMSKPS = {
    "r32xmm": {"mod": "/r", "opcode": "0F50"},
    "r64xmm": {"mod": "/r", "opcode": "0F50"},
}

MOVSS = {
    "xmmxmm": {"mod": "/r", "opcode": "F30F10"},
    "xmmmem32": {"mod": "/r", "opcode": "F30F10"},
    "mem32xmm": {"mod": "/r", "opcode": "F30F11"},
}

ADDPS = {
    "xmmxmm": {"mod": "/r", "opcode": "0F58"},
    "xmmmem128": {"mod": "/r", "opcode": "0F58"},
}

ADDSS = {
    "xmmxmm": {"mod": "/r", "opcode": "F30F58"},
    "xmmmem32": {"mod": "/r", "opcode": "F30F58"},
}

SUBPS = {
    "xmmxmm": {"mod": "/r", "opcode": "0F5C"},
    "xmmmem128": {"mod": "/r", "opcode": "0F5C"},
}

SUBSS = {
    "xmmxmm": {"mod": "/r", "opcode": "F30F5C"},
    "xmmmem32": {"mod": "/r", "opcode": "F30F5C"},
}

MULPS = {
    "xmmxmm": {"mod": "/r", "opcode": "0F59"},
    "xmmmem128": {"mod": "/r", "opcode": "0F59"},
}

MULSS = {
    "xmmxmm": {"mod": "/r", "opcode": "F30F59"},
    "xmmmem32": {"mod": "/r", "opcode": "F30F59"},
}

DIVPS = {
    "xmmxmm": {"mod": "/r", "opcode": "0F5E"},
    "xmmmem128": {"mod": "/r", "opcode": "0F5E"},
}

DIVSS = {
    "xmmxmm": {"mod": "/r", "opcode": "F30F5E"},
    "xmmmem32": {"mod": "/r", "opcode": "F30F5E"},
}

RCPPS = {
    "xmmxmm": {"mod": "/r", "opcode": "0F53"},
    "xmmmem128": {"mod": "/r", "opcode": "0F53"},
}

RCPSS = {
    "xmmxmm": {"mod": "/r", "opcode": "F30F53"},
    "xmmmem32": {"mod": "/r", "opcode": "F30F53"},
}

SQRTPS = {
    "xmmxmm": {"mod": "/r", "opcode": "0F51"},
    "xmmmem128": {"mod": "/r", "opcode": "0F51"},
}

SQRTSS = {
    "xmmxmm": {"mod": "/r", "opcode": "F30F51"},
    "xmmmem32": {"mod": "/r", "opcode": "F30F51"},
}

RSQRTPS = {
    "xmmxmm": {"mod": "/r", "opcode": "0F52"},
    "xmmmem128": {"mod": "/r", "opcode": "0F52"},
}

RSQRTSS = {
    "xmmxmm": {"mod": "/r", "opcode": "F30F52"},
    "xmmmem32": {"mod": "/r", "opcode": "F30F52"},
}

MAXPS = {
    "xmmxmm": {"mod": "/r", "opcode": "0F5F"},
    "xmmmem128": {"mod": "/r", "opcode": "0F5F"},
}

MAXSS = {
    "xmmxmm": {"mod": "/r", "opcode": "F30F5F"},
    "xmmmem32": {"mod": "/r", "opcode": "F30F5F"},
}

MINPS = {
    "xmmxmm": {"mod": "/r", "opcode": "0F5D"},
    "xmmmem128": {"mod": "/r", "opcode": "0F5D"},
}

MINSS = {
    "xmmxmm": {"mod": "/r", "opcode": "F30F5D"},
    "xmmmem32": {"mod": "/r", "opcode": "F30F5D"},
}

CMPPS = {
    "xmmxmmimm8": {"mod": "/r", "opcode": "0FC2", "imm": "ib"},
    "xmmmem128imm8": {"mod": "/r", "opcode": "0FC2", "imm": "ib"},
}

CMPSS = {
    "xmmxmmimm8": {"mod": "/r", "opcode": "F30FC2", "imm": "ib"},
    "xmmmem32imm8": {"mod": "/r", "opcode": "F30FC2", "imm": "ib"},
}

COMISS = {
    "xmmxmm": {"mod": "/r", "opcode": "0F2F"},
    "xmmmem32": {"mod": "/r", "opcode": "0F2F"},
}

UCOMISS = {
    "xmmxmm": {"mod": "/r", "opcode": "0F2E"},
    "xmmmem32": {"mod": "/r", "opcode": "0F2E"},
}

ANDPS = {
    "xmmxmm": {"mod": "/r", "opcode": "0F54"},
    "xmmmem128": {"mod": "/r", "opcode": "0F54"},
}

ANDNPS = {
    "xmmxmm": {"mod": "/r", "opcode": "0F55"},
    "xmmmem128": {"mod": "/r", "opcode": "0F55"},
}

ORPS = {
    "xmmxmm": {"mod": "/r", "opcode": "0F56"},
    "xmmmem128": {"mod": "/r", "opcode": "0F56"},
}

XORPS = {
    "xmmxmm": {"mod": "/r", "opcode": "0F57"},
    "xmmmem128": {"mod": "/r", "opcode": "0F57"},
}

SHUFPS = {
    "xmmxmmimm8": {"mod": "/r", "opcode": "0FC6", "imm": "ib"},
    "xmmmem128imm8": {"mod": "/r", "opcode": "0FC6", "imm": "ib"},
}

UNPCKHPS = {
    "xmmxmm": {"mod": "/r", "opcode": "0F15"},
    "xmmmem128": {"mod": "/r", "opcode": "0F15"},
}

UNPCKLPS = {
    "xmmxmm": {"mod": "/r", "opcode": "0F14"},
    "xmmmem128": {"mod": "/r", "opcode": "0F14"},
}

CVTPI2PS = {
    "xmmmm": {"mod": "/r", "opcode": "0F2A"},
    "xmmmem64": {"mod": "/r", "opcode": "0F2A"},
}

CVTSI2SS = {
    "xmmr32": {"mod": "/r", "opcode": "F30F2A"},
    "xmmr64": {"mod": "/r", "opcode": "F30F2A", "prefix": "REX.W"},
    "xmmmem32": {"mod": "/r", "opcode": "F30F2A"},
    "xmmmem64": {"mod": "/r", "opcode": "F30F2A", "prefix": "REX.W"},
}

CVTPS2PI = {
    "mmxmm": {"mod": "/r", "opcode": "0F2D"},
    "mmmem64": {"mod": "/r", "opcode": "0F2D"},
}

CVTTPS2PI = {
    "mmxmm": {"mod": "/r", "opcode": "0F2C"},
    "mmmem64": {"mod": "/r", "opcode": "0F2C"},
}

CVTSS2SI = {
    "r32xmm": {"mod": "/r", "opcode": "F30F2D"},
    "r64xmm": {"mod": "/r", "opcode": "F30F2D", "prefix": "REX.W"},
    "r32mem32": {"mod": "/r", "opcode": "F30F2D"},
    "r64mem32": {"mod": "/r", "opcode": "F30F2D", "prefix": "REX.W"},
}

CVTTSS2SI = {
    "r32xmm": {"mod": "/r", "opcode": "F30F2C"},
    "r64xmm": {"mod": "/r", "opcode": "F30F2C", "prefix": "REX.W"},
    "r32mem32": {"mod": "/r", "opcode": "F30F2C"},
    "r64mem32": {"mod": "/r", "opcode": "F30F2C", "prefix": "REX.W"},
}

LDMXCSR = {
    "mem32": {"mod": "/2", "opcode": "0FAE"},
}

STMXCSR = {
    "mem32": {"mod": "/3", "opcode": "0FAE"},
}

PAVGB = {
    "mmmm": {"mod": "/r", "opcode": "0FE0"},
    "mmmem64": {"mod": "/r", "opcode": "0FE0"},
    "xmmxmm": {"mod": "/r", "opcode": "660FE0"},
    "xmmmem128": {"mod": "/r", "opcode": "660FE0"},
}

PAVGW = {
    "mmmm": {"mod": "/r", "opcode": "0FE3"},
    "mmmem64": {"mod": "/r", "opcode": "0FE3"},
    "xmmxmm": {"mod": "/r", "opcode": "660FE3"},
    "xmmmem128": {"mod": "/r", "opcode": "660FE3"},
}

PEXTRW = {
    "r32mmimm8": {"mod": "/r", "opcode": "0FC5", "imm": "ib"},
    "r64mmimm8": {"mod": "/r", "opcode": "0FC5", "prefix": "REX.W", "imm": "ib"},
    "r32xmmimm8": {"mod": "/r", "opcode": "660FC5", "imm": "ib"},
    "r64xmmimm8": {"mod": "/r", "opcode": "660FC5", "prefix": "REX.W", "imm": "ib"},
    "mem16xmmimm8": {"mod": "/r", "opcode": "660F3A15", "imm": "ib"},
}

PINSRW = {
    "mmr32imm8": {"mod": "/r", "opcode": "0FC4", "imm": "ib"},
    "mmmem16imm8": {"mod": "/r", "opcode": "0FC4", "imm": "ib"},
    "xmmr32imm8": {"mod": "/r", "opcode": "660FC4", "imm": "ib"},
    "xmmmem16imm8": {"mod": "/r", "opcode": "660FC4", "imm": "ib"},
}

PMAXUB = {
    "mmmm": {"mod": "/r", "opcode": "0FDE"},
    "mmmem64": {"mod": "/r", "opcode": "0FDE"},
    "xmmxmm": {"mod": "/r", "opcode": "660FDE"},
    "xmmmem128": {"mod": "/r", "opcode": "660FDE"},
}

PMAXSW = {
    "mmmm": {"mod": "/r", "opcode": "0FEE"},
    "mmmem64": {"mod": "/r", "opcode": "0FEE"},
    "xmmxmm": {"mod": "/r", "opcode": "660FEE"},
    "xmmmem128": {"mod": "/r", "opcode": "660FEE"},
}

PMINUB = {
    "mmmm": {"mod": "/r", "opcode": "0FDA"},
    "mmmem64": {"mod": "/r", "opcode": "0FDA"},
    "xmmxmm": {"mod": "/r", "opcode": "660FDA"},
    "xmmmem128": {"mod": "/r", "opcode": "660FDA"},
}

PMINSW = {
    "mmmm": {"mod": "/r", "opcode": "0FEA"},
    "mmmem64": {"mod": "/r", "opcode": "0FEA"},
    "xmmxmm": {"mod": "/r", "opcode": "660FEA"},
    "xmmmem128": {"mod": "/r", "opcode": "660FEA"},
}

PMOVMSKB = {
    "r32mm": {"mod": "/r", "opcode": "0FD7"},
    "r64mm": {"mod": "/r", "opcode": "0FD7"},
    "r32xmm": {"mod": "/r", "opcode": "660FD7"},
    "r64xmm": {"mod": "/r", "opcode": "660FD7"},
}

PMULHUW = {
    "mmmm": {"mod": "/r", "opcode": "0FE4"},
    "mmmem64": {"mod": "/r", "opcode": "0FE4"},
    "xmmxmm": {"mod": "/r", "opcode": "660FE4"},
    "xmmmem128": {"mod": "/r", "opcode": "660FE4"},
}

PSADBW = {
    "mmmm": {"mod": "/r", "opcode": "0FF6"},
    "mmmem64": {"mod": "/r", "opcode": "0FF6"},
    "xmmxmm": {"mod": "/r", "opcode": "660FF6"},
    "xmmmem128": {"mod": "/r", "opcode": "660FF6"},
}

PSHUFW = {
    "mmmmimm8": {"mod": "/r", "opcode": "0F70", "imm": "ib"},
    "mmmem64imm8": {"mod": "/r", "opcode": "0F70", "imm": "ib"},
}

MASKMOVQ = {"mmmm": {"mod": "/r", "opcode": "0FF7"}}
MOVNTQ = {"mem64mm": {"mod": "/r", "opcode": "0FE7"}}
MOVNTPS = {"mem128xmm": {"mod": "/r", "opcode": "0F2B"}}
PREFETCHT0 = {"mem8": {"opcode": "0F18", "mod": "/1"}}
PREFETCHT1 = {"mem8": {"opcode": "0F18", "mod": "/2"}}
PREFETCHT2 = {"mem8": {"opcode": "0F18", "mod": "/3"}}
PREFETCHNTA = {"mem8": {"opcode": "0F18", "mod": "/0"}}
SFENCE = {"no_op": {"opcode": "0FAEF8"}}
