# -*- coding: utf-8 -*-

import sys
import os
import shutil
import tempfile
import os
import subprocess
import platform
import re

try:
    from urllib.request import urlopen
except ImportError:
    from urllib import urlopen

DEFAULT_TARGET_FOLDER = {
    "win32": "~\\AppData\\Local\\graphviz",
    "linux": "~/bin",
    "darwin": "~/Applications/graphviz"
}


def _get_graphviz_urls(version="latest"):
    """Get the urls of graphviz's binaries
    Uses sys.platform keys, but removes the 2 from linux2
    Adding a new platform means implementing unpacking in "DownloadgraphvizCommand"
    and adding the URL here

    :param str version: graphviz version.
        Valid values are either a valid graphviz version e.g. "1.19.1", or "latest"
        Default: "latest".

    :return: str graphviz_urls: a dictionary with keys as system platform
        and values as the url pointing to respective binaries

    :return: str version: actual graphviz version. (e.g. "lastest" will be resolved to the actual one)
    """
    graphviz_urls = {}

    for url in [
            'http://www.graphviz.org/Download_macos.php',
            'http://www.graphviz.org/Download_windows.php',
            'http://www.graphviz.org/Download_linux_ubuntu.php',
    ]:

        # read the HTML content
        response = urlopen(url)
        content = response.read()
        # regex for the binaries
        regex = re.compile(r"/pub/graphviz/stable/.*\.(?:msi|deb|pkg)")
        # a list of urls to the bainaries
        graphviz_urls_list = [
            url_frag.split('"')[0]
            for url_frag in regex.findall(content.decode("utf-8"))
        ]
        # actual graphviz version
        version = graphviz_urls_list[0].split('/')[5]
        # dict that lookup the platform from binary extension
        ext2platform = {'msi': 'win32', 'deb': 'linux', 'pkg': 'darwin'}
        # parse graphviz_urls from list to dict
        graphviz_urls.update(
            dict((ext2platform[url_frag[-3:]], ("http://www.graphviz.org" +
                                                url_frag))
                 for url_frag in graphviz_urls_list))

    return graphviz_urls, version


def _make_executable(path):
    mode = os.stat(path).st_mode
    mode |= (mode & 0o444) >> 2  # copy R bits to X
    print("* Making %s executeable..." % (path))
    os.chmod(path, mode)


def _handle_linux(filename, targetfolder):

    print("* Unpacking %s to tempfolder..." % (filename))

    tempfolder = tempfile.mkdtemp()
    cur_wd = os.getcwd()
    filename = os.path.abspath(filename)
    try:
        os.chdir(tempfolder)
        cmd = ["ar", "x", filename]
        # if only 3.5 is supported, should be `run(..., check=True)`
        subprocess.check_call(cmd)
        cmd = ["tar", "xzf", "data.tar.gz"]
        subprocess.check_call(cmd)
        # graphviz and graphviz-citeproc are in ./usr/bin subfolder
        for exe in ["graphviz", "graphviz-citeproc"]:
            src = os.path.join(tempfolder, "usr", "bin", exe)
            dst = os.path.join(targetfolder, exe)
            print("* Copying %s to %s ..." % (exe, targetfolder))
            shutil.copyfile(src, dst)
            _make_executable(dst)
        src = os.path.join(tempfolder, "usr", "share", "doc", "graphviz",
                           "copyright")
        dst = os.path.join(targetfolder, "copyright.graphviz")
        print("* Copying copyright to %s ..." % (targetfolder))
        shutil.copyfile(src, dst)
    finally:
        os.chdir(cur_wd)
        shutil.rmtree(tempfolder)


