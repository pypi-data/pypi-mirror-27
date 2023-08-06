#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# __coconut_hash__ = 0x8a841ccc

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
sys = _coconut_sys  # line 2
import time  # line 2
try:  # line 3
    from typing import Any  # only required for mypy  # line 4
    from typing import Callable  # only required for mypy  # line 4
    from typing import Dict  # only required for mypy  # line 4
    from typing import IO  # only required for mypy  # line 4
    from typing import List  # only required for mypy  # line 4
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
class CallOnce:  # line 13
    ''' This object can be called any time, but will call the wrapped function only once. '''  # line 14
    def __init__(_, func: 'Callable[[], None]') -> 'None':  # line 15
        _.func = func  # type: _coconut.typing.Optional[Callable[[], None]]  # line 15
    def __call__(_) -> 'None':  # sets to None  # line 16
        _.func = _.func() if _.func else None  # sets to None  # line 16

class Accessor(dict):  # line 18
    ''' Dictionary with attribute access. Writing only supported via dictionary access. '''  # line 19
    def __init__(_, mapping: 'Dict[str, Any]') -> 'None':  # line 20
        dict.__init__(_, mapping)  # line 20
    @_coconut_tco  # line 21
    def __getattribute__(_, name: 'str') -> 'Any':  # line 21
        try:  # line 22
            return _[name]  # line 22
        except:  # line 23
            return _coconut_tail_call(dict.__getattribute__, _, name)  # line 23

class Counter:  # line 25
    ''' A simple counter. Can be augmented to return the last value instead. '''  # line 26
    def __init__(_, initial: 'Number'=0) -> 'None':  # line 27
        _.value = initial  # type: Number  # line 27
    def inc(_, by=1) -> 'Number':  # line 28
        _.value += by  # line 28
        return _.value  # line 28

class Logger:  # line 30
    ''' Logger that supports many items. '''  # line 31
    def __init__(_, log):  # line 32
        _._log = log  # line 32
    def debug(_, *s):  # line 33
        _._log.debug(sjoin(*s))  # line 33
    def info(_, *s):  # line 34
        _._log.info(sjoin(*s))  # line 34
    def warn(_, *s):  # line 35
        _._log.warning(sjoin(*s))  # line 35
    def error(_, *s):  # line 36
        _._log.error(sjoin(*s))  # line 36


# Constants
_log = Logger(logging.getLogger(__name__))  # line 40
debug, info, warn, error = _log.debug, _log.info, _log.warn, _log.error  # line 40
UTF8 = "utf_8"  # early used constant, not defined in standard library  # line 41
CONFIGURABLE_FLAGS = ["strict", "track", "picky", "compress"]  # line 42
CONFIGURABLE_LISTS = ["texttype", "bintype", "ignores", "ignoreDirs", "ignoresWhitelist", "ignoreDirsWhitelist"]  # line 43
TRUTH_VALUES = ["true", "yes", "on", "1", "enable", "enabled"]  # all lower-case normalized  # line 44
FALSE_VALUES = ["false", "no", "off", "0", "disable", "disabled"]  # line 45
PROGRESS_MARKER = ["|", "/", "-", "\\"]  # line 46
metaFolder = ".sos"  # type: str  # line 47
metaFile = ".meta"  # type: str  # line 48
bufSize = 1 << 20  # type: int  # 1 MiB  # line 49
SVN = "svn"  # line 50
SLASH = "/"  # line 51
vcsFolders = {".svn": SVN, ".git": "git", ".bzr": "bzr", ".hg": "hg", ".fslckout": "fossil", "_FOSSIL_": "fossil", ".CVS": "cvs"}  # type: Dict[str, str]  # line 52
vcsBranches = {SVN: "trunk", "git": "master", "bzr": "trunk", "hg": "default", "fossil": None, "cvs": None}  # type: Dict[str, _coconut.typing.Optional[str]]  # line 53


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



# Enums
class ConflictResolution:  # prefer their changes, prefer my changes, ask user for each change, go to next deeper level (e.g. from files to lines, characters)  # line 66
    THEIRS, MINE, ASK, NEXT = range(4)  # prefer their changes, prefer my changes, ask user for each change, go to next deeper level (e.g. from files to lines, characters)  # line 66
