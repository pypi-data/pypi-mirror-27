

MOVAPD = {
    "xmmxmm": {"mod": "/r", "opcode": "660F28"},
    "xmmmem128": {"mod": "/r", "opcode": "660F28"},
    "mem128xmm": {"mod": "/r", "opcode": "660F29"},
}

MOVUPD = {
    "xmmxmm": {"mod": "/r", "opcode": "660F10"},
    "xmmmem128": {"mod": "/r", "opcode": "660F10"},
    "mem128xmm": {"mod": "/r", "opcode": "660F11"},
}

MOVHPD = {
    "xmmmem64": {"mod": "/r", "opcode": "660F16"},
    "mem64xmm": {"mod": "/r", "opcode": "660F17"},
}

MOVLPD = {
    "xmmmem64": {"mod": "/r", "opcode": "660F12"},
    "mem64xmm": {"mod": "/r", "opcode": "660F13"},
}

MOVMSKPD = {
    "r32xmm": {"mod": "/r", "opcode": "660F50"},
    "r64xmm": {"mod": "/r", "opcode": "660F50"},
}

MOVSD = {
    "xmmxmm": {"mod": "/r", "opcode": "F20F10"},
    "xmmmem64": {"mod": "/r", "opcode": "F20F10"},
    "mem64xmm": {"mod": "/r", "opcode": "F20F11"},
}

ADDPD = {
    "xmmxmm": {"mod": "/r", "opcode": "660F58"},
    "xmmmem128": {"mod": "/r", "opcode": "660F58"},
}

ADDSD = {
    "xmmxmm": {"mod": "/r", "opcode": "F20F58"},
    "xmmmem64": {"mod": "/r", "opcode": "F20F58"},
}

SUBPD = {
    "xmmxmm": {"mod": "/r", "opcode": "660F5C"},
    "xmmmem128": {"mod": "/r", "opcode": "660F5C"},
}

SUBSD = {
    "xmmxmm": {"mod": "/r", "opcode": "F20F5C"},
    "xmmmem64": {"mod": "/r", "opcode": "F20F5C"},
}

MULPD = {
    "xmmxmm": {"mod": "/r", "opcode": "660F59"},
    "xmmmem128": {"mod": "/r", "opcode": "660F59"},
}

MULSD = {
    "xmmxmm": {"mod": "/r", "opcode": "F20F59"},
    "xmmmem64": {"mod": "/r", "opcode": "F20F59"},
}

DIVPD = {
    "xmmxmm": {"mod": "/r", "opcode": "660F5E"},
    "xmmmem128": {"mod": "/r", "opcode": "660F5E"},
}

DIVSD = {
    "xmmxmm": {"mod": "/r", "opcode": "F20F5E"},
    "xmmmem64": {"mod": "/r", "opcode": "F20F5E"},
}

SQRTPD = {
    "xmmxmm": {"mod": "/r", "opcode": "660F51"},
    "xmmmem128": {"mod": "/r", "opcode": "660F51"},
}

SQRTSD = {
    "xmmxmm": {"mod": "/r", "opcode": "F20F51"},
    "xmmmem64": {"mod": "/r", "opcode": "F20F51"},
}

MAXPD = {
    "xmmxmm": {"mod": "/r", "opcode": "660F5F"},
    "xmmmem128": {"mod": "/r", "opcode": "660F5F"},
}

MAXSD = {
    "xmmxmm": {"mod": "/r", "opcode": "F20F5F"},
    "xmmmem64": {"mod": "/r", "opcode": "F20F5F"},
}

MINPD = {
    "xmmxmm": {"mod": "/r", "opcode": "660F5D"},
    "xmmmem128": {"mod": "/r", "opcode": "660F5D"},
}

MINSD = {
    "xmmxmm": {"mod": "/r", "opcode": "F20F5D"},
    "xmmmem64": {"mod": "/r", "opcode": "F20F5D"},
}

CMPPD = {
    "xmmxmmimm8": {"mod": "/r", "opcode": "660FC2", "imm": "ib"},
    "xmmmem128imm8": {"mod": "/r", "opcode": "660FC2", "imm": "ib"},
}

CMPSD = {
    "xmmxmmimm8": {"mod": "/r", "opcode": "F20FC2", "imm": "ib"},
    "xmmmem64imm8": {"mod": "/r", "opcode": "F20FC2", "imm": "ib"},
}

COMISD = {
    "xmmxmm": {"mod": "/r", "opcode": "660F2F"},
    "xmmmem64": {"mod": "/r", "opcode": "660F2F"},
}

