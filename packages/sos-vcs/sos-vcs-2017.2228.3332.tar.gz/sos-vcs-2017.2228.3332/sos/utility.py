#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# __coconut_hash__ = 0x9f76fa91

# Compiled with Coconut version 1.3.1 [Dead Parrot]

# Coconut Header: -------------------------------------------------------------

import sys as _coconut_sys, os.path as _coconut_os_path
_coconut_file_path = _coconut_os_path.dirname(_coconut_os_path.abspath(__file__))
_coconut_sys.path.insert(0, _coconut_file_path)
from __coconut__ import _coconut, _coconut_NamedTuple, _coconut_MatchError, _coconut_tail_call, _coconut_tco, _coconut_igetitem, _coconut_base_compose, _coconut_forward_compose, _coconut_back_compose, _coconut_forward_star_compose, _coconut_back_star_compose, _coconut_pipe, _coconut_star_pipe, _coconut_back_pipe, _coconut_back_star_pipe, _coconut_bool_and, _coconut_bool_or, _coconut_none_coalesce, _coconut_minus, _coconut_map, _coconut_partial
from __coconut__ import *
_coconut_sys.path.remove(_coconut_file_path)

# Compiled Coconut: -----------------------------------------------------------

# Utiliy functions
import bz2  # line 2
import codecs  # line 2
import difflib  # line 2
import hashlib  # line 2
import logging  # line 2
import os  # line 2
import re  # line 2
sys = _coconut_sys  # line 2
import time  # line 2
try:  # line 3
    from typing import Any  # only required for mypy  # line 4
    from typing import Callable  # only required for mypy  # line 4
    from typing import Dict  # only required for mypy  # line 4
    from typing import FrozenSet  # only required for mypy  # line 4
    from typing import IO  # only required for mypy  # line 4
    from typing import List  # only required for mypy  # line 4
    from typing import Sequence  # only required for mypy  # line 4
    from typing import Tuple  # only required for mypy  # line 4
    from typing import Type  # only required for mypy  # line 4
    from typing import TypeVar  # only required for mypy  # line 4
    from typing import Union  # only required for mypy  # line 4
    Number = Union[int, float]  # line 5
except:  # typing not available (e.g. Python 2)  # line 6
    pass  # typing not available (e.g. Python 2)  # line 6
try:  # line 7
    import wcwidth  # line 7
except:  # optional dependency  # line 8
    pass  # optional dependency  # line 8
longint = eval("long") if sys.version_info.major < 3 else int  # type: Type  # for Python 2 compatibility  # line 9


# Classes
class Accessor(dict):  # line 13
    ''' Dictionary with attribute access. Writing only supported via dictionary access. '''  # line 14
    def __init__(_, mapping: 'Dict[str, Any]') -> 'None':  # line 15
        dict.__init__(_, mapping)  # line 15
    @_coconut_tco  # line 16
    def __getattribute__(_, name: 'str') -> 'Any':  # line 16
        try:  # line 17
            return _[name]  # line 17
        except:  # line 18
            return _coconut_tail_call(dict.__getattribute__, _, name)  # line 18

class Counter:  # line 20
    ''' A simple counter. Can be augmented to return the last value instead. '''  # line 21
    def __init__(_, initial: 'Number'=0) -> 'None':  # line 22
        _.value = initial  # type: Number  # line 22
    def inc(_, by=1) -> 'Number':  # line 23
        _.value += by  # line 23
        return _.value  # line 23

class Logger:  # line 25
    ''' Logger that supports many items. '''  # line 26
    def __init__(_, log):  # line 27
        _._log = log  # line 27
    def debug(_, *s):  # line 28
        _._log.debug(sjoin(*s))  # line 28
    def info(_, *s):  # line 29
        _._log.info(sjoin(*s))  # line 29
    def warn(_, *s):  # line 30
        _._log.warning(sjoin(*s))  # line 30
    def error(_, *s):  # line 31
        _._log.error(sjoin(*s))  # line 31


# Constants
_log = Logger(logging.getLogger(__name__))  # line 35
debug, info, warn, error = _log.debug, _log.info, _log.warn, _log.error  # line 35
UTF8 = "utf_8"  # early used constant, not defined in standard library  # line 36
CONFIGURABLE_FLAGS = ["strict", "track", "picky", "compress"]  # line 37
CONFIGURABLE_LISTS = ["texttype", "bintype", "ignores", "ignoreDirs", "ignoresWhitelist", "ignoreDirsWhitelist"]  # line 38
TRUTH_VALUES = ["true", "yes", "on", "1", "enable", "enabled"]  # all lower-case normalized  # line 39
FALSE_VALUES = ["false", "no", "off", "0", "disable", "disabled"]  # line 40
PROGRESS_MARKER = ["|", "/", "-", "\\"]  # line 41
metaFolder = ".sos"  # type: str  # line 42
metaFile = ".meta"  # type: str  # line 43
bufSize = 1 << 20  # type: int  # 1 MiB  # line 44
SVN = "svn"  # line 45
SLASH = "/"  # line 46
vcsFolders = {".svn": SVN, ".git": "git", ".bzr": "bzr", ".hg": "hg", ".fslckout": "fossil", "_FOSSIL_": "fossil", ".CVS": "cvs"}  # type: Dict[str, str]  # line 47
vcsBranches = {SVN: "trunk", "git": "master", "bzr": "trunk", "hg": "default", "fossil": None, "cvs": None}  # type: Dict[str, _coconut.typing.Optional[str]]  # line 48


