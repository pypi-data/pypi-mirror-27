#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# __coconut_hash__ = 0x4e61c709

# Compiled with Coconut version 1.3.1 [Dead Parrot]

# Coconut Header: -------------------------------------------------------------

import sys as _coconut_sys, os.path as _coconut_os_path
_coconut_file_path = _coconut_os_path.dirname(_coconut_os_path.abspath(__file__))
_coconut_sys.path.insert(0, _coconut_file_path)
from __coconut__ import _coconut, _coconut_NamedTuple, _coconut_MatchError, _coconut_tail_call, _coconut_tco, _coconut_igetitem, _coconut_base_compose, _coconut_forward_compose, _coconut_back_compose, _coconut_forward_star_compose, _coconut_back_star_compose, _coconut_pipe, _coconut_star_pipe, _coconut_back_pipe, _coconut_back_star_pipe, _coconut_bool_and, _coconut_bool_or, _coconut_none_coalesce, _coconut_minus, _coconut_map, _coconut_partial
from __coconut__ import *
_coconut_sys.path.remove(_coconut_file_path)

# Compiled Coconut: -----------------------------------------------------------

import builtins  # line 1
import json  # line 1
import logging  # line 1
import os  # line 1
import shutil  # line 1
sys = _coconut_sys  # line 1
import time  # line 1
import traceback  # line 1
import unittest  # line 1
import uuid  # line 1
StringIO = (__import__("StringIO" if sys.version_info.major < 3 else "io")).StringIO  # enables import via ternary expression  # line 2
try:  # Py3  # line 3
    from unittest import mock  # Py3  # line 3
except:  # installed via pip  # line 4
    import mock  # installed via pip  # line 4
try:  # only required for mypy  # line 5
    from typing import Any  # only required for mypy  # line 5
    from typing import List  # only required for mypy  # line 5
    from typing import Union  # only required for mypy  # line 5
except:  # line 6
    pass  # line 6

testFolder = os.path.abspath(os.path.join(os.getcwd(), "test"))  # line 8
try:  # line 9
    import configr  # optional dependency  # line 10
    os.environ["TEST"] = testFolder  # needed to mock configr library calls in sos  # line 11
except:  # declare as undefined  # line 12
    configr = None  # declare as undefined  # line 12
import sos  # line 13
sos.defaults["defaultbranch"] = "trunk"  # because sos.main() is never called  # line 14

def sync() -> 'None':  # line 16
    if (sys.version_info.major, sys.version_info.minor) >= (3, 3):  # line 17
        os.sync()  # line 17


def determineFilesystemTimeResolution() -> 'float':  # line 20
    name = str(uuid.uuid4())  # line 21
    with open(name, "w") as fd:  # create temporary file  # line 22
        fd.write("x")  # create temporary file  # line 22
    mt = os.stat(name)[8]  # get current timestamp  # line 23
    while os.stat(name)[8] == mt:  # wait until timestamp modified  # line 24
        with open(name, "w") as fd:  # line 25
            fd.write("x")  # line 25
    mt, start, count = os.stat(name)[8], time.time(), 0  # line 26
    while os.stat(name)[8] == mt:  # now cound and measure time until modified again  # line 27
        count += 1  # line 28
        with open(name, "w") as fd:  # line 29
            fd.write("x")  # line 29
    os.unlink(name)  # line 30
    fsprecision = round(time.time() - start, 2)  # line 31
    print("File system timestamp precision is %.2fs; wrote to the file %d times during that time" % (fsprecision, count))  # line 32
    return fsprecision  # line 33


FS_PRECISION = determineFilesystemTimeResolution() * 1.05  # line 36


@_coconut_tco  # line 39
def debugTestRunner(post_mortem=None):  # line 39
    ''' Unittest runner doing post mortem debugging on failing tests. '''  # line 40
    import pdb  # line 41
    if post_mortem is None:  # line 42
        post_mortem = pdb.post_mortem  # line 42
    class DebugTestResult(unittest.TextTestResult):  # line 43
        def addError(self, test, err):  # called before tearDown()  # line 44
            traceback.print_exception(*err)  # line 45
            post_mortem(err[2])  # line 46
            super(DebugTestResult, self).addError(test, err)  # line 47
        def addFailure(self, test, err):  # line 48
            traceback.print_exception(*err)  # line 49
            post_mortem(err[2])  # line 50
            super(DebugTestResult, self).addFailure(test, err)  # line 51
    return _coconut_tail_call(unittest.TextTestRunner, resultclass=DebugTestResult)  # line 52

def branchFolder(branch: 'int', revision: 'int') -> 'str':  # line 54
    return "." + os.sep + sos.metaFolder + os.sep + "b%d" % branch + os.sep + "r%d" % revision  # line 54

@_coconut_tco  # line 56
def wrapChannels(func: '_coconut.typing.Callable[..., Any]'):  # line 56
    ''' Wrap function call to capture and return strings emitted on stdout and stderr. '''  # line 57
    oldv, oldo, olde = sys.argv, sys.stdout, sys.stderr  # line 58
    buf = StringIO()  # line 59
    sys.stdout = sys.stderr = buf  # line 60
    handler = logging.StreamHandler(buf)  # line 61
    logging.getLogger().addHandler(handler)  # line 62
    try:  # capture output into buf  # line 63
        func()  # capture output into buf  # line 63
    except Exception as E:  # line 64
        buf.write(str(E) + "\n")  # line 64
        traceback.print_exc(file=buf)  # line 64
    except SystemExit as F:  # line 65
        buf.write(str(F) + "\n")  # line 65
        traceback.print_exc(file=buf)  # line 65
    logging.getLogger().removeHandler(handler)  # line 66
    sys.argv, sys.stdout, sys.stderr = oldv, oldo, olde  # line 67
    return _coconut_tail_call(buf.getvalue)  # line 68

def mockInput(datas: '_coconut.typing.Sequence[str]', func) -> 'Any':  # line 70
    with mock.patch("builtins.input" if sys.version_info.major >= 3 else "utility._coconut_raw_input", side_effect=datas):  # line 71
        return func()  # line 71

def setRepoFlag(name: 'str', value: 'bool') -> 'None':  # line 73
    with open(sos.metaFolder + os.sep + sos.metaFile, "r") as fd:  # line 74
        flags, branches = json.loads(fd.read())  # line 74
    flags[name] = value  # line 75
    with open(sos.metaFolder + os.sep + sos.metaFile, "w") as fd:  # line 76
        fd.write(json.dumps((flags, branches)))  # line 76

def checkRepoFlag(name: 'str', flag: 'bool') -> 'bool':  # line 78
    with open(sos.metaFolder + os.sep + sos.metaFile, "r") as fd:  # line 78
        flags, branches = json.loads(fd.read())  # line 79
    return name in flags and flags[name] == flag  # line 80


