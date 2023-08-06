
VPBROADCASTB = {
    "xmmxmm": {"L": "128", "pp": "66", "mmmm": "0F38", "W": "W0", "opcode": "78", "mod": "/r", "evex": "1"},
    "xmmmem8": {"L": "128", "pp": "66", "mmmm": "0F38", "W": "W0", "opcode": "78", "mod": "/r", "evex": "1"},
    "ymmxmm": {"L": "256", "pp": "66", "mmmm": "0F38", "W": "W0", "opcode": "78", "mod": "/r", "evex": "1"},
    "ymmmem8": {"L": "256", "pp": "66", "mmmm": "0F38", "W": "W0", "opcode": "78", "mod": "/r", "evex": "1"},
    "zmmxmm": {"L": "512", "pp": "66", "mmmm": "0F38", "W": "W0", "opcode": "78", "mod": "/r", "evex": "1"},
    "zmmmem8": {"L": "512", "pp": "66", "mmmm": "0F38", "W": "W0", "opcode": "78", "mod": "/r", "evex": "1"}
}

VPBROADCASTW = {
    "xmmxmm": {"L": "128", "pp": "66", "mmmm": "0F38", "W": "W0", "opcode": "79", "mod": "/r", "evex": "1"},
    "xmmmem16": {"L": "128", "pp": "66", "mmmm": "0F38", "W": "W0", "opcode": "79", "mod": "/r", "evex": "1"},
    "ymmxmm": {"L": "256", "pp": "66", "mmmm": "0F38", "W": "W0", "opcode": "79", "mod": "/r", "evex": "1"},
    "ymmmem16": {"L": "256", "pp": "66", "mmmm": "0F38", "W": "W0", "opcode": "79", "mod": "/r", "evex": "1"},
    "zmmxmm": {"L": "512", "pp": "66", "mmmm": "0F38", "W": "W0", "opcode": "79", "mod": "/r", "evex": "1"},
    "zmmmem16": {"L": "512", "pp": "66", "mmmm": "0F38", "W": "W0", "opcode": "79", "mod": "/r", "evex": "1"}
}

VPBROADCASTD = {
    "xmmxmm": {"L": "128", "pp": "66", "mmmm": "0F38", "W": "W0", "opcode": "58", "mod": "/r", "evex": "1"},
    "xmmmem32": {"L": "128", "pp": "66", "mmmm": "0F38", "W": "W0", "opcode": "58", "mod": "/r", "evex": "1"},
    "ymmxmm": {"L": "256", "pp": "66", "mmmm": "0F38", "W": "W0", "opcode": "58", "mod": "/r", "evex": "1"},
    "ymmmem32": {"L": "256", "pp": "66", "mmmm": "0F38", "W": "W0", "opcode": "58", "mod": "/r", "evex": "1"},
    "zmmxmm": {"L": "512", "pp": "66", "mmmm": "0F38", "W": "W0", "opcode": "58", "mod": "/r", "evex": "1"},
    "zmmmem32": {"L": "512", "pp": "66", "mmmm": "0F38", "W": "W0", "opcode": "58", "mod": "/r", "evex": "1"}
}

VPBROADCASTQ = {
    "xmmxmm": {"L": "128", "pp": "66", "mmmm": "0F38", "W": "W0", "W512": "W1", "opcode": "59", "mod": "/r", "evex": "1"},
    "xmmmem64": {"L": "128", "pp": "66", "mmmm": "0F38", "W": "W0", "W512": "W1", "opcode": "59", "mod": "/r", "evex": "1"},
    "ymmxmm": {"L": "256", "pp": "66", "mmmm": "0F38", "W": "W0", "W512": "W1", "opcode": "59", "mod": "/r", "evex": "1"},
    "ymmmem64": {"L": "256", "pp": "66", "mmmm": "0F38", "W": "W0", "W512": "W1", "opcode": "59", "mod": "/r", "evex": "1"},
    "zmmxmm": {"L": "512", "pp": "66", "mmmm": "0F38", "W": "W0", "W512": "W1", "opcode": "59", "mod": "/r", "evex": "1"},
    "zmmmem64": {"L": "512", "pp": "66", "mmmm": "0F38", "W": "W0", "W512": "W1", "opcode": "59", "mod": "/r", "evex": "1"}
}

