#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# __coconut_hash__ = 0xe018bb66

# Compiled with Coconut version 1.3.1-post_dev8 [Dead Parrot]

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
class JustOnce:  # line 13
    def __init__(_, value: 'str', depleted: 'str'="") -> 'None':  # line 14
        _.value = value  # type: str  # line 14
        _.depleted = depleted  # line 14
    def __call__(_) -> 'str':  # line 15
        value = _.value  # line 15
        _.value = None  # line 15
        return _.depleted if value is None else value  # line 15

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
    def __init__(_, initial: 'Number'=0) -> 'None':  # line 25
        _.value = initial  # type: Number  # line 25
    def inc(_, by=1) -> 'Number':  # line 26
        _.value += by  # line 26
        return _.value  # line 26

class Logger:  # line 28
    ''' Logger that supports many items. '''  # line 29
    def __init__(_, log):  # line 30
        _._log = log  # line 30
    def debug(_, *s):  # line 31
        _._log.debug(sjoin(*s))  # line 31
    def info(_, *s):  # line 32
        _._log.info(sjoin(*s))  # line 32
    def warn(_, *s):  # line 33
        _._log.warning(sjoin(*s))  # line 33
    def error(_, *s):  # line 34
        _._log.error(sjoin(*s))  # line 34


# Constants
_log = Logger(logging.getLogger(__name__))  # line 38
debug, info, warn, error = _log.debug, _log.info, _log.warn, _log.error  # line 38
UTF8 = "utf_8"  # early used constant, not defined in standard library  # line 39
CONFIGURABLE_FLAGS = ["strict", "track", "picky", "compress"]  # line 40
CONFIGURABLE_LISTS = ["texttype", "bintype", "ignores", "ignoreDirs", "ignoresWhitelist", "ignoreDirsWhitelist"]  # line 41
TRUTH_VALUES = ["true", "yes", "on", "1", "enable", "enabled"]  # all lower-case normalized  # line 42
FALSE_VALUES = ["false", "no", "off", "0", "disable", "disabled"]  # line 43
PROGRESS_MARKER = ["|", "/", "-", "\\"]  # line 44
metaFolder = ".sos"  # type: str  # line 45
metaFile = ".meta"  # type: str  # line 46
bufSize = 1 << 20  # type: int  # 1 MiB  # line 47
SVN = "svn"  # line 48
SLASH = "/"  # line 49
vcsFolders = {".svn": SVN, ".git": "git", ".bzr": "bzr", ".hg": "hg", ".fslckout": "fossil", "_FOSSIL_": "fossil", ".CVS": "cvs"}  # type: Dict[str, str]  # line 50
vcsBranches = {SVN: "trunk", "git": "master", "bzr": "trunk", "hg": "default", "fossil": None, "cvs": None}  # type: Dict[str, _coconut.typing.Optional[str]]  # line 51


# Value types
class BranchInfo(_coconut_NamedTuple("BranchInfo", [("number", 'int'), ("ctime", 'int'), ("name", '_coconut.typing.Optional[str]'), ("insync", 'bool'), ("tracked", 'List[str]')])):  # tracked is a list on purpose, as serialization to JSON needs effort and frequent access is not taking place  # line 55
    __slots__ = ()  # tracked is a list on purpose, as serialization to JSON needs effort and frequent access is not taking place  # line 55
    __ne__ = _coconut.object.__ne__  # tracked is a list on purpose, as serialization to JSON needs effort and frequent access is not taking place  # line 55
    def __new__(_cls, number, ctime, name=None, insync=False, tracked=[]):  # tracked is a list on purpose, as serialization to JSON needs effort and frequent access is not taking place  # line 55
        return _coconut.tuple.__new__(_cls, (number, ctime, name, insync, tracked))  # tracked is a list on purpose, as serialization to JSON needs effort and frequent access is not taking place  # line 55
# tracked is a list on purpose, as serialization to JSON needs effort and frequent access is not taking place
class CommitInfo(_coconut_NamedTuple("CommitInfo", [("number", 'int'), ("ctime", 'int'), ("message", '_coconut.typing.Optional[str]')])):  # line 56
    __slots__ = ()  # line 56
    __ne__ = _coconut.object.__ne__  # line 56
    def __new__(_cls, number, ctime, message=None):  # line 56
        return _coconut.tuple.__new__(_cls, (number, ctime, message))  # line 56

