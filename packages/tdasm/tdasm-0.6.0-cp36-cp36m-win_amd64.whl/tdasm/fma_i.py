

VFMADD132PS = {
    "xmmxmmxmm": {"vvvv": "DDS", "L": "128", "pp": "66", "mmmm": "0F38", "opcode": "98", "mod": "/r", 'W': 'W0', "evex": "1"},
    "xmmxmmmem128": {"vvvv": "DDS", "L": "128", "pp": "66", "mmmm": "0F38", "opcode": "98", "mod": "/r", 'W': 'W0', "evex": "1"},
    "ymmymmymm": {"vvvv": "DDS", "L": "256", "pp": "66", "mmmm": "0F38", "opcode": "98", "mod": "/r", 'W': 'W0', "evex": "1"},
    "ymmymmmem256": {"vvvv": "DDS", "L": "256", "pp": "66", "mmmm": "0F38", "opcode": "98", "mod": "/r", 'W': 'W0', "evex": "1"},
    "zmmzmmzmm": {"vvvv": "DDS", "L": "512", "pp": "66", "mmmm": "0F38", "opcode": "98", "mod": "/r", 'W': 'W0', "evex": "1"},
    "zmmzmmmem512": {"vvvv": "DDS", "L": "512", "pp": "66", "mmmm": "0F38", "opcode": "98", "mod": "/r", 'W': 'W0', "evex": "1"},

    "xmmxmmmem32": {"vvvv": "DDS", "L": "128", "pp": "66", "mmmm": "0F38", "opcode": "98", "mod": "/r", 'W': 'W0', "mbr": "1", "evex": "1"},
    "ymmymmmem32": {"vvvv": "DDS", "L": "256", "pp": "66", "mmmm": "0F38", "opcode": "98", "mod": "/r", 'W': 'W0', "mbr": "1", "evex": "1"},
    "zmmzmmmem32": {"vvvv": "DDS", "L": "512", "pp": "66", "mmmm": "0F38", "opcode": "98", "mod": "/r", 'W': 'W0', "mbr": "1", "evex": "1"}
}

VFMADD132SS = {
    "xmmxmmxmm": {"vvvv": "DDS", "L": "LIG", "pp": "66", "mmmm": "0F38", "opcode": "99", "mod": "/r", 'W': 'W0', "evex": "1"},
    "xmmxmmmem32": {"vvvv": "DDS", "L": "LIG", "pp": "66", "mmmm": "0F38", "opcode": "99", "mod": "/r", 'W': 'W0', "evex": "1"}
}

VFMADD132PD = {
    "xmmxmmxmm": {"vvvv": "DDS", "L": "128", "pp": "66", "mmmm": "0F38", "opcode": "98", "mod": "/r", 'W': 'W1', "evex": "1"},
    "xmmxmmmem128": {"vvvv": "DDS", "L": "128", "pp": "66", "mmmm": "0F38", "opcode": "98", "mod": "/r", 'W': 'W1', "evex": "1"},
    "ymmymmymm": {"vvvv": "DDS", "L": "256", "pp": "66", "mmmm": "0F38", "opcode": "98", "mod": "/r", 'W': 'W1', "evex": "1"},
    "ymmymmmem256": {"vvvv": "DDS", "L": "256", "pp": "66", "mmmm": "0F38", "opcode": "98", "mod": "/r", 'W': 'W1', "evex": "1"},
    "zmmzmmzmm": {"vvvv": "DDS", "L": "512", "pp": "66", "mmmm": "0F38", "opcode": "98", "mod": "/r", 'W': 'W1', "evex": "1"},
    "zmmzmmmem512": {"vvvv": "DDS", "L": "512", "pp": "66", "mmmm": "0F38", "opcode": "98", "mod": "/r", 'W': 'W1', "evex": "1"},

   "xmmxmmmem64": {"vvvv": "DDS", "L": "128", "pp": "66", "mmmm": "0F38", "opcode": "98", "mod": "/r", 'W': 'W1', "mbr": "1", "evex": "1"},
   "ymmymmmem64": {"vvvv": "DDS", "L": "256", "pp": "66", "mmmm": "0F38", "opcode": "98", "mod": "/r", 'W': 'W1', "mbr": "1", "evex": "1"},
   "zmmzmmmem64": {"vvvv": "DDS", "L": "512", "pp": "66", "mmmm": "0F38", "opcode": "98", "mod": "/r", 'W': 'W1', "mbr": "1", "evex": "1"}
}

VFMADD132SD = {
    "xmmxmmxmm": {"vvvv": "DDS", "L": "LIG", "pp": "66", "mmmm": "0F38", "opcode": "99", "mod": "/r", 'W': 'W1', "evex": "1"},
    "xmmxmmmem64": {"vvvv": "DDS", "L": "LIG", "pp": "66", "mmmm": "0F38", "opcode": "99", "mod": "/r", 'W': 'W1', "evex": "1"}
}

VFMADD213PS = {
    "xmmxmmxmm": {"vvvv": "DDS", "L": "128", "pp": "66", "mmmm": "0F38", "opcode": "A8", "mod": "/r", 'W': 'W0', "evex": "1"},
    "xmmxmmmem128": {"vvvv": "DDS", "L": "128", "pp": "66", "mmmm": "0F38", "opcode": "A8", "mod": "/r", 'W': 'W0', "evex": "1"},
    "ymmymmymm": {"vvvv": "DDS", "L": "256", "pp": "66", "mmmm": "0F38", "opcode": "A8", "mod": "/r", 'W': 'W0', "evex": "1"},
    "ymmymmmem256": {"vvvv": "DDS", "L": "256", "pp": "66", "mmmm": "0F38", "opcode": "A8", "mod": "/r", 'W': 'W0', "evex": "1"},
    "zmmzmmzmm": {"vvvv": "DDS", "L": "512", "pp": "66", "mmmm": "0F38", "opcode": "A8", "mod": "/r", 'W': 'W0', "evex": "1"},
    "zmmzmmmem512": {"vvvv": "DDS", "L": "512", "pp": "66", "mmmm": "0F38", "opcode": "A8", "mod": "/r", 'W': 'W0', "evex": "1"},

    "xmmxmmmem32": {"vvvv": "DDS", "L": "128", "pp": "66", "mmmm": "0F38", "opcode": "A8", "mod": "/r", 'W': 'W0', "mbr": "1", "evex": "1"},
    "ymmymmmem32": {"vvvv": "DDS", "L": "256", "pp": "66", "mmmm": "0F38", "opcode": "A8", "mod": "/r", 'W': 'W0', "mbr": "1", "evex": "1"},
    "zmmzmmmem32": {"vvvv": "DDS", "L": "512", "pp": "66", "mmmm": "0F38", "opcode": "A8", "mod": "/r", 'W': 'W0', "mbr": "1", "evex": "1"}
}

VFMADD213SS = {
    "xmmxmmxmm": {"vvvv": "DDS", "L": "LIG", "pp": "66", "mmmm": "0F38", "opcode": "A9", "mod": "/r", 'W': 'W0', "evex": "1"},
    "xmmxmmmem32": {"vvvv": "DDS", "L": "LIG", "pp": "66", "mmmm": "0F38", "opcode": "A9", "mod": "/r", 'W': 'W0', "evex": "1"}
}

VFMADD213PD = {
    "xmmxmmxmm": {"vvvv": "DDS", "L": "128", "pp": "66", "mmmm": "0F38", "opcode": "A8", "mod": "/r", 'W': 'W1', "evex": "1"},
    "xmmxmmmem128": {"vvvv": "DDS", "L": "128", "pp": "66", "mmmm": "0F38", "opcode": "A8", "mod": "/r", 'W': 'W1', "evex": "1"},
    "ymmymmymm": {"vvvv": "DDS", "L": "256", "pp": "66", "mmmm": "0F38", "opcode": "A8", "mod": "/r", 'W': 'W1', "evex": "1"},
    "ymmymmmem256": {"vvvv": "DDS", "L": "256", "pp": "66", "mmmm": "0F38", "opcode": "A8", "mod": "/r", 'W': 'W1', "evex": "1"},
    "zmmzmmzmm": {"vvvv": "DDS", "L": "512", "pp": "66", "mmmm": "0F38", "opcode": "A8", "mod": "/r", 'W': 'W1', "evex": "1"},
    "zmmzmmmem512": {"vvvv": "DDS", "L": "512", "pp": "66", "mmmm": "0F38", "opcode": "A8", "mod": "/r", 'W': 'W1', "evex": "1"},

    "xmmxmmmem64": {"vvvv": "DDS", "L": "128", "pp": "66", "mmmm": "0F38", "opcode": "A8", "mod": "/r", 'W': 'W1', "mbr": "1", "evex": "1"},
    "ymmymmmem64": {"vvvv": "DDS", "L": "256", "pp": "66", "mmmm": "0F38", "opcode": "A8", "mod": "/r", 'W': 'W1', "mbr": "1", "evex": "1"},
    "zmmzmmmem64": {"vvvv": "DDS", "L": "512", "pp": "66", "mmmm": "0F38", "opcode": "A8", "mod": "/r", 'W': 'W1', "mbr": "1", "evex": "1"}
}

VFMADD213SD = {
    "xmmxmmxmm": {"vvvv": "DDS", "L": "LIG", "pp": "66", "mmmm": "0F38", "opcode": "A9", "mod": "/r", 'W': 'W1', "evex": "1"},
    "xmmxmmmem64": {"vvvv": "DDS", "L": "LIG", "pp": "66", "mmmm": "0F38", "opcode": "A9", "mod": "/r", 'W': 'W1', "evex": "1"}
}

