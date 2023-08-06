

# AVX MMX Instruction

VMOVD = {
    "xmmr32": {"L": "128", "pp": "66", "mmmm": "0F", "W": "W0", "opcode": "6E", "mod": "/r", "evex": "1"},
    "xmmmem32": {"L": "128", "pp": "66", "mmmm": "0F", "W": "W0", "opcode": "6E", "mod": "/r", "evex": "1"},
    "r32xmm": {"L": "128", "pp": "66", "mmmm": "0F", "W": "W0", "opcode": "7E", "mod": "/r", "rm": "1", "evex": "1"},
    "mem32xmm": {"L": "128", "pp": "66", "mmmm": "0F", "W": "W0", "opcode": "7E", "mod": "/r", "evex": "1"},
}

VMOVQ = {
    "xmmxmm": {"L": "128", "pp": "F3", "mmmm": "0F", "W": "WIG", "W512": "W1", "opcode": "7E", "mod": "/r", "evex": "1"},
    "xmmmem64": {"L": "128", "pp": "F3", "mmmm": "0F", "W": "WIG", "W512": "W1", "opcode": "7E", "mod": "/r", "evex": "1"},
    "mem64xmm": {"L": "128", "pp": "66", "mmmm": "0F", "W": "WIG", "W512":"W1", "opcode": "D6", "mod": "/r", "evex": "1"},

    "xmmr64": {"L": "128", "pp": "66", "mmmm": "0F", "W": "W1", "opcode": "6E", "mod": "/r", "evex": "1"},
    # "xmmmem64": {"L": "128", "pp": "66", "mmmm": "0F", "W": "W1", "opcode": "6E", "mod": "/r", "evex": "1"},
    "r64xmm": {"L": "128", "pp": "66", "mmmm": "0F", "W": "W1", "opcode": "7E", "mod": "/r", "rm": "1", "evex": "1"},
    # "mem64xmm": {"L": "128", "pp": "66", "mmmm": "0F", "W": "W1", "opcode": "7E", "mod": "/r", "evex": "1"},
}


VPACKSSWB = {
    "xmmxmmxmm": {"vvvv": "NDS", "L": "128", "pp": "66", "mmmm": "0F", "W": "WIG", "opcode": "63", "mod": "/r", "evex": "1"},
    "xmmxmmmem128": {"vvvv": "NDS", "L": "128", "pp": "66", "mmmm": "0F", "W": "WIG", "opcode": "63", "mod": "/r", "evex":"1"},
    "ymmymmymm": {"vvvv": "NDS", "L": "256", "pp": "66", "mmmm": "0F", "W": "WIG", "opcode": "63", "mod": "/r", "evex": "1"},
    "ymmymmmem256": {"vvvv": "NDS", "L": "256", "pp": "66", "mmmm": "0F", "W": "WIG", "opcode": "63", "mod": "/r", "evex": "1"},
    "zmmzmmzmm": {"vvvv": "NDS", "L": "512", "pp": "66", "mmmm": "0F", "W": "WIG", "opcode": "63", "mod": "/r", "evex": "1"},
    "zmmzmmmem512": {"vvvv": "NDS", "L": "512", "pp": "66", "mmmm": "0F", "W": "WIG", "opcode": "63", "mod": "/r", "evex": "1"}
}

VPACKSSDW = {
    "xmmxmmxmm": {"vvvv": "NDS", "L": "128", "pp": "66", "mmmm": "0F", "W": "WIG", "W512": "W0", "opcode": "6B", "mod": "/r", "evex": "1"},
    "xmmxmmmem128": {"vvvv": "NDS", "L": "128", "pp": "66", "mmmm": "0F", "W": "WIG", "W512": "W0", "opcode": "6B", "mod": "/r", "evex": "1"},
    "ymmymmymm": {"vvvv": "NDS", "L": "256", "pp": "66", "mmmm": "0F", "W": "WIG", "W512": "W0", "opcode": "6B", "mod": "/r", "evex": "1"},
    "ymmymmmem256": {"vvvv": "NDS", "L": "256", "pp": "66", "mmmm": "0F", "W": "WIG", "W512": "W0", "opcode": "6B", "mod": "/r", "evex": "1"},
    "zmmzmmzmm": {"vvvv": "NDS", "L": "512", "pp": "66", "mmmm": "0F", "W": "WIG", "W512": "W0", "opcode": "6B", "mod": "/r", "evex": "1"},
    "zmmzmmmem512": {"vvvv": "NDS", "L": "512", "pp": "66", "mmmm": "0F", "W": "WIG", "W512": "W0", "opcode": "6B", "mod": "/r", "evex": "1"},

    "xmmxmmmem32": {"vvvv": "NDS", "L": "128", "pp": "66", "mmmm": "0F", "W": "WIG", "W512": "W0", "opcode": "6B", "mod": "/r", "mbr":"1", "evex": "1"},
    "ymmymmmem32": {"vvvv": "NDS", "L": "256", "pp": "66", "mmmm": "0F", "W": "WIG", "W512": "W0", "opcode": "6B", "mod": "/r", "mbr": "1", "evex": "1"},
    "zmmzmmmem32": {"vvvv": "NDS", "L": "512", "pp": "66", "mmmm": "0F", "W": "WIG", "W512": "W0", "opcode": "6B", "mod": "/r", "mbr": "1", "evex": "1"}
}

VPACKUSWB = {
    "xmmxmmxmm": {"vvvv": "NDS", "L": "128", "pp": "66", "mmmm": "0F", "W": "WIG", "opcode": "67", "mod": "/r", "evex": "1"},
    "xmmxmmmem128": {"vvvv": "NDS", "L": "128", "pp": "66", "mmmm": "0F", "W": "WIG", "opcode": "67", "mod": "/r", "evex": "1"},
    "ymmymmymm": {"vvvv": "NDS", "L": "256", "pp": "66", "mmmm": "0F", "W": "WIG", "opcode": "67", "mod": "/r", "evex": "1"},
    "ymmymmmem256": {"vvvv": "NDS", "L": "256", "pp": "66", "mmmm": "0F", "W": "WIG", "opcode": "67", "mod": "/r", "evex": "1"},
    "zmmzmmzmm": {"vvvv": "NDS", "L": "512", "pp": "66", "mmmm": "0F", "W": "WIG", "opcode": "67", "mod": "/r", "evex": "1"},
    "zmmzmmmem512": {"vvvv": "NDS", "L": "512", "pp": "66", "mmmm": "0F", "W": "WIG", "opcode": "67", "mod": "/r", "evex": "1"}
}

VPUNPCKHBW = {
    "xmmxmmxmm": {"vvvv": "NDS", "L": "128", "pp": "66", "mmmm": "0F", "W": "WIG", "opcode": "68", "mod": "/r", "evex": "1"},
    "xmmxmmmem128": {"vvvv": "NDS", "L": "128", "pp": "66", "mmmm": "0F", "W": "WIG", "opcode": "68", "mod": "/r", "evex": "1"},
    "ymmymmymm": {"vvvv": "NDS", "L": "256", "pp": "66", "mmmm": "0F", "W": "WIG", "opcode": "68", "mod": "/r", "evex": "1"},
    "ymmymmmem256": {"vvvv": "NDS", "L": "256", "pp": "66", "mmmm": "0F", "W": "WIG", "opcode": "68", "mod": "/r", "evex": "1"},
    "zmmzmmzmm": {"vvvv": "NDS", "L": "512", "pp": "66", "mmmm": "0F", "W": "WIG", "opcode": "68", "mod": "/r", "evex": "1"},
    "zmmzmmmem512": {"vvvv": "NDS", "L": "512", "pp": "66", "mmmm": "0F", "W": "WIG", "opcode": "68", "mod": "/r", "evex": "1"}
}

VPUNPCKHWD = {
    "xmmxmmxmm": {"vvvv": "NDS", "L": "128", "pp": "66", "mmmm": "0F", "W": "WIG", "opcode": "69", "mod": "/r", "evex": "1"},
    "xmmxmmmem128": {"vvvv": "NDS", "L": "128", "pp": "66", "mmmm": "0F", "W": "WIG", "opcode": "69", "mod": "/r", "evex": "1"},
    "ymmymmymm": {"vvvv": "NDS", "L": "256", "pp": "66", "mmmm": "0F", "W": "WIG", "opcode": "69", "mod": "/r", "evex": "1"},
    "ymmymmmem256": {"vvvv": "NDS", "L": "256", "pp": "66", "mmmm": "0F", "W": "WIG", "opcode": "69", "mod": "/r", "evex": "1"},
    "zmmzmmzmm": {"vvvv": "NDS", "L": "512", "pp": "66", "mmmm": "0F", "W": "WIG", "opcode": "69", "mod": "/r", "evex": "1"},
    "zmmzmmmem512": {"vvvv": "NDS", "L": "512", "pp": "66", "mmmm": "0F", "W": "WIG", "opcode": "69", "mod": "/r", "evex": "1"}
}

VPUNPCKHDQ = {
    "xmmxmmxmm": {"vvvv": "NDS", "L": "128", "pp": "66", "mmmm": "0F", "W": "WIG", "W512": "W0", "opcode": "6A", "mod": "/r", "evex": "1"},
    "xmmxmmmem128": {"vvvv": "NDS", "L": "128", "pp": "66", "mmmm": "0F", "W": "WIG", "W512": "W0", "opcode": "6A", "mod": "/r", "evex": "1"},
    "ymmymmymm": {"vvvv": "NDS", "L": "256", "pp": "66", "mmmm": "0F", "W": "WIG", "W512": "W0", "opcode": "6A", "mod": "/r", "evex": "1"},
    "ymmymmmem256": {"vvvv": "NDS", "L": "256", "pp": "66", "mmmm": "0F", "W": "WIG", "W512": "W0", "opcode": "6A", "mod": "/r", "evex": "1"},
    "zmmzmmzmm": {"vvvv": "NDS", "L": "512", "pp": "66", "mmmm": "0F", "W": "WIG", "W512": "W0", "opcode": "6A", "mod": "/r", "evex": "1"},
    "zmmzmmmem512": {"vvvv": "NDS", "L": "512", "pp": "66", "mmmm": "0F", "W": "WIG", "W512": "W0", "opcode": "6A", "mod": "/r", "evex": "1"},

    "xmmxmmmem32": {"vvvv": "NDS", "L": "128", "pp": "66", "mmmm": "0F", "W": "WIG", "W512": "W0", "opcode": "6A", "mod": "/r", "mbr": "1", "evex": "1"},
    "ymmymmmem32": {"vvvv": "NDS", "L": "256", "pp": "66", "mmmm": "0F", "W": "WIG", "W512": "W0", "opcode": "6A", "mod": "/r", "mbr": "1", "evex": "1"},
    "zmmzmmmem32": {"vvvv": "NDS", "L": "512", "pp": "66", "mmmm": "0F", "W": "WIG", "W512": "W0", "opcode": "6A", "mod": "/r", "mbr": "1", "evex": "1"},
}

VPUNPCKLBW = {
    "xmmxmmxmm": {"vvvv": "NDS", "L": "128", "pp": "66", "mmmm": "0F", "W": "WIG", "opcode": "60", "mod": "/r", "evex": "1"},
    "xmmxmmmem128": {"vvvv": "NDS", "L": "128", "pp": "66", "mmmm": "0F", "W": "WIG", "opcode": "60", "mod": "/r", "evex": "1"},
    "ymmymmymm": {"vvvv": "NDS", "L": "256", "pp": "66", "mmmm": "0F", "W": "WIG", "opcode": "60", "mod": "/r", "evex": "1"},
    "ymmymmmem256": {"vvvv": "NDS", "L": "256", "pp": "66", "mmmm": "0F", "W": "WIG", "opcode": "60", "mod": "/r", "evex": "1"},
    "zmmzmmzmm": {"vvvv": "NDS", "L": "512", "pp": "66", "mmmm": "0F", "W": "WIG", "opcode": "60", "mod": "/r", "evex": "1"},
    "zmmzmmmem512": {"vvvv": "NDS", "L": "512", "pp": "66", "mmmm": "0F", "W": "WIG", "opcode": "60", "mod": "/r", "evex": "1"}
}

VPUNPCKLWD = {
    "xmmxmmxmm": {"vvvv": "NDS", "L": "128", "pp": "66", "mmmm": "0F", "W": "WIG", "opcode": "61", "mod": "/r", "evex": "1"},
    "xmmxmmmem128": {"vvvv": "NDS", "L": "128", "pp": "66", "mmmm": "0F", "W": "WIG", "opcode": "61", "mod": "/r", "evex": "1"},
    "ymmymmymm": {"vvvv": "NDS", "L": "256", "pp": "66", "mmmm": "0F", "W": "WIG", "opcode": "61", "mod": "/r", "evex": "1"},
    "ymmymmmem256": {"vvvv": "NDS", "L": "256", "pp": "66", "mmmm": "0F", "W": "WIG", "opcode": "61", "mod": "/r", "evex": "1"},
    "zmmzmmzmm": {"vvvv": "NDS", "L": "512", "pp": "66", "mmmm": "0F", "W": "WIG", "opcode": "61", "mod": "/r", "evex": "1"},
    "zmmzmmmem512": {"vvvv": "NDS", "L": "512", "pp": "66", "mmmm": "0F", "W": "WIG", "opcode": "61", "mod": "/r", "evex": "1"}
}

VPUNPCKLDQ = {
    "xmmxmmxmm": {"vvvv": "NDS", "L": "128", "pp": "66", "mmmm": "0F", "W": "WIG", "W512": "W0", "opcode": "62", "mod": "/r", "evex": "1"},
    "xmmxmmmem128": {"vvvv": "NDS", "L": "128", "pp": "66", "mmmm": "0F", "W": "WIG", "W512": "W0", "opcode": "62", "mod": "/r", "evex": "1"},
    "ymmymmymm": {"vvvv": "NDS", "L": "256", "pp": "66", "mmmm": "0F", "W": "WIG", "W512": "W0", "opcode": "62", "mod": "/r", "evex": "1"},
    "ymmymmmem256": {"vvvv": "NDS", "L": "256", "pp": "66", "mmmm": "0F", "W": "WIG", "W512": "W0", "opcode": "62", "mod": "/r", "evex": "1"},
    "zmmzmmzmm": {"vvvv": "NDS", "L": "512", "pp": "66", "mmmm": "0F", "W": "WIG", "W512": "W0", "opcode": "62", "mod": "/r", "evex": "1"},
    "zmmzmmmem512": {"vvvv": "NDS", "L": "512", "pp": "66", "mmmm": "0F", "W": "WIG", "W512": "W0", "opcode": "62", "mod": "/r", "evex": "1"},

    "xmmxmmmem32": {"vvvv": "NDS", "L": "128", "pp": "66", "mmmm": "0F", "W": "WIG", "W512": "W0", "opcode": "62", "mod": "/r", "mbr": "1", "evex": "1"},
    "ymmymmmem32": {"vvvv": "NDS", "L": "256", "pp": "66", "mmmm": "0F", "W": "WIG", "W512": "W0", "opcode": "62", "mod": "/r", "mbr": "1", "evex": "1"},
    "zmmzmmmem32": {"vvvv": "NDS", "L": "512", "pp": "66", "mmmm": "0F", "W": "WIG", "W512": "W0", "opcode": "62", "mod": "/r", "mbr": "1", "evex": "1"},
}

VPADDB = {
    "xmmxmmxmm": {"vvvv": "NDS", "L": "128", "pp": "66", "mmmm": "0F", "W": "WIG", "opcode": "FC", "mod": "/r", "evex": "1"},
    "xmmxmmmem128": {"vvvv": "NDS", "L": "128", "pp": "66", "mmmm": "0F", "W": "WIG", "opcode": "FC", "mod": "/r", "evex": "1"},
    "ymmymmymm": {"vvvv": "NDS", "L": "256", "pp": "66", "mmmm": "0F", "W": "WIG", "opcode": "FC", "mod": "/r", "evex": "1"},
    "ymmymmmem256": {"vvvv": "NDS", "L": "256", "pp": "66", "mmmm": "0F", "W": "WIG", "opcode": "FC", "mod": "/r", "evex": "1"},
    "zmmzmmzmm": {"vvvv": "NDS", "L": "512", "pp": "66", "mmmm": "0F", "W": "WIG", "opcode": "FC", "mod": "/r", "evex": "1"},
    "zmmzmmmem512": {"vvvv": "NDS", "L": "512", "pp": "66", "mmmm": "0F", "W": "WIG", "opcode": "FC", "mod": "/r", "evex": "1"}
}

VPADDW = {
    "xmmxmmxmm": {"vvvv": "NDS", "L": "128", "pp": "66", "mmmm": "0F", "W": "WIG", "opcode": "FD", "mod": "/r", "evex": "1"},
    "xmmxmmmem128": {"vvvv": "NDS", "L": "128", "pp": "66", "mmmm": "0F", "W": "WIG", "opcode": "FD", "mod": "/r", "evex": "1"},
    "ymmymmymm": {"vvvv": "NDS", "L": "256", "pp": "66", "mmmm": "0F", "W": "WIG", "opcode": "FD", "mod": "/r", "evex": "1"},
    "ymmymmmem256": {"vvvv": "NDS", "L": "256", "pp": "66", "mmmm": "0F", "W": "WIG", "opcode": "FD", "mod": "/r", "evex": "1"},
    "zmmzmmzmm": {"vvvv": "NDS", "L": "512", "pp": "66", "mmmm": "0F", "W": "WIG", "opcode": "FD", "mod": "/r", "evex": "1"},
    "zmmzmmmem512": {"vvvv": "NDS", "L": "512", "pp": "66", "mmmm": "0F", "W": "WIG", "opcode": "FD", "mod": "/r", "evex": "1"}
}

VPADDD = {
    "xmmxmmxmm": {"vvvv": "NDS", "L": "128", "pp": "66", "mmmm": "0F", "W": "WIG", "W512": "W0", "opcode": "FE", "mod": "/r", "evex": "1"},
    "xmmxmmmem128": {"vvvv": "NDS", "L": "128", "pp": "66", "mmmm": "0F", "W": "WIG", "W512": "W0", "opcode": "FE", "mod": "/r", "evex": "1"},
    "ymmymmymm": {"vvvv": "NDS", "L": "256", "pp": "66", "mmmm": "0F", "W": "WIG", "W512": "W0", "opcode": "FE", "mod": "/r", "evex": "1"},
    "ymmymmmem256": {"vvvv": "NDS", "L": "256", "pp": "66", "mmmm": "0F", "W": "WIG", "W512": "W0", "opcode": "FE", "mod": "/r", "evex": "1"},
    "zmmzmmzmm": {"vvvv": "NDS", "L": "512", "pp": "66", "mmmm": "0F", "W": "WIG", "W512": "W0", "opcode": "FE", "mod": "/r", "evex": "1"},
    "zmmzmmmem512": {"vvvv": "NDS", "L": "512", "pp": "66", "mmmm": "0F", "W": "WIG", "W512": "W0", "opcode": "FE", "mod": "/r", "evex": "1"},

    "xmmxmmmem32": {"vvvv": "NDS", "L": "128", "pp": "66", "mmmm": "0F", "W": "WIG", "W512": "W0", "opcode": "FE", "mod": "/r", "mbr": "1", "evex": "1"},
    "ymmymmmem32": {"vvvv": "NDS", "L": "256", "pp": "66", "mmmm": "0F", "W": "WIG", "W512": "W0", "opcode": "FE", "mod": "/r", "mbr": "1", "evex": "1"},
    "zmmzmmmem32": {"vvvv": "NDS", "L": "512", "pp": "66", "mmmm": "0F", "W": "WIG", "W512": "W0", "opcode": "FE", "mod": "/r", "mbr": "1", "evex": "1"}
}

VPADDSB = {
    "xmmxmmxmm": {"vvvv": "NDS", "L": "128", "pp": "66", "mmmm": "0F", "W": "WIG", "opcode": "EC", "mod": "/r", "evex": "1"},
    "xmmxmmmem128": {"vvvv": "NDS", "L": "128", "pp": "66", "mmmm": "0F", "W": "WIG", "opcode": "EC", "mod": "/r", "evex": "1"},
    "ymmymmymm": {"vvvv": "NDS", "L": "256", "pp": "66", "mmmm": "0F", "W": "WIG", "opcode": "EC", "mod": "/r", "evex": "1"},
    "ymmymmmem256": {"vvvv": "NDS", "L": "256", "pp": "66", "mmmm": "0F", "W": "WIG", "opcode": "EC", "mod": "/r", "evex": "1"},
    "zmmzmmzmm": {"vvvv": "NDS", "L": "512", "pp": "66", "mmmm": "0F", "W": "WIG", "opcode": "EC", "mod": "/r", "evex": "1"},
    "zmmzmmmem512": {"vvvv": "NDS", "L": "512", "pp": "66", "mmmm": "0F", "W": "WIG", "opcode": "EC", "mod": "/r", "evex": "1"}
}

VPADDSW = {
    "xmmxmmxmm": {"vvvv": "NDS", "L": "128", "pp": "66", "mmmm": "0F", "W": "WIG", "opcode": "ED", "mod": "/r", "evex": "1"},
    "xmmxmmmem128": {"vvvv": "NDS", "L": "128", "pp": "66", "mmmm": "0F", "W": "WIG", "opcode": "ED", "mod": "/r", "evex": "1"},
    "ymmymmymm": {"vvvv": "NDS", "L": "256", "pp": "66", "mmmm": "0F", "W": "WIG", "opcode": "ED", "mod": "/r", "evex": "1"},
    "ymmymmmem256": {"vvvv": "NDS", "L": "256", "pp": "66", "mmmm": "0F", "W": "WIG", "opcode": "ED", "mod": "/r", "evex": "1"},
    "zmmzmmzmm": {"vvvv": "NDS", "L": "512", "pp": "66", "mmmm": "0F", "W": "WIG", "opcode": "ED", "mod": "/r", "evex": "1"},
    "zmmzmmmem512": {"vvvv": "NDS", "L": "512", "pp": "66", "mmmm": "0F", "W": "WIG", "opcode": "ED", "mod": "/r", "evex": "1"}
}

VPADDUSB = {
    "xmmxmmxmm": {"vvvv": "NDS", "L": "128", "pp": "66", "mmmm": "0F", "W": "WIG", "opcode": "DC", "mod": "/r", "evex": "1"},
    "xmmxmmmem128": {"vvvv": "NDS", "L": "128", "pp": "66", "mmmm": "0F", "W": "WIG", "opcode": "DC", "mod": "/r", "evex": "1"},
    "ymmymmymm": {"vvvv": "NDS", "L": "256", "pp": "66", "mmmm": "0F", "W": "WIG", "opcode": "DC", "mod": "/r", "evex": "1"},
    "ymmymmmem256": {"vvvv": "NDS", "L": "256", "pp": "66", "mmmm": "0F", "W": "WIG", "opcode": "DC", "mod": "/r", "evex": "1"},
    "zmmzmmzmm": {"vvvv": "NDS", "L": "512", "pp": "66", "mmmm": "0F", "W": "WIG", "opcode": "DC", "mod": "/r", "evex": "1"},
    "zmmzmmmem512": {"vvvv": "NDS", "L": "512", "pp": "66", "mmmm": "0F", "W": "WIG", "opcode": "DC", "mod": "/r", "evex": "1"}
}

VPADDUSW = {
    "xmmxmmxmm": {"vvvv": "NDS", "L": "128", "pp": "66", "mmmm": "0F", "W": "WIG", "opcode": "DD", "mod": "/r", "evex": "1"},
    "xmmxmmmem128": {"vvvv": "NDS", "L": "128", "pp": "66", "mmmm": "0F", "W": "WIG", "opcode": "DD", "mod": "/r", "evex": "1"},
    "ymmymmymm": {"vvvv": "NDS", "L": "256", "pp": "66", "mmmm": "0F", "W": "WIG", "opcode": "DD", "mod": "/r", "evex": "1"},
    "ymmymmmem256": {"vvvv": "NDS", "L": "256", "pp": "66", "mmmm": "0F", "W": "WIG", "opcode": "DD", "mod": "/r", "evex": "1"},
    "zmmzmmzmm": {"vvvv": "NDS", "L": "512", "pp": "66", "mmmm": "0F", "W": "WIG", "opcode": "DD", "mod": "/r", "evex": "1"},
    "zmmzmmmem512": {"vvvv": "NDS", "L": "512", "pp": "66", "mmmm": "0F", "W": "WIG", "opcode": "DD", "mod": "/r", "evex": "1"}
}

VPSUBB = {
    "xmmxmmxmm": {"vvvv": "NDS", "L": "128", "pp": "66", "mmmm": "0F", "W": "WIG", "opcode": "F8", "mod": "/r", "evex": "1"},
    "xmmxmmmem128": {"vvvv": "NDS", "L": "128", "pp": "66", "mmmm": "0F", "W": "WIG", "opcode": "F8", "mod": "/r", "evex": "1"},
    "ymmymmymm": {"vvvv": "NDS", "L": "256", "pp": "66", "mmmm": "0F", "W": "WIG", "opcode": "F8", "mod": "/r", "evex": "1"},
    "ymmymmmem256": {"vvvv": "NDS", "L": "256", "pp": "66", "mmmm": "0F", "W": "WIG", "opcode": "F8", "mod": "/r", "evex": "1"},
    "zmmzmmzmm": {"vvvv": "NDS", "L": "512", "pp": "66", "mmmm": "0F", "W": "WIG", "opcode": "F8", "mod": "/r", "evex": "1"},
    "zmmzmmmem512": {"vvvv": "NDS", "L": "512", "pp": "66", "mmmm": "0F", "W": "WIG", "opcode": "F8", "mod": "/r", "evex": "1"}
}

VPSUBW = {
    "xmmxmmxmm": {"vvvv": "NDS", "L": "128", "pp": "66", "mmmm": "0F", "W": "WIG", "opcode": "F9", "mod": "/r", "evex": "1"},
    "xmmxmmmem128": {"vvvv": "NDS", "L": "128", "pp": "66", "mmmm": "0F", "W": "WIG", "opcode": "F9", "mod": "/r", "evex": "1"},
    "ymmymmymm": {"vvvv": "NDS", "L": "256", "pp": "66", "mmmm": "0F", "W": "WIG", "opcode": "F9", "mod": "/r", "evex": "1"},
    "ymmymmmem256": {"vvvv": "NDS", "L": "256", "pp": "66", "mmmm": "0F", "W": "WIG", "opcode": "F9", "mod": "/r", "evex": "1"},
    "zmmzmmzmm": {"vvvv": "NDS", "L": "512", "pp": "66", "mmmm": "0F", "W": "WIG", "opcode": "F9", "mod": "/r", "evex": "1"},
    "zmmzmmmem512": {"vvvv": "NDS", "L": "512", "pp": "66", "mmmm": "0F", "W": "WIG", "opcode": "F9", "mod": "/r", "evex": "1"}
}

VPSUBD = {
    "xmmxmmxmm": {"vvvv": "NDS", "L": "128", "pp": "66", "mmmm": "0F", "W": "WIG", "W512": "W0", "opcode": "FA", "mod": "/r", "evex": "1"},
    "xmmxmmmem128": {"vvvv": "NDS", "L": "128", "pp": "66", "mmmm": "0F", "W": "WIG", "W512": "W0", "opcode": "FA", "mod": "/r", "evex": "1"},
    "ymmymmymm": {"vvvv": "NDS", "L": "256", "pp": "66", "mmmm": "0F", "W": "WIG", "W512": "W0", "opcode": "FA", "mod": "/r", "evex": "1"},
    "ymmymmmem256": {"vvvv": "NDS", "L": "256", "pp": "66", "mmmm": "0F", "W": "WIG", "W512": "W0", "opcode": "FA", "mod": "/r", "evex": "1"},
    "zmmzmmzmm": {"vvvv": "NDS", "L": "512", "pp": "66", "mmmm": "0F", "W": "WIG", "W512": "W0", "opcode": "FA", "mod": "/r", "evex": "1"},
    "zmmzmmmem512": {"vvvv": "NDS", "L": "512", "pp": "66", "mmmm": "0F", "W": "WIG", "W512": "W0", "opcode": "FA", "mod": "/r", "evex": "1"},

    "xmmxmmmem32": {"vvvv": "NDS", "L": "128", "pp": "66", "mmmm": "0F", "W": "WIG", "W512": "W0", "opcode": "FA", "mod": "/r", "mbr": "1", "evex": "1"},
    "ymmymmmem32": {"vvvv": "NDS", "L": "256", "pp": "66", "mmmm": "0F", "W": "WIG", "W512": "W0", "opcode": "FA", "mod": "/r", "mbr": "1", "evex": "1"},
    "zmmzmmmem32": {"vvvv": "NDS", "L": "512", "pp": "66", "mmmm": "0F", "W": "WIG", "W512": "W0", "opcode": "FA", "mod": "/r", "mbr": "1", "evex": "1"}
}

VPSUBSB = {
    "xmmxmmxmm": {"vvvv": "NDS", "L": "128", "pp": "66", "mmmm": "0F", "W": "WIG", "opcode": "E8", "mod": "/r", "evex": "1"},
    "xmmxmmmem128": {"vvvv": "NDS", "L": "128", "pp": "66", "mmmm": "0F", "W": "WIG", "opcode": "E8", "mod": "/r", "evex": "1"},
    "ymmymmymm": {"vvvv": "NDS", "L": "256", "pp": "66", "mmmm": "0F", "W": "WIG", "opcode": "E8", "mod": "/r", "evex": "1"},
    "ymmymmmem256": {"vvvv": "NDS", "L": "256", "pp": "66", "mmmm": "0F", "W": "WIG", "opcode": "E8", "mod": "/r", "evex": "1"},
    "zmmzmmzmm": {"vvvv": "NDS", "L": "512", "pp": "66", "mmmm": "0F", "W": "WIG", "opcode": "E8", "mod": "/r", "evex": "1"},
    "zmmzmmmem512": {"vvvv": "NDS", "L": "512", "pp": "66", "mmmm": "0F", "W": "WIG", "opcode": "E8", "mod": "/r", "evex": "1"}
}

VPSUBSW = {
    "xmmxmmxmm": {"vvvv": "NDS", "L": "128", "pp": "66", "mmmm": "0F", "W": "WIG", "opcode": "E9", "mod": "/r", "evex": "1"},
    "xmmxmmmem128": {"vvvv": "NDS", "L": "128", "pp": "66", "mmmm": "0F", "W": "WIG", "opcode": "E9", "mod": "/r", "evex": "1"},
    "ymmymmymm": {"vvvv": "NDS", "L": "256", "pp": "66", "mmmm": "0F", "W": "WIG", "opcode": "E9", "mod": "/r", "evex": "1"},
    "ymmymmmem256": {"vvvv": "NDS", "L": "256", "pp": "66", "mmmm": "0F", "W": "WIG", "opcode": "E9", "mod": "/r", "evex": "1"},
    "zmmzmmzmm": {"vvvv": "NDS", "L": "512", "pp": "66", "mmmm": "0F", "W": "WIG", "opcode": "E9", "mod": "/r", "evex": "1"},
    "zmmzmmmem512": {"vvvv": "NDS", "L": "512", "pp": "66", "mmmm": "0F", "W": "WIG", "opcode": "E9", "mod": "/r", "evex": "1"}
}

VPSUBUSB = {
    "xmmxmmxmm": {"vvvv": "NDS", "L": "128", "pp": "66", "mmmm": "0F", "W": "WIG", "opcode": "D8", "mod": "/r", "evex": "1"},
    "xmmxmmmem128": {"vvvv": "NDS", "L": "128", "pp": "66", "mmmm": "0F", "W": "WIG", "opcode": "D8", "mod": "/r", "evex": "1"},
    "ymmymmymm": {"vvvv": "NDS", "L": "256", "pp": "66", "mmmm": "0F", "W": "WIG", "opcode": "D8", "mod": "/r", "evex": "1"},
    "ymmymmmem256": {"vvvv": "NDS", "L": "256", "pp": "66", "mmmm": "0F", "W": "WIG", "opcode": "D8", "mod": "/r", "evex": "1"},
    "zmmzmmzmm": {"vvvv": "NDS", "L": "512", "pp": "66", "mmmm": "0F", "W": "WIG", "opcode": "D8", "mod": "/r", "evex": "1"},
    "zmmzmmmem512": {"vvvv": "NDS", "L": "512", "pp": "66", "mmmm": "0F", "W": "WIG", "opcode": "D8", "mod": "/r", "evex": "1"}
}

VPSUBUSW = {
    "xmmxmmxmm": {"vvvv": "NDS", "L": "128", "pp": "66", "mmmm": "0F", "W": "WIG", "opcode": "D9", "mod": "/r", "evex": "1"},
    "xmmxmmmem128": {"vvvv": "NDS", "L": "128", "pp": "66", "mmmm": "0F", "W": "WIG", "opcode": "D9", "mod": "/r", "evex": "1"},
    "ymmymmymm": {"vvvv": "NDS", "L": "256", "pp": "66", "mmmm": "0F", "W": "WIG", "opcode": "D9", "mod": "/r", "evex": "1"},
    "ymmymmmem256": {"vvvv": "NDS", "L": "256", "pp": "66", "mmmm": "0F", "W": "WIG", "opcode": "D9", "mod": "/r", "evex": "1"},
    "zmmzmmzmm": {"vvvv": "NDS", "L": "512", "pp": "66", "mmmm": "0F", "W": "WIG", "opcode": "D9", "mod": "/r", "evex": "1"},
    "zmmzmmmem512": {"vvvv": "NDS", "L": "512", "pp": "66", "mmmm": "0F", "W": "WIG", "opcode": "D9", "mod": "/r", "evex": "1"}
}

VPMULHW = {
    "xmmxmmxmm": {"vvvv": "NDS", "L": "128", "pp": "66", "mmmm": "0F", "W": "WIG", "opcode": "E5", "mod": "/r", "evex": "1"},
    "xmmxmmmem128": {"vvvv": "NDS", "L": "128", "pp": "66", "mmmm": "0F", "W": "WIG", "opcode": "E5", "mod": "/r", "evex": "1"},
    "ymmymmymm": {"vvvv": "NDS", "L": "256", "pp": "66", "mmmm": "0F", "W": "WIG", "opcode": "E5", "mod": "/r", "evex": "1"},
    "ymmymmmem256": {"vvvv": "NDS", "L": "256", "pp": "66", "mmmm": "0F", "W": "WIG", "opcode": "E5", "mod": "/r", "evex": "1"},
    "zmmzmmzmm": {"vvvv": "NDS", "L": "512", "pp": "66", "mmmm": "0F", "W": "WIG", "opcode": "E5", "mod": "/r", "evex": "1"},
    "zmmzmmmem512": {"vvvv": "NDS", "L": "512", "pp": "66", "mmmm": "0F", "W": "WIG", "opcode": "E5", "mod": "/r", "evex": "1"}
}

VPMULLW = {
    "xmmxmmxmm": {"vvvv": "NDS", "L": "128", "pp": "66", "mmmm": "0F", "W": "WIG", "opcode": "D5", "mod": "/r", "evex": "1"},
    "xmmxmmmem128": {"vvvv": "NDS", "L": "128", "pp": "66", "mmmm": "0F", "W": "WIG", "opcode": "D5", "mod": "/r", "evex": "1"},
    "ymmymmymm": {"vvvv": "NDS", "L": "256", "pp": "66", "mmmm": "0F", "W": "WIG", "opcode": "D5", "mod": "/r", "evex": "1"},
    "ymmymmmem256": {"vvvv": "NDS", "L": "256", "pp": "66", "mmmm": "0F", "W": "WIG", "opcode": "D5", "mod": "/r", "evex": "1"},
    "zmmzmmzmm": {"vvvv": "NDS", "L": "512", "pp": "66", "mmmm": "0F", "W": "WIG", "opcode": "D5", "mod": "/r", "evex": "1"},
    "zmmzmmmem512": {"vvvv": "NDS", "L": "512", "pp": "66", "mmmm": "0F", "W": "WIG", "opcode": "D5", "mod": "/r", "evex": "1"}
}

VPMADDWD = {
    "xmmxmmxmm": {"vvvv": "NDS", "L": "128", "pp": "66", "mmmm": "0F", "W": "WIG", "opcode": "F5", "mod": "/r", "evex": "1"},
    "xmmxmmmem128": {"vvvv": "NDS", "L": "128", "pp": "66", "mmmm": "0F", "W": "WIG", "opcode": "F5", "mod": "/r", "evex": "1"},
    "ymmymmymm": {"vvvv": "NDS", "L": "256", "pp": "66", "mmmm": "0F", "W": "WIG", "opcode": "F5", "mod": "/r", "evex": "1"},
    "ymmymmmem256": {"vvvv": "NDS", "L": "256", "pp": "66", "mmmm": "0F", "W": "WIG", "opcode": "F5", "mod": "/r", "evex": "1"},
    "zmmzmmzmm": {"vvvv": "NDS", "L": "512", "pp": "66", "mmmm": "0F", "W": "WIG", "opcode": "F5", "mod": "/r", "evex": "1"},
    "zmmzmmmem512": {"vvvv": "NDS", "L": "512", "pp": "66", "mmmm": "0F", "W": "WIG", "opcode": "F5", "mod": "/r", "evex": "1"}
}