class PathInfo(_coconut_NamedTuple("PathInfo", [("namehash", 'str'), ("size", '_coconut.typing.Optional[int]'), ("mtime", 'int'), ("hash", '_coconut.typing.Optional[str]')])):  # size == None means deleted in this revision  # line 57
    __slots__ = ()  # size == None means deleted in this revision  # line 57
    __ne__ = _coconut.object.__ne__  # size == None means deleted in this revision  # line 57
class ChangeSet(_coconut_NamedTuple("ChangeSet", [("additions", 'Dict[str, PathInfo]'), ("deletions", 'Dict[str, PathInfo]'), ("modifications", 'Dict[str, PathInfo]')])):  # avoid default assignment of {} as it leads to runtime errors (contains data on init for unknown reason)  # line 58
    __slots__ = ()  # avoid default assignment of {} as it leads to runtime errors (contains data on init for unknown reason)  # line 58
    __ne__ = _coconut.object.__ne__  # avoid default assignment of {} as it leads to runtime errors (contains data on init for unknown reason)  # line 58
class Range(_coconut_NamedTuple("Range", [("tipe", 'int'), ("indexes", '_coconut.typing.Sequence[int]')])):  # MergeBlockType[1,2,4], line number, length  # line 59
    __slots__ = ()  # MergeBlockType[1,2,4], line number, length  # line 59
    __ne__ = _coconut.object.__ne__  # MergeBlockType[1,2,4], line number, length  # line 59
class MergeBlock(_coconut_NamedTuple("MergeBlock", [("tipe", 'int'), ("lines", '_coconut.typing.Sequence[str]'), ("line", 'int'), ("replaces", '_coconut.typing.Optional[MergeBlock]'), ("changes", '_coconut.typing.Optional[Range]')])):  # line 60
    __slots__ = ()  # line 60
    __ne__ = _coconut.object.__ne__  # line 60
    def __new__(_cls, tipe, lines, line, replaces=None, changes=None):  # line 60
        return _coconut.tuple.__new__(_cls, (tipe, lines, line, replaces, changes))  # line 60



# Enums
class ConflictResolution:  # prefer their changes, prefer my changes, ask user for each change, go to next deeper level (e.g. from files to lines, characters)  # line 64
    THEIRS, MINE, ASK, NEXT = range(4)  # prefer their changes, prefer my changes, ask user for each change, go to next deeper level (e.g. from files to lines, characters)  # line 64
class MergeOperation:  # insert remote changes into current, remove remote deletions from current, do both (replicate remote state) TODO handle inline-operations separate?  # line 65
    INSERT, REMOVE, BOTH = 1, 2, 3  # insert remote changes into current, remove remote deletions from current, do both (replicate remote state) TODO handle inline-operations separate?  # line 65
class MergeBlockType:  # modify = intra-line changes  # line 66
    KEEP, INSERT, REMOVE, REPLACE, MODIFY, MOVE = range(6)  # modify = intra-line changes  # line 66


# Functions
try:  # line 70
    import chardet  # https://github.com/chardet/chardet  # line 71
    def detectEncoding(binary: 'bytes') -> 'str':  # line 72
        return chardet.detect(binary)["encoding"]  # line 72
except:  # line 73
    def detectEncoding(binary: 'bytes') -> 'str':  # Guess the encoding  # line 74
        ''' Fallback if chardet library missing. '''  # line 75
        try:  # line 76
            binary.decode(UTF8)  # line 76
            return UTF8  # line 76
        except UnicodeError:  # line 77
            pass  # line 77
        try:  # line 78
            binary.decode("utf_16")  # line 78
            return "utf_16"  # line 78
        except UnicodeError:  # line 79
            pass  # line 79
        try:  # line 80
            binary.decode("cp1252")  # line 80
            return "cp1252"  # line 80
        except UnicodeError:  # line 81
            pass  # line 81
        return "ascii"  # this code will never be reached, as above is an 8-bit charset that always matches  # line 82

@_coconut_tco  # line 84
def wcswidth(string: 'str') -> 'int':  # line 84
    l = None  # type: int  # line 85
    try:  # line 86
        l = wcwidth.wcswitdh(string)  # line 87
        if l < 0:  # line 88
            return len(string)  # line 88
    except:  # line 89
        return _coconut_tail_call(len, string)  # line 89
    return l  # line 90