UCOMISD = {
    "xmmxmm": {"mod": "/r", "opcode": "660F2E"},
    "xmmmem64": {"mod": "/r", "opcode": "660F2E"},
}

ANDPD = {
    "xmmxmm": {"mod": "/r", "opcode": "660F54"},
    "xmmmem128": {"mod": "/r", "opcode": "660F54"},
}

ANDNPD = {
    "xmmxmm": {"mod": "/r", "opcode": "660F55"},
    "xmmmem128": {"mod": "/r", "opcode": "660F55"},
}

ORPD = {
    "xmmxmm": {"mod": "/r", "opcode": "660F56"},
    "xmmmem128": {"mod": "/r", "opcode": "660F56"},
}

XORPD = {
    "xmmxmm": {"mod": "/r", "opcode": "660F57"},
    "xmmmem128": {"mod": "/r", "opcode": "660F57"},
}

SHUFPD = {
    "xmmxmmimm8": {"mod": "/r", "opcode": "660FC6", "imm": "ib"},
    "xmmmem128imm8": {"mod": "/r", "opcode": "660FC6", "imm": "ib"},
}

UNPCKHPD = {
    "xmmxmm": {"mod": "/r", "opcode": "660F15"},
    "xmmmem128": {"mod": "/r", "opcode": "660F15"},
}

UNPCKLPD = {
    "xmmxmm": {"mod": "/r", "opcode": "660F14"},
    "xmmmem128": {"mod": "/r", "opcode": "660F14"},
}

CVTPD2PI = {
    "mmxmm": {"mod": "/r", "opcode": "660F2D"},
    "mmmem128": {"mod": "/r", "opcode": "660F2D"},
}

CVTTPD2PI = {
    "mmxmm": {"mod": "/r", "opcode": "660F2C"},
    "mmmem128": {"mod": "/r", "opcode": "660F2C"},
}

CVTPI2PD = {
    "xmmmm": {"mod": "/r", "opcode": "660F2A"},
    "xmmmem64": {"mod": "/r", "opcode": "660F2A"},
}

CVTPD2DQ = {
    "xmmxmm": {"mod": "/r", "opcode": "F20FE6"},
    "xmmmem128": {"mod": "/r", "opcode": "F20FE6"},
}

CVTTPD2DQ = {
    "xmmxmm": {"mod": "/r", "opcode": "660FE6"},
    "xmmmem128": {"mod": "/r", "opcode": "660FE6"},
}

CVTDQ2PD = {
    "xmmxmm": {"mod": "/r", "opcode": "F30FE6"},
    "xmmmem64": {"mod": "/r", "opcode": "F30FE6"},
}

CVTPS2PD = {
    "xmmxmm": {"mod": "/r", "opcode": "0F5A"},
    "xmmmem64": {"mod": "/r", "opcode": "0F5A"},
}

CVTPD2PS = {
    "xmmxmm": {"mod": "/r", "opcode": "660F5A"},
    "xmmmem128": {"mod": "/r", "opcode": "660F5A"},
}

CVTSS2SD = {
    "xmmxmm": {"mod": "/r", "opcode": "F30F5A"},
    "xmmmem32": {"mod": "/r", "opcode": "F30F5A"},
}

CVTSD2SS = {
    "xmmxmm": {"mod": "/r", "opcode": "F20F5A"},
    "xmmmem64": {"mod": "/r", "opcode": "F20F5A"},
}

CVTSD2SI = {
    "r32xmm": {"mod": "/r", "opcode": "F20F2D"},
    "r64xmm": {"mod": "/r", "opcode": "F20F2D", "prefix": "REX.W"},
    "r32mem64": {"mod": "/r", "opcode": "F20F2D"},
    "r64mem64": {"mod": "/r", "opcode": "F20F2D", "prefix": "REX.W"},
}

CVTTSD2SI = {
    "r32xmm": {"mod": "/r", "opcode": "F20F2C"},
    "r64xmm": {"mod": "/r", "opcode": "F20F2C", "prefix": "REX.W"},
    "r32mem64": {"mod": "/r", "opcode": "F20F2C"},
    "r64mem64": {"mod": "/r", "opcode": "F20F2C", "prefix": "REX.W"},
}

CVTSI2SD = {
    "xmmr32": {"mod": "/r", "opcode": "F20F2A"},
    "xmmr64": {"mod": "/r", "opcode": "F20F2A", "prefix": "REX.W"},
    "xmmmem32": {"mod": "/r", "opcode": "F20F2A"},
    "xmmmem64": {"mod": "/r", "opcode": "F20F2A", "prefix": "REX.W"},
}

