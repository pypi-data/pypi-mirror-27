#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# __coconut_hash__ = 0xba25ff1d

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
    def __init__(_, value: 'str', depleted: 'str'="") -> 'None':  # line 11
        _.value = value  # type: str  # line 11
        _.depleted = depleted  # line 11
    def __call__(_) -> 'str':  # line 12
        value = _.value  # line 12
        _.value = None  # line 12
        return _.depleted if value is None else value  # line 12

class Accessor(dict):  # line 14
    ''' Dictionary with attribute access. Writing only supported via dictionary access. '''  # line 15
    def __init__(_, mapping: 'Dict[str, Any]') -> 'None':  # line 16
        dict.__init__(_, mapping)  # line 16
    @_coconut_tco  # line 17
    def __getattribute__(_, name: 'str') -> 'Any':  # line 17
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
class BranchInfo(_coconut_NamedTuple("BranchInfo", [("number", 'int'), ("ctime", 'int'), ("name", '_coconut.typing.Optional[str]'), ("insync", 'bool'), ("tracked", 'List[str]')])):  # tracked is a list on purpose, as serialization to JSON needs effort and frequent access is not taking place  # line 52
    __slots__ = ()  # tracked is a list on purpose, as serialization to JSON needs effort and frequent access is not taking place  # line 52
    __ne__ = _coconut.object.__ne__  # tracked is a list on purpose, as serialization to JSON needs effort and frequent access is not taking place  # line 52
    def __new__(_cls, number, ctime, name=None, insync=False, tracked=[]):  # tracked is a list on purpose, as serialization to JSON needs effort and frequent access is not taking place  # line 52
        return _coconut.tuple.__new__(_cls, (number, ctime, name, insync, tracked))  # tracked is a list on purpose, as serialization to JSON needs effort and frequent access is not taking place  # line 52
# tracked is a list on purpose, as serialization to JSON needs effort and frequent access is not taking place
class CommitInfo(_coconut_NamedTuple("CommitInfo", [("number", 'int'), ("ctime", 'int'), ("message", '_coconut.typing.Optional[str]')])):  # line 53
    __slots__ = ()  # line 53
    __ne__ = _coconut.object.__ne__  # line 53
    def __new__(_cls, number, ctime, message=None):  # line 53
        return _coconut.tuple.__new__(_cls, (number, ctime, message))  # line 53

class PathInfo(_coconut_NamedTuple("PathInfo", [("namehash", 'str'), ("size", '_coconut.typing.Optional[int]'), ("mtime", 'int'), ("hash", 'str')])):  # size == None means deleted in this revision  # line 54
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



# Enums
class ConflictResolution:  # prefer their changes, prefer my changes, ask user for each change, go to next deeper level (e.g. from files to lines, characters)  # line 61
    THEIRS, MINE, ASK, NEXT = range(4)  # prefer their changes, prefer my changes, ask user for each change, go to next deeper level (e.g. from files to lines, characters)  # line 61
class MergeOperation:  # insert remote changes into current, remove remote deletions from current, do both (replicate remote state) TODO handle inline-operations separate?  # line 62
    INSERT, REMOVE, BOTH = 1, 2, 3  # insert remote changes into current, remove remote deletions from current, do both (replicate remote state) TODO handle inline-operations separate?  # line 62
class MergeBlockType:  # modify = intra-line changes  # line 63
    KEEP, INSERT, REMOVE, REPLACE, MODIFY, MOVE = range(6)  # modify = intra-line changes  # line 63


# Functions
try:  # line 67
    import chardet  # https://github.com/chardet/chardet  # line 68
    def detectEncoding(binary: 'bytes') -> 'str':  # line 69
        return chardet.detect(binary)["encoding"]  # line 69
except:  # line 70
    def detectEncoding(binary: 'bytes') -> 'str':  # Guess the encoding  # line 71
        ''' Fallback if chardet library missing. '''  # line 72
        try:  # line 73
            binary.decode(UTF8)  # line 73
            return UTF8  # line 73
        except UnicodeError:  # line 74
            pass  # line 74
        try:  # line 75
            binary.decode("utf_16")  # line 75
            return "utf_16"  # line 75
        except UnicodeError:  # line 76
            pass  # line 76
        try:  # line 77
            binary.decode("cp1252")  # line 77
            return "cp1252"  # line 77
        except UnicodeError:  # line 78
            pass  # line 78
        return "ascii"  # this code will never be reached, as above is an 8-bit charset that always matches  # line 79