def openIt(file: 'str', mode: 'str', compress: 'bool'=False) -> 'IO':  # Abstraction for opening both compressed and plain files  # line 92
    return bz2.BZ2File(file, mode) if compress else open(file, mode + "b")  # Abstraction for opening both compressed and plain files  # line 92

def eoldet(file: 'bytes') -> '_coconut.typing.Optional[bytes]':  # line 94
    ''' Determine EOL style from a binary string. '''  # line 95
    lf = file.count(b"\n")  # type: int  # line 96
    cr = file.count(b"\r")  # type: int  # line 97
    crlf = file.count(b"\r\n")  # type: int  # line 98
    if crlf > 0:  # DOS/Windows/Symbian etc.  # line 99
        if lf != crlf or cr != crlf:  # line 100
            warn("Inconsistent CR/NL count with CR+NL. Mixed EOL style detected, may cause problems during merge")  # line 100
        return b"\r\n"  # line 101
    if lf != 0 and cr != 0:  # line 102
        warn("Inconsistent CR/NL count without CR+NL. Mixed EOL style detected, may cause problems during merge")  # line 102
    if lf > cr:  # Linux/Unix  # line 103
        return b"\n"  # Linux/Unix  # line 103
    if cr > lf:  # older 8-bit machines  # line 104
        return b"\r"  # older 8-bit machines  # line 104
    return None  # no new line contained, cannot determine  # line 105

def Exit(message: 'str'="") -> 'None':  # line 107
    print(message, file=sys.stderr)  # line 107
    sys.exit(1)  # line 107

@_coconut_tco  # referenceso __builtin__.raw_input on Python 2  # line 109
def user_input(msg: 'str') -> 'str':  # referenceso __builtin__.raw_input on Python 2  # line 109
    return _coconut_tail_call(input, msg)  # referenceso __builtin__.raw_input on Python 2  # line 109

try:  # line 111
    Splittable = TypeVar("Splittable", str, bytes)  # line 111
except:  # Python 2  # line 112
    pass  # Python 2  # line 112
def safeSplit(s: 'Splittable', d: '_coconut.typing.Optional[Splittable]'=None) -> '_coconut.typing.Sequence[Splittable]':  # line 113
    return s.split(("\n" if isinstance(s, str) else b"\n") if d is None else d) if len(s) > 0 else []  # line 113

def ajoin(sep: 'str', seq: '_coconut.typing.Sequence[str]', nl="") -> 'str':  # line 115
    return sep + (nl + sep).join(seq) if seq else ""  # line 115

@_coconut_tco  # line 117
def sjoin(*s: 'Tuple[Any]') -> 'str':  # line 117
    return _coconut_tail_call(" ".join, [str(e) for e in s if e != ''])  # line 117

@_coconut_tco  # line 119
def hashStr(datas: 'str') -> 'str':  # line 119
    return _coconut_tail_call(hashlib.sha256(datas.encode(UTF8)).hexdigest)  # line 119

def modified(changes: 'ChangeSet', onlyBinary: 'bool'=False) -> 'bool':  # line 121
    return len(changes.additions) > 0 or len(changes.deletions) > 0 or len(changes.modifications) > 0  # line 121

def getTermWidth() -> 'int':  # line 123
    try:  # line 124
        import termwidth  # line 124
    except:  # line 125
        return 80  # line 125
    return termwidth.getTermWidth()[0]  # line 126

def hashFile(path: 'str', compress: 'bool', saveTo: '_coconut.typing.Optional[str]'=None) -> 'Tuple[str, longint]':  # line 128
    ''' Calculate hash of file contents, and return compressed sized, if in write mode, or zero. '''  # line 129
    _hash = hashlib.sha256()  # line 130
    wsize = 0  # type: longint  # line 131
    to = openIt(saveTo, "w", compress) if saveTo else None  # line 132
    with open(path, "rb") as fd:  # line 133
        while True:  # line 134
            buffer = fd.read(bufSize)  # line 135
            _hash.update(buffer)  # line 136
            if to:  # line 137
                to.write(buffer)  # line 137
            if len(buffer) < bufSize:  # line 138
                break  # line 138
        if to:  # line 139
            to.close()  # line 140
            wsize = os.stat(saveTo).st_size  # line 141
    return (_hash.hexdigest(), wsize)  # line 142

