
"""
.. module:: tdasm
.. moduleauthor:: Mario Vidov <mvidov@yahoo.com>


"""

import struct
from .code import MachineCode
from .lex import Lexer
from .parser import Parser
from .encoder import Encoder
from .holders import Directive, Label, Keyword, DataMembers,\
    Instruction, LabelOperand, EncodedInstruction, StructDefinition,\
    NameOperand, MemOperand


class Tdasm:
    lexer = Lexer()
    parser = Parser()

    def __init__(self):
        pass

    def translate(self, source: str, standalone: bool=True, force_avx512: bool=False)-> MachineCode:

        self.encoder = Encoder(force_avx512=force_avx512)
        self._in_code_section = True
        self._in_struct_def = False
        self._struct_def = None
        self._address = 0
        self._fix_insts = []
        self._code = MachineCode()
        self._labels = {}
        self._align_labels = True

        function_callbacks = {
            Directive: self._process_directive,
            Label: self._process_label,
            Keyword: self._process_keyword,
            DataMembers: self._process_members,
            Instruction: self._process_instruction
        }

        if standalone:
            source = self._prolog_code() + source + self._epilog_code()

        lines = self.lexer.tokenize(source)
        for line in lines:
            self._tokens = line
            result = self.parser.parse(line, self._in_code_section)
            if result is None:
                continue
            function_callbacks[type(result)](result)
        self._fix_local_labels()

        return self._code

    def _prolog_code(self):
        src = """
        #DATA
        uint64 __gen_reg[16]
        #CODE
        mov qword [__gen_reg], rax
        mov qword [__gen_reg + 8], rbx
        mov qword [__gen_reg + 16], rcx
        mov qword [__gen_reg + 24], rdx
        mov qword [__gen_reg + 32], rsi
        mov qword [__gen_reg + 40], rdi
        mov qword [__gen_reg + 48], rsp
        mov qword [__gen_reg + 56], rbp
        mov qword [__gen_reg + 64], r8
        mov qword [__gen_reg + 72], r9
        mov qword [__gen_reg + 80], r10
        mov qword [__gen_reg + 88], r11
        mov qword [__gen_reg + 96], r12
        mov qword [__gen_reg + 104], r13
        mov qword [__gen_reg + 112], r14
        mov qword [__gen_reg + 120], r15
        """
        return src

    def _epilog_code(self):
        src = """
        #CODE
        mov rax, qword [__gen_reg]
        mov rbx, qword [__gen_reg + 8]
        mov rcx, qword [__gen_reg + 16]
        mov rdx, qword [__gen_reg + 24]
        mov rsi, qword [__gen_reg + 32]
        mov rdi, qword [__gen_reg + 40]
        mov rsp, qword [__gen_reg + 48]
        mov rbp, qword [__gen_reg + 56]
        mov r8, qword [__gen_reg + 64]
        mov r9, qword [__gen_reg + 72]
        mov r10, qword [__gen_reg + 80]
        mov r11, qword [__gen_reg + 88]
        mov r12, qword [__gen_reg + 96]
        mov r13, qword [__gen_reg + 104]
        mov r14, qword [__gen_reg + 112]
        mov r15, qword [__gen_reg + 120]
        ret
        """
        return src

    def _process_directive(self, directive: Directive):
        if directive.name == 'DATA':
            self._in_code_section = False
        elif directive.name == 'CODE':
            self._in_code_section = True
        elif directive.name == 'END':
            # process jump instruction to end
            raise ValueError("DIrecive END must be processed")
        else:
            raise ValueError('Unknown directive', directive.name)

    def _process_label(self, label: Label):

        if label.name in self._labels:
            raise ValueError("Label %s allready exist!" % label.name)

        if self._align_labels:

            nop_codes = {
                1: (b'\x90', 'xchg eax, eax; nop'),
                2: (b'\x66\x90', '66 nop; nop'),
                3: (b'\x66\x90\x90', '66 nop; nop, nop'),
                4: (b'\x0f\x1f\x40\x00', 'nop dword [rax + 0]; nop'),
                5: (b'\x0f\x1f\x44\x00\x00', 'nop dword [rax + rax*1 + 0]; nop'),
                6: (b'\x0f\x1f\x44\x00\x00\x90', 'nop dword [rax + rax*1 + 0]; nop, nop'),
                7: (b'\x0f\x1f\x80\x00\x00\x00\x00', 'nop dword [rax + 0]; nop'),
                8: (b'\x0f\x1f\x84\x00\x00\x00\x00\x00', 'nop dword [rax + rax*1 + 0]; nop'),
                9: (b'\x66\x0f\x1f\x84\x00\x00\x00\x00\x00', 'nop word [rax + rax*1 + 0] ;nop')
            }

            align = 16
            diff = ((self._address + align - 1) & ~(align - 1)) - self._address
            while diff != 0:
                diff = min(9, diff)
                i = EncodedInstruction('nop')
                i.code = nop_codes[diff][0]
                i.source = nop_codes[diff][1]
                self._address += len(i.code)
                self._code.add_instruction(i)
                diff = ((self._address + align - 1) & ~(align - 1)) - self._address

        self._labels[label.name[:-1]] = self._address
        inst = EncodedInstruction("")
        inst.code = b''
        inst.source = label.name
        self._code.add_instruction(inst)

    def _process_keyword(self, keyword: Keyword):
        if not self._in_code_section and keyword.name == 'struct':
            if self._struct_def is not None:
                raise ValueError("Struct inside of another struct not yet supported")
            self._in_struct_def = True
            self._struct_def = StructDefinition(keyword.iden)

        elif not self._in_code_section and keyword.name == 'end':
            self._in_struct_def = False
            if self._struct_def is None:
                raise ValueError("end keyword before struct, syntax error.")
            self._code.add_struct_def(self._struct_def)
            self._struct_def = None
        else:
            raise ValueError("Keyword %s not implemented yet" % keyword.name)

    def _process_members(self, members: DataMembers):
        if self._in_struct_def:
            self._struct_def.add_members(members)
        else:
            self._code.add_members(members)

    def _calc_displacement(self, struct_member):
        parts = struct_member.split('.')
        if len(parts) < 2:
            raise ValueError("Displacement for %s cannot be calculated." % struct_member)
        path = '.'.join(p for p in parts[1:])
        return self._code.struct_member_disp(parts[0], path)

    def _struct_displacement(self, instruction: Instruction):
        def process_op(op):
            if isinstance(op, (NameOperand, MemOperand)):
                if op.struct_member is not None:
                    disp = self._calc_displacement(op.struct_member)
                    if op.displacement is None:
                        op.displacement = disp
                    else:
                        op.displacement += disp

                    op.struct_member = None

        process_op(instruction.op1)
        process_op(instruction.op2)
        process_op(instruction.op3)
        process_op(instruction.op4)

    def _process_instruction(self, instruction: Instruction):
        self._struct_displacement(instruction)

        if isinstance(instruction.op1, LabelOperand):
            addr = self._labels.get(instruction.op1.label, None)
            if addr is not None:
                diff = addr - self._address
                instruction.op1.value = diff
                if diff < 115 and diff > -115:
                    instruction.op1.small_jump = True

        inst = self.encoder.encode(instruction)
        self._address += len(inst.code)
        if inst.rel_label is not None:
            self._fix_insts.append((self._address, inst))
        self._code.add_instruction(inst)
        inst.source = "".join(token[1] for token in self._tokens)

    def _fix_local_labels(self):
        for addr, inst in self._fix_insts:
            rel_label, size = inst.rel_label
            if rel_label in self._labels:
                diff = self._labels[rel_label] - addr
                if size == 1:
                    inst.code = inst.code[:len(inst.code) - 1] + struct.pack('b', diff)
                else:
                    inst.code = inst.code[:len(inst.code) - 4] + struct.pack('i', diff)
                inst.rel_label = None


def translate(source: str, standalone: bool=True, force_avx512: bool=False) -> MachineCode:
    """
    Translate asm source to x86 machine code.
    #TODO simple example of source
    """
    assembler = Tdasm()
    return assembler.translate(source, standalone=standalone, force_avx512=force_avx512)
