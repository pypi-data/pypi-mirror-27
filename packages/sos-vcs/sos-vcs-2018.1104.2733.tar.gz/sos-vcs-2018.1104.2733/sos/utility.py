#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# __coconut_hash__ = 0x1d6b140

# Compiled with Coconut version 1.3.1 [Dead Parrot]

# Coconut Header: -------------------------------------------------------------

import sys as _coconut_sys, os.path as _coconut_os_path
_coconut_file_path = _coconut_os_path.dirname(_coconut_os_path.abspath(__file__))
_coconut_sys.path.insert(0, _coconut_file_path)
from __coconut__ import _coconut, _coconut_NamedTuple, _coconut_MatchError, _coconut_tail_call, _coconut_tco, _coconut_igetitem, _coconut_base_compose, _coconut_forward_compose, _coconut_back_compose, _coconut_forward_star_compose, _coconut_back_star_compose, _coconut_pipe, _coconut_star_pipe, _coconut_back_pipe, _coconut_back_star_pipe, _coconut_bool_and, _coconut_bool_or, _coconut_none_coalesce, _coconut_minus, _coconut_map, _coconut_partial
from __coconut__ import *
_coconut_sys.path.remove(_coconut_file_path)

# Compiled Coconut: -----------------------------------------------------------

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

# Utiliy functions
import bz2  # line 6
import codecs  # line 6
import difflib  # line 6
import hashlib  # line 6
import logging  # line 6
import os  # line 6
import re  # line 6
sys = _coconut_sys  # line 6
import time  # line 6
try:  # line 7
    from typing import Any  # only required for mypy  # line 8
    from typing import Callable  # only required for mypy  # line 8
    from typing import Dict  # only required for mypy  # line 8
    from typing import FrozenSet  # only required for mypy  # line 8
    from typing import IO  # only required for mypy  # line 8
    from typing import List  # only required for mypy  # line 8
    from typing import Sequence  # only required for mypy  # line 8
    from typing import Tuple  # only required for mypy  # line 8
    from typing import Type  # only required for mypy  # line 8
    from typing import TypeVar  # only required for mypy  # line 8
    from typing import Union  # only required for mypy  # line 8
    Number = Union[int, float]  # line 9
except:  # typing not available (e.g. Python 2)  # line 10
    pass  # typing not available (e.g. Python 2)  # line 10
try:  # line 11
    import wcwidth  # line 11
except:  # optional dependency  # line 12
    pass  # optional dependency  # line 12
longint = eval("long") if sys.version_info.major < 3 else int  # type: Type  # for Python 2 compatibility  # line 13


# Classes
class Accessor(dict):  # line 17
    ''' Dictionary with attribute access. Writing only supported via dictionary access. '''  # line 18
    def __init__(_, mapping: 'Dict[str, Any]') -> 'None':  # line 19
        dict.__init__(_, mapping)  # line 19
    @_coconut_tco  # line 20
    def __getattribute__(_, name: 'str') -> 'Any':  # line 20
        try:  # line 21
            return _[name]  # line 21
        except:  # line 22
            return _coconut_tail_call(dict.__getattribute__, _, name)  # line 22

class Counter:  # line 24
    ''' A simple counter. Can be augmented to return the last value instead. '''  # line 25
    def __init__(_, initial: 'Number'=0) -> 'None':  # line 26
        _.value = initial  # type: Number  # line 26
    def inc(_, by=1) -> 'Number':  # line 27
        _.value += by  # line 27
        return _.value  # line 27

class Logger:  # line 29
    ''' Logger that supports many items. '''  # line 30
    def __init__(_, log):  # line 31
        _._log = log  # line 31
    def debug(_, *s):  # line 32
        _._log.debug(sjoin(*s))  # line 32
    def info(_, *s):  # line 33
        _._log.info(sjoin(*s))  # line 33
    def warn(_, *s):  # line 34
        _._log.warning(sjoin(*s))  # line 34
    def error(_, *s):  # line 35
        _._log.error(sjoin(*s))  # line 35


# Constants
_log = Logger(logging.getLogger(__name__))  # line 39
debug, info, warn, error = _log.debug, _log.info, _log.warn, _log.error  # line 39
UTF8 = "utf_8"  # early used constant, not defined in standard library  # line 40
CONFIGURABLE_FLAGS = ["strict", "track", "picky", "compress"]  # line 41
CONFIGURABLE_LISTS = ["texttype", "bintype", "ignores", "ignoreDirs", "ignoresWhitelist", "ignoreDirsWhitelist"]  # line 42
TRUTH_VALUES = ["true", "yes", "on", "1", "enable", "enabled"]  # all lower-case normalized  # line 43
FALSE_VALUES = ["false", "no", "off", "0", "disable", "disabled"]  # line 44
PROGRESS_MARKER = ["|", "/", "-", "\\"]  # line 45
metaFolder = ".sos"  # type: str  # line 46
metaFile = ".meta"  # type: str  # line 47
bufSize = 1 << 20  # type: int  # 1 MiB  # line 48
SVN = "svn"  # line 49
SLASH = "/"  # line 50
vcsFolders = {".svn": SVN, ".git": "git", ".bzr": "bzr", ".hg": "hg", ".fslckout": "fossil", "_FOSSIL_": "fossil", ".CVS": "cvs"}  # type: Dict[str, str]  # line 51
vcsBranches = {SVN: "trunk", "git": "master", "bzr": "trunk", "hg": "default", "fossil": None, "cvs": None}  # type: Dict[str, _coconut.typing.Optional[str]]  # line 52
lateBinding = Accessor({"verbose": False, "start": 0})  # type: Accessor  # line 53