VBROADCASTI128 = {
    "ymmmem128": {"L": "256", "pp": "66", "mmmm": "0F38", "W": "W0", "opcode": "5A", "mod": "/r"},
}

VEXTRACTI128 = {
    "xmmymmimm8": {"L": "256", "pp": "66", "mmmm": "0F3A", "W": "W0", "opcode": "39", "mod": "/r", "imm": "ib", 'rm': '1'},
    "mem128ymmimm8": {"L": "256", "pp": "66", "mmmm": "0F3A", "W": "W0", "opcode": "39", "mod": "/r", "imm": "ib"},
}

VINSERTI128 = {
    "ymmymmxmmimm8": {"vvvv": "NDS", "L": "256", "pp": "66", "mmmm": "0F3A", "W": "W0", "opcode": "38", "mod": "/r", "imm": "ib"},
    "ymmymmmem128imm8": {"vvvv": "NDS", "L": "256", "pp": "66", "mmmm": "0F3A", "W": "W0", "opcode": "38", "mod": "/r", "imm": "ib"},
}

VPMASKMOVD = {
    "xmmxmmmem128": {"vvvv": "NDS", "L": "128", "pp": "66", "mmmm": "0F38", "W": "W0", "opcode": "8C", "mod": "/r"},
    "ymmymmmem256": {"vvvv": "NDS", "L": "256", "pp": "66", "mmmm": "0F38", "W": "W0", "opcode": "8C", "mod": "/r"},
    "mem128xmmxmm": {"vvvv": "NDS", "L": "128", "pp": "66", "mmmm": "0F38", "W": "W0", "opcode": "8E", "mod": "/r"},
    "mem256ymmymm": {"vvvv": "NDS", "L": "256", "pp": "66", "mmmm": "0F38", "W": "W0", "opcode": "8E", "mod": "/r"},
}

VPMASKMOVQ = {
    "xmmxmmmem128": {"vvvv": "NDS", "L": "128", "pp": "66", "mmmm": "0F38", "W": "W1", "opcode": "8C", "mod": "/r"},
    "ymmymmmem256": {"vvvv": "NDS", "L": "256", "pp": "66", "mmmm": "0F38", "W": "W1", "opcode": "8C", "mod": "/r"},
    "mem128xmmxmm": {"vvvv": "NDS", "L": "128", "pp": "66", "mmmm": "0F38", "W": "W1", "opcode": "8E", "mod": "/r"},
    "mem256ymmymm": {"vvvv": "NDS", "L": "256", "pp": "66", "mmmm": "0F38", "W": "W1", "opcode": "8E", "mod": "/r"},
}

VPERM2I128 = {
    "ymmymmymmimm8": {"vvvv": "NDS", "L": "256", "pp": "66", "mmmm": "0F3A", "W": "W0", "opcode": "46", "mod": "/r", "imm": "ib"},
    "ymmymmmem256imm8": {"vvvv": "NDS", "L": "256", "pp": "66", "mmmm": "0F3A", "W": "W0", "opcode": "46", "mod": "/r", "imm": "ib"},
}

VPERMD = {
    "ymmymmymm": {"vvvv": "NDS", "L": "256", "pp": "66", "mmmm": "0F38", "W": "W0", "opcode": "36", "mod": "/r", "evex": "1"},
    "ymmymmmem256": {"vvvv": "NDS", "L": "256", "pp": "66", "mmmm": "0F38", "W": "W0", "opcode": "36", "mod": "/r", "evex": "1"},
    "zmmzmmzmm": {"vvvv": "NDS", "L": "512", "pp": "66", "mmmm": "0F38", "W": "W0", "opcode": "36", "mod": "/r", "evex": "1"},
    "zmmzmmmem512": {"vvvv": "NDS", "L": "512", "pp": "66", "mmmm": "0F38", "W": "W0", "opcode": "36", "mod": "/r", "evex": "1"},

    "ymmymmmem32": {"vvvv": "NDS", "L": "256", "pp": "66", "mmmm": "0F38", "W": "W0", "opcode": "36", "mod": "/r", "mbr": "1", "evex": "1"},
    "zmmzmmmem32": {"vvvv": "NDS", "L": "512", "pp": "66", "mmmm": "0F38", "W": "W0", "opcode": "36", "mod": "/r", "mbr": "1", "evex": "1"}
}

