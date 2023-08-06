#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# __coconut_hash__ = 0xf325018c

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


# Classes
class JustOnce:  # line 10
    def __init__(_, value: 'str', depleted: 'str'=""):  # line 11
        _.value = value  # type: str  # line 11
        _.depleted = depleted  # line 11
    def __call__(_) -> 'str':  # line 12
        value = _.value  # line 12
        _.value = None  # line 12
        return _.depleted if value is None else value  # line 12

class Accessor(dict):  # line 14
    ''' Dictionary with attribute access. Writing only supported via dictionary access. '''  # line 15
    def __init__(_, mapping) -> 'None':  # line 16
        dict.__init__(_, mapping)  # line 16
    @_coconut_tco  # line 17
    def __getattribute__(_, name: 'str') -> 'List[str]':  # line 17
        try:  # line 18
            return _[name]  # line 18
        except:  # line 19
            return _coconut_tail_call(dict.__getattribute__, _, name)  # line 19

class Counter:  # line 21
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
PROGRESS_MARKER = ["|", "/", "-", "\\"]  # line 40
metaFolder = ".sos"  # type: str  # line 41
metaFile = ".meta"  # type: str  # line 42
bufSize = 1 << 20  # type: int  # 1 MiB  # line 43
SVN = "svn"  # line 44
SLASH = "/"  # line 45
vcsFolders = {".svn": SVN, ".git": "git", ".bzr": "bzr", ".hg": "hg", ".fslckout": "fossil", "_FOSSIL_": "fossil", ".CVS": "cvs"}  # type: Dict[str, str]  # line 46
vcsBranches = {SVN: "trunk", "git": "master", "bzr": "trunk", "hg": "default", "fossil": None, "cvs": None}  # type: Dict[str, _coconut.typing.Optional[str]]  # line 47


# Value types
class BranchInfo(_coconut_NamedTuple("BranchInfo", [("number", 'int'), ("ctime", 'int'), ("name", '_coconut.typing.Optional[str]'), ("insync", 'bool'), ("tracked", 'List[str]')])):  # tracked is a list on purpose, as serialization to JSON needs effort and frequent access is not taking place  # line 51
    __slots__ = ()  # tracked is a list on purpose, as serialization to JSON needs effort and frequent access is not taking place  # line 51
    __ne__ = _coconut.object.__ne__  # tracked is a list on purpose, as serialization to JSON needs effort and frequent access is not taking place  # line 51
    def __new__(_cls, number, ctime, name=None, insync=False, tracked=[]):  # tracked is a list on purpose, as serialization to JSON needs effort and frequent access is not taking place  # line 51
        return _coconut.tuple.__new__(_cls, (number, ctime, name, insync, tracked))  # tracked is a list on purpose, as serialization to JSON needs effort and frequent access is not taking place  # line 51
# tracked is a list on purpose, as serialization to JSON needs effort and frequent access is not taking place
class CommitInfo(_coconut_NamedTuple("CommitInfo", [("number", 'int'), ("ctime", 'int'), ("message", '_coconut.typing.Optional[str]')])):  # line 52
    __slots__ = ()  # line 52
    __ne__ = _coconut.object.__ne__  # line 52
    def __new__(_cls, number, ctime, message=None):  # line 52
        return _coconut.tuple.__new__(_cls, (number, ctime, message))  # line 52

class PathInfo(_coconut_NamedTuple("PathInfo", [("namehash", 'str'), ("size", '_coconut.typing.Optional[int]'), ("mtime", 'int'), ("hash", 'str')])):  # size == None means deleted in this revision  # line 53
    __slots__ = ()  # size == None means deleted in this revision  # line 53
    __ne__ = _coconut.object.__ne__  # size == None means deleted in this revision  # line 53
class ChangeSet(_coconut_NamedTuple("ChangeSet", [("additions", 'Dict[str, PathInfo]'), ("deletions", 'Dict[str, PathInfo]'), ("modifications", 'Dict[str, PathInfo]')])):  # avoid default assignment of {} as it leads to runtime errors (contains data on init for unknown reason)  # line 54
    __slots__ = ()  # avoid default assignment of {} as it leads to runtime errors (contains data on init for unknown reason)  # line 54
    __ne__ = _coconut.object.__ne__  # avoid default assignment of {} as it leads to runtime errors (contains data on init for unknown reason)  # line 54
