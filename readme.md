# Surgeon

* Mangle [Surge](https://surge-synthesizer.github.io/) patches
* Change parameters and their attributes
* Set and remove Modulation Routings
* Much danger

You can edit extracted XML with [XML Notepad](https://github.com/microsoft/xmlnotepad) (Windows)
or [QXmlEdit](https://github.com/lbellonda/qxmledit) (cross-platform).

<pre>
usage: surgeon.py [-h] [-o <b>OUTPUT</b>] [-n <b>NAME</b>] [-ca <b>CATEGORY</b>] [-co <b>COMMENT</b>]
                  [-a <b>AUTHOR</b>] [-x [<b>OUTXML</b>]] [-ix <b>INXML</b>] [-w [<b>OUTWAV</b>]]
                  [-p <b>NAME</b> <b>VALUE</b>] [-t <b>PARAM</b> <b>ATTRIB</b> <b>VALUE</b>]
                  [-m <b>PARAM</b> <b>SOURCE</b> <b>DEPTH</b>] [-cc <b>INDEX</b> <b>BIPOLAR</b> <b>VALUE</b> <b>LABEL</b>]
                  <b>INPUT</b>

Operate on Surge patch files, extract wavetables, export and import
XML. Version 1.0.3.

  <b>INPUT</b>                                 input patch file name

  -h, --help                            show this help message and exit
  -o  <b>OUTPUT</b>, --output <b>OUTPUT</b>           output patch file name
  -n  <b>NAME</b>, --name <b>NAME</b>                 new name for patch
  -ca <b>CATEGORY</b>, --category <b>CATEGORY</b>     new category for patch
  -co <b>COMMENT</b>, --comment <b>COMMENT</b>        new comment for patch
  -a  <b>AUTHOR</b>, --author <b>AUTHOR</b>           new author for patch
  -x  [<b>OUTXML</b>], --xml [<b>OUTXML</b>]          XML output file name
  -ix <b>INXML</b>, --inxml <b>INXML</b>              read new XML from <b>INXML</b>
  -w  [<b>OUTWAV</b>], --wav [<b>OUTWAV</b>]          beginning for names of .WAV files
  -p  <b>NAME</b> <b>VALUE</b>,
  --param <b>NAME</b> <b>VALUE</b>                    set <b>NAME</b>d parameter to <b>VALUE</b>
  -t  <b>PARAM</b> <b>ATTRIB</b> <b>VALUE</b>,
  --attrib <b>PARAM</b> <b>ATTRIB</b> <b>VALUE</b>           set <b>ATTRIB</b>ute of <b>PARAM</b>eter to <b>VALUE</b>
  -m  <b>PARAM</b> <b>SOURCE</b> <b>DEPTH</b>,
  --modroute <b>PARAM</b> <b>SOURCE</b> <b>DEPTH</b>         add or remove (<b>DEPTH</b>=None) modulation routing
  -cc <b>INDEX</b> <b>BIPOLAR</b> <b>VALUE</b> <b>LABEL</b>,
  --control <b>INDEX</b> <b>BIPOLAR</b> <b>VALUE</b> <b>LABEL</b>   set <b>INDEX</b>ed controller's state
</pre>
If <b>OUTPUT</b> equals <b>INPUT</b>, it will *overwrite* <b>INPUT</b>.

All <b>OUTPUT</b> from -o will have slightly altered XML, and certain errors
will be silently ignored. -x will save unaltered XML from the <b>INPUT</b>
file.

-x and -w used without file names will base them on <b>OUTPUT</b>, if
present, <b>INPUT</b> otherwise.

-w adds the Surge metadata chunk, so the .WAV can be dragged in to
Surge or a user wavetable directory.

-p, -t, -m and -cc may be used multiple times.

-p and -t will replace a <b>VALUE</b> of True with 1 as Surge expects.
Upon a <b>VALUE</b> of False, -t will *remove* the attribute as Surge
expects. Upon a <b>DEPTH</b> of None, -m will *remove* the routing.

With -cc, use None to leave <b>BIPOLAR</b>, <b>VALUE</b>, or
<b>LABEL</b> unmodified. (This means you cannot set <b>LABEL</b> to 'None' with this
tool.)

-ix reads new XML from <b>INXML</b>, and will apply any changes before
writing <b>OUTPUT</b>. You can use -x with -ix: -x will save the XML from
<b>INPUT</b> in all cases, even if it has errors.

There are no checks on any values. Use at your own risk.
