
"""
.. module:: lex
.. moduleauthor:: Mario Vidov <mvidov@yahoo.com>


"""

import struct
from .holders import Instruction, RegOperand, MemOperand, NameOperand,\
    ConstOperand, LabelOperand, EncodedInstruction
from .insts import find_instruction_params, vex_encoding_needed, evex_encoding_needed, opmask_encoding_needed
from .regs import registers, registers_64bit, registers_avx512


class Encoder:
    def __init__(self, force_avx512: bool=False):
        self._force_avx512 = force_avx512
        self._digits = frozenset(['/0', '/1', '/2', '/3', '/4', '/5', '/6', '/7'])
        self._new_avx512_regs = frozenset(['k0', 'k1', 'k2', 'k3', 'k4', 'k5', 'k6', 'k7',
                                  'zmm0', 'zmm1', 'zmm2', 'zmm3', 'zmm4', 'zmm5',
                                  'zmm6', 'zmm7', 'zmm8', 'zmm9', 'zmm10', 'zmm11',
                                  'zmm12', 'zmm13', 'zmm14', 'zmm15', 'zmm16', 'zmm17',
                                  'zmm18', 'zmm19', 'zmm20', 'zmm21', 'zmm22', 'zmm23',
                                  'zmm24', 'zmm25', 'zmm26', 'zmm27', 'zmm28', 'zmm29',
                                  'zmm30', 'zmm31', 'zmm32'])

        self._addr_regs = frozenset(['rax', 'rbx', 'rcx', 'rdx', 'rsp', 'rbp',
                                     'rsi', 'rdi', 'r8', 'r9', 'r10', 'r11',
                                     'r12', 'r13', 'r14', 'r15'])

        self._reg_complement = {7: 8, 6: 9, 5: 10, 4: 11, 3: 12, 2: 13,
                                1: 14, 0: 15, 8: 7, 9: 6, 10: 5, 11: 4, 12: 3,
                                13: 2, 14: 1, 15: 0}

        self._reg32_complement = {31:0, 30:1, 29:2, 28:3, 27:4, 26:5, 25:6,
                                  24:7, 23:8, 22:9, 21:10, 20:11, 19:12, 18:13,
                                  17:14, 16:15, 15:16, 14:17, 13:18, 12:19,
                                  11:20, 10:21, 9:22, 8:23, 7:24, 6:25, 5:26,
                                  4:27, 3:28, 2:29, 1:30, 0:31}

    def encode(self, instruction: Instruction):
        params = find_instruction_params(instruction)

        if opmask_encoding_needed(instruction.name):
            return self._encode_vex(instruction, params)
        if evex_encoding_needed(instruction.name):
            return self._encode_evex(instruction, params)
        if self._force_avx512 and 'evex' in params:
            return self._encode_evex(instruction, params)

        if vex_encoding_needed(instruction.name):
            if self._evex_needed(instruction, params):
                if 'evex' in params:
                    return self._encode_evex(instruction, params)
                else:
                    raise ValueError("Instruction %s is not encodable using AVX-512 encoding format!" % instruction.name)
            if 'mbr' in params:
                raise ValueError("Instruction %s is not encodable using AVX encoding format!" % instruction.name)
            return self._encode_vex(instruction, params)
        return self._encode(instruction, params)

    def _evex_needed(self, instruction, params):
        if 'mbr' in params:
            return True
        if isinstance(instruction.op1, RegOperand):
            if instruction.op1.reg in self._new_avx512_regs:
                return True
            if instruction.op1.reg in registers_avx512:
                return True
        if isinstance(instruction.op2, RegOperand):
            if instruction.op2.reg in self._new_avx512_regs:
                return True
            if instruction.op2.reg in registers_avx512:
                return True
        if isinstance(instruction.op3, RegOperand):
            if instruction.op3.reg in self._new_avx512_regs:
                return True
            if instruction.op3.reg in registers_avx512:
                return True
        return False

    def _evex_mmmm(self, params):
        vex_mmmm = 1
        if "mmmm" in params:
            if params["mmmm"] == "0F":
                vex_mmmm = 1
            elif params["mmmm"] == "0F38":
                vex_mmmm = 2
            elif params["mmmm"] == "0F3A":
                vex_mmmm = 3
        return vex_mmmm

    def _encode_evex(self, instruction, params):
        inst = EncodedInstruction(instruction.name)
        rexr = rexrr = rexx = rexb = False

        rexw = 0
        if "W512" in params:
            if params["W512"]  == "W1":
                rexw = 1
        else:
            if "W" in params and params["W"] == "W1":
                rexw = 1

        vex_l, vex_ll = 0, 0
        if "L" in params and params["L"] == "256":
            vex_l, vex_ll = 1, 0
        if "L" in params and params["L"] == "512":
            vex_l, vex_ll = 0, 1

        opcode, rexb = self._encode_opcode(instruction, params)

        modrm = b''
        rel_name = None
        disp = b''
        if 'mod' in params:
            modrm, disp, rexr, rexrr, rexb2, rexx, rel_name = self._encode_modrm(instruction, params)
            rexb = rexb or rexb2

        vex_vvvv = 0xF
        vex_vvvv_v = 1
        if 'vvvv' in params:
            vex_vvvv, vex_vvvv_v = self._encode_vvvv(instruction, params)

        pp_c = {'None': 0, '66': 1, 'F3': 2, 'F2': 3}
        vex_pp = pp_c[params['pp']] if 'pp' in params else 0

        vex_mmmm = self._evex_mmmm(params)

        # TODO -- limit immediate to byte size and add support for is4+imm combined
        if 'is4' in params:
            if 'imm' in params:
                raise ValueError("is4 and imm combined not supported yet!")
            imm = self._encode_is4_imm(instruction)
        else:
            imm = self._encode_immediate(instruction, params)

        rr = 0 if rexr else 1
        rb = 0 if rexb else 1
        rx = 0 if rexx else 1
        rrr = 0 if rexrr else 1

        vex1 = b"\x62"

        vex2 = (rr << 7) | (rx << 6) | (rb << 5) | (rrr << 4) | vex_mmmm
        vex2 = struct.pack("B", vex2)

        vex3 = (rexw << 7) | (vex_vvvv << 3) | (1 << 2) | vex_pp
        vex3 = struct.pack("B", vex3)

        aaa = 0
        if hasattr(instruction.op1, 'op_mask') and instruction.op1.op_mask is not None:
            k = {'k0': 0, 'k1': 1, 'k2': 2, 'k3': '3', 'k4': 4, 'k5': 5, 'k6': 6, 'k7': 7}
            aaa = k[instruction.op1.op_mask]
        zero = 0
        if hasattr(instruction.op1, 'op_zero') and instruction.op1.op_zero:
            zero = 1

        # memory broadcast
        br = 0
        if 'mbr' in params:
            br = 1

        vex4 = (zero << 7) | (vex_ll << 6) | (vex_l << 5) | (br << 4) | (vex_vvvv_v << 3) | aaa
        vex4 = struct.pack("B", vex4)

        evex = vex1 + vex2 + vex3 + vex4

        if rel_name is not None:
            inst.disp_offset = len(evex) + len(opcode) + len(modrm)
            inst.mem_name = rel_name

        inst.code = evex + opcode + modrm + disp + imm
        return inst

    def _encode_vex(self, instruction, params):

        inst = EncodedInstruction(instruction.name)
        rexr = rexx = rexb = False

        two_byte = False  # two or three byte VEX

        rexw = 0
        if "W" in params and params["W"] == "WIG":
            two_byte = True
        if "W" in params and params["W"] == "W1":
            two_byte = False
            rexw = 1

        # NOTE: if LIG is present vex_l can be 0 or 1, if LZ is present vex_l must be zero
        vex_l = 0
        if "L" in params and params["L"] == "256":
            vex_l = 1

        opcode, rexb = self._encode_opcode(instruction, params)

        modrm = b''
        rel_name = None
        disp = b''
        if 'mod' in params:
            modrm, disp, rexr, _, rexb2, rexx, rel_name = self._encode_modrm(instruction, params)
            rexb = rexb or rexb2
            if rexb is True or rexx is True:
                two_byte = False

        vex_vvvv = 0xF
        if 'vvvv' in params:
            vex_vvvv, _ = self._encode_vvvv(instruction, params)

        pp_c = {'None': 0, '66': 1, 'F3': 2, 'F2': 3}
        vex_pp = pp_c[params['pp']] if 'pp' in params else 0

        vex_mmmm, two_byte = self._encode_mmmm(params, two_byte)

        # TODO -- limit immediate to byte size and add support for is4+imm combined
        if 'is4' in params:
            if 'imm' in params:
                raise ValueError("is4 and imm combined not supported yet!")
            imm = self._encode_is4_imm(instruction)
        else:
            imm = self._encode_immediate(instruction, params)

        if two_byte:
            vex1 = b"\xC5"
            rr = 0 if rexr else 1
            vex2 = (rr << 7) | (vex_vvvv << 3) | (vex_l << 2) | vex_pp
            vex2 = struct.pack("B", vex2)
            vex = vex1 + vex2
        else:
            vex1 = b"\xC4"
            rr = 0 if rexr else 1
            rb = 0 if rexb else 1
            rx = 0 if rexx else 1

            vex2 = (rr << 7) | (rx << 6) | (rb << 5) | vex_mmmm
            vex2 = struct.pack("B", vex2)

            vex3 = (rexw << 7) | (vex_vvvv << 3) | (vex_l << 2) | vex_pp
            vex3 = struct.pack("B", vex3)
            vex = vex1 + vex2 + vex3

        if rel_name is not None:
            inst.disp_offset = len(vex) + len(opcode) + len(modrm)
            inst.mem_name = rel_name

        inst.code = vex + opcode + modrm + disp + imm
        return inst

    def _encode(self, instruction, params):

        inst = EncodedInstruction(instruction.name)

        rep_prefix = self._encode_repeat_prefix(instruction.repeat)  # REPEAT instruction prefix
        op_prefix = self._encode_operand_prefix(params)
        lock_prefix = self._encode_lock_prefix(instruction.lock)  # LOCK instruction prefix

        rexw = self._rexw_prefix_needed(params)
        rexr = rexx = rexb = False

        opcode, rexb = self._encode_opcode(instruction, params)
        modrm = b''
        rel_name = None
        disp = b''
        if 'mod' in params:
            modrm, disp, rexr, _,rexb2, rexx, rel_name = self._encode_modrm(instruction, params)
            rexb = rexb or rexb2
        imm = self._encode_immediate(instruction, params)

        lbl = b''
        if isinstance(instruction.op1, LabelOperand):
            if instruction.op1.value is None:
                vals = {'cb': 1, 'cd': 4}
                size = vals[params['code_offset']]
                inst.rel_label = (instruction.op1.label, size)
            lbl = self._encode_label(instruction.op1, params, len(op_prefix) + len(opcode))

        rex = self._encode_rex(instruction, rexr, rexw, rexb, rexx)

        if rel_name is not None:
            inst.disp_offset = len(rep_prefix) + len(op_prefix) + len(rex) + len(opcode) + len(modrm)
            inst.mem_name = rel_name

        if opcode[:1] in (b'\x66', b'\xF2', b'\xF3'):
            inst.code = lock_prefix + rep_prefix + op_prefix + opcode[:1] + rex + opcode[1:] + modrm + disp + imm + lbl
        else:
            inst.code = lock_prefix + rep_prefix + op_prefix + rex + opcode + modrm + disp + imm + lbl

        return inst

    def _encode_repeat_prefix(self, repeat):
        if repeat is None:
            return b''

        if repeat in ("rep", "repe", "repz"):
            return b"\xF3"
        elif repeat in ("repne", "repnz"):
            return b"\xF2"
        else:
            raise ValueError("Unsupported repeat prefix. Prefix = ", repeat)

    def _encode_lock_prefix(self, lock):
        if lock:
            return b"\xF0"
        else:
            return b''

    def _encode_operand_prefix(self, params):
        if 'prefix' in params and params['prefix'] == '66':
            return b"\x66"
        return b''

    def _rexw_prefix_needed(self, params):
        if 'prefix' in params and params['prefix'] == 'REX.W':
            return True
        return False

    def _encode_opcode(self, instruction, params):
        if 'post' not in params:
            return self._transform_to_bytes(params['opcode']), False

        # NOTE post can only contain ['+rb', '+rw', '+rd', '+ro', '+i']
        # Logic for all this values is same so we don't need to examine specific value

        if not isinstance(instruction.op1, RegOperand):
            raise ValueError("Operand for %s instruction must be register.", instruction.name)

        op = instruction.op1
        if instruction.op1.reg in ('al', 'ax', 'eax', 'rax', 'st0'):
            if isinstance(instruction.op2, RegOperand):
                op = instruction.op2

        if op.reg in registers_avx512:
            rexb = registers_avx512[op.reg][3] > 7
        else:
            rexb = op.reg in registers_64bit
        opcode = self._transform_to_bytes(params['opcode'], registers[op.reg][3])
        return opcode, rexb

    def _encode_modrm(self, instruction, params):

        rexr = rexrr = rexb = rexx = False
        op1 = instruction.op1
        op2 = instruction.op2
        if 'vvvv' in params:
            vvvv = params['vvvv']
            if vvvv == 'NDS':
                op2 = instruction.op3
            elif vvvv == 'DDS':
                op2 = instruction.op3
            elif vvvv == 'NDD':
                op1 = instruction.op2

        rel_name = None
        disp = b''

        if op1 is None:
            raise ValueError("First operand cannot be None!", instruction.name)

        if op2 is not None:
            if isinstance(op1, (NameOperand, MemOperand)) and isinstance(op2, (NameOperand, MemOperand)):
                raise ValueError("Instruction %s cannot have two memory operands" % instruction.name)

        if params['mod'] == '/r':
            if op2 is None:
                raise ValueError('Second operand is missing for %s instruction' % instruction.name)
            if isinstance(op1, RegOperand) and isinstance(op2, RegOperand):
                # NOTE default value of rm is 2
                if 'rm' in params and params['rm'] == '1':
                    op1, op2 = op2, op1

                if op1.reg in registers_avx512:
                    rexrr = True
                    rexr = registers_avx512[op1.reg][3] > 7
                else:
                    rexrr = False
                    rexr = op1.reg in registers_64bit

                if op2.reg in registers_avx512:
                    rexb = registers_avx512[op2.reg][3] > 7
                else:
                    rexb = op2.reg in registers_64bit

                rexx = op2.reg in registers_avx512
                modrm = self._encode_rm(registers[op2.reg][3], 3, registers[op1.reg][3])
            elif isinstance(op1, RegOperand):
                rexr = op1.reg in registers_64bit
                rexrr = op1.reg in registers_avx512
                modrm, disp, rexb, rexx, rel_name = self._encode_rm_sib(op2, registers[op1.reg][3])
            elif isinstance(op2, RegOperand):
                if op2.reg in registers_avx512:
                    rexrr = True
                    rexr = registers_avx512[op2.reg][3] > 7
                else:
                    rexrr = False
                    rexr = op2.reg in registers_64bit
                modrm, disp, rexb, rexx, rel_name = self._encode_rm_sib(op1, registers[op2.reg][3])
            else:
                raise ValueError("Wrong operand types for % instruction" % instruction.name)

        elif params['mod'] in self._digits:
            digit = int(params['mod'][1])
            if isinstance(op1, RegOperand):
                if op1.reg in registers_avx512:
                    rexb = registers_avx512[op1.reg][3] > 7
                else:
                    rexb = op1.reg in registers_64bit
                modrm = self._encode_rm(registers[op1.reg][3], 3, digit)
            elif isinstance(op1, (NameOperand, MemOperand)):
                modrm, disp, rexb, rexx, rel_name = self._encode_rm_sib(op1, digit)
            else:
                raise ValueError("Unsuported first operand type for %s instruction" % instruction.name, op1)
        else:
            raise ValueError("Unsuported value in mod parameter of %s instruction." % instruction.name)

        return modrm, disp, rexr, rexrr, rexb, rexx, rel_name

    def _encode_rm_sib(self, op, digit):

        if not isinstance(op, (NameOperand, MemOperand)):
            raise ValueError("Memory operand is expected for ModRM encoding.", op)

        rexb = rexx = False
        rel_name = None

        if isinstance(op, NameOperand):
            # NOTE indirect memory access [mem] or [mem + 48]
            rel_name = op.name
            if op.displacement is None:
                disp = b'\x00\x00\x00\x00'
            else:
                disp = struct.pack('i', op.displacement)
            modrm_sib = self._encode_rm(5, 0, digit)
        else:
            if op.scaled_reg is None:
                # NOTE this is for [rax] or [rax + 8] cases
                if op.reg not in self._addr_regs:
                    raise ValueError("Wrong address registers %s" % op.reg)
                disp = op.displacement
                if (op.reg == 'rbp' or op.reg == 'r13') and disp is None:
                    disp = 0
                sib = b''
                if op.reg == 'rsp' or op.reg == 'r12':
                    sib = self._encode_sib(4, 0, 4)

                mod, disp = self._encode_disp(disp)
                rexb = op.reg in registers_64bit
                modrm_sib = self._encode_rm(registers[op.reg][3], mod, digit) + sib
            else:
                # NOTE [rax + rbx] or [4*rcx + rbx] or [2*rax + rdx + 28] cases
                if op.reg not in self._addr_regs:
                    raise ValueError("Wrong address register %s" % op.reg)

                if op.scaled_reg not in self._addr_regs:
                    raise ValueError("Wrong scaled register %s" % op.scaled_reg)

                scale = 1 if op.scale is None else op.scale
                disp = op.displacement
                if (op.reg == 'rbp' or op.reg == 'r13') and disp is None:
                    disp = 0

                scale_maping = {1: 0, 2: 1, 4: 2, 8: 3}
                sib = self._encode_sib(registers[op.scaled_reg][3],
                                       scale_maping[scale], registers[op.reg][3])
                mod, disp = self._encode_disp(disp)
                rexb = op.reg in registers_64bit
                rexx = op.scaled_reg in registers_64bit
                modrm_sib = self._encode_rm(4, mod, digit) + sib

        return modrm_sib, disp, rexb, rexx, rel_name

    def _transform_to_bytes(self, text: str, increment: int=None):
        """Transform text to bytes and if needed add increment."""

        by = b""
        for n in range(0, len(text) - 2, 2):
            ch = text[n:n + 2]
            by += struct.pack('B', int(ch, 16))

        ch = text[len(text) - 2:]
        if increment is not None:
            by += struct.pack('B', int(ch, 16) + increment)
        else:
            by += struct.pack('B', int(ch, 16))
        return by

    def _encode_rm(self, rm, mod, digit):
        modrm = (mod << 6) | (digit << 3) | rm
        return struct.pack('B', modrm)

    def _encode_sib(self, index, scale, base):
        sib = (scale << 6) | (index << 3) | base
        return struct.pack('B', sib)

    def _encode_disp(self, disp=None):
        if disp is None:
            return 0, b''

        # TODO AVX512 -- compressed disp8 encoding missing
        # if disp < 128 and disp > -129:
        #     return 1, struct.pack('b', disp)
        # elif disp < 2147483648 and disp > -2147483649:
        #     return 2, struct.pack('i', disp)
        # else:
        #     raise ValueError("Unallowed displacement values %s." % str(disp))

        if disp < 2147483648 and disp > -2147483649:
            return 2, struct.pack('i', disp)
        else:
            raise ValueError("Unallowed displacement values %s." % str(disp))

    def _encode_is4_imm(self, instruction):
        if instruction.op4 is None:
            raise ValueError("When is4 is defined we must have 4-operand instruction")

        if not isinstance(instruction.op4, RegOperand):
            raise ValueError("When is4 is define 4-operand must be register.", instruction.op4)

        value = registers[instruction.op4.reg][3]
        if instruction.op4.reg in registers_64bit:
            value += 8
        value = value << 4
        imm = self.pack_immediate(1, value)
        return imm

    def _encode_immediate(self, instruction, params):
        if 'imm' not in params:
            return b''
        vals = {'ib': 1, 'iw': 2, 'id': 4, 'io': 8}
        size = vals[params['imm']]
        value = None
        if instruction.op1 is not None and isinstance(instruction.op1, ConstOperand):
            value = instruction.op1.value
        elif instruction.op2 is not None and isinstance(instruction.op2, ConstOperand):
            value = instruction.op2.value
        elif instruction.op3 is not None and isinstance(instruction.op3, ConstOperand):
            value = instruction.op3.value
        elif instruction.op4 is not None and isinstance(instruction.op4, ConstOperand):
            value = instruction.op4.value

        if value is None:
            raise ValueError('Immediate operand is missing.')
        if not isinstance(value, int):
            raise ValueError("Immediate operand can only be integer.", value)

        imm = self.pack_immediate(size, value)
        return imm

    def _encode_label(self, lbl_op, params, ins_size):

        value = lbl_op.value
        if value is None:
            value = 0

        vals = {'cb': 1, 'cd': 4}
        size = vals[params['code_offset']]
        if value < 0:
            value -= ins_size + size

        lbl = self.pack_immediate(size, value)
        return lbl

    def _encode_rex(self, instruction, rexr, rexw, rexb, rexx):
        ret = rexr or rexw or rexb or rexx
        if ret is False:
            return b''

        regs = ("ah", "bh", "ch", "dh")
        if isinstance(instruction.op1, RegOperand) and instruction.op1.reg in regs:
            raise ValueError("ah, b, ch, dh registers not encodable if REX prefix is used.")
        if isinstance(instruction.op2, RegOperand) and instruction.op2.reg in regs:
            raise ValueError("ah, b, ch, dh registers not encodable if REX prefix is used.")

        rw = int(rexw)
        rr = int(rexr)
        rx = int(rexx)
        rb = int(rexb)

        rex_value = (4 << 4) | (rw << 3) | (rr << 2) | (rx << 1) | rb
        rex = struct.pack('B', rex_value)

        return rex

    def _encode_mmmm(self, params, two_byte):
        vex_mmmm = 1
        if "mmmm" in params:
            if params["mmmm"] == "0F":
                vex_mmmm = 1
            elif params["mmmm"] == "0F38":
                vex_mmmm = 2
                two_byte = False
            elif params["mmmm"] == "0F3A":
                vex_mmmm = 3
                two_byte = False
        return vex_mmmm, two_byte

    def _encode_vvvv(self, instruction, params):
        vvvv = params['vvvv']
        vex_vvvv_v = 1

        if vvvv == 'NDS':
            op = instruction.op2
        elif vvvv == 'DDS':
            op = instruction.op2
        elif vvvv == 'NDD':
            op = instruction.op1
        else:
            raise ValueError("Unsupported value for vvvv param! ", vvvv)

        if op.reg in registers_avx512:
            tmp = self._reg32_complement[registers_avx512[op.reg][3] + 16]
            vex_vvvv = tmp & 0xF
            vex_vvvv_v = (tmp >> 4) & 1
        elif op.reg in registers_64bit:
            vex_vvvv = self._reg_complement[registers_64bit[op.reg][3] + 8]
        else:
            vex_vvvv = self._reg_complement[registers[op.reg][3]]
        return vex_vvvv, vex_vvvv_v

    def pack_immediate(self, size, value):
        if size == 1:
            if value < 0:
                immediate = struct.pack("b", value)
            else:
                immediate = struct.pack("B", value)
        elif size == 2:
            if value < 0:
                immediate = struct.pack("h", value)
            else:
                immediate = struct.pack("H", value)
        elif size == 4:
            if value < 0:
                immediate = struct.pack("i", value)
            else:
                immediate = struct.pack("I", value)
        elif size == 8:
            if value < 0:
                immediate = struct.pack("q", value)
            else:
                immediate = struct.pack("Q", value)
        return immediate