class MergeOperation:  # insert remote changes into current, remove remote deletions from current, do both (replicate remote state) TODO handle inline-operations separate?  # line 67
    INSERT, REMOVE, BOTH = 1, 2, 3  # insert remote changes into current, remove remote deletions from current, do both (replicate remote state) TODO handle inline-operations separate?  # line 67
class MergeBlockType:  # modify = intra-line changes  # line 68
    KEEP, INSERT, REMOVE, REPLACE, MODIFY, MOVE = range(6)  # modify = intra-line changes  # line 68


# Functions
try:  # line 72
    import chardet  # https://github.com/chardet/chardet  # line 73
    def detectEncoding(binary: 'bytes') -> 'str':  # line 74
        return chardet.detect(binary)["encoding"]  # line 74
except:  # line 75
    def detectEncoding(binary: 'bytes') -> 'str':  # Guess the encoding  # line 76
        ''' Fallback if chardet library missing. '''  # line 77
        try:  # line 78
            binary.decode(UTF8)  # line 78
            return UTF8  # line 78
        except UnicodeError:  # line 79
            pass  # line 79
        try:  # line 80
            binary.decode("utf_16")  # line 80
            return "utf_16"  # line 80
        except UnicodeError:  # line 81
            pass  # line 81
        try:  # line 82
            binary.decode("cp1252")  # line 82
            return "cp1252"  # line 82
        except UnicodeError:  # line 83
            pass  # line 83
        return "ascii"  # this code will never be reached, as above is an 8-bit charset that always matches  # line 84

@_coconut_tco  # line 86
def wcswidth(string: 'str') -> 'int':  # line 86
    l = None  # type: int  # line 87
    try:  # line 88
        l = wcwidth.wcswitdh(string)  # line 89
        if l < 0:  # line 90
            return len(string)  # line 90
    except:  # line 91
        return _coconut_tail_call(len, string)  # line 91
    return l  # line 92

def openIt(file: 'str', mode: 'str', compress: 'bool'=False) -> 'IO':  # Abstraction for opening both compressed and plain files  # line 94
    return bz2.BZ2File(file, mode) if compress else open(file, mode + "b")  # Abstraction for opening both compressed and plain files  # line 94

def eoldet(file: 'bytes') -> '_coconut.typing.Optional[bytes]':  # line 96
    ''' Determine EOL style from a binary string. '''  # line 97
    lf = file.count(b"\n")  # type: int  # line 98
    cr = file.count(b"\r")  # type: int  # line 99
    crlf = file.count(b"\r\n")  # type: int  # line 100
    if crlf > 0:  # DOS/Windows/Symbian etc.  # line 101
        if lf != crlf or cr != crlf:  # line 102
            warn("Inconsistent CR/NL count with CR+NL. Mixed EOL style detected, may cause problems during merge")  # line 102
        return b"\r\n"  # line 103
    if lf != 0 and cr != 0:  # line 104
        warn("Inconsistent CR/NL count without CR+NL. Mixed EOL style detected, may cause problems during merge")  # line 104
    if lf > cr:  # Linux/Unix  # line 105
        return b"\n"  # Linux/Unix  # line 105
    if cr > lf:  # older 8-bit machines  # line 106
        return b"\r"  # older 8-bit machines  # line 106
    return None  # no new line contained, cannot determine  # line 107

def Exit(message: 'str'="") -> 'None':  # line 109
    print("[EXIT] " + message + ".", file=sys.stderr) if str != "" else None  # line 109
    sys.exit(1)  # line 109

@_coconut_tco  # referenceso __builtin__.raw_input on Python 2  # line 111
def user_input(msg: 'str') -> 'str':  # referenceso __builtin__.raw_input on Python 2  # line 111
    return _coconut_tail_call(input, msg)  # referenceso __builtin__.raw_input on Python 2  # line 111

try:  # line 113
    Splittable = TypeVar("Splittable", str, bytes)  # line 113
except:  # Python 2  # line 114
    pass  # Python 2  # line 114