# Value types
class BranchInfo(_coconut_NamedTuple("BranchInfo", [("number", 'int'), ("ctime", 'int'), ("name", '_coconut.typing.Optional[str]'), ("inSync", 'bool'), ("tracked", 'List[str]')])):  # tracked is a list on purpose, as serialization to JSON needs effort and frequent access is not taking place  # line 52
    __slots__ = ()  # tracked is a list on purpose, as serialization to JSON needs effort and frequent access is not taking place  # line 52
    __ne__ = _coconut.object.__ne__  # tracked is a list on purpose, as serialization to JSON needs effort and frequent access is not taking place  # line 52
    def __new__(_cls, number, ctime, name=None, inSync=False, tracked=[]):  # tracked is a list on purpose, as serialization to JSON needs effort and frequent access is not taking place  # line 52
        return _coconut.tuple.__new__(_cls, (number, ctime, name, inSync, tracked))  # tracked is a list on purpose, as serialization to JSON needs effort and frequent access is not taking place  # line 52
# tracked is a list on purpose, as serialization to JSON needs effort and frequent access is not taking place
class CommitInfo(_coconut_NamedTuple("CommitInfo", [("number", 'int'), ("ctime", 'int'), ("message", '_coconut.typing.Optional[str]')])):  # line 53
    __slots__ = ()  # line 53
    __ne__ = _coconut.object.__ne__  # line 53
    def __new__(_cls, number, ctime, message=None):  # line 53
        return _coconut.tuple.__new__(_cls, (number, ctime, message))  # line 53

class PathInfo(_coconut_NamedTuple("PathInfo", [("nameHash", 'str'), ("size", '_coconut.typing.Optional[int]'), ("mtime", 'int'), ("hash", '_coconut.typing.Optional[str]')])):  # size == None means deleted in this revision  # line 54
    __slots__ = ()  # size == None means deleted in this revision  # line 54
    __ne__ = _coconut.object.__ne__  # size == None means deleted in this revision  # line 54
class ChangeSet(_coconut_NamedTuple("ChangeSet", [("additions", 'Dict[str, PathInfo]'), ("deletions", 'Dict[str, PathInfo]'), ("modifications", 'Dict[str, PathInfo]')])):  # avoid default assignment of {} as it leads to runtime errors (contains data on init for unknown reason)  # line 55
    __slots__ = ()  # avoid default assignment of {} as it leads to runtime errors (contains data on init for unknown reason)  # line 55
    __ne__ = _coconut.object.__ne__  # avoid default assignment of {} as it leads to runtime errors (contains data on init for unknown reason)  # line 55
class Range(_coconut_NamedTuple("Range", [("tipe", 'int'), ("indexes", '_coconut.typing.Sequence[int]')])):  # MergeBlockType[1,2,4], line number, length  # line 56
    __slots__ = ()  # MergeBlockType[1,2,4], line number, length  # line 56
    __ne__ = _coconut.object.__ne__  # MergeBlockType[1,2,4], line number, length  # line 56
class MergeBlock(_coconut_NamedTuple("MergeBlock", [("tipe", 'int'), ("lines", '_coconut.typing.Sequence[str]'), ("line", 'int'), ("replaces", '_coconut.typing.Optional[MergeBlock]'), ("changes", '_coconut.typing.Optional[Range]')])):  # line 57
    __slots__ = ()  # line 57
    __ne__ = _coconut.object.__ne__  # line 57
    def __new__(_cls, tipe, lines, line, replaces=None, changes=None):  # line 57
        return _coconut.tuple.__new__(_cls, (tipe, lines, line, replaces, changes))  # line 57

class GlobBlock(_coconut_NamedTuple("GlobBlock", [("isLiteral", 'bool'), ("content", 'str'), ("index", 'int')])):  # for file pattern rename/move matching  # line 58
    __slots__ = ()  # for file pattern rename/move matching  # line 58
    __ne__ = _coconut.object.__ne__  # for file pattern rename/move matching  # line 58
class GlobBlock2(_coconut_NamedTuple("GlobBlock2", [("isLiteral", 'bool'), ("content", 'str'), ("matches", 'str')])):  # matching file pattern and input filename for translation  # line 59
    __slots__ = ()  # matching file pattern and input filename for translation  # line 59
    __ne__ = _coconut.object.__ne__  # matching file pattern and input filename for translation  # line 59


# Enums
class ConflictResolution:  # prefer their changes, prefer my changes, ask user for each change, go to next deeper level (e.g. from files to lines, characters)  # line 63
    THEIRS, MINE, ASK, NEXT = range(4)  # prefer their changes, prefer my changes, ask user for each change, go to next deeper level (e.g. from files to lines, characters)  # line 63
class MergeOperation:  # insert remote changes into current, remove remote deletions from current, do both (replicate remote state) TODO handle inline-operations separate?  # line 64
    INSERT, REMOVE, BOTH = 1, 2, 3  # insert remote changes into current, remove remote deletions from current, do both (replicate remote state) TODO handle inline-operations separate?  # line 64
