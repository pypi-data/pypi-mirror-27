#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# __coconut_hash__ = 0xf21ec13a

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
    logging.getLogger().removeHandler(handler)  # line 65
    sys.argv, sys.stdout, sys.stderr = oldv, oldo, olde  # line 66
    return _coconut_tail_call(buf.getvalue)  # line 67

def mockInput(datas: '_coconut.typing.Sequence[str]', func) -> 'Any':  # line 69
    with mock.patch("builtins.input" if sys.version_info.major >= 3 else "utility._coconut_raw_input", side_effect=datas):  # line 70
        return func()  # line 70

def setRepoFlag(name: 'str', value: 'bool') -> 'None':  # line 72
    with open(sos.metaFolder + os.sep + sos.metaFile, "r") as fd:  # line 73
        flags, branches = json.loads(fd.read())  # line 73
    flags[name] = value  # line 74
    with open(sos.metaFolder + os.sep + sos.metaFile, "w") as fd:  # line 75
        fd.write(json.dumps((flags, branches)))  # line 75

def checkRepoFlag(name: 'str', flag: 'bool') -> 'bool':  # line 77
    with open(sos.metaFolder + os.sep + sos.metaFile, "r") as fd:  # line 77
        flags, branches = json.loads(fd.read())  # line 78
    return name in flags and flags[name] == flag  # line 79


