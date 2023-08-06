
# DATA TRANSFER INSTRUCTIONS

MOV = {
    "mem8r8": {"mod": "/r", "opcode": "88", "prefix": "REX"},
    "mem16r16": {"mod": "/r", "opcode": "89", "prefix": "66"},
    "mem32r32": {"mod": "/r", "opcode": "89"},
    "mem64r64": {"mod": "/r", "opcode": "89", "prefix": "REX.W"},
    "r8mem8": {"mod": "/r", "opcode": "8A", "prefix": "REX"},
    "r8r8": {"mod": "/r", "opcode": "8A", "prefix": "REX"},
    "r16mem16": {"mod": "/r", "opcode": "8B", "prefix": "66"},
    "r16r16": {"mod": "/r", "opcode": "8B", "prefix": "66"},
    "r32mem32": {"mod": "/r", "opcode": "8B"},
    "r32r32": {"mod": "/r", "opcode": "8B"},
    "r64mem64": {"mod": "/r", "opcode": "8B", "prefix": "REX.W"},
    "r64r64": {"mod": "/r", "opcode": "8B", "prefix": "REX.W"},
    "r8imm8": {"opcode": "B0", "prefix": "REX", "post": "+rb", "imm": "ib"},
    "r16imm16": {"opcode": "B8", "prefix": "66", "post": "+rw", "imm": "iw"},
    "r32imm32": {"opcode": "B8", "post": "+rd", "imm": "id"},
    "r64imm64": {"opcode": "B8", "prefix": "REX.W", "post": "+rd", "imm": "io"},
    "r64imm32": {"opcode": "C7", "mod": "/0", "prefix": "REX.W", "imm": "id", "sign_ext": "4"},
    "mem8imm8": {"opcode": "C6", "mod": "/0", "prefix": "REX", "imm": "ib"},
    "mem16imm16": {"opcode": "C7", "mod": "/0", "prefix": "66", "imm": "iw"},
    "mem32imm32": {"opcode": "C7", "mod": "/0", "imm": "id"},
    "mem64imm32": {"opcode": "C7", "mod": "/0", "prefix": "REX.W", "imm": "id", "sign_ext": "4"}
}

CMOVA = {
    "r16mem16": {"mod": "/r", "opcode": "0F47", "prefix": "66"},
    "r16r16": {"mod": "/r", "opcode": "0F47", "prefix": "66"},
    "r32mem32": {"mod": "/r", "opcode": "0F47"},
    "r32r32": {"mod": "/r", "opcode": "0F47"},
    "r64mem64": {"mod": "/r", "opcode": "0F47", "prefix": "REX.W"},
    "r64r64": {"mod": "/r", "opcode": "0F47", "prefix": "REX.W"},
}

CMOVAE = {
    "r16mem16": {"mod": "/r", "opcode": "0F43", "prefix": "66"},
    "r16r16": {"mod": "/r", "opcode": "0F43", "prefix": "66"},
    "r32mem32": {"mod": "/r", "opcode": "0F43"},
    "r32r32": {"mod": "/r", "opcode": "0F43"},
    "r64mem64": {"mod": "/r", "opcode": "0F43", "prefix": "REX.W"},
    "r64r64": {"mod": "/r", "opcode": "0F43", "prefix": "REX.W"},
}

CMOVB = {
    "r16mem16": {"mod": "/r", "opcode": "0F42", "prefix": "66"},
    "r16r16": {"mod": "/r", "opcode": "0F42", "prefix": "66"},
    "r32mem32": {"mod": "/r", "opcode": "0F42"},
    "r32r32": {"mod": "/r", "opcode": "0F42"},
    "r64mem64": {"mod": "/r", "opcode": "0F42", "prefix": "REX.W"},
    "r64r64": {"mod": "/r", "opcode": "0F42", "prefix": "REX.W"},
}

CMOVBE = {
    "r16mem16": {"mod": "/r", "opcode": "0F46", "prefix": "66"},
    "r16r16": {"mod": "/r", "opcode": "0F46", "prefix": "66"},
    "r32mem32": {"mod": "/r", "opcode": "0F46"},
    "r32r32": {"mod": "/r", "opcode": "0F46"},
    "r64mem64": {"mod": "/r", "opcode": "0F46", "prefix": "REX.W"},
    "r64r64": {"mod": "/r", "opcode": "0F46", "prefix": "REX.W"},
}

CMOVC = {
    "r16mem16": {"mod": "/r", "opcode": "0F42", "prefix": "66"},
    "r16r16": {"mod": "/r", "opcode": "0F42", "prefix": "66"},
    "r32mem32": {"mod": "/r", "opcode": "0F42"},
    "r32r32": {"mod": "/r", "opcode": "0F42"},
    "r64mem64": {"mod": "/r", "opcode": "0F42", "prefix": "REX.W"},
    "r64r64": {"mod": "/r", "opcode": "0F42", "prefix": "REX.W"},
}

CMOVE = {
    "r16mem16": {"mod": "/r", "opcode": "0F44", "prefix": "66"},
    "r16r16": {"mod": "/r", "opcode": "0F44", "prefix": "66"},
    "r32mem32": {"mod": "/r", "opcode": "0F44"},
    "r32r32": {"mod": "/r", "opcode": "0F44"},
    "r64mem64": {"mod": "/r", "opcode": "0F44", "prefix": "REX.W"},
    "r64r64": {"mod": "/r", "opcode": "0F44", "prefix": "REX.W"},
}

CMOVG = {
    "r16mem16": {"mod": "/r", "opcode": "0F4F", "prefix": "66"},
    "r16r16": {"mod": "/r", "opcode": "0F4F", "prefix": "66"},
    "r32mem32": {"mod": "/r", "opcode": "0F4F"},
    "r32r32": {"mod": "/r", "opcode": "0F4F"},
    "r64mem64": {"mod": "/r", "opcode": "0F4F", "prefix": "REX.W"},
    "r64r64": {"mod": "/r", "opcode": "0F4F", "prefix": "REX.W"},
}

CMOVGE = {
    "r16mem16": {"mod": "/r", "opcode": "0F4D", "prefix": "66"},
    "r16r16": {"mod": "/r", "opcode": "0F4D", "prefix": "66"},
    "r32mem32": {"mod": "/r", "opcode": "0F4D"},
    "r32r32": {"mod": "/r", "opcode": "0F4D"},
    "r64mem64": {"mod": "/r", "opcode": "0F4D", "prefix": "REX.W"},
    "r64r64": {"mod": "/r", "opcode": "0F4D", "prefix": "REX.W"},
}

CMOVL = {
    "r16mem16": {"mod": "/r", "opcode": "0F4C", "prefix": "66"},
    "r16r16": {"mod": "/r", "opcode": "0F4C", "prefix": "66"},
    "r32mem32": {"mod": "/r", "opcode": "0F4C"},
    "r32r32": {"mod": "/r", "opcode": "0F4C"},
    "r64mem64": {"mod": "/r", "opcode": "0F4C", "prefix": "REX.W"},
    "r64r64": {"mod": "/r", "opcode": "0F4C", "prefix": "REX.W"},
}

CMOVLE = {
    "r16mem16": {"mod": "/r", "opcode": "0F4E", "prefix": "66"},
    "r16r16": {"mod": "/r", "opcode": "0F4E", "prefix": "66"},
    "r32mem32": {"mod": "/r", "opcode": "0F4E"},
    "r32r32": {"mod": "/r", "opcode": "0F4E"},
    "r64mem64": {"mod": "/r", "opcode": "0F4E", "prefix": "REX.W"},
    "r64r64": {"mod": "/r", "opcode": "0F4E", "prefix": "REX.W"},
}

CMOVNA = {
    "r16mem16": {"mod": "/r", "opcode": "0F46", "prefix": "66"},
    "r16r16": {"mod": "/r", "opcode": "0F46", "prefix": "66"},
    "r32mem32": {"mod": "/r", "opcode": "0F46"},
    "r32r32": {"mod": "/r", "opcode": "0F46"},
    "r64mem64": {"mod": "/r", "opcode": "0F46", "prefix": "REX.W"},
    "r64r64": {"mod": "/r", "opcode": "0F46", "prefix": "REX.W"},
}

CMOVNAE = {
    "r16mem16": {"mod": "/r", "opcode": "0F42", "prefix": "66"},
    "r16r16": {"mod": "/r", "opcode": "0F42", "prefix": "66"},
    "r32mem32": {"mod": "/r", "opcode": "0F42"},
    "r32r32": {"mod": "/r", "opcode": "0F42"},
    "r64mem64": {"mod": "/r", "opcode": "0F42", "prefix": "REX.W"},
    "r64r64": {"mod": "/r", "opcode": "0F42", "prefix": "REX.W"},
}

CMOVNB = {
    "r16mem16": {"mod": "/r", "opcode": "0F43", "prefix": "66"},
    "r16r16": {"mod": "/r", "opcode": "0F43", "prefix": "66"},
    "r32mem32": {"mod": "/r", "opcode": "0F43"},
    "r32r32": {"mod": "/r", "opcode": "0F43"},
    "r64mem64": {"mod": "/r", "opcode": "0F43", "prefix": "REX.W"},
    "r64r64": {"mod": "/r", "opcode": "0F43", "prefix": "REX.W"},
}

CMOVNBE = {
    "r16mem16": {"mod": "/r", "opcode": "0F47", "prefix": "66"},
    "r16r16": {"mod": "/r", "opcode": "0F47", "prefix": "66"},
    "r32mem32": {"mod": "/r", "opcode": "0F47"},
    "r32r32": {"mod": "/r", "opcode": "0F47"},
    "r64mem64": {"mod": "/r", "opcode": "0F47", "prefix": "REX.W"},
    "r64r64": {"mod": "/r", "opcode": "0F47", "prefix": "REX.W"},
}