class Tests(unittest.TestCase):  # line 83
    ''' Entire test suite. '''  # line 84

    def setUp(_):  # line 86
        for entry in os.listdir(testFolder):  # cannot remove testFolder on Windows when using TortoiseSVN as VCS  # line 87
            resource = os.path.join(testFolder, entry)  # line 88
            shutil.rmtree(resource) if os.path.isdir(resource) else os.unlink(resource)  # line 89
        os.chdir(testFolder)  # line 90

    def assertAllIn(_, what: '_coconut.typing.Sequence[str]', where: 'Union[str, List[str]]') -> 'None':  # line 92
        [_.assertIn(w, where) for w in what]  # line 92

    def assertInAll(_, what: 'str', where: '_coconut.typing.Sequence[str]') -> 'None':  # line 94
        [_.assertIn(what, w) for w in where]  # line 94

    def assertInAny(_, what: 'str', where: '_coconut.typing.Sequence[str]') -> 'None':  # line 96
        _.assertTrue(any((what in w for w in where)))  # line 96

    def assertNotInAny(_, what: 'str', where: '_coconut.typing.Sequence[str]') -> 'None':  # line 98
        _.assertFalse(any((what in w for w in where)))  # line 98

    def createFile(_, number: 'Union[int, str]', contents: 'str'="x" * 10, prefix: '_coconut.typing.Optional[str]'=None) -> 'None':  # line 100
        if prefix and not os.path.exists(prefix):  # line 101
            os.makedirs(prefix)  # line 101
        with open(("." if prefix is None else prefix) + os.sep + (("file%d" % number) if isinstance(number, int) else number), "wb") as fd:  # line 102
            fd.write(contents if isinstance(contents, bytes) else contents.encode("cp1252"))  # line 102

    def existsFile(_, number: 'Union[int, str]', expectedContents: 'bytes'=None) -> 'bool':  # line 104
        if not os.path.exists(("." + os.sep + "file%d" % number) if isinstance(number, int) else number):  # line 105
            return False  # line 105
        if expectedContents is None:  # line 106
            return True  # line 106
        with open(("." + os.sep + "file%d" % number) if isinstance(number, int) else number, "rb") as fd:  # line 107
            return fd.read() == expectedContents  # line 107

    def testAccessor(_):  # line 109
        a = sos.Accessor({"a": 1})  # line 110
        _.assertEqual((1, 1), (a["a"], a.a))  # line 111

    def testFirstofmap(_):  # line 113
        _.assertEqual(2, sos.firstOfMap({"a": 1, "b": 2}, ["x", "b"]))  # line 114
        _.assertIsNone(sos.firstOfMap({"a": 1, "b": 2}, []))  # line 115

    def testAjoin(_):  # line 117
        _.assertEqual("a1a2", sos.ajoin("a", ["1", "2"]))  # line 118
        _.assertEqual("* a\n* b", sos.ajoin("* ", ["a", "b"], "\n"))  # line 119

    def testFindChanges(_):  # line 121
        m = sos.Metadata(os.getcwd())  # line 122
        m.loadBranches()  # line 123
        _.createFile(1, "1")  # line 124
        m.createBranch(0)  # line 125
        _.assertEqual(1, len(m.paths))  # line 126
        time.sleep(FS_PRECISION)  # time required by filesystem time resolution issues  # line 127
        _.createFile(1, "2")  # line 128
        _.createFile(2, "2")  # line 129
        changes = m.findChanges()  # detect time skew  # line 130
        _.assertEqual(1, len(changes.additions))  # line 131
        _.assertEqual(0, len(changes.deletions))  # line 132
        _.assertEqual(1, len(changes.modifications))  # line 133
        m.integrateChangeset(changes)  # line 134
        _.createFile(2, "12")  # modify file  # line 135
        changes = m.findChanges(0, 1)  # by size, creating new commit  # line 136
        _.assertEqual(0, len(changes.additions))  # line 137
        _.assertEqual(0, len(changes.deletions))  # line 138
        _.assertEqual(1, len(changes.modifications))  # line 139
        _.assertTrue(os.path.exists(branchFolder(0, 1)))  # line 140
        _.assertTrue(os.path.exists(branchFolder(0, 1) + os.sep + "03b69bc801ae11f1ff2a71a50f165996d0ad681b4f822df13329a27e53f0fcd2"))  # line 141

    def testDiffFunc(_):  # line 143
        a = {"./a": sos.PathInfo("", 0, 0, "")}  # line 144
        b = {"./a": sos.PathInfo("", 0, 0, "")}  # line 145
        changes = sos.diffPathSets(a, b)  # line 146
        _.assertEqual(0, len(changes.additions))  # line 147
        _.assertEqual(0, len(changes.deletions))  # line 148
        _.assertEqual(0, len(changes.modifications))  # line 149
        b = {"./a": sos.PathInfo("", 1, 0, "")}  # line 150
        changes = sos.diffPathSets(a, b)  # line 151
        _.assertEqual(0, len(changes.additions))  # line 152
        _.assertEqual(0, len(changes.deletions))  # line 153
        _.assertEqual(1, len(changes.modifications))  # line 154
        b = {}  # diff contains no entries -> no change  # line 155
        changes = sos.diffPathSets(a, b)  # line 156
        _.assertEqual(0, len(changes.additions))  # line 157
        _.assertEqual(0, len(changes.deletions))  # line 158
        _.assertEqual(0, len(changes.modifications))  # line 159
        b = {"./a": sos.PathInfo("", None, 1, "")}  # in diff marked as deleted  # line 160
        changes = sos.diffPathSets(a, b)  # line 161
        _.assertEqual(0, len(changes.additions))  # line 162
        _.assertEqual(1, len(changes.deletions))  # line 163
        _.assertEqual(0, len(changes.modifications))  # line 164
        b = {"./b": sos.PathInfo("", 1, 1, "")}  # line 165
        changes = sos.diffPathSets(a, b)  # line 166
        _.assertEqual(1, len(changes.additions))  # line 167
        _.assertEqual(0, len(changes.deletions))  # line 168
        _.assertEqual(0, len(changes.modifications))  # line 169
        a = {"./a": sos.PathInfo("", None, 0, "")}  # mark as deleted  # line 170
        b = {"./a": sos.PathInfo("", 1, 0, "")}  # re-added  # line 171
        changes = sos.diffPathSets(a, b)  # line 172
        _.assertEqual(1, len(changes.additions))  # line 173
        _.assertEqual(0, len(changes.deletions))  # line 174
        _.assertEqual(0, len(changes.modifications))  # line 175
        changes = sos.diffPathSets(b, a)  # line 176
        _.assertEqual(0, len(changes.additions))  # line 177
        _.assertEqual(1, len(changes.deletions))  # line 178
        _.assertEqual(0, len(changes.modifications))  # line 179

    def testPatternPaths(_):  # line 181
        sos.offline(options=["--track"])  # line 182
        os.mkdir("sub")  # line 183
        _.createFile("sub" + os.sep + "file1", "sdfsdf")  # line 184
        sos.add("./sub", "sub/file?")  # line 185
        sos.commit("test")  # should pick up sub/file1 pattern  # line 186
        _.assertEqual(2, len(os.listdir(os.path.join(sos.metaFolder, "b0", "r1"))))  # sub/file1 was added  # line 187
        _.createFile(1)  # line 188
        try:  # should not commit anything, as the file in base folder doesn't match the tracked pattern  # line 189
            sos.commit("nothing")  # should not commit anything, as the file in base folder doesn't match the tracked pattern  # line 189
            _.fail()  # should not commit anything, as the file in base folder doesn't match the tracked pattern  # line 189
        except:  # line 190
            pass  # line 190

    def testTokenizeGlobPattern(_):  # line 192
        _.assertEqual([], sos.tokenizeGlobPattern(""))  # line 193
        _.assertEqual([sos.GlobBlock(False, "*", 0)], sos.tokenizeGlobPattern("*"))  # line 194
        _.assertEqual([sos.GlobBlock(False, "*", 0), sos.GlobBlock(False, "???", 1)], sos.tokenizeGlobPattern("*???"))  # line 195
        _.assertEqual([sos.GlobBlock(True, "x", 0), sos.GlobBlock(False, "*", 1), sos.GlobBlock(True, "x", 2)], sos.tokenizeGlobPattern("x*x"))  # line 196
        _.assertEqual([sos.GlobBlock(True, "x", 0), sos.GlobBlock(False, "*", 1), sos.GlobBlock(False, "??", 2), sos.GlobBlock(False, "*", 4), sos.GlobBlock(True, "x", 5)], sos.tokenizeGlobPattern("x*??*x"))  # line 197
        _.assertEqual([sos.GlobBlock(False, "?", 0), sos.GlobBlock(True, "abc", 1), sos.GlobBlock(False, "*", 4)], sos.tokenizeGlobPattern("?abc*"))  # line 198

    def testTokenizeGlobPatterns(_):  # line 200
        try:  # because number of literal strings differs  # line 201
            sos.tokenizeGlobPatterns("x*x", "x*")  # because number of literal strings differs  # line 201
            _.fail()  # because number of literal strings differs  # line 201
        except:  # line 202
            pass  # line 202
        try:  # because glob patterns differ  # line 203
            sos.tokenizeGlobPatterns("x*", "x?")  # because glob patterns differ  # line 203
            _.fail()  # because glob patterns differ  # line 203
        except:  # line 204
            pass  # line 204
        try:  # glob patterns differ, regardless of position  # line 205
            sos.tokenizeGlobPatterns("x*", "?x")  # glob patterns differ, regardless of position  # line 205
            _.fail()  # glob patterns differ, regardless of position  # line 205
        except:  # line 206
            pass  # line 206
        sos.tokenizeGlobPatterns("x*", "*x")  # succeeds, because glob patterns match (differ only in position)  # line 207
        sos.tokenizeGlobPatterns("*xb?c", "*x?bc")  # succeeds, because glob patterns match (differ only in position)  # line 208
        try:  # succeeds, because glob patterns match (differ only in position)  # line 209
            sos.tokenizeGlobPatterns("a???b*", "ab???*")  # succeeds, because glob patterns match (differ only in position)  # line 209
            _.fail()  # succeeds, because glob patterns match (differ only in position)  # line 209
        except:  # line 210
            pass  # line 210

    def testConvertGlobFiles(_):  # line 212
        _.assertEqual(["xxayb", "aacb"], [r[1] for r in sos.convertGlobFiles(["axxby", "aabc"], *sos.tokenizeGlobPatterns("a*b?", "*a?b"))])  # line 213
        _.assertEqual(["1qq2ww3", "1abcbx2xbabc3"], [r[1] for r in sos.convertGlobFiles(["qqxbww", "abcbxxbxbabc"], *sos.tokenizeGlobPatterns("*xb*", "1*2*3"))])  # line 214

    def testFolderRemove(_):  # line 216
        m = sos.Metadata(os.getcwd())  # line 217
        _.createFile(1)  # line 218
        _.createFile("a", prefix="sub")  # line 219
        sos.offline()  # line 220
        _.createFile(2)  # line 221
        os.unlink("sub" + os.sep + "a")  # line 222
        os.rmdir("sub")  # line 223
        changes = sos.changes()  # line 224
        _.assertEqual(1, len(changes.additions))  # line 225
        _.assertEqual(0, len(changes.modifications))  # line 226
        _.assertEqual(1, len(changes.deletions))  # line 227
        _.createFile("a", prefix="sub")  # line 228
        changes = sos.changes()  # line 229
        _.assertEqual(0, len(changes.deletions))  # line 230

    def testComputeSequentialPathSet(_):  # line 232
        os.makedirs(branchFolder(0, 0))  # line 233
        os.makedirs(branchFolder(0, 1))  # line 234
        os.makedirs(branchFolder(0, 2))  # line 235
        os.makedirs(branchFolder(0, 3))  # line 236
        os.makedirs(branchFolder(0, 4))  # line 237
        m = sos.Metadata(os.getcwd())  # line 238
        m.branch = 0  # line 239
        m.commit = 2  # line 240
        m.saveBranches()  # line 241
        m.paths = {"./a": sos.PathInfo("", 0, 0, "")}  # line 242
        m.saveCommit(0, 0)  # initial  # line 243
        m.paths["./a"] = sos.PathInfo("", 1, 0, "")  # line 244
        m.saveCommit(0, 1)  # mod  # line 245
        m.paths["./b"] = sos.PathInfo("", 0, 0, "")  # line 246
        m.saveCommit(0, 2)  # add  # line 247
        m.paths["./a"] = sos.PathInfo("", None, 0, "")  # line 248
        m.saveCommit(0, 3)  # del  # line 249
        m.paths["./a"] = sos.PathInfo("", None, 0, "")  # line 250
        m.saveCommit(0, 4)  # readd  # line 251
        m.commits = {i: sos.CommitInfo(i, 0, None) for i in range(5)}  # line 252
        m.saveBranch(0)  # line 253
        m.computeSequentialPathSet(0, 4)  # line 254
        _.assertEqual(2, len(m.paths))  # line 255

    def testParseRevisionString(_):  # line 257
        m = sos.Metadata(os.getcwd())  # line 258
        m.branch = 1  # line 259
        m.commits = {0: 0, 1: 1, 2: 2}  # line 260
        _.assertEqual((1, 3), m.parseRevisionString("3"))  # line 261
        _.assertEqual((2, 3), m.parseRevisionString("2/3"))  # line 262
        _.assertEqual((1, -1), m.parseRevisionString(None))  # line 263
        _.assertEqual((1, -1), m.parseRevisionString(""))  # line 264
        _.assertEqual((2, -1), m.parseRevisionString("2/"))  # line 265
        _.assertEqual((1, -2), m.parseRevisionString("/-2"))  # line 266
        _.assertEqual((1, -1), m.parseRevisionString("/"))  # line 267

    def testOfflineEmpty(_):  # line 269
        os.mkdir("." + os.sep + sos.metaFolder)  # line 270
        try:  # line 271
            sos.offline("trunk")  # line 271
            _.fail()  # line 271
        except SystemExit:  # line 272
            pass  # line 272
        os.rmdir("." + os.sep + sos.metaFolder)  # line 273
        sos.offline("test")  # line 274
        _.assertIn(sos.metaFolder, os.listdir("."))  # line 275
        _.assertAllIn(["b0", sos.metaFile], os.listdir("." + os.sep + sos.metaFolder))  # line 276
        _.assertAllIn(["r0", sos.metaFile], os.listdir("." + os.sep + sos.metaFolder + os.sep + "b0"))  # line 277
        _.assertEqual(2, len(os.listdir("." + os.sep + sos.metaFolder)))  # only branch folder and meta data file  # line 278
        _.assertEqual(2, len(os.listdir("." + os.sep + sos.metaFolder + os.sep + "b0")))  # only commit folder and meta data file  # line 279
        _.assertEqual(1, len(os.listdir(branchFolder(0, 0))))  # only meta data file  # line 280

    def testOfflineWithFiles(_):  # line 282
        _.createFile(1, "x" * 100)  # line 283
        _.createFile(2)  # line 284
        sos.offline("test")  # line 285
        _.assertAllIn(["file1", "file2", sos.metaFolder], os.listdir("."))  # line 286
        _.assertAllIn(["b0", sos.metaFile], os.listdir("." + os.sep + sos.metaFolder))  # line 287
        _.assertAllIn(["r0", sos.metaFile], os.listdir("." + os.sep + sos.metaFolder + os.sep + "b0"))  # line 288
        _.assertAllIn([sos.metaFile, "03b69bc801ae11f1ff2a71a50f165996d0ad681b4f822df13329a27e53f0fcd2", "b9ee10a87f612e299a6eb208210bc0898092a64c48091327cc2aaeee9b764ffa"], os.listdir("." + os.sep + sos.metaFolder + os.sep + "b0" + os.sep + "r0"))  # line 289
        _.assertEqual(2, len(os.listdir("." + os.sep + sos.metaFolder)))  # only branch folder and meta data file  # line 290
        _.assertEqual(2, len(os.listdir("." + os.sep + sos.metaFolder + os.sep + "b0")))  # only commit folder and meta data file  # line 291
        _.assertEqual(3, len(os.listdir(branchFolder(0, 0))))  # only meta data file plus branch base file copies  # line 292

    def testBranch(_):  # line 294
        _.createFile(1, "x" * 100)  # line 295
        _.createFile(2)  # line 296
        sos.offline("test")  # b0/r0  # line 297
        sos.branch("other")  # b1/r0  # line 298
        _.assertAllIn(["b0", "b1", sos.metaFile], os.listdir("." + os.sep + sos.metaFolder))  # line 299
        _.assertEqual(list(sorted(os.listdir("." + os.sep + sos.metaFolder + os.sep + "b0"))), list(sorted(os.listdir("." + os.sep + sos.metaFolder + os.sep + "b1"))))  # line 300
        _.assertEqual(list(sorted(os.listdir(branchFolder(0, 0)))), list(sorted(os.listdir(branchFolder(1, 0)))))  # line 302
        _.createFile(1, "z")  # modify file  # line 304
        sos.branch()  # b2/r0  branch to unnamed branch with modified file tree contents  # line 305
        _.assertNotEqual(os.stat("." + os.sep + sos.metaFolder + os.sep + "b1" + os.sep + "r0" + os.sep + "b9ee10a87f612e299a6eb208210bc0898092a64c48091327cc2aaeee9b764ffa").st_size, os.stat("." + os.sep + sos.metaFolder + os.sep + "b2" + os.sep + "r0" + os.sep + "b9ee10a87f612e299a6eb208210bc0898092a64c48091327cc2aaeee9b764ffa").st_size)  # line 306
        _.createFile(3, "z")  # line 308
        sos.branch("from_last_revision", ["--last", "--stay"])  # b3/r0 create copy of other file1,file2 and don't switch  # line 309
        _.assertEqual(list(sorted(os.listdir("." + os.sep + sos.metaFolder + os.sep + "b3" + os.sep + "r0"))), list(sorted(os.listdir("." + os.sep + sos.metaFolder + os.sep + "b2" + os.sep + "r0"))))  # line 310