def openIt(file: 'str', mode: 'str', compress: 'bool'=False) -> 'IO':  # Abstraction for opening both compressed and plain files  # line 81
    return bz2.BZ2File(file, mode) if compress else open(file, mode + "b")  # Abstraction for opening both compressed and plain files  # line 81

def eoldet(file: 'bytes') -> '_coconut.typing.Optional[bytes]':  # line 83
    ''' Determine EOL style from a binary string. '''  # line 84
    lf = file.count(b"\n")  # type: int  # line 85
    cr = file.count(b"\r")  # type: int  # line 86
    crlf = file.count(b"\r\n")  # type: int  # line 87
    if crlf > 0:  # DOS/Windows/Symbian etc.  # line 88
        if lf != crlf or cr != crlf:  # line 89
            warn("Inconsistent CR/NL count with CR+NL. Mixed EOL style detected, may cause problems during merge")  # line 89
        return b"\r\n"  # line 90
    if lf != 0 and cr != 0:  # line 91
        warn("Inconsistent CR/NL count without CR+NL. Mixed EOL style detected, may cause problems during merge")  # line 91
    if lf > cr:  # Linux/Unix  # line 92
        return b"\n"  # Linux/Unix  # line 92
    if cr > lf:  # older 8-bit machines  # line 93
        return b"\r"  # older 8-bit machines  # line 93
    return None  # no new line contained, cannot determine  # line 94

def Exit(message: 'str'="") -> 'None':  # line 96
    print(message, file=sys.stderr)  # line 96
    sys.exit(1)  # line 96

@_coconut_tco  # referenceso __builtin__.raw_input on Python 2  # line 98
def user_input(msg: 'str') -> 'str':  # referenceso __builtin__.raw_input on Python 2  # line 98
    return _coconut_tail_call(input, msg)  # referenceso __builtin__.raw_input on Python 2  # line 98

try:  # line 100
    Splittable = TypeVar("Splittable", str, bytes)  # line 100
except:  # Python 2  # line 101
    pass  # Python 2  # line 101
def safeSplit(s: 'Splittable', d: '_coconut.typing.Optional[Splittable]'=None) -> '_coconut.typing.Sequence[Splittable]':  # line 102
    return s.split(("\n" if isinstance(s, str) else b"\n") if d is None else d) if len(s) > 0 else []  # line 102

def ajoin(sep: 'str', seq: '_coconut.typing.Sequence[str]', nl="") -> 'str':  # line 104
    return sep + (nl + sep).join(seq) if seq else ""  # line 104

@_coconut_tco  # line 106
def sjoin(*s: 'Tuple[Any]') -> 'str':  # line 106
    return _coconut_tail_call(" ".join, [str(e) for e in s if e != ''])  # line 106

@_coconut_tco  # line 108
def hashStr(datas: 'str') -> 'str':  # line 108
    return _coconut_tail_call(hashlib.sha256(datas.encode(UTF8)).hexdigest)  # line 108

def modified(changes: 'ChangeSet', onlyBinary: 'bool'=False) -> 'bool':  # line 110
    return len(changes.additions) > 0 or len(changes.deletions) > 0 or len(changes.modifications) > 0  # line 110

def getTermWidth() -> 'int':  # line 112
    try:  # line 112
        import termwidth  # line 113
    except:  # line 114
        return 80  # line 114
    return termwidth.getTermWidth()[0]  # line 115

@_coconut_tco  # line 117
def hashFile(path: 'str', compress: 'bool', saveTo: '_coconut.typing.Optional[str]'=None) -> 'str':  # line 117
    ''' Calculate hash of file contents. '''  # line 118
    _hash = hashlib.sha256()  # line 119
    to = openIt(saveTo, "w", compress) if saveTo else None  # line 120
    with open(path, "rb") as fd:  # line 121
        while True:  # line 122
            buffer = fd.read(bufSize)  # line 123
            _hash.update(buffer)  # line 124
            if to:  # line 125
                to.write(buffer)  # line 125
            if len(buffer) < bufSize:  # line 126
                break  # line 126
        if to:  # line 127
            to.close()  # line 127
    return _coconut_tail_call(_hash.hexdigest)  # line 128