VPCMPEQB = {
    "xmmxmmxmm": {"vvvv": "NDS", "L": "128", "pp": "66", "mmmm": "0F", "W": "WIG", "opcode": "74", "mod": "/r"},
    "xmmxmmmem128": {"vvvv": "NDS", "L": "128", "pp": "66", "mmmm": "0F", "W": "WIG", "opcode": "74", "mod": "/r"},
    "ymmymmymm": {"vvvv": "NDS", "L": "256", "pp": "66", "mmmm": "0F", "W": "WIG", "opcode": "74", "mod": "/r"},
    "ymmymmmem256": {"vvvv": "NDS", "L": "256", "pp": "66", "mmmm": "0F", "W": "WIG", "opcode": "74", "mod": "/r"},

    "k64xmmxmm": {"vvvv": "NDS", "L": "128", "pp": "66", "mmmm": "0F", "W": "WIG", "opcode": "74", "mod": "/r", "evex": "1"},
    "k64xmmmem128": {"vvvv": "NDS", "L": "128", "pp": "66", "mmmm": "0F", "W": "WIG", "opcode": "74", "mod": "/r", "evex": "1"},
    "k64ymmymm": {"vvvv": "NDS", "L": "256", "pp": "66", "mmmm": "0F", "W": "WIG", "opcode": "74", "mod": "/r", "evex": "1"},
    "k64ymmmem256": {"vvvv": "NDS", "L": "256", "pp": "66", "mmmm": "0F", "W": "WIG", "opcode": "74", "mod": "/r", "evex": "1"},
    "k64zmmzmm": {"vvvv": "NDS", "L": "512", "pp": "66", "mmmm": "0F", "W": "WIG", "opcode": "74", "mod": "/r", "evex": "1"},
    "k64zmmmem512": {"vvvv": "NDS", "L": "512", "pp": "66", "mmmm": "0F", "W": "WIG", "opcode": "74", "mod": "/r", "evex": "1"},
}

VPCMPEQW = {
    "xmmxmmxmm": {"vvvv": "NDS", "L": "128", "pp": "66", "mmmm": "0F", "W": "WIG", "opcode": "75", "mod": "/r"},
    "xmmxmmmem128": {"vvvv": "NDS", "L": "128", "pp": "66", "mmmm": "0F", "W": "WIG", "opcode": "75", "mod": "/r"},
    "ymmymmymm": {"vvvv": "NDS", "L": "256", "pp": "66", "mmmm": "0F", "W": "WIG", "opcode": "75", "mod": "/r"},
    "ymmymmmem256": {"vvvv": "NDS", "L": "256", "pp": "66", "mmmm": "0F", "W": "WIG", "opcode": "75", "mod": "/r"},

    "k64xmmxmm": {"vvvv": "NDS", "L": "128", "pp": "66", "mmmm": "0F", "W": "WIG", "opcode": "75", "mod": "/r", "evex": "1"},
    "k64xmmmem128": {"vvvv": "NDS", "L": "128", "pp": "66", "mmmm": "0F", "W": "WIG", "opcode": "75", "mod": "/r", "evex": "1"},
    "k64ymmymm": {"vvvv": "NDS", "L": "256", "pp": "66", "mmmm": "0F", "W": "WIG", "opcode": "75", "mod": "/r", "evex": "1"},
    "k64ymmmem256": {"vvvv": "NDS", "L": "256", "pp": "66", "mmmm": "0F", "W": "WIG", "opcode": "75", "mod": "/r", "evex": "1"},
    "k64zmmzmm": {"vvvv": "NDS", "L": "512", "pp": "66", "mmmm": "0F", "W": "WIG", "opcode": "75", "mod": "/r", "evex": "1"},
    "k64zmmmem512": {"vvvv": "NDS", "L": "512", "pp": "66", "mmmm": "0F", "W": "WIG", "opcode": "75", "mod": "/r", "evex": "1"},
}

VPCMPEQD = {
    "xmmxmmxmm": {"vvvv": "NDS", "L": "128", "pp": "66", "mmmm": "0F", "W": "WIG", "opcode": "76", "mod": "/r"},
    "xmmxmmmem128": {"vvvv": "NDS", "L": "128", "pp": "66", "mmmm": "0F", "W": "WIG", "opcode": "76", "mod": "/r"},
    "ymmymmymm": {"vvvv": "NDS", "L": "256", "pp": "66", "mmmm": "0F", "W": "WIG", "opcode": "76", "mod": "/r"},
    "ymmymmmem256": {"vvvv": "NDS", "L": "256", "pp": "66", "mmmm": "0F", "W": "WIG", "opcode": "76", "mod": "/r"},

    "k64xmmxmm": {"vvvv": "NDS", "L": "128", "pp": "66", "mmmm": "0F", "W512": "W0", "opcode": "76", "mod": "/r", "evex": "1"},
    "k64xmmmem128": {"vvvv": "NDS", "L": "128", "pp": "66", "mmmm": "0F", "W512": "W0", "opcode": "76", "mod": "/r", "evex": "1"},
    "k64ymmymm": {"vvvv": "NDS", "L": "256", "pp": "66", "mmmm": "0F", "W512": "W0", "opcode": "76", "mod": "/r", "evex": "1"},
    "k64ymmmem256": {"vvvv": "NDS", "L": "256", "pp": "66", "mmmm": "0F", "W512": "W0", "opcode": "76", "mod": "/r", "evex": "1"},
    "k64zmmzmm": {"vvvv": "NDS", "L": "512", "pp": "66", "mmmm": "0F", "W512": "W0", "opcode": "76", "mod": "/r", "evex": "1"},
    "k64zmmmem512": {"vvvv": "NDS", "L": "512", "pp": "66", "mmmm": "0F", "W512": "W0", "opcode": "76", "mod": "/r", "evex": "1"},

    "k64xmmmem32": {"vvvv": "NDS", "L": "128", "pp": "66", "mmmm": "0F", "W512": "W0", "opcode": "76", "mod": "/r", "mbr": "1", "evex": "1"},
    "k64ymmmem32": {"vvvv": "NDS", "L": "256", "pp": "66", "mmmm": "0F", "W512": "W0", "opcode": "76", "mod": "/r", "mbr": "1", "evex": "1"},
    "k64zmmmem32": {"vvvv": "NDS", "L": "512", "pp": "66", "mmmm": "0F", "W512": "W0", "opcode": "76", "mod": "/r", "mbr": "1", "evex": "1"},
}

VPCMPGTB = {
    "xmmxmmxmm": {"vvvv": "NDS", "L": "128", "pp": "66", "mmmm": "0F", "W": "WIG", "opcode": "64", "mod": "/r"},
    "xmmxmmmem128": {"vvvv": "NDS", "L": "128", "pp": "66", "mmmm": "0F", "W": "WIG", "opcode": "64", "mod": "/r"},
    "ymmymmymm": {"vvvv": "NDS", "L": "256", "pp": "66", "mmmm": "0F", "W": "WIG", "opcode": "64", "mod": "/r"},
    "ymmymmmem256": {"vvvv": "NDS", "L": "256", "pp": "66", "mmmm": "0F", "W": "WIG", "opcode": "64", "mod": "/r"},

    "k64xmmxmm": {"vvvv": "NDS", "L": "128", "pp": "66", "mmmm": "0F", "W": "WIG", "opcode": "64", "mod": "/r", "evex": "1"},
    "k64xmmmem128": {"vvvv": "NDS", "L": "128", "pp": "66", "mmmm": "0F", "W": "WIG", "opcode": "64", "mod": "/r", "evex": "1"},
    "k64ymmymm": {"vvvv": "NDS", "L": "256", "pp": "66", "mmmm": "0F", "W": "WIG", "opcode": "64", "mod": "/r", "evex": "1"},
    "k64ymmmem256": {"vvvv": "NDS", "L": "256", "pp": "66", "mmmm": "0F", "W": "WIG", "opcode": "64", "mod": "/r", "evex": "1"},
    "k64zmmzmm": {"vvvv": "NDS", "L": "512", "pp": "66", "mmmm": "0F", "W": "WIG", "opcode": "64", "mod": "/r", "evex": "1"},
    "k64zmmmem512": {"vvvv": "NDS", "L": "512", "pp": "66", "mmmm": "0F", "W": "WIG", "opcode": "64", "mod": "/r", "evex": "1"}
}

VPCMPGTW = {
    "xmmxmmxmm": {"vvvv": "NDS", "L": "128", "pp": "66", "mmmm": "0F", "W": "WIG", "opcode": "65", "mod": "/r"},
    "xmmxmmmem128": {"vvvv": "NDS", "L": "128", "pp": "66", "mmmm": "0F", "W": "WIG", "opcode": "65", "mod": "/r"},
    "ymmymmymm": {"vvvv": "NDS", "L": "256", "pp": "66", "mmmm": "0F", "W": "WIG", "opcode": "65", "mod": "/r"},
    "ymmymmmem256": {"vvvv": "NDS", "L": "256", "pp": "66", "mmmm": "0F", "W": "WIG", "opcode": "65", "mod": "/r"},

    "k64xmmxmm": {"vvvv": "NDS", "L": "128", "pp": "66", "mmmm": "0F", "W": "WIG", "opcode": "65", "mod": "/r", "evex": "1"},
    "k64xmmmem128": {"vvvv": "NDS", "L": "128", "pp": "66", "mmmm": "0F", "W": "WIG", "opcode": "65", "mod": "/r", "evex": "1"},
    "k64ymmymm": {"vvvv": "NDS", "L": "256", "pp": "66", "mmmm": "0F", "W": "WIG", "opcode": "65", "mod": "/r", "evex": "1"},
    "k64ymmmem256": {"vvvv": "NDS", "L": "256", "pp": "66", "mmmm": "0F", "W": "WIG", "opcode": "65", "mod": "/r", "evex": "1"},
    "k64zmmzmm": {"vvvv": "NDS", "L": "512", "pp": "66", "mmmm": "0F", "W": "WIG", "opcode": "65", "mod": "/r", "evex": "1"},
    "k64zmmmem512": {"vvvv": "NDS", "L": "512", "pp": "66", "mmmm": "0F", "W": "WIG", "opcode": "65", "mod": "/r", "evex": "1"},
}

VPCMPGTD = {
    "xmmxmmxmm": {"vvvv": "NDS", "L": "128", "pp": "66", "mmmm": "0F", "W": "WIG", "opcode": "66", "mod": "/r"},
    "xmmxmmmem128": {"vvvv": "NDS", "L": "128", "pp": "66", "mmmm": "0F", "W": "WIG", "opcode": "66", "mod": "/r"},
    "ymmymmymm": {"vvvv": "NDS", "L": "256", "pp": "66", "mmmm": "0F", "W": "WIG", "opcode": "66", "mod": "/r"},
    "ymmymmmem256": {"vvvv": "NDS", "L": "256", "pp": "66", "mmmm": "0F", "W": "WIG", "opcode": "66", "mod": "/r"},

    "k64xmmxmm": {"vvvv": "NDS", "L": "128", "pp": "66", "mmmm": "0F", "W512": "W0", "opcode": "66", "mod": "/r", "evex": "1"},
    "k64xmmmem128": {"vvvv": "NDS", "L": "128", "pp": "66", "mmmm": "0F", "W512": "W0", "opcode": "66", "mod": "/r", "evex": "1"},
    "k64ymmymm": {"vvvv": "NDS", "L": "256", "pp": "66", "mmmm": "0F", "W512": "W0", "opcode": "66", "mod": "/r", "evex": "1"},
    "k64ymmmem256": {"vvvv": "NDS", "L": "256", "pp": "66", "mmmm": "0F", "W512": "W0", "opcode": "66", "mod": "/r", "evex": "1"},
    "k64zmmzmm": {"vvvv": "NDS", "L": "512", "pp": "66", "mmmm": "0F", "W512": "W0", "opcode": "66", "mod": "/r", "evex": "1"},
    "k64zmmmem512": {"vvvv": "NDS", "L": "512", "pp": "66", "mmmm": "0F", "W512": "W0", "opcode": "66", "mod": "/r", "evex": "1"},

    "k64xmmmem32": {"vvvv": "NDS", "L": "128", "pp": "66", "mmmm": "0F", "W512": "W0", "opcode": "66", "mod": "/r", "mbr": "1", "evex": "1"},
    "k64ymmmem32": {"vvvv": "NDS", "L": "256", "pp": "66", "mmmm": "0F", "W512": "W0", "opcode": "66", "mod": "/r", "mbr": "1", "evex": "1"},
    "k64zmmmem32": {"vvvv": "NDS", "L": "512", "pp": "66", "mmmm": "0F", "W512": "W0", "opcode": "66", "mod": "/r", "mbr": "1", "evex": "1"}
}

VPAND = {
    "xmmxmmxmm": {"vvvv": "NDS", "L": "128", "pp": "66", "mmmm": "0F", "W": "WIG", "opcode": "DB", "mod": "/r"},
    "xmmxmmmem128": {"vvvv": "NDS", "L": "128", "pp": "66", "mmmm": "0F", "W": "WIG", "opcode": "DB", "mod": "/r"},
    "ymmymmymm": {"vvvv": "NDS", "L": "256", "pp": "66", "mmmm": "0F", "W": "WIG", "opcode": "DB", "mod": "/r"},
    "ymmymmmem256": {"vvvv": "NDS", "L": "256", "pp": "66", "mmmm": "0F", "W": "WIG", "opcode": "DB", "mod": "/r"}
}

VPANDN = {
    "xmmxmmxmm": {"vvvv": "NDS", "L": "128", "pp": "66", "mmmm": "0F", "W": "WIG", "opcode": "DF", "mod": "/r"},
    "xmmxmmmem128": {"vvvv": "NDS", "L": "128", "pp": "66", "mmmm": "0F", "W": "WIG", "opcode": "DF", "mod": "/r"},
    "ymmymmymm": {"vvvv": "NDS", "L": "256", "pp": "66", "mmmm": "0F", "W": "WIG", "opcode": "DF", "mod": "/r"},
    "ymmymmmem256": {"vvvv": "NDS", "L": "256", "pp": "66", "mmmm": "0F", "W": "WIG", "opcode": "DF", "mod": "/r"}
}

VPOR = {
    "xmmxmmxmm": {"vvvv": "NDS", "L": "128", "pp": "66", "mmmm": "0F", "W": "WIG", "opcode": "EB", "mod": "/r"},
    "xmmxmmmem128": {"vvvv": "NDS", "L": "128", "pp": "66", "mmmm": "0F", "W": "WIG", "opcode": "EB", "mod": "/r"},
    "ymmymmymm": {"vvvv": "NDS", "L": "256", "pp": "66", "mmmm": "0F", "W": "WIG", "opcode": "EB", "mod": "/r"},
    "ymmymmmem256": {"vvvv": "NDS", "L": "256", "pp": "66", "mmmm": "0F", "W": "WIG", "opcode": "EB", "mod": "/r"}
}

VPXOR = {
    "xmmxmmxmm": {"vvvv": "NDS", "L": "128", "pp": "66", "mmmm": "0F", "W": "WIG", "opcode": "EF", "mod": "/r"},
    "xmmxmmmem128": {"vvvv": "NDS", "L": "128", "pp": "66", "mmmm": "0F", "W": "WIG", "opcode": "EF", "mod": "/r"},
    "ymmymmymm": {"vvvv": "NDS", "L": "256", "pp": "66", "mmmm": "0F", "W": "WIG", "opcode": "EF", "mod": "/r"},
    "ymmymmmem256": {"vvvv": "NDS", "L": "256", "pp": "66", "mmmm": "0F", "W": "WIG", "opcode": "EF", "mod": "/r"}
}

VPSLLW = {
    "xmmxmmxmm": {"vvvv": "NDS", "L": "128", "pp": "66", "mmmm": "0F", "W": "WIG", "opcode": "F1", "mod": "/r", "evex": "1"},
    "xmmxmmmem128": {"vvvv": "NDS", "L": "128", "pp": "66", "mmmm": "0F", "W": "WIG", "opcode": "F1", "mod": "/r", "evex": "1"},
    "ymmymmymm": {"vvvv": "NDS", "L": "256", "pp": "66", "mmmm": "0F", "W": "WIG", "opcode": "F1", "mod": "/r", "evex": "1"},
    "ymmymmmem256": {"vvvv": "NDS", "L": "256", "pp": "66", "mmmm": "0F", "W": "WIG", "opcode": "F1", "mod": "/r", "evex": "1"},
    "zmmzmmzmm": {"vvvv": "NDS", "L": "512", "pp": "66", "mmmm": "0F", "W": "WIG", "opcode": "F1", "mod": "/r", "evex": "1"},
    "zmmzmmmem512": {"vvvv": "NDS", "L": "512", "pp": "66", "mmmm": "0F", "W": "WIG", "opcode": "F1", "mod": "/r", "evex": "1"},

    "xmmxmmimm8": {"vvvv": "NDD", "L": "128", "pp": "66", "mmmm": "0F", "W": "WIG", "opcode": "71", "mod": "/6", "imm": "ib", "evex": "1"},
    "ymmymmimm8": {"vvvv": "NDD", "L": "256", "pp": "66", "mmmm": "0F", "W": "WIG", "opcode": "71", "mod": "/6", "imm": "ib", "evex": "1"},
    "zmmzmmimm8": {"vvvv": "NDD", "L": "512", "pp": "66", "mmmm": "0F", "W": "WIG", "opcode": "71", "mod": "/6", "imm": "ib", "evex": "1"},

    # ONLY AVX-512 support this combination
    "xmmmem128imm8": {"vvvv": "NDD", "L": "128", "pp": "66", "mmmm": "0F", "W": "WIG", "opcode": "71", "mod": "/6", "imm": "ib", "evex": "1"},
    "ymmmem256imm8": {"vvvv": "NDD", "L": "256", "pp": "66", "mmmm": "0F", "W": "WIG", "opcode": "71", "mod": "/6", "imm": "ib", "evex": "1"},
    "zmmmem512imm8": {"vvvv": "NDD", "L": "512", "pp": "66", "mmmm": "0F", "W": "WIG", "opcode": "71", "mod": "/6", "imm": "ib", "evex": "1"},
}

VPSLLD = {
    "xmmxmmxmm": {"vvvv": "NDS", "L": "128", "pp": "66", "mmmm": "0F", "W": "WIG", "W512": "W0", "opcode": "F2", "mod": "/r", "evex": "1"},
    "xmmxmmmem128": {"vvvv": "NDS", "L": "128", "pp": "66", "mmmm": "0F", "W": "WIG", "W512": "W0", "opcode": "F2", "mod": "/r", "evex": "1"},
    "ymmymmymm": {"vvvv": "NDS", "L": "256", "pp": "66", "mmmm": "0F", "W": "WIG", "W512": "W0", "opcode": "F2", "mod": "/r", "evex": "1"},
    "ymmymmmem256": {"vvvv": "NDS", "L": "256", "pp": "66", "mmmm": "0F", "W": "WIG", "W512": "W0", "opcode": "F2", "mod": "/r", "evex": "1"},
    "zmmzmmzmm": {"vvvv": "NDS", "L": "512", "pp": "66", "mmmm": "0F", "W": "WIG", "W512": "W0", "opcode": "F2", "mod": "/r", "evex": "1"},
    "zmmzmmmem512": {"vvvv": "NDS", "L": "512", "pp": "66", "mmmm": "0F", "W": "WIG", "W512": "W0", "opcode": "F2", "mod": "/r", "evex": "1"},

    "xmmxmmimm8": {"vvvv": "NDD", "L": "128", "pp": "66", "mmmm": "0F", "W": "WIG", "W512": "W0", "opcode": "72", "mod": "/6", "imm": "ib", "evex": "1"},
    "ymmymmimm8": {"vvvv": "NDD", "L": "256", "pp": "66", "mmmm": "0F", "W": "WIG", "W512": "W0", "opcode": "72", "mod": "/6", "imm": "ib", "evex": "1"},
    "zmmzmmimm8": {"vvvv": "NDD", "L": "512", "pp": "66", "mmmm": "0F", "W": "WIG", "W512": "W0", "opcode": "72", "mod": "/6", "imm": "ib", "evex": "1"},

    # ONLY AVX-512 support this combination
    "xmmmem128imm8": {"vvvv": "NDD", "L": "128", "pp": "66", "mmmm": "0F", "W": "WIG", "W512": "W0", "opcode": "72", "mod": "/6", "imm": "ib", "evex": "1"},
    "ymmmem256imm8": {"vvvv": "NDD", "L": "256", "pp": "66", "mmmm": "0F", "W": "WIG", "W512": "W0", "opcode": "72", "mod": "/6", "imm": "ib", "evex": "1"},
    "zmmmem512imm8": {"vvvv": "NDD", "L": "512", "pp": "66", "mmmm": "0F", "W": "WIG", "W512": "W0", "opcode": "72", "mod": "/6", "imm": "ib", "evex": "1"},

    "xmmmem32imm8": {"vvvv": "NDD", "L": "128", "pp": "66", "mmmm": "0F", "W": "WIG", "W512": "W0", "opcode": "72", "mod": "/6", "imm": "ib", "mbr": "1", "evex": "1"},
    "ymmmem32imm8": {"vvvv": "NDD", "L": "256", "pp": "66", "mmmm": "0F", "W": "WIG", "W512": "W0", "opcode": "72", "mod": "/6", "imm": "ib", "mbr": "1", "evex": "1"},
    "zmmmem32imm8": {"vvvv": "NDD", "L": "512", "pp": "66", "mmmm": "0F", "W": "WIG", "W512": "W0", "opcode": "72", "mod": "/6", "imm": "ib", "mbr": "1", "evex": "1"},
}

VPSLLQ = {
    "xmmxmmxmm": {"vvvv": "NDS", "L": "128", "pp": "66", "mmmm": "0F", "W": "WIG", "W512": "W1", "opcode": "F3", "mod": "/r", "evex": "1"},
    "xmmxmmmem128": {"vvvv": "NDS", "L": "128", "pp": "66", "mmmm": "0F", "W": "WIG", "W512": "W1", "opcode": "F3", "mod": "/r", "evex": "1"},
    "ymmymmymm": {"vvvv": "NDS", "L": "256", "pp": "66", "mmmm": "0F", "W": "WIG", "W512": "W1", "opcode": "F3", "mod": "/r", "evex": "1"},
    "ymmymmmem256": {"vvvv": "NDS", "L": "256", "pp": "66", "mmmm": "0F", "W": "WIG", "W512": "W1", "opcode": "F3", "mod": "/r", "evex": "1"},
    "zmmzmmzmm": {"vvvv": "NDS", "L": "512", "pp": "66", "mmmm": "0F", "W": "WIG", "W512": "W1", "opcode": "F3", "mod": "/r", "evex": "1"},
    "zmmzmmmem512": {"vvvv": "NDS", "L": "512", "pp": "66", "mmmm": "0F", "W": "WIG", "W512": "W1", "opcode": "F3", "mod": "/r", "evex": "1"},

    "xmmxmmimm8": {"vvvv": "NDD", "L": "128", "pp": "66", "mmmm": "0F", "W": "WIG", "W512": "W1", "opcode": "73", "mod": "/6", "imm": "ib", "evex": "1"},
    "ymmymmimm8": {"vvvv": "NDD", "L": "256", "pp": "66", "mmmm": "0F", "W": "WIG", "W512": "W1", "opcode": "73", "mod": "/6", "imm": "ib", "evex": "1"},
    "zmmzmmimm8": {"vvvv": "NDD", "L": "512", "pp": "66", "mmmm": "0F", "W": "WIG", "W512": "W1", "opcode": "73", "mod": "/6", "imm": "ib", "evex": "1"},

    # ONLY AVX-512 support this combination
    "xmmmem128imm8": {"vvvv": "NDD", "L": "128", "pp": "66", "mmmm": "0F", "W": "WIG", "W512": "W1", "opcode": "73", "mod": "/6", "imm": "ib", "evex": "1"},
    "ymmmem256imm8": {"vvvv": "NDD", "L": "256", "pp": "66", "mmmm": "0F", "W": "WIG", "W512": "W1", "opcode": "73", "mod": "/6", "imm": "ib", "evex": "1"},
    "zmmmem512imm8": {"vvvv": "NDD", "L": "512", "pp": "66", "mmmm": "0F", "W": "WIG", "W512": "W1", "opcode": "73", "mod": "/6", "imm": "ib", "evex": "1"},

    "xmmmem64imm8": {"vvvv": "NDD", "L": "128", "pp": "66", "mmmm": "0F", "W": "WIG", "W512": "W1", "opcode": "73", "mod": "/6", "imm": "ib", "mbr": "1", "evex": "1"},
    "ymmmem64imm8": {"vvvv": "NDD", "L": "256", "pp": "66", "mmmm": "0F", "W": "WIG", "W512": "W1", "opcode": "73", "mod": "/6", "imm": "ib", "mbr": "1", "evex": "1"},
    "zmmmem64imm8": {"vvvv": "NDD", "L": "512", "pp": "66", "mmmm": "0F", "W": "WIG", "W512": "W1", "opcode": "73", "mod": "/6", "imm": "ib", "mbr": "1", "evex": "1"},
}

VPSRLW = {
    "xmmxmmxmm": {"vvvv": "NDS", "L": "128", "pp": "66", "mmmm": "0F", "W": "WIG", "opcode": "D1", "mod": "/r", "evex": "1"},
    "xmmxmmmem128": {"vvvv": "NDS", "L": "128", "pp": "66", "mmmm": "0F", "W": "WIG", "opcode": "D1", "mod": "/r", "evex": "1"},
    "ymmymmymm": {"vvvv": "NDS", "L": "256", "pp": "66", "mmmm": "0F", "W": "WIG", "opcode": "D1", "mod": "/r", "evex": "1"},
    "ymmymmmem256": {"vvvv": "NDS", "L": "256", "pp": "66", "mmmm": "0F", "W": "WIG", "opcode": "D1", "mod": "/r", "evex": "1"},
    "zmmzmmzmm": {"vvvv": "NDS", "L": "512", "pp": "66", "mmmm": "0F", "W": "WIG", "opcode": "D1", "mod": "/r", "evex": "1"},
    "zmmzmmmem512": {"vvvv": "NDS", "L": "512", "pp": "66", "mmmm": "0F", "W": "WIG", "opcode": "D1", "mod": "/r", "evex": "1"},

    "xmmxmmimm8": {"vvvv": "NDD", "L": "128", "pp": "66", "mmmm": "0F", "W": "WIG", "opcode": "71", "mod": "/2", "imm": "ib", "evex": "1"},
    "ymmymmimm8": {"vvvv": "NDD", "L": "256", "pp": "66", "mmmm": "0F", "W": "WIG", "opcode": "71", "mod": "/2", "imm": "ib", "evex": "1"},
    "zmmzmmimm8": {"vvvv": "NDD", "L": "512", "pp": "66", "mmmm": "0F", "W": "WIG", "opcode": "71", "mod": "/2", "imm": "ib", "evex": "1"},

    # ONLY AVX-512 support this combination
    "xmmmem128imm8": {"vvvv": "NDD", "L": "128", "pp": "66", "mmmm": "0F", "W": "WIG", "opcode": "71", "mod": "/2", "imm": "ib", "evex": "1"},
    "ymmmem256imm8": {"vvvv": "NDD", "L": "256", "pp": "66", "mmmm": "0F", "W": "WIG", "opcode": "71", "mod": "/2", "imm": "ib", "evex": "1"},
    "zmmmem512imm8": {"vvvv": "NDD", "L": "512", "pp": "66", "mmmm": "0F", "W": "WIG", "opcode": "71", "mod": "/2", "imm": "ib", "evex": "1"}
}

VPSRLD = {
    "xmmxmmxmm": {"vvvv": "NDS", "L": "128", "pp": "66", "mmmm": "0F", "W": "WIG", "W512": "W0", "opcode": "D2", "mod": "/r", "evex": "1"},
    "xmmxmmmem128": {"vvvv": "NDS", "L": "128", "pp": "66", "mmmm": "0F", "W": "WIG", "W512": "W0", "opcode": "D2", "mod": "/r", "evex": "1"},
    "ymmymmymm": {"vvvv": "NDS", "L": "256", "pp": "66", "mmmm": "0F", "W": "WIG", "W512": "W0", "opcode": "D2", "mod": "/r", "evex": "1"},
    "ymmymmmem256": {"vvvv": "NDS", "L": "256", "pp": "66", "mmmm": "0F", "W": "WIG", "W512": "W0", "opcode": "D2", "mod": "/r", "evex": "1"},
    "zmmzmmzmm": {"vvvv": "NDS", "L": "512", "pp": "66", "mmmm": "0F", "W": "WIG", "W512": "W0", "opcode": "D2", "mod": "/r", "evex": "1"},
    "zmmzmmmem512": {"vvvv": "NDS", "L": "512", "pp": "66", "mmmm": "0F", "W": "WIG", "W512": "W0", "opcode": "D2", "mod": "/r", "evex": "1"},

    "xmmxmmimm8": {"vvvv": "NDD", "L": "128", "pp": "66", "mmmm": "0F", "W": "WIG", "W512": "W0", "opcode": "72", "mod": "/2", "imm": "ib", "evex": "1"},
    "ymmymmimm8": {"vvvv": "NDD", "L": "256", "pp": "66", "mmmm": "0F", "W": "WIG", "W512": "W0", "opcode": "72", "mod": "/2", "imm": "ib", "evex": "1"},
    "zmmzmmimm8": {"vvvv": "NDD", "L": "512", "pp": "66", "mmmm": "0F", "W": "WIG", "W512": "W0", "opcode": "72", "mod": "/2", "imm": "ib", "evex": "1"},

    # ONLY AVX-512 support this combination
    "xmmmem128imm8": {"vvvv": "NDD", "L": "128", "pp": "66", "mmmm": "0F", "W": "WIG", "W512": "W0", "opcode": "72", "mod": "/2", "imm": "ib", "evex": "1"},
    "ymmmem256imm8": {"vvvv": "NDD", "L": "256", "pp": "66", "mmmm": "0F", "W": "WIG", "W512": "W0", "opcode": "72", "mod": "/2", "imm": "ib", "evex": "1"},
    "zmmmem512imm8": {"vvvv": "NDD", "L": "512", "pp": "66", "mmmm": "0F", "W": "WIG", "W512": "W0", "opcode": "72", "mod": "/2", "imm": "ib", "evex": "1"},
    "xmmmem32imm8": {"vvvv": "NDD", "L": "128", "pp": "66", "mmmm": "0F", "W": "WIG", "W512": "W0", "opcode": "72", "mod": "/2", "imm": "ib", "mbr": "1", "evex": "1"},
    "ymmmem32imm8": {"vvvv": "NDD", "L": "256", "pp": "66", "mmmm": "0F", "W": "WIG", "W512": "W0", "opcode": "72", "mod": "/2", "imm": "ib", "mbr": "1", "evex": "1"},
    "zmmmem32imm8": {"vvvv": "NDD", "L": "512", "pp": "66", "mmmm": "0F", "W": "WIG", "W512": "W0", "opcode": "72", "mod": "/2", "imm": "ib", "mbr": "1", "evex": "1"},
}

VPSRLQ = {
    "xmmxmmxmm": {"vvvv": "NDS", "L": "128", "pp": "66", "mmmm": "0F", "W": "WIG", "W512": "W1", "opcode": "D3", "mod": "/r", "evex": "1"},
    "xmmxmmmem128": {"vvvv": "NDS", "L": "128", "pp": "66", "mmmm": "0F", "W": "WIG", "W512": "W1", "opcode": "D3", "mod": "/r", "evex": "1"},
    "ymmymmymm": {"vvvv": "NDS", "L": "256", "pp": "66", "mmmm": "0F", "W": "WIG", "W512": "W1", "opcode": "D3", "mod": "/r", "evex": "1"},
    "ymmymmmem256": {"vvvv": "NDS", "L": "256", "pp": "66", "mmmm": "0F", "W": "WIG", "W512": "W1", "opcode": "D3", "mod": "/r", "evex": "1"},
    "zmmzmmzmm": {"vvvv": "NDS", "L": "512", "pp": "66", "mmmm": "0F", "W": "WIG", "W512": "W1", "opcode": "D3", "mod": "/r", "evex": "1"},
    "zmmzmmmem512": {"vvvv": "NDS", "L": "512", "pp": "66", "mmmm": "0F", "W": "WIG", "W512": "W1", "opcode": "D3", "mod": "/r", "evex": "1"},

    "xmmxmmimm8": {"vvvv": "NDD", "L": "128", "pp": "66", "mmmm": "0F", "W": "WIG", "W512": "W1", "opcode": "73", "mod": "/2", "imm": "ib", "evex": "1"},
    "ymmymmimm8": {"vvvv": "NDD", "L": "256", "pp": "66", "mmmm": "0F", "W": "WIG", "W512": "W1", "opcode": "73", "mod": "/2", "imm": "ib", "evex": "1"},
    "zmmzmmimm8": {"vvvv": "NDD", "L": "512", "pp": "66", "mmmm": "0F", "W": "WIG", "W512": "W1", "opcode": "73", "mod": "/2", "imm": "ib", "evex": "1"},

    # ONLY AVX-512 support this combination
    "xmmmem128imm8": {"vvvv": "NDD", "L": "128", "pp": "66", "mmmm": "0F", "W": "WIG", "W512": "W1", "opcode": "73", "mod": "/2", "imm": "ib", "evex": "1"},
    "ymmmem256imm8": {"vvvv": "NDD", "L": "256", "pp": "66", "mmmm": "0F", "W": "WIG", "W512": "W1", "opcode": "73", "mod": "/2", "imm": "ib", "evex": "1"},
    "zmmmem512imm8": {"vvvv": "NDD", "L": "512", "pp": "66", "mmmm": "0F", "W": "WIG", "W512": "W1", "opcode": "73", "mod": "/2", "imm": "ib", "evex": "1"},
    "xmmmem32imm8": {"vvvv": "NDD", "L": "128", "pp": "66", "mmmm": "0F", "W": "WIG", "W512": "W1", "opcode": "73", "mod": "/2", "imm": "ib", "mbr": "1", "evex": "1"},
    "ymmmem32imm8": {"vvvv": "NDD", "L": "256", "pp": "66", "mmmm": "0F", "W": "WIG", "W512": "W1", "opcode": "73", "mod": "/2", "imm": "ib", "mbr": "1", "evex": "1"},
    "zmmmem32imm8": {"vvvv": "NDD", "L": "512", "pp": "66", "mmmm": "0F", "W": "WIG", "W512": "W1", "opcode": "73", "mod": "/2", "imm": "ib", "mbr": "1", "evex": "1"},
}

VPSRAW = {
    "xmmxmmxmm": {"vvvv": "NDS", "L": "128", "pp": "66", "mmmm": "0F", "W": "WIG", "opcode": "E1", "mod": "/r", "evex": "1"},
    "xmmxmmmem128": {"vvvv": "NDS", "L": "128", "pp": "66", "mmmm": "0F", "W": "WIG", "opcode": "E1", "mod": "/r", "evex": "1"},
    "ymmymmymm": {"vvvv": "NDS", "L": "256", "pp": "66", "mmmm": "0F", "W": "WIG", "opcode": "E1", "mod": "/r", "evex": "1"},
    "ymmymmmem256": {"vvvv": "NDS", "L": "256", "pp": "66", "mmmm": "0F", "W": "WIG", "opcode": "E1", "mod": "/r", "evex": "1"},
    "zmmzmmzmm": {"vvvv": "NDS", "L": "512", "pp": "66", "mmmm": "0F", "W": "WIG", "opcode": "E1", "mod": "/r", "evex": "1"},
    "zmmzmmmem512": {"vvvv": "NDS", "L": "512", "pp": "66", "mmmm": "0F", "W": "WIG", "opcode": "E1", "mod": "/r", "evex": "1"},

    "xmmxmmimm8": {"vvvv": "NDD", "L": "128", "pp": "66", "mmmm": "0F", "W": "WIG", "opcode": "71", "mod": "/4", "imm": "ib", "evex": "1"},
    "ymmymmimm8": {"vvvv": "NDD", "L": "256", "pp": "66", "mmmm": "0F", "W": "WIG", "opcode": "71", "mod": "/4", "imm": "ib", "evex": "1"},
    "zmmzmmimm8": {"vvvv": "NDD", "L": "512", "pp": "66", "mmmm": "0F", "W": "WIG", "opcode": "71", "mod": "/4", "imm": "ib", "evex": "1"},

    # ONLY AVX-512 support this combination
    "xmmmem128imm8": {"vvvv": "NDD", "L": "128", "pp": "66", "mmmm": "0F", "W": "WIG", "opcode": "71", "mod": "/4", "imm": "ib", "evex": "1"},
    "ymmmem256imm8": {"vvvv": "NDD", "L": "256", "pp": "66", "mmmm": "0F", "W": "WIG", "opcode": "71", "mod": "/4", "imm": "ib", "evex": "1"},
    "zmmmem512imm8": {"vvvv": "NDD", "L": "512", "pp": "66", "mmmm": "0F", "W": "WIG", "opcode": "71", "mod": "/4", "imm": "ib", "evex": "1"}
}