def firstOfMap(map: 'Dict[str, Any]', params: '_coconut.typing.Sequence[str]', default: 'Any'=None) -> 'Any':  # line 144
    ''' Utility. '''  # line 145
    for k, v in map.items():  # line 146
        if k in params:  # line 147
            return v  # line 147
    return default  # line 148

@_coconut_tco  # line 150
def strftime(timestamp: '_coconut.typing.Optional[int]'=None) -> 'str':  # line 150
    return _coconut_tail_call(time.strftime, "%Y-%m-%d %H:%M:%S", time.localtime(timestamp / 1000. if timestamp is not None else None))  # line 150

def detectAndLoad(filename: '_coconut.typing.Optional[str]'=None, content: '_coconut.typing.Optional[bytes]'=None) -> 'Tuple[str, bytes, _coconut.typing.Sequence[str]]':  # line 152
    encoding = None  # type: str  # line 153
    eol = None  # type: bytes  # line 153
    lines = []  # type: _coconut.typing.Sequence[str]  # line 153
    if filename is not None:  # line 154
        with open(filename, "rb") as fd:  # line 155
            content = fd.read()  # line 155
    encoding = (lambda _coconut_none_coalesce_item: sys.getdefaultencoding() if _coconut_none_coalesce_item is None else _coconut_none_coalesce_item)(detectEncoding(content))  # line 156
    eol = eoldet(content)  # line 157
    if filename is not None:  # line 158
        with codecs.open(filename, encoding=encoding) as fd:  # line 159
            lines = safeSplit(fd.read(), (b"\n" if eol is None else eol).decode(encoding))  # line 159
    elif content is not None:  # line 160
        lines = safeSplit(content.decode(encoding), (b"\n" if eol is None else eol).decode(encoding))  # line 161
    else:  # line 162
        return (sys.getdefaultencoding(), b"\n", [])  # line 162
    return (encoding, eol, lines)  # line 163

def diffPathSets(last: 'Dict[str, PathInfo]', diff: 'Dict[str, PathInfo]') -> 'ChangeSet':  # line 165
    ''' Computes a changeset between in-memory and on-disk file lists.
      Additions contains PathInfo for entries in diff
      Deletions contains PathInfo for entries not anymore in diff
      Modifications contains PathInfo for entries changed from last to diff (new state)
  '''  # line 170
    changes = ChangeSet({}, {}, {})  # type: ChangeSet  # line 171
    for path, pinfo in last.items():  # line 172
        if path not in diff:  # now change  changes.deletions[path] = pinfo; continue  # line 173
            continue  # now change  changes.deletions[path] = pinfo; continue  # line 173
        vs = diff[path]  # reference to potentially changed path set  # line 174
        if vs.size is None:  # marked for deletion  # line 175
            changes.deletions[path] = pinfo  # marked for deletion  # line 175
            continue  # marked for deletion  # line 175
        if pinfo.size == None:  # re-added  # line 176
            changes.additions[path] = pinfo  # re-added  # line 176
            continue  # re-added  # line 176
        if pinfo.size != vs.size or pinfo.mtime != vs.mtime or pinfo.hash != vs.hash:  # not need to make hash comparison optional here  # line 177
            changes.modifications[path] = vs  # not need to make hash comparison optional here  # line 177
    for path, pinfo in diff.items():  # added loop  # line 178
        if path not in last:  # line 179
            changes.additions[path] = pinfo  # line 179
    assert not any([path in changes.deletions for path in changes.additions])  # invariant checks  # line 180
    assert not any([path in changes.additions for path in changes.deletions])  # line 181
    return changes  # line 182

try:  # line 184
    DataType = TypeVar("DataType", ChangeSet, MergeBlock, BranchInfo)  # line 184
except:  # Python 2  # line 185
    pass  # Python 2  # line 185

@_coconut_tco  # line 187
def dataCopy(_tipe: 'Type[DataType]', _old: 'DataType', *_args, **_kwargs) -> 'DataType':  # line 187
    r = _old._asdict()  # line 187
    r.update(**_kwargs)  # line 187
    return _coconut_tail_call(makedata, _tipe, *(list(_args) + [r[field] for field in _old._fields]))  # line 187