class Tests(unittest.TestCase):  # line 82
    ''' Entire test suite. '''  # line 83

    def setUp(_):  # line 85
        for entry in os.listdir(testFolder):  # cannot remove testFolder on Windows when using TortoiseSVN as VCS  # line 86
            resource = os.path.join(testFolder, entry)  # line 87
            shutil.rmtree(resource) if os.path.isdir(resource) else os.unlink(resource)  # line 88
        os.chdir(testFolder)  # line 89

    def assertAllIn(_, what: '_coconut.typing.Sequence[str]', where: 'Union[str, List[str]]') -> 'None':  # line 91
        [_.assertIn(w, where) for w in what]  # line 91

    def assertInAll(_, what: 'str', where: '_coconut.typing.Sequence[str]') -> 'None':  # line 93
        [_.assertIn(what, w) for w in where]  # line 93

    def assertInAny(_, what: 'str', where: '_coconut.typing.Sequence[str]') -> 'None':  # line 95
        _.assertTrue(any((what in w for w in where)))  # line 95

    def assertNotInAny(_, what: 'str', where: '_coconut.typing.Sequence[str]') -> 'None':  # line 97
        _.assertFalse(any((what in w for w in where)))  # line 97

    def createFile(_, number: 'Union[int, str]', contents: 'str'="x" * 10, prefix: '_coconut.typing.Optional[str]'=None) -> 'None':  # line 99
        with open(("." if prefix is None else prefix) + os.sep + (("file%d" % number) if isinstance(number, int) else number), "wb") as fd:  # line 100
            fd.write(contents if isinstance(contents, bytes) else contents.encode("cp1252"))  # line 100

    def existsFile(_, number: 'Union[int, str]', expectedContents: 'bytes'=None) -> 'bool':  # line 102
        if not os.path.exists(("." + os.sep + "file%d" % number) if isinstance(number, int) else number):  # line 103
            return False  # line 103
        if expectedContents is None:  # line 104
            return True  # line 104
        with open(("." + os.sep + "file%d" % number) if isinstance(number, int) else number, "rb") as fd:  # line 105
            return fd.read() == expectedContents  # line 105

    def testAccessor(_):  # line 107
        a = sos.Accessor({"a": 1})  # line 108
        _.assertEqual((1, 1), (a["a"], a.a))  # line 109

    def testFirstofmap(_):  # line 111
        _.assertEqual(2, sos.firstOfMap({"a": 1, "b": 2}, ["x", "b"]))  # line 112
        _.assertIsNone(sos.firstOfMap({"a": 1, "b": 2}, []))  # line 113

    def testAjoin(_):  # line 115
        _.assertEqual("a1a2", sos.ajoin("a", ["1", "2"]))  # line 116
        _.assertEqual("* a\n* b", sos.ajoin("* ", ["a", "b"], "\n"))  # line 117

    def testFindChanges(_):  # line 119
        m = sos.Metadata(os.getcwd())  # line 120
        m.loadBranches()  # line 121
        _.createFile(1, "1")  # line 122
        m.createBranch(0)  # line 123
        _.assertEqual(1, len(m.paths))  # line 124
        time.sleep(FS_PRECISION)  # time required by filesystem time resolution issues  # line 125
        _.createFile(1, "2")  # line 126
        _.createFile(2, "2")  # line 127
        changes = m.findChanges()  # detect time skew  # line 128
        _.assertEqual(1, len(changes.additions))  # line 129
        _.assertEqual(0, len(changes.deletions))  # line 130
        _.assertEqual(1, len(changes.modifications))  # line 131
        m.integrateChangeset(changes)  # line 132
        _.createFile(2, "12")  # modify file  # line 133
        changes = m.findChanges(0, 1)  # by size, creating new commit  # line 134
        _.assertEqual(0, len(changes.additions))  # line 135
        _.assertEqual(0, len(changes.deletions))  # line 136
        _.assertEqual(1, len(changes.modifications))  # line 137
        _.assertTrue(os.path.exists(branchFolder(0, 1)))  # line 138
        _.assertTrue(os.path.exists(branchFolder(0, 1) + os.sep + "03b69bc801ae11f1ff2a71a50f165996d0ad681b4f822df13329a27e53f0fcd2"))  # line 139

    def testDiffFunc(_):  # line 141
        a = {"./a": sos.PathInfo("", 0, 0, "")}  # line 142
        b = {"./a": sos.PathInfo("", 0, 0, "")}  # line 143
        changes = sos.diffPathSets(a, b)  # line 144
        _.assertEqual(0, len(changes.additions))  # line 145
        _.assertEqual(0, len(changes.deletions))  # line 146
        _.assertEqual(0, len(changes.modifications))  # line 147
        b = {"./a": sos.PathInfo("", 1, 0, "")}  # line 148
        changes = sos.diffPathSets(a, b)  # line 149
        _.assertEqual(0, len(changes.additions))  # line 150
        _.assertEqual(0, len(changes.deletions))  # line 151
        _.assertEqual(1, len(changes.modifications))  # line 152
        b = {}  # diff contains no entries -> no change  # line 153
        changes = sos.diffPathSets(a, b)  # line 154
        _.assertEqual(0, len(changes.additions))  # line 155
        _.assertEqual(0, len(changes.deletions))  # line 156
        _.assertEqual(0, len(changes.modifications))  # line 157
        b = {"./a": sos.PathInfo("", None, 1, "")}  # in diff marked as deleted  # line 158
        changes = sos.diffPathSets(a, b)  # line 159
        _.assertEqual(0, len(changes.additions))  # line 160
        _.assertEqual(1, len(changes.deletions))  # line 161
        _.assertEqual(0, len(changes.modifications))  # line 162
        b = {"./b": sos.PathInfo("", 1, 1, "")}  # line 163
        changes = sos.diffPathSets(a, b)  # line 164
        _.assertEqual(1, len(changes.additions))  # line 165
        _.assertEqual(0, len(changes.deletions))  # line 166
        _.assertEqual(0, len(changes.modifications))  # line 167
        a = {"./a": sos.PathInfo("", None, 0, "")}  # mark as deleted  # line 168
        b = {"./a": sos.PathInfo("", 1, 0, "")}  # re-added  # line 169
        changes = sos.diffPathSets(a, b)  # line 170
        _.assertEqual(1, len(changes.additions))  # line 171
        _.assertEqual(0, len(changes.deletions))  # line 172
        _.assertEqual(0, len(changes.modifications))  # line 173
        changes = sos.diffPathSets(b, a)  # line 174
        _.assertEqual(0, len(changes.additions))  # line 175
        _.assertEqual(1, len(changes.deletions))  # line 176
        _.assertEqual(0, len(changes.modifications))  # line 177

    def testPatternPaths(_):  # line 179
        sos.offline(options=["--track"])  # line 180
        os.mkdir("sub")  # line 181
        _.createFile("sub" + os.sep + "file1", "sdfsdf")  # line 182
        sos.add("./sub", "sub/file?")  # line 183
        sos.commit("test")  # should pick up sub/file1 pattern  # line 184
        _.assertEqual(2, len(os.listdir(os.path.join(sos.metaFolder, "b0", "r1"))))  # sub/file1 was added  # line 185
        _.createFile(1)  # line 186
        try:  # should not commit anything, as the file in base folder doesn't match the tracked pattern  # line 187
            sos.commit("nothing")  # should not commit anything, as the file in base folder doesn't match the tracked pattern  # line 187
            _.fail()  # should not commit anything, as the file in base folder doesn't match the tracked pattern  # line 187
        except:  # line 188
            pass  # line 188

    def testTokenizeGlobPattern(_):  # line 190
        _.assertEqual([], sos.tokenizeGlobPattern(""))  # line 191
        _.assertEqual([sos.GlobBlock(False, "*", 0)], sos.tokenizeGlobPattern("*"))  # line 192
        _.assertEqual([sos.GlobBlock(False, "*", 0), sos.GlobBlock(False, "???", 1)], sos.tokenizeGlobPattern("*???"))  # line 193
        _.assertEqual([sos.GlobBlock(True, "x", 0), sos.GlobBlock(False, "*", 1), sos.GlobBlock(True, "x", 2)], sos.tokenizeGlobPattern("x*x"))  # line 194
        _.assertEqual([sos.GlobBlock(True, "x", 0), sos.GlobBlock(False, "*", 1), sos.GlobBlock(False, "??", 2), sos.GlobBlock(False, "*", 4), sos.GlobBlock(True, "x", 5)], sos.tokenizeGlobPattern("x*??*x"))  # line 195
        _.assertEqual([sos.GlobBlock(False, "?", 0), sos.GlobBlock(True, "abc", 1), sos.GlobBlock(False, "*", 4)], sos.tokenizeGlobPattern("?abc*"))  # line 196

    def testTokenizeGlobPatterns(_):  # line 198
        try:  # because number of literal strings differs  # line 199
            sos.tokenizeGlobPatterns("x*x", "x*")  # because number of literal strings differs  # line 199
            _.fail()  # because number of literal strings differs  # line 199
        except:  # line 200
            pass  # line 200
        try:  # because glob patterns differ  # line 201
            sos.tokenizeGlobPatterns("x*", "x?")  # because glob patterns differ  # line 201
            _.fail()  # because glob patterns differ  # line 201
        except:  # line 202
            pass  # line 202
        try:  # glob patterns differ, regardless of position  # line 203
            sos.tokenizeGlobPatterns("x*", "?x")  # glob patterns differ, regardless of position  # line 203
            _.fail()  # glob patterns differ, regardless of position  # line 203
        except:  # line 204
            pass  # line 204
        sos.tokenizeGlobPatterns("x*", "*x")  # succeeds, because glob patterns match (differ only in position)  # line 205
        sos.tokenizeGlobPatterns("*xb?c", "*x?bc")  # succeeds, because glob patterns match (differ only in position)  # line 206
        try:  # succeeds, because glob patterns match (differ only in position)  # line 207
            sos.tokenizeGlobPatterns("a???b*", "ab???*")  # succeeds, because glob patterns match (differ only in position)  # line 207
            _.fail()  # succeeds, because glob patterns match (differ only in position)  # line 207
        except:  # line 208
            pass  # line 208

    def testConvertGlobFiles(_):  # line 210
        _.assertEqual(["xxayb", "aacb"], [r[1] for r in sos.convertGlobFiles(["axxby", "aabc"], *sos.tokenizeGlobPatterns("a*b?", "*a?b"))])  # line 211
        _.assertEqual(["1qq2ww3", "1abcbx2xbabc3"], [r[1] for r in sos.convertGlobFiles(["qqxbww", "abcbxxbxbabc"], *sos.tokenizeGlobPatterns("*xb*", "1*2*3"))])  # line 212

    def testComputeSequentialPathSet(_):  # line 214
        os.makedirs(branchFolder(0, 0))  # line 215
        os.makedirs(branchFolder(0, 1))  # line 216
        os.makedirs(branchFolder(0, 2))  # line 217
        os.makedirs(branchFolder(0, 3))  # line 218
        os.makedirs(branchFolder(0, 4))  # line 219
        m = sos.Metadata(os.getcwd())  # line 220
        m.branch = 0  # line 221
        m.commit = 2  # line 222
        m.saveBranches()  # line 223
        m.paths = {"./a": sos.PathInfo("", 0, 0, "")}  # line 224
        m.saveCommit(0, 0)  # initial  # line 225
        m.paths["./a"] = sos.PathInfo("", 1, 0, "")  # line 226
        m.saveCommit(0, 1)  # mod  # line 227
        m.paths["./b"] = sos.PathInfo("", 0, 0, "")  # line 228
        m.saveCommit(0, 2)  # add  # line 229
        m.paths["./a"] = sos.PathInfo("", None, 0, "")  # line 230
        m.saveCommit(0, 3)  # del  # line 231
        m.paths["./a"] = sos.PathInfo("", None, 0, "")  # line 232
        m.saveCommit(0, 4)  # readd  # line 233
        m.commits = {i: sos.CommitInfo(i, 0, None) for i in range(5)}  # line 234
        m.saveBranch(0)  # line 235
        m.computeSequentialPathSet(0, 4)  # line 236
        _.assertEqual(2, len(m.paths))  # line 237

    def testParseRevisionString(_):  # line 239
        m = sos.Metadata(os.getcwd())  # line 240
        m.branch = 1  # line 241
        m.commits = {0: 0, 1: 1, 2: 2}  # line 242
        _.assertEqual((1, 3), m.parseRevisionString("3"))  # line 243
        _.assertEqual((2, 3), m.parseRevisionString("2/3"))  # line 244
        _.assertEqual((1, -1), m.parseRevisionString(None))  # line 245
        _.assertEqual((2, -1), m.parseRevisionString("2/"))  # line 246
        _.assertEqual((1, -2), m.parseRevisionString("/-2"))  # line 247
        _.assertEqual((1, -1), m.parseRevisionString("/"))  # line 248

    def testOfflineEmpty(_):  # line 250
        os.mkdir("." + os.sep + sos.metaFolder)  # line 251
        try:  # line 252
            sos.offline("trunk")  # line 252
            _.fail()  # line 252
        except SystemExit:  # line 253
            pass  # line 253
        os.rmdir("." + os.sep + sos.metaFolder)  # line 254
        sos.offline("test")  # line 255
        _.assertIn(sos.metaFolder, os.listdir("."))  # line 256
        _.assertAllIn(["b0", sos.metaFile], os.listdir("." + os.sep + sos.metaFolder))  # line 257
        _.assertAllIn(["r0", sos.metaFile], os.listdir("." + os.sep + sos.metaFolder + os.sep + "b0"))  # line 258
        _.assertEqual(2, len(os.listdir("." + os.sep + sos.metaFolder)))  # only branch folder and meta data file  # line 259
        _.assertEqual(2, len(os.listdir("." + os.sep + sos.metaFolder + os.sep + "b0")))  # only commit folder and meta data file  # line 260
        _.assertEqual(1, len(os.listdir(branchFolder(0, 0))))  # only meta data file  # line 261

    def testOfflineWithFiles(_):  # line 263
        _.createFile(1, "x" * 100)  # line 264
        _.createFile(2)  # line 265
        sos.offline("test")  # line 266
        _.assertAllIn(["file1", "file2", sos.metaFolder], os.listdir("."))  # line 267
        _.assertAllIn(["b0", sos.metaFile], os.listdir("." + os.sep + sos.metaFolder))  # line 268
        _.assertAllIn(["r0", sos.metaFile], os.listdir("." + os.sep + sos.metaFolder + os.sep + "b0"))  # line 269
        _.assertAllIn([sos.metaFile, "03b69bc801ae11f1ff2a71a50f165996d0ad681b4f822df13329a27e53f0fcd2", "b9ee10a87f612e299a6eb208210bc0898092a64c48091327cc2aaeee9b764ffa"], os.listdir("." + os.sep + sos.metaFolder + os.sep + "b0" + os.sep + "r0"))  # line 270
        _.assertEqual(2, len(os.listdir("." + os.sep + sos.metaFolder)))  # only branch folder and meta data file  # line 271
        _.assertEqual(2, len(os.listdir("." + os.sep + sos.metaFolder + os.sep + "b0")))  # only commit folder and meta data file  # line 272
        _.assertEqual(3, len(os.listdir(branchFolder(0, 0))))  # only meta data file plus branch base file copies  # line 273

    def testBranch(_):  # line 275
        _.createFile(1, "x" * 100)  # line 276
        _.createFile(2)  # line 277
        sos.offline("test")  # b0/r0  # line 278
        sos.branch("other")  # b1/r0  # line 279
        _.assertAllIn(["b0", "b1", sos.metaFile], os.listdir("." + os.sep + sos.metaFolder))  # line 280
        _.assertEqual(list(sorted(os.listdir("." + os.sep + sos.metaFolder + os.sep + "b0"))), list(sorted(os.listdir("." + os.sep + sos.metaFolder + os.sep + "b1"))))  # line 281
        _.assertEqual(list(sorted(os.listdir(branchFolder(0, 0)))), list(sorted(os.listdir(branchFolder(1, 0)))))  # line 283
        _.createFile(1, "z")  # modify file  # line 285
        sos.branch()  # b2/r0  branch to unnamed branch with modified file tree contents  # line 286
        _.assertNotEqual(os.stat("." + os.sep + sos.metaFolder + os.sep + "b1" + os.sep + "r0" + os.sep + "b9ee10a87f612e299a6eb208210bc0898092a64c48091327cc2aaeee9b764ffa").st_size, os.stat("." + os.sep + sos.metaFolder + os.sep + "b2" + os.sep + "r0" + os.sep + "b9ee10a87f612e299a6eb208210bc0898092a64c48091327cc2aaeee9b764ffa").st_size)  # line 287
        _.createFile(3, "z")  # line 289
        sos.branch("from_last_revision", ["--last", "--stay"])  # b3/r0 create copy of other file1,file2 and don't switch  # line 290
        _.assertEqual(list(sorted(os.listdir("." + os.sep + sos.metaFolder + os.sep + "b3" + os.sep + "r0"))), list(sorted(os.listdir("." + os.sep + sos.metaFolder + os.sep + "b2" + os.sep + "r0"))))  # line 291
