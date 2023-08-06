
"""
.. module:: code
.. moduleauthor:: Mario Vidov <mvidov@yahoo.com>


"""

from .holders import ArrayMember, DataMember


class StructDesc:
    def __init__(self, offsets, size):
        self._offsets = offsets
        self._size = size

    def size(self):
        return self._size

    def offset(self, name):
        return self._offsets[name]


class MachineCode:
    def __init__(self):
        self._members = {}

        self._align = {'uint8': 4, 'uint16': 4, 'uint32': 4, 'int8': 4,
                       'int16': 4, 'int32': 4, 'int64': 8, 'uint64': 8,
                       'float': 4, 'double': 8, 'string': 16}

        self._data_size = {'uint8': 1, "uint16": 2, 'uint32': 4, 'int8': 1,
                           'int16': 2, 'int32': 4, "float": 4, "int64": 8,
                           "uint64": 8, "double": 8}
        self._offset = 0
        self._instructions = []
        self._labels = {}
        self._struct_defs = {}
        self._code_size = 0

    def iter_members(self):
        for name, (member, offset) in self._members.items():
            yield name, member, offset

    def iter_instructions(self):
        for instruction in self._instructions:
            yield instruction

    def _calc_new_offset(self, member, cur_offset):

        if isinstance(member, ArrayMember):
            if member.typ == 'string':
                raise ValueError("Array string member %s not supported!" % member.name)
            length = len(member) * self._data_size[member.typ]
            align = 16
            if length > 32:
                align = 64
            elif length > 16:
                align = 32
            # align = 32 if length > 16 else 16
            offset = (cur_offset + align - 1) & ~(align - 1)
        else:
            align = self._align[member.typ]
            offset = (cur_offset + align - 1) & ~(align - 1)
            if member.typ == 'string':
                if member.value is None:
                    raise ValueError("String data member %s must have value" % member.name)
                length = len(member.value)
            else:
                length = self._data_size[member.typ]

        return offset, length

    def add_members(self, members):
        for member in members:
            if member.name in self._members:
                raise ValueError('Member %s allready exist.' % member.name)
            if member.typ in self._struct_defs:
                struct_def, desc = self._struct_defs[member.typ]
                if member.value is not None:
                    raise ValueError("Struct instance %s must not have value." % member.typ)

                # align = 32
                align = 64
                self._offset = (self._offset + align - 1) & ~(align - 1)
                struct_member = DataMember(member.name, 'uint8')
                self._members[member.name] = (struct_member, self._offset)
                for smember in struct_def.members:
                    mname = '%s.%s' % (member.name, smember.name)
                    if smember.typ in self._struct_defs:
                        self._members[mname] = (DataMember(mname, 'uint8'), self._offset + desc.offset(smember.name))
                        s_def, dsc = self._struct_defs[smember.typ]
                        for ssmem in s_def.members:
                            self._members[mname + '.' + ssmem.name] = (ssmem, self._offset + desc.offset(smember.name + '.' + ssmem.name))
                    else:
                        self._members[mname] = (smember, self._offset + desc.offset(smember.name))
                self._offset += desc.size()
                continue

            self._offset, length = self._calc_new_offset(member, self._offset)
            self._members[member.name] = (member, self._offset)
            self._offset += length

    def _create_struct_desc(self, struct_def):
        offset = 0
        offsets = {}
        align = 4
        for member in struct_def.members:
            if isinstance(member, ArrayMember):
                length = len(member) * self._data_size[member.typ]
                align = 16
                if length > 32:
                    align = 64
                elif length > 16:
                    align = 32
                # align = 32 if length > 16 else 16
            if member.typ in self._struct_defs:
                s_def, dsc = self._struct_defs[member.typ]
                # align = 32
                ailgn = 64
                offset = (offset + align - 1) & ~(align - 1)
                offsets[member.name] = offset
                for mem_name, mem_off in dsc._offsets.items():
                    offsets[member.name + '.' + mem_name] = offset + mem_off
                offset += dsc.size()
            else:
                offset, length = self._calc_new_offset(member, offset)
                offsets[member.name] = offset
                offset += length

        size = (offset + align - 1) & ~(align - 1)
        desc = StructDesc(offsets, size)
        return desc

    def add_struct_def(self, struct_def):
        if struct_def.name in self._struct_defs:
            raise ValueError("Struct definition for %s allready exist" % struct_def.name)
        desc = self._create_struct_desc(struct_def)
        self._struct_defs[struct_def.name] = (struct_def, desc)

    def code_section_size(self):
        """Return size of code section in bytes."""
        return self._code_size

    def data_section_size(self):
        """Return size of data section in bytes."""
        return self._offset

    def add_instruction(self, inst):
        self._code_size += len(inst.code)
        self._instructions.append(inst)

    def add_label(self, name, address):
        if name in self._labels:
            raise ValueError("Label %s allready exist" % name)
        self._labels[name] = address

    def address_of_label(self, name):
        return self._labels.get(name, None)

    def struct_member_disp(self, struct_typ, path):
        if struct_typ not in self._struct_defs:
            raise ValueError("Struct definition %s doesn't exist" % struct_typ)
        struct_def, desc = self._struct_defs[struct_typ]
        return desc.offset(path)

    def dis(self):
        cur_byte = 0
        text = ""
        for inst in self._instructions:
            hex_code = " ".join("%.2x " % c for c in inst.code)

            hex_code = hex_code + (20 - len(hex_code)) * " "
            out_byte = "%.8d" % cur_byte
            cur_byte += len(inst.code)
            text += out_byte + " " + hex_code + inst.source + "\n"
        return text

    def get_struct_desc(self, name):
        return self._struct_defs[name][1]
