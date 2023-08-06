#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# __coconut_hash__ = 0x73cafcff

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


# Value types
class BranchInfo(_coconut_NamedTuple("BranchInfo", [("number", 'int'), ("ctime", 'int'), ("name", '_coconut.typing.Optional[str]'), ("inSync", 'bool'), ("tracked", 'List[str]')])):  # tracked is a list on purpose, as serialization to JSON needs effort and frequent access is not taking place  # line 56
    __slots__ = ()  # tracked is a list on purpose, as serialization to JSON needs effort and frequent access is not taking place  # line 56
    __ne__ = _coconut.object.__ne__  # tracked is a list on purpose, as serialization to JSON needs effort and frequent access is not taking place  # line 56
    def __new__(_cls, number, ctime, name=None, inSync=False, tracked=[]):  # tracked is a list on purpose, as serialization to JSON needs effort and frequent access is not taking place  # line 56
        return _coconut.tuple.__new__(_cls, (number, ctime, name, inSync, tracked))  # tracked is a list on purpose, as serialization to JSON needs effort and frequent access is not taking place  # line 56
# tracked is a list on purpose, as serialization to JSON needs effort and frequent access is not taking place
class CommitInfo(_coconut_NamedTuple("CommitInfo", [("number", 'int'), ("ctime", 'int'), ("message", '_coconut.typing.Optional[str]')])):  # line 57
    __slots__ = ()  # line 57
    __ne__ = _coconut.object.__ne__  # line 57
    def __new__(_cls, number, ctime, message=None):  # line 57
        return _coconut.tuple.__new__(_cls, (number, ctime, message))  # line 57

class PathInfo(_coconut_NamedTuple("PathInfo", [("nameHash", 'str'), ("size", '_coconut.typing.Optional[int]'), ("mtime", 'int'), ("hash", '_coconut.typing.Optional[str]')])):  # size == None means deleted in this revision  # line 58
    __slots__ = ()  # size == None means deleted in this revision  # line 58
    __ne__ = _coconut.object.__ne__  # size == None means deleted in this revision  # line 58
class ChangeSet(_coconut_NamedTuple("ChangeSet", [("additions", 'Dict[str, PathInfo]'), ("deletions", 'Dict[str, PathInfo]'), ("modifications", 'Dict[str, PathInfo]')])):  # avoid default assignment of {} as it leads to runtime errors (contains data on init for unknown reason)  # line 59
    __slots__ = ()  # avoid default assignment of {} as it leads to runtime errors (contains data on init for unknown reason)  # line 59
    __ne__ = _coconut.object.__ne__  # avoid default assignment of {} as it leads to runtime errors (contains data on init for unknown reason)  # line 59
class Range(_coconut_NamedTuple("Range", [("tipe", 'int'), ("indexes", '_coconut.typing.Sequence[int]')])):  # MergeBlockType[1,2,4], line number, length  # line 60
    __slots__ = ()  # MergeBlockType[1,2,4], line number, length  # line 60
    __ne__ = _coconut.object.__ne__  # MergeBlockType[1,2,4], line number, length  # line 60
class MergeBlock(_coconut_NamedTuple("MergeBlock", [("tipe", 'int'), ("lines", '_coconut.typing.Sequence[str]'), ("line", 'int'), ("replaces", '_coconut.typing.Optional[MergeBlock]'), ("changes", '_coconut.typing.Optional[Range]')])):  # line 61
    __slots__ = ()  # line 61
    __ne__ = _coconut.object.__ne__  # line 61
    def __new__(_cls, tipe, lines, line, replaces=None, changes=None):  # line 61
        return _coconut.tuple.__new__(_cls, (tipe, lines, line, replaces, changes))  # line 61

class GlobBlock(_coconut_NamedTuple("GlobBlock", [("isLiteral", 'bool'), ("content", 'str'), ("index", 'int')])):  # for file pattern rename/move matching  # line 62
    __slots__ = ()  # for file pattern rename/move matching  # line 62
    __ne__ = _coconut.object.__ne__  # for file pattern rename/move matching  # line 62
class GlobBlock2(_coconut_NamedTuple("GlobBlock2", [("isLiteral", 'bool'), ("content", 'str'), ("matches", 'str')])):  # matching file pattern and input filename for translation  # line 63
    __slots__ = ()  # matching file pattern and input filename for translation  # line 63
    __ne__ = _coconut.object.__ne__  # matching file pattern and input filename for translation  # line 63


# Enums
class ConflictResolution:  # prefer their changes, prefer my changes, ask user for each change, go to next deeper level (e.g. from files to lines, characters)  # line 67
    THEIRS, MINE, ASK, NEXT = range(4)  # prefer their changes, prefer my changes, ask user for each change, go to next deeper level (e.g. from files to lines, characters)  # line 67