VPERMPS = {
    "ymmymmymm": {"vvvv": "NDS", "L": "256", "pp": "66", "mmmm": "0F38", "W": "W0", "opcode": "16", "mod": "/r", "evex": "1"},
    "ymmymmmem256": {"vvvv": "NDS", "L": "256", "pp": "66", "mmmm": "0F38", "W": "W0", "opcode": "16", "mod": "/r", "evex": "1"},
    "zmmzmmzmm": {"vvvv": "NDS", "L": "512", "pp": "66", "mmmm": "0F38", "W": "W0", "opcode": "16", "mod": "/r", "evex": "1"},
    "zmmzmmmem512": {"vvvv": "NDS", "L": "512", "pp": "66", "mmmm": "0F38", "W": "W0", "opcode": "16", "mod": "/r", "evex": "1"},

    "ymmymmmem32": {"vvvv": "NDS", "L": "256", "pp": "66", "mmmm": "0F38", "W": "W0", "opcode": "16", "mod": "/r", "mbr": "1", "evex": "1"},
    "zmmzmmmem32": {"vvvv": "NDS", "L": "512", "pp": "66", "mmmm": "0F38", "W": "W0", "opcode": "16", "mod": "/r", "mbr": "1", "evex": "1"}
}

VPERMQ = {
    "ymmymmimm8": {"L": "256", "pp": "66", "mmmm": "0F3A", "W": "W1", "opcode": "00", "mod": "/r", "imm": "ib", "evex": "1"},
    "ymmmem256imm8": {"L": "256", "pp": "66", "mmmm": "0F3A", "W": "W1", "opcode": "00", "mod": "/r", "imm": "ib", "evex": "1"},
    "zmmzmmimm8": {"L": "512", "pp": "66", "mmmm": "0F3A", "W": "W1", "opcode": "00", "mod": "/r", "imm": "ib", "evex": "1"},
    "zmmmem512imm8": {"L": "512", "pp": "66", "mmmm": "0F3A", "W": "W1", "opcode": "00", "mod": "/r", "imm": "ib", "evex": "1"},

    "ymmmem64imm8": {"L": "256", "pp": "66", "mmmm": "0F3A", "W": "W1", "opcode": "00", "mod": "/r", "imm": "ib", "mbr": "1", "evex": "1"},
    "zmmmem64imm8": {"L": "512", "pp": "66", "mmmm": "0F3A", "W": "W1", "opcode": "00", "mod": "/r", "imm": "ib", "mbr": "1", "evex": "1"},

    "ymmymmymm": {"vvvv": "NDS", "L": "256", "pp": "66", "mmmm": "0F38", "W": "W1", "opcode": "36", "mod": "/r", "evex": "1"},
    "ymmymmmem256": {"vvvv": "NDS", "L": "256", "pp": "66", "mmmm": "0F38", "W": "W1", "opcode": "36", "mod": "/r", "evex": "1"},
    "zmmzmmzmm": {"vvvv": "NDS", "L": "512", "pp": "66", "mmmm": "0F38", "W": "W1", "opcode": "36", "mod": "/r", "evex": "1"},
    "zmmzmmmem512": {"vvvv": "NDS", "L": "512", "pp": "66", "mmmm": "0F38", "W": "W1", "opcode": "36", "mod": "/r", "evex": "1"},

    "ymmymmmem64": {"vvvv": "NDS", "L": "256", "pp": "66", "mmmm": "0F38", "W": "W1", "opcode": "36", "mod": "/r", "mbr": "1", "evex": "1"},
    "zmmzmmmem64": {"vvvv": "NDS", "L": "512", "pp": "66", "mmmm": "0F38", "W": "W1", "opcode": "36", "mod": "/r", "mbr": "1", "evex": "1"}
}