# Check sos.status output which branch is marked


    def testComittingAndChanges(_):  # line 296
        _.createFile(1, "x" * 100)  # line 297
        _.createFile(2)  # line 298
        sos.offline("test")  # line 299
        changes = sos.changes()  # line 300
        _.assertEqual(0, len(changes.additions))  # line 301
        _.assertEqual(0, len(changes.deletions))  # line 302
        _.assertEqual(0, len(changes.modifications))  # line 303
        _.createFile(1, "z")  # size change  # line 304
        changes = sos.changes()  # line 305
        _.assertEqual(0, len(changes.additions))  # line 306
        _.assertEqual(0, len(changes.deletions))  # line 307
        _.assertEqual(1, len(changes.modifications))  # line 308
        sos.commit("message")  # line 309
        _.assertAllIn(["r0", "r1", sos.metaFile], os.listdir("." + os.sep + sos.metaFolder + os.sep + "b0"))  # line 310
        _.assertAllIn([sos.metaFile, "b9ee10a87f612e299a6eb208210bc0898092a64c48091327cc2aaeee9b764ffa"], os.listdir(branchFolder(0, 1)))  # line 311
        _.assertEqual(2, len(os.listdir(branchFolder(0, 1))))  # no further files, only the modified one  # line 312
        _.assertEqual(1, len(sos.changes("/0").modifications))  # vs. explicit revision on current branch  # line 313
        _.assertEqual(1, len(sos.changes("0/0").modifications))  # vs. explicit branch/revision  # line 314
        _.createFile(1, "")  # modify to empty file, mentioned in meta data, but not stored as own file  # line 315
        os.unlink("file2")  # line 316
        changes = sos.changes()  # line 317
        _.assertEqual(0, len(changes.additions))  # line 318
        _.assertEqual(1, len(changes.deletions))  # line 319
        _.assertEqual(1, len(changes.modifications))  # line 320
        sos.commit("modified")  # line 321
        _.assertEqual(1, len(os.listdir(branchFolder(0, 2))))  # no additional files, only mentions in metadata  # line 322
        try:  # expecting Exit due to no changes  # line 323
            sos.commit("nothing")  # expecting Exit due to no changes  # line 323
            _.fail()  # expecting Exit due to no changes  # line 323
        except:  # line 324
            pass  # line 324

    def testGetBranch(_):  # line 326
        m = sos.Metadata(os.getcwd())  # line 327
        m.branch = 1  # current branch  # line 328
        m.branches = {0: sos.BranchInfo(0, 0, "trunk")}  # line 329
        _.assertEqual(27, m.getBranchByName(27))  # line 330
        _.assertEqual(0, m.getBranchByName("trunk"))  # line 331
        _.assertEqual(1, m.getBranchByName(""))  # split from "/"  # line 332
        _.assertIsNone(m.getBranchByName("unknown"))  # line 333
        m.commits = {0: sos.CommitInfo(0, 0, "bla")}  # line 334
        _.assertEqual(13, m.getRevisionByName("13"))  # line 335
        _.assertEqual(0, m.getRevisionByName("bla"))  # line 336
        _.assertEqual(-1, m.getRevisionByName(""))  # split from "/"  # line 337

    def testTagging(_):  # line 339
        m = sos.Metadata(os.getcwd())  # line 340
        sos.offline()  # line 341
        _.createFile(111)  # line 342
        sos.commit("tag", ["--tag"])  # line 343
        _.createFile(2)  # line 344
        try:  # line 345
            sos.commit("tag")  # line 345
            _.fail()  # line 345
        except:  # line 346
            pass  # line 346
        sos.commit("tag-2", ["--tag"])  # line 347

    def testSwitch(_):  # line 349
        _.createFile(1, "x" * 100)  # line 350
        _.createFile(2, "y")  # line 351
        sos.offline("test")  # file1-2  in initial branch commit  # line 352
        sos.branch("second")  # file1-2  switch, having same files  # line 353
        sos.switch("0")  # no change  switch back, no problem  # line 354
        sos.switch("second")  # no change  # switch back, no problem  # line 355
        _.createFile(3, "y")  # generate a file  # line 356
        try:  # uncommited changes detected  # line 357
            sos.switch("test")  # uncommited changes detected  # line 357
            _.fail()  # uncommited changes detected  # line 357
        except SystemExit:  # line 358
            pass  # line 358
        sos.commit("Finish")  # file1-3  commit third file into branch second  # line 359
        sos.changes()  # line 360
        sos.switch("test")  # file1-2, remove file3 from file tree  # line 361
        _.assertFalse(_.existsFile(3))  # removed when switching back to test  # line 362
        out = wrapChannels(lambda: sos.status()).replace("\r", "")  # line 363
        _.assertIn("  * b00   'test'", out)  # line 364
        _.assertIn("    b01 'second'", out)  # line 365
        _.assertIn("(dirty)", out)  # one branch has commits  # line 366
        _.assertIn("(in sync)", out)  # the other doesn't  # line 367
        _.createFile(4, "xy")  # generate a file  # line 368
        sos.switch("second", "--force")  # avoids warning on uncommited changes, but keeps file4  # line 369
        _.assertFalse(_.existsFile(4))  # removed when forcedly switching back to test  # line 370
        _.assertTrue(_.existsFile(3))  # was restored from branch's revision r1  # line 371
        os.unlink("." + os.sep + "file1")  # remove old file1  # line 372
        sos.switch("test", "--force")  # should restore file1 and remove file3  # line 373
        _.assertTrue(_.existsFile(1))  # was restored from branch's revision r1  # line 374
        _.assertFalse(_.existsFile(3))  # was restored from branch's revision r1  # line 375

    def testAutoDetectVCS(_):  # line 377
        os.mkdir(".git")  # line 378
        sos.offline(sos.vcsBranches[sos.findSosVcsBase()[2]])  # create initial branch  # line 379
        with open(sos.metaFolder + os.sep + sos.metaFile, "r") as fd:  # line 380
            meta = fd.read()  # line 380
        _.assertTrue("\"master\"" in meta)  # line 381
        os.rmdir(".git")  # line 382

    def testUpdate(_):  # line 384
        sos.offline("trunk")  # create initial branch b0/r0  # line 385
        _.createFile(1, "x" * 100)  # line 386
        sos.commit("second")  # create b0/r1  # line 387

        sos.switch("/0")  # go back to b0/r0 - deletes file1  # line 389
        _.assertFalse(_.existsFile(1))  # line 390

        sos.update("/1")  # recreate file1  # line 392
        _.assertTrue(_.existsFile(1))  # line 393

        sos.commit("third", ["--force"])  # force because nothing to commit. should create r2 with same contents as r1, but as differential from r1, not from r0 (= no changes in meta folder)  # line 395
        _.assertTrue(os.path.exists(branchFolder(0, 2)))  # line 396
        _.assertTrue(os.path.exists(branchFolder(0, 2) + os.sep + sos.metaFile))  # line 397
        _.assertEqual(1, len(os.listdir(branchFolder(0, 2))))  # only meta data file, no differential files  # line 398

        sos.update("/1")  # do nothing, as nothing has changed  # line 400
        _.assertTrue(_.existsFile(1))  # line 401

        _.createFile(2, "y" * 100)  # line 403