VFMADD231PS = {
    "xmmxmmxmm": {"vvvv": "DDS", "L": "128", "pp": "66", "mmmm": "0F38", "opcode": "B8", "mod": "/r", 'W': 'W0', "evex": "1"},
    "xmmxmmmem128": {"vvvv": "DDS", "L": "128", "pp": "66", "mmmm": "0F38", "opcode": "B8", "mod": "/r", 'W': 'W0', "evex": "1"},
    "ymmymmymm": {"vvvv": "DDS", "L": "256", "pp": "66", "mmmm": "0F38", "opcode": "B8", "mod": "/r", 'W': 'W0', "evex": "1"},
    "ymmymmmem256": {"vvvv": "DDS", "L": "256", "pp": "66", "mmmm": "0F38", "opcode": "B8", "mod": "/r", 'W': 'W0', "evex": "1"},
    "zmmzmmzmm": {"vvvv": "DDS", "L": "512", "pp": "66", "mmmm": "0F38", "opcode": "B8", "mod": "/r", 'W': 'W0', "evex": "1"},
    "zmmzmmmem512": {"vvvv": "DDS", "L": "512", "pp": "66", "mmmm": "0F38", "opcode": "B8", "mod": "/r", 'W': 'W0', "evex": "1"},

    "xmmxmmmem32": {"vvvv": "DDS", "L": "128", "pp": "66", "mmmm": "0F38", "opcode": "B8", "mod": "/r", 'W': 'W0', "mbr": "1", "evex": "1"},
    "ymmymmmem32": {"vvvv": "DDS", "L": "256", "pp": "66", "mmmm": "0F38", "opcode": "B8", "mod": "/r", 'W': 'W0', "mbr": "1", "evex": "1"},
    "zmmzmmmem32": {"vvvv": "DDS", "L": "512", "pp": "66", "mmmm": "0F38", "opcode": "B8", "mod": "/r", 'W': 'W0', "mbr": "1", "evex": "1"}
}

VFMADD231SS = {
    "xmmxmmxmm": {"vvvv": "DDS", "L": "LIG", "pp": "66", "mmmm": "0F38", "opcode": "B9", "mod": "/r", 'W': 'W0', "evex": "1"},
    "xmmxmmmem32": {"vvvv": "DDS", "L": "LIG", "pp": "66", "mmmm": "0F38", "opcode": "B9", "mod": "/r", 'W': 'W0', "evex": "1"}
}

VFMADD231PD = {
    "xmmxmmxmm": {"vvvv": "DDS", "L": "128", "pp": "66", "mmmm": "0F38", "opcode": "B8", "mod": "/r", 'W': 'W1', "evex": "1"},
    "xmmxmmmem128": {"vvvv": "DDS", "L": "128", "pp": "66", "mmmm": "0F38", "opcode": "B8", "mod": "/r", 'W': 'W1', "evex": "1"},
    "ymmymmymm": {"vvvv": "DDS", "L": "256", "pp": "66", "mmmm": "0F38", "opcode": "B8", "mod": "/r", 'W': 'W1', "evex": "1"},
    "ymmymmmem256": {"vvvv": "DDS", "L": "256", "pp": "66", "mmmm": "0F38", "opcode": "B8", "mod": "/r", 'W': 'W1', "evex": "1"},
    "zmmzmmzmm": {"vvvv": "DDS", "L": "512", "pp": "66", "mmmm": "0F38", "opcode": "B8", "mod": "/r", 'W': 'W1', "evex": "1"},
    "zmmzmmmem512": {"vvvv": "DDS", "L": "512", "pp": "66", "mmmm": "0F38", "opcode": "B8", "mod": "/r", 'W': 'W1', "evex": "1"},

    "xmmxmmmem64": {"vvvv": "DDS", "L": "128", "pp": "66", "mmmm": "0F38", "opcode": "B8", "mod": "/r", 'W': 'W1', "mbr": "1", "evex": "1"},
    "ymmymmmem64": {"vvvv": "DDS", "L": "256", "pp": "66", "mmmm": "0F38", "opcode": "B8", "mod": "/r", 'W': 'W1', "mbr": "1", "evex": "1"},
    "zmmzmmmem64": {"vvvv": "DDS", "L": "512", "pp": "66", "mmmm": "0F38", "opcode": "B8", "mod": "/r", 'W': 'W1', "mbr": "1", "evex": "1"}
}

VFMADD231SD = {
    "xmmxmmxmm": {"vvvv": "DDS", "L": "LIG", "pp": "66", "mmmm": "0F38", "opcode": "B9", "mod": "/r", 'W': 'W1', "evex": "1"},
    "xmmxmmmem64": {"vvvv": "DDS", "L": "LIG", "pp": "66", "mmmm": "0F38", "opcode": "B9", "mod": "/r", 'W': 'W1', "evex": "1"}
}

VFMADDSUB132PS = {
    "xmmxmmxmm": {"vvvv": "DDS", "L": "128", "pp": "66", "mmmm": "0F38", "opcode": "96", "mod": "/r", 'W': 'W0', "evex": "1"},
    "xmmxmmmem128": {"vvvv": "DDS", "L": "128", "pp": "66", "mmmm": "0F38", "opcode": "96", "mod": "/r", 'W': 'W0', "evex": "1"},
    "ymmymmymm": {"vvvv": "DDS", "L": "256", "pp": "66", "mmmm": "0F38", "opcode": "96", "mod": "/r", 'W': 'W0', "evex": "1"},
    "ymmymmmem256": {"vvvv": "DDS", "L": "256", "pp": "66", "mmmm": "0F38", "opcode": "96", "mod": "/r", 'W': 'W0', "evex": "1"},
    "zmmzmmzmm": {"vvvv": "DDS", "L": "512", "pp": "66", "mmmm": "0F38", "opcode": "96", "mod": "/r", 'W': 'W0', "evex": "1"},
    "zmmzmmmem512": {"vvvv": "DDS", "L": "512", "pp": "66", "mmmm": "0F38", "opcode": "96", "mod": "/r", 'W': 'W0', "evex": "1"},

    "xmmxmmmem32": {"vvvv": "DDS", "L": "128", "pp": "66", "mmmm": "0F38", "opcode": "96", "mod": "/r", 'W': 'W0', "mbr": "1", "evex": "1"},
    "ymmymmmem32": {"vvvv": "DDS", "L": "256", "pp": "66", "mmmm": "0F38", "opcode": "96", "mod": "/r", 'W': 'W0', "mbr": "1", "evex": "1"},
    "zmmzmmmem32": {"vvvv": "DDS", "L": "512", "pp": "66", "mmmm": "0F38", "opcode": "96", "mod": "/r", 'W': 'W0', "mbr": "1", "evex": "1"}
}

VFMADDSUB132PD = {
    "xmmxmmxmm": {"vvvv": "DDS", "L": "128", "pp": "66", "mmmm": "0F38", "opcode": "96", "mod": "/r", 'W': 'W1', "evex": "1"},
    "xmmxmmmem128": {"vvvv": "DDS", "L": "128", "pp": "66", "mmmm": "0F38", "opcode": "96", "mod": "/r", 'W': 'W1', "evex": "1"},
    "ymmymmymm": {"vvvv": "DDS", "L": "256", "pp": "66", "mmmm": "0F38", "opcode": "96", "mod": "/r", 'W': 'W1', "evex": "1"},
    "ymmymmmem256": {"vvvv": "DDS", "L": "256", "pp": "66", "mmmm": "0F38", "opcode": "96", "mod": "/r", 'W': 'W1', "evex": "1"},
    "zmmzmmzmm": {"vvvv": "DDS", "L": "512", "pp": "66", "mmmm": "0F38", "opcode": "96", "mod": "/r", 'W': 'W1', "evex": "1"},
    "zmmzmmmem512": {"vvvv": "DDS", "L": "512", "pp": "66", "mmmm": "0F38", "opcode": "96", "mod": "/r", 'W': 'W1', "evex": "1"},

    "xmmxmmmem64": {"vvvv": "DDS", "L": "128", "pp": "66", "mmmm": "0F38", "opcode": "96", "mod": "/r", 'W': 'W1', "mbr": "1", "evex": "1"},
    "ymmymmmem64": {"vvvv": "DDS", "L": "256", "pp": "66", "mmmm": "0F38", "opcode": "96", "mod": "/r", 'W': 'W1', "mbr": "1", "evex": "1"},
    "zmmzmmmem64": {"vvvv": "DDS", "L": "512", "pp": "66", "mmmm": "0F38", "opcode": "96", "mod": "/r", 'W': 'W1', "mbr": "1", "evex": "1"}
}

VFMADDSUB213PS = {
    "xmmxmmxmm": {"vvvv": "DDS", "L": "128", "pp": "66", "mmmm": "0F38", "opcode": "A6", "mod": "/r", 'W': 'W0', "evex": "1"},
    "xmmxmmmem128": {"vvvv": "DDS", "L": "128", "pp": "66", "mmmm": "0F38", "opcode": "A6", "mod": "/r", 'W': 'W0', "evex": "1"},
    "ymmymmymm": {"vvvv": "DDS", "L": "256", "pp": "66", "mmmm": "0F38", "opcode": "A6", "mod": "/r", 'W': 'W0', "evex": "1"},
    "ymmymmmem256": {"vvvv": "DDS", "L": "256", "pp": "66", "mmmm": "0F38", "opcode": "A6", "mod": "/r", 'W': 'W0', "evex": "1"},
    "zmmzmmzmm": {"vvvv": "DDS", "L": "512", "pp": "66", "mmmm": "0F38", "opcode": "A6", "mod": "/r", 'W': 'W0', "evex": "1"},
    "zmmzmmmem512": {"vvvv": "DDS", "L": "512", "pp": "66", "mmmm": "0F38", "opcode": "A6", "mod": "/r", 'W': 'W0', "evex": "1"},

    "xmmxmmmem32": {"vvvv": "DDS", "L": "128", "pp": "66", "mmmm": "0F38", "opcode": "A6", "mod": "/r", 'W': 'W0', "mbr": "1", "evex": "1"},
    "ymmymmmem32": {"vvvv": "DDS", "L": "256", "pp": "66", "mmmm": "0F38", "opcode": "A6", "mod": "/r", 'W': 'W0', "mbr": "1", "evex": "1"},
    "zmmzmmmem32": {"vvvv": "DDS", "L": "512", "pp": "66", "mmmm": "0F38", "opcode": "A6", "mod": "/r", 'W': 'W0', "mbr": "1", "evex": "1"}
}

