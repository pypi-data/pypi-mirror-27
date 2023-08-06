#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# __coconut_hash__ = 0xb0017c10

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

import builtins  # line 5
import json  # line 5
import logging  # line 5
import os  # line 5
import shutil  # line 5
sys = _coconut_sys  # line 5
import time  # line 5
import traceback  # line 5
import unittest  # line 5
import uuid  # line 5
StringIO = (__import__("StringIO" if sys.version_info.major < 3 else "io")).StringIO  # enables import via ternary expression  # line 6
try:  # Py3  # line 7
    from unittest import mock  # Py3  # line 7
except:  # installed via pip  # line 8
    import mock  # installed via pip  # line 8
try:  # only required for mypy  # line 9
    from typing import Any  # only required for mypy  # line 9
    from typing import List  # only required for mypy  # line 9
    from typing import Union  # only required for mypy  # line 9
except:  # line 10
    pass  # line 10

testFolder = os.path.abspath(os.path.join(os.getcwd(), "test"))  # line 12
try:  # line 13
    import configr  # optional dependency  # line 14
    os.environ["TEST"] = testFolder  # needed to mock configr library calls in sos  # line 15
except:  # declare as undefined  # line 16
    configr = None  # declare as undefined  # line 16
import sos  # line 17
sos.defaults["defaultbranch"] = "trunk"  # because sos.main() is never called  # line 18

def sync() -> 'None':  # line 20
    if (sys.version_info.major, sys.version_info.minor) >= (3, 3):  # line 21
        os.sync()  # line 21


def determineFilesystemTimeResolution() -> 'float':  # line 24
    name = str(uuid.uuid4())  # line 25
    with open(name, "w") as fd:  # create temporary file  # line 26
        fd.write("x")  # create temporary file  # line 26
    mt = os.stat(name).st_mtime  # get current timestamp  # line 27
    while os.stat(name).st_mtime == mt:  # wait until timestamp modified  # line 28
        time.sleep(0.05)  # to avoid 0.00s bugs (came up some time for unknown reasons)  # line 29
        with open(name, "w") as fd:  # line 30
            fd.write("x")  # line 30
    mt, start, _count = os.stat(name).st_mtime, time.time(), 0  # line 31
    while os.stat(name).st_mtime == mt:  # now cound and measure time until modified again  # line 32
        time.sleep(0.05)  # line 33
        _count += 1  # line 34
        with open(name, "w") as fd:  # line 35
            fd.write("x")  # line 35
    os.unlink(name)  # line 36
    fsprecision = round(time.time() - start, 2)  # line 37
    print("File system timestamp precision is %.2fs; wrote to the file %d times during that time" % (fsprecision, _count))  # line 38
    return fsprecision  # line 39


FS_PRECISION = determineFilesystemTimeResolution() * 1.05  # line 42


@_coconut_tco  # line 45
def debugTestRunner(post_mortem=None):  # line 45
    ''' Unittest runner doing post mortem debugging on failing tests. '''  # line 46
    import pdb  # line 47
    if post_mortem is None:  # line 48
        post_mortem = pdb.post_mortem  # line 48
    class DebugTestResult(unittest.TextTestResult):  # line 49
        def addError(self, test, err):  # called before tearDown()  # line 50
            traceback.print_exception(*err)  # line 51
            post_mortem(err[2])  # line 52
            super(DebugTestResult, self).addError(test, err)  # line 53
        def addFailure(self, test, err):  # line 54
            traceback.print_exception(*err)  # line 55
            post_mortem(err[2])  # line 56
            super(DebugTestResult, self).addFailure(test, err)  # line 57
    return _coconut_tail_call(unittest.TextTestRunner, resultclass=DebugTestResult)  # line 58

def branchFolder(branch: 'int', revision: 'int') -> 'str':  # line 60
    return "." + os.sep + sos.metaFolder + os.sep + "b%d" % branch + os.sep + "r%d" % revision  # line 60

@_coconut_tco  # line 62
def wrapChannels(func: '_coconut.typing.Callable[..., Any]'):  # line 62
    ''' Wrap function call to capture and return strings emitted on stdout and stderr. '''  # line 63
    oldv, oldo, olde = sys.argv, sys.stdout, sys.stderr  # line 64
    buf = StringIO()  # line 65
    sys.stdout = sys.stderr = buf  # line 66
    handler = logging.StreamHandler(buf)  # line 67
    logging.getLogger().addHandler(handler)  # line 68
    try:  # capture output into buf  # line 69
        func()  # capture output into buf  # line 69
    except Exception as E:  # line 70
        buf.write(str(E) + "\n")  # line 70
        traceback.print_exc(file=buf)  # line 70
    except SystemExit as F:  # line 71
        buf.write(str(F) + "\n")  # line 71
        traceback.print_exc(file=buf)  # line 71
    logging.getLogger().removeHandler(handler)  # line 72
    sys.argv, sys.stdout, sys.stderr = oldv, oldo, olde  # line 73
    return _coconut_tail_call(buf.getvalue)  # line 74

def mockInput(datas: '_coconut.typing.Sequence[str]', func) -> 'Any':  # line 76
    with mock.patch("builtins.input" if sys.version_info.major >= 3 else "utility._coconut_raw_input", side_effect=datas):  # line 77
        return func()  # line 77

def setRepoFlag(name: 'str', value: 'bool') -> 'None':  # line 79
    with open(sos.metaFolder + os.sep + sos.metaFile, "r") as fd:  # line 80
        flags, branches = json.loads(fd.read())  # line 80
    flags[name] = value  # line 81
    with open(sos.metaFolder + os.sep + sos.metaFile, "w") as fd:  # line 82
        fd.write(json.dumps((flags, branches)))  # line 82

def checkRepoFlag(name: 'str', flag: 'bool') -> 'bool':  # line 84
    with open(sos.metaFolder + os.sep + sos.metaFile, "r") as fd:  # line 84
        flags, branches = json.loads(fd.read())  # line 85
    return name in flags and flags[name] == flag  # line 86