# TODO test namedtuple instead of instantiated tuple types in "datatype"?

@_coconut_tco  # line 190
def merge(file: '_coconut.typing.Optional[bytes]'=None, into: '_coconut.typing.Optional[bytes]'=None, filename: '_coconut.typing.Optional[str]'=None, intoname: '_coconut.typing.Optional[str]'=None, mergeOperation=MergeOperation.BOTH, conflictResolution=ConflictResolution.ASK, diffOnly: 'bool'=False) -> 'Union[bytes, List[MergeBlock]]':  # line 190
    ''' Merges binary text contents 'file' into file 'into', returning merged result. '''  # line 191
    encoding = None  # type: str  # line 192
    othr = None  # type: _coconut.typing.Sequence[str]  # line 192
    othreol = None  # type: _coconut.typing.Optional[bytes]  # line 192
    curr = None  # type: _coconut.typing.Sequence[str]  # line 192
    curreol = None  # type: _coconut.typing.Optional[bytes]  # line 192
    differ = difflib.Differ()  # line 193
    try:  # load files line-wise and normalize line endings (keep the one of the current file) TODO document  # line 194
        encoding, othreol, othr = detectAndLoad(filename=filename, content=file)  # line 195
        encoding, curreol, curr = detectAndLoad(filename=intoname, content=into)  # line 196
    except Exception as E:  # line 197
        Exit("Cannot merge '%s' into '%s': %r" % (filename, intoname, E))  # line 197
    if None not in [othreol, curreol] and othreol != curreol:  # line 198
        warn("Differing EOL-styles detected during merge. Using current file's style for merge output")  # line 198
    output = list(differ.compare(othr, curr))  # type: List[str]  # from generator expression  # line 199
    debug("Diff output: " + "".join([o.replace("\n", "\\n") for o in output]))  # line 200
    blocks = []  # type: List[MergeBlock]  # merged result in blocks  # line 201
    tmp = []  # type: List[str]  # block lines  # line 202
    last = " "  # line 203
    for no, line in enumerate(output + ["X"]):  # EOF marker (difflib's output will never be "X" alone)  # line 204
        if line[0] == last:  # continue filling consecutive block, no matter what type of block  # line 205
            tmp.append(line[2:])  # continue filling consecutive block, no matter what type of block  # line 205
            continue  # continue filling consecutive block, no matter what type of block  # line 205
        if line == "X":  # EOF marker - perform action for remaining block  # line 206
            if len(tmp) == 0:  # nothing left to do  # line 207
                break  # nothing left to do  # line 207
        if last == " ":  # block is same in both files  # line 208
            blocks.append(MergeBlock(MergeBlockType.KEEP, [line for line in tmp], line=no - len(tmp)))  # line 209
        elif last == "-":  # may be a deletion or replacement, store for later  # line 210
            blocks.append(MergeBlock(MergeBlockType.REMOVE, [line for line in tmp], line=no - len(tmp)))  # line 211
        elif last == "+":  # may be insertion or replacement  # line 212
            blocks.append(MergeBlock(MergeBlockType.INSERT, [line for line in tmp], line=no - len(tmp)))  # line 213
            if len(blocks) >= 2 and len(blocks[-1].lines) == len(blocks[-2].lines):  # replaces previously removed section entirely if any  # line 214
                if len(blocks[-1].lines) >= 2 or (blocks[-1].changes is None and blocks[-2].changes is None):  # full block or no intra-line comment  # line 215
                    blocks[-2] = MergeBlock(MergeBlockType.REPLACE, blocks[-1].lines, line=no - len(tmp) - 1, replaces=blocks[-2])  # remember replaced stuff TODO why -1 necessary?  # line 216
                else:  # may have intra-line modifications  # line 217
                    blocks[-2] = MergeBlock(MergeBlockType.MODIFY, blocks[-1].lines, line=no - len(tmp), replaces=blocks[-2], changes=blocks[-1].changes)  # line 218
                blocks.pop()  # remove TOS  # line 219
        elif last == "?":  # intra-line change comment  # line 220
            ilm = getIntraLineMarkers(tmp[0])  # tipe is one of MergeBlockType 1, 2, 4. # "? " line includes a trailing \n for some reason  # line 221
            blocks[-1] = dataCopy(MergeBlock, blocks[-1], tipe=MergeBlockType.MODIFY, changes=ilm)  # update to MODIFY, otherwise may be REPLACE instead  # line 222
        last = line[0]  # line 223
        tmp[:] = [line[2:]]  # line 224
    debug("Diff blocks: " + repr(blocks))  # line 225
    if diffOnly:  # line 226
        return blocks  # line 226
    output = []  # line 227
    for block in blocks:  # line 228
        if block.tipe == MergeBlockType.KEEP:  # line 229
            output.extend(block.lines)  # line 230
        elif block.tipe == MergeBlockType.INSERT and not (mergeOperation & MergeOperation.REMOVE):  # line 231
            output.extend(block.lines)  # line 232
        elif block.tipe == MergeBlockType.REPLACE:  # complete block replacement  # line 233
            if mergeOperation & MergeOperation.INSERT:  # replaced stuff TODO allow insertion BEFORE and alternatively AFTER?  # line 234
                output.extend(block.replaces.lines)  # replaced stuff TODO allow insertion BEFORE and alternatively AFTER?  # line 234
            if not (mergeOperation & MergeBlockType.REMOVE):  # if remove, don't add replaced lines, otherwise do  # line 235
                output.extend(block.lines)  # if remove, don't add replaced lines, otherwise do  # line 235
        elif block.tipe == MergeBlockType.REMOVE and mergeOperation & MergeOperation.INSERT:  # line 236
            output.extend(block.lines)  # line 237
        elif block.tipe == MergeBlockType.MODIFY:  # line 238
            if block.changes is not None and block.changes.tipe == MergeBlockType.INSERT:  # cannot be REMOVE, because it's always "-" then "+"  # line 239
                output.extend(block.lines if mergeOperation & MergeOperation.INSERT else block.replaces.lines)  # TODO logic?  # line 240
            elif block.replaces.changes is not None and block.replaces.changes.tipe == MergeBlockType.REMOVE:  # line 241
                output.extend(block.lines if mergeOperation & MergeOperation.REMOVE else block.replaces.lines)  # line 242
            elif block.changes is not None and block.changes.tipe == MergeBlockType.MODIFY:  # always both sides modified, but may differ in markers  # line 243
                if conflictResolution == ConflictResolution.THEIRS:  # line 244
                    output.extend(block.replaces.lines)  # line 245
                elif conflictResolution == ConflictResolution.MINE:  # line 246
                    output.extend(block.lines)  # line 247
                elif conflictResolution == ConflictResolution.ASK:  # line 248
                    print(ajoin("THR ", block.replaces.lines, "\n"))  # line 249
                    print(ajoin("MIN ", block.lines, "\n"))  # line 250
                    reso = {"i": ConflictResolution.MINE, "t": ConflictResolution.THEIRS, "m": ConflictResolution.NEXT, "u": None}.get(user_input(" Resolve: *M[I]ne, [T]heirs, [M]erge, [U]ser defined: ").strip().lower(), ConflictResolution.MINE)  # type: _coconut.typing.Optional[int]  # line 251
                    debug("User selected %d" % reso)  # line 252
                    _coconut_match_check = False  # line 253
                    _coconut_match_to = reso  # line 253
                    if _coconut_match_to is None:  # line 253
                        _coconut_match_check = True  # line 253
                    if _coconut_match_check:  # line 253
                        warn("Manual input not implemented yet")  # TODO allow multi-line input (CTRL+D?)  # line 254
                    _coconut_match_check = False  # line 255
                    _coconut_match_to = reso  # line 255
                    if _coconut_match_to == ConflictResolution.MINE:  # line 255
                        _coconut_match_check = True  # line 255
                    if _coconut_match_check:  # line 255
                        debug("Using mine")  # line 256
                        output.extend(block.lines)  # line 257
                    _coconut_match_check = False  # line 258
                    _coconut_match_to = reso  # line 258
                    if _coconut_match_to == ConflictResolution.THEIRS:  # line 258
                        _coconut_match_check = True  # line 258
                    if _coconut_match_check:  # line 258
                        debug("Using theirs")  # line 259
                        output.extend(block.replaces.lines)  # line 260
                    _coconut_match_check = False  # line 261
                    _coconut_match_to = reso  # line 261
                    if _coconut_match_to == ConflictResolution.NEXT:  # line 261
                        _coconut_match_check = True  # line 261
                    if _coconut_match_check:  # line 261
                        warn("Intra-line merge not implemented yet, skipping line(s)")  # line 262
                        output.extend(block.replaces.lines)  # line 263
            else:  # e.g. contains a deletion, but user was asking for insert only??  # line 264
                warn("Investigate this case")  # line 265
                output.extend(block.lines)  # default or not .replaces?  # line 266
    debug("Merge output: " + "; ".join(output))  # line 267
    nl = b"\n" if othreol is None else othreol if curreol is None else curreol  # type: bytes  # line 268
    return _coconut_tail_call(nl.join, [line.encode(encoding) for line in output])  # returning bytes  # line 269