VPSRAD = {
    "xmmxmmxmm": {"vvvv": "NDS", "L": "128", "pp": "66", "mmmm": "0F", "W": "WIG", "W512": "W0", "opcode": "E2", "mod": "/r", "evex": "1"},
    "xmmxmmmem128": {"vvvv": "NDS", "L": "128", "pp": "66", "mmmm": "0F", "W": "WIG", "W512": "W0", "opcode": "E2", "mod": "/r", "evex": "1"},
    "ymmymmymm": {"vvvv": "NDS", "L": "256", "pp": "66", "mmmm": "0F", "W": "WIG", "W512": "W0", "opcode": "E2", "mod": "/r", "evex": "1"},
    "ymmymmmem256": {"vvvv": "NDS", "L": "256", "pp": "66", "mmmm": "0F", "W": "WIG", "W512": "W0", "opcode": "E2", "mod": "/r", "evex": "1"},
    "zmmzmmzmm": {"vvvv": "NDS", "L": "512", "pp": "66", "mmmm": "0F", "W": "WIG", "W512": "W0", "opcode": "E2", "mod": "/r", "evex": "1"},
    "zmmzmmmem512": {"vvvv": "NDS", "L": "512", "pp": "66", "mmmm": "0F", "W": "WIG", "W512": "W0", "opcode": "E2", "mod": "/r", "evex": "1"},

    "xmmxmmimm8": {"vvvv": "NDD", "L": "128", "pp": "66", "mmmm": "0F", "W": "WIG", "W512": "W0", "opcode": "72", "mod": "/4", "imm": "ib", "evex": "1"},
    "ymmymmimm8": {"vvvv": "NDD", "L": "256", "pp": "66", "mmmm": "0F", "W": "WIG", "W512": "W0", "opcode": "72", "mod": "/4", "imm": "ib", "evex": "1"},
    "zmmzmmimm8": {"vvvv": "NDD", "L": "512", "pp": "66", "mmmm": "0F", "W": "WIG", "W512": "W0", "opcode": "72", "mod": "/4", "imm": "ib", "evex": "1"},

    # ONLY AVX-512 support this combination
    "xmmmem128imm8": {"vvvv": "NDD", "L": "128", "pp": "66", "mmmm": "0F", "W": "WIG", "W512": "W0", "opcode": "72", "mod": "/4", "imm": "ib", "evex": "1"},
    "ymmmem256imm8": {"vvvv": "NDD", "L": "256", "pp": "66", "mmmm": "0F", "W": "WIG", "W512": "W0", "opcode": "72", "mod": "/4", "imm": "ib", "evex": "1"},
    "zmmmem512imm8": {"vvvv": "NDD", "L": "512", "pp": "66", "mmmm": "0F", "W": "WIG", "W512": "W0", "opcode": "72", "mod": "/4", "imm": "ib", "evex": "1"},
    "xmmmem32imm8": {"vvvv": "NDD", "L": "128", "pp": "66", "mmmm": "0F", "W": "WIG", "W512": "W0", "opcode": "72", "mod": "/4", "imm": "ib", "mbr": "1", "evex": "1"},
    "ymmmem32imm8": {"vvvv": "NDD", "L": "256", "pp": "66", "mmmm": "0F", "W": "WIG", "W512": "W0", "opcode": "72", "mod": "/4", "imm": "ib", "mbr": "1", "evex": "1"},
    "zmmmem32imm8": {"vvvv": "NDD", "L": "512", "pp": "66", "mmmm": "0F", "W": "WIG", "W512": "W0", "opcode": "72", "mod": "/4", "imm": "ib", "mbr": "1", "evex": "1"}
}

# AVX SSE Instructions

VMOVAPS = {
    "xmmxmm": {"L": "128", "mmmm": "0F", "W": "WIG", "W512": "W0", "opcode": "28", "mod": "/r", "evex": "1"},
    "xmmmem128": {"L": "128", "mmmm": "0F", "W": "WIG", "W512": "W0", "opcode": "28", "mod": "/r", "evex": "1"},
    "mem128xmm": {"L": "128", "mmmm": "0F", "W": "WIG", "W512": "W0", "opcode": "29", "mod": "/r", "evex": "1"},

    "ymmymm": {"L": "256", "mmmm": "0F", "W": "WIG", "W512": "W0", "opcode": "28", "mod": "/r", "evex": "1"},
    "ymmmem256": {"L": "256", "mmmm": "0F", "W": "WIG", "W512": "W0", "opcode": "28", "mod": "/r", "evex": "1"},
    "mem256ymm": {"L": "256", "mmmm": "0F", "W": "WIG", "W512": "W0", "opcode": "29", "mod": "/r", "evex": "1"},

    "zmmzmm": {"L": "512", "mmmm": "0F", "W": "WIG", "W512": "W0", "opcode": "28", "mod": "/r", "evex": "1"},
    "zmmmem512": {"L": "512", "mmmm": "0F", "W": "WIG", "W512": "W0", "opcode": "28", "mod": "/r", "evex": "1"},
    "mem512zmm": {"L": "512", "mmmm": "0F", "W": "WIG", "W512": "W0", "opcode": "29", "mod": "/r", "evex": "1"},
}

VMOVUPS = {
    "xmmxmm": {"L": "128", "mmmm": "0F", "W": "WIG", "W512": "W0", "opcode": "10", "mod": "/r", "evex": "1"},
    "xmmmem128": {"L": "128", "mmmm": "0F", "W": "WIG", "W512": "W0", "opcode": "10", "mod": "/r", "evex": "1"},
    "mem128xmm": {"L": "128", "mmmm": "0F", "W": "WIG", "W512": "W0", "opcode": "11", "mod": "/r", "evex": "1"},

    "ymmymm": {"L": "256", "mmmm": "0F", "W": "WIG", "W512": "W0", "opcode": "10", "mod": "/r", "evex": "1"},
    "ymmmem256": {"L": "256", "mmmm": "0F", "W": "WIG", "W512": "W0", "opcode": "10", "mod": "/r", "evex": "1"},
    "mem256ymm": {"L": "256", "mmmm": "0F", "W": "WIG", "W512": "W0", "opcode": "11", "mod": "/r", "evex": "1"},

    "zmmzmm": {"L": "512", "mmmm": "0F", "W": "WIG", "W512": "W0", "opcode": "10", "mod": "/r", "evex": "1"},
    "zmmmem512": {"L": "512", "mmmm": "0F", "W": "WIG", "W512": "W0", "opcode": "10", "mod": "/r", "evex": "1"},
    "mem512zmm": {"L": "512", "mmmm": "0F", "W": "WIG", "W512": "W0", "opcode": "11", "mod": "/r", "evex": "1"},
}

VMOVHPS = {
    "xmmxmmmem64": {"L": "128", "vvvv": "NDS", "mmmm": "0F", "W": "WIG", "W512": "W0", "opcode": "16", "mod": "/r", "evex": "1"},
    "mem64xmm": {"L": "128", "mmmm": "0F", "W": "WIG", "W512": "W0", "opcode": "17", "mod": "/r", "evex": "1"},
}

VMOVHLPS = {
    "xmmxmmxmm": {"L": "128", "vvvv": "NDS", "mmmm": "0F", "W": "WIG", "W512": "W0", "opcode": "12", "mod": "/r", "evex": "1"},
}

VMOVLPS = {
    "xmmxmmmem64": {"L": "128", "vvvv": "NDS", "mmmm": "0F", "W": "WIG", "W512": "W0", "opcode": "12", "mod": "/r", "evex": "1"},
    "mem64xmm": {"L": "128", "mmmm": "0F", "W": "WIG", "W512": "W0", "opcode": "13", "mod": "/r", "evex": "1"},
}

VMOVLHPS = {
    "xmmxmmxmm": {"L": "128", "vvvv": "NDS", "mmmm": "0F", "W": "WIG", "W512": "W0", "opcode": "16", "mod": "/r", "evex": "1"},
}

VMOVMSKPS = {
    "r32xmm": {"L": "128", "mmmm": "0F", "W": "WIG", "opcode": "50", "mod": "/r"},
    "r64xmm": {"L": "128", "mmmm": "0F", "W": "WIG", "opcode": "50", "mod": "/r"},
    "r32ymm": {"L": "256", "mmmm": "0F", "W": "WIG", "opcode": "50", "mod": "/r"},
    "r64ymm": {"L": "256", "mmmm": "0F", "W": "WIG", "opcode": "50", "mod": "/r"},
}

VMOVSS = {
    "xmmxmmxmm": {"L": "LIG", "vvvv": "NDS", "pp": "F3", "mmmm": "0F", "W": "WIG", "W512": "W0", "opcode": "10", "mod": "/r", "evex": "1"},
    "xmmmem32": {"L": "LIG", "pp": "F3", "mmmm": "0F", "W": "WIG", "W512": "W0", "opcode": "10", "mod": "/r", "evex": "1"},
    "mem32xmm": {"L": "LIG", "pp": "F3", "mmmm": "0F", "W": "WIG", "W512": "W0", "opcode": "11", "mod": "/r", "evex": "1"},
}

VADDPS = {
    "xmmxmmxmm": {"L": "128", "vvvv": "NDS", "mmmm": "0F", "W": "WIG", "W512": "W0", "opcode": "58", "mod": "/r", "evex": "1"},
    "xmmxmmmem128": {"L": "128", "vvvv": "NDS", "mmmm": "0F", "W": "WIG", "W512": "W0", "opcode": "58", "mod": "/r", "evex": "1"},
    "ymmymmymm": {"L": "256", "vvvv": "NDS", "mmmm": "0F", "W": "WIG", "W512": "W0", "opcode": "58", "mod": "/r", "evex": "1"},
    "ymmymmmem256": {"L": "256", "vvvv": "NDS", "mmmm": "0F", "W": "WIG", "W512": "W0", "opcode": "58", "mod": "/r", "evex": "1"},
    "zmmzmmzmm": {"L": "512", "vvvv": "NDS", "mmmm": "0F", "W": "WIG", "W512": "W0", "opcode": "58", "mod": "/r", "evex": "1"},
    "zmmzmmmem512": {"L": "512", "vvvv": "NDS", "mmmm": "0F", "W": "WIG", "W512": "W0", "opcode": "58", "mod": "/r", "evex": "1"},

    "xmmxmmmem32": {"L": "128", "vvvv": "NDS", "mmmm": "0F", "W": "WIG", "W512": "W0", "opcode": "58", "mod": "/r", "mbr": "1", "evex": "1"},
    "ymmymmmem32": {"L": "256", "vvvv": "NDS", "mmmm": "0F", "W": "WIG", "W512": "W0", "opcode": "58", "mod": "/r", "mbr": "1", "evex": "1"},
    "zmmzmmmem32": {"L": "512", "vvvv": "NDS", "mmmm": "0F", "W": "WIG", "W512": "W0", "opcode": "58", "mod": "/r", "mbr": "1", "evex": "1"}
}

VADDSS = {
    "xmmxmmxmm": {"L": "LIG", "vvvv": "NDS", "pp": "F3", "mmmm": "0F", "W": "WIG", "W512": "W0", "opcode": "58", "mod": "/r", "evex": "1"},
    "xmmxmmmem32": {"L": "LIG", "vvvv": "NDS", "pp": "F3", "mmmm": "0F", "W": "WIG", "W512": "W0", "opcode": "58", "mod": "/r", "evex": "1"}
}

VSUBPS = {
    "xmmxmmxmm": {"L": "128", "vvvv": "NDS", "mmmm": "0F", "W": "WIG", "W512": "W0", "opcode": "5C", "mod": "/r", "evex": "1"},
    "xmmxmmmem128": {"L": "128", "vvvv": "NDS", "mmmm": "0F", "W": "WIG", "W512": "W0", "opcode": "5C", "mod": "/r", "evex": "1"},
    "ymmymmymm": {"L": "256", "vvvv": "NDS", "mmmm": "0F", "W": "WIG", "W512": "W0", "opcode": "5C", "mod": "/r", "evex": "1"},
    "ymmymmmem256": {"L": "256", "vvvv": "NDS", "mmmm": "0F", "W": "WIG", "W512": "W0", "opcode": "5C", "mod": "/r", "evex": "1"},
    "zmmzmmzmm": {"L": "512", "vvvv": "NDS", "mmmm": "0F", "W": "WIG", "W512": "W0", "opcode": "5C", "mod": "/r", "evex": "1"},
    "zmmzmmmem512": {"L": "512", "vvvv": "NDS", "mmmm": "0F", "W": "WIG", "W512": "W0", "opcode": "5C", "mod": "/r", "evex": "1"},

    "xmmxmmmem32": {"L": "128", "vvvv": "NDS", "mmmm": "0F", "W": "WIG", "W512": "W0", "opcode": "5C", "mod": "/r", "mbr": "1", "evex": "1"},
    "ymmymmmem32": {"L": "256", "vvvv": "NDS", "mmmm": "0F", "W": "WIG", "W512": "W0", "opcode": "5C", "mod": "/r", "mbr": "1", "evex": "1"},
    "zmmzmmmem32": {"L": "512", "vvvv": "NDS", "mmmm": "0F", "W": "WIG", "W512": "W0", "opcode": "5C", "mod": "/r", "mbr": "1", "evex": "1"}
}

VSUBSS = {
    "xmmxmmxmm": {"L": "LIG", "vvvv": "NDS", "pp": "F3", "mmmm": "0F", "W": "WIG", "W512": "W0", "opcode": "5C", "mod": "/r", "evex": "1"},
    "xmmxmmmem32": {"L": "LIG", "vvvv": "NDS", "pp": "F3", "mmmm": "0F", "W": "WIG", "W512": "W0", "opcode": "5C", "mod": "/r", "evex": "1"}
}

VMULPS = {
    "xmmxmmxmm": {"L": "128", "vvvv": "NDS", "mmmm": "0F", "W": "WIG", "W512": "W0", "opcode": "59", "mod": "/r", "evex": "1"},
    "xmmxmmmem128": {"L": "128", "vvvv": "NDS", "mmmm": "0F", "W": "WIG", "W512": "W0", "opcode": "59", "mod": "/r", "evex": "1"},
    "ymmymmymm": {"L": "256", "vvvv": "NDS", "mmmm": "0F", "W": "WIG", "W512": "W0", "opcode": "59", "mod": "/r", "evex": "1"},
    "ymmymmmem256": {"L": "256", "vvvv": "NDS", "mmmm": "0F", "W": "WIG", "W512": "W0", "opcode": "59", "mod": "/r", "evex": "1"},
    "zmmzmmzmm": {"L": "512", "vvvv": "NDS", "mmmm": "0F", "W": "WIG", "W512": "W0", "opcode": "59", "mod": "/r", "evex": "1"},
    "zmmzmmmem512": {"L": "512", "vvvv": "NDS", "mmmm": "0F", "W": "WIG", "W512": "W0", "opcode": "59", "mod": "/r", "evex": "1"},

    "xmmxmmmem32": {"L": "128", "vvvv": "NDS", "mmmm": "0F", "W": "WIG", "W512": "W0", "opcode": "59", "mod": "/r", "mbr": "1", "evex": "1"},
    "ymmymmmem32": {"L": "256", "vvvv": "NDS", "mmmm": "0F", "W": "WIG", "W512": "W0", "opcode": "59", "mod": "/r", "mbr": "1", "evex": "1"},
    "zmmzmmmem32": {"L": "512", "vvvv": "NDS", "mmmm": "0F", "W": "WIG", "W512": "W0", "opcode": "59", "mod": "/r", "mbr": "1", "evex": "1"}
}

VMULSS = {
    "xmmxmmxmm": {"L": "LIG", "vvvv": "NDS", "pp": "F3", "mmmm": "0F", "W": "WIG", "W512": "W0", "opcode": "59", "mod": "/r", "evex": "1"},
    "xmmxmmmem32": {"L": "LIG", "vvvv": "NDS", "pp": "F3", "mmmm": "0F", "W": "WIG", "W512": "W0", "opcode": "59", "mod": "/r", "evex": "1"}
}

VDIVPS = {
    "xmmxmmxmm": {"L": "128", "vvvv": "NDS", "mmmm": "0F", "W": "WIG", "W512": "W0", "opcode": "5E", "mod": "/r", "evex": "1"},
    "xmmxmmmem128": {"L": "128", "vvvv": "NDS", "mmmm": "0F", "W": "WIG", "W512": "W0", "opcode": "5E", "mod": "/r", "evex": "1"},
    "ymmymmymm": {"L": "256", "vvvv": "NDS", "mmmm": "0F", "W": "WIG", "W512": "W0", "opcode": "5E", "mod": "/r", "evex": "1"},
    "ymmymmmem256": {"L": "256", "vvvv": "NDS", "mmmm": "0F", "W": "WIG", "W512": "W0", "opcode": "5E", "mod": "/r", "evex": "1"},
    "zmmzmmzmm": {"L": "512", "vvvv": "NDS", "mmmm": "0F", "W": "WIG", "W512": "W0", "opcode": "5E", "mod": "/r", "evex": "1"},
    "zmmzmmmem512": {"L": "512", "vvvv": "NDS", "mmmm": "0F", "W": "WIG", "W512": "W0", "opcode": "5E", "mod": "/r", "evex": "1"},

    "xmmxmmmem32": {"L": "128", "vvvv": "NDS", "mmmm": "0F", "W": "WIG", "W512": "W0", "opcode": "5E", "mod": "/r", "mbr": "1", "evex": "1"},
    "ymmymmmem32": {"L": "256", "vvvv": "NDS", "mmmm": "0F", "W": "WIG", "W512": "W0", "opcode": "5E", "mod": "/r", "mbr": "1", "evex": "1"},
    "zmmzmmmem32": {"L": "512", "vvvv": "NDS", "mmmm": "0F", "W": "WIG", "W512": "W0", "opcode": "5E", "mod": "/r", "mbr": "1", "evex": "1"}
}

VDIVSS = {
    "xmmxmmxmm": {"L": "LIG", "vvvv": "NDS", "pp": "F3", "mmmm": "0F", "W": "WIG", "W512": "W0", "opcode": "5E", "mod": "/r", "evex": "1"},
    "xmmxmmmem32": {"L": "LIG", "vvvv": "NDS", "pp": "F3", "mmmm": "0F", "W": "WIG", "W512": "W0", "opcode": "5E", "mod": "/r", "evex": "1"},
}

VRCPPS = {
    "xmmxmm": {"L": "128", "mmmm": "0F", "W": "WIG", "opcode": "53", "mod": "/r"},
    "xmmmem128": {"L": "128", "mmmm": "0F", "W": "WIG", "opcode": "53", "mod": "/r"},
    "ymmymm": {"L": "256", "mmmm": "0F", "W": "WIG", "opcode": "53", "mod": "/r"},
    "ymmmem256": {"L": "256", "mmmm": "0F", "W": "WIG", "opcode": "53", "mod": "/r"},
}

VRCPSS = {
    "xmmxmmxmm": {"L": "LIG", "vvvv": "NDS", "pp": "F3", "mmmm": "0F", "W": "WIG", "opcode": "53", "mod": "/r"},
    "xmmxmmmem32": {"L": "LIG", "vvvv": "NDS", "pp": "F3", "mmmm": "0F", "W": "WIG", "opcode": "53", "mod": "/r"},
}

VSQRTPS = {
    "xmmxmm": {"L": "128", "mmmm": "0F", "W": "WIG", "W512": "W0", "opcode": "51", "mod": "/r", "evex": "1"},
    "xmmmem128": {"L": "128", "mmmm": "0F", "W": "WIG", "W512": "W0", "opcode": "51", "mod": "/r", "evex": "1"},
    "ymmymm": {"L": "256", "mmmm": "0F", "W": "WIG", "W512": "W0", "opcode": "51", "mod": "/r", "evex": "1"},
    "ymmmem256": {"L": "256", "mmmm": "0F", "W": "WIG", "W512": "W0", "opcode": "51", "mod": "/r", "evex": "1"},
    "zmmzmm": {"L": "512", "mmmm": "0F", "W": "WIG", "W512": "W0", "opcode": "51", "mod": "/r", "evex": "1"},
    "zmmmem512": {"L": "512", "mmmm": "0F", "W": "WIG", "W512": "W0", "opcode": "51", "mod": "/r", "evex": "1"},

    "xmmmem32": {"L": "128", "mmmm": "0F", "W": "WIG", "W512": "W0", "opcode": "51", "mod": "/r", "mbr": "1", "evex": "1"},
    "ymmmem32": {"L": "256", "mmmm": "0F", "W": "WIG", "W512": "W0", "opcode": "51", "mod": "/r", "mbr": "1", "evex": "1"},
    "zmmmem32": {"L": "512", "mmmm": "0F", "W": "WIG", "W512": "W0", "opcode": "51", "mod": "/r", "mbr": "1", "evex": "1"}
}

VSQRTSS = {
    "xmmxmmxmm": {"L": "LIG", "vvvv": "NDS", "pp": "F3", "mmmm": "0F", "W": "WIG", "W512": "W0", "opcode": "51", "mod": "/r", "evex": "1"},
    "xmmxmmmem32": {"L": "LIG", "vvvv": "NDS", "pp": "F3", "mmmm": "0F", "W": "WIG", "W512": "W0", "opcode": "51", "mod": "/r", "evex": "1"},
}

VRSQRTPS = {
    "xmmxmm": {"L": "128", "mmmm": "0F", "W": "WIG", "opcode": "51", "mod": "/r"},
    "xmmmem128": {"L": "128", "mmmm": "0F", "W": "WIG", "opcode": "51", "mod": "/r"},
    "ymmymm": {"L": "256", "mmmm": "0F", "W": "WIG", "opcode": "51", "mod": "/r"},
    "ymmmem256": {"L": "256", "mmmm": "0F", "W": "WIG", "opcode": "51", "mod": "/r"},
}

VRSQRTSS = {
    "xmmxmmxmm": {"L": "LIG", "vvvv": "NDS", "pp": "F3", "mmmm": "0F", "W": "WIG", "opcode": "52", "mod": "/r"},
    "xmmxmmmem32": {"L": "LIG", "vvvv": "NDS", "pp": "F3", "mmmm": "0F", "W": "WIG", "opcode": "52", "mod": "/r"},
}

VMAXPS = {
    "xmmxmmxmm": {"L": "128", "vvvv": "NDS", "mmmm": "0F", "W": "WIG", "W512": "W0", "opcode": "5F", "mod": "/r", "evex": "1"},
    "xmmxmmmem128": {"L": "128", "vvvv": "NDS", "mmmm": "0F", "W": "WIG", "W512": "W0", "opcode": "5F", "mod": "/r", "evex": "1"},
    "ymmymmymm": {"L": "256", "vvvv": "NDS", "mmmm": "0F", "W": "WIG", "W512": "W0", "opcode": "5F", "mod": "/r", "evex": "1"},
    "ymmymmmem256": {"L": "256", "vvvv": "NDS", "mmmm": "0F", "W": "WIG", "W512": "W0", "opcode": "5F", "mod": "/r", "evex": "1"},
    "zmmzmmzmm": {"L": "512", "vvvv": "NDS", "mmmm": "0F", "W": "WIG", "W512": "W0", "opcode": "5F", "mod": "/r", "evex": "1"},
    "zmmzmmmem512": {"L": "512", "vvvv": "NDS", "mmmm": "0F", "W": "WIG", "W512": "W0", "opcode": "5F", "mod": "/r", "evex": "1"},

    "xmmxmmmem32": {"L": "128", "vvvv": "NDS", "mmmm": "0F", "W": "WIG", "W512": "W0", "opcode": "5F", "mod": "/r", "mbr": "1", "evex": "1"},
    "ymmymmmem32": {"L": "256", "vvvv": "NDS", "mmmm": "0F", "W": "WIG", "W512": "W0", "opcode": "5F", "mod": "/r", "mbr": "1", "evex": "1"},
    "zmmzmmmem32": {"L": "512", "vvvv": "NDS", "mmmm": "0F", "W": "WIG", "W512": "W0", "opcode": "5F", "mod": "/r", "mbr": "1", "evex": "1"}
}

VMAXSS = {
    "xmmxmmxmm": {"L": "LIG", "vvvv": "NDS", "pp": "F3", "mmmm": "0F", "W": "WIG", "W512": "W0", "opcode": "5F", "mod": "/r", "evex": "1"},
    "xmmxmmmem32": {"L": "LIG", "vvvv": "NDS", "pp": "F3", "mmmm": "0F", "W": "WIG", "W512": "W0", "opcode": "5F", "mod": "/r", "evex": "1"},
}

VMINPS = {
    "xmmxmmxmm": {"L": "128", "vvvv": "NDS", "mmmm": "0F", "W": "WIG", "W512": "W0", "opcode": "5D", "mod": "/r", "evex": "1"},
    "xmmxmmmem128": {"L": "128", "vvvv": "NDS", "mmmm": "0F", "W": "WIG", "W512": "W0", "opcode": "5D", "mod": "/r", "evex": "1"},
    "ymmymmymm": {"L": "256", "vvvv": "NDS", "mmmm": "0F", "W": "WIG", "W512": "W0", "opcode": "5D", "mod": "/r", "evex": "1"},
    "ymmymmmem256": {"L": "256", "vvvv": "NDS", "mmmm": "0F", "W": "WIG", "W512": "W0", "opcode": "5D", "mod": "/r", "evex": "1"},
    "zmmzmmzmm": {"L": "512", "vvvv": "NDS", "mmmm": "0F", "W": "WIG", "W512": "W0", "opcode": "5D", "mod": "/r", "evex": "1"},
    "zmmzmmmem512": {"L": "512", "vvvv": "NDS", "mmmm": "0F", "W": "WIG", "W512": "W0", "opcode": "5D", "mod": "/r", "evex": "1"},

    "xmmxmmmem32": {"L": "128", "vvvv": "NDS", "mmmm": "0F", "W": "WIG", "W512": "W0", "opcode": "5D", "mod": "/r", "mbr": "1", "evex": "1"},
    "ymmymmmem32": {"L": "256", "vvvv": "NDS", "mmmm": "0F", "W": "WIG", "W512": "W0", "opcode": "5D", "mod": "/r", "mbr": "1", "evex": "1"},
    "zmmzmmmem32": {"L": "512", "vvvv": "NDS", "mmmm": "0F", "W": "WIG", "W512": "W0", "opcode": "5D", "mod": "/r", "mbr": "1", "evex": "1"}
}

VMINSS = {
    "xmmxmmxmm": {"L": "LIG", "vvvv": "NDS", "pp": "F3", "mmmm": "0F", "W": "WIG", "W512": "W0", "opcode": "5D", "mod": "/r", "evex": "1"},
    "xmmxmmmem32": {"L": "LIG", "vvvv": "NDS", "pp": "F3", "mmmm": "0F", "W": "WIG", "W512": "W0", "opcode": "5D", "mod": "/r", "evex": "1"},
}

VCMPPS = {
    "xmmxmmxmmimm8": {"vvvv": "NDS", "L": "128", "mmmm": "0F", "W": "WIG", "opcode": "C2", "mod": "/r", "imm": "ib"},
    "xmmxmmmem128imm8": {"vvvv": "NDS", "L": "128", "mmmm": "0F", "W": "WIG", "opcode": "C2", "mod": "/r", "imm": "ib"},
    "ymmymmymmimm8": {"vvvv": "NDS", "L": "256", "mmmm": "0F", "W": "WIG", "opcode": "C2", "mod": "/r", "imm": "ib"},
    "ymmymmmem256imm8": {"vvvv": "NDS", "L": "256", "mmmm": "0F", "W": "WIG", "opcode": "C2", "mod": "/r", "imm": "ib"},

    # Only AVX-512 support this combinations
    "k64xmmxmmimm8": {"vvvv": "NDS", "L": "128", "mmmm": "0F", "W": "WIG", "W512": "W0", "opcode": "C2", "mod": "/r", "imm": "ib", "evex": "1"},
    "k64xmmmem128imm8": {"vvvv": "NDS", "L": "128", "mmmm": "0F", "W": "WIG", "W512": "W0", "opcode": "C2", "mod": "/r", "imm": "ib", "evex": "1"},
    "k64xmmmem32imm8": {"vvvv": "NDS", "L": "128", "mmmm": "0F", "W": "WIG", "W512": "W0", "opcode": "C2", "mod": "/r", "imm": "ib", "mbr": "1", "evex": "1"},
    "k64ymmymmimm8": {"vvvv": "NDS", "L": "256", "mmmm": "0F", "W": "WIG", "W512": "W0", "opcode": "C2", "mod": "/r", "imm": "ib", "evex": "1"},
    "k64ymmmem256imm8": {"vvvv": "NDS", "L": "256", "mmmm": "0F", "W": "WIG", "W512": "W0", "opcode": "C2", "mod": "/r", "imm": "ib", "evex": "1"},
    "k64ymmmem32imm8": {"vvvv": "NDS", "L": "256", "mmmm": "0F", "W": "WIG", "W512": "W0", "opcode": "C2", "mod": "/r", "imm": "ib", "mbr": "1", "evex": "1"},
    "k64zmmzmmimm8": {"vvvv": "NDS", "L": "512", "mmmm": "0F", "W": "WIG", "W512": "W0", "opcode": "C2", "mod": "/r", "imm": "ib", "evex": "1"},
    "k64zmmmem512imm8": {"vvvv": "NDS", "L": "512", "mmmm": "0F", "W": "WIG", "W512": "W0", "opcode": "C2", "mod": "/r", "imm": "ib", "evex": "1"},
    "k64zmmmem32imm8": {"vvvv": "NDS", "L": "512", "mmmm": "0F", "W": "WIG", "W512": "W0", "opcode": "C2", "mod": "/r", "imm": "ib", "mbr": "1", "evex": "1"}
}

VCMPSS = {
    "xmmxmmxmmimm8": {"vvvv": "NDS", "L": "LIG", "pp": "F3", "mmmm": "0F", "W": "WIG", "opcode": "C2", "mod": "/r", "imm": "ib"},
    "xmmxmmmem32imm8": {"vvvv": "NDS", "L": "LIG", "pp": "F3", "mmmm": "0F", "W": "WIG", "opcode": "C2", "mod": "/r", "imm": "ib"},

    "k64xmmxmmimm8": {"vvvv": "NDS", "L": "LIG", "pp": "F3", "mmmm": "0F", "W": "WIG", "W512": "W0", "opcode": "C2", "mod": "/r", "imm": "ib", "evex": "1"},
    "k64xmmmem32imm8": {"vvvv": "NDS", "L": "LIG", "pp": "F3", "mmmm": "0F", "W": "WIG", "W512": "W0", "opcode": "C2", "mod": "/r", "imm": "ib", "evex": "1"}
}

VCOMISS = {
    "xmmxmm": {"L": "LIG", "mmmm": "0F", "W": "WIG", "W512": "W0", "opcode": "2F", "mod": "/r", "evex": "1"},
    "xmmmem32": {"L": "LIG", "mmmm": "0F", "W": "WIG", "W512": "W0", "opcode": "2F", "mod": "/r", "evex": "1"},
}

VUCOMISS = {
    "xmmxmm": {"L": "LIG", "mmmm": "0F", "W": "WIG", "W512": "W0", "opcode": "2E", "mod": "/r", "evex": "1"},
    "xmmmem32": {"L": "LIG", "mmmm": "0F", "W": "WIG", "W512": "W0", "opcode": "2E", "mod": "/r", "evex": "1"},
}

VANDPS = {
    "xmmxmmxmm": {"L": "128", "vvvv": "NDS", "mmmm": "0F", "W": "WIG", "W512": "W0", "opcode": "54", "mod": "/r", "evex": "1"},
    "xmmxmmmem128": {"L": "128", "vvvv": "NDS", "mmmm": "0F", "W": "WIG", "W512": "W0", "opcode": "54", "mod": "/r", "evex": "1"},
    "ymmymmymm": {"L": "256", "vvvv": "NDS", "mmmm": "0F", "W": "WIG", "W512": "W0", "opcode": "54", "mod": "/r", "evex": "1"},
    "ymmymmmem256": {"L": "256", "vvvv": "NDS", "mmmm": "0F", "W": "WIG", "W512": "W0", "opcode": "54", "mod": "/r", "evex": "1"},
    "zmmzmmzmm": {"L": "512", "vvvv": "NDS", "mmmm": "0F", "W": "WIG", "W512": "W0", "opcode": "54", "mod": "/r", "evex": "1"},
    "zmmzmmmem512": {"L": "512", "vvvv": "NDS", "mmmm": "0F", "W": "WIG", "W512": "W0", "opcode": "54", "mod": "/r", "evex": "1"},

    "xmmxmmmem32": {"L": "128", "vvvv": "NDS", "mmmm": "0F", "W": "WIG", "W512": "W0", "opcode": "54", "mod": "/r", "mbr": "1", "evex": "1"},
    "ymmymmmem32": {"L": "256", "vvvv": "NDS", "mmmm": "0F", "W": "WIG", "W512": "W0", "opcode": "54", "mod": "/r", "mbr": "1", "evex": "1"},
    "zmmzmmmem32": {"L": "512", "vvvv": "NDS", "mmmm": "0F", "W": "WIG", "W512": "W0", "opcode": "54", "mod": "/r", "mbr": "1", "evex": "1"}
}

VANDNPS = {
    "xmmxmmxmm": {"L": "128", "vvvv": "NDS", "mmmm": "0F", "W": "WIG", "W512": "W0", "opcode": "55", "mod": "/r", "evex": "1"},
    "xmmxmmmem128": {"L": "128", "vvvv": "NDS", "mmmm": "0F", "W": "WIG", "W512": "W0", "opcode": "55", "mod": "/r", "evex": "1"},
    "ymmymmymm": {"L": "256", "vvvv": "NDS", "mmmm": "0F", "W": "WIG", "W512": "W0", "opcode": "55", "mod": "/r", "evex": "1"},
    "ymmymmmem256": {"L": "256", "vvvv": "NDS", "mmmm": "0F", "W": "WIG", "W512": "W0", "opcode": "55", "mod": "/r", "evex": "1"},
    "zmmzmmzmm": {"L": "512", "vvvv": "NDS", "mmmm": "0F", "W": "WIG", "W512": "W0", "opcode": "55", "mod": "/r", "evex": "1"},
    "zmmzmmmem512": {"L": "512", "vvvv": "NDS", "mmmm": "0F", "W": "WIG", "W512": "W0", "opcode": "55", "mod": "/r", "evex": "1"},

    "xmmxmmmem32": {"L": "128", "vvvv": "NDS", "mmmm": "0F", "W": "WIG", "W512": "W0", "opcode": "55", "mod": "/r", "mbr": "1", "evex": "1"},
    "ymmymmmem32": {"L": "256", "vvvv": "NDS", "mmmm": "0F", "W": "WIG", "W512": "W0", "opcode": "55", "mod": "/r", "mbr": "1", "evex": "1"},
    "zmmzmmmem32": {"L": "512", "vvvv": "NDS", "mmmm": "0F", "W": "WIG", "W512": "W0", "opcode": "55", "mod": "/r", "mbr": "1", "evex": "1"}
}

VORPS = {
    "xmmxmmxmm": {"L": "128", "vvvv": "NDS", "mmmm": "0F", "W": "WIG", "W512": "W0", "opcode": "56", "mod": "/r", "evex": "1"},
    "xmmxmmmem128": {"L": "128", "vvvv": "NDS", "mmmm": "0F", "W": "WIG", "W512": "W0", "opcode": "56", "mod": "/r", "evex": "1"},
    "ymmymmymm": {"L": "256", "vvvv": "NDS", "mmmm": "0F", "W": "WIG", "W512": "W0", "opcode": "56", "mod": "/r", "evex": "1"},
    "ymmymmmem256": {"L": "256", "vvvv": "NDS", "mmmm": "0F", "W": "WIG", "W512": "W0", "opcode": "56", "mod": "/r", "evex": "1"},
    "zmmzmmzmm": {"L": "512", "vvvv": "NDS", "mmmm": "0F", "W": "WIG", "W512": "W0", "opcode": "56", "mod": "/r", "evex": "1"},
    "zmmzmmmem512": {"L": "512", "vvvv": "NDS", "mmmm": "0F", "W": "WIG", "W512": "W0", "opcode": "56", "mod": "/r", "evex": "1"},

    "xmmxmmmem32": {"L": "128", "vvvv": "NDS", "mmmm": "0F", "W": "WIG", "W512": "W0", "opcode": "56", "mod": "/r", "mbr": "1", "evex": "1"},
    "ymmymmmem32": {"L": "256", "vvvv": "NDS", "mmmm": "0F", "W": "WIG", "W512": "W0", "opcode": "56", "mod": "/r", "mbr": "1", "evex": "1"},
    "zmmzmmmem32": {"L": "512", "vvvv": "NDS", "mmmm": "0F", "W": "WIG", "W512": "W0", "opcode": "56", "mod": "/r", "mbr": "1", "evex": "1"}
}

VXORPS = {
    "xmmxmmxmm": {"L": "128", "vvvv": "NDS", "mmmm": "0F", "W": "WIG", "W512": "W0", "opcode": "57", "mod": "/r", "evex": "1"},
    "xmmxmmmem128": {"L": "128", "vvvv": "NDS", "mmmm": "0F", "W": "WIG", "W512": "W0", "opcode": "57", "mod": "/r", "evex": "1"},
    "ymmymmymm": {"L": "256", "vvvv": "NDS", "mmmm": "0F", "W": "WIG", "W512": "W0", "opcode": "57", "mod": "/r", "evex": "1"},
    "ymmymmmem256": {"L": "256", "vvvv": "NDS", "mmmm": "0F", "W": "WIG", "W512": "W0", "opcode": "57", "mod": "/r", "evex": "1"},
    "zmmzmmzmm": {"L": "512", "vvvv": "NDS", "mmmm": "0F", "W": "WIG", "W512": "W0", "opcode": "57", "mod": "/r", "evex": "1"},
    "zmmzmmmem512": {"L": "512", "vvvv": "NDS", "mmmm": "0F", "W": "WIG", "W512": "W0", "opcode": "57", "mod": "/r", "evex": "1"},

    "xmmxmmmem32": {"L": "128", "vvvv": "NDS", "mmmm": "0F", "W": "WIG", "W512": "W0", "opcode": "57", "mod": "/r", "mbr": "1", "evex": "1"},
    "ymmymmmem32": {"L": "256", "vvvv": "NDS", "mmmm": "0F", "W": "WIG", "W512": "W0", "opcode": "57", "mod": "/r", "mbr": "1", "evex": "1"},
    "zmmzmmmem32": {"L": "512", "vvvv": "NDS", "mmmm": "0F", "W": "WIG", "W512": "W0", "opcode": "57", "mod": "/r", "mbr": "1", "evex": "1"}
}