class Tests(unittest.TestCase):  # line 89
    ''' Entire test suite. '''  # line 90

    def setUp(_):  # line 92
        for entry in os.listdir(testFolder):  # cannot remove testFolder on Windows when using TortoiseSVN as VCS  # line 93
            resource = os.path.join(testFolder, entry)  # line 94
            shutil.rmtree(resource) if os.path.isdir(resource) else os.unlink(resource)  # line 95
        os.chdir(testFolder)  # line 96

    def assertAllIn(_, what: '_coconut.typing.Sequence[str]', where: 'Union[str, List[str]]') -> 'None':  # line 98
        [_.assertIn(w, where) for w in what]  # line 98

    def assertAllNotIn(_, what: '_coconut.typing.Sequence[str]', where: 'Union[str, List[str]]') -> 'None':  # line 100
        [_.assertNotIn(w, where) for w in what]  # line 100

    def assertInAll(_, what: 'str', where: '_coconut.typing.Sequence[str]') -> 'None':  # line 102
        [_.assertIn(what, w) for w in where]  # line 102

    def assertInAny(_, what: 'str', where: '_coconut.typing.Sequence[str]') -> 'None':  # line 104
        _.assertTrue(any((what in w for w in where)))  # line 104

    def assertNotInAny(_, what: 'str', where: '_coconut.typing.Sequence[str]') -> 'None':  # line 106
        _.assertFalse(any((what in w for w in where)))  # line 106

    def createFile(_, number: 'Union[int, str]', contents: 'str'="x" * 10, prefix: '_coconut.typing.Optional[str]'=None) -> 'None':  # line 108
        if prefix and not os.path.exists(prefix):  # line 109
            os.makedirs(prefix)  # line 109
        with open(("." if prefix is None else prefix) + os.sep + (("file%d" % number) if isinstance(number, int) else number), "wb") as fd:  # line 110
            fd.write(contents if isinstance(contents, bytes) else contents.encode("cp1252"))  # line 110

    def existsFile(_, number: 'Union[int, str]', expectedContents: 'bytes'=None) -> 'bool':  # line 112
        if not os.path.exists(("." + os.sep + "file%d" % number) if isinstance(number, int) else number):  # line 113
            return False  # line 113
        if expectedContents is None:  # line 114
            return True  # line 114
        with open(("." + os.sep + "file%d" % number) if isinstance(number, int) else number, "rb") as fd:  # line 115
            return fd.read() == expectedContents  # line 115

    def testAccessor(_):  # line 117
        a = sos.Accessor({"a": 1})  # line 118
        _.assertEqual((1, 1), (a["a"], a.a))  # line 119

    def testFirstofmap(_):  # line 121
        _.assertEqual(2, sos.firstOfMap({"a": 1, "b": 2}, ["x", "b"]))  # line 122
        _.assertIsNone(sos.firstOfMap({"a": 1, "b": 2}, []))  # line 123

    def testAjoin(_):  # line 125
        _.assertEqual("a1a2", sos.ajoin("a", ["1", "2"]))  # line 126
        _.assertEqual("* a\n* b", sos.ajoin("* ", ["a", "b"], "\n"))  # line 127

    def testFindChanges(_):  # line 129
        m = sos.Metadata(os.getcwd())  # line 130
        sos.config("set", ["texttype", "*"])  # line 131
        sos.config("set", ["ignores", "*.cfg;*.cfg.bak"])  # line 132
        m = sos.Metadata(os.getcwd())  # reload from file system  # line 133
        m.loadBranches()  # line 134
        _.createFile(1, "1")  # line 135
        m.createBranch(0)  # line 136
        _.assertEqual(1, len(m.paths))  # line 137
        time.sleep(FS_PRECISION)  # time required by filesystem time resolution issues  # line 138
        _.createFile(1, "2")  # modify existing file  # line 139
        _.createFile(2, "2")  # add another file  # line 140
        m.loadCommit(0, 0)  # line 141
        changes = m.findChanges()  # detect time skew  # line 142
        _.assertEqual(1, len(changes.additions))  # line 143
        _.assertEqual(0, len(changes.deletions))  # line 144
        _.assertEqual(1, len(changes.modifications))  # line 145
        m.integrateChangeset(changes)  # line 146
        _.createFile(2, "12")  # modify file again  # line 147
        changes = m.findChanges(0, 1)  # by size, creating new commit  # line 148
        _.assertEqual(0, len(changes.additions))  # line 149
        _.assertEqual(0, len(changes.deletions))  # line 150
        _.assertEqual(1, len(changes.modifications))  # line 151
        _.assertTrue(os.path.exists(branchFolder(0, 1)))  # line 152
        _.assertTrue(os.path.exists(branchFolder(0, 1) + os.sep + "03b69bc801ae11f1ff2a71a50f165996d0ad681b4f822df13329a27e53f0fcd2"))  # line 153

    def testDiffFunc(_):  # line 155
        a = {"./a": sos.PathInfo("", 0, 0, "")}  # line 156
        b = {"./a": sos.PathInfo("", 0, 0, "")}  # line 157
        changes = sos.diffPathSets(a, b)  # line 158
        _.assertEqual(0, len(changes.additions))  # line 159
        _.assertEqual(0, len(changes.deletions))  # line 160
        _.assertEqual(0, len(changes.modifications))  # line 161
        b = {"./a": sos.PathInfo("", 1, 0, "")}  # line 162
        changes = sos.diffPathSets(a, b)  # line 163
        _.assertEqual(0, len(changes.additions))  # line 164
        _.assertEqual(0, len(changes.deletions))  # line 165
        _.assertEqual(1, len(changes.modifications))  # line 166
        b = {}  # diff contains no entries -> no change  # line 167
        changes = sos.diffPathSets(a, b)  # line 168
        _.assertEqual(0, len(changes.additions))  # line 169
        _.assertEqual(0, len(changes.deletions))  # line 170
        _.assertEqual(0, len(changes.modifications))  # line 171
        b = {"./a": sos.PathInfo("", None, 1, "")}  # in diff marked as deleted  # line 172
        changes = sos.diffPathSets(a, b)  # line 173
        _.assertEqual(0, len(changes.additions))  # line 174
        _.assertEqual(1, len(changes.deletions))  # line 175
        _.assertEqual(0, len(changes.modifications))  # line 176
        b = {"./b": sos.PathInfo("", 1, 1, "")}  # line 177
        changes = sos.diffPathSets(a, b)  # line 178
        _.assertEqual(1, len(changes.additions))  # line 179
        _.assertEqual(0, len(changes.deletions))  # line 180
        _.assertEqual(0, len(changes.modifications))  # line 181
        a = {"./a": sos.PathInfo("", None, 0, "")}  # mark as deleted  # line 182
        b = {"./a": sos.PathInfo("", 1, 0, "")}  # re-added  # line 183
        changes = sos.diffPathSets(a, b)  # line 184
        _.assertEqual(1, len(changes.additions))  # line 185
        _.assertEqual(0, len(changes.deletions))  # line 186
        _.assertEqual(0, len(changes.modifications))  # line 187
        changes = sos.diffPathSets(b, a)  # line 188
        _.assertEqual(0, len(changes.additions))  # line 189
        _.assertEqual(1, len(changes.deletions))  # line 190
        _.assertEqual(0, len(changes.modifications))  # line 191

    def testPatternPaths(_):  # line 193
        sos.offline(options=["--track"])  # line 194
        os.mkdir("sub")  # line 195
        _.createFile("sub" + os.sep + "file1", "sdfsdf")  # line 196
        sos.add("sub", "sub/file?")  # line 197
        sos.commit("test")  # should pick up sub/file1 pattern  # line 198
        _.assertEqual(2, len(os.listdir(os.path.join(sos.metaFolder, "b0", "r1"))))  # sub/file1 was added  # line 199
        _.createFile(1)  # line 200
        try:  # should not commit anything, as the file in base folder doesn't match the tracked pattern  # line 201
            sos.commit("nothing")  # should not commit anything, as the file in base folder doesn't match the tracked pattern  # line 201
            _.fail()  # should not commit anything, as the file in base folder doesn't match the tracked pattern  # line 201
        except:  # line 202
            pass  # line 202

    def testTokenizeGlobPattern(_):  # line 204
        _.assertEqual([], sos.tokenizeGlobPattern(""))  # line 205
        _.assertEqual([sos.GlobBlock(False, "*", 0)], sos.tokenizeGlobPattern("*"))  # line 206
        _.assertEqual([sos.GlobBlock(False, "*", 0), sos.GlobBlock(False, "???", 1)], sos.tokenizeGlobPattern("*???"))  # line 207
        _.assertEqual([sos.GlobBlock(True, "x", 0), sos.GlobBlock(False, "*", 1), sos.GlobBlock(True, "x", 2)], sos.tokenizeGlobPattern("x*x"))  # line 208
        _.assertEqual([sos.GlobBlock(True, "x", 0), sos.GlobBlock(False, "*", 1), sos.GlobBlock(False, "??", 2), sos.GlobBlock(False, "*", 4), sos.GlobBlock(True, "x", 5)], sos.tokenizeGlobPattern("x*??*x"))  # line 209
        _.assertEqual([sos.GlobBlock(False, "?", 0), sos.GlobBlock(True, "abc", 1), sos.GlobBlock(False, "*", 4)], sos.tokenizeGlobPattern("?abc*"))  # line 210

    def testTokenizeGlobPatterns(_):  # line 212
        try:  # because number of literal strings differs  # line 213
            sos.tokenizeGlobPatterns("x*x", "x*")  # because number of literal strings differs  # line 213
            _.fail()  # because number of literal strings differs  # line 213
        except:  # line 214
            pass  # line 214
        try:  # because glob patterns differ  # line 215
            sos.tokenizeGlobPatterns("x*", "x?")  # because glob patterns differ  # line 215
            _.fail()  # because glob patterns differ  # line 215
        except:  # line 216
            pass  # line 216
        try:  # glob patterns differ, regardless of position  # line 217
            sos.tokenizeGlobPatterns("x*", "?x")  # glob patterns differ, regardless of position  # line 217
            _.fail()  # glob patterns differ, regardless of position  # line 217
        except:  # line 218
            pass  # line 218
        sos.tokenizeGlobPatterns("x*", "*x")  # succeeds, because glob patterns match (differ only in position)  # line 219
        sos.tokenizeGlobPatterns("*xb?c", "*x?bc")  # succeeds, because glob patterns match (differ only in position)  # line 220
        try:  # succeeds, because glob patterns match (differ only in position)  # line 221
            sos.tokenizeGlobPatterns("a???b*", "ab???*")  # succeeds, because glob patterns match (differ only in position)  # line 221
            _.fail()  # succeeds, because glob patterns match (differ only in position)  # line 221
        except:  # line 222
            pass  # line 222

    def testConvertGlobFiles(_):  # line 224
        _.assertEqual(["xxayb", "aacb"], [r[1] for r in sos.convertGlobFiles(["axxby", "aabc"], *sos.tokenizeGlobPatterns("a*b?", "*a?b"))])  # line 225
        _.assertEqual(["1qq2ww3", "1abcbx2xbabc3"], [r[1] for r in sos.convertGlobFiles(["qqxbww", "abcbxxbxbabc"], *sos.tokenizeGlobPatterns("*xb*", "1*2*3"))])  # line 226

    def testFolderRemove(_):  # line 228
        m = sos.Metadata(os.getcwd())  # line 229
        _.createFile(1)  # line 230
        _.createFile("a", prefix="sub")  # line 231
        sos.offline()  # line 232
        _.createFile(2)  # line 233
        os.unlink("sub" + os.sep + "a")  # line 234
        os.rmdir("sub")  # line 235
        changes = sos.changes()  # line 236
        _.assertEqual(1, len(changes.additions))  # line 237
        _.assertEqual(0, len(changes.modifications))  # line 238
        _.assertEqual(1, len(changes.deletions))  # line 239
        _.createFile("a", prefix="sub")  # line 240
        changes = sos.changes()  # line 241
        _.assertEqual(0, len(changes.deletions))  # line 242

    def testComputeSequentialPathSet(_):  # line 244
        os.makedirs(branchFolder(0, 0))  # line 245
        os.makedirs(branchFolder(0, 1))  # line 246
        os.makedirs(branchFolder(0, 2))  # line 247
        os.makedirs(branchFolder(0, 3))  # line 248
        os.makedirs(branchFolder(0, 4))  # line 249
        m = sos.Metadata(os.getcwd())  # line 250
        m.branch = 0  # line 251
        m.commit = 2  # line 252
        m.saveBranches()  # line 253
        m.paths = {"./a": sos.PathInfo("", 0, 0, "")}  # line 254
        m.saveCommit(0, 0)  # initial  # line 255
        m.paths["./a"] = sos.PathInfo("", 1, 0, "")  # line 256
        m.saveCommit(0, 1)  # mod  # line 257
        m.paths["./b"] = sos.PathInfo("", 0, 0, "")  # line 258
        m.saveCommit(0, 2)  # add  # line 259
        m.paths["./a"] = sos.PathInfo("", None, 0, "")  # line 260
        m.saveCommit(0, 3)  # del  # line 261
        m.paths["./a"] = sos.PathInfo("", None, 0, "")  # line 262
        m.saveCommit(0, 4)  # readd  # line 263
        m.commits = {i: sos.CommitInfo(i, 0, None) for i in range(5)}  # line 264
        m.saveBranch(0)  # line 265
        m.computeSequentialPathSet(0, 4)  # line 266
        _.assertEqual(2, len(m.paths))  # line 267

    def testParseRevisionString(_):  # line 269
        m = sos.Metadata(os.getcwd())  # line 270
        m.branch = 1  # line 271
        m.commits = {0: 0, 1: 1, 2: 2}  # line 272
        _.assertEqual((1, 3), m.parseRevisionString("3"))  # line 273
        _.assertEqual((2, 3), m.parseRevisionString("2/3"))  # line 274
        _.assertEqual((1, -1), m.parseRevisionString(None))  # line 275
        _.assertEqual((1, -1), m.parseRevisionString(""))  # line 276
        _.assertEqual((2, -1), m.parseRevisionString("2/"))  # line 277
        _.assertEqual((1, -2), m.parseRevisionString("/-2"))  # line 278
        _.assertEqual((1, -1), m.parseRevisionString("/"))  # line 279

    def testOfflineEmpty(_):  # line 281
        os.mkdir("." + os.sep + sos.metaFolder)  # line 282
        try:  # line 283
            sos.offline("trunk")  # line 283
            _.fail()  # line 283
        except SystemExit:  # line 284
            pass  # line 284
        os.rmdir("." + os.sep + sos.metaFolder)  # line 285
        sos.offline("test")  # line 286
        _.assertIn(sos.metaFolder, os.listdir("."))  # line 287
        _.assertAllIn(["b0", sos.metaFile], os.listdir("." + os.sep + sos.metaFolder))  # line 288
        _.assertAllIn(["r0", sos.metaFile], os.listdir("." + os.sep + sos.metaFolder + os.sep + "b0"))  # line 289
        _.assertEqual(2, len(os.listdir("." + os.sep + sos.metaFolder)))  # only branch folder and meta data file  # line 290
        _.assertEqual(2, len(os.listdir("." + os.sep + sos.metaFolder + os.sep + "b0")))  # only commit folder and meta data file  # line 291
        _.assertEqual(1, len(os.listdir(branchFolder(0, 0))))  # only meta data file  # line 292

    def testOfflineWithFiles(_):  # line 294
        _.createFile(1, "x" * 100)  # line 295
        _.createFile(2)  # line 296
        sos.offline("test")  # line 297
        _.assertAllIn(["file1", "file2", sos.metaFolder], os.listdir("."))  # line 298
        _.assertAllIn(["b0", sos.metaFile], os.listdir("." + os.sep + sos.metaFolder))  # line 299
        _.assertAllIn(["r0", sos.metaFile], os.listdir("." + os.sep + sos.metaFolder + os.sep + "b0"))  # line 300
        _.assertAllIn([sos.metaFile, "03b69bc801ae11f1ff2a71a50f165996d0ad681b4f822df13329a27e53f0fcd2", "b9ee10a87f612e299a6eb208210bc0898092a64c48091327cc2aaeee9b764ffa"], os.listdir("." + os.sep + sos.metaFolder + os.sep + "b0" + os.sep + "r0"))  # line 301
        _.assertEqual(2, len(os.listdir("." + os.sep + sos.metaFolder)))  # only branch folder and meta data file  # line 302
        _.assertEqual(2, len(os.listdir("." + os.sep + sos.metaFolder + os.sep + "b0")))  # only commit folder and meta data file  # line 303
        _.assertEqual(3, len(os.listdir(branchFolder(0, 0))))  # only meta data file plus branch base file copies  # line 304

    def testBranch(_):  # line 306
        _.createFile(1, "x" * 100)  # line 307
        _.createFile(2)  # line 308
        sos.offline("test")  # b0/r0  # line 309
        sos.branch("other")  # b1/r0  # line 310
        _.assertAllIn(["b0", "b1", sos.metaFile], os.listdir("." + os.sep + sos.metaFolder))  # line 311
        _.assertEqual(list(sorted(os.listdir("." + os.sep + sos.metaFolder + os.sep + "b0"))), list(sorted(os.listdir("." + os.sep + sos.metaFolder + os.sep + "b1"))))  # line 312
        _.assertEqual(list(sorted(os.listdir(branchFolder(0, 0)))), list(sorted(os.listdir(branchFolder(1, 0)))))  # line 314
        _.createFile(1, "z")  # modify file  # line 316
        sos.branch()  # b2/r0  branch to unnamed branch with modified file tree contents  # line 317
        _.assertNotEqual(os.stat("." + os.sep + sos.metaFolder + os.sep + "b1" + os.sep + "r0" + os.sep + "b9ee10a87f612e299a6eb208210bc0898092a64c48091327cc2aaeee9b764ffa").st_size, os.stat("." + os.sep + sos.metaFolder + os.sep + "b2" + os.sep + "r0" + os.sep + "b9ee10a87f612e299a6eb208210bc0898092a64c48091327cc2aaeee9b764ffa").st_size)  # line 318
        _.createFile(3, "z")  # line 320
        sos.branch("from_last_revision", ["--last", "--stay"])  # b3/r0 create copy of other file1,file2 and don't switch  # line 321
        _.assertEqual(list(sorted(os.listdir("." + os.sep + sos.metaFolder + os.sep + "b3" + os.sep + "r0"))), list(sorted(os.listdir("." + os.sep + sos.metaFolder + os.sep + "b2" + os.sep + "r0"))))  # line 322