# TODO handle check for more/less lines in found -/+ blocks to find common section and splitting prefix/suffix out

@_coconut_tco  # line 272
def getIntraLineMarkers(line: 'str') -> 'Range':  # line 272
    ''' Return (type, [affected indices]) of "? "-line diff markers ("? " suffix must be removed). '''  # line 273
    if "^" in line:  # line 274
        return _coconut_tail_call(Range, MergeBlockType.MODIFY, [i for i, c in enumerate(line) if c == "^"])  # line 274
    if "+" in line:  # line 275
        return _coconut_tail_call(Range, MergeBlockType.INSERT, [i for i, c in enumerate(line) if c == "+"])  # line 275
    if "-" in line:  # line 276
        return _coconut_tail_call(Range, MergeBlockType.REMOVE, [i for i, c in enumerate(line) if c == "-"])  # line 276
    return _coconut_tail_call(Range, MergeBlockType.KEEP, [])  # line 277

def findSosVcsBase() -> 'Tuple[_coconut.typing.Optional[str], _coconut.typing.Optional[str], _coconut.typing.Optional[str]]':  # line 279
    ''' Attempts to find sos and legacy VCS base folders. '''  # line 280
    debug("Detecting root folders...")  # line 281
    path = os.getcwd()  # type: str  # start in current folder, check parent until found or stopped  # line 282
    vcs = (None, None)  # type: Tuple[_coconut.typing.Optional[str], _coconut.typing.Optional[str]]  # line 283
    while not os.path.exists(os.path.join(path, metaFolder)):  # line 284
        contents = set(os.listdir(path))  # line 285
        vcss = [executable for folder, executable in vcsFolders.items() if folder in contents]  # type: _coconut.typing.Sequence[str]  # determine VCS type from dot folder  # line 286
        choice = None  # type: _coconut.typing.Optional[str]  # line 287
        if len(vcss) > 1:  # line 288
            choice = SVN if SVN in vcss else vcss[0]  # line 289
            warn("Detected more than one parallel VCS checkouts %r. Falling back to '%s'" % (vcss, choice))  # line 290
        elif len(vcss) > 0:  # line 291
            choice = vcss[0]  # line 291
        if not vcs[0] and choice:  # memorize current repo root  # line 292
            vcs = (path, choice)  # memorize current repo root  # line 292
        new = os.path.dirname(path)  # get parent path  # line 293
        if new == path:  # avoid infinite loop  # line 294
            break  # avoid infinite loop  # line 294
        path = new  # line 295
    if os.path.exists(os.path.join(path, metaFolder)):  # found something  # line 296
        if vcs[0]:  # already detected vcs base and command  # line 297
            return (path, vcs[0], vcs[1])  # already detected vcs base and command  # line 297
        sos = path  # line 298
        while True:  # continue search for VCS base  # line 299
            new = os.path.dirname(path)  # get parent path  # line 300
            if new == path:  # no VCS folder found  # line 301
                return (sos, None, None)  # no VCS folder found  # line 301
            path = new  # line 302
            contents = set(os.listdir(path))  # line 303
            vcss = [executable for folder, executable in vcsFolders.items() if folder in contents]  # determine VCS type  # line 304
            choice = None  # line 305
            if len(vcss) > 1:  # line 306
                choice = SVN if SVN in vcss else vcss[0]  # line 307
                warn("Detected more than one parallel VCS checkouts %r. Falling back to '%s'" % (vcss, choice))  # line 308
            elif len(vcss) > 0:  # line 309
                choice = vcss[0]  # line 309
            if choice:  # line 310
                return (sos, path, choice)  # line 310
    return (None, vcs[0], vcs[1])  # line 311