def safeSplit(s: 'Splittable', d: '_coconut.typing.Optional[Splittable]'=None) -> '_coconut.typing.Sequence[Splittable]':  # line 115
    return s.split(("\n" if isinstance(s, str) else b"\n") if d is None else d) if len(s) > 0 else []  # line 115

def ajoin(sep: 'str', seq: '_coconut.typing.Sequence[str]', nl="") -> 'str':  # line 117
    return sep + (nl + sep).join(seq) if seq else ""  # line 117

@_coconut_tco  # line 119
def sjoin(*s: 'Tuple[Any]') -> 'str':  # line 119
    return _coconut_tail_call(" ".join, [str(e) for e in s if e != ''])  # line 119

@_coconut_tco  # line 121
def hashStr(datas: 'str') -> 'str':  # line 121
    return _coconut_tail_call(hashlib.sha256(datas.encode(UTF8)).hexdigest)  # line 121

def modified(changes: 'ChangeSet', onlyBinary: 'bool'=False) -> 'bool':  # line 123
    return len(changes.additions) > 0 or len(changes.deletions) > 0 or len(changes.modifications) > 0  # line 123

def getTermWidth() -> 'int':  # line 125
    try:  # line 125
        import termwidth  # line 126
    except:  # line 127
        return 80  # line 127
    return termwidth.getTermWidth()[0]  # line 128

def hashFile(path: 'str', compress: 'bool', saveTo: '_coconut.typing.Optional[str]'=None) -> 'Tuple[str, longint]':  # line 130
    ''' Calculate hash of file contents, and return compressed sized, if in write mode, or zero. '''  # line 131
    _hash = hashlib.sha256()  # line 132
    wsize = 0  # type: longint  # line 133
    to = openIt(saveTo, "w", compress) if saveTo else None  # line 134
    with open(path, "rb") as fd:  # line 135
        while True:  # line 136
            buffer = fd.read(bufSize)  # line 137
            _hash.update(buffer)  # line 138
            if to:  # line 139
                to.write(buffer)  # line 139
            if len(buffer) < bufSize:  # line 140
                break  # line 140
        if to:  # line 141
            to.close()  # line 142
            wsize = os.stat(saveTo).st_size  # line 143
    return (_hash.hexdigest(), wsize)  # line 144

def firstOfMap(map: 'Dict[str, Any]', params: '_coconut.typing.Sequence[str]', default: 'Any'=None) -> 'Any':  # line 146
    ''' Utility. '''  # line 147
    for k, v in map.items():  # line 148
        if k in params:  # line 149
            return v  # line 149
    return default  # line 150

@_coconut_tco  # line 152
def strftime(timestamp: '_coconut.typing.Optional[int]'=None) -> 'str':  # line 152
    return _coconut_tail_call(time.strftime, "%Y-%m-%d %H:%M:%S", time.localtime(timestamp / 1000. if timestamp is not None else None))  # line 152

def detectAndLoad(filename: '_coconut.typing.Optional[str]'=None, content: '_coconut.typing.Optional[bytes]'=None) -> 'Tuple[str, bytes, _coconut.typing.Sequence[str]]':  # line 154
    encoding = None  # type: str  # line 154
    eol = None  # type: bytes  # line 154
    lines = []  # type: _coconut.typing.Sequence[str]  # line 155
    if filename is not None:  # line 156
        with open(filename, "rb") as fd:  # line 157
            content = fd.read()  # line 157
    encoding = (lambda _coconut_none_coalesce_item: sys.getdefaultencoding() if _coconut_none_coalesce_item is None else _coconut_none_coalesce_item)(detectEncoding(content))  # line 158
    eol = eoldet(content)  # line 159
    if filename is not None:  # line 160
        with codecs.open(filename, encoding=encoding) as fd:  # line 161
            lines = safeSplit(fd.read(), (b"\n" if eol is None else eol).decode(encoding))  # line 161
    elif content is not None:  # line 162
        lines = safeSplit(content.decode(encoding), (b"\n" if eol is None else eol).decode(encoding))  # line 163
    else:  # line 164
        return (sys.getdefaultencoding(), b"\n", [])  # line 164
    return (encoding, eol, lines)  # line 165