#    out = wrapChannels(() -> sos.branch("other"))  # won't comply as there are changes
#    _.assertIn("--force", out)
        sos.branch("other", ["--force"])  # automatically including file 2 (as we are in simple mode)  # line 406
        _.assertTrue(_.existsFile(2))  # line 407
        sos.update("trunk", ["--add"])  # only add stuff  # line 408
        _.assertTrue(_.existsFile(2))  # line 409
        sos.update("trunk")  # nothing to do  # line 410
        _.assertFalse(_.existsFile(2))  # removes file not present in original branch  # line 411

        theirs = b"a\nb\nc\nd\ne\nf\ng\nh\nx\nx\nj\nk"  # line 413
        _.createFile(10, theirs)  # line 414
        mine = b"a\nc\nd\ne\ng\nf\nx\nh\ny\ny\nj"  # missing "b", inserted g, modified g->x, replace x/x -> y/y, removed k  # line 415
        _.createFile(11, mine)  # line 416
        _.assertEqual(b"a\nb\nc\nd\ne\nf\ng\nh\nx\nx\nj\nk", sos.merge(filename="." + os.sep + "file10", intoname="." + os.sep + "file11", mergeOperation=sos.MergeOperation.BOTH, conflictResolution=sos.ConflictResolution.THEIRS))  # completely recreated other file  # line 417
        _.assertEqual(b"a\nb\nc\nd\ne\ng\nf\ng\nx\nh\nx\nx\ny\ny\nj\nk", sos.merge(filename="." + os.sep + "file10", intoname="." + os.sep + "file11", mergeOperation=sos.MergeOperation.INSERT, conflictResolution=sos.ConflictResolution.MINE))  # line 418

    def testUpdate2(_):  # line 420
        _.createFile("test.txt", "x" * 10)  # line 421
        sos.offline("trunk", ["--strict"])  # use strict mode, as timestamp differences are too small for testing  # line 422
        sos.branch("mod")  # line 423
        _.createFile("test.txt", "x" * 5 + "y" * 5)  # line 424
        time.sleep(FS_PRECISION)  # line 425
        sos.commit("mod")  # create b0/r1  # line 426
        sos.switch("trunk", ["--force"])  # should replace contents, force in case some other files were modified (e.g. during working on the code) TODO investigate more  # line 427
        with open("test.txt", "rb") as fd:  # line 428
            _.assertEqual(b"x" * 10, fd.read())  # line 428
        sos.update("mod", ["--theirs"])  # integrate changes TODO same with ask -> theirs  # line 429
        with open("test.txt", "rb") as fd:  # line 430
            _.assertEqual(b"x" * 5 + b"y" * 5, fd.read())  # line 430
        _.createFile("test.txt", "x" * 10)  # line 431
        mockInput(["t"], lambda: sos.update("mod", ["--ask"]))  # same as above with interaction -> theirs  # line 432
        with open("test.txt", "rb") as fd:  # line 433
            _.assertEqual(b"x" * 5 + b"y" * 5, fd.read())  # line 433

    def testIsTextType(_):  # line 435
        m = sos.Metadata(".")  # line 436
        m.c.texttype = ["*.x", "*.md", "*.md.*"]  # line 437
        m.c.bintype = ["*.md.confluence"]  # line 438
        _.assertTrue(m.isTextType("ab.txt"))  # line 439
        _.assertTrue(m.isTextType("./ab.txt"))  # line 440
        _.assertTrue(m.isTextType("bc/ab.txt"))  # line 441
        _.assertFalse(m.isTextType("bc/ab."))  # line 442
        _.assertTrue(m.isTextType("23_3.x.x"))  # line 443
        _.assertTrue(m.isTextType("dfg/dfglkjdf7/test.md"))  # line 444
        _.assertTrue(m.isTextType("./test.md.pdf"))  # line 445
        _.assertFalse(m.isTextType("./test_a.md.confluence"))  # line 446

    def testEolDet(_):  # line 448
        ''' Check correct end-of-line detection. '''  # line 449
        _.assertEqual(b"\n", sos.eoldet(b"a\nb"))  # line 450
        _.assertEqual(b"\r\n", sos.eoldet(b"a\r\nb\r\n"))  # line 451
        _.assertEqual(b"\r", sos.eoldet(b"\ra\rb"))  # line 452
        _.assertAllIn(["Inconsistent", "with "], wrapChannels(lambda: _.assertEqual(b"\n", sos.eoldet(b"\r\na\r\nb\n"))))  # line 453
        _.assertAllIn(["Inconsistent", "without"], wrapChannels(lambda: _.assertEqual(b"\n", sos.eoldet(b"\ra\nnb\n"))))  # line 454
        _.assertIsNone(sos.eoldet(b""))  # line 455
        _.assertIsNone(sos.eoldet(b"sdf"))  # line 456

    def testMerge(_):  # line 458
        ''' Check merge results depending on conflict solution options. '''  # line 459
        a = b"a\nb\ncc\nd"  # line 460
        b = b"a\nb\nee\nd"  # line 461
        _.assertEqual(b"a\nb\ncc\nee\nd", sos.merge(a, b, mergeOperation=sos.MergeOperation.INSERT))  # means insert changes from a into b, but don't replace  # line 462
        _.assertEqual(b"a\nb\nd", sos.merge(a, b, mergeOperation=sos.MergeOperation.REMOVE))  # line 463
        _.assertEqual(b"a\nb\ncc\nd", sos.merge(a, b, mergeOperation=sos.MergeOperation.BOTH))  # line 464