# Check sos.status output which branch is marked


    def testComittingAndChanges(_):  # line 315
        _.createFile(1, "x" * 100)  # line 316
        _.createFile(2)  # line 317
        sos.offline("test")  # line 318
        changes = sos.changes()  # line 319
        _.assertEqual(0, len(changes.additions))  # line 320
        _.assertEqual(0, len(changes.deletions))  # line 321
        _.assertEqual(0, len(changes.modifications))  # line 322
        _.createFile(1, "z")  # size change  # line 323
        changes = sos.changes()  # line 324
        _.assertEqual(0, len(changes.additions))  # line 325
        _.assertEqual(0, len(changes.deletions))  # line 326
        _.assertEqual(1, len(changes.modifications))  # line 327
        sos.commit("message")  # line 328
        _.assertAllIn(["r0", "r1", sos.metaFile], os.listdir("." + os.sep + sos.metaFolder + os.sep + "b0"))  # line 329
        _.assertAllIn([sos.metaFile, "b9ee10a87f612e299a6eb208210bc0898092a64c48091327cc2aaeee9b764ffa"], os.listdir(branchFolder(0, 1)))  # line 330
        _.assertEqual(2, len(os.listdir(branchFolder(0, 1))))  # no further files, only the modified one  # line 331
        _.assertEqual(1, len(sos.changes("/0").modifications))  # vs. explicit revision on current branch  # line 332
        _.assertEqual(1, len(sos.changes("0/0").modifications))  # vs. explicit branch/revision  # line 333
        _.createFile(1, "")  # modify to empty file, mentioned in meta data, but not stored as own file  # line 334
        os.unlink("file2")  # line 335
        changes = sos.changes()  # line 336
        _.assertEqual(0, len(changes.additions))  # line 337
        _.assertEqual(1, len(changes.deletions))  # line 338
        _.assertEqual(1, len(changes.modifications))  # line 339
        sos.commit("modified")  # line 340
        _.assertEqual(1, len(os.listdir(branchFolder(0, 2))))  # no additional files, only mentions in metadata  # line 341
        try:  # expecting Exit due to no changes  # line 342
            sos.commit("nothing")  # expecting Exit due to no changes  # line 342
            _.fail()  # expecting Exit due to no changes  # line 342
        except:  # line 343
            pass  # line 343

    def testGetBranch(_):  # line 345
        m = sos.Metadata(os.getcwd())  # line 346
        m.branch = 1  # current branch  # line 347
        m.branches = {0: sos.BranchInfo(0, 0, "trunk")}  # line 348
        _.assertEqual(27, m.getBranchByName(27))  # line 349
        _.assertEqual(0, m.getBranchByName("trunk"))  # line 350
        _.assertEqual(1, m.getBranchByName(""))  # split from "/"  # line 351
        _.assertIsNone(m.getBranchByName("unknown"))  # line 352
        m.commits = {0: sos.CommitInfo(0, 0, "bla")}  # line 353
        _.assertEqual(13, m.getRevisionByName("13"))  # line 354
        _.assertEqual(0, m.getRevisionByName("bla"))  # line 355
        _.assertEqual(-1, m.getRevisionByName(""))  # split from "/"  # line 356

    def testTagging(_):  # line 358
        m = sos.Metadata(os.getcwd())  # line 359
        sos.offline()  # line 360
        _.createFile(111)  # line 361
        sos.commit("tag", ["--tag"])  # line 362
        _.createFile(2)  # line 363
        try:  # line 364
            sos.commit("tag")  # line 364
            _.fail()  # line 364
        except:  # line 365
            pass  # line 365
        sos.commit("tag-2", ["--tag"])  # line 366

    def testSwitch(_):  # line 368
        _.createFile(1, "x" * 100)  # line 369
        _.createFile(2, "y")  # line 370
        sos.offline("test")  # file1-2  in initial branch commit  # line 371
        sos.branch("second")  # file1-2  switch, having same files  # line 372
        sos.switch("0")  # no change  switch back, no problem  # line 373
        sos.switch("second")  # no change  # switch back, no problem  # line 374
        _.createFile(3, "y")  # generate a file  # line 375
        try:  # uncommited changes detected  # line 376
            sos.switch("test")  # uncommited changes detected  # line 376
            _.fail()  # uncommited changes detected  # line 376
        except SystemExit:  # line 377
            pass  # line 377
        sos.commit("Finish")  # file1-3  commit third file into branch second  # line 378
        sos.changes()  # line 379
        sos.switch("test")  # file1-2, remove file3 from file tree  # line 380
        _.assertFalse(_.existsFile(3))  # removed when switching back to test  # line 381
        out = wrapChannels(lambda: sos.status()).replace("\r", "")  # line 382
        _.assertIn("  * b00   'test'", out)  # line 383
        _.assertIn("    b01 'second'", out)  # line 384
        _.assertIn("(dirty)", out)  # one branch has commits  # line 385
        _.assertIn("(in sync)", out)  # the other doesn't  # line 386
        _.createFile(4, "xy")  # generate a file  # line 387
        sos.switch("second", "--force")  # avoids warning on uncommited changes, but keeps file4  # line 388
        _.assertFalse(_.existsFile(4))  # removed when forcedly switching back to test  # line 389
        _.assertTrue(_.existsFile(3))  # was restored from branch's revision r1  # line 390
        os.unlink("." + os.sep + "file1")  # remove old file1  # line 391
        sos.switch("test", "--force")  # should restore file1 and remove file3  # line 392
        _.assertTrue(_.existsFile(1))  # was restored from branch's revision r1  # line 393
        _.assertFalse(_.existsFile(3))  # was restored from branch's revision r1  # line 394

    def testAutoDetectVCS(_):  # line 396
        os.mkdir(".git")  # line 397
        sos.offline(sos.vcsBranches[sos.findSosVcsBase()[2]])  # create initial branch  # line 398
        with open(sos.metaFolder + os.sep + sos.metaFile, "r") as fd:  # line 399
            meta = fd.read()  # line 399
        _.assertTrue("\"master\"" in meta)  # line 400
        os.rmdir(".git")  # line 401

    def testUpdate(_):  # line 403
        sos.offline("trunk")  # create initial branch b0/r0  # line 404
        _.createFile(1, "x" * 100)  # line 405
        sos.commit("second")  # create b0/r1  # line 406

        sos.switch("/0")  # go back to b0/r0 - deletes file1  # line 408
        _.assertFalse(_.existsFile(1))  # line 409

        sos.update("/1")  # recreate file1  # line 411
        _.assertTrue(_.existsFile(1))  # line 412

        sos.commit("third", ["--force"])  # force because nothing to commit. should create r2 with same contents as r1, but as differential from r1, not from r0 (= no changes in meta folder)  # line 414
        _.assertTrue(os.path.exists(branchFolder(0, 2)))  # line 415
        _.assertTrue(os.path.exists(branchFolder(0, 2) + os.sep + sos.metaFile))  # line 416
        _.assertEqual(1, len(os.listdir(branchFolder(0, 2))))  # only meta data file, no differential files  # line 417

        sos.update("/1")  # do nothing, as nothing has changed  # line 419
        _.assertTrue(_.existsFile(1))  # line 420

        _.createFile(2, "y" * 100)  # line 422
