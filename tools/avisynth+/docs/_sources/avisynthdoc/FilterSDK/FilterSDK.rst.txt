
AviSynth FilterSDK
==================

AviSynth external Filter SDK is a package for developers to create your own
filters (plugins and console applications) for AviSynth.

The package consists of:

-   these documentation text files (in HTML or Wiki format);
-   the header file 'avisynth.h' (recent version) with all declarations
    to include in plugin source code;
-   several plugin and console application source codes;
-   some extra files in 'Extra' folder.

.. toctree::
    :maxdepth: 3

.. contents:: Table of contents


Necessary software
------------------

You must have some :doc:`necessary software. <SDKNecessaries>`

Writing a plugin
----------------

We will start by writing some simple plugins to show you the basics.

Processing video
~~~~~~~~~~~~~~~~

* :doc:`InvertNeg` produces a photo-negative of the input clip.
* :doc:`SimpleSample` has some very simple examples covering development
  of a filter that draws a variable sized square, in the middle of
  the screen. It does so for all color formats.

One thing not covered in SimpleSample, is how to :doc:`change frame size <ChangeFrameSize>` in a
filter.

Processing audio
~~~~~~~~~~~~~~~~

* xxx

Also have a look at :doc:`Getting started with Audio <GettingStartedWithAudio>`.

Runtime functions
~~~~~~~~~~~~~~~~~

See :doc:`Non-clip sample <Non-ClipSample>` how to create runtime AviSynth functions.

Source filters
~~~~~~~~~~~~~~

* :doc:`GradientMask <GradientMask>` creates a simple Gradient. The example explains a
  few things how source filters work.

Speeding up your plugin using assembler
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

You can also browse various topic on :doc:`Assembler Optimizing <AssemblerOptimizing>`.

Making dual plugins
~~~~~~~~~~~~~~~~~~~

One of the features of AviSynth 2.6 is that 2.5 plugins (plugins
compiled with plugin api v3) can still be used in AviSynth 2.6,
although you need to make sure you use it properly since it doesn't
know about the new features in AviSynth 2.6. So when processing a clip
(with say color format YV16) with a 2.5 plugin you will get a messed up
clip at best, and a crash at worst, since YV16 is not supported in the
v3 api.

There are several ways to make 2.6 plugins (plugins compiled with
plugin api v5 or higher) also work with AviSynth 2.5. They are
described :doc:`here <DualPlugins>`.

Writing console applications that access AviSynth
-------------------------------------------------

When writing console applications (commandline programs) it is possible
to access AviSynth in two ways.

The first one is to use the VfW api (using the `AVIFile library`_)
like is done in avs2avi (see `[1]`_ or `[2]`_), avs2yuv (`using
the C api`_, or `using the C++ api`_), or `avs2wav`_ for example. See
also `here`_ to get you going.

The second one is to call AviSynth directly like is done in
`avs2pipe`_ for example (it uses the C api). It's a tool to output y4m
video or wav audio to stdout. The way to do this is importing
avisynth.dll via loadlibrary() and getprocaddress(). Then creating a
scriptenvironment and importing a script using invoke(). At that point
you will have a clip from which you can call getframe() to access the
video and getaudio() to access the audio.
 
Below are some examples that have a script as input and raw video or
audio as output:

* :doc:`avs2yuv` reads a script and outputs raw video.
* :doc:`avs2pcm` reads a script and outputs raw audio.

Compiling plugins and console applications that access AviSynth
---------------------------------------------------------------

How to compile plugins and console applications that access AviSynth is
described :doc:`here <CompilingAvisynthPlugins>`.

Debugging plugins and console applications that access AviSynth
---------------------------------------------------------------

How to debug plugins and console applications that access AviSynth is
described :doc:`here <DebuggingAvisynthPlugins>`.

AviSynth and its plugin api's
-----------------------------

AviSynth exists as an instance of the ScriptEnvironment class, that
implements the IScriptEnvironment interface. The IScriptEnvironment
interface is defined in avisynth.h (and avisynth_c.h) and it is the
only way for plugins and external applications to communicate with
AviSynth. A pointer to ScriptEnvironment object is passed along to all
plugins, so that they can use AviSynth facilities. Plugins are
forbidden from storing this pointer. AviSynth creates one
ScriptEnvironment object when Windows attempts to use AviSynth to open
a script via AVIFile API.

When ScriptEnvironment is created, it checks for CPU extensions (to
provide this information to filters that are able to use CPU
extensions), sets up memory limits for itself and performs pre-scanning
of all plugins.