# Check sos.status output which branch is marked


    def testComittingAndChanges(_):  # line 327
        _.createFile(1, "x" * 100)  # line 328
        _.createFile(2)  # line 329
        sos.offline("test")  # line 330
        changes = sos.changes()  # line 331
        _.assertEqual(0, len(changes.additions))  # line 332
        _.assertEqual(0, len(changes.deletions))  # line 333
        _.assertEqual(0, len(changes.modifications))  # line 334
        _.createFile(1, "z")  # size change  # line 335
        changes = sos.changes()  # line 336
        _.assertEqual(0, len(changes.additions))  # line 337
        _.assertEqual(0, len(changes.deletions))  # line 338
        _.assertEqual(1, len(changes.modifications))  # line 339
        sos.commit("message")  # line 340
        _.assertAllIn(["r0", "r1", sos.metaFile], os.listdir("." + os.sep + sos.metaFolder + os.sep + "b0"))  # line 341
        _.assertAllIn([sos.metaFile, "b9ee10a87f612e299a6eb208210bc0898092a64c48091327cc2aaeee9b764ffa"], os.listdir(branchFolder(0, 1)))  # line 342
        _.assertEqual(2, len(os.listdir(branchFolder(0, 1))))  # no further files, only the modified one  # line 343
        _.assertEqual(1, len(sos.changes("/0").modifications))  # vs. explicit revision on current branch  # line 344
        _.assertEqual(1, len(sos.changes("0/0").modifications))  # vs. explicit branch/revision  # line 345
        _.createFile(1, "")  # modify to empty file, mentioned in meta data, but not stored as own file  # line 346
        os.unlink("file2")  # line 347
        changes = sos.changes()  # line 348
        _.assertEqual(0, len(changes.additions))  # line 349
        _.assertEqual(1, len(changes.deletions))  # line 350
        _.assertEqual(1, len(changes.modifications))  # line 351
        sos.commit("modified")  # line 352
        _.assertEqual(1, len(os.listdir(branchFolder(0, 2))))  # no additional files, only mentions in metadata  # line 353
        try:  # expecting Exit due to no changes  # line 354
            sos.commit("nothing")  # expecting Exit due to no changes  # line 354
            _.fail()  # expecting Exit due to no changes  # line 354
        except:  # line 355
            pass  # line 355

    def testGetBranch(_):  # line 357
        m = sos.Metadata(os.getcwd())  # line 358
        m.branch = 1  # current branch  # line 359
        m.branches = {0: sos.BranchInfo(0, 0, "trunk")}  # line 360
        _.assertEqual(27, m.getBranchByName(27))  # line 361
        _.assertEqual(0, m.getBranchByName("trunk"))  # line 362
        _.assertEqual(1, m.getBranchByName(""))  # split from "/"  # line 363
        _.assertIsNone(m.getBranchByName("unknown"))  # line 364
        m.commits = {0: sos.CommitInfo(0, 0, "bla")}  # line 365
        _.assertEqual(13, m.getRevisionByName("13"))  # line 366
        _.assertEqual(0, m.getRevisionByName("bla"))  # line 367
        _.assertEqual(-1, m.getRevisionByName(""))  # split from "/"  # line 368

    def testTagging(_):  # line 370
        m = sos.Metadata(os.getcwd())  # line 371
        sos.offline()  # line 372
        _.createFile(111)  # line 373
        sos.commit("tag", ["--tag"])  # line 374
        _.createFile(2)  # line 375
        try:  # line 376
            sos.commit("tag")  # line 376
            _.fail()  # line 376
        except:  # line 377
            pass  # line 377
        sos.commit("tag-2", ["--tag"])  # line 378

    def testSwitch(_):  # line 380
        _.createFile(1, "x" * 100)  # line 381
        _.createFile(2, "y")  # line 382
        sos.offline("test")  # file1-2  in initial branch commit  # line 383
        sos.branch("second")  # file1-2  switch, having same files  # line 384
        sos.switch("0")  # no change  switch back, no problem  # line 385
        sos.switch("second")  # no change  # switch back, no problem  # line 386
        _.createFile(3, "y")  # generate a file  # line 387
        try:  # uncommited changes detected  # line 388
            sos.switch("test")  # uncommited changes detected  # line 388
            _.fail()  # uncommited changes detected  # line 388
        except SystemExit:  # line 389
            pass  # line 389
        sos.commit("Finish")  # file1-3  commit third file into branch second  # line 390
        sos.changes()  # line 391
        sos.switch("test")  # file1-2, remove file3 from file tree  # line 392
        _.assertFalse(_.existsFile(3))  # removed when switching back to test  # line 393
        out = wrapChannels(lambda: sos.status()).replace("\r", "")  # line 394
        _.assertIn("  * b00   'test'", out)  # line 395
        _.assertIn("    b01 'second'", out)  # line 396
        _.assertIn("(dirty)", out)  # one branch has commits  # line 397
        _.assertIn("(in sync)", out)  # the other doesn't  # line 398
        _.createFile(4, "xy")  # generate a file  # line 399
        sos.switch("second", "--force")  # avoids warning on uncommited changes, but keeps file4  # line 400
        _.assertFalse(_.existsFile(4))  # removed when forcedly switching back to test  # line 401
        _.assertTrue(_.existsFile(3))  # was restored from branch's revision r1  # line 402
        os.unlink("." + os.sep + "file1")  # remove old file1  # line 403
        sos.switch("test", "--force")  # should restore file1 and remove file3  # line 404
        _.assertTrue(_.existsFile(1))  # was restored from branch's revision r1  # line 405
        _.assertFalse(_.existsFile(3))  # was restored from branch's revision r1  # line 406

    def testAutoDetectVCS(_):  # line 408
        os.mkdir(".git")  # line 409
        sos.offline(sos.vcsBranches[sos.findSosVcsBase()[2]])  # create initial branch  # line 410
        with open(sos.metaFolder + os.sep + sos.metaFile, "r") as fd:  # line 411
            meta = fd.read()  # line 411
        _.assertTrue("\"master\"" in meta)  # line 412
        os.rmdir(".git")  # line 413

    def testUpdate(_):  # line 415
        sos.offline("trunk")  # create initial branch b0/r0  # line 416
        _.createFile(1, "x" * 100)  # line 417
        sos.commit("second")  # create b0/r1  # line 418

        sos.switch("/0")  # go back to b0/r0 - deletes file1  # line 420
        _.assertFalse(_.existsFile(1))  # line 421

        sos.update("/1")  # recreate file1  # line 423
        _.assertTrue(_.existsFile(1))  # line 424

        sos.commit("third", ["--force"])  # force because nothing to commit. should create r2 with same contents as r1, but as differential from r1, not from r0 (= no changes in meta folder)  # line 426
        _.assertTrue(os.path.exists(branchFolder(0, 2)))  # line 427
        _.assertTrue(os.path.exists(branchFolder(0, 2) + os.sep + sos.metaFile))  # line 428
        _.assertEqual(1, len(os.listdir(branchFolder(0, 2))))  # only meta data file, no differential files  # line 429

        sos.update("/1")  # do nothing, as nothing has changed  # line 431
        _.assertTrue(_.existsFile(1))  # line 432

        _.createFile(2, "y" * 100)  # line 434