VFMADDSUB213PD = {
    "xmmxmmxmm": {"vvvv": "DDS", "L": "128", "pp": "66", "mmmm": "0F38", "opcode": "A6", "mod": "/r", 'W': 'W1', "evex": "1"},
    "xmmxmmmem128": {"vvvv": "DDS", "L": "128", "pp": "66", "mmmm": "0F38", "opcode": "A6", "mod": "/r", 'W': 'W1', "evex": "1"},
    "ymmymmymm": {"vvvv": "DDS", "L": "256", "pp": "66", "mmmm": "0F38", "opcode": "A6", "mod": "/r", 'W': 'W1', "evex": "1"},
    "ymmymmmem256": {"vvvv": "DDS", "L": "256", "pp": "66", "mmmm": "0F38", "opcode": "A6", "mod": "/r", 'W': 'W1', "evex": "1"},
    "zmmzmmzmm": {"vvvv": "DDS", "L": "512", "pp": "66", "mmmm": "0F38", "opcode": "A6", "mod": "/r", 'W': 'W1', "evex": "1"},
    "zmmzmmmem512": {"vvvv": "DDS", "L": "512", "pp": "66", "mmmm": "0F38", "opcode": "A6", "mod": "/r", 'W': 'W1', "evex": "1"},

    "xmmxmmmem64": {"vvvv": "DDS", "L": "128", "pp": "66", "mmmm": "0F38", "opcode": "A6", "mod": "/r", 'W': 'W1', "mbr": "1", "evex": "1"},
    "ymmymmmem64": {"vvvv": "DDS", "L": "256", "pp": "66", "mmmm": "0F38", "opcode": "A6", "mod": "/r", 'W': 'W1', "mbr": "1", "evex": "1"},
    "zmmzmmmem64": {"vvvv": "DDS", "L": "512", "pp": "66", "mmmm": "0F38", "opcode": "A6", "mod": "/r", 'W': 'W1', "mbr": "1", "evex": "1"}
}

VFMADDSUB231PS = {
    "xmmxmmxmm": {"vvvv": "DDS", "L": "128", "pp": "66", "mmmm": "0F38", "opcode": "B6", "mod": "/r", 'W': 'W0', "evex": "1"},
    "xmmxmmmem128": {"vvvv": "DDS", "L": "128", "pp": "66", "mmmm": "0F38", "opcode": "B6", "mod": "/r", 'W': 'W0', "evex": "1"},
    "ymmymmymm": {"vvvv": "DDS", "L": "256", "pp": "66", "mmmm": "0F38", "opcode": "B6", "mod": "/r", 'W': 'W0', "evex": "1"},
    "ymmymmmem256": {"vvvv": "DDS", "L": "256", "pp": "66", "mmmm": "0F38", "opcode": "B6", "mod": "/r", 'W': 'W0', "evex": "1"},
    "zmmzmmzmm": {"vvvv": "DDS", "L": "512", "pp": "66", "mmmm": "0F38", "opcode": "B6", "mod": "/r", 'W': 'W0', "evex": "1"},
    "zmmzmmmem512": {"vvvv": "DDS", "L": "512", "pp": "66", "mmmm": "0F38", "opcode": "B6", "mod": "/r", 'W': 'W0', "evex": "1"},

    "xmmxmmmem32": {"vvvv": "DDS", "L": "128", "pp": "66", "mmmm": "0F38", "opcode": "B6", "mod": "/r", 'W': 'W0', "mbr": "1", "evex": "1"},
    "ymmymmmem32": {"vvvv": "DDS", "L": "256", "pp": "66", "mmmm": "0F38", "opcode": "B6", "mod": "/r", 'W': 'W0', "mbr": "1", "evex": "1"},
    "zmmzmmmem32": {"vvvv": "DDS", "L": "512", "pp": "66", "mmmm": "0F38", "opcode": "B6", "mod": "/r", 'W': 'W0', "mbr": "1", "evex": "1"}
}

VFMADDSUB231PD = {
    "xmmxmmxmm": {"vvvv": "DDS", "L": "128", "pp": "66", "mmmm": "0F38", "opcode": "B6", "mod": "/r", 'W': 'W1', "evex": "1"},
    "xmmxmmmem128": {"vvvv": "DDS", "L": "128", "pp": "66", "mmmm": "0F38", "opcode": "B6", "mod": "/r", 'W': 'W1', "evex": "1"},
    "ymmymmymm": {"vvvv": "DDS", "L": "256", "pp": "66", "mmmm": "0F38", "opcode": "B6", "mod": "/r", 'W': 'W1', "evex": "1"},
    "ymmymmmem256": {"vvvv": "DDS", "L": "256", "pp": "66", "mmmm": "0F38", "opcode": "B6", "mod": "/r", 'W': 'W1', "evex": "1"},
    "zmmzmmzmm": {"vvvv": "DDS", "L": "512", "pp": "66", "mmmm": "0F38", "opcode": "B6", "mod": "/r", 'W': 'W1', "evex": "1"},
    "zmmzmmmem512": {"vvvv": "DDS", "L": "512", "pp": "66", "mmmm": "0F38", "opcode": "B6", "mod": "/r", 'W': 'W1', "evex": "1"},

    "xmmxmmmem64": {"vvvv": "DDS", "L": "128", "pp": "66", "mmmm": "0F38", "opcode": "B6", "mod": "/r", 'W': 'W1', "mbr": "1", "evex": "1"},
    "ymmymmmem64": {"vvvv": "DDS", "L": "256", "pp": "66", "mmmm": "0F38", "opcode": "B6", "mod": "/r", 'W': 'W1', "mbr": "1", "evex": "1"},
    "zmmzmmmem64": {"vvvv": "DDS", "L": "512", "pp": "66", "mmmm": "0F38", "opcode": "B6", "mod": "/r", 'W': 'W1', "mbr": "1", "evex": "1"}
}

VFMSUBADD132PS = {
    "xmmxmmxmm": {"vvvv": "DDS", "L": "128", "pp": "66", "mmmm": "0F38", "opcode": "97", "mod": "/r", 'W': 'W0', "evex": "1"},
    "xmmxmmmem128": {"vvvv": "DDS", "L": "128", "pp": "66", "mmmm": "0F38", "opcode": "97", "mod": "/r", 'W': 'W0', "evex": "1"},
    "ymmymmymm": {"vvvv": "DDS", "L": "256", "pp": "66", "mmmm": "0F38", "opcode": "97", "mod": "/r", 'W': 'W0', "evex": "1"},
    "ymmymmmem256": {"vvvv": "DDS", "L": "256", "pp": "66", "mmmm": "0F38", "opcode": "97", "mod": "/r", 'W': 'W0', "evex": "1"},
    "zmmzmmzmm": {"vvvv": "DDS", "L": "512", "pp": "66", "mmmm": "0F38", "opcode": "97", "mod": "/r", 'W': 'W0', "evex": "1"},
    "zmmzmmmem512": {"vvvv": "DDS", "L": "512", "pp": "66", "mmmm": "0F38", "opcode": "97", "mod": "/r", 'W': 'W0', "evex": "1"},

    "xmmxmmmem32": {"vvvv": "DDS", "L": "128", "pp": "66", "mmmm": "0F38", "opcode": "97", "mod": "/r", 'W': 'W0', "mbr": "1", "evex": "1"},
    "ymmymmmem32": {"vvvv": "DDS", "L": "256", "pp": "66", "mmmm": "0F38", "opcode": "97", "mod": "/r", 'W': 'W0', "mbr": "1", "evex": "1"},
    "zmmzmmmem32": {"vvvv": "DDS", "L": "512", "pp": "66", "mmmm": "0F38", "opcode": "97", "mod": "/r", 'W': 'W0', "mbr": "1", "evex": "1"}
}

VFMSUBADD132PD = {
    "xmmxmmxmm": {"vvvv": "DDS", "L": "128", "pp": "66", "mmmm": "0F38", "opcode": "97", "mod": "/r", 'W': 'W1', "evex": "1"},
    "xmmxmmmem128": {"vvvv": "DDS", "L": "128", "pp": "66", "mmmm": "0F38", "opcode": "97", "mod": "/r", 'W': 'W1', "evex": "1"},
    "ymmymmymm": {"vvvv": "DDS", "L": "256", "pp": "66", "mmmm": "0F38", "opcode": "97", "mod": "/r", 'W': 'W1', "evex": "1"},
    "ymmymmmem256": {"vvvv": "DDS", "L": "256", "pp": "66", "mmmm": "0F38", "opcode": "97", "mod": "/r", 'W': 'W1', "evex": "1"},
    "zmmzmmzmm": {"vvvv": "DDS", "L": "512", "pp": "66", "mmmm": "0F38", "opcode": "97", "mod": "/r", 'W': 'W1', "evex": "1"},
    "zmmzmmmem512": {"vvvv": "DDS", "L": "512", "pp": "66", "mmmm": "0F38", "opcode": "97", "mod": "/r", 'W': 'W1', "evex": "1"},

    "xmmxmmmem64": {"vvvv": "DDS", "L": "128", "pp": "66", "mmmm": "0F38", "opcode": "97", "mod": "/r", 'W': 'W1', "mbr": "1", "evex": "1"},
    "ymmymmmem64": {"vvvv": "DDS", "L": "256", "pp": "66", "mmmm": "0F38", "opcode": "97", "mod": "/r", 'W': 'W1', "mbr": "1", "evex": "1"},
    "zmmzmmmem64": {"vvvv": "DDS", "L": "512", "pp": "66", "mmmm": "0F38", "opcode": "97", "mod": "/r", 'W': 'W1', "mbr": "1", "evex": "1"}
}