class MergeOperation:  # insert remote changes into current, remove remote deletions from current, do both (replicate remote state) TODO handle inline-operations separate?  # line 68
    INSERT, REMOVE, BOTH = 1, 2, 3  # insert remote changes into current, remove remote deletions from current, do both (replicate remote state) TODO handle inline-operations separate?  # line 68
class MergeBlockType:  # modify = intra-line changes  # line 69
    KEEP, INSERT, REMOVE, REPLACE, MODIFY, MOVE = range(6)  # modify = intra-line changes  # line 69


# Functions
try:  # line 73
    import chardet  # https://github.com/chardet/chardet  # line 74
    def detectEncoding(binary: 'bytes') -> 'str':  # line 75
        return chardet.detect(binary)["encoding"]  # line 75
except:  # line 76
    def detectEncoding(binary: 'bytes') -> 'str':  # Guess the encoding  # line 77
        ''' Fallback if chardet library missing. '''  # line 78
        try:  # line 79
            binary.decode(UTF8)  # line 79
            return UTF8  # line 79
        except UnicodeError:  # line 80
            pass  # line 80
        try:  # line 81
            binary.decode("utf_16")  # line 81
            return "utf_16"  # line 81
        except UnicodeError:  # line 82
            pass  # line 82
        try:  # line 83
            binary.decode("cp1252")  # line 83
            return "cp1252"  # line 83
        except UnicodeError:  # line 84
            pass  # line 84
        return "ascii"  # this code will never be reached, as above is an 8-bit charset that always matches  # line 85

@_coconut_tco  # line 87
def wcswidth(string: 'str') -> 'int':  # line 87
    l = None  # type: int  # line 88
    try:  # line 89
        l = wcwidth.wcswitdh(string)  # line 90
        if l < 0:  # line 91
            return len(string)  # line 91
    except:  # line 92
        return _coconut_tail_call(len, string)  # line 92
    return l  # line 93

def conditionalIntersection(a: '_coconut.typing.Optional[FrozenSet[str]]', b: 'FrozenSet[str]') -> 'FrozenSet[str]':  # line 95
    return a & b if a else b  # line 95

def openIt(file: 'str', mode: 'str', compress: 'bool'=False) -> 'IO':  # Abstraction for opening both compressed and plain files  # line 97
    return bz2.BZ2File(file, mode) if compress else open(file, mode + "b")  # Abstraction for opening both compressed and plain files  # line 97

def eoldet(file: 'bytes') -> '_coconut.typing.Optional[bytes]':  # line 99
    ''' Determine EOL style from a binary string. '''  # line 100
    lf = file.count(b"\n")  # type: int  # line 101
    cr = file.count(b"\r")  # type: int  # line 102
    crlf = file.count(b"\r\n")  # type: int  # line 103
    if crlf > 0:  # DOS/Windows/Symbian etc.  # line 104
        if lf != crlf or cr != crlf:  # line 105
            warn("Inconsistent CR/NL count with CR+NL. Mixed EOL style detected, may cause problems during merge")  # line 105
        return b"\r\n"  # line 106
    if lf != 0 and cr != 0:  # line 107
        warn("Inconsistent CR/NL count without CR+NL. Mixed EOL style detected, may cause problems during merge")  # line 107
    if lf > cr:  # Linux/Unix  # line 108
        return b"\n"  # Linux/Unix  # line 108
    if cr > lf:  # older 8-bit machines  # line 109
        return b"\r"  # older 8-bit machines  # line 109
    return None  # no new line contained, cannot determine  # line 110

def Exit(message: 'str'="") -> 'None':  # line 112
    print("[EXIT]" + (" " + message + "." if message != "" else ""), file=sys.stderr)  # line 112
    sys.exit(1)  # line 112

@_coconut_tco  # referenceso __builtin__.raw_input on Python 2  # line 114
def user_input(msg: 'str') -> 'str':  # referenceso __builtin__.raw_input on Python 2  # line 114
    return _coconut_tail_call(input, msg)  # referenceso __builtin__.raw_input on Python 2  # line 114

try:  # line 116
    Splittable = TypeVar("Splittable", str, bytes)  # line 116
except:  # Python 2  # line 117
    pass  # Python 2  # line 117
def safeSplit(s: 'Splittable', d: '_coconut.typing.Optional[Splittable]'=None) -> '_coconut.typing.Sequence[Splittable]':  # line 118
    return s.split(("\n" if isinstance(s, str) else b"\n") if d is None else d) if len(s) > 0 else []  # line 118