VSHUFPS = {
    "xmmxmmxmmimm8": {"vvvv": "NDS", "L": "128", "mmmm": "0F", "W": "WIG", "W512": "W0", "opcode": "C6", "mod": "/r", "imm": "ib", "evex": "1"},
    "xmmxmmmem128imm8": {"vvvv": "NDS", "L": "128", "mmmm": "0F", "W": "WIG", "W512": "W0", "opcode": "C6", "mod": "/r", "imm": "ib", "evex": "1"},
    "ymmymmymmimm8": {"vvvv": "NDS", "L": "256", "mmmm": "0F", "W": "WIG", "W512": "W0", "opcode": "C6", "mod": "/r", "imm": "ib", "evex": "1"},
    "ymmymmmem256imm8": {"vvvv": "NDS", "L": "256", "mmmm": "0F", "W": "WIG", "W512": "W0", "opcode": "C6", "mod": "/r", "imm": "ib", "evex": "1"},
    "zmmzmmzmmimm8": {"vvvv": "NDS", "L": "512", "mmmm": "0F", "W": "WIG", "W512": "W0", "opcode": "C6", "mod": "/r", "imm": "ib", "evex": "1"},
    "zmmzmmmem512imm8": {"vvvv": "NDS", "L": "512", "mmmm": "0F", "W": "WIG", "W512": "W0", "opcode": "C6", "mod": "/r", "imm": "ib", "evex": "1"},

    "xmmxmmmem32imm8": {"vvvv": "NDS", "L": "128", "mmmm": "0F", "W": "WIG", "W512": "W0", "opcode": "C6", "mod": "/r", "imm": "ib", "mbr": "1", "evex": "1"},
    "ymmymmmem32imm8": {"vvvv": "NDS", "L": "256", "mmmm": "0F", "W": "WIG", "W512": "W0", "opcode": "C6", "mod": "/r", "imm": "ib", "mbr": "1", "evex": "1"},
    "zmmzmmmem32imm8": {"vvvv": "NDS", "L": "512", "mmmm": "0F", "W": "WIG", "W512": "W0", "opcode": "C6", "mod": "/r", "imm": "ib", "mbr": "1", "evex": "1"}
}


VUNPCKHPS = {
    "xmmxmmxmm": {"L": "128", "vvvv": "NDS", "mmmm": "0F", "W": "WIG", "W512": "W0", "opcode": "15", "mod": "/r", "evex": "1"},
    "xmmxmmmem128": {"L": "128", "vvvv": "NDS", "mmmm": "0F", "W": "WIG", "W512": "W0", "opcode": "15", "mod": "/r", "evex": "1"},
    "ymmymmymm": {"L": "256", "vvvv": "NDS", "mmmm": "0F", "W": "WIG", "W512": "W0", "opcode": "15", "mod": "/r", "evex": "1"},
    "ymmymmmem256": {"L": "256", "vvvv": "NDS", "mmmm": "0F", "W": "WIG", "W512": "W0", "opcode": "15", "mod": "/r", "evex": "1"},
    "zmmzmmzmm": {"L": "512", "vvvv": "NDS", "mmmm": "0F", "W": "WIG", "W512": "W0", "opcode": "15", "mod": "/r", "evex": "1"},
    "zmmzmmmem512": {"L": "512", "vvvv": "NDS", "mmmm": "0F", "W": "WIG", "W512": "W0", "opcode": "15", "mod": "/r", "evex": "1"},

    "xmmxmmmem32": {"L": "128", "vvvv": "NDS", "mmmm": "0F", "W": "WIG", "W512": "W0", "opcode": "15", "mod": "/r", "mbr": "1", "evex": "1"},
    "ymmymmmem32": {"L": "256", "vvvv": "NDS", "mmmm": "0F", "W": "WIG", "W512": "W0", "opcode": "15", "mod": "/r", "mbr": "1", "evex": "1"},
    "zmmzmmmem32": {"L": "512", "vvvv": "NDS", "mmmm": "0F", "W": "WIG", "W512": "W0", "opcode": "15", "mod": "/r", "mbr": "1", "evex": "1"}
}

VUNPCKLPS = {
    "xmmxmmxmm": {"L": "128", "vvvv": "NDS", "mmmm": "0F", "W": "WIG", "W512": "W0", "opcode": "14", "mod": "/r", "evex": "1"},
    "xmmxmmmem128": {"L": "128", "vvvv": "NDS", "mmmm": "0F", "W": "WIG", "W512": "W0", "opcode": "14", "mod": "/r", "evex": "1"},
    "ymmymmymm": {"L": "256", "vvvv": "NDS", "mmmm": "0F", "W": "WIG", "W512": "W0", "opcode": "14", "mod": "/r", "evex": "1"},
    "ymmymmmem256": {"L": "256", "vvvv": "NDS", "mmmm": "0F", "W": "WIG", "W512": "W0", "opcode": "14", "mod": "/r", "evex": "1"},
    "zmmzmmzmm": {"L": "512", "vvvv": "NDS", "mmmm": "0F", "W": "WIG", "W512": "W0", "opcode": "14", "mod": "/r", "evex": "1"},
    "zmmzmmmem512": {"L": "512", "vvvv": "NDS", "mmmm": "0F", "W": "WIG", "W512": "W0", "opcode": "14", "mod": "/r", "evex": "1"},

    "xmmxmmmem32": {"L": "128", "vvvv": "NDS", "mmmm": "0F", "W": "WIG", "W512": "W0", "opcode": "14", "mod": "/r", "mbr": "1", "evex": "1"},
    "ymmymmmem32": {"L": "256", "vvvv": "NDS", "mmmm": "0F", "W": "WIG", "W512": "W0", "opcode": "14", "mod": "/r", "mbr": "1", "evex": "1"},
    "zmmzmmmem32": {"L": "512", "vvvv": "NDS", "mmmm": "0F", "W": "WIG", "W512": "W0", "opcode": "14", "mod": "/r", "mbr": "1", "evex": "1"}
}

VCVTSI2SS = {
    "xmmxmmr32": {"L": "LIG", "vvvv": "NDS", "pp": "F3", "mmmm": "0F", "W": "W0", "opcode": "2A", "mod": "/r", "evex": "1"},
    "xmmxmmmem32": {"L": "LIG", "vvvv": "NDS", "pp": "F3", "mmmm": "0F", "W": "W0", "opcode": "2A", "mod": "/r", "evex": "1"},
    "xmmxmmr64": {"L": "LIG", "vvvv": "NDS", "pp": "F3", "mmmm": "0F", "W": "W1", "opcode": "2A", "mod": "/r", "evex": "1"},
    "xmmxmmmem64": {"L": "LIG", "vvvv": "NDS", "pp": "F3", "mmmm": "0F", "W": "W1", "opcode": "2A", "mod": "/r", "evex": "1"}
}

VCVTSS2SI = {
    "r32xmm": {"L": "LIG", "pp": "F3", "mmmm": "0F", "W": "W0", "opcode": "2D", "mod": "/r", "evex": "1"},
    "r32mem32": {"L": "LIG", "pp": "F3", "mmmm": "0F", "W": "W0", "opcode": "2D", "mod": "/r", "evex": "1"},
    "r64xmm": {"L": "LIG", "pp": "F3", "mmmm": "0F", "W": "W1", "opcode": "2D", "mod": "/r", "evex": "1"},
    "r64mem32": {"L": "LIG", "pp": "F3", "mmmm": "0F", "W": "W1", "opcode": "2D", "mod": "/r", "evex": "1"}
}

VCVTTSS2SI = {
    "r32xmm": {"L": "LIG", "pp": "F3", "mmmm": "0F", "W": "W0", "opcode": "2C", "mod": "/r", "evex": "1"},
    "r32mem32": {"L": "LIG", "pp": "F3", "mmmm": "0F", "W": "W0", "opcode": "2C", "mod": "/r", "evex": "1"},
    "r64xmm": {"L": "LIG", "pp": "F3", "mmmm": "0F", "W": "W1", "opcode": "2C", "mod": "/r", "evex": "1"},
    "r64mem32": {"L": "LIG", "pp": "F3", "mmmm": "0F", "W": "W1", "opcode": "2C", "mod": "/r", "evex": "1"}
}

VLDMXCSR = {
    "mem32": {"L": "LZ", "mmmm": "0F", "W": "WIG", "opcode": "AE", "mod": "/2"},
}

VSTMXCSR = {
    "mem32": {"L": "LZ", "mmmm": "0F", "W": "WIG", "opcode": "AE", "mod": "/3"},
}

VPAVGB = {
    "xmmxmmxmm": {"vvvv": "NDS", "L": "128", "pp": "66", "mmmm": "0F", "W": "WIG", "opcode": "E0", "mod": "/r", "evex": "1"},
    "xmmxmmmem128": {"vvvv": "NDS", "L": "128", "pp": "66", "mmmm": "0F", "W": "WIG", "opcode": "E0", "mod": "/r", "evex": "1"},
    "ymmymmymm": {"vvvv": "NDS", "L": "256", "pp": "66", "mmmm": "0F", "W": "WIG", "opcode": "E0", "mod": "/r", "evex": "1"},
    "ymmymmmem256": {"vvvv": "NDS", "L": "256", "pp": "66", "mmmm": "0F", "W": "WIG", "opcode": "E0", "mod": "/r", "evex": "1"},
    "zmmzmmzmm": {"vvvv": "NDS", "L": "512", "pp": "66", "mmmm": "0F", "W": "WIG", "opcode": "E0", "mod": "/r", "evex": "1"},
    "zmmzmmmem512": {"vvvv": "NDS", "L": "512", "pp": "66", "mmmm": "0F", "W": "WIG", "opcode": "E0", "mod": "/r", "evex": "1"}
}

VPAVGW = {
    "xmmxmmxmm": {"vvvv": "NDS", "L": "128", "pp": "66", "mmmm": "0F", "W": "WIG", "opcode": "E3", "mod": "/r", "evex": "1"},
    "xmmxmmmem128": {"vvvv": "NDS", "L": "128", "pp": "66", "mmmm": "0F", "W": "WIG", "opcode": "E3", "mod": "/r", "evex": "1"},
    "ymmymmymm": {"vvvv": "NDS", "L": "256", "pp": "66", "mmmm": "0F", "W": "WIG", "opcode": "E3", "mod": "/r", "evex": "1"},
    "ymmymmmem256": {"vvvv": "NDS", "L": "256", "pp": "66", "mmmm": "0F", "W": "WIG", "opcode": "E3", "mod": "/r", "evex": "1"},
    "zmmzmmzmm": {"vvvv": "NDS", "L": "512", "pp": "66", "mmmm": "0F", "W": "WIG", "opcode": "E3", "mod": "/r", "evex": "1"},
    "zmmzmmmem512": {"vvvv": "NDS", "L": "512", "pp": "66", "mmmm": "0F", "W": "WIG", "opcode": "E3", "mod": "/r", "evex": "1"}
}

VPEXTRW = {
    "r32xmmimm8": {"L": "128", "pp": "66", "mmmm": "0F", "W": "W0", "W512": "WIG", "opcode": "C5", "mod": "/r", "imm": "ib", "evex": "1"},
    "r64xmmimm8": {"L": "128", "pp": "66", "mmmm": "0F", "W": "W0", "W512": "WIG", "opcode": "C5", "mod": "/r", "imm": "ib", "evex": "1"},
    "mem16xmmimm8": {"L": "128", "pp": "66", "mmmm": "0F3A", "W": "W0", "W512": "WIG", "opcode": "15", "mod": "/r", "imm": "ib", "evex": "1"}
}

VPINSRW = {
    "xmmxmmr32imm8": {"vvvv": "NDS", "L": "128", "pp": "66", "mmmm": "0F", "W": "W0", "W512": "WIG", "opcode": "C4", "mod": "/r", "imm": "ib", "evex": "1"},
    "xmmxmmmem16imm8": {"vvvv": "NDS", "L": "128", "pp": "66", "mmmm": "0F", "W": "W0", "W512": "WIG", "opcode": "C4", "mod": "/r", "imm": "ib", "evex": "1"}
}

VPMAXUB = {
    "xmmxmmxmm": {"vvvv": "NDS", "L": "128", "pp": "66", "mmmm": "0F", "W": "WIG", "opcode": "DE", "mod": "/r", "evex": "1"},
    "xmmxmmmem128": {"vvvv": "NDS", "L": "128", "pp": "66", "mmmm": "0F", "W": "WIG", "opcode": "DE", "mod": "/r", "evex": "1"},
    "ymmymmymm": {"vvvv": "NDS", "L": "256", "pp": "66", "mmmm": "0F", "W": "WIG", "opcode": "DE", "mod": "/r", "evex": "1"},
    "ymmymmmem256": {"vvvv": "NDS", "L": "256", "pp": "66", "mmmm": "0F", "W": "WIG", "opcode": "DE", "mod": "/r", "evex": "1"},
    "zmmzmmzmm": {"vvvv": "NDS", "L": "512", "pp": "66", "mmmm": "0F", "W": "WIG", "opcode": "DE", "mod": "/r", "evex": "1"},
    "zmmzmmmem512": {"vvvv": "NDS", "L": "512", "pp": "66", "mmmm": "0F", "W": "WIG", "opcode": "DE", "mod": "/r", "evex": "1"}
}

VPMAXSW = {
    "xmmxmmxmm": {"vvvv": "NDS", "L": "128", "pp": "66", "mmmm": "0F", "W": "WIG", "opcode": "EE", "mod": "/r", "evex": "1"},
    "xmmxmmmem128": {"vvvv": "NDS", "L": "128", "pp": "66", "mmmm": "0F", "W": "WIG", "opcode": "EE", "mod": "/r", "evex": "1"},
    "ymmymmymm": {"vvvv": "NDS", "L": "256", "pp": "66", "mmmm": "0F", "W": "WIG", "opcode": "EE", "mod": "/r", "evex": "1"},
    "ymmymmmem256": {"vvvv": "NDS", "L": "256", "pp": "66", "mmmm": "0F", "W": "WIG", "opcode": "EE", "mod": "/r", "evex": "1"},
    "zmmzmmzmm": {"vvvv": "NDS", "L": "512", "pp": "66", "mmmm": "0F", "W": "WIG", "opcode": "EE", "mod": "/r", "evex": "1"},
    "zmmzmmmem512": {"vvvv": "NDS", "L": "512", "pp": "66", "mmmm": "0F", "W": "WIG", "opcode": "EE", "mod": "/r", "evex": "1"}
}

VPMINUB = {
    "xmmxmmxmm": {"vvvv": "NDS", "L": "128", "pp": "66", "mmmm": "0F", "W": "WIG", "opcode": "DA", "mod": "/r", "evex": "1"},
    "xmmxmmmem128": {"vvvv": "NDS", "L": "128", "pp": "66", "mmmm": "0F", "W": "WIG", "opcode": "DA", "mod": "/r", "evex": "1"},
    "ymmymmymm": {"vvvv": "NDS", "L": "256", "pp": "66", "mmmm": "0F", "W": "WIG", "opcode": "DA", "mod": "/r", "evex": "1"},
    "ymmymmmem256": {"vvvv": "NDS", "L": "256", "pp": "66", "mmmm": "0F", "W": "WIG", "opcode": "DA", "mod": "/r", "evex": "1"},
    "zmmzmmzmm": {"vvvv": "NDS", "L": "512", "pp": "66", "mmmm": "0F", "W": "WIG", "opcode": "DA", "mod": "/r", "evex": "1"},
    "zmmzmmmem512": {"vvvv": "NDS", "L": "512", "pp": "66", "mmmm": "0F", "W": "WIG", "opcode": "DA", "mod": "/r", "evex": "1"}
}

VPMINSW = {
    "xmmxmmxmm": {"vvvv": "NDS", "L": "128", "pp": "66", "mmmm": "0F", "W": "WIG", "opcode": "EA", "mod": "/r", "evex": "1"},
    "xmmxmmmem128": {"vvvv": "NDS", "L": "128", "pp": "66", "mmmm": "0F", "W": "WIG", "opcode": "EA", "mod": "/r", "evex": "1"},
    "ymmymmymm": {"vvvv": "NDS", "L": "256", "pp": "66", "mmmm": "0F", "W": "WIG", "opcode": "EA", "mod": "/r", "evex": "1"},
    "ymmymmmem256": {"vvvv": "NDS", "L": "256", "pp": "66", "mmmm": "0F", "W": "WIG", "opcode": "EA", "mod": "/r", "evex": "1"},
    "zmmzmmzmm": {"vvvv": "NDS", "L": "512", "pp": "66", "mmmm": "0F", "W": "WIG", "opcode": "EA", "mod": "/r", "evex": "1"},
    "zmmzmmmem512": {"vvvv": "NDS", "L": "512", "pp": "66", "mmmm": "0F", "W": "WIG", "opcode": "EA", "mod": "/r", "evex": "1"}
}

VPMOVMSKB = {
    "r32xmm": {"L": "128", "pp": "66", "mmmm": "0F", "W": "WIG", "opcode": "D7", "mod": "/r"},
    "r64xmm": {"L": "128", "pp": "66", "mmmm": "0F", "W": "WIG", "opcode": "D7", "mod": "/r"},
    "r32ymm": {"L": "256", "pp": "66", "mmmm": "0F", "W": "WIG", "opcode": "D7", "mod": "/r"},
    "r64ymm": {"L": "256", "pp": "66", "mmmm": "0F", "W": "WIG", "opcode": "D7", "mod": "/r"},
}

VPMULHUW = {
    "xmmxmmxmm": {"vvvv": "NDS", "L": "128", "pp": "66", "mmmm": "0F", "W": "WIG", "opcode": "E4", "mod": "/r", "evex": "1"},
    "xmmxmmmem128": {"vvvv": "NDS", "L": "128", "pp": "66", "mmmm": "0F", "W": "WIG", "opcode": "E4", "mod": "/r", "evex": "1"},
    "ymmymmymm": {"vvvv": "NDS", "L": "256", "pp": "66", "mmmm": "0F", "W": "WIG", "opcode": "E4", "mod": "/r", "evex": "1"},
    "ymmymmmem256": {"vvvv": "NDS", "L": "256", "pp": "66", "mmmm": "0F", "W": "WIG", "opcode": "E4", "mod": "/r", "evex": "1"},
    "zmmzmmzmm": {"vvvv": "NDS", "L": "512", "pp": "66", "mmmm": "0F", "W": "WIG", "opcode": "E4", "mod": "/r", "evex": "1"},
    "zmmzmmmem512": {"vvvv": "NDS", "L": "512", "pp": "66", "mmmm": "0F", "W": "WIG", "opcode": "E4", "mod": "/r", "evex": "1"}
}

VPSADBW = {
    "xmmxmmxmm": {"vvvv": "NDS", "L": "128", "pp": "66", "mmmm": "0F", "W": "WIG", "opcode": "F6", "mod": "/r", "evex": "1"},
    "xmmxmmmem128": {"vvvv": "NDS", "L": "128", "pp": "66", "mmmm": "0F", "W": "WIG", "opcode": "F6", "mod": "/r", "evex": "1"},
    "ymmymmymm": {"vvvv": "NDS", "L": "256", "pp": "66", "mmmm": "0F", "W": "WIG", "opcode": "F6", "mod": "/r", "evex": "1"},
    "ymmymmmem256": {"vvvv": "NDS", "L": "256", "pp": "66", "mmmm": "0F", "W": "WIG", "opcode": "F6", "mod": "/r", "evex": "1"},
    "zmmzmmzmm": {"vvvv": "NDS", "L": "512", "pp": "66", "mmmm": "0F", "W": "WIG", "opcode": "F6", "mod": "/r", "evex": "1"},
    "zmmzmmmem512": {"vvvv": "NDS", "L": "512", "pp": "66", "mmmm": "0F", "W": "WIG", "opcode": "F6", "mod": "/r", "evex": "1"}
}

VMOVNTPS = {
    "mem128xmm": {"L": "128", "mmmm": "0F", "W": "WIG", "W512": "W0", "opcode": "2B", "mod": "/r", "evex": "1"},
    "mem256ymm": {"L": "256", "mmmm": "0F", "W": "WIG", "W512": "W0", "opcode": "2B", "mod": "/r", "evex": "1"},
    "mem512zmm": {"L": "512", "mmmm": "0F", "W": "WIG", "W512": "W0", "opcode": "2B", "mod": "/r", "evex": "1"}
}


# AVX SSE2 Instructions

VMOVAPD = {
    "xmmxmm": {"L": "128", "pp": "66", "mmmm": "0F", "W": "WIG", "W512": "W1", "opcode": "28", "mod": "/r", "evex": "1"},
    "xmmmem128": {"L": "128", "pp": "66", "mmmm": "0F", "W": "WIG", "W512": "W1", "opcode": "28", "mod": "/r", "evex": "1"},
    "mem128xmm": {"L": "128", "pp": "66", "mmmm": "0F", "W": "WIG", "W512": "W1", "opcode": "29", "mod": "/r", "evex": "1"},

    "ymmymm": {"L": "256", "pp": "66", "mmmm": "0F", "W": "WIG", "W512": "W1", "opcode": "28", "mod": "/r", "evex": "1"},
    "ymmmem256": {"L": "256", "pp": "66", "mmmm": "0F", "W": "WIG", "W512": "W1", "opcode": "28", "mod": "/r", "evex": "1"},
    "mem256ymm": {"L": "256", "pp": "66", "mmmm": "0F", "W": "WIG", "W512": "W1", "opcode": "29", "mod": "/r", "evex": "1"},

    "zmmzmm": {"L": "512", "pp": "66", "mmmm": "0F", "W": "WIG", "W512": "W1", "opcode": "28", "mod": "/r", "evex": "1"},
    "zmmmem512": {"L": "512", "pp": "66", "mmmm": "0F", "W": "WIG", "W512": "W1", "opcode": "28", "mod": "/r", "evex": "1"},
    "mem512zmm": {"L": "512", "pp": "66", "mmmm": "0F", "W": "WIG", "W512": "W1", "opcode": "29", "mod": "/r", "evex": "1"}
}

VMOVUPD = {
    "xmmxmm": {"L": "128", "pp": "66", "mmmm": "0F", "W": "WIG", "W512": "W1", "opcode": "10", "mod": "/r", "evex": "1"},
    "xmmmem128": {"L": "128", "pp": "66", "mmmm": "0F", "W": "WIG", "W512": "W1", "opcode": "10", "mod": "/r", "evex": "1"},
    "mem128xmm": {"L": "128", "pp": "66", "mmmm": "0F", "W": "WIG", "W512": "W1", "opcode": "11", "mod": "/r", "evex": "1"},

    "ymmymm": {"L": "256", "pp": "66", "mmmm": "0F", "W": "WIG", "W512": "W1", "opcode": "10", "mod": "/r", "evex": "1"},
    "ymmmem256": {"L": "256", "pp": "66", "mmmm": "0F", "W": "WIG", "W512": "W1", "opcode": "10", "mod": "/r", "evex": "1"},
    "mem256ymm": {"L": "256", "pp": "66", "mmmm": "0F", "W": "WIG", "W512": "W1", "opcode": "11", "mod": "/r", "evex": "1"},

    "zmmzmm": {"L": "512", "pp": "66", "mmmm": "0F", "W": "WIG", "W512": "W1", "opcode": "10", "mod": "/r", "evex": "1"},
    "zmmmem512": {"L": "512", "pp": "66", "mmmm": "0F", "W": "WIG", "W512": "W1", "opcode": "10", "mod": "/r", "evex": "1"},
    "mem512zmm": {"L": "512", "pp": "66", "mmmm": "0F", "W": "WIG", "W512": "W1", "opcode": "11", "mod": "/r", "evex": "1"}
}

VMOVHPD = {
    "xmmxmmmem64": {"L": "128", "pp": "66", "vvvv": "NDS", "mmmm": "0F", "W": "WIG", "W512": "W1", "opcode": "16", "mod": "/r", "evex": "1"},
    "mem64xmm": {"L": "128", "pp": "66", "mmmm": "0F", "W": "WIG", "W512": "W1", "opcode": "17", "mod": "/r", "evex": "1"}
}

VMOVLPD = {
    "xmmxmmmem64": {"L": "128", "pp": "66", "vvvv": "NDS", "mmmm": "0F", "W": "WIG", "W512": "W1", "opcode": "12", "mod": "/r", "evex": "1"},
    "mem64xmm": {"L": "128", "pp": "66", "mmmm": "0F", "W": "WIG", "W512": "W1", "opcode": "13", "mod": "/r", "evex": "1"}
}

VMOVMSKPD = {
    "r32xmm": {"L": "128", "pp": "66", "mmmm": "0F", "W": "WIG", "opcode": "50", "mod": "/r"},
    "r64xmm": {"L": "128", "pp": "66", "mmmm": "0F", "W": "WIG", "opcode": "50", "mod": "/r"},
    "r32ymm": {"L": "256", "pp": "66", "mmmm": "0F", "W": "WIG", "opcode": "50", "mod": "/r"},
    "r64ymm": {"L": "256", "pp": "66", "mmmm": "0F", "W": "WIG", "opcode": "50", "mod": "/r"},
}

VMOVSD = {
    "xmmxmmxmm": {"L": "LIG", "vvvv": "NDS", "pp": "F2", "mmmm": "0F", "W": "WIG", "W512": "W1", "opcode": "10", "mod": "/r", "evex": "1"},
    "xmmmem64": {"L": "LIG", "pp": "F2", "mmmm": "0F", "W": "WIG", "W512": "W1", "opcode": "10", "mod": "/r", "evex": "1"},
    "mem64xmm": {"L": "LIG", "pp": "F2", "mmmm": "0F", "W": "WIG", "W512": "W1", "opcode": "11", "mod": "/r", "evex": "1"}
}

VADDPD = {
    "xmmxmmxmm": {"L": "128", "pp": "66", "vvvv": "NDS", "mmmm": "0F", "W": "WIG", "W512": "W1", "opcode": "58", "mod": "/r", "evex": "1"},
    "xmmxmmmem128": {"L": "128", "pp": "66", "vvvv": "NDS", "mmmm": "0F", "W": "WIG", "W512": "W1", "opcode": "58", "mod": "/r", "evex": "1"},
    "ymmymmymm": {"L": "256", "pp": "66", "vvvv": "NDS", "mmmm": "0F", "W": "WIG", "W512": "W1", "opcode": "58", "mod": "/r", "evex": "1"},
    "ymmymmmem256": {"L": "256", "pp": "66", "vvvv": "NDS", "mmmm": "0F", "W": "WIG", "W512": "W1", "opcode": "58", "mod": "/r", "evex": "1"},
    "zmmzmmzmm": {"L": "512", "pp": "66", "vvvv": "NDS", "mmmm": "0F", "W": "WIG", "W512": "W1", "opcode": "58", "mod": "/r", "evex": "1"},
    "zmmzmmmem512": {"L": "512", "pp": "66", "vvvv": "NDS", "mmmm": "0F", "W": "WIG", "W512": "W1", "opcode": "58", "mod": "/r", "evex": "1"},

    "xmmxmmmem64": {"L": "128", "pp": "66", "vvvv": "NDS", "mmmm": "0F", "W": "WIG", "W512": "W1", "opcode": "58", "mod": "/r", "mbr": "1", "evex": "1"},
    "ymmymmmem64": {"L": "256", "pp": "66", "vvvv": "NDS", "mmmm": "0F", "W": "WIG", "W512": "W1", "opcode": "58", "mod": "/r", "mbr": "1", "evex": "1"},
    "zmmzmmmem64": {"L": "512", "pp": "66", "vvvv": "NDS", "mmmm": "0F", "W": "WIG", "W512": "W1", "opcode": "58", "mod": "/r", "mbr": "1", "evex": "1"}
}

VADDSD = {
    "xmmxmmxmm": {"L": "LIG", "vvvv": "NDS", "pp": "F2", "mmmm": "0F", "W": "WIG", "W512": "W1", "opcode": "58", "mod": "/r", "evex": "1"},
    "xmmxmmmem64": {"L": "LIG", "vvvv": "NDS", "pp": "F2", "mmmm": "0F", "W": "WIG", "W512": "W1", "opcode": "58", "mod": "/r", "evex": "1"}
}

VSUBPD = {
    "xmmxmmxmm": {"L": "128", "pp": "66", "vvvv": "NDS", "mmmm": "0F", "W": "WIG", "W512": "W1", "opcode": "5C", "mod": "/r", "evex": "1"},
    "xmmxmmmem128": {"L": "128", "pp": "66", "vvvv": "NDS", "mmmm": "0F", "W": "WIG", "W512": "W1", "opcode": "5C", "mod": "/r", "evex": "1"},
    "ymmymmymm": {"L": "256", "pp": "66", "vvvv": "NDS", "mmmm": "0F", "W": "WIG", "W512": "W1", "opcode": "5C", "mod": "/r", "evex": "1"},
    "ymmymmmem256": {"L": "256", "pp": "66", "vvvv": "NDS", "mmmm": "0F", "W": "WIG", "W512": "W1", "opcode": "5C", "mod": "/r", "evex": "1"},
    "zmmzmmzmm": {"L": "512", "pp": "66", "vvvv": "NDS", "mmmm": "0F", "W": "WIG", "W512": "W1", "opcode": "5C", "mod": "/r", "evex": "1"},
    "zmmzmmmem512": {"L": "512", "pp": "66", "vvvv": "NDS", "mmmm": "0F", "W": "WIG", "W512": "W1", "opcode": "5C", "mod": "/r", "evex": "1"},

    "xmmxmmmem64": {"L": "128", "pp": "66", "vvvv": "NDS", "mmmm": "0F", "W": "WIG", "W512": "W1", "opcode": "5C", "mod": "/r", "mbr": "1", "evex": "1"},
    "ymmymmmem64": {"L": "256", "pp": "66", "vvvv": "NDS", "mmmm": "0F", "W": "WIG", "W512": "W1", "opcode": "5C", "mod": "/r", "mbr": "1", "evex": "1"},
    "zmmzmmmem64": {"L": "512", "pp": "66", "vvvv": "NDS", "mmmm": "0F", "W": "WIG", "W512": "W1", "opcode": "5C", "mod": "/r", "mbr": "1", "evex": "1"}
}

VSUBSD = {
    "xmmxmmxmm": {"L": "LIG", "vvvv": "NDS", "pp": "F2", "mmmm": "0F", "W": "WIG", "W512": "W1", "opcode": "5C", "mod": "/r", "evex": "1"},
    "xmmxmmmem64": {"L": "LIG", "vvvv": "NDS", "pp": "F2", "mmmm": "0F", "W": "WIG", "W512": "W1", "opcode": "5C", "mod": "/r", "evex": "1"},
}

VMULPD = {
    "xmmxmmxmm": {"L": "128", "pp": "66", "vvvv": "NDS", "mmmm": "0F", "W": "WIG", "W512": "W1", "opcode": "59", "mod": "/r", "evex": "1"},
    "xmmxmmmem128": {"L": "128", "pp": "66", "vvvv": "NDS", "mmmm": "0F", "W": "WIG", "W512": "W1", "opcode": "59", "mod": "/r", "evex": "1"},
    "ymmymmymm": {"L": "256", "pp": "66", "vvvv": "NDS", "mmmm": "0F", "W": "WIG", "W512": "W1", "opcode": "59", "mod": "/r", "evex": "1"},
    "ymmymmmem256": {"L": "256", "pp": "66", "vvvv": "NDS", "mmmm": "0F", "W": "WIG", "W512": "W1", "opcode": "59", "mod": "/r", "evex": "1"},
    "zmmzmmzmm": {"L": "512", "pp": "66", "vvvv": "NDS", "mmmm": "0F", "W": "WIG", "W512": "W1", "opcode": "59", "mod": "/r", "evex": "1"},
    "zmmzmmmem512": {"L": "512", "pp": "66", "vvvv": "NDS", "mmmm": "0F", "W": "WIG", "W512": "W1", "opcode": "59", "mod": "/r", "evex": "1"},

    "xmmxmmmem64": {"L": "128", "pp": "66", "vvvv": "NDS", "mmmm": "0F", "W": "WIG", "W512": "W1", "opcode": "59", "mod": "/r", "mbr": "1", "evex": "1"},
    "ymmymmmem64": {"L": "256", "pp": "66", "vvvv": "NDS", "mmmm": "0F", "W": "WIG", "W512": "W1", "opcode": "59", "mod": "/r", "mbr": "1", "evex": "1"},
    "zmmzmmmem64": {"L": "512", "pp": "66", "vvvv": "NDS", "mmmm": "0F", "W": "WIG", "W512": "W1", "opcode": "59", "mod": "/r", "mbr": "1", "evex": "1"}
}

VMULSD = {
    "xmmxmmxmm": {"L": "LIG", "vvvv": "NDS", "pp": "F2", "mmmm": "0F", "W": "WIG", "W512": "W1", "opcode": "59", "mod": "/r", "evex": "1"},
    "xmmxmmmem64": {"L": "LIG", "vvvv": "NDS", "pp": "F2", "mmmm": "0F", "W": "WIG", "W512": "W1", "opcode": "59", "mod": "/r", "evex": ""},
}

VDIVPD = {
    "xmmxmmxmm": {"L": "128", "pp": "66", "vvvv": "NDS", "mmmm": "0F", "W": "WIG", "W512": "W1", "opcode": "5E", "mod": "/r", "evex": "1"},
    "xmmxmmmem128": {"L": "128", "pp": "66", "vvvv": "NDS", "mmmm": "0F", "W": "WIG", "W512": "W1", "opcode": "5E", "mod": "/r", "evex": "1"},
    "ymmymmymm": {"L": "256", "pp": "66", "vvvv": "NDS", "mmmm": "0F", "W": "WIG", "W512": "W1", "opcode": "5E", "mod": "/r", "evex": "1"},
    "ymmymmmem256": {"L": "256", "pp": "66", "vvvv": "NDS", "mmmm": "0F", "W": "WIG", "W512": "W1", "opcode": "5E", "mod": "/r", "evex": "1"},
    "zmmzmmzmm": {"L": "512", "pp": "66", "vvvv": "NDS", "mmmm": "0F", "W": "WIG", "W512": "W1", "opcode": "5E", "mod": "/r", "evex": "1"},
    "zmmzmmmem512": {"L": "512", "pp": "66", "vvvv": "NDS", "mmmm": "0F", "W": "WIG", "W512": "W1", "opcode": "5E", "mod": "/r", "evex": "1"},

    "xmmxmmmem64": {"L": "128", "pp": "66", "vvvv": "NDS", "mmmm": "0F", "W": "WIG", "W512": "W1", "opcode": "5E", "mod": "/r", "mbr": "1", "evex": "1"},
    "ymmymmmem64": {"L": "256", "pp": "66", "vvvv": "NDS", "mmmm": "0F", "W": "WIG", "W512": "W1", "opcode": "5E", "mod": "/r", "mbr": "1", "evex": "1"},
    "zmmzmmmem64": {"L": "512", "pp": "66", "vvvv": "NDS", "mmmm": "0F", "W": "WIG", "W512": "W1", "opcode": "5E", "mod": "/r", "mbr": "1", "evex": "1"}
}

VDIVSD = {
    "xmmxmmxmm": {"L": "LIG", "vvvv": "NDS", "pp": "F2", "mmmm": "0F", "W": "WIG", "W512": "W1", "opcode": "5E", "mod": "/r", "evex": "1"},
    "xmmxmmmem64": {"L": "LIG", "vvvv": "NDS", "pp": "F2", "mmmm": "0F", "W": "WIG", "W512": "W1", "opcode": "5E", "mod": "/r", "evex": "1"},
}

VSQRTPD = {
    "xmmxmm": {"L": "128", "pp": "66", "mmmm": "0F", "W": "WIG", "W512": "W1", "opcode": "51", "mod": "/r", "evex": "1"},
    "xmmmem128": {"L": "128", "pp": "66", "mmmm": "0F", "W": "WIG", "W512": "W1", "opcode": "51", "mod": "/r", "evex": "1"},
    "ymmymm": {"L": "256", "pp": "66", "mmmm": "0F", "W": "WIG", "W512": "W1", "opcode": "51", "mod": "/r", "evex": "1"},
    "ymmmem256": {"L": "256", "pp": "66", "mmmm": "0F", "W": "WIG", "W512": "W1", "opcode": "51", "mod": "/r", "evex": "1"},
    "zmmzmm": {"L": "512", "pp": "66", "mmmm": "0F", "W": "WIG", "W512": "W1", "opcode": "51", "mod": "/r", "evex": "1"},
    "zmmmem512": {"L": "512", "pp": "66", "mmmm": "0F", "W": "WIG", "W512": "W1", "opcode": "51", "mod": "/r", "evex": "1"},

    "xmmmem64": {"L": "128", "pp": "66", "mmmm": "0F", "W": "WIG", "W512": "W1", "opcode": "51", "mod": "/r", "mbr": "1", "evex": "1"},
    "ymmmem64": {"L": "256", "pp": "66", "mmmm": "0F", "W": "WIG", "W512": "W1", "opcode": "51", "mod": "/r", "mbr": "1", "evex": "1"},
    "zmmmem64": {"L": "512", "pp": "66", "mmmm": "0F", "W": "WIG", "W512": "W1", "opcode": "51", "mod": "/r", "mbr": "1", "evex": "1"}
}