AviSynth has the capability to load third-party libraries that include
their own video and audio filters. It comes with two language
interfaces (or plugin api's):

* C++ API (through avisynth.h) - The classes and miscellaneous
  constants are described in :doc:`here <Cplusplus_api>`.
* C API (through avisynth_c.h) - The classes and miscellaneous
  constants are described in :doc:`here <C_api>`.

The built-in filters use the C++ API. This Filter SDK (or Source
Development Kit) describes how to create plugins using both interfaces.

Although not included in AviSynth itself, several people wrote other
language interfaces in Delphi, Purebasic, NET and Java. They can be
found `here <http://forum.doom9.org/showthread.php?p=566904#post566904>`__.

...

There are several different Colorspaces in AviSynth. See more information
about :doc:`Color Spaces <ColorSpaces>` and :doc:`Working With Images <WorkingWithImages>`.

What's new in the 2.6 api
-------------------------

- C++ API (AVISYNTH_INTERFACE_VERSION = 6):

    - Plugin api v3 and older contained :doc:`baked code <AVSLinkage>` meaning code
      that is "baked" into all and every plugin instead being called
      from avisynth.dll. Starting from 2.6 the version 2.5 plugins
      are supported directly (with current baked code; meaning that
      plugins compiled for 2.5 can be loaded when using 2.6) and all
      the baked code from 2.6+ plugins is removed and the plugins
      are still source compatible. Note that the baked code is moved
      to interface.cpp, where also the structure :doc:`AVS_Linkage <AVSLinkage>` is
      defined.
    - The :ref:`IScriptEnvironment <cplusplus_iscriptenvironment>` interface has several new members:

        - :ref:`ApplyMessage <cplusplus_applymessage>` writes text on a frame.
        - :ref:`DeleteScriptEnvironment <cplusplus_deletescriptenvironment>` provides a method to delete
          the ScriptEnvironment which is created with
          CreateScriptEnvironment.
        - :ref:`GetAVSLinkage <cplusplus_getavslinkage>` returns the AVSLinkage.
        - :ref:`GetVarDef <cplusplus_getvardef>` can be used to access AviSynth variables.
          It will not throw an error if the variable doesn't exist.

    - It uses size_t for things that are memory sizes, ready for 64 bit port.
    - New colorformats are added: Y8, YV411, YV16 and YV24.
    - :doc:`VideoInfo` has several new constants and functions (the
      ones relating to the new colorformats, the chroma placement
      constants, GetPlaneHeightSubsampling,
      GetPlaneWidthSubsampling).
    - Some new cache and cpu constants for GetCPUFlags (the v5/v6 ones).
    - SetCacheHints changed from void to int.

- C API (AVISYNTH_INTERFACE_VERSION = 6):
    - The following functions are added to the interface:
      avs_is_yv24, avs_is_yv16, avs_is_yv12, avs_is_yv411,
      avs_is_y8, avs_is_color_space,
      avs_get_plane_width_subsampling,
      avs_get_plane_height_subsampling, avs_bits_per_pixel,
      avs_bytes_from_pixels, avs_row_size, avs_bmp_size,
      avs_get_row_size_p, avs_get_height_p and
      avs_delete_script_environment.


Some history
------------

:doc:`Ben's AviSynth Docs <BensAviSynthDocs>` is the documentation written for AviSynth 1.0
by Ben Rudiak-Gould, in its original form.

See more about the modifications for AviSynth 2.5 in the :doc:`AviSynth Two-Five SDK <AviSynthTwoFiveSDK>`.

Please read AviSynth :doc:`SDK History <SDKHistory>`. ---

Other sources ???
-----------------

Once you've got the basics down on AVS development (Ben's text is quite
good), the `[SDK]`_ for VirtualDub is also a good read. Good news is you
won't have to worry about writing `[function pointers]`_ and `[raw Win32]`_;
meanwhile, Avery knows his stuff when it comes to video & CPU optimization
techniques, so you better pay attention.

Some video related ebooks (PDF) can be downloaded freely from `[Snell & Wilcox]`_. edit -
`this`_???

License terms
-------------

Note: Avisynth Filter SDK parts are under specific :doc:`SDK license <SDKLicense>` terms.

$Date: 2015/09/14 20:23:59 $

Latest online mediaWiki version is at http://avisynth.nl/Filter_SDK

.. _[SDK]: http://virtualdub.org/filtersdk
.. _[function pointers]: http://function-pointer.org/
.. _[raw Win32]: http://www.charlespetzold.com/pw5/index.html
.. _[Snell & Wilcox]: http://www.snellwilcox.com/reference.html
.. _[AviSynth Development forum]:
    http://forum.doom9.org/forumdisplay.php?s=&f=69
.. _AVIFile library: http://msdn.microsoft.com/en-us/library/windows/desktop/dd756808(v=vs.85).aspx
.. _[1]: http://forum.doom9.org/showthread.php?t=71493
.. _[2]: http://www.avisynth.info/?%E3%82%A2%E3%83%BC%E3%82%AB%E3%82%A4%E3%83%96#t952b3b1
.. _using the C api: http://komisar.gin.by/tools/avs2yuv/avs2yuv-0.24bm2.zip
.. _using the C++ api: http://kemuri9.net/dev/avs/avs2yuv/avs2yuv.zip
.. _avs2wav: http://forum.doom9.org/showthread.php?p=1502613#post1502613
.. _here: http://forum.doom9.org/showthread.php?p=589781#post589781
.. _avs2pipe: http://forum.doom9.org/showthread.php?t=160383
.. _this: http://www.snellgroup.com/support/documentation/engineering-guides
