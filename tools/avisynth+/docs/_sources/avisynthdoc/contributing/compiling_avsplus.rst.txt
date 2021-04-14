
Compiling AviSynth+
===================

This guide uses a command line-based compilation methodology, because
it's easier to provide direct instructions for this that can just be copy/pasted.

`MSys2 <https://msys2.github.io/>`_ and `7zip <http://www.7-zip.org/>`_ should
already be installed, and msys2's bin directory should have been added to Windows'
%PATH% variable.

.. toctree::
    :maxdepth: 3

.. contents:: Table of contents



AviSynth+ prerequisites
-----------------------

AviSynth+ can be built by a few different compilers:

* Visual Studio 2017 or higher.
* Clang 7.0.1 or higher.
* GCC 7 or higher.

| Download and install Visual Studio Community:
| `<https://visualstudio.microsoft.com/downloads/>`_

| Install the latest version of CMake:
| `<http://www.cmake.org/cmake/resources/software.html>`_

After installing MSys2, make sure to enable some convenience functions in MSys2's config files.

In msys.ini:
::

    CHERE_INVOKING=1
    MSYS2_PATH_TYPE=inherit
    MSYSTEM=MSYS

In mingw64.ini:
::

    CHERE_INVOKING=1
    MSYS2_PATH_TYPE=inherit
    MSYSTEM=MINGW64

In mingw32.ini:
::

    CHERE_INVOKING=1
    MSYS2_PATH_TYPE=inherit
    MSYSTEM=MINGW32

Add CMake's bin directory to the system %PATH% manually if the installer won't.
Also add 7zip and upx to the %PATH%.


Building with Visual Studio
---------------------------

For ease of use, we'll also be making use of MSys2 to streamline the build process,
even with the VC++ compiler.


DirectShowSource Prerequisites
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

DirectShowSource requires extra setup that building the AviSynth+ core does not.
DirectShowSource is not a requirement for a working AviSynth+ setup, especially
with the options of using either FFmpegSource2 or LSMASHSource, but the guide
wouldn't be complete otherwise.


C++ Base Classes library
........................

DirectShowSource requires strmbase.lib, the C++ Base Classes library, which for some
reason isn't included in a standard install of Visual Studio.  The source code for
the library is provided with the Windows SDK, and requires the user to build it first.

| Download the Windows SDK 7.1:
| `<http://www.microsoft.com/en-US/download/details.aspx?Id=8442>`_

| Download the following ISO for 32-bit Windows installations:
| GRMSDK_EN_DVD.iso

| Download the following ISO for 64-bit Windows installations:
| GRMSDKX_EN_DVD.iso

The ISO you download is based on the version of Windows you're actually running,
*not* on the Windows installs you're targetting.  Both ISOs include the correct
tools to build for either 32-bit or 64-bit targets.

| Verify the 32-bit ISO against CRC32 or SHA1:
| CRC#: 0xBD8F1237
| SHA1: 0xCDE254E83677C34C8FD509D6B733C32002FE3572

| Verify the 64-bit ISO against CRC32 or SHA1:
| CRC#: 0x04F59E55
| SHA1: 0x9203529F5F70D556A60C37F118A95214E6D10B5A

