
from .tdasm import translate
from .runtime import Runtime

MMX = False
SSE = False
SSE2 = False
SSE3 = False
SSSE3 = False
SSE41 = False
SSE42 = False
AVX = False
FMA = False
AVX2 = False
RDRAND = False
RDSEED = False
MOVBE = False
BMI1 = False
BMI2 = False
ADX = False
F16C = False
VENDOR_NAME = ''
MAX_CPUID = 1

AVX512F = False
AVX512ER = False
AVX512PF = False
AVX512CD = False
AVX512DQ = False
AVX512BW = False
AVX512VL = False


def _detect_sse():
    asm_source = """
    #DATA
    string vendor_name = "xxxxxxxxxxxx"
    uint32 max_cpuid ;max input value for cpuid information
    uint32 feature1, feature2 ; support for different instructions set

    #CODE
    mov eax, 0
    cpuid
    mov dword [vendor_name], ebx
    mov dword [vendor_name+4], edx
    mov dword [vendor_name+8], ecx
    mov dword [max_cpuid], eax

    mov eax, 1
    cpuid
    mov dword [feature1], ecx
    mov dword [feature2], edx
    """

    run = Runtime()
    ds = run.load('detect', translate(asm_source))
    run.run('detect')

    global MMX
    global SSE
    global SSE2
    global SSE3
    global SSSE3
    global SSE41
    global SSE42
    global RDRAND
    global MOVBE
    global VENDOR_NAME
    global MAX_CPUID

    feature1 = ds['feature1']
    feature2 = ds['feature2']
    MAX_CPUID = ds['max_cpuid']

    MMX = bool(feature2 & 0x00800000)
    SSE = bool(feature2 & 0x02000000)
    SSE2 = bool(feature2 & 0x04000000)
    SSE3 = bool(feature1 & 0x00000001)
    SSSE3 = bool(feature1 & 0x00000200)
    SSE41 = bool(feature1 & 0x00080000)
    SSE42 = bool(feature1 & 0x00100000)
    RDRAND = bool(feature1 & 0x40000000)
    MOVBE = bool(feature1 & 0x00400000)
    VENDOR_NAME = ds['vendor_name']


def _detect_avx():
    asm_source = """
    #DATA
    uint32 avx_supported = 0
    #CODE
    mov eax, 1
    cpuid
    and ecx, 0x18000000
    cmp ecx, 0x18000000
    jne not_supported
    mov ecx, 0
    xgetbv
    and eax, 0x6
    cmp  eax,0x6
    jne not_supported
    mov dword [avx_supported], 1
    jmp done
    not_supported:
    mov dword [avx_supported], 0
    done:
    """
    run = Runtime()
    ds = run.load('detect', translate(asm_source))
    run.run('detect')

    global AVX
    AVX = bool(ds['avx_supported'])


def _detect_f16c():
    asm_source = """
    #DATA
    uint32 f16c_supported = 0
    #CODE
    mov eax, 1
    cpuid
    and ecx, 0x38000000
    cmp ecx, 0x38000000
    jne not_supported

    mov ecx, 0
    xgetbv
    and eax, 0x6
    cmp eax, 0x6
    jne not_supported
    mov dword [f16c_supported], 1
    jmp done
    not_supported:
    mov dword [f16c_supported], 0
    done:
    """
    run = Runtime()
    ds = run.load('detect', translate(asm_source))
    run.run('detect')

    global F16C
    F16C = bool(ds['f16c_supported'])


def _detect_fma():
    asm_source = """
    #DATA
    uint32 fma_supported = 0
    #CODE
    mov eax, 1
    cpuid
    and ecx, 0x18001000
    cmp ecx, 0x18001000
    jne not_supported
    mov ecx, 0
    xgetbv
    and eax, 0x6
    cmp eax, 0x6
    jne not_supported
    mov dword [fma_supported], 1
    jmp done
    not_supported:
    mov dword [fma_supported], 0
    done:
    """
    run = Runtime()
    ds = run.load('detect', translate(asm_source))
    run.run('detect')

    global FMA
    FMA = bool(ds['fma_supported'])


