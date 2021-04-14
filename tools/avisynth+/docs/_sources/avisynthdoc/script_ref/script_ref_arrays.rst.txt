
Arrays
======

As everybody using Avisynth knows, arrays are not supported natively by the
scripting language.

However, a library named [`AVSLib`_] exists that provides a functional
interface for creating and manipulating arrays. Coupled with Avisynth's OOP
style for calling functions, one can treat arrays as objects with methods,
which is a familiar and easy to understand and code scripting concept.

Therefore, two preparatory steps are needed before being able to create and
manipulate process arrays into your script:

-   [`Download`_] and install the most current version of AVSLib into
    your system.
-   Import the needed AVSLib files in your script as follows (see the
    instructions inside the library's documentation to fill-in the gaps):
-   AVSLib 1.1.x versions: Enter ``LoadPackage("avslib", "array")`` to
    load the array implementation files, or ``LoadLibrary("avslib",
    CONFIG_AVSLIB_FULL)`` to load entire AVSLib.
-   AVSLib 1.0.x versions: Enter an appropriate :doc:`Import <../corefilters/import>` ({path to AVSLib
    header}) statement as the first line of your script.

Now you are ready to create your first array! In order to provide an almost
real case example let's assume the following (which are commonplace in many
situations) about the script you want to create:

-   The script selects a distinct range of frames from each video clip.
-   Some of the input clips may have different size, fps, audio and/or
    colorspace; thus they need to be converted.
-   Some of the filtering parameters are distinct for each clip.

Having done that, let's proceed to the actual code:

First, we create the array; ..1.., ..2.., etc. are actual filename strings.
Clip loading is made by :doc:`AviSource <../corefilters/avisource>` in the example but
:doc:`DirectShowSource <../corefilters/directshowsource>` may also be specified.

::

    inp = ArrayCreate( \
        AviSource(..1..), \
        AviSource(..2..), \
        ... \
        AviSource(..n..) )

Then we convert to same fps, audio, colorspace and size by using
:doc:`AssumeFPS <../corefilters/fps>`, :doc:`ConvertAudioTo16bit <../corefilters/convertaudio>`,
:doc:`ConvertToYV12 <../corefilters/convert>` and :doc:`BilinearResize <../corefilters/resize>`
respectively (or any resizer that you find fit). We use OOP + chaining to
make compact expressions.

Note that since Avisynth does not provide a way for in-place variable
modification we must reassign to an array variable after each array operation
(usually the same).

::

    inp = inp.ArrayOpFunc("AssumeFPS", "24").ArrayOpFunc("ConvertAudioTo16bit" \
        ).ArrayOpFunc("ConvertToYV12").ArrayOpFunc("BilinearResize", "640,480")

To perform trimming we will use arrays of other types also. Below *ts* stands
for first frame to trim, *te* for last; each number corresponds to a clip in
*inp* variable.

::

    ts = ArrayCreate(12, 24, ..., 33) # n numbers in total
    te = ArrayCreate(8540, 7834, ..., 5712) # n numbers in total

We also need a counter to make things easier; we will use ArrayRange to
create an array of 0,1,2,...

::

    cnt = ArrayRange(0, inp.ArrayLen()-1)

In addition we must define a user function that will accept *inp*, *ts*, *te*
and *cnt* and do the trimming.

Since ArrayOpArrayFunc only accepts two arrays for per-element processing, it
is easier to pass 'inp' and *cnt* as array elements and *ts*, *te* as entire
arrays.

::

    Function MyTrim(clip c, int count, string fs, string fe) {
        return c.Trim(fs.ArrayGet(count), fe.ArrayGet(count))
    }

Now we are ready to do the trim (line below).

::

    inp = ArrayOpArrayFunc(inp, cnt, "MyTrim", StrQuote(ts)+","+StrQuote(te))

We will finish the processing with a final tweak on brightness with different
settings on each clip and on hue with same settings for all clips.

::

    bright = ArrayCreate(2.0, 1.5, ..., 3.1) # n numbers in total

    Function MyTweak(clip c, float br) {
        return c.Tweak(bright=br, hue=12.3)
    }

    inp = ArrayOpArrayFunc(inp, bright, "MyTweak")

And now we are ready to combine the results and return them as script's
output. We will use `Dissolve`_ for a smoother transition.

::

    return inp.ArraySum(sum_func="Dissolve", sum_args="5")

This is it; the n input clips have been converted to a common video and audio
format, trimmed and tweaked with individual settings and returned as a single
video stream with only 11 lines of code (excluding comments).

Other types of array processing are also possible (slicing ie operation on a
subset of elements, joining, multiplexing, etc.) but these are topics to be
discussed in other pages. Those that are interested can browse the `AVSLib`_
documentation. One can also take a closer look at the `examples section`_
of the AVSLib documentation.

--------

Back to :doc:`scripting reference <script_ref>`.

$Date: 2008/04/20 19:07:33 $

.. _AVSLib: http://avslib.sourceforge.net/
.. _Download: http://sourceforge.net/projects/avslib/
.. _Dissolve: http://avisynth.org/mediawiki/Dissolve
.. _examples section: http://avslib.sourceforge.net/examples/index.html