#    out = wrapChannels(() -> sos.branch("other"))  # won't comply as there are changes
#    _.assertIn("--force", out)
        sos.branch("other", ["--force"])  # automatically including file 2 (as we are in simple mode)  # line 437
        _.assertTrue(_.existsFile(2))  # line 438
        sos.update("trunk", ["--add"])  # only add stuff  # line 439
        _.assertTrue(_.existsFile(2))  # line 440
        sos.update("trunk")  # nothing to do  # line 441
        _.assertFalse(_.existsFile(2))  # removes file not present in original branch  # line 442

        theirs = b"a\nb\nc\nd\ne\nf\ng\nh\nx\nx\nj\nk"  # line 444
        _.createFile(10, theirs)  # line 445
        mine = b"a\nc\nd\ne\ng\nf\nx\nh\ny\ny\nj"  # missing "b", inserted g, modified g->x, replace x/x -> y/y, removed k  # line 446
        _.createFile(11, mine)  # line 447
        _.assertEqual(b"a\nb\nc\nd\ne\nf\ng\nh\nx\nx\nj\nk", sos.merge(filename="." + os.sep + "file10", intoname="." + os.sep + "file11", mergeOperation=sos.MergeOperation.BOTH, conflictResolution=sos.ConflictResolution.THEIRS))  # completely recreated other file  # line 448
        _.assertEqual(b"a\nb\nc\nd\ne\ng\nf\ng\nx\nh\nx\nx\ny\ny\nj\nk", sos.merge(filename="." + os.sep + "file10", intoname="." + os.sep + "file11", mergeOperation=sos.MergeOperation.INSERT, conflictResolution=sos.ConflictResolution.MINE))  # line 449

    def testUpdate2(_):  # line 451
        _.createFile("test.txt", "x" * 10)  # line 452
        sos.offline("trunk", ["--strict"])  # use strict mode, as timestamp differences are too small for testing  # line 453
        sos.branch("mod")  # line 454
        _.createFile("test.txt", "x" * 5 + "y" * 5)  # line 455
        time.sleep(FS_PRECISION)  # line 456
        sos.commit("mod")  # create b0/r1  # line 457
        sos.switch("trunk", ["--force"])  # should replace contents, force in case some other files were modified (e.g. during working on the code) TODO investigate more  # line 458
        with open("test.txt", "rb") as fd:  # line 459
            _.assertEqual(b"x" * 10, fd.read())  # line 459
        sos.update("mod", ["--theirs"])  # integrate changes TODO same with ask -> theirs  # line 460
        with open("test.txt", "rb") as fd:  # line 461
            _.assertEqual(b"x" * 5 + b"y" * 5, fd.read())  # line 461
        _.createFile("test.txt", "x" * 10)  # line 462
        mockInput(["t"], lambda: sos.update("mod", ["--ask"]))  # same as above with interaction -> theirs  # line 463
        with open("test.txt", "rb") as fd:  # line 464
            _.assertEqual(b"x" * 5 + b"y" * 5, fd.read())  # line 464

    def testIsTextType(_):  # line 466
        m = sos.Metadata(".")  # line 467
        m.c.texttype = ["*.x", "*.md", "*.md.*"]  # line 468
        m.c.bintype = ["*.md.confluence"]  # line 469
        _.assertTrue(m.isTextType("ab.txt"))  # line 470
        _.assertTrue(m.isTextType("./ab.txt"))  # line 471
        _.assertTrue(m.isTextType("bc/ab.txt"))  # line 472
        _.assertFalse(m.isTextType("bc/ab."))  # line 473
        _.assertTrue(m.isTextType("23_3.x.x"))  # line 474
        _.assertTrue(m.isTextType("dfg/dfglkjdf7/test.md"))  # line 475
        _.assertTrue(m.isTextType("./test.md.pdf"))  # line 476
        _.assertFalse(m.isTextType("./test_a.md.confluence"))  # line 477

    def testEolDet(_):  # line 479
        ''' Check correct end-of-line detection. '''  # line 480
        _.assertEqual(b"\n", sos.eoldet(b"a\nb"))  # line 481
        _.assertEqual(b"\r\n", sos.eoldet(b"a\r\nb\r\n"))  # line 482
        _.assertEqual(b"\r", sos.eoldet(b"\ra\rb"))  # line 483
        _.assertAllIn(["Inconsistent", "with "], wrapChannels(lambda: _.assertEqual(b"\n", sos.eoldet(b"\r\na\r\nb\n"))))  # line 484
        _.assertAllIn(["Inconsistent", "without"], wrapChannels(lambda: _.assertEqual(b"\n", sos.eoldet(b"\ra\nnb\n"))))  # line 485
        _.assertIsNone(sos.eoldet(b""))  # line 486
        _.assertIsNone(sos.eoldet(b"sdf"))  # line 487

    def testMerge(_):  # line 489
        ''' Check merge results depending on conflict solution options. '''  # line 490
        a = b"a\nb\ncc\nd"  # line 491
        b = b"a\nb\nee\nd"  # line 492
        _.assertEqual(b"a\nb\ncc\nee\nd", sos.merge(a, b, mergeOperation=sos.MergeOperation.INSERT))  # means insert changes from a into b, but don't replace  # line 493
        _.assertEqual(b"a\nb\nd", sos.merge(a, b, mergeOperation=sos.MergeOperation.REMOVE))  # line 494
        _.assertEqual(b"a\nb\ncc\nd", sos.merge(a, b, mergeOperation=sos.MergeOperation.BOTH))  # line 495
