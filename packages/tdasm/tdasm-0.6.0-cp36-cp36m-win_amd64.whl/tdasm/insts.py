
from .holders import Instruction, RegOperand, MemOperand, NameOperand,\
    ConstOperand, LabelOperand
from .regs import registers
from .general_i import *
from .fpu_i import *
from .mmx_i import *
from .sse_i import *
from .sse2_i import *
from .avx_i import *
from .fma_i import *
from .sse3_i import *
from .ssse3_i import *
from .sse41_i import *
from .sse42_i import *
from .avx2_i import *
from .avx_512 import *


instructions = {

    # Data transfer instructions
    'mov': MOV,
    'cmova': CMOVA,
    'cmovae': CMOVAE,
    'cmovb': CMOVB,
    'cmovbe': CMOVBE,
    'cmovc': CMOVC,
    'cmove': CMOVE,
    'cmovg': CMOVG,
    'cmovge': CMOVGE,
    'cmovl': CMOVL,
    'cmovle': CMOVLE,
    'cmovna': CMOVNA,
    'cmovnae': CMOVNAE,
    'cmovnb': CMOVNB,
    'cmovnbe': CMOVNBE,
    'cmovnc': CMOVNC,
    'cmovne': CMOVNE,
    'cmovng': CMOVNG,
    'cmovnge': CMOVNGE,
    'cmovnl': CMOVNL,
    'cmovnle': CMOVNLE,
    'cmovno': CMOVNO,
    'cmovnp': CMOVNP,
    'cmovns': CMOVNS,
    'cmovnz': CMOVNZ,
    'cmovo': CMOVO,
    'cmovp': CMOVP,
    'cmovpe': CMOVPE,
    'cmovpo': CMOVPO,
    'cmovs': CMOVS,
    'cmovz': CMOVZ,
    'xchg': XCHG,
    'bswap': BSWAP,
    'xadd': XADD,
    'cmpxchg': CMPXCHG,
    'cmpxchg8b': CMPXCHG8B,
    'push': PUSH,
    'pop': POP,
    'cwd': CWD,
    'cdq': CDQ,
    'cqo': CQO,
    'cbw': CBW,
    'cwde': CWDE,
    'cdqe': CDQE,
    'movsx': MOVSX,
    'movzx': MOVZX,

    # Binary Arithmetic instructions
    'adcx': ADCX,
    'adox': ADOX,
    'add': ADD,
    'adc': ADC,
    'sub': SUB,
    'sbb': SBB,
    'imul': IMUL,
    'mul': MUL,
    'idiv': IDIV,
    'div': DIV,
    'inc': INC,
    'dec': DEC,
    'neg': NEG,
    'cmp': CMP,

    # Logical instructions
    'and': AND,
    'or': OR,
    'xor': XOR,
    'not': NOT,

    # Shift and rotate instructions
    'sar': SAR,
    'shr': SHR,
    'sal': SAL,
    'shl': SHL,
    'shrd': SHRD,
    'shld': SHLD,
    'ror': ROR,
    'rol': ROL,
    'rcr': RCR,
    'rcl': RCL,

    # Control Transfer Instructions
    'jmp': JMP,
    'je': JE,
    'jz': JZ,
    'jne': JNE,
    'jnz': JNZ,
    'ja': JA,
    'jnbe': JNBE,
    'jae': JAE,
    'jnb': JNB,
    'jb': JB,
    'jnae': JNAE,
    'jbe': JBE,
    'jna': JNA,
    'jg': JG,
    'jnle': JNLE,
    'jge': JGE,
    'jnl': JNL,
    'jl': JL,
    'jnge': JNGE,
    'jle': JLE,
    'jng': JNG,
    'jc': JC,
    'jnc': JNC,
    'jo': JO,
    'jno': JNO,
    'js': JS,
    'jns': JNS,
    'jpo': JPO,
    'jnp': JNP,
    'jpe': JPE,
    'jp': JP,
    'jecxz': JECXZ,
    'jrcxz': JRCXZ,
    'loop': LOOP,
    'loope': LOOPE,
    'loopz': LOOPZ,
    'loopne': LOOPNE,
    'loopnz': LOOPNZ,
    'call': CALL,
    'ret': RET,
    'iret': IRET,
    'iretd': IRETD,
    'iretq': IRETQ,
    'int3': INT3,
    'int': INT,

    # String Instructions
    'movsb': MOVSB,
    'movsw': MOVSW,
    'movsd': MOVSD,
    'movsq': MOVSQ,

    # Miscellaneous Instructions
    'lea': LEA,
    'nop': NOP,
    'ud2': UD2,
    'xlatb': XLATB,
    'cpuid': CPUID,
    'movbe': MOVBE,
    'prefetchw': PREFETCHW,
    'prefetchwt1': PREFETCHWT1,
    'xgetbv': XGETBV,

    # Random Number Generator Instructions
    'rdrand': RDRAND,
    'rdseed': RDSEED,

    # FPU Data Transfer Instructions
    'fld': FLD,
    'fst': FST,
    'fstp': FSTP,
    'fild': FILD,
    'fist': FIST,
    'fistp': FISTP,
    'fbld': FBLD,
    'fbstp': FBSTP,
    'fxch': FXCH,
    'fcmovb': FCMOVB,
    'fcmove': FCMOVE,
    'fcmovbe': FCMOVBE,
    'fcmovu': FCMOVU,
    'fcmovnb': FCMOVNB,
    'fcmovne': FCMOVNE,
    'fcmovnbe': FCMOVNBE,
    'fcmovnu': FCMOVNU,

    # FPU Basic Arithmetic Instructions
    'fadd': FADD,
    'faddp': FADDP,
    'fiadd': FIADD,
    'fsub': FSUB,
    'fsubp': FSUBP,
    'fisub': FISUB,
    'fsubr': FSUBR,
    'fsubrp': FSUBRP,
    'fisubr': FISUBR,
    'fmul': FMUL,
    'fmulp': FMULP,
    'fimul': FIMUL,
    'fdiv': FDIV,
    'fdivp': FDIVP,
    'fidiv': FIDIV,
    'fdivr': FDIVR,
    'fdivrp': FDIVRP,
    'fidivr': FIDIVR,
    'fprem': FPREM,
    'fprem1': FPREM1,
    'fabs': FABS,
    'fchs': FCHS,
    'frndint': FRNDINT,
    'fscale': FSCALE,
    'fsqrt': FSQRT,
    'fxtract': FXTRACT,

    # FPU Comparison Instructions
    'fcom': FCOM,
    'fcomp': FCOMP,
    'fcompp': FCOMPP,
    'fucom': FUCOM,
    'fucomp': FUCOMP,
    'fucompp': FUCOMPP,
    'ficom': FICOM,
    'ficomp': FICOMP,
    'fcomi': FCOMI,
    'fucomi': FUCOMI,
    'fcomip': FCOMIP,
    'fucomip': FUCOMIP,
    'ftst': FTST,
    'fxam': FXAM,

    # FPU Transcendental Instructions
    'fsin': FSIN,
    'fcos': FCOS,
    'fsincos': FSINCOS,
    'fptan': FPTAN,
    'fpatan': FPATAN,
    'f2xm1': F2XM1,
    'fyl2x': FYL2X,
    'fyl2xp1': FYL2XP1,

    # FPU constants
    'fld1': FLD1,
    'fldl2t': FLDL2T,
    'fldl2e': FLDL2E,
    'fldpi': FLDPI,
    'fldlg2': FLDLG2,
    'fldln2': FLDLN2,
    'fldz': FLDZ,

    # FPU Control Instructions
    'fincstp': FINCSTP,
    'fdecstp': FDECSTP,
    'ffree': FFREE,
    'finit': FINIT,
    'fninit': FNINIT,
    'fclex': FCLEX,
    'fnclex': FNCLEX,
    'fstcw': FSTCW,
    'fnstcw': FNSTCW,
    'fldcw': FLDCW,
    'fstenv': FSTENV,
    'fnstenv': FNSTENV,
    'fldenv': FLDENV,
    'fsave': FSAVE,
    'fnsave': FNSAVE,
    'frstor': FRSTOR,
    'fstsw': FSTSW,
    'fnstsw': FNSTSW,
    'wait': WAIT,
    'fwait': FWAIT,
    'fnop': FNOP,

    # FPU and SIMD State Managment Instructions
    'fxsave': FXSAVE,
    'fxsave64': FXSAVE64,
    'fxrstor': FXRSTOR,
    'fxrstor64': FXRSTOR64,

    # MMX Data Transfer Instructions
    'movd': MOVD,
    'movq': MOVQ,

    # MMX Conversion Instructions
    'packsswb': PACKSSWB,
    'packssdw': PACKSSDW,
    'packuswb': PACKUSWB,
    'punpckhbw': PUNPCKHBW,
    'punpckhwd': PUNPCKHWD,
    'punpckhdq': PUNPCKHDQ,
    'punpcklbw': PUNPCKLBW,
    'punpcklwd': PUNPCKLWD,
    'punpckldq': PUNPCKLDQ,

    # MMX Arithmetic Instructions
    'paddb': PADDB,
    'paddw': PADDW,
    'paddd': PADDD,
    'paddsb': PADDSB,
    'paddsw': PADDSW,
    'paddusb': PADDUSB,
    'paddusw': PADDUSW,
    'psubb': PSUBB,
    'psubw': PSUBW,
    'psubd': PSUBD,
    'psubsb': PSUBSB,
    'psubsw': PSUBSW,
    'psubusb': PSUBUSB,
    'psubusw': PSUBUSW,
    'pmulhw': PMULHW,
    'pmullw': PMULLW,
    'pmaddwd': PMADDWD,

    # MMX Comparison Instructions
    'pcmpeqb': PCMPEQB,
    'pcmpeqw': PCMPEQW,
    'pcmpeqd': PCMPEQD,
    'pcmpgtb': PCMPGTB,
    'pcmpgtw': PCMPGTW,
    'pcmpgtd': PCMPGTD,

    # MMX Logical Instructions
    'pand': PAND,
    'pandn': PANDN,
    'por': POR,
    'pxor': PXOR,

    # MMX Shift and Rotate Instructions
    'psllw': PSLLW,
    'pslld': PSLLD,
    'psllq': PSLLQ,
    'psrlw': PSRLW,
    'psrld': PSRLD,
    'psrlq': PSRLQ,
    'psraw': PSRAW,
    'psrad': PSRAD,

    'emms': EMMS,

    # SSE Data Transfer Instructions
    'movaps': MOVAPS,
    'movups': MOVUPS,
    'movhps': MOVHPS,
    'movhlps': MOVHLPS,
    'movlps': MOVLPS,
    'movlhps': MOVLHPS,
    'movmskps': MOVMSKPS,
    'movss': MOVSS,

    # SSE Arithmetic Instructions
    'addps': ADDPS,
    'addss': ADDSS,
    'subps': SUBPS,
    'subss': SUBSS,
    'mulps': MULPS,
    'mulss': MULSS,
    'divps': DIVPS,
    'divss': DIVSS,
    'rcpps': RCPPS,
    'rcpss': RCPSS,
    'sqrtps': SQRTPS,
    'sqrtss': SQRTSS,
    'rsqrtps': RSQRTPS,
    'rsqrtss': RSQRTSS,
    'maxps': MAXPS,
    'maxss': MAXSS,
    'minps': MINPS,
    'minss': MINSS,

    # SSE Comparison Instructions
    'cmpps': CMPPS,
    'cmpss': CMPSS,
    'comiss': COMISS,
    'ucomiss': UCOMISS,

    # SSE Logical Instructions
    'andps': ANDPS,
    'andnps': ANDNPS,
    'orps': ORPS,
    'xorps': XORPS,

    # SSE Shuffle and Unpack Instructions
    'shufps': SHUFPS,
    'unpckhps': UNPCKHPS,
    'unpcklps': UNPCKLPS,

    # SSE Conversion Instructions
    'cvtpi2ps': CVTPI2PS,
    'cvtsi2ss': CVTSI2SS,
    'cvtps2pi': CVTPS2PI,
    'cvttps2pi': CVTTPS2PI,
    'cvtss2si': CVTSS2SI,
    'cvttss2si': CVTTSS2SI,

    # SSE State Managment Instructions
    'ldmxcsr': LDMXCSR,
    'stmxcsr': STMXCSR,

    # SSE Integer Instructions
    'pavgb': PAVGB,
    'pavgw': PAVGW,
    'pextrw': PEXTRW,
    'pinsrw': PINSRW,
    'pmaxub': PMAXUB,
    'pmaxsw': PMAXSW,
    'pminub': PMINUB,
    'pminsw': PMINSW,
    'pmovmskb': PMOVMSKB,
    'pmulhuw': PMULHUW,
    'psadbw': PSADBW,
    'pshufw': PSHUFW,

    # SSE Misc Instructions
    'maskmovq': MASKMOVQ,
    'movntq': MOVNTQ,
    'movntps': MOVNTPS,
    'prefetcht0': PREFETCHT0,
    'prefetcht1': PREFETCHT1,
    'prefetcht2': PREFETCHT2,
    'prefetchnta': PREFETCHNTA,
    'sfence': SFENCE,

    # SSE2 Data Transfer Instructions
    'movapd': MOVAPD,
    'movupd': MOVUPD,
    'movhpd': MOVHPD,
    'movlpd': MOVLPD,
    'movmskpd': MOVMSKPD,
    'movsd': MOVSD,

    # SSE2 Arithmetic Instructions
    'addpd': ADDPD,
    'addsd': ADDSD,
    'subpd': SUBPD,
    'subsd': SUBSD,
    'mulpd': MULPD,
    'mulsd': MULSD,
    'divpd': DIVPD,
    'divsd': DIVSD,
    'sqrtpd': SQRTPD,
    'sqrtsd': SQRTSD,
    'maxpd': MAXPD,
    'maxsd': MAXSD,
    'minpd': MINPD,
    'minsd': MINSD,

    # SSE2 Comparison Instructions
    'cmppd': CMPPD,
    'cmpsd': CMPSD,
    'comisd': COMISD,
    'ucomisd': UCOMISD,

    # SSE2 Logical Instructions
    'andpd': ANDPD,
    'andnpd': ANDNPD,
    'orpd': ORPD,
    'xorpd': XORPD,

    # SSE2 Shuffle and Unpack Instructions
    'shufpd': SHUFPD,
    'unpckhpd': UNPCKHPD,
    'unpcklpd': UNPCKLPD,

    # SSE2 Conversion Instructions
    'cvtpd2pi': CVTPD2PI,
    'cvttpd2pi': CVTTPD2PI,
    'cvtpi2pd': CVTPI2PD,
    'cvtpd2dq': CVTPD2DQ,
    'cvttpd2dq': CVTTPD2DQ,
    'cvtdq2pd': CVTDQ2PD,
    'cvtps2pd': CVTPS2PD,
    'cvtpd2ps': CVTPD2PS,
    'cvtss2sd': CVTSS2SD,
    'cvtsd2ss': CVTSD2SS,
    'cvtsd2si': CVTSD2SI,
    'cvttsd2si': CVTTSD2SI,
    'cvtsi2sd': CVTSI2SD,
    'cvtdq2ps': CVTDQ2PS,
    'cvtps2dq': CVTPS2DQ,
    'cvttps2dq': CVTTPS2DQ,

    # SSE2 Integer instructions
    'movdqa': MOVDQA,
    'movdqu': MOVDQU,
    'movq2dq': MOVQ2DQ,
    'movdq2q': MOVDQ2Q,
    'pmuludq': PMULUDQ,
    'paddq': PADDQ,
    'psubq': PSUBQ,
    'pshuflw': PSHUFLW,
    'pshufhw': PSHUFHW,
    'pshufd': PSHUFD,
    'pslldq': PSLLDQ,
    'psrldq': PSRLDQ,
    'punpckhqdq': PUNPCKHQDQ,
    'punpcklqdq': PUNPCKLQDQ,

    # SSE2 Cacheability control instructions
    'clflush': CLFLUSH,
    'lfence': LFENCE,
    'mfence': MFENCE,
    'puase': PAUSE,
    'maskmovdqu': MASKMOVDQU,
    'movntpd': MOVNTPD,
    'movnti': MOVNTI,
    'movntdq': MOVNTDQ,

    # SSE3 Instructions
    'fisttp': FISTTP,
    'lddqu': LDDQU,
    'addsubps': ADDSUBPS,
    'addsubpd': ADDSUBPD,
    'haddps': HADDPS,
    'hsubps': HSUBPS,
    'haddpd': HADDPD,
    'hsubpd': HSUBPD,
    'movsldup': MOVSLDUP,
    'movshdup': MOVSHDUP,
    'movddup': MOVDDUP,
    'monitor': MONITOR,
    'mwait': MWAIT,

    # SSSE3 Instructions
    'phaddw': PHADDW,
    'phaddsw': PHADDSW,
    'phaddd': PHADDD,
    'phsubw': PHSUBW,
    'phsubsw': PHSUBSW,
    'phsubd': PHSUBD,
    'pabsb': PABSB,
    'pabsw': PABSW,
    'pabsd': PABSD,
    'pmaddubsw': PMADDUBSW,
    'pmulhrsw': PMULHRSW,
    'pshufb': PSHUFB,
    'psignb': PSIGNB,
    'psignw': PSIGNW,
    'psignd': PSIGND,
    'palignr': PALIGNR,

    # SSE41 Instruction
    'pmulld': PMULLD,
    'pmuldq': PMULDQ,
    'dppd': DPPD,
    'dpps': DPPS,
    'movntdqa': MOVNTDQA,
    'blendpd': BLENDPD,
    'blendps': BLENDPS,
    'blendvpd': BLENDVPD,
    'blendvps': BLENDVPS,
    'pblendvb': PBLENDVB,
    'pblendw': PBLENDW,
    'pminuw': PMINUW,
    'pminud': PMINUD,
    'pminsb': PMINSB,
    'pminsd': PMINSD,
    'pmaxuw': PMAXUW,
    'pmaxud': PMAXUD,
    'pmaxsb': PMAXSB,
    'pmaxsd': PMAXSD,
    'roundps': ROUNDPS,
    'roundpd': ROUNDPD,
    'roundss': ROUNDSS,
    'roundsd': ROUNDSD,
    'extractps': EXTRACTPS,
    'insertps': INSERTPS,
    'pinsrb': PINSRB,
    'pinsrd': PINSRD,
    'pinsrq': PINSRQ,
    'pextrb': PEXTRB,
    'pextrw': PEXTRW,
    'pextrd': PEXTRD,
    'pextrq': PEXTRQ,
    'pmovsxbw': PMOVSXBW,
    'pmovzxbw': PMOVZXBW,
    'pmovsxbd': PMOVSXBD,
    'pmovzxbd': PMOVZXBD,
    'pmovsxwd': PMOVSXWD,
    'pmovzxwd': PMOVZXWD,
    'pmovsxbq': PMOVSXBQ,
    'pmovzxbq': PMOVZXBQ,
    'pmovsxwq': PMOVSXWQ,
    'pmovzxwq': PMOVZXWQ,
    'pmovsxdq': PMOVSXDQ,
    'pmovzxdq': PMOVZXDQ,
    'mpsadbw': MPSADBW,
    'phminposuw': PHMINPOSUW,
    'ptest': PTEST,
    'pcmpeqq': PCMPEQQ,
    'packusdw': PACKUSDW,

    # SSE42 Instruction
    'pcmpestri': PCMPESTRI,
    'pcmpestrm': PCMPESTRM,
    'pcmpistri': PCMPISTRI,
    'pcmpistrm': PCMPISTRM,
    'pcmpgtq': PCMPGTQ,
}

