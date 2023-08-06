

MOVD = {
    "mmr32": {"mod": "/r", "opcode": "0F6E"},
    "mmmem32": {"mod": "/r", "opcode": "0F6E"},
    "r32mm": {"mod": "/r", "opcode": "0F7E", "rm": "1"},
    "mem32mm": {"mod": "/r", "opcode": "0F7E"},
    "xmmr32": {"mod": "/r", "opcode": "660F6E"},
    "xmmmem32": {"mod": "/r", "opcode": "660F6E"},
    "r32xmm": {"mod": "/r", "opcode": "660F7E", "rm": "1"},
    "mem32xmm": {"mod": "/r", "opcode": "660F7E"},
}

MOVQ = {
    "mmmm": {"mod": "/r", "opcode": "0F6F"},
    "mmmem64": {"mod": "/r", "opcode": "0F6F"},
    "mem64mm": {"mod": "/r", "opcode": "0F7F"},
    "xmmxmm": {"mod": "/r", "opcode": "F30F7E"},
    "xmmmem64": {"mod": "/r", "opcode": "F30F7E"},
    "mem64xmm": {"mod": "/r", "opcode": "660FD6"},

    "mmr64": {"mod": "/r", "opcode": "0F6E", "prefix": "REX.W"},
    # "mmmem64": {"mod": "/r", "opcode": "0F6E", "prefix": "REX.W"},
    "r64mm": {"mod": "/r", "opcode": "0F7E", "prefix": "REX.W", "rm": "1"},
    # "mem64mm": {"mod": "/r", "opcode": "0F7E", "prefix": "REX.W"},
    "xmmr64": {"mod": "/r", "opcode": "660F6E", "prefix": "REX.W"},
    # "xmmmem64": {"mod": "/r", "opcode": "660F6E", "prefix": "REX.W"},
    "r64xmm": {"mod": "/r", "opcode": "660F7E", "prefix": "REX.W", "rm": "1"},
    # "mem64xmm": {"mod": "/r", "opcode": "660F7E", "prefix": "REX.W"}
}

PACKSSWB = {
    "mmmm": {"mod": "/r", "opcode": "0F63"},
    "mmmem64": {"mod": "/r", "opcode": "0F63"},
    "xmmxmm": {"mod": "/r", "opcode": "660F63"},
    "xmmmem128": {"mod": "/r", "opcode": "660F63"},
}

PACKSSDW = {
    "mmmm": {"mod": "/r", "opcode": "0F6B"},
    "mmmem64": {"mod": "/r", "opcode": "0F6B"},
    "xmmxmm": {"mod": "/r", "opcode": "660F6B"},
    "xmmmem128": {"mod": "/r", "opcode": "660F6B"},
}

PACKUSWB = {
    "mmmm": {"mod": "/r", "opcode": "0F67"},
    "mmmem64": {"mod": "/r", "opcode": "0F67"},
    "xmmxmm": {"mod": "/r", "opcode": "660F67"},
    "xmmmem128": {"mod": "/r", "opcode": "660F67"},
}

PUNPCKHBW = {
    "mmmm": {"mod": "/r", "opcode": "0F68"},
    "mmmem64": {"mod": "/r", "opcode": "0F68"},
    "xmmxmm": {"mod": "/r", "opcode": "660F68"},
    "xmmmem128": {"mod": "/r", "opcode": "660F68"},
}

PUNPCKHWD = {
    "mmmm": {"mod": "/r", "opcode": "0F69"},
    "mmmem64": {"mod": "/r", "opcode": "0F69"},
    "xmmxmm": {"mod": "/r", "opcode": "660F69"},
    "xmmmem128": {"mod": "/r", "opcode": "660F69"},
}

PUNPCKHDQ = {
    "mmmm": {"mod": "/r", "opcode": "0F6A"},
    "mmmem64": {"mod": "/r", "opcode": "0F6A"},
    "xmmxmm": {"mod": "/r", "opcode": "660F6A"},
    "xmmmem128": {"mod": "/r", "opcode": "660F6A"},
}

PUNPCKLBW = {
    "mmmm": {"mod": "/r", "opcode": "0F60"},
    "mmmem32": {"mod": "/r", "opcode": "0F60"},
    "xmmxmm": {"mod": "/r", "opcode": "660F60"},
    "xmmmem128": {"mod": "/r", "opcode": "660F60"},
}