#    out = wrapChannels(() -> sos.branch("other"))  # won't comply as there are changes
#    _.assertIn("--force", out)
        sos.branch("other", ["--force"])  # automatically including file 2 (as we are in simple mode)  # line 425
        _.assertTrue(_.existsFile(2))  # line 426
        sos.update("trunk", ["--add"])  # only add stuff  # line 427
        _.assertTrue(_.existsFile(2))  # line 428
        sos.update("trunk")  # nothing to do  # line 429
        _.assertFalse(_.existsFile(2))  # removes file not present in original branch  # line 430

        theirs = b"a\nb\nc\nd\ne\nf\ng\nh\nx\nx\nj\nk"  # line 432
        _.createFile(10, theirs)  # line 433
        mine = b"a\nc\nd\ne\ng\nf\nx\nh\ny\ny\nj"  # missing "b", inserted g, modified g->x, replace x/x -> y/y, removed k  # line 434
        _.createFile(11, mine)  # line 435
        _.assertEqual(b"a\nb\nc\nd\ne\nf\ng\nh\nx\nx\nj\nk", sos.merge(filename="." + os.sep + "file10", intoname="." + os.sep + "file11", mergeOperation=sos.MergeOperation.BOTH, conflictResolution=sos.ConflictResolution.THEIRS))  # completely recreated other file  # line 436
        _.assertEqual(b"a\nb\nc\nd\ne\ng\nf\ng\nx\nh\nx\nx\ny\ny\nj\nk", sos.merge(filename="." + os.sep + "file10", intoname="." + os.sep + "file11", mergeOperation=sos.MergeOperation.INSERT, conflictResolution=sos.ConflictResolution.MINE))  # line 437

    def testUpdate2(_):  # line 439
        _.createFile("test.txt", "x" * 10)  # line 440
        sos.offline("trunk", ["--strict"])  # use strict mode, as timestamp differences are too small for testing  # line 441
        sos.branch("mod")  # line 442
        _.createFile("test.txt", "x" * 5 + "y" * 5)  # line 443
        time.sleep(FS_PRECISION)  # line 444
        sos.commit("mod")  # create b0/r1  # line 445
        sos.switch("trunk", ["--force"])  # should replace contents, force in case some other files were modified (e.g. during working on the code) TODO investigate more  # line 446
        with open("test.txt", "rb") as fd:  # line 447
            _.assertEqual(b"x" * 10, fd.read())  # line 447
        sos.update("mod", ["--theirs"])  # integrate changes TODO same with ask -> theirs  # line 448
        with open("test.txt", "rb") as fd:  # line 449
            _.assertEqual(b"x" * 5 + b"y" * 5, fd.read())  # line 449
        _.createFile("test.txt", "x" * 10)  # line 450
        mockInput(["t"], lambda: sos.update("mod", ["--ask"]))  # same as above with interaction -> theirs  # line 451
        with open("test.txt", "rb") as fd:  # line 452
            _.assertEqual(b"x" * 5 + b"y" * 5, fd.read())  # line 452

    def testIsTextType(_):  # line 454
        m = sos.Metadata(".")  # line 455
        m.c.texttype = ["*.x", "*.md", "*.md.*"]  # line 456
        m.c.bintype = ["*.md.confluence"]  # line 457
        _.assertTrue(m.isTextType("ab.txt"))  # line 458
        _.assertTrue(m.isTextType("./ab.txt"))  # line 459
        _.assertTrue(m.isTextType("bc/ab.txt"))  # line 460
        _.assertFalse(m.isTextType("bc/ab."))  # line 461
        _.assertTrue(m.isTextType("23_3.x.x"))  # line 462
        _.assertTrue(m.isTextType("dfg/dfglkjdf7/test.md"))  # line 463
        _.assertTrue(m.isTextType("./test.md.pdf"))  # line 464
        _.assertFalse(m.isTextType("./test_a.md.confluence"))  # line 465

    def testEolDet(_):  # line 467
        ''' Check correct end-of-line detection. '''  # line 468
        _.assertEqual(b"\n", sos.eoldet(b"a\nb"))  # line 469
        _.assertEqual(b"\r\n", sos.eoldet(b"a\r\nb\r\n"))  # line 470
        _.assertEqual(b"\r", sos.eoldet(b"\ra\rb"))  # line 471
        _.assertAllIn(["Inconsistent", "with "], wrapChannels(lambda: _.assertEqual(b"\n", sos.eoldet(b"\r\na\r\nb\n"))))  # line 472
        _.assertAllIn(["Inconsistent", "without"], wrapChannels(lambda: _.assertEqual(b"\n", sos.eoldet(b"\ra\nnb\n"))))  # line 473
        _.assertIsNone(sos.eoldet(b""))  # line 474
        _.assertIsNone(sos.eoldet(b"sdf"))  # line 475

    def testMerge(_):  # line 477
        ''' Check merge results depending on conflict solution options. '''  # line 478
        a = b"a\nb\ncc\nd"  # line 479
        b = b"a\nb\nee\nd"  # line 480
        _.assertEqual(b"a\nb\ncc\nee\nd", sos.merge(a, b, mergeOperation=sos.MergeOperation.INSERT))  # means insert changes from a into b, but don't replace  # line 481
        _.assertEqual(b"a\nb\nd", sos.merge(a, b, mergeOperation=sos.MergeOperation.REMOVE))  # line 482
        _.assertEqual(b"a\nb\ncc\nd", sos.merge(a, b, mergeOperation=sos.MergeOperation.BOTH))  # line 483
