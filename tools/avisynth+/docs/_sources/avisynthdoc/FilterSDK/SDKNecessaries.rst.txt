
SDKNecessaries
==============

You must have some compatible development tool
----------------------------------------------

- Microsoft Visual C/C++ 6 (1998), 7.0 (2002), 7.1 (2003), 8 (2005),
  9 (2008), 10 (2010), 11 (2012), or 12 (2013)
- Microsoft Visual C++ Toolkit 2003 (free, try search
  vctoolkitsetup.exe) with some IDE (e.g. free `CodeBlocks`_)
- Microsoft Visual C++ 2005 Express edition (requires W2KSP4; has a
  converter for upgrading VC6 projects)
- Microsoft Visual C++ 2008 Express edition (requires WinXPSP3; has a
  converter for upgrading VC6 projects) (free download [1])
- Microsoft Visual C++ 2010 Express edition (`free download
  <http://www.visualstudio.com/downloads/download-visual-studio-vs#DownloadFamilies_4>`__,
  `direct link`_; requires WinXPSP3)
- Microsoft Visual C++ 2013 Express edition (`free download
  <http://www.visualstudio.com/en-us/downloads/>`__ (web version is fine); requires Win7)
- Intel ICL Compiler v7 (?), up to to ICL10.1

Notes

- Visual C/C++ 6, 7, 7.1 Standard Edition (and NET 1.1 SDK) lack in
  optimizing compiler (only expensive Professional or Enterprise
  Edition included it). As a partial workaround you can add free
  Visual C++ Toolkit 2003 optimizing compiler to your Standard
  Edition IDE (by setting directories properly) or use Visual C++
  2005 (any edition).
- None of the express editions have a resource editor.
- Starting from Express 2012 there is support 64-bit applications.
  For earlier versions it is included in the Platform SDK (?).
- Free registration is mandatory to use this product beyond 30 days.


You also need in Microsoft Platform SDK (if it is not included with compiler)
-----------------------------------------------------------------------------

When using VC6.0, you will need the February 2003 Edition `[5]`_, or
the Windows Server 2003 SP1 Platform SDK edition `[6]`_ `[7]`_.

For MS VC++ 2005 you can use the latest Platform SDK: `[8]`_.

For MS VC++ 2008 or more recent it is included in the compiler (?) (and
it is called Windows PSK).

For some very special plugins (GPU) you might need the DirectX SDK t00
(when compiling AviSynth itself you will need it).


Finally, you must include the small header file 'avisynth.h'
------------------------------------------------------------

You can get it with this FilterSDK, download with AviSynth source code, or
take from some plugin source package. There are several versions of this
header file from various AviSynth versions.

Header file avisynth.h from v1.0.x to v2.0.x have
``AVISYNTH_INTERFACE_VERSION = 1.`` Plugins compiled with them will not be
(natively) compatible with AviSynth 2.5.x.

Header file avisynth.h from v2.5.0 to v2.5.5 have
``AVISYNTH_INTERFACE_VERSION = 2.`` Plugins compiled with them will
(generally) work in AviSynth v2.5.0 to v2.5.7 (and above). But avisynth.h
files from versions v2.5.0 - v2.5.5 (and betas) are not identical. We
recommend to use avisynth.h from versions 2.5.5 or later. Previous versions
of avisynth.h are obsolete and have some bugs.

Header file avisynth.h from v2.5.6 to v2.5.8 are almost identical and have
``AVISYNTH_INTERFACE_VERSION = 3.`` Plugins compliled with them will work in
v2.5.6 and up, and v2.5.5 and below if you do not use new
interface features and do not call ``env->CheckVersion`` function.

Now being developed, AviSynth version 2.6.x will use new header avisynth.h,
currently with ``AVISYNTH_INTERFACE_VERSION = 6.`` Plugins compiled with
AviSynth v2.5.x header will work in AviSynth 2.6.x too, but plugins compiled
with new AviSynth v2.6.x header will probably not work in AviSynth v2.5.x.

Generally good start is to take some similar plugin source code as a draft
for improving or own development. Attention: there are many old plugins
source code packages with older avisynth.h included. Simply replace it by new one.


Compiling options
-----------------

Plugin CPP source code must be compiled as Win32 DLL (multi-threaded or
multi-threaded DLL) without MFC.

Notes. If you use Visual C++ Toolkit 2003 itself (without VC++ 7), you can
not build plugin as multi-treaded DLL: the toolkit missed some libraries, in
particular msvcrt.lib. You can get additional libs with MS .NET 1.1 SDK (free
download) or simply use multi-treaded option (IMHO it is better - no need in
MSVCRT71.DLL).

Of course, use Release build with optimization. Typical compiler switches are
/MT /O2 and /dll /nologo for linker

See step by step :doc:`compiling instructions. <CompilingAvisynthPlugins>`


Other compilers
---------------

Since v2.5.7, AviSynth includes an updated version of Kevin Atkinson's
AviSynth C API you can use to create "C-Plugins" with compilers such as
GNU C++, Visual Basic and Delphi.

You can NOT use the C++ API with compilers like GNU C++ to create
plugins, because of :doc:`binary incompatibilities <CompilingAvisynthPlugins>`.

There is also `Pascal conversion of avisynth_c.h`_ by Myrsloik

Some info about `Using in Visual Basic`_

`PureBasic port of the Avisynth C Interface`_ by Inc

There is also `AvsFilterNet`_ wrapper for Avisynth in .NET (any .NET
language) by SAPikachu, see `discussion`_

----

Back to :doc:`FilterSDK <FilterSDK>`

$Date: 2015/03/30 06:08:10 $

.. _[1]: 
   http://www.google.nl/url?sa=t&rct=j&q=&esrc=s&source=web&cd=1&cad=rja&ved=0CCoQFjAA&url=http://go.microsoft.com/?linkid=7729279&ei=HfWhUuTjL8Og0wW7wYDwBw&usg=AFQjCNEulTGchEeozkLGRH8LZELiTKlC5A&sig2=Mi7Rwn_jNL5Qffi7LiGS3w&bvm=bv.57752919,d.d2k
.. _[5]: http://www.visualstudio.com/en-us/downloads/
.. _[6]: http://social.msdn.microsoft.com/Forums/windowsdesktop/en-US/ad4e4015-6867-4ff1-845e-143e6052834e/windows-platform-sdk-feb-2003?forum=windowssdk
.. _[7]: http://www.microsoft.com/en-us/download/details.aspx?id=15656
.. _[8]: http://download.cnet.com/Windows-Server-2003-R2-Platform-SDK-ISO-Download/3000-10248_4-10731094.html
.. _CodeBlocks: http://www.codeblocks.org
.. _Microsoft site: http://www.microsoft.com/downloads/details.aspx?familyid=EBA0128F-A770-45F1-86F3-7AB010B398A3&displaylang=en
.. _Pascal conversion of avisynth_c.h:
    http://forum.doom9.org/showthread.php?t=98327
.. _Using in Visual Basic: http://forum.doom9.org/showthread.php?t=125370
.. _PureBasic port of the Avisynth C Interface:
    http://forum.doom9.org/showthread.php?t=126530
.. _AvsFilterNet: http://www.codeplex.com/AvsFilterNet
.. _discussion: http://forum.doom9.org/showthread.php?t=144663
.. _direct link: http://go.microsoft.com/?linkid=9709949