VFMSUBADD213PS = {
    "xmmxmmxmm": {"vvvv": "DDS", "L": "128", "pp": "66", "mmmm": "0F38", "opcode": "A7", "mod": "/r", 'W': 'W0', "evex": "1"},
    "xmmxmmmem128": {"vvvv": "DDS", "L": "128", "pp": "66", "mmmm": "0F38", "opcode": "A7", "mod": "/r", 'W': 'W0', "evex": "1"},
    "ymmymmymm": {"vvvv": "DDS", "L": "256", "pp": "66", "mmmm": "0F38", "opcode": "A7", "mod": "/r", 'W': 'W0', "evex": "1"},
    "ymmymmmem256": {"vvvv": "DDS", "L": "256", "pp": "66", "mmmm": "0F38", "opcode": "A7", "mod": "/r", 'W': 'W0', "evex": "1"},
    "zmmzmmzmm": {"vvvv": "DDS", "L": "512", "pp": "66", "mmmm": "0F38", "opcode": "A7", "mod": "/r", 'W': 'W0', "evex": "1"},
    "zmmzmmmem512": {"vvvv": "DDS", "L": "512", "pp": "66", "mmmm": "0F38", "opcode": "A7", "mod": "/r", 'W': 'W0', "evex": "1"},

    "xmmxmmmem32": {"vvvv": "DDS", "L": "128", "pp": "66", "mmmm": "0F38", "opcode": "A7", "mod": "/r", 'W': 'W0', "mbr": "1", "evex": "1"},
    "ymmymmmem32": {"vvvv": "DDS", "L": "256", "pp": "66", "mmmm": "0F38", "opcode": "A7", "mod": "/r", 'W': 'W0', "mbr": "1", "evex": "1"},
    "zmmzmmmem32": {"vvvv": "DDS", "L": "512", "pp": "66", "mmmm": "0F38", "opcode": "A7", "mod": "/r", 'W': 'W0', "mbr": "1", "evex": "1"}
}

VFMSUBADD213PD = {
    "xmmxmmxmm": {"vvvv": "DDS", "L": "128", "pp": "66", "mmmm": "0F38", "opcode": "A7", "mod": "/r", 'W': 'W1', "evex": "1"},
    "xmmxmmmem128": {"vvvv": "DDS", "L": "128", "pp": "66", "mmmm": "0F38", "opcode": "A7", "mod": "/r", 'W': 'W1', "evex": "1"},
    "ymmymmymm": {"vvvv": "DDS", "L": "256", "pp": "66", "mmmm": "0F38", "opcode": "A7", "mod": "/r", 'W': 'W1', "evex": "1"},
    "ymmymmmem256": {"vvvv": "DDS", "L": "256", "pp": "66", "mmmm": "0F38", "opcode": "A7", "mod": "/r", 'W': 'W1', "evex": "1"},
    "zmmzmmzmm": {"vvvv": "DDS", "L": "512", "pp": "66", "mmmm": "0F38", "opcode": "A7", "mod": "/r", 'W': 'W1', "evex": "1"},
    "zmmzmmmem512": {"vvvv": "DDS", "L": "512", "pp": "66", "mmmm": "0F38", "opcode": "A7", "mod": "/r", 'W': 'W1', "evex": "1"},

    "xmmxmmmem64": {"vvvv": "DDS", "L": "128", "pp": "66", "mmmm": "0F38", "opcode": "A7", "mod": "/r", 'W': 'W1', "mbr": "1", "evex": "1"},
    "ymmymmmem64": {"vvvv": "DDS", "L": "256", "pp": "66", "mmmm": "0F38", "opcode": "A7", "mod": "/r", 'W': 'W1', "mbr": "1", "evex": "1"},
    "zmmzmmmem64": {"vvvv": "DDS", "L": "512", "pp": "66", "mmmm": "0F38", "opcode": "A7", "mod": "/r", 'W': 'W1', "mbr": "1", "evex": "1"}
}

VFMSUBADD231PS = {
    "xmmxmmxmm": {"vvvv": "DDS", "L": "128", "pp": "66", "mmmm": "0F38", "opcode": "B7", "mod": "/r", 'W': 'W0', "evex": "1"},
    "xmmxmmmem128": {"vvvv": "DDS", "L": "128", "pp": "66", "mmmm": "0F38", "opcode": "B7", "mod": "/r", 'W': 'W0', "evex": "1"},
    "ymmymmymm": {"vvvv": "DDS", "L": "256", "pp": "66", "mmmm": "0F38", "opcode": "B7", "mod": "/r", 'W': 'W0', "evex": "1"},
    "ymmymmmem256": {"vvvv": "DDS", "L": "256", "pp": "66", "mmmm": "0F38", "opcode": "B7", "mod": "/r", 'W': 'W0', "evex": "1"},
    "zmmzmmzmm": {"vvvv": "DDS", "L": "512", "pp": "66", "mmmm": "0F38", "opcode": "B7", "mod": "/r", 'W': 'W0', "evex": "1"},
    "zmmzmmmem512": {"vvvv": "DDS", "L": "512", "pp": "66", "mmmm": "0F38", "opcode": "B7", "mod": "/r", 'W': 'W0', "evex": "1"},

    "xmmxmmmem32": {"vvvv": "DDS", "L": "128", "pp": "66", "mmmm": "0F38", "opcode": "B7", "mod": "/r", 'W': 'W0', "mbr": "1", "evex": "1"},
    "ymmymmmem32": {"vvvv": "DDS", "L": "256", "pp": "66", "mmmm": "0F38", "opcode": "B7", "mod": "/r", 'W': 'W0', "mbr": "1", "evex": "1"},
    "zmmzmmmem32": {"vvvv": "DDS", "L": "512", "pp": "66", "mmmm": "0F38", "opcode": "B7", "mod": "/r", 'W': 'W0', "mbr": "1", "evex": "1"}
}

VFMSUBADD231PD = {
    "xmmxmmxmm": {"vvvv": "DDS", "L": "128", "pp": "66", "mmmm": "0F38", "opcode": "B7", "mod": "/r", 'W': 'W1', "evex": "1"},
    "xmmxmmmem128": {"vvvv": "DDS", "L": "128", "pp": "66", "mmmm": "0F38", "opcode": "B7", "mod": "/r", 'W': 'W1', "evex": "1"},
    "ymmymmymm": {"vvvv": "DDS", "L": "256", "pp": "66", "mmmm": "0F38", "opcode": "B7", "mod": "/r", 'W': 'W1', "evex": "1"},
    "ymmymmmem256": {"vvvv": "DDS", "L": "256", "pp": "66", "mmmm": "0F38", "opcode": "B7", "mod": "/r", 'W': 'W1', "evex": "1"},
    "zmmzmmzmm": {"vvvv": "DDS", "L": "512", "pp": "66", "mmmm": "0F38", "opcode": "B7", "mod": "/r", 'W': 'W1', "evex": "1"},
    "zmmzmmmem512": {"vvvv": "DDS", "L": "512", "pp": "66", "mmmm": "0F38", "opcode": "B7", "mod": "/r", 'W': 'W1', "evex": "1"},

    "xmmxmmmem64": {"vvvv": "DDS", "L": "128", "pp": "66", "mmmm": "0F38", "opcode": "B7", "mod": "/r", 'W': 'W1', "mbr": "1", "evex": "1"},
    "ymmymmmem64": {"vvvv": "DDS", "L": "256", "pp": "66", "mmmm": "0F38", "opcode": "B7", "mod": "/r", 'W': 'W1', "mbr": "1", "evex": "1"},
    "zmmzmmmem64": {"vvvv": "DDS", "L": "512", "pp": "66", "mmmm": "0F38", "opcode": "B7", "mod": "/r", 'W': 'W1', "mbr": "1", "evex": "1"}
}

VFMSUB132PS = {
    "xmmxmmxmm": {"vvvv": "DDS", "L": "128", "pp": "66", "mmmm": "0F38", "opcode": "9A", "mod": "/r", 'W': 'W0', "evex": "1"},
    "xmmxmmmem128": {"vvvv": "DDS", "L": "128", "pp": "66", "mmmm": "0F38", "opcode": "9A", "mod": "/r", 'W': 'W0', "evex": "1"},
    "ymmymmymm": {"vvvv": "DDS", "L": "256", "pp": "66", "mmmm": "0F38", "opcode": "9A", "mod": "/r", 'W': 'W0', "evex": "1"},
    "ymmymmmem256": {"vvvv": "DDS", "L": "256", "pp": "66", "mmmm": "0F38", "opcode": "9A", "mod": "/r", 'W': 'W0', "evex": "1"},
    "zmmzmmzmm": {"vvvv": "DDS", "L": "512", "pp": "66", "mmmm": "0F38", "opcode": "9A", "mod": "/r", 'W': 'W0', "evex": "1"},
    "zmmzmmmem512": {"vvvv": "DDS", "L": "512", "pp": "66", "mmmm": "0F38", "opcode": "9A", "mod": "/r", 'W': 'W0', "evex": "1"},

    "xmmxmmmem32": {"vvvv": "DDS", "L": "128", "pp": "66", "mmmm": "0F38", "opcode": "9A", "mod": "/r", 'W': 'W0', "mbr": "1", "evex": "1"},
    "ymmymmmem32": {"vvvv": "DDS", "L": "256", "pp": "66", "mmmm": "0F38", "opcode": "9A", "mod": "/r", 'W': 'W0', "mbr": "1", "evex": "1"},
    "zmmzmmmem32": {"vvvv": "DDS", "L": "512", "pp": "66", "mmmm": "0F38", "opcode": "9A", "mod": "/r", 'W': 'W0', "mbr": "1", "evex": "1"}
}

VFMSUB132SS = {
    "xmmxmmxmm": {"vvvv": "DDS", "L": "LIG", "pp": "66", "mmmm": "0F38", "opcode": "9B", "mod": "/r", 'W': 'W0', "evex": "1"},
    "xmmxmmmem32": {"vvvv": "DDS", "L": "LIG", "pp": "66", "mmmm": "0F38", "opcode": "9B", "mod": "/r", 'W': 'W0', "evex": "1"}
}