For convenience (and on computers without an optical drive), you can use either Pismo
File Mount (if you've already got it installed for AVFS) or Windows 10's own Mount option
to mount the ISO to a virtual drive. Then just launch setup.exe and follow the wizard.

Install only the Samples, uncheck everything else.

| Open Visual Studio, and open the .sln file in the 7.1 SDK, at
| ``C:\Program Files\Microsoft SDKs\Windows\v7.1\Samples\multimedia\directshow\baseclasses``

Allow Visual Studio to convert the project, switch the configuration to ``Release``,
and enter the project Properties by right-clicking on the solution name and selecting
``Properties``.

Select the ``Visual Studio 17 - Windows XP (v141_xp)`` option on the main Properties page
under ``Toolset``, and on the ``C/C++ Code Generation`` page select *Disabled* or *SSE*
from the ``Enhanced Instruction Set`` option (IMO, it's safer to disable it for system
support libraries like strmbase.lib), and finally, exit back to the main screen.

Now select ``Build``. That's it.

For 64-bit, change to ``Release x64`` and ``Build``. The SSE2 note isn't relevant here, since
64-bit CPUs are required to have SSE2 support.


Miscellaneous
.............

To make the AviSynth+ build instructions more concise, we'll set a couple of environment
variables.  After starting msys2, open the file /etc/profile in Wordpad:
::

    write /etc/profile

and copy the following three lines into it somewhere:
::

    export STRMBASELIB="C:/Program Files/Microsoft SDKs/Windows/v7.1/Samples/multimedia/directshow/baseclasses/Release/strmbase.lib"
    export STRMBASELIB64="C:/Program Files/Microsoft SDKs/Windows/v7.1/Samples/multimedia/directshow/baseclasses/x64/Release/strmbase.lib"

(64-bit Windows users should use ``Program Files (x86)``, but you probably already knew that ;P)

Thankfully, all of this setup only needs to be done once.


Building AviSynth+
~~~~~~~~~~~~~~~~~~

Start the Visual Studio x86 Native Command Prompt.

You can use Visual Studio's compilers from MSys2 by launching MSys2 from the Visual Studio
Command Prompt. So type 'msys' and hit Enter.

Note: in the instructions below, the ``\`` character means the command spans more than
one line.  Make sure to copy/paste all of the lines in the command.

Download the AviSynth+ source:
::

    git clone -b MT git://github.com/pinterf/AviSynthPlus.git && \
    cd AviSynthPlus

Set up the packaging directory for later:
::

    AVSDIRNAME=avisynth+_r$(git rev-list --count HEAD)-g$(git rev-parse --short HEAD)-$(date --rfc-3339=date | sed 's/-//g') && \
    cd .. && \
    mkdir -p avisynth_build $AVSDIRNAME/32bit/dev $AVSDIRNAME/64bit/dev && \
    cd avisynth_build

Now, we can build AviSynth+.


Using MSBuild
.............

For 32-bit:
::

    cmake ../AviSynthPlus -DBUILD_DIRECTSHOWSOURCE:bool=on && \

    cmake --build . --config Release -j $(nproc)


Copy the .dlls to the packaging directory:
::

    cp Output/AviSynth.dll Output/system/DevIL.dll Output/plugins/* ../$AVSDIRNAME/32bit

Copy the .libs to the packaging directory:
::

    cp avs_core/Release/AviSynth.lib plugins/DirectShowSource/Release/*.lib \
    ../AviSynthPlus/plugins/ImageSeq/lib/DevIL_x86/DevIL.lib plugins/ImageSeq/Release/ImageSeq.lib \
    plugins/Shibatch/PFC/Release/PFC.lib plugins/Shibatch/Release/Shibatch.lib \
    plugins/TimeStretch/Release/TimeStretch.lib plugins/TimeStretch/SoundTouch/Release/SoundTouch.lib \
    plugins/VDubFilter/Release/VDubFilter.lib ../$AVSDIRNAME/32bit/dev


Undo the upx packing on the 32-bit copy of DevIL.dll:
::

    upx -d ../$AVSDIRNAME/32bit/DevIL.dll


For 64-bit:
::

    cmake ../AviSynthPlus -G "Visual Studio 15 2017 Win64" -DBUILD_DIRECTSHOWSOURCE:bool=on && \

    cmake --build . --config Release -j $(nproc)

Copy the .dlls to the packaging directory:
::

    cp Output/AviSynth.dll Output/system/DevIL.dll Output/plugins/* ../$AVSDIRNAME/64bit

Copy the .libs to the packaging directory:
::

    cp avs_core/Release/AviSynth.lib plugins/DirectShowSource/Release/*.lib \
    ../AviSynthPlus/plugins/ImageSeq/lib/DevIL_x64/DevIL.lib plugins/ImageSeq/Release/ImageSeq.lib \
    plugins/Shibatch/PFC/Release/PFC.lib plugins/Shibatch/Release/Shibatch.lib \
    plugins/TimeStretch/Release/TimeStretch.lib plugins/TimeStretch/SoundTouch/Release/SoundTouch.lib \
    plugins/VDubFilter/Release/VDubFilter.lib ../$AVSDIRNAME/64bit/dev


Finishing up
~~~~~~~~~~~~

Packaging up everything can be quickly done with 7-zip:
::

    cd ..
    7z a -mx9 $AVSDIRNAME.7z $AVSDIRNAME


Building with Clang
-------------------

todo


Building with GCC
-----------------

AviSynth+ can be built with GCC two different ways: using MSys2 as a native toolchain,
or cross-compiled under another OS such as a Linux distribution.

Building with GCC in MSys2
~~~~~~~~~~~~~~~~~~~~~~~~~~

Launch MSys2 and install GCC and Ninja:
::

    pacman -S mingw64/mingw-w64-x86_64-gcc gcc mingw64/ninja mingw32/ninja mingw32/mingw-w64-i686-gcc

Grab the AviSynth+ source code:
::

    cd $HOME && \
    git clone -b MT git://github.com/pinterf/AviSynthPlus.git && \
    cd AviSynthPlus && \
    mkdir -p avisynth-build/i686 avisynth-build/amd64

If you were in the MSys2 MSYS prompt, open the MinGW32 prompt, then navigate into
the build directory, build AviSynth+, and install it:
::

    cd $HOME/AviSynthPlus/avisynth-build/i686 && \
        cmake ../../ -G "Ninja" -DCMAKE_INSTALL_PREFIX=$HOME/avisynth+_build/32bit \
        -DBUILD_SHIBATCH:bool=off && \
    ninja && \
    ninja install

(The Shibatch plugin currently has issues on GCC, so disable it for now.
DirectShowSource also has issues, but it doesn't get built by default.)

Open the MinGW64 prompt now, navigate into the build directory, build AviSynth+, and install it:
::

    cd $HOME/AviSynthPlus && \
    AVSDIRNAME=avisynth+_r$(git rev-list --count HEAD)-g$(git rev-parse --short HEAD)-$(date --rfc-3339=date | sed 's/-//g') && \
    cd avisynth-build/amd64 && \
        cmake ../../ -G "Ninja" -DCMAKE_INSTALL_PREFIX=$HOME/avisynth+_build/64bit \
        -DBUILD_SHIBATCH:bool=off && \
    ninja && \
    ninja install

(The Shibatch plugin currently has issues on GCC, so disable it for now.
DirectShowSource also has issues, but it doesn't get built by default.)


Finishing up
............

Now, without leaving the MinGW64 prompt, package the binaries up in a 7zip archive:
::

    mv $HOME/avisynth+_build $HOME/$AVSDIRNAME && \
    7za a -mx9 ~/$AVSDIRNAME.7z ~/$AVSDIRNAME


Cross-compiling with GCC
~~~~~~~~~~~~~~~~~~~~~~~~

For ease of explanation, we'll assume Ubuntu Linux.  The method to cross-compile under
most distributions is largely the same, so don't worry about that.

Ubuntu's repositories lag behind upstream GCC releases, and my current build
instructions are built around a most-recent-stable version of GCC and MinGW.
The full instructions for that are contained in the first section of
`<https://github.com/qyot27/mpv/blob/extra-new/DOCS/crosscompile-mingw-tedious.txt>`_

Download the source code and prepare the build directories:
::

    git clone -b MT git://github.com/pinterf/AviSynthPlus.git && \
    cd AviSynthPlus && \
    mkdir -p avisynth-build/i686 avisynth-build/amd64 && \
    AVSDIRNAME=avisynth+-gcc_r$(git rev-list --count HEAD)-g$(git rev-parse --short HEAD)-$(date --rfc-3339=date | sed 's/-//g') && \

32-bit:
::

    cd avisynth-build/i686 && \
        cmake ../../ -G "Ninja" -DCMAKE_INSTALL_PREFIX=$HOME/avisynth+_build/32bit \
        -DCMAKE_TOOLCHAIN_FILE="/usr/x86_64-w64-mingw32/toolchain-x86_64-w64-mingw32.cmake" \
        -DCMAKE_C_FLAGS="-m32" -DCMAKE_CXX_FLAGS="-m32" -DCMAKE_RC_FLAGS="-F pe-i386" \
        -DBUILD_SHIBATCH:bool=off && \
    ninja && \
    ninja install

64-bit:
::

    cd ../amd64 && \
        cmake ../../ -G "Ninja" -DCMAKE_INSTALL_PREFIX=$HOME/avisynth+_build/64bit \
        -DCMAKE_TOOLCHAIN_FILE="/usr/x86_64-w64-mingw32/toolchain-x86_64-w64-mingw32.cmake" \
        -DBUILD_SHIBATCH:bool=off && \
    ninja && \
    ninja install


Finishing up
............

Packaging:
::

    mv $HOME/avisynth+_build $HOME/$AVSDIRNAME
    7za a -mx9 ~/$AVSDIRNAME.7z ~/$AVSDIRNAME


Back to the :doc:`main page <../../index>`

$ Date: 2019-04-11 21:48:49 -04:00 $