def _detect_avx2():
    asm_source = """
    #DATA
    uint32 avx2_supported = 0
    uint32 feature
    #CODE
    mov eax, 1
    cpuid
    and ecx, 0x18000000
    cmp ecx, 0x18000000
    jne not_supported
    mov eax, 7
    mov ecx, 0
    cpuid
    mov dword [feature], ebx
    and ebx, 0x20
    cmp ebx, 0x20
    jne not_supported
    mov ecx,0
    xgetbv
    and eax, 0x6
    cmp eax, 0x6
    jne not_supported
    mov dword [avx2_supported], 1
    jmp done
    not_supported:
    mov dword [avx2_supported], 0
    done:
    """
    run = Runtime()
    ds = run.load('detect', translate(asm_source))
    run.run('detect')

    global AVX2
    AVX2 = bool(ds['avx2_supported'])

    global BMI1
    global BMI2
    global ADX
    global RDSEED
    feature = ds['feature']
    BMI1 = bool(feature & 0x00000008)
    BMI2 = bool(feature & 0x00000100)
    ADX = bool(feature & 0x00080000)
    RDSEED = bool(feature & 0x00040000)


def _detect_avx512():
    asm_source = """
    #DATA
    uint32 feature
    
    #CODE
    mov dword[feature], 0
    mov eax, 1
    cpuid
    and ecx, 0x08000000
    cmp ecx, 0x08000000
    jne not_supported
    
    mov ecx,0
    xgetbv
    and eax, 0x6
    cmp eax, 0x6
    jne not_supported
    
    mov ecx,0
    xgetbv
    and eax, 0xE0
    cmp eax, 0xE0
    jne not_supported
    
    mov eax, 7
    mov ecx, 0
    cpuid
    mov dword [feature], ebx
    jmp done
    
    not_supported:
    mov dword [feature], 0
    done:
    """
    run = Runtime()
    ds = run.load('detect', translate(asm_source))
    run.run('detect')

    feature = ds['feature']

    global AVX512F
    global AVX512ER
    global AVX512PF
    global AVX512CD
    global AVX512DQ
    global AVX512BW
    global AVX512VL
    AVX512F = bool(feature & 0x00010000)
    AVX512ER = AVX512F and bool(feature & 0x08000000)
    AVX512PF = AVX512F and bool(feature & 0x04000000)
    AVX512CD = AVX512F and bool(feature & 0x10000000)
    AVX512DQ = AVX512F and bool(feature & 0x00020000)
    AVX512BW = AVX512F and bool(feature & 0x40000000)
    AVX512VL = bool(feature & 0x80000000)


class CPUFeatures:
    def __init__(self, MMX=False, SSE=False, SSE2=False, SSE3=False,
                 SSSE3=False, SSE41=False, SSE42=False, RDRAND=False,
                 MOVBE=False, F16C=False, AVX=False, FMA=False, AVX2=False,
                 RDSEED=False, BMI1=False, BMI2=False, ADX=False, VENDOR_NAME=None,
                 AVX512F=False, AVX512ER=False, AVX512PF=False, AVX512CD=False,
                 AVX512DQ=False, AVX512BW=False, AVX512VL=False):

        self.MMX = MMX
        self.SSE = SSE
        self.SSE2 = SSE2
        self.SSE3 = SSE3
        self.SSSE3 = SSSE3
        self.SSE41 = SSE41
        self.SSE42 = SSE42
        self.RDRAND = RDRAND
        self.RDSEED = RDSEED
        self.MOVBE = MOVBE
        self.F16C = F16C
        self.AVX = AVX
        self.FMA = FMA
        self.AVX2 = AVX2
        self.BMI1 = BMI1
        self.BMI2 = BMI2
        self.ADX = ADX
        self.VENDOR_NAME = VENDOR_NAME
        self.AVX512F = AVX512F
        self.AVX512ER = AVX512ER
        self.AVX512PF = AVX512PF
        self.AVX512CD = AVX512CD
        self.AVX512DQ = AVX512DQ
        self.AVX512BW = AVX512BW
        self.AVX512VL = AVX512VL


def cpu_features():
    if MMX is False:
        _detect_sse()
        _detect_f16c()
        _detect_avx()
        _detect_fma()
        if MAX_CPUID > 6:
            _detect_avx2()
            _detect_avx512()

    cpu = CPUFeatures(MMX=MMX, SSE=SSE, SSE2=SSE2, SSE3=SSE3, SSSE3=SSSE3,
                      SSE41=SSE41, SSE42=SSE42, RDRAND=RDRAND,
                      MOVBE=MOVBE, F16C=F16C, AVX=AVX, FMA=FMA, AVX2=AVX2,
                      RDSEED=RDSEED, BMI1=BMI1, BMI2=BMI2, ADX=ADX, VENDOR_NAME=VENDOR_NAME,
                      AVX512F=AVX512F, AVX512ER=AVX512ER, AVX512PF=AVX512PF, AVX512CD=AVX512CD,
                      AVX512DQ=AVX512DQ, AVX512BW=AVX512BW, AVX512VL=AVX512VL)
    return cpu