VSQRTSD = {
    "xmmxmmxmm": {"L": "LIG", "vvvv": "NDS", "pp": "F2", "mmmm": "0F", "W": "WIG", "W512": "W1", "opcode": "51", "mod": "/r", "evex": "1"},
    "xmmxmmmem64": {"L": "LIG", "vvvv": "NDS", "pp": "F2", "mmmm": "0F", "W": "WIG", "W512": "W1", "opcode": "51", "mod": "/r", "evex": "1"},
}

VMAXPD = {
    "xmmxmmxmm": {"L": "128", "vvvv": "NDS", "pp": "66", "mmmm": "0F", "W": "WIG", "W512": "W1", "opcode": "5F", "mod": "/r", "evex": "1"},
    "xmmxmmmem128": {"L": "128", "vvvv": "NDS", "pp": "66", "mmmm": "0F", "W": "WIG", "W512": "W1", "opcode": "5F", "mod": "/r", "evex": "1"},
    "ymmymmymm": {"L": "256", "vvvv": "NDS", "pp": "66", "mmmm": "0F", "W": "WIG", "W512": "W1", "opcode": "5F", "mod": "/r", "evex": "1"},
    "ymmymmmem256": {"L": "256", "vvvv": "NDS", "pp": "66", "mmmm": "0F", "W": "WIG", "W512": "W1", "opcode": "5F", "mod": "/r", "evex": "1"},
    "zmmzmmzmm": {"L": "512", "vvvv": "NDS", "pp": "66", "mmmm": "0F", "W": "WIG", "W512": "W1", "opcode": "5F", "mod": "/r", "evex": "1"},
    "zmmzmmmem512": {"L": "512", "vvvv": "NDS", "pp": "66", "mmmm": "0F", "W": "WIG", "W512": "W1", "opcode": "5F", "mod": "/r", "evex": "1"},

    "xmmxmmmem64": {"L": "128", "vvvv": "NDS", "pp": "66", "mmmm": "0F", "W": "WIG", "W512": "W1", "opcode": "5F", "mod": "/r", "mbr": "1", "evex": "1"},
    "ymmymmmem64": {"L": "256", "vvvv": "NDS", "pp": "66", "mmmm": "0F", "W": "WIG", "W512": "W1", "opcode": "5F", "mod": "/r", "mbr": "1", "evex": "1"},
    "zmmzmmmem64": {"L": "512", "vvvv": "NDS", "pp": "66", "mmmm": "0F", "W": "WIG", "W512": "W1", "opcode": "5F", "mod": "/r", "mbr": "1", "evex": "1"}
}

VMAXSD = {
    "xmmxmmxmm": {"L": "LIG", "vvvv": "NDS", "pp": "F2", "mmmm": "0F", "W": "WIG", "W512": "W1", "opcode": "5F", "mod": "/r", "evex": "1"},
    "xmmxmmmem64": {"L": "LIG", "vvvv": "NDS", "pp": "F2", "mmmm": "0F", "W": "WIG", "W512": "W1", "opcode": "5F", "mod": "/r", "evex": "1"},
}

VMINPD = {
    "xmmxmmxmm": {"L": "128", "vvvv": "NDS", "pp": "66", "mmmm": "0F", "W": "WIG", "W512": "W1", "opcode": "5D", "mod": "/r", "evex": "1"},
    "xmmxmmmem128": {"L": "128", "vvvv": "NDS", "pp": "66", "mmmm": "0F", "W": "WIG", "W512": "W1", "opcode": "5D", "mod": "/r", "evex": "1"},
    "ymmymmymm": {"L": "256", "vvvv": "NDS", "pp": "66", "mmmm": "0F", "W": "WIG", "W512": "W1", "opcode": "5D", "mod": "/r", "evex": "1"},
    "ymmymmmem256": {"L": "256", "vvvv": "NDS", "pp": "66", "mmmm": "0F", "W": "WIG", "W512": "W1", "opcode": "5D", "mod": "/r", "evex": "1"},
    "zmmzmmzmm": {"L": "512", "vvvv": "NDS", "pp": "66", "mmmm": "0F", "W": "WIG", "W512": "W1", "opcode": "5D", "mod": "/r", "evex": "1"},
    "zmmzmmmem512": {"L": "512", "vvvv": "NDS", "pp": "66", "mmmm": "0F", "W": "WIG", "W512": "W1", "opcode": "5D", "mod": "/r", "evex": "1"},

    "xmmxmmmem64": {"L": "128", "vvvv": "NDS", "pp": "66", "mmmm": "0F", "W": "WIG", "W512": "W1", "opcode": "5D", "mod": "/r", "mbr": "1", "evex": "1"},
    "ymmymmmem64": {"L": "256", "vvvv": "NDS", "pp": "66", "mmmm": "0F", "W": "WIG", "W512": "W1", "opcode": "5D", "mod": "/r", "mbr": "1", "evex": "1"},
    "zmmzmmmem64": {"L": "512", "vvvv": "NDS", "pp": "66", "mmmm": "0F", "W": "WIG", "W512": "W1", "opcode": "5D", "mod": "/r", "mbr": "1", "evex": "1"}
}

VMINSD = {
    "xmmxmmxmm": {"L": "LIG", "vvvv": "NDS", "pp": "F2", "mmmm": "0F", "W": "WIG", "W512": "W1", "opcode": "5D", "mod": "/r", "evex": "1"},
    "xmmxmmmem64": {"L": "LIG", "vvvv": "NDS", "pp": "F2", "mmmm": "0F", "W": "WIG", "W512": "W1", "opcode": "5D", "mod": "/r", "evex": "1"},
}

VCMPPD = {
    "xmmxmmxmmimm8": {"vvvv": "NDS", "L": "128", "pp": "66", "mmmm": "0F", "W": "WIG", "opcode": "C2", "mod": "/r", "imm": "ib"},
    "xmmxmmmem128imm8": {"vvvv": "NDS", "L": "128", "pp": "66", "mmmm": "0F", "W": "WIG", "opcode": "C2", "mod": "/r", "imm": "ib"},
    "ymmymmymmimm8": {"vvvv": "NDS", "L": "256", "pp": "66", "mmmm": "0F", "W": "WIG", "opcode": "C2", "mod": "/r", "imm": "ib"},
    "ymmymmmem256imm8": {"vvvv": "NDS", "L": "256", "pp": "66", "mmmm": "0F", "W": "WIG", "opcode": "C2", "mod": "/r", "imm": "ib"},

    "k64xmmxmmimm8": {"vvvv": "NDS", "L": "128", "pp": "66", "mmmm": "0F", "W": "WIG", "W512": "W1", "opcode": "C2", "mod": "/r", "imm": "ib", "evex": "1"},
    "k64xmmmem128imm8": {"vvvv": "NDS", "L": "128", "pp": "66", "mmmm": "0F", "W": "WIG", "W512": "W1", "opcode": "C2", "mod": "/r", "imm": "ib", "evex": "1"},
    "k64ymmymmimm8": {"vvvv": "NDS", "L": "256", "pp": "66", "mmmm": "0F", "W": "WIG", "W512": "W1", "opcode": "C2", "mod": "/r", "imm": "ib", "evex": "1"},
    "k64ymmmem256imm8": {"vvvv": "NDS", "L": "256", "pp": "66", "mmmm": "0F", "W": "WIG", "W512": "W1", "opcode": "C2", "mod": "/r", "imm": "ib", "evex": "1"},
    "k64zmmzmmimm8": {"vvvv": "NDS", "L": "512", "pp": "66", "mmmm": "0F", "W": "WIG", "W512": "W1", "opcode": "C2", "mod": "/r", "imm": "ib", "evex": "1"},
    "k64zmmmem512imm8": {"vvvv": "NDS", "L": "512", "pp": "66", "mmmm": "0F", "W": "WIG", "W512": "W1", "opcode": "C2", "mod": "/r", "imm": "ib", "evex": "1"},

    "k64xmmmem64imm8": {"vvvv": "NDS", "L": "128", "pp": "66", "mmmm": "0F", "W": "WIG", "W512": "W1", "opcode": "C2", "mod": "/r", "imm": "ib", "mbr": "1", "evex": "1"},
    "k64ymmmem64imm8": {"vvvv": "NDS", "L": "256", "pp": "66", "mmmm": "0F", "W": "WIG", "W512": "W1", "opcode": "C2", "mod": "/r", "imm": "ib", "mbr": "1", "evex": "1"},
    "k64zmmmem64imm8": {"vvvv": "NDS", "L": "512", "pp": "66", "mmmm": "0F", "W": "WIG", "W512": "W1", "opcode": "C2", "mod": "/r", "imm": "ib", "mbr": "1", "evex": "1"}
}

VCMPSD = {
    "xmmxmmxmmimm8": {"vvvv": "NDS", "L": "LIG", "pp": "F2", "mmmm": "0F", "W": "WIG", "opcode": "C2", "mod": "/r", "imm": "ib"},
    "xmmxmmmem64imm8": {"vvvv": "NDS", "L": "LIG", "pp": "F2", "mmmm": "0F", "W": "WIG", "opcode": "C2", "mod": "/r", "imm": "ib"},
    "k64xmmxmmimm8": {"vvvv": "NDS", "L": "LIG", "pp": "F2", "mmmm": "0F", "W512": "W1", "opcode": "C2", "mod": "/r", "imm": "ib", "evex": "1"},
    "k64xmmmem64imm8": {"vvvv": "NDS", "L": "LIG", "pp": "F2", "mmmm": "0F", "W512": "W1", "opcode": "C2", "mod": "/r", "imm": "ib", "evex": "1"}
}

VCOMISD = {
    "xmmxmm": {"L": "LIG", "pp": "66", "mmmm": "0F", "W": "WIG", "W512": "W1", "opcode": "2F", "mod": "/r", "evex": "1"},
    "xmmmem64": {"L": "LIG", "pp": "66", "mmmm": "0F", "W": "WIG", "W512": "W1", "opcode": "2F", "mod": "/r", "evex": "1"},
}

VUCOMISD = {
    "xmmxmm": {"L": "LIG", "pp": "66", "mmmm": "0F", "W": "WIG", "W512": "W1", "opcode": "2E", "mod": "/r", "evex": "1"},
    "xmmmem64": {"L": "LIG", "pp": "66", "mmmm": "0F", "W": "WIG", "W512": "W1", "opcode": "2E", "mod": "/r", "evex": "1"},
}


VANDPD = {
    "xmmxmmxmm": {"L": "128", "vvvv": "NDS", "pp": "66", "mmmm": "0F", "W": "WIG", "W512": "W1", "opcode": "54", "mod": "/r", "evex": "1"},
    "xmmxmmmem128": {"L": "128", "vvvv": "NDS", "pp": "66", "mmmm": "0F", "W": "WIG", "W512": "W1", "opcode": "54", "mod": "/r", "evex": "1"},
    "ymmymmymm": {"L": "256", "vvvv": "NDS", "pp": "66", "mmmm": "0F", "W": "WIG", "W512": "W1", "opcode": "54", "mod": "/r", "evex": "1"},
    "ymmymmmem256": {"L": "256", "vvvv": "NDS", "pp": "66", "mmmm": "0F", "W": "WIG", "W512": "W1", "opcode": "54", "mod": "/r", "evex": "1"},
    "zmmzmmzmm": {"L": "512", "vvvv": "NDS", "pp": "66", "mmmm": "0F", "W": "WIG", "W512": "W1", "opcode": "54", "mod": "/r", "evex": "1"},
    "zmmzmmmem512": {"L": "512", "vvvv": "NDS", "pp": "66", "mmmm": "0F", "W": "WIG", "W512": "W1", "opcode": "54", "mod": "/r", "evex": "1"},

    "xmmxmmmem64": {"L": "128", "vvvv": "NDS", "pp": "66", "mmmm": "0F", "W": "WIG", "W512": "W1", "opcode": "54", "mod": "/r", "mbr": "1", "evex": "1"},
    "ymmymmmem64": {"L": "256", "vvvv": "NDS", "pp": "66", "mmmm": "0F", "W": "WIG", "W512": "W1", "opcode": "54", "mod": "/r", "mbr": "1", "evex": "1"},
    "zmmzmmmem64": {"L": "512", "vvvv": "NDS", "pp": "66", "mmmm": "0F", "W": "WIG", "W512": "W1", "opcode": "54", "mod": "/r", "mbr": "1", "evex": "1"}
}

VANDNPD = {
    "xmmxmmxmm": {"L": "128", "vvvv": "NDS", "pp": "66", "mmmm": "0F", "W": "WIG", "W512": "W1", "opcode": "55", "mod": "/r", "evex": "1"},
    "xmmxmmmem128": {"L": "128", "vvvv": "NDS", "pp": "66", "mmmm": "0F", "W": "WIG", "W512": "W1", "opcode": "55", "mod": "/r", "evex": "1"},
    "ymmymmymm": {"L": "256", "vvvv": "NDS", "pp": "66", "mmmm": "0F", "W": "WIG", "W512": "W1", "opcode": "55", "mod": "/r", "evex": "1"},
    "ymmymmmem256": {"L": "256", "vvvv": "NDS", "pp": "66", "mmmm": "0F", "W": "WIG", "W512": "W1", "opcode": "55", "mod": "/r", "evex": "1"},
    "zmmzmmzmm": {"L": "512", "vvvv": "NDS", "pp": "66", "mmmm": "0F", "W": "WIG", "W512": "W1", "opcode": "55", "mod": "/r", "evex": "1"},
    "zmmzmmmem512": {"L": "512", "vvvv": "NDS", "pp": "66", "mmmm": "0F", "W": "WIG", "W512": "W1", "opcode": "55", "mod": "/r", "evex": "1"},

    "xmmxmmmem64": {"L": "128", "vvvv": "NDS", "pp": "66", "mmmm": "0F", "W": "WIG", "W512": "W1", "opcode": "55", "mod": "/r", "mbr": "1", "evex": "1"},
    "ymmymmmem64": {"L": "256", "vvvv": "NDS", "pp": "66", "mmmm": "0F", "W": "WIG", "W512": "W1", "opcode": "55", "mod": "/r", "mbr": "1", "evex": "1"},
    "zmmzmmmem64": {"L": "512", "vvvv": "NDS", "pp": "66", "mmmm": "0F", "W": "WIG", "W512": "W1", "opcode": "55", "mod": "/r", "mbr": "1", "evex": "1"}
}

VORPD = {
    "xmmxmmxmm": {"L": "128", "vvvv": "NDS", "pp": "66", "mmmm": "0F", "W": "WIG", "W512": "W1", "opcode": "56", "mod": "/r", "evex": "1"},
    "xmmxmmmem128": {"L": "128", "vvvv": "NDS", "pp": "66", "mmmm": "0F", "W": "WIG", "W512": "W1", "opcode": "56", "mod": "/r", "evex": "1"},
    "ymmymmymm": {"L": "256", "vvvv": "NDS", "pp": "66", "mmmm": "0F", "W": "WIG", "W512": "W1", "opcode": "56", "mod": "/r", "evex": "1"},
    "ymmymmmem256": {"L": "256", "vvvv": "NDS", "pp": "66", "mmmm": "0F", "W": "WIG", "W512": "W1", "opcode": "56", "mod": "/r", "evex": "1"},
    "zmmzmmzmm": {"L": "512", "vvvv": "NDS", "pp": "66", "mmmm": "0F", "W": "WIG", "W512": "W1", "opcode": "56", "mod": "/r", "evex": "1"},
    "zmmzmmmem512": {"L": "512", "vvvv": "NDS", "pp": "66", "mmmm": "0F", "W": "WIG", "W512": "W1", "opcode": "56", "mod": "/r", "evex": "1"},

    "xmmxmmmem64": {"L": "128", "vvvv": "NDS", "pp": "66", "mmmm": "0F", "W": "WIG", "W512": "W1", "opcode": "56", "mod": "/r", "mbr": "1", "evex": "1"},
    "ymmymmmem64": {"L": "256", "vvvv": "NDS", "pp": "66", "mmmm": "0F", "W": "WIG", "W512": "W1", "opcode": "56", "mod": "/r", "mbr": "1", "evex": "1"},
    "zmmzmmmem64": {"L": "512", "vvvv": "NDS", "pp": "66", "mmmm": "0F", "W": "WIG", "W512": "W1", "opcode": "56", "mod": "/r", "mbr": "1", "evex": "1"}
}

VXORPD = {
    "xmmxmmxmm": {"L": "128", "vvvv": "NDS", "pp": "66", "mmmm": "0F", "W": "WIG", "W512": "W1", "opcode": "57", "mod": "/r", "evex": "1"},
    "xmmxmmmem128": {"L": "128", "vvvv": "NDS", "pp": "66", "mmmm": "0F", "W": "WIG", "W512": "W1", "opcode": "57", "mod": "/r", "evex": "1"},
    "ymmymmymm": {"L": "256", "vvvv": "NDS", "pp": "66", "mmmm": "0F", "W": "WIG", "W512": "W1", "opcode": "57", "mod": "/r", "evex": "1"},
    "ymmymmmem256": {"L": "256", "vvvv": "NDS", "pp": "66", "mmmm": "0F", "W": "WIG", "W512": "W1", "opcode": "57", "mod": "/r", "evex": "1"},
    "zmmzmmzmm": {"L": "512", "vvvv": "NDS", "pp": "66", "mmmm": "0F", "W": "WIG", "W512": "W1", "opcode": "57", "mod": "/r", "evex": "1"},
    "zmmzmmmem512": {"L": "512", "vvvv": "NDS", "pp": "66", "mmmm": "0F", "W": "WIG", "W512": "W1", "opcode": "57", "mod": "/r", "evex": "1"},

    "xmmxmmmem64": {"L": "128", "vvvv": "NDS", "pp": "66", "mmmm": "0F", "W": "WIG", "W512": "W1", "opcode": "57", "mod": "/r", "mbr": "1", "evex": "1"},
    "ymmymmmem64": {"L": "256", "vvvv": "NDS", "pp": "66", "mmmm": "0F", "W": "WIG", "W512": "W1", "opcode": "57", "mod": "/r", "mbr": "1", "evex": "1"},
    "zmmzmmmem64": {"L": "512", "vvvv": "NDS", "pp": "66", "mmmm": "0F", "W": "WIG", "W512": "W1", "opcode": "57", "mod": "/r", "mbr": "1", "evex": "1"}
}

VSHUFPD = {
    "xmmxmmxmmimm8": {"vvvv": "NDS", "L": "128", "pp": "66", "mmmm": "0F", "W": "WIG", "W512": "W1", "opcode": "C6", "mod": "/r", "imm": "ib", "evex": "1"},
    "xmmxmmmem128imm8": {"vvvv": "NDS", "L": "128", "pp": "66", "mmmm": "0F", "W": "WIG", "W512": "W1", "opcode": "C6", "mod": "/r", "imm": "ib", "evex": "1"},
    "ymmymmymmimm8": {"vvvv": "NDS", "L": "256", "pp": "66", "mmmm": "0F", "W": "WIG", "W512": "W1", "opcode": "C6", "mod": "/r", "imm": "ib", "evex": "1"},
    "ymmymmmem256imm8": {"vvvv": "NDS", "L": "256", "pp": "66", "mmmm": "0F", "W": "WIG", "W512": "W1", "opcode": "C6", "mod": "/r", "imm": "ib", "evex": "1"},
    "zmmzmmzmmimm8": {"vvvv": "NDS", "L": "512", "pp": "66", "mmmm": "0F", "W": "WIG", "W512": "W1", "opcode": "C6", "mod": "/r", "imm": "ib", "evex": "1"},
    "zmmzmmmem512imm8": {"vvvv": "NDS", "L": "512", "pp": "66", "mmmm": "0F", "W": "WIG", "W512": "W1", "opcode": "C6", "mod": "/r", "imm": "ib", "evex": "1"},

   "xmmxmmmem64imm8": {"vvvv": "NDS", "L": "128", "pp": "66", "mmmm": "0F", "W": "WIG", "W512": "W1", "opcode": "C6", "mod": "/r", "imm": "ib", "mbr": "1", "evex": "1"},
   "ymmymmmem64imm8": {"vvvv": "NDS", "L": "256", "pp": "66", "mmmm": "0F", "W": "WIG", "W512": "W1", "opcode": "C6", "mod": "/r", "imm": "ib", "mbr": "1", "evex": "1"},
   "zmmzmmmem64imm8": {"vvvv": "NDS", "L": "512", "pp": "66", "mmmm": "0F", "W": "WIG", "W512": "W1", "opcode": "C6", "mod": "/r", "imm": "ib", "mbr": "1", "evex": "1"}
}

VUNPCKHPD = {
    "xmmxmmxmm": {"L": "128", "vvvv": "NDS", "pp": "66", "mmmm": "0F", "W": "WIG", "W512": "W1", "opcode": "15", "mod": "/r", "evex": "1"},
    "xmmxmmmem128": {"L": "128", "vvvv": "NDS", "pp": "66", "mmmm": "0F", "W": "WIG", "W512": "W1", "opcode": "15", "mod": "/r", "evex": "1"},
    "ymmymmymm": {"L": "256", "vvvv": "NDS", "pp": "66", "mmmm": "0F", "W": "WIG", "W512": "W1", "opcode": "15", "mod": "/r", "evex": "1"},
    "ymmymmmem256": {"L": "256", "vvvv": "NDS", "pp": "66", "mmmm": "0F", "W": "WIG", "W512": "W1", "opcode": "15", "mod": "/r", "evex": "1"},
    "zmmzmmzmm": {"L": "512", "vvvv": "NDS", "pp": "66", "mmmm": "0F", "W": "WIG", "W512": "W1", "opcode": "15", "mod": "/r", "evex": "1"},
    "zmmzmmmem512": {"L": "512", "vvvv": "NDS", "pp": "66", "mmmm": "0F", "W": "WIG", "W512": "W1", "opcode": "15", "mod": "/r", "evex": "1"},

    "xmmxmmmem64": {"L": "128", "vvvv": "NDS", "pp": "66", "mmmm": "0F", "W": "WIG", "W512": "W1", "opcode": "15", "mod": "/r", "mbr": "1", "evex": "1"},
    "ymmymmmem64": {"L": "256", "vvvv": "NDS", "pp": "66", "mmmm": "0F", "W": "WIG", "W512": "W1", "opcode": "15", "mod": "/r", "mbr": "1", "evex": "1"},
    "zmmzmmmem64": {"L": "512", "vvvv": "NDS", "pp": "66", "mmmm": "0F", "W": "WIG", "W512": "W1", "opcode": "15", "mod": "/r", "mbr": "1", "evex": "1"}
}

VUNPCKLPD = {
    "xmmxmmxmm": {"L": "128", "vvvv": "NDS", "pp": "66", "mmmm": "0F", "W": "WIG", "W512": "W1", "opcode": "14", "mod": "/r", "evex": "1"},
    "xmmxmmmem128": {"L": "128", "vvvv": "NDS", "pp": "66", "mmmm": "0F", "W": "WIG", "W512": "W1", "opcode": "14", "mod": "/r", "evex": "1"},
    "ymmymmymm": {"L": "256", "vvvv": "NDS", "pp": "66", "mmmm": "0F", "W": "WIG", "W512": "W1", "opcode": "14", "mod": "/r", "evex": "1"},
    "ymmymmmem256": {"L": "256", "vvvv": "NDS", "pp": "66", "mmmm": "0F", "W": "WIG", "W512": "W1", "opcode": "14", "mod": "/r", "evex": "1"},
    "zmmzmmzmm": {"L": "512", "vvvv": "NDS", "pp": "66", "mmmm": "0F", "W": "WIG", "W512": "W1", "opcode": "14", "mod": "/r", "evex": "1"},
    "zmmzmmmem512": {"L": "512", "vvvv": "NDS", "pp": "66", "mmmm": "0F", "W": "WIG", "W512": "W1", "opcode": "14", "mod": "/r", "evex": "1"},

    "xmmxmmmem64": {"L": "128", "vvvv": "NDS", "pp": "66", "mmmm": "0F", "W": "WIG", "W512": "W1", "opcode": "14", "mod": "/r", "mbr": "1", "evex": "1"},
    "ymmymmmem64": {"L": "256", "vvvv": "NDS", "pp": "66", "mmmm": "0F", "W": "WIG", "W512": "W1", "opcode": "14", "mod": "/r", "mbr": "1", "evex": "1"},
    "zmmzmmmem64": {"L": "512", "vvvv": "NDS", "pp": "66", "mmmm": "0F", "W": "WIG", "W512": "W1", "opcode": "14", "mod": "/r", "mbr": "1", "evex": "1"}
}

VCVTPD2DQ = {
    "xmmxmm": {"L": "128", "pp": "F2", "mmmm": "0F", "W": "WIG", "W512": "W1", "opcode": "E6", "mod": "/r", "evex": "1"},
    "xmmmem128": {"L": "128", "pp": "F2", "mmmm": "0F", "W": "WIG", "W512": "W1", "opcode": "E6", "mod": "/r", "evex": "1"},
    "xmmymm": {"L": "256", "pp": "F2", "mmmm": "0F", "W": "WIG", "W512": "W1", "opcode": "E6", "mod": "/r", "evex": "1"},
    "xmmmem256": {"L": "256", "pp": "F2", "mmmm": "0F", "W": "WIG", "W512": "W1", "opcode": "E6", "mod": "/r", "evex": "1"},
    "ymmzmm": {"L": "512", "pp": "F2", "mmmm": "0F", "W": "WIG", "W512": "W1", "opcode": "E6", "mod": "/r", "evex": "1"},
    "ymmmem512": {"L": "512", "pp": "F2", "mmmm": "0F", "W": "WIG", "W512": "W1", "opcode": "E6", "mod": "/r", "evex": "1"}
}

VCVTTPD2DQ = {
    "xmmxmm": {"L": "128", "pp": "66", "mmmm": "0F", "W": "WIG", "W512": "W1", "opcode": "E6", "mod": "/r", "evex": "1"},
    "xmmmem128": {"L": "128", "pp": "66", "mmmm": "0F", "W": "WIG", "W512": "W1", "opcode": "E6", "mod": "/r", "evex": "1"},
    "xmmymm": {"L": "256", "pp": "66", "mmmm": "0F", "W": "WIG", "W512": "W1", "opcode": "E6", "mod": "/r", "evex": "1"},
    "xmmmem256": {"L": "256", "pp": "66", "mmmm": "0F", "W": "WIG", "W512": "W1", "opcode": "E6", "mod": "/r", "evex": "1"},
    "ymmzmm": {"L": "512", "pp": "66", "mmmm": "0F", "W": "WIG", "W512": "W1", "opcode": "E6", "mod": "/r", "evex": "1"},
    "ymmmem512": {"L": "512", "pp": "66", "mmmm": "0F", "W": "WIG", "W512": "W1", "opcode": "E6", "mod": "/r", "evex": "1"}
}

VCVTDQ2PD = {
    "xmmxmm": {"L": "128", "pp": "F3", "mmmm": "0F", "W": "WIG", "W512": "W0", "opcode": "E6", "mod": "/r", "evex": "1"},
    "xmmmem64": {"L": "128", "pp": "F3", "mmmm": "0F", "W": "WIG", "W512": "W0", "opcode": "E6", "mod": "/r", "evex": "1"},
    "ymmxmm": {"L": "256", "pp": "F3", "mmmm": "0F", "W": "WIG", "W512": "W0", "opcode": "E6", "mod": "/r", "evex": "1"},
    "ymmmem128": {"L": "256", "pp": "F3", "mmmm": "0F", "W": "WIG", "W512": "W0", "opcode": "E6", "mod": "/r", "evex": "1"},
    "zmmymm": {"L": "512", "pp": "F3", "mmmm": "0F", "W": "WIG", "W512": "W0", "opcode": "E6", "mod": "/r", "evex": "1"},
    "zmmmem256": {"L": "512", "pp": "F3", "mmmm": "0F", "W": "WIG", "W512": "W0", "opcode": "E6", "mod": "/r", "evex": "1"}
}

VCVTPS2PD = {
    "xmmxmm": {"L": "128", "mmmm": "0F", "W": "WIG", "W512": "W0", "opcode": "5A", "mod": "/r", "evex": "1"},
    "xmmmem64": {"L": "128", "mmmm": "0F", "W": "WIG", "W512": "W0", "opcode": "5A", "mod": "/r", "evex": "1"},
    "ymmxmm": {"L": "256", "mmmm": "0F", "W": "WIG", "W512": "W0", "opcode": "5A", "mod": "/r", "evex": "1"},
    "ymmmem128": {"L": "256", "mmmm": "0F", "W": "WIG", "W512": "W0", "opcode": "5A", "mod": "/r", "evex": "1"},
    "zmmymm": {"L": "512", "mmmm": "0F", "W": "WIG", "W512": "W0", "opcode": "5A", "mod": "/r", "evex": "1"},
    "zmmmem256": {"L": "512", "mmmm": "0F", "W": "WIG", "W512": "W0", "opcode": "5A", "mod": "/r", "evex": "1"}
}

VCVTPD2PS = {
    "xmmxmm": {"L": "128", "pp": "66", "mmmm": "0F", "W": "WIG", "W512": "W1", "opcode": "5A", "mod": "/r", "evex": "1"},
    "xmmmem128": {"L": "128", "pp": "66", "mmmm": "0F", "W": "WIG", "W512": "W1", "opcode": "5A", "mod": "/r", "evex": "1"},
    "xmmymm": {"L": "256", "pp": "66", "mmmm": "0F", "W": "WIG", "W512": "W1", "opcode": "5A", "mod": "/r", "evex": "1"},
    "xmmmem256": {"L": "256", "pp": "66", "mmmm": "0F", "W": "WIG", "W512": "W1", "opcode": "5A", "mod": "/r", "evex": "1"},
    "ymmzmm": {"L": "512", "pp": "66", "mmmm": "0F", "W": "WIG", "W512": "W1", "opcode": "5A", "mod": "/r", "evex": "1"},
    "ymmmem512": {"L": "512", "pp": "66", "mmmm": "0F", "W": "WIG", "W512": "W1", "opcode": "5A", "mod": "/r", "evex": "1"}
}

VCVTSS2SD = {
    "xmmxmmxmm": {"L": "LIG", "vvvv": "NDS", "pp": "F3", "mmmm": "0F", "W": "WIG", "W512": "W0", "opcode": "5A", "mod": "/r", "evex": "1"},
    "xmmxmmmem32": {"L": "LIG", "vvvv": "NDS", "pp": "F3", "mmmm": "0F", "W": "WIG", "W512": "W0", "opcode": "5A", "mod": "/r", "evex": "1"}
}

VCVTSD2SS = {
    "xmmxmmxmm": {"L": "LIG", "vvvv": "NDS", "pp": "F2", "mmmm": "0F", "W": "WIG", "W512": "W1", "opcode": "5A", "mod": "/r", "evex": "1"},
    "xmmxmmmem64": {"L": "LIG", "vvvv": "NDS", "pp": "F2", "mmmm": "0F", "W": "WIG", "W512": "W1", "opcode": "5A", "mod": "/r", "evex": "1"}
}

VCVTSD2SI = {
    "r32xmm": {"L": "LIG", "pp": "F2", "mmmm": "0F", "W": "W0", "opcode": "2D", "mod": "/r", "evex": "1"},
    "r32mem64": {"L": "LIG", "pp": "F2", "mmmm": "0F", "W": "W0", "opcode": "2D", "mod": "/r", "evex": "1"},
    "r64xmm": {"L": "LIG", "pp": "F2", "mmmm": "0F", "W": "W1", "opcode": "2D", "mod": "/r", "evex": "1"},
    "r64mem64": {"L": "LIG", "pp": "F2", "mmmm": "0F", "W": "W1", "opcode": "2D", "mod": "/r", "evex": "1"}
}

VCVTTSD2SI = {
    "r32xmm": {"L": "LIG", "pp": "F2", "mmmm": "0F", "W": "W0", "opcode": "2C", "mod": "/r", "evex": "1"},
    "r32mem64": {"L": "LIG", "pp": "F2", "mmmm": "0F", "W": "W0", "opcode": "2C", "mod": "/r", "evex": "1"},
    "r64xmm": {"L": "LIG", "pp": "F2", "mmmm": "0F", "W": "W1", "opcode": "2C", "mod": "/r", "evex": "1"},
    "r64mem64": {"L": "LIG", "pp": "F2", "mmmm": "0F", "W": "W1", "opcode": "2C", "mod": "/r", "evex": "1"}
}

VCVTSI2SD = {
    "xmmxmmr32": {"L": "LIG", "vvvv": "NDS", "pp": "F2", "mmmm": "0F", "W": "W0", "opcode": "2A", "mod": "/r", "evex": "1"},
    "xmmxmmmem32": {"L": "LIG", "vvvv": "NDS", "pp": "F2", "mmmm": "0F", "W": "W0", "opcode": "2A", "mod": "/r", "evex": "1"},
    "xmmxmmr64": {"L": "LIG", "vvvv": "NDS", "pp": "F2", "mmmm": "0F", "W": "W1", "opcode": "2A", "mod": "/r", "evex": "1"},
    "xmmxmmmem64": {"L": "LIG", "vvvv": "NDS", "pp": "F2", "mmmm": "0F", "W": "W1", "opcode": "2A", "mod": "/r", "evex": "1"}
}

VCVTDQ2PS = {
    "xmmxmm": {"L": "128", "mmmm": "0F", "W": "WIG", "W512": "W0", "opcode": "5B", "mod": "/r", "evex": "1"},
    "xmmmem128": {"L": "128", "mmmm": "0F", "W": "WIG", "W512": "W0", "opcode": "5B", "mod": "/r", "evex": "1"},
    "ymmymm": {"L": "256", "mmmm": "0F", "W": "WIG", "W512": "W0", "opcode": "5B", "mod": "/r", "evex": "1"},
    "ymmmem256": {"L": "256", "mmmm": "0F", "W": "WIG", "W512": "W0", "opcode": "5B", "mod": "/r", "evex": "1"},
    "zmmzmm": {"L": "512", "mmmm": "0F", "W": "WIG", "W512": "W0", "opcode": "5B", "mod": "/r", "evex": "1"},
    "zmmmem512": {"L": "512", "mmmm": "0F", "W": "WIG", "W512": "W0", "opcode": "5B", "mod": "/r", "evex": "1"},

    "xmmmem32": {"L": "128", "mmmm": "0F", "W": "WIG", "W512": "W0", "opcode": "5B", "mod": "/r", "mbr": "1", "evex": "1"},
    "ymmmem32": {"L": "256", "mmmm": "0F", "W": "WIG", "W512": "W0", "opcode": "5B", "mod": "/r", "mbr": "1", "evex": "1"},
    "zmmmem32": {"L": "512", "mmmm": "0F", "W": "WIG", "W512": "W0", "opcode": "5B", "mod": "/r", "mbr": "1", "evex": "1"}
}

VCVTPS2DQ = {
    "xmmxmm": {"L": "128", "pp": "66", "mmmm": "0F", "W": "WIG", "W512": "W0", "opcode": "5B", "mod": "/r", "evex": "1"},
    "xmmmem128": {"L": "128", "pp": "66", "mmmm": "0F", "W": "WIG", "W512": "W0", "opcode": "5B", "mod": "/r", "evex": "1"},
    "ymmymm": {"L": "256", "pp": "66", "mmmm": "0F", "W": "WIG", "W512": "W0", "opcode": "5B", "mod": "/r", "evex": "1"},
    "ymmmem256": {"L": "256", "pp": "66", "mmmm": "0F", "W": "WIG", "W512": "W0", "opcode": "5B", "mod": "/r", "evex": "1"},
    "zmmzmm": {"L": "512", "pp": "66", "mmmm": "0F", "W": "WIG", "W512": "W0", "opcode": "5B", "mod": "/r", "evex": "1"},
    "zmmmem512": {"L": "512", "pp": "66", "mmmm": "0F", "W": "WIG", "W512": "W0", "opcode": "5B", "mod": "/r", "evex": "1"},

    "xmmmem32": {"L": "128", "pp": "66", "mmmm": "0F", "W": "WIG", "W512": "W0", "opcode": "5B", "mod": "/r", "mbr": "1", "evex": "1"},
    "ymmmem32": {"L": "256", "pp": "66", "mmmm": "0F", "W": "WIG", "W512": "W0", "opcode": "5B", "mod": "/r", "mbr": "1", "evex": "1"},
    "zmmmem32": {"L": "512", "pp": "66", "mmmm": "0F", "W": "WIG", "W512": "W0", "opcode": "5B", "mod": "/r", "mbr": "1", "evex": "1"}
}