def ajoin(sep: 'str', seq: '_coconut.typing.Sequence[str]', nl="") -> 'str':  # line 120
    return (sep + (nl + sep).join(seq)) if seq else ""  # line 120

@_coconut_tco  # line 122
def sjoin(*s: 'Tuple[Any]') -> 'str':  # line 122
    return _coconut_tail_call(" ".join, [str(e) for e in s if e != ''])  # line 122

@_coconut_tco  # line 124
def hashStr(datas: 'str') -> 'str':  # line 124
    return _coconut_tail_call(hashlib.sha256(datas.encode(UTF8)).hexdigest)  # line 124

def modified(changes: 'ChangeSet', onlyBinary: 'bool'=False) -> 'bool':  # line 126
    return len(changes.additions) > 0 or len(changes.deletions) > 0 or len(changes.modifications) > 0  # line 126

def listindex(lizt: 'Sequence[Any]', what: 'Any', index: 'int'=0) -> 'int':  # line 128
    return lizt[index:].index(what) + index  # line 128

def getTermWidth() -> 'int':  # line 130
    try:  # line 130
        import termwidth  # line 131
    except:  # line 132
        return 80  # line 132
    return termwidth.getTermWidth()[0]  # line 133

def hashFile(path: 'str', compress: 'bool', saveTo: '_coconut.typing.Optional[str]'=None) -> 'Tuple[str, longint]':  # line 135
    ''' Calculate hash of file contents, and return compressed sized, if in write mode, or zero. '''  # line 136
    _hash = hashlib.sha256()  # line 137
    wsize = 0  # type: longint  # line 138
    to = openIt(saveTo, "w", compress) if saveTo else None  # line 139
    with open(path, "rb") as fd:  # line 140
        while True:  # line 141
            buffer = fd.read(bufSize)  # line 142
            _hash.update(buffer)  # line 143
            if to:  # line 144
                to.write(buffer)  # line 144
            if len(buffer) < bufSize:  # line 145
                break  # line 145
        if to:  # line 146
            to.close()  # line 147
            wsize = os.stat(saveTo).st_size  # line 148
    return (_hash.hexdigest(), wsize)  # line 149

def firstOfMap(map: 'Dict[str, Any]', params: '_coconut.typing.Sequence[str]', default: 'Any'=None) -> 'Any':  # line 151
    ''' Utility. '''  # line 152
    for k, v in map.items():  # line 153
        if k in params:  # line 154
            return v  # line 154
    return default  # line 155

@_coconut_tco  # line 157
def strftime(timestamp: '_coconut.typing.Optional[int]'=None) -> 'str':  # line 157
    return _coconut_tail_call(time.strftime, "%Y-%m-%d %H:%M:%S", time.localtime(timestamp / 1000. if timestamp is not None else None))  # line 157

def detectAndLoad(filename: '_coconut.typing.Optional[str]'=None, content: '_coconut.typing.Optional[bytes]'=None) -> 'Tuple[str, bytes, _coconut.typing.Sequence[str]]':  # line 159
    encoding = None  # type: str  # line 159
    eol = None  # type: bytes  # line 159
    lines = []  # type: _coconut.typing.Sequence[str]  # line 160
    if filename is not None:  # line 161
        with open(filename, "rb") as fd:  # line 162
            content = fd.read()  # line 162
    encoding = (lambda _coconut_none_coalesce_item: sys.getdefaultencoding() if _coconut_none_coalesce_item is None else _coconut_none_coalesce_item)(detectEncoding(content))  # line 163
    eol = eoldet(content)  # line 164
    if filename is not None:  # line 165
        with codecs.open(filename, encoding=encoding) as fd:  # line 166
            lines = safeSplit(fd.read(), (b"\n" if eol is None else eol).decode(encoding))  # line 166
    elif content is not None:  # line 167
        lines = safeSplit(content.decode(encoding), (b"\n" if eol is None else eol).decode(encoding))  # line 168
    else:  # line 169
        return (sys.getdefaultencoding(), b"\n", [])  # line 169
    return (encoding, eol, lines)  # line 170

