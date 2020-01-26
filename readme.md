# Surgeon

* Mangle patches.
* Much danger.

<pre>
usage: surgeon.py [-h] [-o <b>OUTPUT</b>] [-n <b>NAME</b>] [-ca <b>CATEGORY</b>] [-co <b>COMMENT</b>]
                  [-a <b>AUTHOR</b>] [-x [<b>OUTXML</b>]] [-ix <b>INXML</b>] [-w [<b>OUTWAV</b>]]
                  [-p <b>NAME</b> <b>VALUE</b>] [-cc <b>INDEX</b> <b>BIPOLAR</b> <b>VALUE</b> <b>LABEL</b>]
                  <b>INPUT</b>

Operate on Surge patch files, extract wavetables and XML.

  <b>INPUT</b>                                input patch file name

  -h, --help                           show this help message and exit
  -o <b>OUTPUT</b>, --output <b>OUTPUT</b>           output patch file name
  -n <b>NAME</b>, --name <b>NAME</b>                 new name for patch
  -ca <b>CATEGORY</b>, --category <b>CATEGORY</b>    new category for patch
  -co <b>COMMENT</b>, --comment <b>COMMENT</b>       new comment for patch
  -a <b>AUTHOR</b>, --author <b>AUTHOR</b>           new author for patch
  -x [<b>OUTXML</b>], --xml [<b>OUTXML</b>]          XML output file name
  -ix <b>INXML</b>, --inxml <b>INXML</b>             read new XML from <b>INXML</b>
  -w [<b>OUTWAV</b>], --wav [<b>OUTWAV</b>]          beginning for names of .WAV files
  -p <b>NAME</b> <b>VALUE</b>, --param <b>NAME</b> <b>VALUE</b>    set <b>NAME</b>d parameter to <b>VALUE</b>
  -cc <b>INDEX</b> <b>BIPOLAR</b> <b>VALUE</b> <b>LABEL</b>,
  --control <b>INDEX</b> <b>BIPOLAR</b> <b>VALUE</b> <b>LABEL</b>  set custom controller state

If <b>OUTPUT</b> equals <b>INPUT</b>, it will *overwrite* <b>INPUT</b>.

All <b>OUTPUT</b> from -o will have slightly altered XML. -x will save
unaltered XML from the <b>INPUT</b> file.

-x and -w used without file names will base them on <b>OUTPUT</b>, if
present, <b>INPUT</b> otherwise.

-w adds the Surge metadata chunk, so the .WAV can be dragged in to
Surge or a user wavetable directory.

-p and -cc may be used multiple times.

With -cc, use 'None' (without quotes) to leave <b>BIPOLAR</b>, <b>VALUE</b>, or
<b>LABEL</b> unmodified. (This means you cannot set <b>LABEL</b> to 'None' with this
tool.)

-ix reads new XML from <b>INXML</b>, and will apply any changes before
writing <b>OUTPUT</b>. You can use -x with -ix: -x will save the XML from
<b>INPUT</b> in all cases.

There are no checks on any values. Use at your own risk.
</pre>