vex_instructions = {

    # AVX Instructions
    # AVX MMX Instructions
    'vmovd': VMOVD,
    'vmovq': VMOVQ,
    'vpacksswb': VPACKSSWB,
    'vpackssdw': VPACKSSDW,
    'vpackuswb': VPACKUSWB,
    'vpunpckhbw': VPUNPCKHBW,
    'vpunpckhwd': VPUNPCKHWD,
    'vpunpckhdq': VPUNPCKHDQ,
    'vpunpcklbw': VPUNPCKLBW,
    'vpunpcklwd': VPUNPCKLWD,
    'vpunpckldq': VPUNPCKLDQ,
    'vpaddb': VPADDB,
    'vpaddw': VPADDW,
    'vpaddd': VPADDD,
    'vpaddsb': VPADDSB,
    'vpaddsw': VPADDSW,
    'vpaddusb': VPADDUSB,
    'vpaddusw': VPADDUSW,
    'vpsubb': VPSUBB,
    'vpsubw': VPSUBW,
    'vpsubd': VPSUBD,
    'vpsubsb': VPSUBSB,
    'vpsubsw': VPSUBSW,
    'vpsubusb': VPSUBUSB,
    'vpsubusw': VPSUBUSW,
    'vpmulhw': VPMULHW,
    'vpmullw': VPMULLW,
    'vpmaddwd': VPMADDWD,
    'vpcmpeqb': VPCMPEQB,
    'vpcmpeqw': VPCMPEQW,
    'vpcmpeqd': VPCMPEQD,
    'vpcmpgtb': VPCMPGTB,
    'vpcmpgtw': VPCMPGTW,
    'vpcmpgtd': VPCMPGTD,
    'vpand': VPAND,
    'vpandn': VPANDN,
    'vpor': VPOR,
    'vpxor': VPXOR,
    'vpsllw': VPSLLW,
    'vpslld': VPSLLD,
    'vpsllq': VPSLLQ,
    'vpsrlw': VPSRLW,
    'vpsrld': VPSRLD,
    'vpsrlq': VPSRLQ,
    'vpsraw': VPSRAW,
    'vpsrad': VPSRAD,

    # AVX SSE Instructions
    'vmovaps': VMOVAPS,
    'vmovups': VMOVUPS,
    'vmovhps': VMOVHPS,
    'vmovhlps': VMOVHLPS,
    'vmovlps': VMOVLPS,
    'vmovlhps': VMOVLHPS,
    'vmovmskps': VMOVMSKPS,
    'vmovss': VMOVSS,
    'vaddps': VADDPS,
    'vaddss': VADDSS,
    'vsubps': VSUBPS,
    'vsubss': VSUBSS,
    'vmulps': VMULPS,
    'vmulss': VMULSS,
    'vdivps': VDIVPS,
    'vdivss': VDIVSS,
    'vrcpps': VRCPPS,
    'vrcpss': VRCPSS,
    'vsqrtps': VSQRTPS,
    'vsqrtss': VSQRTSS,
    'vrsqrtps': VRSQRTPS,
    'vrsqrtss': VRSQRTSS,
    'vmaxps': VMAXPS,
    'vmaxss': VMAXSS,
    'vminps': VMINPS,
    'vminss': VMINSS,
    'vcmpps': VCMPPS,
    'vcmpss': VCMPSS,
    'vcomiss': VCOMISS,
    'vucomiss': VUCOMISS,
    'vandps': VANDPS,
    'vandnps': VANDNPS,
    'vorps': VORPS,
    'vxorps': VXORPS,
    'vshufps': VSHUFPS,
    'vunpckhps': VUNPCKHPS,
    'vunpcklps': VUNPCKLPS,
    'vcvtsi2ss': VCVTSI2SS,
    'vcvtss2si': VCVTSS2SI,
    'vcvttss2si': VCVTTSS2SI,
    'vldmxcsr': VLDMXCSR,
    'vstmxcsr': VSTMXCSR,
    'vpavgb': VPAVGB,
    'vpavgw': VPAVGW,
    'vpextrw': VPEXTRW,
    'vpinsrw': VPINSRW,
    'vpmaxub': VPMAXUB,
    'vpmaxsw': VPMAXSW,
    'vpminub': VPMINUB,
    'vpminsw': VPMINSW,
    'vpmovmskb': VPMOVMSKB,
    'vpmulhuw': VPMULHUW,
    'vpsadbw': VPSADBW,
    'vmovntps': VMOVNTPS,

    # AVX SSE2 Instructions
    'vmovapd': VMOVAPD,
    'vmovupd': VMOVUPD,
    'vmovhpd': VMOVHPD,
    'vmovlpd': VMOVLPD,
    'vmovmskpd': VMOVMSKPD,
    'vmovsd': VMOVSD,
    'vaddpd': VADDPD,
    'vaddsd': VADDSD,
    'vsubpd': VSUBPD,
    'vsubsd': VSUBSD,
    'vmulpd': VMULPD,
    'vmulsd': VMULSD,
    'vdivpd': VDIVPD,
    'vdivsd': VDIVSD,
    'vsqrtpd': VSQRTPD,
    'vsqrtsd': VSQRTSD,
    'vmaxpd': VMAXPD,
    'vmaxsd': VMAXSD,
    'vminpd': VMINPD,
    'vminsd': VMINSD,
    'vcmppd': VCMPPD,
    'vcmpsd': VCMPSD,
    'vcomisd': VCOMISD,
    'vucomisd': VUCOMISD,
    'vandpd': VANDPD,
    'vandnpd': VANDNPD,
    'vorpd': VORPD,
    'vxorpd': VXORPD,
    'vshufpd': VSHUFPD,
    'vunpckhpd': VUNPCKHPD,
    'vunpcklpd': VUNPCKLPD,
    'vcvtpd2dq': VCVTPD2DQ,
    'vcvttpd2dq': VCVTTPD2DQ,
    'vcvtdq2pd': VCVTDQ2PD,
    'vcvtps2pd': VCVTPS2PD,
    'vcvtpd2ps': VCVTPD2PS,
    'vcvtss2sd': VCVTSS2SD,
    'vcvtsd2ss': VCVTSD2SS,
    'vcvtsd2si': VCVTSD2SI,
    'vcvttsd2si': VCVTTSD2SI,
    'vcvtsi2sd': VCVTSI2SD,
    'vcvtdq2ps': VCVTDQ2PS,
    'vcvtps2dq': VCVTPS2DQ,
    'vcvttps2dq': VCVTTPS2DQ,
    'vmovdqa': VMOVDQA,
    'vmovdqu': VMOVDQU,
    'vpmuludq': VPMULUDQ,
    'vpaddq': VPADDQ,
    'vpsubq': VPSUBQ,
    'vpshuflw': VPSHUFLW,
    'vpshufhw': VPSHUFHW,
    'vpshufd': VPSHUFD,
    'vpslldq': VPSLLDQ,
    'vpsrldq': VPSRLDQ,
    'vpunpckhqdq': VPUNPCKHQDQ,
    'vpunpcklqdq': VPUNPCKLQDQ,
    'vmaskmovdqu': VMASKMOVDQU,
    'vmovntpd': VMOVNTPD,
    'vmovntdq': VMOVNTDQ,

    # AVX SSE3 Instructions
    'vlddqu': VLDDQU,
    'vaddsubps': VADDSUBPS,
    'vaddsubpd': VADDSUBPD,
    'vhaddps': VHADDPS,
    'vhsubps': VHSUBPS,
    'vhaddpd': VHADDPD,
    'vhsubpd': VHSUBPD,
    'vmovsldup': VMOVSLDUP,
    'vmovshdup': VMOVSHDUP,
    'vmovddup': VMOVDDUP,

    # AVX SSSE3 Instructions
    'vphaddw': VPHADDW,
    'vphaddsw': VPHADDSW,
    'vphaddd': VPHADDD,
    'vphsubw': VPHSUBW,
    'vphsubsw': VPHSUBSW,
    'vphsubd': VPHSUBD,
    'vpabsb': VPABSB,
    'vpabsw': VPABSW,
    'vpabsd': VPABSD,
    'vpmaddubsw': VPMADDUBSW,
    'vpmulhrsw': VPMULHRSW,
    'vpshufb': VPSHUFB,
    'vpsignb': VPSIGNB,
    'vpsignw': VPSIGNW,
    'vpsignd': VPSIGND,
    'vpalignr': VPALIGNR,

    # AVX SSE41 Instructions
    'vpmulld': VPMULLD,
    'vpmuldq': VPMULDQ,
    'vdppd': VDPPD,
    'vdpps': VDPPS,
    'vmovntdqa': VMOVNTDQA,
    'vblendpd': VBLENDPD,
    'vblendps': VBLENDPS,
    'vblendvpd': VBLENDVPD,
    'vblendvps': VBLENDVPS,
    'vpblendvb': VPBLENDVB,
    'vpblendw': VPBLENDW,
    'vpminuw': VPMINUW,
    'vpminud': VPMINUD,
    'vpminsb': VPMINSB,
    'vpminsd': VPMINSD,
    'vpmaxuw': VPMAXUW,
    'vpmaxud': VPMAXUD,
    'vpmaxsb': VPMAXSB,
    'vpmaxsd': VPMAXSD,
    'vroundps': VROUNDPS,
    'vroundpd': VROUNDPD,
    'vroundss': VROUNDSS,
    'vroundsd': VROUNDSD,
    'vextractps': VEXTRACTPS,
    'vinsertps': VINSERTPS,
    'vpinsrb': VPINSRB,
    'vpinsrd': VPINSRD,
    'vpinsrq': VPINSRQ,
    'vpextrb': VPEXTRB,
    'vpextrw': VPEXTRW,
    'vpextrd': VPEXTRD,
    'vpextrq': VPEXTRQ,
    'vpmovsxbw': VPMOVSXBW,
    'vpmovzxbw': VPMOVZXBW,
    'vpmovsxbd': VPMOVSXBD,
    'vpmovzxbd': VPMOVZXBD,
    'vpmovsxwd': VPMOVSXWD,
    'vpmovzxwd': VPMOVZXWD,
    'vpmovsxbq': VPMOVSXBQ,
    'vpmovzxbq': VPMOVZXBQ,
    'vpmovsxwq': VPMOVSXWQ,
    'vpmovzxwq': VPMOVZXWQ,
    'vpmovsxdq': VPMOVSXDQ,
    'vpmovzxdq': VPMOVZXDQ,
    'vmpsadbw': VMPSADBW,
    'vphminposuw': VPHMINPOSUW,
    'vptest': VPTEST,
    'vpcmpeqq': VPCMPEQQ,
    'vpackusdw': VPACKUSDW,

    # AVX SSE42 Instruction
    'vpcmpestri': VPCMPESTRI,
    'vpcmpestrm': VPCMPESTRM,
    'vpcmpistri': VPCMPISTRI,
    'vpcmpistrm': VPCMPISTRM,
    'vpcmpgtq': VPCMPGTQ,

    # AVX FMA Instructions
    'vfmadd132ps': VFMADD132PS,
    'vfmadd132ss': VFMADD132SS,
    'vfmadd132pd': VFMADD132PD,
    'vfmadd132sd': VFMADD132SD,
    'vfmadd213ps': VFMADD213PS,
    'vfmadd213ss': VFMADD213SS,
    'vfmadd213pd': VFMADD213PD,
    'vfmadd213sd': VFMADD213SD,
    'vfmadd231ps': VFMADD231PS,
    'vfmadd231ss': VFMADD231SS,
    'vfmadd231pd': VFMADD231PD,
    'vfmadd231sd': VFMADD231SD,
    'vfmaddsub132ps': VFMADDSUB132PS,
    'vfmaddsub132pd': VFMADDSUB132PD,
    'vfmaddsub213ps': VFMADDSUB213PS,
    'vfmaddsub213pd': VFMADDSUB213PD,
    'vfmaddsub231ps': VFMADDSUB231PS,
    'vfmaddsub231pd': VFMADDSUB231PD,
    'vfmsubadd132ps': VFMSUBADD132PS,
    'vfmsubadd132pd': VFMSUBADD132PD,
    'vfmsubadd213ps': VFMSUBADD213PS,
    'vfmsubadd213pd': VFMSUBADD213PD,
    'vfmsubadd231ps': VFMSUBADD231PS,
    'vfmsubadd231pd': VFMSUBADD231PD,
    'vfmsub132ps': VFMSUB132PS,
    'vfmsub132ss': VFMSUB132SS,
    'vfmsub213ps': VFMSUB213PS,
    'vfmsub213ss': VFMSUB213SS,
    'vfmsub231ps': VFMSUB231PS,
    'vfmsub231ss': VFMSUB231SS,
    'vfmsub132pd': VFMSUB132PD,
    'vfmsub132sd': VFMSUB132SD,
    'vfmsub213pd': VFMSUB213PD,
    'vfmsub213sd': VFMSUB213SD,
    'vfmsub231pd': VFMSUB231PD,
    'vfmsub231sd': VFMSUB231SD,
    'vfnmadd132ps': VFNMADD132PS,
    'vfnmadd132ss': VFNMADD132SS,
    'vfnmadd213ps': VFNMADD213PS,
    'vfnmadd213ss': VFNMADD213SS,
    'vfnmadd231ps': VFNMADD231PS,
    'vfnmadd231ss': VFNMADD231SS,
    'vfnmadd132pd': VFNMADD132PD,
    'vfnmadd132sd': VFNMADD132SD,
    'vfnmadd213pd': VFNMADD213PD,
    'vfnmadd213sd': VFNMADD213SD,
    'vfnmadd231pd': VFNMADD231PD,
    'vfnmadd231sd': VFNMADD231SD,
    'vfnmsub132ps': VFNMSUB132PS,
    'vfnmsub132ss': VFNMSUB132SS,
    'vfnmsub213ps': VFNMSUB213PS,
    'vfnmsub213ss': VFNMSUB213SS,
    'vfnmsub231ps': VFNMSUB231PS,
    'vfnmsub231ss': VFNMSUB231SS,
    'vfnmsub132pd': VFNMSUB132PD,
    'vfnmsub132sd': VFNMSUB132SD,
    'vfnmsub213pd': VFNMSUB213PD,
    'vfnmsub213sd': VFNMSUB213SD,
    'vfnmsub231pd': VFNMSUB231PD,
    'vfnmsub231sd': VFNMSUB231SD,

    # AVX Instructions
    'vbroadcastf128': VBROADCASTF128,
    'vbroadcastsd': VBROADCASTSD,
    'vbroadcastss': VBROADCASTSS,
    'vextractf128': VEXTRACTF128,
    'vinsertf128': VINSERTF128,
    'vmaskmovps': VMASKMOVPS,
    'vmaskmovpd': VMASKMOVPD,
    'vpermilpd': VPERMILPD,
    'vpermilps': VPERMILPS,
    'vperm2f128': VPERM2F128,
    'vtestps': VTESTPS,
    'vtestpd': VTESTPD,
    'vzeroall': VZEROALL,
    'vzeroupper': VZEROUPPER,

    # AVX2 Instructions
    'vpbroadcastb': VPBROADCASTB,
    'vpbroadcastw': VPBROADCASTW,
    'vpbroadcastd': VPBROADCASTD,
    'vpbroadcastq': VPBROADCASTQ,
    'vbroadcasti128': VBROADCASTI128,
    'vextracti128': VEXTRACTI128,
    'vinserti128': VINSERTI128,
    'vpmaskmovd': VPMASKMOVD,
    'vpmaskmovq': VPMASKMOVQ,
    'vperm2i128': VPERM2I128,
    'vpermd': VPERMD,
    'vpermps': VPERMPS,
    'vpermq': VPERMQ,
    'vpermpd': VPERMPD,
    'vpblendd': VPBLENDD,
    'vpsllvd': VPSLLVD,
    'vpsllvq': VPSLLVQ,
    'vpsravd': VPSRAVD,
    'vpsrlvd': VPSRLVD,
    'vpsrlvq': VPSRLVQ,
}

