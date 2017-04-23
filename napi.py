#!/usr/bin/env python2
#
# Copyright (C) 2013 Damian Gorlach
# Optimization, conversion to UTF-8 added, conversion to subrip format added.
#
# Copyright (C) 2010 Bartosz SKOWRON.
#
# Author: Bartosz SKOWRON <getxsick at gmail dot com>
#
# convert() is based on reversed napi 0.16.3.1 application without any license
#
# Requirements: 7z (p7zip-full on Debian system), iconv, file
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.


import hashlib, urllib
import sys, os, os.path
from shutil import copy2 as copyfile
from glob import glob
from optparse import OptionParser
from tempfile import NamedTemporaryFile
import subprocess

FILE_FORMATS = ['avi', 'mpg', 'mpeg', 'mp4', 'rmvb', 'mkv', 'mov', 'wmv',]

def convert(z):
    idx = [ 0xe, 0x3,  0x6, 0x8, 0x2 ]
    mul = [   2,   2,    5,   4,   3 ]
    add = [   0, 0xd, 0x10, 0xb, 0x5 ]

    b = []
    for i in xrange(len(idx)):
        a = add[i]
        m = mul[i]
        i = idx[i]

        t = a + int(z[i], 16)
        v = int(z[t:t+2], 16)
        b.append( ("%x" % (v*m))[-1] )

    return ''.join(b)

def split_fn_ext(filename):
    """
    Return tuple of directory and filename and extenstion.
    """
    l = filename.rpartition('.')
    d = filename.rpartition('/')
    l = d[2].rpartition('.')
    di = ''
    if d[0] == '':
        di = ''
    else:
        di = d[0] + '/'
    return (di, l[0], l[2])

def split_ext(filename):
    """
    Return tuple of filename and extenstion.
    """
    l = filename.rpartition('.')
    return (l[0], l[2])

def gen_hashname(fname):
    hp = split_fn_ext(fname)
    r = hp[0] + '.' + hp[1] + '.hash'
    verbose("hashname: " + r);
    return r

def gen_url(fname):
    hashpath=gen_hashname(fname)
    #message(os.path.basename(hashpath), "hash", 1)
    first_line=""
    if os.path.exists(hashpath):
        verbose("hash exists");
        with open(hashpath, 'r') as f:
            hexdigest = f.readline()
        verbose("cached hash %s" % (hexdigest))
        message(os.path.basename(fname), "Cached hash %s" % (hexdigest), 1)
    else:
        hashsum = hashlib.md5();
        hashsum.update(open(fname).read(10485760))
        hexdigest = hashsum.hexdigest()
        verbose("generated hash: " + hexdigest);
        with open(hashpath, 'w') as f:
            f.write(hexdigest)

    url = "http://napiprojekt.pl/unit_napisy/dl.php?l=PL&f=%s&t=%s&v=other&kolejka=false&nick=&pass=&napios=%s" % (
            hexdigest, convert(hexdigest), os.name)
    verbose("url: " + url);
    return url

def run_command(command):
    verbose("running: [%s]" % ', '.join(map(str, command)));
    p = subprocess.Popen(command,
                         stdout=subprocess.PIPE,
                         stderr=subprocess.STDOUT)
    return iter(p.stdout.readline, b'')