def firstOfMap(map: 'Dict[str, Any]', params: '_coconut.typing.Sequence[str]', default: 'Any'=None) -> 'Any':  # line 130
    ''' Utility. '''  # line 131
    for k, v in map.items():  # line 132
        if k in params:  # line 133
            return v  # line 133
    return default  # line 134

@_coconut_tco  # line 136
def strftime(timestamp: '_coconut.typing.Optional[int]'=None) -> 'str':  # line 136
    return _coconut_tail_call(time.strftime, "%Y-%m-%d %H:%M:%S", time.localtime(timestamp / 1000. if timestamp is not None else None))  # line 136

def detectAndLoad(filename: '_coconut.typing.Optional[str]'=None, content: '_coconut.typing.Optional[bytes]'=None) -> 'Tuple[str, bytes, _coconut.typing.Sequence[str]]':  # line 138
    encoding = None  # type: str  # line 138
    eol = None  # type: bytes  # line 138
    lines = []  # type: _coconut.typing.Sequence[str]  # line 139
    if filename is not None:  # line 140
        with open(filename, "rb") as fd:  # line 141
            content = fd.read()  # line 141
    encoding = (lambda _coconut_none_coalesce_item: sys.getdefaultencoding() if _coconut_none_coalesce_item is None else _coconut_none_coalesce_item)(detectEncoding(content))  # line 142
    eol = eoldet(content)  # line 143
    if filename is not None:  # line 144
        with codecs.open(filename, encoding=encoding) as fd:  # line 145
            lines = safeSplit(fd.read(), (b"\n" if eol is None else eol).decode(encoding))  # line 145
    elif content is not None:  # line 146
        lines = safeSplit(content.decode(encoding), (b"\n" if eol is None else eol).decode(encoding))  # line 147
    else:  # line 148
        return (sys.getdefaultencoding(), b"\n", [])  # line 148
    return (encoding, eol, lines)  # line 149

def diffPathSets(last: 'Dict[str, PathInfo]', diff: 'Dict[str, PathInfo]') -> 'ChangeSet':  # line 151
    ''' Computes a changeset between in-memory and on-disk file lists.
      Additions contains PathInfo for entries in diff
      Deletions contains PathInfo for entries not anymore in diff
      Modifications contains PathInfo for entries changed from last to diff (new state)
  '''  # line 156
    changes = ChangeSet({}, {}, {})  # type: ChangeSet  # line 157
    for path, pinfo in last.items():  # line 158
        if path not in diff:  # now change  changes.deletions[path] = pinfo; continue  # line 159
            continue  # now change  changes.deletions[path] = pinfo; continue  # line 159
        vs = diff[path]  # reference to potentially changed path set  # line 160
        if vs.size is None:  # marked for deletion  # line 161
            changes.deletions[path] = pinfo  # marked for deletion  # line 161
            continue  # marked for deletion  # line 161
        if pinfo.size == None:  # re-added  # line 162
            changes.additions[path] = pinfo  # re-added  # line 162
            continue  # re-added  # line 162
        if pinfo.size != vs.size or pinfo.mtime != vs.mtime or pinfo.hash != vs.hash:  # not need to make hash comparison optional here  # line 163
            changes.modifications[path] = vs  # not need to make hash comparison optional here  # line 163
    for path, pinfo in diff.items():  # added loop  # line 164
        if path not in last:  # line 165
            changes.additions[path] = pinfo  # line 165
    assert not any([path in changes.deletions for path in changes.additions])  # invariant checks  # line 166
    assert not any([path in changes.additions for path in changes.deletions])  # line 167
    return changes  # line 168

try:  # line 170
    DataType = TypeVar("DataType", ChangeSet, MergeBlock, BranchInfo)  # line 170
except:  # Python 2  # line 171
    pass  # Python 2  # line 171

@_coconut_tco  # line 173
def dataCopy(_tipe: 'Type[DataType]', _old: 'DataType', *_args, **_kwargs) -> 'DataType':  # line 173
    r = _old._asdict()  # line 173
    r.update(**_kwargs)  # line 173
    return _coconut_tail_call(makedata, _tipe, *(list(_args) + [r[field] for field in _old._fields]))  # line 173
# TODO test namedtuple instead of instantiated tuple types in "datatype"?

