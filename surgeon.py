# -*- coding: utf-8 -*-
# Todd wrote this for the Surge synth project and places it in the public domain.
__version__ = '1.0.5'

import io, argparse, wave, struct, chunk, textwrap
import sys
from enum import Enum
from itertools import product
import os.path as path
import xml.etree.ElementTree as ET

sys.tracebacklimit = None   # kludgey solution to uselessly long stack traces

def dprint(stringy):
    """Debug print"""
#    print(stringy)
    pass

def pprint(stringy):
    """Progress print"""
    print(stringy)
    pass

# A metaclass that provides a simple Read-Only Memory for static
# data (like #defines) with slick ClassName.whatever dot access.
# Looks for a value in a class's "__rom__" Enum (must have that name)
# before looking in the rest of the class.  Enum provides immutability.

class metarom(type):
    def __getattribute__(self, name):
        dat = object.__getattribute__(self, '__rom__')
        if name in dat.__members__.keys():
            return dat[name].value
        else:
            return object.__getattribute__(self, name)

def littleEndBytes32(intval):
    """Make 4 bytes of intval as little-endian"""
    return intval.to_bytes(4, 'little')

# adapted from patch-tool.py --

# Class that holds the "Leader" of the .FXP, from the start
# of the patch file up to the XML part (bytes 0x00 through 0x5C):
class Leader(dict, metaclass=metarom):
    class __rom__(Enum):
        beNames = """ chunkmagic byteSize fxMagic version fxId
                        fxVersion numPrograms prgName chunkSize """.split()
        beFormat = '>4si4siiii28si'

        leNames = """sub3 xmlSize wA1 wA2 wA3 wB1 wB2 wB3""".split()
        leFormat = '<4siiiiiii'

        xmlOfs = 0x5C   # where the XML starts
        sub3Ofs = 0x3C  # little-endian sub3 chunk
        sub3size = xmlOfs - sub3Ofs

    def __init__(self, filelike):
        byteslike = filelike.read(Leader.xmlOfs)
        unpacked = struct.unpack(Leader.beFormat, byteslike[:Leader.sub3Ofs])
        for name, val in zip(Leader.beNames, unpacked):
            self[name] = val

        unpacked = struct.unpack(Leader.leFormat, byteslike[Leader.sub3Ofs:])
        for name, val in zip(Leader.leNames, unpacked):
            self[name] = val

    def bytes(self):
        topack = tuple([self[n] for n in Leader.beNames])
        bePart = struct.pack(Leader.beFormat, *topack)

        topack = tuple([self[n] for n in Leader.leNames])
        lePart = struct.pack(Leader.leFormat, *topack)

        return bePart + lePart

# adapted from add-surge-metadata.py --

# Instantiate with BytesIO bytesIO and the wave size
# (from WaveData.getSizeWav(), you know - what you
# tell add-surge-metadata-py with the -s size argument)
class Surger(bytearray, metaclass=metarom):
    class __rom__(Enum):
        # offsets of fields in RIFF chunk of WAV output file
        fileSizeOfs = 0x04  # file size field aka "chunkSize"
        waveOfs     = 0x08  # offset of "WAVE" ; chunkSize = from here to EOF
        riffSkip    = 0x0C  # to skip the RIFF - tag, size, and format

    """Add metadatada into a new patch"""
    def __init__(self, bytesIO, tablesize):
        super().__init__()
        finalpos = self.fmtEnd(bytesIO)
        bdata = bytesIO.getvalue()

        self += bdata[:finalpos]
        self += self.make_surge_chunk(tablesize)
        self += bdata[finalpos:]

        # fix up file size field
        self.setFileSize()

    def setFileSize(self):
        self[Surger.fileSizeOfs : Surger.fileSizeOfs + 4] = \
            littleEndBytes32(len(self) - Surger.waveOfs)

# make the Surge metadata chunk
    def make_surge_chunk(self, tablesize):
        newck = bytearray()
        newck += b'srge'                        # Surge metadata chunk tag
        newck += littleEndBytes32(8)            # chunk data size = 8
        newck += littleEndBytes32(1)            # Surge chunk version = 1
        newck += littleEndBytes32(tablesize)    # size of each wave table cycle
        dprint('Surge Chunk {} : {}'.format(len(newck), newck))
        return newck

