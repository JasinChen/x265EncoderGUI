import vapoursynth as vs
core = vs.core
try:
   core.std.LoadPlugin(r"/*ffms2_path*/")
except Exception:
   pass
clip = core.ffms2.Source(r"/*video_path*/")
clip.set_output()
