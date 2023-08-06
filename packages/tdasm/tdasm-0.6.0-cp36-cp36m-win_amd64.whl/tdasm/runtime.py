
import struct
import x86
from .code import MachineCode
from .holders import ArrayMember, DataMember


class DataAccess:
    def __init__(self, address, getter, setter):
        self.address = address
        self.getter = getter
        self.setter = setter

    def get(self):
        return self.getter(self.address, 0, 0)

    def set(self, value):
        # NOTE: if value is tuple he will overwrite other members in data section
        # NOTE: Also overflow of numbers is not checked
        # TODO: must be improved
        return self.setter(self.address, value, 0)


class DataArrayAccess:
    def __init__(self, address, getter, setter, length):
        self.address = address
        self.getter = getter
        self.setter = setter
        self.length = length

    def get(self):
        return self.getter(self.address, 0, self.length)

    def get_subarray(self):
        raise NotImplementedError()

    def set(self, value):
        # NOTE: check for remarks in DataSetter
        # NOTE: value must be tuple (list not supported)
        # TODO: must be improved
        return self.setter(self.address, value, 0)

    def set_subarray(self):
        raise NotImplementedError()


class DataSection:
    def __init__(self, code: MachineCode, address: int):

        self._members = {}
        self._address = address
        for name, member, offset in code.iter_members():
            self._add_member(name, member, offset)

    def _add_member(self, name, member, offset):
        flags = {'uint8': 'B', 'int8': 'b', 'uint16': 'H', 'int16': 'h',
                 'uint32': 'I', 'int32': 'i', 'float': 'f', 'double': 'd',
                 'int64': 'q', 'uint64': 'Q'}

        if member.typ == "string":
            flags['string'] = str(len(member.value)) + 's'

        data = b''
        if isinstance(member, ArrayMember) and member.values is not None:
            for val in member.values:
                data += struct.pack(flags[member.typ], val)

        if isinstance(member, DataMember) and member.value is not None:
            value = member.value
            if isinstance(member.value, str):
                value = value.encode("ascii")
            data = struct.pack(flags[member.typ], value)

        x86.SetData(self._address + offset, data)

        get_ = {"int8": x86.GetInt8,
                "int16": x86.GetInt16,
                "int32": x86.GetInt32,
                "uint8": x86.GetUInt8,
                "uint16": x86.GetUInt16,
                "uint32": x86.GetUInt32,
                "int64": x86.GetInt64,
                "uint64": x86.GetUInt64,
                "float": x86.GetFloat,
                "double": x86.GetDouble}

        set_ = {"int8": x86.SetInt8,
                "int16": x86.SetInt16,
                "int32": x86.SetInt32,
                "uint8": x86.SetUInt8,
                "uint16": x86.SetUInt16,
                "uint32": x86.SetUInt32,
                "int64": x86.SetInt64,
                "uint64": x86.SetUInt64,
                "float": x86.SetFloat,
                "double": x86.SetDouble}

        def get_string(address, size, flags):
            def get_mem(dummy, dummy2, dummy3):
                num_bytes = x86.GetData(address, size)
                ret = struct.unpack(flags, num_bytes[:])
                if len(ret) == 1:
                    return ret[0].decode('ascii')
                return ret
            return get_mem

        addr = self._address + offset
        if member.typ == 'string':
            # TODO string setter
            fn = get_string(addr, len(member.value), flags[member.typ])
            self._members[name] = DataAccess(addr, fn, None)
        else:
            if isinstance(member, ArrayMember):
                self._members[name] = DataArrayAccess(addr, get_[member.typ],
                                                      set_[member.typ], member.length)
            if isinstance(member, DataMember):
                self._members[name] = DataAccess(addr, get_[member.typ], set_[member.typ])

    def __getitem__(self, key):
        return self._members[key].get()

    def __setitem__(self, key, value):
        return self._members[key].set(value)

    def address_off(self, name):
        return self._members[name].address


class DataSectionOverflow(Exception):
    def __init__(self, size: int, capacity: int):
        self.size = size
        self.capacity = capacity

    def __str__(self):
        return 'Capacity of data section is %i and current size is %i' % (self.capacity, self.size)


class CodeSectionOverflow(Exception):
    def __init__(self, size: int, capacity: int):
        self.size = size
        self.capacity = capacity

    def __str__(self):
        return 'Capacity of code section is %i and current size is %i' % (self.capacity, self.size)


class Runtime:
    def __init__(self, ncode_pages: int=None, ndata_pages: int=None):

        ncode_pages = 1 if ncode_pages is None else ncode_pages
        ndata_pages = 1 if ndata_pages is None else ndata_pages

        # NOTE: memory page is fixed at 64KB (this could be improved)
        self._data_capacity = 65536 * ndata_pages
        self._code_capacity = 65536 * ncode_pages
        self._memory = x86.MemExe(ncode_pages + ndata_pages)
        self._offset = 0
        self._data_size = 0
        self._global_labes = {}
        self._modules = {}

    def load(self, name: str, code: MachineCode, labels_to_resolve={}) -> DataSection:

        if name in self._modules:
            raise ValueError("Module with name %s allready loaded in memory" % name)

        # NOTE: data is placed immediately after executable code in memory
        address = self._memory.ptr() + self._code_capacity + self._data_size
        data_size = code.data_section_size()
        align = 64
        data_size = (data_size + align - 1) & ~(align - 1)
        self._data_size += data_size

        if self._data_size > self._data_capacity:
            raise DataSectionOverflow(self._data_size, self._data_capacity)

        data = DataSection(code, address)

        rip = self._memory.ptr() + self._offset
        raw_code = b''
        for inst in code.iter_instructions():
            rip += len(inst.code)
            if inst.mem_name is not None:
                addr = data.address_off(inst.mem_name)
                doff = inst.disp_offset
                disp = struct.unpack('i', inst.code[doff:doff + 4])[0]
                addr = addr + disp - rip  # rip relative addressing
                code = inst.code[:doff] + struct.pack("i", addr) + inst.code[doff + 4:]
            elif inst.rel_label is not None:
                lbl, size = inst.rel_label
                if lbl in labels_to_resolve:
                    addr, dummy = self._modules[labels_to_resolve[lbl]]
                else:
                    addr, dummy = self._modules[lbl]
                diff = addr - rip
                if size == 1:
                    code = inst.code[:len(inst.code) - 1] + struct.pack('b', diff)
                else:
                    code = inst.code[:len(inst.code) - 4] + struct.pack('i', diff)
            else:
                code = inst.code

            raw_code += code

        if self._offset + len(raw_code) > self._code_capacity:
            raise CodeSectionOverflow(self._offset + len(raw_code), self._code_capacity)

        x86.SetData(self._memory.ptr() + self._offset, raw_code)
        self._modules[name] = (self._memory.ptr() + self._offset, data)
        self._offset += len(raw_code)
        self._offset = (self._offset + align - 1) & ~(align - 1)
        return data

    def run(self, name):
        x86.ExecuteModule(self._modules[name][0])

    def run_multiple(self, names):
        x86.ExecuteModules(tuple(self._modules[name][0] for name in names))

    def __contains__(self, name):
        return name in self._modules