# Now test intra-line merging without conflicts
        _.assertEqual(b"a\nbc d\ne", sos.merge(b"a\nbc d\ne", b"a\nbcd\ne", mergeOperation=sos.MergeOperation.INSERT))  # because it's a deletion ['  a', '- bc d', '?   -\n', '+ bcd', '  e']  # line 485
        _.assertEqual(b"a\nbcd\ne", sos.merge(b"a\nbc d\ne", b"a\nbcd\ne", mergeOperation=sos.MergeOperation.REMOVE))  # ['  a', '- bc d', '?   -\n', '+ bcd', '  e']  # line 486
        _.assertEqual(b"a\nbc d\ne", sos.merge(b"a\nbcd\ne", b"a\nbc d\ne", mergeOperation=sos.MergeOperation.INSERT))  # nothing to insert  # line 487
        _.assertEqual(b"a\nbcd\ne", sos.merge(b"a\nbcd\ne", b"a\nbc d\ne", mergeOperation=sos.MergeOperation.REMOVE))  # remove space  # line 488
# Test with change + insert (conflict)
        _.assertEqual(b"a\nb fdd d\ne", sos.merge(b"a\nb cd d\ne", b"a\nb fdd d\ne", conflictResolution=sos.ConflictResolution.MINE))  # line 490
        _.assertEqual(b"a\nb cd d\ne", sos.merge(b"a\nb cd d\ne", b"a\nb fdd d\ne", conflictResolution=sos.ConflictResolution.THEIRS))  # ['  a', '- b cd d', '?   ^\n', '+ b fdd d', '?   ^^\n', '  e']  # line 491
        _.assertEqual(b"a\nb fdd d\ne", mockInput(["i"], lambda: sos.merge(b"a\nb cd d\ne", b"a\nb fdd d\ne", conflictResolution=sos.ConflictResolution.ASK)))  # ['  a', '- b cd d', '?   ^\n', '+ b fdd d', '?   ^^\n', '  e']  # line 492
        _.assertEqual(b"a\nb cd d\ne", mockInput(["t"], lambda: sos.merge(b"a\nb cd d\ne", b"a\nb fdd d\ne", conflictResolution=sos.ConflictResolution.ASK)))  # ['  a', '- b cd d', '?   ^\n', '+ b fdd d', '?   ^^\n', '  e']  # line 493
        _.assertEqual(b"abbc", sos.merge(b"abbc", b"addc", mergeOperation=sos.MergeOperation.BOTH, conflictResolution=sos.ConflictResolution.THEIRS))  # line 494
        _.assertEqual(b"a\nbb\nc", sos.merge(b"a\nbb\nc", b"a\ndd\nc", mergeOperation=sos.MergeOperation.BOTH, conflictResolution=sos.ConflictResolution.THEIRS))  # line 495
        _.assertIn("Differing EOL-styles", wrapChannels(lambda: sos.merge(b"a\nb", b"a\r\nb")))  # expect warning  # line 496
        _.assertIn(b"a\r\nb", sos.merge(b"a\nb", b"a\r\nb"))  # in doubt, use "mine" CR-LF  # line 497

    def testPickyMode(_):  # line 499
        ''' Confirm that picky mode reset tracked patterns after commits. '''  # line 500
        sos.offline("trunk", ["--picky"])  # line 501
        changes = sos.changes()  # line 502
        _.assertEqual(0, len(changes.additions))  # do not list any existing file as an addition  # line 503
        sos.add(".", "./file?", ["--force"])  # line 504
        _.createFile(1, "aa")  # line 505
        sos.commit("First")  # add one file  # line 506
        _.assertEqual(2, len(os.listdir(branchFolder(0, 1))))  # line 507
        _.createFile(2, "b")  # line 508
        try:  # add nothing, because picky  # line 509
            sos.commit("Second")  # add nothing, because picky  # line 509
        except:  # line 510
            pass  # line 510
        sos.add(".", "./file?")  # line 511
        sos.commit("Third")  # line 512
        _.assertEqual(2, len(os.listdir(branchFolder(0, 2))))  # line 513
        out = wrapChannels(lambda: sos.log([])).replace("\r", "")  # line 514
        _.assertIn("  * r2", out)  # line 515

    def testTrackedSubfolder(_):  # line 517
        ''' See if patterns for files in sub folders are picked up correctly. '''  # line 518
        os.mkdir("." + os.sep + "sub")  # line 519
        sos.offline("trunk", ["--track"])  # line 520
        _.createFile(1, "x")  # line 521
        _.createFile(1, "x", prefix="sub")  # line 522
        sos.add(".", "./file?")  # add glob pattern to track  # line 523
        sos.commit("First")  # line 524
        _.assertEqual(2, len(os.listdir(branchFolder(0, 1))))  # one new file + meta file  # line 525
        sos.add(".", "sub/file?")  # add glob pattern to track  # line 526
        sos.commit("Second")  # one new file + meta  # line 527
        _.assertEqual(2, len(os.listdir(branchFolder(0, 1))))  # one new file + meta file  # line 528
        os.unlink("file1")  # remove from basefolder  # line 529
        _.createFile(2, "y")  # line 530
        sos.remove(".", "sub/file?")  # line 531
        try:  # raises Exit. TODO test the "suggest a pattern" case  # line 532
            sos.remove(".", "sub/bla")  # raises Exit. TODO test the "suggest a pattern" case  # line 532
            _.fail()  # raises Exit. TODO test the "suggest a pattern" case  # line 532
        except:  # line 533
            pass  # line 533
        sos.commit("Third")  # line 534
        _.assertEqual(2, len(os.listdir(branchFolder(0, 2))))  # one new file + meta  # line 535