CMOVNC = {
    "r16mem16": {"mod": "/r", "opcode": "0F43", "prefix": "66"},
    "r16r16": {"mod": "/r", "opcode": "0F43", "prefix": "66"},
    "r32mem32": {"mod": "/r", "opcode": "0F43"},
    "r32r32": {"mod": "/r", "opcode": "0F43"},
    "r64mem64": {"mod": "/r", "opcode": "0F43", "prefix": "REX.W"},
    "r64r64": {"mod": "/r", "opcode": "0F43", "prefix": "REX.W"},
}

CMOVNE = {
    "r16mem16": {"mod": "/r", "opcode": "0F45", "prefix": "66"},
    "r16r16": {"mod": "/r", "opcode": "0F45", "prefix": "66"},
    "r32mem32": {"mod": "/r", "opcode": "0F45"},
    "r32r32": {"mod": "/r", "opcode": "0F45"},
    "r64mem64": {"mod": "/r", "opcode": "0F45", "prefix": "REX.W"},
    "r64r64": {"mod": "/r", "opcode": "0F45", "prefix": "REX.W"},
}

CMOVNG = {
    "r16mem16": {"mod": "/r", "opcode": "0F4E", "prefix": "66"},
    "r16r16": {"mod": "/r", "opcode": "0F4E", "prefix": "66"},
    "r32mem32": {"mod": "/r", "opcode": "0F4E"},
    "r32r32": {"mod": "/r", "opcode": "0F4E"},
    "r64mem64": {"mod": "/r", "opcode": "0F4E", "prefix": "REX.W"},
    "r64r64": {"mod": "/r", "opcode": "0F4E", "prefix": "REX.W"},
}

CMOVNGE = {
    "r16mem16": {"mod": "/r", "opcode": "0F4C", "prefix": "66"},
    "r16r16": {"mod": "/r", "opcode": "0F4C", "prefix": "66"},
    "r32mem32": {"mod": "/r", "opcode": "0F4C"},
    "r32r32": {"mod": "/r", "opcode": "0F4C"},
    "r64mem64": {"mod": "/r", "opcode": "0F4C", "prefix": "REX.W"},
    "r64r64": {"mod": "/r", "opcode": "0F4C", "prefix": "REX.W"},
}

CMOVNL = {
    "r16mem16": {"mod": "/r", "opcode": "0F4D", "prefix": "66"},
    "r16r16": {"mod": "/r", "opcode": "0F4D", "prefix": "66"},
    "r32mem32": {"mod": "/r", "opcode": "0F4D"},
    "r32r32": {"mod": "/r", "opcode": "0F4D"},
    "r64mem64": {"mod": "/r", "opcode": "0F4D", "prefix": "REX.W"},
    "r64r64": {"mod": "/r", "opcode": "0F4D", "prefix": "REX.W"},
}

CMOVNLE = {
    "r16mem16": {"mod": "/r", "opcode": "0F4F", "prefix": "66"},
    "r16r16": {"mod": "/r", "opcode": "0F4F", "prefix": "66"},
    "r32mem32": {"mod": "/r", "opcode": "0F4F"},
    "r32r32": {"mod": "/r", "opcode": "0F4F"},
    "r64mem64": {"mod": "/r", "opcode": "0F4F", "prefix": "REX.W"},
    "r64r64": {"mod": "/r", "opcode": "0F4F", "prefix": "REX.W"},
}

CMOVNO = {
    "r16mem16": {"mod": "/r", "opcode": "0F41", "prefix": "66"},
    "r16r16": {"mod": "/r", "opcode": "0F41", "prefix": "66"},
    "r32mem32": {"mod": "/r", "opcode": "0F41"},
    "r32r32": {"mod": "/r", "opcode": "0F41"},
    "r64mem64": {"mod": "/r", "opcode": "0F41", "prefix": "REX.W"},
    "r64r64": {"mod": "/r", "opcode": "0F41", "prefix": "REX.W"},
}

CMOVNP = {
    "r16mem16": {"mod": "/r", "opcode": "0F4B", "prefix": "66"},
    "r16r16": {"mod": "/r", "opcode": "0F4B", "prefix": "66"},
    "r32mem32": {"mod": "/r", "opcode": "0F4B"},
    "r32r32": {"mod": "/r", "opcode": "0F4B"},
    "r64mem64": {"mod": "/r", "opcode": "0F4B", "prefix": "REX.W"},
    "r64r64": {"mod": "/r", "opcode": "0F4B", "prefix": "REX.W"},
}

CMOVNS = {
    "r16mem16": {"mod": "/r", "opcode": "0F49", "prefix": "66"},
    "r16r16": {"mod": "/r", "opcode": "0F49", "prefix": "66"},
    "r32mem32": {"mod": "/r", "opcode": "0F49"},
    "r32r32": {"mod": "/r", "opcode": "0F49"},
    "r64mem64": {"mod": "/r", "opcode": "0F49", "prefix": "REX.W"},
    "r64r64": {"mod": "/r", "opcode": "0F49", "prefix": "REX.W"},
}

CMOVNZ = {
    "r16mem16": {"mod": "/r", "opcode": "0F45", "prefix": "66"},
    "r16r16": {"mod": "/r", "opcode": "0F45", "prefix": "66"},
    "r32mem32": {"mod": "/r", "opcode": "0F45"},
    "r32r32": {"mod": "/r", "opcode": "0F45"},
    "r64mem64": {"mod": "/r", "opcode": "0F45", "prefix": "REX.W"},
    "r64r64": {"mod": "/r", "opcode": "0F45", "prefix": "REX.W"},
}

CMOVO = {
    "r16mem16": {"mod": "/r", "opcode": "0F40", "prefix": "66"},
    "r16r16": {"mod": "/r", "opcode": "0F40", "prefix": "66"},
    "r32mem32": {"mod": "/r", "opcode": "0F40"},
    "r32r32": {"mod": "/r", "opcode": "0F40"},
    "r64mem64": {"mod": "/r", "opcode": "0F40", "prefix": "REX.W"},
    "r64r64": {"mod": "/r", "opcode": "0F40", "prefix": "REX.W"},
}

CMOVP = {
    "r16mem16": {"mod": "/r", "opcode": "0F4A", "prefix": "66"},
    "r16r16": {"mod": "/r", "opcode": "0F4A", "prefix": "66"},
    "r32mem32": {"mod": "/r", "opcode": "0F4A"},
    "r32r32": {"mod": "/r", "opcode": "0F4A"},
    "r64mem64": {"mod": "/r", "opcode": "0F4A", "prefix": "REX.W"},
    "r64r64": {"mod": "/r", "opcode": "0F4A", "prefix": "REX.W"},
}

CMOVPE = {
    "r16mem16": {"mod": "/r", "opcode": "0F4A", "prefix": "66"},
    "r16r16": {"mod": "/r", "opcode": "0F4A", "prefix": "66"},
    "r32mem32": {"mod": "/r", "opcode": "0F4A"},
    "r32r32": {"mod": "/r", "opcode": "0F4A"},
    "r64mem64": {"mod": "/r", "opcode": "0F4A", "prefix": "REX.W"},
    "r64r64": {"mod": "/r", "opcode": "0F4A", "prefix": "REX.W"},
}

CMOVPO = {
    "r16mem16": {"mod": "/r", "opcode": "0F4B", "prefix": "66"},
    "r16r16": {"mod": "/r", "opcode": "0F4B", "prefix": "66"},
    "r32mem32": {"mod": "/r", "opcode": "0F4B"},
    "r32r32": {"mod": "/r", "opcode": "0F4B"},
    "r64mem64": {"mod": "/r", "opcode": "0F4B", "prefix": "REX.W"},
    "r64r64": {"mod": "/r", "opcode": "0F4B", "prefix": "REX.W"},
}

CMOVS = {
    "r16mem16": {"mod": "/r", "opcode": "0F48", "prefix": "66"},
    "r16r16": {"mod": "/r", "opcode": "0F48", "prefix": "66"},
    "r32mem32": {"mod": "/r", "opcode": "0F48"},
    "r32r32": {"mod": "/r", "opcode": "0F48"},
    "r64mem64": {"mod": "/r", "opcode": "0F48", "prefix": "REX.W"},
    "r64r64": {"mod": "/r", "opcode": "0F48", "prefix": "REX.W"},
}

CMOVZ = {
    "r16mem16": {"mod": "/r", "opcode": "0F44", "prefix": "66"},
    "r16r16": {"mod": "/r", "opcode": "0F44", "prefix": "66"},
    "r32mem32": {"mod": "/r", "opcode": "0F44"},
    "r32r32": {"mod": "/r", "opcode": "0F44"},
    "r64mem64": {"mod": "/r", "opcode": "0F44", "prefix": "REX.W"},
    "r64r64": {"mod": "/r", "opcode": "0F44", "prefix": "REX.W"},
}

XCHG = {
    "AXr16": {"opcode": "90", "prefix": "66", "post": "+rw"},
    "r16AX": {"opcode": "90", "prefix": "66", "post": "+rw"},
    "EAXr32": {"opcode": "90", "post": "+rd"},
    "RAXr64": {"opcode": "90", "prefix": "REX.W", "post": "+rd"},
    "r32EAX": {"opcode": "90", "post": "+rd"},
    "r64RAX": {"opcode": "90", "prefix": "REX.W", "post": "+rd"},

    "mem8r8": {"mod": "/r", "opcode": "86", "prefix": "REX"},
    "mem16r16": {"mod": "/r", "opcode": "87", "prefix": "66"},
    "mem32r32": {"mod": "/r", "opcode": "87"},
    "mem64r64": {"mod": "/r", "opcode": "87", "prefix": "REX.W"},
    "r8mem8": {"mod": "/r", "opcode": "86", "prefix": "REX"},
    "r8r8": {"mod": "/r", "opcode": "86", "prefix": "REX"},
    "r16mem16": {"mod": "/r", "opcode": "87", "prefix": "66"},
    "r16r16": {"mod": "/r", "opcode": "87", "prefix": "66"},
    "r32mem32": {"mod": "/r", "opcode": "87"},
    "r32r32": {"mod": "/r", "opcode": "87"},
    "r64mem64": {"mod": "/r", "opcode": "87", "prefix": "REX.W"},
    "r64r64": {"mod": "/r", "opcode": "87", "prefix": "REX.W"},
}