# Value types
class BranchInfo(_coconut_NamedTuple("BranchInfo", [("number", 'int'), ("ctime", 'int'), ("name", '_coconut.typing.Optional[str]'), ("inSync", 'bool'), ("tracked", 'List[str]')])):  # tracked is a list on purpose, as serialization to JSON needs effort and frequent access is not taking place  # line 57
    __slots__ = ()  # tracked is a list on purpose, as serialization to JSON needs effort and frequent access is not taking place  # line 57
    __ne__ = _coconut.object.__ne__  # tracked is a list on purpose, as serialization to JSON needs effort and frequent access is not taking place  # line 57
    def __new__(_cls, number, ctime, name=None, inSync=False, tracked=[]):  # tracked is a list on purpose, as serialization to JSON needs effort and frequent access is not taking place  # line 57
        return _coconut.tuple.__new__(_cls, (number, ctime, name, inSync, tracked))  # tracked is a list on purpose, as serialization to JSON needs effort and frequent access is not taking place  # line 57
# tracked is a list on purpose, as serialization to JSON needs effort and frequent access is not taking place
class CommitInfo(_coconut_NamedTuple("CommitInfo", [("number", 'int'), ("ctime", 'int'), ("message", '_coconut.typing.Optional[str]')])):  # line 58
    __slots__ = ()  # line 58
    __ne__ = _coconut.object.__ne__  # line 58
    def __new__(_cls, number, ctime, message=None):  # line 58
        return _coconut.tuple.__new__(_cls, (number, ctime, message))  # line 58

class PathInfo(_coconut_NamedTuple("PathInfo", [("nameHash", 'str'), ("size", '_coconut.typing.Optional[int]'), ("mtime", 'int'), ("hash", '_coconut.typing.Optional[str]')])):  # size == None means deleted in this revision  # line 59
    __slots__ = ()  # size == None means deleted in this revision  # line 59
    __ne__ = _coconut.object.__ne__  # size == None means deleted in this revision  # line 59
class ChangeSet(_coconut_NamedTuple("ChangeSet", [("additions", 'Dict[str, PathInfo]'), ("deletions", 'Dict[str, PathInfo]'), ("modifications", 'Dict[str, PathInfo]')])):  # avoid default assignment of {} as it leads to runtime errors (contains data on init for unknown reason)  # line 60
    __slots__ = ()  # avoid default assignment of {} as it leads to runtime errors (contains data on init for unknown reason)  # line 60
    __ne__ = _coconut.object.__ne__  # avoid default assignment of {} as it leads to runtime errors (contains data on init for unknown reason)  # line 60
class Range(_coconut_NamedTuple("Range", [("tipe", 'int'), ("indexes", '_coconut.typing.Sequence[int]')])):  # MergeBlockType[1,2,4], line number, length  # line 61
    __slots__ = ()  # MergeBlockType[1,2,4], line number, length  # line 61
    __ne__ = _coconut.object.__ne__  # MergeBlockType[1,2,4], line number, length  # line 61
class MergeBlock(_coconut_NamedTuple("MergeBlock", [("tipe", 'int'), ("lines", '_coconut.typing.Sequence[str]'), ("line", 'int'), ("replaces", '_coconut.typing.Optional[MergeBlock]'), ("changes", '_coconut.typing.Optional[Range]')])):  # line 62
    __slots__ = ()  # line 62
    __ne__ = _coconut.object.__ne__  # line 62
    def __new__(_cls, tipe, lines, line, replaces=None, changes=None):  # line 62
        return _coconut.tuple.__new__(_cls, (tipe, lines, line, replaces, changes))  # line 62

class GlobBlock(_coconut_NamedTuple("GlobBlock", [("isLiteral", 'bool'), ("content", 'str'), ("index", 'int')])):  # for file pattern rename/move matching  # line 63
    __slots__ = ()  # for file pattern rename/move matching  # line 63
    __ne__ = _coconut.object.__ne__  # for file pattern rename/move matching  # line 63
class GlobBlock2(_coconut_NamedTuple("GlobBlock2", [("isLiteral", 'bool'), ("content", 'str'), ("matches", 'str')])):  # matching file pattern and input filename for translation  # line 64
    __slots__ = ()  # matching file pattern and input filename for translation  # line 64
    __ne__ = _coconut.object.__ne__  # matching file pattern and input filename for translation  # line 64


# Enums
class ConflictResolution:  # prefer their changes, prefer my changes, ask user for each change, go to next deeper level (e.g. from files to lines, characters)  # line 68
    THEIRS, MINE, ASK, NEXT = range(4)  # prefer their changes, prefer my changes, ask user for each change, go to next deeper level (e.g. from files to lines, characters)  # line 68
class MergeOperation:  # insert remote changes into current, remove remote deletions from current, do both (replicate remote state) TODO handle inline-operations separate?  # line 69
    INSERT, REMOVE, BOTH = 1, 2, 3  # insert remote changes into current, remove remote deletions from current, do both (replicate remote state) TODO handle inline-operations separate?  # line 69
