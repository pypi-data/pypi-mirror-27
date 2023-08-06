

class Acums:
    def __init__(self):
        self._k = ['k7', 'k6', 'k5', 'k4', 'k3', 'k2', 'k1']
        self._zmm = ['zmm31', 'zmm30', 'zmm29', 'zmm28', 'zmm27', 'zmm26', 'zmm25', 'zmm24',
                     'zmm23', 'zmm22', 'zmm21', 'zmm20', 'zmm19', 'zmm18', 'zmm17', 'zmm16',
                     'zmm15', 'zmm14', 'zmm13', 'zmm12', 'zmm11', 'zmm10', 'zmm9', 'zmm8',
                     'zmm7', 'zmm6', 'zmm5', 'zmm4', 'zmm3', 'zmm2', 'zmm1', 'zmm0']
        self._ymm = ['ymm31', 'ymm30', 'ymm29', 'ymm28', 'ymm27', 'ymm26', 'ymm25', 'ymm24',
                     'ymm23', 'ymm22', 'ymm21', 'ymm20', 'ymm19', 'ymm18', 'ymm17', 'ymm16',
                     'ymm15', 'ymm14', 'ymm13', 'ymm12', 'ymm11', 'ymm10', 'ymm9', 'ymm8',
                     'ymm7', 'ymm6', 'ymm5', 'ymm4', 'ymm3', 'ymm2', 'ymm1', 'ymm0']
        self._xmm = ['xmm31', 'xmm30', 'xmm29', 'xmm28', 'xmm27', 'xmm26', 'xmm25', 'xmm24',
                     'xmm23', 'xmm22', 'xmm21', 'xmm20', 'xmm19', 'xmm18', 'xmm17', 'xmm16',
                     'xmm15', 'xmm14', 'xmm13', 'xmm12', 'xmm11', 'xmm10', 'xmm9', 'xmm8',
                     'xmm7', 'xmm6', 'xmm5', 'xmm4', 'xmm3', 'xmm2', 'xmm1', 'xmm0']

        self._general = ['r15d', 'r14d', 'r12d', 'r11d', 'r10d', 'r9d', 'r8d',
                         'ebp', 'edi', 'esi', 'edx', 'ecx', 'ebx', 'eax']
        self._general64 = ['r15', 'r14', 'r12', 'r11', 'r10', 'r9', 'r8',
                           'rbp', 'rdi', 'rsi', 'rdx', 'rcx', 'rbx', 'rax']

    def pop(self, cgen, reg):
        if cgen.regs.is_reg32(reg):
            self._general64.pop()
            return self._general.pop()
        elif cgen.regs.is_reg64(reg):
            self._general.pop()
            return self._general64.pop()
        elif cgen.regs.is_xmm(reg):
            self._ymm.pop()
            self._zmm.pop()
            return self._xmm.pop()
        elif cgen.regs.is_ymm(reg):
            self._xmm.pop()
            self._zmm.pop()
            return self._ymm.pop()
        elif cgen.regs.is_zmm(reg):
            self._xmm.pop()
            self._ymm.pop()
            return self._zmm.pop()
        elif cgen.regs.is_mask(reg):
            return self._k.pop()
        else:
            raise ValueError("Allocation of accumulator %s failed." % reg)

    def pop_type(self, cgen, arg):
        typ = arg.acum_type(cgen)
        if typ == 'pointer':
            self._general.pop()
            return self._general64.pop()
        elif typ == 'general':
            self._general64.pop()
            return self._general.pop()
        elif typ == 'general64':
            self._general.pop()
            return self._general64.pop()
        elif typ == 'xmm':
            self._ymm.pop()
            self._zmm.pop()
            return self._xmm.pop()
        elif typ == 'ymm':
            self._xmm.pop()
            self._zmm.pop()
            return self._ymm.pop()
        elif typ == 'zmm':
            self._xmm.pop()
            self._ymm.pop()
            return self._zmm.pop()
        elif typ == 'mask':
            return self._k.pop()
        else:
            raise ValueError("Unknown type of register", typ)

    def in_used_regs(self, cgen, reg, used_regs):
        if reg in used_regs:
            return True
        if cgen.regs.is_reg32(reg):
            return cgen.regs.t_32_to_64(reg) in used_regs
        elif cgen.regs.is_reg64(reg):
            return cgen.regs.t_64_to_32(reg) in used_regs
        elif cgen.regs.is_xmm(reg):
            return 'y' + reg[1:] in used_regs or 'z' + reg[1:] in used_regs
        elif cgen.regs.is_ymm(reg):
            return 'x' + reg[1:] in used_regs or 'z' + reg[1:] in used_regs
        elif cgen.regs.is_zmm(reg):
            return 'x' + reg[1:] in used_regs or 'y' + reg[1:] in used_regs
        else:
            raise ValueError("Unknown register %s" % reg)

    def pop_free_reg(self, cgen, used_regs, reg):
        if cgen.regs.is_reg32(reg):
            for r1, r2 in zip(self._general, self._general64):
                if r1 not in used_regs and r2 not in used_regs:
                    self._general.remove(r1)
                    self._general64.remove(r2)
                    return r1
        elif cgen.regs.is_reg64(reg):
            for r1, r2 in zip(self._general, self._general64):
                if r1 not in used_regs and r2 not in used_regs:
                    self._general.remove(r1)
                    self._general64.remove(r2)
                    return r2
        elif cgen.regs.is_xmm(reg):
            for r1, r2, r3 in zip(self._xmm, self._ymm, self._zmm):
                if r1 not in used_regs and r2 not in used_regs and r3 not in used_regs:
                    self._xmm.remove(r1)
                    self._ymm.remove(r2)
                    self._zmm.remove(r3)
                    return r1
        elif cgen.regs.is_ymm(reg):
            for r1, r2, r3 in zip(self._xmm, self._ymm, self._zmm):
                if r1 not in used_regs and r2 not in used_regs and r3 not in used_regs:
                    self._xmm.remove(r1)
                    self._ymm.remove(r2)
                    self._zmm.remove(r3)
                    return r2
        elif cgen.regs.is_zmm(reg):
            for r1, r2, r3 in zip(self._xmm, self._ymm, self._zmm):
                if r1 not in used_regs and r2 not in used_regs and r3 not in used_regs:
                    self._xmm.remove(r1)
                    self._ymm.remove(r2)
                    self._zmm.remove(r3)
                    return r3
        elif cgen.regs.is_mask(reg):
            for reg in self._k:
                if reg not in used_regs:
                    self._k.remove(reg)
                    return reg
        else:
            raise ValueError("Unknown register %s" % reg)

    def get_index(self, cgen, acum, used_regs):

        for index, reg in enumerate(used_regs):
            if reg == acum:
                return index
            if cgen.regs.is_reg32(reg) and cgen.regs.t_32_to_64(reg) == acum:
                return index
            elif cgen.regs.is_reg64(reg) and cgen.regs.t_64_to_32(reg) == acum:
                return index
            elif cgen.regs.is_xmm(reg) and ('y' + reg[1:] == acum or 'z' + reg[1:] == acum):
                return index
            elif cgen.regs.is_ymm(reg) and ('x' + reg[1:] == acum or 'z' + reg[1:] == acum):
                return index
            elif cgen.regs.is_zmm(reg) and ('x' + reg[1:] == acum or 'y' + reg[1:] == acum):
                return index

        raise IndexError("Cannot find acumulator %s in " % acum, used_regs)


def move_regs_to_acums(cgen, regs):
    acumulators = Acums()
    code = ''
    used_regs = list(regs)
    while len(used_regs) != 0:
        ureg = used_regs.pop(0)
        acum = acumulators.pop(cgen, ureg)
        if acum != ureg:
            if acumulators.in_used_regs(cgen, acum, used_regs):
                index = acumulators.get_index(cgen, acum, used_regs)
                free_reg = acumulators.pop_free_reg(cgen, used_regs, used_regs[index])
                code += cgen.gen.move_reg(free_reg, used_regs[index])
                used_regs[index] = free_reg
                code += cgen.gen.move_reg(acum, ureg)
            else:
                code += cgen.gen.move_reg(acum, ureg)
    return code