def diffPathSets(last: 'Dict[str, PathInfo]', diff: 'Dict[str, PathInfo]') -> 'ChangeSet':  # line 172
    ''' Computes a changeset between in-memory and on-disk file lists.
      Additions contains PathInfo for entries in diff
      Deletions contains PathInfo for entries not anymore in diff
      Modifications contains PathInfo for entries changed from last to diff (new state)
  '''  # line 177
    changes = ChangeSet({}, {}, {})  # type: ChangeSet  # line 178
    for path, pinfo in last.items():  # line 179
        if path not in diff:  # now change  changes.deletions[path] = pinfo; continue  # line 180
            continue  # now change  changes.deletions[path] = pinfo; continue  # line 180
        vs = diff[path]  # reference to potentially changed path set  # line 181
        if vs.size is None:  # marked for deletion  # line 182
            changes.deletions[path] = pinfo  # marked for deletion  # line 182
            continue  # marked for deletion  # line 182
        if pinfo.size == None:  # re-added  # line 183
            changes.additions[path] = pinfo  # re-added  # line 183
            continue  # re-added  # line 183
        if pinfo.size != vs.size or pinfo.mtime != vs.mtime or pinfo.hash != vs.hash:  # not need to make hash comparison optional here  # line 184
            changes.modifications[path] = vs  # not need to make hash comparison optional here  # line 184
    for path, pinfo in diff.items():  # added loop  # line 185
        if path not in last:  # line 186
            changes.additions[path] = pinfo  # line 186
    assert not any([path in changes.deletions for path in changes.additions])  # invariant checks  # line 187
    assert not any([path in changes.additions for path in changes.deletions])  # line 188
    return changes  # line 189

try:  # line 191
    DataType = TypeVar("DataType", ChangeSet, MergeBlock, BranchInfo)  # line 191
except:  # Python 2  # line 192
    pass  # Python 2  # line 192

@_coconut_tco  # line 194
def dataCopy(_tipe: 'Type[DataType]', _old: 'DataType', *_args, **_kwargs) -> 'DataType':  # line 194
    r = _old._asdict()  # line 194
    r.update(**_kwargs)  # line 194
    return _coconut_tail_call(makedata, _tipe, *(list(_args) + [r[field] for field in _old._fields]))  # line 194
# TODO test namedtuple instead of instantiated tuple types in "datatype"?