class MergeBlockType:  # modify = intra-line changes  # line 70
    KEEP, INSERT, REMOVE, REPLACE, MODIFY, MOVE = range(6)  # modify = intra-line changes  # line 70


# Functions
try:  # line 74
    import chardet  # https://github.com/chardet/chardet  # line 75
    def detectEncoding(binary: 'bytes') -> 'str':  # line 76
        return chardet.detect(binary)["encoding"]  # line 76
except:  # line 77
    def detectEncoding(binary: 'bytes') -> 'str':  # Guess the encoding  # line 78
        ''' Fallback if chardet library missing. '''  # line 79
        try:  # line 80
            binary.decode(UTF8)  # line 80
            return UTF8  # line 80
        except UnicodeError:  # line 81
            pass  # line 81
        try:  # line 82
            binary.decode("utf_16")  # line 82
            return "utf_16"  # line 82
        except UnicodeError:  # line 83
            pass  # line 83
        try:  # line 84
            binary.decode("cp1252")  # line 84
            return "cp1252"  # line 84
        except UnicodeError:  # line 85
            pass  # line 85
        return "ascii"  # this code will never be reached, as above is an 8-bit charset that always matches  # line 86

@_coconut_tco  # line 88
def wcswidth(string: 'str') -> 'int':  # line 88
    l = None  # type: int  # line 89
    try:  # line 90
        l = wcwidth.wcswitdh(string)  # line 91
        if l < 0:  # line 92
            return len(string)  # line 92
    except:  # line 93
        return _coconut_tail_call(len, string)  # line 93
    return l  # line 94

def conditionalIntersection(a: '_coconut.typing.Optional[FrozenSet[str]]', b: 'FrozenSet[str]') -> 'FrozenSet[str]':  # line 96
    return a & b if a else b  # line 96

def openIt(file: 'str', mode: 'str', compress: 'bool'=False) -> 'IO':  # Abstraction for opening both compressed and plain files  # line 98
    return bz2.BZ2File(file, mode) if compress else open(file, mode + "b")  # Abstraction for opening both compressed and plain files  # line 98

def eoldet(file: 'bytes') -> '_coconut.typing.Optional[bytes]':  # line 100
    ''' Determine EOL style from a binary string. '''  # line 101
    lf = file.count(b"\n")  # type: int  # line 102
    cr = file.count(b"\r")  # type: int  # line 103
    crlf = file.count(b"\r\n")  # type: int  # line 104
    if crlf > 0:  # DOS/Windows/Symbian etc.  # line 105
        if lf != crlf or cr != crlf:  # line 106
            warn("Inconsistent CR/NL count with CR+NL. Mixed EOL style detected, may cause problems during merge")  # line 106
        return b"\r\n"  # line 107
    if lf != 0 and cr != 0:  # line 108
        warn("Inconsistent CR/NL count without CR+NL. Mixed EOL style detected, may cause problems during merge")  # line 108
    if lf > cr:  # Linux/Unix  # line 109
        return b"\n"  # Linux/Unix  # line 109
    if cr > lf:  # older 8-bit machines  # line 110
        return b"\r"  # older 8-bit machines  # line 110
    return None  # no new line contained, cannot determine  # line 111

def Exit(message: 'str'="", code=1) -> 'None':  # line 113
    print("[EXIT%s]" % (" %.1fs" % (time.time() - lateBinding.start) if lateBinding.verbose else "") + (" " + message + "." if message != "" else ""), file=sys.stderr)  # line 113
    sys.exit(1)  # line 113

@_coconut_tco  # referenceso __builtin__.raw_input on Python 2  # line 115
def user_input(msg: 'str') -> 'str':  # referenceso __builtin__.raw_input on Python 2  # line 115
    return _coconut_tail_call(input, msg)  # referenceso __builtin__.raw_input on Python 2  # line 115

try:  # line 117
    Splittable = TypeVar("Splittable", str, bytes)  # line 117
except:  # Python 2  # line 118
    pass  # Python 2  # line 118
def safeSplit(s: 'Splittable', d: '_coconut.typing.Optional[Splittable]'=None) -> '_coconut.typing.Sequence[Splittable]':  # line 119
    return s.split(("\n" if isinstance(s, str) else b"\n") if d is None else d) if len(s) > 0 else []  # line 119

def ajoin(sep: 'str', seq: '_coconut.typing.Sequence[str]', nl="") -> 'str':  # line 121
    return (sep + (nl + sep).join(seq)) if seq else ""  # line 121

@_coconut_tco  # line 123
def sjoin(*s: 'Tuple[Any]') -> 'str':  # line 123
    return _coconut_tail_call(" ".join, [str(e) for e in s if e != ''])  # line 123

@_coconut_tco  # line 125
def hashStr(datas: 'str') -> 'str':  # line 125
    return _coconut_tail_call(hashlib.sha256(datas.encode(UTF8)).hexdigest)  # line 125

def modified(changes: 'ChangeSet', onlyBinary: 'bool'=False) -> 'bool':  # line 127
    return len(changes.additions) > 0 or len(changes.deletions) > 0 or len(changes.modifications) > 0  # line 127

def listindex(lizt: 'Sequence[Any]', what: 'Any', index: 'int'=0) -> 'int':  # line 129
    return lizt[index:].index(what) + index  # line 129