def get_subtitle(fname):
    txtpath=split_ext(fname)[0] + '.txt'
    srtpath=split_ext(fname)[0] + '.srt'
    hashpath=gen_hashname(fname)

    verbose("txtpath: " + txtpath);
    verbose("srtpath: " + srtpath);
    verbose("hashpath: " + hashpath);

    if os.path.exists(txtpath):
        message(os.path.basename(fname), "OK (exists)", 1)
    else:
        message(os.path.basename(fname), "Searching...", 1)
        url = gen_url(fname)
        f_archive7z = NamedTemporaryFile(delete=False)
        verbose("f_archive7z: " + str(f_archive7z));
        f_archive7z.write(urllib.urlopen(url).read())
        f_archive7z.close() # flush buffers
        f_newtxt = NamedTemporaryFile(delete=False)
        verbose("f_newtxt: " + str(f_newtxt));
        f_newtxt.close()

        # XXX Use this when resolved - http://bugs.python.org/issue5689
        if os.system("7z x -y -so -piBlm8NTigvru0Jr0 %s 2>/dev/null >\"%s\"" % (f_archive7z.name, f_newtxt.name)):
            message(os.path.basename(fname), "FAIL", 1)
        else:
            try:
                command = ["file", f_newtxt.name]
                txtype = 0
                for line in run_command(command):
                    if line.find('UTF') > 0:
                        txtype = 1
                verbose("txtype: " + str(txtype))
                if txtype == 0:
                    message(os.path.basename(fname), "Trying to make UTF", 1)
                    f_newtxtu8 = NamedTemporaryFile(delete=False)
                    verbose("f_newtxtu8: " + str(f_newtxtu8));
                    f_newtxtu8.close()
                    os.system("iconv -f windows-1250 -t utf-8 -o %s %s" % (f_newtxtu8.name, f_newtxt.name))
                    verbose("copy " + str(f_newtxtu8.name) + " to " + str(f_newtxt));
                    copyfile(f_newtxtu8.name, f_newtxt.name)
                    os.remove(f_newtxtu8.name)
                if options.subrip:
                    message(os.path.basename(fname), "Trying to make SRT", 1)
                    if 0 != os.system("mplayer -frames 0 -really-quiet -vo null -ao null -subcp utf8 -sub \"%s\" -dumpsrtsub \"%s\"" %(
                        f_newtxt.name, fname)) or 0 != os.system("mv dumpsub.srt \"%s\"" %(srtpath)):
                        message(os.path.basename(fname), "Failed to make SRT", 1)
                verbose("copy " + str(f_newtxt.name) + " to " + str(txtpath));
                copyfile(f_newtxt.name, txtpath)
                os.remove(hashpath)
                message(os.path.basename(fname), "OK", 1)
            except:
                message(os.path.basename(fname), sys.exc_info(), 1)
            finally:
                os.remove(f_archive7z.name)
                os.remove(f_newtxt.name)

def get_files(dirpath):
    def add_file(l, directory, files):
        for f in files:
            path = os.path.join(directory, f)
            if os.path.isfile(path) and split_ext(f)[1].lower() in FILE_FORMATS:
                l.append(path)

    l = []
    if dirpath and os.path.isdir(dirpath):
        os.path.walk(dirpath, add_file, l)
    else:
        message(dirpath, 'NOT FOUND', 0)
    return l

def message(file, message, type):
    if not options.silent:
        if type == 1:
            print("%s - %s" % (file, message))
        else:
            print("%s - %s" % (file, message))

def verbose(message):
    if not options.silent:
        if options.verbose:
            print("> %s" % message)

def which(program):
    import os
    def is_exe(fpath):
        return os.path.isfile(fpath) and os.access(fpath, os.X_OK)

    fpath, fname = os.path.split(program)
    if fpath:
        if is_exe(program):
            return program
    else:
        for path in os.environ["PATH"].split(os.pathsep):
            path = path.strip('"')
            exe_file = os.path.join(path, program)
            if is_exe(exe_file):
                return exe_file

    return None


def needed_software(name):
    verbose("checking " + name)
    if which(name) is None:
        print('You must install %s to use this program.' % (name))
        sys.exit(2)

if __name__=='__main__':
    usage = "usage: %prog [options] FILE1 FILE2 ..."
    parser = OptionParser(usage)
    parser.add_option("-e", "--ext", dest="ext", metavar="EXT1,EXT2",
                      help="follow up additional extensions")
    parser.add_option("-s", "--silent", dest="silent", action="store_true",
                      help="silent mode")
    parser.add_option("-r", "--subrip", dest="subrip", action="store_true",
                      help="use mplayer for generating .srt")
    parser.add_option("-v", "--verbose", dest="verbose", action="store_true",
                      help="be more verbose")
    (options, args) = parser.parse_args()

    if not args:
        parser.print_help()
        sys.exit(1)

    needed_software("iconv")
    needed_software("mplayer")
    needed_software("7z")
    needed_software("mv")

    verbose("options.ext " + str(options.ext));
    verbose("options.subrip " + str(options.subrip));
    verbose("options.silent " + str(options.silent));
    verbose("options.verbose " + str(options.verbose));

    # add new extesions to the list
    if options.ext:
        l = options.ext.split(',')
        FILE_FORMATS.extend([ x.lower() for x in l ])

    # detect dirs
    filelist = []
    for f in args:
        if os.path.isdir(f):
            filelist.extend(get_files(f))
        else:
            filelist.append(f)

    # main action
    for f in filelist:
        if os.path.isfile(f):
            verbose("file " + f);
            get_subtitle(f)
        else:
            message(f, "NOT FOUND", 0)