# Now test intra-line merging without conflicts
        _.assertEqual(b"a\nbc d\ne", sos.merge(b"a\nbc d\ne", b"a\nbcd\ne", mergeOperation=sos.MergeOperation.INSERT))  # because it's a deletion ['  a', '- bc d', '?   -\n', '+ bcd', '  e']  # line 466
        _.assertEqual(b"a\nbcd\ne", sos.merge(b"a\nbc d\ne", b"a\nbcd\ne", mergeOperation=sos.MergeOperation.REMOVE))  # ['  a', '- bc d', '?   -\n', '+ bcd', '  e']  # line 467
        _.assertEqual(b"a\nbc d\ne", sos.merge(b"a\nbcd\ne", b"a\nbc d\ne", mergeOperation=sos.MergeOperation.INSERT))  # nothing to insert  # line 468
        _.assertEqual(b"a\nbcd\ne", sos.merge(b"a\nbcd\ne", b"a\nbc d\ne", mergeOperation=sos.MergeOperation.REMOVE))  # remove space  # line 469
# Test with change + insert (conflict)
        _.assertEqual(b"a\nb fdd d\ne", sos.merge(b"a\nb cd d\ne", b"a\nb fdd d\ne", conflictResolution=sos.ConflictResolution.MINE))  # line 471
        _.assertEqual(b"a\nb cd d\ne", sos.merge(b"a\nb cd d\ne", b"a\nb fdd d\ne", conflictResolution=sos.ConflictResolution.THEIRS))  # ['  a', '- b cd d', '?   ^\n', '+ b fdd d', '?   ^^\n', '  e']  # line 472
        _.assertEqual(b"a\nb fdd d\ne", mockInput(["i"], lambda: sos.merge(b"a\nb cd d\ne", b"a\nb fdd d\ne", conflictResolution=sos.ConflictResolution.ASK)))  # ['  a', '- b cd d', '?   ^\n', '+ b fdd d', '?   ^^\n', '  e']  # line 473
        _.assertEqual(b"a\nb cd d\ne", mockInput(["t"], lambda: sos.merge(b"a\nb cd d\ne", b"a\nb fdd d\ne", conflictResolution=sos.ConflictResolution.ASK)))  # ['  a', '- b cd d', '?   ^\n', '+ b fdd d', '?   ^^\n', '  e']  # line 474
        _.assertEqual(b"abbc", sos.merge(b"abbc", b"addc", mergeOperation=sos.MergeOperation.BOTH, conflictResolution=sos.ConflictResolution.THEIRS))  # line 475
        _.assertEqual(b"a\nbb\nc", sos.merge(b"a\nbb\nc", b"a\ndd\nc", mergeOperation=sos.MergeOperation.BOTH, conflictResolution=sos.ConflictResolution.THEIRS))  # line 476
        _.assertIn("Differing EOL-styles", wrapChannels(lambda: sos.merge(b"a\nb", b"a\r\nb")))  # expect warning  # line 477
        _.assertIn(b"a\r\nb", sos.merge(b"a\nb", b"a\r\nb"))  # in doubt, use "mine" CR-LF  # line 478

    def testPickyMode(_):  # line 480
        ''' Confirm that picky mode reset tracked patterns after commits. '''  # line 481
        sos.offline("trunk", ["--picky"])  # line 482
        sos.add(".", "./file?", ["--force"])  # line 483
        _.createFile(1, "aa")  # line 484
        sos.commit("First")  # add one file  # line 485
        _.assertEqual(2, len(os.listdir(branchFolder(0, 1))))  # line 486
        _.createFile(2, "b")  # line 487
        try:  # add nothing, because picky  # line 488
            sos.commit("Second")  # add nothing, because picky  # line 488
        except:  # line 489
            pass  # line 489
        sos.add(".", "./file?")  # line 490
        sos.commit("Third")  # line 491
        _.assertEqual(2, len(os.listdir(branchFolder(0, 2))))  # line 492
        out = wrapChannels(lambda: sos.log([])).replace("\r", "")  # line 493
        _.assertIn("  * r2", out)  # line 494

    def testTrackedSubfolder(_):  # line 496
        ''' See if patterns for files in sub folders are picked up correctly. '''  # line 497
        os.mkdir("." + os.sep + "sub")  # line 498
        sos.offline("trunk", ["--track"])  # line 499
        _.createFile(1, "x")  # line 500
        _.createFile(1, "x", prefix="sub")  # line 501
        sos.add(".", "./file?")  # add glob pattern to track  # line 502
        sos.commit("First")  # line 503
        _.assertEqual(2, len(os.listdir(branchFolder(0, 1))))  # one new file + meta file  # line 504
        sos.add(".", "sub/file?")  # add glob pattern to track  # line 505
        sos.commit("Second")  # one new file + meta  # line 506
        _.assertEqual(2, len(os.listdir(branchFolder(0, 1))))  # one new file + meta file  # line 507
        os.unlink("file1")  # remove from basefolder  # line 508
        _.createFile(2, "y")  # line 509
        sos.rm(".", "sub/file?")  # line 510
        try:  # raises Exit. TODO test the "suggest a pattern" case  # line 511
            sos.rm(".", "sub/bla")  # raises Exit. TODO test the "suggest a pattern" case  # line 511
            _.fail()  # raises Exit. TODO test the "suggest a pattern" case  # line 511
        except:  # line 512
            pass  # line 512
        sos.commit("Third")  # line 513
        _.assertEqual(2, len(os.listdir(branchFolder(0, 2))))  # one new file + meta  # line 514