def diffPathSets(last: 'Dict[str, PathInfo]', diff: 'Dict[str, PathInfo]') -> 'ChangeSet':  # line 167
    ''' Computes a changeset between in-memory and on-disk file lists.
      Additions contains PathInfo for entries in diff
      Deletions contains PathInfo for entries not anymore in diff
      Modifications contains PathInfo for entries changed from last to diff (new state)
  '''  # line 172
    changes = ChangeSet({}, {}, {})  # type: ChangeSet  # line 173
    for path, pinfo in last.items():  # line 174
        if path not in diff:  # now change  changes.deletions[path] = pinfo; continue  # line 175
            continue  # now change  changes.deletions[path] = pinfo; continue  # line 175
        vs = diff[path]  # reference to potentially changed path set  # line 176
        if vs.size is None:  # marked for deletion  # line 177
            changes.deletions[path] = pinfo  # marked for deletion  # line 177
            continue  # marked for deletion  # line 177
        if pinfo.size == None:  # re-added  # line 178
            changes.additions[path] = pinfo  # re-added  # line 178
            continue  # re-added  # line 178
        if pinfo.size != vs.size or pinfo.mtime != vs.mtime or pinfo.hash != vs.hash:  # not need to make hash comparison optional here  # line 179
            changes.modifications[path] = vs  # not need to make hash comparison optional here  # line 179
    for path, pinfo in diff.items():  # added loop  # line 180
        if path not in last:  # line 181
            changes.additions[path] = pinfo  # line 181
    assert not any([path in changes.deletions for path in changes.additions])  # invariant checks  # line 182
    assert not any([path in changes.additions for path in changes.deletions])  # line 183
    return changes  # line 184

try:  # line 186
    DataType = TypeVar("DataType", ChangeSet, MergeBlock, BranchInfo)  # line 186
except:  # Python 2  # line 187
    pass  # Python 2  # line 187

@_coconut_tco  # line 189
def dataCopy(_tipe: 'Type[DataType]', _old: 'DataType', *_args, **_kwargs) -> 'DataType':  # line 189
    r = _old._asdict()  # line 189
    r.update(**_kwargs)  # line 189
    return _coconut_tail_call(makedata, _tipe, *(list(_args) + [r[field] for field in _old._fields]))  # line 189
# TODO test namedtuple instead of instantiated tuple types in "datatype"?