def _handle_darwin(filename, targetfolder):
    print("* Unpacking %s to tempfolder..." % (filename))

    tempfolder = tempfile.mkdtemp()

    pkgutilfolder = os.path.join(tempfolder, 'tmp')
    cmd = ["pkgutil", "--expand", filename, pkgutilfolder]
    # if only 3.5 is supported, should be `run(..., check=True)`
    subprocess.check_call(cmd)

    # this will generate usr/local/bin below the dir
    cmd = [
        "tar", "xvf", os.path.join(pkgutilfolder, "graphviz.pkg", "Payload"),
        "-C", pkgutilfolder
    ]
    subprocess.check_call(cmd)

    # graphviz and graphviz-citeproc are in the ./usr/local/bin subfolder
    for exe in ["graphviz", "graphviz-citeproc"]:
        src = os.path.join(pkgutilfolder, "usr", "local", "bin", exe)
        dst = os.path.join(targetfolder, exe)
        print("* Copying %s to %s ..." % (exe, targetfolder))
        shutil.copyfile(src, dst)
        _make_executable(dst)

    # remove temporary dir
    shutil.rmtree(tempfolder)
    print("* Done.")


def _handle_win32(filename, targetfolder):
    print("* Unpacking %s to tempfolder..." % (filename))

    tempfolder = tempfile.mkdtemp()

    cmd = ["msiexec", "/a", filename, "/qb", "TARGETDIR=%s" % (tempfolder)]
    # if only 3.5 is supported, should be `run(..., check=True)`
    subprocess.check_call(cmd)

    # graphviz.exe, graphviz-citeproc.exe, and the COPYRIGHT are in the graphviz subfolder
    for exe in os.listdir(os.path.join(tempfolder, "bin")):
        src = os.path.join(tempfolder, "bin", exe)
        dst = os.path.join(targetfolder, exe)
        print("* Copying %s to %s ..." % (exe, targetfolder))
        shutil.copyfile(src, dst)

    # remove temporary dir
    shutil.rmtree(tempfolder)
    print("* Done.")


def download_graphviz(url=None, targetfolder=None, version="latest"):
    """Download and unpack graphviz

    Downloads prebuild binaries for graphviz from `url` and unpacks it into
    `targetfolder`.

    :param str url: URL for the to be downloaded graphviz binary distribution for
        the platform under which this python runs. If no `url` is give, uses
        the latest available release at the time pygraphviz was released.

    :param str targetfolder: directory, where the binaries should be installed
        to. If no `targetfolder` is give, uses a platform specific user
        location: `~/bin` on Linux, `~/Applications/graphviz` on Mac OS X, and
        `~\\AppData\\Local\\graphviz` on Windows.
    """
    # get graphviz_urls
    graphviz_urls, _ = _get_graphviz_urls(version)

    pf = sys.platform

    # compatibility with py3
    if pf.startswith("linux"):
        pf = "linux"
        if platform.architecture()[0] != "64bit":
            raise RuntimeError("Linux graphviz is only compiled for 64bit.")

    if pf not in graphviz_urls:
        raise RuntimeError(
            "Can't handle your platform (only Linux, Mac OS X, Windows).")

    if url is None:
        url = graphviz_urls[pf]

    filename = url.split("/")[-1]
    if os.path.isfile(filename):
        print("* Using already downloaded file %s" % (filename))
    else:
        print("* Downloading graphviz from %s ..." % url)
        # https://stackoverflow.com/questions/30627937/tracebaclk-attributeerroraddinfourl-instance-has-no-attribute-exit
        response = urlopen(url)
        with open(filename, 'wb') as out_file:
            shutil.copyfileobj(response, out_file)

    if targetfolder is None:
        targetfolder = DEFAULT_TARGET_FOLDER[pf]
    targetfolder = os.path.expanduser(targetfolder)

    # Make sure target folder exists...
    try:
        os.makedirs(targetfolder)
    except OSError:
        pass  # dir already exists...

    unpack = globals().get("_handle_" + pf)
    assert unpack is not None, "Can't handle download, only Linux, Windows and OS X are supported."

    unpack(filename, targetfolder)