class Range(_coconut_NamedTuple("Range", [("tipe", 'int'), ("indexes", '_coconut.typing.Sequence[int]')])):  # MergeBlockType[1,2,4], line number, length  # line 55
    __slots__ = ()  # MergeBlockType[1,2,4], line number, length  # line 55
    __ne__ = _coconut.object.__ne__  # MergeBlockType[1,2,4], line number, length  # line 55
class MergeBlock(_coconut_NamedTuple("MergeBlock", [("tipe", 'int'), ("lines", '_coconut.typing.Sequence[str]'), ("line", 'int'), ("replaces", '_coconut.typing.Optional[MergeBlock]'), ("changes", '_coconut.typing.Optional[Range]')])):  # line 56
    __slots__ = ()  # line 56
    __ne__ = _coconut.object.__ne__  # line 56
    def __new__(_cls, tipe, lines, line, replaces=None, changes=None):  # line 56
        return _coconut.tuple.__new__(_cls, (tipe, lines, line, replaces, changes))  # line 56



# Enums
class ConflictResolution:  # prefer their changes, prefer my changes, ask user for each change, go to next deeper level (e.g. from files to lines, characters)  # line 60
    THEIRS, MINE, ASK, NEXT = range(4)  # prefer their changes, prefer my changes, ask user for each change, go to next deeper level (e.g. from files to lines, characters)  # line 60
class MergeOperation:  # insert remote changes into current, remove remote deletions from current, do both (replicate remote state) TODO handle inline-operations separate?  # line 61
    INSERT, REMOVE, BOTH = 1, 2, 3  # insert remote changes into current, remove remote deletions from current, do both (replicate remote state) TODO handle inline-operations separate?  # line 61
class MergeBlockType:  # modify = intra-line changes  # line 62
    KEEP, INSERT, REMOVE, REPLACE, MODIFY, MOVE = range(6)  # modify = intra-line changes  # line 62


# Functions
try:  # line 66
    import chardet  # https://github.com/chardet/chardet  # line 67
    def detectEncoding(binary: 'bytes') -> 'str':  # line 68
        return chardet.detect(binary)["encoding"]  # line 68
except:  # line 69
    def detectEncoding(binary: 'bytes') -> 'str':  # Guess the encoding  # line 70
        ''' Fallback if chardet library missing. '''  # line 71
        try:  # line 72
            binary.decode(UTF8)  # line 72
            return UTF8  # line 72
        except UnicodeError:  # line 73
            pass  # line 73
        try:  # line 74
            binary.decode("utf_16")  # line 74
            return "utf_16"  # line 74
        except UnicodeError:  # line 75
            pass  # line 75
        try:  # line 76
            binary.decode("cp1252")  # line 76
            return "cp1252"  # line 76
        except UnicodeError:  # line 77
            pass  # line 77
        return "ascii"  # this code will never be reached, as above is an 8-bit charset that always matches  # line 78

def openIt(file: 'str', mode: 'str', compress: 'bool'=False) -> 'IO':  # Abstraction for opening both compressed and plain files  # line 80
    return bz2.BZ2File(file, mode) if compress else open(file, mode + "b")  # Abstraction for opening both compressed and plain files  # line 80

def eoldet(file: 'bytes') -> '_coconut.typing.Optional[bytes]':  # line 82
    ''' Determine EOL style from a binary string. '''  # line 83
    lf = file.count(b"\n")  # type: int  # line 84
    cr = file.count(b"\r")  # type: int  # line 85
    crlf = file.count(b"\r\n")  # type: int  # line 86
    if crlf > 0:  # DOS/Windows/Symbian etc.  # line 87
        if lf != crlf or cr != crlf:  # line 88
            warn("Inconsistent CR/NL count with CR+NL. Mixed EOL style detected, may cause problems during merge")  # line 88
        return b"\r\n"  # line 89
    if lf != 0 and cr != 0:  # line 90
        warn("Inconsistent CR/NL count without CR+NL. Mixed EOL style detected, may cause problems during merge")  # line 90
    if lf > cr:  # Linux/Unix  # line 91
        return b"\n"  # Linux/Unix  # line 91
    if cr > lf:  # older 8-bit machines  # line 92
        return b"\r"  # older 8-bit machines  # line 92
    return None  # no new line contained, cannot determine  # line 93