@_coconut_tco  # line 192
def merge(file: '_coconut.typing.Optional[bytes]'=None, into: '_coconut.typing.Optional[bytes]'=None, filename: '_coconut.typing.Optional[str]'=None, intoname: '_coconut.typing.Optional[str]'=None, mergeOperation=MergeOperation.BOTH, conflictResolution=ConflictResolution.ASK, diffOnly: 'bool'=False) -> 'Union[bytes, List[MergeBlock]]':  # line 192
    ''' Merges binary text contents 'file' into file 'into', returning merged result. '''  # line 193
    encoding = None  # type: str  # line 194
    othr = None  # type: _coconut.typing.Sequence[str]  # line 194
    othreol = None  # type: _coconut.typing.Optional[bytes]  # line 194
    curr = None  # type: _coconut.typing.Sequence[str]  # line 194
    curreol = None  # type: _coconut.typing.Optional[bytes]  # line 194
    differ = difflib.Differ()  # line 195
    try:  # load files line-wise and normalize line endings (keep the one of the current file) TODO document  # line 196
        encoding, othreol, othr = detectAndLoad(filename=filename, content=file)  # line 197
        encoding, curreol, curr = detectAndLoad(filename=intoname, content=into)  # line 198
    except Exception as E:  # line 199
        Exit("Cannot merge '%s' into '%s': %r" % (filename, intoname, E))  # line 199
    if None not in [othreol, curreol] and othreol != curreol:  # line 200
        warn("Differing EOL-styles detected during merge. Using current file's style for merge output")  # line 200
    output = list(differ.compare(othr, curr))  # type: List[str]  # from generator expression  # line 201
    debug("Diff output: " + "".join([o.replace("\n", "\\n") for o in output]))  # line 202
    blocks = []  # type: List[MergeBlock]  # merged result in blocks  # line 203
    tmp = []  # type: List[str]  # block lines  # line 204
    last = " "  # line 205
    for no, line in enumerate(output + ["X"]):  # EOF marker (difflib's output will never be "X" alone)  # line 206
        if line[0] == last:  # continue filling consecutive block, no matter what type of block  # line 207
            tmp.append(line[2:])  # continue filling consecutive block, no matter what type of block  # line 207
            continue  # continue filling consecutive block, no matter what type of block  # line 207
        if line == "X":  # EOF marker - perform action for remaining block  # line 208
            if len(tmp) == 0:  # nothing left to do  # line 209
                break  # nothing left to do  # line 209
        if last == " ":  # block is same in both files  # line 210
            blocks.append(MergeBlock(MergeBlockType.KEEP, [line for line in tmp], line=no - len(tmp)))  # line 211
        elif last == "-":  # may be a deletion or replacement, store for later  # line 212
            blocks.append(MergeBlock(MergeBlockType.REMOVE, [line for line in tmp], line=no - len(tmp)))  # line 213
        elif last == "+":  # may be insertion or replacement  # line 214
            blocks.append(MergeBlock(MergeBlockType.INSERT, [line for line in tmp], line=no - len(tmp)))  # line 215
            if len(blocks) >= 2 and len(blocks[-1].lines) == len(blocks[-2].lines):  # replaces previously removed section entirely if any  # line 216
                if len(blocks[-1].lines) >= 2 or (blocks[-1].changes is None and blocks[-2].changes is None):  # full block or no intra-line comment  # line 217
                    blocks[-2] = MergeBlock(MergeBlockType.REPLACE, blocks[-1].lines, line=no - len(tmp) - 1, replaces=blocks[-2])  # remember replaced stuff TODO why -1 necessary?  # line 218
                else:  # may have intra-line modifications  # line 219
                    blocks[-2] = MergeBlock(MergeBlockType.MODIFY, blocks[-1].lines, line=no - len(tmp), replaces=blocks[-2], changes=blocks[-1].changes)  # line 220
                blocks.pop()  # remove TOS  # line 221
        elif last == "?":  # intra-line change comment  # line 222
            ilm = getIntraLineMarkers(tmp[0])  # tipe is one of MergeBlockType 1, 2, 4. # "? " line includes a trailing \n for some reason  # line 223
            blocks[-1] = dataCopy(MergeBlock, blocks[-1], tipe=MergeBlockType.MODIFY, changes=ilm)  # update to MODIFY, otherwise may be REPLACE instead  # line 224
        last = line[0]  # line 225
        tmp[:] = [line[2:]]  # line 226
    debug("Diff blocks: " + repr(blocks))  # line 227
    if diffOnly:  # line 228
        return blocks  # line 228
    output = []  # line 229
    for block in blocks:  # line 230
        if block.tipe == MergeBlockType.KEEP:  # line 231
            output.extend(block.lines)  # line 232
        elif block.tipe == MergeBlockType.INSERT and not (mergeOperation & MergeOperation.REMOVE):  # line 233
            output.extend(block.lines)  # line 234
        elif block.tipe == MergeBlockType.REPLACE:  # complete block replacement  # line 235
            if mergeOperation & MergeOperation.INSERT:  # replaced stuff TODO allow insertion BEFORE and alternatively AFTER?  # line 236
                output.extend(block.replaces.lines)  # replaced stuff TODO allow insertion BEFORE and alternatively AFTER?  # line 236
            if not (mergeOperation & MergeBlockType.REMOVE):  # if remove, don't add replaced lines, otherwise do  # line 237
                output.extend(block.lines)  # if remove, don't add replaced lines, otherwise do  # line 237
        elif block.tipe == MergeBlockType.REMOVE and mergeOperation & MergeOperation.INSERT:  # line 238
            output.extend(block.lines)  # line 239
        elif block.tipe == MergeBlockType.MODIFY:  # line 240
            if block.changes is not None and block.changes.tipe == MergeBlockType.INSERT:  # cannot be REMOVE, because it's always "-" then "+"  # line 241
                output.extend(block.lines if mergeOperation & MergeOperation.INSERT else block.replaces.lines)  # TODO logic?  # line 242
            elif block.replaces.changes is not None and block.replaces.changes.tipe == MergeBlockType.REMOVE:  # line 243
                output.extend(block.lines if mergeOperation & MergeOperation.REMOVE else block.replaces.lines)  # line 244
            elif block.changes is not None and block.changes.tipe == MergeBlockType.MODIFY:  # always both sides modified, but may differ in markers  # line 245
                if conflictResolution == ConflictResolution.THEIRS:  # line 246
                    output.extend(block.replaces.lines)  # line 247
                elif conflictResolution == ConflictResolution.MINE:  # line 248
                    output.extend(block.lines)  # line 249
                elif conflictResolution == ConflictResolution.ASK:  # line 250
                    print(ajoin("THR ", block.replaces.lines, "\n"))  # line 251
                    print(ajoin("MIN ", block.lines, "\n"))  # line 252
                    reso = {"i": ConflictResolution.MINE, "t": ConflictResolution.THEIRS, "m": ConflictResolution.NEXT, "u": None}.get(user_input(" Resolve: *M[I]ne, [T]heirs, [M]erge, [U]ser defined: ").strip().lower(), ConflictResolution.MINE)  # type: _coconut.typing.Optional[int]  # line 253
                    debug("User selected %d" % reso)  # line 254
                    _coconut_match_check = False  # line 255
                    _coconut_match_to = reso  # line 255
                    if _coconut_match_to is None:  # line 255
                        _coconut_match_check = True  # line 255
                    if _coconut_match_check:  # line 255
                        warn("Manual input not implemented yet")  # TODO allow multi-line input (CTRL+D?)  # line 256
                    _coconut_match_check = False  # line 257
                    _coconut_match_to = reso  # line 257
                    if _coconut_match_to == ConflictResolution.MINE:  # line 257
                        _coconut_match_check = True  # line 257
                    if _coconut_match_check:  # line 257
                        debug("Using mine")  # line 258
                        output.extend(block.lines)  # line 259
                    _coconut_match_check = False  # line 260
                    _coconut_match_to = reso  # line 260
                    if _coconut_match_to == ConflictResolution.THEIRS:  # line 260
                        _coconut_match_check = True  # line 260
                    if _coconut_match_check:  # line 260
                        debug("Using theirs")  # line 261
                        output.extend(block.replaces.lines)  # line 262
                    _coconut_match_check = False  # line 263
                    _coconut_match_to = reso  # line 263
                    if _coconut_match_to == ConflictResolution.NEXT:  # line 263
                        _coconut_match_check = True  # line 263
                    if _coconut_match_check:  # line 263
                        warn("Intra-line merge not implemented yet, skipping line(s)")  # line 264
                        output.extend(block.replaces.lines)  # line 265
            else:  # e.g. contains a deletion, but user was asking for insert only??  # line 266
                warn("Investigate this case")  # line 267
                output.extend(block.lines)  # default or not .replaces?  # line 268
    debug("Merge output: " + "; ".join(output))  # line 269
    nl = b"\n" if othreol is None else othreol if curreol is None else curreol  # type: bytes  # line 270
    return _coconut_tail_call(nl.join, [line.encode(encoding) for line in output])  # returning bytes  # line 271