# find the end of the fmt chunk
    def fmtEnd(self, bytesIO):
        bytesIO.seek(Surger.riffSkip)       # skip RIFF tag, size, format fields
        cc = chunk.Chunk(bytesIO, bigendian=False)  # tee up first RIFF sub-chunk
        cn = b''
        while cn != b'fmt ':        # until we've traversed the 'fmt ' chunk:
            cn = cc.getname()       # remember name of chunk
            cc.close()              # advance to next chunk (its tag, not size or data)
            pos = bytesIO.tell()    # remember where next chunk begins

        return pos
#
class WaveData(object, metaclass=metarom):
    class __rom__(Enum):
        sizeWavHdr = 0x0C   # size of the header between XML and PCM

    def __init__(self, view):
        (self.u1, self.sizeWav, self.numWav, self.u2) = struct.unpack('<iihh', view[:WaveData.sizeWavHdr])
        self.pcm = view[WaveData.sizeWavHdr:]
#
def getparts(infile):
    """Get the three parts of the patch file -
       Leader leader, bytes XML, and bytes wavetable (may be empty)"""

    dprint('Attempting patch read from {0}'.format(path.abspath(infile)))
    leader = bxml = wavey = None
    with open(infile, 'rb') as pf:
        leader = Leader(pf)

        pxsize = leader['xmlSize'] #leader.getXMLSize()
        bxml = pf.read(pxsize)      # XML as bytes
        dprint('End of XML: 0x{:04X}'.format(pf.tell()))

        wavey = pf.read()    # anything else, if any
    pprint('Patch read from {0}'.format(path.abspath(infile)))
    return leader, bxml, wavey
#
def splitFixExt(basename, desired):
    root, extn = path.splitext(basename)
    if extn.lower() != desired:             # fix if not .WAV or .wav or .WaV...
        extn = desired
    return root, extn
#
def writeparts(basename, leader, newxml, wavey):
    """Write the three parts to a file -
       string file name, bytes leader, bytes newxml, bytes wavey"""

    outfile = ''.join(splitFixExt(basename, '.fxp'))
    dprint('Attempting patch write to {0}'.format(path.abspath(outfile)))
    with open(outfile, 'wb') as nf:
        nf.write(leader)
        nf.write(newxml)
        nf.write(wavey)
    pprint('Patch written to {0}'.format(path.abspath(outfile)))
#
oscNames = [''.join(x) for x in product('AB','123')]  # A1,A2…B3
#
def writeAllWavs(basename, leader, wavey):
    root, extn = splitFixExt(basename, '.wav')

    waview = memoryview(wavey)      # no unnecessary copying
    pos = 0 # offset into wavey/waview
    for osc in range(6):
        size = leader['w{}'.format(oscNames[osc])]
        dprint('wavdat size osc {} = {}'.format(osc, size))
        if size > 0:
            wavdat = WaveData(waview[pos : pos + size])
            pos += size

            sizwav = wavdat.sizeWav
            numwav = wavdat.numWav
            dprint("Number Waves: {}  Size Waves: {}".format(numwav, sizwav))

            # write WAV file into a BytesIO() so we can add_surge_chunk() to it
            bio = io.BytesIO()
            with wave.open(bio, 'wb') as ow:
                ow.setnchannels(1)      # mono
                ow.setsampwidth(2)      # 16-bit
                ow.setframerate(44100)  # in Wavetable Land this does not matter
                ow.writeframes(wavdat.pcm)  # the PCM itself
                dprint("Nframes expected: {}  Nframes actual: {}".format(sizwav*numwav, ow.getnframes()))

            surged = Surger(bio, sizwav)  # make a new one since bio is non-insertable

            wavname = '{}-{}-{}x{}{}'.format(root, oscNames[osc], numwav, sizwav, extn)
            dprint('Attempting wavetable write to {0}'.format(path.abspath(wavname)))
            with open(wavname, 'wb') as f:
                f.write(surged)
            pprint('Wavetable written to {0}'.format(path.abspath(wavname)))

def writeXML(basename, bxml):
    """string file name, bytes xml"""
    xmlname = ''.join(splitFixExt(basename, '.xml'))
    dprint('Attempting XML write to {0}'.format(path.abspath(xmlname)))
    with open(xmlname, 'wb') as xf:
        xf.write(bxml)
    pprint('XML written to {0}'.format(path.abspath(xmlname)))

