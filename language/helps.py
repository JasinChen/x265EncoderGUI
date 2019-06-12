helps={'log-level': {
'English': '''--log-level <integer|string>
Controls the level of information displayed on the console.
Debug level enables per-frame QP, metric, and bitrate logging.
Full level enables hash and weight logging.

-1 disables all logging, except certain fatal errors,
and can be specified by the string “none”.
0.error
1.warning
2.info (default)
3.debug
4.full''',

'Chinese': '''--log-level <integer|string>
控制控制台上显示的信息级别。
调试级别启用每帧QP，度量标准和比特率日志记录。
完整级别启用散列和重量记录。

-1禁用所有日志记录，但某些致命错误除外，并且可以由字符串“none”指定。
0.错误
1.警告
2.信息（默认）
3.调试
4.完整'''},

'progress': {
'English': '''--no-progress
Disable periodic progress reports from the CLI''',

'Chinese': '''--no-progress
从CLI禁用定期的进度报告'''},

'csv': {
'English': '''--csv <filename>
Write encoding statistics to a Comma Separated Values log file.
Creates the file if it doesn’t already exist.
If --csv-log-level is 0, it adds one line per run.
If --csv-log-level is greater than 0, it writes one line per frame.
Default none''',

'Chinese':
'''--csv <filename>
将编码统计信息写入逗号分隔值的日志文件。如果文件尚不存在，则创建该文件。
如果--csv-log-level为0，则每次运行添加一行。
如果--csv-log-level大于0，则每帧写入一行。
默认为无。''',

'csv-log-level': 
{'English':'''--csv-log-level <integer>
Controls the level of detail (and size) of –csv log files

summary (default)
frame level logging
frame level logging with performance statistics''',
'Chinese':'''控制–csv log files的详细程度（和大小）

0.摘要（默认）
1.帧级日志记录
2.含性能统计的帧级日志'''},

'ssim':
{'English': '''--ssim, --no-ssim
Calculate and report Structural Similarity values.
It is recommended to use --tune ssim if you are measuring ssim,
else the results should not be used for comparison purposes.
Default disabled''',
'Chinese': '''--ssim, --no-ssim
计算并报告结构相似度值。
如果您正在测量ssim，建议使用--tune ssim，否则结果不应用于比较。
默认禁用'''},

'psnr':
{'English': '''--psnr, --no-psnr
Calculate and report Peak Signal to Noise Ratio.
It is recommended to use --tune psnr if you are measuring PSNR,
else the results should not be used for comparison purposes.
Default disabled''',

'Chinese': '''--psnr, --no-psnr
计算并报告峰值信噪比。
如果您正在测量PSNR，建议使用--tune psnr，否则结果不应用于比较。
默认禁用'''},

'asm':
{'English': '''--asm <integer:false:string>, --no-asm
x265 will use all detected CPU SIMD architectures by default.
You can disable all assembly by using --no-asm or you can specify
a comman separated list of SIMD architectures to use,
matching these strings: MMX2, SSE, SSE2, SSE3, SSSE3, SSE4, SSE4.1, SSE4.2, AVX, XOP, FMA4, AVX2, FMA3

Some higher architectures imply lower ones being present, this is handled implicitly.

One may also directly supply the CPU capability bitmap as an integer.

Note that by specifying this option you are overriding x265’s CPU
detection and it is possible to do this wrong. You can cause encoder
crashes by specifying SIMD architectures which are not supported on your CPU.

Default: auto-detected SIMD architectures''',

'Chinese': '''--asm <integer:false:string>, --no-asm
默认情况下，x265将使用所有检测到的CPU SIMD架构。
您可以使用--no-asm禁用所有程序集，或者您可以指定要使用的逗号分隔的SIMD体系结构列表，
匹配这些字符串：MMX2，SSE，SSE2，SSE3，SSSE3，SSE4，SSE4.1，SSE4.2，AVX，XOP，FMA4 ，AVX2，FMA3

一些较高的体系结构意味着较低的体系结构存在，这是隐式处理的。

也可以直接提供CPU能力位图作为整数。

请注意，通过指定此选项，您将覆盖x265的CPU检测，并且可能会执行错误操作。
通过指定CPU不支持的SIMD体系结构会编码器崩溃。

默认值：自动检测SIMD架构'''},

'frame-threads':
{'English': '''--frame-threads, -F <integer>
Number of concurrently encoded frames.
Using a single frame thread gives a slight improvement in compression,
since the entire reference frames are always available for motion compensation,
but it has severe performance implications.
Default is an autodetected count based on the number of CPU cores and whether WPP is enabled or not.

Over-allocation of frame threads will not improve performance, it will generally just increase memory use.

Values: any value between 0 and 16. Default is 0, auto-detect''',

'Chinese': '''--frame-threads, -F <integer>
并发编码帧的数量。使用单帧线程可以略微改善压缩，因为整个参考帧始终可用于运动补偿，但它严重影响性能。
默认值是基于CPU核心数以及是否启用WPP的自动检测计数。

帧线程的过度分配不会提高性能，通常只会增加内存使用量。

值： 0到16之间的任何值。默认值为0，自动检测'''},

'pools':
{'English': '''--pools <string>, --numa-pools <string>
Comma seperated list of threads per NUMA node. If "none",
then no worker pools are created and only frame parallelism is possible.
If NULL or ""(default) x265 will use all available threads on each NUMA node:

'+'  is a special value indicating all cores detected on the node
'*'  is a special value indicating all cores detected on the node and all remaining nodes
'-'  is a special value indicating no cores on the node, same as '0'
example strings for a 4-node system:

""        - default, unspecified, all numa nodes are used for thread pools
"*"       - same as default
"none"    - no thread pools are created, only frame parallelism possible
"-"       - same as "none"
"10"      - allocate one pool, using up to 10 cores on all available nodes
"-,+"     - allocate one pool, using all cores on node 1
"+,-,+"   - allocate one pool, using only cores on nodes 0 and 2
"+,-,+,-" - allocate one pool, using only cores on nodes 0 and 2
"-,*"     - allocate one pool, using all cores on nodes 1, 2 and 3
"8,8,8,8" - allocate four pools with up to 8 threads in each pool
"8,+,+,+" - allocate two pools, the first with 8 threads on node 0, 
            and the second with all cores on node 1,2,3
A thread pool dedicated to a given NUMA node is enabled only when the number of threads
to be created on that NUMA node is explicitly mentioned in that corresponding position
with the –pools option. Else, all threads are spawned from a single pool. The total number
of threads will be determined by the number of threads assigned to the enabled NUMA nodes
for that pool. The worker threads are be given affinity to all the enabled NUMA nodes for
that pool and may migrate between them, unless explicitly specified as described above.

In the case that any threadpool has more than 64 threads, the threadpool may be broken down
into multiple pools of 64 threads each; on 32-bit machines, this number is 32. All pools are
given affinity to the NUMA nodes on which the original pool had affinity. For performance reasons,
the last thread pool is spawned only if it has more than 32 threads for 64-bit machines, 
or 16 for 32-bit machines. If the total number of threads in the system doesn’t obey this constraint, 
we may spawn fewer threads than cores which has been emperically shown to be better for performance.

If the four pool features: --wpp, --pmode, --pme and --lookahead-slices are all disabled,
then --pools is ignored and no thread pools are created.

If "none" is specified, then all four of the thread pool features are implicitly disabled.

Frame encoders are distributed between the available thread pools, and the encoder will never
generate more thread pools than --frame-threads. The pools are used for WPP and for distributed
analysis and motion search.

On Windows, the native APIs offer sufficient functionality to discover the NUMA topology and 
enforce the thread affinity that libx265 needs (so long as you have not chosen to target XP or 
Vista), but on POSIX systems it relies on libnuma for this functionality. If your target POSIX 
system is single socket, then building without libnuma is a perfectly reasonable option, as it 
will have no effect on the runtime behavior. On a multiple-socket system, a POSIX build of 
libx265 without libnuma will be less work efficient. See thread pools for more detail.

Default "", one pool is created across all available NUMA nodes, with one thread allocated 
per detected hardware thread (logical CPU cores). In the case that the total number of threads 
is more than the maximum size that ATOMIC operations can handle (32 for 32-bit compiles, 
and 64 for 64-bit compiles), multiple thread pools may be spawned subject to the performance 
constraint described above.

Note that the string value will need to be escaped or quoted to protect against shell expansion 
on many platforms''',

'Chinese':'''--pools <string>, --numa-pools <string>
逗号分隔的每个NUMA(非统一内存访问架构)节点的线程列表。
如果为"none"，则不会创建任何工作池，只能实现帧并行性。
如果为NULL或""（默认）x265将使用每个NUMA节点上的所有可用线程：

'+'  是一个特殊值，指在节点上检测到的所有核心
'*'  是一个特殊值，指在节点和所有剩余节点上检测到的所有核心
'-'  是一个特殊值，指节点上没有核心, 和'0'相同

4节点系统的示例：

""        - 默认, 未指定的, 所有numa节点都用于线程池
"*"       - 和默认值相同
"none"    - 没有创建线程池，只进行帧并行
"-"       - 和"none"相同
"10"      - 在所有可用节点上使用最多10个核心分配一个进程池
"-,+"     - 仅在节点1上使用核心分配一个进程池
"+,-,+"   - 仅在节点0和2上使用核心分配一个进程池
"+,-,+,-" - 仅在节点0和2上使用核心分配一个进程池
"-,*"     - 使用节点1、2和3上的所有核心分配一个池
"8,8,8,8" - 分配四个池，每个池最多8个线程
"8,+,+,+" - 分配两个池，第一个池在节点0上有8个线程，
            第二个池在节点1、2、3上使用所有核心

仅当在具有-pools选项的相应位置中明确提到要在该NUMA节点上创建的线程数时，
才启用专用于给定NUMA节点的线程池。否则，所有线程都是从单个池中生成的。
线程总数将由分配给该池的已启用NUMA节点的线程数确定。除非如上所述明确指定，
否则工作线程被赋予对该池的所有启用的NUMA节点的亲和性，并且可以在它们之间迁移。

在任何线程池具有超过64个线程的情况下，线程池可以分解为多个64个线程的池; 
在32位计算机上，此数字为32.所有池都与原始池具有亲缘关系的NUMA节点具有亲缘关系。
出于性能原因，只有当64位计算机的线程数超过32个，或者32位计算机的线程数超过16时，
才会生成最后一个线程池。如果系统中的线程总数不遵守此约束条件，那么我们可能会产生
的线程少于核心，这些核心已经被证明对性能更好。

如果这四个线程池功能：--wpp，--pmode，--pme和--lookahead-slices都禁用，--pools将被忽略，不创建线程池。

如果指定“none”，则隐式禁用所有四个线程池功能。

帧编码器分布在可用的线程池之间，编码器永远不会生成比--frame-threads更多的线程池。
这些池用于WPP以及分布式分析和运动搜索。

在Windows上，本机API提供了足够的功能来发现NUMA拓扑并强制执行libx265所需的线程关联
（只要您没有选择以XP或Vista为目标），但在POSIX系统上，它依赖于libnuma来实现此功能。
如果您的目标POSIX系统是单个套接字，那么在没有libnuma的情况下构建是一个非常合理的选择，
因为它对运行时行为没有影响。在多插槽系统上，没有libnuma的libx265的POSIX构建将降低工作效率。
有关详细信息，请参阅线程池

默认""，在所有可用的NUMA节点上创建一个池，每个检测到的硬件线程（逻辑CPU核心）分配一个线程。
如果线程总数超过ATOMIC操作可以处理的最大值（32位编译为32位，64位编译为64位），则可能会产
生多个线程池，但受上述性能限制的影响。

请注意，需要对字符串值进行转义或引用，以防止在许多平台上进行shell扩展'''},

'wpp':
{'English':'''--wpp, --no-wpp
Enable Wavefront Parallel Processing. The encoder may begin encoding a row as 
soon as the row above it is at least two CTUs ahead in the encode process. 
This gives a 3-5x gain in parallelism for about 1% overhead in compression efficiency.

This feature is implicitly disabled when no thread pool is present.

Default: Enabled''',

'Chinese': '''--wpp, --no-wpp
启用Wavefront并行处理。一旦在其上方的行是编码处理中的至少两个CTU，
编码器就可以开始对一行进行编码。这使得并行性增加3-5倍，压缩效率约为1％。

没有线程池时，将隐式禁用此功能。

默认值：已启用'''},

'pmode':
{'English': '''--pmode, --no-pmode
Parallel mode decision, or distributed mode analysis. When enabled the 
encoder will distribute the analysis work of each CU (merge, inter, intra) 
across multiple worker threads. Only recommended if x265 is not already 
saturating the CPU cores. In RD levels 3 and 4 it will be most effective 
if –rect is enabled. At RD levels 5 and 6 there is generally always enough 
work to distribute to warrant the overhead, assuming your CPUs are not 
already saturated.

–pmode will increase utilization without reducing compression efficiency.
In fact, since the modes are all measured in parallel it makes certain 
early-outs impractical and thus you usually get slightly better compression
when it is enabled (at the expense of not skipping improbable modes). 
This bypassing of early-outs can cause pmode to slow down encodes, 
especially at faster presets.

This feature is implicitly disabled when no thread pool is present.

Default disabled''',

'Chinese': '''--pmode, --no-pmode
并行模式决策或分布式模式分析。启用后，编码器将在多个工作线程中分配每个
CU（合并，帧间，帧内）的分析工作。仅在x265尚未使CPU内核饱和时才建议使用。
在RD级别3和4中，如果启用了-rect，则最有效。在RD级别5和6，通常总是有足够
的工作来分配以保证开销，假设您的CPU尚未饱和。

-pmode将在不降低压缩效率的情况下提高利用率。实际上，由于这些模式都是并行
测量的，因此某些早期实现不切实际，因此在启用时通常会获得稍微好一些的压缩
（以不跳过不可能的模式为代价）。绕过早期输出可能会导致pmode减慢编码速度，
尤其是在更快的预设时。

没有线程池时，将隐式禁用此功能。

默认禁用'''},

'pme':
{'English': '''--pme, --no-pme
Parallel motion estimation. When enabled the encoder will distribute
motion estimation across multiple worker threads when more than two 
references require motion searches for a given CU. Only recommended 
if x265 is not already saturating CPU cores. --pmode is much more 
effective than this option, since the amount of work it distributes 
is substantially higher. With –pme it is not unusual for the overhead 
of distributing the work to outweigh the parallelism benefits.

This feature is implicitly disabled when no thread pool is present.

–pme will increase utilization on many core systems with no effect 
on the output bitstream.

Default disabled''',

'Chinese': '''--pme, --no-pme
并行运动估计。启用后，当两个以上的引用需要对给定CU进行运动搜索时，
编码器将在多个工作线程上分配运动估计。仅在x265尚未使CPU内核饱和时才推荐使用。
--pmode比这个选项更有效，因为它分配的工作量要高得多。使用-pme，
分配工作的开销超过并行性优势并不罕见。

没有线程池时，将隐式禁用此功能。

-pme将提高许多核心系统的利用率，而不会影响输出比特流。

默认禁用'''},

'preset':
{'English': '''--preset, -p <integer|string>
Sets parameters to preselected values, trading off compression 
efficiency against encoding speed. These parameters are applied 
before all other input parameters are applied, and so you can
override any parameters that these values control.

0.ultrafast
1.superfast
2.veryfast
3.faster
4.fast
5.medium (default)
6.slow
7.slower
8.veryslow
9.placebo''',

'Chinese': '''--preset, -p <integer|string>
将参数设置为预选值，将压缩效率与编码速度进行折衷。
这些参数在应用所有其他输入参数之前应用，
因此您可以覆盖这些值控制的任何参数。

0.ultrafast
1.superfast
2.veryfast
3.faster
4.fast
5.medium (default)
6.slow
7.slower
8.veryslow
9.placebo'''},

'tune':
{'English': '''--tune, -t <string>
Tune the settings for a particular type of source or situation. 
The changes will be applied after --preset but before all other 
parameters. Default none.

Values: psnr, ssim, grain, zero-latency, fast-decode.''',

'Chinese': '''--tune, -t <string>
调整特定类型的源或情境的设置。更改将在--preset之后但在所有其他参数之前应用。默认无

值： psnr，ssim，噪点，零延迟，快速解码。'''},

'slices':
{'English': '''--slices <integer>
Encode each incoming frame as multiple parallel slices that 
may be decoded independently. Support available only for 
rectangular slices that cover the entire width of the image.

Recommended for improving encoder performance only if 
frame-parallelism and WPP are unable to maximize utilization 
on given hardware.

Default: 1 slice per frame. Experimental feature''',

'Chinese': '''--slices <integer>
将每个输入帧编码为可以独立解码的多个并行切片。
支持仅适用于覆盖图像整个宽度的矩形切片。

建议仅当帧并行和WPP无法在给定硬件上最大化利用率时，
才用于提高编码器性能。

默认值：每帧1个切片。实验功能'''},

'copy-pic':
{'English': '''--copy-pic, --no-copy-pic
Allow encoder to copy input x265 pictures to internal 
frame buffers. When disabled, x265 will not make an 
internal copy of the input picture and will work with 
the application’s buffers. While this allows for deeper 
integration, it is the responsbility of the application 
to (a) ensure that the allocated picture has extra space 
for padding that will be done by the library, and (b) the 
buffers aren’t recycled until the library has completed 
encoding this frame (which can be figured out by tracking 
NALs output by x265)

Default: enabled''',

'Chinese': '''--copy-pic, --no-copy-pic
允许编码器将输入x265图像复制到内部帧缓冲区。
禁用时，x265不会生成输入图片的内部副本，并且可以使用应用程序的缓冲区。
虽然这允许更深入的集成，但应用程序的责任是：（a）确保分配的图片具有额外的填充空间，
这将由库完成；（b）缓冲区在库具有之前不会被回收完成对此帧的编码（可以通过跟踪由x265输出的NAL来计算）

默认值：启用'''},

'input':
{'English': '''--input <filename>
Input filename, only raw YUV or Y4M supported. 
Use single dash for stdin. This option name will 
be implied for the first “extra” command line argument.''',

'Chinese': '''--input <filename>
输入文件名，仅支持原始YUV或Y4M。对stdin使用单个破折号。
第一个“额外”命令行参数将隐含此选项名称。'''},

'y4m':
{'English': '''--y4m
Parse input stream as YUV4MPEG2 regardless of file extension, 
primarily intended for use with stdin (ie: --input - --y4m). 
This option is implied if the input filename has a “.y4m” extension''',

'Chinese': '''--y4m
无论文件扩展名如何，都将输入流解析为YUV4MPEG2，
主要用于stdin（即：--input - --y4m）。
如果输入文件名的扩展名为“.y4m”，则表示此选项'''},

'input-depth':
{'English': '''--input-depth <integer>
YUV only: Bit-depth of input file or stream

Values: any value between 8 and 16. Default is internal depth.''',

'Chinese': '''--input-depth <integer>
仅YUV：输入文件或流的位深度

值：8到16之间的任何值。默认值为内部深度。'''},

'frames':
{'English': '''--frames <integer>
The number of frames intended to be encoded. It may be left unspecified, 
but when it is specified rate control can make use of this information. 
It is also used to determine if an encode is actually a stillpicture 
profile encode (single frame)''',

'Chinese': '''--frames <integer>
要编码的帧数。它可能未指定，但是当指定时，速率控制可以使用此信息。
它还用于确定编码是否实际上是静止图像配置文件编码（单帧）'''},

'dither':
{'English': '''--dither
Enable high quality downscaling to the encoder’s internal bitdepth. 
Dithering is based on the diffusion of errors from one row of pixels 
to the next row of pixels in a picture. Only applicable when the input 
bit depth is larger than 8bits. Default disabled''',

'Chinese': '''--dither
为编码器的内部bitdepth启用高质量缩减。
抖动基于从一行像素到图像中的下一行像素的误差的扩散。
仅在输入位深度大于8位时适用。默认禁用'''},

'input-res':
{'English': '''--input-res <wxh>
YUV only: Source picture size [w x h]''',

'Chinese': '''--input-res <wxh>
仅限YUV：源图片大小[wxh]'''},

'input-csp':
{'English': '''--input-csp <integer|string>
Chroma Subsampling (YUV only): Only 4:0:0(monochrome), 
4:2:0, 4:2:2, and 4:4:4 are supported at this time. 
The chroma subsampling format of your input must match your 
desired output chroma subsampling format (libx265 will not
perform any chroma subsampling conversion), and it must be 
supported by the HEVC profile you have specified.

0.i400 (4:0:0 monochrome) - Not supported by Main or Main10 profiles
1.i420 (4:2:0 default) - Supported by all HEVC profiles
2.i422 (4:2:2) - Not supported by Main, Main10 and Main12 profiles
3.i444 (4:4:4) - Supported by Main 4:4:4, Main 4:4:4 10, Main 4:4:4 12, Main 4:4:4 16 Intra profiles
4.nv12
5.nv16''',

'Chinese': '''--input-csp <integer|string>
色度子采样（仅限YUV）：此时仅支持4：0：0（单色），4：2：0，4：2：2和4：4：4。
输入的色度子采样格式必须与您所需的输出色度子采样格式匹配（libx265不会执行任何色度子采样转换），
并且必须由您指定的HEVC配置文件支持。

0.i400（4：0：0单色） - Main或Main10配置文件不支持
1.i420（默认值为4：2：0） - 所有HEVC配置文件均支持
2.i422（4：2：2） - Main，Main10和Main12配置文件不支持
3.i444（4：4：4） - 被Main 4:4:4, Main 4:4:4 10, Main 4:4:4 12, Main 4:4:4 16 Intra支持
4.NV12
5.nv16'''},

'fps':
{'English': '''--fps <integer|float|numerator/denominator>
YUV only: Source frame rate

Range of values: positive int or float, or num/denom''',

'Chinese': '''--fps <integer|float|numerator/denominator>
仅YUV：源帧速率

值范围：正整数或浮点数，或num / denom'''},

'interlace':
{'English': '''--interlace <false|tff|bff>, --no-interlace
0.progressive pictures (default)
1.top field first
2.bottom field first
HEVC encodes interlaced content as fields. Fields must be provided to the encoder in the correct temporal order. The source dimensions must be field dimensions and the FPS must be in units of fields per second. The decoder must re-combine the fields in their correct orientation for display.''',

'Chinese': '''--interlace <false|tff|bff>, --no-interlace
0.逐行扫描（默认）
1.TFF
2.BFF
HEVC将隔行内容编码为字段。必须以正确的时间顺序将字段提供给编码器。源维度必须是字段维度，FPS必须以每秒字段为单位。解码器必须以正确的方向重新组合字段以进行显示。'''},

'seek':
{'English': '''--seek <integer>
Number of frames to skip at start of input file. Default 0''',

'Chinese': '''--seek <integer>
输入文件开头要跳过的帧数。默认值为0'''},

'output':
{'English': '''--output, -o <filename>
Bitstream output file name. If there are two extra CLI options, the first is implicitly the input filename and the second is the output filename, making the --output option optional.

The output file will always contain a raw HEVC bitstream, the CLI does not support any container file formats.''',

'Chinese': '''--output, -o <filename>
比特流输出文件名。如果有两个额外的CLI选项，第一个是隐式输入文件名，第二个是输出文件名，使--output选项可选。

输出文件将始终包含原始HEVC比特流，CLI不支持任何容器文件格式。'''},

'output-depth':
{'English': '''--output-depth, -D 8|10|12
Bitdepth of output HEVC bitstream, which is also the internal bit depth of the encoder. If the requested bit depth is not the bit depth of the linked libx265, it will attempt to bind libx265_main for an 8bit encoder, libx265_main10 for a 10bit encoder, or libx265_main12 for a 12bit encoder, with the same API version as the linked libx265.

If the output depth is not specified but --profile is specified, the output depth will be derived from the profile name.''',

'Chinese': '''--output-depth, -D 8|10|12
输出HEVC比特流的位深，也是编码器的内部比特深度。如果请求的位深度不是链接的libx265的位深度，它将尝试绑定libx265_main用于8位编码器，libx265_main10用于10位编码器，或libx265_main12用于12位编码器，其API版本与链接的libx265相同。

如果未指定输出深度但--profile指定了输出深度，则将从配置文件名称派生输出深度。'''},

'chunk-start':
{'English': '''--chunk-start <integer>
First frame of the chunk. Frames preceeding this in display order will be encoded, however, they will be discarded in the bitstream. This feature can be enabled only in closed GOP structures. Default 0 (disabled).''',

'Chinese': '''--chunk-start <integer>
块的第一帧。将按照显示顺序在此之前的帧进行编码，但是，它们将在比特流中被丢弃。只能在封闭的GOP结构中启用此功能。默认值为0（禁用）。'''},

'chunk-end':
{'English': '''--chunk-end <integer>
Last frame of the chunk. Frames following this in display order will be used in taking lookahead decisions, but, they will not be encoded. This feature can be enabled only in closed GOP structures. Default 0 (disabled).''',

'Chinese': '''--chunk-end <integer>
块的最后一帧。显示顺序后面的帧将用于做出先行决定，但是，它们不会被编码。只能在封闭的GOP结构中启用此功能。默认值为0（禁用）。'''},

'profile':
{'English': '''--profile, -P <string>
Enforce the requirements of the specified profile, ensuring the output stream will be decodable by a decoder which supports that profile. May abort the encode if the specified profile is impossible to be supported by the compile options chosen for the encoder (a high bit depth encoder will be unable to output bitstreams compliant with Main or MainStillPicture).

The following profiles are supported in x265.

8bit profiles:
* main, main-intra, mainstillpicture (or msp for short)
* main444-8, main444-intra, main444-stillpicture
See note below on signaling intra and stillpicture profiles.

10bit profiles:
* main10, main10-intra
* main422-10, main422-10-intra
* main444-10, main444-10-intra

12bit profiles:
* main12, main12-intra
* main422-12, main422-12-intra
* main444-12, main444-12-intra''',

'Chinese': '''--profile, -P <string>
强制执行指定配置文件的要求，确保输出流可由支持该配置文件的解码器解码。如果为编码器选择的编译选项不能支持指定的配置文件，则可以中止编码（高位深度编码器将无法输出符合Main或MainStillPicture的比特流）。

x265支持以下配置文件。

8位配置文件：
* main, main-intra, mainstillpicture (or msp for short)
* main444-8, main444-intra, main444-stillpicture
请参阅有关发送内部和静止图像配置文件的注释。

10位配置文件：
* main10, main10-intra
* main422-10, main422-10-intra
* main444-10, main444-10-intra

12位配置文件：
* main12, main12-intra
* main422-12, main422-12-intra
* main444-12, main444-12-intra'''},

'level-idc':
{'English': '''--level-idc <integer|float>
Minimum decoder requirement level. Defaults to 0, which implies auto-detection by the encoder. If specified, the encoder will attempt to bring the encode specifications within that specified level. If the encoder is unable to reach the level it issues a warning and aborts the encode. If the requested requirement level is higher than the actual level, the actual requirement level is signaled.

Beware, specifying a decoder level will force the encoder to enable VBV for constant rate factor encodes, which may introduce non-determinism.

The value is specified as a float or as an integer with the level times 10, for example level 5.1 is specified as “5.1” or “51”, and level 5.0 is specified as “5.0” or “50”.

Annex A levels: 1, 2, 2.1, 3, 3.1, 4, 4.1, 5, 5.1, 5.2, 6, 6.1, 6.2, 8.5''',

'Chinese': '''--level-idc <integer|float>
最低解码器要求级别。默认为0，表示编码器自动检测。如果指定，编码器将尝试将编码规范置于该指定级别内。如果编码器无法达到该级别，则会发出警告并中止编码。如果请求的需求级别高于实际级别，则发信号通知实际需求级别。

请注意，指定解码器级别将迫使编码器启用VBV以进行恒定速率因子编码，这可能会造成非确定性。

该值指定为浮点数或10倍整数，例如级别5.1指定为“5.1”或“51”，级别5.0指定为“5.0”或“50”。

附件A级别：1,2,2.1,3,3.1,4,4.1,5,5.1,5.2,6,6.1,6.2,8.5'''},

'high-tier':
{'English': '''--high-tier, --no-high-tier
If --level-idc has been specified, –high-tier allows the support of high tier at that level. The encoder will first attempt to encode at the specified level, main tier first, turning on high tier only if necessary and available at that level.If your requested level does not support a High tier, high tier will not be supported. If –no-high-tier has been specified, then the encoder will attempt to encode only at the main tier.

Default: enabled''',

'Chinese': '''--high-tier, --no-high-tier
如果--level-idc已指定，则-high-tier允许在该级别支持high级别。编码器将首先尝试在指定级别进行编码，首先是main级别，仅在必要时在该级别使用high级别。如果您请求的级别不支持high级别，则不支持high级别。如果指定了-no-high-tier，则编码器将尝试仅在main级别进行编码。

默认值：已启用'''},

'ref':
{'English': '''--ref <1..16>
Max number of L0 references to be allowed. This number has a linear multiplier effect on the amount of work performed in motion search, but will generally have a beneficial affect on compression and distortion.

Note that x265 allows up to 16 L0 references but the HEVC specification only allows a maximum of 8 total reference frames. So if you have B frames enabled only 7 L0 refs are valid and if you have --b-pyramid enabled (which is enabled by default in all presets), then only 6 L0 refs are the maximum allowed by the HEVC specification. If x265 detects that the total reference count is greater than 8, it will issue a warning that the resulting stream is non-compliant and it signals the stream as profile NONE and level NONE and will abort the encode unless --allow-non-conformance it specified. Compliant HEVC decoders may refuse to decode such streams.

Default 3''',

'Chinese': '''--ref <1..16>
允许的最大L0引用数。此数字对运动搜索中执行的工作量具有线性乘数效应，但通常会对压缩和失真产生有益影响。

请注意，x265最多允许16个L0参考，但HEVC规范仅允许最多8个参考帧。因此，如果启用了B帧，则只有7个L0引用有效且如果已--b-pyramid启用（默认情况下在所有预设中启用），则只有6个L0引用是HEVC规范允许的最大值。如果x265检测到总引用计数大于8，它将发出警告，指出结果流不符合要求，并且它将信号通知为配置文件NONE和level NONE，并且除非--allow-non-conformance指定，否则将中止编码 。兼容的HEVC解码器可以拒绝解码这样的流。

默认3'''},

'allow-non-conformance':
{'English': '''--allow-non-conformance, --no-allow-non-conformance
Allow libx265 to generate a bitstream with profile and level NONE. By default it will abort any encode which does not meet strict level compliance. The two most likely causes for non-conformance are --ctu being too small, --ref being too high, or the bitrate or resolution being out of specification.

Default: disabled''',

'Chinese': '''--allow-non-conformance, --no-allow-non-conformance
允许libx265生成具有配置文件和级别NONE的比特流。默认情况下，它将中止任何不符合严格级别合规性的编码。导致不合规的两个最可能的原因 --ctu太小，--ref太高，或者比特率或分辨率超出规范。

默认值：已禁用'''},

'uhd-bd':
{'English': '''--uhd-bd
Enable Ultra HD Blu-ray format support. If specified with incompatible encoding options, the encoder will attempt to modify/set the right encode specifications. If the encoder is unable to do so, this option will be turned OFF. Highly experimental.

Default: disabled''',

'Chinese': '''--uhd-bd
启用超高清蓝光格式支持。如果使用不兼容的编码选项，编码器将尝试修改/设置正确的编码规范。如果编码器无法执行此操作，则此选项将关闭。高度实验性。

默认值：已禁用'''},

'rd':
{'English': '''--rd <1..6>
Level of RDO in mode decision. The higher the value, the more exhaustive the analysis and the more rate distortion optimization is used. The lower the value the faster the encode, the higher the value the smaller the bitstream (in general). Default 3

Note that this table aims for accuracy, but is not necessarily our final target behavior for each mode.

Level	Description
0	sa8d mode and split decisions, intra w/ source pixels, currently not supported
1	recon generated (better intra), RDO merge/skip selection
2	RDO splits and merge/skip selection
3	RDO mode and split decisions, chroma residual used for sa8d
4	Currently same as 3
5	Adds RDO prediction decisions
6	Currently same as 5
Range of values: 1: least .. 6: full RDO analysis

Options which affect the coding unit quad-tree, sometimes referred to as the prediction quad-tree.''',

'Chinese': '''--rd <1..6>
模式决策中的RDO级别。值越高，分析越详尽，使用的失真优化越多。值越低，编码越快，值越高，比特流越小（通常）。默认3

请注意，此表旨在提高准确性，但不一定是每种模式的最终目标行为。

水平	描述
0	sa8d模式和拆分决策，内部w /源像素，目前不支持
1	重新生成（更好的intra），RDO合并/跳过选择
2	RDO拆分和合并/跳过选择
3	RDO模式和拆分决策，用于sa8d的色度残差
4	目前与3相同
5	添加RDO预测决策
6	目前与5相同
值范围： 1：最少.. 6：完整的RDO分析

影响编码单元四叉树的选项，有时称为预测四叉树。'''},

'ctu':
{'English': '''--ctu, -s <64|32|16>
Maximum CU size (width and height). The larger the maximum CU size, the more efficiently x265 can encode flat areas of the picture, giving large reductions in bitrate. However this comes at a loss of parallelism with fewer rows of CUs that can be encoded in parallel, and less frame parallelism as well. Because of this the faster presets use a CU size of 32. Default: 64''',

'Chinese': '''--ctu, -s <64|32|16>
最大CU尺寸（宽度和高度）。最大CU尺寸越大，x265可以更有效地编码图像的平坦区域，从而大大降低了比特率。然而，这导致并行性的损失，可以并行编码的CU行数较少，并且帧并行性也较少。因此，更快的预设使用CU大小32.默认值：64'''},

'min-cu-size':
{'English': '''--min-cu-size <32|16|8>
Minimum CU size (width and height). By using 16 or 32 the encoder will not analyze the cost of CUs below that minimum threshold, saving considerable amounts of compute with a predictable increase in bitrate. This setting has a large effect on performance on the faster presets.

Default: 8 (minimum 8x8 CU for HEVC, best compression efficiency)''',

'Chinese': '''--min-cu-size <32|16|8>
最小CU尺寸（宽度和高度）。通过使用16或32，编码器将不会分析低于该最小阈值的CU的成本，从而在可预测的比特率增加的情况下节省大量计算。此设置对更快预设的性能有很大影响。

默认值：8（HEVC最小8x8 CU，最佳压缩效率）'''},

'limit-refs':
{'English': '''--limit-refs <0|1|2|3>
When set to X265_REF_LIMIT_DEPTH (1) x265 will limit the references analyzed at the current depth based on the references used to code the 4 sub-blocks at the next depth. For example, a 16x16 CU will only use the references used to code its four 8x8 CUs.

When set to X265_REF_LIMIT_CU (2), the rectangular and asymmetrical partitions will only use references selected by the 2Nx2N motion search (including at the lowest depth which is otherwise unaffected by the depth limit).

When set to 3 (X265_REF_LIMIT_DEPTH && X265_REF_LIMIT_CU), the 2Nx2N motion search at each depth will only use references from the split CUs and the rect/amp motion searches at that depth will only use the reference(s) selected by 2Nx2N.

For all non-zero values of limit-refs, the current depth will evaluate intra mode (in inter slices), only if intra mode was chosen as the best mode for atleast one of the 4 sub-blocks.

You can often increase the number of references you are using (within your decoder level limits) if you enable one or both of these flags.

Default 3.''',

'Chinese': '''--limit-refs <0|1|2|3>
当设置为X265_REF_LIMIT_DEPTH（1）时，x265将根据用于编码下一个深度处的4个子块的参考来限制在当前深度处分析的参考。例如，16x16 CU仅使用用于编码其四个8x8 CU的引用。

当设置为X265_REF_LIMIT_CU（2）时，矩形和非对称分区将仅使用由2Nx2N运动搜索选择的参考（包括在最低深度，否则不受深度限制影响）。

当设置为3（X265_REF_LIMIT_DEPTH && X265_REF_LIMIT_CU），在各深度2Nx2N的运动搜索将只使用的引用从分割的CU和rect/amp运动搜索在该深度处将只使用由2Nx2N的选择的参考（或多个）。

对于limit-ref的所有非零值，当前深度将评估帧内模式（在片间），仅当帧内模式被选择为4个子块中的至少一个的最佳模式时。

如果启用这些标志中的一个或两个，通常可以增加正在使用的引用数（在解码器级别限制内）。

默认3。'''},

'limit-modes':
{'English': '''--limit-modes, --no-limit-modes
When enabled, limit-modes will limit modes analyzed for each CU using cost metrics from the 4 sub-CUs. When multiple inter modes like --rect and/or --amp are enabled, this feature will use motion cost heuristics from the 4 sub-CUs to bypass modes that are unlikely to be the best choice. This can significantly improve performance when rect and/or --amp are enabled at minimal compression efficiency loss.''',

'Chinese': '''--limit-modes, --no-limit-modes
启用后，将使用来自4个子CU的成本度量来限制针对每个CU分析的模式。当启用多个帧间模式--rect 和/或--amp启用时，此功能将使用来自4个子CU的运动成本启发法来绕过不太可能是最佳选择的模式。当rect 和/或--amp以最小的压缩效率损失启用时，这可以显着改善性能。'''},

'rect':
{'English': '''--rect, --no-rect
Enable analysis of rectangular motion partitions Nx2N and 2NxN (50/50 splits, two directions). Default disabled''',

'Chinese': '''--rect, --no-rect
启用矩形运动分区Nx2N和2NxN（50/50分割，两个方向）的分析。默认禁用'''},

'amp':
{'English': '''--amp, --no-amp
Enable analysis of asymmetric motion partitions (75/25 splits, four directions). At RD levels 0 through 4, AMP partitions are only considered at CU sizes 32x32 and below. At RD levels 5 and 6, it will only consider AMP partitions as merge candidates (no motion search) at 64x64, and as merge or inter candidates below 64x64.

The AMP partitions which are searched are derived from the current best inter partition. If Nx2N (vertical rectangular) is the best current prediction, then left and right asymmetrical splits will be evaluated. If 2NxN (horizontal rectangular) is the best current prediction, then top and bottom asymmetrical splits will be evaluated, If 2Nx2N is the best prediction, and the block is not a merge/skip, then all four AMP partitions are evaluated.

This setting has no effect if rectangular partitions are disabled. Default disabled''',

'Chinese': '''--amp, --no-amp
启用非对称运动分区的分析（75/25分割，四个方向）。在RD级别0到4，AMP分区仅在CU大小32x32及以下时考虑。在RD级别5和6，它将仅考虑AMP分区作为64x64处的合并候选（无运动搜索），以及作为64x64以下的合并或帧间候选。

搜索到的AMP分区是从当前最佳的分区间派生的。如果Nx2N（垂直矩形）是最佳当前预测，则将评估左和右不对称分裂。如果2NxN（水平矩形）是最佳当前预测，则将评估顶部和底部非对称分裂，如果2Nx2N是最佳预测，并且该块不是合并/跳过，则评估所有四个AMP分区。

如果禁用矩形分区，则此设置无效。默认禁用'''},

'early-skip':
{'English': '''--early-skip, --no-early-skip
Measure 2Nx2N merge candidates first; if no residual is found, additional modes at that depth are not analysed. Default disabled''',

'Chinese': '''--early-skip, --no-early-skip
首先测量2Nx2N merge候选；如果没有发现剩余，则不分析该深度处的附加模式。默认禁用'''},

'rskip':
{'English': '''--rskip, --no-rskip
This option determines early exit from CU depth recursion. When a skip CU is found, additional heuristics (depending on rd-level) are used to decide whether to terminate recursion. In rdlevels 5 and 6, comparison with inter2Nx2N is used, while at rdlevels 4 and neighbour costs are used to skip recursion. Provides minimal quality degradation at good performance gains when enabled.

Default: enabled, disabled for --tune grain''',

'Chinese': '''--rskip, --no-rskip
此选项确定提前退出CU深度递归。当找到跳过CU时，使用附加的启发式（取决于rd等级）来决定是否终止递归。在rd-levels 5和6中，使用与inter2Nx2N的比较，而在rdlevels 4和邻居成本用于跳过递归。启用时，在性能提升时提供最低质量降级。

默认值：启用，在--tune grain中禁用'''},

'splitrd-skip':
{'English': '''--splitrd-skip, --no-splitrd-skip
Enable skipping split RD analysis when sum of split CU rdCost larger than one split CU rdCost for Intra CU. Default disabled.''',

'Chinese': '''--splitrd-skip, --no-splitrd-skip
当分割CU rdCost的总和大于用于Intra CU的一个分割CU rdCost时，允许跳过分裂RD分析。默认禁用。'''},

'fast-intra':
{'English': '''--fast-intra, --no-fast-intra
Perform an initial scan of every fifth intra angular mode, then check modes +/- 2 distance from the best mode, then +/- 1 distance from the best mode, effectively performing a gradient descent. When enabled 10 modes in total are checked. When disabled all 33 angular modes are checked. Only applicable for --rd levels 4 and below (medium preset and faster).''',

'Chinese': '''--fast-intra, --no-fast-intra
对每五个帧内角度模式执行初始扫描，然后检查距离最佳模式+/- 2的模式，然后距离最佳模式+/- 1的模式，有效地执行梯度下降。启用后，将检查总共10种模式。禁用时，将检查所有33种角度模式。仅适用于--rd4级及以下（预设medium和faster）。'''},

'b-intra':
{'English': '''--b-intra, --no-b-intra
Enables the evaluation of intra modes in B slices. Default disabled.''',

'Chinese': '''--b-intra, --no-b-intra
允许评估B切片中的帧内模式。默认禁用。'''},

'--cu-lossless, --no-cu-lossless':
{'English': '''--cu-lossless, --no-cu-lossless
For each CU, evaluate lossless (transform and quant bypass) encode of the best non-lossless mode option as a potential rate distortion optimization. If the global option --lossless has been specified, all CUs will be encoded as lossless unconditionally regardless of whether this option was enabled. Default disabled.

Only effective at RD levels 3 and above, which perform RDO mode decisions.''',

'Chinese': '''--cu-lossless, --no-cu-lossless
对于每个CU，评估最佳非无损模式选项的无损（变换和量子旁路）编码作为潜在的速率失真优化。如果--lossless已指定全局选项，则无论是否启用此选项，所有CU都将无条件地编码为无损。默认禁用。

仅在RD级别3及以上有效。'''},

'tskip-fast':
{'English': '''--tskip-fast, --no-tskip-fast
Only evaluate transform skip for NxN intra predictions (4x4 blocks). Only applicable if transform skip is enabled. For chroma, only evaluate if luma used tskip. Inter block tskip analysis is unmodified. Default disabled''',

'Chinese': '''--tskip-fast, --no-tskip-fast
仅评估NxN帧内预测的transform skip（4x4块）。仅适用于启用变换跳过的情况。对于色度，仅当亮度使用tskip时评估。Inter block tskip分析未经修改。默认禁用'''},

'--rd-refine, --no-rd-refine':
{'English': '''--rd-refine, --no-rd-refine
For each analysed CU, calculate R-D cost on the best partition mode for a range of QP values, to find the optimal rounding effect. Default disabled.

Only effective at RD levels 5 and 6

Analysis re-use options, to improve performance when encoding the same sequence multiple times (presumably at varying bitrates). The encoder will not reuse analysis if slice type parameters do not match.''',

'Chinese': '''--rd-refine, --no-rd-refine
对于每个分析的CU，在一系列QP值的最佳分区模式下计算RD成本，以找到最佳舍入效果。默认禁用。

仅在RD级别5和6有效

分析re-use选项，以便在多次编码相同序列时提高性能（可能是在不同的比特率下）。如果切片类型参数不匹配，编码器将不重新使用分析。'''},

'analysis-save':
{'English': '''--analysis-save <filename>
Encoder outputs analysis information of each frame. Analysis data from save mode is written to the file specified. Requires cutree, pmode to be off. Default disabled.''',

'Chinese': '''--analysis-save <filename>
编码器输出每帧的分析信息。保存模式下的分析数据将写入指定的文件。需要关闭cutree，pmode。默认禁用。'''},

'analysis-load':
{'English': '''--analysis-load <filename>
Encoder reuses analysis information from the file specified. By reading the analysis data writen by an earlier encode of the same sequence, substantial redundant work may be avoided. Requires cutree, pmode to be off. Default disabled.

The amount of analysis data stored/reused is determined by --analysis-reuse-level.''',

'Chinese': '''--analysis-load <filename>
编码器重新使用指定文件中的分析信息。通过读取由相同序列的早期编码所写的分析数据，可以避免大量的冗余工作。需要关闭cutree，pmode。默认禁用。

存储/重用的分析数据量取决于--analysis-reuse-level。'''},

'analysis-reuse-file':
{'English': '''--analysis-reuse-file <filename>
Specify a filename for multi-pass-opt-analysis and multi-pass-opt-distortion. If no filename is specified, x265_analysis.dat is used.''',

'Chinese': '''--analysis-reuse-file <filename>
为multi-pass-opt-analysis和multi-pass-opt-distortion指定文件名。如果未指定文件名，则使用x265_analysis.dat。'''},

'analysis-reuse-level':
{'English': '''--analysis-reuse-level <1..10>
Amount of information stored/reused in --analysis-reuse-mode is distributed across levels. Higher the value, higher the information stored/reused, faster the encode. Default 5.

Note that –analysis-reuse-level must be paired with analysis-reuse-mode.

Level	Description
1	Lookahead information
2 to 4	Level 1 + intra/inter modes, ref's
5 and 6	Level 2 + rect-amp
7	Level 5 + AVC size CU refinement
8 and 9	Level 5 + AVC size Full CU analysis-info
10	Level 5 + Full CU analysis-info''',

'Chinese': '''--analysis-reuse-level <1..10>
存储/重用的信息量--analysis-reuse-mode分布在各个级别上。值越高，存储/重用的信息越高，编码越快。默认5。

请注意，–analysis-reuse-level必须与analysis-reuse-mode匹配。

等级	描述
1	前瞻(Lookahead)信息
2到4	1级+帧内/帧间模式，refs
5和6	2级+rect-amp
7	5级+AVC尺寸CU细化
8和9	5级+AVC大小完整CU分析 - 信息
10	5级+全CU分析 - 信息'''},

'refine-mv-type':
{'English': '''--refine-mv-type <string>
Reuse MV information received through API call. Currently receives information for AVC size and the accepted string input is "avc". Default is disabled.''',

'Chinese': '''--refine-mv-type <string>
重用通过API调用接收的MV信息。当前接收AVC大小的信息，并且接受的字符串输入是"avc"。默认为禁用。'''},

'refine-ctu-distortion':
{'English': '''--refine-ctu-distortion <0/1>
Store/normalize ctu distortion in analysis-save/load. 0 - Disabled. 1 - Save ctu distortion to the analysis file specified during analysis-save.

Load CTU distortion from the analysis file and normalize it across every frame during analysis-load.
Default 0.''',

'Chinese': '''--refine-ctu-distortion <0/1>
在analysis-save/load中存储/标准化ctu失真。
0 - 已禁用。

1 - 将ctu失真保存到analysis-save期间指定的分析文件中。
从分析文件加载CTU失真，并在分析加载期间将其标准化为每帧。
默认值为0。'''},

'scale-factor':
{'English': '''--scale-factor
Factor by which input video is scaled down for analysis save mode. This option should be coupled with analysis-reuse-mode option,
–analysis-reuse-level 10. The ctu size of load can either be the same as that of save or double the size of save. Default 0.''',

'Chinese': '''--scale-factor
输入视频按比例缩小以用于分析保存模式的因子。此选项应与analysis-reuse-mode，–analysis-reuse-level 10选项结合使用。
加载的ctu大小可以与保存大小相同，也可以是保存大小的两倍。默认值为0。'''},

'refine-intra':
{'English': '''--refine-intra <0..4>
Enables refinement of intra blocks in current encode.

Level 0 - Forces both mode and depth from the save encode.

Level 1 - Evaluates all intra modes at current depth(n) and at depth (n+1) when current block size is one greater than the min-cu-size. Forces modes for larger blocks.

Level 2 - In addition to the functionality of level 1, at all depths, force (a) only depth when angular mode is chosen by the save encode.
(b) depth and mode when other intra modes are chosen by the save encode.

Level 3 - Perform analysis of intra modes for depth reused from first encode.

Level 4 - Does not reuse any analysis information - redo analysis for the intra block.

Default 0.''',

'Chinese': '''--refine-intra <0..4>
允许在当前编码中细化帧内块。

0级 - 强制保存编码的模式和深度。

级别1 - 当前块大小比min-cu-size大1时，评估当前深度（n）和深度（n + 1）处的所有帧内模式。强制较大块的模式。

级别2 - 除了级别1的功能外，在所有深度处，强制（a）仅在保存编码选择角度模式时的深度。（b）保存编码选择其他帧内模式时的深度和模式。

级别3 - 对从第一次编码重用的深度的帧内模式进行分析。

级别4 - 不重用任何分析信息 - 内部块的重做分析。

默认值为0。'''},

'refine-inter':
{'English': '''--refine-inter <0..3>
Enables refinement of inter blocks in current encode.

Level 0 - Forces both mode and depth from the save encode.

Level 1 - Evaluates all inter modes at current depth(n) and at depth (n+1) when current block size is one greater than the min-cu-size. Forces modes for larger blocks.

Level 2 - In addition to the functionality of level 1, restricts the modes evaluated when specific modes are decided as the best mode by the save encode.

2nx2n in save encode - disable re-evaluation of rect and amp.

skip in save encode - re-evaluates only skip, merge and 2nx2n modes.

Level 3 - Perform analysis of inter modes while reusing depths from the save encode.

Default 0.''',

'Chinese': '''--refine-inter <0..3>
允许在当前编码中细化帧间块。

0级 - 强制保存编码的模式和深度。

1级 - 当前块大小比min-cu-size大1时，评估当前深度（n）和深度（n + 1）处的所有帧间模式。强制较大块的模式。

级别2 - 除了级别1的功能外，还限制在通过保存编码将特定模式确定为最佳模式时评估的模式。

保存编码中的2nx2n - 禁用对rect和amp的重新评估。

跳过保存编码 - 仅重新计算跳过，合并和2nx2n模式。

3级 - 在重用保存编码的深度时执行帧间模式分析。

默认值为0。'''},

'dynamic-refine':
{'English': '''--dynamic-refine, --no-dynamic-refine
Dynamically switches --refine-inter levels 0-3 based on the content and the encoder settings. It is recommended to use --refine-intra 4 with dynamic refinement.
Default disabled.''',

'Chinese': '''--dynamic-refine, --no-dynamic-refine
--refine-inter根据内容和编码器设置动态切换级别0-3。建议使用--refine-intra4进行动态细化。默认禁用。'''},

'refine-mv':
{'English': '''--refine-mv
Enables refinement of motion vector for scaled video. Evaluates the best motion vector by searching the surrounding eight integer and subpel pixel positions.

Options which affect the transform unit quad-tree, sometimes referred to as the residual quad-tree (RQT).''',

'Chinese': '''--refine-mv
为缩放视频启用运动矢量的细化。通过搜索周围的八个整数和子面像素位置来评估最佳运动矢量。

影响变换单元四叉树的选项，有时称为残差四叉树（RQT）。'''},

'rdoq-level':
{'English': '''--rdoq-level <0|1|2>, --no-rdoq-level
Specify the amount of rate-distortion analysis to use within quantization:

At level 0 rate-distortion cost is not considered in quant

At level 1 rate-distortion cost is used to find optimal rounding values for each level (and allows psy-rdoq to be effective).
It trades-off the signaling cost of the coefficient vs its post-inverse quant distortion from the pre-quant coefficient.
When --psy-rdoq is enabled, this formula is biased in favor of more energy in the residual (larger coefficient absolute levels)

At level 2 rate-distortion cost is used to make decimate decisions on each 4x4 coding group, including the cost of signaling the group within the group bitmap.
If the total distortion of not signaling the entire coding group is less than the rate cost, the block is decimated. Next
, it applies rate-distortion cost analysis to the last non-zero coefficient, which can result in many (or all) of the coding groups being decimated.
Psy-rdoq is less effective at preserving energy when RDOQ is at level 2, since it only has influence over the level distortion costs.''',

'Chinese': '''--rdoq-level <0|1|2>, --no-rdoq-level
指定在量化中使用的速率 - 失真分析量：

在0级时，量化不考虑速率失真成本

在1级时，速​​率 - 失真成本用于找到每个级别的最佳值（并允许psy-rdoq有效）。它从预定量系数中消除了系数的信令成本与其反后量化失真之间的关系。
当 --psy-rdoq启用时，该式偏向于更多的能量中的残余（较大系数的绝对水平）

在2级时，速率 - 失真成本用于对每个4x4编码组进行抽取决策，包括在组位图内发信号通知组的成本。如果不发信号通知整个编码组的总失真小于速率成本，
则该块被抽取。接下来，它将速率 - 失真成本分析应用于最后的非零系数，这可导致许多（或所有）编码组被抽取。当RDOQ处于2级时，Psy-rdoq在保存能量
方面效果较差，因为它只影响水平失真成本。'''},

'tu-intra-depth':
{'English': '''--tu-intra-depth <1..4>
The transform unit (residual) quad-tree begins with the same depth as the coding unit quad-tree,
but the encoder may decide to further split the transform unit tree if it improves compression efficiency.
This setting limits the number of extra recursion depth which can be attempted for intra coded units.
Default: 1, which means the residual quad-tree is always at the same depth as the coded unit quad-tree

Note that when the CU intra prediction is NxN (only possible with 8x8 CUs), a TU split is implied,
and thus the residual quad-tree begins at 4x4 and cannot split any futhrer.''',

'Chinese': '''--tu-intra-depth <1..4>
变换单元（残差）四叉树以与编码单元四叉树相同的深度开始，但是如果编码单元树提高了压缩效率，则编码器可以决定进一步分割变换单元树。
此设置限制了可以针对帧内编码单元尝试的额外递归深度的数量。默认值：1，表示残差四叉树始终与编码单位四叉树处于相同深度

注意，当CU帧内预测是NxN（仅可能具有8x8 CU）时，暗示TU分裂，因此残余四叉树从4x4开始并且不能分割任何后者。'''},

'tu-inter-depth':
{'English': '''--tu-inter-depth <1..4>
The transform unit (residual) quad-tree begins with the same depth as the coding unit quad-tree, but the encoder may decide to further split the transform unit tree if it improves compression efficiency.
This setting limits the number of extra recursion depth which can be attempted for inter coded units.
Default: 1. which means the residual quad-tree is always at the same depth as the coded unit quad-tree unless the CU was coded with rectangular or AMP partitions,
in which case a TU split is implied and thus the residual quad-tree begins one layer below the CU quad-tree.''',

'Chinese': '''--tu-inter-depth <1..4>
变换单元（残差）四叉树以与编码单元四叉树相同的深度开始，但是如果编码单元树提高了压缩效率，则编码器可以决定进一步分割变换单元树。此设置限制了可以针对帧间编码单元尝试的额外递归深度的数量。
默认值：1。这意味着残差四叉树总是与编码单元四叉树处于相同的深度，除非CU用矩形或AMP分区编码，在这种情况下暗示TU分裂，因此残差四叉树从CU四叉树下面开始一层。'''},

'limit-tu':
{'English': '''--limit-tu <0..4>
Enables early exit from TU depth recursion, for inter coded blocks.

Level 1 - decides to recurse to next higher depth based on cost comparison of full size TU and split TU.

Level 2 - based on first split subTU’s depth, limits recursion of other split subTUs.

Level 3 - based on the average depth of the co-located and the neighbor CUs’ TU depth, limits recursion of the current CU.

Level 4 - uses the depth of the neighbouring/ co-located CUs TU depth to limit the 1st subTU depth. The 1st subTU depth is taken as the limiting depth for the other subTUs.

Enabling levels 3 or 4 may cause a mismatch in the output bitstreams between option:–analysis-save and option:–analysis-load as all neighbouring CUs TU depth may not be available
in the option:–analysis-load run as only the best mode’s information is available to it.

Default: 0''',

'Chinese': '''--limit-tu <0..4>
对于帧间编码块，允许提前退出TU深度递归。

等级1 - 根据全尺寸TU和分割TU的成本比较决定递归到下一个更高的深度。

级别2 - 基于第一次分割子TU的深度，限制其他分割子组的递归。

级别3 - 基于共址的平均深度和相邻CU的TU深度，限制当前CU的递归。

级别4 - 使用邻近/共同定位的CU TU深度的深度来限制第一subTU深度。第一个subTU深度作为其他subTU的限制深度。

启用级别3或4可能会导致选项之间的输出比特流不匹配： - 分析 - 保存和选项： - 分析 - 加载， 因为所有相邻的CU TU深度可能在选项中不可用： - 分析 - 加载运行仅为最佳模式的信息可用。

默认值：0'''},

'nr-intra':
{'English': '''--nr-intra <integer>, --nr-inter <integer>
Noise reduction - an adaptive deadzone applied after DCT (subtracting from DCT coefficients), 
before quantization. 
It does no pixel-level filtering, doesn’t cross DCT block boundaries, has no overlap, 
The higher the strength value parameter, the more aggressively it will reduce noise.

Enabling noise reduction will make outputs diverge between different numbers of frame threads. 
Outputs will be deterministic but the outputs of -F2 will no longer match the outputs of -F3, etc.

Values: any value in range of 0 to 2000. Default 0 (disabled).''',

'Chinese': '''--nr-intra <integer>, --nr-inter <integer>
降噪 - 在量化之前在DCT（从DCT系数中减去）之后应用的自适应死区。
它没有像素级滤波，不跨越DCT块边界，没有重叠，强度值参数越高，它就会越积极地降低噪点。

启用降噪将使输出在不同数量的帧线程之间发生分歧。输出将是确定性的，但-F2的输出将不再与-F3等的输出匹配。

值：0到2000范围内的任何值。
默认值0（禁用）。'''},

'nr-inter':
{'English': '''Same as "nr-intra"''',

'Chinese': '''和"nr-intra"相同'''},

'tskip':
{'English': '''--tskip, --no-tskip
Enable evaluation of transform skip (bypass DCT but still use quantization) coding for 4x4 TU coded blocks.

Only effective at RD levels 3 and above, which perform RDO mode decisions.
Default disabled''',

'Chinese': '''--tskip, --no-tskip
启用对4x4 TU编码块的变换跳过（旁路DCT但仍使用量化）编码的评估。

仅在RD级别3及以上有效，执行RDO模式决策。默认禁用'''},

'rdpenalty':
{'English': '''--rdpenalty <0..2>
When set to 1, transform units of size 32x32 are given a 4x bit cost penalty compared to smaller transform units, in intra coded CUs in P or B slices.

When set to 2, transform units of size 32x32 are not even attempted, unless otherwise required by the maximum recursion depth.
For this option to be effective with 32x32 intra CUs, --tu-intra-depth must be at least 2. For it to be effective with 64x64 intra CUs, --tu-intra-depth must be at least 3.

Note that in HEVC an intra transform unit (a block of the residual quad-tree) is also a prediction unit,
meaning that the intra prediction signal is generated for each TU block, the residual subtracted and then coded.
The coding unit simply provides the prediction modes that will be used when predicting all of the transform units within the CU.
This means that when you prevent 32x32 intra transform units, you are preventing 32x32 intra predictions.

Default 0, disabled.

Values: 0:disabled 1:4x cost penalty 2:force splits''',

'Chinese': '''--rdpenalty <0..2>
当设置为1时，与较小的变换单元相比，在P或B切片中的帧内编码CU中，大小为32×32的变换单元被给予4x比特成本代价。

设置为2时，除非最大递归深度另有要求，否则甚至不会尝试大小为32x32的变换单元。要使此选项对32x32内部CU有效
--tu-intra-depth必须至少为2.要使其对64x64内部CU有效，--tu-intra-depth必须至少为3。

注意，在HEVC中，帧内变换单元（残余四叉树的块）也是预测单元，意味着针对每个TU块生成帧内预测信号，减去残差然后编码。
编码单元简单地提供将在预测CU内的所有变换单元时使用的预测模式。这意味着当您阻止32x32帧内变换单元时，您将阻止32x32帧内预测。

默认值为0，已禁用。

值： 0：禁用1：4x成本惩罚2：强制拆分'''},

'max-tu-size':
{'English': '''--max-tu-size <32|16|8|4>
Maximum TU size (width and height).
The residual can be more efficiently compressed by the DCT transform when
the max TU size is larger, but at the expense of more computation.
Transform unit quad-tree begins at the same depth of the coded tree unit,
but if the maximum TU size is smaller than the CU size then transform QT 
begins at the depth of the max-tu-size. Default: 32.''',

'Chinese': '''--max-tu-size <32|16|8|4>
最大TU尺寸（宽度和高度）。当最大TU尺寸较大时，可以通过DCT变换更有效地压缩残差，但是以更多计算为代价。
变换单元四叉树开始于编码树单元的相同深度，但是如果最大TU尺寸小于CU尺寸，则变换QT开始于最大调整大小的深度。
默认值：32。'''},

'dynamic-rd':
{'English': '''--dynamic-rd <0..4>
Increases the RD level at points where quality drops due to VBV rate control enforcement.
The number of CUs for which the RD is reconfigured is determined based on the strength.
Strength 1 gives the best FPS, strength 4 gives the best SSIM. Strength 0 switches this feature off.
Default: 0.

Effective for RD levels 4 and below.''',

'Chinese': '''--dynamic-rd <0..4>
由于VBV速率控制实施而导致质量下降的点处的RD级别增加。基于强度确定重新配置RD的CU的数量。
强度1给出最佳FPS，强度4给出最佳SSIM。强度0关闭此功能。默认值：0。

RD级别4及以下有效。'''},

'ssim-rd':
{'English': '''--ssim-rd, --no-ssim-rd
Enable/Disable SSIM RDO.
SSIM is a better perceptual quality assessment method as compared to MSE.
SSIM based RDO calculation is based on residual divisive normalization scheme.
This normalization is consistent with the luminance and contrast masking effect of Human Visual System.
It is used for mode selection during analysis of CTUs and can achieve significant gain in terms of 
objective quality metrics SSIM and PSNR.
It only has effect on presets which use RDO-based mode decisions (--rd 3 and above).''',

'Chinese': '''--ssim-rd, --no-ssim-rd
启用/禁用SSIM RDO。与MSE相比，SSIM是一种更好的感知质量评估方法。
基于SSIM的RDO计算基于残差分裂归一化方案。该归一化与人类视觉系统的亮度和对比度掩蔽效果一致。
它用于在CTU分析期间进行模式选择，并且可以在客观质量度量SSIM和PSNR方面实现显着增益。
它仅对使用基于RDO的模式决策（--rd3及以上）的预设有影响。'''},

'max-merge':
{'English': '''--max-merge <1..5>
Maximum number of neighbor (spatial and temporal) candidate blocks that the encoder may consider for merging motion predictions.
If a merge candidate results in no residual, it is immediately selected as a “skip”.
Otherwise the merge candidates are tested as part of motion estimation when searching for the least cost inter option.
The max candidate number is encoded in the SPS and determines the bit cost of signaling merge CUs.
Default 2''',

'Chinese': '''--max-merge <1..5>
编码器可以考虑用于合并运动预测的邻居（空间和时间）候选块的最大数量。
如果合并候选者没有导致残差，则立即将其选为“跳过”。
否则，在搜索最低成本的inter选项时，将合并候选者作为运动估计的一部分进行测试。
最大候选编号在SPS中编码，并确定信令合并CU的比特成本。默认2'''},

'me':
{'English': '''--me <integer|string>
Motion search method. 
Generally, the higher the number the harder the ME method will try to find an optimal match. 
Diamond search is the simplest. Hexagon search is a little better. 
Uneven Multi-Hexegon is an adaption of the search method used by x264 for slower presets. 
Star is a three step search adapted from the HM encoder: a star-pattern search followed 
by an optional radix scan followed by an optional star-search refinement. 
Full is an exhaustive search; an order of magnitude slower than all other searches but 
not much better than umh or star. SEA is similar to FULL search; a three step motion search 
adopted from x264: DC calculation followed by ADS calculation followed by SAD of the passed 
motion vector candidates, hence faster than Full search.

0.dia
1.hex (default)
2.umh
3.star
4.sea
5.full''',

'Chinese': '''--me <integer|string>
运动搜索方法。通常，数字越大，ME方法将尝试找到最佳匹配的难度越大。
Diamond搜索是最简单的。六角搜索更好一点。Uneven Multi-Hexegon是x264用于较慢预设的搜索方法的改编。
Star是从HM编码器改编的三步搜索：星型搜索，然后是可选的基数扫描，然后是可选的星形搜索细化。
Full是一个详尽的搜索; 比所有其他搜索速度慢一个数量级，但不比umh或star好多少。
SEA类似于全搜索; 从x264采用的三步运动搜索：DC计算，然后是ADS计算，然后是传递的运动矢量候选的SAD，
因此比完全搜索更快。

0.dia
1.hex (默认)
2.umh
3.star
4.sea
5.full'''},

'subme':
{'English': '''--subme, -m <0..7>
Amount of subpel refinement to perform. The higher the number
the more subpel iterations and steps are performed.
Default 2

-m  HPEL iters  HPEL dirs  QPEL iters  QPEL dirs  HPEL SATD
0	    1           4           0          4        false
1	    1           4           1          4        false
2	    1           4           1          4        true
3	    2           4           1          4        true
4	    2           4           2          4        true
5	    1           8           1          8        true
6	    2           8           1          8        true
7	    2           8           2          8        true
At –subme values larger than 2, chroma residual cost is included
in all subpel refinement steps and chroma residual is included 
in all motion estimation decisions (selecting the best reference 
picture in each list, and chosing between merge, uni-directional 
motion and bi-directional motion). The ‘slow’ preset is the first 
preset to enable the use of chroma residual.''',

'Chinese': '''--subme, -m <0..7>
要执行的子精炼的数量。数字越大，执行的子主题迭代和步骤越多。
默认2

-m  HPEL iters  HPEL dirs  QPEL iters  QPEL dirs  HPEL SATD
0	    1           4           0          4        false
1	    1           4           1          4        false
2	    1           4           1          4        true
3	    2           4           1          4        true
4	    2           4           2          4        true
5	    1           8           1          8        true
6	    2           8           1          8        true
7	    2           8           2          8        true
在-subme值大于2时，色度残差成本包括在所有子摘要细化步骤中，
并且色度残差包括在所有运动估计决策中（选择每个列表中的最佳参考图片，
并且在合并，单向运动和双向之间选择）定向运动）。“slow”预设是第一个
允许使用色度残差的预设。'''},

'merange':
{'English': '''--merange <integer>
Motion search range. Default 57

The default is derived from the default CTU size (64) minus the luma interpolation half-length (4) minus
maximum subpel distance (2) minus one extra pixel just in case the hex search method is used.
If the search range were any larger than this, another CTU row of latency would be required for reference frames.

Range of values: an integer from 0 to 32768''',

'Chinese': '''--merange <integer>
动作搜索范围。默认57

默认值来自默认CTU大小（64）减去亮度内插半长度
（4）减去最大子位置距离（2）减去一个额外像素，
以防使用十六进制搜索方法。如果搜索范围大于此值，
则参考帧将需要另一个CTU行延迟。

值范围： 0到32768之间的整数'''},

'temporal-mvp':
{'English': '''--temporal-mvp, --no-temporal-mvp
Enable temporal motion vector predictors in P and B slices.
This enables the use of the motion vector from the collocated block in the previous frame to be used as a predictor.
Default is enabled''',

'Chinese': '''--temporal-mvp, --no-temporal-mvp
在P和B切片中启用时间运动矢量预测值。
这使得能够使用来自前一帧中的并置块的运动矢量作为预测器。
默认值已启用'''},

'weightp':
{'English': '''--weightp, -w, --no-weightp
Enable weighted prediction in P slices. This enables weighting analysis in the lookahead,
which influences slice decisions, and enables weighting analysis in the main encoder which
allows P reference samples to have a weight function applied to them prior to using them
for motion compensation. In video which has lighting changes,
it can give a large improvement in compression efficiency.
Default is enabled''',

'Chinese': '''--weightp, -w, --no-weightp
在P切片中启用加权预测。这使得前瞻中的加权分析能够影响切片决策，
并且能够在主编码器中进行加权分析，其允许P参考样本在将它们用于
运动补偿之前应用权重函数。在具有照明变化的视频中，它可以大大提
高压缩效率。
默认值已启用'''},

'weightb':
{'English': '''--weightb, --no-weightb
Enable weighted prediction in B slices.
Default disabled''',

'Chinese': '''--weightb, --no-weightb
在B切片中启用加权预测。默认禁用'''},

'analyze-src-pics':
{'English': '''--analyze-src-pics, --no-analyze-src-pics
Enable motion estimation with source frame pixels, in this mode,
motion estimation can be computed independently.
Default disabled.''',

'Chinese': '''--analyze-src-pics, --no-analyze-src-pics
启用源帧像素的运动估计，在该模式下，可以独立地计算运动估计。
默认禁用。'''},

'strong-intra-smoothing':
{'English': '''--strong-intra-smoothing, --no-strong-intra-smoothing
Enable strong intra smoothing for 32x32 intra blocks.
This flag performs bi-linear interpolation of the corner reference samples for a strong smoothing effect.
The purpose is to prevent blocking or banding artifacts in regions with few/zero AC coefficients.
Default enabled''',

'Chinese': '''--strong-intra-smoothing, --no-strong-intra-smoothing
为32x32内部块启用强帧内平滑。该标志执行角参考样本的双线性插值以获得强平滑效果。
目的是防止具有很少/零AC系数的区域中的阻塞或带状伪像。
默认启用'''},

'constrained-intra':
{'English': '''--constrained-intra, --no-constrained-intra
Constrained intra prediction. When generating intra predictions for blocks in inter slices,
only intra-coded reference pixels are used. Inter-coded reference pixels are replaced with 
intra-coded neighbor pixels or default values.
The general idea is to block the propagation of reference errors that may have resulted from lossy signals.
Default disabled''',

'Chinese': '''--constrained-intra, --no-constrained-intra
约束帧内预测。当为帧间片段中的块生成帧内预测时，仅使用帧内编码的参考像素。
帧间编码的参考像素被帧内编码的相邻像素或默认值替换。一般的想法是阻止可能由
有损信号引起的参考误差的传播。
默认禁用'''},

'psy-rd':
{'English': '''--psy-rd <float>
Influence rate distortion optimizated mode decision to preserve the energy of the
source image in the encoded image at the expense of compression efficiency.
It only has effect on presets which use RDO-based mode decisions (--rd 3 and above).
1.0 is a typical value. Default 2.0

Range of values: 0 .. 5.0''',

'Chinese': '''--psy-rd <float>
影响率失真优化模式决定以牺牲压缩效率为代价来保持编码图像中的源图像的能量。
它仅对使用基于RDO的模式决策（--rd3及以上）的预设有影响。1.0是典型值。
默认2.0

值范围： 0 - 5.0'''},

'psy-rdoq':
{'English': '''--psy-rdoq <float>
Influence rate distortion optimized quantization by favoring higher energy in the reconstructed image.
This generally improves perceived visual quality at the cost of lower quality metric scores.
It only has effect when --rdoq-level is 1 or 2. High values can be beneficial in preserving high-frequency detail.
Default: 0.0 (1.0 for presets slow, slower, veryslow)

Range of values: 0 .. 50.0''',

'Chinese': '''--psy-rdoq <float>
影响率失真通过在重建图像中支持更高的能量来优化量化。
这通常以较低质量度量分数为代价改善感知视觉质量。
它仅在--rdoq-level1或2 时有效。高值可有利于保留高频细节。
默认值：0.0（1.0为预设slow，slower，veryslow）

值范围： 0 .. 50.0'''},

'open-gop':
{'English': '''--open-gop, --no-open-gop
Enable open GOP, allow I-slices to be non-IDR.
Default enabled''',

'Chinese': '''--open-gop, --no-open-gop
启用开放GOP，允许I-slice为非IDR。
默认启用'''},

'keyint':
{'English': '''--keyint, -I <integer>
Max intra period in frames. A special case of infinite-gop (single keyframe at the beginning of
the stream) can be triggered with argument -1. Use 1 to force all-intra. When intra-refresh is
enabled it specifies the interval between which refresh sweeps happen.
Default 250''',

'Chinese': '''--keyint, -I <integer>
帧内最大帧内周期。可以使用参数-1触发无限gop（流的开头处的单个关键帧）的特殊情况。
使用1强制全内部。启用内部刷新时，它指定刷新扫描发生的间隔。
默认250'''},

'min-keyint':
{'English': '''--min-keyint, -i <integer>
Minimum GOP size. Scenecuts beyond this interval are coded as IDR and start a new keyframe,
while scenecuts closer together are coded as I or P. For fixed keyframe interval,
set value to be equal to keyint.

Range of values: >=0 (0: auto)''',

'Chinese': '''--min-keyint, -i <integer>
最低GOP大小。超出此间隔的场景切换编码为IDR并开始新的关键帧，
而更靠近的场景切换编码为I或P.对于固定的关键帧间隔，将值设置为等于keyint。

值范围： > = 0（0：自动）'''},

'scenecut':
{'English': '''''',

'Chinese': '''--scenecut <integer>, --no-scenecut
需要多么积极地插入I帧。阈值越高，I帧放置越激进。
--scenecut 0或--no-scenecut禁用自适应I帧放置。
默认40'''},

'scenecut-bias':
{'English': '''''',

'Chinese': '''--scenecut-bias <0..100.0>
该值表示场景检测中使用的帧的帧间成本和帧内成本之间的百分比差异。
例如，值5表示，如果帧的帧间成本大于或等于帧的帧内成本的95％，
则将该帧检测为场景切换。建议值介于5和15之间。
默认5。'''},

'radl':
{'English': '''''',

'Chinese': '''--radl <integer>
允许在IDR前面的RADL图片数量。需要固定的关键帧间隔。
建议值是2-3。默认值为0（禁用）。

**值范围：介于0和 -bframe之间'''},

'':
{'English': '''''',

'Chinese': ''''''},

'':
{'English': '''''',

'Chinese': ''''''},

'':
{'English': '''''',

'Chinese': ''''''},

'':
{'English': '''''',

'Chinese': ''''''},

'':
{'English': '''''',

'Chinese': ''''''}}}