# Now test intra-line merging without conflicts
        _.assertEqual(b"a\nbc d\ne", sos.merge(b"a\nbc d\ne", b"a\nbcd\ne", mergeOperation=sos.MergeOperation.INSERT))  # because it's a deletion ['  a', '- bc d', '?   -\n', '+ bcd', '  e']  # line 497
        _.assertEqual(b"a\nbcd\ne", sos.merge(b"a\nbc d\ne", b"a\nbcd\ne", mergeOperation=sos.MergeOperation.REMOVE))  # ['  a', '- bc d', '?   -\n', '+ bcd', '  e']  # line 498
        _.assertEqual(b"a\nbc d\ne", sos.merge(b"a\nbcd\ne", b"a\nbc d\ne", mergeOperation=sos.MergeOperation.INSERT))  # nothing to insert  # line 499
        _.assertEqual(b"a\nbcd\ne", sos.merge(b"a\nbcd\ne", b"a\nbc d\ne", mergeOperation=sos.MergeOperation.REMOVE))  # remove space  # line 500
# Test with change + insert (conflict)
        _.assertEqual(b"a\nb fdd d\ne", sos.merge(b"a\nb cd d\ne", b"a\nb fdd d\ne", conflictResolution=sos.ConflictResolution.MINE))  # line 502
        _.assertEqual(b"a\nb cd d\ne", sos.merge(b"a\nb cd d\ne", b"a\nb fdd d\ne", conflictResolution=sos.ConflictResolution.THEIRS))  # ['  a', '- b cd d', '?   ^\n', '+ b fdd d', '?   ^^\n', '  e']  # line 503
        _.assertEqual(b"a\nb fdd d\ne", mockInput(["i"], lambda: sos.merge(b"a\nb cd d\ne", b"a\nb fdd d\ne", conflictResolution=sos.ConflictResolution.ASK)))  # ['  a', '- b cd d', '?   ^\n', '+ b fdd d', '?   ^^\n', '  e']  # line 504
        _.assertEqual(b"a\nb cd d\ne", mockInput(["t"], lambda: sos.merge(b"a\nb cd d\ne", b"a\nb fdd d\ne", conflictResolution=sos.ConflictResolution.ASK)))  # ['  a', '- b cd d', '?   ^\n', '+ b fdd d', '?   ^^\n', '  e']  # line 505
        _.assertEqual(b"abbc", sos.merge(b"abbc", b"addc", mergeOperation=sos.MergeOperation.BOTH, conflictResolution=sos.ConflictResolution.THEIRS))  # line 506
        _.assertEqual(b"a\nbb\nc", sos.merge(b"a\nbb\nc", b"a\ndd\nc", mergeOperation=sos.MergeOperation.BOTH, conflictResolution=sos.ConflictResolution.THEIRS))  # line 507
        _.assertIn("Differing EOL-styles", wrapChannels(lambda: sos.merge(b"a\nb", b"a\r\nb")))  # expect warning  # line 508
        _.assertIn(b"a\r\nb", sos.merge(b"a\nb", b"a\r\nb"))  # in doubt, use "mine" CR-LF  # line 509

    def testPickyMode(_):  # line 511
        ''' Confirm that picky mode reset tracked patterns after commits. '''  # line 512
        sos.offline("trunk", ["--picky"])  # line 513
        changes = sos.changes()  # line 514
        _.assertEqual(0, len(changes.additions))  # do not list any existing file as an addition  # line 515
        sos.add(".", "./file?", ["--force"])  # line 516
        _.createFile(1, "aa")  # line 517
        sos.commit("First")  # add one file  # line 518
        _.assertEqual(2, len(os.listdir(branchFolder(0, 1))))  # line 519
        _.createFile(2, "b")  # line 520
        try:  # add nothing, because picky  # line 521
            sos.commit("Second")  # add nothing, because picky  # line 521
        except:  # line 522
            pass  # line 522
        sos.add(".", "./file?")  # line 523
        sos.commit("Third")  # line 524
        _.assertEqual(2, len(os.listdir(branchFolder(0, 2))))  # line 525
        out = wrapChannels(lambda: sos.log([])).replace("\r", "")  # line 526
        _.assertIn("  * r2", out)  # line 527
        _.createFile(3, prefix="sub")  # line 528
        sos.add("sub", "sub/file?")  # line 529
        changes = sos.changes()  # line 530
        _.assertEqual(1, len(changes.additions))  # line 531
        _.assertTrue("sub/file3" in changes.additions)  # line 532

    def testTrackedSubfolder(_):  # line 534
        ''' See if patterns for files in sub folders are picked up correctly. '''  # line 535
        os.mkdir("." + os.sep + "sub")  # line 536
        sos.offline("trunk", ["--track"])  # line 537
        _.createFile(1, "x")  # line 538
        _.createFile(1, "x", prefix="sub")  # line 539
        sos.add(".", "./file?")  # add glob pattern to track  # line 540
        sos.commit("First")  # line 541
        _.assertEqual(2, len(os.listdir(branchFolder(0, 1))))  # one new file + meta file  # line 542
        sos.add(".", "sub/file?")  # add glob pattern to track  # line 543
        sos.commit("Second")  # one new file + meta  # line 544
        _.assertEqual(2, len(os.listdir(branchFolder(0, 1))))  # one new file + meta file  # line 545
        os.unlink("file1")  # remove from basefolder  # line 546
        _.createFile(2, "y")  # line 547
        sos.remove(".", "sub/file?")  # line 548
        try:  # raises Exit. TODO test the "suggest a pattern" case  # line 549
            sos.remove(".", "sub/bla")  # raises Exit. TODO test the "suggest a pattern" case  # line 549
            _.fail()  # raises Exit. TODO test the "suggest a pattern" case  # line 549
        except:  # line 550
            pass  # line 550
        sos.commit("Third")  # line 551
        _.assertEqual(2, len(os.listdir(branchFolder(0, 2))))  # one new file + meta  # line 552