evex_instructions = {
    'vpandd': VPANDD,
    'vpandq': VPANDQ,
    'vpandnd': VPANDND,
    'vpandnq': VPANDNQ,
    'vpord': VPORD,
    'vporq': VPORQ,
    'vpxord': VPXORD,
    'vpxorq': VPXORQ,
    'vpsraq': VPSRAQ,
    'vmovdqa32': VMOVDQA32,
    'vmovdqa64': VMOVDQA64,
    'vmovdqu8': VMOVDQU8,
    'vmovdqu16': VMOVDQU16,
    'vmovdqu32': VMOVDQU32,
    'vmovdqu64': VMOVDQU64,
    'vpabsq': VPABSQ,
    'vpmullq': VPMULLQ,
    'vpminuq': VPMINUQ,
    'vpminsq': VPMINSQ,
    'vpmaxuq': VPMAXUQ,
    'vpmaxsq': VPMAXSQ,
    'vbroadcastf32x2': VBROADCASTF32X2,
    'vbroadcastf32x4': VBROADCASTF32X4,
    'vbroadcastf32x8': VBROADCASTF32X8,
    'vbroadcastf64x2': VBROADCASTF64X2,
    'vbroadcastf64x4': VBROADCASTF64X4,
    'vextractf32x4': VEXTRACTF32X4,
    'vextractf32x8': VEXTRACTF32X8,
    'vextractf64x2': VEXTRACTF64X2,
    'vextractf64x4': VEXTRACTF64X4,
    'vinsertf32x4': VINSERTF32X4,
    'vinsertf32x8': VINSERTF32X8,
    'vinsertf64x2': VINSERTF64X2,
    'vinsertf64x4': VINSERTF64X4,
    'vbroadcasti32x2': VBROADCASTI32X2,
    'vbroadcasti32x4': VBROADCASTI32X4,
    'vbroadcasti32x8': VBROADCASTI32X8,
    'vbroadcasti64x2': VBROADCASTI64X2,
    'vbroadcasti64x4': VBROADCASTI64X4,
    'vextracti32x4': VEXTRACTI32X4,
    'vextracti32x8': VEXTRACTI32X8,
    'vextracti64x2': VEXTRACTI64X2,
    'vextracti64x4': VEXTRACTI64X4,
    'vinserti32x4': VINSERTI32X4,
    'vinserti32x8': VINSERTI32X8,
    'vinserti64x2': VINSERTI64X2,
    'vinserti64x4': VINSERTI64X4,
    'vpermw': VPERMW,
    'vpsllvw': VPSLLVW,
    'vpsravq': VPSRAVQ,
    'vpsravw': VPSRAVW,
    'vpsrlvw': VPSRLVW,
    'vrndscaless': VRNDSCALESS,
    'vrndscaleps': VRNDSCALEPS,
    'vrndscalesd': VRNDSCALESD,
    'vrndscalepd': VRNDSCALEPD,
    'valignd': VALIGND,
    'valignq': VALIGNQ,
    'vblendmps': VBLENDMPS,
    'vblendmpd': VBLENDMPD,

    'vpmovqd': VPMOVQD,
    'vpmovsqd': VPMOVSQD,
    'vpmovusqd': VPMOVUSQD,
    'vpmovqb': VPMOVQB,
    'vpmovsqb': VPMOVSQB,
    'vpmovusqb': VPMOVUSQB,
    'vpmovqw': VPMOVQW,
    'vpmovsqw': VPMOVSQW,
    'vpmovusqw': VPMOVUSQW,
    'vcompressps': VCOMPRESSPS,
    'vcompresspd': VCOMPRESSPD,

    'vscalefss': VSCALEFSS,
    'vscalefps': VSCALEFPS,
    'vscalefsd': VSCALEFSD,
    'vscalefpd': VSCALEFPD,
}