@_coconut_tco  # line 197
def merge(file: '_coconut.typing.Optional[bytes]'=None, into: '_coconut.typing.Optional[bytes]'=None, filename: '_coconut.typing.Optional[str]'=None, intoname: '_coconut.typing.Optional[str]'=None, mergeOperation=MergeOperation.BOTH, conflictResolution=ConflictResolution.ASK, diffOnly: 'bool'=False) -> 'Union[bytes, List[MergeBlock]]':  # line 197
    ''' Merges binary text contents 'file' into file 'into', returning merged result. '''  # line 198
    encoding = None  # type: str  # line 199
    othr = None  # type: _coconut.typing.Sequence[str]  # line 199
    othreol = None  # type: _coconut.typing.Optional[bytes]  # line 199
    curr = None  # type: _coconut.typing.Sequence[str]  # line 199
    curreol = None  # type: _coconut.typing.Optional[bytes]  # line 199
    differ = difflib.Differ()  # line 200
    try:  # load files line-wise and normalize line endings (keep the one of the current file) TODO document  # line 201
        encoding, othreol, othr = detectAndLoad(filename=filename, content=file)  # line 202
        encoding, curreol, curr = detectAndLoad(filename=intoname, content=into)  # line 203
    except Exception as E:  # line 204
        Exit("Cannot merge '%s' into '%s': %r" % (filename, intoname, E))  # line 204
    if None not in [othreol, curreol] and othreol != curreol:  # line 205
        warn("Differing EOL-styles detected during merge. Using current file's style for merge output")  # line 205
    output = list(differ.compare(othr, curr))  # type: List[str]  # from generator expression  # line 206
    debug("Diff output: " + "".join([o.replace("\n", "\\n") for o in output]))  # line 207
    blocks = []  # type: List[MergeBlock]  # merged result in blocks  # line 208
    tmp = []  # type: List[str]  # block lines  # line 209
    last = " "  # line 210
    for no, line in enumerate(output + ["X"]):  # EOF marker (difflib's output will never be "X" alone)  # line 211
        if line[0] == last:  # continue filling consecutive block, no matter what type of block  # line 212
            tmp.append(line[2:])  # continue filling consecutive block, no matter what type of block  # line 212
            continue  # continue filling consecutive block, no matter what type of block  # line 212
        if line == "X":  # EOF marker - perform action for remaining block  # line 213
            if len(tmp) == 0:  # nothing left to do  # line 214
                break  # nothing left to do  # line 214
        if last == " ":  # block is same in both files  # line 215
            blocks.append(MergeBlock(MergeBlockType.KEEP, [line for line in tmp], line=no - len(tmp)))  # line 216
        elif last == "-":  # may be a deletion or replacement, store for later  # line 217
            blocks.append(MergeBlock(MergeBlockType.REMOVE, [line for line in tmp], line=no - len(tmp)))  # line 218
        elif last == "+":  # may be insertion or replacement  # line 219
            blocks.append(MergeBlock(MergeBlockType.INSERT, [line for line in tmp], line=no - len(tmp)))  # line 220
            if len(blocks) >= 2 and len(blocks[-1].lines) == len(blocks[-2].lines):  # replaces previously removed section entirely if any  # line 221
                if len(blocks[-1].lines) >= 2 or (blocks[-1].changes is None and blocks[-2].changes is None):  # full block or no intra-line comment  # line 222
                    blocks[-2] = MergeBlock(MergeBlockType.REPLACE, blocks[-1].lines, line=no - len(tmp) - 1, replaces=blocks[-2])  # remember replaced stuff TODO why -1 necessary?  # line 223
                else:  # may have intra-line modifications  # line 224
                    blocks[-2] = MergeBlock(MergeBlockType.MODIFY, blocks[-1].lines, line=no - len(tmp), replaces=blocks[-2], changes=blocks[-1].changes)  # line 225
                blocks.pop()  # remove TOS  # line 226
        elif last == "?":  # intra-line change comment  # line 227
            ilm = getIntraLineMarkers(tmp[0])  # tipe is one of MergeBlockType 1, 2, 4. # "? " line includes a trailing \n for some reason  # line 228
            blocks[-1] = dataCopy(MergeBlock, blocks[-1], tipe=MergeBlockType.MODIFY, changes=ilm)  # update to MODIFY, otherwise may be REPLACE instead  # line 229
        last = line[0]  # line 230
        tmp[:] = [line[2:]]  # line 231
    debug("Diff blocks: " + repr(blocks))  # line 232
    if diffOnly:  # line 233
        return blocks  # line 233
    output = []  # line 234
    for block in blocks:  # line 235
        if block.tipe == MergeBlockType.KEEP:  # line 236
            output.extend(block.lines)  # line 237
        elif block.tipe == MergeBlockType.INSERT and not (mergeOperation & MergeOperation.REMOVE):  # line 238
            output.extend(block.lines)  # line 239
        elif block.tipe == MergeBlockType.REPLACE:  # complete block replacement  # line 240
            if mergeOperation & MergeOperation.INSERT:  # replaced stuff TODO allow insertion BEFORE and alternatively AFTER?  # line 241
                output.extend(block.replaces.lines)  # replaced stuff TODO allow insertion BEFORE and alternatively AFTER?  # line 241
            if not (mergeOperation & MergeBlockType.REMOVE):  # if remove, don't add replaced lines, otherwise do  # line 242
                output.extend(block.lines)  # if remove, don't add replaced lines, otherwise do  # line 242
        elif block.tipe == MergeBlockType.REMOVE and mergeOperation & MergeOperation.INSERT:  # line 243
            output.extend(block.lines)  # line 244
        elif block.tipe == MergeBlockType.MODIFY:  # line 245
            if block.changes is not None and block.changes.tipe == MergeBlockType.INSERT:  # cannot be REMOVE, because it's always "-" then "+"  # line 246
                output.extend(block.lines if mergeOperation & MergeOperation.INSERT else block.replaces.lines)  # TODO logic?  # line 247
            elif block.replaces.changes is not None and block.replaces.changes.tipe == MergeBlockType.REMOVE:  # line 248
                output.extend(block.lines if mergeOperation & MergeOperation.REMOVE else block.replaces.lines)  # line 249
            elif block.changes is not None and block.changes.tipe == MergeBlockType.MODIFY:  # always both sides modified, but may differ in markers  # line 250
                if conflictResolution == ConflictResolution.THEIRS:  # line 251
                    output.extend(block.replaces.lines)  # line 252
                elif conflictResolution == ConflictResolution.MINE:  # line 253
                    output.extend(block.lines)  # line 254
                elif conflictResolution == ConflictResolution.ASK:  # line 255
                    print(ajoin("THR ", block.replaces.lines, "\n"))  # line 256
                    print(ajoin("MIN ", block.lines, "\n"))  # line 257
                    reso = {"i": ConflictResolution.MINE, "t": ConflictResolution.THEIRS, "m": ConflictResolution.NEXT, "u": None}.get(user_input(" Resolve: *M[I]ne, [T]heirs, [M]erge, [U]ser defined: ").strip().lower(), ConflictResolution.MINE)  # type: _coconut.typing.Optional[int]  # line 258
                    debug("User selected %d" % reso)  # line 259
                    _coconut_match_check = False  # line 260
                    _coconut_match_to = reso  # line 260
                    if _coconut_match_to is None:  # line 260
                        _coconut_match_check = True  # line 260
                    if _coconut_match_check:  # line 260
                        warn("Manual input not implemented yet")  # TODO allow multi-line input (CTRL+D?)  # line 261
                    _coconut_match_check = False  # line 262
                    _coconut_match_to = reso  # line 262
                    if _coconut_match_to == ConflictResolution.MINE:  # line 262
                        _coconut_match_check = True  # line 262
                    if _coconut_match_check:  # line 262
                        debug("Using mine")  # line 263
                        output.extend(block.lines)  # line 264
                    _coconut_match_check = False  # line 265
                    _coconut_match_to = reso  # line 265
                    if _coconut_match_to == ConflictResolution.THEIRS:  # line 265
                        _coconut_match_check = True  # line 265
                    if _coconut_match_check:  # line 265
                        debug("Using theirs")  # line 266
                        output.extend(block.replaces.lines)  # line 267
                    _coconut_match_check = False  # line 268
                    _coconut_match_to = reso  # line 268
                    if _coconut_match_to == ConflictResolution.NEXT:  # line 268
                        _coconut_match_check = True  # line 268
                    if _coconut_match_check:  # line 268
                        warn("Intra-line merge not implemented yet, skipping line(s)")  # line 269
                        output.extend(block.replaces.lines)  # line 270
            else:  # e.g. contains a deletion, but user was asking for insert only??  # line 271
                warn("Investigate this case")  # line 272
                output.extend(block.lines)  # default or not .replaces?  # line 273
    debug("Merge output: " + "; ".join(output))  # line 274
    nl = b"\n" if othreol is None else othreol if curreol is None else curreol  # type: bytes  # line 275
    return _coconut_tail_call(nl.join, [line.encode(encoding) for line in output])  # returning bytes  # line 276