# TODO also check if /file1 and sub/file1 were removed from index

    def testTrackedMode(_):  # line 555
        ''' Difference in semantics vs simple mode:
          - For remote/other branch we can only know and consider tracked files, thus ignoring all complexity stemming from handling addition of untracked files.
          - For current branch, we can take into account tracked and untracked ones, in theory, but it doesn't make sense.
        In conclusion, using the union of tracking patterns from both sides to find affected files makes sense, but disallow deleting files not present in remote branch.
    '''  # line 560
        sos.offline("test", options=["--track"])  # set up repo in tracking mode (SVN- or gitless-style)  # line 561
        _.createFile(1)  # line 562
        _.createFile("a123a")  # untracked file "a123a"  # line 563
        sos.add(".", "./file?")  # add glob tracking pattern  # line 564
        sos.commit("second")  # versions "file1"  # line 565
        _.assertEqual(2, len(os.listdir(branchFolder(0, 1))))  # one new file + meta file  # line 566
        out = wrapChannels(lambda: sos.status()).replace("\r", "")  # line 567
        _.assertIn("  | ./file?", out)  # line 568

        _.createFile(2)  # untracked file "file2"  # line 570
        sos.commit("third")  # versions "file2"  # line 571
        _.assertEqual(2, len(os.listdir(branchFolder(0, 2))))  # one new file + meta file  # line 572

        os.mkdir("." + os.sep + "sub")  # line 574
        _.createFile(3, prefix="sub")  # untracked file "sub/file3"  # line 575
        sos.commit("fourth", ["--force"])  # no tracking pattern matches the subfolder  # line 576
        _.assertEqual(1, len(os.listdir(branchFolder(0, 3))))  # meta file only, no other tracked path/file  # line 577

        sos.branch("Other")  # second branch containing file1 and file2 tracked by "./file?"  # line 579
        sos.remove(".", "./file?")  # remove tracking pattern, but don't touch previously created and versioned files  # line 580
        sos.add(".", "./a*a")  # add tracking pattern  # line 581
        changes = sos.changes()  # should pick up addition only, because tracked, but not the deletion, as not tracked anymore  # line 582
        _.assertEqual(0, len(changes.modifications))  # line 583
        _.assertEqual(0, len(changes.deletions))  # not tracked anymore, but contained in version history and not removed  # line 584
        _.assertEqual(1, len(changes.additions))  # detected one addition "a123a", but won't recognize untracking files as deletion  # line 585

        sos.commit("Second_2")  # line 587
        _.assertEqual(2, len(os.listdir(branchFolder(1, 1))))  # "a123a" + meta file  # line 588
        _.assertTrue(os.path.exists("." + os.sep + "file1"))  # line 589
        _.assertTrue(os.path.exists("." + os.sep + "file2"))  # line 590

        sos.switch("test")  # go back to first branch - tracks only "file?", but not "a*a"  # line 592
        _.assertTrue(os.path.exists("." + os.sep + "file1"))  # line 593
        _.assertTrue(os.path.exists("." + os.sep + "a123a"))  # should not have been touched so far  # line 594

        sos.update("Other")  # integrate tracked files and tracking pattern from second branch into working state of master branch  # line 596
        _.assertTrue(os.path.exists("." + os.sep + "file1"))  # line 597
        _.assertTrue(os.path.exists("." + os.sep + "a123a"))  # line 598

        _.createFile("axxxa")  # new file that should be tracked on "test" now that we integrated "Other"  # line 600
        sos.commit("fifth")  # create new revision after integrating updates from second branch  # line 601
        _.assertEqual(3, len(os.listdir(branchFolder(0, 4))))  # one new file from other branch + one new in current folder + meta file  # line 602
        sos.switch("Other")  # switch back to just integrated branch that tracks only "a*a" - shouldn't do anything  # line 603
        _.assertTrue(os.path.exists("." + os.sep + "file1"))  # line 604
        _.assertTrue(os.path.exists("." + os.sep + "a123a"))  # line 605
        _.assertFalse(os.path.exists("." + os.sep + "axxxa"))  # because tracked in both branches, but not present in other -> delete in file tree  # line 606
