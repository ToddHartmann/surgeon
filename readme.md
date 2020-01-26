# Surgeon

* Mangle patches.
* Much danger.

<pre>
usage: surgeon.py [-h] [-o <b>OUTPUT</b>] [-n <b>NAME</b>] [-ca <b>CATEGORY</b>] [-co <b>COMMENT</b>]
                  [-a <b>AUTHOR</b>] [-x [<b>OUTXML</b>]] [-ix <b>INXML</b>] [-w [<b>OUTWAV</b>]]
                  [-p <b>NAME</b> <b>VALUE</b>] [-cc <b>INDEX</b> <b>BIPOLAR</b> <b>VALUE</b> <b>LABEL</b>]
                  <b>INPUT</b>

Operate on Surge patch files, extract wavetables and XML.

  <b>INPUT</b><span style="margin-left:16em">input patch file name</span>

  -h, --help<span style="margin-left:13em"> show this help message and exit</span>
  -o <b>OUTPUT</b>, --output <b>OUTPUT</b><span style="margin-left:5em"> output patch file name</span>
  -n <b>NAME</b>, --name <b>NAME</b><span style="margin-left:8em"> new name for patch</span>
  -ca <b>CATEGORY</b>, --category <b>CATEGORY</b><span style="margin-left:2em">new category for patch</span>
  -co <b>COMMENT</b>, --comment <b>COMMENT</b><span style="margin-left:3em"> new comment for patch</span>
  -a <b>AUTHOR</b>, --author <b>AUTHOR</b><span style="margin-left:5em"> new author for patch</span>
  -x [<b>OUTXML</b>], --xml [<b>OUTXML</b>]<span style="margin-left:5em">XML output file name</span>
  -ix <b>INXML</b>, --inxml <b>INXML</b><span style="margin-left:6em"> read new XML from <b>INXML</b></span>
  -w [<b>OUTWAV</b>], --wav [<b>OUTWAV</b>]<span style="margin-left:5em">beginning for names of .WAV files</span>
  -p <b>NAME</b> <b>VALUE</b>, --param <b>NAME</b> <b>VALUE</b><span style="margin-left:2em">set <b>NAME</b>d parameter to <b>VALUE</b></span>
  -cc <b>INDEX</b> <b>BIPOLAR</b> <b>VALUE</b> <b>LABEL</b>,
  --control <b>INDEX</b> <b>BIPOLAR</b> <b>VALUE</b> <b>LABEL</b><span style="margin-left:1em">set custom controller state</span>

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