# TODO check if /file1 and sub/file1 were removed from index

    def testTrackedMode(_):  # line 538
        ''' Difference in semantics vs simple mode:
          - For remote/other branch we can only know and consider tracked files, thus ignoring all complexity stemming from handling addition of untracked files.
          - For current branch, we can take into account tracked and untracked ones, in theory, but it doesn't make sense.
        In conclusion, using the union of tracking patterns from both sides to find affected files makes sense, but disallow deleting files not present in remote branch.
    '''  # line 543
        sos.offline("test", options=["--track"])  # set up repo in tracking mode (SVN- or gitless-style)  # line 544
        _.createFile(1)  # line 545
        _.createFile("a123a")  # untracked file "a123a"  # line 546
        sos.add(".", "./file?")  # add glob tracking pattern  # line 547
        sos.commit("second")  # versions "file1"  # line 548
        _.assertEqual(2, len(os.listdir(branchFolder(0, 1))))  # one new file + meta file  # line 549
        out = wrapChannels(lambda: sos.status()).replace("\r", "")  # line 550
        _.assertIn("  | ./file?", out)  # line 551

        _.createFile(2)  # untracked file "file2"  # line 553
        sos.commit("third")  # versions "file2"  # line 554
        _.assertEqual(2, len(os.listdir(branchFolder(0, 2))))  # one new file + meta file  # line 555

        os.mkdir("." + os.sep + "sub")  # line 557
        _.createFile(3, prefix="sub")  # untracked file "sub/file3"  # line 558
        sos.commit("fourth", ["--force"])  # no tracking pattern matches the subfolder  # line 559
        _.assertEqual(1, len(os.listdir(branchFolder(0, 3))))  # meta file only, no other tracked path/file  # line 560

        sos.branch("Other")  # second branch containing file1 and file2 tracked by "./file?"  # line 562
        sos.remove(".", "./file?")  # remove tracking pattern, but don't touch previously created and versioned files  # line 563
        sos.add(".", "./a*a")  # add tracking pattern  # line 564
        changes = sos.changes()  # should pick up addition only, because tracked, but not the deletion, as not tracked anymore  # line 565
        _.assertEqual(0, len(changes.modifications))  # line 566
        _.assertEqual(0, len(changes.deletions))  # not tracked anymore, but contained in version history and not removed  # line 567
        _.assertEqual(1, len(changes.additions))  # detected one addition "a123a", but won't recognize untracking files as deletion  # line 568

        sos.commit("Second_2")  # line 570
        _.assertEqual(2, len(os.listdir(branchFolder(1, 1))))  # "a123a" + meta file  # line 571
        _.assertTrue(os.path.exists("." + os.sep + "file1"))  # line 572
        _.assertTrue(os.path.exists("." + os.sep + "file2"))  # line 573

        sos.switch("test")  # go back to first branch - tracks only "file?", but not "a*a"  # line 575
        _.assertTrue(os.path.exists("." + os.sep + "file1"))  # line 576
        _.assertTrue(os.path.exists("." + os.sep + "a123a"))  # should not have been touched so far  # line 577

        sos.update("Other")  # integrate tracked files and tracking pattern from second branch into working state of master branch  # line 579
        _.assertTrue(os.path.exists("." + os.sep + "file1"))  # line 580
        _.assertTrue(os.path.exists("." + os.sep + "a123a"))  # line 581

        _.createFile("axxxa")  # new file that should be tracked on "test" now that we integrated "Other"  # line 583
        sos.commit("fifth")  # create new revision after integrating updates from second branch  # line 584
        _.assertEqual(3, len(os.listdir(branchFolder(0, 4))))  # one new file from other branch + one new in current folder + meta file  # line 585
        sos.switch("Other")  # switch back to just integrated branch that tracks only "a*a" - shouldn't do anything  # line 586
        _.assertTrue(os.path.exists("." + os.sep + "file1"))  # line 587
        _.assertTrue(os.path.exists("." + os.sep + "a123a"))  # line 588
        _.assertFalse(os.path.exists("." + os.sep + "axxxa"))  # because tracked in both branches, but not present in other -> delete in file tree TODO document  # line 589