# TODO check if /file1 and sub/file1 were removed from index

    def testTrackedMode(_):  # line 517
        ''' Difference in semantics vs simple mode:
          - For remote/other branch we can only know and consider tracked files, thus ignoring all complexity stemming from handling addition of untracked files.
          - For current branch, we can take into account tracked and untracked ones, in theory, but it doesn't make sense.
        In conclusion, using the union of tracking patterns from both sides to find affected files makes sense, but disallow deleting files not present in remote branch.
    '''  # line 522
        sos.offline("test", options=["--track"])  # set up repo in tracking mode (SVN- or gitless-style)  # line 523
        _.createFile(1)  # line 524
        _.createFile("a123a")  # untracked file "a123a"  # line 525
        sos.add(".", "./file?")  # add glob tracking pattern  # line 526
        sos.commit("second")  # versions "file1"  # line 527
        _.assertEqual(2, len(os.listdir(branchFolder(0, 1))))  # one new file + meta file  # line 528
        out = wrapChannels(lambda: sos.status()).replace("\r", "")  # line 529
        _.assertIn("  | ./file?", out)  # line 530

        _.createFile(2)  # untracked file "file2"  # line 532
        sos.commit("third")  # versions "file2"  # line 533
        _.assertEqual(2, len(os.listdir(branchFolder(0, 2))))  # one new file + meta file  # line 534

        os.mkdir("." + os.sep + "sub")  # line 536
        _.createFile(3, prefix="sub")  # untracked file "sub/file3"  # line 537
        sos.commit("fourth", ["--force"])  # no tracking pattern matches the subfolder  # line 538
        _.assertEqual(1, len(os.listdir(branchFolder(0, 3))))  # meta file only, no other tracked path/file  # line 539

        sos.branch("Other")  # second branch containing file1 and file2 tracked by "./file?"  # line 541
        sos.rm(".", "./file?")  # remove tracking pattern, but don't touch previously created and versioned files  # line 542
        sos.add(".", "./a*a")  # add tracking pattern  # line 543
        changes = sos.changes()  # should pick up addition only, because tracked, but not the deletion, as not tracked anymore  # line 544
        _.assertEqual(0, len(changes.modifications))  # line 545
        _.assertEqual(0, len(changes.deletions))  # not tracked anymore, but contained in version history and not removed  # line 546
        _.assertEqual(1, len(changes.additions))  # detected one addition "a123a", but won't recognize untracking files as deletion  # line 547

        sos.commit("Second_2")  # line 549
        _.assertEqual(2, len(os.listdir(branchFolder(1, 1))))  # "a123a" + meta file  # line 550
        _.assertTrue(os.path.exists("." + os.sep + "file1"))  # line 551
        _.assertTrue(os.path.exists("." + os.sep + "file2"))  # line 552

        sos.switch("test")  # go back to first branch - tracks only "file?", but not "a*a"  # line 554
        _.assertTrue(os.path.exists("." + os.sep + "file1"))  # line 555
        _.assertTrue(os.path.exists("." + os.sep + "a123a"))  # should not have been touched so far  # line 556

        sos.update("Other")  # integrate tracked files and tracking pattern from second branch into working state of master branch  # line 558
        _.assertTrue(os.path.exists("." + os.sep + "file1"))  # line 559
        _.assertTrue(os.path.exists("." + os.sep + "a123a"))  # line 560

        _.createFile("axxxa")  # new file that should be tracked on "test" now that we integrated "Other"  # line 562
        sos.commit("fifth")  # create new revision after integrating updates from second branch  # line 563
        _.assertEqual(3, len(os.listdir(branchFolder(0, 4))))  # one new file from other branch + one new in current folder + meta file  # line 564
        sos.switch("Other")  # switch back to just integrated branch that tracks only "a*a" - shouldn't do anything  # line 565
        _.assertTrue(os.path.exists("." + os.sep + "file1"))  # line 566
        _.assertTrue(os.path.exists("." + os.sep + "a123a"))  # line 567
        _.assertFalse(os.path.exists("." + os.sep + "axxxa"))  # because tracked in both branches, but not present in other -> delete in file tree TODO document  # line 568