BSWAP = {
    "r32": {"opcode": "0FC8", "post": "+rd"},
    "r64": {"opcode": "0FC8", "prefix": "REX.W", "post": "+rd"},
}

XADD = {
    "r8r8": {"mod": "/r", "opcode": "0FC0", "prefix": "REX", "rm": "1"},
    "mem8r8": {"mod": "/r", "opcode": "0FC0", "prefix": "REX"},
    "r16r16": {"mod": "/r", "opcode": "0FC1", "prefix": "66", "rm": "1"},
    "mem16r16": {"mod": "/r", "opcode": "0FC1", "prefix": "66"},
    "r32r32": {"mod": "/r", "opcode": "0FC1", "rm": "1"},
    "mem32r32": {"mod": "/r", "opcode": "0FC1"},
    "r64r64": {"mod": "/r", "opcode": "0FC1", "prefix": "REX.W", "rm": "1"},
    "mem64r64": {"mod": "/r", "opcode": "0FC1", "prefix": "REX.W"},
}

CMPXCHG = {
    "r8r8": {"opcode": "0FB0", "prefix": "REX", "mod": "/r", 'rm': '1'},
    "r16r16": {"opcode": "0FB1", "prefix": "66", "mod": "/r", 'rm': '1'},
    "r32r32": {"opcode": "0FB1", "mod": "/r", 'rm': '1'},
    "r64r64": {"opcode": "0FB1", "prefix": "REX.W", "mod": "/r", 'rm': '1'},
    "mem8r8": {"opcode": "0FB0", "prefix": "REX", "mod": "/r"},
    "mem16r16": {"opcode": "0FB1", "prefix": "66", "mod": "/r"},
    "mem32r32": {"opcode": "0FB1", "mod": "/r"},
    "mem64r64": {"opcode": "0FB1", "prefix": "REX.W", "mod": "/r"},
}

CMPXCHG8B = {
    "mem64": {"opcode": "0FC7", "mod": "/1"}
}

PUSH = {
    "r64": {"opcode": "50", "post": "+rd"},
    "mem64": {"opcode": "FF", "mod": "/6"},
    "imm8": {"opcode": "6A", "imm": "ib", "sign_ext": "1"},
    "imm32": {"opcode": "68", "imm": "id", "sign_ext": "4"},
}

POP = {
    "r64": {"opcode": "58", "post": "+rd"},
    "mem64": {"opcode": "8F", "mod": "/0"},
}

CWD = {"no_op": {"opcode": "99", "prefix": "66"}}
CDQ = {"no_op": {"opcode": "99"}}
CQO = {"no_op": {"opcode": "99", "prefix": "REX.W"}}

CBW = {"no_op": {"opcode": "98", "prefix": "66"}}
CWDE = {"no_op": {"opcode": "98"}}
CDQE = {"no_op": {"opcode": "98", "prefix": "REX.W"}}

MOVSX = {
    "r16r8": {"mod": "/r", "opcode": "0FBE", "prefix": "66"},
    "r16mem8": {"mod": "/r", "opcode": "0FBE", "prefix": "66"},
    "r32r8": {"mod": "/r", "opcode": "0FBE"},
    "r32mem8": {"mod": "/r", "opcode": "0FBE"},
    "r64r8": {"mod": "/r", "opcode": "0FBE", "prefix": "REX.W"},
    "r64mem8": {"mod": "/r", "opcode": "0FBE", "prefix": "REX.W"},

    "r32r16": {"mod": "/r", "opcode": "0FBF"},
    "r32mem16": {"mod": "/r", "opcode": "0FBF"},
    "r64r16": {"mod": "/r", "opcode": "0FBF", "prefix": "REX.W"},
    "r64mem16": {"mod": "/r", "opcode": "0FBF", "prefix": "REX.W"},

    "r64r32": {"mod": "/r", "opcode": "63", "prefix": "REX.W"},
    "r64mem32": {"mod": "/r", "opcode": "63", "prefix": "REX.W"},
}

MOVZX = {
    "r16r8": {"mod": "/r", "opcode": "0FB6", "prefix": "66"},
    "r16mem8": {"mod": "/r", "opcode": "0FB6", "prefix": "66"},
    "r32r8": {"mod": "/r", "opcode": "0FB6"},
    "r32mem8": {"mod": "/r", "opcode": "0FB6"},
    "r64r8": {"mod": "/r", "opcode": "0FB6", "prefix": "REX.W"},
    "r64mem8": {"mod": "/r", "opcode": "0FB6", "prefix": "REX.W"},

    "r32r16": {"mod": "/r", "opcode": "0FB7"},
    "r32mem16": {"mod": "/r", "opcode": "0FB7"},
    "r64r16": {"mod": "/r", "opcode": "0FB7", "prefix": "REX.W"},
    "r64mem16": {"mod": "/r", "opcode": "0FB7", "prefix": "REX.W"},
}

# Binary Arithmetic Instructions

ADCX = {
    "r32r32": {"opcode": "660F38F6", "mod": "/r"},
    "r32mem32": {"opcode": "660F38F6", "mod": "/r"},
    "r64r64": {"opcode": "660F38F6", "prefix": "REX.W", "mod": "/r"},
    "r64mem64": {"opcode": "660F38F6", "prefix": "REX.W", "mod": "/r"},
}

ADOX = {
    "r32r32": {"opcode": "F30F38F6", "mod": "/r"},
    "r32mem32": {"opcode": "F30F38F6", "mod": "/r"},
    "r64r64": {"opcode": "F30F38F6", "prefix": "REX.W", "mod": "/r"},
    "r64mem64": {"opcode": "F30F38F6", "prefix": "REX.W", "mod": "/r"},
}

ADD = {
    "ALimm8": {"opcode": "04", "imm": "ib"},
    "AXimm16": {"opcode": "05", "prefix": "66", "imm": "iw"},
    "EAXimm32": {"opcode": "05", "imm": "id"},
    "RAXimm32": {"opcode": "05", "prefix": "REX.W", "imm": "id", "sign_ext": "4"},
    "r8imm8": {"opcode": "80", "mod": "/0", "prefix": "REX", "imm": "ib"},
    "r16imm16": {"opcode": "81", "mod": "/0", "prefix": "66", "imm": "iw"},
    "r32imm32": {"opcode": "81", "mod": "/0", "imm": "id"},
    "r64imm32": {"opcode": "81", "mod": "/0", "prefix": "REX.W", "imm": "id", "sign_ext": "4"},
    "mem8imm8": {"opcode": "80", "mod": "/0", "prefix": "REX", "imm": "ib"},
    "mem16imm16": {"opcode": "81", "mod": "/0", "prefix": "66", "imm": "iw"},
    "mem32imm32": {"opcode": "81", "mod": "/0", "imm": "id"},
    "mem64imm32": {"opcode": "81", "mod": "/0", "prefix": "REX.W", "imm": "id"},
    "r16imm8": {"opcode": "83", "mod": "/0", "prefix": "66", "imm": "ib", "sign_ext": "1"},
    "r32imm8": {"opcode": "83", "mod": "/0", "imm": "ib", "sign_ext": "1"},
    "r64imm8": {"opcode": "83", "mod": "/0", "prefix": "REX.W", "imm": "ib", "sign_ext": "1"},
    "mem16imm8": {"opcode": "83", "mod": "/0", "prefix": "66", "imm": "ib", "sign_ext": "1"},
    "mem32imm8": {"opcode": "83", "mod": "/0", "imm": "ib", "sign_ext": "1"},
    "mem64imm8": {"opcode": "83", "mod": "/0", "prefix": "REX.W", "imm": "ib", "sign_ext": "1"},

    "mem8r8": {"opcode": "00", "prefix": "REX", "mod": "/r"},
    "mem16r16": {"opcode": "01", "prefix": "66", "mod": "/r"},
    "mem32r32": {"opcode": "01", "mod": "/r"},
    "mem64r64": {"opcode": "01", "prefix": "REX.W", "mod": "/r"},

    "r8r8": {"opcode": "02", "prefix": "REX", "mod": "/r"},
    "r16r16": {"opcode": "03", "prefix": "66", "mod": "/r"},
    "r32r32": {"opcode": "03", "mod": "/r"},
    "r64r64": {"opcode": "03", "prefix": "REX.W", "mod": "/r"},
    "r8mem8": {"opcode": "02", "prefix": "REX", "mod": "/r"},
    "r16mem16": {"opcode": "03", "prefix": "66", "mod": "/r"},
    "r32mem32": {"opcode": "03", "mod": "/r"},
    "r64mem64": {"opcode": "03", "prefix": "REX.W", "mod": "/r"},
}