VFMSUB213PS = {
    "xmmxmmxmm": {"vvvv": "DDS", "L": "128", "pp": "66", "mmmm": "0F38", "opcode": "AA", "mod": "/r", 'W': 'W0', "evex": "1"},
    "xmmxmmmem128": {"vvvv": "DDS", "L": "128", "pp": "66", "mmmm": "0F38", "opcode": "AA", "mod": "/r", 'W': 'W0', "evex": "1"},
    "ymmymmymm": {"vvvv": "DDS", "L": "256", "pp": "66", "mmmm": "0F38", "opcode": "AA", "mod": "/r", 'W': 'W0', "evex": "1"},
    "ymmymmmem256": {"vvvv": "DDS", "L": "256", "pp": "66", "mmmm": "0F38", "opcode": "AA", "mod": "/r", 'W': 'W0', "evex": "1"},
    "zmmzmmzmm": {"vvvv": "DDS", "L": "512", "pp": "66", "mmmm": "0F38", "opcode": "AA", "mod": "/r", 'W': 'W0', "evex": "1"},
    "zmmzmmmem512": {"vvvv": "DDS", "L": "512", "pp": "66", "mmmm": "0F38", "opcode": "AA", "mod": "/r", 'W': 'W0', "evex": "1"},

    "xmmxmmmem32": {"vvvv": "DDS", "L": "128", "pp": "66", "mmmm": "0F38", "opcode": "AA", "mod": "/r", 'W': 'W0', "mbr": "1", "evex": "1"},
    "ymmymmmem32": {"vvvv": "DDS", "L": "256", "pp": "66", "mmmm": "0F38", "opcode": "AA", "mod": "/r", 'W': 'W0', "mbr": "1", "evex": "1"},
    "zmmzmmmem32": {"vvvv": "DDS", "L": "512", "pp": "66", "mmmm": "0F38", "opcode": "AA", "mod": "/r", 'W': 'W0', "mbr": "1", "evex": "1"}
}

VFMSUB213SS = {
    "xmmxmmxmm": {"vvvv": "DDS", "L": "LIG", "pp": "66", "mmmm": "0F38", "opcode": "AB", "mod": "/r", 'W': 'W0', "evex": "1"},
    "xmmxmmmem32": {"vvvv": "DDS", "L": "LIG", "pp": "66", "mmmm": "0F38", "opcode": "AB", "mod": "/r", 'W': 'W0', "evex": "1"}
}

VFMSUB231PS = {
    "xmmxmmxmm": {"vvvv": "DDS", "L": "128", "pp": "66", "mmmm": "0F38", "opcode": "BA", "mod": "/r", 'W': 'W0', "evex": "1"},
    "xmmxmmmem128": {"vvvv": "DDS", "L": "128", "pp": "66", "mmmm": "0F38", "opcode": "BA", "mod": "/r", 'W': 'W0', "evex": "1"},
    "ymmymmymm": {"vvvv": "DDS", "L": "256", "pp": "66", "mmmm": "0F38", "opcode": "BA", "mod": "/r", 'W': 'W0', "evex": "1"},
    "ymmymmmem256": {"vvvv": "DDS", "L": "256", "pp": "66", "mmmm": "0F38", "opcode": "BA", "mod": "/r", 'W': 'W0', "evex": "1"},
    "zmmzmmzmm": {"vvvv": "DDS", "L": "512", "pp": "66", "mmmm": "0F38", "opcode": "BA", "mod": "/r", 'W': 'W0', "evex": "1"},
    "zmmzmmmem512": {"vvvv": "DDS", "L": "512", "pp": "66", "mmmm": "0F38", "opcode": "BA", "mod": "/r", 'W': 'W0', "evex": "1"},

    "xmmxmmmem32": {"vvvv": "DDS", "L": "128", "pp": "66", "mmmm": "0F38", "opcode": "BA", "mod": "/r", 'W': 'W0', "mbr": "1", "evex": "1"},
    "ymmymmmem32": {"vvvv": "DDS", "L": "256", "pp": "66", "mmmm": "0F38", "opcode": "BA", "mod": "/r", 'W': 'W0', "mbr": "1", "evex": "1"},
    "zmmzmmmem32": {"vvvv": "DDS", "L": "512", "pp": "66", "mmmm": "0F38", "opcode": "BA", "mod": "/r", 'W': 'W0', "mbr": "1", "evex": "1"}
}

VFMSUB231SS = {
    "xmmxmmxmm": {"vvvv": "DDS", "L": "LIG", "pp": "66", "mmmm": "0F38", "opcode": "BB", "mod": "/r", 'W': 'W0', "evex": "1"},
    "xmmxmmmem32": {"vvvv": "DDS", "L": "LIG", "pp": "66", "mmmm": "0F38", "opcode": "BB", "mod": "/r", 'W': 'W0', "evex": "1"}
}

VFMSUB132PD = {
    "xmmxmmxmm": {"vvvv": "DDS", "L": "128", "pp": "66", "mmmm": "0F38", "opcode": "9A", "mod": "/r", 'W': 'W1', "evex": "1"},
    "xmmxmmmem128": {"vvvv": "DDS", "L": "128", "pp": "66", "mmmm": "0F38", "opcode": "9A", "mod": "/r", 'W': 'W1', "evex": "1"},
    "ymmymmymm": {"vvvv": "DDS", "L": "256", "pp": "66", "mmmm": "0F38", "opcode": "9A", "mod": "/r", 'W': 'W1', "evex": "1"},
    "ymmymmmem256": {"vvvv": "DDS", "L": "256", "pp": "66", "mmmm": "0F38", "opcode": "9A", "mod": "/r", 'W': 'W1', "evex": "1"},
    "zmmzmmzmm": {"vvvv": "DDS", "L": "512", "pp": "66", "mmmm": "0F38", "opcode": "9A", "mod": "/r", 'W': 'W1', "evex": "1"},
    "zmmzmmmem512": {"vvvv": "DDS", "L": "512", "pp": "66", "mmmm": "0F38", "opcode": "9A", "mod": "/r", 'W': 'W1', "evex": "1"},

    "xmmxmmmem64": {"vvvv": "DDS", "L": "128", "pp": "66", "mmmm": "0F38", "opcode": "9A", "mod": "/r", 'W': 'W1', "mbr": "1", "evex": "1"},
    "ymmymmmem64": {"vvvv": "DDS", "L": "256", "pp": "66", "mmmm": "0F38", "opcode": "9A", "mod": "/r", 'W': 'W1', "mbr": "1", "evex": "1"},
    "zmmzmmmem64": {"vvvv": "DDS", "L": "512", "pp": "66", "mmmm": "0F38", "opcode": "9A", "mod": "/r", 'W': 'W1', "mbr": "1", "evex": "1"}
}

VFMSUB132SD = {
    "xmmxmmxmm": {"vvvv": "DDS", "L": "LIG", "pp": "66", "mmmm": "0F38", "opcode": "9B", "mod": "/r", 'W': 'W1', "evex": "1"},
    "xmmxmmmem64": {"vvvv": "DDS", "L": "LIG", "pp": "66", "mmmm": "0F38", "opcode": "9B", "mod": "/r", 'W': 'W1', "evex": "1"}
}

VFMSUB213PD = {
    "xmmxmmxmm": {"vvvv": "DDS", "L": "128", "pp": "66", "mmmm": "0F38", "opcode": "AA", "mod": "/r", 'W': 'W1', "evex": "1"},
    "xmmxmmmem128": {"vvvv": "DDS", "L": "128", "pp": "66", "mmmm": "0F38", "opcode": "AA", "mod": "/r", 'W': 'W1', "evex": "1"},
    "ymmymmymm": {"vvvv": "DDS", "L": "256", "pp": "66", "mmmm": "0F38", "opcode": "AA", "mod": "/r", 'W': 'W1', "evex": "1"},
    "ymmymmmem256": {"vvvv": "DDS", "L": "256", "pp": "66", "mmmm": "0F38", "opcode": "AA", "mod": "/r", 'W': 'W1', "evex": "1"},
    "zmmzmmzmm": {"vvvv": "DDS", "L": "512", "pp": "66", "mmmm": "0F38", "opcode": "AA", "mod": "/r", 'W': 'W1', "evex": "1"},
    "zmmzmmmem512": {"vvvv": "DDS", "L": "512", "pp": "66", "mmmm": "0F38", "opcode": "AA", "mod": "/r", 'W': 'W1', "evex": "1"},

    "xmmxmmmem64": {"vvvv": "DDS", "L": "128", "pp": "66", "mmmm": "0F38", "opcode": "AA", "mod": "/r", 'W': 'W1', "mbr": "1", "evex": "1"},
    "ymmymmmem64": {"vvvv": "DDS", "L": "256", "pp": "66", "mmmm": "0F38", "opcode": "AA", "mod": "/r", 'W': 'W1', "mbr": "1", "evex": "1"},
    "zmmzmmmem64": {"vvvv": "DDS", "L": "512", "pp": "66", "mmmm": "0F38", "opcode": "AA", "mod": "/r", 'W': 'W1', "mbr": "1", "evex": "1"}
}

VFMSUB213SD = {
    "xmmxmmxmm": {"vvvv": "DDS", "L": "LIG", "pp": "66", "mmmm": "0F38", "opcode": "AB", "mod": "/r", 'W': 'W1', "evex": "1"},
    "xmmxmmmem64": {"vvvv": "DDS", "L": "LIG", "pp": "66", "mmmm": "0F38", "opcode": "AB", "mod": "/r", 'W': 'W1', "evex": "1"}
}