PUNPCKLWD = {
    "mmmm": {"mod": "/r", "opcode": "0F61"},
    "mmmem32": {"mod": "/r", "opcode": "0F61"},
    "xmmxmm": {"mod": "/r", "opcode": "660F61"},
    "xmmmem128": {"mod": "/r", "opcode": "660F61"},
}

PUNPCKLDQ = {
    "mmmm": {"mod": "/r", "opcode": "0F62"},
    "mmmem32": {"mod": "/r", "opcode": "0F62"},
    "xmmxmm": {"mod": "/r", "opcode": "660F62"},
    "xmmmem128": {"mod": "/r", "opcode": "660F62"},
}

PADDB = {
    "mmmm": {"mod": "/r", "opcode": "0FFC"},
    "mmmem64": {"mod": "/r", "opcode": "0FFC"},
    "xmmxmm": {"mod": "/r", "opcode": "660FFC"},
    "xmmmem128": {"mod": "/r", "opcode": "660FFC"},
}

PADDW = {
    "mmmm": {"mod": "/r", "opcode": "0FFD"},
    "mmmem64": {"mod": "/r", "opcode": "0FFD"},
    "xmmxmm": {"mod": "/r", "opcode": "660FFD"},
    "xmmmem128": {"mod": "/r", "opcode": "660FFD"},
}

PADDD = {
    "mmmm": {"mod": "/r", "opcode": "0FFE"},
    "mmmem64": {"mod": "/r", "opcode": "0FFE"},
    "xmmxmm": {"mod": "/r", "opcode": "660FFE"},
    "xmmmem128": {"mod": "/r", "opcode": "660FFE"},
}

PADDSB = {
    "mmmm": {"mod": "/r", "opcode": "0FEC"},
    "mmmem64": {"mod": "/r", "opcode": "0FEC"},
    "xmmxmm": {"mod": "/r", "opcode": "660FEC"},
    "xmmmem128": {"mod": "/r", "opcode": "660FEC"},
}

PADDSW = {
    "mmmm": {"mod": "/r", "opcode": "0FED"},
    "mmmem64": {"mod": "/r", "opcode": "0FED"},
    "xmmxmm": {"mod": "/r", "opcode": "660FED"},
    "xmmmem128": {"mod": "/r", "opcode": "660FED"},
}

PADDUSB = {
    "mmmm": {"mod": "/r", "opcode": "0FDC"},
    "mmmem64": {"mod": "/r", "opcode": "0FDC"},
    "xmmxmm": {"mod": "/r", "opcode": "660FDC"},
    "xmmmem128": {"mod": "/r", "opcode": "660FDC"},
}

PADDUSW = {
    "mmmm": {"mod": "/r", "opcode": "0FDD"},
    "mmmem64": {"mod": "/r", "opcode": "0FDD"},
    "xmmxmm": {"mod": "/r", "opcode": "660FDD"},
    "xmmmem128": {"mod": "/r", "opcode": "660FDD"},
}

PSUBB = {
    "mmmm": {"mod": "/r", "opcode": "0FF8"},
    "mmmem64": {"mod": "/r", "opcode": "0FF8"},
    "xmmxmm": {"mod": "/r", "opcode": "660FF8"},
    "xmmmem128": {"mod": "/r", "opcode": "660FF8"},
}

PSUBW = {
    "mmmm": {"mod": "/r", "opcode": "0FF9"},
    "mmmem64": {"mod": "/r", "opcode": "0FF9"},
    "xmmxmm": {"mod": "/r", "opcode": "660FF9"},
    "xmmmem128": {"mod": "/r", "opcode": "660FF9"},
}

PSUBD = {
    "mmmm": {"mod": "/r", "opcode": "0FFA"},
    "mmmem64": {"mod": "/r", "opcode": "0FFA"},
    "xmmxmm": {"mod": "/r", "opcode": "660FFA"},
    "xmmmem128": {"mod": "/r", "opcode": "660FFA"},
}

PSUBSB = {
    "mmmm": {"mod": "/r", "opcode": "0FE8"},
    "mmmem64": {"mod": "/r", "opcode": "0FE8"},
    "xmmxmm": {"mod": "/r", "opcode": "660FE8"},
    "xmmmem128": {"mod": "/r", "opcode": "660FE8"},
}

PSUBSW = {
    "mmmm": {"mod": "/r", "opcode": "0FE9"},
    "mmmem64": {"mod": "/r", "opcode": "0FE9"},
    "xmmxmm": {"mod": "/r", "opcode": "660FE9"},
    "xmmmem128": {"mod": "/r", "opcode": "660FE9"},
}