class MergeBlockType:  # modify = intra-line changes  # line 65
    KEEP, INSERT, REMOVE, REPLACE, MODIFY, MOVE = range(6)  # modify = intra-line changes  # line 65


# Functions
try:  # line 69
    import chardet  # https://github.com/chardet/chardet  # line 70
    def detectEncoding(binary: 'bytes') -> 'str':  # line 71
        return chardet.detect(binary)["encoding"]  # line 71
except:  # line 72
    def detectEncoding(binary: 'bytes') -> 'str':  # Guess the encoding  # line 73
        ''' Fallback if chardet library missing. '''  # line 74
        try:  # line 75
            binary.decode(UTF8)  # line 75
            return UTF8  # line 75
        except UnicodeError:  # line 76
            pass  # line 76
        try:  # line 77
            binary.decode("utf_16")  # line 77
            return "utf_16"  # line 77
        except UnicodeError:  # line 78
            pass  # line 78
        try:  # line 79
            binary.decode("cp1252")  # line 79
            return "cp1252"  # line 79
        except UnicodeError:  # line 80
            pass  # line 80
        return "ascii"  # this code will never be reached, as above is an 8-bit charset that always matches  # line 81

@_coconut_tco  # line 83
def wcswidth(string: 'str') -> 'int':  # line 83
    l = None  # type: int  # line 84
    try:  # line 85
        l = wcwidth.wcswitdh(string)  # line 86
        if l < 0:  # line 87
            return len(string)  # line 87
    except:  # line 88
        return _coconut_tail_call(len, string)  # line 88
    return l  # line 89

def conditionalIntersection(a: '_coconut.typing.Optional[FrozenSet[str]]', b: 'FrozenSet[str]') -> 'FrozenSet[str]':  # line 91
    return a & b if a else b  # line 91

def openIt(file: 'str', mode: 'str', compress: 'bool'=False) -> 'IO':  # Abstraction for opening both compressed and plain files  # line 93
    return bz2.BZ2File(file, mode) if compress else open(file, mode + "b")  # Abstraction for opening both compressed and plain files  # line 93

def eoldet(file: 'bytes') -> '_coconut.typing.Optional[bytes]':  # line 95
    ''' Determine EOL style from a binary string. '''  # line 96
    lf = file.count(b"\n")  # type: int  # line 97
    cr = file.count(b"\r")  # type: int  # line 98
    crlf = file.count(b"\r\n")  # type: int  # line 99
    if crlf > 0:  # DOS/Windows/Symbian etc.  # line 100
        if lf != crlf or cr != crlf:  # line 101
            warn("Inconsistent CR/NL count with CR+NL. Mixed EOL style detected, may cause problems during merge")  # line 101
        return b"\r\n"  # line 102
    if lf != 0 and cr != 0:  # line 103
        warn("Inconsistent CR/NL count without CR+NL. Mixed EOL style detected, may cause problems during merge")  # line 103
    if lf > cr:  # Linux/Unix  # line 104
        return b"\n"  # Linux/Unix  # line 104
    if cr > lf:  # older 8-bit machines  # line 105
        return b"\r"  # older 8-bit machines  # line 105
    return None  # no new line contained, cannot determine  # line 106

def Exit(message: 'str'="") -> 'None':  # line 108
    print("[EXIT] " + message + ".", file=sys.stderr) if str != "" else None  # line 108
    sys.exit(1)  # line 108

@_coconut_tco  # referenceso __builtin__.raw_input on Python 2  # line 110
def user_input(msg: 'str') -> 'str':  # referenceso __builtin__.raw_input on Python 2  # line 110
    return _coconut_tail_call(input, msg)  # referenceso __builtin__.raw_input on Python 2  # line 110

try:  # line 112
    Splittable = TypeVar("Splittable", str, bytes)  # line 112
except:  # Python 2  # line 113
    pass  # Python 2  # line 113
def safeSplit(s: 'Splittable', d: '_coconut.typing.Optional[Splittable]'=None) -> '_coconut.typing.Sequence[Splittable]':  # line 114
    return s.split(("\n" if isinstance(s, str) else b"\n") if d is None else d) if len(s) > 0 else []  # line 114

def ajoin(sep: 'str', seq: '_coconut.typing.Sequence[str]', nl="") -> 'str':  # line 116
    return (sep + (nl + sep).join(seq)) if seq else ""  # line 116

@_coconut_tco  # line 118
def sjoin(*s: 'Tuple[Any]') -> 'str':  # line 118
    return _coconut_tail_call(" ".join, [str(e) for e in s if e != ''])  # line 118

@_coconut_tco  # line 120
def hashStr(datas: 'str') -> 'str':  # line 120
    return _coconut_tail_call(hashlib.sha256(datas.encode(UTF8)).hexdigest)  # line 120

def modified(changes: 'ChangeSet', onlyBinary: 'bool'=False) -> 'bool':  # line 122
    return len(changes.additions) > 0 or len(changes.deletions) > 0 or len(changes.modifications) > 0  # line 122

def listindex(lizt: 'Sequence[Any]', what: 'Any', index: 'int'=0) -> 'int':  # line 124
    return lizt[index:].index(what) + index  # line 124

def getTermWidth() -> 'int':  # line 126
    try:  # line 126
        import termwidth  # line 127
    except:  # line 128
        return 80  # line 128
    return termwidth.getTermWidth()[0]  # line 129