# TODO test switch --meta

    def testLsTracked(_):  # line 609
        sos.offline("test", options=["--track"])  # set up repo in tracking mode (SVN- or gitless-style)  # line 610
        _.createFile(1)  # line 611
        _.createFile("foo")  # line 612
        sos.add(".", "./file*")  # capture one file  # line 613
        sos.ls()  # line 614
        out = sos.safeSplit(wrapChannels(lambda: sos.ls()).replace("\r", ""), "\n")  # line 615
        _.assertInAny("TRK file1  (file*)", out)  # line 616
        _.assertNotInAny("... file1  (file*)", out)  # line 617
        _.assertInAny("... foo", out)  # line 618
        out = sos.safeSplit(wrapChannels(lambda: sos.ls(options=["--patterns"])).replace("\r", ""), "\n")  # line 619
        _.assertInAny("TRK file*", out)  # line 620
        _.createFile("a", prefix="sub")  # line 621
        sos.add("sub", "sub/a")  # line 622
        sos.ls("sub")  # line 623
        _.assertIn("TRK a  (a)", sos.safeSplit(wrapChannels(lambda: sos.ls("sub")).replace("\r", ""), "\n"))  # line 624

    def testCompression(_):  # line 626
        _.createFile(1)  # line 627
        sos.offline("master", options=["--force"])  # line 628
        _.assertTrue(_.existsFile(branchFolder(0, 0) + os.sep + "b9ee10a87f612e299a6eb208210bc0898092a64c48091327cc2aaeee9b764ffa", b"x" * 10))  # line 629
        setRepoFlag("compress", True)  # was plain = uncompressed before  # line 630
        _.createFile(2)  # line 631
        sos.commit("Added file2")  # line 632
        _.assertTrue(_.existsFile(branchFolder(0, 1) + os.sep + "03b69bc801ae11f1ff2a71a50f165996d0ad681b4f822df13329a27e53f0fcd2"))  # exists  # line 633
        _.assertFalse(_.existsFile(branchFolder(0, 1) + os.sep + "03b69bc801ae11f1ff2a71a50f165996d0ad681b4f822df13329a27e53f0fcd2", b"x" * 10))  # but is compressed instead  # line 634

    def testConfigVariations(_):  # line 636
        def makeRepo():  # line 637
            try:  # line 638
                os.unlink("file1")  # line 638
            except:  # line 639
                pass  # line 639
            sos.offline("master", options=["--plain", "--force"])  # line 640
            _.createFile(1)  # line 641
            sos.commit("Added file1")  # line 642
        sos.config("set", ["strict", "on"])  # line 643
        makeRepo()  # line 644
        _.assertTrue(checkRepoFlag("strict", True))  # line 645
        sos.config("set", ["strict", "off"])  # line 646
        makeRepo()  # line 647
        _.assertTrue(checkRepoFlag("strict", False))  # line 648
        sos.config("set", ["strict", "yes"])  # line 649
        makeRepo()  # line 650
        _.assertTrue(checkRepoFlag("strict", True))  # line 651
        sos.config("set", ["strict", "no"])  # line 652
        makeRepo()  # line 653
        _.assertTrue(checkRepoFlag("strict", False))  # line 654
        sos.config("set", ["strict", "1"])  # line 655
        makeRepo()  # line 656
        _.assertTrue(checkRepoFlag("strict", True))  # line 657
        sos.config("set", ["strict", "0"])  # line 658
        makeRepo()  # line 659
        _.assertTrue(checkRepoFlag("strict", False))  # line 660
        sos.config("set", ["strict", "true"])  # line 661
        makeRepo()  # line 662
        _.assertTrue(checkRepoFlag("strict", True))  # line 663
        sos.config("set", ["strict", "false"])  # line 664
        makeRepo()  # line 665
        _.assertTrue(checkRepoFlag("strict", False))  # line 666
        sos.config("set", ["strict", "enable"])  # line 667
        makeRepo()  # line 668
        _.assertTrue(checkRepoFlag("strict", True))  # line 669
        sos.config("set", ["strict", "disable"])  # line 670
        makeRepo()  # line 671
        _.assertTrue(checkRepoFlag("strict", False))  # line 672
        sos.config("set", ["strict", "enabled"])  # line 673
        makeRepo()  # line 674
        _.assertTrue(checkRepoFlag("strict", True))  # line 675
        sos.config("set", ["strict", "disabled"])  # line 676
        makeRepo()  # line 677
        _.assertTrue(checkRepoFlag("strict", False))  # line 678
        try:  # line 679
            sos.config("set", ["strict", "nope"])  # line 679
            _.fail()  # line 679
        except:  # line 680
            pass  # line 680

    def testLsSimple(_):  # line 682
        _.createFile(1)  # line 683
        _.createFile("foo")  # line 684
        _.createFile("ign1")  # line 685
        _.createFile("ign2")  # line 686
        sos.offline("test")  # set up repo in tracking mode (SVN- or gitless-style)  # line 687
        sos.config("set", ["ignores", "ign1"])  # define an ignore pattern  # line 688
        sos.config("add", ["ignores", "ign2"])  # additional ignore pattern  # line 689
        sos.config("set", ["ignoresWhitelist", "ign1;ign2"])  # define a list of ignore patterns  # line 690
        out = wrapChannels(lambda: sos.config("show")).replace("\r", "")  # line 691
        _.assertIn("             ignores: ['ign1', 'ign2']", out)  # line 692
        out = sos.safeSplit(wrapChannels(lambda: sos.ls()).replace("\r", ""), "\n")  # line 693
        _.assertInAny('... file1', out)  # line 694
        _.assertInAny('... ign1', out)  # line 695
        _.assertInAny('... ign2', out)  # line 696
        try:  # line 697
            sos.config("rm", ["foo", "bar"])  # line 697
            _.fail()  # line 697
        except:  # line 698
            pass  # line 698
        try:  # line 699
            sos.config("rm", ["ignores", "foo"])  # line 699
            _.fail()  # line 699
        except:  # line 700
            pass  # line 700
        sos.config("rm", ["ignores", "ign1"])  # line 701
        sos.config("unset", ["ignoresWhitelist"])  # remove ignore pattern  # line 702
        out = sos.safeSplit(wrapChannels(lambda: sos.ls()).replace("\r", ""), "\n")  # line 703
        _.assertInAny('... ign1', out)  # line 704
        _.assertInAny('IGN ign2', out)  # line 705
        _.assertNotInAny('... ign2', out)  # line 706

    def testWhitelist(_):  # line 708
# TODO test same for simple mode
        _.createFile(1)  # line 710
        sos.defaults.ignores[:] = ["file*"]  # replace in-place  # line 711
        sos.offline("xx", ["--track", "--strict"])  # because nothing to commit due to ignore pattern  # line 712
        sos.add(".", "./file*")  # add tracking pattern for "file1"  # line 713
        sos.commit(options=["--force"])  # attempt to commit the file  # line 714
        _.assertEqual(1, len(os.listdir(branchFolder(0, 1))))  # only meta data, file1 was ignored  # line 715
        try:  # Exit because dirty  # line 716
            sos.online()  # Exit because dirty  # line 716
            _.fail()  # Exit because dirty  # line 716
        except:  # exception expected  # line 717
            pass  # exception expected  # line 717
        _.createFile("x2")  # add another change  # line 718
        sos.add(".", "./x?")  # add tracking pattern for "file1"  # line 719
        try:  # force beyond dirty flag check  # line 720
            sos.online(["--force"])  # force beyond dirty flag check  # line 720
            _.fail()  # force beyond dirty flag check  # line 720
        except:  # line 721
            pass  # line 721
        sos.online(["--force", "--force"])  # force beyond file tree modifications check  # line 722
        _.assertFalse(os.path.exists(sos.metaFolder))  # line 723

        _.createFile(1)  # line 725
        sos.defaults.ignoresWhitelist[:] = ["file*"]  # line 726
        sos.offline("xx", ["--track"])  # line 727
        sos.add(".", "./file*")  # line 728
        sos.commit()  # should NOT ask for force here  # line 729
        _.assertEqual(2, len(os.listdir(branchFolder(0, 1))))  # meta data and "file1", file1 was whitelisted  # line 730

    def testRemove(_):  # line 732
        _.createFile(1, "x" * 100)  # line 733
        sos.offline("trunk")  # line 734
        try:  # line 735
            sos.delete("trunk")  # line 735
            _fail()  # line 735
        except:  # line 736
            pass  # line 736
        _.createFile(2, "y" * 10)  # line 737
        sos.branch("added")  # line 738
        sos.delete("trunk")  # line 739
        _.assertEqual(2, len(os.listdir("." + os.sep + sos.metaFolder)))  # meta data file and "b1"  # line 740
        _.assertTrue(os.path.exists("." + os.sep + sos.metaFolder + os.sep + "b1"))  # line 741
        _.assertFalse(os.path.exists("." + os.sep + sos.metaFolder + os.sep + "b0"))  # line 742
        sos.branch("next")  # line 743
        _.createFile(3, "y" * 10)  # make a change  # line 744
        sos.delete("added", "--force")  # should succeed  # line 745

    def testUsage(_):  # line 747
        try:  # TODO expect sys.exit(0)  # line 748
            sos.usage()  # TODO expect sys.exit(0)  # line 748
            _.fail()  # TODO expect sys.exit(0)  # line 748
        except:  # line 749
            pass  # line 749
        try:  # line 750
            sos.usage(short=True)  # line 750
            _.fail()  # line 750
        except:  # line 751
            pass  # line 751

    def testOnly(_):  # line 753
        _.assertEqual((_coconut.frozenset(("./A", "x/B")), _coconut.frozenset(("./C",))), sos.parseOnlyOptions(".", ["abc", "def", "--only", "A", "--x", "--only", "x/B", "--except", "C", "--only"]))  # line 754
        _.assertEqual(_coconut.frozenset(("B",)), sos.conditionalIntersection(_coconut.frozenset(("A", "B", "C")), _coconut.frozenset(("B", "D"))))  # line 755
        _.assertEqual(_coconut.frozenset(("B", "D")), sos.conditionalIntersection(_coconut.frozenset(), _coconut.frozenset(("B", "D"))))  # line 756
        _.assertEqual(_coconut.frozenset(("B", "D")), sos.conditionalIntersection(None, _coconut.frozenset(("B", "D"))))  # line 757
        sos.offline(os.getcwd(), ["--track", "--strict"])  # line 758
        _.createFile(1)  # line 759
        _.createFile(2)  # line 760
        sos.add(".", "./file1")  # line 761
        sos.add(".", "./file2")  # line 762
        sos.commit(onlys=_coconut.frozenset(("./file1",)))  # line 763
        _.assertEqual(2, len(os.listdir(branchFolder(0, 1))))  # only meta and file1  # line 764
        sos.commit()  # adds also file2  # line 765
        _.assertEqual(2, len(os.listdir(branchFolder(0, 2))))  # only meta and file1  # line 766
        _.createFile(1, "cc")  # modify both files  # line 767
        _.createFile(2, "dd")  # line 768
        sos.config("set", ["texttype", "file2"])  # line 769
        changes = sos.changes(excps=["./file1"])  # line 770
        _.assertEqual(1, len(changes.modifications))  # only file2  # line 771
        _.assertTrue("./file2" in changes.modifications)  # line 772
        _.assertIn("DIF ./file2", wrapChannels(lambda: sos.diff(onlys=_coconut.frozenset(("./file2",)))))  # line 773
        _.assertAllNotIn(["MOD ./file1", "DIF ./file1", "MOD ./file2"], wrapChannels(lambda: sos.diff(onlys=_coconut.frozenset(("./file2",)))))  # line 774

    def testDiff(_):  # line 776
        sos.config("set", ["texttype", "file1"])  # line 777
        sos.offline(options=["--strict"])  # line 778
        _.createFile(1)  # line 779
        _.createFile(2)  # line 780
        sos.commit()  # line 781
        _.createFile(1, "sdfsdgfsdf")  # line 782
        _.createFile(2, "12343")  # line 783
        sos.commit()  # line 784
        _.createFile(1, "foobar")  # line 785
        _.assertAllIn(["MOD ./file2", "DIF ./file1", "- | 0000 |xxxxxxxxxx|", "+ | 0000 |foobar|"], wrapChannels(lambda: sos.diff("/-2")))  # vs. second last  # line 786
        _.assertAllNotIn(["MOD ./file1", "DIF ./file1"], wrapChannels(lambda: sos.diff("/-2", onlys=_coconut.frozenset(("./file2",)))))  # line 787

    def testReorderRenameActions(_):  # line 789
        result = sos.reorderRenameActions([("123", "312"), ("312", "132"), ("321", "123")], exitOnConflict=False)  # type: _coconut.typing.Sequence[Tuple[str, str]]  # line 790
        _.assertEqual([("312", "132"), ("123", "312"), ("321", "123")], result)  # line 791
        try:  # line 792
            sos.reorderRenameActions([("123", "312"), ("312", "123")], exitOnConflict=True)  # line 792
            _.fail()  # line 792
        except:  # line 793
            pass  # line 793

    def testMove(_):  # line 795
        sos.offline(options=["--strict", "--track"])  # line 796
        _.createFile(1)  # line 797
        sos.add(".", "./file?")  # line 798
