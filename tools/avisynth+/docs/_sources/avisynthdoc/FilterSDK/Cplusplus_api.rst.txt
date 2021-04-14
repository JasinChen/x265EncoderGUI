
C++ API
=======

The header, avisynth.h, declares all the classes, structures and
miscellaneous constants of the C++ API that you might need when writing
a plugin. All external plugins should #include it:
::

    #include "avisynth.h"

Note, sometimes there is a reference to a version number of the plugin
api (for example v3 or v6). This refers to the value of
:doc:`AVISYNTH_INTERFACE_VERSION <AviSynthInterfaceVersion>`. The
classes and miscellaneous constants are described below.


.. toctree::
    :maxdepth: 4

.. contents:: Table of contents


.. _cplusplus_createscriptenvironment:

CreateScriptEnvironment
-----------------------

::

    IScriptEnvironment* __stdcall CreateScriptEnvironment(int version = AVISYNTH_INTERFACE_VERSION);


AviSynth exports this. It enables you to use AviSynth as a library,
without writing an AviSynth script or without going through AVIFile.
[todo add link]


Classes
-------


.. _cplusplus_avisyntherror:

AvisynthError
~~~~~~~~~~~~~

::

    AvisynthError(const char* _msg)


Wrap your code in try/catch statements to enable exception handling.
AvisynthError will tell you what's wrong.
::

    try
    {
        Val = Env->Invoke("Import", Args, 0);
        Clip = Val.AsClip();
        VidInfo = Clip->GetVideoInfo();
        Frame = Clip->GetFrame( 1, Env);
    }
     catch (AvisynthError err)
    {
        printf("%s\n", err.msg);
        return 1;
    }


.. _cplusplus_videoframebuffer:

VideoFrameBuffer
~~~~~~~~~~~~~~~~

VideoFrameBuffer (VFB) holds information about a memory block which is
used for video data. For efficiency, instances of this class are not
deleted when the refcount reaches zero; instead they are stored in a
linked list to be reused. The instances are deleted when the
corresponding AVS file is closed. Or more accurately, a
VideoFrameBuffer once new'd generally is not released until the
IScriptEnvironment is deleted, except if SetMemoryMax is exceeded by
too much then not in use VideoFrameBuffer's are forcible deleted until
SetMemoryMax is satisfied.


.. _cplusplus_videoframe:

VideoFrame
~~~~~~~~~~

VideoFrame holds a "window" into a VideoFrameBuffer. Operator new is
overloaded to recycle class instances. Its members can be called by:
::

    PVideoFrame src = child->GetFrame(n, env);
    src->GetReadPtr(..)


VideoFrame has the following members: GetPitch, GetRowSize, GetHeight,
GetReadPtr, GetWritePtr and IsWritable.

All those filters (except IsWritable) will give you a property (pitch,
rowsize, etc ...) of a plane (of the frame it points to). The
interleaved formats (BGR(A) or YUY2) consist of one plane, and the
planar formats consists of one (Y) or three (YUV) planes. The default
plane is just the first plane (which is plane Y for the planar
formats).


.. _cplusplus_getpitch:

GetPitch
^^^^^^^^

::

    int GetPitch(int plane=0) const;


The "pitch" (also called stride) of a frame buffer is the offset (in
bytes) from the beginning of one scan line to the beginning of the
next. The source and destination buffers won't necessarily have the
same pitch. The pitch can vary among frames in a clip, and it can
differ from the width of the clip. [todo add link]

| The scan line will be padded to a multiple of 8 (if necessary) due to
  speed reasons, so the pitch will always be a multiple of 8. Image
  processing is expensive, so SIMD instructions are used to speed tasks
  up:

| SSE uses 128 bit = 16 byte registers, so 8 YUY2 pixels can be processed
  the same time.

| AVX uses 256 bit = 32 byte registers, so 16 YUY2 pixels can be
  processed the same time.

NOTE that the pitch can change anytime, so in most use cases you must
request the pitch dynamically.


Usage:

GetPitch must be used on every plane (interleaved like YUY2 means 1
plane...) of every PVideoFrame that you want to read or write to. It is
the only way to get the size of the Video Buffer (e.g. get the size of
PVideoFrame):
::

    int buffer_size = src->GetPitch() * src->GetHeight(); //YUY2, interleaved


