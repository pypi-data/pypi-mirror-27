
"""
.. module:: parser
.. moduleauthor:: Mario Vidov <mvidov@yahoo.com>


"""

from .regs import registers
from .holders import Directive, Label, Keyword, DataMember, ArrayMember,\
    DataMembers, RegOperand, MemOperand, NameOperand, ConstOperand,\
    Instruction, LabelOperand, KeywordOperand


class SyntaxError(Exception):
    def __init__(self, msg: str, tokens: list):
        self.msg = msg
        self.tokens = tokens

    def __str__(self):
        text = ''
        ln_num = 0
        for tk_type, tk_val, ln in self.tokens:
            text += tk_val
            ln_num = ln
        line = ' Line %i:' % ln_num
        return self.msg + line + text


class Parser:
    """ Examples of content in data section:
            #DATA
            ;this is comment
            uint8 a1, a2
            float val1
            double val2 = 0.8 ;comment
            uint64 end ;end is keyword but can also be a variable
            uint32 array[16]
            float array2[4] = -1.0, -1.0, -1.0, -1.0

            struct ray
            float dir[4]
            float origin[4]
            end ; end of structure

        Examples of content in code section:
            #CODE
            fsin
            this_is_label:
            global this_is_global_label:
            mov bl, al
            mov dword [eax + 16 + 20], edx
            mov dword [eax + ebx + 16 + 20], edx
            mov eax, 3333
            movaps oword [eax + ray.dir], xmm1
            add dword [eax], sizeof ray
            #END
    """

    def __init__(self):
        self._dtypes = frozenset(('byte', 'word', 'dword', 'qword',
                                  'tbyte', 'dqword', 'oword', 'yword', 'zword'))

    def parse(self, tokens: list, in_code_section: bool):
        "Parse array of tokens."

        self._tokens = tokens
        self._gen = self._make_generator()

        if in_code_section:
            return self._parse_code_sec()
        else:
            return self._parse_data_sec()

    def _make_generator(self):
        for token in self._tokens:
            yield token

    def _next(self):
        try:
            return next(self._gen)
        except StopIteration:
            return ('empty', None, 0)

    def _consume_spaces(self):
        tk_type, tk_val, ln = self._next()
        while tk_type == 'space':
            tk_type, tk_val, ln = self._next()
        return tk_type, tk_val, ln

    def _parse_data_sec(self):

        tk_type, tk_val, ln = self._consume_spaces()
        if tk_type == 'empty' or tk_type == 'comment':
            return
        elif tk_type == 'directive':
            return self._parse_directive(tk_val)
        elif tk_type == 'keyword':
            return self._parse_data_keyword(tk_val)
        elif tk_type == 'iden':
            return self._parse_data_iden(tk_val)
        else:
            raise SyntaxError('Syntax error in data section!', self._tokens)

    def _parse_code_sec(self):
        tk_type, tk_val, ln = self._consume_spaces()
        if tk_type == 'empty' or tk_type == 'comment':
            return
        elif tk_type == 'directive':
            return self._parse_directive(tk_val)
        elif tk_type == 'label':
            return self._parse_label(tk_val)
        elif tk_type == 'keyword':
            return self._parse_code_keyword(tk_val)
        elif tk_type == 'iden':
            return self._parse_code_iden(tk_val)
        else:
            raise SyntaxError('Syntax error in code section!', self._tokens)

    def _parse_directive(self, tk_value: str):
        directive = Directive(tk_value[1:].upper())
        self._check_end_of_line()
        return directive

    def _parse_label(self, tk_value: str):
        label = Label(tk_value)
        self._check_end_of_line()
        return label

    def _parse_data_keyword(self, tk_value: str):
        tk_type, tk_val, ln = self._consume_spaces()
        if tk_type == 'empty' or tk_type == 'comment':
            return Keyword(tk_value)
        elif tk_type == 'iden':
            keyword = Keyword(tk_value, tk_val)
        else:
            raise SyntaxError('Identifier expected after %s keyword.' % tk_value, self._tokens)
        self._check_end_of_line()
        return keyword

    def _parse_code_keyword(self, tk_value: str):
        tk_type, tk_val, ln = self._consume_spaces()
        if tk_type != 'label':
            raise SyntaxError('Label expected', self._tokens)
        keyword = Keyword(tk_value, tk_val)
        self._check_end_of_line()
        return keyword

    def _parse_data_iden(self, tk_value: str):
        mem_type = tk_value
        tk_type, tk_val, ln = self._consume_spaces()
        if tk_type != 'iden' and tk_type != 'keyword':
            raise SyntaxError('Identifier expected after %s data type.' % tk_value, self._tokens)
        mem_name = tk_val
        tk_type, tk_val, ln = self._consume_spaces()
        if tk_type == 'empty' or tk_type == 'comment':
            return DataMembers([DataMember(mem_name, mem_type)])
        elif tk_type == 'comma':
            return self._parse_multiple_data_members(mem_name, mem_type)
        elif tk_type == 'lbracket':
            return self._parse_array_member(mem_name, mem_type)
        elif tk_type == 'equal':
            return self._parse_data_member_value(mem_name, mem_type)
        else:
            raise SyntaxError('Wrong data member declaration.', self._tokens)

    def _parse_code_iden(self, tk_value: str):
        repeat = None
        lock = False
        if tk_value in ("rep", "repe", "repz", "repne", "repnz", "lock"):
            if tk_value == 'lock':
                lock = True
            else:
                repeat = tk_value
            tk_type, tk_value, ln = self._consume_spaces()
            if tk_type != 'iden':
                raise SyntaxError('Wrong instruction declaration.', self._tokens)

        name = tk_value
        op1 = self._parse_code_operand()
        if op1 is None:
            return Instruction(name, repeat=repeat, lock=lock)
        op2 = self._parse_code_operand()
        if op2 is None:
            return Instruction(name, op1=op1, repeat=repeat, lock=lock)
        op3 = self._parse_code_operand()
        if op3 is None:
            return Instruction(name, op1=op1, op2=op2, repeat=repeat, lock=lock)
        op4 = self._parse_code_operand()
        if op4 is None:
            return Instruction(name, op1=op1, op2=op2, op3=op3, repeat=repeat, lock=lock)
        return Instruction(name, op1=op1, op2=op2, op3=op3, op4=op4, repeat=repeat, lock=lock)

    def _parse_code_operand(self):
        def check_comma():
            tk_type, tk_val, ln = self._consume_spaces()
            if tk_type != 'comma' and tk_type not in ('empty', 'comment'):
                raise SyntaxError('Wrong operand declaration.', self._tokens)

        tk_type, tk_val, ln = self._consume_spaces()
        if tk_type == 'empty' or tk_type == 'comment':
            return None
        elif tk_type == 'iden':
            if tk_val in self._dtypes:
                mem_operand = self._parse_mem_operand(tk_val)
                check_comma()
                return mem_operand
            elif tk_val in registers:
                #check_comma()
                tk_type1, tk_val1, ln1 = self._consume_spaces()
                if tk_type1 == 'lcurly':
                    return self._parse_reg_with_masks(tk_val)
                if tk_type1 != 'comma' and tk_type1 not in ('empty', 'comment'):
                    raise SyntaxError('Wrong operand declaration.', self._tokens)
                return RegOperand(tk_val)
            else:
                check_comma()
                return LabelOperand(tk_val)
        elif tk_type in ('num', 'float'):
            val = self._parse_value(tk_type, tk_val)
            check_comma()
            return ConstOperand(val)
        elif tk_type in ('minus', 'plus'):
            prefix = tk_val
            tk_type, tk_val, ln = self._consume_spaces()
            if tk_type in ('float', 'num'):
                val = self._parse_value(tk_type, tk_val, prefix)
                check_comma()
                return ConstOperand(val)
            else:
                raise SyntaxError('Wrong operand declaration.', self._tokens)
        elif tk_type == 'keyword' and tk_val == 'sizeof':  # sizeof ray
            tk_type, tk_val, ln = self._consume_spaces()
            if tk_type == 'iden':
                check_comma()
                return KeywordOperand('sizeof', tk_val)
            else:
                raise SyntaxError('Wrong operand declaration.', self._tokens)
        elif tk_type == 'keyword' and tk_val == 'end':
            check_comma()
            return LabelOperand(tk_val)
        else:
            raise SyntaxError('Wrong operand declaration.', self._tokens)

    def _parse_mem_operand(self, data_type: str):
        tk_type, tk_val, ln = self._consume_spaces()
        if tk_type != 'lbracket':
            raise SyntaxError('Wrong operand declaration.', self._tokens)

        reg = scaled_reg = name = scale = displacement = struct_member = None

        prev_type = tk_type
        prev_val = tk_val

        while True:
            tk_type, tk_val, ln = self._consume_spaces()
            if tk_type == 'rbracket':
                if prev_type not in ('iden', 'float', 'num'):
                    raise SyntaxError('Wrong operand declaration.', self._tokens)
                if name is None and reg is None:
                    raise SyntaxError('Wrong operand declaration.', self._tokens)
                if name is not None and (reg is not None or scaled_reg is not None):
                    if '.' in name:
                        struct_member = name
                        name = None
                    else:
                        raise SyntaxError('Wrong operand declaration.', self._tokens)
                break
            elif tk_type == 'empty' or tk_type == 'comment':
                raise SyntaxError('Wrong operand declaration.', self._tokens)
            elif tk_type == 'iden':
                if prev_type not in ('lbracket', 'plus', 'minus', 'mul'):
                    raise SyntaxError('Wrong operand declaration.', self._tokens)
                if prev_type == 'mul':
                    if tk_val not in registers:
                        raise SyntaxError('Wrong operand declaration.', self._tokens)
                    if scaled_reg is not None:
                        raise SyntaxError('Wrong operand declaration.', self._tokens)
                    scaled_reg = tk_val
                else:
                    if tk_val in registers:
                        if reg is None:
                            reg = tk_val
                        elif scaled_reg is None:
                            scaled_reg = tk_val
                        else:
                            raise SyntaxError('Wrong operand declaration.', self._tokens)
                    else:
                        if name is None:
                            name = tk_val
                        else:
                            raise SyntaxError('Wrong operand declaration.', self._tokens)
            elif tk_type == 'plus':
                if prev_type not in ('iden', 'float', 'num'):
                    raise SyntaxError('Wrong operand declaration.', self._tokens)
            elif tk_type == 'minus':
                raise SyntaxError('minus operand NOT YET implemented.', self._tokens)
            elif tk_type == 'mul':
                if prev_type not in ('iden', 'float', 'num'):
                    raise SyntaxError('Wrong operand declaration.', self._tokens)
                if prev_type == 'iden' and prev_val not in registers:
                    raise SyntaxError('Wrong operand declaration.', self._tokens)

                if prev_type == 'iden':  # scaled_reg
                    if reg is None:
                        raise SyntaxError('Wrong operand declaration.', self._tokens)
                    if scaled_reg is not None and reg is None:
                        raise SyntaxError('Wrong operand declaration.', self._tokens)

                    if scaled_reg is None:
                        scaled_reg = reg
                        reg = None
                else:  # float, num
                    val = self._parse_value(prev_type, prev_val)
                    if not isinstance(val, int):
                        raise SyntaxError('Wrong operand declaration.', self._tokens)
                    if displacement is None:
                        raise SyntaxError('Wrong operand declaration.', self._tokens)
                    if scale is not None:
                        raise SyntaxError('Wrong operand declaration.', self._tokens)
                    scale = val
                    displacement -= val
                    if displacement == 0:
                        displacement = None
            elif tk_type == 'float' or tk_type == 'num':
                if prev_type not in ('lbracket', 'plus', 'minus', 'mul'):
                    raise SyntaxError('Wrong operand declaration.', self._tokens)
                if prev_type == 'minus':
                    val = self._parse_value(tk_type, tk_val, prefix='-')
                else:
                    val = self._parse_value(tk_type, tk_val)
                if not isinstance(val, int):
                    raise SyntaxError('Wrong operand declaration.', self._tokens)
                if prev_type == 'mul':
                    if scale is not None:
                        raise SyntaxError('Wrong operand declaration.', self._tokens)
                    scale = val
                else:
                    if displacement is None:
                        displacement = 0
                    displacement += val
            else:
                raise SyntaxError('Wrong operand declaration.', self._tokens)

            prev_type = tk_type
            prev_val = tk_val

        if name is not None:
            return NameOperand(name, data_type, displacement=displacement,
                               struct_member=struct_member)
        else:
            return MemOperand(reg, data_type, scaled_reg=scaled_reg, scale=scale,
                              displacement=displacement, struct_member=struct_member)

    def _parse_multiple_data_members(self, mem_name: str, mem_type: str):
        members = [DataMember(mem_name, mem_type)]
        while True:
            tk_type, tk_val, ln = self._consume_spaces()
            if tk_type == 'iden' or tk_type == 'keyword':
                members.append(DataMember(tk_val, mem_type))
            elif tk_type == 'empty' or tk_type == 'comment':
                return DataMembers(members)
            else:
                raise SyntaxError('Wrong data member declaration.', self._tokens)

            tk_type, tk_val, ln = self._consume_spaces()
            if tk_type == 'empty' or tk_type == 'comment':
                return DataMembers(members)
            elif tk_type != 'comma':
                raise SyntaxError('Comma is expected to separate data members.', self._tokens)

    def _parse_array_member(self, mem_name: str, mem_type: str):
        tk_type, tk_val, ln = self._consume_spaces()
        if tk_type != 'num' and tk_type != 'float':
            raise SyntaxError('Array length is expected.', self._tokens)
        if not tk_val.isdigit():
            raise SyntaxError('Array length must be integer.', self._tokens)
        length = int(tk_val)
        tk_type, tk_val, ln = self._consume_spaces()
        if tk_type != 'rbracket':
            raise SyntaxError('Right bracket is expected.', self._tokens)
        tk_type, tk_val, ln = self._consume_spaces()
        if tk_type == 'empty' or tk_type == 'comment':
            return DataMembers([ArrayMember(mem_name, mem_type, length)])
        elif tk_type == 'equal':
            return self._parse_array_member_values(mem_name, mem_type, length)
        else:
            raise SyntaxError('Wrong array data member declaration.', self._tokens)

    def _parse_array_member_values(self, mem_name: str, mem_type: str, length: int):
        values = []
        while True:
            tk_type, tk_val, ln = self._consume_spaces()
            if tk_type in ('string', 'float', 'num'):
                values.append(self._parse_value(tk_type, tk_val))
            elif tk_type in ('minus', 'plus'):
                prefix = tk_val
                tk_type, tk_val, ln = self._consume_spaces()
                if tk_type in ('string', 'float', 'num'):
                    values.append(self._parse_value(tk_type, tk_val, prefix))
                else:
                    raise SyntaxError('Array value expected.', self._tokens)
            else:
                raise SyntaxError('Array value expected.', self._tokens)

            tk_type, tk_val, ln = self._consume_spaces()
            if tk_type == 'empty' or tk_type == 'comment':
                return DataMembers([ArrayMember(mem_name, mem_type, length, values)])
            elif tk_type == 'comma':
                continue
            else:
                raise SyntaxError('Array values must be spearated with comma.', self._tokens)

    def _parse_data_member_value(self, mem_name: str, mem_type: str):
        tk_type, tk_val, ln = self._consume_spaces()
        if tk_type in ('string', 'float', 'num'):
            value = self._parse_value(tk_type, tk_val)
        elif tk_type in ('minus', 'plus'):
            prefix = tk_val
            tk_type, tk_val, ln = self._consume_spaces()
            if tk_type in ('string', 'float', 'num'):
                value = self._parse_value(tk_type, tk_val, prefix)
            else:
                raise SyntaxError('Wrong data member declaration.', self._tokens)
        else:
            raise SyntaxError('Wrong data member declaration.', self._tokens)
        self._check_end_of_line()
        return DataMembers([DataMember(mem_name, mem_type, value)])

    def _parse_value(self, typ: str, value: str, prefix: str=''):
        if typ == 'string':
            value = prefix + value
        elif typ == 'num':
            value = int(prefix + value)
        elif typ == 'float':
            if value.isdigit():
                value = int(prefix + value)
            else:
                value = float(prefix + value)
        return value

    def _check_end_of_line(self):
        tk_type, tk_val, ln = self._consume_spaces()
        if tk_type == 'empty' or tk_type == 'comment':
            return
        raise SyntaxError('Only comments are allowed at the end of line.', self._tokens)

    def _parse_reg_with_masks(self, reg):
        tk_type, tk_val, ln = self._consume_spaces()
        if tk_val not in ('k0', 'k1', 'k2', 'k3', 'k4', 'k5', 'k6', 'k7', 'z'):
            raise SyntaxError('In curly braces only mask registers and zero flag is allowed. (k0, k1, k2, k3, k4, k5, k6, k7, z).', self._tokens)

        op_zero = None
        op_mask = None
        if tk_val == 'z':
            op_zero = True
        else:
            op_mask = tk_val

        tk_type, tk_val, ln = self._consume_spaces()
        if tk_type != 'rcurly':
            raise SyntaxError('Missing right curly braces!', self._tokens)

        tk_type, tk_val, ln = self._consume_spaces()
        if tk_type != 'lcurly':
            if tk_type != 'comma' and tk_type not in ('empty', 'comment'):
                raise SyntaxError('Wrong operand declaration.', self._tokens)
            op = RegOperand(reg)
            op.op_mask = op_mask
            op.op_zero = op_zero
            return op
        raise ValueError("TODO: Parsing of {k} {z} is not fully finished yet!")