# test source folder missing
        try:  # line 800
            sos.move("sub", "sub/file?", ".", "?file")  # line 800
            _.fail()  # line 800
        except:  # line 801
            pass  # line 801
# test target folder missing: create it
        sos.move(".", "./file?", "sub", "sub/file?")  # line 803
        _.assertTrue(os.path.exists("sub"))  # line 804
        _.assertTrue(os.path.exists("sub/file1"))  # line 805
        _.assertFalse(os.path.exists("file1"))  # line 806
# test move
        sos.move("sub", "sub/file?", ".", "./?file")  # line 808
        _.assertTrue(os.path.exists("1file"))  # line 809
        _.assertFalse(os.path.exists("sub/file1"))  # line 810
# test nothing matches source pattern
        try:  # line 812
            sos.move(".", "a*", ".", "b*")  # line 812
            _.fail()  # line 812
        except:  # line 813
            pass  # line 813
        sos.add(".", "*")  # anything pattern  # line 814
        try:  # TODO check that alternative pattern "*" was suggested (1 hit)  # line 815
            sos.move(".", "a*", ".", "b*")  # TODO check that alternative pattern "*" was suggested (1 hit)  # line 815
            _.fail()  # TODO check that alternative pattern "*" was suggested (1 hit)  # line 815
        except:  # line 816
            pass  # line 816
# test rename no conflict
        _.createFile(1)  # line 818
        _.createFile(2)  # line 819
        _.createFile(3)  # line 820
        sos.add(".", "./file*")  # line 821
        sos.config("set", ["ignores", "file3;file4"])  # define an ignore pattern  # line 822
        sos.config("set", ["ignoresWhitelist", "file3"])  # line 823
        sos.move(".", "./file*", ".", "fi*le")  # line 824
        _.assertTrue(all((os.path.exists("fi%dle" % i) for i in range(1, 4))))  # line 825
        _.assertFalse(os.path.exists("fi4le"))  # line 826
# test rename solvable conflicts
        [_.createFile("%s-%s-%s" % tuple((c for c in n))) for n in ["312", "321", "123", "231"]]  # line 828
#    sos.move("?-?-?")
# test rename unsolvable conflicts
# test --soft option
        sos.remove(".", "./?file")  # was renamed before  # line 832
        sos.add(".", "./?a?b", ["--force"])  # line 833
        sos.move(".", "./?a?b", ".", "./a?b?", ["--force", "--soft"])  # line 834
        _.createFile("1a2b")  # should not be tracked  # line 835
        _.createFile("a1b2")  # should be tracked  # line 836
        sos.commit()  # line 837
        _.assertEqual(2, len(os.listdir(branchFolder(0, 1))))  # line 838
        _.assertTrue(os.path.exists(branchFolder(0, 1) + os.sep + "93b38f90892eb5c57779ca9c0b6fbdf6774daeee3342f56f3e78eb2fe5336c50"))  # a1b2  # line 839
        _.createFile("1a1b1")  # line 840
        _.createFile("1a1b2")  # line 841
        sos.add(".", "?a?b*")  # line 842
        _.assertIn("not unique", wrapChannels(lambda: sos.move(".", "?a?b*", ".", "z?z?")))  # should raise error due to same target name  # line 843
# TODO only rename if actually any files are versioned? or simply what is alife?
# TODO add test if two single question marks will be moved into adjacent characters

    def testFindBase(_):  # line 847
        old = os.getcwd()  # line 848
        try:  # line 849
            os.mkdir("." + os.sep + ".git")  # line 850
            os.makedirs("." + os.sep + "a" + os.sep + sos.metaFolder)  # line 851
            os.makedirs("." + os.sep + "a" + os.sep + "b")  # line 852
            os.chdir("a" + os.sep + "b")  # line 853
            s, vcs, cmd = sos.findSosVcsBase()  # line 854
            _.assertIsNotNone(s)  # line 855
            _.assertIsNotNone(vcs)  # line 856
            _.assertEqual("git", cmd)  # line 857
        finally:  # line 858
            os.chdir(old)  # line 858

# TODO test command line operation --sos vs. --vcs
# check exact output instead of expected fail


if __name__ == '__main__':  # line 864
    logging.basicConfig(level=logging.DEBUG if '-v' in sys.argv or os.getenv("DEBUG", "false").strip().lower() == "true" or os.getenv("CI", "false").strip().lower() == "true" else logging.INFO, stream=sys.stderr, format="%(asctime)-23s %(levelname)-8s %(name)s:%(lineno)d | %(message)s" if '-v' in sys.argv or os.getenv("DEBUG", "false") == "true" else "%(message)s")  # line 865
    if configr:  # line 866
        c = configr.Configr("sos")  # line 867
        c.loadSettings()  # line 867
        if len(c.keys()) > 0:  # line 868
            sos.Exit("Cannot run test suite with existing local SOS user configuration (would affect results)")  # line 868
    unittest.main(testRunner=debugTestRunner() if '-v' in sys.argv and not os.getenv("CI", "false").lower() == "true" else None)  # warnings = "ignore")  # line 869