def Exit(message: 'str'="") -> 'None':  # line 95
    print(message, file=sys.stderr)  # line 95
    sys.exit(1)  # line 95

@_coconut_tco  # referenceso __builtin__.raw_input on Python 2  # line 97
def user_input(msg: 'str') -> 'str':  # referenceso __builtin__.raw_input on Python 2  # line 97
    return _coconut_tail_call(input, msg)  # referenceso __builtin__.raw_input on Python 2  # line 97

try:  # line 99
    Splittable = TypeVar("Splittable", str, bytes)  # line 99
except:  # Python 2  # line 100
    pass  # Python 2  # line 100
def safeSplit(s: 'Splittable', d: '_coconut.typing.Optional[Splittable]'=None) -> '_coconut.typing.Sequence[Splittable]':  # line 101
    return s.split(("\n" if isinstance(s, str) else b"\n") if d is None else d) if len(s) > 0 else []  # line 101

def ajoin(sep: 'str', seq: '_coconut.typing.Sequence[str]', nl="") -> 'str':  # line 103
    return sep + (nl + sep).join(seq) if seq else ""  # line 103

@_coconut_tco  # line 105
def sjoin(*s: 'Tuple[Any]') -> 'str':  # line 105
    return _coconut_tail_call(" ".join, [str(e) for e in s if e != ''])  # line 105

@_coconut_tco  # line 107
def hashStr(datas: 'str') -> 'str':  # line 107
    return _coconut_tail_call(hashlib.sha256(datas.encode(UTF8)).hexdigest)  # line 107

def modified(changes: 'ChangeSet', onlyBinary: 'bool'=False) -> 'bool':  # line 109
    return len(changes.additions) > 0 or len(changes.deletions) > 0 or len(changes.modifications) > 0  # line 109

def getTermWidth() -> 'int':  # line 111
    try:  # line 111
        import termwidth  # line 112
    except:  # line 113
        return 80  # line 113
    return termwidth.getTermWidth()[0]  # line 114

@_coconut_tco  # line 116
def hashFile(path: 'str', compress: 'bool', saveTo: '_coconut.typing.Optional[str]'=None) -> 'str':  # line 116
    ''' Calculate hash of file contents. '''  # line 117
    _hash = hashlib.sha256()  # line 118
    to = openIt(saveTo, "w", compress) if saveTo else None  # line 119
    with open(path, "rb") as fd:  # line 120
        while True:  # line 121
            buffer = fd.read(bufSize)  # line 122
            _hash.update(buffer)  # line 123
            if to:  # line 124
                to.write(buffer)  # line 124
            if len(buffer) < bufSize:  # line 125
                break  # line 125
        if to:  # line 126
            to.close()  # line 126
    return _coconut_tail_call(_hash.hexdigest)  # line 127

def firstOfMap(map: 'Dict[str, Any]', params: '_coconut.typing.Sequence[str]', default: 'Any'=None) -> 'Any':  # line 129
    ''' Utility. '''  # line 130
    for k, v in map.items():  # line 131
        if k in params:  # line 132
            return v  # line 132
    return default  # line 133

@_coconut_tco  # line 135
def strftime(timestamp: '_coconut.typing.Optional[int]'=None) -> 'str':  # line 135
    return _coconut_tail_call(time.strftime, "%Y-%m-%d %H:%M:%S", time.localtime(timestamp / 1000. if timestamp is not None else None))  # line 135