VCVTTPS2DQ = {
    "xmmxmm": {"L": "128", "pp": "F3", "mmmm": "0F", "W": "WIG", "W512": "W0", "opcode": "5B", "mod": "/r", "evex": "1"},
    "xmmmem128": {"L": "128", "pp": "F3", "mmmm": "0F", "W": "WIG", "W512": "W0", "opcode": "5B", "mod": "/r", "evex": "1"},
    "ymmymm": {"L": "256", "pp": "F3", "mmmm": "0F", "W": "WIG", "W512": "W0", "opcode": "5B", "mod": "/r", "evex": "1"},
    "ymmmem256": {"L": "256", "pp": "F3", "mmmm": "0F", "W": "WIG", "W512": "W0", "opcode": "5B", "mod": "/r", "evex": "1"},
    "zmmzmm": {"L": "512", "pp": "F3", "mmmm": "0F", "W": "WIG", "W512": "W0", "opcode": "5B", "mod": "/r", "evex": "1"},
    "zmmmem512": {"L": "512", "pp": "F3", "mmmm": "0F", "W": "WIG", "W512": "W0", "opcode": "5B", "mod": "/r", "evex": "1"},

   "xmmmem32": {"L": "128", "pp": "F3", "mmmm": "0F", "W": "WIG", "W512": "W0", "opcode": "5B", "mod": "/r", "mbr": "1", "evex": "1"},
   "ymmmem32": {"L": "256", "pp": "F3", "mmmm": "0F", "W": "WIG", "W512": "W0", "opcode": "5B", "mod": "/r", "mbr": "1", "evex": "1"},
   "zmmmem32": {"L": "512", "pp": "F3", "mmmm": "0F", "W": "WIG", "W512": "W0", "opcode": "5B", "mod": "/r", "mbr": "1", "evex": "1"}
}

VMOVDQA = {
    "xmmxmm": {"L": "128", "pp": "66", "mmmm": "0F", "W": "WIG", "opcode": "6F", "mod": "/r"},
    "xmmmem128": {"L": "128", "pp": "66", "mmmm": "0F", "W": "WIG", "opcode": "6F", "mod": "/r"},
    "mem128xmm": {"L": "128", "pp": "66", "mmmm": "0F", "W": "WIG", "opcode": "7F", "mod": "/r"},

    "ymmymm": {"L": "256", "pp": "66", "mmmm": "0F", "W": "WIG", "opcode": "6F", "mod": "/r"},
    "ymmmem256": {"L": "256", "pp": "66", "mmmm": "0F", "W": "WIG", "opcode": "6F", "mod": "/r"},
    "mem256ymm": {"L": "256", "pp": "66", "mmmm": "0F", "W": "WIG", "opcode": "7F", "mod": "/r"},
}

VMOVDQU = {
    "xmmxmm": {"L": "128", "pp": "F3", "mmmm": "0F", "W": "WIG", "opcode": "6F", "mod": "/r"},
    "xmmmem128": {"L": "128", "pp": "F3", "mmmm": "0F", "W": "WIG", "opcode": "6F", "mod": "/r"},
    "mem128xmm": {"L": "128", "pp": "F3", "mmmm": "0F", "W": "WIG", "opcode": "7F", "mod": "/r"},

    "ymmymm": {"L": "256", "pp": "F3", "mmmm": "0F", "W": "WIG", "opcode": "6F", "mod": "/r"},
    "ymmmem256": {"L": "256", "pp": "F3", "mmmm": "0F", "W": "WIG", "opcode": "6F", "mod": "/r"},
    "mem256ymm": {"L": "256", "pp": "F3", "mmmm": "0F", "W": "WIG", "opcode": "7F", "mod": "/r"},
}

VPMULUDQ = {
    "xmmxmmxmm": {"vvvv": "NDS", "L": "128", "pp": "66", "mmmm": "0F", "W": "WIG", "W512": "W1", "opcode": "F4", "mod": "/r", "evex": "1"},
    "xmmxmmmem128": {"vvvv": "NDS", "L": "128", "pp": "66", "mmmm": "0F", "W": "WIG", "W512": "W1", "opcode": "F4", "mod": "/r", "evex": "1"},
    "ymmymmymm": {"vvvv": "NDS", "L": "256", "pp": "66", "mmmm": "0F", "W": "WIG", "W512": "W1", "opcode": "F4", "mod": "/r", "evex": "1"},
    "ymmymmmem256": {"vvvv": "NDS", "L": "256", "pp": "66", "mmmm": "0F", "W": "WIG", "W512": "W1", "opcode": "F4", "mod": "/r", "evex": "1"},
    "zmmzmmzmm": {"vvvv": "NDS", "L": "512", "pp": "66", "mmmm": "0F", "W": "WIG", "W512": "W1", "opcode": "F4", "mod": "/r", "evex": "1"},
    "zmmzmmmem512": {"vvvv": "NDS", "L": "512", "pp": "66", "mmmm": "0F", "W": "WIG", "W512": "W1", "opcode": "F4", "mod": "/r", "evex": "1"},

    "xmmxmmmem64": {"vvvv": "NDS", "L": "128", "pp": "66", "mmmm": "0F", "W": "WIG", "W512": "W1", "opcode": "F4", "mod": "/r", "mbr": "1", "evex": "1"},
    "ymmymmmem64": {"vvvv": "NDS", "L": "256", "pp": "66", "mmmm": "0F", "W": "WIG", "W512": "W1", "opcode": "F4", "mod": "/r", "mbr": "1", "evex": "1"},
    "zmmzmmmem64": {"vvvv": "NDS", "L": "512", "pp": "66", "mmmm": "0F", "W": "WIG", "W512": "W1", "opcode": "F4", "mod": "/r", "mbr": "1", "evex": "1"}
}

VPADDQ = {
    "xmmxmmxmm": {"vvvv": "NDS", "L": "128", "pp": "66", "mmmm": "0F", "W": "WIG", "W512": "W1", "opcode": "D4", "mod": "/r", "evex": "1"},
    "xmmxmmmem128": {"vvvv": "NDS", "L": "128", "pp": "66", "mmmm": "0F", "W": "WIG", "W512": "W1", "opcode": "D4", "mod": "/r", "evex": "1"},
    "ymmymmymm": {"vvvv": "NDS", "L": "256", "pp": "66", "mmmm": "0F", "W": "WIG", "W512": "W1", "opcode": "D4", "mod": "/r", "evex": "1"},
    "ymmymmmem256": {"vvvv": "NDS", "L": "256", "pp": "66", "mmmm": "0F", "W": "WIG", "W512": "W1", "opcode": "D4", "mod": "/r", "evex": "1"},
    "zmmzmmzmm": {"vvvv": "NDS", "L": "512", "pp": "66", "mmmm": "0F", "W": "WIG", "W512": "W1", "opcode": "D4", "mod": "/r", "evex": "1"},
    "zmmzmmmem512": {"vvvv": "NDS", "L": "512", "pp": "66", "mmmm": "0F", "W": "WIG", "W512": "W1", "opcode": "D4", "mod": "/r", "evex": "1"},

    "xmmxmmmem64": {"vvvv": "NDS", "L": "128", "pp": "66", "mmmm": "0F", "W": "WIG", "W512": "W1", "opcode": "D4", "mod": "/r", "mbr": "1", "evex": "1"},
    "ymmymmmem64": {"vvvv": "NDS", "L": "256", "pp": "66", "mmmm": "0F", "W": "WIG", "W512": "W1", "opcode": "D4", "mod": "/r", "mbr": "1", "evex": "1"},
    "zmmzmmmem64": {"vvvv": "NDS", "L": "512", "pp": "66", "mmmm": "0F", "W": "WIG", "W512": "W1", "opcode": "D4", "mod": "/r", "mbr": "1", "evex": "1"}
}

VPSUBQ = {
    "xmmxmmxmm": {"vvvv": "NDS", "L": "128", "pp": "66", "mmmm": "0F", "W": "WIG", "W512": "W1", "opcode": "FB", "mod": "/r", "evex": "1"},
    "xmmxmmmem128": {"vvvv": "NDS", "L": "128", "pp": "66", "mmmm": "0F", "W": "WIG", "W512": "W1", "opcode": "FB", "mod": "/r", "evex": "1"},
    "ymmymmymm": {"vvvv": "NDS", "L": "256", "pp": "66", "mmmm": "0F", "W": "WIG", "W512": "W1", "opcode": "FB", "mod": "/r", "evex": "1"},
    "ymmymmmem256": {"vvvv": "NDS", "L": "256", "pp": "66", "mmmm": "0F", "W": "WIG", "W512": "W1", "opcode": "FB", "mod": "/r", "evex": "1"},
    "zmmzmmzmm": {"vvvv": "NDS", "L": "512", "pp": "66", "mmmm": "0F", "W": "WIG", "W512": "W1", "opcode": "FB", "mod": "/r", "evex": "1"},
    "zmmzmmmem512": {"vvvv": "NDS", "L": "512", "pp": "66", "mmmm": "0F", "W": "WIG", "W512": "W1", "opcode": "FB", "mod": "/r", "evex": "1"},

    "xmmxmmmem64": {"vvvv": "NDS", "L": "128", "pp": "66", "mmmm": "0F", "W": "WIG", "W512": "W1", "opcode": "FB", "mod": "/r", "mbr": "1", "evex": "1"},
    "ymmymmmem64": {"vvvv": "NDS", "L": "256", "pp": "66", "mmmm": "0F", "W": "WIG", "W512": "W1", "opcode": "FB", "mod": "/r", "mbr": "1", "evex": "1"},
    "zmmzmmmem64": {"vvvv": "NDS", "L": "512", "pp": "66", "mmmm": "0F", "W": "WIG", "W512": "W1", "opcode": "FB", "mod": "/r", "mbr": "1", "evex": "1"}
}

VPSHUFLW = {
    "xmmxmmxmmimm8": {"L": "128", "pp": "F2", "mmmm": "0F", "W": "WIG", "opcode": "70", "mod": "/r", "imm": "ib", "evex": "1"},
    "xmmxmmmem128imm8": {"L": "128", "pp": "F2", "mmmm": "0F", "W": "WIG", "opcode": "70", "mod": "/r", "imm": "ib", "evex": "1"},
    "ymmymmymmimm8": {"L": "256", "pp": "F2", "mmmm": "0F", "W": "WIG", "opcode": "70", "mod": "/r", "imm": "ib", "evex": "1"},
    "ymmymmmem256imm8": {"L": "256", "pp": "F2", "mmmm": "0F", "W": "WIG", "opcode": "70", "mod": "/r", "imm": "ib", "evex": "1"},
    "zmmzmmzmmimm8": {"L": "512", "pp": "F2", "mmmm": "0F", "W": "WIG", "opcode": "70", "mod": "/r", "imm": "ib", "evex": "1"},
    "zmmzmmmem512imm8": {"L": "512", "pp": "F2", "mmmm": "0F", "W": "WIG", "opcode": "70", "mod": "/r", "imm": "ib", "evex": "1"}
}

VPSHUFHW = {
    "xmmxmmxmmimm8": {"L": "128", "pp": "F3", "mmmm": "0F", "W": "WIG", "opcode": "70", "mod": "/r", "imm": "ib", "evex": "1"},
    "xmmxmmmem128imm8": {"L": "128", "pp": "F3", "mmmm": "0F", "W": "WIG", "opcode": "70", "mod": "/r", "imm": "ib", "evex": "1"},
    "ymmymmymmimm8": {"L": "256", "pp": "F3", "mmmm": "0F", "W": "WIG", "opcode": "70", "mod": "/r", "imm": "ib", "evex": "1"},
    "ymmymmmem256imm8": {"L": "256", "pp": "F3", "mmmm": "0F", "W": "WIG", "opcode": "70", "mod": "/r", "imm": "ib", "evex": "1"},
    "zmmzmmzmmimm8": {"L": "512", "pp": "F3", "mmmm": "0F", "W": "WIG", "opcode": "70", "mod": "/r", "imm": "ib", "evex": "1"},
    "zmmzmmmem512imm8": {"L": "512", "pp": "F3", "mmmm": "0F", "W": "WIG", "opcode": "70", "mod": "/r", "imm": "ib", "evex": "1"}
}

VPSHUFD = {
    "xmmxmmimm8": {"L": "128", "pp": "66", "mmmm": "0F", "W": "WIG", "W512": "W0", "opcode": "70", "mod": "/r", "imm": "ib", "evex": "1"},
    "xmmmem128imm8": {"L": "128", "pp": "66", "mmmm": "0F", "W": "WIG", "W512": "W0", "opcode": "70", "mod": "/r", "imm": "ib", "evex": "1"},
    "ymmymmimm8": {"L": "256", "pp": "66", "mmmm": "0F", "W": "WIG", "W512": "W0", "opcode": "70", "mod": "/r", "imm": "ib", "evex": "1"},
    "ymmmem256imm8": {"L": "256", "pp": "66", "mmmm": "0F", "W": "WIG", "W512": "W0", "opcode": "70", "mod": "/r", "imm": "ib", "evex": "1"},
    "zmmzmmimm8": {"L": "512", "pp": "66", "mmmm": "0F", "W": "WIG", "W512": "W0", "opcode": "70", "mod": "/r", "imm": "ib", "evex": "1"},
    "zmmmem512imm8": {"L": "512", "pp": "66", "mmmm": "0F", "W": "WIG", "W512": "W0", "opcode": "70", "mod": "/r", "imm": "ib", "evex": "1"},

    "xmmmem32imm8": {"L": "128", "pp": "66", "mmmm": "0F", "W": "WIG", "W512": "W0", "opcode": "70", "mod": "/r", "imm": "ib", "mbr": "1", "evex": "1"},
    "ymmmem32imm8": {"L": "256", "pp": "66", "mmmm": "0F", "W": "WIG", "W512": "W0", "opcode": "70", "mod": "/r", "imm": "ib", "mbr": "1", "evex": "1"},
    "zmmmem32imm8": {"L": "512", "pp": "66", "mmmm": "0F", "W": "WIG", "W512": "W0", "opcode": "70", "mod": "/r", "imm": "ib", "mbr": "1", "evex": "1"}
}

VPSLLDQ = {
    "xmmxmmimm8": {"vvvv": "NDD", "L": "128", "pp": "66", "mmmm": "0F", "W": "WIG", "opcode": "73", "mod": "/7", "imm": "ib", "evex": "1"},
    "ymmymmimm8": {"vvvv": "NDD", "L": "256", "pp": "66", "mmmm": "0F", "W": "WIG", "opcode": "73", "mod": "/7", "imm": "ib", "evex": "1"},
    # Only AVX-512 support combinations with memory as second operand
    "zmmzmmimm8": {"vvvv": "NDD", "L": "512", "pp": "66", "mmmm": "0F", "W": "WIG", "opcode": "73", "mod": "/7", "imm": "ib", "evex": "1"},
    "xmmmem128imm8": {"vvvv": "NDD", "L": "128", "pp": "66", "mmmm": "0F", "W": "WIG", "opcode": "73", "mod": "/7", "imm": "ib", "evex": "1"},
    "ymmmem256imm8": {"vvvv": "NDD", "L": "256", "pp": "66", "mmmm": "0F", "W": "WIG", "opcode": "73", "mod": "/7", "imm": "ib", "evex": "1"},
    "zmmmem512imm8": {"vvvv": "NDD", "L": "512", "pp": "66", "mmmm": "0F", "W": "WIG", "opcode": "73", "mod": "/7", "imm": "ib", "evex": "1"}
}

VPSRLDQ = {
    "xmmxmmimm8": {"vvvv": "NDD", "L": "128", "pp": "66", "mmmm": "0F", "W": "WIG", "opcode": "73", "mod": "/3", "imm": "ib", "evex": "1"},
    "ymmymmimm8": {"vvvv": "NDD", "L": "256", "pp": "66", "mmmm": "0F", "W": "WIG", "opcode": "73", "mod": "/3", "imm": "ib", "evex": "1"},
    "zmmzmmimm8": {"vvvv": "NDD", "L": "512", "pp": "66", "mmmm": "0F", "W": "WIG", "opcode": "73", "mod": "/3", "imm": "ib", "evex": "1"},

    # Only AVX-512 support combinations with memory as second operand
    "xmmmem128imm8": {"vvvv": "NDD", "L": "128", "pp": "66", "mmmm": "0F", "W": "WIG", "opcode": "73", "mod": "/3", "imm": "ib", "evex": "1"},
    "ymmmem256imm8": {"vvvv": "NDD", "L": "256", "pp": "66", "mmmm": "0F", "W": "WIG", "opcode": "73", "mod": "/3", "imm": "ib", "evex": "1"},
    "zmmmem512imm8": {"vvvv": "NDD", "L": "512", "pp": "66", "mmmm": "0F", "W": "WIG", "opcode": "73", "mod": "/3", "imm": "ib", "evex": "1"}
}

VPUNPCKHQDQ = {
    "xmmxmmxmm": {"vvvv": "NDS", "L": "128", "pp": "66", "mmmm": "0F", "W": "WIG", "W512": "W1", "opcode": "6D", "mod": "/r", "evex": "1"},
    "xmmxmmmem128": {"vvvv": "NDS", "L": "128", "pp": "66", "mmmm": "0F", "W": "WIG", "W512": "W1", "opcode": "6D", "mod": "/r", "evex": "1"},
    "ymmymmymm": {"vvvv": "NDS", "L": "256", "pp": "66", "mmmm": "0F", "W": "WIG", "W512": "W1", "opcode": "6D", "mod": "/r", "evex": "1"},
    "ymmymmmem256": {"vvvv": "NDS", "L": "256", "pp": "66", "mmmm": "0F", "W": "WIG", "W512": "W1", "opcode": "6D", "mod": "/r", "evex": "1"},
    "zmmzmmzmm": {"vvvv": "NDS", "L": "512", "pp": "66", "mmmm": "0F", "W": "WIG", "W512": "W1", "opcode": "6D", "mod": "/r", "evex": "1"},
    "zmmzmmmem512": {"vvvv": "NDS", "L": "512", "pp": "66", "mmmm": "0F", "W": "WIG", "W512": "W1", "opcode": "6D", "mod": "/r", "evex": "1"},

    "xmmxmmmem64": {"vvvv": "NDS", "L": "128", "pp": "66", "mmmm": "0F", "W": "WIG", "W512": "W1", "opcode": "6D", "mod": "/r", "mbr": "1", "evex": "1"},
    "ymmymmmem64": {"vvvv": "NDS", "L": "256", "pp": "66", "mmmm": "0F", "W": "WIG", "W512": "W1", "opcode": "6D", "mod": "/r", "mbr": "1", "evex": "1"},
    "zmmzmmmem64": {"vvvv": "NDS", "L": "512", "pp": "66", "mmmm": "0F", "W": "WIG", "W512": "W1", "opcode": "6D", "mod": "/r", "mbr": "1", "evex": "1"}
}

VPUNPCKLQDQ = {
    "xmmxmmxmm": {"vvvv": "NDS", "L": "128", "pp": "66", "mmmm": "0F", "W": "WIG", "W512": "W1", "opcode": "6C", "mod": "/r", "evex": "1"},
    "xmmxmmmem128": {"vvvv": "NDS", "L": "128", "pp": "66", "mmmm": "0F", "W": "WIG", "W512": "W1", "opcode": "6C", "mod": "/r", "evex": "1"},
    "ymmymmymm": {"vvvv": "NDS", "L": "256", "pp": "66", "mmmm": "0F", "W": "WIG", "W512": "W1", "opcode": "6C", "mod": "/r", "evex": "1"},
    "ymmymmmem256": {"vvvv": "NDS", "L": "256", "pp": "66", "mmmm": "0F", "W": "WIG", "W512": "W1", "opcode": "6C", "mod": "/r", "evex": "1"},
    "zmmzmmzmm": {"vvvv": "NDS", "L": "512", "pp": "66", "mmmm": "0F", "W": "WIG", "W512": "W1", "opcode": "6C", "mod": "/r", "evex": "1"},
    "zmmzmmmem512": {"vvvv": "NDS", "L": "512", "pp": "66", "mmmm": "0F", "W": "WIG", "W512": "W1", "opcode": "6C", "mod": "/r", "evex": "1"},

    "xmmxmmmem64": {"vvvv": "NDS", "L": "128", "pp": "66", "mmmm": "0F", "W": "WIG", "W512": "W1", "opcode": "6C", "mod": "/r", "mbr": "1", "evex": "1"},
    "ymmymmmem64": {"vvvv": "NDS", "L": "256", "pp": "66", "mmmm": "0F", "W": "WIG", "W512": "W1", "opcode": "6C", "mod": "/r", "mbr": "1", "evex": "1"},
    "zmmzmmmem64": {"vvvv": "NDS", "L": "512", "pp": "66", "mmmm": "0F", "W": "WIG", "W512": "W1", "opcode": "6C", "mod": "/r", "mbr": "1", "evex": "1"}
}

VMASKMOVDQU = {
    "xmmxmm": {"L": "128", "pp": "66", "mmmm": "0F", "W": "WIG", "opcode": "F7", "mod": "/r"},
}

VMOVNTPD = {
    "mem128xmm": {"L": "128", "pp": "66", "mmmm": "0F", "W": "WIG", "W512": "W1", "opcode": "2B", "mod": "/r", "evex": "1"},
    "mem256ymm": {"L": "256", "pp": "66", "mmmm": "0F", "W": "WIG", "W512": "W1", "opcode": "2B", "mod": "/r", "evex": "1"},
    "mem512zmm": {"L": "512", "pp": "66", "mmmm": "0F", "W": "WIG", "W512": "W1", "opcode": "2B", "mod": "/r", "evex": "1"}
}

VMOVNTDQ = {
    "mem128xmm": {"L": "128", "pp": "66", "mmmm": "0F", "W": "WIG", "W512": "W0", "opcode": "E7", "mod": "/r", "evex": "1"},
    "mem256ymm": {"L": "256", "pp": "66", "mmmm": "0F", "W": "WIG", "W512": "W0", "opcode": "E7", "mod": "/r", "evex": "1"},
    "mem512zmm": {"L": "512", "pp": "66", "mmmm": "0F", "W": "WIG", "W512": "W0", "opcode": "E7", "mod": "/r", "evex": "1"}
}

# AVX SSE3 Instructions

VLDDQU = {
    "xmmmem128": {"L": "128", "pp": "F2", "mmmm": "0F", "W": "WIG", "opcode": "F0", "mod": "/r"},
    "ymmmem256": {"L": "256", "pp": "F2", "mmmm": "0F", "W": "WIG", "opcode": "F0", "mod": "/r"},
}

VADDSUBPS = {
    "xmmxmmxmm": {"vvvv": "NDS", "L": "128", "pp": "F2", "mmmm": "0F", "W": "WIG", "opcode": "D0", "mod": "/r"},
    "xmmxmmmem128": {"vvvv": "NDS", "L": "128", "pp": "F2", "mmmm": "0F", "W": "WIG", "opcode": "D0", "mod": "/r"},
    "ymmymmymm": {"vvvv": "NDS", "L": "256", "pp": "F2", "mmmm": "0F", "W": "WIG", "opcode": "D0", "mod": "/r"},
    "ymmymmmem256": {"vvvv": "NDS", "L": "256", "pp": "F2", "mmmm": "0F", "W": "WIG", "opcode": "D0", "mod": "/r"},
}

VADDSUBPD = {
    "xmmxmmxmm": {"vvvv": "NDS", "L": "128", "pp": "66", "mmmm": "0F", "W": "WIG", "opcode": "D0", "mod": "/r"},
    "xmmxmmmem128": {"vvvv": "NDS", "L": "128", "pp": "66", "mmmm": "0F", "W": "WIG", "opcode": "D0", "mod": "/r"},
    "ymmymmymm": {"vvvv": "NDS", "L": "256", "pp": "66", "mmmm": "0F", "W": "WIG", "opcode": "D0", "mod": "/r"},
    "ymmymmmem256": {"vvvv": "NDS", "L": "256", "pp": "66", "mmmm": "0F", "W": "WIG", "opcode": "D0", "mod": "/r"},
}

VHADDPS = {
    "xmmxmmxmm": {"vvvv": "NDS", "L": "128", "pp": "F2", "mmmm": "0F", "W": "WIG", "opcode": "7C", "mod": "/r"},
    "xmmxmmmem128": {"vvvv": "NDS", "L": "128", "pp": "F2", "mmmm": "0F", "W": "WIG", "opcode": "7C", "mod": "/r"},
    "ymmymmymm": {"vvvv": "NDS", "L": "256", "pp": "F2", "mmmm": "0F", "W": "WIG", "opcode": "7C", "mod": "/r"},
    "ymmymmmem256": {"vvvv": "NDS", "L": "256", "pp": "F2", "mmmm": "0F", "W": "WIG", "opcode": "7C", "mod": "/r"},
}

VHSUBPS = {
    "xmmxmmxmm": {"vvvv": "NDS", "L": "128", "pp": "F2", "mmmm": "0F", "W": "WIG", "opcode": "7D", "mod": "/r"},
    "xmmxmmmem128": {"vvvv": "NDS", "L": "128", "pp": "F2", "mmmm": "0F", "W": "WIG", "opcode": "7D", "mod": "/r"},
    "ymmymmymm": {"vvvv": "NDS", "L": "256", "pp": "F2", "mmmm": "0F", "W": "WIG", "opcode": "7D", "mod": "/r"},
    "ymmymmmem256": {"vvvv": "NDS", "L": "256", "pp": "F2", "mmmm": "0F", "W": "WIG", "opcode": "7D", "mod": "/r"},
}

VHADDPD = {
    "xmmxmmxmm": {"vvvv": "NDS", "L": "128", "pp": "66", "mmmm": "0F", "W": "WIG", "opcode": "7C", "mod": "/r"},
    "xmmxmmmem128": {"vvvv": "NDS", "L": "128", "pp": "66", "mmmm": "0F", "W": "WIG", "opcode": "7C", "mod": "/r"},
    "ymmymmymm": {"vvvv": "NDS", "L": "256", "pp": "66", "mmmm": "0F", "W": "WIG", "opcode": "7C", "mod": "/r"},
    "ymmymmmem256": {"vvvv": "NDS", "L": "256", "pp": "66", "mmmm": "0F", "W": "WIG", "opcode": "7C", "mod": "/r"},
}

VHSUBPD = {
    "xmmxmmxmm": {"vvvv": "NDS", "L": "128", "pp": "66", "mmmm": "0F", "W": "WIG", "opcode": "7D", "mod": "/r"},
    "xmmxmmmem128": {"vvvv": "NDS", "L": "128", "pp": "66", "mmmm": "0F", "W": "WIG", "opcode": "7D", "mod": "/r"},
    "ymmymmymm": {"vvvv": "NDS", "L": "256", "pp": "66", "mmmm": "0F", "W": "WIG", "opcode": "7D", "mod": "/r"},
    "ymmymmmem256": {"vvvv": "NDS", "L": "256", "pp": "66", "mmmm": "0F", "W": "WIG", "opcode": "7D", "mod": "/r"},
}

VMOVSLDUP = {
    "xmmxmm": {"L": "128", "pp": "F3", "mmmm": "0F", "W": "WIG", "W512": "W0", "opcode": "12", "mod": "/r", "evex": "1"},
    "xmmmem128": {"L": "128", "pp": "F3", "mmmm": "0F", "W": "WIG", "W512": "W0", "opcode": "12", "mod": "/r", "evex": "1"},
    "ymmymm": {"L": "256", "pp": "F3", "mmmm": "0F", "W": "WIG", "W512": "W0", "opcode": "12", "mod": "/r", "evex": "1"},
    "ymmmem256": {"L": "256", "pp": "F3", "mmmm": "0F", "W": "WIG", "W512": "W0", "opcode": "12", "mod": "/r", "evex": "1"},
    "zmmzmm": {"L": "512", "pp": "F3", "mmmm": "0F", "W": "WIG", "W512": "W0", "opcode": "12", "mod": "/r", "evex": "1"},
    "zmmmem512": {"L": "512", "pp": "F3", "mmmm": "0F", "W": "WIG", "W512": "W0", "opcode": "12", "mod": "/r", "evex": "1"}
}

VMOVSHDUP = {
    "xmmxmm": {"L": "128", "pp": "F3", "mmmm": "0F", "W": "WIG", "W512": "W0", "opcode": "16", "mod": "/r", "evex": "1"},
    "xmmmem128": {"L": "128", "pp": "F3", "mmmm": "0F", "W": "WIG", "W512": "W0", "opcode": "16", "mod": "/r", "evex": "1"},
    "ymmymm": {"L": "256", "pp": "F3", "mmmm": "0F", "W": "WIG", "W512": "W0", "opcode": "16", "mod": "/r", "evex": "1"},
    "ymmmem256": {"L": "256", "pp": "F3", "mmmm": "0F", "W": "WIG", "W512": "W0", "opcode": "16", "mod": "/r", "evex": "1"},
    "zmmzmm": {"L": "512", "pp": "F3", "mmmm": "0F", "W": "WIG", "W512": "W0", "opcode": "16", "mod": "/r", "evex": "1"},
    "zmmmem512": {"L": "512", "pp": "F3", "mmmm": "0F", "W": "WIG", "W512": "W0", "opcode": "16", "mod": "/r", "evex": "1"}
}

VMOVDDUP = {
    "xmmxmm": {"L": "128", "pp": "F2", "mmmm": "0F", "W": "WIG", "W512": "W1", "opcode": "12", "mod": "/r", "evex": "1"},
    "xmmmem64": {"L": "128", "pp": "F2", "mmmm": "0F", "W": "WIG", "W512": "W1", "opcode": "12", "mod": "/r", "evex": "1"},
    "ymmymm": {"L": "256", "pp": "F2", "mmmm": "0F", "W": "WIG", "W512": "W1", "opcode": "12", "mod": "/r", "evex": "1"},
    "ymmmem256": {"L": "256", "pp": "F2", "mmmm": "0F", "W": "WIG", "W512": "W1", "opcode": "12", "mod": "/r", "evex": "1"},
    "zmmzmm": {"L": "512", "pp": "F2", "mmmm": "0F", "W": "WIG", "W512": "W1", "opcode": "12", "mod": "/r", "evex": "1"},
    "zmmmem512": {"L": "512", "pp": "F2", "mmmm": "0F", "W": "WIG", "W512": "W1", "opcode": "12", "mod": "/r", "evex": "1"}
}

# AVX SSSE3 Instructions

VPHADDW = {
    "xmmxmmxmm": {"vvvv": "NDS", "L": "128", "pp": "66", "mmmm": "0F38", "W": "WIG", "opcode": "01", "mod": "/r"},
    "xmmxmmmem128": {"vvvv": "NDS", "L": "128", "pp": "66", "mmmm": "0F38", "W": "WIG", "opcode": "01", "mod": "/r"},
    "ymmymmymm": {"vvvv": "NDS", "L": "256", "pp": "66", "mmmm": "0F38", "W": "WIG", "opcode": "01", "mod": "/r"},
    "ymmymmmem256": {"vvvv": "NDS", "L": "256", "pp": "66", "mmmm": "0F38", "W": "WIG", "opcode": "01", "mod": "/r"},
}

VPHADDSW = {
    "xmmxmmxmm": {"vvvv": "NDS", "L": "128", "pp": "66", "mmmm": "0F38", "W": "WIG", "opcode": "03", "mod": "/r"},
    "xmmxmmmem128": {"vvvv": "NDS", "L": "128", "pp": "66", "mmmm": "0F38", "W": "WIG", "opcode": "03", "mod": "/r"},
    "ymmymmymm": {"vvvv": "NDS", "L": "256", "pp": "66", "mmmm": "0F38", "W": "WIG", "opcode": "03", "mod": "/r"},
    "ymmymmmem256": {"vvvv": "NDS", "L": "256", "pp": "66", "mmmm": "0F38", "W": "WIG", "opcode": "03", "mod": "/r"},
}

VPHADDD = {
    "xmmxmmxmm": {"vvvv": "NDS", "L": "128", "pp": "66", "mmmm": "0F38", "W": "WIG", "opcode": "02", "mod": "/r"},
    "xmmxmmmem128": {"vvvv": "NDS", "L": "128", "pp": "66", "mmmm": "0F38", "W": "WIG", "opcode": "02", "mod": "/r"},
    "ymmymmymm": {"vvvv": "NDS", "L": "256", "pp": "66", "mmmm": "0F38", "W": "WIG", "opcode": "02", "mod": "/r"},
    "ymmymmmem256": {"vvvv": "NDS", "L": "256", "pp": "66", "mmmm": "0F38", "W": "WIG", "opcode": "02", "mod": "/r"},
}

VPHSUBW = {
    "xmmxmmxmm": {"vvvv": "NDS", "L": "128", "pp": "66", "mmmm": "0F38", "W": "WIG", "opcode": "05", "mod": "/r"},
    "xmmxmmmem128": {"vvvv": "NDS", "L": "128", "pp": "66", "mmmm": "0F38", "W": "WIG", "opcode": "05", "mod": "/r"},
    "ymmymmymm": {"vvvv": "NDS", "L": "256", "pp": "66", "mmmm": "0F38", "W": "WIG", "opcode": "05", "mod": "/r"},
    "ymmymmmem256": {"vvvv": "NDS", "L": "256", "pp": "66", "mmmm": "0F38", "W": "WIG", "opcode": "05", "mod": "/r"},
}

VPHSUBSW = {
    "xmmxmmxmm": {"vvvv": "NDS", "L": "128", "pp": "66", "mmmm": "0F38", "W": "WIG", "opcode": "07", "mod": "/r"},
    "xmmxmmmem128": {"vvvv": "NDS", "L": "128", "pp": "66", "mmmm": "0F38", "W": "WIG", "opcode": "07", "mod": "/r"},
    "ymmymmymm": {"vvvv": "NDS", "L": "256", "pp": "66", "mmmm": "0F38", "W": "WIG", "opcode": "07", "mod": "/r"},
    "ymmymmmem256": {"vvvv": "NDS", "L": "256", "pp": "66", "mmmm": "0F38", "W": "WIG", "opcode": "07", "mod": "/r"},
}

VPHSUBD = {
    "xmmxmmxmm": {"vvvv": "NDS", "L": "128", "pp": "66", "mmmm": "0F38", "W": "WIG", "opcode": "06", "mod": "/r"},
    "xmmxmmmem128": {"vvvv": "NDS", "L": "128", "pp": "66", "mmmm": "0F38", "W": "WIG", "opcode": "06", "mod": "/r"},
    "ymmymmymm": {"vvvv": "NDS", "L": "256", "pp": "66", "mmmm": "0F38", "W": "WIG", "opcode": "06", "mod": "/r"},
    "ymmymmmem256": {"vvvv": "NDS", "L": "256", "pp": "66", "mmmm": "0F38", "W": "WIG", "opcode": "06", "mod": "/r"},
}

VPABSB = {
    "xmmxmm": {"L": "128", "pp": "66", "mmmm": "0F38", "W": "WIG", "opcode": "1C", "mod": "/r", "evex": "1"},
    "xmmmem128": {"L": "128", "pp": "66", "mmmm": "0F38", "W": "WIG", "opcode": "1C", "mod": "/r", "evex": "1"},
    "ymmymm": {"L": "256", "pp": "66", "mmmm": "0F38", "W": "WIG", "opcode": "1C", "mod": "/r", "evex": "1"},
    "ymmmem256": {"L": "256", "pp": "66", "mmmm": "0F38", "W": "WIG", "opcode": "1C", "mod": "/r", "evex": "1"},
    "zmmzmm": {"L": "512", "pp": "66", "mmmm": "0F38", "W": "WIG", "opcode": "1C", "mod": "/r", "evex": "1"},
    "zmmmem512": {"L": "512", "pp": "66", "mmmm": "0F38", "W": "WIG", "opcode": "1C", "mod": "/r", "evex": "1"}
}

VPABSW = {
    "xmmxmm": {"L": "128", "pp": "66", "mmmm": "0F38", "W": "WIG", "opcode": "1D", "mod": "/r", "evex": "1"},
    "xmmmem128": {"L": "128", "pp": "66", "mmmm": "0F38", "W": "WIG", "opcode": "1D", "mod": "/r", "evex": "1"},
    "ymmymm": {"L": "256", "pp": "66", "mmmm": "0F38", "W": "WIG", "opcode": "1D", "mod": "/r", "evex": "1"},
    "ymmmem256": {"L": "256", "pp": "66", "mmmm": "0F38", "W": "WIG", "opcode": "1D", "mod": "/r", "evex": "1"},
    "zmmzmm": {"L": "512", "pp": "66", "mmmm": "0F38", "W": "WIG", "opcode": "1D", "mod": "/r", "evex": "1"},
    "zmmmem512": {"L": "512", "pp": "66", "mmmm": "0F38", "W": "WIG", "opcode": "1D", "mod": "/r", "evex": "1"}
}

VPABSD = {
    "xmmxmm": {"L": "128", "pp": "66", "mmmm": "0F38", "W": "WIG", "W512": "W0", "opcode": "1E", "mod": "/r", "evex": "1"},
    "xmmmem128": {"L": "128", "pp": "66", "mmmm": "0F38", "W": "WIG", "W512": "W0", "opcode": "1E", "mod": "/r", "evex": "1"},
    "ymmymm": {"L": "256", "pp": "66", "mmmm": "0F38", "W": "WIG", "W512": "W0", "opcode": "1E", "mod": "/r", "evex": "1"},
    "ymmmem256": {"L": "256", "pp": "66", "mmmm": "0F38", "W": "WIG", "W512": "W0", "opcode": "1E", "mod": "/r", "evex": "1"},
    "zmmzmm": {"L": "512", "pp": "66", "mmmm": "0F38", "W": "WIG", "W512": "W0", "opcode": "1E", "mod": "/r", "evex": "1"},
    "zmmmem512": {"L": "512", "pp": "66", "mmmm": "0F38", "W": "WIG", "W512": "W0", "opcode": "1E", "mod": "/r", "evex": "1"},

    "xmmmem32": {"L": "128", "pp": "66", "mmmm": "0F38", "W": "WIG", "W512": "W0", "opcode": "1E", "mod": "/r", "mbr": "1", "evex": "1"},
    "ymmmem32": {"L": "256", "pp": "66", "mmmm": "0F38", "W": "WIG", "W512": "W0", "opcode": "1E", "mod": "/r", "mbr": "1", "evex": "1"},
    "zmmmem32": {"L": "512", "pp": "66", "mmmm": "0F38", "W": "WIG", "W512": "W0", "opcode": "1E", "mod": "/r", "mbr": "1", "evex": "1"}
}