# TODO test switch --meta

    def testLsTracked(_):  # line 571
        sos.offline("test", options=["--track"])  # set up repo in tracking mode (SVN- or gitless-style)  # line 572
        _.createFile(1)  # line 573
        _.createFile("foo")  # line 574
        sos.add(".", "./file*")  # capture one file  # line 575
        out = sos.safeSplit(wrapChannels(lambda: sos.ls()).replace("\r", ""), "\n")  # line 576
        _.assertInAny('TRK file1 by "./file*"', out)  # line 577
        _.assertNotInAny('    file1 by "./file*"', out)  # line 578
        _.assertInAny("    foo", out)  # line 579

    def testCompression(_):  # line 581
        _.createFile(1)  # line 582
        sos.offline("master", options=["--plain", "--force"])  # line 583
        _.assertTrue(_.existsFile(branchFolder(0, 0) + os.sep + "b9ee10a87f612e299a6eb208210bc0898092a64c48091327cc2aaeee9b764ffa", b"x" * 10))  # line 584
        setRepoFlag("compress", True)  # was plain = uncompressed before  # line 585
        _.createFile(2)  # line 586
        sos.commit("Added file2")  # line 587
        _.assertTrue(_.existsFile(branchFolder(0, 1) + os.sep + "03b69bc801ae11f1ff2a71a50f165996d0ad681b4f822df13329a27e53f0fcd2"))  # exists  # line 588
        _.assertFalse(_.existsFile(branchFolder(0, 1) + os.sep + "03b69bc801ae11f1ff2a71a50f165996d0ad681b4f822df13329a27e53f0fcd2", b"x" * 10))  # but is compressed instead  # line 589

    def testConfigVariations(_):  # line 591
        def makeRepo():  # line 592
            try:  # line 593
                os.unlink("file1")  # line 593
            except:  # line 594
                pass  # line 594
            sos.offline("master", options=["--plain", "--force"])  # line 595
            _.createFile(1)  # line 596
            sos.commit("Added file1")  # line 597
        sos.config("set", ["strict", "on"])  # line 598
        makeRepo()  # line 599
        _.assertTrue(checkRepoFlag("strict", True))  # line 600
        sos.config("set", ["strict", "off"])  # line 601
        makeRepo()  # line 602
        _.assertTrue(checkRepoFlag("strict", False))  # line 603
        sos.config("set", ["strict", "yes"])  # line 604
        makeRepo()  # line 605
        _.assertTrue(checkRepoFlag("strict", True))  # line 606
        sos.config("set", ["strict", "no"])  # line 607
        makeRepo()  # line 608
        _.assertTrue(checkRepoFlag("strict", False))  # line 609
        sos.config("set", ["strict", "1"])  # line 610
        makeRepo()  # line 611
        _.assertTrue(checkRepoFlag("strict", True))  # line 612
        sos.config("set", ["strict", "0"])  # line 613
        makeRepo()  # line 614
        _.assertTrue(checkRepoFlag("strict", False))  # line 615
        sos.config("set", ["strict", "true"])  # line 616
        makeRepo()  # line 617
        _.assertTrue(checkRepoFlag("strict", True))  # line 618
        sos.config("set", ["strict", "false"])  # line 619
        makeRepo()  # line 620
        _.assertTrue(checkRepoFlag("strict", False))  # line 621
        sos.config("set", ["strict", "enable"])  # line 622
        makeRepo()  # line 623
        _.assertTrue(checkRepoFlag("strict", True))  # line 624
        sos.config("set", ["strict", "disable"])  # line 625
        makeRepo()  # line 626
        _.assertTrue(checkRepoFlag("strict", False))  # line 627
        sos.config("set", ["strict", "enabled"])  # line 628
        makeRepo()  # line 629
        _.assertTrue(checkRepoFlag("strict", True))  # line 630
        sos.config("set", ["strict", "disabled"])  # line 631
        makeRepo()  # line 632
        _.assertTrue(checkRepoFlag("strict", False))  # line 633
        try:  # line 634
            sos.config("set", ["strict", "nope"])  # line 634
            _.fail()  # line 634
        except:  # line 635
            pass  # line 635

    def testLsSimple(_):  # line 637
        _.createFile(1)  # line 638
        _.createFile("foo")  # line 639
        _.createFile("ign1")  # line 640
        _.createFile("ign2")  # line 641
        sos.offline("test")  # set up repo in tracking mode (SVN- or gitless-style)  # line 642
        sos.config("set", ["ignores", "ign1"])  # define an ignore pattern  # line 643
        sos.config("add", ["ignores", "ign2"])  # define an ignore pattern  # line 644
        sos.config("set", ["ignoresWhitelist", "ign1;ign2"])  # define a list of ignore patterns  # line 645
        out = wrapChannels(lambda: sos.config("show")).replace("\r", "")  # line 646
        _.assertIn("ignores => ['ign1', 'ign2']", out)  # line 647
        out = sos.safeSplit(wrapChannels(lambda: sos.ls()).replace("\r", ""), "\n")  # line 648
        _.assertInAny('    file1', out)  # line 649
        _.assertInAny('    ign1', out)  # line 650
        _.assertInAny('    ign2', out)  # line 651
        try:  # line 652
            sos.config("rm", ["foo", "bar"])  # line 652
            _.fail()  # line 652
        except:  # line 653
            pass  # line 653
        try:  # line 654
            sos.config("rm", ["ignores", "foo"])  # line 654
            _.fail()  # line 654
        except:  # line 655
            pass  # line 655
        sos.config("rm", ["ignores", "ign1"])  # line 656
        sos.config("unset", ["ignoresWhitelist"])  # remove ignore pattern  # line 657
        out = sos.safeSplit(wrapChannels(lambda: sos.ls()).replace("\r", ""), "\n")  # line 658
        _.assertInAny('    ign1', out)  # line 659
        _.assertInAny('IGN ign2', out)  # line 660
        _.assertNotInAny('    ign2', out)  # line 661

    def testWhitelist(_):  # line 663
