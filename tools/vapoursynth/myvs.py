import vapoursynth as vs
import havsfunc as haf
import mvsfunc as mvf
import insaneAA
import descale
import CSMOD as CS
import adjust
import os
import nnedi3_resample as nnrs
import functools
import math

core: vs.Core = vs.core
core.max_cache_size = 24576
core.num_threads = 14


def make_clt(first, last, fps):
    content = [r'<?xml version="1.0"?>',
               r'<Cuts xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema">',
               f'  <Framerate>{fps}</Framerate>',
               r'  <Style>NO_TRANSITION</Style>',
               r'  <AllCuts>',
               r'    <CutSection>',
               f'      <startFrame>{first}</startFrame>',
               f'      <endFrame>{last}</endFrame>',
               r'    </CutSection>',
               r'  </AllCuts>',
               r'</Cuts>']
    return content


class VS:
    def __init__(self, src: [str, vs.VideoNode]):
        if isinstance(src, str):
            self.src_name = src
            self.src = self.load(src)
            self.compare_clips = []
            self.diff_clips = []
            self.diff_clip = None
            self.super_clip = None
            self.masks: list[vs.VideoNode] = []

        elif isinstance(src, VS):
            self.src_name = src.src_name
            self.src = src.src
            self.compare_clips = src.compare_clips.copy()
            self.diff_clips = src.diff_clips.copy()
            self.diff_clip = src.diff_clip
            self.super_clip = src.super_clip
            self.masks = src.masks.copy()

    def __add__(self, b):
        b: VS
        self.src = self.src + b()

    def __getitem__(self, item):
        if isinstance(item, slice):
            first, last, step = item.start, item.stop, item.step
            if step is not None:
                self.src = self.src[item]
            else:
                self.trim(first, last)
        elif isinstance(item, int):
            self.trim(0, item)

    def __call__(self):
        return self.src

    @classmethod
    def load(cls, name: str) -> vs.VideoNode:
        task_type = os.path.splitext(name)[1][1:]
        if task_type in ('mp4', 'm4v', 'mov', '3gp', '3g2', 'm2ts', 'mpeg', 'vob',
                         'm2v', 'mpg', 'ogm', 'ogv', 'ts', 'tp', 'ps'):
            return core.lsmas.LWLibavSource(name)            
        elif task_type == 'avi':
            return core.avisource.AVISource(name)
        else:
            return core.ffms2.Source(name)

    def aa(self, *args, **kwargs):
        self.src = haf.santiag(self.src, opencl=True, *args, **kwargs)

    def copy(self):
        c = VS(self.src[:])
        c.src_name = self.src_name
        return c

    def border(self, left: int = 0, right: int = 0, top: int = 0, bottom: int = 0):
        self.src = core.std.addBorders(self.src, left, right, top, bottom)

    def crop(self, left: int = 0, right: int = 0, top: int = 0, bottom: int = 0):
        self.src = core.std.CropRel(self.src, left, right, top, bottom)
    
    def depan(self, x: int = 2, y: int = 2, prev=2, next=2, *args, **kwargs):
        data = core.mv.DepanEstimate(self.src)
        self.src = core.mv.DepanStabilise(self.src, data=data, prev=prev, next=next, blur=30,
                                          dxmax=x, dymax=y, subpixel=2, *args, **kwargs)
    
    def tofull(self):
        depth = self.src.format.bits_per_sample
        self.src = core.std.Levels(core.std.Levels(self.src, min_in=1 << depth - 4, max_in=235 << depth - 8,
                                                   min_out=0, max_out=(1 << depth) - 1, planes=0),
                                   min_in=1 << depth - 4, max_in=240 << depth - 8,
                                   min_out=0, max_out=(1 << depth) - 1, planes=[1, 2])

    def tolimit(self):
        depth = self.src.format.bits_per_sample
        self.src = core.std.Levels(core.std.Levels(self.src, min_out=1 << depth - 4, max_out=235 << depth - 8,
                                                   min_in=0, max_in=(1 << depth) - 1, planes=0),
                                   min_out=1 << depth - 4, max_out=240 << depth - 8,
                                   min_in=0, max_in=(1 << depth) - 1, planes=[1, 2])

    def limiter(self):
        depth = self.src.format.bits_per_sample
        self.src = core.std.Limiter(self.src, min=16 << depth - 8, max=235 << depth - 8, planes=[0])
        self.src = core.std.Limiter(self.src, min=16 << depth - 8, max=240 << depth - 8, planes=[1, 2])

    def split_gray(self, threshold: float = 0.5) -> vs.VideoNode:
        depth = self.src.format.bits_per_sample
        if 0 < threshold < 1:
            threshold = ((1 << depth) - 1) * threshold
        else:
            raise ValueError('threshold必须是0~1之间的小数')
        return core.std.Binarize(self.src, threshold=threshold, v0=0, v1=(1 << depth) - 1, planes=0)

    @staticmethod
    def split_gray_rel(n: int, f: vs.VideoFrame, clip: vs.VideoNode, threshold: float):
        depth = clip.format.bits_per_sample
        max_luma = f.props['PlaneStatsMax']
        min_luma = f.props['PlaneStatsMin']
        threshold = (max_luma - min_luma) * threshold + min_luma
        return core.std.Binarize(clip, threshold=threshold, v0=0, v1=(1 << depth) - 1, planes=0)

    def lim(self, full: bool = False):
        def func(n: int, f: vs.VideoFrame, clip: vs.VideoNode):
            luma_max = (1 << depth) - 1
            cur_max = f.props['PlaneStatsMax']
            cur_min = f.props['PlaneStatsMin']
            diff = cur_max - cur_min + 0.1
            if diff > luma_max // 5:
                return clip.std.Lut(planes=0,
                                    function=functools.partial(adjust.lut,
                                                               cont=luma_max/diff,
                                                               bright=-luma_max*cur_min/diff,
                                                               luma_min=0,
                                                               luma_max=luma_max))
            else:
                return clip.std.Lut(planes=0,
                                    function=functools.partial(adjust.lut,
                                                               cont=5,
                                                               bright=-5*cur_min,
                                                               luma_min=0,
                                                               luma_max=luma_max))

        depth = self.src.format.bits_per_sample
        props_clip = core.std.PlaneStats(self.src)
        self.src = core.std.FrameEval(self.src,
                                      functools.partial(func, clip=self.src),
                                      prop_src=props_clip)
        if full is False:
            self.src = core.std.Levels(self.src, min_out=16 << depth - 8, max_out=235 << depth - 8,
                                       min_in=0, max_in=(1 << depth) - 1, planes=0)

    def tridenoise(self, mode: int = 0, bright: bool = True, bright_args: dict = None,
                   middle: bool = True, middle_args: dict = None,
                   dark: bool = True, dark_args: dict = None,
                   threshold: [float] = None, prevent_mask: list[bool] = None):
        if threshold is None:
            threshold = [0.2, 0.8]
        if bright_args is None:
            bright_args = {}
        elif 'channels' in bright_args:
            del bright_args['channels']
        if middle_args is None:
            middle_args = {}
        elif 'channels' in middle_args:
            del middle_args['channels']
        if dark_args is None:
            dark_args = {'a': 3, 'h': 1.5}
        elif 'channels' in dark_args:
            del dark_args['channels']
        if prevent_mask is None:
            prevent_mask = [True, True, True]
        elif len(prevent_mask) > 3:
            raise ValueError('length of prevent_mask must <= 3')
        if bright:
            bright_clip = core.knlm.KNLMeansCL(self.src, channels='Y', **bright_args)
            if prevent_mask[0]:
                bright_clip = core.std.MaskedMerge(clipa=bright_clip, clipb=self.src, mask=self.mask, planes=0)
        else:
            bright_clip = self.src
        if middle:
            middle_clip = core.knlm.KNLMeansCL(self.src, channels='Y', **middle_args)
            if prevent_mask[1]:
                middle_clip = core.std.MaskedMerge(clipa=middle_clip, clipb=self.src, mask=self.mask, planes=0)
        else:
            middle_clip = self.src
        if dark:
            dark_clip = core.knlm.KNLMeansCL(self.src, channels='Y', **dark_args)
            if prevent_mask[2]:
                dark_clip = core.std.MaskedMerge(clipa=dark_clip, clipb=self.src, mask=self.mask, planes=0)
        else:
            dark_clip = self.src

        if mode == 0:
            props_clip = core.std.PlaneStats(self.src)
            denoise = core.std.MaskedMerge(clipa=dark_clip, clipb=middle_clip,
                                           mask=core.std.FrameEval(
                                                   self.src,
                                                   functools.partial(
                                                       self.split_gray_rel,
                                                       clip=self.src,
                                                       threshold=threshold[0]),
                                                   prop_src=props_clip),
                                           planes=0)

            denoise = core.std.MaskedMerge(clipa=denoise, clipb=bright_clip,
                                           mask=core.std.FrameEval(
                                                   self.src,
                                                   functools.partial(
                                                       self.split_gray_rel,
                                                       clip=self.src,
                                                       threshold=threshold[1]),
                                                   prop_src=props_clip),
                                           planes=0)

        elif mode == 1:
            denoise = core.std.MaskedMerge(clipa=dark_clip, clipb=middle_clip, mask=self.split_gray(threshold[0]), planes=0)
            denoise = core.std.MaskedMerge(clipa=denoise, clipb=bright_clip, mask=self.split_gray(threshold[1]), planes=0)
        else:
            raise ValueError('mode must be 0 or 1')
        self.src = denoise
    
    def denoise(self, channels: str = 'YUV', prevent_mask: bool = True, *args, **kwargs):
        channels = channels.upper()
        if channels == 'YUV':
            denoise = core.knlm.KNLMeansCL(core.knlm.KNLMeansCL(self.src,
                                                                channels='Y',
                                                                *args, **kwargs),
                                           channels='UV',
                                           *args, **kwargs)
        elif channels in ('Y', 'UV'):
            denoise = core.knlm.KNLMeansCL(self.src, channels=channels, *args, **kwargs)
        else:
            raise ValueError('channels必须是YUV, Y, UV')
        
        if prevent_mask:                
            self.src = core.std.MaskedMerge(clipa=denoise, clipb=self.src, mask=self.mask, planes=[0, 1, 2])
        else:
            self.src = denoise

    def tdenoise(self):
        vectorf = core.mv.Analyse(self.super_clip, blksize=4, overlap=2, search=5, truemotion=True, delta=1)
        vectorf2 = core.mv.Analyse(self.super_clip, blksize=4, overlap=2, search=5, truemotion=True, delta=2)
        vectorf3 = core.mv.Analyse(self.super_clip, blksize=4, overlap=2, search=5, truemotion=True, delta=3)
        vectorb = core.mv.Analyse(self.super_clip, blksize=4, search=5, overlap=2, truemotion=True, isb=True, delta=1)
        vectorb2 = core.mv.Analyse(self.super_clip, blksize=4, search=5, overlap=2, truemotion=True, isb=True, delta=2)
        vectorb3 = core.mv.Analyse(self.super_clip, blksize=4, search=5, overlap=2, truemotion=True, isb=True, delta=3)
        self.src = core.mv.Degrain3(self.src, self.super_clip, mvbw=vectorb, mvbw2=vectorb2, mvbw3=vectorb3, mvfw=vectorf,
                                    mvfw2=vectorf2, mvfw3=vectorf3)

    def super(self):
        self.super_clip = core.mv.Super(self.src, pel=4)

    def csmod(self, *args, **kwargs):
        if args or kwargs:
            self.src = CS.CSMOD(self.src, *args, **kwargs)
        else:
            self.src = CS.CSMOD(self.src, preset='very slow', edgemode=1, edgemask=self.mask,
                                kernel=8, preblur=0, tcannysigma=1, Soft=0)

    def insane(self, strength: int = 0.3, kernel='bilinear', height=720, *args, **kwargs):
        self.src = insaneAA.insaneAA(self.src,
                                     eedi3_mode=insaneAA.EEDI3Mode.OPENCL,
                                     nnedi3_mode=insaneAA.NNEDI3Mode.NNEDI3CL,
                                     descale_strength=strength,
                                     kernel=kernel,
                                     descale_height=height,
                                     *args, **kwargs)

    def edgefix(self, left: int, right: int, top: int, bottom: int):
        self.src = core.edgefixer.ContinuityFixer(self.src, left, top, right, bottom)

    def get_mask(self, sigma: [float, list[int, int, int]] = None, *args, **kwargs):
        if sigma is None:
            sigma = [1.2, 1.5, 1.5]
        self.masks.append(core.tcanny.TCanny(self.src, sigma=sigma, *args, **kwargs))

    @property
    def mask(self):
        return self.masks[-1]

    def trim(self, first: int = None, last: int = None, length: int = None):
        if first is None:
            first = 0
        if length is None:
            if last is None:
                last = self.src.num_frames - 1
        else:
            last = first + length - 1
        self.src = core.std.Trim(self.src, first, last, length)
        fps = round(self.src.fps.numerator/self.src.fps.denominator, 15)
        content = make_clt(first, last, fps)
        name = os.path.split(self.src_name)[1]
        with open(f'{name} - ({first} - {last}).clt', 'w', encoding='utf-8') as f:
            for c in content:
                f.write(f'{c}\n')

    def resize(self, width: int, height: int):
        src_width = self.src.width
        src_height = self.src.height
        ratio = max(width // src_width, height // src_height)
        if ratio > 1:
            self.src = nnrs.nnedi3_resample(self.src, src_width * (ratio + 1), src_height * (ratio + 1))

        self.src = core.resize.Bicubic(self.src, width=width, height=height)

    def descale(self, width: int, height: int, kernel: str = 'bilinear', *args, **kwargs):
        self.src = descale.Descale(self.src, width, height, kernel=kernel, *args, **kwargs)
    
    def depth(self, depth: int):
        self.src = mvf.Depth(self.src, depth)

    def toyuv(self, css='22'):
        self.src = mvf.ToYUV(self.src, css=css)

    def torgb(self):
        self.src = mvf.ToRGB(self.src)

    def deband(self, preset: str, prevent_mask: bool = True, *args, **kwargs):
        if args or kwargs:
            deband = core.f3kdb.Deband(self.src, presst=f'{preset}/nograin', *args, **kwargs)
        else:
            deband = core.f3kdb.Deband(self.src, dither_algo=3, keep_tv_range=True,
                                       output_depth=16, preset=f'{preset}/nograin')
        if prevent_mask:                
            self.src = core.std.MaskedMerge(clipa=deband, clipb=self.src, mask=self.mask, planes=[0, 1, 2])
        else:
            self.src = deband

    def flowfps(self, num: int, den: int):
        vectors = core.mv.Analyse(self.super_clip, blksize=4, overlap=2, search=5, truemotion=True)
        vectors = core.mv.Recalculate(self.super_clip, vectors)
        vector = core.mv.Analyse(self.super_clip, blksize=4, search=5, overlap=2, truemotion=True, isb=True)
        vector = core.mv.Recalculate(self.super_clip, vectors=vector)
        self.src = core.mv.FlowFPS(self.src, self.super_clip, mvbw=vector, mvfw=vectors, num=num, den=den, blend=False)
    
    def waifu2x(self, model: int, noise: int = -1, scale: int = 2):
        self.src = core.caffe.Waifu2x(self.src, noise=noise, model=model, scale=scale)

    def dering(self, mrad: int = 1):
        self.src = haf.HQDeringmod(self.src, mrad=mrad, planes=[0, 1, 2])

    def m4(self, x: int, full: bool = False):
        depth = self.src.format.bits_per_sample
        if full:
            return x
        else:
            return 16 << depth - 8 if x < 16 << depth - 8 else math.floor(x / 4 + 0.5) * 4

    @staticmethod
    def scale(val: int, depth: int):
        return val * ((1 << depth) - 1) // 255

    def dering_process(self, r=2.0, darkstr=0.0, brightstr=1.0, lowsens=50, highsens=50, ss=1.5, predering=False,
                       nrmode=1, dering_mask=None):
        clip = self.src
        depth = clip.format.bits_per_sample
        width = clip.width
        height = clip.height
        x2 = self.m4(width / r)
        y2 = self.m4(height / r)
        xs = self.m4(width * ss)
        ys = self.m4(height * ss)

        ps1 = core.std.MaskedMerge(clip, haf.MinBlur(clip, nrmode),
                                   dering_mask) if predering and dering_mask is not None else clip

        halo = core.resize.Bicubic(ps1, x2, y2, range_in_s='full', range_s='full').resize.Bicubic(width, height,
                                                                                                  filter_param_a=1,
                                                                                                  filter_param_b=0,
                                                                                                  range_in_s='full',
                                                                                                  range_s='full')
        expr = 'z a - {multiple} / x y - {multiple} / - z a - {multiple} / 0.001 + / 255 * {LOS} - z a - {multiple} / 256 + 512 / {HIS} + * {multiple} *'.format(
            multiple=self.scale(1, depth), LOS=lowsens, HIS=highsens / 100)
        halotomask = core.std.Expr(
            [core.std.Maximum(halo), core.std.Minimum(halo), core.std.Maximum(ps1), core.std.Minimum(clip)], [expr])
        pshalo = core.std.MaskedMerge(halo, ps1, halotomask)

        pshalo2 = core.resize.Spline36(ps1, xs, ys, range_in_s='full', range_s='full')
        pshalo2 = core.std.Expr(
            [pshalo2, core.std.Maximum(pshalo).resize.Bicubic(xs, ys, range_in_s='full', range_s='full'),
             core.std.Minimum(pshalo).resize.Bicubic(xs, ys, range_in_s='full', range_s='full')], ['x y min z max'])
        pshalo2 = core.resize.Spline36(pshalo2, width, height, range_in_s='full', range_s='full')
        self.src = core.std.Expr([ps1, pshalo2],
                             ['x y < x x y - {DRK} * - x x y - {BRT} * - ?'.format(DRK=darkstr, BRT=brightstr)])

    def ivtc_simple(self):
        matched_clip = core.vivtc.VFM(self.src, mode=0, order=1, cthresh=0, mi=0)
        self.src = core.vivtc.VDecimate(matched_clip)

    @staticmethod
    def postprocess(n: int, f: vs.VideoFrame, clip: vs.VideoNode, deinterlaced: vs.VideoNode) -> vs.VideoNode:
        if f.props['_Combed']:
            return deinterlaced
        else:
            return clip

    def get_interlace(self, cthresh: int = 6, mi: int = 5):
        comb_props = core.tdm.IsCombed(self.src, cthresh=cthresh, metric=1, mi=mi)
        comb_props: vs.VideoNode
        combs_nums = set()
        for n, frame in enumerate(comb_props.frames()):
            if frame.props['_Combed']:
                combs_nums.add(n)
        if combs_nums:
            combs_nums = sorted(list(combs_nums))
            combs_frames = [core.text.Text(self.src[num], str(num)) for num in combs_nums]
            comb_src = core.std.Splice(clips=combs_frames)
            comb_src.set_output()
            with open(f'{self.src_name}.txt', 'w', encoding='utf-8') as f:
                f.write(str(combs_nums))
        else:
            return None
    
    def ivtc(self, mode: int = 3, vd: bool = True, cthresh: int = 6, mi: int = 20):
        matched_clip = core.vivtc.VFM(self.src, order=1, mode=mode, cthresh=-1, mi=mi)
        deinterlaced_clip = core.tdm.TDeintMod(matched_clip, order=1,
                                               edeint=core.nnedi3cl.NNEDI3CL(matched_clip, field=1))
        comb_props = core.tdm.IsCombed(matched_clip, cthresh=cthresh, metric=1, mi=mi)
        self.src = core.std.FrameEval(matched_clip,
                                      functools.partial(self.postprocess,
                                                        clip=matched_clip, deinterlaced=deinterlaced_clip),
                                      prop_src=comb_props)
        if vd:
            self.src = core.vivtc.VDecimate(self.src)

    def deint(self, d=1):
        if d == 2:
            self.src = haf.QTGMC(self.src, TFF=True, opencl=True, ShutterBlur=2, FPSDivisor=2)
        else:
            self.src = haf.QTGMC(self.src, TFF=True, opencl=True, FPSDivisor=d)

    def warp(self, thresh=128, blur=7, depth=7):
        self.src = core.warp.AWarpSharp2(self.src, thresh=thresh, blur=blur, type=1, depth=depth)

    def fps(self, fpsnum: int, fpsden: int):
        self.src = core.std.AssumeFPS(self.src, fpsnum=fpsnum, fpsden=fpsden)

    def deblock(self):
        self.src = haf.Deblock_QED(self.src)

    def tweak(self, hue=0.0, sat=1.0, bright=0.0, cont=1.0, coring=True):
        self.src = adjust.Tweak(self.src, hue=hue, sat=sat, bright=bright, cont=cont, coring=coring)

    def mark(self, clip: vs.VideoNode = None):
        if clip:
            self.compare_clips.append(clip)
        else:
            self.compare_clips.append(self.src)

    def compare(self):
        if self.compare_clips:
            self.compare_clips.append(self.src)
            self.src = core.std.Interleave(self.compare_clips)
        else:
            raise TypeError('You must run mark() first')

    def mark_diff(self, clip: vs.VideoNode = None):
        if len(self.diff_clips) < 2:
            if clip:
                self.diff_clips.append(clip)
            else:
                self.diff_clips.append(self.src)
            if len(self.diff_clips) == 2:
                self.diff_clip = core.std.MakeDiff(*self.diff_clips)
        else:
            raise TypeError('You can mark_diff() twice only')

    def diff(self, planes: int = None):
        if planes is None:
            planes = [0, 1, 2]
        if self.diff_clip:
            self.src = core.std.MergeDiff(self.src, self.diff_clip, planes)
        else:
            raise TypeError('You must run mark_diff() first')

    def output(self):
        self.src.set_output()