ADC = {
    "ALimm8": {"opcode": "14", "imm": "ib"},
    "AXimm16": {"opcode": "15", "prefix": "66", "imm": "iw"},
    "EAXimm32": {"opcode": "15", "imm": "id"},
    "RAXimm32": {"opcode": "15", "prefix": "REX.W", "imm": "id", "sign_ext": "4"},
    "r8imm8": {"opcode": "80", "mod": "/2", "prefix": "REX", "imm": "ib"},
    "r16imm16": {"opcode": "81", "mod": "/2", "prefix": "66", "imm": "iw"},
    "r32imm32": {"opcode": "81", "mod": "/2", "imm": "id"},
    "r64imm32": {"opcode": "81", "mod": "/2", "prefix": "REX.W", "imm": "id", "sign_ext": "4"},
    "mem8imm8": {"opcode": "80", "mod": "/2", "prefix": "REX", "imm": "ib"},
    "mem16imm16": {"opcode": "81", "mod": "/2", "prefix": "66", "imm": "iw"},
    "mem32imm32": {"opcode": "81", "mod": "/2", "imm": "id"},
    "mem64imm32": {"opcode": "81", "mod": "/2", "prefix": "REX.W", "imm": "id"},
    "r16imm8": {"opcode": "83", "mod": "/2", "prefix": "66", "imm": "ib", "sign_ext": "1"},
    "r32imm8": {"opcode": "83", "mod": "/2", "imm": "ib", "sign_ext": "1"},
    "r64imm8": {"opcode": "83", "mod": "/2", "prefix": "REX.W", "imm": "ib", "sign_ext": "1"},
    "mem16imm8": {"opcode": "83", "mod": "/2", "prefix": "66", "imm": "ib", "sign_ext": "1"},
    "mem32imm8": {"opcode": "83", "mod": "/2", "imm": "ib", "sign_ext": "1"},
    "mem64imm8": {"opcode": "83", "mod": "/2", "prefix": "REX.W", "imm": "ib", "sign_ext": "1"},

    "mem8r8": {"opcode": "10", "prefix": "REX", "mod": "/r"},
    "mem16r16": {"opcode": "11", "prefix": "66", "mod": "/r"},
    "mem32r32": {"opcode": "11", "mod": "/r"},
    "mem64r64": {"opcode": "11", "prefix": "REX.W", "mod": "/r"},

    "r8r8": {"opcode": "12", "prefix": "REX", "mod": "/r"},
    "r16r16": {"opcode": "13", "prefix": "66", "mod": "/r"},
    "r32r32": {"opcode": "13", "mod": "/r"},
    "r64r64": {"opcode": "13", "prefix": "REX.W", "mod": "/r"},
    "r8mem8": {"opcode": "12", "prefix": "REX", "mod": "/r"},
    "r16mem16": {"opcode": "13", "prefix": "66", "mod": "/r"},
    "r32mem32": {"opcode": "13", "mod": "/r"},
    "r64mem64": {"opcode": "13", "prefix": "REX.W", "mod": "/r"},
}

SUB = {
    "ALimm8": {"opcode": "2C", "imm": "ib"},
    "AXimm16": {"opcode": "2D", "prefix": "66", "imm": "iw"},
    "EAXimm32": {"opcode": "2D", "imm": "id"},
    "RAXimm32": {"opcode": "2D", "prefix": "REX.W", "imm": "id", "sign_ext": "4"},
    "r8imm8": {"opcode": "80", "mod": "/5", "prefix": "REX", "imm": "ib"},
    "r16imm16": {"opcode": "81", "mod": "/5", "prefix": "66", "imm": "iw"},
    "r32imm32": {"opcode": "81", "mod": "/5", "imm": "id"},
    "r64imm32": {"opcode": "81", "mod": "/5", "prefix": "REX.W", "imm": "id", "sign_ext": "4"},
    "mem8imm8": {"opcode": "80", "mod": "/5", "prefix": "REX", "imm": "ib"},
    "mem16imm16": {"opcode": "81", "mod": "/5", "prefix": "66", "imm": "iw"},
    "mem32imm32": {"opcode": "81", "mod": "/5", "imm": "id"},
    "mem64imm32": {"opcode": "81", "mod": "/5", "prefix": "REX.W", "imm": "id"},
    "r16imm8": {"opcode": "83", "mod": "/5", "prefix": "66", "imm": "ib", "sign_ext": "1"},
    "r32imm8": {"opcode": "83", "mod": "/5", "imm": "ib", "sign_ext": "1"},
    "r64imm8": {"opcode": "83", "mod": "/5", "prefix": "REX.W", "imm": "ib", "sign_ext": "1"},
    "mem16imm8": {"opcode": "83", "mod": "/5", "prefix": "66", "imm": "ib", "sign_ext": "1"},
    "mem32imm8": {"opcode": "83", "mod": "/5", "imm": "ib", "sign_ext": "1"},
    "mem64imm8": {"opcode": "83", "mod": "/5", "prefix": "REX.W", "imm": "ib", "sign_ext": "1"},

    "mem8r8": {"opcode": "28", "prefix": "REX", "mod": "/r"},
    "mem16r16": {"opcode": "29", "prefix": "66", "mod": "/r"},
    "mem32r32": {"opcode": "29", "mod": "/r"},
    "mem64r64": {"opcode": "29", "prefix": "REX.W", "mod": "/r"},

    "r8r8": {"opcode": "2A", "prefix": "REX", "mod": "/r"},
    "r16r16": {"opcode": "2B", "prefix": "66", "mod": "/r"},
    "r32r32": {"opcode": "2B", "mod": "/r"},
    "r64r64": {"opcode": "2B", "prefix": "REX.W", "mod": "/r"},
    "r8mem8": {"opcode": "2A", "prefix": "REX", "mod": "/r"},
    "r16mem16": {"opcode": "2B", "prefix": "66", "mod": "/r"},
    "r32mem32": {"opcode": "2B", "mod": "/r"},
    "r64mem64": {"opcode": "2B", "prefix": "REX.W", "mod": "/r"},
}

SBB = {
    "ALimm8": {"opcode": "1C", "imm": "ib"},
    "AXimm16": {"opcode": "1D", "prefix": "66", "imm": "iw"},
    "EAXimm32": {"opcode": "1D", "imm": "id"},
    "RAXimm32": {"opcode": "1D", "prefix": "REX.W", "imm": "id", "sign_ext": "4"},
    "r8imm8": {"opcode": "80", "mod": "/3", "prefix": "REX", "imm": "ib"},
    "r16imm16": {"opcode": "81", "mod": "/3", "prefix": "66", "imm": "iw"},
    "r32imm32": {"opcode": "81", "mod": "/3", "imm": "id"},
    "r64imm32": {"opcode": "81", "mod": "/3", "prefix": "REX.W", "imm": "id", "sign_ext": "4"},
    "mem8imm8": {"opcode": "80", "mod": "/3", "prefix": "REX", "imm": "ib"},
    "mem16imm16": {"opcode": "81", "mod": "/3", "prefix": "66", "imm": "iw"},
    "mem32imm32": {"opcode": "81", "mod": "/3", "imm": "id"},
    "mem64imm32": {"opcode": "81", "mod": "/3", "prefix": "REX.W", "imm": "id"},
    "r16imm8": {"opcode": "83", "mod": "/3", "prefix": "66", "imm": "ib", "sign_ext": "1"},
    "r32imm8": {"opcode": "83", "mod": "/3", "imm": "ib", "sign_ext": "1"},
    "r64imm8": {"opcode": "83", "mod": "/3", "prefix": "REX.W", "imm": "ib", "sign_ext": "1"},
    "mem16imm8": {"opcode": "83", "mod": "/3", "prefix": "66", "imm": "ib", "sign_ext": "1"},
    "mem32imm8": {"opcode": "83", "mod": "/3", "imm": "ib", "sign_ext": "1"},
    "mem64imm8": {"opcode": "83", "mod": "/3", "prefix": "REX.W", "imm": "ib", "sign_ext": "1"},

    "mem8r8": {"opcode": "18", "prefix": "REX", "mod": "/r"},
    "mem16r16": {"opcode": "19", "prefix": "66", "mod": "/r"},
    "mem32r32": {"opcode": "19", "mod": "/r"},
    "mem64r64": {"opcode": "19", "prefix": "REX.W", "mod": "/r"},

    "r8r8": {"opcode": "1A", "prefix": "REX", "mod": "/r"},
    "r16r16": {"opcode": "1B", "prefix": "66", "mod": "/r"},
    "r32r32": {"opcode": "1B", "mod": "/r"},
    "r64r64": {"opcode": "1B", "prefix": "REX.W", "mod": "/r"},
    "r8mem8": {"opcode": "1A", "prefix": "REX", "mod": "/r"},
    "r16mem16": {"opcode": "1B", "prefix": "66", "mod": "/r"},
    "r32mem32": {"opcode": "1B", "mod": "/r"},
    "r64mem64": {"opcode": "1B", "prefix": "REX.W", "mod": "/r"},
}