opmask_instructions = {
    'kaddw': KADDW,
    'kaddb': KADDB,
    'kaddq': KADDQ,
    'kaddd': KADDD,

    'kandw': KANDW,
    'kandb': KANDB,
    'kandq': KANDQ,
    'kandd': KANDD,

    'kandnw': KANDNW,
    'kandnb': KANDNB,
    'kandnq': KANDNQ,
    'kandnd': KANDND,

    'korw': KORW,
    'korb': KORB,
    'korq': KORQ,
    'kord': KORD,

    'kunpckbw': KUNPCKBW,
    'kunpckwd': KUNPCKWD,
    'kunpckdq': KUNPCKDQ,

    'kxnorw': KXNORW,
    'kxnorb': KXNORB,
    'kxnorq': KXNORQ,
    'kxnord': KXNORD,

    'kxorw': KXORW,
    'kxorb': KXORB,
    'kxorq': KXORQ,
    'kxord': KXORD,

    'kmovw': KMOVW,
    'kmovb': KMOVB,
    'kmovq': KMOVQ,
    'kmovd': KMOVD,

    'knotw': KNOTW,
    'knotb': KNOTB,
    'knotq': KNOTQ,
    'knotd': KNOTD,

    'kortestw': KORTESTW,
    'kortestb': KORTESTB,
    'kortestq': KORTESTQ,
    'kortestd': KORTESTD,

    'kshiftlw': KSHIFTLW,
    'kshiftlb': KSHIFTLB,
    'kshiftlq': KSHIFTLQ,
    'kshiftld': KSHIFTLD,

    'kshiftrw': KSHIFTRW,
    'kshiftrb': KSHIFTRB,
    'kshiftrq': KSHIFTRQ,
    'kshiftrd': KSHIFTRD,

    'ktestw': KTESTW,
    'ktestb': KTESTB,
    'ktestq': KTESTQ,
    'ktestd': KTESTD,
}