# TODO test switch --meta

    def testLsTracked(_):  # line 592
        sos.offline("test", options=["--track"])  # set up repo in tracking mode (SVN- or gitless-style)  # line 593
        _.createFile(1)  # line 594
        _.createFile("foo")  # line 595
        sos.add(".", "./file*")  # capture one file  # line 596
        out = sos.safeSplit(wrapChannels(lambda: sos.ls()).replace("\r", ""), "\n")  # line 597
        _.assertInAny('TRK file1 by "./file*"', out)  # line 598
        _.assertNotInAny('... file1 by "./file*"', out)  # line 599
        _.assertInAny("... foo", out)  # line 600
        out = sos.safeSplit(wrapChannels(lambda: sos.ls(options=["--patterns"])).replace("\r", ""), "\n")  # line 601
        _.assertInAny("TRK ./file*", out)  # line 602

    def testCompression(_):  # line 604
        _.createFile(1)  # line 605
        sos.offline("master", options=["--plain", "--force"])  # line 606
        _.assertTrue(_.existsFile(branchFolder(0, 0) + os.sep + "b9ee10a87f612e299a6eb208210bc0898092a64c48091327cc2aaeee9b764ffa", b"x" * 10))  # line 607
        setRepoFlag("compress", True)  # was plain = uncompressed before  # line 608
        _.createFile(2)  # line 609
        sos.commit("Added file2")  # line 610
        _.assertTrue(_.existsFile(branchFolder(0, 1) + os.sep + "03b69bc801ae11f1ff2a71a50f165996d0ad681b4f822df13329a27e53f0fcd2"))  # exists  # line 611
        _.assertFalse(_.existsFile(branchFolder(0, 1) + os.sep + "03b69bc801ae11f1ff2a71a50f165996d0ad681b4f822df13329a27e53f0fcd2", b"x" * 10))  # but is compressed instead  # line 612

    def testConfigVariations(_):  # line 614
        def makeRepo():  # line 615
            try:  # line 616
                os.unlink("file1")  # line 616
            except:  # line 617
                pass  # line 617
            sos.offline("master", options=["--plain", "--force"])  # line 618
            _.createFile(1)  # line 619
            sos.commit("Added file1")  # line 620
        sos.config("set", ["strict", "on"])  # line 621
        makeRepo()  # line 622
        _.assertTrue(checkRepoFlag("strict", True))  # line 623
        sos.config("set", ["strict", "off"])  # line 624
        makeRepo()  # line 625
        _.assertTrue(checkRepoFlag("strict", False))  # line 626
        sos.config("set", ["strict", "yes"])  # line 627
        makeRepo()  # line 628
        _.assertTrue(checkRepoFlag("strict", True))  # line 629
        sos.config("set", ["strict", "no"])  # line 630
        makeRepo()  # line 631
        _.assertTrue(checkRepoFlag("strict", False))  # line 632
        sos.config("set", ["strict", "1"])  # line 633
        makeRepo()  # line 634
        _.assertTrue(checkRepoFlag("strict", True))  # line 635
        sos.config("set", ["strict", "0"])  # line 636
        makeRepo()  # line 637
        _.assertTrue(checkRepoFlag("strict", False))  # line 638
        sos.config("set", ["strict", "true"])  # line 639
        makeRepo()  # line 640
        _.assertTrue(checkRepoFlag("strict", True))  # line 641
        sos.config("set", ["strict", "false"])  # line 642
        makeRepo()  # line 643
        _.assertTrue(checkRepoFlag("strict", False))  # line 644
        sos.config("set", ["strict", "enable"])  # line 645
        makeRepo()  # line 646
        _.assertTrue(checkRepoFlag("strict", True))  # line 647
        sos.config("set", ["strict", "disable"])  # line 648
        makeRepo()  # line 649
        _.assertTrue(checkRepoFlag("strict", False))  # line 650
        sos.config("set", ["strict", "enabled"])  # line 651
        makeRepo()  # line 652
        _.assertTrue(checkRepoFlag("strict", True))  # line 653
        sos.config("set", ["strict", "disabled"])  # line 654
        makeRepo()  # line 655
        _.assertTrue(checkRepoFlag("strict", False))  # line 656
        try:  # line 657
            sos.config("set", ["strict", "nope"])  # line 657
            _.fail()  # line 657
        except:  # line 658
            pass  # line 658

    def testLsSimple(_):  # line 660
        _.createFile(1)  # line 661
        _.createFile("foo")  # line 662
        _.createFile("ign1")  # line 663
        _.createFile("ign2")  # line 664
        sos.offline("test")  # set up repo in tracking mode (SVN- or gitless-style)  # line 665
        sos.config("set", ["ignores", "ign1"])  # define an ignore pattern  # line 666
        sos.config("add", ["ignores", "ign2"])  # define an ignore pattern  # line 667
        sos.config("set", ["ignoresWhitelist", "ign1;ign2"])  # define a list of ignore patterns  # line 668
        out = wrapChannels(lambda: sos.config("show")).replace("\r", "")  # line 669
        _.assertIn("ignores => ['ign1', 'ign2']", out)  # line 670
        out = sos.safeSplit(wrapChannels(lambda: sos.ls()).replace("\r", ""), "\n")  # line 671
        _.assertInAny('... file1', out)  # line 672
        _.assertInAny('... ign1', out)  # line 673
        _.assertInAny('... ign2', out)  # line 674
        try:  # line 675
            sos.config("rm", ["foo", "bar"])  # line 675
            _.fail()  # line 675
        except:  # line 676
            pass  # line 676
        try:  # line 677
            sos.config("rm", ["ignores", "foo"])  # line 677
            _.fail()  # line 677
        except:  # line 678
            pass  # line 678
        sos.config("rm", ["ignores", "ign1"])  # line 679
        sos.config("unset", ["ignoresWhitelist"])  # remove ignore pattern  # line 680
        out = sos.safeSplit(wrapChannels(lambda: sos.ls()).replace("\r", ""), "\n")  # line 681
        _.assertInAny('... ign1', out)  # line 682
        _.assertInAny('IGN ign2', out)  # line 683
        _.assertNotInAny('... ign2', out)  # line 684

    def testWhitelist(_):  # line 686