def hashFile(path: 'str', compress: 'bool', saveTo: '_coconut.typing.Optional[str]'=None) -> 'Tuple[str, longint]':  # line 131
    ''' Calculate hash of file contents, and return compressed sized, if in write mode, or zero. '''  # line 132
    _hash = hashlib.sha256()  # line 133
    wsize = 0  # type: longint  # line 134
    to = openIt(saveTo, "w", compress) if saveTo else None  # line 135
    with open(path, "rb") as fd:  # line 136
        while True:  # line 137
            buffer = fd.read(bufSize)  # line 138
            _hash.update(buffer)  # line 139
            if to:  # line 140
                to.write(buffer)  # line 140
            if len(buffer) < bufSize:  # line 141
                break  # line 141
        if to:  # line 142
            to.close()  # line 143
            wsize = os.stat(saveTo).st_size  # line 144
    return (_hash.hexdigest(), wsize)  # line 145

def firstOfMap(map: 'Dict[str, Any]', params: '_coconut.typing.Sequence[str]', default: 'Any'=None) -> 'Any':  # line 147
    ''' Utility. '''  # line 148
    for k, v in map.items():  # line 149
        if k in params:  # line 150
            return v  # line 150
    return default  # line 151

@_coconut_tco  # line 153
def strftime(timestamp: '_coconut.typing.Optional[int]'=None) -> 'str':  # line 153
    return _coconut_tail_call(time.strftime, "%Y-%m-%d %H:%M:%S", time.localtime(timestamp / 1000. if timestamp is not None else None))  # line 153

def detectAndLoad(filename: '_coconut.typing.Optional[str]'=None, content: '_coconut.typing.Optional[bytes]'=None) -> 'Tuple[str, bytes, _coconut.typing.Sequence[str]]':  # line 155
    encoding = None  # type: str  # line 155
    eol = None  # type: bytes  # line 155
    lines = []  # type: _coconut.typing.Sequence[str]  # line 156
    if filename is not None:  # line 157
        with open(filename, "rb") as fd:  # line 158
            content = fd.read()  # line 158
    encoding = (lambda _coconut_none_coalesce_item: sys.getdefaultencoding() if _coconut_none_coalesce_item is None else _coconut_none_coalesce_item)(detectEncoding(content))  # line 159
    eol = eoldet(content)  # line 160
    if filename is not None:  # line 161
        with codecs.open(filename, encoding=encoding) as fd:  # line 162
            lines = safeSplit(fd.read(), (b"\n" if eol is None else eol).decode(encoding))  # line 162
    elif content is not None:  # line 163
        lines = safeSplit(content.decode(encoding), (b"\n" if eol is None else eol).decode(encoding))  # line 164
    else:  # line 165
        return (sys.getdefaultencoding(), b"\n", [])  # line 165
    return (encoding, eol, lines)  # line 166

def diffPathSets(last: 'Dict[str, PathInfo]', diff: 'Dict[str, PathInfo]') -> 'ChangeSet':  # line 168
    ''' Computes a changeset between in-memory and on-disk file lists.
      Additions contains PathInfo for entries in diff
      Deletions contains PathInfo for entries not anymore in diff
      Modifications contains PathInfo for entries changed from last to diff (new state)
  '''  # line 173
    changes = ChangeSet({}, {}, {})  # type: ChangeSet  # line 174
    for path, pinfo in last.items():  # line 175
        if path not in diff:  # now change  changes.deletions[path] = pinfo; continue  # line 176
            continue  # now change  changes.deletions[path] = pinfo; continue  # line 176
        vs = diff[path]  # reference to potentially changed path set  # line 177
        if vs.size is None:  # marked for deletion  # line 178
            changes.deletions[path] = pinfo  # marked for deletion  # line 178
            continue  # marked for deletion  # line 178
        if pinfo.size == None:  # re-added  # line 179
            changes.additions[path] = pinfo  # re-added  # line 179
            continue  # re-added  # line 179
        if pinfo.size != vs.size or pinfo.mtime != vs.mtime or pinfo.hash != vs.hash:  # not need to make hash comparison optional here  # line 180
            changes.modifications[path] = vs  # not need to make hash comparison optional here  # line 180
    for path, pinfo in diff.items():  # added loop  # line 181
        if path not in last:  # line 182
            changes.additions[path] = pinfo  # line 182
    assert not any([path in changes.deletions for path in changes.additions])  # invariant checks  # line 183
    assert not any([path in changes.additions for path in changes.deletions])  # line 184
    return changes  # line 185

try:  # line 187
    DataType = TypeVar("DataType", ChangeSet, MergeBlock, BranchInfo)  # line 187
except:  # Python 2  # line 188
    pass  # Python 2  # line 188

@_coconut_tco  # line 190
def dataCopy(_tipe: 'Type[DataType]', _old: 'DataType', *_args, **_kwargs) -> 'DataType':  # line 190
    r = _old._asdict()  # line 190
    r.update(**_kwargs)  # line 190
    return _coconut_tail_call(makedata, _tipe, *(list(_args) + [r[field] for field in _old._fields]))  # line 190
# TODO test namedtuple instead of instantiated tuple types in "datatype"?