CVTDQ2PS = {
    "xmmxmm": {"mod": "/r", "opcode": "0F5B"},
    "xmmmem128": {"mod": "/r", "opcode": "0F5B"},
}

CVTPS2DQ = {
    "xmmxmm": {"mod": "/r", "opcode": "660F5B"},
    "xmmmem128": {"mod": "/r", "opcode": "660F5B"},
}

CVTTPS2DQ = {
    "xmmxmm": {"mod": "/r", "opcode": "F30F5B"},
    "xmmmem128": {"mod": "/r", "opcode": "F30F5B"},
}

MOVDQA = {
    "xmmxmm": {"mod": "/r", "opcode": "660F6F"},
    "xmmmem128": {"mod": "/r", "opcode": "660F6F"},
    "mem128xmm": {"mod": "/r", "opcode": "660F7F"},
}

MOVDQU = {
    "xmmxmm": {"mod": "/r", "opcode": "F30F6F"},
    "xmmmem128": {"mod": "/r", "opcode": "F30F6F"},
    "mem128xmm": {"mod": "/r", "opcode": "F30F7F"},
}

MOVQ2DQ = {"xmmmm": {"mod": "/r", "opcode": "F30FD6"}}
MOVDQ2Q = {"mmxmm": {"mod": "/r", "opcode": "F20FD6"}}

PMULUDQ = {
    "mmmm": {"mod": "/r", "opcode": "0FF4"},
    "mmmem64": {"mod": "/r", "opcode": "0FF4"},

    "xmmxmm": {"mod": "/r", "opcode": "660FF4"},
    "xmmmem128": {"mod": "/r", "opcode": "660FF4"},
}

PADDQ = {
    "mmmm": {"mod": "/r", "opcode": "0FD4"},
    "mmmem64": {"mod": "/r", "opcode": "0FD4"},

    "xmmxmm": {"mod": "/r", "opcode": "660FD4"},
    "xmmmem128": {"mod": "/r", "opcode": "660FD4"},
}

PSUBQ = {
    "mmmm": {"mod": "/r", "opcode": "0FFB"},
    "mmmem64": {"mod": "/r", "opcode": "0FFB"},

    "xmmxmm": {"mod": "/r", "opcode": "660FFB"},
    "xmmmem128": {"mod": "/r", "opcode": "660FFB"},
}

PSHUFLW = {
    "xmmxmmimm8": {"mod": "/r", "opcode": "F20F70", "imm": "ib"},
    "xmmmem128imm8": {"mod": "/r", "opcode": "F20F70", "imm": "ib"},
}

PSHUFHW = {
    "xmmxmmimm8": {"mod": "/r", "opcode": "F30F70", "imm": "ib"},
    "xmmmem128imm8": {"mod": "/r", "opcode": "F30F70", "imm": "ib"},
}

PSHUFD = {
    "xmmxmmimm8": {"mod": "/r", "opcode": "660F70", "imm": "ib"},
    "xmmmem128imm8": {"mod": "/r", "opcode": "660F70", "imm": "ib"},
}

PSLLDQ = {"xmmimm8": {"mod": "/7", "opcode": "660F73", "imm": "ib"}}
PSRLDQ = {"xmmimm8": {"mod": "/3", "opcode": "660F73", "imm": "ib"}}


PUNPCKHQDQ = {
    "xmmxmm": {"mod": "/r", "opcode": "660F6D"},
    "xmmmem128": {"mod": "/r", "opcode": "660F6D"},
}

PUNPCKLQDQ = {
    "xmmxmm": {"mod": "/r", "opcode": "660F6C"},
    "xmmmem128": {"mod": "/r", "opcode": "660F6C"},
}

CLFLUSH = {"mem8": {"opcode": "0FAE", "mod": "/7"}}
LFENCE = {"no_op": {"opcode": "0FAEE8"}}
MFENCE = {"no_op": {"opcode": "0FAEF0"}}
PAUSE = {"no_op": {"opcode": "F390"}}
MASKMOVDQU = {"xmmxmm": {"mod": "/r", "opcode": "660FF7"}}
MOVNTPD = {"mem128xmm": {"mod": "/r", "opcode": "660F2B"}}
MOVNTI = {
    "mem32r32": {"mod": "/r", "opcode": "0FC3"},
    "mem64r64": {"mod": "/r", "opcode": "0FC3", "prefix": "REX.W"},
}

MOVNTDQ = {"mem128xmm": {"mod": "/r", "opcode": "660FE7"}}