# TODO test same for simple mode
        _.createFile(1)  # line 688
        sos.defaults.ignores[:] = ["file*"]  # replace in-place  # line 689
        sos.offline("xx", ["--track", "--strict"])  # because nothing to commit due to ignore pattern  # line 690
        sos.add(".", "./file*")  # add tracking pattern for "file1"  # line 691
        sos.commit(options=["--force"])  # attempt to commit the file  # line 692
        _.assertEqual(1, len(os.listdir(branchFolder(0, 1))))  # only meta data, file1 was ignored  # line 693
        try:  # Exit because dirty  # line 694
            sos.online()  # Exit because dirty  # line 694
            _.fail()  # Exit because dirty  # line 694
        except:  # exception expected  # line 695
            pass  # exception expected  # line 695
        _.createFile("x2")  # add another change  # line 696
        sos.add(".", "./x?")  # add tracking pattern for "file1"  # line 697
        try:  # force beyond dirty flag check  # line 698
            sos.online(["--force"])  # force beyond dirty flag check  # line 698
            _.fail()  # force beyond dirty flag check  # line 698
        except:  # line 699
            pass  # line 699
        sos.online(["--force", "--force"])  # force beyond file tree modifications check  # line 700
        _.assertFalse(os.path.exists(sos.metaFolder))  # line 701

        _.createFile(1)  # line 703
        sos.defaults.ignoresWhitelist[:] = ["file*"]  # line 704
        sos.offline("xx", ["--track"])  # line 705
        sos.add(".", "./file*")  # line 706
        sos.commit()  # should NOT ask for force here  # line 707
        _.assertEqual(2, len(os.listdir(branchFolder(0, 1))))  # meta data and "file1", file1 was whitelisted  # line 708

    def testRemove(_):  # line 710
        _.createFile(1, "x" * 100)  # line 711
        sos.offline("trunk")  # line 712
        try:  # line 713
            sos.delete("trunk")  # line 713
            _fail()  # line 713
        except:  # line 714
            pass  # line 714
        _.createFile(2, "y" * 10)  # line 715
        sos.branch("added")  # line 716
        sos.delete("trunk")  # line 717
        _.assertEqual(2, len(os.listdir("." + os.sep + sos.metaFolder)))  # meta data file and "b1"  # line 718
        _.assertTrue(os.path.exists("." + os.sep + sos.metaFolder + os.sep + "b1"))  # line 719
        _.assertFalse(os.path.exists("." + os.sep + sos.metaFolder + os.sep + "b0"))  # line 720
        sos.branch("next")  # line 721
        _.createFile(3, "y" * 10)  # make a change  # line 722
        sos.delete("added", "--force")  # should succeed  # line 723

    def testUsage(_):  # line 725
        sos.usage()  # line 726

    def testOnly(_):  # line 728
        _.assertEqual((_coconut.frozenset(("./A", "x/B")), _coconut.frozenset(("./C",))), sos.parseOnlyOptions(".", ["abc", "def", "--only", "A", "--x", "--only", "x/B", "--except", "C", "--only"]))  # line 729
        _.assertEqual(_coconut.frozenset(("B",)), sos.conditionalIntersection(_coconut.frozenset(("A", "B", "C")), _coconut.frozenset(("B", "D"))))  # line 730
        _.assertEqual(_coconut.frozenset(("B", "D")), sos.conditionalIntersection(_coconut.frozenset(), _coconut.frozenset(("B", "D"))))  # line 731
        _.assertEqual(_coconut.frozenset(("B", "D")), sos.conditionalIntersection(None, _coconut.frozenset(("B", "D"))))  # line 732
        sos.offline(os.getcwd(), ["--track", "--strict"])  # line 733
        _.createFile(1)  # line 734
        _.createFile(2)  # line 735
        sos.add(".", "./file1")  # line 736
        sos.add(".", "./file2")  # line 737
        sos.commit(onlys=_coconut.frozenset(("./file1",)))  # line 738
        _.assertEqual(2, len(os.listdir(branchFolder(0, 1))))  # only meta and file1  # line 739
        sos.commit()  # adds also file2  # line 740
        _.assertEqual(2, len(os.listdir(branchFolder(0, 2))))  # only meta and file1  # line 741
        _.createFile(1, "cc")  # modify both files  # line 742
        _.createFile(2, "dd")  # line 743
        changes = sos.changes(excps=["./file1"])  # line 744
        _.assertEqual(1, len(changes.modifications))  # only file2  # line 745
        _.assertTrue("./file2" in changes.modifications)  # line 746
        _.assertAllIn(["MOD ./file2", "DIF ./file2"], wrapChannels(lambda: sos.diff(onlys=_coconut.frozenset(("./file2",)))))  # line 747

    def testDiff(_):  # line 749
        sos.offline(options=["--strict"])  # line 750
        _.createFile(1)  # line 751
        _.createFile(2)  # line 752
        sos.commit()  # line 753
        _.createFile(1, "sdfsdgfsdf")  # line 754
        _.createFile(2, "12343")  # line 755
        sos.commit()  # line 756
        _.createFile(1, "foobar")  # line 757
        _.assertAllIn(["MOD ./file1", "MOD ./file2", "DIF ./file1", "- | 0000 |xxxxxxxxxx|", "+ | 0000 |foobar|"], wrapChannels(lambda: sos.diff("/-2")))  # vs. second last  # line 758
        _.assertNotIn("MOD ./file1", wrapChannels(lambda: sos.diff("/-2", onlys=_coconut.frozenset(("./file2",)))))  # line 759

    def testReorderRenameActions(_):  # line 761
        result = sos.reorderRenameActions([("123", "312"), ("312", "132"), ("321", "123")], exitOnConflict=False)  # type: _coconut.typing.Sequence[Tuple[str, str]]  # line 762
        _.assertEqual([("312", "132"), ("123", "312"), ("321", "123")], result)  # line 763
        try:  # line 764
            sos.reorderRenameActions([("123", "312"), ("312", "123")], exitOnConflict=True)  # line 764
            _.fail()  # line 764
        except:  # line 765
            pass  # line 765

    def testMove(_):  # line 767
        sos.offline(options=["--strict", "--track"])  # line 768
        _.createFile(1)  # line 769
        sos.add(".", "./file?")  # line 770
# test source folder missing
        try:  # line 772
            sos.move("sub", "sub/file?", ".", "?file")  # line 772
            _.fail()  # line 772
        except:  # line 773
            pass  # line 773
# test target folder missing: create it
        sos.move(".", "./file?", "sub", "sub/file?")  # line 775
        _.assertTrue(os.path.exists("sub"))  # line 776
        _.assertTrue(os.path.exists("sub/file1"))  # line 777
        _.assertFalse(os.path.exists("file1"))  # line 778
# test move
        sos.move("sub", "sub/file?", ".", "./?file")  # line 780
        _.assertTrue(os.path.exists("1file"))  # line 781
        _.assertFalse(os.path.exists("sub/file1"))  # line 782
# test nothing matches source pattern
        try:  # line 784
            sos.move(".", "a*", ".", "b*")  # line 784
            _.fail()  # line 784
        except:  # line 785
            pass  # line 785
        sos.add(".", "*")  # anything pattern  # line 786
        try:  # TODO check that alternative pattern "*" was suggested (1 hit)  # line 787
            sos.move(".", "a*", ".", "b*")  # TODO check that alternative pattern "*" was suggested (1 hit)  # line 787
            _.fail()  # TODO check that alternative pattern "*" was suggested (1 hit)  # line 787
        except:  # line 788
            pass  # line 788
# test rename no conflict
        _.createFile(1)  # line 790
        _.createFile(2)  # line 791
        sos.add(".", "./file*")  # line 792
        sos.move(".", "./file*", ".", "fi*le")  # line 793
        _.assertTrue(all((os.path.exists("fi%dle" % i) for i in range(1, 3))))  # line 794
# test rename solvable conflicts
        [_.createFile("%s-%s-%s" % tuple((c for c in n))) for n in ["312", "321", "123", "231"]]  # line 796
#    sos.move("?-?-?")
# test rename unsolvable conflicts
# test --soft option
        sos.remove(".", "./?file")  # was renamed before  # line 800
        sos.add(".", "./?a?b", ["--force"])  # line 801
        sos.move(".", "./?a?b", ".", "./a?b?", ["--force", "--soft"])  # line 802
        _.createFile("1a2b")  # should not be tracked  # line 803
        _.createFile("a1b2")  # should be tracked  # line 804
        sos.commit()  # line 805
        _.assertEqual(2, len(os.listdir(branchFolder(0, 1))))  # line 806
        _.assertTrue(os.path.exists(branchFolder(0, 1) + os.sep + "93b38f90892eb5c57779ca9c0b6fbdf6774daeee3342f56f3e78eb2fe5336c50"))  # a1b2  # line 807
        _.createFile("1a1b1")  # line 808
        _.createFile("1a1b2")  # line 809
        sos.add(".", "?a?b*")  # line 810
        _.assertIn("not unique", wrapChannels(lambda: sos.move(".", "?a?b*", ".", "z?z?")))  # should raise error due to same target name  # line 811
# TODO only rename if actually any files are versioned? or simply what is alife?
# TODO add test if two single question marks will be moved into adjacent characters

    def testFindBase(_):  # line 815
        old = os.getcwd()  # line 816
        try:  # line 817
            os.mkdir("." + os.sep + ".git")  # line 818
            os.makedirs("." + os.sep + "a" + os.sep + sos.metaFolder)  # line 819
            os.makedirs("." + os.sep + "a" + os.sep + "b")  # line 820
            os.chdir("a" + os.sep + "b")  # line 821
            s, vcs, cmd = sos.findSosVcsBase()  # line 822
            _.assertIsNotNone(s)  # line 823
            _.assertIsNotNone(vcs)  # line 824
            _.assertEqual("git", cmd)  # line 825
        finally:  # line 826
            os.chdir(old)  # line 826


if __name__ == '__main__':  # line 829
    logging.basicConfig(level=logging.DEBUG if '-v' in sys.argv or os.getenv("DEBUG", "false").strip().lower() == "true" or os.getenv("CI", "false").strip().lower() == "true" else logging.INFO, stream=sys.stderr, format="%(asctime)-23s %(levelname)-8s %(name)s:%(lineno)d | %(message)s" if '-v' in sys.argv or os.getenv("DEBUG", "false") == "true" else "%(message)s")  # line 830
    if configr:  # line 831
        c = configr.Configr("sos")  # line 832
        c.loadSettings()  # line 832
        if len(c.keys()) > 0:  # line 833
            sos.Exit("Cannot run test suite with existing local SOS user configuration (would affect results)")  # line 833
    unittest.main(testRunner=debugTestRunner() if '-v' in sys.argv and not os.getenv("CI", "false").lower() == "true" else None)  # warnings = "ignore")  # line 834