def detectAndLoad(filename: '_coconut.typing.Optional[str]'=None, content: '_coconut.typing.Optional[bytes]'=None) -> 'Tuple[str, bytes, _coconut.typing.Sequence[str]]':  # line 137
    encoding = None  # type: str  # line 137
    eol = None  # type: bytes  # line 137
    lines = []  # type: _coconut.typing.Sequence[str]  # line 138
    if filename is not None:  # line 139
        with open(filename, "rb") as fd:  # line 140
            content = fd.read()  # line 140
    encoding = (lambda _coconut_none_coalesce_item: sys.getdefaultencoding() if _coconut_none_coalesce_item is None else _coconut_none_coalesce_item)(detectEncoding(content))  # line 141
    eol = eoldet(content)  # line 142
    if filename is not None:  # line 143
        with codecs.open(filename, encoding=encoding) as fd:  # line 144
            lines = safeSplit(fd.read(), (b"\n" if eol is None else eol).decode(encoding))  # line 144
    elif content is not None:  # line 145
        lines = safeSplit(content.decode(encoding), (b"\n" if eol is None else eol).decode(encoding))  # line 146
    else:  # line 147
        return (sys.getdefaultencoding(), b"\n", [])  # line 147
    return (encoding, eol, lines)  # line 148

def diffPathSets(last: 'Dict[str, PathInfo]', diff: 'Dict[str, PathInfo]') -> 'ChangeSet':  # line 150
    ''' Computes a changeset between in-memory and on-disk file lists.
      Additions contains PathInfo for entries in diff
      Deletions contains PathInfo for entries not anymore in diff
      Modifications contains PathInfo for entries changed from last to diff (new state)
  '''  # line 155
    changes = ChangeSet({}, {}, {})  # type: ChangeSet  # line 156
    for path, pinfo in last.items():  # line 157
        if path not in diff:  # now change  changes.deletions[path] = pinfo; continue  # line 158
            continue  # now change  changes.deletions[path] = pinfo; continue  # line 158
        vs = diff[path]  # reference to potentially changed path set  # line 159
        if vs.size is None:  # marked for deletion  # line 160
            changes.deletions[path] = pinfo  # marked for deletion  # line 160
            continue  # marked for deletion  # line 160
        if pinfo.size == None:  # re-added  # line 161
            changes.additions[path] = pinfo  # re-added  # line 161
            continue  # re-added  # line 161
        if pinfo.size != vs.size or pinfo.mtime != vs.mtime or pinfo.hash != vs.hash:  # not need to make hash comparison optional here  # line 162
            changes.modifications[path] = vs  # not need to make hash comparison optional here  # line 162
    for path, pinfo in diff.items():  # added loop  # line 163
        if path not in last:  # line 164
            changes.additions[path] = pinfo  # line 164
    assert not any([path in changes.deletions for path in changes.additions])  # invariant checks  # line 165
    assert not any([path in changes.additions for path in changes.deletions])  # line 166
    return changes  # line 167

try:  # line 169
    DataType = TypeVar("DataType", MergeBlock, BranchInfo)  # line 169
except:  # Python 2  # line 170
    pass  # Python 2  # line 170

@_coconut_tco  # line 172
def dataCopy(_tipe: 'Type[DataType]', _old: 'DataType', *_args, **_kwargs) -> 'DataType':  # line 172
    r = _old._asdict()  # line 172
    r.update(**_kwargs)  # line 172
    return _coconut_tail_call(makedata, _tipe, *(list(_args) + [r[field] for field in _old._fields]))  # line 172
# TODO test namedtuple instead of instantiated tuple types in "datatype"?

