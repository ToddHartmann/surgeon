# Surgeon

* Mangle [Surge](https://surge-synthesizer.github.io/) patches
* Change parameters and their attributes
* Set and remove Modulation Routings
* Goof around with Step Sequences
* Much danger

You can edit extracted XML with [XML Notepad](https://github.com/microsoft/xmlnotepad) (Windows)
or [QXmlEdit](https://github.com/lbellonda/qxmledit) (cross-platform).

## Example
<pre>surgeon -o seq.fxp "Init Saw.fxp" -m a_osc1_pitch lfo0 7.0 -p a_lfo0_shape 7 -s A lfo0 s1 0.25 -s A lfo0 s3 -0.25 -s A lfo0 loop_end 3</pre>

Starting with a copy of "Init Saw.fxp" and saving to "seq.fxp" the above does the following (all in Scene A):

<pre>-m a_osc1_pitch lfo0 7.0</pre>Adds a modulation routing from voice LFO1 to OSC1's pitch with a depth of 7.0 (from center to top of range).

<pre>-p a_lfo0_shape 7</pre>Sets LFO1 to Step Seq.

<pre>-s A 0 s1 0.25 -s A 0 s3 -0.25 -s A 0 loop_end 3</pre>Gives LFO1 a silly litle sequence to play.

## The Help
<pre>
surgeon.py [-h] [-o <b>OUTPUT</b>] [-n <b>NAME</b>] [-ca <b>CATEGORY</b>] [-co <b>COMMENT</b>]
           [-a <b>AUTHOR</b>] [-x [<b>OUTXML</b>]] [-ix <b>INXML</b>] [-w [<b>OUTWAV</b>]]
           [-p <b>NAME</b> <b>VALUE</b>] [-t <b>NAME</b> <b>ATTRIB</b> <b>VALUE</b>]
           [-m <b>NAME</b> <b>SOURCE</b> <b>DEPTH</b>] [-s <b>SCENE</b> <b>INDEX</b> <b>ATTRIB</b> <b>VALUE</b>]
           [-cc <b>INDEX</b> <b>BIPOLAR</b> <b>VALUE</b> <b>LABEL</b>]
           <b>INPUT</b>

Operate on Surge patch files, extract wavetables, export and import
XML. Version 1.0.5.

  <b>INPUT</b>                                 input patch file name
  -h, --help                            show this help message and exit
  -o  <b>OUTPUT</b>, --output <b>OUTPUT</b>           applies any changes and saves to <b>OUTPUT</b>
  -n  <b>NAME</b>, --name <b>NAME</b>                 new name for patch
  -ca <b>CATEGORY</b>, --category <b>CATEGORY</b>     new category for patch
  -co <b>COMMENT</b>, --comment <b>COMMENT</b>        new comment for patch
  -a  <b>AUTHOR</b>, --author <b>AUTHOR</b>           new author for patch
  -x [<b>OUTXML</b>], --xml [<b>OUTXML</b>]           save XML from <b>INPUT</b> to <b>OUTXML</b>
  -ix <b>INXML</b>, --inxml <b>INXML</b>              read new XML from <b>INXML</b>
  -w [<b>OUTWAV</b>], --wav [<b>OUTWAV</b>]           save waves
  -p  <b>NAME</b> <b>VALUE</b>, --param <b>NAME</b> <b>VALUE</b>    set <b>NAME</b>d parameter to <b>VALUE</b>
  -t  <b>NAME</b> <b>ATTRIB</b> <b>VALUE</b>,
  --attrib <b>NAME</b> <b>ATTRIB</b> <b>VALUE</b>            set <b>ATTRIB</b>ute of <b>NAME</b>d parameter to <b>VALUE</b>
  -m  <b>NAME</b> <b>SOURCE</b> <b>DEPTH</b>,
  --modroute <b>NAME</b> <b>SOURCE</b> <b>DEPTH</b>          set modulation routing for <b>NAME</b>d parameter
  -s  <b>SCENE</b> <b>INDEX</b> <b>ATTRIB</b> <b>VALUE</b>,
  --sequence <b>SCENE</b> <b>INDEX</b> <b>ATTRIB</b> <b>VALUE</b>   set <b>ATTRIB</b>ute of sequence
  -cc <b>INDEX</b> <b>BIPOLAR</b> <b>VALUE</b> <b>LABEL</b>,
  --control <b>INDEX</b> <b>BIPOLAR</b> <b>VALUE</b> <b>LABEL</b>   set <b>INDEX</b>ed controller's state</pre>

If <b>OUTPUT</b> equals <b>INPUT</b>, it will *overwrite* <b>INPUT</b>.
All <b>OUTPUT</b> from -o will have slightly altered XML, and certain errors
will be silently ignored. -x will save unaltered XML from the <b>INPUT</b>
file.

-x and -w used without file names will base them on <b>OUTPUT</b>, if
present, <b>INPUT</b> otherwise.
-w adds the Surge metadata chunk, so the .WAV can be dragged in to
Surge or a user wavetable directory.
-ix reads new XML from <b>INXML</b>, and will apply any changes before
writing <b>OUTPUT</b>. You can use -x with -ix.

-p, -t, -m, -s and -cc may be used multiple times.

-p and -t will replace a <b>VALUE</b> of True with 1 as Surge expects.

Upon a <b>VALUE</b> of False, -t will *remove* the attribute as Surge
expects.

Upon a <b>DEPTH</b> of None, -m will *remove* the routing.

Upon a <b>SOURCE</b> of None, -m will *remove all* routing from the
parameter.

Upon a <b>VALUE</b> of None, -s will *remove* the attribute.

Upon an <b>ATTRIB</b> of None, -s will *remove* the sequence.

With -cc, use None to leave <b>BIPOLAR</b>, <b>VALUE</b>, or <b>LABEL</b> unmodified. (This
means you cannot set <b>LABEL</b> to 'None' with this tool.)

You can use these names for the <b>SOURCE</b> of -m:

original, velocity, keytrack, polyaftertouch, aftertouch, pitchbend,
modwheel, ctrl1, ctrl2, ctrl3, ctrl4, ctrl5, ctrl6, ctrl7, ctrl8,
ampeg, filtereg, lfo0, lfo1, lfo2, lfo3, lfo4, lfo5, slfo0, slfo1,
slfo2, slfo3, slfo4, slfo5, timbre, releasevelocity

You can use these names for the <b>INDEX</b> of -s:

lfo0, lfo1, lfo2, lfo3, lfo4, lfo5, slfo0, slfo1, slfo2, slfo3, slfo4,
slfo5

You can use these names for the <b>INDEX</b> of -cc:

ctrl1, ctrl2, ctrl3, ctrl4, ctrl5, ctrl6, ctrl7, ctrl8

There are no checks on any values. Use at your own risk.