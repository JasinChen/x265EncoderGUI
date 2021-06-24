from vapoursynth import core, VideoNode, GRAY, YUV
import descale
from enum import Enum
from typing import Any, Type, Union, Tuple

__version__ = 0.9

"""
InsaneAA Anti-Aliasing Script (VS port) v0.9c (16.02.2020)
Original idea by tonik & tophf, edited and ported by DJATOM.
Use this script to fix ugly upscaled anime BDs.
Processing chain: 
    1) extract luma from clip;
    2) apply Descale to it;
    3) resize luma with Spline36 for smooth edges;
    4) merge "smooth" clip with Descale clip according to descale_strength;
    5) re-upscale it back to 1080p (or clip's original resolution) using eedi3+nnedi3 method;
    6) merge rescaled clip with source clip using lines mask. This should prevent noise and textures distortion;
    7) combine merged clip with color planes. 
Prerequisites:
    eedi3/eedi3cl: https://github.com/HomeOfVapourSynthEvolution/VapourSynth-EEDI3
    znedi3: https://github.com/sekrit-twc/znedi3/releases
    nnedi3: https://github.com/dubhater/vapoursynth-nnedi3
    nnedi3cl: https://github.com/HomeOfVapourSynthEvolution/VapourSynth-NNEDI3CL
    descale: https://github.com/Irrational-Encoding-Wizardry/vapoursynth-descale
Basic usage:
    import insaneAA
    insaneAA.insaneAA(clip, external_aa=None, external_mask=None, faster_aa=False, eedi3_mode=insaneAA.EEDI3Mode.CPU, eedi3_device=-1, eedi3_opt=0, nnedi3_mode=insaneAA.NNEDI3Mode.NNEDI3, nnedi3_device=-1, nnedi3_opt=0, descale_strength=0.3, kernel='bilinear', bicubic_b=1/3, bicubic_c=1/3, lanczos_taps=3, descale_width=None, descale_height=720, pscrn=1, alpha=0.2, beta=0.25, gamma=1000.0, nrad=2, mdis=20, nsize=0, nns=4, output_mode=insaneAA.ClipMode.FULL, input_mode=insaneAA.ClipMode.FULL)
        external_aa: if clip is passed, will use it intead of making rescale, otherwise do all processing.
        external_mask: pass external lines mask. Must be clip or ignored.
        faster_aa: slightly different upscaling routine, proposed by ZASTIN. Notably faster at higher native resolutions, but might produce worse results.
        eedi3_mode: enum/int with mode or tuple with two enums/ints representing modes for the first and second calls of eedi3.
        eedi3_device: integer or tuple with two integers representing device IDs for the first and second calls of eedi3.
        eedi3_opt: Controls eedi3 opt related options. You can pass single value or tuple with two values for separated opt on the instances. Passed value should be int type.
        nnedi3_mode: enum/int with mode or tuple with two enums/ints representing modes for the first and second calls of nnedi3.
        nnedi3_device: integer or tuple with two integers representing device IDs for the first and second calls of nnedi3.
        nnedi3_opt: Controls nnedi3 opt related options. You can pass single value or tuple with two values for separated opt on the instances. znedi3 expects string, classic nnedi3 - int (0 - use opt, 1 - disable, use C functions), means nothing for NNEDI3CL. 
        descale_strength: strength of mixing between descaled clip and Spline36 clip (AA purposes). More strengh means more haloes with sharp kernel (mostly bilinear), keep that in mind.
        kernel: descaling kernel. Use getnative.py for determining native resolution and try various kernels to find the best suitable.
        bicubic_b/bicubic_c: bicubic options for Descale.
        lanczos_taps: lanczos options for Descale.
        descale_height/descale_width: once you know native resolution, set descale_height.
        pscrn: nnedi3's prescreener for faster operation.
        alpha: eedi3's alpha.
        beta: eedi3's beta.
        gamma: eedi3's gamma.
        nrad: eedi3's nrad.
        mdis: eedi3's mdis.
        nsize: nnedi3's nsize.
        nns: nnedi3's nns.
        output_mode: UNMASKED - just rescale (GRAY), MASKED - linemasked rescale (GRAY), FULL - linemasked rescale + source colors.
        input_mode: UNMASKED - expects output_mode=1 at external_aa clip. Anything else will skip applying lines mask.
    Please do something with FullHD details! At least mask them or somehow exclude from processing.
Changelog:
    version 0.9c
        Fix: pass lanczos_taps to actual Descale call.
    version 0.9b
        New: add lanczos_taps option.
    version 0.9a
        Fix: allow ints on eedi3/nnedi3/clip modes.
    version 0.9
        Change: huge changes in parameter values. Usage updated.
    version 0.8
        New: expose nsize/nns options from nnedi3. Sometimes different nsize preset can produce better results and nsize is simply for setting tradeoff between speed and quality (max quality by default).
    version 0.7
        New: tunable bicubic_b and bicubic_c options for bicubic descaling.
        Change: descale_str -> descale_strength.
    version 0.6b
        Fix: nnedi3 mode used slow C routines by default (behaviour differs from classic avisynth option).
    version 0.6
        New: parameters eedi3Opt/nnedi3Opt. Controls eedi3/nnedi3 opt related options.
        New: expose nrad/mdis parameters from eedi3. It's possible to improve speed with nearly the same results (say, use mdis=12 for 720p rescales).
        New: parameter 'externalMask'. Overrides built-in mask clip.
        Change: eedi3/nnedi3 mode related configuration. Now you can pass single 'cpu' or 'opencl' for eedi3Mode and single 'nnedi3', 'znedi3' or 'opencl' for nnedi3Mode. 
                If you need to use non-default device, set eedi3Device and nnedi3Device with proper values. 
                If you have 2 GPUs or wanna run 1st instance on GPU and second on CPU (or vice versa), just pass tuple with 2 values.
        Change: parameter 'ref' is now 'externalAA'.
        Change: parameter 'fasterAA' is now False by default.
    version 0.5
        New: inputMode. If set to 1, line masking on ref will be performed.
    version 0.4
        New: ref paramenter. You can supply processed clip there, it will be used instead of calculating new rescale.
        Speed-ups for AA processing by ZASTIN.
    version 0.3
        Major change in eedi3/nnedi3 options: use dict(first=dict(mode='cpu', device=-1), second=dict(mode='cpu', device=-1)) for eedi3Mode/nnedi3Mode. More in usage.
        Now you can pick znedi3 for sclip. The fastest nnedi3 option on my observation, but in complex scripts it might be better to use opencl nnedi3 for saving cpu cycles for other stuff.
    version 0.2
        Turn off OpenCL plugins by default.
        Split eedi3Cl for every eedi3 call, may improve performance on cheap GPUs.
    version 0.1
        Initial release.
"""