VFMSUB231PD = {
    "xmmxmmxmm": {"vvvv": "DDS", "L": "128", "pp": "66", "mmmm": "0F38", "opcode": "BA", "mod": "/r", 'W': 'W1', "evex": "1"},
    "xmmxmmmem128": {"vvvv": "DDS", "L": "128", "pp": "66", "mmmm": "0F38", "opcode": "BA", "mod": "/r", 'W': 'W1', "evex": "1"},
    "ymmymmymm": {"vvvv": "DDS", "L": "256", "pp": "66", "mmmm": "0F38", "opcode": "BA", "mod": "/r", 'W': 'W1', "evex": "1"},
    "ymmymmmem256": {"vvvv": "DDS", "L": "256", "pp": "66", "mmmm": "0F38", "opcode": "BA", "mod": "/r", 'W': 'W1', "evex": "1"},
    "zmmzmmzmm": {"vvvv": "DDS", "L": "512", "pp": "66", "mmmm": "0F38", "opcode": "BA", "mod": "/r", 'W': 'W1', "evex": "1"},
    "zmmzmmmem512": {"vvvv": "DDS", "L": "512", "pp": "66", "mmmm": "0F38", "opcode": "BA", "mod": "/r", 'W': 'W1', "evex": "1"},

    "xmmxmmmem64": {"vvvv": "DDS", "L": "128", "pp": "66", "mmmm": "0F38", "opcode": "BA", "mod": "/r", 'W': 'W1', "mbr": "1", "evex": "1"},
    "ymmymmmem64": {"vvvv": "DDS", "L": "256", "pp": "66", "mmmm": "0F38", "opcode": "BA", "mod": "/r", 'W': 'W1', "mbr": "1", "evex": "1"},
    "zmmzmmmem64": {"vvvv": "DDS", "L": "512", "pp": "66", "mmmm": "0F38", "opcode": "BA", "mod": "/r", 'W': 'W1', "mbr": "1", "evex": "1"}
}

VFMSUB231SD = {
    "xmmxmmxmm": {"vvvv": "DDS", "L": "LIG", "pp": "66", "mmmm": "0F38", "opcode": "BB", "mod": "/r", 'W': 'W1', "evex": "1"},
    "xmmxmmmem64": {"vvvv": "DDS", "L": "LIG", "pp": "66", "mmmm": "0F38", "opcode": "BB", "mod": "/r", 'W': 'W1', "evex": "1"}
}

VFNMADD132PS = {
    "xmmxmmxmm": {"vvvv": "DDS", "L": "128", "pp": "66", "mmmm": "0F38", "opcode": "9C", "mod": "/r", 'W': 'W0', "evex": "1"},
    "xmmxmmmem128": {"vvvv": "DDS", "L": "128", "pp": "66", "mmmm": "0F38", "opcode": "9C", "mod": "/r", 'W': 'W0', "evex": "1"},
    "ymmymmymm": {"vvvv": "DDS", "L": "256", "pp": "66", "mmmm": "0F38", "opcode": "9C", "mod": "/r", 'W': 'W0', "evex": "1"},
    "ymmymmmem256": {"vvvv": "DDS", "L": "256", "pp": "66", "mmmm": "0F38", "opcode": "9C", "mod": "/r", 'W': 'W0', "evex": "1"},
    "zmmzmmzmm": {"vvvv": "DDS", "L": "512", "pp": "66", "mmmm": "0F38", "opcode": "9C", "mod": "/r", 'W': 'W0', "evex": "1"},
    "zmmzmmmem512": {"vvvv": "DDS", "L": "512", "pp": "66", "mmmm": "0F38", "opcode": "9C", "mod": "/r", 'W': 'W0', "evex": "1"},

    "xmmxmmmem32": {"vvvv": "DDS", "L": "128", "pp": "66", "mmmm": "0F38", "opcode": "9C", "mod": "/r", 'W': 'W0', "mbr": "1", "evex": "1"},
    "ymmymmmem32": {"vvvv": "DDS", "L": "256", "pp": "66", "mmmm": "0F38", "opcode": "9C", "mod": "/r", 'W': 'W0', "mbr": "1", "evex": "1"},
    "zmmzmmmem32": {"vvvv": "DDS", "L": "512", "pp": "66", "mmmm": "0F38", "opcode": "9C", "mod": "/r", 'W': 'W0', "mbr": "1", "evex": "1"}
}

VFNMADD132SS = {
    "xmmxmmxmm": {"vvvv": "DDS", "L": "LIG", "pp": "66", "mmmm": "0F38", "opcode": "9D", "mod": "/r", 'W': 'W0', "evex": "1"},
    "xmmxmmmem32": {"vvvv": "DDS", "L": "LIG", "pp": "66", "mmmm": "0F38", "opcode": "9D", "mod": "/r", 'W': 'W0', "evex": "1"}
}

VFNMADD213PS = {
    "xmmxmmxmm": {"vvvv": "DDS", "L": "128", "pp": "66", "mmmm": "0F38", "opcode": "AC", "mod": "/r", 'W': 'W0', "evex": "1"},
    "xmmxmmmem128": {"vvvv": "DDS", "L": "128", "pp": "66", "mmmm": "0F38", "opcode": "AC", "mod": "/r", 'W': 'W0', "evex": "1"},
    "ymmymmymm": {"vvvv": "DDS", "L": "256", "pp": "66", "mmmm": "0F38", "opcode": "AC", "mod": "/r", 'W': 'W0', "evex": "1"},
    "ymmymmmem256": {"vvvv": "DDS", "L": "256", "pp": "66", "mmmm": "0F38", "opcode": "AC", "mod": "/r", 'W': 'W0', "evex": "1"},
    "zmmzmmzmm": {"vvvv": "DDS", "L": "512", "pp": "66", "mmmm": "0F38", "opcode": "AC", "mod": "/r", 'W': 'W0', "evex": "1"},
    "zmmzmmmem512": {"vvvv": "DDS", "L": "512", "pp": "66", "mmmm": "0F38", "opcode": "AC", "mod": "/r", 'W': 'W0', "evex": "1"},

    "xmmxmmmem32": {"vvvv": "DDS", "L": "128", "pp": "66", "mmmm": "0F38", "opcode": "AC", "mod": "/r", 'W': 'W0', "mbr": "1", "evex": "1"},
    "ymmymmmem32": {"vvvv": "DDS", "L": "256", "pp": "66", "mmmm": "0F38", "opcode": "AC", "mod": "/r", 'W': 'W0', "mbr": "1", "evex": "1"},
    "zmmzmmmem32": {"vvvv": "DDS", "L": "512", "pp": "66", "mmmm": "0F38", "opcode": "AC", "mod": "/r", 'W': 'W0', "mbr": "1", "evex": "1"}
}

VFNMADD213SS = {
    "xmmxmmxmm": {"vvvv": "DDS", "L": "LIG", "pp": "66", "mmmm": "0F38", "opcode": "AD", "mod": "/r", 'W': 'W0', "evex": "1"},
    "xmmxmmmem32": {"vvvv": "DDS", "L": "LIG", "pp": "66", "mmmm": "0F38", "opcode": "AD", "mod": "/r", 'W': 'W0', "evex": "1"}
}

VFNMADD231PS = {
    "xmmxmmxmm": {"vvvv": "DDS", "L": "128", "pp": "66", "mmmm": "0F38", "opcode": "BC", "mod": "/r", 'W': 'W0', "evex": "1"},
    "xmmxmmmem128": {"vvvv": "DDS", "L": "128", "pp": "66", "mmmm": "0F38", "opcode": "BC", "mod": "/r", 'W': 'W0', "evex": "1"},
    "ymmymmymm": {"vvvv": "DDS", "L": "256", "pp": "66", "mmmm": "0F38", "opcode": "BC", "mod": "/r", 'W': 'W0', "evex": "1"},
    "ymmymmmem256": {"vvvv": "DDS", "L": "256", "pp": "66", "mmmm": "0F38", "opcode": "BC", "mod": "/r", 'W': 'W0', "evex": "1"},
    "zmmzmmzmm": {"vvvv": "DDS", "L": "512", "pp": "66", "mmmm": "0F38", "opcode": "BC", "mod": "/r", 'W': 'W0', "evex": "1"},
    "zmmzmmmem512": {"vvvv": "DDS", "L": "512", "pp": "66", "mmmm": "0F38", "opcode": "BC", "mod": "/r", 'W': 'W0', "evex": "1"},

    "xmmxmmmem32": {"vvvv": "DDS", "L": "128", "pp": "66", "mmmm": "0F38", "opcode": "BC", "mod": "/r", 'W': 'W0', "mbr": "1", "evex": "1"},
    "ymmymmmem32": {"vvvv": "DDS", "L": "256", "pp": "66", "mmmm": "0F38", "opcode": "BC", "mod": "/r", 'W': 'W0', "mbr": "1", "evex": "1"},
    "zmmzmmmem32": {"vvvv": "DDS", "L": "512", "pp": "66", "mmmm": "0F38", "opcode": "BC", "mod": "/r", 'W': 'W0', "mbr": "1", "evex": "1"}
}

VFNMADD231SS = {
    "xmmxmmxmm": {"vvvv": "DDS", "L": "LIG", "pp": "66", "mmmm": "0F38", "opcode": "BD", "mod": "/r", 'W': 'W0', "evex": "1"},
    "xmmxmmmem32": {"vvvv": "DDS", "L": "LIG", "pp": "66", "mmmm": "0F38", "opcode": "BD", "mod": "/r", 'W': 'W0', "evex": "1"},
}

VFNMADD132PD = {
    "xmmxmmxmm": {"vvvv": "DDS", "L": "128", "pp": "66", "mmmm": "0F38", "opcode": "9C", "mod": "/r", 'W': 'W1', "evex": "1"},
    "xmmxmmmem128": {"vvvv": "DDS", "L": "128", "pp": "66", "mmmm": "0F38", "opcode": "9C", "mod": "/r", 'W': 'W1', "evex": "1"},
    "ymmymmymm": {"vvvv": "DDS", "L": "256", "pp": "66", "mmmm": "0F38", "opcode": "9C", "mod": "/r", 'W': 'W1', "evex": "1"},
    "ymmymmmem256": {"vvvv": "DDS", "L": "256", "pp": "66", "mmmm": "0F38", "opcode": "9C", "mod": "/r", 'W': 'W1', "evex": "1"},
    "zmmzmmzmm": {"vvvv": "DDS", "L": "512", "pp": "66", "mmmm": "0F38", "opcode": "9C", "mod": "/r", 'W': 'W1', "evex": "1"},
    "zmmzmmmem512": {"vvvv": "DDS", "L": "512", "pp": "66", "mmmm": "0F38", "opcode": "9C", "mod": "/r", 'W': 'W1', "evex": "1"},

    "xmmxmmmem64": {"vvvv": "DDS", "L": "128", "pp": "66", "mmmm": "0F38", "opcode": "9C", "mod": "/r", 'W': 'W1', "mbr": "1", "evex": "1"},
    "ymmymmmem64": {"vvvv": "DDS", "L": "256", "pp": "66", "mmmm": "0F38", "opcode": "9C", "mod": "/r", 'W': 'W1', "mbr": "1", "evex": "1"},
    "zmmzmmmem64": {"vvvv": "DDS", "L": "512", "pp": "66", "mmmm": "0F38", "opcode": "9C", "mod": "/r", 'W': 'W1', "mbr": "1", "evex": "1"}
}

