import vapoursynth as vs
import havsfunc as haf
import mvsfunc as mvf
import insaneAA
import CSMOD as CS
import functools
import adjust
import os

core = vs.core
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
               f'      <endFrame>{last+1}</endFrame>',
               r'    </CutSection>',
               r'  </AllCuts>',
               r'</Cuts>']
    return content


class VS:
    def __init__(self, src:str):
        if isinstance(src, str):
            self.src_name = src
            self.src = self.load(src)
        elif isinstance(src, vs.VideoNode):
            self.src_name = 'unknown'
            self.src = src

    def __add__(self, b):
        self.src = self.src + b()
        return self

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
    def load(cls, name):
        return core.ffms2.Source(name)

    def aa(self, **args):
        if args:
            self.src = haf.santiag(self.src, args)
        else:
            self.src = haf.santiag(self.src, opencl=True)

    def tofull(self):
        depth = self.src.format.bits_per_sample
        self.src = core.std.Levels(core.std.Levels(self.src, min_in=2**(depth - 4), max_in=2**(depth - 8) * 235,
                                                   min_out=0, max_out=2**depth, planes=0),
                                   min_in=2**(depth - 4), max_in=2**(depth - 8) * 240,
                                   min_out=0, max_out=2**depth, planes=[1, 2])

    def denoise(self, **args):
        if args:
            self.src = core.knlm.KNLMeansCL(core.knlm.KNLMeansCL(self.src, channels='Y', **args), channels='UV', **args)
        else:
            self.src = core.knlm.KNLMeansCL(core.knlm.KNLMeansCL(self.src, channels='Y'), channels='UV')

    def csmod(self, **args):
        if args:
            self.src = CS.CSMOD(self.src, args)
        else:
            self.src = CS.CSMOD(self.src, preset='very slow', edgemode=1, edgemask=5, kernel=8,
                                preblur=0, tcannysigma=1, Soft=0)

    def insane(self):
        self.src = insaneAA.insaneAA(self.src, eedi3Mode=dict(first=dict(mode='opencl', device=0)),
                                     nnedi3Mode=dict(first=dict(mode='opencl', device=0)))

    def edgefix(self, left, right, top, bottom):
        self.src = core.edgefixer.ContinuityFixer(self.src, left, top, right, bottom)

    def trim(self, first=None, last=None, length=None):
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

    def resize(self, width, height):
        self.src = core.resize.Spline36(self.src, width=width, height=height)

    def depth(self, depth):
        self.src = mvf.Depth(self.src, depth)

    def yuv(self, css='22'):
        self.src = mvf.ToYUV(self.src, css=css)

    def rgb(self):
        self.src = mvf.ToRGB(self.src)

    def deband(self, preset, **args):
        if args:
            self.src = core.f3kdb.Deband(self.src, presst=f'{preset}/nograin', **args)
        else:
            self.src = core.f3kdb.Deband(self.src, dither_algo=3, keep_tv_range=True,
                                         output_depth=16, preset=f'{preset}/nograin')

    def mvtools(self, num, den):
        super = core.mv.Super(self.src,pel=2)
        vectors = core.mv.Analyse(super,overlap=4,search=3,truemotion=True)
        vectors = core.mv.Recalculate(super, vectors)
        vector = core.mv.Analyse(super,search=3,overlap=4,truemotion=True,isb=True)
        vector = core.mv.Recalculate(super, vectors=vector)
        self.src = core.mv.FlowFPS(self.src, super, mvbw = vector, mvfw = vectors,num=num, den=den, blend=False)
    
    def waifu(self, model, noise=-1, scale=2):
        self.src = core.caffe.Waifu2x(self.src, noise=noise, model=model, scale=scale)

    def dering(self):
        self.src = haf.HQDeringmod(self.src, planes=[0, 1, 2])

    def ivtc(self, vd=True):
        matched_clip = core.vivtc.VFM(self.src, order=1, mode=3, cthresh=6)
        deinterlaced_clip = core.tdm.TDeintMod(matched_clip, order=1,
                                               edeint=core.nnedi3cl.NNEDI3CL(matched_clip, field=1))
        postprocessed_clip = mvf.FilterCombed(matched_clip, deinterlaced_clip)
        if vd:
            self.src = core.vivtc.VDecimate(postprocessed_clip)
        else:
            self.src = postprocessed_clip
        self.src = core.std.SetFieldBased(self.src, 0)

    def deint(self, d=1):
        if d == 2:
            self.src = haf.QTGMC(self.src, TFF=True, opencl=True, ShutterBlur=2, FPSDivisor=2)
        else:
            self.src = haf.QTGMC(self.src, TFF=True, opencl=True, FPSDivisor=d)

    def warp(self, blur=7, depth=7):
        self.src = core.warp.AWarpSharp2(self.src, thresh=128, blur=blur, type=1, depth=depth)

    def fps(self, fpsnum, fpsden):
        self.src = core.std.AssumeFPS(self.src, fpsnum=fpsnum, fpsden=fpsden)

    def deblock(self):
        self.src = core.deblock.Deblock(self.src)

    def tweak(self, hue=0.0, sat=1.0, bright=0.0, cont=1.0):
        self.src = adjust.Tweak(self.src, hue=hue, sat=sat, bright=bright, cont=cont)

    def output(self):
        self.src.set_output()