# TODO test same for simple mode
        _.createFile(1)  # line 665
        sos.defaults.ignores[:] = ["file*"]  # replace in-place  # line 666
        sos.offline("xx", ["--track", "--strict"])  # because nothing to commit due to ignore pattern  # line 667
        sos.add(".", "./file*")  # add tracking pattern for "file1"  # line 668
        sos.commit(options=["--force"])  # attempt to commit the file  # line 669
        _.assertEqual(1, len(os.listdir(branchFolder(0, 1))))  # only meta data, file1 was ignored  # line 670
        try:  # Exit because dirty  # line 671
            sos.online()  # Exit because dirty  # line 671
            _.fail()  # Exit because dirty  # line 671
        except:  # exception expected  # line 672
            pass  # exception expected  # line 672
        _.createFile("x2")  # add another change  # line 673
        sos.add(".", "./x?")  # add tracking pattern for "file1"  # line 674
        try:  # force beyond dirty flag check  # line 675
            sos.online(["--force"])  # force beyond dirty flag check  # line 675
            _.fail()  # force beyond dirty flag check  # line 675
        except:  # line 676
            pass  # line 676
        sos.online(["--force", "--force"])  # force beyond file tree modifications check  # line 677
        _.assertFalse(os.path.exists(sos.metaFolder))  # line 678

        _.createFile(1)  # line 680
        sos.defaults.ignoresWhitelist[:] = ["file*"]  # line 681
        sos.offline("xx", ["--track"])  # line 682
        sos.add(".", "./file*")  # line 683
        sos.commit()  # should NOT ask for force here  # line 684
        _.assertEqual(2, len(os.listdir(branchFolder(0, 1))))  # meta data and "file1", file1 was whitelisted  # line 685

    def testRemove(_):  # line 687
        _.createFile(1, "x" * 100)  # line 688
        sos.offline("trunk")  # line 689
        try:  # line 690
            sos.delete("trunk")  # line 690
            _fail()  # line 690
        except:  # line 691
            pass  # line 691
        _.createFile(2, "y" * 10)  # line 692
        sos.branch("added")  # line 693
        sos.delete("trunk")  # line 694
        _.assertEqual(2, len(os.listdir("." + os.sep + sos.metaFolder)))  # meta data file and "b1"  # line 695
        _.assertTrue(os.path.exists("." + os.sep + sos.metaFolder + os.sep + "b1"))  # line 696
        _.assertFalse(os.path.exists("." + os.sep + sos.metaFolder + os.sep + "b0"))  # line 697
        sos.branch("next")  # line 698
        _.createFile(3, "y" * 10)  # make a change  # line 699
        sos.delete("added", "--force")  # should succeed  # line 700

    def testUsage(_):  # line 702
        sos.usage()  # line 703

    def testOnly(_):  # line 705
        _.assertEqual((_coconut.frozenset(("./A", "x/B")), _coconut.frozenset(("./C",))), sos.parseOnlyOptions(".", ["abc", "def", "--only", "A", "--x", "--only", "x/B", "--except", "C", "--only"]))  # line 706
        _.assertEqual(_coconut.frozenset(("B",)), sos.conditionalIntersection(_coconut.frozenset(("A", "B", "C")), _coconut.frozenset(("B", "D"))))  # line 707
        _.assertEqual(_coconut.frozenset(("B", "D")), sos.conditionalIntersection(_coconut.frozenset(), _coconut.frozenset(("B", "D"))))  # line 708
        _.assertEqual(_coconut.frozenset(("B", "D")), sos.conditionalIntersection(None, _coconut.frozenset(("B", "D"))))  # line 709

    def testDiff(_):  # line 711
        sos.offline(options=["--strict"])  # line 712
        _.createFile(1)  # line 713
        _.createFile(2)  # line 714
        sos.commit()  # line 715
        _.createFile(1, "sdfsdgfsdf")  # line 716
        _.createFile(2, "12343")  # line 717
        sos.commit()  # line 718
        _.createFile(1, "foobar")  # line 719
        _.assertAllIn(["MOD ./file1", "MOD ./file2", "DIF ./file1", "- | 0000 |xxxxxxxxxx|", "+ | 0000 |foobar|"], wrapChannels(lambda: sos.diff("/-2")))  # vs. second last  # line 720
        _.assertNotIn("MOD ./file1", wrapChannels(lambda: sos.diff("/-2", onlys=_coconut.frozenset(("./file2",)))))  # line 721

    def testFindBase(_):  # line 723
        old = os.getcwd()  # line 724
        try:  # line 725
            os.mkdir("." + os.sep + ".git")  # line 726
            os.makedirs("." + os.sep + "a" + os.sep + sos.metaFolder)  # line 727
            os.makedirs("." + os.sep + "a" + os.sep + "b")  # line 728
            os.chdir("a" + os.sep + "b")  # line 729
            s, vcs, cmd = sos.findSosVcsBase()  # line 730
            _.assertIsNotNone(s)  # line 731
            _.assertIsNotNone(vcs)  # line 732
            _.assertEqual("git", cmd)  # line 733
        finally:  # line 734
            os.chdir(old)  # line 734


if __name__ == '__main__':  # line 737
    logging.basicConfig(level=logging.DEBUG if '-v' in sys.argv or os.getenv("DEBUG", "false").strip().lower() == "true" or os.getenv("CI", "false").strip().lower() == "true" else logging.INFO, stream=sys.stderr, format="%(asctime)-23s %(levelname)-8s %(name)s:%(lineno)d | %(message)s" if '-v' in sys.argv or os.getenv("DEBUG", "false") == "true" else "%(message)s")  # line 738
    if configr:  # line 739
        c = configr.Configr("sos")  # line 740
        c.loadSettings()  # line 740
        if len(c.keys()) > 0:  # line 741
            sos.Exit("Cannot run test suite with existing local SOS user configuration (would affect results)")  # line 741
    unittest.main(testRunner=debugTestRunner() if '-v' in sys.argv and not os.getenv("CI", "false").lower() == "true" else None)  # warnings = "ignore")  # line 742
