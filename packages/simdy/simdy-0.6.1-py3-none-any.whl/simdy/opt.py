import re
from .regs import Regs


class FunctionOptimizer:
    def __init__(self, cgen, code, stores):
        self._cgen = cgen
        self._code = code
        self._stores = stores.copy()
        self._regs = Regs()

        self._ok_insts = frozenset([
            'mov', 'add', 'adc', 'sub', 'sbb', 'imul', 'mul', 'neg', 'cmp' 'and', 'or', 'xor', 'not',
            'sar', 'shr', 'sal', 'shl', 'ror', 'rol', 'rcr', 'rcl',

            'movd', 'movq', 'packssdw', 'packuswb', 'punpckhbw', 'punpckhwd', 'punpckhdq',
            'punpcklbw', 'punpcklwd', 'punpckldq', 'paddd', 'psubd', 'pcmpeqd', 'pcmpgtd', 'pand',
            'pandn', 'por', 'pxor', 'pslld', 'psllq', 'psrld', 'psrlq', 'psrad',

            'movaps', 'movups', 'movss', 'addps', 'addss', 'subps', 'subss', 'mulps', 'mulss', 'divps', 'divss',
            'sqrtps', 'sqrtss', 'maxps', 'maxss', 'minps', 'minss', 'cmpps', 'cmpss', 'comiss', 'ucomiss',
            'andps', 'andnps', 'orps', 'xorps', 'shufps', 'unpckhps', 'unpcklps', 'cvtpi2ps', 'cvtsi2ss',
            'cvtps2pi', 'cvttps2pi', 'cvtss2si', 'cvttss2si',

            'movapd', 'movupd', 'movsd', 'addpd', 'addsd', 'subpd', 'subsd', 'mulpd', 'mulsd', 'divpd',
            'divsd', 'sqrtpd', 'sqrtsd', 'maxpd', 'maxsd', 'minpd', 'minsd', 'cmppd', 'cmpsd', 'comisd',
            'ucomisd', 'andpd', 'andnpd', 'orpd', 'xorpd', 'shufpd', 'unpckhpd', 'unpcklpd', 'cvtpd2pi',
            'cvttpd2pi', 'cvtpi2pd', 'cvtpd2dq', 'cvttpd2dq', 'cvtdq2pd', 'cvtps2pd', 'cvtpd2ps','cvtss2sd',
            'cvtsd2ss', 'cvtsd2si', 'cvttsd2si', 'cvtsi2sd', 'cvtdq2ps', 'cvtps2dq', 'cvttps2dq',
            'movdqa', 'movdqu', 'paddq', 'psubq', 'pshufd', 'pslldq', 'psrldq', 'punpckhqdq', 'punpcklqdq',

            'movsldup', 'movshdup', 'movddup', 'pabsd', 'palignr',

            'pmulld', 'pmuldq', 'dppd', 'dpps', 'blendpd', 'blendps', 'pminud', 'pminsd', 'pmaxud', 'pmaxsd',
            'roundps', 'roundpd', 'roundss', 'roundsd', 'extractps', 'insertps', 'pinsrd', 'pinsrq', 'pextrd',
            'pextrq', 'pmovsxdq', 'pmovzxdq', 'ptest', 'pcmpeqq', 'pcmpgtq',

            'vmovd', 'vmovq', 'vpackuswb', 'vpunpckhbw', 'vpunpckhwd', 'vpunpckhdq', 'vpunpcklbw', 'vpunpcklwd',
            'vpunpckldq', 'vpaddd', 'vpsubb', 'vpsubd', 'vpsubsb', 'vpmaddwd', 'vpcmpeqd', 'vpcmpgtd',

            'vpand', 'vpandn', 'vpor', 'vpxor', 'vpsllw', 'vpslld', 'vpsllq', 'vpsrlw', 'vpsrld', 'vpsrlq', 'vpsraw',
            'vpsrad', 'vmovaps', 'vmovups', 'vmovss', 'vaddps', 'vaddss', 'vsubps', 'vsubss', 'vmulps', 'vmulss',
            'vdivps', 'vdivss', 'vsqrtps', 'vsqrtss', 'vmaxps', 'vmaxss', 'vminps', 'vminss', 'vcmpps', 'vcmpss',
            'vcomiss', 'vucomiss', 'vandps', 'vandnps', 'vorps', 'vxorps', 'vshufps', 'vunpckhps', 'vunpcklps',

            'vcvtsi2ss', 'vcvtss2si', 'vcvttss2si', 'vmovapd', 'vmovupd', 'vmovsd', 'vaddpd', 'vaddsd',

            'vsubpd', 'vsubsd', 'vmulpd', 'vmulsd', 'vdivpd', 'vdivsd', 'vsqrtpd', 'vsqrtsd', 'vmaxpd',
            'vmaxsd', 'vminpd', 'vminsd', 'vcmppd', 'vcmpsd', 'vcomisd', 'vucomisd', 'vandpd', 'vandnpd', 'vorpd',
            'vxorpd', 'vshufpd', 'vunpckhpd', 'vunpcklpd', 'vcvtpd2dq', 'vcvttpd2dq', 'vcvtdq2pd', 'vcvtps2pd',
            'vcvtpd2ps', 'vcvtss2sd', 'vcvtsd2ss', 'vcvtsd2si', 'vcvttsd2si', 'vcvtsi2sd', 'vcvtdq2ps', 'vcvtps2dq',
            'vcvttps2dq', 'vmovdqa', 'vmovdqu', 'vpaddq', 'vpsubq', 'vpshufd', 'vpslldq', 'vpsrldq', 'vpunpckhqdq',
            'vpunpcklqdq', 'vmovsldup', 'vmovshdup', 'vmovddup', 'vpabsd', 'vpalignr',

            'vpmulld', 'vpmuldq', 'vdppd', 'vdpps', 'vblendpd', 'vblendps', 'vblendvpd', 'vblendvps', 'vpblendvb',
            'vpblendw', 'vpminud', 'vpminsd', 'vpmaxud', 'vpmaxsd', 'vroundps', 'vroundpd', 'vroundss', 'vroundsd',
            'vextractps', 'vinsertps', 'vpinsrd', 'vpinsrq', 'vpextrd', 'vpextrq', 'vpmovsxdq', 'vpmovzxdq',
            'vptest', 'vpcmpeqq', 'vpcmpgtq',

            'vfmadd132ps', 'vfmadd132ss', 'vfmadd132pd', 'vfmadd132sd', 'vfmadd213ps', 'vfmadd213ss', 'vfmadd213pd',
            'vfmadd213sd', 'vfmadd231ps', 'vfmadd231ss', 'vfmadd231pd', 'vfmadd231sd', 'vfmaddsub132ps',
            'vfmaddsub132pd', 'vfmaddsub213ps', 'vfmaddsub213pd', 'vfmaddsub231ps', 'vfmaddsub231pd', 'vfmsubadd132ps',
            'vfmsubadd132pd', 'vfmsubadd213ps', 'vfmsubadd213pd', 'vfmsubadd231ps', 'vfmsubadd231pd', 'vfmsub132ps',
            'vfmsub132ss', 'vfmsub213ps', 'vfmsub213ss', 'vfmsub231ps', 'vfmsub231ss', 'vfmsub132pd', 'vfmsub132sd',
            'vfmsub213pd', 'vfmsub213sd', 'vfmsub231pd', 'vfmsub231sd', 'vfnmadd132ps', 'vfnmadd132ss', 'vfnmadd213ps',
            'vfnmadd213ss', 'vfnmadd231ps', 'vfnmadd231ss', 'vfnmadd132pd', 'vfnmadd132sd', 'vfnmadd213pd',
            'vfnmadd213sd', 'vfnmadd231pd', 'vfnmadd231sd', 'vfnmsub132ps', 'vfnmsub132ss', 'vfnmsub213ps',
            'vfnmsub213ss', 'vfnmsub231ps', 'vfnmsub231ss', 'vfnmsub132pd', 'vfnmsub132sd', 'vfnmsub213pd',
            'vfnmsub213sd', 'vfnmsub231pd', 'vfnmsub231sd',

            'vextractf128', 'vinsertf128', 'vpermilpd', 'vpermilps', 'vperm2f128', 'vtestps', 'vtestpd',

            'vextracti128', 'vinserti128', 'vperm2i128', 'vpermd',
            'vpermps', 'vpermq', 'vpermpd', 'vpblendd', 'vpsllvd', 'vpsllvq', 'vpsravd', 'vpsrlvd', 'vpsrlvq',

            'vpandd', 'vpandq', 'vpandnd', 'vpandnq', 'vpord', 'vporq', 'vpxord', 'vpxorq', 'vpsraq',
            'vmovdqa32', 'vmovdqa64', 'vmovdqu32', 'vmovdqu64', 'vpabsq', 'vpmullq', 'vpminuq', 'vpminsq',
            'vpmaxuq', 'vpmaxsq', 'vextractf32x4', 'vextractf32x8', 'vextractf64x2', 'vextractf64x4',
            'vinsertf32x4', 'vinsertf32x8', 'vinsertf64x2', 'vinsertf64x4',

            'vextracti32x4', 'vextracti32x8', 'vextracti64x2', 'vextracti64x4', 'vinserti32x4', 'vinserti32x8',
            'vinserti64x2', 'vinserti64x4', 'vpsllvw', 'vpsravq', 'vpsravw', 'vpsrlvw', 'vrndscaless',
            'vrndscaleps', 'vrndscalesd', 'vrndscalepd', 'vblendmps', 'vblendmpd',
            'vpmovqd', 'vpmovsqd', 'vpmovusqd', 'vpmovqb', 'vpmovsqb', 'vpmovusqb', 'vpmovqw', 'vpmovsqw',
            'vpmovusqw', 'vscalefss', 'vscalefps', 'vscalefsd', 'vscalefpd',

        ])

        self._mem_ok_inst = frozenset([
            'movd', 'movq', 'movss','addss', 'subss', 'mulss', 'divss', 'sqrtss', 'maxss', 'minss', 'cmpss',
            'comiss', 'ucomiss', 'cvtsi2ss',

            'movsd', 'addsd', 'subsd', 'mulsd', 'divsd', 'sqrtsd', 'maxsd', 'minsd', 'cmpsd', 'comisd',
            'ucomisd',  'cvtss2sd', 'cvtsd2ss', 'cvtsd2si', 'cvttsd2si', 'cvtsi2sd',
            'roundss', 'roundsd', 'extractps', 'insertps', 'pinsrd', 'pinsrq', 'pextrd',
            'pextrq', 'vmovd', 'vmovq', 'vmovss', 'vaddss', 'vsubss', 'vmulss', 'vdivss', 'vsqrtss', 'vmaxss', 'vminss',
            'vcmpss', 'vcomiss', 'vucomiss', 'vcvtsi2ss', 'vcvtss2si', 'vcvttss2si',  'vmovsd', 'vaddsd',
            'vsubsd', 'vmulsd', 'vdivsd', 'vsqrtsd', 'vmaxsd', 'vminsd', 'vcmpsd', 'vcomisd', 'vucomisd',

            'vcvtss2sd', 'vcvtsd2ss', 'vcvtsd2si', 'vcvttsd2si', 'vcvtsi2sd', 'vroundss', 'vroundsd',
            'vextractps', 'vinsertps', 'vpinsrd', 'vpinsrq', 'vpextrd', 'vpextrq',

            'vfmadd132ss', 'vfmadd132sd', 'vfmadd213ss',
            'vfmadd213sd', 'vfmadd231ss', 'vfmadd231sd', 'vfmsub132ss', 'vfmsub213ss', 'vfmsub231ss', 'vfmsub132sd',
            'vfmsub213sd', 'vfmsub231sd', 'vfnmadd132ss', 'vfnmadd213ss', 'vfnmadd231ss', 'vfnmadd132sd',
            'vfnmadd213sd', 'vfnmadd231sd', 'vfnmsub132ss', 'vfnmsub213ss', 'vfnmsub231ss', 'vfnmsub132sd',
            'vfnmsub213sd', 'vfnmsub231pd', 'vfnmsub231sd',

            'vrndscaless', 'vrndscalesd', 'vscalefss', 'vscalefsd',

        ])

    def _ret_unused_regs(self):
        general = [('r15', 'r15d'), ('r14', 'r14d'), ('r12', 'r12d'), ('r11', 'r11d'),
                   ('r10', 'r10d'), ('r9', 'r9d'), ('r8', 'r8d'), ('rdi', 'edi'), ('rsi', 'esi')]

        xmms = [('xmm15', 'ymm15', 'zmm15'), ('xmm14', 'ymm14', 'zmm14'), ('xmm13', 'ymm13', 'zmm13'),
                ('xmm12', 'ymm12', 'zmm12'), ('xmm11', 'ymm11', 'zmm11'), ('xmm10', 'ymm10', 'zmm10'),
                ('xmm9', 'ymm9', 'zmm9'), ('xmm8', 'ymm8', 'zmm8'), ('xmm7', 'ymm7', 'zmm7'),
                ('xmm6', 'ymm6', 'zmm6'), ('xmm5', 'ymm5', 'zmm5'), ('xmm4', 'ymm4', 'zmm4')]

        if self._cgen.cpu.AVX512F:
            new_r = [('xmm31', 'ymm31', 'zmm31'), ('xmm30', 'ymm30', 'zmm30'), ('xmm29', 'ymm29', 'zmm29'),
                     ('xmm28', 'ymm28', 'zmm28'), ('xmm27', 'ymm27', 'zmm27'), ('xmm26', 'ymm26', 'zmm26'),
                     ('xmm25', 'ymm25', 'zmm25'), ('xmm24', 'ymm24', 'zmm24'), ('xmm23', 'ymm23', 'zmm23'),
                     ('xmm22', 'ymm22', 'zmm22'), ('xmm21', 'ymm21', 'zmm21'), ('xmm20', 'ymm20', 'zmm20'),
                     ('xmm19', 'ymm19', 'zmm19'), ('xmm18', 'ymm18', 'zmm18'), ('xmm17', 'ymm17', 'zmm17'),
                     ('xmm16', 'ymm16', 'zmm16')]
            xmms = new_r + xmms

        unused_general = []
        code = self._code
        for r64, r32 in general:
            if r64 in code or r32 in code:
                continue
            unused_general.append((r64, r32))

        unused_xmms = []
        for xmm, ymm, zmm in xmms:
            if xmm in code or ymm in code or zmm in code:
                continue
            unused_xmms.append((xmm, ymm, zmm))

        return unused_general, unused_xmms

    def _build_args_map(self):
        general, xmms = self._ret_unused_regs()
        stores = self._stores
        cgen = self._cgen
        arg_map = {}
        while True:
            if len(stores) == 0:
                break
            arg, n = stores.popitem()
            # TODO multi part args not supported in optimization, add support
            if arg.is_multi_part(cgen):
                continue
            acum = arg.acum_type(cgen)
            if acum == 'general' and len(general) > 0:
                arg_map[arg] = general.pop()[1]
            elif acum == 'general64' and len(general) > 0:
                arg_map[arg] = general.pop()[0]
            elif acum == 'xmm' and len(xmms) > 0:
                arg_map[arg] = xmms.pop()[0]
            elif acum == 'ymm' and len(xmms) > 0:
                arg_map[arg] = xmms.pop()[1]
            elif acum == 'zmm' and len(xmms) > 0:
                arg_map[arg] = xmms.pop()[2]
        return arg_map

    def _replace_arg(self, line, arg, reg):
        start = line.find('dword')
        if start == -1:
            start = line.find('qword')
        if start == -1:
            start = line.find('oword')
        if start == -1:
            start = line.find('yword')
        if start == -1:
            start = line.find('zword')
        if start == -1:
            raise ValueError("Optimization failed! ", line)

        end = line.index(']', start)
        line = line[0:start] + reg + line[end + 1:]

        if 'vmovsd' in line:
            line = line.replace('vmovsd', 'vmovaps')
        elif 'movsd' in line:
            line = line.replace('movsd', 'movaps')
        elif 'vmovss' in line:
            line = line.replace('vmovss', 'vmovaps')
        elif 'movss' in line:
            line = line.replace('movss', 'movaps')
        return line

    def _mem_allowed(self, inst, line, reg):
        if inst in self._mem_ok_inst:
            return True
        size = None
        start = line.find('dword')
        if start != -1:
            size = 32
        start = line.find('qword')
        if start != -1:
            size = 64
        if size is None:
            return True
        if self._regs.is_xmm(reg) or self._regs.is_ymm(reg) or self._regs.is_zmm(reg):
            return False
        return True

    def _filter_args(self, arg_map):
        new_arg_map = arg_map.copy()
        for line in self._code.splitlines():
            for arg, reg in arg_map.items():
                if arg.name in line:
                    tokens = re.split(' |,|\[|\]|;|\.', line)
                    if arg.name in tokens:
                        if '+' in line or '.' in line or tokens[0] not in self._ok_insts or not self._mem_allowed(tokens[0], line, reg):
                            if arg in new_arg_map:
                                del new_arg_map[arg]
        return new_arg_map

    def optimize(self):
        # TODO Improve optimization, call not supported in optimizations yet
        if 'call' in self._code:
            return self._code

        arg_map = self._build_args_map()
        arg_map = self._filter_args(arg_map)

        new_code = []
        for line in self._code.splitlines():
            for arg, reg in arg_map.items():
                if arg.name in line:
                    tokens = re.split(' |,|\[|\]|;|\.', line)
                    if arg.name in tokens:
                        line = self._replace_arg(line, arg, reg)
            new_code.append(line)
        return '\n'.join(new_code) + '\n'