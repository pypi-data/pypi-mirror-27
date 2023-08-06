
from tdasm import cpu_features
from .regs import Regs


class AsmGen:
    def __init__(self, cpu_features=cpu_features()):
        self.regs = Regs()
        self.cpu = cpu_features

    def _calc_name(self, name=None, ptr_reg=None, offset=None):
        off = ' + %i' % offset if offset else ''
        src = ptr_reg if ptr_reg else name
        return src + off

    def load_i32(self, dst_reg, name=None, ptr_reg=None, offset=None, value=None):
        if value == 0:
            return 'xor %s, %s\n' % (dst_reg, dst_reg)
        if value is not None:
            return 'mov %s, %i\n' % (dst_reg, value)
        return 'mov %s, dword[%s]\n' % (dst_reg, self._calc_name(name, ptr_reg, offset))

    def store_i32(self, reg, name=None, ptr_reg=None, offset=None):
        return 'mov dword[%s], %s\n' % (self._calc_name(name, ptr_reg, offset), reg)

    def _arith_i32_i64(self, dst_reg, op, bit32, name=None, value=None, src_reg=None, tmp_reg1=None, tmp_reg2=None):
        if value is not None and op == '*' and value == -1:
            return 'neg %s\n' % dst_reg

        if value is not None:
            ins = {'+': 'add', '-': 'sub', '&': 'and', '^': 'xor', '|': 'or', '<<': 'sal', '>>': 'sar'}
        elif name is not None or src_reg is not None:
            ins = {'+': 'add', '*': 'imul', '-': 'sub', '&': 'and', '^': 'xor', '|': 'or'}

        if op in ins:
            if value is not None:
                return '%s %s, %i\n' % (ins[op], dst_reg, value)
            elif src_reg is not None:
                return '%s %s, %s\n' % (ins[op], dst_reg, src_reg)
            if bit32:
                return '%s %s, dword[%s]\n' % (ins[op], dst_reg, name)
            else:
                return '%s %s, qword[%s]\n' % (ins[op], dst_reg, name)

        # NOTE Special cases because of optimizations, need for aditional register, ...

        if value is not None and op == '*':
            sv = {2: 1, 4: 2, 8: 3, 16: 4, 32: 5, 64: 6, 128: 7, 256: 8, 512: 9, 1024: 10}
            if value in sv:
                return 'sal %s, %i\n' % (dst_reg, sv[value])
            return 'imul %s, %s, %i\n' % (dst_reg, dst_reg, value)

        if src_reg is not None and op in ('<<', '>>'):
            if tmp_reg1 is None:
                raise ValueError("For shift with register tmp_reg1 is needed.")
            if bit32:
                return self._shift_i32_i64(op, dst_reg, src_reg, tmp_reg1, 'ecx')
            else:
                return self._shift_i32_i64(op, dst_reg, src_reg, tmp_reg1, 'rcx')
        if src_reg is not None and op in ('/', '%'):
            if tmp_reg1 is None or tmp_reg2 is None:
                raise ValueError("For division/modulo with register tmp_reg1 and tmp_reg2 is needed.")
            if bit32:
                return self._div_mod_i32_i64(op, dst_reg, src_reg, tmp_reg1, tmp_reg2, 'eax', 'edx', True)
            else:
                return self._div_mod_i32_i64(op, dst_reg, src_reg, tmp_reg1, tmp_reg2, 'rax', 'rdx', False)

        raise ValueError("Arithmetic %s cannot be generated." % op, dst_reg, bit32, src_reg)

    def arith_i32(self, dst_reg, op, name=None, value=None, src_reg=None, tmp_reg1=None, tmp_reg2=None):
        return self._arith_i32_i64(dst_reg, op, True, name=name, value=value,
                                   src_reg=src_reg, tmp_reg1=tmp_reg1, tmp_reg2=tmp_reg2)

    def load_i64(self, dst_reg, name=None, ptr_reg=None, offset=None, value=None):
        if value == 0:
            reg = self.regs.t_64_to_32(dst_reg)
            return 'xor %s, %s\n' % (reg, reg)
        if value is not None:
            return 'mov %s, %i\n' % (dst_reg, value)
        return 'mov %s, qword[%s]\n' % (dst_reg, self._calc_name(name, ptr_reg, offset))

    def store_i64(self, reg, name=None, ptr_reg=None, offset=None):
        return 'mov qword[%s], %s\n' % (self._calc_name(name, ptr_reg, offset), reg)

    def arith_i64(self, dst_reg, op, name=None, value=None, src_reg=None, tmp_reg1=None, tmp_reg2=None):
        return self._arith_i32_i64(dst_reg, op, False, name=name, value=value,
                                   src_reg=src_reg, tmp_reg1=tmp_reg1, tmp_reg2=tmp_reg2)

    def _div_mod_i32_i64(self, op, dst_reg, src_reg, tmp_reg1, tmp_reg2, eax, edx, bit32):
        if tmp_reg1 == edx:
            code = 'mov %s, %s\n' % (tmp_reg2, eax)
        elif tmp_reg2 == eax:
            code = 'mov %s, %s\n' % (tmp_reg1, edx)
        else:
            code = 'mov %s, %s\n' % (tmp_reg1, eax)
            code += 'mov %s, %s\n' % (tmp_reg2, edx)

        code += 'mov %s, %s\n' % (eax, dst_reg)

        if bit32:
            code += 'cdq\n'
        else:
            code += 'cqo\n'

        if src_reg == eax:
            if tmp_reg1 == edx:
                code += 'idiv %s\n' % tmp_reg2
            else:
                code += 'idiv %s\n' % tmp_reg1
        elif src_reg == edx:
            if tmp_reg2 == eax:
                code += 'idiv %s\n' % tmp_reg1
            else:
                code += 'idiv %s\n' % tmp_reg2
        else:
            code += 'idiv %s\n' % src_reg

        if op == '/':
            code += 'mov %s, %s\n' % (dst_reg, eax)
        else:
            code += 'mov %s, %s\n' % (dst_reg, edx)

        if dst_reg != eax:
            if tmp_reg1 == edx:
                code += 'mov %s, %s\n' % (eax, tmp_reg2)
            else:
                code += 'mov %s, %s\n' % (eax, tmp_reg1)
        if dst_reg != edx:
            if tmp_reg2 == eax:
                code += 'mov %s, %s\n' % (edx, tmp_reg1)
            else:
                code += 'mov %s, %s\n' % (edx, tmp_reg2)
        return code

    def _shift_i32_i64(self, op, dst_reg, src_reg, tmp_reg, ecx):
        cmd = 'sal' if op == '<<' else 'sar'
        if tmp_reg == ecx:
            code = 'mov %s, %s\n' % (ecx, src_reg)
            code += '%s %s, cl\n' % (cmd, dst_reg)
        elif dst_reg == ecx and src_reg == ecx:
            code = '%s %s, cl\n' % (cmd, src_reg)
        elif dst_reg == ecx:
            code = 'mov %s, %s\n' % (tmp_reg, ecx)
            code += 'mov %s, %s\n' % (ecx, src_reg)
            code += '%s %s, cl\n' % (cmd, tmp_reg)
            code += 'mov %s, %s\n' % (ecx, tmp_reg)
        elif src_reg == ecx:
            code = '%s %s, cl\n' % (cmd, dst_reg)
        else:
            code = 'mov %s, %s\n' % (tmp_reg, ecx)
            code += 'mov %s, %s\n' % (ecx, src_reg)
            code += '%s %s, cl\n' % (cmd, dst_reg)
            code += 'mov %s, %s\n' % (ecx, tmp_reg)
        return code

    def load_f64(self, dst_reg, name=None, ptr_reg=None, offset=None):
        inst = 'vmovsd' if self.cpu.AVX or self.cpu.AVX512F else 'movsd'
        return '%s %s, qword[%s]\n' % (inst, dst_reg, self._calc_name(name, ptr_reg, offset))

    def store_f64(self, xmm, name=None, ptr_reg=None, offset=None):
        inst = 'vmovsd' if self.cpu.AVX or self.cpu.AVX512F else 'movsd'
        return '%s qword [%s], %s\n' % (inst, self._calc_name(name, ptr_reg, offset), xmm)

    def _arith_f64_f32(self, xmm1, op, bit32, vec_size, name=None, xmm2=None, dst_reg=None, offset=None):
        comp = {'==': 0, '<': 1, '<=': 2, '!=': 4, '>=': 5, '>': 6}
        off = ' + %i' % offset if offset else ''
        code = ''
        if bit32:
            if vec_size == 1:
                arith = {'+': 'addss', '-': 'subss', '*': 'mulss', '/': 'divss'}
                cmp, mem_size = 'cmpss', 'dword'
            elif vec_size in (2, 3, 4):
                arith = {'+': 'addps', '-': 'subps', '*': 'mulps', '/': 'divps', '&': 'andps', '^': 'xorps', '|': 'orps'}
                cmp, mem_size = 'cmpps', 'oword'
            elif vec_size == 8:
                arith = {'+': 'addps', '-': 'subps', '*': 'mulps', '/': 'divps', '&': 'andps', '^': 'xorps', '|': 'orps'}
                cmp, mem_size = 'cmpps', 'yword'
            elif vec_size == 16:
                arith = {'+': 'addps', '-': 'subps', '*': 'mulps', '/': 'divps', '&': 'andps', '^': 'xorps', '|': 'orps'}
                cmp, mem_size = 'cmpps', 'zword'
        else:
            if vec_size == 1:
                arith = {'+': 'addsd', '-': 'subsd', '*': 'mulsd', '/': 'divsd'}
                cmp, mem_size = 'cmpsd', 'qword'
            elif vec_size == 2:
                arith = {'+': 'addpd', '-': 'subpd', '*': 'mulpd', '/': 'divpd', '&': 'andpd', '^': 'xorpd', '|': 'orpd'}
                cmp, mem_size = 'cmppd', 'oword'
            elif vec_size == 4:
                arith = {'+': 'addpd', '-': 'subpd', '*': 'mulpd', '/': 'divpd', '&': 'andpd', '^': 'xorpd', '|': 'orpd'}
                cmp, mem_size = 'cmppd', 'yword'
            elif vec_size == 8:
                arith = {'+': 'addpd', '-': 'subpd', '*': 'mulpd', '/': 'divpd', '&': 'andpd', '^': 'xorpd', '|': 'orpd'}
                cmp, mem_size = 'cmppd', 'zword'

        if self.cpu.AVX or self.cpu.AVX512F:
            if self.cpu.AVX512F and op in comp and dst_reg is None:
                raise ValueError("Missing destination op mask, AVX-512", op)
            if dst_reg is None:
                dst_reg = xmm1
        else:
            if dst_reg is not None and dst_reg != xmm1:
                code = 'movaps %s, %s\n' % (dst_reg, xmm1)
            else:
                dst_reg = xmm1

        if op in comp:
            if self.cpu.AVX:
                if xmm2 is None:
                    code += 'v%s %s, %s, %s[%s%s], %i\n' % (cmp, dst_reg, xmm1, mem_size, name, off, comp[op])
                else:
                    code += 'v%s %s, %s, %s, %i\n' % (cmp, dst_reg, xmm1, xmm2, comp[op])
            else:
                if xmm2 is None:
                    code += '%s %s, %s[%s%s], %i\n' % (cmp, dst_reg, mem_size, name, off, comp[op])
                else:
                    code += '%s %s, %s, %i\n' % (cmp, dst_reg, xmm2, comp[op])
        else:
            if self.cpu.AVX or self.cpu.AVX512F:
                if xmm2 is None:
                    code += 'v%s %s, %s, %s[%s%s]\n' % (arith[op], dst_reg, xmm1, mem_size, name, off)
                else:
                    code += 'v%s %s, %s, %s\n' % (arith[op], dst_reg, xmm1, xmm2)
            else:
                if xmm2 is None:
                    code += '%s %s, %s[%s%s]\n' % (arith[op], dst_reg, mem_size, name, off)
                else:
                    code += '%s %s, %s\n' % (arith[op], dst_reg, xmm2)
        return code

    def arith_f64(self, xmm1, op, name=None, xmm2=None, dst_reg=None):
        return self._arith_f64_f32(xmm1, op, False, 1, name=name, xmm2=xmm2, dst_reg=dst_reg)

    def load_f32(self, dst_reg, name=None, ptr_reg=None, offset=None):
        inst = 'vmovss' if self.cpu.AVX or self.cpu.AVX512F else 'movss'
        return '%s %s, dword[%s]\n' % (inst, dst_reg, self._calc_name(name, ptr_reg, offset))

    def store_f32(self, xmm, name=None, ptr_reg=None, offset=None):
        inst = 'vmovss' if self.cpu.AVX or self.cpu.AVX512F else 'movss'
        return '%s dword [%s], %s\n' % (inst, self._calc_name(name, ptr_reg, offset), xmm)

    def arith_f32(self, xmm1, op, name=None, xmm2=None, dst_reg=None):
        return self._arith_f64_f32(xmm1, op, True, 1, name=name, xmm2=xmm2, dst_reg=dst_reg)

    def load_f64x2(self, dst_reg, name=None, ptr_reg=None, offset=None, align=True):
        if align:
            inst = 'vmovapd' if self.cpu.AVX or self.cpu.AVX512F else 'movapd'
        else:
            inst = 'vmovupd' if self.cpu.AVX or self.cpu.AVX512F else 'movupd'
        return '%s %s, oword[%s]\n' % (inst, dst_reg, self._calc_name(name, ptr_reg, offset))

    def load_f64x4(self, dst_reg, name=None, ptr_reg=None, offset=None, align=True):
        inst = 'vmovapd' if align else 'vmovupd'
        return '%s %s, yword[%s]\n' % (inst, dst_reg, self._calc_name(name, ptr_reg, offset))

    def load_f64x8(self, dst_reg, name=None, ptr_reg=None, offset=None, align=True):
        inst = 'vmovapd' if align else 'vmovupd'
        return '%s %s, zword[%s]\n' % (inst, dst_reg, self._calc_name(name, ptr_reg, offset))

    def store_f64x2(self, xmm, name=None, ptr_reg=None, offset=None, align=True):
        if align:
            inst = 'vmovapd' if self.cpu.AVX or self.cpu.AVX512F else 'movapd'
        else:
            inst = 'vmovupd' if self.cpu.AVX or self.cpu.AVX512F else 'movupd'
        return '%s oword [%s], %s\n' % (inst, self._calc_name(name, ptr_reg, offset), xmm)

    def store_f64x4(self, xmm, name=None, ptr_reg=None, offset=None, align=True):
        inst = 'vmovapd' if align else 'vmovupd'
        return '%s yword [%s], %s\n' % (inst, self._calc_name(name, ptr_reg, offset), xmm)

    def store_f64x8(self, xmm, name=None, ptr_reg=None, offset=None, align=True):
        inst = 'vmovapd' if align else 'vmovupd'
        return '%s zword [%s], %s\n' % (inst, self._calc_name(name, ptr_reg, offset), xmm)

    def load_f32x4(self, dst_reg, name=None, ptr_reg=None, offset=None, align=True):
        if align:
            inst = 'vmovaps' if self.cpu.AVX or self.cpu.AVX512F else 'movaps'
        else:
            inst = 'vmovups' if self.cpu.AVX or self.cpu.AVX512F else 'movups'
        return '%s %s, oword[%s]\n' % (inst, dst_reg, self._calc_name(name, ptr_reg, offset))

    def load_f32x8(self, dst_reg, name=None, ptr_reg=None, offset=None, align=True):
        inst = 'vmovaps' if align else 'vmovups'
        return '%s %s, yword[%s]\n' % (inst, dst_reg, self._calc_name(name, ptr_reg, offset))

    def load_f32x16(self, dst_reg, name=None, ptr_reg=None, offset=None, align=True):
        inst = 'vmovaps' if align else 'vmovups'
        return '%s %s, zword[%s]\n' % (inst, dst_reg, self._calc_name(name, ptr_reg, offset))

    def store_f32x4(self, xmm, name=None, ptr_reg=None, offset=None):
        inst = 'vmovaps' if self.cpu.AVX or self.cpu.AVX512F else 'movaps'
        return '%s oword [%s], %s\n' % (inst, self._calc_name(name, ptr_reg, offset), xmm)

    def store_f32x8(self, ymm, name=None, ptr_reg=None, offset=None, align=True):
        inst = 'vmovaps' if align else 'vmovups'
        return '%s yword [%s], %s\n' % (inst, self._calc_name(name, ptr_reg, offset), ymm)

    def store_f32x16(self, zmm, name=None, ptr_reg=None, offset=None, align=True):
        inst = 'vmovaps' if align else 'vmovups'
        return '%s zword [%s], %s\n' % (inst, self._calc_name(name, ptr_reg, offset), zmm)

    def load_i64x2(self, dst_reg, name=None, ptr_reg=None, offset=None, align=True):
        if align:
            if self.cpu.AVX512F:
                inst = 'vmovdqa64'
            elif self.cpu.AVX:
                inst = 'vmovdqa'
            else:
                inst = 'movdqa'
        else:
            if self.cpu.AVX512F:
                inst = 'vmovdqu64'
            elif self.cpu.AVX:
                inst = 'vmovdqu'
            else:
                inst = 'movdqu'
        return '%s %s, oword[%s]\n' % (inst, dst_reg, self._calc_name(name, ptr_reg, offset))

    def load_i64x4(self, dst_reg, name=None, ptr_reg=None, offset=None, align=True):
        if self.cpu.AVX512F:
            inst = 'vmovdqa64' if align else 'vmovdqu64'
        else:
            inst = 'vmovdqa' if align else 'vmovdqu'
        return '%s %s, yword[%s]\n' % (inst, dst_reg, self._calc_name(name, ptr_reg, offset))

    def load_i64x8(self, dst_reg, name=None, ptr_reg=None, offset=None, align=True):
        inst = 'vmovdqa64' if align else 'vmovdqu64'
        return '%s %s, zword[%s]\n' % (inst, dst_reg, self._calc_name(name, ptr_reg, offset))

    def store_i64x2(self, xmm, name=None, ptr_reg=None, offset=None, align=True):
        if align:
            if self.cpu.AVX512F:
                inst = 'vmovdqa64'
            elif self.cpu.AVX:
                inst = 'vmovdqa'
            else:
                inst = 'movdqa'
        else:
            if self.cpu.AVX512F:
                inst = 'vmovdqu64'
            elif self.cpu.AVX:
                inst = 'vmovdqu'
            else:
                inst = 'movdqu'
        return '%s oword [%s], %s\n' % (inst, self._calc_name(name, ptr_reg, offset), xmm)

    def store_i64x4(self, xmm, name=None, ptr_reg=None, offset=None, align=True):
        if self.cpu.AVX512F:
            inst = 'vmovdqa64' if align else 'vmovdqu64'
        else:
            inst = 'vmovdqa' if align else 'vmovdqu'
        return '%s yword [%s], %s\n' % (inst, self._calc_name(name, ptr_reg, offset), xmm)

    def store_i64x8(self, xmm, name=None, ptr_reg=None, offset=None, align=True):
        inst = 'vmovdqa64' if align else 'vmovdqu64'
        return '%s zword [%s], %s\n' % (inst, self._calc_name(name, ptr_reg, offset), xmm)

    def load_i32x4(self, dst_reg, name=None, ptr_reg=None, offset=None, align=True):
        if align:
            if self.cpu.AVX512F:
                inst = 'vmovdqa32'
            elif self.cpu.AVX:
                inst = 'vmovdqa'
            else:
                inst = 'movdqa'
        else:
            if self.cpu.AVX512F:
                inst = 'vmovdqu32'
            elif self.cpu.AVX:
                inst = 'vmovdqu'
            else:
                inst = 'movdqu'
        return '%s %s, oword[%s]\n' % (inst, dst_reg, self._calc_name(name, ptr_reg, offset))

    def load_i32x8(self, dst_reg, name=None, ptr_reg=None, offset=None, align=True):
        if self.cpu.AVX512F:
            inst = 'vmovdqa32' if align else 'vmovdqu32'
        else:
            inst = 'vmovdqa' if align else 'vmovdqu'
        return '%s %s, yword[%s]\n' % (inst, dst_reg, self._calc_name(name, ptr_reg, offset))

    def load_i32x16(self, dst_reg, name=None, ptr_reg=None, offset=None, align=True):
        inst = 'vmovdqa32' if align else 'vmovdqu32'
        return '%s %s, zword[%s]\n' % (inst, dst_reg, self._calc_name(name, ptr_reg, offset))

    def store_i32x4(self, xmm, name=None, ptr_reg=None, offset=None):
        if self.cpu.AVX512F:
            inst = 'vmovdqa32'
        elif self.cpu.AVX:
            inst = 'vmovdqa'
        else:
            inst = 'movdqa'
        return '%s oword [%s], %s\n' % (inst, self._calc_name(name, ptr_reg, offset), xmm)

    def store_i32x8(self, ymm, name=None, ptr_reg=None, offset=None, align=True):
        if self.cpu.AVX512F:
            inst = 'vmovdqa32' if align else 'vmovdqu32'
        else:
            inst = 'vmovdqa' if align else 'vmovdqu'
        return '%s yword [%s], %s\n' % (inst, self._calc_name(name, ptr_reg, offset), ymm)

    def store_i32x16(self, zmm, name=None, ptr_reg=None, offset=None, align=True):
        inst = 'vmovdqa32' if align else 'vmovdqu32'
        return '%s zword [%s], %s\n' % (inst, self._calc_name(name, ptr_reg, offset), zmm)

    def arith_f64x2(self, xmm1, op, name=None, xmm2=None, dst_reg=None, offset=None):
        return self._arith_f64_f32(xmm1, op, False, 2, name=name, xmm2=xmm2, dst_reg=dst_reg, offset=offset)

    def arith_f64x4(self, xmm1, op, name=None, xmm2=None, dst_reg=None, offset=None):
        return self._arith_f64_f32(xmm1, op, False, 4, name=name, xmm2=xmm2, dst_reg=dst_reg, offset=offset)

    def arith_f64x8(self, zmm1, op, name=None, zmm2=None, dst_reg=None, offset=None):
        return self._arith_f64_f32(zmm1, op, False, 8, name=name, xmm2=zmm2, dst_reg=dst_reg, offset=offset)

    def arith_f32x4(self, xmm1, op, name=None, xmm2=None, dst_reg=None, offset=None):
        return self._arith_f64_f32(xmm1, op, True, 4, name=name, xmm2=xmm2, dst_reg=dst_reg, offset=offset)

    def arith_f32x8(self, xmm1, op, name=None, xmm2=None, dst_reg=None, offset=None):
        return self._arith_f64_f32(xmm1, op, True, 8, name=name, xmm2=xmm2, dst_reg=dst_reg, offset=offset)

    def arith_f32x16(self, zmm1, op, name=None, zmm2=None, dst_reg=None, offset=None):
        return self._arith_f64_f32(zmm1, op, True, 16, name=name, xmm2=zmm2, dst_reg=dst_reg, offset=offset)

    def _arith_i64_i32(self, xmm1, op, bit32, vec_size, name=None, xmm2=None, dst_reg=None, offset=None):
        off = ' + %i' % offset if offset else ''
        code = ''
        if bit32:
            if self.cpu.AVX512F:
                arith = {'+': 'paddd', '-': 'psubd', '*': 'pmulld', '==': 'pcmpeqd', '>': 'pcmpgtd', '&': 'pandd', '^': 'pxord', '|': 'pord'}
            else:
                arith = {'+': 'paddd', '-': 'psubd', '*': 'pmulld', '==': 'pcmpeqd', '>': 'pcmpgtd', '&': 'pand', '^': 'pxor', '|': 'por'}
            if vec_size in (2, 3, 4):
                mem_size = 'oword'
            elif vec_size == 8:
                mem_size = 'yword'
            elif vec_size == 16:
                mem_size = 'zword'
        else:
            if self.cpu.AVX512F:
                arith = {'+': 'paddq', '-': 'psubq', '==': 'pcmpeqq', '>': 'pcmpgtq', '&': 'pandq', '^': 'pxorq', '|': 'porq'}
            else:
                arith = {'+': 'paddq', '-': 'psubq', '==': 'pcmpeqq', '>': 'pcmpgtq', '&': 'pand', '^': 'pxor', '|': 'por'}
            if vec_size == 2:
                mem_size = 'oword'
            elif vec_size == 4:
                mem_size = 'yword'
            elif vec_size == 8:
                mem_size = 'zword'

        if self.cpu.AVX or self.cpu.AVX512F:
            if dst_reg is None:
                dst_reg = xmm1
        else:
            if dst_reg is not None and dst_reg != xmm1:
                code = 'movdqa %s, %s\n' % (dst_reg, xmm1)
            else:
                dst_reg = xmm1

        if self.cpu.AVX or self.cpu.AVX512F:
            if xmm2 is None:
                code += 'v%s %s, %s, %s[%s%s]\n' % (arith[op], dst_reg, xmm1, mem_size, name, off)
            else:
                code += 'v%s %s, %s, %s\n' % (arith[op], dst_reg, xmm1, xmm2)
        else:
            if xmm2 is None:
                code += '%s %s, %s[%s%s]\n' % (arith[op], dst_reg, mem_size, name, off)
            else:
                code += '%s %s, %s\n' % (arith[op], dst_reg, xmm2)
        return code

    def arith_i32x4(self, xmm1, op, name=None, xmm2=None, dst_reg=None, offset=None):
        return self._arith_i64_i32(xmm1, op, True, 4, name=name, xmm2=xmm2, dst_reg=dst_reg, offset=offset)

    def arith_i32x8(self, xmm1, op, name=None, xmm2=None, dst_reg=None, offset=None):
        return self._arith_i64_i32(xmm1, op, True, 8, name=name, xmm2=xmm2, dst_reg=dst_reg, offset=offset)

    def arith_i32x16(self, xmm1, op, name=None, xmm2=None, dst_reg=None, offset=None):
        return self._arith_i64_i32(xmm1, op, True, 16, name=name, xmm2=xmm2, dst_reg=dst_reg, offset=offset)

    def arith_i64x2(self, xmm1, op, name=None, xmm2=None, dst_reg=None, offset=None):
        return self._arith_i64_i32(xmm1, op, False, 2, name=name, xmm2=xmm2, dst_reg=dst_reg, offset=offset)

    def arith_i64x4(self, xmm1, op, name=None, xmm2=None, dst_reg=None, offset=None):
        return self._arith_i64_i32(xmm1, op, False, 4, name=name, xmm2=xmm2, dst_reg=dst_reg, offset=offset)

    def arith_i64x8(self, xmm1, op, name=None, xmm2=None, dst_reg=None, offset=None):
        return self._arith_i64_i32(xmm1, op, False, 8, name=name, xmm2=xmm2, dst_reg=dst_reg, offset=offset)

    def load_float234(self, xmm, name=None, reg=None, offset=None, is_aligned=True):
        off = ' + %i' % offset if offset else ''
        inst = 'movaps' if is_aligned else 'movups'
        src = reg if reg else name

        if self.cpu.AVX or self.cpu.AVX512F:
            return 'v%s %s, oword[%s%s]\n' % (inst, xmm, src, off)
        else:
            return '%s %s, oword[%s%s]\n' % (inst, xmm, src, off)

    def load_int234(self, xmm, name=None, reg=None, offset=None, is_aligned=True):
        off = ' + %i' % offset if offset else ''
        inst = 'movdqa' if is_aligned else 'movdqu'
        src = reg if reg else name

        if self.cpu.AVX512F:
            return 'v%s32 %s, oword[%s%s]\n' % (inst, xmm, src, off)
        elif self.cpu.AVX:
            return 'v%s %s, oword[%s%s]\n' % (inst, xmm, src, off)
        else:
            return '%s %s, oword[%s%s]\n' % (inst, xmm, src, off)

    def _load_data64_234(self, inst, xmm, name=None, reg=None, offset=None):
        off = ' + %i' % offset if offset else ''
        src = reg if reg else name

        if self.cpu.AVX or self.cpu.AVX512F:
            if self.regs.is_ymm(xmm):
                return 'v%s %s, yword[%s%s]\n' % (inst, xmm, src, off)
            else:
                return 'v%s %s, oword[%s%s]\n' % (inst, xmm, src, off)
        else:
            return '%s %s, oword[%s%s]\n' % (inst, xmm, src, off)

    def load_double234(self, xmm, name=None, reg=None, offset=None, is_aligned=True):
        inst = 'movapd' if is_aligned else 'movupd'
        return self._load_data64_234(inst, xmm, name=name, reg=reg, offset=offset)

    def store_float234(self, xmm, name=None, reg=None, offset=None, is_aligned=True):
        off = ' + %i' % offset if offset else ''
        inst = 'movaps' if is_aligned else 'movups'
        dest = reg if reg else name

        if self.cpu.AVX or self.cpu.AVX512F:
            return 'v%s oword [%s%s], %s\n' % (inst, dest, off, xmm)
        else:
            return '%s oword [%s%s], %s\n' % (inst, dest, off, xmm)

    def store_int234(self, xmm, name=None, reg=None, offset=None, is_aligned=True):
        off = ' + %i' % offset if offset else ''
        inst = 'movdqa' if is_aligned else 'movdqu'
        dest = reg if reg else name

        if self.cpu.AVX512F:
            return 'v%s32 oword [%s%s], %s\n' % (inst, dest, off, xmm)
        elif self.cpu.AVX:
            return 'v%s oword [%s%s], %s\n' % (inst, dest, off, xmm)
        else:
            return '%s oword [%s%s], %s\n' % (inst, dest, off, xmm)

    def _store_data64_234(self, inst, xmm, name=None, reg=None, offset=None):
        off = ' + %i' % offset if offset else ''
        dest = reg if reg else name

        if self.cpu.AVX or self.cpu.AVX512F:
            if self.regs.is_ymm(xmm):
                return 'v%s yword [%s%s], %s\n' % (inst, dest, off, xmm)
            else:
                return 'v%s oword [%s%s], %s\n' % (inst, dest, off, xmm)
        else:
            return '%s oword [%s%s], %s\n' % (inst, dest, off, xmm)

    def store_double234(self, xmm, name=None, reg=None, offset=None, is_aligned=True):
        inst = 'movapd' if is_aligned else 'movupd'
        return self._store_data64_234(inst, xmm, name=name, reg=reg, offset=offset)

    def _arith_i32x4_i64x2_con(self, inst, xmm, value, dst_reg=None):
        code = ''
        if self.cpu.AVX or self.cpu.AVX512F:
            if dst_reg is None:
                dst_reg = xmm
        else:
            if dst_reg is not None and dst_reg != xmm:
                code = 'movdqa %s, %s\n' % (dst_reg, xmm)
            else:
                dst_reg = xmm

        if self.cpu.AVX or self.cpu.AVX512F:
            code += 'v%s %s, %s, %i\n' % (inst, dst_reg, xmm, value)
        else:
            code += '%s %s, %i\n' % (inst, dst_reg, value)
        return code

    def arith_i32x4_con(self, xmm, op, value, dst_reg=None):
        arith = {'<<': 'pslld', '>>': 'psrad'}
        if op not in arith:
            raise ValueError("Arithmetic %s not yet supported." % op, xmm, op, value)
        if value > 128:
            raise ValueError("Constant value is too big!", xmm, op, value)
        return self._arith_i32x4_i64x2_con(arith[op], xmm, value, dst_reg=dst_reg)

    def arith_i64x2_con(self, xmm, op, value, dst_reg=None):
        arith = {'<<': 'psllq'}
        if op not in arith:
            raise ValueError("Arithmetic %s not yet supported." % op, xmm, op, value)
        if value > 128:
            raise ValueError("Constant value is too big!", xmm, op, value)
        return self._arith_i32x4_i64x2_con(arith[op], xmm, value, dst_reg=dst_reg)

    def arith_i32x8_con(self, ymm, op, value, dst_reg=None):
        arith = {'<<': 'pslld', '>>': 'psrad'}
        if op not in arith:
            raise ValueError("Arithmetic %s not yet supported." % op, ymm, op, value)
        if value > 128:
            raise ValueError("Constant value is too big!", ymm, op, value)
        if dst_reg is None:
            dst_reg = ymm
        code = 'v%s %s, %s, %i\n' % (arith[op], dst_reg, ymm, value)
        return code

    def arith_i32x16_con(self, zmm, op, value, dst_reg=None):
        arith = {'<<': 'pslld', '>>': 'psrad'}
        if op not in arith:
            raise ValueError("Arithmetic %s not yet supported." % op, zmm, op, value)
        if value > 128:
            raise ValueError("Constant value is too big!", zmm, op, value)
        if dst_reg is None:
            dst_reg = zmm
        code = 'v%s %s, %s, %i\n' % (arith[op], dst_reg, zmm, value)
        return code

    def arith_i64x4_con(self, ymm, op, value, dst_reg=None):
        arith = {'<<': 'psllq'}
        if op not in arith:
            raise ValueError("Arithmetic %s not yet supported." % op, ymm, op, value)
        if value > 128:
            raise ValueError("Constant value is too big!", ymm, op, value)
        code = 'v%s %s, %s, %i\n' % (arith[op], dst_reg, ymm, value)
        return code

    def arith_i64x8_con(self, zmm, op, value, dst_reg=None):
        arith = {'<<': 'psllq'}
        if op not in arith:
            raise ValueError("Arithmetic %s not yet supported." % op, zmm, op, value)
        if value > 128:
            raise ValueError("Constant value is too big!", zmm, op, value)
        code = 'v%s %s, %s, %i\n' % (arith[op], dst_reg, zmm, value)
        return code

    def move_reg(self, dest, src):
        if self.regs.is_reg32(dest) or self.regs.is_reg64(dest):
            return 'mov %s, %s\n' % (dest, src)
        elif self.regs.is_xmm(dest) or self.regs.is_ymm(dest) or self.regs.is_zmm(dest):
            if self.cpu.AVX or self.cpu.AVX512F:
                return 'vmovaps %s, %s\n' % (dest, src)
            else:
                return 'movaps %s, %s\n' % (dest, src)
        else:
            raise ValueError("Move of %s to %s not yet supported." % (src, dest))

    def conv_f32_to_f64(self, dst_xmm, src_xmm=None, name=None):
        if self.cpu.AVX or self.cpu.AVX512F:
            if src_xmm is None:
                return 'vcvtss2sd %s, %s, dword [%s]\n' % (dst_xmm, dst_xmm, name)
            else:
                return 'vcvtss2sd %s, %s, %s\n' % (dst_xmm, dst_xmm, src_xmm)
        else:
            if src_xmm is None:
                return 'cvtss2sd %s, dword [%s]\n' % (dst_xmm, name)
            else:
                return 'cvtss2sd %s, %s\n' % (dst_xmm, src_xmm)

    def conv_f64_to_f32(self, dst_xmm, src_xmm=None, name=None):
        if self.cpu.AVX or self.cpu.AVX512F:
            if src_xmm is None:
                return 'vcvtsd2ss %s, %s, qword [%s]\n' % (dst_xmm, dst_xmm, name)
            else:
                return 'vcvtsd2ss %s, %s, %s\n' % (dst_xmm, dst_xmm, src_xmm)
        else:
            if src_xmm is None:
                return 'cvtsd2ss %s, qword [%s]\n' % (dst_xmm, name)
            else:
                return 'cvtsd2ss %s, %s\n' % (dst_xmm, src_xmm)

    def _conv_i32_i64_to_f32(self, dst_xmm, bit32, src_reg=None, name=None):
        mem_size = 'dword' if bit32 else 'qword'
        if self.cpu.AVX or self.cpu.AVX512F:
            if src_reg is None:
                return 'vcvtsi2ss %s, %s, %s[%s]\n' % (dst_xmm, dst_xmm, mem_size, name)
            else:
                return 'vcvtsi2ss %s, %s, %s\n' % (dst_xmm, dst_xmm, src_reg)
        else:
            if src_reg is None:
                return 'cvtsi2ss %s, %s[%s]\n' % (dst_xmm, mem_size, name)
            else:
                return 'cvtsi2ss %s, %s\n' % (dst_xmm, src_reg)

    def conv_i32_to_f32(self, dst_xmm, src_reg=None, name=None):
        return self._conv_i32_i64_to_f32(dst_xmm, True, src_reg=src_reg, name=name)

    def conv_i64_to_f32(self, dst_xmm, src_reg=None, name=None):
        return self._conv_i32_i64_to_f32(dst_xmm, False, src_reg=src_reg, name=name)

    def _conv_i32_i64_to_f64(self, dst_xmm, bit32, src_reg=None, name=None):
        mem_size = 'dword' if bit32 else 'qword'
        if self.cpu.AVX or self.cpu.AVX512F:
            if src_reg is None:
                return 'vcvtsi2sd %s, %s, %s[%s]\n' % (dst_xmm, dst_xmm, mem_size, name)
            else:
                return 'vcvtsi2sd %s, %s, %s\n' % (dst_xmm, dst_xmm, src_reg)
        else:
            if src_reg is None:
                return 'cvtsi2sd %s, %s[%s]\n' % (dst_xmm, mem_size, name)
            else:
                return 'cvtsi2sd %s, %s\n' % (dst_xmm, src_reg)

    def conv_i32_to_f64(self, dst_xmm, src_reg=None, name=None):
        return self._conv_i32_i64_to_f64(dst_xmm, True, src_reg=src_reg, name=name)

    def conv_i64_to_f64(self, dst_xmm, src_reg=None, name=None):
        return self._conv_i32_i64_to_f64(dst_xmm, False, src_reg=src_reg, name=name)

    def _conv_f64_to_i32_i64(self, dst_reg, xmm=None, name=None):
        inst = 'vcvttsd2si' if self.cpu.AVX or self.cpu.AVX512F else 'cvttsd2si'
        if xmm:
            return '%s %s, %s\n' % (inst, dst_reg, xmm)
        else:
            return '%s %s, qword [%s]\n' % (inst, dst_reg, name)

    def conv_f64_to_i32(self, dst_reg, xmm=None, name=None):
        return self._conv_f64_to_i32_i64(dst_reg, xmm=xmm, name=name)

    def conv_f64_to_i64(self, dst_reg, xmm=None, name=None):
        return self._conv_f64_to_i32_i64(dst_reg, xmm=xmm, name=name)

    def _conv_f32_to_i32_i64(self, dst_reg, xmm=None, name=None):
        inst = 'vcvttss2si' if self.cpu.AVX or self.cpu.AVX512F else 'cvttss2si'
        if xmm:
            return '%s %s, %s\n' % (inst, dst_reg, xmm)
        else:
            return '%s %s, dword [%s]\n' % (inst, dst_reg, name)

    def conv_f32_to_i32(self, dst_reg, xmm=None, name=None):
        return self._conv_f32_to_i32_i64(dst_reg, xmm=xmm, name=name)

    def conv_f32_to_i64(self, dst_reg, xmm=None, name=None):
        return self._conv_f32_to_i32_i64(dst_reg, xmm=xmm, name=name)

    def _fma_f64_f32(self, inst, xmm1, xmm2, op, bit32, packed, xmm3=None, name=None, offset=None):

        if bit32:
            mem = 'oword' if packed else 'dword'
            ps = 'ps' if packed else 'ss'
        else:
            mem = 'oword' if packed else 'qword'
            ps = 'pd' if packed else 'sd'
        if self.regs.is_zmm(xmm1):
            mem = 'zword'
        elif self.regs.is_ymm(xmm1):
            mem = 'yword'

        if xmm3 is not None:
            return '%s%s %s, %s, %s\n' % (inst, ps, xmm1, xmm2, xmm3)
        else:
            off = ' + %i' % offset if offset else ''
            return '%s%s %s, %s, %s [%s%s]\n' % (inst, ps, xmm1, xmm2, mem, name, off)

    def _fma_inst(self, order, negate, op):
        if order == '213':
            if negate:
                # dst_xmm = -(dst_xmm * src1) + [src2, name]
                inst = 'vfnmsub213' if op == '-' else 'vfnmadd213'
            else:
                # dst_xmm = dst_xmm * src1 + [src2, name]
                inst = 'vfmsub213' if op == '-' else 'vfmadd213'
        elif order == '231':
            if negate:
                inst = 'vfnmsub231' if op == '-' else 'vfnmadd231'
            else:
                inst = 'vfmsub231' if op == '-' else 'vfmadd231'
        return inst

    def fma_f64_213(self, xmm1, xmm2, op, negate, xmm3=None, name=None):
        inst = self._fma_inst('213', negate, op)
        return self._fma_f64_f32(inst, xmm1, xmm2, op, False, False, xmm3=xmm3, name=name)

    def fma_f64_231(self, xmm1, xmm2, op, negate, xmm3=None, name=None):
        inst = self._fma_inst('231', negate, op)
        return self._fma_f64_f32(inst, xmm1, xmm2, op, False, False, xmm3=xmm3, name=name)

    def fma_f32_213(self, xmm1, xmm2, op, negate, xmm3=None, name=None):
        inst = self._fma_inst('213', negate, op)
        return self._fma_f64_f32(inst, xmm1, xmm2, op, True, False, xmm3=xmm3, name=name)

    def fma_f32_231(self, xmm1, xmm2, op, negate, xmm3=None, name=None):
        inst = self._fma_inst('231', negate, op)
        return self._fma_f64_f32(inst, xmm1, xmm2, op, True, False, xmm3=xmm3, name=name)

    def fma_f64x2_213(self, xmm1, xmm2, op, negate, xmm3=None, name=None):
        inst = self._fma_inst('213', negate, op)
        return self._fma_f64_f32(inst, xmm1, xmm2, op, False, True, xmm3=xmm3, name=name)

    def fma_f64x2_231(self, xmm1, xmm2, op, negate, xmm3=None, name=None):
        inst = self._fma_inst('231', negate, op)
        return self._fma_f64_f32(inst, xmm1, xmm2, op, False, True, xmm3=xmm3, name=name)

    def fma_f64x4_213(self, ymm1, ymm2, op, negate, ymm3=None, name=None, offset=None):
        inst = self._fma_inst('213', negate, op)
        return self._fma_f64_f32(inst, ymm1, ymm2, op, False, True, xmm3=ymm3, name=name, offset=offset)

    def fma_f64x8_213(self, zmm1, zmm2, op, negate, zmm3=None, name=None, offset=None):
        inst = self._fma_inst('213', negate, op)
        return self._fma_f64_f32(inst, zmm1, zmm2, op, False, True, xmm3=zmm3, name=name, offset=offset)

    def fma_f64x4_231(self, ymm1, ymm2, op, negate, ymm3=None, name=None, offset=None):
        inst = self._fma_inst('231', negate, op)
        return self._fma_f64_f32(inst, ymm1, ymm2, op, False, True, xmm3=ymm3, name=name, offset=offset)

    def fma_f64x8_231(self, zmm1, zmm2, op, negate, zmm3=None, name=None, offset=None):
        inst = self._fma_inst('231', negate, op)
        return self._fma_f64_f32(inst, zmm1, zmm2, op, False, True, xmm3=zmm3, name=name, offset=offset)

    def fma_f32x4_213(self, xmm1, xmm2, op, negate, xmm3=None, name=None):
        inst = self._fma_inst('213', negate, op)
        return self._fma_f64_f32(inst, xmm1, xmm2, op, True, True, xmm3=xmm3, name=name)

    def fma_f32x4_231(self, xmm1, xmm2, op, negate, xmm3=None, name=None):
        inst = self._fma_inst('231', negate, op)
        return self._fma_f64_f32(inst, xmm1, xmm2, op, True, True, xmm3=xmm3, name=name)

    def fma_f32x8_213(self, ymm1, ymm2, op, negate, ymm3=None, name=None, offset=None):
        inst = self._fma_inst('213', negate, op)
        return self._fma_f64_f32(inst, ymm1, ymm2, op, True, True, xmm3=ymm3, name=name, offset=offset)

    def fma_f32x16_213(self, zmm1, zmm2, op, negate, zmm3=None, name=None, offset=None):
        inst = self._fma_inst('213', negate, op)
        return self._fma_f64_f32(inst, zmm1, zmm2, op, True, True, xmm3=zmm3, name=name, offset=offset)

    def fma_f32x8_231(self, ymm1, ymm2, op, negate, ymm3=None, name=None, offset=None):
        inst = self._fma_inst('231', negate, op)
        return self._fma_f64_f32(inst, ymm1, ymm2, op, True, True, xmm3=ymm3, name=name, offset=offset)

    def fma_f32x16_231(self, zmm1, zmm2, op, negate, zmm3=None, name=None, offset=None):
        inst = self._fma_inst('231', negate, op)
        return self._fma_f64_f32(inst, zmm1, zmm2, op, True, True, xmm3=zmm3, name=name, offset=offset)

    def load_addr(self, ptr_reg, name):
        return 'lea %s, byte [%s]\n' % (ptr_reg, name)

    def _abs_f32_f32x4(self, xmm, tmp_xmm):
        if self.cpu.AVX512F:
            code = 'vpslld %s, %s, 1\n' % (xmm, xmm)
            code += 'vpsrld %s, %s, 1\n' % (xmm, xmm)
        elif self.cpu.AVX:
            code = 'vpcmpeqw %s, %s, %s\n' % (tmp_xmm, tmp_xmm, tmp_xmm)
            code += 'vpsrld %s, %s, 1\n' % (tmp_xmm, tmp_xmm)
            code += 'vandps %s, %s, %s\n' % (xmm, xmm, tmp_xmm)
        else:
            code = 'pcmpeqw %s, %s\n' % (tmp_xmm, tmp_xmm)
            code += 'psrld %s, 1\n' % tmp_xmm
            code += 'andps %s, %s\n' % (xmm, tmp_xmm)
        return code

    def _abs_f64_f64x2(self, xmm, tmp_xmm):
        if self.cpu.AVX512F:
            code = 'vpsllq %s, %s, 1\n' % (xmm, xmm)
            code += 'vpsrlq %s, %s, 1\n' % (xmm, xmm)
        elif self.cpu.AVX:
            code = 'vpcmpeqw %s, %s, %s\n' % (tmp_xmm, tmp_xmm, tmp_xmm)
            code += 'vpsrlq %s, %s, 1\n' % (tmp_xmm, tmp_xmm)
            code += 'vandpd %s, %s, %s\n' % (xmm, xmm, tmp_xmm)
        else:
            code = 'pcmpeqw %s, %s\n' % (tmp_xmm, tmp_xmm)
            code += 'psrlq %s, 1\n' % tmp_xmm
            code += 'andpd %s, %s\n' % (xmm, tmp_xmm)
        return code

    def abs_f64(self, xmm, tmp_xmm):
        return self._abs_f64_f64x2(xmm, tmp_xmm)

    def abs_f64x2(self, xmm, tmp_xmm):
        return self._abs_f64_f64x2(xmm, tmp_xmm)

    def abs_f32(self, xmm, tmp_xmm):
        return self._abs_f32_f32x4(xmm, tmp_xmm)

    def abs_f32x4(self, xmm, tmp_xmm):
        return self._abs_f32_f32x4(xmm, tmp_xmm)

    def abs_f64x2_x2(self, xmm1, xmm2, tmp_xmm, ptr_reg, bit32=False):
        inst = 'andps' if bit32 else 'andpd'
        shift = 'psrld' if bit32 else 'psrlq'
        if self.cpu.AVX:
            code = 'vpcmpeqw %s, %s, %s\n' % (tmp_xmm, tmp_xmm, tmp_xmm)
            code += 'v%s %s, %s, 1\n' % (shift, tmp_xmm, tmp_xmm)
            code += 'v%s %s, %s, oword [%s]\n' % (inst, xmm1, tmp_xmm, ptr_reg)
            code += 'v%s %s, %s, oword [%s + 16]\n' % (inst, xmm2, tmp_xmm, ptr_reg)
        else:
            code = 'pcmpeqw %s, %s\n' % (tmp_xmm, tmp_xmm)
            code += '%s %s, 1\n' % (shift, tmp_xmm)
            code += 'movaps %s, %s\n' % (xmm1, tmp_xmm)
            code += '%s %s, oword[%s]\n' % (inst, xmm1, ptr_reg)
            code += 'movaps %s, %s\n' % (xmm2, tmp_xmm)
            code += '%s %s, oword[%s + 16]\n' % (inst, xmm2, ptr_reg)
        return code

    def abs_f32x4_x2(self, xmm1, xmm2, tmp_xmm, ptr_reg):
        return self.abs_f64x2_x2(xmm1, xmm2, tmp_xmm, ptr_reg, bit32=True)

    def abs_f64x2_x4(self, xmm1, xmm2, xmm3, xmm4, tmp_xmm, ptr_reg, bit32=False):
        inst = 'andps' if bit32 else 'andpd'
        shift = 'psrld' if bit32 else 'psrlq'
        if self.cpu.AVX:
            code = 'vpcmpeqw %s, %s, %s\n' % (tmp_xmm, tmp_xmm, tmp_xmm)
            code += 'v%s %s, %s, 1\n' % (shift, tmp_xmm, tmp_xmm)
            code += 'v%s %s, %s, oword [%s]\n' % (inst, xmm1, tmp_xmm, ptr_reg)
            code += 'v%s %s, %s, oword [%s + 16]\n' % (inst, xmm2, tmp_xmm, ptr_reg)
            code += 'v%s %s, %s, oword [%s + 32]\n' % (inst, xmm3, tmp_xmm, ptr_reg)
            code += 'v%s %s, %s, oword [%s + 48]\n' % (inst, xmm4, tmp_xmm, ptr_reg)
        else:
            code = 'pcmpeqw %s, %s\n' % (tmp_xmm, tmp_xmm)
            code += '%s %s, 1\n' % (shift, tmp_xmm)
            code += 'movaps %s, %s\n' % (xmm1, tmp_xmm)
            code += '%s %s, oword[%s]\n' % (inst, xmm1, ptr_reg)
            code += 'movaps %s, %s\n' % (xmm2, tmp_xmm)
            code += '%s %s, oword[%s + 16]\n' % (inst, xmm2, ptr_reg)
            code += 'movaps %s, %s\n' % (xmm3, tmp_xmm)
            code += '%s %s, oword[%s + 32]\n' % (inst, xmm3, ptr_reg)
            code += 'movaps %s, %s\n' % (xmm4, tmp_xmm)
            code += '%s %s, oword[%s + 48]\n' % (inst, xmm4, ptr_reg)
        return code

    def abs_f32x4_x4(self, xmm1, xmm2, xmm3, xmm4, tmp_xmm, ptr_reg):
        return self.abs_f64x2_x4(xmm1, xmm2, xmm3, xmm4, tmp_xmm, ptr_reg, bit32=True)

    def abs_f64x4_x2(self, ymm1, ymm2, tmp_ymm, ptr_reg, bit32=False):
        inst = 'vandps' if bit32 else 'vandpd'
        shift = 'vpsrld' if bit32 else 'vpsrlq'
        if self.cpu.AVX2:
            code = 'vpcmpeqw %s, %s, %s\n' % (tmp_ymm, tmp_ymm, tmp_ymm)
            code += '%s %s, %s, 1\n' % (shift, tmp_ymm, tmp_ymm)
            code += '%s %s, %s, yword [%s]\n' % (inst, ymm1, tmp_ymm, ptr_reg)
            code += '%s %s, %s, yword [%s + 32]\n' % (inst, ymm2, tmp_ymm, ptr_reg)
        else:
            rxmm = 'x' + tmp_ymm[1:]
            code = 'vpcmpeqw %s, %s, %s\n' % (rxmm, rxmm, rxmm)
            code += '%s %s, %s, 1\n' % (shift, rxmm, rxmm)
            code += 'vinsertf128 %s, %s, %s, 1\n' % (tmp_ymm, tmp_ymm, rxmm)
            code += '%s %s, %s, yword [%s]\n' % (inst, ymm1, tmp_ymm, ptr_reg)
            code += '%s %s, %s, yword [%s + 32]\n' % (inst, ymm2, tmp_ymm, ptr_reg)
        return code

    def abs_f32x8_x2(self, ymm1, ymm2, tmp_ymm, ptr_reg):
        return self.abs_f64x4_x2(ymm1, ymm2, tmp_ymm, ptr_reg, bit32=True)

    def _abs_f64x3_f64x4(self, ymm, tmp_ymm, bit32=False):
        if self.cpu.AVX512F:
            if bit32:
                code = 'vpslld %s, %s, 1\n' % (ymm, ymm)
                code += 'vpsrld %s, %s, 1\n' % (ymm, ymm)
            else:
                code = 'vpsllq %s, %s, 1\n' % (ymm, ymm)
                code += 'vpsrlq %s, %s, 1\n' % (ymm, ymm)
            return code

        inst = 'vandps' if bit32 else 'vandpd'
        shift = 'vpsrld' if bit32 else 'vpsrlq'
        if self.cpu.AVX2:
            code = 'vpcmpeqw %s, %s, %s\n' % (tmp_ymm, tmp_ymm, tmp_ymm)
            code += '%s %s, %s, 1\n' % (shift, tmp_ymm, tmp_ymm)
            code += '%s %s, %s, %s\n' % (inst, ymm, ymm, tmp_ymm)
        else:
            rxmm = 'x' + tmp_ymm[1:]
            code = 'vpcmpeqw %s, %s, %s\n' % (rxmm, rxmm, rxmm)
            code += '%s %s, %s, 1\n' % (shift, rxmm, rxmm)
            code += 'vinsertf128 %s, %s, %s, 1\n' % (tmp_ymm, tmp_ymm, rxmm)
            code += '%s %s, %s, %s\n' % (inst, ymm, ymm, tmp_ymm)
        return code

    def abs_f64x3(self, ymm, tmp_ymm):
        return self._abs_f64x3_f64x4(ymm, tmp_ymm, bit32=False)

    def abs_f64x4(self, ymm, tmp_ymm):
        return self._abs_f64x3_f64x4(ymm, tmp_ymm, bit32=False)

    def abs_f32x8(self, ymm, tmp_ymm):
        return self._abs_f64x3_f64x4(ymm, tmp_ymm, bit32=True)

    def copysign_f64x2(self, xmm1, xmm2, tmp_xmm):
        if self.cpu.AVX:
            code = 'vpcmpeqw %s, %s, %s\n' % (tmp_xmm, tmp_xmm, tmp_xmm)
            code += 'vpsllq %s, %s, 63\n' % (tmp_xmm, tmp_xmm)
            code += 'vandpd %s, %s, %s\n' % (xmm2, xmm2, tmp_xmm)
            code += 'vandnpd %s, %s, %s\n' % (tmp_xmm, tmp_xmm, xmm1)
            code += 'vxorpd %s, %s, %s\n' % (xmm2, tmp_xmm, xmm2)
        else:
            code = 'pcmpeqw %s, %s\n' % (tmp_xmm, tmp_xmm)
            code += 'psllq %s, 63\n' % tmp_xmm
            code += 'andpd %s, %s\n' % (xmm2, tmp_xmm)
            code += 'andnpd %s, %s\n' % (tmp_xmm, xmm1)
            code += 'xorpd %s, %s\n' % (xmm2, tmp_xmm)
        return code

    def copysign_f32x4(self, xmm1, xmm2, tmp_xmm):
        if self.cpu.AVX:
            code = 'vpcmpeqw %s, %s, %s\n' % (tmp_xmm, tmp_xmm, tmp_xmm)
            code += 'vpslld %s, %s, 31\n' % (tmp_xmm, tmp_xmm)
            code += 'vandps %s, %s, %s\n' % (xmm2, xmm2, tmp_xmm)
            code += 'vandnps %s, %s, %s\n' % (tmp_xmm, tmp_xmm, xmm1)
            code += 'vxorps %s, %s, %s\n' % (xmm2, tmp_xmm, xmm2)
        else:
            code = 'pcmpeqw %s, %s\n' % (tmp_xmm, tmp_xmm)
            code += 'pslld %s, 31\n' % tmp_xmm
            code += 'andps %s, %s\n' % (xmm2, tmp_xmm)
            code += 'andnps %s, %s\n' % (tmp_xmm, xmm1)
            code += 'xorps %s, %s\n' % (xmm2, tmp_xmm)
        return code

    def copysign_f64x4(self, ymm1, ymm2, tmp_ymm):
        if self.cpu.AVX2:
            code = 'vpcmpeqw %s, %s, %s\n' % (tmp_ymm, tmp_ymm, tmp_ymm)
            code += 'vpsllq %s, %s, 63\n' % (tmp_ymm, tmp_ymm)
            code += 'vandpd %s, %s, %s\n' % (ymm2, ymm2, tmp_ymm)
            code += 'vandnpd %s, %s, %s\n' % (tmp_ymm, tmp_ymm, ymm1)
            code += 'vxorpd %s, %s, %s\n' % (ymm2, tmp_ymm, ymm2)
        else:
            rxmm = 'x' + tmp_ymm[1:]
            code = 'vpcmpeqw %s, %s, %s\n' % (rxmm, rxmm, rxmm)
            code += 'vpsllq %s, %s, 63\n' % (rxmm, rxmm)
            code += 'vinsertf128 %s, %s, %s, 1\n' % (tmp_ymm, tmp_ymm, rxmm)
            code += 'vandpd %s, %s, %s\n' % (ymm2, ymm2, tmp_ymm)
            code += 'vandnpd %s, %s, %s\n' % (tmp_ymm, tmp_ymm, ymm1)
            code += 'vxorpd %s, %s, %s\n' % (ymm2, tmp_ymm, ymm2)
        return code

    def copysign_f32x8(self, ymm1, ymm2, tmp_ymm):
        if self.cpu.AVX2:
            code = 'vpcmpeqw %s, %s, %s\n' % (tmp_ymm, tmp_ymm, tmp_ymm)
            code += 'vpslld %s, %s, 31\n' % (tmp_ymm, tmp_ymm)
            code += 'vandps %s, %s, %s\n' % (ymm2, ymm2, tmp_ymm)
            code += 'vandnps %s, %s, %s\n' % (tmp_ymm, tmp_ymm, ymm1)
            code += 'vxorps %s, %s, %s\n' % (ymm2, tmp_ymm, ymm2)
        else:
            rxmm = 'x' + tmp_ymm[1:]
            code = 'vpcmpeqw %s, %s, %s\n' % (rxmm, rxmm, rxmm)
            code += 'vpslld %s, %s, 31\n' % (rxmm, rxmm)
            code += 'vinsertf128 %s, %s, %s, 1\n' % (tmp_ymm, tmp_ymm, rxmm)
            code += 'vandps %s, %s, %s\n' % (ymm2, ymm2, tmp_ymm)
            code += 'vandnps %s, %s, %s\n' % (tmp_ymm, tmp_ymm, ymm1)
            code += 'vxorps %s, %s, %s\n' % (ymm2, tmp_ymm, ymm2)
        return code

    def broadcast_f64(self, xmm):
        if self.cpu.AVX or self.cpu.AVX512F:
            return "vpermilpd %s, %s, 0\n" % (xmm, xmm)
        else:
            return "shufpd %s, %s, 0\n" % (xmm, xmm)

    def broadcast_f32(self, xmm):
        if self.cpu.AVX or self.cpu.AVX512F:
            return "vpermilps %s, %s, 0\n" % (xmm, xmm)
        else:
            return "shufps %s, %s, 0\n" % (xmm, xmm)

    def broadcast_i32(self, xmm):
        if self.cpu.AVX or self.cpu.AVX512F:
            return "vpshufd %s, %s, 0\n" % (xmm, xmm)
        else:
            return "pshufd %s, %s, 0\n" % (xmm, xmm)

    def conv_i32x2_to_f64x2(self, dst_reg, xmm=None, name=None):
        inst = 'vcvtdq2pd' if self.cpu.AVX or self.cpu.AVX512F else 'cvtdq2pd'
        if xmm:
            return '%s %s, %s\n' % (inst, dst_reg, xmm)
        else:
            return '%s %s, qword [%s]\n' % (inst, dst_reg, name)

    def conv_f64x2_to_i32x2(self, dst_reg, xmm=None, name=None):
        inst = 'vcvttpd2dq' if self.cpu.AVX or self.cpu.AVX512F else 'cvttpd2dq'
        if xmm:
            return '%s %s, %s\n' % (inst, dst_reg, xmm)
        else:
            return '%s %s, oword [%s]\n' % (inst, dst_reg, name)

    def conv_i32x4_to_f32x4(self, dst_reg, xmm=None, name=None):
        inst = 'vcvtdq2ps' if self.cpu.AVX or self.cpu.AVX512F else 'cvtdq2ps'
        if xmm:
            return '%s %s, %s\n' % (inst, dst_reg, xmm)
        else:
            return '%s %s, oword [%s]\n' % (inst, dst_reg, name)

    def conv_f32x2_to_i32x2(self, dst_reg, xmm=None, name=None):
        inst = 'vcvttps2dq' if self.cpu.AVX or self.cpu.AVX512F else 'cvttps2dq'
        if xmm:
            return '%s %s, %s\n' % (inst, dst_reg, xmm)
        else:
            return '%s %s, oword [%s]\n' % (inst, dst_reg, name)

    def conv_f32x2_to_f64x2(self, dst_reg, xmm=None, name=None):
        inst = 'vcvtps2pd' if self.cpu.AVX or self.cpu.AVX512F else 'cvtps2pd'
        if xmm:
            return '%s %s, %s\n' % (inst, dst_reg, xmm)
        else:
            return '%s %s, qword [%s]\n' % (inst, dst_reg, name)

    def conv_f64x2_to_f32x2(self, dst_reg, xmm=None, name=None):
        inst = 'vcvtpd2ps' if self.cpu.AVX or self.cpu.AVX512F else 'cvtpd2ps'
        if xmm:
            return '%s %s, %s\n' % (inst, dst_reg, xmm)
        else:
            return '%s %s, oword [%s]\n' % (inst, dst_reg, name)

    def _sqrt_f32_f64(self, xmm, inst, mem, name=None):
        if name is not None:
            if self.cpu.AVX or self.cpu.AVX512F:
                code = 'v%s %s, %s, %s [%s]\n' % (inst, xmm, xmm, mem, name)
            else:
                code = '%s %s, %s [%s]\n' % (inst, xmm, mem, name)
        else:
            if self.cpu.AVX or self.cpu.AVX512F:
                code = 'v%s %s, %s, %s\n' % (inst, xmm, xmm, xmm)
            else:
                code = '%s %s, %s\n' % (inst, xmm, xmm)
        return code

    def sqrt_f32(self, xmm, name=None):
        return self._sqrt_f32_f64(xmm, 'sqrtss', 'dword', name=name)

    def sqrt_f64(self, xmm, name=None):
        return self._sqrt_f32_f64(xmm, 'sqrtsd', 'qword', name=name)

    def sqrt_f64x2(self, xmm, name=None):
        if name is not None:
            if self.cpu.AVX or self.cpu.AVX512F:
                code = 'vsqrtpd %s, oword[%s]\n' % (xmm, name)
            else:
                code = 'sqrtpd %s, oword[%s]\n' % (xmm, name)
        else:
            if self.cpu.AVX or self.cpu.AVX512F:
                code = 'vsqrtpd %s, %s\n' % (xmm, xmm)
            else:
                code = 'sqrtpd %s, %s\n' % (xmm, xmm)
        return code

    def sqrt_f32x4(self, xmm, name=None):
        if name is not None:
            if self.cpu.AVX or self.cpu.AVX512F:
                code = 'vsqrtps %s, oword[%s]\n' % (xmm, name)
            else:
                code = 'sqrtps %s, oword[%s]\n' % (xmm, name)
        else:
            if self.cpu.AVX or self.cpu.AVX512F:
                code = 'vsqrtps %s, %s\n' % (xmm, xmm)
            else:
                code = 'sqrtps %s, %s\n' % (xmm, xmm)
        return code