# TODO handle check for more/less lines in found -/+ blocks to find common section and splitting prefix/suffix out

@_coconut_tco  # line 279
def getIntraLineMarkers(line: 'str') -> 'Range':  # line 279
    ''' Return (type, [affected indices]) of "? "-line diff markers ("? " suffix must be removed). '''  # line 280
    if "^" in line:  # line 281
        return _coconut_tail_call(Range, MergeBlockType.MODIFY, [i for i, c in enumerate(line) if c == "^"])  # line 281
    if "+" in line:  # line 282
        return _coconut_tail_call(Range, MergeBlockType.INSERT, [i for i, c in enumerate(line) if c == "+"])  # line 282
    if "-" in line:  # line 283
        return _coconut_tail_call(Range, MergeBlockType.REMOVE, [i for i, c in enumerate(line) if c == "-"])  # line 283
    return _coconut_tail_call(Range, MergeBlockType.KEEP, [])  # line 284

def findSosVcsBase() -> 'Tuple[_coconut.typing.Optional[str], _coconut.typing.Optional[str], _coconut.typing.Optional[str]]':  # line 286
    ''' Attempts to find sos and legacy VCS base folders. '''  # line 287
    debug("Detecting root folders...")  # line 288
    path = os.getcwd()  # type: str  # start in current folder, check parent until found or stopped  # line 289
    vcs = (None, None)  # type: Tuple[_coconut.typing.Optional[str], _coconut.typing.Optional[str]]  # line 290
    while not os.path.exists(os.path.join(path, metaFolder)):  # line 291
        contents = set(os.listdir(path))  # line 292
        vcss = [executable for folder, executable in vcsFolders.items() if folder in contents]  # type: _coconut.typing.Sequence[str]  # determine VCS type from dot folder  # line 293
        choice = None  # type: _coconut.typing.Optional[str]  # line 294
        if len(vcss) > 1:  # line 295
            choice = SVN if SVN in vcss else vcss[0]  # line 296
            warn("Detected more than one parallel VCS checkouts %r. Falling back to '%s'" % (vcss, choice))  # line 297
        elif len(vcss) > 0:  # line 298
            choice = vcss[0]  # line 298
        if not vcs[0] and choice:  # memorize current repo root  # line 299
            vcs = (path, choice)  # memorize current repo root  # line 299
        new = os.path.dirname(path)  # get parent path  # line 300
        if new == path:  # avoid infinite loop  # line 301
            break  # avoid infinite loop  # line 301
        path = new  # line 302
    if os.path.exists(os.path.join(path, metaFolder)):  # found something  # line 303
        if vcs[0]:  # already detected vcs base and command  # line 304
            return (path, vcs[0], vcs[1])  # already detected vcs base and command  # line 304
        sos = path  # line 305
        while True:  # continue search for VCS base  # line 306
            new = os.path.dirname(path)  # get parent path  # line 307
            if new == path:  # no VCS folder found  # line 308
                return (sos, None, None)  # no VCS folder found  # line 308
            path = new  # line 309
            contents = set(os.listdir(path))  # line 310
            vcss = [executable for folder, executable in vcsFolders.items() if folder in contents]  # determine VCS type  # line 311
            choice = None  # line 312
            if len(vcss) > 1:  # line 313
                choice = SVN if SVN in vcss else vcss[0]  # line 314
                warn("Detected more than one parallel VCS checkouts %r. Falling back to '%s'" % (vcss, choice))  # line 315
            elif len(vcss) > 0:  # line 316
                choice = vcss[0]  # line 316
            if choice:  # line 317
                return (sos, path, choice)  # line 317
    return (None, vcs[0], vcs[1])  # line 318