def getTermWidth() -> 'int':  # line 131
    try:  # line 131
        import termwidth  # line 132
    except:  # line 133
        return 80  # line 133
    return termwidth.getTermWidth()[0]  # line 134

def hashFile(path: 'str', compress: 'bool', saveTo: '_coconut.typing.Optional[str]'=None) -> 'Tuple[str, longint]':  # line 136
    ''' Calculate hash of file contents, and return compressed sized, if in write mode, or zero. '''  # line 137
    _hash = hashlib.sha256()  # line 138
    wsize = 0  # type: longint  # line 139
    to = openIt(saveTo, "w", compress) if saveTo else None  # line 140
    with open(path, "rb") as fd:  # line 141
        while True:  # line 142
            buffer = fd.read(bufSize)  # line 143
            _hash.update(buffer)  # line 144
            if to:  # line 145
                to.write(buffer)  # line 145
            if len(buffer) < bufSize:  # line 146
                break  # line 146
        if to:  # line 147
            to.close()  # line 148
            wsize = os.stat(saveTo).st_size  # line 149
    return (_hash.hexdigest(), wsize)  # line 150

def firstOfMap(map: 'Dict[str, Any]', params: '_coconut.typing.Sequence[str]', default: 'Any'=None) -> 'Any':  # line 152
    ''' Utility. '''  # line 153
    for k, v in map.items():  # line 154
        if k in params:  # line 155
            return v  # line 155
    return default  # line 156

@_coconut_tco  # line 158
def strftime(timestamp: '_coconut.typing.Optional[int]'=None) -> 'str':  # line 158
    return _coconut_tail_call(time.strftime, "%Y-%m-%d %H:%M:%S", time.localtime(timestamp / 1000. if timestamp is not None else None))  # line 158

def detectAndLoad(filename: '_coconut.typing.Optional[str]'=None, content: '_coconut.typing.Optional[bytes]'=None) -> 'Tuple[str, bytes, _coconut.typing.Sequence[str]]':  # line 160
    encoding = None  # type: str  # line 160
    eol = None  # type: bytes  # line 160
    lines = []  # type: _coconut.typing.Sequence[str]  # line 161
    if filename is not None:  # line 162
        with open(filename, "rb") as fd:  # line 163
            content = fd.read()  # line 163
    encoding = (lambda _coconut_none_coalesce_item: sys.getdefaultencoding() if _coconut_none_coalesce_item is None else _coconut_none_coalesce_item)(detectEncoding(content))  # line 164
    eol = eoldet(content)  # line 165
    if filename is not None:  # line 166
        with codecs.open(filename, encoding=encoding) as fd:  # line 167
            lines = safeSplit(fd.read(), (b"\n" if eol is None else eol).decode(encoding))  # line 167
    elif content is not None:  # line 168
        lines = safeSplit(content.decode(encoding), (b"\n" if eol is None else eol).decode(encoding))  # line 169
    else:  # line 170
        return (sys.getdefaultencoding(), b"\n", [])  # line 170
    return (encoding, eol, lines)  # line 171

def diffPathSets(last: 'Dict[str, PathInfo]', diff: 'Dict[str, PathInfo]') -> 'ChangeSet':  # line 173
    ''' Computes a changeset between in-memory and on-disk file lists.
      Additions contains PathInfo for entries in diff
      Deletions contains PathInfo for entries not anymore in diff
      Modifications contains PathInfo for entries changed from last to diff (new state)
  '''  # line 178
    changes = ChangeSet({}, {}, {})  # type: ChangeSet  # line 179
    for path, pinfo in last.items():  # line 180
        if path not in diff:  # now change  changes.deletions[path] = pinfo; continue  # line 181
            continue  # now change  changes.deletions[path] = pinfo; continue  # line 181
        vs = diff[path]  # reference to potentially changed path set  # line 182
        if vs.size is None:  # marked for deletion  # line 183
            changes.deletions[path] = pinfo  # marked for deletion  # line 183
            continue  # marked for deletion  # line 183
        if pinfo.size == None:  # re-added  # line 184
            changes.additions[path] = pinfo  # re-added  # line 184
            continue  # re-added  # line 184
        if pinfo.size != vs.size or pinfo.mtime != vs.mtime or pinfo.hash != vs.hash:  # not need to make hash comparison optional here  # line 185
            changes.modifications[path] = vs  # not need to make hash comparison optional here  # line 185
    for path, pinfo in diff.items():  # added loop  # line 186
        if path not in last:  # line 187
            changes.additions[path] = pinfo  # line 187
    assert not any([path in changes.deletions for path in changes.additions])  # invariant checks  # line 188
    assert not any([path in changes.additions for path in changes.deletions])  # line 189
    return changes  # line 190

try:  # line 192
    DataType = TypeVar("DataType", ChangeSet, MergeBlock, BranchInfo)  # line 192
except:  # Python 2  # line 193
    pass  # Python 2  # line 193

@_coconut_tco  # line 195
def dataCopy(_tipe: 'Type[DataType]', _old: 'DataType', *_args, **_kwargs) -> 'DataType':  # line 195
    r = _old._asdict()  # line 195
    r.update(**_kwargs)  # line 195
    return _coconut_tail_call(makedata, _tipe, *(list(_args) + [r[field] for field in _old._fields]))  # line 195