VFNMADD132SD = {
    "xmmxmmxmm": {"vvvv": "DDS", "L": "LIG", "pp": "66", "mmmm": "0F38", "opcode": "9D", "mod": "/r", 'W': 'W1', "evex": "1"},
    "xmmxmmmem64": {"vvvv": "DDS", "L": "LIG", "pp": "66", "mmmm": "0F38", "opcode": "9D", "mod": "/r", 'W': 'W1', "evex": "1"}
}

VFNMADD213PD = {
    "xmmxmmxmm": {"vvvv": "DDS", "L": "128", "pp": "66", "mmmm": "0F38", "opcode": "AC", "mod": "/r", 'W': 'W1', "evex": "1"},
    "xmmxmmmem128": {"vvvv": "DDS", "L": "128", "pp": "66", "mmmm": "0F38", "opcode": "AC", "mod": "/r", 'W': 'W1', "evex": "1"},
    "ymmymmymm": {"vvvv": "DDS", "L": "256", "pp": "66", "mmmm": "0F38", "opcode": "AC", "mod": "/r", 'W': 'W1', "evex": "1"},
    "ymmymmmem256": {"vvvv": "DDS", "L": "256", "pp": "66", "mmmm": "0F38", "opcode": "AC", "mod": "/r", 'W': 'W1', "evex": "1"},
    "zmmzmmzmm": {"vvvv": "DDS", "L": "512", "pp": "66", "mmmm": "0F38", "opcode": "AC", "mod": "/r", 'W': 'W1', "evex": "1"},
    "zmmzmmmem512": {"vvvv": "DDS", "L": "512", "pp": "66", "mmmm": "0F38", "opcode": "AC", "mod": "/r", 'W': 'W1', "evex": "1"},

    "xmmxmmmem64": {"vvvv": "DDS", "L": "128", "pp": "66", "mmmm": "0F38", "opcode": "AC", "mod": "/r", 'W': 'W1', "mbr": "1", "evex": "1"},
    "ymmymmmem64": {"vvvv": "DDS", "L": "256", "pp": "66", "mmmm": "0F38", "opcode": "AC", "mod": "/r", 'W': 'W1', "mbr": "1", "evex": "1"},
    "zmmzmmmem64": {"vvvv": "DDS", "L": "512", "pp": "66", "mmmm": "0F38", "opcode": "AC", "mod": "/r", 'W': 'W1', "mbr": "1", "evex": "1"}
}

VFNMADD213SD = {
    "xmmxmmxmm": {"vvvv": "DDS", "L": "LIG", "pp": "66", "mmmm": "0F38", "opcode": "AD", "mod": "/r", 'W': 'W1', "evex": "1"},
    "xmmxmmmem64": {"vvvv": "DDS", "L": "LIG", "pp": "66", "mmmm": "0F38", "opcode": "AD", "mod": "/r", 'W': 'W1', "evex": "1"}
}

VFNMADD231PD = {
    "xmmxmmxmm": {"vvvv": "DDS", "L": "128", "pp": "66", "mmmm": "0F38", "opcode": "BC", "mod": "/r", 'W': 'W1', "evex": "1"},
    "xmmxmmmem128": {"vvvv": "DDS", "L": "128", "pp": "66", "mmmm": "0F38", "opcode": "BC", "mod": "/r", 'W': 'W1', "evex": "1"},
    "ymmymmymm": {"vvvv": "DDS", "L": "256", "pp": "66", "mmmm": "0F38", "opcode": "BC", "mod": "/r", 'W': 'W1', "evex": "1"},
    "ymmymmmem256": {"vvvv": "DDS", "L": "256", "pp": "66", "mmmm": "0F38", "opcode": "BC", "mod": "/r", 'W': 'W1', "evex": "1"},
    "zmmzmmzmm": {"vvvv": "DDS", "L": "512", "pp": "66", "mmmm": "0F38", "opcode": "BC", "mod": "/r", 'W': 'W1', "evex": "1"},
    "zmmzmmmem512": {"vvvv": "DDS", "L": "512", "pp": "66", "mmmm": "0F38", "opcode": "BC", "mod": "/r", 'W': 'W1', "evex": "1"},

    "xmmxmmmem64": {"vvvv": "DDS", "L": "128", "pp": "66", "mmmm": "0F38", "opcode": "BC", "mod": "/r", 'W': 'W1', "mbr": "1", "evex": "1"},
    "ymmymmmem64": {"vvvv": "DDS", "L": "256", "pp": "66", "mmmm": "0F38", "opcode": "BC", "mod": "/r", 'W': 'W1', "mbr": "1", "evex": "1"},
    "zmmzmmmem64": {"vvvv": "DDS", "L": "512", "pp": "66", "mmmm": "0F38", "opcode": "BC", "mod": "/r", 'W': 'W1', "mbr": "1", "evex": "1"}
}

VFNMADD231SD = {
    "xmmxmmxmm": {"vvvv": "DDS", "L": "LIG", "pp": "66", "mmmm": "0F38", "opcode": "BD", "mod": "/r", 'W': 'W1', "evex": "1"},
    "xmmxmmmem64": {"vvvv": "DDS", "L": "LIG", "pp": "66", "mmmm": "0F38", "opcode": "BD", "mod": "/r", 'W': 'W1', "evex": "1"}
}

VFNMSUB132PS = {
    "xmmxmmxmm": {"vvvv": "DDS", "L": "128", "pp": "66", "mmmm": "0F38", "opcode": "9E", "mod": "/r", 'W': 'W0', "evex": "1"},
    "xmmxmmmem128": {"vvvv": "DDS", "L": "128", "pp": "66", "mmmm": "0F38", "opcode": "9E", "mod": "/r", 'W': 'W0', "evex": "1"},
    "ymmymmymm": {"vvvv": "DDS", "L": "256", "pp": "66", "mmmm": "0F38", "opcode": "9E", "mod": "/r", 'W': 'W0', "evex": "1"},
    "ymmymmmem256": {"vvvv": "DDS", "L": "256", "pp": "66", "mmmm": "0F38", "opcode": "9E", "mod": "/r", 'W': 'W0', "evex": "1"},
    "zmmzmmzmm": {"vvvv": "DDS", "L": "512", "pp": "66", "mmmm": "0F38", "opcode": "9E", "mod": "/r", 'W': 'W0', "evex": "1"},
    "zmmzmmmem512": {"vvvv": "DDS", "L": "512", "pp": "66", "mmmm": "0F38", "opcode": "9E", "mod": "/r", 'W': 'W0', "evex": "1"},

    "xmmxmmmem32": {"vvvv": "DDS", "L": "128", "pp": "66", "mmmm": "0F38", "opcode": "9E", "mod": "/r", 'W': 'W0', "mbr": "1", "evex": "1"},
    "ymmymmmem32": {"vvvv": "DDS", "L": "256", "pp": "66", "mmmm": "0F38", "opcode": "9E", "mod": "/r", 'W': 'W0', "mbr": "1", "evex": "1"},
    "zmmzmmmem32": {"vvvv": "DDS", "L": "512", "pp": "66", "mmmm": "0F38", "opcode": "9E", "mod": "/r", 'W': 'W0', "mbr": "1", "evex": "1"}
}

VFNMSUB132SS = {
    "xmmxmmxmm": {"vvvv": "DDS", "L": "LIG", "pp": "66", "mmmm": "0F38", "opcode": "9F", "mod": "/r", 'W': 'W0', "evex": "1"},
    "xmmxmmmem32": {"vvvv": "DDS", "L": "LIG", "pp": "66", "mmmm": "0F38", "opcode": "9F", "mod": "/r", 'W': 'W0', "evex": "1"}
}

VFNMSUB213PS = {
    "xmmxmmxmm": {"vvvv": "DDS", "L": "128", "pp": "66", "mmmm": "0F38", "opcode": "AE", "mod": "/r", 'W': 'W0', "evex": "1"},
    "xmmxmmmem128": {"vvvv": "DDS", "L": "128", "pp": "66", "mmmm": "0F38", "opcode": "AE", "mod": "/r", 'W': 'W0', "evex": "1"},
    "ymmymmymm": {"vvvv": "DDS", "L": "256", "pp": "66", "mmmm": "0F38", "opcode": "AE", "mod": "/r", 'W': 'W0', "evex": "1"},
    "ymmymmmem256": {"vvvv": "DDS", "L": "256", "pp": "66", "mmmm": "0F38", "opcode": "AE", "mod": "/r", 'W': 'W0', "evex": "1"},
    "zmmzmmzmm": {"vvvv": "DDS", "L": "512", "pp": "66", "mmmm": "0F38", "opcode": "AE", "mod": "/r", 'W': 'W0', "evex": "1"},
    "zmmzmmmem512": {"vvvv": "DDS", "L": "512", "pp": "66", "mmmm": "0F38", "opcode": "AE", "mod": "/r", 'W': 'W0', "evex": "1"},

    "xmmxmmmem32": {"vvvv": "DDS", "L": "128", "pp": "66", "mmmm": "0F38", "opcode": "AE", "mod": "/r", 'W': 'W0', "mbr": "1", "evex": "1"},
    "ymmymmmem32": {"vvvv": "DDS", "L": "256", "pp": "66", "mmmm": "0F38", "opcode": "AE", "mod": "/r", 'W': 'W0', "mbr": "1", "evex": "1"},
    "zmmzmmmem32": {"vvvv": "DDS", "L": "512", "pp": "66", "mmmm": "0F38", "opcode": "AE", "mod": "/r", 'W': 'W0', "mbr": "1", "evex": "1"}
}