instructions.update(vex_instructions)
instructions.update(evex_instructions)
instructions.update(opmask_instructions)

_mem_size = {
    'byte': '8',
    'word': '16',
    'dword': '32',
    'qword': '64',
    'tbyte': '80',
    'dqword': '128',
    'oword': '128',
    'yword': '256',
    'zword': '512'
}


def _generate_keys(operand):
    if isinstance(operand, RegOperand):
        if operand.reg in ('rax', 'eax', 'ax', 'al', 'st0', 'cl'):
            return [operand.reg.upper(), registers[operand.reg][1]]
        return [registers[operand.reg][1]]
    elif isinstance(operand, (MemOperand, NameOperand)):
        return ['mem' + _mem_size[operand.data_type]]
    elif isinstance(operand, ConstOperand):
        if not isinstance(operand.value, int):
            raise ValueError('Only integer operand supported.', operand.value)
        if operand.value >= -128 and operand.value <= 255:
            return ["imm8", "imm16", "imm32", "imm64"]
        elif operand.value >= -32768 and operand.value <= 65535:
            return ["imm16", "imm32", "imm64"]
        elif operand.value >= -2147483648 and operand.value <= 4294967295:
            return ["imm32", "imm64"]
        else:
            return ["imm64"]
    elif isinstance(operand, LabelOperand):
        if operand.small_jump:
            return ["rel8", "rel32"]
        else:
            return ["rel32"]
    else:
        raise ValueError("Unsupported operand type for encoding.", operand)


