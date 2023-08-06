

class Directive:
    def __init__(self, name: str):
        self.name = name


class Label:
    def __init__(self, name: str):
        self.name = name


class Keyword:
    def __init__(self, name: str, iden: str=None):
        self.name = name
        self.iden = iden


class DataMember:
    def __init__(self, name: str, typ: str, value=None):
        self.name = name
        self.typ = typ
        self.value = value


class ArrayMember:
    def __init__(self, name: str, typ: str, length: int, values: list=None):
        self.name = name
        self.typ = typ
        self.length = length
        self.values = values

    def __len__(self):
        return self.length


class StructDefinition:
    def __init__(self, name: str):
        self.name = name
        self._members = {}
        self.members = []

    def add_members(self, members):
        for member in members:
            if member.name in self._members:
                raise ValueError('Member %s allready exist.' % member.name)
            self._members[member.name] = member
            self.members.append(member)


class DataMembers:
    def __init__(self, members: list):
        self.members = members

    def __iter__(self):
        for member in self.members:
            yield member


class RegOperand:
    def __init__(self, reg: str):
        self.reg = reg
        self.op_mask = None
        self.op_zero = None


class MemOperand:
    def __init__(self, reg: str, data_type: str, scaled_reg: str=None,
                 scale: int=None, displacement: int=None, struct_member: str=None):
        self.reg = reg
        self.data_type = data_type
        self.scaled_reg = scaled_reg
        self.scale = scale
        self.displacement = displacement
        self.struct_member = struct_member
        self.op_mask = None
        self.op_zero = None


class NameOperand:
    def __init__(self, name: str, data_type: str,
                 displacement: int=None, struct_member: str=None):
        self.name = name
        self.data_type = data_type
        self.displacement = displacement
        self.struct_member = struct_member
        self.op_mask = None
        self.op_zero = None


class ConstOperand:
    def __init__(self, value: int):
        self.value = value


class LabelOperand:
    def __init__(self, label: str, small_jump: bool=False, value: int=None):
        self.label = label
        self.small_jump = small_jump
        self.value = value


class KeywordOperand:
    def __init__(self, name: str, iden: str):
        self.name = name
        self.iden = iden


class Instruction:
    def __init__(self, name: str, op1=None, op2=None,
                 op3=None, op4=None, repeat: str=None, lock: bool=False):
        self.name = name
        self.op1 = op1
        self.op2 = op2
        self.op3 = op3
        self.op4 = op4
        self.repeat = repeat
        self.lock = lock


class EncodedInstruction:
    def __init__(self, name: str):
        self.name = name
        self.code = None
        self.disp_offset = None
        self.mem_name = None
        self.rel_label = None
        self.source = None