IMUL = {
    "r8": {"mod": "/5", "opcode": "F6"},
    "mem8": {"mod": "/5", "opcode": "F6"},
    "r16": {"mod": "/5", "opcode": "F7", "prefix": "66"},
    "mem16": {"mod": "/5", "opcode": "F7", "prefix": "66"},
    "r32": {"mod": "/5", "opcode": "F7"},
    "mem32": {"mod": "/5", "opcode": "F7"},
    "r64": {"mod": "/5", "opcode": "F7", "prefix": "REX.W"},
    "mem64": {"mod": "/5", "opcode": "F7", "prefix": "REX.W"},

    "r16r16": {"mod": "/r", "opcode": "0FAF", "prefix": "66"},
    "r16mem16": {"mod": "/r", "opcode": "0FAF", "prefix": "66"},
    "r32r32": {"mod": "/r", "opcode": "0FAF"},
    "r32mem32": {"mod": "/r", "opcode": "0FAF"},
    "r64r64": {"mod": "/r", "opcode": "0FAF", "prefix": "REX.W"},
    "r64mem64": {"mod": "/r", "opcode": "0FAF", "prefix": "REX.W"},

    "r16r16imm8": {"mod": "/r", "opcode": "6B", "prefix": "66", "imm": "ib", "sign_ext": "1"},
    "r16mem16imm8": {"mod": "/r", "opcode": "6B", "prefix": "66", "imm": "ib", "sign_ext": "1"},
    "r32r32imm8": {"mod": "/r", "opcode": "6B", "imm": "ib", "sign_ext": "1"},
    "r32mem32imm8": {"mod": "/r", "opcode": "6B", "imm": "ib", "sign_ext": "1"},
    "r64r64imm8": {"mod": "/r", "opcode": "6B", "prefix": "REX.W", "imm": "ib", "sign_ext": "1"},
    "r64mem64imm8": {"mod": "/r", "opcode": "6B", "prefix": "REX.W", "imm": "ib", "sign_ext": "1"},

    "r16r16imm16": {"mod": "/r", "opcode": "69", "prefix": "66", "imm": "iw"},
    "r16mem16imm16": {"mod": "/r", "opcode": "69", "prefix": "66", "imm": "iw"},
    "r32r32imm32": {"mod": "/r", "opcode": "69", "imm": "id"},
    "r32mem32imm32": {"mod": "/r", "opcode": "69", "imm": "id"},
    "r64r64imm32": {"mod": "/r", "opcode": "69", "prefix": "REX.W", "imm": "id", "sign_ext": "4"},
    "r64mem64imm32": {"mod": "/r", "opcode": "69", "prefix": "REX.W", "imm": "id", "sign_ext": "4"}
}

MUL = {
    "r8": {"opcode": "F6", "prefix": "REX", "mod": "/4"},
    "r16": {"opcode": "F7", "prefix": "66", "mod": "/4"},
    "r32": {"opcode": "F7", "mod": "/4"},
    "r64": {"opcode": "F7", "prefix": "REX.W", "mod": "/4"},
    "mem8": {"opcode": "F6", "prefix": "REX", "mod": "/4"},
    "mem16": {"opcode": "F7", "prefix": "66", "mod": "/4"},
    "mem32": {"opcode": "F7", "mod": "/4"},
    "mem64": {"opcode": "F7", "prefix": "REX.W", "mod": "/4"},
}

IDIV = {
    "r8": {"mod": "/7", "opcode": "F6", "prefix": "REX"},
    "mem8": {"mod": "/7", "opcode": "F6", "prefix": "REX"},
    "r16": {"mod": "/7", "opcode": "F7", "prefix": "66"},
    "mem16": {"mod": "/7", "opcode": "F7", "prefix": "66"},
    "r32": {"mod": "/7", "opcode": "F7"},
    "mem32": {"mod": "/7", "opcode": "F7"},
    "r64": {"mod": "/7", "opcode": "F7", "prefix": "REX.W"},
    "mem64": {"mod": "/7", "opcode": "F7", "prefix": "REX.W"}
}

DIV = {
    "r8": {"mod": "/6", "opcode": "F6", "prefix": "REX"},
    "mem8": {"mod": "/6", "opcode": "F6", "prefix": "REX"},
    "r16": {"mod": "/6", "opcode": "F7", "prefix": "66"},
    "mem16": {"mod": "/6", "opcode": "F7", "prefix": "66"},
    "r32": {"mod": "/6", "opcode": "F7"},
    "mem32": {"mod": "/6", "opcode": "F7"},
    "r64": {"mod": "/6", "opcode": "F7", "prefix": "REX.W"},
    "mem64": {"mod": "/6", "opcode": "F7", "prefix": "REX.W"},
}

INC = {
    "r8": {"mod": "/0", "opcode": "FE", "prefix": "REX"},
    "mem8": {"mod": "/0", "opcode": "FE", "prefix": "REX"},
    "r16": {"mod": "/0", "opcode": "FF", "prefix": "66"},
    "mem16": {"mod": "/0", "opcode": "FF", "prefix": "66"},
    "r32": {"mod": "/0", "opcode": "FF"},
    "mem32": {"mod": "/0", "opcode": "FF"},
    "r64": {"mod": "/0", "opcode": "FF", "prefix": "REX.W"},
    "mem64": {"mod": "/0", "opcode": "FF", "prefix": "REX.W"},
}

DEC = {
    "r8": {"mod": "/1", "opcode": "FE", "prefix": "REX"},
    "mem8": {"mod": "/1", "opcode": "FE", "prefix": "REX"},
    "r16": {"mod": "/1", "opcode": "FF", "prefix": "66"},
    "mem16": {"mod": "/1", "opcode": "FF", "prefix": "66"},
    "r32": {"mod": "/1", "opcode": "FF"},
    "mem32": {"mod": "/1", "opcode": "FF"},
    "r64": {"mod": "/1", "opcode": "FF", "prefix": "REX.W"},
    "mem64": {"mod": "/1", "opcode": "FF", "prefix": "REX.W"},
}

NEG = {
    "r8": {"mod": "/3", "opcode": "F6", "prefix": "REX"},
    "mem8": {"mod": "/3", "opcode": "F6", "prefix": "REX"},
    "r16": {"mod": "/3", "opcode": "F7", "prefix": "66"},
    "mem16": {"mod": "/3", "opcode": "F7", "prefix": "66"},
    "r32": {"mod": "/3", "opcode": "F7"},
    "mem32": {"mod": "/3", "opcode": "F7"},
    "r64": {"mod": "/3", "opcode": "F7", "prefix": "REX.W"},
    "mem64": {"mod": "/3", "opcode": "F7", "prefix": "REX.W"},
}

CMP = {
    "ALimm8": {"opcode": "3C", "imm": "ib"},
    "AXimm16": {"opcode": "3D", "prefix": "66", "imm": "iw"},
    "EAXimm32": {"opcode": "3D", "imm": "id"},
    "RAXimm32": {"opcode": "3D", "prefix": "REX.W", "imm": "id", "sign_ext": "4"},
    "r8imm8": {"opcode": "80", "mod": "/7", "prefix": "REX", "imm": "ib"},
    "r16imm16": {"opcode": "81", "mod": "/7", "prefix": "66", "imm": "iw"},
    "r32imm32": {"opcode": "81", "mod": "/7", "imm": "id"},
    "r64imm32": {"opcode": "81", "mod": "/7", "prefix": "REX.W", "imm": "id", "sign_ext": "4"},
    "mem8imm8": {"opcode": "80", "mod": "/7", "prefix": "REX", "imm": "ib"},
    "mem16imm16": {"opcode": "81", "mod": "/7", "prefix": "66", "imm": "iw"},
    "mem32imm32": {"opcode": "81", "mod": "/7", "imm": "id"},
    "mem64imm32": {"opcode": "81", "mod": "/7", "prefix": "REX.W", "imm": "id", "sign_ext": "4"},

    "r16imm8": {"opcode": "83", "mod": "/7", "prefix": "66", "imm": "ib", "sign_ext": "1"},
    "r32imm8": {"opcode": "83", "mod": "/7", "imm": "ib", "sign_ext": "1"},
    "r64imm8": {"opcode": "83", "mod": "/7", "prefix": "REX.W", "imm": "ib", "sign_ext": "1"},
    "mem16imm8": {"opcode": "83", "mod": "/7", "prefix": "66", "imm": "ib", "sign_ext": "1"},
    "mem32imm8": {"opcode": "83", "mod": "/7", "imm": "ib", "sign_ext": "1"},
    "mem64imm8": {"opcode": "83", "mod": "/7", "prefix": "REX.W", "imm": "ib", "sign_ext": "1"},

    "mem8r8": {"opcode": "38", "prefix": "REX", "mod": "/r"},
    "mem16r16": {"opcode": "39", "prefix": "66", "mod": "/r"},
    "mem32r32": {"opcode": "39", "mod": "/r"},
    "mem64r64": {"opcode": "39", "prefix": "REX.W", "mod": "/r"},
    "r8r8": {"opcode": "3A", "prefix": "REX", "mod": "/r"},
    "r16r16": {"opcode": "3B", "prefix": "66", "mod": "/r"},
    "r32r32": {"opcode": "3B", "mod": "/r"},
    "r64r64": {"opcode": "3B", "prefix": "REX.W", "mod": "/r"},
    "r8mem8": {"opcode": "3A", "prefix": "REX", "mod": "/r"},
    "r16mem16": {"opcode": "3B", "prefix": "66", "mod": "/r"},
    "r32mem32": {"opcode": "3B", "mod": "/r"},
    "r64mem64": {"opcode": "3B", "prefix": "REX.W", "mod": "/r"},
}

# General logical instructions