VPERMPD = {
    "ymmymmimm8": {"L": "256", "pp": "66", "mmmm": "0F3A", "W": "W1", "opcode": "01", "mod": "/r", "imm": "ib", "evex": "1"},
    "ymmmem256imm8": {"L": "256", "pp": "66", "mmmm": "0F3A", "W": "W1", "opcode": "01", "mod": "/r", "imm": "ib", "evex": "1"},
    "zmmzmmimm8": {"L": "512", "pp": "66", "mmmm": "0F3A", "W": "W1", "opcode": "01", "mod": "/r", "imm": "ib", "evex": "1"},
    "zmmmem512imm8": {"L": "512", "pp": "66", "mmmm": "0F3A", "W": "W1", "opcode": "01", "mod": "/r", "imm": "ib", "evex": "1"},

    "ymmmem64imm8": {"L": "256", "pp": "66", "mmmm": "0F3A", "W": "W1", "opcode": "01", "mod": "/r", "imm": "ib", "mbr": "1", "evex": "1"},
    "zmmmem64imm8": {"L": "512", "pp": "66", "mmmm": "0F3A", "W": "W1", "opcode": "01", "mod": "/r", "imm": "ib", "mbr": "1", "evex": "1"},

    "ymmymmymm": {"vvvv": "NDS", "L": "256", "pp": "66", "mmmm": "0F38", "W": "W1", "opcode": "16", "mod": "/r", "evex": "1"},
    "ymmymmmem256": {"vvvv": "NDS", "L": "256", "pp": "66", "mmmm": "0F38", "W": "W1", "opcode": "16", "mod": "/r", "evex": "1"},
    "zmmzmmzmm": {"vvvv": "NDS", "L": "512", "pp": "66", "mmmm": "0F38", "W": "W1", "opcode": "16", "mod": "/r", "evex": "1"},
    "zmmzmmmem512": {"vvvv": "NDS", "L": "512", "pp": "66", "mmmm": "0F38", "W": "W1", "opcode": "16", "mod": "/r", "evex": "1"},

    "ymmymmmem64": {"vvvv": "NDS", "L": "256", "pp": "66", "mmmm": "0F38", "W": "W1", "opcode": "16", "mod": "/r", "mbr": "1", "evex": "1"},
    "zmmzmmmem64": {"vvvv": "NDS", "L": "512", "pp": "66", "mmmm": "0F38", "W": "W1", "opcode": "16", "mod": "/r", "mbr": "1", "evex": "1"}
}

VPBLENDD = {
    "xmmxmmxmmimm8": {"vvvv": "NDS", "L": "128", "pp": "66", "mmmm": "0F3A", "W": "W0", "opcode": "02", "mod": "/r", "imm": "ib"},
    "xmmxmmmem128imm8": {"vvvv": "NDS", "L": "128", "pp": "66", "mmmm": "0F3A", "W": "W0", "opcode": "02", "mod": "/r", "imm": "ib"},
    "ymmymmymmimm8": {"vvvv": "NDS", "L": "256", "pp": "66", "mmmm": "0F3A", "W": "W0", "opcode": "02", "mod": "/r", "imm": "ib"},
    "ymmymmmem256imm8": {"vvvv": "NDS", "L": "256", "pp": "66", "mmmm": "0F3A", "W": "W0", "opcode": "02", "mod": "/r", "imm": "ib"},
}

VPSLLVD = {
    "xmmxmmxmm": {"vvvv": "NDS", "L": "128", "pp": "66", "mmmm": "0F38", "W": "W0", "opcode": "47", "mod": "/r", "evex": "1"},
    "xmmxmmmem128": {"vvvv": "NDS", "L": "128", "pp": "66", "mmmm": "0F38", "W": "W0", "opcode": "47", "mod": "/r", "evex": "1"},
    "ymmymmymm": {"vvvv": "NDS", "L": "256", "pp": "66", "mmmm": "0F38", "W": "W0", "opcode": "47", "mod": "/r", "evex": "1"},
    "ymmymmmem256": {"vvvv": "NDS", "L": "256", "pp": "66", "mmmm": "0F38", "W": "W0", "opcode": "47", "mod": "/r", "evex": "1"},
    "zmmzmmzmm": {"vvvv": "NDS", "L": "512", "pp": "66", "mmmm": "0F38", "W": "W0", "opcode": "47", "mod": "/r", "evex": "1"},
    "zmmzmmmem512": {"vvvv": "NDS", "L": "512", "pp": "66", "mmmm": "0F38", "W": "W0", "opcode": "47", "mod": "/r", "evex": "1"},

    "xmmxmmmem32": {"vvvv": "NDS", "L": "128", "pp": "66", "mmmm": "0F38", "W": "W0", "opcode": "47", "mod": "/r", "mbr": "1", "evex": "1"},
    "ymmymmmem32": {"vvvv": "NDS", "L": "256", "pp": "66", "mmmm": "0F38", "W": "W0", "opcode": "47", "mod": "/r", "mbr": "1", "evex": "1"},
    "zmmzmmmem32": {"vvvv": "NDS", "L": "512", "pp": "66", "mmmm": "0F38", "W": "W0", "opcode": "47", "mod": "/r", "mbr": "1", "evex": "1"}
}