@_coconut_tco  # line 175
def merge(file: '_coconut.typing.Optional[bytes]'=None, into: '_coconut.typing.Optional[bytes]'=None, filename: '_coconut.typing.Optional[str]'=None, intoname: '_coconut.typing.Optional[str]'=None, mergeOperation=MergeOperation.BOTH, conflictResolution=ConflictResolution.ASK, diffOnly: 'bool'=False) -> 'Union[bytes, List[MergeBlock]]':  # line 175
    ''' Merges binary text contents 'file' into file 'into', returning merged result. '''  # line 176
    encoding = None  # type: str  # line 177
    othr = None  # type: _coconut.typing.Sequence[str]  # line 177
    othreol = None  # type: _coconut.typing.Optional[bytes]  # line 177
    curr = None  # type: _coconut.typing.Sequence[str]  # line 177
    curreol = None  # type: _coconut.typing.Optional[bytes]  # line 177
    differ = difflib.Differ()  # line 178
    try:  # load files line-wise and normalize line endings (keep the one of the current file) TODO document  # line 179
        encoding, othreol, othr = detectAndLoad(filename=filename, content=file)  # line 180
        encoding, curreol, curr = detectAndLoad(filename=intoname, content=into)  # line 181
    except Exception as E:  # line 182
        Exit("Cannot merge '%s' into '%s': %r" % (filename, intoname, E))  # line 182
    if None not in [othreol, curreol] and othreol != curreol:  # line 183
        warn("Differing EOL-styles detected during merge. Using current file's style for merge output")  # line 183
    output = list(differ.compare(othr, curr))  # type: List[str]  # from generator expression  # line 184
    debug("Diff output: " + "".join([o.replace("\n", "\\n") for o in output]))  # line 185
    blocks = []  # type: List[MergeBlock]  # merged result in blocks  # line 186
    tmp = []  # type: List[str]  # block lines  # line 187
    last = " "  # line 188
    for no, line in enumerate(output + ["X"]):  # EOF marker (difflib's output will never be "X" alone)  # line 189
        if line[0] == last:  # continue filling consecutive block, no matter what type of block  # line 190
            tmp.append(line[2:])  # continue filling consecutive block, no matter what type of block  # line 190
            continue  # continue filling consecutive block, no matter what type of block  # line 190
        if line == "X":  # EOF marker - perform action for remaining block  # line 191
            if len(tmp) == 0:  # nothing left to do  # line 192
                break  # nothing left to do  # line 192
        if last == " ":  # block is same in both files  # line 193
            blocks.append(MergeBlock(MergeBlockType.KEEP, [line for line in tmp], line=no - len(tmp)))  # line 194
        elif last == "-":  # may be a deletion or replacement, store for later  # line 195
            blocks.append(MergeBlock(MergeBlockType.REMOVE, [line for line in tmp], line=no - len(tmp)))  # line 196
        elif last == "+":  # may be insertion or replacement  # line 197
            blocks.append(MergeBlock(MergeBlockType.INSERT, [line for line in tmp], line=no - len(tmp)))  # line 198
            if len(blocks) >= 2 and len(blocks[-1].lines) == len(blocks[-2].lines):  # replaces previously removed section entirely if any  # line 199
                if len(blocks[-1].lines) >= 2 or (blocks[-1].changes is None and blocks[-2].changes is None):  # full block or no intra-line comment  # line 200
                    blocks[-2] = MergeBlock(MergeBlockType.REPLACE, blocks[-1].lines, line=no - len(tmp) - 1, replaces=blocks[-2])  # remember replaced stuff TODO why -1 necessary?  # line 201
                else:  # may have intra-line modifications  # line 202
                    blocks[-2] = MergeBlock(MergeBlockType.MODIFY, blocks[-1].lines, line=no - len(tmp), replaces=blocks[-2], changes=blocks[-1].changes)  # line 203
                blocks.pop()  # remove TOS  # line 204
        elif last == "?":  # intra-line change comment  # line 205
            ilm = getIntraLineMarkers(tmp[0])  # tipe is one of MergeBlockType 1, 2, 4. # "? " line includes a trailing \n for some reason  # line 206
            blocks[-1] = dataCopy(MergeBlock, blocks[-1], tipe=MergeBlockType.MODIFY, changes=ilm)  # update to MODIFY, otherwise may be REPLACE instead  # line 207
        last = line[0]  # line 208
        tmp[:] = [line[2:]]  # line 209
    debug("Diff blocks: " + repr(blocks))  # line 210
    if diffOnly:  # line 211
        return blocks  # line 211
    output = []  # line 212
    for block in blocks:  # line 213
        if block.tipe == MergeBlockType.KEEP:  # line 214
            output.extend(block.lines)  # line 215
        elif block.tipe == MergeBlockType.INSERT and not (mergeOperation & MergeOperation.REMOVE):  # line 216
            output.extend(block.lines)  # line 217
        elif block.tipe == MergeBlockType.REPLACE:  # complete block replacement  # line 218
            if mergeOperation & MergeOperation.INSERT:  # replaced stuff TODO allow insertion BEFORE and alternatively AFTER?  # line 219
                output.extend(block.replaces.lines)  # replaced stuff TODO allow insertion BEFORE and alternatively AFTER?  # line 219
            if not (mergeOperation & MergeBlockType.REMOVE):  # if remove, don't add replaced lines, otherwise do  # line 220
                output.extend(block.lines)  # if remove, don't add replaced lines, otherwise do  # line 220
        elif block.tipe == MergeBlockType.REMOVE and mergeOperation & MergeOperation.INSERT:  # line 221
            output.extend(block.lines)  # line 222
        elif block.tipe == MergeBlockType.MODIFY:  # line 223
            if block.changes is not None and block.changes.tipe == MergeBlockType.INSERT:  # cannot be REMOVE, because it's always "-" then "+"  # line 224
                output.extend(block.lines if mergeOperation & MergeOperation.INSERT else block.replaces.lines)  # TODO logic?  # line 225
            elif block.replaces.changes is not None and block.replaces.changes.tipe == MergeBlockType.REMOVE:  # line 226
                output.extend(block.lines if mergeOperation & MergeOperation.REMOVE else block.replaces.lines)  # line 227
            elif block.changes is not None and block.changes.tipe == MergeBlockType.MODIFY:  # always both sides modified, but may differ in markers  # line 228
                if conflictResolution == ConflictResolution.THEIRS:  # line 229
                    output.extend(block.replaces.lines)  # line 230
                elif conflictResolution == ConflictResolution.MINE:  # line 231
                    output.extend(block.lines)  # line 232
                elif conflictResolution == ConflictResolution.ASK:  # line 233
                    print(ajoin("THR ", block.replaces.lines, "\n"))  # line 234
                    print(ajoin("MIN ", block.lines, "\n"))  # line 235
                    reso = {"i": ConflictResolution.MINE, "t": ConflictResolution.THEIRS, "m": ConflictResolution.NEXT, "u": None}.get(user_input(" Resolve: *M[I]ne, [T]heirs, [M]erge, [U]ser defined: ").strip().lower(), ConflictResolution.MINE)  # type: _coconut.typing.Optional[int]  # line 236
                    debug("User selected %d" % reso)  # line 237
                    _coconut_match_check = False  # line 238
                    _coconut_match_to = reso  # line 238
                    if _coconut_match_to is None:  # line 238
                        _coconut_match_check = True  # line 238
                    if _coconut_match_check:  # line 238
                        warn("Manual input not implemented yet")  # TODO allow multi-line input (CTRL+D?)  # line 239
                    _coconut_match_check = False  # line 240
                    _coconut_match_to = reso  # line 240
                    if _coconut_match_to == ConflictResolution.MINE:  # line 240
                        _coconut_match_check = True  # line 240
                    if _coconut_match_check:  # line 240
                        debug("Using mine")  # line 241
                        output.extend(block.lines)  # line 242
                    _coconut_match_check = False  # line 243
                    _coconut_match_to = reso  # line 243
                    if _coconut_match_to == ConflictResolution.THEIRS:  # line 243
                        _coconut_match_check = True  # line 243
                    if _coconut_match_check:  # line 243
                        debug("Using theirs")  # line 244
                        output.extend(block.replaces.lines)  # line 245
                    _coconut_match_check = False  # line 246
                    _coconut_match_to = reso  # line 246
                    if _coconut_match_to == ConflictResolution.NEXT:  # line 246
                        _coconut_match_check = True  # line 246
                    if _coconut_match_check:  # line 246
                        warn("Intra-line merge not implemented yet, skipping line(s)")  # line 247
                        output.extend(block.replaces.lines)  # line 248
            else:  # e.g. contains a deletion, but user was asking for insert only??  # line 249
                warn("Investigate this case")  # line 250
                output.extend(block.lines)  # default or not .replaces?  # line 251
    debug("Merge output: " + "; ".join(output))  # line 252
    nl = b"\n" if othreol is None else othreol if curreol is None else curreol  # type: bytes  # line 253
    return _coconut_tail_call(nl.join, [line.encode(encoding) for line in output])  # line 254