def _sign_ext_check(instruction, size):

    def check(value):
        if not isinstance(value, int):
            raise ValueError("Integer constant expected for sign extension.")

        if size == '1':
            if value <= 127 and value >= -128:
                return True
        elif size == '2':
            if value <= 32767 and value >= -32768:
                return True
        elif size == '4':
            if value <= 2147483647 and value >= -2147483648:
                return True
        return False

    if isinstance(instruction.op1, ConstOperand):
        return check(instruction.op1.value)
    elif isinstance(instruction.op2, ConstOperand):
        return check(instruction.op2.value)
    elif isinstance(instruction.op3, ConstOperand):
        return check(instruction.op3.value)
    elif isinstance(instruction.op4, ConstOperand):
        return check(instruction.op4.value)
    raise ValueError("When sign extension one operand must be integer.", instruction.name)


def find_instruction_params(instruction: Instruction):

    if instruction.name not in instructions:
        raise ValueError("Instruction %s does not exist." % instruction.name)

    if instruction.op1 is None:
        return instructions[instruction.name]['no_op']

    k1 = k2 = k3 = k4 = [""]
    k1 = _generate_keys(instruction.op1)
    if instruction.op2 is not None:
        k2 = _generate_keys(instruction.op2)
    if instruction.op3 is not None:
        k3 = _generate_keys(instruction.op3)
    if instruction.op4 is not None:
        k4 = _generate_keys(instruction.op4)

    inst = instructions[instruction.name]

    for h1 in k1:
        for h2 in k2:
            for h3 in k3:
                for h4 in k4:
                    key = h1 + h2 + h3 + h4
                    params = inst.get(key, None)
                    if params is not None:
                        if 'sign_ext' in params:
                            if not _sign_ext_check(instruction, params['sign_ext']):
                                continue
                        return params
    raise ValueError('Instruction %s not found with params' % instruction.name, k1, k2, k3, k4)


def vex_encoding_needed(name: str):
    return name in vex_instructions


def evex_encoding_needed(name: str):
    return name in evex_instructions


def opmask_encoding_needed(name: str):
    return name in opmask_instructions