@_coconut_tco  # line 193
def merge(file: '_coconut.typing.Optional[bytes]'=None, into: '_coconut.typing.Optional[bytes]'=None, filename: '_coconut.typing.Optional[str]'=None, intoname: '_coconut.typing.Optional[str]'=None, mergeOperation=MergeOperation.BOTH, conflictResolution=ConflictResolution.ASK, diffOnly: 'bool'=False) -> 'Union[bytes, List[MergeBlock]]':  # line 193
    ''' Merges binary text contents 'file' into file 'into', returning merged result. '''  # line 194
    encoding = None  # type: str  # line 195
    othr = None  # type: _coconut.typing.Sequence[str]  # line 195
    othreol = None  # type: _coconut.typing.Optional[bytes]  # line 195
    curr = None  # type: _coconut.typing.Sequence[str]  # line 195
    curreol = None  # type: _coconut.typing.Optional[bytes]  # line 195
    differ = difflib.Differ()  # line 196
    try:  # load files line-wise and normalize line endings (keep the one of the current file) TODO document  # line 197
        encoding, othreol, othr = detectAndLoad(filename=filename, content=file)  # line 198
        encoding, curreol, curr = detectAndLoad(filename=intoname, content=into)  # line 199
    except Exception as E:  # line 200
        Exit("Cannot merge '%s' into '%s': %r" % (filename, intoname, E))  # line 200
    if None not in [othreol, curreol] and othreol != curreol:  # line 201
        warn("Differing EOL-styles detected during merge. Using current file's style for merge output")  # line 201
    output = list(differ.compare(othr, curr))  # type: List[str]  # from generator expression  # line 202
    debug("Diff output: " + "".join([o.replace("\n", "\\n") for o in output]))  # line 203
    blocks = []  # type: List[MergeBlock]  # merged result in blocks  # line 204
    tmp = []  # type: List[str]  # block lines  # line 205
    last = " "  # line 206
    for no, line in enumerate(output + ["X"]):  # EOF marker (difflib's output will never be "X" alone)  # line 207
        if line[0] == last:  # continue filling consecutive block, no matter what type of block  # line 208
            tmp.append(line[2:])  # continue filling consecutive block, no matter what type of block  # line 208
            continue  # continue filling consecutive block, no matter what type of block  # line 208
        if line == "X":  # EOF marker - perform action for remaining block  # line 209
            if len(tmp) == 0:  # nothing left to do  # line 210
                break  # nothing left to do  # line 210
        if last == " ":  # block is same in both files  # line 211
            blocks.append(MergeBlock(MergeBlockType.KEEP, [line for line in tmp], line=no - len(tmp)))  # line 212
        elif last == "-":  # may be a deletion or replacement, store for later  # line 213
            blocks.append(MergeBlock(MergeBlockType.REMOVE, [line for line in tmp], line=no - len(tmp)))  # line 214
        elif last == "+":  # may be insertion or replacement  # line 215
            blocks.append(MergeBlock(MergeBlockType.INSERT, [line for line in tmp], line=no - len(tmp)))  # line 216
            if len(blocks) >= 2 and len(blocks[-1].lines) == len(blocks[-2].lines):  # replaces previously removed section entirely if any  # line 217
                if len(blocks[-1].lines) >= 2 or (blocks[-1].changes is None and blocks[-2].changes is None):  # full block or no intra-line comment  # line 218
                    blocks[-2] = MergeBlock(MergeBlockType.REPLACE, blocks[-1].lines, line=no - len(tmp) - 1, replaces=blocks[-2])  # remember replaced stuff TODO why -1 necessary?  # line 219
                else:  # may have intra-line modifications  # line 220
                    blocks[-2] = MergeBlock(MergeBlockType.MODIFY, blocks[-1].lines, line=no - len(tmp), replaces=blocks[-2], changes=blocks[-1].changes)  # line 221
                blocks.pop()  # remove TOS  # line 222
        elif last == "?":  # intra-line change comment  # line 223
            ilm = getIntraLineMarkers(tmp[0])  # tipe is one of MergeBlockType 1, 2, 4. # "? " line includes a trailing \n for some reason  # line 224
            blocks[-1] = dataCopy(MergeBlock, blocks[-1], tipe=MergeBlockType.MODIFY, changes=ilm)  # update to MODIFY, otherwise may be REPLACE instead  # line 225
        last = line[0]  # line 226
        tmp[:] = [line[2:]]  # line 227
    debug("Diff blocks: " + repr(blocks))  # line 228
    if diffOnly:  # line 229
        return blocks  # line 229
    output = []  # line 230
    for block in blocks:  # line 231
        if block.tipe == MergeBlockType.KEEP:  # line 232
            output.extend(block.lines)  # line 233
        elif block.tipe == MergeBlockType.INSERT and not (mergeOperation & MergeOperation.REMOVE):  # line 234
            output.extend(block.lines)  # line 235
        elif block.tipe == MergeBlockType.REPLACE:  # complete block replacement  # line 236
            if mergeOperation & MergeOperation.INSERT:  # replaced stuff TODO allow insertion BEFORE and alternatively AFTER?  # line 237
                output.extend(block.replaces.lines)  # replaced stuff TODO allow insertion BEFORE and alternatively AFTER?  # line 237
            if not (mergeOperation & MergeBlockType.REMOVE):  # if remove, don't add replaced lines, otherwise do  # line 238
                output.extend(block.lines)  # if remove, don't add replaced lines, otherwise do  # line 238
        elif block.tipe == MergeBlockType.REMOVE and mergeOperation & MergeOperation.INSERT:  # line 239
            output.extend(block.lines)  # line 240
        elif block.tipe == MergeBlockType.MODIFY:  # line 241
            if block.changes is not None and block.changes.tipe == MergeBlockType.INSERT:  # cannot be REMOVE, because it's always "-" then "+"  # line 242
                output.extend(block.lines if mergeOperation & MergeOperation.INSERT else block.replaces.lines)  # TODO logic?  # line 243
            elif block.replaces.changes is not None and block.replaces.changes.tipe == MergeBlockType.REMOVE:  # line 244
                output.extend(block.lines if mergeOperation & MergeOperation.REMOVE else block.replaces.lines)  # line 245
            elif block.changes is not None and block.changes.tipe == MergeBlockType.MODIFY:  # always both sides modified, but may differ in markers  # line 246
                if conflictResolution == ConflictResolution.THEIRS:  # line 247
                    output.extend(block.replaces.lines)  # line 248
                elif conflictResolution == ConflictResolution.MINE:  # line 249
                    output.extend(block.lines)  # line 250
                elif conflictResolution == ConflictResolution.ASK:  # line 251
                    print(ajoin("THR ", block.replaces.lines, "\n"))  # line 252
                    print(ajoin("MIN ", block.lines, "\n"))  # line 253
                    reso = {"i": ConflictResolution.MINE, "t": ConflictResolution.THEIRS, "m": ConflictResolution.NEXT, "u": None}.get(user_input(" Resolve: *M[I]ne, [T]heirs, [M]erge, [U]ser defined: ").strip().lower(), ConflictResolution.MINE)  # type: _coconut.typing.Optional[int]  # line 254
                    debug("User selected %d" % reso)  # line 255
                    _coconut_match_check = False  # line 256
                    _coconut_match_to = reso  # line 256
                    if _coconut_match_to is None:  # line 256
                        _coconut_match_check = True  # line 256
                    if _coconut_match_check:  # line 256
                        warn("Manual input not implemented yet")  # TODO allow multi-line input (CTRL+D?)  # line 257
                    _coconut_match_check = False  # line 258
                    _coconut_match_to = reso  # line 258
                    if _coconut_match_to == ConflictResolution.MINE:  # line 258
                        _coconut_match_check = True  # line 258
                    if _coconut_match_check:  # line 258
                        debug("Using mine")  # line 259
                        output.extend(block.lines)  # line 260
                    _coconut_match_check = False  # line 261
                    _coconut_match_to = reso  # line 261
                    if _coconut_match_to == ConflictResolution.THEIRS:  # line 261
                        _coconut_match_check = True  # line 261
                    if _coconut_match_check:  # line 261
                        debug("Using theirs")  # line 262
                        output.extend(block.replaces.lines)  # line 263
                    _coconut_match_check = False  # line 264
                    _coconut_match_to = reso  # line 264
                    if _coconut_match_to == ConflictResolution.NEXT:  # line 264
                        _coconut_match_check = True  # line 264
                    if _coconut_match_check:  # line 264
                        warn("Intra-line merge not implemented yet, skipping line(s)")  # line 265
                        output.extend(block.replaces.lines)  # line 266
            else:  # e.g. contains a deletion, but user was asking for insert only??  # line 267
                warn("Investigate this case")  # line 268
                output.extend(block.lines)  # default or not .replaces?  # line 269
    debug("Merge output: " + "; ".join(output))  # line 270
    nl = b"\n" if othreol is None else othreol if curreol is None else curreol  # type: bytes  # line 271
    return _coconut_tail_call(nl.join, [line.encode(encoding) for line in output])  # returning bytes  # line 272