PSUBUSB = {
    "mmmm": {"mod": "/r", "opcode": "0FD8"},
    "mmmem64": {"mod": "/r", "opcode": "0FD8"},
    "xmmxmm": {"mod": "/r", "opcode": "660FD8"},
    "xmmmem128": {"mod": "/r", "opcode": "660FD8"},
}

PSUBUSW = {
    "mmmm": {"mod": "/r", "opcode": "0FD9"},
    "mmmem64": {"mod": "/r", "opcode": "0FD9"},
    "xmmxmm": {"mod": "/r", "opcode": "660FD9"},
    "xmmmem128": {"mod": "/r", "opcode": "660FD9"},
}

PMULHW = {
    "mmmm": {"mod": "/r", "opcode": "0FE5"},
    "mmmem64": {"mod": "/r", "opcode": "0FE5"},
    "xmmxmm": {"mod": "/r", "opcode": "660FE5"},
    "xmmmem128": {"mod": "/r", "opcode": "660FE5"},
}

PMULLW = {
    "mmmm": {"mod": "/r", "opcode": "0FD5"},
    "mmmem64": {"mod": "/r", "opcode": "0FD5"},
    "xmmxmm": {"mod": "/r", "opcode": "660FD5"},
    "xmmmem128": {"mod": "/r", "opcode": "660FD5"},
}

PMADDWD = {
    "mmmm": {"mod": "/r", "opcode": "0FF5"},
    "mmmem64": {"mod": "/r", "opcode": "0FF5"},
    "xmmxmm": {"mod": "/r", "opcode": "660FF5"},
    "xmmmem128": {"mod": "/r", "opcode": "660FF5"},
}

PCMPEQB = {
    "mmmm": {"mod": "/r", "opcode": "0F74"},
    "mmmem64": {"mod": "/r", "opcode": "0F74"},
    "xmmxmm": {"mod": "/r", "opcode": "660F74"},
    "xmmmem128": {"mod": "/r", "opcode": "660F74"},
}

PCMPEQW = {
    "mmmm": {"mod": "/r", "opcode": "0F75"},
    "mmmem64": {"mod": "/r", "opcode": "0F75"},
    "xmmxmm": {"mod": "/r", "opcode": "660F75"},
    "xmmmem128": {"mod": "/r", "opcode": "660F75"},
}

PCMPEQD = {
    "mmmm": {"mod": "/r", "opcode": "0F76"},
    "mmmem64": {"mod": "/r", "opcode": "0F76"},
    "xmmxmm": {"mod": "/r", "opcode": "660F76"},
    "xmmmem128": {"mod": "/r", "opcode": "660F76"},
}

PCMPGTB = {
    "mmmm": {"mod": "/r", "opcode": "0F64"},
    "mmmem64": {"mod": "/r", "opcode": "0F64"},
    "xmmxmm": {"mod": "/r", "opcode": "660F64"},
    "xmmmem128": {"mod": "/r", "opcode": "660F64"},
}

PCMPGTW = {
    "mmmm": {"mod": "/r", "opcode": "0F65"},
    "mmmem64": {"mod": "/r", "opcode": "0F65"},
    "xmmxmm": {"mod": "/r", "opcode": "660F65"},
    "xmmmem128": {"mod": "/r", "opcode": "660F65"},
}

PCMPGTD = {
    "mmmm": {"mod": "/r", "opcode": "0F66"},
    "mmmem64": {"mod": "/r", "opcode": "0F66"},
    "xmmxmm": {"mod": "/r", "opcode": "660F66"},
    "xmmmem128": {"mod": "/r", "opcode": "660F66"},
}

PAND = {
    "mmmm": {"mod": "/r", "opcode": "0FDB"},
    "mmmem64": {"mod": "/r", "opcode": "0FDB"},
    "xmmxmm": {"mod": "/r", "opcode": "660FDB"},
    "xmmmem128": {"mod": "/r", "opcode": "660FDB"},
}

PANDN = {
    "mmmm": {"mod": "/r", "opcode": "0FDF"},
    "mmmem64": {"mod": "/r", "opcode": "0FDF"},
    "xmmxmm": {"mod": "/r", "opcode": "660FDF"},
    "xmmmem128": {"mod": "/r", "opcode": "660FDF"},
}

POR = {
    "mmmm": {"mod": "/r", "opcode": "0FEB"},
    "mmmem64": {"mod": "/r", "opcode": "0FEB"},
    "xmmxmm": {"mod": "/r", "opcode": "660FEB"},
    "xmmmem128": {"mod": "/r", "opcode": "660FEB"},
}