@_coconut_tco  # line 176
def merge(file: '_coconut.typing.Optional[bytes]'=None, into: '_coconut.typing.Optional[bytes]'=None, filename: '_coconut.typing.Optional[str]'=None, intoname: '_coconut.typing.Optional[str]'=None, mergeOperation=MergeOperation.BOTH, conflictResolution=ConflictResolution.ASK, diffOnly: 'bool'=False) -> 'Union[bytes, List[MergeBlock]]':  # line 176
    ''' Merges binary text contents 'file' into file 'into', returning merged result. '''  # line 177
    encoding = None  # type: str  # line 178
    othr = None  # type: _coconut.typing.Sequence[str]  # line 178
    othreol = None  # type: _coconut.typing.Optional[bytes]  # line 178
    curr = None  # type: _coconut.typing.Sequence[str]  # line 178
    curreol = None  # type: _coconut.typing.Optional[bytes]  # line 178
    differ = difflib.Differ()  # line 179
    try:  # load files line-wise and normalize line endings (keep the one of the current file) TODO document  # line 180
        encoding, othreol, othr = detectAndLoad(filename=filename, content=file)  # line 181
        encoding, curreol, curr = detectAndLoad(filename=intoname, content=into)  # line 182
    except Exception as E:  # line 183
        Exit("Cannot merge '%s' into '%s': %r" % (filename, intoname, E))  # line 183
    if None not in [othreol, curreol] and othreol != curreol:  # line 184
        warn("Differing EOL-styles detected during merge. Using current file's style for merge output")  # line 184
    output = list(differ.compare(othr, curr))  # type: List[str]  # from generator expression  # line 185
    debug("Diff output: " + "".join([o.replace("\n", "\\n") for o in output]))  # line 186
    blocks = []  # type: List[MergeBlock]  # merged result in blocks  # line 187
    tmp = []  # type: List[str]  # block lines  # line 188
    last = " "  # line 189
    for no, line in enumerate(output + ["X"]):  # EOF marker (difflib's output will never be "X" alone)  # line 190
        if line[0] == last:  # continue filling consecutive block, no matter what type of block  # line 191
            tmp.append(line[2:])  # continue filling consecutive block, no matter what type of block  # line 191
            continue  # continue filling consecutive block, no matter what type of block  # line 191
        if line == "X":  # EOF marker - perform action for remaining block  # line 192
            if len(tmp) == 0:  # nothing left to do  # line 193
                break  # nothing left to do  # line 193
        if last == " ":  # block is same in both files  # line 194
            blocks.append(MergeBlock(MergeBlockType.KEEP, [line for line in tmp], line=no - len(tmp)))  # line 195
        elif last == "-":  # may be a deletion or replacement, store for later  # line 196
            blocks.append(MergeBlock(MergeBlockType.REMOVE, [line for line in tmp], line=no - len(tmp)))  # line 197
        elif last == "+":  # may be insertion or replacement  # line 198
            blocks.append(MergeBlock(MergeBlockType.INSERT, [line for line in tmp], line=no - len(tmp)))  # line 199
            if len(blocks) >= 2 and len(blocks[-1].lines) == len(blocks[-2].lines):  # replaces previously removed section entirely if any  # line 200
                if len(blocks[-1].lines) >= 2 or (blocks[-1].changes is None and blocks[-2].changes is None):  # full block or no intra-line comment  # line 201
                    blocks[-2] = MergeBlock(MergeBlockType.REPLACE, blocks[-1].lines, line=no - len(tmp) - 1, replaces=blocks[-2])  # remember replaced stuff TODO why -1 necessary?  # line 202
                else:  # may have intra-line modifications  # line 203
                    blocks[-2] = MergeBlock(MergeBlockType.MODIFY, blocks[-1].lines, line=no - len(tmp), replaces=blocks[-2], changes=blocks[-1].changes)  # line 204
                blocks.pop()  # remove TOS  # line 205
        elif last == "?":  # intra-line change comment  # line 206
            ilm = getIntraLineMarkers(tmp[0])  # tipe is one of MergeBlockType 1, 2, 4. # "? " line includes a trailing \n for some reason  # line 207
            blocks[-1] = dataCopy(MergeBlock, blocks[-1], tipe=MergeBlockType.MODIFY, changes=ilm)  # update to MODIFY, otherwise may be REPLACE instead  # line 208
        last = line[0]  # line 209
        tmp[:] = [line[2:]]  # line 210
    debug("Diff blocks: " + repr(blocks))  # line 211
    if diffOnly:  # line 212
        return blocks  # line 212
    output = []  # line 213
    for block in blocks:  # line 214
        if block.tipe == MergeBlockType.KEEP:  # line 215
            output.extend(block.lines)  # line 216
        elif block.tipe == MergeBlockType.INSERT and not (mergeOperation & MergeOperation.REMOVE):  # line 217
            output.extend(block.lines)  # line 218
        elif block.tipe == MergeBlockType.REPLACE:  # complete block replacement  # line 219
            if mergeOperation & MergeOperation.INSERT:  # replaced stuff TODO allow insertion BEFORE and alternatively AFTER?  # line 220
                output.extend(block.replaces.lines)  # replaced stuff TODO allow insertion BEFORE and alternatively AFTER?  # line 220
            if not (mergeOperation & MergeBlockType.REMOVE):  # if remove, don't add replaced lines, otherwise do  # line 221
                output.extend(block.lines)  # if remove, don't add replaced lines, otherwise do  # line 221
        elif block.tipe == MergeBlockType.REMOVE and mergeOperation & MergeOperation.INSERT:  # line 222
            output.extend(block.lines)  # line 223
        elif block.tipe == MergeBlockType.MODIFY:  # line 224
            if block.changes is not None and block.changes.tipe == MergeBlockType.INSERT:  # cannot be REMOVE, because it's always "-" then "+"  # line 225
                output.extend(block.lines if mergeOperation & MergeOperation.INSERT else block.replaces.lines)  # TODO logic?  # line 226
            elif block.replaces.changes is not None and block.replaces.changes.tipe == MergeBlockType.REMOVE:  # line 227
                output.extend(block.lines if mergeOperation & MergeOperation.REMOVE else block.replaces.lines)  # line 228
            elif block.changes is not None and block.changes.tipe == MergeBlockType.MODIFY:  # always both sides modified, but may differ in markers  # line 229
                if conflictResolution == ConflictResolution.THEIRS:  # line 230
                    output.extend(block.replaces.lines)  # line 231
                elif conflictResolution == ConflictResolution.MINE:  # line 232
                    output.extend(block.lines)  # line 233
                elif conflictResolution == ConflictResolution.ASK:  # line 234
                    print(ajoin("THR ", block.replaces.lines, "\n"))  # line 235
                    print(ajoin("MIN ", block.lines, "\n"))  # line 236
                    reso = {"i": ConflictResolution.MINE, "t": ConflictResolution.THEIRS, "m": ConflictResolution.NEXT, "u": None}.get(user_input(" Resolve: *M[I]ne, [T]heirs, [M]erge, [U]ser defined: ").strip().lower(), ConflictResolution.MINE)  # type: _coconut.typing.Optional[int]  # line 237
                    debug("User selected %d" % reso)  # line 238
                    _coconut_match_check = False  # line 239
                    _coconut_match_to = reso  # line 239
                    if _coconut_match_to is None:  # line 239
                        _coconut_match_check = True  # line 239
                    if _coconut_match_check:  # line 239
                        warn("Manual input not implemented yet")  # TODO allow multi-line input (CTRL+D?)  # line 240
                    _coconut_match_check = False  # line 241
                    _coconut_match_to = reso  # line 241
                    if _coconut_match_to == ConflictResolution.MINE:  # line 241
                        _coconut_match_check = True  # line 241
                    if _coconut_match_check:  # line 241
                        debug("Using mine")  # line 242
                        output.extend(block.lines)  # line 243
                    _coconut_match_check = False  # line 244
                    _coconut_match_to = reso  # line 244
                    if _coconut_match_to == ConflictResolution.THEIRS:  # line 244
                        _coconut_match_check = True  # line 244
                    if _coconut_match_check:  # line 244
                        debug("Using theirs")  # line 245
                        output.extend(block.replaces.lines)  # line 246
                    _coconut_match_check = False  # line 247
                    _coconut_match_to = reso  # line 247
                    if _coconut_match_to == ConflictResolution.NEXT:  # line 247
                        _coconut_match_check = True  # line 247
                    if _coconut_match_check:  # line 247
                        warn("Intra-line merge not implemented yet, skipping line(s)")  # line 248
                        output.extend(block.replaces.lines)  # line 249
            else:  # e.g. contains a deletion, but user was asking for insert only??  # line 250
                warn("Investigate this case")  # line 251
                output.extend(block.lines)  # default or not .replaces?  # line 252
    debug("Merge output: " + "; ".join(output))  # line 253
    nl = b"\n" if othreol is None else othreol if curreol is None else curreol  # type: bytes  # line 254
    return _coconut_tail_call(nl.join, [line.encode(encoding) for line in output])  # returning bytes  # line 255