# TODO handle check for more/less lines in found -/+ blocks to find common section and splitting prefix/suffix out

@_coconut_tco  # line 274
def getIntraLineMarkers(line: 'str') -> 'Range':  # line 274
    ''' Return (type, [affected indices]) of "? "-line diff markers ("? " suffix must be removed). '''  # line 275
    if "^" in line:  # line 276
        return _coconut_tail_call(Range, MergeBlockType.MODIFY, [i for i, c in enumerate(line) if c == "^"])  # line 276
    if "+" in line:  # line 277
        return _coconut_tail_call(Range, MergeBlockType.INSERT, [i for i, c in enumerate(line) if c == "+"])  # line 277
    if "-" in line:  # line 278
        return _coconut_tail_call(Range, MergeBlockType.REMOVE, [i for i, c in enumerate(line) if c == "-"])  # line 278
    return _coconut_tail_call(Range, MergeBlockType.KEEP, [])  # line 279

def findSosVcsBase() -> 'Tuple[_coconut.typing.Optional[str], _coconut.typing.Optional[str], _coconut.typing.Optional[str]]':  # line 281
    ''' Attempts to find sos and legacy VCS base folders. '''  # line 282
    debug("Detecting root folders...")  # line 283
    path = os.getcwd()  # type: str  # start in current folder, check parent until found or stopped  # line 284
    vcs = (None, None)  # type: Tuple[_coconut.typing.Optional[str], _coconut.typing.Optional[str]]  # line 285
    while not os.path.exists(os.path.join(path, metaFolder)):  # line 286
        contents = set(os.listdir(path))  # line 287
        vcss = [executable for folder, executable in vcsFolders.items() if folder in contents]  # type: _coconut.typing.Sequence[str]  # determine VCS type from dot folder  # line 288
        choice = None  # type: _coconut.typing.Optional[str]  # line 289
        if len(vcss) > 1:  # line 290
            choice = SVN if SVN in vcss else vcss[0]  # line 291
            warn("Detected more than one parallel VCS checkouts %r. Falling back to '%s'" % (vcss, choice))  # line 292
        elif len(vcss) > 0:  # line 293
            choice = vcss[0]  # line 293
        if not vcs[0] and choice:  # memorize current repo root  # line 294
            vcs = (path, choice)  # memorize current repo root  # line 294
        new = os.path.dirname(path)  # get parent path  # line 295
        if new == path:  # avoid infinite loop  # line 296
            break  # avoid infinite loop  # line 296
        path = new  # line 297
    if os.path.exists(os.path.join(path, metaFolder)):  # found something  # line 298
        if vcs[0]:  # already detected vcs base and command  # line 299
            return (path, vcs[0], vcs[1])  # already detected vcs base and command  # line 299
        sos = path  # line 300
        while True:  # continue search for VCS base  # line 301
            new = os.path.dirname(path)  # get parent path  # line 302
            if new == path:  # no VCS folder found  # line 303
                return (sos, None, None)  # no VCS folder found  # line 303
            path = new  # line 304
            contents = set(os.listdir(path))  # line 305
            vcss = [executable for folder, executable in vcsFolders.items() if folder in contents]  # determine VCS type  # line 306
            choice = None  # line 307
            if len(vcss) > 1:  # line 308
                choice = SVN if SVN in vcss else vcss[0]  # line 309
                warn("Detected more than one parallel VCS checkouts %r. Falling back to '%s'" % (vcss, choice))  # line 310
            elif len(vcss) > 0:  # line 311
                choice = vcss[0]  # line 311
            if choice:  # line 312
                return (sos, path, choice)  # line 312
    return (None, vcs[0], vcs[1])  # line 313