AND = {
    "ALimm8": {"opcode": "24", "imm": "ib"},
    "AXimm16": {"opcode": "25", "prefix": "66", "imm": "iw"},
    "EAXimm32": {"opcode": "25", "imm": "id"},
    "RAXimm32": {"opcode": "25", "prefix": "REX.W", "imm": "id", "sign_ext": "4"},
    "r8imm8": {"opcode": "80", "mod": "/4", "prefix": "REX", "imm": "ib"},
    "r16imm16": {"opcode": "81", "mod": "/4", "prefix": "66", "imm": "iw"},
    "r32imm32": {"opcode": "81", "mod": "/4", "imm": "id"},
    "r64imm32": {"opcode": "81", "mod": "/4", "prefix": "REX.W", "imm": "id"},
    "mem8imm8": {"opcode": "80", "mod": "/4", "prefix": "REX", "imm": "ib"},
    "mem16imm16": {"opcode": "81", "mod": "/4", "prefix": "66", "imm": "iw"},
    "mem32imm32": {"opcode": "81", "mod": "/4", "imm": "id"},
    "mem64imm32": {"opcode": "81", "mod": "/4", "prefix": "REX.W", "imm": "id"},
    "r16imm8": {"opcode": "83", "mod": "/4", "prefix": "66", "imm": "ib", "sign_ext": "1"},
    "r32imm8": {"opcode": "83", "mod": "/4", "imm": "ib", "sign_ext": "1"},
    "r64imm8": {"opcode": "83", "mod": "/4", "prefix": "REX.W", "imm": "ib", "sign_ext": "1"},
    "mem16imm8": {"opcode": "83", "mod": "/4", "prefix": "66", "imm": "ib", "sign_ext": "1"},
    "mem32imm8": {"opcode": "83", "mod": "/4", "imm": "ib", "sign_ext": "1"},
    "mem64imm8": {"opcode": "83", "mod": "/4", "prefix": "REX.W", "imm": "ib", "sign_ext": "1"},

    "mem8r8": {"opcode": "20", "prefix": "REX", "mod": "/r"},
    "mem16r16": {"opcode": "21", "prefix": "66", "mod": "/r"},
    "mem32r32": {"opcode": "21", "mod": "/r"},
    "mem64r64": {"opcode": "21", "prefix": "REX.W", "mod": "/r"},

    "r8r8": {"opcode": "22", "prefix": "REX", "mod": "/r"},
    "r16r16": {"opcode": "23", "prefix": "66", "mod": "/r"},
    "r32r32": {"opcode": "23", "mod": "/r"},
    "r64r64": {"opcode": "23", "prefix": "REX.W", "mod": "/r"},
    "r8mem8": {"opcode": "22", "prefix": "REX", "mod": "/r"},
    "r16mem16": {"opcode": "23", "prefix": "66", "mod": "/r"},
    "r32mem32": {"opcode": "23", "mod": "/r"},
    "r64mem64": {"opcode": "23", "prefix": "REX.W", "mod": "/r"},
}

OR = {
    "ALimm8": {"opcode": "0C", "imm": "ib"},
    "AXimm16": {"opcode": "0D", "prefix": "66", "imm": "iw"},
    "EAXimm32": {"opcode": "0D", "imm": "id"},
    "RAXimm32": {"opcode": "0D", "prefix": "REX.W", "imm": "id", "sign_ext": "4"},
    "r8imm8": {"opcode": "80", "mod": "/1", "prefix": "REX", "imm": "ib"},
    "r16imm16": {"opcode": "81", "mod": "/1", "prefix": "66", "imm": "iw"},
    "r32imm32": {"opcode": "81", "mod": "/1", "imm": "id"},
    "r64imm32": {"opcode": "81", "mod": "/1", "prefix": "REX.W", "imm": "id"},
    "mem8imm8": {"opcode": "80", "mod": "/1", "prefix": "REX", "imm": "ib"},
    "mem16imm16": {"opcode": "81", "mod": "/1", "prefix": "66", "imm": "iw"},
    "mem32imm32": {"opcode": "81", "mod": "/1", "imm": "id"},
    "mem64imm32": {"opcode": "81", "mod": "/1", "prefix": "REX.W", "imm": "id"},
    "r16imm8": {"opcode": "83", "mod": "/1", "prefix": "66", "imm": "ib", "sign_ext": "1"},
    "r32imm8": {"opcode": "83", "mod": "/1", "imm": "ib", "sign_ext": "1"},
    "r64imm8": {"opcode": "83", "mod": "/1", "prefix": "REX.W", "imm": "ib", "sign_ext": "1"},
    "mem16imm8": {"opcode": "83", "mod": "/1", "prefix": "66", "imm": "ib", "sign_ext": "1"},
    "mem32imm8": {"opcode": "83", "mod": "/1", "imm": "ib", "sign_ext": "1"},
    "mem64imm8": {"opcode": "83", "mod": "/1", "prefix": "REX.W", "imm": "ib", "sign_ext": "1"},

    "mem8r8": {"opcode": "08", "prefix": "REX", "mod": "/r"},
    "mem16r16": {"opcode": "09", "prefix": "66", "mod": "/r"},
    "mem32r32": {"opcode": "09", "mod": "/r"},
    "mem64r64": {"opcode": "09", "prefix": "REX.W", "mod": "/r"},

    "r8r8": {"opcode": "0A", "prefix": "REX", "mod": "/r"},
    "r16r16": {"opcode": "0B", "prefix": "66", "mod": "/r"},
    "r32r32": {"opcode": "0B", "mod": "/r"},
    "r64r64": {"opcode": "0B", "prefix": "REX.W", "mod": "/r"},
    "r8mem8": {"opcode": "0A", "prefix": "REX", "mod": "/r"},
    "r16mem16": {"opcode": "0B", "prefix": "66", "mod": "/r"},
    "r32mem32": {"opcode": "0B", "mod": "/r"},
    "r64mem64": {"opcode": "0B", "prefix": "REX.W", "mod": "/r"},
}

XOR = {
    "ALimm8": {"opcode": "34", "imm": "ib"},
    "AXimm16": {"opcode": "35", "prefix": "66", "imm": "iw"},
    "EAXimm32": {"opcode": "35", "imm": "id"},
    "RAXimm32": {"opcode": "35", "prefix": "REX.W", "imm": "id", "sign_ext": "4"},
    "r8imm8": {"opcode": "80", "mod": "/6", "prefix": "REX", "imm": "ib"},
    "r16imm16": {"opcode": "81", "mod": "/6", "prefix": "66", "imm": "iw"},
    "r32imm32": {"opcode": "81", "mod": "/6", "imm": "id"},
    "r64imm32": {"opcode": "81", "mod": "/6", "prefix": "REX.W", "imm": "id"},
    "mem8imm8": {"opcode": "80", "mod": "/6", "prefix": "REX", "imm": "ib"},
    "mem16imm16": {"opcode": "81", "mod": "/6", "prefix": "66", "imm": "iw"},
    "mem32imm32": {"opcode": "81", "mod": "/6", "imm": "id"},
    "mem64imm32": {"opcode": "81", "mod": "/6", "prefix": "REX.W", "imm": "id"},
    "r16imm8": {"opcode": "83", "mod": "/6", "prefix": "66", "imm": "ib", "sign_ext": "1"},
    "r32imm8": {"opcode": "83", "mod": "/6", "imm": "ib", "sign_ext": "1"},
    "r64imm8": {"opcode": "83", "mod": "/6", "prefix": "REX.W", "imm": "ib", "sign_ext": "1"},
    "mem16imm8": {"opcode": "83", "mod": "/6", "prefix": "66", "imm": "ib", "sign_ext": "1"},
    "mem32imm8": {"opcode": "83", "mod": "/6", "imm": "ib", "sign_ext": "1"},
    "mem64imm8": {"opcode": "83", "mod": "/6", "prefix": "REX.W", "imm": "ib", "sign_ext": "1"},

    "mem8r8": {"opcode": "30", "prefix": "REX", "mod": "/r"},
    "mem16r16": {"opcode": "31", "prefix": "66", "mod": "/r"},
    "mem32r32": {"opcode": "31", "mod": "/r"},
    "mem64r64": {"opcode": "31", "prefix": "REX.W", "mod": "/r"},

    "r8r8": {"opcode": "32", "prefix": "REX", "mod": "/r"},
    "r16r16": {"opcode": "33", "prefix": "66", "mod": "/r"},
    "r32r32": {"opcode": "33", "mod": "/r"},
    "r64r64": {"opcode": "33", "prefix": "REX.W", "mod": "/r"},
    "r8mem8": {"opcode": "32", "prefix": "REX", "mod": "/r"},
    "r16mem16": {"opcode": "33", "prefix": "66", "mod": "/r"},
    "r32mem32": {"opcode": "33", "mod": "/r"},
    "r64mem64": {"opcode": "33", "prefix": "REX.W", "mod": "/r"},
}

NOT = {
    "r8": {"opcode": "F6", "prefix": "REX", "mod": "/2"},
    "r16": {"opcode": "F7", "prefix": "66", "mod": "/2"},
    "r32": {"opcode": "F7", "mod": "/2"},
    "r64": {"opcode": "F7", "prefix": "REX.W", "mod": "/2"},
    "mem8": {"opcode": "F6", "prefix": "REX", "mod": "/2"},
    "mem16": {"opcode": "F7", "prefix": "66", "mod": "/2"},
    "mem32": {"opcode": "F7", "mod": "/2"},
    "mem64": {"opcode": "F7", "prefix": "REX.W", "mod": "/2"},
}

# Shift and Rotate Instructions

SAR = {
    "r8imm8": {"opcode": "C0", "mod": "/7", "prefix": "REX", "imm": "ib"},
    "mem8imm8": {"opcode": "C0", "mod": "/7", "prefix": "REX", "imm": "ib"},
    "r16imm8": {"opcode": "C1", "mod": "/7", "prefix": "66", "imm": "ib"},
    "mem16imm8": {"opcode": "C1", "mod": "/7", "prefix": "66", "imm": "ib"},
    "r32imm8": {"opcode": "C1", "mod": "/7", "imm": "ib"},
    "mem32imm8": {"opcode": "C1", "mod": "/7", "imm": "ib"},
    "r64imm8": {"opcode": "C1", "mod": "/7", "prefix": "REX.W", "imm": "ib"},
    "mem64imm8": {"opcode": "C1", "mod": "/7", "prefix": "REX.W", "imm": "ib"},
    "mem32CL": {"opcode": "D3", "mod": "/7"},
    "r32CL": {"opcode": "D3", "mod": "/7"},
    "r64CL": {"opcode": "D3", "mod": "/7", "prefix": "REX.W"},
    "mem64CL": {"opcode": "D3", "mod": "/7", "prefix": "REX.W"},
}