def setMetas(args, root):
    meta = root.find('meta')
    for attr in ('name', 'category', 'comment', 'author'):
        if args.__getattribute__(attr):
            meta.set(attr, args.__getattribute__(attr))
            pprint('Meta {0} set to {1}'.format(attr, meta.get(attr)))

# <a_osc1_pitch type="2" value="0.000000" extend_range="1" absolute="1" />

def setAttrib(xroot, pname, aname, value):
    parameters = xroot.find('parameters')
    param = parameters.find(pname)
    if param != None:
        if value == 'True':
            param.set(aname, '1')
        elif value == 'False' and aname != 'value':     # don't delete 'value' attributes
            param.attrib.pop(aname, None)
        else:
            param.set(aname, value)

        if value == 'False' and aname != 'value':
            pprint('Removed attribute {0} of parameter {1}'.format(aname, param.tag))
        else:
            if aname == 'value':
                pprint('Parameter {0} set to {1}'.format(param.tag, param.get('value')))
            else:
                pprint('Attribute {0} of parameter {1} set to {2}'.format(aname, param.tag, param.get(aname)))

def setParameters(args, xroot):
    if args.param:
        for pname, value in args.param:
            setAttrib(xroot, pname, 'value', value)

def setAttributes(args, xroot):
    if args.attrib:
        for pname, aname, value in args.attrib:     # args.attrib is very different from param.attrib
            setAttrib(xroot, pname, aname, value)
#
# From ModulationSource.h
modSources = ['original', 'velocity', 'keytrack', 'polyaftertouch',
              'aftertouch', 'pitchbend', 'modwheel',
              'ctrl1', 'ctrl2', 'ctrl3', 'ctrl4', 'ctrl5', 'ctrl6', 'ctrl7', 'ctrl8',
              'ampeg', 'filtereg',
              'lfo0', 'lfo1', 'lfo2', 'lfo3', 'lfo4', 'lfo5',
              'slfo0', 'slfo1', 'slfo2', 'slfo3', 'slfo4', 'slfo5',
              'timbre', 'releasevelocity']
#
def setRoutings(args, xroot):
    if args.modroute:
        for pname, source, depth in args.modroute:
            if source.lower() in modSources:
                source = str(modSources.index(source.lower()))
            param = xroot.find('/'.join(['parameters', pname]))
            if param != None:
                if source == None:  # remove all routing from this param
                    for routing in param.findall('modrouting'):
                        param.remove(routing)
                    pprint('Removed all mod routing for parameter {0}'.format(pname))
                else:
                    routing = param.find("modrouting[@source='{0}']".format(source))    # Highlander Rule?  (There can be only one routing w/ given source.)
                    if depth == 'None':             # delete the routing if it exists
                        if routing != None:
                            param.remove(routing)
                            pprint('Removed mod route from {0} to {1}'.format(modSources[int(source)], pname))
                    else:
                        if routing == None:                                 # make a new one
                            routing = ET.SubElement(param, 'modrouting', \
                                {'source' : source, 'depth' : depth})
                        else:
                            routing.set('depth', depth)
                        pprint('Set mod route from {0} to {1} with depth {2}'.format(modSources[int(source)], pname, depth))
#
def noneSet(e, n, v):
    if v != 'None':
        e.set(n, v)
#
cusCons = modSources[7:15]
#
def setControllers(args, xroot):
    if args.control:
        for index, bipolar, value, label in args.control:
            if index.lower() in cusCons:
                index = str(cusCons.index(index.lower()))   # oh gosh indexes galore
            iname = cusCons[int(index)]
            bipolar = {'False':'0', 'True':'1'}.get(bipolar, bipolar)

            entry = xroot.find("customcontroller/entry[@i='{0}']".format(index))
            noneSet(entry, 'bipolar', bipolar)
            noneSet(entry, 'v', value)
            noneSet(entry, 'label', label)

            bipname = ['False', 'True'][int(entry.get('bipolar'))]       # nice name for message
            pprint('Controller {0} bipolar={1} v={2} label={3}'.format( \
                iname, bipname, entry.get('v'), entry.get('label')))
