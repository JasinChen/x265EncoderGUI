import vapoursynth as vs
core = vs.core
core.max_cache_size = 2048
core.num_threads = 8

clip = core.ffms2.Source(r"/*video_path*/")
clip.set_output()