# TODO handle check for more/less lines in found -/+ blocks to find common section and splitting prefix/suffix out

@_coconut_tco  # line 275
def getIntraLineMarkers(line: 'str') -> 'Range':  # line 275
    ''' Return (type, [affected indices]) of "? "-line diff markers ("? " suffix must be removed). '''  # line 276
    if "^" in line:  # line 277
        return _coconut_tail_call(Range, MergeBlockType.MODIFY, [i for i, c in enumerate(line) if c == "^"])  # line 277
    if "+" in line:  # line 278
        return _coconut_tail_call(Range, MergeBlockType.INSERT, [i for i, c in enumerate(line) if c == "+"])  # line 278
    if "-" in line:  # line 279
        return _coconut_tail_call(Range, MergeBlockType.REMOVE, [i for i, c in enumerate(line) if c == "-"])  # line 279
    return _coconut_tail_call(Range, MergeBlockType.KEEP, [])  # line 280

def findSosVcsBase() -> 'Tuple[_coconut.typing.Optional[str], _coconut.typing.Optional[str], _coconut.typing.Optional[str]]':  # line 282
    ''' Attempts to find sos and legacy VCS base folders. '''  # line 283
    debug("Detecting root folders...")  # line 284
    path = os.getcwd()  # type: str  # start in current folder, check parent until found or stopped  # line 285
    vcs = (None, None)  # type: Tuple[_coconut.typing.Optional[str], _coconut.typing.Optional[str]]  # line 286
    while not os.path.exists(os.path.join(path, metaFolder)):  # line 287
        contents = set(os.listdir(path))  # line 288
        vcss = [executable for folder, executable in vcsFolders.items() if folder in contents]  # type: _coconut.typing.Sequence[str]  # determine VCS type from dot folder  # line 289
        choice = None  # type: _coconut.typing.Optional[str]  # line 290
        if len(vcss) > 1:  # line 291
            choice = SVN if SVN in vcss else vcss[0]  # line 292
            warn("Detected more than one parallel VCS checkouts %r. Falling back to '%s'" % (vcss, choice))  # line 293
        elif len(vcss) > 0:  # line 294
            choice = vcss[0]  # line 294
        if not vcs[0] and choice:  # memorize current repo root  # line 295
            vcs = (path, choice)  # memorize current repo root  # line 295
        new = os.path.dirname(path)  # get parent path  # line 296
        if new == path:  # avoid infinite loop  # line 297
            break  # avoid infinite loop  # line 297
        path = new  # line 298
    if os.path.exists(os.path.join(path, metaFolder)):  # found something  # line 299
        if vcs[0]:  # already detected vcs base and command  # line 300
            return (path, vcs[0], vcs[1])  # already detected vcs base and command  # line 300
        sos = path  # line 301
        while True:  # continue search for VCS base  # line 302
            new = os.path.dirname(path)  # get parent path  # line 303
            if new == path:  # no VCS folder found  # line 304
                return (sos, None, None)  # no VCS folder found  # line 304
            path = new  # line 305
            contents = set(os.listdir(path))  # line 306
            vcss = [executable for folder, executable in vcsFolders.items() if folder in contents]  # determine VCS type  # line 307
            choice = None  # line 308
            if len(vcss) > 1:  # line 309
                choice = SVN if SVN in vcss else vcss[0]  # line 310
                warn("Detected more than one parallel VCS checkouts %r. Falling back to '%s'" % (vcss, choice))  # line 311
            elif len(vcss) > 0:  # line 312
                choice = vcss[0]  # line 312
            if choice:  # line 313
                return (sos, path, choice)  # line 313
    return (None, vcs[0], vcs[1])  # line 314