PXOR = {
    "mmmm": {"mod": "/r", "opcode": "0FEF"},
    "mmmem64": {"mod": "/r", "opcode": "0FEF"},
    "xmmxmm": {"mod": "/r", "opcode": "660FEF"},
    "xmmmem128": {"mod": "/r", "opcode": "660FEF"},
}

PSLLW = {
    "mmmm": {"mod": "/r", "opcode": "0FF1"},
    "mmmem64": {"mod": "/r", "opcode": "0FF1"},
    "xmmxmm": {"mod": "/r", "opcode": "660FF1"},
    "xmmmem128": {"mod": "/r", "opcode": "660FF1"},
    "mmimm8": {"opcode": "0F71", "mod": "/6", "imm": "ib"},
    "xmmimm8": {"opcode": "660F71", "mod": "/6", "imm": "ib"},
}

PSLLD = {
    "mmmm": {"mod": "/r", "opcode": "0FF2"},
    "mmmem64": {"mod": "/r", "opcode": "0FF2"},
    "xmmxmm": {"mod": "/r", "opcode": "660FF2"},
    "xmmmem128": {"mod": "/r", "opcode": "660FF2"},
    "mmimm8": {"opcode": "0F72", "mod": "/6", "imm": "ib"},
    "xmmimm8": {"opcode": "660F72", "mod": "/6", "imm": "ib"},
}

PSLLQ = {
    "mmmm": {"mod": "/r", "opcode": "0FF3"},
    "mmmem64": {"mod": "/r", "opcode": "0FF3"},
    "xmmxmm": {"mod": "/r", "opcode": "660FF3"},
    "xmmmem128": {"mod": "/r", "opcode": "660FF3"},
    "mmimm8": {"opcode": "0F73", "mod": "/6", "imm": "ib"},
    "xmmimm8": {"opcode": "660F73", "mod": "/6", "imm": "ib"},
}

PSRLW = {
    "mmmm": {"mod": "/r", "opcode": "0FD1"},
    "mmmem64": {"mod": "/r", "opcode": "0FD1"},
    "xmmxmm": {"mod": "/r", "opcode": "660FD1"},
    "xmmmem128": {"mod": "/r", "opcode": "660FD1"},
    "mmimm8": {"opcode": "0F71", "mod": "/2", "imm": "ib"},
    "xmmimm8": {"opcode": "660F71", "mod": "/2", "imm": "ib"},
}

PSRLD = {
    "mmmm": {"mod": "/r", "opcode": "0FD2"},
    "mmmem64": {"mod": "/r", "opcode": "0FD2"},
    "xmmxmm": {"mod": "/r", "opcode": "660FD2"},
    "xmmmem128": {"mod": "/r", "opcode": "660FD2"},
    "mmimm8": {"opcode": "0F72", "mod": "/2", "imm": "ib"},
    "xmmimm8": {"opcode": "660F72", "mod": "/2", "imm": "ib"},
}

PSRLQ = {
    "mmmm": {"mod": "/r", "opcode": "0FD3"},
    "mmmem64": {"mod": "/r", "opcode": "0FD3"},
    "xmmxmm": {"mod": "/r", "opcode": "660FD3"},
    "xmmmem128": {"mod": "/r", "opcode": "660FD3"},
    "mmimm8": {"opcode": "0F73", "mod": "/2", "imm": "ib"},
    "xmmimm8": {"opcode": "660F73", "mod": "/2", "imm": "ib"},
}

PSRAW = {
    "mmmm": {"mod": "/r", "opcode": "0FE1"},
    "mmmem64": {"mod": "/r", "opcode": "0FE1"},
    "xmmxmm": {"mod": "/r", "opcode": "660FE1"},
    "xmmmem128": {"mod": "/r", "opcode": "660FE1"},
    "mmimm8": {"opcode": "0F71", "mod": "/4", "imm": "ib"},
    "xmmimm8": {"opcode": "660F71", "mod": "/4", "imm": "ib"},
}

PSRAD = {
    "mmmm": {"mod": "/r", "opcode": "0FE2"},
    "mmmem64": {"mod": "/r", "opcode": "0FE2"},
    "xmmxmm": {"mod": "/r", "opcode": "660FE2"},
    "xmmmem128": {"mod": "/r", "opcode": "660FE2"},
    "mmimm8": {"opcode": "0F72", "mod": "/4", "imm": "ib"},
    "xmmimm8": {"opcode": "660F72", "mod": "/4", "imm": "ib"},
}

EMMS = {"no_op": {"opcode": "0F77"}}