VFNMSUB213SS = {
    "xmmxmmxmm": {"vvvv": "DDS", "L": "LIG", "pp": "66", "mmmm": "0F38", "opcode": "AF", "mod": "/r", 'W': 'W0', "evex": "1"},
    "xmmxmmmem32": {"vvvv": "DDS", "L": "LIG", "pp": "66", "mmmm": "0F38", "opcode": "AF", "mod": "/r", 'W': 'W0', "evex": "1"}
}

VFNMSUB231PS = {
    "xmmxmmxmm": {"vvvv": "DDS", "L": "128", "pp": "66", "mmmm": "0F38", "opcode": "BE", "mod": "/r", 'W': 'W0', "evex": "1"},
    "xmmxmmmem128": {"vvvv": "DDS", "L": "128", "pp": "66", "mmmm": "0F38", "opcode": "BE", "mod": "/r", 'W': 'W0', "evex": "1"},
    "ymmymmymm": {"vvvv": "DDS", "L": "256", "pp": "66", "mmmm": "0F38", "opcode": "BE", "mod": "/r", 'W': 'W0', "evex": "1"},
    "ymmymmmem256": {"vvvv": "DDS", "L": "256", "pp": "66", "mmmm": "0F38", "opcode": "BE", "mod": "/r", 'W': 'W0', "evex": "1"},
    "zmmzmmzmm": {"vvvv": "DDS", "L": "512", "pp": "66", "mmmm": "0F38", "opcode": "BE", "mod": "/r", 'W': 'W0', "evex": "1"},
    "zmmzmmmem512": {"vvvv": "DDS", "L": "512", "pp": "66", "mmmm": "0F38", "opcode": "BE", "mod": "/r", 'W': 'W0', "evex": "1"},

    "xmmxmmmem32": {"vvvv": "DDS", "L": "128", "pp": "66", "mmmm": "0F38", "opcode": "BE", "mod": "/r", 'W': 'W0', "mbr": "1", "evex": "1"},
    "ymmymmmem32": {"vvvv": "DDS", "L": "256", "pp": "66", "mmmm": "0F38", "opcode": "BE", "mod": "/r", 'W': 'W0', "mbr": "1", "evex": "1"},
    "zmmzmmmem32": {"vvvv": "DDS", "L": "512", "pp": "66", "mmmm": "0F38", "opcode": "BE", "mod": "/r", 'W': 'W0', "mbr": "1", "evex": "1"}
}

VFNMSUB231SS = {
    "xmmxmmxmm": {"vvvv": "DDS", "L": "LIG", "pp": "66", "mmmm": "0F38", "opcode": "BF", "mod": "/r", 'W': 'W0', "evex": "1"},
    "xmmxmmmem32": {"vvvv": "DDS", "L": "LIG", "pp": "66", "mmmm": "0F38", "opcode": "BF", "mod": "/r", 'W': 'W0', "evex": "1"}
}

VFNMSUB132PD = {
    "xmmxmmxmm": {"vvvv": "DDS", "L": "128", "pp": "66", "mmmm": "0F38", "opcode": "9E", "mod": "/r", 'W': 'W1', "evex": "1"},
    "xmmxmmmem128": {"vvvv": "DDS", "L": "128", "pp": "66", "mmmm": "0F38", "opcode": "9E", "mod": "/r", 'W': 'W1', "evex": "1"},
    "ymmymmymm": {"vvvv": "DDS", "L": "256", "pp": "66", "mmmm": "0F38", "opcode": "9E", "mod": "/r", 'W': 'W1', "evex": "1"},
    "ymmymmmem256": {"vvvv": "DDS", "L": "256", "pp": "66", "mmmm": "0F38", "opcode": "9E", "mod": "/r", 'W': 'W1', "evex": "1"},
    "zmmzmmzmm": {"vvvv": "DDS", "L": "512", "pp": "66", "mmmm": "0F38", "opcode": "9E", "mod": "/r", 'W': 'W1', "evex": "1"},
    "zmmzmmmem512": {"vvvv": "DDS", "L": "512", "pp": "66", "mmmm": "0F38", "opcode": "9E", "mod": "/r", 'W': 'W1', "evex": "1"},

    "xmmxmmmem64": {"vvvv": "DDS", "L": "128", "pp": "66", "mmmm": "0F38", "opcode": "9E", "mod": "/r", 'W': 'W1', "mbr": "1", "evex": "1"},
    "ymmymmmem64": {"vvvv": "DDS", "L": "256", "pp": "66", "mmmm": "0F38", "opcode": "9E", "mod": "/r", 'W': 'W1', "mbr": "1", "evex": "1"},
    "zmmzmmmem64": {"vvvv": "DDS", "L": "512", "pp": "66", "mmmm": "0F38", "opcode": "9E", "mod": "/r", 'W': 'W1', "mbr": "1", "evex": "1"}
}

VFNMSUB132SD = {
    "xmmxmmxmm": {"vvvv": "DDS", "L": "LIG", "pp": "66", "mmmm": "0F38", "opcode": "9F", "mod": "/r", 'W': 'W1', "evex": "1"},
    "xmmxmmmem64": {"vvvv": "DDS", "L": "LIG", "pp": "66", "mmmm": "0F38", "opcode": "9F", "mod": "/r", 'W': 'W1', "evex": "1"}
}

VFNMSUB213PD = {
    "xmmxmmxmm": {"vvvv": "DDS", "L": "128", "pp": "66", "mmmm": "0F38", "opcode": "AE", "mod": "/r", 'W': 'W1', "evex": "1"},
    "xmmxmmmem128": {"vvvv": "DDS", "L": "128", "pp": "66", "mmmm": "0F38", "opcode": "AE", "mod": "/r", 'W': 'W1', "evex": "1"},
    "ymmymmymm": {"vvvv": "DDS", "L": "256", "pp": "66", "mmmm": "0F38", "opcode": "AE", "mod": "/r", 'W': 'W1', "evex": "1"},
    "ymmymmmem256": {"vvvv": "DDS", "L": "256", "pp": "66", "mmmm": "0F38", "opcode": "AE", "mod": "/r", 'W': 'W1', "evex": "1"},
    "zmmzmmzmm": {"vvvv": "DDS", "L": "512", "pp": "66", "mmmm": "0F38", "opcode": "AE", "mod": "/r", 'W': 'W1', "evex": "1"},
    "zmmzmmmem512": {"vvvv": "DDS", "L": "512", "pp": "66", "mmmm": "0F38", "opcode": "AE", "mod": "/r", 'W': 'W1', "evex": "1"},

    "xmmxmmmem64": {"vvvv": "DDS", "L": "128", "pp": "66", "mmmm": "0F38", "opcode": "AE", "mod": "/r", 'W': 'W1', "mbr": "1", "evex": "1"},
    "ymmymmmem64": {"vvvv": "DDS", "L": "256", "pp": "66", "mmmm": "0F38", "opcode": "AE", "mod": "/r", 'W': 'W1', "mbr": "1", "evex": "1"},
    "zmmzmmmem64": {"vvvv": "DDS", "L": "512", "pp": "66", "mmmm": "0F38", "opcode": "AE", "mod": "/r", 'W': 'W1', "mbr": "1", "evex": "1"}
}

VFNMSUB213SD = {
    "xmmxmmxmm": {"vvvv": "DDS", "L": "LIG", "pp": "66", "mmmm": "0F38", "opcode": "AF", "mod": "/r", 'W': 'W1', "evex": "1"},
    "xmmxmmmem64": {"vvvv": "DDS", "L": "LIG", "pp": "66", "mmmm": "0F38", "opcode": "AF", "mod": "/r", 'W': 'W1', "evex": "1"}
}

VFNMSUB231PD = {
    "xmmxmmxmm": {"vvvv": "DDS", "L": "128", "pp": "66", "mmmm": "0F38", "opcode": "BE", "mod": "/r", 'W': 'W1', "evex": "1"},
    "xmmxmmmem128": {"vvvv": "DDS", "L": "128", "pp": "66", "mmmm": "0F38", "opcode": "BE", "mod": "/r", 'W': 'W1', "evex": "1"},
    "ymmymmymm": {"vvvv": "DDS", "L": "256", "pp": "66", "mmmm": "0F38", "opcode": "BE", "mod": "/r", 'W': 'W1', "evex": "1"},
    "ymmymmmem256": {"vvvv": "DDS", "L": "256", "pp": "66", "mmmm": "0F38", "opcode": "BE", "mod": "/r", 'W': 'W1', "evex": "1"},
    "zmmzmmzmm": {"vvvv": "DDS", "L": "512", "pp": "66", "mmmm": "0F38", "opcode": "BE", "mod": "/r", 'W': 'W1', "evex": "1"},
    "zmmzmmmem512": {"vvvv": "DDS", "L": "512", "pp": "66", "mmmm": "0F38", "opcode": "BE", "mod": "/r", 'W': 'W1', "evex": "1"},

    "xmmxmmmem64": {"vvvv": "DDS", "L": "128", "pp": "66", "mmmm": "0F38", "opcode": "BE", "mod": "/r", 'W': 'W1', "mbr": "1", "evex": "1"},
    "ymmymmmem64": {"vvvv": "DDS", "L": "256", "pp": "66", "mmmm": "0F38", "opcode": "BE", "mod": "/r", 'W': 'W1', "mbr": "1", "evex": "1"},
    "zmmzmmmem64": {"vvvv": "DDS", "L": "512", "pp": "66", "mmmm": "0F38", "opcode": "BE", "mod": "/r", 'W': 'W1', "mbr": "1", "evex": "1"}
}

VFNMSUB231SD = {
    "xmmxmmxmm": {"vvvv": "DDS", "L": "LIG", "pp": "66", "mmmm": "0F38", "opcode": "BF", "mod": "/r", 'W': 'W1', "evex": "1"},
    "xmmxmmmem64": {"vvvv": "DDS", "L": "LIG", "pp": "66", "mmmm": "0F38", "opcode": "BF", "mod": "/r", 'W': 'W1', "evex": "1"}
}