def tokenizeGlobPattern(pattern: 'str') -> 'List[GlobBlock]':  # line 316
    index = 0  # type: int  # line 317
    out = []  # type: List[GlobBlock]  # literal = True, first index  # line 318
    while index < len(pattern):  # line 319
        if pattern[index:index + 3] in ("[?]", "[*]", "[[]", "[]]"):  # line 320
            out.append(GlobBlock(False, pattern[index:index + 3], index))  # line 320
            continue  # line 320
        if pattern[index] in "*?":  # line 321
            count = 1  # type: int  # line 322
            while index + count < len(pattern) and pattern[index] == "?" and pattern[index + count] == "?":  # line 323
                count += 1  # line 323
            out.append(GlobBlock(False, pattern[index:index + count], index))  # line 324
            index += count  # line 324
            continue  # line 324
        if pattern[index:index + 2] == "[!":  # line 325
            out.append(GlobBlock(False, pattern[index:pattern.index("]", index + 2) + 1], index))  # line 325
            index += len(out[-1][1])  # line 325
            continue  # line 325
        count = 1  # line 326
        while index + count < len(pattern) and pattern[index + count] not in "*?[":  # line 327
            count += 1  # line 327
        out.append(GlobBlock(True, pattern[index:index + count], index))  # line 328
        index += count  # line 328
# TODO [abc]
    return out  # line 330

def tokenizeGlobPatterns(oldPattern: 'str', newPattern: 'str') -> 'Tuple[_coconut.typing.Sequence[GlobBlock], _coconut.typing.Sequence[GlobBlock]]':  # line 332
    ot = tokenizeGlobPattern(oldPattern)  # type: List[GlobBlock]  # line 333
    nt = tokenizeGlobPattern(newPattern)  # type: List[GlobBlock]  # line 334
#  if len(ot) != len(nt): Exit("Source and target patterns can't be translated due to differing number of parsed glob markers and literal strings")
    if len([o for o in ot if not o.isLiteral]) < len([n for n in nt if not n.isLiteral]):  # line 336
        Exit("Source and target file patterns contain differing number of glob markers and can't be translated")  # line 336
    if any((O.content != N.content for O, N in zip([o for o in ot if not o.isLiteral], [n for n in nt if not n.isLiteral]))):  # line 337
        Exit("Source and target file patterns differ in semantics")  # line 337
    return (ot, nt)  # line 338