This will give you the pitch of the U-plane (it will be zero if the
plane doesn't exist):
::

    PVideoFrame src = child->GetFrame(n, env);
    const int src_pitchUV = src->GetPitch(PLANAR_U);


.. _cplusplus_getrowsize:

GetRowSize
^^^^^^^^^^

::

    int GetRowSize(int plane=0) const;


GetRowSize gives the length of each row in bytes (thus not in pixels).
It's usually equal to the pitch or slightly less, but it may be
significantly less if the frame in question has been through Crop. This
will give you the rowsize of a frame for the interleaved formats, or
the rowsize of the Y-plane for the planar formats (being the default
plane).
::

    const int src_width = src->GetRowSize();


.. _cplusplus_getheight:

GetHeight
^^^^^^^^^

::

    int GetHeight(int plane=0) const;


GetHeight gives the height of the plane in pixels.


.. _cplusplus_getreadptr:

GetReadPtr
^^^^^^^^^^

::

    const BYTE* GetReadPtr(int plane=0) const;


GetReadPtr gives you a read pointer to a plane. This will give a read
pointer to the default plane:
::

    PVideoFrame src = child->GetFrame(n, env);
    const unsigned char* srcp = src->GetReadPtr()


.. _cplusplus_getwriteptr:

GetWritePtr
^^^^^^^^^^^

::

    BYTE* GetWritePtr(int plane=0) const;


GetWritePtr gives you a write pointer to a plane.

Any buffer you get from NewVideoFrame is guaranteed to be writable (as
long as you only assign it to one PVideoFrame). Our filter's dst came
from NewVideoFrame, so we can safely call dst->GetWritePtr(). However,
frames you get from other clips via GetFrame may not be writable, in
which case GetWritePtr() will return a null pointer.
::

    PVideoFrame dst = env->NewVideoFrame(vi);
    unsigned char* dstp = dst->GetWritePtr();


If you want to write a frame which is not new (the source frame for
example), you will have to call MakeWritable first:
::

    PVideoFrame src = child->GetFrame(n, env);
    env->MakeWritable(&src);
    unsigned char* srcp = src->GetWritePtr(PLANAR_Y);


See IsWritable for more details.


.. _cplusplus_iswritable:

IsWritable
^^^^^^^^^^

::

    bool IsWritable() const;


All frame buffers are readable, but not all are writable. This method
can be used to find out if a buffer is writable or not, and there's a
MakeWritable callback (described below) to ensure that it is.

The rule about writability is this: A buffer is writable if and only if
there is exactly one PVideoFrame pointing to it. In other words, you
can only write to a buffer if no one else might be reading it. This
rule guarantees that as long as you hold on to a PVideoFrame and don't
write to it yourself, that frame will remain unchanged. The only
drawback is that you can't have two PVideoFrames pointing to a writable
buffer.
::

    PVideoFrame src = child->GetFrame(n, env);
    if (src->IsWritetable()) {...}


.. _cplusplus_alignplanar:

AlignPlanar
~~~~~~~~~~~

::

    AlignPlanar(PClip _clip);


AlignPlanar does nothing, if the pitch of a frame is at least mod16 (16
bytes, being the default frame alignment for luma and chroma).
Otherwise it realigns the image, by blitting it to a larger buffer.

Filters can enforce a lower pitch, but they must always apply the
AlignPlanar filter after itself, if they intend to return a frame with
a lower pitch. VFW delivers a 4 byte alignment for example, so the
AlignPlanar filters needs to be applied on all frames when using
AviSource.


.. _cplusplus_fillborder:

FillBorder
~~~~~~~~~~

::

    FillBorder(PClip _clip);


This function fills up the right side of the picture on planar images
with duplicates of the rightmost pixel if the planes are not aligned.
That is, if src->GetRowSize(PLANAR_Y) !=
src->GetRowSize(PLANAR_Y_ALIGNED).


.. _cplusplus_convertaudio:

ConvertAudio
~~~~~~~~~~~~

::

    ConvertAudio(PClip _clip, int prefered_format);


ConvertAudio converts the sample type of the audio to one of the
following sample types: SAMPLE_INT8 (8 bits), SAMPLE_INT16 (16 bits),
SAMPLE_INT24 (24 bits), SAMPLE_INT32 (32 bits) or SAMPLE_FLOAT (float).

The following example converts the sample type of the clip child to
SAMPLE_INT16 (16 bit) if the input isn't 16 bit.
::

    ConvertAudio(child, SAMPLE_INT16);


.. _cplusplus_iscriptenvironment:

IScriptEnvironment
~~~~~~~~~~~~~~~~~~

AviSynth exports an IScriptEnvironment interface. It enables you to use
AviSynth as a library, without writing an AVS script or without going
through AVIFile. Its members can be called by:
::

    IScriptEnvironment* env
    env->Invoke(..)


IScriptEnvironment has the following members: ThrowError, GetCPUFlags,
SaveString, Sprintf, VSprintf, Invoke, BitBlt, AtExit, AddFunction,
MakeWritable, FunctionExists, GetVar, GetVarDef, SetVar, SetGlobalVar,
PushContext, PopContext, NewVideoFrame, CheckVersion, Subframe,
SubframePlanar, SetMemoryMax, SetWorkingDir, DeleteScriptEnvironment
and ApplyMessage. They are described in the following subsections.


.. _cplusplus_throwerror:

ThrowError
^^^^^^^^^^

::

    __declspec(noreturn) virtual void __stdcall ThrowError(const char* fmt, ...) = 0;


ThrowError throws an exception (of type AvisynthError). Usually, your
error message will end up being displayed on the user's screen in lieu
of the video clip they were expecting:
::

    if (!vi.IsRGB()) {
        env->ThrowError("RGBAdjust requires RGB input");
    }


.. _cplusplus_getcpuflags:

GetCPUFlags
^^^^^^^^^^^

::

    virtual long GetCPUFlags();


GetCPUFlags returns the instruction set of your CPU. To find out if
you're running for example on a CPU that supports MMX, test:
::

    env->GetCPUFlags() & CPUF_MMX


There's a complete list of flags in avisynth.h.


.. _cplusplus_savestring:

SaveString
^^^^^^^^^^

::

    virtual char* SaveString(const char* s, int length = -1);


This function copies its argument to a safe "permanent" location and
returns a pointer to the new location. Each ScriptEnvironment instance
has a buffer set aside for storing strings, which is expanded as
needed. The strings are not deleted until the ScriptEnvironment
instance goes away (when the script file is closed, usually). This is
usually all the permanence that is needed, since all related filter
instances will already be gone by then. The returned pointer is not
const-qualified, and you're welcome to write to it, as long as you
don't stray beyond the bounds of the string.

Example usage (converting a string to upper case):
::

    AVSValue UCase(AVSValue args, void*, IScriptEnvironment* env) {
        return _strupr(env->SaveString(args[0].AsString()));
    }


.. _cplusplus_sprintf_vsprintf:

Sprintf and VSprintf
^^^^^^^^^^^^^^^^^^^^

::

    virtual char* Sprintf(const char* fmt, ...);
    virtual char* VSprintf(const char* fmt, char* val);


These store strings away in the same way as SaveString, but they treat
their arguments like printf and vprintf. Currently there's a size limit
of 4096 characters on strings created this way. (The implementation
uses _vsnprintf, so you don't need to worry about buffer overrun.)


.. _cplusplus_invoke:

Invoke
^^^^^^

::

    virtual AVSValue Invoke(const char* name, const AVSValue args, const char** arg_names=0);


You can use this to call a script function. There are many script
functions which can be useful from other filters; for example, the Bob
filter uses SeparateFields, and several source filters use
UnalignedSplice. Some functions, like Weave, are implemented entirely
in terms of other functions. If you're calling a function taking
exactly one argument, you can simply pass it in the args parameter;
Invoke will convert it into an array for you. In order to call a
function taking multiple arguments, you will need to create the array
yourself; it can be done like this:
::

    AVSValue up_args[3] = {child, 384, 288};
    PClip resized = env->Invoke("LanczosResize", AVSValue(up_args,3)).AsClip();


In this case LanczosResize would need to have a parameter-type string
like "cii".

The arg_names parameter can be used to specify named arguments. Named
arguments can also be given positionally, if you prefer.

Invoke throws IScriptEnvironment::NotFound if it can't find a matching
function prototype. You should be prepared to catch this unless you
know that the function exists and will accept the given arguments.


.. _cplusplus_bitblt:

BitBlt
^^^^^^

::

    virtual void BitBlt(unsigned char* dstp, int dst_pitch, const unsigned char* srcp, int src_pitch, int row_size, int height);


This brilliantly-named function does a line-by-line copy from the
source to the destination. It's useful for quite a number of things;
the built-in filters DoubleWeave, FlipVertical, AddBorders,
PeculiarBlend, StackVertical, StackHorizontal, and ShowFiveVersions all
use it to do their dirty work.

In AddBorders it's to copy the Y-plane from the source to the
destination frame (for planar formats):
::

    const int initial_black = top*dst_pitch + vi.BytesFromPixels(left);
    if (vi.IsPlanar()) {
        BitBlt(dstp+initial_black, dst_pitch, srcp, src_pitch, src_row_size, src_height);
        ...
    }


left is the number of pixels which is added to the left, top the number
which is added to the top. So the first source pixel, srcp[0], is
copied to its new location dstp[x], and so on. The remaining bytes are
zeroed and can be refilled later on.


.. _cplusplus_atexit:

AtExit
^^^^^^

::

    virtual void AtExit(ShutdownFunc function, void* user_data);


When IScriptEnvironment is deleted on script close the AtExit functions
get run. When you register the function you can optionally provide some
user data. When the function is finally called this data will be
provided as the argument to the procedure.

The example below (thanks to tsp) loads a library and automatically
unloads it (by using AtExit) after the script is closed. It can be
useful when your plugin depends on a library and you want to load the
library in your script (the plugin fft3dfilter.dll depends on the
library fftw3.dll for example):
::

    void __cdecl UnloadDll(void* hinst, IScriptEnvironment* env) {
        if (hinst)
        FreeLibrary(static_cast<HMODULE>(hinst));
    }

    AVSValue __cdecl LoadDll(AVSValue args, void* user_data, IScriptEnvironment* env){
        HMODULE hinst = 0;
        hinst = LoadLibrary(args[0].AsString()); // loads a library
        env->AtExit(UnloadDll, hinst); // calls UnloadDll to unload the library upon script exit
        return hinst!=NULL;
    }


.. _cplusplus_addfunction:

AddFunction
^^^^^^^^^^^

::

    virtual void __stdcall AddFunction(const char* name, const char* params, ApplyFunc apply, void* user_data) = 0;


The main purpose of the AvisynthPluginInit2 (or AvisynthPluginInit3)
function is to call env->AddFunction.
::

    env->AddFunction("Sepia", "c[color]i[mode]s", Create_Sepia, 0);


AddFunction is called to let Avisynth know of the existence of our
filter. It just registers a function with Avisynth's internal function
table. This function takes four arguments: the name of the new script
function; the parameter-type string; the C++ function implementing the
script function; and the user_data cookie.

The added function is of type AVSValue and can therefore return any
AVSValue. Here are a few options how to return from the "added"
function:
::

    AVSValue __cdecl returnSomething(AVSValue args, void* user_data, IScriptEnvironment* env){

    char *strlit = "AnyOldName";
    int len = strlen(strlit);
    char *s = new char[len+1];

    if (s==NULL)
        env->ThrowError("Cannot allocate string mem");

    strcpy(s, strlit); // duplicate
    char *e = s+len; // point at null

    // make safe copy of string (memory is freed on Avisynth closure)
    AVSValue ret = env->SaveString(s,e-s); // e-s is text len only (excl null) {SaveString uses memcpy)

    // alternative, Avisynth uses strlen to ascertain length
    // AVSValue ret = env->SaveString(s);

    delete []s; // delete our temp s buffer
    return ret; // return saved string as AVSValue

    // alternative to MOST of above code char* converted to AVSValue.
    // return strlit;

    // alternative to ALL of above code char* converted to AVSValue.
    // return "AnyOldName";

    // String literals are read only and at constant address and so need not be saved.
    }


.. _cplusplus_makewritable:

MakeWritable
^^^^^^^^^^^^

::

    virtual bool __stdcall MakeWritable(PVideoFrame* pvf) = 0;


MakeWritable only copies the active part of the frame to a completely
new frame with a default pitch. You need this to recieve a valid write
pointer to an existing frame.
::

    PVideoFrame src = child->GetFrame(n, env);
    env->MakeWritable(&src);


.. _cplusplus_functionexists:

FunctionExists
^^^^^^^^^^^^^^

::

    virtual bool __stdcall FunctionExists(const char* name) = 0;


FunctionExists returns true if the specified filter exists, otherwise
returns false:
::

    if (env->FunctionExists("Import")) {
        env->ThrowError("Yes, the IMPORT function exist.");
    } else {
        env->ThrowError("No, the IMPORT function don't exist.");
    }


.. _cplusplus_getvar:

GetVar
^^^^^^

::

    virtual AVSValue __stdcall GetVar(const char* name) = 0;


GetVar can be used to access AviSynth variables. It will throw an error
if the variable doesn't exist.

Internal and external (plugin) functions are, for example, exported as
AviSynth variables:

* $InternalFunctions$ Should contain a string consisting of function
  names of all internal functions.
* $InternalFunctions!Functionname!Param$ Should contain all
  parameters for each internal function.
* $PluginFunctions$ Should contain a string of all plugins in your
  autoloading plugin folder.
* $Plugin!Functionname!Param$ Should contain all parameters.

Use env->GetVar() to access them. This example returns a string
consisting of all parameters of ConvertToYV12:
::

    const char* plugin_dir;
    plugin_dir = env->GetVar("$Plugin!ConverttoYV12!Param$").AsString();


This example returns the plugin folder which is used to autoload your
plugins (and returns an error if it's not set):
::

    try {
        const char* plugin_dir;
        plugin_dir = env->GetVar("$PluginDir$").AsString();
        env->ThrowError(plugin_dir);
    } catch(...) {
        env->ThrowError("Plugin directory not set.");
    }


If you are making a conditional filter you can use it to get the
current framenumber:
::

    // Get current frame number
    AVSValue cf = env->GetVar("current_frame");
    if (!cf.IsInt())
        env->ThrowError("MinMaxAudio: This filter can only be used within ConditionalFilter");
    int n = cf.AsInt();
    PVideoFrame src = child->GetFrame(n, env);


.. _cplusplus_getvardef:

GetVarDef, v6
^^^^^^^^^^^^^

::

    virtual AVSValue __stdcall GetVarDef(const char* name, const AVSValue& def=AVSValue()) = 0;


GetVarDef can be used to access AviSynth variables. It will return
'def' if the variable doesn't exist (instead of throwing an error):
::

    int error;
    AVSValue error = env->GetVarDef("VarUnknown", AVSValue(-1)); // returns -1 when 'VarUnknown' doesn't exist
    if (error==-1)
        env->ThrowError("Plugin: The variable 'VarUnknown' doesn't exist!");


.. _cplusplus_setvar:

SetVar
^^^^^^

::

    virtual bool __stdcall SetVar(const char* name, const AVSValue& val) = 0;


It will return true if the variable was created and filled with the
given value. It will return false in case the variable was already
there and we just updated its value.

SetVar can be used to set/create AviSynth variables. The created
variables are only visible in the local scope, e.g. script functions
have a new scope.

This example sets the autoloading plugin folder to ``"C:\\"``
::

    if (env->SetVar("$PluginDir$", AVSValue("C:\\"))) {
        //variable was created
    } else {
        //variable was already existing and updated
    }


This example sets variables in GetFrame which can be accessed later on
in a script within the conditional environment:
::

    // saves the blue value of a pixel
    int BlueValue;
    BlueValue = srcp[x];
    env->SetVar("BlueValue", AVSValue(BlueValue));


.. _cplusplus_setglobalvar:

SetGlobalVar
^^^^^^^^^^^^

::

    virtual bool __stdcall SetGlobalVar(const char* name, const AVSValue& val) = 0;


Usage:

SetGlobalVar can be used to create or set AviSynth variables that are
visible within global scope. It is possible that a single filter may
want to use SetVar in order to exchange signals to possible other
instances of itself.

There are at least 4 different components that make use of
Set(Global)Var functions:

* the core itself
* the user within the avs script
* filters/plugins
* a custom application that invoked the environment

All of above may have their own requirements for the SetVar function.
Some may want to be visible globally, others may not.


.. _cplusplus_pushcontext:

PushContext
^^^^^^^^^^^

::

    virtual void __stdcall PushContext(int level=0) = 0;


| // TODO - see (also similar functions)
| http://forum.doom9.org/showthread.php?p=1595750#post1595750


.. _cplusplus_popcontext:

PopContext
^^^^^^^^^^

::

    virtual void __stdcall PopContext() = 0;


?


.. _cplusplus_popcontextglobal:

PopContextGlobal
^^^^^^^^^^^^^^^^

::

    virtual void __stdcall PopContextGlobal() = 0;


?


.. _cplusplus_newvideoframe:

NewVideoFrame
^^^^^^^^^^^^^

::

    virtual PVideoFrame __stdcall NewVideoFrame(const VideoInfo& vi, int align=FRAME_ALIGN) = 0;
    // default align is 16


The NewVideoFrame callback allocates space for a video frame of the
supplied size. (In this case it will hold our filter's output.) The
frame buffer is uninitialized raw memory (except that in the debug
build it gets filled with the repeating byte pattern 0A 11 0C A7 ED,
which is easy to recognize because it looks like "ALLOCATED"). "vi" is
a protected member of GenericVideoFilter. It is a structure of type
VideoInfo, which contains information about the clip (like frame size,
frame rate, pixel format, audio sample rate, etc.). NewVideoFrame uses
the information in this structure to return a frame buffer of the
appropriate size.

The following example creates a new VideoInfo structure and creates a
new video frame from it:
::

    VideoInfo vi;
    PVideoFrame frame;
    memset(&vi, 0, sizeof(VideoInfo));
    vi.width = 640;
    vi.height = 480;
    vi.fps_numerator = 30000;
    vi.fps_denominator = 1001;
    vi.num_frames = 107892; // 1 hour
    vi.pixel_type = VideoInfo::CS_BGR32;
    vi.sample_type = SAMPLE_FLOAT;
    vi.nchannels = 2;
    vi.audio_samples_per_second = 48000;
    vi.num_audio_samples = vi.AudioSamplesFromFrames(vi.num_frames);
    frame = env->NewVideoFrame(vi);


.. _cplusplus_checkversion:

CheckVersion
^^^^^^^^^^^^

::

    virtual void __stdcall CheckVersion(int version = AVISYNTH_INTERFACE_VERSION) = 0;


CheckVersion checks the interface version (avisynth.h). It throws an
error if 'version' is bigger than the used interface version. The
following interface versions are in use:

AVISYNTH_INTERFACE_VERSION = 1 (v1.0-v2.0.8), 2 (v2.5.0-v2.5.5), 3
(v2.5.6-v2.5.8), 5 (v2.6.0a1-v2.6.0a5), or 6 (v2.6.0) [version 4 doesn't exist].

This example will throw an error if v2.5x or an older AviSynth version
is being used:
::

    env->CheckVersion(5)


This can be used in a plugin, for example, if it needs at least a
certain interface version for it to work.


.. _cplusplus_subframe:

Subframe
^^^^^^^^

::

    virtual PVideoFrame __stdcall Subframe(PVideoFrame src, int rel_offset, int new_pitch, int new_row_size, int new_height) = 0;


Subframe (for interleaved formats) extracts a part of a video frame.
For planar formats use SubframePlanar. For examples see SubframePlanar.


.. _cplusplus_subframeplanar:

SubframePlanar
^^^^^^^^^^^^^^

::

    virtual PVideoFrame __stdcall SubframePlanar(PVideoFrame src, int rel_offset, int new_pitch, int new_row_size, int new_height, int rel_offsetU, int rel_offsetV, int new_pitchUV) = 0;


SubframePlanar (for planar formats) extracts a part of a video frame.
The example below returns the first field of a frame:
::

    vi.height >>= 1; // sets new height in the constructor
    PVideoFrame frame = child->GetFrame(n, env);
    if (vi.IsPlanar()) { // SubframePlanar works on planar formats only
        const int frame_pitch = frame->GetPitch(PLANAR_Y);
        const int frame_width = frame->GetRowSize(PLANAR_Y);
        const int frame_height = frame->GetHeight(PLANAR_Y);
        const int frame_pitchUV = frame->GetPitch(PLANAR_U);
        return env->SubframePlanar(frame, 0, 2*frame_pitch, frame_width, frame_height>>1, 0, 0, 2*frame_pitchUV);
    }


Note that it copies the first row of pixels and moves on to the third
row (by moving the offset by '2*frame_pitch'). After frame_height/2 it
stops reading.

The following example keeps the left 100 pixels of a clip (it leaves
the height unaltered) and throws away the rest:
::

    vi.width = 100; // sets new width in the constructor
    PVideoFrame frame = child->GetFrame(n, env);
    if (vi.IsPlanar()) { // SubframePlanar works on planar formats only
        const int frame_pitch = frame->GetPitch(PLANAR_Y);
        const int frame_height = frame->GetHeight(PLANAR_Y);
        const int frame_pitchUV = frame->GetPitch(PLANAR_U);
        return env->SubframePlanar(frame, 0, frame_pitch, 100, frame_height, 0, 0, frame_pitchUV);
    }


Note that it copies 100 pixels and moves on to the next row (by moving
the offset by 'frame_pitch').

You need to check somewhere that the source frames is more than 100
pixels wide, otherwise throw an error.


.. _cplusplus_setmemorymax:

SetMemoryMax
^^^^^^^^^^^^

::

    virtual int __stdcall SetMemoryMax(int mem) = 0;


There is a builtin cache automatically inserted in between all filters.
You can use SetmemoryMax to increase the size.

SetMemoryMax only sets the size of the frame buffer cache. It is
independent of any other memory allocation. Memory usage due to the
frame cache should ramp up pretty quickly to the limited value and stay
there. Setting a lower SetMemoryMax value will make more memory
available for other purposes and provide less cache buffer frames. It
is pointless having more buffers available than are needed by the
scripts temporal requirements. If each and every frame generated at
each and every stage of a script is only ever used once then the cache
is entirely useless. By definition a cache is only useful if a
generated element is needed a second or subsequent time.


.. _cplusplus_setworkingdir:

SetWorkingDir
^^^^^^^^^^^^^

::

    virtual int __stdcall SetWorkingDir(const char * newdir) = 0;


Sets the default directory for AviSynth.


.. _cplusplus_deletescriptenvironment:

DeleteScriptEnvironment, v5
^^^^^^^^^^^^^^^^^^^^^^^^^^^

::

    virtual void __stdcall DeleteScriptEnvironment() = 0;


Provides a method to delete the ScriptEnvironment which is created with
CreateScriptEnvironment.


.. _cplusplus_applymessage:

ApplyMessage, v5
^^^^^^^^^^^^^^^^

::

    virtual void _stdcall ApplyMessage(PVideoFrame* frame, const VideoInfo& vi, const char* message, int size, int textcolor, int halocolor, int bgcolor) = 0;


ApplyMessage writes text on a frame. For example:
::

    char BUF[256];
    PVideoFrame src = child->GetFrame(n, env);
    env->MakeWritable(&src);
    sprintf(BUF, "Filter: Frame %d is processed.", n);
    env->ApplyMessage(&src, vi, BUF, vi.width/4, 0xf0f080, 0, 0);


.. _cplusplus_getavslinkage:

GetAVSLinkage, v5
^^^^^^^^^^^^^^^^^

::

    virtual const AVS_Linkage* const __stdcall GetAVSLinkage() = 0;

Returns the :doc:`AVSLinkage <AVSLinkage>`.

todo: how and when to use that ...


.. _cplusplus_pvideoframe:

PVideoFrame
~~~~~~~~~~~

PVideoFrame is a smart pointer to VideoFrame.

In this example it gives a pointer to frame 'n' from child:
::

    PVideoFrame src = child->GetFrame(n, env);


"child" is a protected member of GenericVideoFilter, of type PClip. It
contains the clip that was passed to the constructor. For our filter to
produce frame n we need the corresponding frame of the input. If you
need a different frame from the input, all you have to do is pass a
different frame number to child->GetFrame.

In this example it gives a pointer to a new created VideoFrame from vi
(which is a VideoInfo structure):
::

    PVideoFrame dst = env->NewVideoFrame(vi);


"vi" is another protected member of GenericVideoFilter (the only other
member, actually). It is a structure of type VideoInfo, which contains
information about the clip (like frame size, frame rate, pixel format,
audio sample rate, etc.). NewVideoFrame uses the information in this
struct to return a frame buffer of the appropriate size.


.. _cplusplus_iclip:

IClip
~~~~~

An Avisynth filter is simply a C++ class implementing the IClip
interface. IClip has four pure virtual methods: GetVideoInfo, GetFrame,
GetParity, and GetAudio. The class GenericVideoFilter is a simple
do-nothing filter defined in avisynth.h. It derives from IClip and
implements all four methods. Most filters can inherit from
GenericVideoFilter rather than directly from IClip; this saves you from
having to implement methods that you don't care about, like GetAudio.

IClip has the following members: GetVersion, GetFrame, GetParity,
GetAudio, SetCacheHints and GetVideoInfo. They are described in the
following subsections.


.. _cplusplus_getversion:

GetVersion
^^^^^^^^^^

::

    virtual int __stdcall GetVersion() { return AVISYNTH_INTERFACE_VERSION; }


GetVersion returns the interface version of the loaded avisynth.dll:

AVISYNTH_INTERFACE_VERSION = 1 (v1.0-v2.0.8), 2 (v2.5.0-v2.5.5), 3
(v2.5.6-v2.5.8), 5 (v2.6.0a1-v2.6.0a5), or 6 (v2.6.0) [version 4 doesn't exist].


.. _cplusplus_getframe:

GetFrame
^^^^^^^^

::

    virtual PVideoFrame __stdcall GetFrame(int n, IScriptEnvironment* env) = 0;


GetFrame returns a video frame. In this example, the even frames (0, 2,
4, ...) of 'child' are returned:
::

    PVideoFrame src = child->GetFrame(2*n, env);


You should do all the GetFrame() calls BEFORE you get any pointers and
start manipulating any data.


.. _cplusplus_getparity:

GetParity
^^^^^^^^^

::

    virtual bool __stdcall GetParity(int n) = 0;


GetParity returns the field parity if the clip is field-based,
otherwise it returns the parity of first field of a frame. In other
words, it distinguishes between top field first (TFF) and bottom field
first (BFF). When it returns true, it means that this frame should be
considered TFF, otherwise it should be considered BFF.


.. _cplusplus_getaudio:

GetAudio
^^^^^^^^

::

    virtual void __stdcall GetAudio(void* buf, __int64 start, __int64 count, IScriptEnvironment* env) = 0;


Audio processing is handled through the GetAudio method. You must fill
in the buffer with count samples beginning at the sample start. A
sample may vary from one to four bytes, depending on whether the audio
is 8, 16, 24 or 32-bit (float is also 32-bit). The flag vi.SampleType()
will tell you this.

If you cannot do your audio processing in-place, you must allocate your
own buffer for the source audio using new or malloc.

In this example, the audio of frame 'n' is returned (in the buffer
'samples'):
::

    VideoInfo vi = child->GetVideoInfo();
    PVideoFrame src = child->GetFrame(n, env);
    const __int64 start = vi.AudioSamplesFromFrames(n);
    const __int64 count = vi.AudioSamplesFromFrames(1);
    SFLOAT* samples = new SFLOAT[count*vi.AudioChannels()];
    child->GetAudio(samples, max(0,start), count, env);


.. _cplusplus_setcachehints:

SetCacheHints
^^^^^^^^^^^^^

::

    void __stdcall SetCacheHints(int cachehints, int frame_range) = 0 ;
    // We do not pass cache requests upwards, only to the next filter.

    // int __stdcall SetCacheHints(int cachehints, int frame_range) = 0 ;
    // We do not pass cache requests upwards, only to the next filter.


SetCacheHints should be used in filters that request multiple frames
from any single PClip source per input GetFrame call. frame_range is
maximal 21.

The possible values of cachehints are:
::

    CACHE_NOTHING=0    // Filter requested no caching.
    CACHE_RANGE=1      // An explicit cache of "frame_range" frames around the current frame.
    CACHE_ALL=2        // This is default operation, a simple LRU cache.
    CACHE_AUDIO=3      // Audio caching.
    CACHE_AUDIO_NONE=4 // Filter requested no audio caching.
    CACHE_AUDIO_AUTO=5 // Audio caching (difference with CACHE_AUDIO?).


When caching video frames (cachehints=0, 1, 2), frame_range is the
radius around the current frame. When caching audio samples
(cachehints=3, 4, 5), the value 0 creates a default buffer of 64kb and
positive values allocate frame_range bytes for the cache.

E.g. If you have a single PClip source, i.e. child and you get asked
for frame 100 and you in turn then ask for frames 98, 99, 100, 101 and
102 then you need to call CACHE_RANGE with frame_range set to 3:
::

    child->SetCacheHints(CACHE_RANGE, 3);

Frames outside the specified radius are candidate for normal LRU
caching.

| // TODO - describe input and output for v5 //
| http://forum.doom9.org/showthread.php?p=1595750#post1595750


.. _cplusplus_getvideoinfo:

GetVideoInfo
^^^^^^^^^^^^

::

    virtual const VideoInfo& __stdcall GetVideoInfo() = 0;


GetVideoInfo returns a :doc:`VideoInfo <VideoInfo>` structure.


.. _cplusplus_pclip:

PClip
~~~~~

PClip is a smart pointer to an IClip, and IClip is a generic abstract
class.. It maintains a reference count on the IClip object and
automagically deletes it when the last PClip referencing it goes away.
For obvious reasons, you should always use PClip rather than IClip* to
refer to clips.

Like a genuine pointer, a PClip is only four bytes long, so you can
pass it around by value. Also like a pointer, a PClip can be assigned a
null value (0), which is often useful as a sentinel. Unlike a pointer,

PClip is initialized to 0 by default.

You'll need to make sure your class doesn't contain any circular PClip
references, or any PClips sitting in dynamically allocated memory that
you forget to delete. Other than that, you don't have to worry about
the reference-counting machinery.

AviSynth filters have a standardized output channel via IClip, but
(unlike VirtualDub filters) no standardized input channel. Each filter
is responsible for obtaining its own source material -- usually (as in
this case) from another clip, but sometimes from several different
clips, or from a file.

The clip functionality must be provided by some concrete subclass of
IClip which implements the functions GetFrame(), etc. So you cannot
create a PClip without having an appropriate IClip subclass. For most
filters, the GenericVideoFilter class provides the basis for this, but
'source' filters (which is basically what you have) do not have a
parent clip and so GenericVideoFilter is not appropriate.


.. _cplusplus_avsvalue:

AVSValue
~~~~~~~~

AVSValue is a variant type which can hold any one of the following
types: a boolean value (true/false); an integer; a floating-point
number; a string; a video clip (PClip); an array of AVSValues; or
nothing ("undefined").

It holds an array of AVSValues in the following way:
::

    AVSValue(const AVSValue* a, int size) { type = 'a'; array = a; array_size = size; }


For example:
::

    AVSValue up_args[3] = {child, 384, 288};
    PClip resized = env->Invoke("LanczosResize", AVSValue(up_args,3)).AsClip();


Note that
::

    AVSValue(up_args,3)


returns the following:
::

    {'a'; {child, 384, 288}; 3}


Also Invoke returns an AVSValue (see its declaration) which in that
case is a PClip.


.. _cplusplus_structures:

Structures
----------

The following structure is available: VideoInfo structure. It holds
global information about a clip (i.e. information that does not depend
on the framenumber). The GetVideoInfo method in IClip returns this
structure. A description (for AVISYNTH_INTERFACE_VERSION=6) of it can
be found :doc:`here <VideoInfo>`.


.. _cplusplus_constants:

Constants
---------

The following constants are defined in avisynth.h:
::

    // Audio Sample information
    typedef float SFLOAT;


::

    enum { // sample types
        SAMPLE_INT8 = 1<<0,
        SAMPLE_INT16 = 1<<1,
        SAMPLE_INT24 = 1<<2,
        SAMPLE_INT32 = 1<<3,
        SAMPLE_FLOAT = 1<<4
    };


::

    enum { // plane types
        PLANAR_Y = 1<<0,
        PLANAR_U = 1<<1,
        PLANAR_V = 1<<2,
        PLANAR_ALIGNED = 1<<3,
        PLANAR_Y_ALIGNED = PLANAR_Y | PLANAR_ALIGNED,
        PLANAR_U_ALIGNED = PLANAR_U | PLANAR_ALIGNED,
        PLANAR_V_ALIGNED = PLANAR_V | PLANAR_ALIGNED,
        PLANAR_A = 1<<4, // v5
        PLANAR_R = 1<<5, // v5
        PLANAR_G = 1<<6, // v5
        PLANAR_B = 1<<7, // v5
        PLANAR_A_ALIGNED = PLANAR_A | PLANAR_ALIGNED, // v5
        PLANAR_R_ALIGNED = PLANAR_R | PLANAR_ALIGNED, // v5
        PLANAR_G_ALIGNED = PLANAR_G | PLANAR_ALIGNED, // v5
        PLANAR_B_ALIGNED = PLANAR_B | PLANAR_ALIGNED, // v5
    };


::

    enum { // cache types
        // Old 2.5 poorly defined cache hints (v3).
        // Reserve values used by 2.5 API
        // Do not use in new filters
        CACHE_25_NOTHING = 0,    // Filter requested no caching.
        CACHE_25_RANGE = 1,      // An explicit cache of "frame_range" frames around the current frame.
        CACHE_25_ALL = 2,        // This is default operation, a simple LRU cache.
        CACHE_25_AUDIO = 3,      // Audio caching.
        CACHE_25_AUDIO_NONE = 4, // Filter requested no audio caching.
        CACHE_25_AUDIO_AUTO = 5, // Audio caching (difference with CACHE_AUDIO?).

        // New 2.6 explicitly defined cache hints (v5).
        CACHE_NOTHING = 10,       // Do not cache video.
        CACHE_WINDOW = 11,        // Hard protect upto X frames within a range of X from the current frame N.
        CACHE_GENERIC = 12,       // LRU cache upto X frames.
        CACHE_FORCE_GENERIC = 13, // LRU cache upto X frames, override any previous CACHE_WINDOW.

        CACHE_GET_POLICY = 30, // Get the current policy.
        CACHE_GET_WINDOW = 31, // Get the current window h_span.
        CACHE_GET_RANGE = 32,  // Get the current generic frame range.

        CACHE_AUDIO = 50,         // Explicitly do cache audio, X byte cache.
        CACHE_AUDIO_NOTHING = 51, // Explicitly do not cache audio.
        CACHE_AUDIO_NONE = 52,    // Audio cache off (auto mode), X byte intial cache.
        CACHE_AUDIO_AUTO = 53,    // Audio cache on (auto mode), X byte intial cache.

        CACHE_GET_AUDIO_POLICY = 70, // Get the current audio policy.
        CACHE_GET_AUDIO_SIZE = 71,   // Get the current audio cache size.

        CACHE_PREFETCH_FRAME = 100, // Queue request to prefetch frame N.
        CACHE_PREFETCH_GO = 101,    // Action video prefetches.

        CACHE_PREFETCH_AUDIO_BEGIN = 120,   // Begin queue request transaction to prefetch audio (take critical section).
        CACHE_PREFETCH_AUDIO_STARTLO = 121, // Set low 32 bits of start.
        CACHE_PREFETCH_AUDIO_STARTHI = 122, // Set high 32 bits of start.
        CACHE_PREFETCH_AUDIO_COUNT = 123,   // Set low 32 bits of length.
        CACHE_PREFETCH_AUDIO_COMMIT = 124,  // Enqueue request transaction to prefetch audio (release critical section).
        CACHE_PREFETCH_AUDIO_GO = 125,      // Action audio prefetches.

        CACHE_GETCHILD_CACHE_MODE = 200, // Cache ask Child for desired video cache mode.
        CACHE_GETCHILD_CACHE_SIZE = 201, // Cache ask Child for desired video cache size.
        CACHE_GETCHILD_AUDIO_MODE = 202, // Cache ask Child for desired audio cache mode.
        CACHE_GETCHILD_AUDIO_SIZE = 203, // Cache ask Child for desired audio cache size.

        CACHE_GETCHILD_COST = 220, // Cache ask Child for estimated processing cost.
        CACHE_COST_ZERO = 221,     // Child response of zero cost (ptr arithmetic only).
        CACHE_COST_UNIT = 222,     // Child response of unit cost (less than or equal 1 full frame blit).
        CACHE_COST_LOW = 223,      // Child response of light cost. (Fast)
        CACHE_COST_MED = 224,      // Child response of medium cost. (Real time)
        CACHE_COST_HI = 225,       // Child response of heavy cost. (Slow)

        CACHE_GETCHILD_THREAD_MODE = 240, // Cache ask Child for thread safetyness.
        CACHE_THREAD_UNSAFE = 241,        // Only 1 thread allowed for all instances. 2.5 filters default!
        CACHE_THREAD_CLASS = 242,         // Only 1 thread allowed for each instance. 2.6 filters default!
        CACHE_THREAD_SAFE = 243,          // Allow all threads in any instance.
        CACHE_THREAD_OWN = 244,           // Safe but limit to 1 thread, internally threaded.

        CACHE_GETCHILD_ACCESS_COST = 260, // Cache ask Child for preferred access pattern.
        CACHE_ACCESS_RAND = 261,          // Filter is access order agnostic.
        CACHE_ACCESS_SEQ0 = 262,          // Filter prefers sequential access (low cost)
        CACHE_ACCESS_SEQ1 = 263,          // Filter needs sequential access (high cost)
    };


::

    enum { // For GetCPUFlags. These are backwards-compatible with those in VirtualDub.
        /* oldest CPU to support extension */
        CPUF_FORCE = 0x01,       // N/A
        CPUF_FPU = 0x02,         // 386/486DX
        CPUF_MMX = 0x04,         // P55C, K6, PII
        CPUF_INTEGER_SSE = 0x08, // PIII, Athlon
        CPUF_SSE = 0x10,         // PIII, Athlon XP/MP
        CPUF_SSE2 = 0x20,        // PIV, K8
        CPUF_3DNOW = 0x40,       // K6-2
        CPUF_3DNOW_EXT = 0x80,   // Athlon
        CPUF_X86_64 = 0xA0,      // Hammer (note: equiv. to 3DNow + SSE2, which only Hammer will have anyway)
        CPUF_SSE3 = 0x100,       // PIV+, K8 Venice

        // Additional CPU flags in 2.6 (v5).
        CPUF_SSSE3 = 0x200,     // Core 2
        CPUF_SSE4 = 0x400,      // Penryn, Wolfdale, Yorkfield
        CPUF_SSE4_1 = 0x400,
        CPUF_SSE4_2 = 0x1000,   //  Nehalem (note this was 0x800 in v5)
    };


____

Back to :doc:`FilterSDK`

$Date: 2015/01/13 00:24:50 $