# TODO test namedtuple instead of instantiated tuple types in "datatype"?

@_coconut_tco  # line 198
def merge(file: '_coconut.typing.Optional[bytes]'=None, into: '_coconut.typing.Optional[bytes]'=None, filename: '_coconut.typing.Optional[str]'=None, intoname: '_coconut.typing.Optional[str]'=None, mergeOperation=MergeOperation.BOTH, conflictResolution=ConflictResolution.ASK, diffOnly: 'bool'=False) -> 'Union[bytes, List[MergeBlock]]':  # line 198
    ''' Merges binary text contents 'file' into file 'into', returning merged result. '''  # line 199
    encoding = None  # type: str  # line 200
    othr = None  # type: _coconut.typing.Sequence[str]  # line 200
    othreol = None  # type: _coconut.typing.Optional[bytes]  # line 200
    curr = None  # type: _coconut.typing.Sequence[str]  # line 200
    curreol = None  # type: _coconut.typing.Optional[bytes]  # line 200
    differ = difflib.Differ()  # line 201
    try:  # load files line-wise and normalize line endings (keep the one of the current file) TODO document  # line 202
        encoding, othreol, othr = detectAndLoad(filename=filename, content=file)  # line 203
        encoding, curreol, curr = detectAndLoad(filename=intoname, content=into)  # line 204
    except Exception as E:  # line 205
        Exit("Cannot merge '%s' into '%s': %r" % (filename, intoname, E))  # line 205
    if None not in [othreol, curreol] and othreol != curreol:  # line 206
        warn("Differing EOL-styles detected during merge. Using current file's style for merge output")  # line 206
    output = list(differ.compare(othr, curr))  # type: List[str]  # from generator expression  # line 207
    debug("Diff output: " + "".join([o.replace("\n", "\\n") for o in output]))  # line 208
    blocks = []  # type: List[MergeBlock]  # merged result in blocks  # line 209
    tmp = []  # type: List[str]  # block lines  # line 210
    last = " "  # line 211
    for no, line in enumerate(output + ["X"]):  # EOF marker (difflib's output will never be "X" alone)  # line 212
        if line[0] == last:  # continue filling consecutive block, no matter what type of block  # line 213
            tmp.append(line[2:])  # continue filling consecutive block, no matter what type of block  # line 213
            continue  # continue filling consecutive block, no matter what type of block  # line 213
        if line == "X":  # EOF marker - perform action for remaining block  # line 214
            if len(tmp) == 0:  # nothing left to do  # line 215
                break  # nothing left to do  # line 215
        if last == " ":  # block is same in both files  # line 216
            blocks.append(MergeBlock(MergeBlockType.KEEP, [line for line in tmp], line=no - len(tmp)))  # line 217
        elif last == "-":  # may be a deletion or replacement, store for later  # line 218
            blocks.append(MergeBlock(MergeBlockType.REMOVE, [line for line in tmp], line=no - len(tmp)))  # line 219
        elif last == "+":  # may be insertion or replacement  # line 220
            blocks.append(MergeBlock(MergeBlockType.INSERT, [line for line in tmp], line=no - len(tmp)))  # line 221
            if len(blocks) >= 2 and len(blocks[-1].lines) == len(blocks[-2].lines):  # replaces previously removed section entirely if any  # line 222
                if len(blocks[-1].lines) >= 2 or (blocks[-1].changes is None and blocks[-2].changes is None):  # full block or no intra-line comment  # line 223
                    blocks[-2] = MergeBlock(MergeBlockType.REPLACE, blocks[-1].lines, line=no - len(tmp) - 1, replaces=blocks[-2])  # remember replaced stuff TODO why -1 necessary?  # line 224
                else:  # may have intra-line modifications  # line 225
                    blocks[-2] = MergeBlock(MergeBlockType.MODIFY, blocks[-1].lines, line=no - len(tmp), replaces=blocks[-2], changes=blocks[-1].changes)  # line 226
                blocks.pop()  # remove TOS  # line 227
        elif last == "?":  # intra-line change comment  # line 228
            ilm = getIntraLineMarkers(tmp[0])  # tipe is one of MergeBlockType 1, 2, 4. # "? " line includes a trailing \n for some reason  # line 229
            blocks[-1] = dataCopy(MergeBlock, blocks[-1], tipe=MergeBlockType.MODIFY, changes=ilm)  # update to MODIFY, otherwise may be REPLACE instead  # line 230
        last = line[0]  # line 231
        tmp[:] = [line[2:]]  # line 232
    debug("Diff blocks: " + repr(blocks))  # line 233
    if diffOnly:  # line 234
        return blocks  # line 234
    output = []  # line 235
    for block in blocks:  # line 236
        if block.tipe == MergeBlockType.KEEP:  # line 237
            output.extend(block.lines)  # line 238
        elif block.tipe == MergeBlockType.INSERT and not (mergeOperation & MergeOperation.REMOVE):  # line 239
            output.extend(block.lines)  # line 240
        elif block.tipe == MergeBlockType.REPLACE:  # complete block replacement  # line 241
            if mergeOperation & MergeOperation.INSERT:  # replaced stuff TODO allow insertion BEFORE and alternatively AFTER?  # line 242
                output.extend(block.replaces.lines)  # replaced stuff TODO allow insertion BEFORE and alternatively AFTER?  # line 242
            if not (mergeOperation & MergeBlockType.REMOVE):  # if remove, don't add replaced lines, otherwise do  # line 243
                output.extend(block.lines)  # if remove, don't add replaced lines, otherwise do  # line 243
        elif block.tipe == MergeBlockType.REMOVE and mergeOperation & MergeOperation.INSERT:  # line 244
            output.extend(block.lines)  # line 245
        elif block.tipe == MergeBlockType.MODIFY:  # line 246
            if block.changes is not None and block.changes.tipe == MergeBlockType.INSERT:  # cannot be REMOVE, because it's always "-" then "+"  # line 247
                output.extend(block.lines if mergeOperation & MergeOperation.INSERT else block.replaces.lines)  # TODO logic?  # line 248
            elif block.replaces.changes is not None and block.replaces.changes.tipe == MergeBlockType.REMOVE:  # line 249
                output.extend(block.lines if mergeOperation & MergeOperation.REMOVE else block.replaces.lines)  # line 250
            elif block.changes is not None and block.changes.tipe == MergeBlockType.MODIFY:  # always both sides modified, but may differ in markers  # line 251
                if conflictResolution == ConflictResolution.THEIRS:  # line 252
                    output.extend(block.replaces.lines)  # line 253
                elif conflictResolution == ConflictResolution.MINE:  # line 254
                    output.extend(block.lines)  # line 255
                elif conflictResolution == ConflictResolution.ASK:  # line 256
                    print(ajoin("THR ", block.replaces.lines, "\n"))  # line 257
                    print(ajoin("MIN ", block.lines, "\n"))  # line 258
                    reso = {"i": ConflictResolution.MINE, "t": ConflictResolution.THEIRS, "m": ConflictResolution.NEXT, "u": None}.get(user_input(" Resolve: *M[I]ne, [T]heirs, [M]erge, [U]ser defined: ").strip().lower(), ConflictResolution.MINE)  # type: _coconut.typing.Optional[int]  # line 259
                    debug("User selected %d" % reso)  # line 260
                    _coconut_match_check = False  # line 261
                    _coconut_match_to = reso  # line 261
                    if _coconut_match_to is None:  # line 261
                        _coconut_match_check = True  # line 261
                    if _coconut_match_check:  # line 261
                        warn("Manual input not implemented yet")  # TODO allow multi-line input (CTRL+D?)  # line 262
                    _coconut_match_check = False  # line 263
                    _coconut_match_to = reso  # line 263
                    if _coconut_match_to == ConflictResolution.MINE:  # line 263
                        _coconut_match_check = True  # line 263
                    if _coconut_match_check:  # line 263
                        debug("Using mine")  # line 264
                        output.extend(block.lines)  # line 265
                    _coconut_match_check = False  # line 266
                    _coconut_match_to = reso  # line 266
                    if _coconut_match_to == ConflictResolution.THEIRS:  # line 266
                        _coconut_match_check = True  # line 266
                    if _coconut_match_check:  # line 266
                        debug("Using theirs")  # line 267
                        output.extend(block.replaces.lines)  # line 268
                    _coconut_match_check = False  # line 269
                    _coconut_match_to = reso  # line 269
                    if _coconut_match_to == ConflictResolution.NEXT:  # line 269
                        _coconut_match_check = True  # line 269
                    if _coconut_match_check:  # line 269
                        warn("Intra-line merge not implemented yet, skipping line(s)")  # line 270
                        output.extend(block.replaces.lines)  # line 271
            else:  # e.g. contains a deletion, but user was asking for insert only??  # line 272
                warn("Investigate this case")  # line 273
                output.extend(block.lines)  # default or not .replaces?  # line 274
    debug("Merge output: " + "; ".join(output))  # line 275
    nl = b"\n" if othreol is None else othreol if curreol is None else curreol  # type: bytes  # line 276
    return _coconut_tail_call(nl.join, [line.encode(encoding) for line in output])  # returning bytes  # line 277