def convertGlobFiles(filenames: '_coconut.typing.Sequence[str]', oldPattern: '_coconut.typing.Sequence[GlobBlock]', newPattern: '_coconut.typing.Sequence[GlobBlock]') -> '_coconut.typing.Sequence[Tuple[str, str]]':  # line 340
    ''' Converts given filename according to specified file patterns. No support for adjacent glob markers currently. '''  # TODO use list of filenames instead  # line 341
    pairs = []  # type: List[Tuple[str, str]]  # line 342
    for filename in filenames:  # line 343
        literals = [l for l in oldPattern if l.isLiteral]  # type: List[GlobBlock]  # source literals  # line 344
        nextliteral = 0  # type: int  # line 345
        parsedOld = []  # type: List[GlobBlock2]  # line 346
        index = 0  # type: int  # line 347
        for part in oldPattern:  # match everything in the old filename  # line 348
            if part.isLiteral:  # line 349
                parsedOld.append(GlobBlock2(True, part.content, part.content))  # line 349
                index += len(part.content)  # line 349
                nextliteral += 1  # line 349
            elif part.content.startswith("?"):  # line 350
                parsedOld.append(GlobBlock2(False, part.content, filename[index:index + len(part.content)]))  # line 350
                index += len(part.content)  # line 350
            elif part.content.startswith("["):  # line 351
                parsedOld.append(GlobBlock2(False, part.content, filename[index]))  # line 351
                index += 1  # line 351
            elif part.content == "*":  # line 352
                if nextliteral >= len(literals):  # line 353
                    parsedOld.append(GlobBlock2(False, part.content, filename[index:]))  # line 353
                    break  # line 353
                nxt = filename.index(literals[nextliteral].content, index)  # type: int  # also matches empty string  # line 354
                parsedOld.append(GlobBlock2(False, part.content, filename[index:nxt]))  # line 355
                index = nxt  # line 355
            else:  # line 356
                Exit("Invalid file pattern specified for move/rename")  # line 356
        globs = [g for g in parsedOld if not g.isLiteral]  # type: List[GlobBlock2]  # line 357
        literals = [l for l in newPattern if l.isLiteral]  # target literals  # line 358
        nextliteral = 0  # line 359
        nextglob = 0  # type: int  # line 359
        outname = ""  # type: str  # TODO join a list instead?  # line 360
        for part in newPattern:  # generate new filename  # line 361
            if part.isLiteral:  # line 362
                outname += literals[nextliteral].content  # line 362
                nextliteral += 1  # line 362
            else:  # line 363
                outname += globs[nextglob].matches  # line 363
                nextglob += 1  # line 363
        pairs.append((filename, outname))  # line 364
    return pairs  # line 365

@_coconut_tco  # line 367
def reorderRenameActions(actions: '_coconut.typing.Sequence[Tuple[str, str]]', exitOnConflict: 'bool'=True) -> '_coconut.typing.Sequence[Tuple[str, str]]':  # line 367
    ''' Attempt to put all rename actions into an order that avoids target == source names.
      Note, that it's currently not really possible to specify patterns that make this work (swapping "*" elements with a reference).
      An alternative would be to always have one (or all) files renamed to a temporary name before renaming to target filename.
  '''  # line 371
    if not actions:  # line 372
        return []  # line 372
    sources = None  # type: List[str]  # line 373
    targets = None  # type: List[str]  # line 373
    sources, targets = [list(l) for l in zip(*actions)]  # line 374
    last = len(actions)  # type: int  # line 375
    while last > 1:  # line 376
        clean = True  # type: bool  # line 377
        for i in range(1, last):  # line 378
            try:  # line 379
                index = targets[:i].index(sources[i])  # type: int  # TODO not correct? consider entries further down to push up  # line 380
                sources.insert(index, sources.pop(i))  # bubble up the action right before conflict  # line 381
                targets.insert(index, targets.pop(i))  # line 382
                clean = False  # line 383
            except:  # target not found in sources: good!  # line 384
                continue  # target not found in sources: good!  # line 384
        if clean:  # line 385
            break  # line 385
        last -= 1  # we know that the last entry in the list has the least conflicts, so we can disregard it in the next iteration  # line 386
    if exitOnConflict:  # line 387
        for i in range(1, len(actions)):  # line 388
            if sources[i] in targets[:i]:  # line 389
                Exit("There is no order of renaming actions that avoids copying over not-yet renamed files: '%s' is contained in matching source filenames" % (targets[i]))  # line 389
    return _coconut_tail_call(list, zip(sources, targets))  # line 390

def relativize(root: 'str', path: 'str') -> 'Tuple[str, str]':  # line 392
    ''' Determine OS-independent relative folder path, and relative pattern path. '''  # line 393
    relpath = os.path.relpath(os.path.dirname(os.path.abspath(path)), root).replace(os.sep, SLASH)  # line 394
    return relpath, os.path.join(relpath, os.path.basename(path)).replace(os.sep, SLASH)  # line 395

def parseOnlyOptions(root: 'str', options: '_coconut.typing.Sequence[str]') -> 'Tuple[_coconut.typing.Optional[FrozenSet[str]], _coconut.typing.Optional[FrozenSet[str]]]':  # line 397
    ''' Returns set of --only arguments, and set or --except arguments. '''  # line 398
    cwd = os.getcwd()  # type: str  # line 399
    onlys = []  # type: List[str]  # line 400
    excps = []  # type: List[str]  # line 400
    index = 0  # type: int  # line 400
    while True:  # line 401
        try:  # line 402
            index = 1 + listindex(options, "--only", index)  # line 403
            onlys.append(options[index])  # line 404
        except:  # line 405
            break  # line 405
    index = 0  # line 406
    while True:  # line 407
        try:  # line 408
            index = 1 + listindex(options, "--except", index)  # line 409
            excps.append(options[index])  # line 410
        except:  # line 411
            break  # line 411
    return (frozenset((relativize(root, o)[1] for o in onlys)) if onlys else None, frozenset((relativize(root, e)[1] for e in excps)) if excps else None)  # line 412