""" various modes stuff """
class ClipMode(Enum):
    FULL     = 0
    UNMASKED = 1
    MASKED   = 2

class EEDI3Mode(Enum):
    CPU      = 0
    OPENCL   = 1

class NNEDI3Mode(Enum):
    NNEDI3   = 0
    ZNEDI3   = 1
    NNEDI3CL = 2

def insaneAA(clip: VideoNode, external_aa: VideoNode = None, external_mask: VideoNode = None, faster_aa: bool = False, \
    eedi3_mode: Union[EEDI3Mode, Tuple[EEDI3Mode, EEDI3Mode]] = EEDI3Mode.CPU, eedi3_device: Union[int, Tuple[int, int]] = -1, eedi3_opt: Union[int, Tuple[int, int]] = 0, \
    nnedi3_mode: Union[NNEDI3Mode, Tuple[NNEDI3Mode, NNEDI3Mode]] = NNEDI3Mode.NNEDI3, nnedi3_device: Union[int, Tuple[int, int]] = -1, nnedi3_opt: Union[int, str, Tuple[Union[int, str], Union[int, str]]] = 0, \
    descale_strength: float = 0.3, kernel: str = 'bilinear', bicubic_b: float = 1/3, bicubic_c: float = 1/3, lanczos_taps: int = 3, descale_width: int = None, descale_height: int = 720, pscrn: int = 1, \
    alpha: float = 0.2, beta: float = 0.25, gamma: float = 1000.0, nrad: int = 2, mdis: float = 20, nsize: int = 0, nns: int = 4, \
    output_mode: ClipMode = ClipMode.FULL, input_mode: ClipMode = ClipMode.FULL) -> VideoNode:
    if not isinstance(clip, VideoNode):
        raise TypeError('insaneAA: this is not a clip.')
    width = clip.width
    height = clip.height
    gray_clip = core.std.ShufflePlanes(clip, 0, GRAY)
    if not isinstance(external_aa, VideoNode):
        descale_clip = revert_upscale(gray_clip, descale_strength, kernel, descale_width, descale_height, bicubic_b, bicubic_c, lanczos_taps)
        upscale = rescale(descale_clip, faster_aa, eedi3_mode, eedi3_device, eedi3_opt, nnedi3_mode, nnedi3_device, nnedi3_opt, width, height, pscrn, alpha, beta, gamma, nrad, mdis, nsize, nns)
    else:
        upscale = external_aa
    if output_mode in [ClipMode.UNMASKED, 1, "unmasked"]:
        return upscale
    if not isinstance(external_aa, VideoNode) or input_mode in [ClipMode.UNMASKED, 1, "unmasked"]:
        if not isinstance(external_mask, VideoNode):
            linemask = core.std.Sobel(gray_clip).std.Expr("x 2 *").std.Maximum()
        else:
            linemask = external_mask
        aa_clip = core.std.MaskedMerge(gray_clip, upscale, linemask)
    else:
        aa_clip = external_aa
    if output_mode in [ClipMode.MASKED, 2, "masked"] or clip.format.num_planes == 1:
        return aa_clip
    else:
        return core.std.ShufflePlanes([aa_clip, clip], planes=[0, 1, 2], colorfamily=YUV)

