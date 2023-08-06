
class Regs:
    def __init__(self):
        self._k = frozenset(['k0', 'k1', 'k2', 'k3', 'k4', 'k5', 'k6', 'k7'])
        self._zmm = frozenset(['zmm31', 'zmm30', 'zmm29', 'zmm28', 'zmm27', 'zmm26', 'zmm25', 'zmm24',
                               'zmm23', 'zmm22', 'zmm21', 'zmm20', 'zmm19', 'zmm18', 'zmm17', 'zmm16',
                               'zmm15', 'zmm14', 'zmm13', 'zmm12', 'zmm11', 'zmm10', 'zmm9', 'zmm8',
                               'zmm7', 'zmm6', 'zmm5', 'zmm4', 'zmm3', 'zmm2', 'zmm1', 'zmm0'])
        self._ymm = frozenset(['ymm31', 'ymm30', 'ymm29', 'ymm28', 'ymm27', 'ymm26', 'ymm25', 'ymm24',
                               'ymm23', 'ymm22', 'ymm21', 'ymm20', 'ymm19', 'ymm18', 'ymm17', 'ymm16',
                               'ymm15', 'ymm14', 'ymm13', 'ymm12', 'ymm11', 'ymm10', 'ymm9', 'ymm8',
                               'ymm7', 'ymm6', 'ymm5', 'ymm4', 'ymm3', 'ymm2', 'ymm1', 'ymm0'])
        self._xmm = frozenset(['xmm31', 'xmm30', 'xmm29', 'xmm28', 'xmm27', 'xmm26', 'xmm25', 'xmm24',
                               'xmm23', 'xmm22', 'xmm21', 'xmm20', 'xmm19', 'xmm18', 'xmm17', 'xmm16',
                               'xmm15', 'xmm14', 'xmm13', 'xmm12', 'xmm11', 'xmm10', 'xmm9', 'xmm8',
                               'xmm7', 'xmm6', 'xmm5', 'xmm4', 'xmm3', 'xmm2', 'xmm1', 'xmm0'])

        self._general = frozenset(['r15d', 'r14d', 'r12d', 'r11d', 'r10d', 'r9d', 'r8d',
                                   'ebp', 'edi', 'esi', 'edx', 'ecx', 'ebx', 'eax'])
        self._general64 = frozenset(['r15', 'r14', 'r12', 'r11', 'r10', 'r9', 'r8',
                                     'rbp', 'rdi', 'rsi', 'rdx', 'rcx', 'rbx', 'rax'])

        self._t_32 = {'eax': 'rax', 'ebx': 'rbx', 'ecx': 'rcx', 'edx': 'rdx',
                      'esi': 'rsi', 'edi': 'rdi', 'ebp': 'rbp', 'esp': 'rsp',
                      'r8d': 'r8', 'r9d': 'r9', 'r10d': 'r10', 'r11d': 'r11',
                      'r12d': 'r12', 'r13d': 'r13', 'r14d': 'r14', 'r15d': 'r15'}

        self._t_64 = {'rax': 'eax', 'rbx': 'ebx', 'rcx': 'ecx', 'rdx': 'edx',
                      'rsi': 'esi', 'rdi': 'edi', 'rbp': 'ebp', 'rsp': 'esp',
                      'r8': 'r8d', 'r9': 'r9d', 'r10': 'r10d', 'r11': 'r11d',
                      'r12': 'r12d', 'r13': 'r13d', 'r14': 'r14d', 'r15': 'r15d'}

    def is_mask(self, reg):
        return reg in self._k

    def is_xmm(self, reg):
        return reg in self._xmm

    def is_ymm(self, reg):
        return reg in self._ymm

    def is_zmm(self, reg):
        return reg in self._zmm

    def is_reg32(self, reg):
        return reg in self._general

    def is_reg64(self, reg):
        return reg in self._general64

    def t_32_to_64(self, reg):
        return self._t_32[reg]

    def t_64_to_32(self, reg):
        return self._t_64[reg]