SHR = {
    "r8imm8": {"opcode": "C0", "mod": "/5", "prefix": "REX", "imm": "ib"},
    "mem8imm8": {"opcode": "C0", "mod": "/5", "prefix": "REX", "imm": "ib"},
    "r16imm8": {"opcode": "C1", "mod": "/5", "prefix": "66", "imm": "ib"},
    "mem16imm8": {"opcode": "C1", "mod": "/5", "prefix": "66", "imm": "ib"},
    "r32imm8": {"opcode": "C1", "mod": "/5", "imm": "ib"},
    "mem32imm8": {"opcode": "C1", "mod": "/5", "imm": "ib"},
    "r64imm8": {"opcode": "C1", "mod": "/5", "prefix": "REX.W", "imm": "ib"},
    "mem64imm8": {"opcode": "C1", "mod": "/5", "prefix": "REX.W", "imm": "ib"},
    "mem32CL": {"opcode": "D3", "mod": "/5"},
    "r32CL": {"opcode": "D3", "mod": "/5"},
    "r64CL": {"opcode": "D3", "mod": "/5", "prefix": "REX.W"},
    "mem64CL": {"opcode": "D3", "mod": "/5", "prefix": "REX.W"},
}

SAL = {
    "r8imm8": {"opcode": "C0", "mod": "/4", "prefix": "REX", "imm": "ib"},
    "mem8imm8": {"opcode": "C0", "mod": "/4", "prefix": "REX", "imm": "ib"},
    "r16imm8": {"opcode": "C1", "mod": "/4", "prefix": "66", "imm": "ib"},
    "mem16imm8": {"opcode": "C1", "mod": "/4", "prefix": "66", "imm": "ib"},
    "r32imm8": {"opcode": "C1", "mod": "/4", "imm": "ib"},
    "mem32imm8": {"opcode": "C1", "mod": "/4", "imm": "ib"},
    "r64imm8": {"opcode": "C1", "mod": "/4", "prefix": "REX.W", "imm": "ib"},
    "mem64imm8": {"opcode": "C1", "mod": "/4", "prefix": "REX.W", "imm": "ib"},
    "mem32CL": {"opcode": "D3", "mod": "/4"},
    "r32CL": {"opcode": "D3", "mod": "/4"},
    "r64CL": {"opcode": "D3", "mod": "/4", "prefix": "REX.W"},
    "mem64CL": {"opcode": "D3", "mod": "/4", "prefix": "REX.W"},
}

SHL = {
    "r8imm8": {"opcode": "C0", "mod": "/4", "prefix": "REX", "imm": "ib"},
    "mem8imm8": {"opcode": "C0", "mod": "/4", "prefix": "REX", "imm": "ib"},
    "r16imm8": {"opcode": "C1", "mod": "/4", "prefix": "66", "imm": "ib"},
    "mem16imm8": {"opcode": "C1", "mod": "/4", "prefix": "66", "imm": "ib"},
    "r32imm8": {"opcode": "C1", "mod": "/4", "imm": "ib"},
    "mem32imm8": {"opcode": "C1", "mod": "/4", "imm": "ib"},
    "r64imm8": {"opcode": "C1", "mod": "/4", "prefix": "REX.W", "imm": "ib"},
    "mem64imm8": {"opcode": "C1", "mod": "/4", "prefix": "REX.W", "imm": "ib"},
    "mem32CL": {"opcode": "D3", "mod": "/4"},
    "r32CL": {"opcode": "D3", "mod": "/4"},
    "r64CL": {"opcode": "D3", "mod": "/4", "prefix": "REX.W"},
    "mem64CL": {"opcode": "D3", "mod": "/4", "prefix": "REX.W"},
}

SHRD = {
    "r16r16imm8": {"opcode": "0FAC", "mod": "/r", "prefix": "66", "imm": "ib", "rm": "1"},
    "mem16r16imm8": {"opcode": "0FAC", "mod": "/r", "prefix": "66", "imm": "ib"},
    "r32r32imm8": {"opcode": "0FAC", "mod": "/r", "imm": "ib", "rm": "1"},
    "mem32r32imm8": {"opcode": "0FAC", "mod": "/r", "imm": "ib"},
    "r64r64imm8": {"opcode": "0FAC", "mod": "/r", "prefix": "REX.W", "imm": "ib", "rm": "1"},
    "mem64r64imm8": {"opcode": "0FAC", "mod": "/r", "prefix": "REX.W", "imm": "ib"},
}

SHLD = {
    "r16r16imm8": {"opcode": "0FA4", "mod": "/r", "prefix": "66", "imm": "ib", "rm": "1"},
    "mem16r16imm8": {"opcode": "0FA4", "mod": "/r", "prefix": "66", "imm": "ib"},
    "r32r32imm8": {"opcode": "0FA4", "mod": "/r", "imm": "ib", "rm": "1"},
    "mem32r32imm8": {"opcode": "0FA4", "mod": "/r", "imm": "ib"},
    "r64r64imm8": {"opcode": "0FA4", "mod": "/r", "prefix": "REX.W", "imm": "ib", "rm": "1"},
    "mem64r64imm8": {"opcode": "0FA4", "mod": "/r", "prefix": "REX.W", "imm": "ib"},
}

ROR = {
    "r8imm8": {"opcode": "C0", "mod": "/1", "prefix": "REX", "imm": "ib"},
    "mem8imm8": {"opcode": "C0", "mod": "/1", "prefix": "REX", "imm": "ib"},
    "r16imm8": {"opcode": "C1", "mod": "/1", "prefix": "66", "imm": "ib"},
    "mem16imm8": {"opcode": "C1", "mod": "/1", "prefix": "66", "imm": "ib"},
    "r32imm8": {"opcode": "C1", "mod": "/1", "imm": "ib"},
    "mem32imm8": {"opcode": "C1", "mod": "/1", "imm": "ib"},
    "r64imm8": {"opcode": "C1", "mod": "/1", "prefix": "REX.W", "imm": "ib"},
    "mem64imm8": {"opcode": "C1", "mod": "/1", "prefix": "REX.W", "imm": "ib"},
    "mem32CL": {"opcode": "D3", "mod": "/1"},
    "r32CL": {"opcode": "D3", "mod": "/1"},
    "r64CL": {"opcode": "D3", "mod": "/1", "prefix": "REX.W"},
    "mem64CL": {"opcode": "D3", "mod": "/1", "prefix": "REX.W"},
}

ROL = {
    "r8imm8": {"opcode": "C0", "mod": "/0", "prefix": "REX", "imm": "ib"},
    "mem8imm8": {"opcode": "C0", "mod": "/0", "prefix": "REX", "imm": "ib"},
    "r16imm8": {"opcode": "C1", "mod": "/0", "prefix": "66", "imm": "ib"},
    "mem16imm8": {"opcode": "C1", "mod": "/0", "prefix": "66", "imm": "ib"},
    "r32imm8": {"opcode": "C1", "mod": "/0", "imm": "ib"},
    "mem32imm8": {"opcode": "C1", "mod": "/0", "imm": "ib"},
    "r64imm8": {"opcode": "C1", "mod": "/0", "prefix": "REX.W", "imm": "ib"},
    "mem64imm8": {"opcode": "C1", "mod": "/0", "prefix": "REX.W", "imm": "ib"},
    "mem32CL": {"opcode": "D3", "mod": "/0"},
    "r32CL": {"opcode": "D3", "mod": "/0"},
    "r64CL": {"opcode": "D3", "mod": "/0", "prefix": "REX.W"},
    "mem64CL": {"opcode": "D3", "mod": "/0", "prefix": "REX.W"},
}

RCR = {
    "r8imm8": {"opcode": "C0", "mod": "/3", "prefix": "REX", "imm": "ib"},
    "mem8imm8": {"opcode": "C0", "mod": "/3", "prefix": "REX", "imm": "ib"},
    "r16imm8": {"opcode": "C1", "mod": "/3", "prefix": "66", "imm": "ib"},
    "mem16imm8": {"opcode": "C1", "mod": "/3", "prefix": "66", "imm": "ib"},
    "r32imm8": {"opcode": "C1", "mod": "/3", "imm": "ib"},
    "mem32imm8": {"opcode": "C1", "mod": "/3", "imm": "ib"},
    "r64imm8": {"opcode": "C1", "mod": "/3", "prefix": "REX.W", "imm": "ib"},
    "mem64imm8": {"opcode": "C1", "mod": "/3", "prefix": "REX.W", "imm": "ib"},
    "mem32CL": {"opcode": "D3", "mod": "/3"},
    "r32CL": {"opcode": "D3", "mod": "/3"},
    "r64CL": {"opcode": "D3", "mod": "/3", "prefix": "REX.W"},
    "mem64CL": {"opcode": "D3", "mod": "/3", "prefix": "REX.W"},
}

RCL = {
    "r8imm8": {"opcode": "C0", "mod": "/2", "prefix": "REX", "imm": "ib"},
    "mem8imm8": {"opcode": "C0", "mod": "/2", "prefix": "REX", "imm": "ib"},
    "r16imm8": {"opcode": "C1", "mod": "/2", "prefix": "66", "imm": "ib"},
    "mem16imm8": {"opcode": "C1", "mod": "/2", "prefix": "66", "imm": "ib"},
    "r32imm8": {"opcode": "C1", "mod": "/2", "imm": "ib"},
    "mem32imm8": {"opcode": "C1", "mod": "/2", "imm": "ib"},
    "r64imm8": {"opcode": "C1", "mod": "/2", "prefix": "REX.W", "imm": "ib"},
    "mem64imm8": {"opcode": "C1", "mod": "/2", "prefix": "REX.W", "imm": "ib"},
    "mem32CL": {"opcode": "D3", "mod": "/2"},
    "r32CL": {"opcode": "D3", "mod": "/2"},
    "r64CL": {"opcode": "D3", "mod": "/2", "prefix": "REX.W"},
    "mem64CL": {"opcode": "D3", "mod": "/2", "prefix": "REX.W"},
}