VPSLLVQ = {
    "xmmxmmxmm": {"vvvv": "NDS", "L": "128", "pp": "66", "mmmm": "0F38", "W": "W1", "opcode": "47", "mod": "/r", "evex": "1"},
    "xmmxmmmem128": {"vvvv": "NDS", "L": "128", "pp": "66", "mmmm": "0F38", "W": "W1", "opcode": "47", "mod": "/r", "evex": "1"},
    "ymmymmymm": {"vvvv": "NDS", "L": "256", "pp": "66", "mmmm": "0F38", "W": "W1", "opcode": "47", "mod": "/r", "evex": "1"},
    "ymmymmmem256": {"vvvv": "NDS", "L": "256", "pp": "66", "mmmm": "0F38", "W": "W1", "opcode": "47", "mod": "/r", "evex": "1"},
    "zmmzmmzmm": {"vvvv": "NDS", "L": "512", "pp": "66", "mmmm": "0F38", "W": "W1", "opcode": "47", "mod": "/r", "evex": "1"},
    "zmmzmmmem512": {"vvvv": "NDS", "L": "512", "pp": "66", "mmmm": "0F38", "W": "W1", "opcode": "47", "mod": "/r", "evex": "1"},

    "xmmxmmmem64": {"vvvv": "NDS", "L": "128", "pp": "66", "mmmm": "0F38", "W": "W1", "opcode": "47", "mod": "/r", "mbr": "1", "evex": "1"},
    "ymmymmmem64": {"vvvv": "NDS", "L": "256", "pp": "66", "mmmm": "0F38", "W": "W1", "opcode": "47", "mod": "/r", "mbr": "1", "evex": "1"},
    "zmmzmmmem64": {"vvvv": "NDS", "L": "512", "pp": "66", "mmmm": "0F38", "W": "W1", "opcode": "47", "mod": "/r", "mbr": "1", "evex": "1"}
}

VPSRAVD = {
    "xmmxmmxmm": {"vvvv": "NDS", "L": "128", "pp": "66", "mmmm": "0F38", "W": "W0", "opcode": "46", "mod": "/r", "evex": "1"},
    "xmmxmmmem128": {"vvvv": "NDS", "L": "128", "pp": "66", "mmmm": "0F38", "W": "W0", "opcode": "46", "mod": "/r", "evex": "1"},
    "ymmymmymm": {"vvvv": "NDS", "L": "256", "pp": "66", "mmmm": "0F38", "W": "W0", "opcode": "46", "mod": "/r", "evex": "1"},
    "ymmymmmem256": {"vvvv": "NDS", "L": "256", "pp": "66", "mmmm": "0F38", "W": "W0", "opcode": "46", "mod": "/r", "evex": "1"},
    "zmmzmmzmm": {"vvvv": "NDS", "L": "512", "pp": "66", "mmmm": "0F38", "W": "W0", "opcode": "46", "mod": "/r", "evex": "1"},
    "zmmzmmmem512": {"vvvv": "NDS", "L": "512", "pp": "66", "mmmm": "0F38", "W": "W0", "opcode": "46", "mod": "/r", "evex": "1"},

    "xmmxmmmem32": {"vvvv": "NDS", "L": "128", "pp": "66", "mmmm": "0F38", "W": "W0", "opcode": "46", "mod": "/r", "mbr": "1", "evex": "1"},
    "ymmymmmem32": {"vvvv": "NDS", "L": "256", "pp": "66", "mmmm": "0F38", "W": "W0", "opcode": "46", "mod": "/r", "mbr": "1", "evex": "1"},
    "zmmzmmmem32": {"vvvv": "NDS", "L": "512", "pp": "66", "mmmm": "0F38", "W": "W0", "opcode": "46", "mod": "/r", "mbr": "1", "evex": "1"}
}

