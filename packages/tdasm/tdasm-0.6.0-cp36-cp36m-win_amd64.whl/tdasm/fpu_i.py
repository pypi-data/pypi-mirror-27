

FLD = {
    "mem32": {"mod": "/0", "opcode": "D9"},
    "mem64": {"mod": "/0", "opcode": "DD"},
    "mem80": {"mod": "/5", "opcode": "DB"},
    "ST(i)": {"opcode": "D9C0", "post": "+i"},
}

FST = {
    "mem32": {"mod": "/2", "opcode": "D9"},
    "mem64": {"mod": "/2", "opcode": "DD"},
    "ST(i)": {"opcode": "DDD0", "post": "+i"},
}

FSTP = {
    "mem32": {"mod": "/3", "opcode": "D9"},
    "mem64": {"mod": "/3", "opcode": "DD"},
    "mem80": {"mod": "/7", "opcode": "DB"},
    "ST(i)": {"opcode": "DDD8", "post": "+i"},
}

FILD = {
    "mem16": {"mod": "/0", "opcode": "DF"},
    "mem32": {"mod": "/0", "opcode": "DB"},
    "mem64": {"mod": "/5", "opcode": "DF"},
}

FIST = {
    "mem16": {"mod": "/2", "opcode": "DF"},
    "mem32": {"mod": "/2", "opcode": "DB"},
}

FISTP = {
    "mem16": {"mod": "/3", "opcode": "DF"},
    "mem32": {"mod": "/3", "opcode": "DB"},
    "mem64": {"mod": "/7", "opcode": "DF"},
}

FBLD = {
    "mem80": {"mod": "/4", "opcode": "DF"},
}

FBSTP = {
    "mem80": {"mod": "/6", "opcode": "DF"},
}

FXCH = {
    "no_op": {"opcode": "D9C9"},
    "ST(i)": {"opcode": "D9C8", "post": "+i"},
}

FCMOVB = {
    "ST0ST(i)": {"opcode": "DAC0", "post": "+i"},
}

FCMOVE = {
    "ST0ST(i)": {"opcode": "DAC8", "post": "+i"},
}

FCMOVBE = {
    "ST0ST(i)": {"opcode": "DAD0", "post": "+i"},
}

FCMOVU = {
    "ST0ST(i)": {"opcode": "DAD8", "post": "+i"},
}

FCMOVNB = {
    "ST0ST(i)": {"opcode": "DBC0", "post": "+i"},
}

FCMOVNE = {
    "ST0ST(i)": {"opcode": "DBC8", "post": "+i"},
}

FCMOVNBE = {
    "ST0ST(i)": {"opcode": "DBD0", "post": "+i"},
}

FCMOVNU = {
    "ST0ST(i)": {"opcode": "DBD8", "post": "+i"},
}

# FPU Basic Arithmetic Instructions

FADD = {
    "mem32": {"mod": "/0", "opcode": "D8"},
    "mem64": {"mod": "/0", "opcode": "DC"},
    "ST0ST(i)": {"post": "+i", "opcode": "D8C0"},
    "ST(i)ST0": {"post": "+i", "opcode": "DCC0"},
}

FADDP = {
    "ST(i)ST0": {"post": "+i", "opcode": "DEC0"},
    "no_op": {"opcode": "DEC1"}
}

FIADD = {
    "mem32": {"mod": "/0", "opcode": "DA"},
    "mem16": {"mod": "/0", "opcode": "DE"},
}

FSUB = {
    "mem32": {"mod": "/4", "opcode": "D8"},
    "mem64": {"mod": "/4", "opcode": "DC"},
    "ST0ST(i)": {"post": "+i", "opcode": "D8E0"},
    "ST(i)ST0": {"post": "+i", "opcode": "DCE8"},
}

FSUBP = {
    "ST(i)ST0": {"post": "+i", "opcode": "DEE8"},
    "no_op": {"opcode": "DEE9"}
}

FISUB = {
    "mem32": {"mod": "/4", "opcode": "DA"},
    "mem16": {"mod": "/4", "opcode": "DE"},
}

FSUBR = {
    "mem32": {"mod": "/5", "opcode": "D8"},
    "mem64": {"mod": "/5", "opcode": "DC"},
    "ST0ST(i)": {"post": "+i", "opcode": "D8E8"},
    "ST(i)ST0": {"post": "+i", "opcode": "DCE0"},
}