def tokenizeGlobPattern(pattern: 'str') -> 'List[GlobBlock]':  # line 320
    index = 0  # type: int  # line 321
    out = []  # type: List[GlobBlock]  # literal = True, first index  # line 322
    while index < len(pattern):  # line 323
        if pattern[index:index + 3] in ("[?]", "[*]", "[[]", "[]]"):  # line 324
            out.append(GlobBlock(False, pattern[index:index + 3], index))  # line 324
            continue  # line 324
        if pattern[index] in "*?":  # line 325
            count = 1  # type: int  # line 326
            while index + count < len(pattern) and pattern[index] == "?" and pattern[index + count] == "?":  # line 327
                count += 1  # line 327
            out.append(GlobBlock(False, pattern[index:index + count], index))  # line 328
            index += count  # line 328
            continue  # line 328
        if pattern[index:index + 2] == "[!":  # line 329
            out.append(GlobBlock(False, pattern[index:pattern.index("]", index + 2) + 1], index))  # line 329
            index += len(out[-1][1])  # line 329
            continue  # line 329
        count = 1  # line 330
        while index + count < len(pattern) and pattern[index + count] not in "*?[":  # line 331
            count += 1  # line 331
        out.append(GlobBlock(True, pattern[index:index + count], index))  # line 332
        index += count  # line 332
    return out  # line 333

def tokenizeGlobPatterns(oldPattern: 'str', newPattern: 'str') -> 'Tuple[_coconut.typing.Sequence[GlobBlock], _coconut.typing.Sequence[GlobBlock]]':  # line 335
    ot = tokenizeGlobPattern(oldPattern)  # type: List[GlobBlock]  # line 336
    nt = tokenizeGlobPattern(newPattern)  # type: List[GlobBlock]  # line 337
#  if len(ot) != len(nt): Exit("Source and target patterns can't be translated due to differing number of parsed glob markers and literal strings")
    if len([o for o in ot if not o.isLiteral]) < len([n for n in nt if not n.isLiteral]):  # line 339
        Exit("Source and target file patterns contain differing number of glob markers and can't be translated")  # line 339
    if any((O.content != N.content for O, N in zip([o for o in ot if not o.isLiteral], [n for n in nt if not n.isLiteral]))):  # line 340
        Exit("Source and target file patterns differ in semantics")  # line 340
    return (ot, nt)  # line 341

def convertGlobFiles(filenames: '_coconut.typing.Sequence[str]', oldPattern: '_coconut.typing.Sequence[GlobBlock]', newPattern: '_coconut.typing.Sequence[GlobBlock]') -> '_coconut.typing.Sequence[Tuple[str, str]]':  # line 343
    ''' Converts given filename according to specified file patterns. No support for adjacent glob markers currently. '''  # line 344
    pairs = []  # type: List[Tuple[str, str]]  # line 345
    for filename in filenames:  # line 346
        literals = [l for l in oldPattern if l.isLiteral]  # type: List[GlobBlock]  # source literals  # line 347
        nextliteral = 0  # type: int  # line 348
        parsedOld = []  # type: List[GlobBlock2]  # line 349
        index = 0  # type: int  # line 350
        for part in oldPattern:  # match everything in the old filename  # line 351
            if part.isLiteral:  # line 352
                parsedOld.append(GlobBlock2(True, part.content, part.content))  # line 352
                index += len(part.content)  # line 352
                nextliteral += 1  # line 352
            elif part.content.startswith("?"):  # line 353
                parsedOld.append(GlobBlock2(False, part.content, filename[index:index + len(part.content)]))  # line 353
                index += len(part.content)  # line 353
            elif part.content.startswith("["):  # line 354
                parsedOld.append(GlobBlock2(False, part.content, filename[index]))  # line 354
                index += 1  # line 354
            elif part.content == "*":  # line 355
                if nextliteral >= len(literals):  # line 356
                    parsedOld.append(GlobBlock2(False, part.content, filename[index:]))  # line 356
                    break  # line 356
                nxt = filename.index(literals[nextliteral].content, index)  # type: int  # also matches empty string  # line 357
                parsedOld.append(GlobBlock2(False, part.content, filename[index:nxt]))  # line 358
                index = nxt  # line 358
            else:  # line 359
                Exit("Invalid file pattern specified for move/rename")  # line 359
        globs = [g for g in parsedOld if not g.isLiteral]  # type: List[GlobBlock2]  # line 360
        literals = [l for l in newPattern if l.isLiteral]  # target literals  # line 361
        nextliteral = 0  # line 362
        nextglob = 0  # type: int  # line 362
        outname = []  # type: List[str]  # line 363
        for part in newPattern:  # generate new filename  # line 364
            if part.isLiteral:  # line 365
                outname.append(literals[nextliteral].content)  # line 365
                nextliteral += 1  # line 365
            else:  # line 366
                outname.append(globs[nextglob].matches)  # line 366
                nextglob += 1  # line 366
        pairs.append((filename, "".join(outname)))  # line 367
    return pairs  # line 368