#
# <stepsequences>
#   <sequence scene="0" i="0" s0="0.489583" s1="0.489583" s2="0.427083" s3="0.343750" s4="0.343750" s5="0.343750" s6="0.343750" s7="0.343750" s8="0.343750" s9="0.343750" s10="0.385417" s11="0.385417" s12="0.385417" s13="0.385417" s14="0.385417"
#    s15="0.447917" loop_start="0" loop_end="15" shuffle="0.000000" trigmask="4369" />
# </stepsequences>
#
lfos = modSources[17:29]

def setSeqAttrib(xroot, scene, index, aname, avalue):
    scene = {'A':'0', 'B':'1',
             'a':'0', 'b':'1'}.get(scene, scene)    # turn A,B into numbers
    scname = ['A', 'B'][int(scene)]                 # nice name for messages

    if index.lower() in lfos:
        index = str(lfos.index(index.lower()))   # oh gosh indexes galore
    iname = lfos[int(index)]

    stepseqs = xroot.find('stepsequences')
    seq = stepseqs.find("sequence[@scene='{0}'][@i='{1}']".format(scene, index))

    if seq == None:                             # did not find <sequence>
        tribs = { 'scene':scene, 'i':index,
                    'loop_start':'0', 'loop_end':'15', 'shuffle':'0.000000'}
        if index == '0':
            tribs['trigmask'] = '0'
        seq = ET.SubElement(stepseqs, 'sequence', tribs)    # make sequence
        pprint('Created sequence for {0} in scene {1}'.format(iname, scname))

    if aname == 'None':     # delete the sequence
        stepseqs.remove(seq)
        pprint('Removed sequence for {0} in scene {1}'.format(iname, scname))
    else:
        if avalue == 'None':
            seq.attrib.pop(aname, None)
            pprint('Removed attribute {0} in sequence for {1} in scene {2}'.format(aname, iname, scname))
        else:
            seq.set(aname, avalue)
            pprint('Set attribute {0} to {1} in sequence for {2} in scene {3}'.format(aname, avalue, iname, scname))
#
def setSequences(args, xroot):
    if args.sequence:
        for scene, index, aname, avalue in args.sequence:
            setSeqAttrib(xroot, scene, index, aname, avalue)
#
# -x only = 'const'=bool, no -x = 'default'=None, -x whatevs = whatevs
def pickName(argh, inFile, outFile):
    """prefer outFile to inFile, and argh to both"""
    answer = inFile                 # because it is required
    if argh:                        # argh is bool(True) or string whatevs
        if argh == True:            # -x with no name given
            if outFile:
                answer = outFile
        else:                       # -x with name given
            answer = argh           # so use it
    else:                           # argh is None
        if outFile:                 # prefer outFile if given
            answer = outFile

    return answer
#
def fillit(s): return textwrap.fill(' '.join(s.split()))