FSUBRP = {
    "ST(i)ST0": {"post": "+i", "opcode": "DEE0"},
    "no_op": {"opcode": "DEE1"}
}

FISUBR = {
    "mem32": {"mod": "/5", "opcode": "DA"},
    "mem16": {"mod": "/5", "opcode": "DE"},
}

FMUL = {
    "mem32": {"mod": "/1", "opcode": "D8"},
    "mem64": {"mod": "/1", "opcode": "DC"},
    "ST0ST(i)": {"post": "+i", "opcode": "D8C8"},
    "ST(i)ST0": {"post": "+i", "opcode": "DCC8"},
}

FMULP = {
    "ST(i)ST0": {"post": "+i", "opcode": "DEC8"},
    "no_op": {"opcode": "DEC9"}
}

FIMUL = {
    "mem32": {"mod": "/1", "opcode": "DA"},
    "mem16": {"mod": "/1", "opcode": "DE"},
}

FDIV = {
    "mem32": {"mod": "/6", "opcode": "D8"},
    "mem64": {"mod": "/6", "opcode": "DC"},
    "ST0ST(i)": {"post": "+i", "opcode": "D8F0"},
    "ST(i)ST0": {"post": "+i", "opcode": "DCF8"},
}

FDIVP = {
    "ST(i)ST0": {"post": "+i", "opcode": "DEF8"},
    "no_op": {"opcode": "DEF9"}
}

FIDIV = {
    "mem32": {"mod": "/6", "opcode": "DA"},
    "mem16": {"mod": "/6", "opcode": "DE"},
}

FDIVR = {
    "mem32": {"mod": "/7", "opcode": "D8"},
    "mem64": {"mod": "/7", "opcode": "DC"},
    "ST0ST(i)": {"post": "+i", "opcode": "D8F8"},
    "ST(i)ST0": {"post": "+i", "opcode": "DCF0"},
}

FDIVRP = {
    "ST(i)ST0": {"post": "+i", "opcode": "DEF0"},
    "no_op": {"opcode": "DEF1"}
}

FIDIVR = {
    "mem32": {"mod": "/7", "opcode": "DA"},
    "mem16": {"mod": "/7", "opcode": "DE"},
}

FPREM = {
    "no_op": {"opcode": "D9F8"}
}

FPREM1 = {
    "no_op": {"opcode": "D9F5"}
}

FABS = {
    "no_op": {"opcode": "D9E1"}
}

FCHS = {
    "no_op": {"opcode": "D9E0"}
}

FRNDINT = {
    "no_op": {"opcode": "D9FC"}
}

FSCALE = {
    "no_op": {"opcode": "D9FD"}
}

FSQRT = {
    "no_op": {"opcode": "D9FA"}
}

FXTRACT = {
    "no_op": {"opcode": "D9F4"}
}

# FPU Comparison Instructions

FCOM = {
    "mem32": {"mod": "/2", "opcode": "D8"},
    "mem64": {"mod": "/2", "opcode": "DC"},
    "ST(i)": {"opcode": "D8D0", "post": "+i"},
    "no_op": {"opcode": "D8D1"}
}

FCOMP = {
    "mem32": {"mod": "/3", "opcode": "D8"},
    "mem64": {"mod": "/3", "opcode": "DC"},
    "ST(i)": {"opcode": "D8D8", "post": "+i"},
    "no_op": {"opcode": "D8D9"}
}

FCOMPP = {
    "no_op": {"opcode": "DED9"}
}

FUCOM = {
    "ST(i)": {"opcode": "DDE0", "post": "+i"},
    "no_op": {"opcode": "DDE1"}
}

FUCOMP = {
    "ST(i)": {"opcode": "DDE8", "post": "+i"},
    "no_op": {"opcode": "DDE9"}
}

FUCOMPP = {
    "no_op": {"opcode": "DAE9"}
}

FICOM = {
    "mem32": {"mod": "/2", "opcode": "DA"},
    "mem16": {"mod": "/2", "opcode": "DE"},
}

FICOMP = {
    "mem32": {"mod": "/3", "opcode": "DA"},
    "mem16": {"mod": "/3", "opcode": "DE"},
}

FCOMI = {
    "ST0ST(i)": {"post": "+i", "opcode": "DBF0"},
}