# TODO handle check for more/less lines in found -/+ blocks to find common section and splitting prefix/suffix out

@_coconut_tco  # line 257
def getIntraLineMarkers(line: 'str') -> 'Range':  # line 257
    ''' Return (type, [affected indices]) of "? "-line diff markers ("? " suffix must be removed). '''  # line 258
    if "^" in line:  # line 259
        return _coconut_tail_call(Range, MergeBlockType.MODIFY, [i for i, c in enumerate(line) if c == "^"])  # line 259
    if "+" in line:  # line 260
        return _coconut_tail_call(Range, MergeBlockType.INSERT, [i for i, c in enumerate(line) if c == "+"])  # line 260
    if "-" in line:  # line 261
        return _coconut_tail_call(Range, MergeBlockType.REMOVE, [i for i, c in enumerate(line) if c == "-"])  # line 261
    return _coconut_tail_call(Range, MergeBlockType.KEEP, [])  # line 262

def findSosVcsBase() -> 'Tuple[_coconut.typing.Optional[str], _coconut.typing.Optional[str], _coconut.typing.Optional[str]]':  # line 264
    ''' Attempts to find sos and legacy VCS base folders. '''  # line 265
    debug("Detecting root folders...")  # line 266
    path = os.getcwd()  # type: str  # start in current folder, check parent until found or stopped  # line 267
    vcs = (None, None)  # type: Tuple[_coconut.typing.Optional[str], _coconut.typing.Optional[str]]  # line 268
    while not os.path.exists(os.path.join(path, metaFolder)):  # line 269
        contents = set(os.listdir(path))  # line 270
        vcss = [executable for folder, executable in vcsFolders.items() if folder in contents]  # type: _coconut.typing.Sequence[str]  # determine VCS type from dot folder  # line 271
        choice = None  # type: _coconut.typing.Optional[str]  # line 272
        if len(vcss) > 1:  # line 273
            choice = SVN if SVN in vcss else vcss[0]  # line 274
            warn("Detected more than one parallel VCS checkouts %r. Falling back to '%s'" % (vcss, choice))  # line 275
        elif len(vcss) > 0:  # line 276
            choice = vcss[0]  # line 276
        if not vcs[0] and choice:  # memorize current repo root  # line 277
            vcs = (path, choice)  # memorize current repo root  # line 277
        new = os.path.dirname(path)  # get parent path  # line 278
        if new == path:  # avoid infinite loop  # line 279
            break  # avoid infinite loop  # line 279
        path = new  # line 280
    if os.path.exists(os.path.join(path, metaFolder)):  # found something  # line 281
        if vcs[0]:  # already detected vcs base and command  # line 282
            return (path, vcs[0], vcs[1])  # already detected vcs base and command  # line 282
        sos = path  # line 283
        while True:  # continue search for VCS base  # line 284
            new = os.path.dirname(path)  # get parent path  # line 285
            if new == path:  # no VCS folder found  # line 286
                return (sos, None, None)  # no VCS folder found  # line 286
            path = new  # line 287
            contents = set(os.listdir(path))  # line 288
            vcss = [executable for folder, executable in vcsFolders.items() if folder in contents]  # determine VCS type  # line 289
            choice = None  # line 290
            if len(vcss) > 1:  # line 291
                choice = SVN if SVN in vcss else vcss[0]  # line 292
                warn("Detected more than one parallel VCS checkouts %r. Falling back to '%s'" % (vcss, choice))  # line 293
            elif len(vcss) > 0:  # line 294
                choice = vcss[0]  # line 294
            if choice:  # line 295
                return (sos, path, choice)  # line 295
    return (None, vcs[0], vcs[1])  # line 296