def parseArgs():
    parser = argparse.ArgumentParser(
        description =   fillit("""Operate on Surge patch files, extract wavetables,
                                  export and import XML.  Version {0}.""".format(__version__)
        ),
        epilog = '\n\n'.join( [fillit(s) for s in [
            """If OUTPUT equals INPUT, it will *overwrite* INPUT.""",
            """All OUTPUT from -o will have slightly altered XML, and certain errors
               will be silently ignored.  -x will save unaltered XML from the INPUT file.""",
            """-x and -w used without file names will base them on OUTPUT, if
               present, INPUT otherwise.""",
            """-w adds the Surge metadata chunk, so the .WAV can be dragged
               in to Surge or a user wavetable directory.""",
            """-ix reads new XML from INXML, and will apply any changes before writing OUTPUT.
               You can use -x with -ix: -x will save the XML from INPUT in all cases,
               even if it has errors.""",
            """-p, -t, -m, -s and -cc may be used multiple times.""",
            """-p and -t will replace a VALUE of True with 1 as Surge expects.""",
            """Upon a VALUE of False, -t will *remove* the attribute as Surge expects.""",
            """Upon a DEPTH of None, -m will *remove* the routing.""",
            """Upon a SOURCE of None, -m will *remove all* routing from the parameter.""",
            """Upon a VALUE of None, -s will *remove* the attribute.""",
            """Upon an ATTRIB of None, -s will *remove* the sequence.""",
            """With -cc, use None to leave BIPOLAR, VALUE,
               or LABEL unmodified.  (This means you cannot set LABEL
               to 'None' with this tool.)""",
            """You can use these names for the SOURCE of -m:""",
            ', '.join(modSources),
            """You can use these names for the INDEX of -s:""",
            ', '.join(lfos),
            """You can use these names for the INDEX of -cc:""",
            ', '.join(cusCons),
               """There are no checks on any values.  Use at your own risk."""]]),
        formatter_class=argparse.RawTextHelpFormatter
    )

    parser.add_argument('input', metavar='INPUT', help='input patch file name')
    parser.add_argument('-o',  '--output', metavar='OUTPUT',  help='output patch file name\n ')
    parser.add_argument('-n',  '--name', metavar='NAME', help='new name for patch\n ')
    parser.add_argument('-ca', '--category', metavar='CATEGORY', help='new category for patch\n ')
    parser.add_argument('-co', '--comment', metavar='COMMENT', help='new comment for patch\n ')
    parser.add_argument('-a',  '--author', metavar='AUTHOR', help='new author for patch\n ')
    parser.add_argument('-x',  '--xml', metavar='OUTXML', nargs='?', const=True, default=None, help='XML output file name\n ')
    parser.add_argument('-ix', '--inxml', metavar='INXML', help='read new XML from INXML\n ')
    parser.add_argument('-w',  '--wav', metavar='OUTWAV', nargs='?', const=True, default=None, help='beginning for names of .WAV files\n ')
    parser.add_argument('-p',  '--param', action='append', nargs=2, metavar=('NAME', 'VALUE'),help='set NAMEd parameter to VALUE\n ')
    parser.add_argument('-t',  '--attrib', action = 'append', nargs=3, \
        metavar=('NAME', 'ATTRIB', 'VALUE'), help='set ATTRIBute of NAMEd parameter\n ')
    parser.add_argument('-m',  '--modroute', action='append', nargs=3, \
        metavar=('NAME', 'SOURCE', 'DEPTH'), help='set modulation routing for NAMEd parameter\n ')
    parser.add_argument('-s', '--sequence', action='append', nargs=4, \
        metavar=('SCENE', 'INDEX', 'ATTRIB', 'VALUE'),help="set ATTRIBute of sequence")
    parser.add_argument('-cc', '--control', action='append', nargs=4, \
        metavar=('INDEX', 'BIPOLAR', 'VALUE', 'LABEL'),help="set INDEXed controller's state")
    args = parser.parse_args()
    dprint(args)
    return args
#
def main():
    args = parseArgs()

    leader, bxml, wavey = getparts(args.input)
    pname = leader['prgName']
    ez = pname.find(b'\x00')    # end zero (-1 if not found)
    pprint('Leader prgName is {0}'.format(pname[:ez])) #.decode()))

    if args.xml:
        writeXML(pickName(args.xml, args.input, args.output), bxml)

    if args.wav:
        baseName = pickName(args.wav, args.input, args.output)
        writeAllWavs(baseName, leader, wavey)

    if args.output:
        xroot = None
        if args.inxml:
            xroot = ET.parse(args.inxml).getroot()
            pprint('New XML read from {0}'.format(path.abspath(args.inxml)))
        else:
            sxml = bxml.decode('UTF-8', 'ignore') # XML as str()
            xroot = ET.fromstring(sxml)

        setMetas(args, xroot)
        setParameters(args, xroot)
        setAttributes(args, xroot)
        setRoutings(args, xroot)
        setSequences(args, xroot)
        setControllers(args, xroot)

        if(args.name):
            sn = args.name.encode()
            leader['prgName'] = sn[:28] + b'\00' * (28 - len(sn[:28]))
            pprint('Leader prgName set to {0}'.format(leader['prgName']))

        with io.BytesIO() as newxml:
            tree = ET.ElementTree(xroot)
            tree.write(newxml)
            nbxml = newxml.getvalue()    # get it as bytes()
            xmlSize = len(nbxml)

            leader['xmlSize'] = xmlSize
            leader['chunkSize'] = xmlSize + len(wavey) + Leader.sub3size

            writeparts(args.output, leader.bytes(), nbxml, wavey)

if __name__ == '__main__':
    main()