# TODO handle check for more/less lines in found -/+ blocks to find common section and splitting prefix/suffix out

@_coconut_tco  # line 280
def getIntraLineMarkers(line: 'str') -> 'Range':  # line 280
    ''' Return (type, [affected indices]) of "? "-line diff markers ("? " suffix must be removed). '''  # line 281
    if "^" in line:  # line 282
        return _coconut_tail_call(Range, MergeBlockType.MODIFY, [i for i, c in enumerate(line) if c == "^"])  # line 282
    if "+" in line:  # line 283
        return _coconut_tail_call(Range, MergeBlockType.INSERT, [i for i, c in enumerate(line) if c == "+"])  # line 283
    if "-" in line:  # line 284
        return _coconut_tail_call(Range, MergeBlockType.REMOVE, [i for i, c in enumerate(line) if c == "-"])  # line 284
    return _coconut_tail_call(Range, MergeBlockType.KEEP, [])  # line 285

def findSosVcsBase() -> 'Tuple[_coconut.typing.Optional[str], _coconut.typing.Optional[str], _coconut.typing.Optional[str]]':  # line 287
    ''' Attempts to find sos and legacy VCS base folders. '''  # line 288
    debug("Detecting root folders...")  # line 289
    path = os.getcwd()  # type: str  # start in current folder, check parent until found or stopped  # line 290
    vcs = (None, None)  # type: Tuple[_coconut.typing.Optional[str], _coconut.typing.Optional[str]]  # line 291
    while not os.path.exists(os.path.join(path, metaFolder)):  # line 292
        contents = set(os.listdir(path))  # line 293
        vcss = [executable for folder, executable in vcsFolders.items() if folder in contents]  # type: _coconut.typing.Sequence[str]  # determine VCS type from dot folder  # line 294
        choice = None  # type: _coconut.typing.Optional[str]  # line 295
        if len(vcss) > 1:  # line 296
            choice = SVN if SVN in vcss else vcss[0]  # line 297
            warn("Detected more than one parallel VCS checkouts %r. Falling back to '%s'" % (vcss, choice))  # line 298
        elif len(vcss) > 0:  # line 299
            choice = vcss[0]  # line 299
        if not vcs[0] and choice:  # memorize current repo root  # line 300
            vcs = (path, choice)  # memorize current repo root  # line 300
        new = os.path.dirname(path)  # get parent path  # line 301
        if new == path:  # avoid infinite loop  # line 302
            break  # avoid infinite loop  # line 302
        path = new  # line 303
    if os.path.exists(os.path.join(path, metaFolder)):  # found something  # line 304
        if vcs[0]:  # already detected vcs base and command  # line 305
            return (path, vcs[0], vcs[1])  # already detected vcs base and command  # line 305
        sos = path  # line 306
        while True:  # continue search for VCS base  # line 307
            new = os.path.dirname(path)  # get parent path  # line 308
            if new == path:  # no VCS folder found  # line 309
                return (sos, None, None)  # no VCS folder found  # line 309
            path = new  # line 310
            contents = set(os.listdir(path))  # line 311
            vcss = [executable for folder, executable in vcsFolders.items() if folder in contents]  # determine VCS type  # line 312
            choice = None  # line 313
            if len(vcss) > 1:  # line 314
                choice = SVN if SVN in vcss else vcss[0]  # line 315
                warn("Detected more than one parallel VCS checkouts %r. Falling back to '%s'" % (vcss, choice))  # line 316
            elif len(vcss) > 0:  # line 317
                choice = vcss[0]  # line 317
            if choice:  # line 318
                return (sos, path, choice)  # line 318
    return (None, vcs[0], vcs[1])  # line 319