# TODO handle check for more/less lines in found -/+ blocks to find common section and splitting prefix/suffix out

@_coconut_tco  # line 258
def getIntraLineMarkers(line: 'str') -> 'Range':  # line 258
    ''' Return (type, [affected indices]) of "? "-line diff markers ("? " suffix must be removed). '''  # line 259
    if "^" in line:  # line 260
        return _coconut_tail_call(Range, MergeBlockType.MODIFY, [i for i, c in enumerate(line) if c == "^"])  # line 260
    if "+" in line:  # line 261
        return _coconut_tail_call(Range, MergeBlockType.INSERT, [i for i, c in enumerate(line) if c == "+"])  # line 261
    if "-" in line:  # line 262
        return _coconut_tail_call(Range, MergeBlockType.REMOVE, [i for i, c in enumerate(line) if c == "-"])  # line 262
    return _coconut_tail_call(Range, MergeBlockType.KEEP, [])  # line 263

def findSosVcsBase() -> 'Tuple[_coconut.typing.Optional[str], _coconut.typing.Optional[str], _coconut.typing.Optional[str]]':  # line 265
    ''' Attempts to find sos and legacy VCS base folders. '''  # line 266
    debug("Detecting root folders...")  # line 267
    path = os.getcwd()  # type: str  # start in current folder, check parent until found or stopped  # line 268
    vcs = (None, None)  # type: Tuple[_coconut.typing.Optional[str], _coconut.typing.Optional[str]]  # line 269
    while not os.path.exists(os.path.join(path, metaFolder)):  # line 270
        contents = set(os.listdir(path))  # line 271
        vcss = [executable for folder, executable in vcsFolders.items() if folder in contents]  # type: _coconut.typing.Sequence[str]  # determine VCS type from dot folder  # line 272
        choice = None  # type: _coconut.typing.Optional[str]  # line 273
        if len(vcss) > 1:  # line 274
            choice = SVN if SVN in vcss else vcss[0]  # line 275
            warn("Detected more than one parallel VCS checkouts %r. Falling back to '%s'" % (vcss, choice))  # line 276
        elif len(vcss) > 0:  # line 277
            choice = vcss[0]  # line 277
        if not vcs[0] and choice:  # memorize current repo root  # line 278
            vcs = (path, choice)  # memorize current repo root  # line 278
        new = os.path.dirname(path)  # get parent path  # line 279
        if new == path:  # avoid infinite loop  # line 280
            break  # avoid infinite loop  # line 280
        path = new  # line 281
    if os.path.exists(os.path.join(path, metaFolder)):  # found something  # line 282
        if vcs[0]:  # already detected vcs base and command  # line 283
            return (path, vcs[0], vcs[1])  # already detected vcs base and command  # line 283
        sos = path  # line 284
        while True:  # continue search for VCS base  # line 285
            new = os.path.dirname(path)  # get parent path  # line 286
            if new == path:  # no VCS folder found  # line 287
                return (sos, None, None)  # no VCS folder found  # line 287
            path = new  # line 288
            contents = set(os.listdir(path))  # line 289
            vcss = [executable for folder, executable in vcsFolders.items() if folder in contents]  # determine VCS type  # line 290
            choice = None  # line 291
            if len(vcss) > 1:  # line 292
                choice = SVN if SVN in vcss else vcss[0]  # line 293
                warn("Detected more than one parallel VCS checkouts %r. Falling back to '%s'" % (vcss, choice))  # line 294
            elif len(vcss) > 0:  # line 295
                choice = vcss[0]  # line 295
            if choice:  # line 296
                return (sos, path, choice)  # line 296
    return (None, vcs[0], vcs[1])  # line 297