def relativize(root: 'str', path: 'str') -> 'Tuple[str, str]':  # line 315
    ''' Gets relative path for specified file. '''  # line 316
    relpath = os.path.relpath(os.path.dirname(os.path.abspath(path)), root).replace(os.sep, SLASH)  # line 317
    return relpath, os.path.join(relpath, os.path.basename(path)).replace(os.sep, SLASH)  # line 318

def parseOnlyOptions(root: 'str', options: '_coconut.typing.Sequence[str]') -> 'Tuple[_coconut.typing.Optional[Frozenset[str]], _coconut.typing.Optional[Frozenset[str]]]':  # line 320
    cwd = os.getcwd()  # type: str  # line 321
    onlys = []  # type: _coconut.typing.Sequence[str]  # line 322
    excps = []  # type: _coconut.typing.Sequence[str]  # line 322
    index = 0  # type: int  # line 322
    while True:  # line 323
        try:  # line 324
            index = 1 + options.index("--only", index)  # line 325
            onlys.append(options[index])  # line 326
        except:  # line 327
            break  # line 327
    index = 0  # line 328
    while True:  # line 329
        try:  # line 330
            index = 1 + options.index("--except", index)  # line 331
            excps.append(options[index])  # line 332
        except:  # line 333
            break  # line 333
    return (frozenset((relativize(root, o) for o in onlys)) if onlys else None, frozenset((relativize(root, e) for e in excps)) if excps else None)  # line 334

def conditionalIntersection(a: '_coconut.typing.Optional[FrozenSet[str]]', b: 'FrozenSet[str]') -> 'FrozenSet[str]':  # line 336
    return a & b if a else b  # line 336