def tokenizeGlobPattern(pattern: 'str') -> 'List[GlobBlock]':  # line 321
    index = 0  # type: int  # line 322
    out = []  # type: List[GlobBlock]  # literal = True, first index  # line 323
    while index < len(pattern):  # line 324
        if pattern[index:index + 3] in ("[?]", "[*]", "[[]", "[]]"):  # line 325
            out.append(GlobBlock(False, pattern[index:index + 3], index))  # line 325
            continue  # line 325
        if pattern[index] in "*?":  # line 326
            count = 1  # type: int  # line 327
            while index + count < len(pattern) and pattern[index] == "?" and pattern[index + count] == "?":  # line 328
                count += 1  # line 328
            out.append(GlobBlock(False, pattern[index:index + count], index))  # line 329
            index += count  # line 329
            continue  # line 329
        if pattern[index:index + 2] == "[!":  # line 330
            out.append(GlobBlock(False, pattern[index:pattern.index("]", index + 2) + 1], index))  # line 330
            index += len(out[-1][1])  # line 330
            continue  # line 330
        count = 1  # line 331
        while index + count < len(pattern) and pattern[index + count] not in "*?[":  # line 332
            count += 1  # line 332
        out.append(GlobBlock(True, pattern[index:index + count], index))  # line 333
        index += count  # line 333
    return out  # line 334

def tokenizeGlobPatterns(oldPattern: 'str', newPattern: 'str') -> 'Tuple[_coconut.typing.Sequence[GlobBlock], _coconut.typing.Sequence[GlobBlock]]':  # line 336
    ot = tokenizeGlobPattern(oldPattern)  # type: List[GlobBlock]  # line 337
    nt = tokenizeGlobPattern(newPattern)  # type: List[GlobBlock]  # line 338
#  if len(ot) != len(nt): Exit("Source and target patterns can't be translated due to differing number of parsed glob markers and literal strings")
    if len([o for o in ot if not o.isLiteral]) < len([n for n in nt if not n.isLiteral]):  # line 340
        Exit("Source and target file patterns contain differing number of glob markers and can't be translated")  # line 340
    if any((O.content != N.content for O, N in zip([o for o in ot if not o.isLiteral], [n for n in nt if not n.isLiteral]))):  # line 341
        Exit("Source and target file patterns differ in semantics")  # line 341
    return (ot, nt)  # line 342