@_coconut_tco  # line 370
def reorderRenameActions(actions: '_coconut.typing.Sequence[Tuple[str, str]]', exitOnConflict: 'bool'=True) -> '_coconut.typing.Sequence[Tuple[str, str]]':  # line 370
    ''' Attempt to put all rename actions into an order that avoids target == source names.
      Note, that it's currently not really possible to specify patterns that make this work (swapping "*" elements with a reference).
      An alternative would be to always have one (or all) files renamed to a temporary name before renaming to target filename.
  '''  # line 374
    if not actions:  # line 375
        return []  # line 375
    sources = None  # type: List[str]  # line 376
    targets = None  # type: List[str]  # line 376
    sources, targets = [list(l) for l in zip(*actions)]  # line 377
    last = len(actions)  # type: int  # line 378
    while last > 1:  # line 379
        clean = True  # type: bool  # line 380
        for i in range(1, last):  # line 381
            try:  # line 382
                index = targets[:i].index(sources[i])  # type: int  # line 383
                sources.insert(index, sources.pop(i))  # bubble up the action right before conflict  # line 384
                targets.insert(index, targets.pop(i))  # line 385
                clean = False  # line 386
            except:  # target not found in sources: good!  # line 387
                continue  # target not found in sources: good!  # line 387
        if clean:  # line 388
            break  # line 388
        last -= 1  # we know that the last entry in the list has the least conflicts, so we can disregard it in the next iteration  # line 389
    if exitOnConflict:  # line 390
        for i in range(1, len(actions)):  # line 391
            if sources[i] in targets[:i]:  # line 392
                Exit("There is no order of renaming actions that avoids copying over not-yet renamed files: '%s' is contained in matching source filenames" % (targets[i]))  # line 392
    return _coconut_tail_call(list, zip(sources, targets))  # line 393

def relativize(root: 'str', path: 'str') -> 'Tuple[str, str]':  # line 395
    ''' Determine OS-independent relative folder path, and relative pattern path. '''  # line 396
    relpath = os.path.relpath(os.path.dirname(os.path.abspath(path)), root).replace(os.sep, SLASH)  # line 397
    return relpath, os.path.join(relpath, os.path.basename(path)).replace(os.sep, SLASH)  # line 398

def parseOnlyOptions(root: 'str', options: '_coconut.typing.Sequence[str]') -> 'Tuple[_coconut.typing.Optional[FrozenSet[str]], _coconut.typing.Optional[FrozenSet[str]]]':  # line 400
    ''' Returns set of --only arguments, and set or --except arguments. '''  # line 401
    cwd = os.getcwd()  # type: str  # line 402
    onlys = []  # type: List[str]  # line 403
    excps = []  # type: List[str]  # line 403
    index = 0  # type: int  # line 403
    while True:  # line 404
        try:  # line 405
            index = 1 + listindex(options, "--only", index)  # line 406
            onlys.append(options[index])  # line 407
        except:  # line 408
            break  # line 408
    index = 0  # line 409
    while True:  # line 410
        try:  # line 411
            index = 1 + listindex(options, "--except", index)  # line 412
            excps.append(options[index])  # line 413
        except:  # line 414
            break  # line 414
    return (frozenset((relativize(root, o)[1] for o in onlys)) if onlys else None, frozenset((relativize(root, e)[1] for e in excps)) if excps else None)  # line 415