# Control Transfer Instructions

JMP = {
    "rel8": {"opcode": "EB", 'code_offset': "cb"},
    "rel32": {"opcode": "E9", "code_offset": "cd"},
    "r64": {"opcode": "FF", "mod": "/4"},
    "mem64": {"opcode": "FF", "mod": "/4"},
}

JE = {
    "rel8": {"opcode": "74", 'code_offset': "cb"},
    "rel32": {"opcode": "0F84", "code_offset": "cd"}
}

JZ = {
    "rel8": {"opcode": "74", 'code_offset': "cb"},
    "rel32": {"opcode": "0F84", "code_offset": "cd"}
}

JNE = {
    "rel8": {"opcode": "75", 'code_offset': "cb"},
    "rel32": {"opcode": "0F85", "code_offset": "cd"}
}

JNZ = {
    "rel8": {"opcode": "75", 'code_offset': "cb"},
    "rel32": {"opcode": "0F85", "code_offset": "cd"}
}

JA = {
    "rel8": {"opcode": "77", 'code_offset': "cb"},
    "rel32": {"opcode": "0F87", "code_offset": "cd"}
}

JNBE = {
    "rel8": {"opcode": "77", 'code_offset': "cb"},
    "rel32": {"opcode": "0F87", "code_offset": "cd"}
}

JAE = {
    "rel8": {"opcode": "73", 'code_offset': "cb"},
    "rel32": {"opcode": "0F83", "code_offset": "cd"}
}

JNB = {
    "rel8": {"opcode": "73", 'code_offset': "cb"},
    "rel32": {"opcode": "0F83", "code_offset": "cd"}
}

JB = {
    "rel8": {"opcode": "72", 'code_offset': "cb"},
    "rel32": {"opcode": "0F82", "code_offset": "cd"}
}

JNAE = {
    "rel8": {"opcode": "72", 'code_offset': "cb"},
    "rel32": {"opcode": "0F82", "code_offset": "cd"}
}

JBE = {
    "rel8": {"opcode": "76", 'code_offset': "cb"},
    "rel32": {"opcode": "0F86", "code_offset": "cd"}
}

JNA = {
    "rel8": {"opcode": "76", 'code_offset': "cb"},
    "rel32": {"opcode": "0F86", "code_offset": "cd"}
}

JG = {
    "rel8": {"opcode": "7F", 'code_offset': "cb"},
    "rel32": {"opcode": "0F8F", "code_offset": "cd"}
}

JNLE = {
    "rel8": {"opcode": "7F", 'code_offset': "cb"},
    "rel32": {"opcode": "0F8F", "code_offset": "cd"}
}

JGE = {
    "rel8": {"opcode": "7D", 'code_offset': "cb"},
    "rel32": {"opcode": "0F8D", "code_offset": "cd"}
}

JNL = {
    "rel8": {"opcode": "7D", 'code_offset': "cb"},
    "rel32": {"opcode": "0F8D", "code_offset": "cd"}
}

JL = {
    "rel8": {"opcode": "7C", 'code_offset': "cb"},
    "rel32": {"opcode": "0F8C", "code_offset": "cd"}
}

JNGE = {
    "rel8": {"opcode": "7C", 'code_offset': "cb"},
    "rel32": {"opcode": "0F8C", "code_offset": "cd"}
}

JLE = {
    "rel8": {"opcode": "7E", 'code_offset': "cb"},
    "rel32": {"opcode": "0F8E", "code_offset": "cd"}
}

JNG = {
    "rel8": {"opcode": "7E", 'code_offset': "cb"},
    "rel32": {"opcode": "0F8E", "code_offset": "cd"}
}

JC = {
    "rel8": {"opcode": "72", 'code_offset': "cb"},
    "rel32": {"opcode": "0F82", "code_offset": "cd"}
}

JNC = {
    "rel8": {"opcode": "73", 'code_offset': "cb"},
    "rel32": {"opcode": "0F83", "code_offset": "cd"}
}

JO = {
    "rel8": {"opcode": "70", 'code_offset': "cb"},
    "rel32": {"opcode": "0F80", "code_offset": "cd"}
}

JNO = {
    "rel8": {"opcode": "71", 'code_offset': "cb"},
    "rel32": {"opcode": "0F81", "code_offset": "cd"}
}

JS = {
    "rel8": {"opcode": "78", 'code_offset': "cb"},
    "rel32": {"opcode": "0F88", "code_offset": "cd"}
}

JNS = {
    "rel8": {"opcode": "79", 'code_offset': "cb"},
    "rel32": {"opcode": "0F89", "code_offset": "cd"}
}

JPO = {
    "rel8": {"opcode": "7B", 'code_offset': "cb"},
    "rel32": {"opcode": "0F8B", "code_offset": "cd"}
}

JNP = {
    "rel8": {"opcode": "7B", 'code_offset': "cb"},
    "rel32": {"opcode": "0F8B", "code_offset": "cd"}
}

JPE = {
    "rel8": {"opcode": "7A", 'code_offset': "cb"},
    "rel32": {"opcode": "0F8A", "code_offset": "cd"}
}

JP = {
    "rel8": {"opcode": "7A", 'code_offset': "cb"},
    "rel32": {"opcode": "0F8A", "code_offset": "cd"}
}

JECXZ = {"rel8": {"opcode": "E3", 'code_offset': "cb"}}
JRCXZ = {"rel8": {"opcode": "E3", 'code_offset': "cb"}}

LOOP = {"rel8": {"opcode": "E2", 'code_offset': "cb"}}
LOOPE = {"rel8": {"opcode": "E1", 'code_offset': "cb"}}
LOOPZ = {"rel8": {"opcode": "E1", 'code_offset': "cb"}}
LOOPNE = {"rel8": {"opcode": "E0", 'code_offset': "cb"}}
LOOPNZ = {"rel8": {"opcode": "E0", 'code_offset': "cb"}}

CALL = {
    "rel32": {"opcode": "E8", "code_offset": "cd"},
    "r64": {"opcode": "FF", "mod": "/2"},
    "mem64": {"opcode": "FF", "mod": "/2"},
}

RET = {
    "no_op": {"opcode": "C3"},
    "imm16": {"opcode": "C2", "imm": "iw"}
}

IRET = {"no_op": {"opcode": "CF", "prefix": "66"}}
IRETD = {"no_op": {"opcode": "CF"}}
IRETQ = {"no_op": {"opcode": "CF", "prefix": "REX.W"}}

INT3 = {"no_op": {"opcode": "CC"}}
INT = {"imm8": {"opcode": "CD", "imm": "ib"}}

# String Instructions

MOVSB = {"no_op": {"opcode": "A4"}}
MOVSW = {"no_op": {"opcode": "A5", "prefix": "66"}}
MOVSD = {"no_op": {"opcode": "A5"}}
MOVSQ = {"no_op": {"opcode": "A5", "prefix": "REX.W"}}


# Miscellaneous Instructions

LEA = {
    "r64mem8": {"opcode": "8D", "mod": "/r", "prefix": "REX.W"},
    "r64mem16": {"opcode": "8D", "mod": "/r", "prefix": "REX.W"},
    "r64mem32": {"opcode": "8D", "mod": "/r", "prefix": "REX.W"},
    "r64mem64": {"opcode": "8D", "mod": "/r", "prefix": "REX.W"},
    "r64mem128": {"opcode": "8D", "mod": "/r", "prefix": "REX.W"},
    "r64mem256": {"opcode": "8D", "mod": "/r", "prefix": "REX.W"},
}

NOP = {
    "no_op": {"opcode": "90"},
    "mem16": {"opcode": "0F1F", "mod": "/0", "prefix": "66"},
    "mem32": {"opcode": "0F1F", "mod": "/0"}
}

UD2 = {"no_op": {"opcode": "0F0B"}}
XLATB = {"no_op": {"opcode": "D7", "prefix": "REX.W"}}
CPUID = {"no_op": {"opcode": "0FA2"}}

MOVBE = {
    "r16mem16": {"mod": "/r", "opcode": "0F38F0", "prefix": "66"},
    "r32mem32": {"mod": "/r", "opcode": "0F38F0"},
    "r64mem64": {"mod": "/r", "opcode": "0F38F0", "prefix": "REX.W"},
    "mem16r16": {"mod": "/r", "opcode": "0F38F1", "prefix": "66"},
    "mem32r32": {"mod": "/r", "opcode": "0F38F1"},
    "mem64r64": {"mod": "/r", "opcode": "0F38F1", "prefix": "REX.W"},
}

PREFETCHW = {"mem8": {"opcode": "0F0D", "mod": "/1"}}
PREFETCHWT1 = {"mem8": {"opcode": "0F0D", "mod": "/2"}}
XGETBV = {"no_op": {"opcode": "0F01D0"}}

# Random Number Generator Instructions

RDRAND = {
    "r16": {"opcode": "0FC7", "mod": "/6", 'prefix': '66'},
    "r32": {"opcode": "0FC7", "mod": "/6"},
    "r64": {"opcode": "0FC7", "mod": "/6", "prefix": "REX.W"},
}

RDSEED = {
    "r16": {"opcode": "0FC7", "mod": "/7", 'prefix': '66'},
    "r32": {"opcode": "0FC7", "mod": "/7"},
    "r64": {"opcode": "0FC7", "mod": "/7", "prefix": "REX.W"},
}