def convertGlobFiles(filenames: '_coconut.typing.Sequence[str]', oldPattern: '_coconut.typing.Sequence[GlobBlock]', newPattern: '_coconut.typing.Sequence[GlobBlock]') -> '_coconut.typing.Sequence[Tuple[str, str]]':  # line 344
    ''' Converts given filename according to specified file patterns. No support for adjacent glob markers currently. '''  # line 345
    pairs = []  # type: List[Tuple[str, str]]  # line 346
    for filename in filenames:  # line 347
        literals = [l for l in oldPattern if l.isLiteral]  # type: List[GlobBlock]  # source literals  # line 348
        nextliteral = 0  # type: int  # line 349
        parsedOld = []  # type: List[GlobBlock2]  # line 350
        index = 0  # type: int  # line 351
        for part in oldPattern:  # match everything in the old filename  # line 352
            if part.isLiteral:  # line 353
                parsedOld.append(GlobBlock2(True, part.content, part.content))  # line 353
                index += len(part.content)  # line 353
                nextliteral += 1  # line 353
            elif part.content.startswith("?"):  # line 354
                parsedOld.append(GlobBlock2(False, part.content, filename[index:index + len(part.content)]))  # line 354
                index += len(part.content)  # line 354
            elif part.content.startswith("["):  # line 355
                parsedOld.append(GlobBlock2(False, part.content, filename[index]))  # line 355
                index += 1  # line 355
            elif part.content == "*":  # line 356
                if nextliteral >= len(literals):  # line 357
                    parsedOld.append(GlobBlock2(False, part.content, filename[index:]))  # line 357
                    break  # line 357
                nxt = filename.index(literals[nextliteral].content, index)  # type: int  # also matches empty string  # line 358
                parsedOld.append(GlobBlock2(False, part.content, filename[index:nxt]))  # line 359
                index = nxt  # line 359
            else:  # line 360
                Exit("Invalid file pattern specified for move/rename")  # line 360
        globs = [g for g in parsedOld if not g.isLiteral]  # type: List[GlobBlock2]  # line 361
        literals = [l for l in newPattern if l.isLiteral]  # target literals  # line 362
        nextliteral = 0  # line 363
        nextglob = 0  # type: int  # line 363
        outname = []  # type: List[str]  # line 364
        for part in newPattern:  # generate new filename  # line 365
            if part.isLiteral:  # line 366
                outname.append(literals[nextliteral].content)  # line 366
                nextliteral += 1  # line 366
            else:  # line 367
                outname.append(globs[nextglob].matches)  # line 367
                nextglob += 1  # line 367
        pairs.append((filename, "".join(outname)))  # line 368
    return pairs  # line 369

@_coconut_tco  # line 371
def reorderRenameActions(actions: '_coconut.typing.Sequence[Tuple[str, str]]', exitOnConflict: 'bool'=True) -> '_coconut.typing.Sequence[Tuple[str, str]]':  # line 371
    ''' Attempt to put all rename actions into an order that avoids target == source names.
      Note, that it's currently not really possible to specify patterns that make this work (swapping "*" elements with a reference).
      An alternative would be to always have one (or all) files renamed to a temporary name before renaming to target filename.
  '''  # line 375
    if not actions:  # line 376
        return []  # line 376
    sources = None  # type: List[str]  # line 377
    targets = None  # type: List[str]  # line 377
    sources, targets = [list(l) for l in zip(*actions)]  # line 378
    last = len(actions)  # type: int  # line 379
    while last > 1:  # line 380
        clean = True  # type: bool  # line 381
        for i in range(1, last):  # line 382
            try:  # line 383
                index = targets[:i].index(sources[i])  # type: int  # line 384
                sources.insert(index, sources.pop(i))  # bubble up the action right before conflict  # line 385
                targets.insert(index, targets.pop(i))  # line 386
                clean = False  # line 387
            except:  # target not found in sources: good!  # line 388
                continue  # target not found in sources: good!  # line 388
        if clean:  # line 389
            break  # line 389
        last -= 1  # we know that the last entry in the list has the least conflicts, so we can disregard it in the next iteration  # line 390
    if exitOnConflict:  # line 391
        for i in range(1, len(actions)):  # line 392
            if sources[i] in targets[:i]:  # line 393
                Exit("There is no order of renaming actions that avoids copying over not-yet renamed files: '%s' is contained in matching source filenames" % (targets[i]))  # line 393
    return _coconut_tail_call(list, zip(sources, targets))  # line 394

def relativize(root: 'str', path: 'str') -> 'Tuple[str, str]':  # line 396
    ''' Determine OS-independent relative folder path, and relative pattern path. '''  # line 397
    relpath = os.path.relpath(os.path.dirname(os.path.abspath(path)), root).replace(os.sep, SLASH)  # line 398
    return relpath, os.path.join(relpath, os.path.basename(path)).replace(os.sep, SLASH)  # line 399

def parseOnlyOptions(root: 'str', options: '_coconut.typing.Sequence[str]') -> 'Tuple[_coconut.typing.Optional[FrozenSet[str]], _coconut.typing.Optional[FrozenSet[str]]]':  # line 401
    ''' Returns set of --only arguments, and set or --except arguments. '''  # line 402
    cwd = os.getcwd()  # type: str  # line 403
    onlys = []  # type: List[str]  # line 404
    excps = []  # type: List[str]  # line 404
    index = 0  # type: int  # line 404
    while True:  # line 405
        try:  # line 406
            index = 1 + listindex(options, "--only", index)  # line 407
            onlys.append(options[index])  # line 408
        except:  # line 409
            break  # line 409
    index = 0  # line 410
    while True:  # line 411
        try:  # line 412
            index = 1 + listindex(options, "--except", index)  # line 413
            excps.append(options[index])  # line 414
        except:  # line 415
            break  # line 415
    return (frozenset((relativize(root, o)[1] for o in onlys)) if onlys else None, frozenset((relativize(root, e)[1] for e in excps)) if excps else None)  # line 416