VPSRLVD = {
    "xmmxmmxmm": {"vvvv": "NDS", "L": "128", "pp": "66", "mmmm": "0F38", "W": "W0", "opcode": "45", "mod": "/r", "evex": "1"},
    "xmmxmmmem128": {"vvvv": "NDS", "L": "128", "pp": "66", "mmmm": "0F38", "W": "W0", "opcode": "45", "mod": "/r", "evex": "1"},
    "ymmymmymm": {"vvvv": "NDS", "L": "256", "pp": "66", "mmmm": "0F38", "W": "W0", "opcode": "45", "mod": "/r", "evex": "1"},
    "ymmymmmem256": {"vvvv": "NDS", "L": "256", "pp": "66", "mmmm": "0F38", "W": "W0", "opcode": "45", "mod": "/r", "evex": "1"},
    "zmmzmmzmm": {"vvvv": "NDS", "L": "512", "pp": "66", "mmmm": "0F38", "W": "W0", "opcode": "45", "mod": "/r", "evex": "1"},
    "zmmzmmmem512": {"vvvv": "NDS", "L": "512", "pp": "66", "mmmm": "0F38", "W": "W0", "opcode": "45", "mod": "/r", "evex": "1"},

    "xmmxmmmem32": {"vvvv": "NDS", "L": "128", "pp": "66", "mmmm": "0F38", "W": "W0", "opcode": "45", "mod": "/r", "mbr": "1", "evex": "1"},
    "ymmymmmem32": {"vvvv": "NDS", "L": "256", "pp": "66", "mmmm": "0F38", "W": "W0", "opcode": "45", "mod": "/r", "mbr": "1", "evex": "1"},
    "zmmzmmmem32": {"vvvv": "NDS", "L": "512", "pp": "66", "mmmm": "0F38", "W": "W0", "opcode": "45", "mod": "/r", "mbr": "1", "evex": "1"}
}

VPSRLVQ = {
    "xmmxmmxmm": {"vvvv": "NDS", "L": "128", "pp": "66", "mmmm": "0F38", "W": "W1", "opcode": "45", "mod": "/r", "evex": "1"},
    "xmmxmmmem128": {"vvvv": "NDS", "L": "128", "pp": "66", "mmmm": "0F38", "W": "W1", "opcode": "45", "mod": "/r", "evex": "1"},
    "ymmymmymm": {"vvvv": "NDS", "L": "256", "pp": "66", "mmmm": "0F38", "W": "W1", "opcode": "45", "mod": "/r", "evex": "1"},
    "ymmymmmem256": {"vvvv": "NDS", "L": "256", "pp": "66", "mmmm": "0F38", "W": "W1", "opcode": "45", "mod": "/r", "evex": "1"},
    "zmmzmmzmm": {"vvvv": "NDS", "L": "512", "pp": "66", "mmmm": "0F38", "W": "W1", "opcode": "45", "mod": "/r", "evex": "1"},
    "zmmzmmmem512": {"vvvv": "NDS", "L": "512", "pp": "66", "mmmm": "0F38", "W": "W1", "opcode": "45", "mod": "/r", "evex": "1"},

    "xmmxmmmem64": {"vvvv": "NDS", "L": "128", "pp": "66", "mmmm": "0F38", "W": "W1", "opcode": "45", "mod": "/r", "mbr": "1", "evex": "1"},
    "ymmymmmem64": {"vvvv": "NDS", "L": "256", "pp": "66", "mmmm": "0F38", "W": "W1", "opcode": "45", "mod": "/r", "mbr": "1", "evex": "1"},
    "zmmzmmmem64": {"vvvv": "NDS", "L": "512", "pp": "66", "mmmm": "0F38", "W": "W1", "opcode": "45", "mod": "/r", "mbr": "1", "evex": "1"}
}