FCOMIP = {
    "ST0ST(i)": {"post": "+i", "opcode": "DFF0"},
}

FUCOMI = {
    "ST0ST(i)": {"post": "+i", "opcode": "DBE8"},
}

FUCOMIP = {
    "ST0ST(i)": {"post": "+i", "opcode": "DFE8"},
}

FTST = {
    "no_op": {"opcode": "D9E4"}
}

FXAM = {
    "no_op": {"opcode": "D9E5"}
}

# FPU Transcendental Instructions

FSIN = {
    "no_op": {"opcode": "D9FE"}
}

FCOS = {
    "no_op": {"opcode": "D9FF"}
}

FSINCOS = {
    "no_op": {"opcode": "D9FB"}
}

FPTAN = {
    "no_op": {"opcode": "D9F2"}
}

FPATAN = {
    "no_op": {"opcode": "D9F3"}
}

F2XM1 = {
    "no_op": {"opcode": "D9F0"}
}

FYL2X = {
    "no_op": {"opcode": "D9F1"}
}

FYL2XP1 = {
    "no_op": {"opcode": "D9F9"}
}

# FPU Constants

FLD1 = {
    "no_op": {"opcode": "D9E8"}
}

FLDL2T = {
    "no_op": {"opcode": "D9E9"}
}

FLDL2E = {
    "no_op": {"opcode": "D9EA"}
}

FLDPI = {
    "no_op": {"opcode": "D9EB"}
}

FLDLG2 = {
    "no_op": {"opcode": "D9EC"}
}

FLDLN2 = {
    "no_op": {"opcode": "D9ED"}
}

FLDZ = {
    "no_op": {"opcode": "D9EE"}
}

# FPU Control Instructions

FINCSTP = {
    "no_op": {"opcode": "D9F7"}
}

FDECSTP = {
    "no_op": {"opcode": "D9F6"}
}

FFREE = {
    "ST(i)": {"post": "+i", "opcode": "DDC0"}
}

FINIT = {
    "no_op": {"opcode": "9BDBE3"}
}

FNINIT = {
    "no_op": {"opcode": "DBE3"}
}

FCLEX = {
    "no_op": {"opcode": "9BDBE2"}
}

FNCLEX = {
    "no_op": {"opcode": "DBE2"}
}

FSTCW = {
    "r16": {"mod": "/7", "opcode": "9BD9"},
    "mem16": {"mod": "/7", "opcode": "9BD9"}
}

FNSTCW = {
    "r16": {"mod": "/7", "opcode": "D9"},
    "mem16": {"mod": "/7", "opcode": "D9"}
}

FLDCW = {
    "r16": {"mod": "/5", "opcode": "D9"},
    "mem16": {"mod": "/5", "opcode": "D9"}
}

FSTENV = {
    "mem8": {"mod": "/6", "opcode": "9BD9"}
}

FNSTENV = {
    "mem8": {"mod": "/6", "opcode": "D9"}
}

FLDENV = {
    "mem8": {"mod": "/4", "opcode": "D9"}
}

FSAVE = {
    "mem8": {"mod": "/6", "opcode": "9BDD"}
}

FNSAVE = {
    "mem8": {"mod": "/6", "opcode": "DD"}
}

FRSTOR = {
    "mem8": {"mod": "/4", "opcode": "DD"}
}

FSTSW = {
    "ax": {"opcode": "9BDFE0"},
    "mem16": {"mod": "/7", "opcode": "9BDD"}
}

FNSTSW = {
    "ax": {"opcode": "DFE0"},
    "mem16": {"mod": "/7", "opcode": "DD"}
}

WAIT = {
    "no_op": {"opcode": "9B"}
}

FWAIT = {
    "no_op": {"opcode": "9B"}
}

FNOP = {
    "no_op": {"opcode": "D9D0"}
}

# FPU and SIMD State Managment Instructions

FXSAVE = {
    "mem8": {"mod": "/0", "opcode": "0FAE"}
}

FXSAVE64 = {
    "mem8": {"mod": "/0", "opcode": "0FAE", "prefix": "REX.W"}
}

FXRSTOR = {
    "mem8": {"mod": "/1", "opcode": "0FAE"}
}

FXRSTOR64 = {
    "mem8": {"mod": "/1", "opcode": "0FAE", "prefix": "REX.W"}
}