VPMADDUBSW = {
    "xmmxmmxmm": {"vvvv": "NDS", "L": "128", "pp": "66", "mmmm": "0F38", "W": "WIG", "opcode": "04", "mod": "/r", "evex": "1"},
    "xmmxmmmem128": {"vvvv": "NDS", "L": "128", "pp": "66", "mmmm": "0F38", "W": "WIG", "opcode": "04", "mod": "/r", "evex": "1"},
    "ymmymmymm": {"vvvv": "NDS", "L": "256", "pp": "66", "mmmm": "0F38", "W": "WIG", "opcode": "04", "mod": "/r", "evex": "1"},
    "ymmymmmem256": {"vvvv": "NDS", "L": "256", "pp": "66", "mmmm": "0F38", "W": "WIG", "opcode": "04", "mod": "/r", "evex": "1"},
    "zmmzmmzmm": {"vvvv": "NDS", "L": "512", "pp": "66", "mmmm": "0F38", "W": "WIG", "opcode": "04", "mod": "/r", "evex": "1"},
    "zmmzmmmem512": {"vvvv": "NDS", "L": "512", "pp": "66", "mmmm": "0F38", "W": "WIG", "opcode": "04", "mod": "/r", "evex": "1"}
}

VPMULHRSW = {
    "xmmxmmxmm": {"vvvv": "NDS", "L": "128", "pp": "66", "mmmm": "0F38", "W": "WIG", "opcode": "0B", "mod": "/r", "evex": "1"},
    "xmmxmmmem128": {"vvvv": "NDS", "L": "128", "pp": "66", "mmmm": "0F38", "W": "WIG", "opcode": "0B", "mod": "/r", "evex": "1"},
    "ymmymmymm": {"vvvv": "NDS", "L": "256", "pp": "66", "mmmm": "0F38", "W": "WIG", "opcode": "0B", "mod": "/r", "evex": "1"},
    "ymmymmmem256": {"vvvv": "NDS", "L": "256", "pp": "66", "mmmm": "0F38", "W": "WIG", "opcode": "0B", "mod": "/r", "evex": "1"},
    "zmmzmmzmm": {"vvvv": "NDS", "L": "512", "pp": "66", "mmmm": "0F38", "W": "WIG", "opcode": "0B", "mod": "/r", "evex": "1"},
    "zmmzmmmem512": {"vvvv": "NDS", "L": "512", "pp": "66", "mmmm": "0F38", "W": "WIG", "opcode": "0B", "mod": "/r", "evex": "1"}
}

VPSHUFB = {
    "xmmxmmxmm": {"vvvv": "NDS", "L": "128", "pp": "66", "mmmm": "0F38", "W": "WIG", "opcode": "00", "mod": "/r", "evex": "1"},
    "xmmxmmmem128": {"vvvv": "NDS", "L": "128", "pp": "66", "mmmm": "0F38", "W": "WIG", "opcode": "00", "mod": "/r", "evex": "1"},
    "ymmymmymm": {"vvvv": "NDS", "L": "256", "pp": "66", "mmmm": "0F38", "W": "WIG", "opcode": "00", "mod": "/r", "evex": "1"},
    "ymmymmmem256": {"vvvv": "NDS", "L": "256", "pp": "66", "mmmm": "0F38", "W": "WIG", "opcode": "00", "mod": "/r", "evex": "1"},
    "zmmzmmzmm": {"vvvv": "NDS", "L": "512", "pp": "66", "mmmm": "0F38", "W": "WIG", "opcode": "00", "mod": "/r", "evex": "1"},
    "zmmzmmmem512": {"vvvv": "NDS", "L": "512", "pp": "66", "mmmm": "0F38", "W": "WIG", "opcode": "00", "mod": "/r", "evex": "1"}
}

VPSIGNB = {
    "xmmxmmxmm": {"vvvv": "NDS", "L": "128", "pp": "66", "mmmm": "0F38", "W": "WIG", "opcode": "08", "mod": "/r"},
    "xmmxmmmem128": {"vvvv": "NDS", "L": "128", "pp": "66", "mmmm": "0F38", "W": "WIG", "opcode": "08", "mod": "/r"},
    "ymmymmymm": {"vvvv": "NDS", "L": "256", "pp": "66", "mmmm": "0F38", "W": "WIG", "opcode": "08", "mod": "/r"},
    "ymmymmmem256": {"vvvv": "NDS", "L": "256", "pp": "66", "mmmm": "0F38", "W": "WIG", "opcode": "08", "mod": "/r"},
}

VPSIGNW = {
    "xmmxmmxmm": {"vvvv": "NDS", "L": "128", "pp": "66", "mmmm": "0F38", "W": "WIG", "opcode": "09", "mod": "/r"},
    "xmmxmmmem128": {"vvvv": "NDS", "L": "128", "pp": "66", "mmmm": "0F38", "W": "WIG", "opcode": "09", "mod": "/r"},
    "ymmymmymm": {"vvvv": "NDS", "L": "256", "pp": "66", "mmmm": "0F38", "W": "WIG", "opcode": "09", "mod": "/r"},
    "ymmymmmem256": {"vvvv": "NDS", "L": "256", "pp": "66", "mmmm": "0F38", "W": "WIG", "opcode": "09", "mod": "/r"},
}

VPSIGND = {
    "xmmxmmxmm": {"vvvv": "NDS", "L": "128", "pp": "66", "mmmm": "0F38", "W": "WIG", "opcode": "0A", "mod": "/r"},
    "xmmxmmmem128": {"vvvv": "NDS", "L": "128", "pp": "66", "mmmm": "0F38", "W": "WIG", "opcode": "0A", "mod": "/r"},
    "ymmymmymm": {"vvvv": "NDS", "L": "256", "pp": "66", "mmmm": "0F38", "W": "WIG", "opcode": "0A", "mod": "/r"},
    "ymmymmmem256": {"vvvv": "NDS", "L": "256", "pp": "66", "mmmm": "0F38", "W": "WIG", "opcode": "0A", "mod": "/r"},
}

VPALIGNR = {
    "xmmxmmxmmimm8": {"vvvv": "NDS", "L": "128", "pp": "66", "mmmm": "0F3A", "W": "WIG", "opcode": "0F", "mod": "/r", "imm": "ib", "evex": "1"},
    "xmmxmmmem128imm8": {"vvvv": "NDS", "L": "128", "pp": "66", "mmmm": "0F3A", "W": "WIG", "opcode": "0F", "mod": "/r", "imm": "ib", "evex": "1"},
    "ymmymmymmimm8": {"vvvv": "NDS", "L": "256", "pp": "66", "mmmm": "0F3A", "W": "WIG", "opcode": "0F", "mod": "/r", "imm": "ib", "evex": "1"},
    "ymmymmmem256imm8": {"vvvv": "NDS", "L": "256", "pp": "66", "mmmm": "0F3A", "W": "WIG", "opcode": "0F", "mod": "/r", "imm": "ib", "evex": "1"},
    "zmmzmmzmmimm8": {"vvvv": "NDS", "L": "512", "pp": "66", "mmmm": "0F3A", "W": "WIG", "opcode": "0F", "mod": "/r", "imm": "ib", "evex": "1"},
    "zmmzmmmem512imm8": {"vvvv": "NDS", "L": "512", "pp": "66", "mmmm": "0F3A", "W": "WIG", "opcode": "0F", "mod": "/r", "imm": "ib", "evex": "1"}
}

# AVX SSE41 Instructions

VPMULLD = {
    "xmmxmmxmm": {"vvvv": "NDS", "L": "128", "pp": "66", "mmmm": "0F38", "W": "WIG", "W512": "W0", "opcode": "40", "mod": "/r", "evex": "1"},
    "xmmxmmmem128": {"vvvv": "NDS", "L": "128", "pp": "66", "mmmm": "0F38", "W": "WIG", "W512": "W0", "opcode": "40", "mod": "/r", "evex": "1"},
    "ymmymmymm": {"vvvv": "NDS", "L": "256", "pp": "66", "mmmm": "0F38", "W": "WIG", "W512": "W0", "opcode": "40", "mod": "/r", "evex": "1"},
    "ymmymmmem256": {"vvvv": "NDS", "L": "256", "pp": "66", "mmmm": "0F38", "W": "WIG", "W512": "W0", "opcode": "40", "mod": "/r", "evex": "1"},
    "zmmzmmzmm": {"vvvv": "NDS", "L": "512", "pp": "66", "mmmm": "0F38", "W": "WIG", "W512": "W0", "opcode": "40", "mod": "/r", "evex": "1"},
    "zmmzmmmem512": {"vvvv": "NDS", "L": "512", "pp": "66", "mmmm": "0F38", "W": "WIG", "W512": "W0", "opcode": "40", "mod": "/r", "evex": "1"},

    "xmmxmmmem32": {"vvvv": "NDS", "L": "128", "pp": "66", "mmmm": "0F38", "W": "WIG", "W512": "W0", "opcode": "40", "mod": "/r", "mbr": "1", "evex": "1"},
    "ymmymmmem32": {"vvvv": "NDS", "L": "256", "pp": "66", "mmmm": "0F38", "W": "WIG", "W512": "W0", "opcode": "40", "mod": "/r", "mbr": "1", "evex": "1"},
    "zmmzmmmem32": {"vvvv": "NDS", "L": "512", "pp": "66", "mmmm": "0F38", "W": "WIG", "W512": "W0", "opcode": "40", "mod": "/r", "mbr": "1", "evex": "1"}
}

VPMULDQ = {
    "xmmxmmxmm": {"vvvv": "NDS", "L": "128", "pp": "66", "mmmm": "0F38", "W": "WIG", "W512": "W1", "opcode": "28", "mod": "/r", "evex": "1"},
    "xmmxmmmem128": {"vvvv": "NDS", "L": "128", "pp": "66", "mmmm": "0F38", "W": "WIG", "W512": "W1", "opcode": "28", "mod": "/r", "evex": "1"},
    "ymmymmymm": {"vvvv": "NDS", "L": "256", "pp": "66", "mmmm": "0F38", "W": "WIG", "W512": "W1", "opcode": "28", "mod": "/r", "evex": "1"},
    "ymmymmmem256": {"vvvv": "NDS", "L": "256", "pp": "66", "mmmm": "0F38", "W": "WIG", "W512": "W1", "opcode": "28", "mod": "/r", "evex": "1"},
    "zmmzmmzmm": {"vvvv": "NDS", "L": "512", "pp": "66", "mmmm": "0F38", "W": "WIG", "W512": "W1", "opcode": "28", "mod": "/r", "evex": "1"},
    "zmmzmmmem512": {"vvvv": "NDS", "L": "512", "pp": "66", "mmmm": "0F38", "W": "WIG", "W512": "W1", "opcode": "28", "mod": "/r", "evex": "1"},

    "xmmxmmmem64": {"vvvv": "NDS", "L": "128", "pp": "66", "mmmm": "0F38", "W": "WIG", "W512": "W1", "opcode": "28", "mod": "/r", "mbr": "1", "evex": "1"},
    "ymmymmmem64": {"vvvv": "NDS", "L": "256", "pp": "66", "mmmm": "0F38", "W": "WIG", "W512": "W1", "opcode": "28", "mod": "/r", "mbr": "1", "evex": "1"},
    "zmmzmmmem64": {"vvvv": "NDS", "L": "512", "pp": "66", "mmmm": "0F38", "W": "WIG", "W512": "W1", "opcode": "28", "mod": "/r", "mbr": "1", "evex": "1"}
}

VDPPD = {
    "xmmxmmxmmimm8": {"vvvv": "NDS", "L": "128", "pp": "66", "mmmm": "0F3A", "W": "WIG", "opcode": "41", "mod": "/r", "imm": "ib"},
    "xmmxmmmem128imm8": {"vvvv": "NDS", "L": "128", "pp": "66", "mmmm": "0F3A", "W": "WIG", "opcode": "41", "mod": "/r", "imm": "ib"},
}

VDPPS = {
    "xmmxmmxmmimm8": {"vvvv": "NDS", "L": "128", "pp": "66", "mmmm": "0F3A", "W": "WIG", "opcode": "40", "mod": "/r", "imm": "ib"},
    "xmmxmmmem128imm8": {"vvvv": "NDS", "L": "128", "pp": "66", "mmmm": "0F3A", "W": "WIG", "opcode": "40", "mod": "/r", "imm": "ib"},
    "ymmymmymmimm8": {"vvvv": "NDS", "L": "256", "pp": "66", "mmmm": "0F3A", "W": "WIG", "opcode": "40", "mod": "/r", "imm": "ib"},
    "ymmymmmem256imm8": {"vvvv": "NDS", "L": "256", "pp": "66", "mmmm": "0F3A", "W": "WIG", "opcode": "40", "mod": "/r", "imm": "ib"},
}

VMOVNTDQA = {
    "xmmmem128": {"L": "128", "pp": "66", "mmmm": "0F38", "W": "WIG", "W512": "W0", "opcode": "2A", "mod": "/r", "evex": "1"},
    "ymmmem256": {"L": "256", "pp": "66", "mmmm": "0F38", "W": "WIG", "W512": "W0", "opcode": "2A", "mod": "/r", "evex": "1"},
    "zmmmem512": {"L": "256", "pp": "66", "mmmm": "0F38", "W": "WIG", "W512": "W0", "opcode": "2A", "mod": "/r", "evex": "1"}
}

VBLENDPD = {
    "xmmxmmxmmimm8": {"vvvv": "NDS", "L": "128", "pp": "66", "mmmm": "0F3A", "W": "WIG", "opcode": "0D", "mod": "/r", "imm": "ib"},
    "xmmxmmmem128imm8": {"vvvv": "NDS", "L": "128", "pp": "66", "mmmm": "0F3A", "W": "WIG", "opcode": "0D", "mod": "/r", "imm": "ib"},
    "ymmymmymmimm8": {"vvvv": "NDS", "L": "256", "pp": "66", "mmmm": "0F3A", "W": "WIG", "opcode": "0D", "mod": "/r", "imm": "ib"},
    "ymmymmmem256imm8": {"vvvv": "NDS", "L": "256", "pp": "66", "mmmm": "0F3A", "W": "WIG", "opcode": "0D", "mod": "/r", "imm": "ib"},
}

VBLENDPS = {
    "xmmxmmxmmimm8": {"vvvv": "NDS", "L": "128", "pp": "66", "mmmm": "0F3A", "W": "WIG", "opcode": "0C", "mod": "/r", "imm": "ib"},
    "xmmxmmmem128imm8": {"vvvv": "NDS", "L": "128", "pp": "66", "mmmm": "0F3A", "W": "WIG", "opcode": "0C", "mod": "/r", "imm": "ib"},
    "ymmymmymmimm8": {"vvvv": "NDS", "L": "256", "pp": "66", "mmmm": "0F3A", "W": "WIG", "opcode": "0C", "mod": "/r", "imm": "ib"},
    "ymmymmmem256imm8": {"vvvv": "NDS", "L": "256", "pp": "66", "mmmm": "0F3A", "W": "WIG", "opcode": "0C", "mod": "/r", "imm": "ib"},
}

VBLENDVPD = {
    "xmmxmmxmmxmm": {"vvvv": "NDS", "L": "128", "pp": "66", "mmmm": "0F3A", "W": "W0", "opcode": "4B", "mod": "/r", "is4": "True"},
    "xmmxmmmem128xmm": {"vvvv": "NDS", "L": "128", "pp": "66", "mmmm": "0F3A", "W": "W0", "opcode": "4B", "mod": "/r", "is4": "True"},
    "ymmymmymmymm": {"vvvv": "NDS", "L": "256", "pp": "66", "mmmm": "0F3A", "W": "W0", "opcode": "4B", "mod": "/r", "is4": "True"},
    "ymmymmmem256ymm": {"vvvv": "NDS", "L": "256", "pp": "66", "mmmm": "0F3A", "W": "W0", "opcode": "4B", "mod": "/r", "is4": "True"},
}

VBLENDVPS = {
    "xmmxmmxmmxmm": {"vvvv": "NDS", "L": "128", "pp": "66", "mmmm": "0F3A", "W": "W0", "opcode": "4A", "mod": "/r", "is4": "True"},
    "xmmxmmmem128xmm": {"vvvv": "NDS", "L": "128", "pp": "66", "mmmm": "0F3A", "W": "W0", "opcode": "4A", "mod": "/r", "is4": "True"},
    "ymmymmymmymm": {"vvvv": "NDS", "L": "256", "pp": "66", "mmmm": "0F3A", "W": "W0", "opcode": "4A", "mod": "/r", "is4": "True"},
    "ymmymmmem256ymm": {"vvvv": "NDS", "L": "256", "pp": "66", "mmmm": "0F3A", "W": "W0", "opcode": "4A", "mod": "/r", "is4": "True"},
}

VPBLENDVB = {
    "xmmxmmxmmxmm": {"vvvv": "NDS", "L": "128", "pp": "66", "mmmm": "0F3A", "W": "W0", "opcode": "4C", "mod": "/r", "is4": "True"},
    "xmmxmmmem128xmm": {"vvvv": "NDS", "L": "128", "pp": "66", "mmmm": "0F3A", "W": "W0", "opcode": "4C", "mod": "/r", "is4": "True"},
    "ymmymmymmymm": {"vvvv": "NDS", "L": "256", "pp": "66", "mmmm": "0F3A", "W": "W0", "opcode": "4C", "mod": "/r", "is4": "True"},
    "ymmymmmem256ymm": {"vvvv": "NDS", "L": "256", "pp": "66", "mmmm": "0F3A", "W": "W0", "opcode": "4C", "mod": "/r", "is4": "True"},
}

VPBLENDW = {
    "xmmxmmxmmimm8": {"vvvv": "NDS", "L": "128", "pp": "66", "mmmm": "0F3A", "W": "WIG", "opcode": "0E", "mod": "/r", "imm": "ib"},
    "xmmxmmmem128imm8": {"vvvv": "NDS", "L": "128", "pp": "66", "mmmm": "0F3A", "W": "WIG", "opcode": "0E", "mod": "/r", "imm": "ib"},
    "ymmymmymmimm8": {"vvvv": "NDS", "L": "256", "pp": "66", "mmmm": "0F3A", "W": "WIG", "opcode": "0E", "mod": "/r", "imm": "ib"},
    "ymmymmmem256imm8": {"vvvv": "NDS", "L": "256", "pp": "66", "mmmm": "0F3A", "W": "WIG", "opcode": "0E", "mod": "/r", "imm": "ib"},
}

VPMINUW = {
    "xmmxmmxmm": {"vvvv": "NDS", "L": "128", "pp": "66", "mmmm": "0F38", "W": "WIG", "opcode": "3A", "mod": "/r", "evex": "1"},
    "xmmxmmmem128": {"vvvv": "NDS", "L": "128", "pp": "66", "mmmm": "0F38", "W": "WIG", "opcode": "3A", "mod": "/r", "evex": "1"},
    "ymmymmymm": {"vvvv": "NDS", "L": "256", "pp": "66", "mmmm": "0F38", "W": "WIG", "opcode": "3A", "mod": "/r", "evex": "1"},
    "ymmymmmem256": {"vvvv": "NDS", "L": "256", "pp": "66", "mmmm": "0F38", "W": "WIG", "opcode": "3A", "mod": "/r", "evex": "1"},
    "zmmzmmzmm": {"vvvv": "NDS", "L": "512", "pp": "66", "mmmm": "0F38", "W": "WIG", "opcode": "3A", "mod": "/r", "evex": "1"},
    "zmmzmmmem512": {"vvvv": "NDS", "L": "512", "pp": "66", "mmmm": "0F38", "W": "WIG", "opcode": "3A", "mod": "/r", "evex": "1"}
}

VPMINUD = {
    "xmmxmmxmm": {"vvvv": "NDS", "L": "128", "pp": "66", "mmmm": "0F38", "W": "WIG", "W512": "W0", "opcode": "3B", "mod": "/r", "evex": "1"},
    "xmmxmmmem128": {"vvvv": "NDS", "L": "128", "pp": "66", "mmmm": "0F38", "W": "WIG", "W512": "W0", "opcode": "3B", "mod": "/r", "evex": "1"},
    "ymmymmymm": {"vvvv": "NDS", "L": "256", "pp": "66", "mmmm": "0F38", "W": "WIG", "W512": "W0", "opcode": "3B", "mod": "/r", "evex": "1"},
    "ymmymmmem256": {"vvvv": "NDS", "L": "256", "pp": "66", "mmmm": "0F38", "W": "WIG", "W512": "W0", "opcode": "3B", "mod": "/r", "evex": "1"},
    "zmmzmmzmm": {"vvvv": "NDS", "L": "512", "pp": "66", "mmmm": "0F38", "W": "WIG", "W512": "W0", "opcode": "3B", "mod": "/r", "evex": "1"},
    "zmmzmmmem512": {"vvvv": "NDS", "L": "512", "pp": "66", "mmmm": "0F38", "W": "WIG", "W512": "W0", "opcode": "3B", "mod": "/r", "evex": "1"},

    "xmmxmmmem32": {"vvvv": "NDS", "L": "128", "pp": "66", "mmmm": "0F38", "W": "WIG", "W512": "W0", "opcode": "3B", "mod": "/r", "mbr": "1", "evex": "1"},
    "ymmymmmem32": {"vvvv": "NDS", "L": "256", "pp": "66", "mmmm": "0F38", "W": "WIG", "W512": "W0", "opcode": "3B", "mod": "/r", "mbr": "1", "evex": "1"},
    "zmmzmmmem32": {"vvvv": "NDS", "L": "512", "pp": "66", "mmmm": "0F38", "W": "WIG", "W512": "W0", "opcode": "3B", "mod": "/r", "mbr": "1", "evex": "1"}
}

VPMINSB = {
    "xmmxmmxmm": {"vvvv": "NDS", "L": "128", "pp": "66", "mmmm": "0F38", "W": "WIG", "opcode": "38", "mod": "/r", "evex": "1"},
    "xmmxmmmem128": {"vvvv": "NDS", "L": "128", "pp": "66", "mmmm": "0F38", "W": "WIG", "opcode": "38", "mod": "/r", "evex": "1"},
    "ymmymmymm": {"vvvv": "NDS", "L": "256", "pp": "66", "mmmm": "0F38", "W": "WIG", "opcode": "38", "mod": "/r", "evex": "1"},
    "ymmymmmem256": {"vvvv": "NDS", "L": "256", "pp": "66", "mmmm": "0F38", "W": "WIG", "opcode": "38", "mod": "/r", "evex": "1"},
    "zmmzmmzmm": {"vvvv": "NDS", "L": "512", "pp": "66", "mmmm": "0F38", "W": "WIG", "opcode": "38", "mod": "/r", "evex": "1"},
    "zmmzmmmem512": {"vvvv": "NDS", "L": "512", "pp": "66", "mmmm": "0F38", "W": "WIG", "opcode": "38", "mod": "/r", "evex": "1"}
}

VPMINSD = {
    "xmmxmmxmm": {"vvvv": "NDS", "L": "128", "pp": "66", "mmmm": "0F38", "W": "WIG", "W512": "W0", "opcode": "39", "mod": "/r", "evex": "1"},
    "xmmxmmmem128": {"vvvv": "NDS", "L": "128", "pp": "66", "mmmm": "0F38", "W": "WIG", "W512": "W0", "opcode": "39", "mod": "/r", "evex": "1"},
    "ymmymmymm": {"vvvv": "NDS", "L": "256", "pp": "66", "mmmm": "0F38", "W": "WIG", "W512": "W0", "opcode": "39", "mod": "/r", "evex": "1"},
    "ymmymmmem256": {"vvvv": "NDS", "L": "256", "pp": "66", "mmmm": "0F38", "W": "WIG", "W512": "W0", "opcode": "39", "mod": "/r", "evex": "1"},
    "zmmzmmzmm": {"vvvv": "NDS", "L": "512", "pp": "66", "mmmm": "0F38", "W": "WIG", "W512": "W0", "opcode": "39", "mod": "/r", "evex": "1"},
    "zmmzmmmem512": {"vvvv": "NDS", "L": "512", "pp": "66", "mmmm": "0F38", "W": "WIG", "W512": "W0", "opcode": "39", "mod": "/r", "evex": "1"},

    "xmmxmmmem32": {"vvvv": "NDS", "L": "128", "pp": "66", "mmmm": "0F38", "W": "WIG", "W512": "W0", "opcode": "39", "mod": "/r", "mbr": "1", "evex": "1"},
    "ymmymmmem32": {"vvvv": "NDS", "L": "256", "pp": "66", "mmmm": "0F38", "W": "WIG", "W512": "W0", "opcode": "39", "mod": "/r", "mbr": "1", "evex": "1"},
    "zmmzmmmem32": {"vvvv": "NDS", "L": "512", "pp": "66", "mmmm": "0F38", "W": "WIG", "W512": "W0", "opcode": "39", "mod": "/r", "mbr": "1", "evex": "1"}
}

VPMAXUW = {
    "xmmxmmxmm": {"vvvv": "NDS", "L": "128", "pp": "66", "mmmm": "0F38", "W": "WIG", "opcode": "3E", "mod": "/r", "evex": "1"},
    "xmmxmmmem128": {"vvvv": "NDS", "L": "128", "pp": "66", "mmmm": "0F38", "W": "WIG", "opcode": "3E", "mod": "/r", "evex": "1"},
    "ymmymmymm": {"vvvv": "NDS", "L": "256", "pp": "66", "mmmm": "0F38", "W": "WIG", "opcode": "3E", "mod": "/r", "evex": "1"},
    "ymmymmmem256": {"vvvv": "NDS", "L": "256", "pp": "66", "mmmm": "0F38", "W": "WIG", "opcode": "3E", "mod": "/r", "evex": "1"},
    "zmmzmmzmm": {"vvvv": "NDS", "L": "512", "pp": "66", "mmmm": "0F38", "W": "WIG", "opcode": "3E", "mod": "/r", "evex": "1"},
    "zmmzmmmem512": {"vvvv": "NDS", "L": "512", "pp": "66", "mmmm": "0F38", "W": "WIG", "opcode": "3E", "mod": "/r", "evex": "1"}
}

VPMAXUD = {
    "xmmxmmxmm": {"vvvv": "NDS", "L": "128", "pp": "66", "mmmm": "0F38", "W": "WIG", "W512": "W0", "opcode": "3F", "mod": "/r", "evex": "1"},
    "xmmxmmmem128": {"vvvv": "NDS", "L": "128", "pp": "66", "mmmm": "0F38", "W": "WIG", "W512": "W0", "opcode": "3F", "mod": "/r", "evex": "1"},
    "ymmymmymm": {"vvvv": "NDS", "L": "256", "pp": "66", "mmmm": "0F38", "W": "WIG", "W512": "W0", "opcode": "3F", "mod": "/r", "evex": "1"},
    "ymmymmmem256": {"vvvv": "NDS", "L": "256", "pp": "66", "mmmm": "0F38", "W": "WIG", "W512": "W0", "opcode": "3F", "mod": "/r", "evex": "1"},
    "zmmzmmzmm": {"vvvv": "NDS", "L": "512", "pp": "66", "mmmm": "0F38", "W": "WIG", "W512": "W0", "opcode": "3F", "mod": "/r", "evex": "1"},
    "zmmzmmmem512": {"vvvv": "NDS", "L": "512", "pp": "66", "mmmm": "0F38", "W": "WIG", "W512": "W0", "opcode": "3F", "mod": "/r", "evex": "1"},

    "xmmxmmmem32": {"vvvv": "NDS", "L": "128", "pp": "66", "mmmm": "0F38", "W": "WIG", "W512": "W0", "opcode": "3F", "mod": "/r", "mbr": "1", "evex": "1"},
    "ymmymmmem32": {"vvvv": "NDS", "L": "256", "pp": "66", "mmmm": "0F38", "W": "WIG", "W512": "W0", "opcode": "3F", "mod": "/r", "mbr": "1", "evex": "1"},
    "zmmzmmmem32": {"vvvv": "NDS", "L": "512", "pp": "66", "mmmm": "0F38", "W": "WIG", "W512": "W0", "opcode": "3F", "mod": "/r", "mbr": "1", "evex": "1"}
}

VPMAXSB = {
    "xmmxmmxmm": {"vvvv": "NDS", "L": "128", "pp": "66", "mmmm": "0F38", "W": "WIG", "opcode": "3C", "mod": "/r", "evex":"1"},
    "xmmxmmmem128": {"vvvv": "NDS", "L": "128", "pp": "66", "mmmm": "0F38", "W": "WIG", "opcode": "3C", "mod": "/r", "evex": "1"},
    "ymmymmymm": {"vvvv": "NDS", "L": "256", "pp": "66", "mmmm": "0F38", "W": "WIG", "opcode": "3C", "mod": "/r", "evex": "1"},
    "ymmymmmem256": {"vvvv": "NDS", "L": "256", "pp": "66", "mmmm": "0F38", "W": "WIG", "opcode": "3C", "mod": "/r", "evex": "1"},
    "zmmzmmzmm": {"vvvv": "NDS", "L": "512", "pp": "66", "mmmm": "0F38", "W": "WIG", "opcode": "3C", "mod": "/r", "evex": "1"},
    "zmmzmmmem512": {"vvvv": "NDS", "L": "512", "pp": "66", "mmmm": "0F38", "W": "WIG", "opcode": "3C", "mod": "/r", "evex": "1"}
}

VPMAXSD = {
    "xmmxmmxmm": {"vvvv": "NDS", "L": "128", "pp": "66", "mmmm": "0F38", "W": "WIG", "W512": "W0", "opcode": "3D", "mod": "/r", "evex": "1"},
    "xmmxmmmem128": {"vvvv": "NDS", "L": "128", "pp": "66", "mmmm": "0F38", "W": "WIG", "W512": "W0", "opcode": "3D", "mod": "/r", "evex": "1"},
    "ymmymmymm": {"vvvv": "NDS", "L": "256", "pp": "66", "mmmm": "0F38", "W": "WIG", "W512": "W0", "opcode": "3D", "mod": "/r", "evex": "1"},
    "ymmymmmem256": {"vvvv": "NDS", "L": "256", "pp": "66", "mmmm": "0F38", "W": "WIG", "W512": "W0", "opcode": "3D", "mod": "/r", "evex": "1"},
    "zmmzmmzmm": {"vvvv": "NDS", "L": "512", "pp": "66", "mmmm": "0F38", "W": "WIG", "W512": "W0", "opcode": "3D", "mod": "/r", "evex": "1"},
    "zmmzmmmem512": {"vvvv": "NDS", "L": "512", "pp": "66", "mmmm": "0F38", "W": "WIG", "W512": "W0", "opcode": "3D", "mod": "/r", "evex": "1"},

    "xmmxmmmem32": {"vvvv": "NDS", "L": "128", "pp": "66", "mmmm": "0F38", "W": "WIG", "W512": "W0", "opcode": "3D", "mod": "/r", "mbr": "1", "evex": "1"},
    "ymmymmmem32": {"vvvv": "NDS", "L": "256", "pp": "66", "mmmm": "0F38", "W": "WIG", "W512": "W0", "opcode": "3D", "mod": "/r", "mbr": "1", "evex": "1"},
    "zmmzmmmem32": {"vvvv": "NDS", "L": "512", "pp": "66", "mmmm": "0F38", "W": "WIG", "W512": "W0", "opcode": "3D", "mod": "/r", "mbr": "1", "evex": "1"}
}

VROUNDPS = {
    "xmmxmmimm8": {"L": "128", "pp": "66", "mmmm": "0F3A", "W": "WIG", "opcode": "08", "mod": "/r", "imm": "ib"},
    "xmmmem128imm8": {"L": "128", "pp": "66", "mmmm": "0F3A", "W": "WIG", "opcode": "08", "mod": "/r", "imm": "ib"},
    "ymmymmimm8": {"L": "256", "pp": "66", "mmmm": "0F3A", "W": "WIG", "opcode": "08", "mod": "/r", "imm": "ib"},
    "ymmmem256imm8": {"L": "256", "pp": "66", "mmmm": "0F3A", "W": "WIG", "opcode": "08", "mod": "/r", "imm": "ib"},
}

VROUNDPD = {
    "xmmxmmimm8": {"L": "128", "pp": "66", "mmmm": "0F3A", "W": "WIG", "opcode": "09", "mod": "/r", "imm": "ib"},
    "xmmmem128imm8": {"L": "128", "pp": "66", "mmmm": "0F3A", "W": "WIG", "opcode": "09", "mod": "/r", "imm": "ib"},
    "ymmymmimm8": {"L": "256", "pp": "66", "mmmm": "0F3A", "W": "WIG", "opcode": "09", "mod": "/r", "imm": "ib"},
    "ymmmem256imm8": {"L": "256", "pp": "66", "mmmm": "0F3A", "W": "WIG", "opcode": "09", "mod": "/r", "imm": "ib"},
}

VROUNDSS = {
    "xmmxmmxmmimm8": {"vvvv": "NDS", "L": "LIG", "pp": "66", "mmmm": "0F3A", "W": "WIG", "opcode": "0A", "mod": "/r", "imm": "ib"},
    "xmmxmmmem32imm8": {"vvvv": "NDS", "L": "LIG", "pp": "66", "mmmm": "0F3A", "W": "WIG", "opcode": "0A", "mod": "/r", "imm": "ib"},
}

VROUNDSD = {
    "xmmxmmxmmimm8": {"vvvv": "NDS", "L": "LIG", "pp": "66", "mmmm": "0F3A", "W": "WIG", "opcode": "0B", "mod": "/r", "imm": "ib"},
    "xmmxmmmem64imm8": {"vvvv": "NDS", "L": "LIG", "pp": "66", "mmmm": "0F3A", "W": "WIG", "opcode": "0B", "mod": "/r", "imm": "ib"},
}

VEXTRACTPS = {
    "r32xmmimm8": {"L": "128", "pp": "66", "mmmm": "0F3A", "W": "WIG", "opcode": "17", "mod": "/r", "imm": "ib", "evex": "1"},
    "r64xmmimm8": {"L": "128", "pp": "66", "mmmm": "0F3A", "W": "WIG", "opcode": "17", "mod": "/r", "imm": "ib", "evex": "1"},
    "mem32xmmimm8": {"L": "128", "pp": "66", "mmmm": "0F3A", "W": "WIG", "opcode": "17", "mod": "/r", "imm": "ib", "evex": "1"}
}

VINSERTPS = {
    "xmmxmmxmmimm8": {"vvvv": "NDS", "L": "128", "pp": "66", "mmmm": "0F3A", "W": "WIG", "W512": "W0", "opcode": "21", "mod": "/r", "imm": "ib", "evex": "1"},
    "xmmxmmmem32imm8": {"vvvv": "NDS", "L": "128", "pp": "66", "mmmm": "0F3A", "W": "WIG", "W512": "W0", "opcode": "21", "mod": "/r", "imm": "ib", "evex": "1"},
}

VPINSRB = {
    "xmmxmmr32imm8": {"vvvv": "NDS", "L": "128", "pp": "66", "mmmm": "0F3A", "W": "W0", "W512": "WIG", "opcode": "20", "mod": "/r", "imm": "ib", "evex": "1"},
    "xmmxmmmem8imm8": {"vvvv": "NDS", "L": "128", "pp": "66", "mmmm": "0F3A", "W": "W0", "W512": "WIG", "opcode": "20", "mod": "/r", "imm": "ib", "evex": "1"}
}

VPINSRD = {
    "xmmxmmr32imm8": {"vvvv": "NDS", "L": "128", "pp": "66", "mmmm": "0F3A", "W": "W0", "opcode": "22", "mod": "/r", "imm": "ib", "evex": "1"},
    "xmmxmmmem32imm8": {"vvvv": "NDS", "L": "128", "pp": "66", "mmmm": "0F3A", "W": "W0", "opcode": "22", "mod": "/r", "imm": "ib", "evex": "1"}
}

VPINSRQ = {
    "xmmxmmr64imm8": {"vvvv": "NDS", "L": "128", "pp": "66", "mmmm": "0F3A", "W": "W1", "opcode": "22", "mod": "/r", "imm": "ib", "evex": "1"},
    "xmmxmmmem64imm8": {"vvvv": "NDS", "L": "128", "pp": "66", "mmmm": "0F3A", "W": "W1", "opcode": "22", "mod": "/r", "imm": "ib", "evex": "1"}
}

VPEXTRB = {
    "r32xmmimm8": {"L": "128", "pp": "66", "mmmm": "0F3A", "W": "W0", "W512": "WIG", "opcode": "14", "mod": "/r", "imm": "ib", "rm": "1", "evex": "1"},
    "r64xmmimm8": {"L": "128", "pp": "66", "mmmm": "0F3A", "W": "W0", "W512": "WIG", "opcode": "14", "mod": "/r", "imm": "ib", "rm": "1", "evex": "1"},
    "mem8xmmimm8": {"L": "128", "pp": "66", "mmmm": "0F3A", "W": "W0", "W512": "WIG", "opcode": "14", "mod": "/r", "imm": "ib", "evex": "1"},
}