def revert_upscale(clip: VideoNode, descale_strength: float = 0.3, kernel: str = 'bilinear', descale_width: int = None, descale_height: int = 720, bicubic_b: float = 1/3, bicubic_c: float = 1/3, lanczos_taps: int = 3) -> VideoNode:
    width = clip.width
    height = clip.height
    descale_width = m4((width * descale_height) / height) if descale_width == None else descale_width
    descale_natural = descale.Descale(clip, descale_width, descale_height, kernel=kernel, b=bicubic_b, c=bicubic_c, taps=lanczos_taps)
    descale_smooth = core.resize.Spline36(clip, descale_width, descale_height)
    return core.std.Expr([descale_natural, descale_smooth], 'x {strength} * y 1 {strength} - * +'.format(strength=descale_strength))

def rescale(clip: VideoNode, faster_aa: bool = False, eedi3_mode: Union[EEDI3Mode, Tuple[EEDI3Mode, EEDI3Mode]] = EEDI3Mode.CPU, eedi3_device: Union[int, Tuple[int, int]] = -1, eedi3_opt: Union[int, Tuple[int, int]] = 0, nnedi3_mode: Union[NNEDI3Mode, Tuple[NNEDI3Mode, NNEDI3Mode]] = NNEDI3Mode.NNEDI3, nnedi3_device: Union[int, Tuple[int, int]] = -1, nnedi3_opt: Union[int, str, Tuple[Union[int, str], Union[int, str]]] = 0, dx: int = None, dy: int = None, pscrn: int = 1, alpha: float = 0.2, beta: float = 0.25, gamma: float = 1000.0, nrad: int = 2, mdis: float = 20, nsize: int = 0, nns: int = 4):
    ux = clip.width * 2
    uy = clip.height * 2
    if dx is None:
        raise ValueError('insaneAA: rescale lacks "dx" parameter.')
    if dy is None:
        raise ValueError('insaneAA: rescale lacks "dy" parameter.')
    eedi3_mode_a,       eedi3_mode_b = validateInput(eedi3_mode,   (EEDI3Mode, int), 'insaneAA: eedi3_mode should be enum with valid mode or tuple with 2 values providing valid modes.')
    nnedi3_mode_a,     nnedi3_mode_b = validateInput(nnedi3_mode, (NNEDI3Mode, int), 'insaneAA: nnedi3_mode should be enum with valid mode or tuple with 2 values providing valid modes.')
    eedi3_device_a,   eedi3_device_b = validateInput(eedi3_device,              int, 'insaneAA: eedi3_device should be integer with valid device ID or tuple with 2 values providing valid device IDs.')
    nnedi3_device_a, nnedi3_device_b = validateInput(nnedi3_device,             int, 'insaneAA: nnedi3_device should be integer with valid device ID or tuple with 2 values providing valid device IDs.')
    eedi3_opt_a,         eedi3_opt_b = validateInput(eedi3_opt,                 int, 'insaneAA: eedi3_opt should be integer with valid eedi3/eedi3cl opt value or tuple with 2 values providing valid values.')
    nnedi3_opt_a,       nnedi3_opt_b = validateInput(nnedi3_opt,         (int, str), 'insaneAA: nnedi3_opt should be integer or string with valid eedi3/eedi3cl opt value or tuple with 2 values providing valid values.')
    if faster_aa:
        clip = core.std.Transpose(clip)
        clip = eedi3_instance(clip, eedi3_mode_a, eedi3_device_a, eedi3_opt_a, nnedi3_mode_a, nnedi3_device_a, nnedi3_opt_a, pscrn, alpha, beta, gamma, nrad, mdis, nsize, nns)
        clip = core.resize.Spline36(clip, height=dx, src_top=-0.5, src_height=ux)
        clip = core.std.Transpose(clip)
        clip = eedi3_instance(clip, eedi3_mode_b, eedi3_device_b, eedi3_opt_b, nnedi3_mode_b, nnedi3_device_b, nnedi3_opt_b, pscrn, alpha, beta, gamma, nrad, mdis, nsize, nns)
        return core.resize.Spline36(clip, height=dy, src_top=-0.5, src_height=uy)
    else:
        clip = eedi3_instance(clip, eedi3_mode_a, eedi3_device_a, eedi3_opt_a, nnedi3_mode_a, nnedi3_device_a, nnedi3_opt_a, pscrn, alpha, beta, gamma, nrad, mdis, nsize, nns)
        clip = core.std.Transpose(clip)
        clip = eedi3_instance(clip, eedi3_mode_b, eedi3_device_b, eedi3_opt_b, nnedi3_mode_b, nnedi3_device_b, nnedi3_opt_b, pscrn, alpha, beta, gamma, nrad, mdis, nsize, nns)
        clip = core.std.Transpose(clip)
        return core.resize.Spline36(clip, dx, dy, src_left=-0.5, src_top=-0.5, src_width=ux, src_height=uy)