VPEXTRD = {
    "r32xmmimm8": {"L": "128", "pp": "66", "mmmm": "0F3A", "W": "W0", "opcode": "16", "mod": "/r", "imm": "ib", "rm": "1", "evex": "1"},
    "mem32xmmimm8": {"L": "128", "pp": "66", "mmmm": "0F3A", "W": "W0", "opcode": "16", "mod": "/r", "imm": "ib", "rm": "1", "evex": "1"}
}

VPEXTRQ = {
    "r64xmmimm8": {"L": "128", "pp": "66", "mmmm": "0F3A", "W": "W1", "opcode": "16", "mod": "/r", "imm": "ib", "rm": "1", "evex": "1"},
    "mem64xmmimm8": {"L": "128", "pp": "66", "mmmm": "0F3A", "W": "W1", "opcode": "16", "mod": "/r", "imm": "ib", "rm": "1", "evex": "1"}
}

VPMOVSXBW = {
    "xmmxmm": {"L": "128", "pp": "66", "mmmm": "0F38", "W": "WIG", "opcode": "20", "mod": "/r", "evex": "1"},
    "xmmmem64": {"L": "128", "pp": "66", "mmmm": "0F38", "W": "WIG", "opcode": "20", "mod": "/r", "evex": "1"},
    "ymmxmm": {"L": "256", "pp": "66", "mmmm": "0F38", "W": "WIG", "opcode": "20", "mod": "/r", "evex": "1"},
    "ymmmem128": {"L": "256", "pp": "66", "mmmm": "0F38", "W": "WIG", "opcode": "20", "mod": "/r", "evex": "1"},
    "zmmymm": {"L": "512", "pp": "66", "mmmm": "0F38", "W": "WIG", "opcode": "20", "mod": "/r", "evex": "1"},
    "zmmmem256": {"L": "512", "pp": "66", "mmmm": "0F38", "W": "WIG", "opcode": "20", "mod": "/r", "evex": "1"}
}

VPMOVSXBD = {
    "xmmxmm": {"L": "128", "pp": "66", "mmmm": "0F38", "W": "WIG", "opcode": "21", "mod": "/r", "evex": "1"},
    "xmmmem32": {"L": "128", "pp": "66", "mmmm": "0F38", "W": "WIG", "opcode": "21", "mod": "/r", "evex": "1"},
    "ymmxmm": {"L": "256", "pp": "66", "mmmm": "0F38", "W": "WIG", "opcode": "21", "mod": "/r", "evex": "1"},
    "ymmmem64": {"L": "256", "pp": "66", "mmmm": "0F38", "W": "WIG", "opcode": "21", "mod": "/r", "evex": "1"},
    "zmmxmm": {"L": "512", "pp": "66", "mmmm": "0F38", "W": "WIG", "opcode": "21", "mod": "/r", "evex": "1"},
    "zmmmem128": {"L": "512", "pp": "66", "mmmm": "0F38", "W": "WIG", "opcode": "21", "mod": "/r", "evex": "1"}
}

VPMOVSXBQ = {
    "xmmxmm": {"L": "128", "pp": "66", "mmmm": "0F38", "W": "WIG", "opcode": "22", "mod": "/r", "evex": "1"},
    "xmmmem16": {"L": "128", "pp": "66", "mmmm": "0F38", "W": "WIG", "opcode": "22", "mod": "/r", "evex": "1"},
    "ymmxmm": {"L": "256", "pp": "66", "mmmm": "0F38", "W": "WIG", "opcode": "22", "mod": "/r", "evex": "1"},
    "ymmmem32": {"L": "256", "pp": "66", "mmmm": "0F38", "W": "WIG", "opcode": "22", "mod": "/r", "evex": "1"},
    "zmmxmm": {"L": "512", "pp": "66", "mmmm": "0F38", "W": "WIG", "opcode": "22", "mod": "/r", "evex": "1"},
    "zmmmem64": {"L": "512", "pp": "66", "mmmm": "0F38", "W": "WIG", "opcode": "22", "mod": "/r", "evex": "1"}
}

VPMOVSXWD = {
    "xmmxmm": {"L": "128", "pp": "66", "mmmm": "0F38", "W": "WIG", "opcode": "23", "mod": "/r", "evex": "1"},
    "xmmmem64": {"L": "128", "pp": "66", "mmmm": "0F38", "W": "WIG", "opcode": "23", "mod": "/r", "evex": "1"},
    "ymmxmm": {"L": "256", "pp": "66", "mmmm": "0F38", "W": "WIG", "opcode": "23", "mod": "/r", "evex": "1"},
    "ymmmem128": {"L": "256", "pp": "66", "mmmm": "0F38", "W": "WIG", "opcode": "23", "mod": "/r", "evex": "1"},
    "zmmymm": {"L": "512", "pp": "66", "mmmm": "0F38", "W": "WIG", "opcode": "23", "mod": "/r", "evex": "1"},
    "zmmmem256": {"L": "512", "pp": "66", "mmmm": "0F38", "W": "WIG", "opcode": "23", "mod": "/r", "evex": "1"}
}

VPMOVSXWQ = {
    "xmmxmm": {"L": "128", "pp": "66", "mmmm": "0F38", "W": "WIG", "opcode": "24", "mod": "/r", "evex": "1"},
    "xmmmem32": {"L": "128", "pp": "66", "mmmm": "0F38", "W": "WIG", "opcode": "24", "mod": "/r", "evex": "1"},
    "ymmxmm": {"L": "256", "pp": "66", "mmmm": "0F38", "W": "WIG", "opcode": "24", "mod": "/r", "evex": "1"},
    "ymmmem64": {"L": "256", "pp": "66", "mmmm": "0F38", "W": "WIG", "opcode": "24", "mod": "/r", "evex": "1"},
    "zmmxmm": {"L": "512", "pp": "66", "mmmm": "0F38", "W": "WIG", "opcode": "24", "mod": "/r", "evex": "1"},
    "zmmmem128": {"L": "512", "pp": "66", "mmmm": "0F38", "W": "WIG", "opcode": "24", "mod": "/r", "evex": "1"}
}

VPMOVSXDQ = {
    "xmmxmm": {"L": "128", "pp": "66", "mmmm": "0F38", "W": "WIG", "W512": "W0", "opcode": "25", "mod": "/r", "evex": "1"},
    "xmmmem64": {"L": "128", "pp": "66", "mmmm": "0F38", "W": "WIG", "W512": "W0", "opcode": "25", "mod": "/r", "evex": "1"},
    "ymmxmm": {"L": "256", "pp": "66", "mmmm": "0F38", "W": "WIG", "W512": "W0", "opcode": "25", "mod": "/r", "evex": "1"},
    "ymmmem128": {"L": "256", "pp": "66", "mmmm": "0F38", "W": "WIG", "W512": "W0", "opcode": "25", "mod": "/r", "evex": "1"},
    "zmmymm": {"L": "512", "pp": "66", "mmmm": "0F38", "W": "WIG", "W512": "W0", "opcode": "25", "mod": "/r", "evex": "1"},
    "zmmmem256": {"L": "512", "pp": "66", "mmmm": "0F38", "W": "WIG", "W512": "W0", "opcode": "25", "mod": "/r", "evex": "1"}
}

VPMOVZXBW = {
    "xmmxmm": {"L": "128", "pp": "66", "mmmm": "0F38", "W": "WIG", "opcode": "30", "mod": "/r", "evex": "1"},
    "xmmmem64": {"L": "128", "pp": "66", "mmmm": "0F38", "W": "WIG", "opcode": "30", "mod": "/r", "evex": "1"},
    "ymmxmm": {"L": "256", "pp": "66", "mmmm": "0F38", "W": "WIG", "opcode": "30", "mod": "/r", "evex": "1"},
    "ymmmem128": {"L": "256", "pp": "66", "mmmm": "0F38", "W": "WIG", "opcode": "30", "mod": "/r", "evex": "1"},
    "zmmymm": {"L": "512", "pp": "66", "mmmm": "0F38", "W": "WIG", "opcode": "30", "mod": "/r", "evex": "1"},
    "zmmmem256": {"L": "512", "pp": "66", "mmmm": "0F38", "W": "WIG", "opcode": "30", "mod": "/r", "evex": "1"}
}

VPMOVZXBD = {
    "xmmxmm": {"L": "128", "pp": "66", "mmmm": "0F38", "W": "WIG", "opcode": "31", "mod": "/r", "evex": "1"},
    "xmmmem32": {"L": "128", "pp": "66", "mmmm": "0F38", "W": "WIG", "opcode": "31", "mod": "/r", "evex": "1"},
    "ymmxmm": {"L": "256", "pp": "66", "mmmm": "0F38", "W": "WIG", "opcode": "31", "mod": "/r", "evex": "1"},
    "ymmmem64": {"L": "256", "pp": "66", "mmmm": "0F38", "W": "WIG", "opcode": "31", "mod": "/r", "evex": "1"},
    "zmmxmm": {"L": "512", "pp": "66", "mmmm": "0F38", "W": "WIG", "opcode": "31", "mod": "/r", "evex": "1"},
    "zmmmem128": {"L": "512", "pp": "66", "mmmm": "0F38", "W": "WIG", "opcode": "31", "mod": "/r", "evex": "1"}
}

VPMOVZXBQ = {
    "xmmxmm": {"L": "128", "pp": "66", "mmmm": "0F38", "W": "WIG", "opcode": "32", "mod": "/r", "evex": "1"},
    "xmmmem16": {"L": "128", "pp": "66", "mmmm": "0F38", "W": "WIG", "opcode": "32", "mod": "/r", "evex": "1"},
    "ymmxmm": {"L": "256", "pp": "66", "mmmm": "0F38", "W": "WIG", "opcode": "32", "mod": "/r", "evex": "1"},
    "ymmmem32": {"L": "256", "pp": "66", "mmmm": "0F38", "W": "WIG", "opcode": "32", "mod": "/r", "evex": "1"},
    "zmmxmm": {"L": "256", "pp": "66", "mmmm": "0F38", "W": "WIG", "opcode": "32", "mod": "/r", "evex": "1"},
    "zmmmem64": {"L": "256", "pp": "66", "mmmm": "0F38", "W": "WIG", "opcode": "32", "mod": "/r", "evex": "1"},
}

VPMOVZXWD = {
    "xmmxmm": {"L": "128", "pp": "66", "mmmm": "0F38", "W": "WIG", "opcode": "33", "mod": "/r", "evex": "1"},
    "xmmmem64": {"L": "128", "pp": "66", "mmmm": "0F38", "W": "WIG", "opcode": "33", "mod": "/r", "evex": "1"},
    "ymmxmm": {"L": "256", "pp": "66", "mmmm": "0F38", "W": "WIG", "opcode": "33", "mod": "/r", "evex": "1"},
    "ymmmem128": {"L": "256", "pp": "66", "mmmm": "0F38", "W": "WIG", "opcode": "33", "mod": "/r", "evex": "1"},
    "zmmymm": {"L": "512", "pp": "66", "mmmm": "0F38", "W": "WIG", "opcode": "33", "mod": "/r", "evex": "1"},
    "zmmmem256": {"L": "512", "pp": "66", "mmmm": "0F38", "W": "WIG", "opcode": "33", "mod": "/r", "evex": "1"}
}

VPMOVZXWQ = {
    "xmmxmm": {"L": "128", "pp": "66", "mmmm": "0F38", "W": "WIG", "opcode": "34", "mod": "/r", "evex": "1"},
    "xmmmem32": {"L": "128", "pp": "66", "mmmm": "0F38", "W": "WIG", "opcode": "34", "mod": "/r", "evex": "1"},
    "ymmxmm": {"L": "256", "pp": "66", "mmmm": "0F38", "W": "WIG", "opcode": "34", "mod": "/r", "evex": "1"},
    "ymmmem64": {"L": "256", "pp": "66", "mmmm": "0F38", "W": "WIG", "opcode": "34", "mod": "/r", "evex": "1"},
    "zmmymm": {"L": "512", "pp": "66", "mmmm": "0F38", "W": "WIG", "opcode": "34", "mod": "/r", "evex": "1"},
    "zmmmem128": {"L": "512", "pp": "66", "mmmm": "0F38", "W": "WIG", "opcode": "34", "mod": "/r", "evex": "1"}
}

VPMOVZXDQ = {
    "xmmxmm": {"L": "128", "pp": "66", "mmmm": "0F38", "W": "WIG", "opcode": "35", "mod": "/r", "evex": "1"},
    "xmmmem64": {"L": "128", "pp": "66", "mmmm": "0F38", "W": "WIG", "opcode": "35", "mod": "/r", "evex": "1"},
    "ymmxmm": {"L": "256", "pp": "66", "mmmm": "0F38", "W": "WIG", "opcode": "35", "mod": "/r", "evex": "1"},
    "ymmmem128": {"L": "256", "pp": "66", "mmmm": "0F38", "W": "WIG", "opcode": "35", "mod": "/r", "evex": "1"},
    "zmmymm": {"L": "512", "pp": "66", "mmmm": "0F38", "W": "WIG", "opcode": "35", "mod": "/r", "evex": "1"},
    "zmmmem256": {"L": "512", "pp": "66", "mmmm": "0F38", "W": "WIG", "opcode": "35", "mod": "/r", "evex": "1"}
}

VMPSADBW = {
    "xmmxmmxmmimm8": {"vvvv": "NDS", "L": "128", "pp": "66", "mmmm": "0F3A", "W": "WIG", "opcode": "42", "mod": "/r", "imm": "ib"},
    "xmmxmmmem128imm8": {"vvvv": "NDS", "L": "128", "pp": "66", "mmmm": "0F3A", "W": "WIG", "opcode": "42", "mod": "/r", "imm": "ib"},
    "ymmymmymmimm8": {"vvvv": "NDS", "L": "256", "pp": "66", "mmmm": "0F3A", "W": "WIG", "opcode": "42", "mod": "/r", "imm": "ib"},
    "ymmymmmem256imm8": {"vvvv": "NDS", "L": "256", "pp": "66", "mmmm": "0F3A", "W": "WIG", "opcode": "42", "mod": "/r", "imm": "ib"},
}

VPHMINPOSUW = {
    "xmmxmm": {"L": "128", "pp": "66", "mmmm": "0F38", "W": "WIG", "opcode": "41", "mod": "/r"},
    "xmmmem128": {"L": "128", "pp": "66", "mmmm": "0F38", "W": "WIG", "opcode": "41", "mod": "/r"},
}

VPTEST = {
    "xmmxmm": {"L": "128", "pp": "66", "mmmm": "0F38", "W": "WIG", "opcode": "17", "mod": "/r"},
    "xmmmem128": {"L": "128", "pp": "66", "mmmm": "0F38", "W": "WIG", "opcode": "17", "mod": "/r"},
    "ymmymm": {"L": "256", "pp": "66", "mmmm": "0F38", "W": "WIG", "opcode": "17", "mod": "/r"},
    "ymmmem256": {"L": "256", "pp": "66", "mmmm": "0F38", "W": "WIG", "opcode": "17", "mod": "/r"},
}

VPCMPEQQ = {
    "xmmxmmxmm": {"vvvv": "NDS", "L": "128", "pp": "66", "mmmm": "0F38", "W": "WIG", "opcode": "29", "mod": "/r"},
    "xmmxmmmem128": {"vvvv": "NDS", "L": "128", "pp": "66", "mmmm": "0F38", "W": "WIG", "opcode": "29", "mod": "/r"},
    "ymmymmymm": {"vvvv": "NDS", "L": "256", "pp": "66", "mmmm": "0F38", "W": "WIG", "opcode": "29", "mod": "/r"},
    "ymmymmmem256": {"vvvv": "NDS", "L": "256", "pp": "66", "mmmm": "0F38", "W": "WIG", "opcode": "29", "mod": "/r"},

    "k64xmmxmm": {"vvvv": "NDS", "L": "128", "pp": "66", "mmmm": "0F38", "W": "W1", "opcode": "29", "mod": "/r", "evex": "1"},
    "k64xmmmem128": {"vvvv": "NDS", "L": "128", "pp": "66", "mmmm": "0F38", "W": "W1", "opcode": "29", "mod": "/r", "evex": "1"},
    "k64ymmymm": {"vvvv": "NDS", "L": "256", "pp": "66", "mmmm": "0F38", "W": "W1", "opcode": "29", "mod": "/r", "evex": "1"},
    "k64ymmmem256": {"vvvv": "NDS", "L": "256", "pp": "66", "mmmm": "0F38", "W": "W1", "opcode": "29", "mod": "/r", "evex": "1"},
    "k64zmmzmm": {"vvvv": "NDS", "L": "512", "pp": "66", "mmmm": "0F38", "W": "W1", "opcode": "29", "mod": "/r", "evex": "1"},
    "k64zmmmem512": {"vvvv": "NDS", "L": "512", "pp": "66", "mmmm": "0F38", "W": "W1", "opcode": "29", "mod": "/r", "evex": "1"},

    "k64xmmmem64": {"vvvv": "NDS", "L": "128", "pp": "66", "mmmm": "0F38", "W": "W1", "opcode": "29", "mod": "/r", "mbr": "1", "evex": "1"},
    "k64ymmmem64": {"vvvv": "NDS", "L": "256", "pp": "66", "mmmm": "0F38", "W": "W1", "opcode": "29", "mod": "/r", "mbr": "1", "evex": "1"},
    "k64zmmmem64": {"vvvv": "NDS", "L": "512", "pp": "66", "mmmm": "0F38", "W": "W1", "opcode": "29", "mod": "/r", "mbr": "1", "evex": "1"}
}

VPACKUSDW = {
    "xmmxmmxmm": {"vvvv": "NDS", "L": "128", "pp": "66", "mmmm": "0F38", "W": "WIG", "W512": "W0", "opcode": "2B", "mod": "/r", "evex": "1"},
    "xmmxmmmem128": {"vvvv": "NDS", "L": "128", "pp": "66", "mmmm": "0F38", "W": "WIG", "W512": "W0", "opcode": "2B", "mod": "/r", "evex": "1"},
    "ymmymmymm": {"vvvv": "NDS", "L": "256", "pp": "66", "mmmm": "0F38", "W": "WIG", "W512": "W0", "opcode": "2B", "mod": "/r", "evex": "1"},
    "ymmymmmem256": {"vvvv": "NDS", "L": "256", "pp": "66", "mmmm": "0F38", "W": "WIG", "W512": "W0", "opcode": "2B", "mod": "/r", "evex": "1"},
    "zmmzmmzmm": {"vvvv": "NDS", "L": "512", "pp": "66", "mmmm": "0F38", "W": "WIG", "W512": "W0", "opcode": "2B", "mod": "/r", "evex": "1"},
    "zmmzmmmem256": {"vvvv": "NDS", "L": "512", "pp": "66", "mmmm": "0F38", "W": "WIG", "W512": "W0", "opcode": "2B", "mod": "/r", "evex": "1"},

    "xmmxmmmem32": {"vvvv": "NDS", "L": "128", "pp": "66", "mmmm": "0F38", "W": "WIG", "W512": "W0", "opcode": "2B", "mod": "/r", "mbr": "1", "evex": "1"},
    "ymmymmmem32": {"vvvv": "NDS", "L": "256", "pp": "66", "mmmm": "0F38", "W": "WIG", "W512": "W0", "opcode": "2B", "mod": "/r", "mbr": "1", "evex": "1"},
    "zmmzmmmem32": {"vvvv": "NDS", "L": "512", "pp": "66", "mmmm": "0F38", "W": "WIG", "W512": "W0", "opcode": "2B", "mod": "/r", "mbr": "1", "evex": "1"}
}

# AVX SSE42 Instructions

VPCMPESTRI = {
    "xmmxmmimm8": {"L": "128", "pp": "66", "mmmm": "0F3A", "W": "WIG", "opcode": "61", "mod": "/r", "imm": "ib"},
    "xmmmem128imm8": {"L": "128", "pp": "66", "mmmm": "0F3A", "W": "WIG", "opcode": "61", "mod": "/r", "imm": "ib"},
}

VPCMPESTRM = {
    "xmmxmmimm8": {"L": "128", "pp": "66", "mmmm": "0F3A", "W": "WIG", "opcode": "60", "mod": "/r", "imm": "ib"},
    "xmmmem128imm8": {"L": "128", "pp": "66", "mmmm": "0F3A", "W": "WIG", "opcode": "60", "mod": "/r", "imm": "ib"},
}

VPCMPISTRI = {
    "xmmxmmimm8": {"L": "128", "pp": "66", "mmmm": "0F3A", "W": "WIG", "opcode": "63", "mod": "/r", "imm": "ib"},
    "xmmmem128imm8": {"L": "128", "pp": "66", "mmmm": "0F3A", "W": "WIG", "opcode": "63", "mod": "/r", "imm": "ib"},
}

VPCMPISTRM = {
    "xmmxmmimm8": {"L": "128", "pp": "66", "mmmm": "0F3A", "W": "WIG", "opcode": "62", "mod": "/r", "imm": "ib"},
    "xmmmem128imm8": {"L": "128", "pp": "66", "mmmm": "0F3A", "W": "WIG", "opcode": "62", "mod": "/r", "imm": "ib"},
}

VPCMPGTQ = {
    "xmmxmmxmm": {"vvvv": "NDS", "L": "128", "pp": "66", "mmmm": "0F38", "W": "WIG", "opcode": "37", "mod": "/r"},
    "xmmxmmmem128": {"vvvv": "NDS", "L": "128", "pp": "66", "mmmm": "0F38", "W": "WIG", "opcode": "37", "mod": "/r"},
    "ymmymmymm": {"vvvv": "NDS", "L": "256", "pp": "66", "mmmm": "0F38", "W": "WIG", "opcode": "37", "mod": "/r"},
    "ymmymmmem256": {"vvvv": "NDS", "L": "256", "pp": "66", "mmmm": "0F38", "W": "WIG", "opcode": "37", "mod": "/r"},

    "k64xmmxmm": {"vvvv": "NDS", "L": "128", "pp": "66", "mmmm": "0F38", "W": "W1", "opcode": "37", "mod": "/r", "evex": "1"},
    "k64xmmmem128": {"vvvv": "NDS", "L": "128", "pp": "66", "mmmm": "0F38", "W": "W1", "opcode": "37", "mod": "/r", "evex": "1"},
    "k64ymmymm": {"vvvv": "NDS", "L": "256", "pp": "66", "mmmm": "0F38", "W": "W1", "opcode": "37", "mod": "/r", "evex": "1"},
    "k64ymmmem256": {"vvvv": "NDS", "L": "256", "pp": "66", "mmmm": "0F38", "W": "W1", "opcode": "37", "mod": "/r", "evex": "1"},
    "k64zmmzmm": {"vvvv": "NDS", "L": "512", "pp": "66", "mmmm": "0F38", "W": "W1", "opcode": "37", "mod": "/r", "evex": "1"},
    "k64zmmmem512": {"vvvv": "NDS", "L": "512", "pp": "66", "mmmm": "0F38", "W": "W1", "opcode": "37", "mod": "/r", "evex": "1"},

    "k64xmmmem64": {"vvvv": "NDS", "L": "128", "pp": "66", "mmmm": "0F38", "W": "W1", "opcode": "37", "mod": "/r", "mbr": "1", "evex": "1"},
    "k64ymmmem64": {"vvvv": "NDS", "L": "256", "pp": "66", "mmmm": "0F38", "W": "W1", "opcode": "37", "mod": "/r", "mbr": "1", "evex": "1"},
    "k64zmmmem64": {"vvvv": "NDS", "L": "512", "pp": "66", "mmmm": "0F38", "W": "W1", "opcode": "37", "mod": "/r", "mbr": "1", "evex": "1"}
}


# New AVX Instructions

VBROADCASTSS = {
    "xmmmem32": {"L": "128", "pp": "66", "mmmm": "0F38", "W": "W0", "opcode": "18", "mod": "/r", "evex": "1"},
    "ymmmem32": {"L": "256", "pp": "66", "mmmm": "0F38", "W": "W0", "opcode": "18", "mod": "/r", "evex": "1"},
    "xmmxmm": {"L": "128", "pp": "66", "mmmm": "0F38", "W": "W0", "opcode": "18", "mod": "/r", "evex": "1"},
    "ymmxmm": {"L": "256", "pp": "66", "mmmm": "0F38", "W": "W0", "opcode": "18", "mod": "/r", "evex": "1"},

    "zmmmem32": {"L": "512", "pp": "66", "mmmm": "0F38", "W": "W0", "opcode": "18", "mod": "/r", "evex": "1"},
    "zmmxmm": {"L": "512", "pp": "66", "mmmm": "0F38", "W": "W0", "opcode": "18", "mod": "/r", "evex": "1"}
}

VBROADCASTSD = {
    "ymmmem64": {"L": "256", "pp": "66", "mmmm": "0F38", "W": "W0", "W512": "W1", "opcode": "19", "mod": "/r", "evex": "1"},
    "ymmxmm": {"L": "256", "pp": "66", "mmmm": "0F38", "W": "W0", "W512": "W1", "opcode": "19", "mod": "/r", "evex": "1"},
    "zmmmem64": {"L": "512", "pp": "66", "mmmm": "0F38", "W": "W0", "W512": "W1", "opcode": "19", "mod": "/r", "evex": "1"},
    "zmmxmm": {"L": "512", "pp": "66", "mmmm": "0F38", "W": "W0", "W512": "W1", "opcode": "19", "mod": "/r", "evex": "1"}
}

VBROADCASTF128 = {
    "ymmmem128": {"L": "256", "pp": "66", "mmmm": "0F38", "W": "W0", "opcode": "1A", "mod": "/r"},
}

VEXTRACTF128 = {
    "xmmymmimm8": {"L": "256", "pp": "66", "mmmm": "0F3A", "W": "W0", "opcode": "19", "mod": "/r", "imm": "ib", 'rm': '1'},
    "mem128ymmimm8": {"L": "256", "pp": "66", "mmmm": "0F3A", "W": "W0", "opcode": "19", "mod": "/r", "imm": "ib"},
}

VINSERTF128 = {
    "ymmymmxmmimm8": {"vvvv": "NDS", "L": "256", "pp": "66", "mmmm": "0F3A", "W": "W0", "opcode": "18", "mod": "/r", "imm": "ib"},
    "ymmymmmem128imm8": {"vvvv": "NDS", "L": "256", "pp": "66", "mmmm": "0F3A", "W": "W0", "opcode": "18", "mod": "/r", "imm": "ib"},
}

VMASKMOVPS = {
    "xmmxmmmem128": {"vvvv": "NDS", "L": "128", "pp": "66", "mmmm": "0F38", "W": "W0", "opcode": "2C", "mod": "/r"},
    "ymmymmmem256": {"vvvv": "NDS", "L": "256", "pp": "66", "mmmm": "0F38", "W": "W0", "opcode": "2C", "mod": "/r"},
    "mem128xmmxmm": {"vvvv": "NDS", "L": "128", "pp": "66", "mmmm": "0F38", "W": "W0", "opcode": "2E", "mod": "/r"},
    "mem256ymmymm": {"vvvv": "NDS", "L": "256", "pp": "66", "mmmm": "0F38", "W": "W0", "opcode": "2E", "mod": "/r"},
}

VMASKMOVPD = {
    "xmmxmmmem128": {"vvvv": "NDS", "L": "128", "pp": "66", "mmmm": "0F38", "W": "W0", "opcode": "2D", "mod": "/r"},
    "ymmymmmem256": {"vvvv": "NDS", "L": "256", "pp": "66", "mmmm": "0F38", "W": "W0", "opcode": "2D", "mod": "/r"},
    "mem128xmmxmm": {"vvvv": "NDS", "L": "128", "pp": "66", "mmmm": "0F38", "W": "W0", "opcode": "2F", "mod": "/r"},
    "mem256ymmymm": {"vvvv": "NDS", "L": "256", "pp": "66", "mmmm": "0F38", "W": "W0", "opcode": "2F", "mod": "/r"},
}

VPERMILPD = {
    "xmmxmmxmm": {"vvvv": "NDS", "L": "128", "pp": "66", "mmmm": "0F38", "W": "W0", "W512": "W1", "opcode": "0D", "mod": "/r", "evex": "1"},
    "xmmxmmmem128": {"vvvv": "NDS", "L": "128", "pp": "66", "mmmm": "0F38", "W": "W0", "W512": "W1", "opcode": "0D", "mod": "/r", "evex": "1"},
    "ymmymmymm": {"vvvv": "NDS", "L": "256", "pp": "66", "mmmm": "0F38", "W": "W0", "W512": "W1", "opcode": "0D", "mod": "/r", "evex": "1"},
    "ymmymmmem256": {"vvvv": "NDS", "L": "256", "pp": "66", "mmmm": "0F38", "W": "W0", "W512": "W1", "opcode": "0D", "mod": "/r", "evex": "1"},
    "zmmzmmzmm": {"vvvv": "NDS", "L": "512", "pp": "66", "mmmm": "0F38", "W": "W0", "W512": "W1", "opcode": "0D", "mod": "/r", "evex": "1"},
    "zmmzmmmem512": {"vvvv": "NDS", "L": "512", "pp": "66", "mmmm": "0F38", "W": "W0", "W512": "W1", "opcode": "0D", "mod": "/r", "evex": "1"},

    "xmmxmmmem64": {"vvvv": "NDS", "L": "128", "pp": "66", "mmmm": "0F38", "W": "W0", "W512": "W1", "opcode": "0D", "mod": "/r", "mbr": "1", "evex": "1"},
    "ymmymmmem64": {"vvvv": "NDS", "L": "256", "pp": "66", "mmmm": "0F38", "W": "W0", "W512": "W1", "opcode": "0D", "mod": "/r", "mbr": "1", "evex": "1"},
    "zmmzmmmem64": {"vvvv": "NDS", "L": "512", "pp": "66", "mmmm": "0F38", "W": "W0", "W512": "W1", "opcode": "0D", "mod": "/r", "mbr": "1", "evex": "1"},

    "xmmxmmimm8": {"L": "128", "pp": "66", "mmmm": "0F3A", "W": "W0", "W512": "W1", "opcode": "05", "mod": "/r", "imm": "ib", "evex": "1"},
    "xmmmem128imm8": {"L": "128", "pp": "66", "mmmm": "0F3A", "W": "W0", "W512": "W1", "opcode": "05", "mod": "/r", "imm": "ib", "evex": "1"},
    "ymmymmimm8": {"L": "256", "pp": "66", "mmmm": "0F3A", "W": "W0", "W512": "W1", "opcode": "05", "mod": "/r", "imm": "ib", "evex": "1"},
    "ymmmem256imm8": {"L": "256", "pp": "66", "mmmm": "0F3A", "W": "W0", "W512": "W1", "opcode": "05", "mod": "/r", "imm": "ib", "evex": "1"},
    "zmmzmmimm8": {"L": "512", "pp": "66", "mmmm": "0F3A", "W": "W0", "W512": "W1", "opcode": "05", "mod": "/r", "imm": "ib", "evex": "1"},
    "zmmmem512imm8": {"L": "512", "pp": "66", "mmmm": "0F3A", "W": "W0", "W512": "W1", "opcode": "05", "mod": "/r", "imm": "ib", "evex": "1"},

    "xmmmem64imm8": {"L": "128", "pp": "66", "mmmm": "0F3A", "W": "W0", "W512": "W1", "opcode": "05", "mod": "/r", "imm": "ib", "mbr": "1", "evex": "1"},
    "ymmmem64imm8": {"L": "256", "pp": "66", "mmmm": "0F3A", "W": "W0", "W512": "W1", "opcode": "05", "mod": "/r", "imm": "ib", "mbr": "1", "evex": "1"},
    "zmmmem64imm8": {"L": "512", "pp": "66", "mmmm": "0F3A", "W": "W0", "W512": "W1", "opcode": "05", "mod": "/r", "imm": "ib", "mbr": "1", "evex": "1"}
}

VPERMILPS = {
    "xmmxmmxmm": {"vvvv": "NDS", "L": "128", "pp": "66", "mmmm": "0F38", "W": "W0", "opcode": "0C", "mod": "/r", "evex": "1"},
    "xmmxmmmem128": {"vvvv": "NDS", "L": "128", "pp": "66", "mmmm": "0F38", "W": "W0", "opcode": "0C", "mod": "/r", "evex": "1"},
    "ymmymmymm": {"vvvv": "NDS", "L": "256", "pp": "66", "mmmm": "0F38", "W": "W0", "opcode": "0C", "mod": "/r", "evex": "1"},
    "ymmymmmem256": {"vvvv": "NDS", "L": "256", "pp": "66", "mmmm": "0F38", "W": "W0", "opcode": "0C", "mod": "/r", "evex": "1"},
    "zmmzmmzmm": {"vvvv": "NDS", "L": "512", "pp": "66", "mmmm": "0F38", "W": "W0", "opcode": "0C", "mod": "/r", "evex": "1"},
    "zmmzmmmem512": {"vvvv": "NDS", "L": "512", "pp": "66", "mmmm": "0F38", "W": "W0", "opcode": "0C", "mod": "/r", "evex": "1"},

    "xmmxmmmem32": {"vvvv": "NDS", "L": "128", "pp": "66", "mmmm": "0F38", "W": "W0", "opcode": "0C", "mod": "/r", "mbr": "1", "evex": "1"},
    "ymmymmmem32": {"vvvv": "NDS", "L": "256", "pp": "66", "mmmm": "0F38", "W": "W0", "opcode": "0C", "mod": "/r", "mbr": "1", "evex": "1"},
    "zmmzmmmem32": {"vvvv": "NDS", "L": "512", "pp": "66", "mmmm": "0F38", "W": "W0", "opcode": "0C", "mod": "/r", "mbr": "1", "evex": "1"},

    "xmmxmmimm8": {"L": "128", "pp": "66", "mmmm": "0F3A", "W": "W0", "opcode": "04", "mod": "/r", "imm": "ib", "evex": "1"},
    "xmmmem128imm8": {"L": "128", "pp": "66", "mmmm": "0F3A", "W": "W0", "opcode": "04", "mod": "/r", "imm": "ib", "evex": "1"},
    "ymmymmimm8": {"L": "256", "pp": "66", "mmmm": "0F3A", "W": "W0", "opcode": "04", "mod": "/r", "imm": "ib", "evex": "1"},
    "ymmmem256imm8": {"L": "256", "pp": "66", "mmmm": "0F3A", "W": "W0", "opcode": "04", "mod": "/r", "imm": "ib", "evex": "1"},
    "zmmzmmimm8": {"L": "512", "pp": "66", "mmmm": "0F3A", "W": "W0", "opcode": "04", "mod": "/r", "imm": "ib", "evex": "1"},
    "zmmmem512imm8": {"L": "512", "pp": "66", "mmmm": "0F3A", "W": "W0", "opcode": "04", "mod": "/r", "imm": "ib", "evex": "1"},

    "xmmmem32imm8": {"L": "128", "pp": "66", "mmmm": "0F3A", "W": "W0", "opcode": "04", "mod": "/r", "imm": "ib", "mbr": "1", "evex": "1"},
    "ymmmem32imm8": {"L": "256", "pp": "66", "mmmm": "0F3A", "W": "W0", "opcode": "04", "mod": "/r", "imm": "ib", "mbr": "1", "evex": "1"},
    "zmmmem32imm8": {"L": "512", "pp": "66", "mmmm": "0F3A", "W": "W0", "opcode": "04", "mod": "/r", "imm": "ib", "mbr": "1", "evex": "1"}
}

VPERM2F128 = {
    "ymmymmymmimm8": {"vvvv": "NDS", "L": "256", "pp": "66", "mmmm": "0F3A", "W": "W0", "opcode": "06", "mod": "/r", "imm": "ib"},
    "ymmymmmem256imm8": {"vvvv": "NDS", "L": "256", "pp": "66", "mmmm": "0F3A", "W": "W0", "opcode": "06", "mod": "/r", "imm": "ib"},
}

VTESTPS = {
    "xmmxmm": {"L": "128", "pp": "66", "mmmm": "0F38", "W": "W0", "opcode": "0E", "mod": "/r"},
    "xmmmem128": {"L": "128", "pp": "66", "mmmm": "0F38", "W": "W0", "opcode": "0E", "mod": "/r"},
    "ymmymm": {"L": "256", "pp": "66", "mmmm": "0F38", "W": "W0", "opcode": "0E", "mod": "/r"},
    "ymmmem256": {"L": "256", "pp": "66", "mmmm": "0F38", "W": "W0", "opcode": "0E", "mod": "/r"},
}

VTESTPD = {
    "xmmxmm": {"L": "128", "pp": "66", "mmmm": "0F38", "W": "W0", "opcode": "0F", "mod": "/r"},
    "xmmmem128": {"L": "128", "pp": "66", "mmmm": "0F38", "W": "W0", "opcode": "0F", "mod": "/r"},
    "ymmymm": {"L": "256", "pp": "66", "mmmm": "0F38", "W": "W0", "opcode": "0F", "mod": "/r"},
    "ymmmem256": {"L": "256", "pp": "66", "mmmm": "0F38", "W": "W0", "opcode": "0F", "mod": "/r"},
}

VZEROALL = {
    "no_op": {"L": "256", "mmmm": "0F", "W": "WIG", "opcode": "77"}
}

VZEROUPPER = {
    "no_op": {"L": "128", "mmmm": "0F", "W": "WIG", "opcode": "77"}
}