def eedi3_instance(clip: VideoNode, eedi3_mode: EEDI3Mode = EEDI3Mode.CPU, eedi3_device: int = -1, eedi3_opt: int = 0, nnedi3_mode: NNEDI3Mode = NNEDI3Mode.NNEDI3, nnedi3_device: int = -1, nnedi3_opt: Union[int, str] = 0, pscrn: int = 1, alpha: float = 0.2, beta: float = 0.25, gamma: float = 1000.0, nrad: int = 2, mdis: float = 20, nsize: int = 0, nns: int = 4) -> VideoNode:
    if eedi3_mode in [EEDI3Mode.OPENCL, 1, "opencl"]:
        return core.eedi3m.EEDI3CL(clip, field=1, dh=True, alpha=alpha, beta=beta, gamma=gamma, vcheck=3, nrad=nrad, mdis=mdis, sclip=nnedi3_superclip(clip, nnedi3_mode, nnedi3_device, nnedi3_opt, pscrn, nsize, nns), device=eedi3_device, opt=eedi3_opt)
    elif eedi3_mode in [EEDI3Mode.CPU, 0, "cpu"]:
        return core.eedi3m.EEDI3(clip, field=1, dh=True, alpha=alpha, beta=beta, gamma=gamma, vcheck=3, nrad=nrad, mdis=mdis, sclip=nnedi3_superclip(clip, nnedi3_mode, nnedi3_device, nnedi3_opt, pscrn, nsize, nns), opt=eedi3_opt)
    else:
        raise ValueError(f'insaneAA: invalid eedi3 mode - {eedi3_mode}.')

def nnedi3_superclip(clip: VideoNode, nnedi3_mode: NNEDI3Mode = NNEDI3Mode.NNEDI3, nnedi3_device: int = -1, opt: Union[int, str] = 0, pscrn: int = 1, nsize: int = 0, nns: int = 4) -> VideoNode:
    if nnedi3_mode in [NNEDI3Mode.NNEDI3CL, 2, "nnedi3cl"]:
        return core.nnedi3cl.NNEDI3CL(clip, field=1, dh=True, nsize=nsize, nns=nns, pscrn=pscrn, device=nnedi3_device)
    elif nnedi3_mode in [NNEDI3Mode.ZNEDI3, 1, "znedi3"]:
        if opt == 0:
            _opt = True
            _x_cpu = ""
        elif opt == 1:
            _opt = False
            _x_cpu = ""
        else:
            _opt = True
            _x_cpu = str(opt)
        return core.znedi3.nnedi3(clip, field=1, dh=True, nsize=nsize, nns=nns, pscrn=pscrn, opt=_opt, x_cpu=_x_cpu)
    elif nnedi3_mode in [NNEDI3Mode.NNEDI3, 0, "nnedi3"]:
        # swap 0 and 1 for nnedi3 to behave like a classic avisynth: 0 - use best available functions and 1 - use C functions
        return core.nnedi3.nnedi3(clip, field=1, dh=True, nsize=nsize, nns=nns, pscrn=pscrn, opt={0: 1, 1: 0}.get(int(opt), 1))
    else:
        raise ValueError(f'insaneAA: invalid nnedi3 mode - {nnedi3_mode}.')

def validateInput(var: Union[EEDI3Mode, NNEDI3Mode, int, str, tuple], varType: Union[Type[EEDI3Mode], Type[NNEDI3Mode], Type[int], Type[str], Type[tuple], tuple], errorString: str) -> Any:
    if isinstance(var, varType):
        return var, var
    elif isinstance(var, tuple):
        if len(var) == 2 and isinstance(var[0], varType) and isinstance(var[1], varType):
            return var
        else:
            raise ValueError(errorString)
    else:
        raise ValueError(errorString)

def m4(x: int) -> int:
    return 16 if x < 16 else int(x // 4 + 0.5) * 4
