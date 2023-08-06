#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# __coconut_hash__ = 0x236e0a6d

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


@_coconut_tco  # line 17
def debugTestRunner(post_mortem=None):  # line 17
    ''' Unittest runner doing post mortem debugging on failing tests. '''  # line 18
    import pdb  # line 19
    if post_mortem is None:  # line 20
        post_mortem = pdb.post_mortem  # line 20
    class DebugTestResult(unittest.TextTestResult):  # line 21
        def addError(self, test, err):  # called before tearDown()  # line 22
            traceback.print_exception(*err)  # line 23
            post_mortem(err[2])  # line 24
            super(DebugTestResult, self).addError(test, err)  # line 25
        def addFailure(self, test, err):  # line 26
            traceback.print_exception(*err)  # line 27
            post_mortem(err[2])  # line 28
            super(DebugTestResult, self).addFailure(test, err)  # line 29
    return _coconut_tail_call(unittest.TextTestRunner, resultclass=DebugTestResult)  # line 30

def branchFolder(branch: 'int', revision: 'int') -> 'str':  # line 32
    return "." + os.sep + sos.metaFolder + os.sep + "b%d" % branch + os.sep + "r%d" % revision  # line 32

@_coconut_tco  # line 34
def wrapChannels(func: '_coconut.typing.Callable[..., Any]'):  # line 34
    ''' Wrap function call to capture and return strings emitted on stdout and stderr. '''  # line 35
    oldv, oldo, olde = sys.argv, sys.stdout, sys.stderr  # line 36
    buf = StringIO()  # line 37
    sys.stdout = sys.stderr = buf  # line 38
    handler = logging.StreamHandler(buf)  # line 39
    logging.getLogger().addHandler(handler)  # line 40
    try:  # capture output into buf  # line 41
        func()  # capture output into buf  # line 41
    except Exception as E:  # line 42
        buf.write(str(E) + "\n")  # line 42
        traceback.print_exc(file=buf)  # line 42
    logging.getLogger().removeHandler(handler)  # line 43
    sys.argv, sys.stdout, sys.stderr = oldv, oldo, olde  # line 44
    return _coconut_tail_call(buf.getvalue)  # line 45

def mockInput(datas: '_coconut.typing.Sequence[str]', func) -> 'Any':  # line 47
    with mock.patch("builtins.input" if sys.version_info.major >= 3 else "utility._coconut_raw_input", side_effect=datas):  # line 48
        return func()  # line 48

def setRepoFlag(name: 'str', value: 'bool') -> 'None':  # line 50
    with open(sos.metaFolder + os.sep + sos.metaFile, "r") as fd:  # line 51
        flags, branches = json.loads(fd.read())  # line 51
    flags[name] = value  # line 52
    with open(sos.metaFolder + os.sep + sos.metaFile, "w") as fd:  # line 53
        fd.write(json.dumps((flags, branches)))  # line 53


class Tests(unittest.TestCase):  # line 56
    ''' Entire test suite. '''  # line 57

    def setUp(_):  # line 59
        for entry in os.listdir(testFolder):  # cannot remove testFolder on Windows when using TortoiseSVN as VCS  # line 60
            resource = os.path.join(testFolder, entry)  # line 61
            shutil.rmtree(resource) if os.path.isdir(resource) else os.unlink(resource)  # line 62
        os.chdir(testFolder)  # line 63

    def assertAllIn(_, what: '_coconut.typing.Sequence[str]', where: 'Union[str, List[str]]') -> 'None':  # line 65
        [_.assertIn(w, where) for w in what]  # line 65

    def assertInAll(_, what: 'str', where: '_coconut.typing.Sequence[str]') -> 'None':  # line 67
        [_.assertIn(what, w) for w in where]  # line 67

    def assertInAny(_, what: 'str', where: '_coconut.typing.Sequence[str]') -> 'None':  # line 69
        _.assertTrue(any((what in w for w in where)))  # line 69

    def assertNotInAny(_, what: 'str', where: '_coconut.typing.Sequence[str]') -> 'None':  # line 71
        _.assertFalse(any((what in w for w in where)))  # line 71

    def createFile(_, number: 'Union[int, str]', contents: 'str'="x" * 10, prefix: '_coconut.typing.Optional[str]'=None) -> 'None':  # line 73
        with open(("." if prefix is None else prefix) + os.sep + (("file%d" % number) if isinstance(number, int) else number), "wb") as fd:  # line 74
            fd.write(contents if isinstance(contents, bytes) else contents.encode("cp1252"))  # line 74

    def existsFile(_, number: 'Union[int, str]', expectedContents: 'bytes'=None) -> 'bool':  # line 76
        if not os.path.exists(("." + os.sep + "file%d" % number) if isinstance(number, int) else number):  # line 77
            return False  # line 77
        if expectedContents is None:  # line 78
            return True  # line 78
        with open(("." + os.sep + "file%d" % number) if isinstance(number, int) else number, "rb") as fd:  # line 79
            return fd.read() == expectedContents  # line 79

    def testAccessor(_):  # line 81
        a = sos.Accessor({"a": 1})  # line 82
        _.assertEqual((1, 1), (a["a"], a.a))  # line 83

    def testFirstofmap(_):  # line 85
        _.assertEqual(2, sos.firstOfMap({"a": 1, "b": 2}, ["x", "b"]))  # line 86
        _.assertIsNone(sos.firstOfMap({"a": 1, "b": 2}, []))  # line 87

    def testAjoin(_):  # line 89
        _.assertEqual("a1a2", sos.ajoin("a", ["1", "2"]))  # line 90
        _.assertEqual("* a\n* b", sos.ajoin("* ", ["a", "b"], "\n"))  # line 91

    def testFindChanges(_):  # line 93
        m = sos.Metadata(os.getcwd())  # line 94
        m.loadBranches()  # line 95
        _.createFile(1, "1")  # line 96
        m.createBranch(0)  # line 97
        _.assertEqual(1, len(m.paths))  # line 98
        time.sleep(1.1)  # time required by filesystem time resolution issues  # line 99
        _.createFile(1, "2")  # line 100
        _.createFile(2, "2")  # line 101
        changes = m.findChanges()  # detect time skew  # line 102
        _.assertEqual(1, len(changes.additions))  # line 103
        _.assertEqual(0, len(changes.deletions))  # line 104
        _.assertEqual(1, len(changes.modifications))  # line 105
        m.integrateChangeset(changes)  # line 106
        _.createFile(2, "12")  # modify file  # line 107
        changes = m.findChanges(0, 1)  # by size, creating new commit  # line 108
        _.assertEqual(0, len(changes.additions))  # line 109
        _.assertEqual(0, len(changes.deletions))  # line 110
        _.assertEqual(1, len(changes.modifications))  # line 111
        _.assertTrue(os.path.exists(branchFolder(0, 1)))  # line 112
        _.assertTrue(os.path.exists(branchFolder(0, 1) + os.sep + "03b69bc801ae11f1ff2a71a50f165996d0ad681b4f822df13329a27e53f0fcd2"))  # line 113

    def testDiffFunc(_):  # line 115
        a = {"./a": sos.PathInfo("", 0, 0, "")}  # line 116
        b = {"./a": sos.PathInfo("", 0, 0, "")}  # line 117
        changes = sos.diffPathSets(a, b)  # line 118
        _.assertEqual(0, len(changes.additions))  # line 119
        _.assertEqual(0, len(changes.deletions))  # line 120
        _.assertEqual(0, len(changes.modifications))  # line 121
        b = {"./a": sos.PathInfo("", 1, 0, "")}  # line 122
        changes = sos.diffPathSets(a, b)  # line 123
        _.assertEqual(0, len(changes.additions))  # line 124
        _.assertEqual(0, len(changes.deletions))  # line 125
        _.assertEqual(1, len(changes.modifications))  # line 126
        b = {}  # diff contains no entries -> no change  # line 127
        changes = sos.diffPathSets(a, b)  # line 128
        _.assertEqual(0, len(changes.additions))  # line 129
        _.assertEqual(0, len(changes.deletions))  # line 130
        _.assertEqual(0, len(changes.modifications))  # line 131
        b = {"./a": sos.PathInfo("", None, 1, "")}  # in diff marked as deleted  # line 132
        changes = sos.diffPathSets(a, b)  # line 133
        _.assertEqual(0, len(changes.additions))  # line 134
        _.assertEqual(1, len(changes.deletions))  # line 135
        _.assertEqual(0, len(changes.modifications))  # line 136
        b = {"./b": sos.PathInfo("", 1, 1, "")}  # line 137
        changes = sos.diffPathSets(a, b)  # line 138
        _.assertEqual(1, len(changes.additions))  # line 139
        _.assertEqual(0, len(changes.deletions))  # line 140
        _.assertEqual(0, len(changes.modifications))  # line 141
        a = {"./a": sos.PathInfo("", None, 0, "")}  # mark as deleted  # line 142
        b = {"./a": sos.PathInfo("", 1, 0, "")}  # re-added  # line 143
        changes = sos.diffPathSets(a, b)  # line 144
        _.assertEqual(1, len(changes.additions))  # line 145
        _.assertEqual(0, len(changes.deletions))  # line 146
        _.assertEqual(0, len(changes.modifications))  # line 147
        changes = sos.diffPathSets(b, a)  # line 148
        _.assertEqual(0, len(changes.additions))  # line 149
        _.assertEqual(1, len(changes.deletions))  # line 150
        _.assertEqual(0, len(changes.modifications))  # line 151

    def testPatternPaths(_):  # line 153
        sos.offline(options=["--track"])  # line 154
        os.mkdir("sub")  # line 155
        _.createFile("sub" + os.sep + "file1", "sdfsdf")  # line 156
        sos.add("./sub", "file?")  # this doesn't work as direct call won't invoke getRoot and therefore won't chdir virtually into that folder  # line 157
        sos.commit("test")  # line 158
        _.assertEqual(2, len(os.listdir(os.path.join(sos.metaFolder, "b0", "r1"))))  # sub/file1 was added  # line 159
        _.createFile(1)  # line 160
        try:  # should not commit anything, as the file in base folder doesn't match the path pattern  # line 161
            sos.commit("nothing")  # should not commit anything, as the file in base folder doesn't match the path pattern  # line 161
            _.fail()  # should not commit anything, as the file in base folder doesn't match the path pattern  # line 161
        except:  # line 162
            pass  # line 162

    def testComputeSequentialPathSet(_):  # line 164
        os.makedirs(branchFolder(0, 0))  # line 165
        os.makedirs(branchFolder(0, 1))  # line 166
        os.makedirs(branchFolder(0, 2))  # line 167
        os.makedirs(branchFolder(0, 3))  # line 168
        os.makedirs(branchFolder(0, 4))  # line 169
        m = sos.Metadata(os.getcwd())  # line 170
        m.branch = 0  # line 171
        m.commit = 2  # line 172
        m.saveBranches()  # line 173
        m.paths = {"./a": sos.PathInfo("", 0, 0, "")}  # line 174
        m.saveCommit(0, 0)  # initial  # line 175
        m.paths["./a"] = sos.PathInfo("", 1, 0, "")  # line 176
        m.saveCommit(0, 1)  # mod  # line 177
        m.paths["./b"] = sos.PathInfo("", 0, 0, "")  # line 178
        m.saveCommit(0, 2)  # add  # line 179
        m.paths["./a"] = sos.PathInfo("", None, 0, "")  # line 180
        m.saveCommit(0, 3)  # del  # line 181
        m.paths["./a"] = sos.PathInfo("", None, 0, "")  # line 182
        m.saveCommit(0, 4)  # readd  # line 183
        m.commits = {i: sos.CommitInfo(i, 0, None) for i in range(5)}  # line 184
        m.saveBranch(0)  # line 185
        m.computeSequentialPathSet(0, 4)  # line 186
        _.assertEqual(2, len(m.paths))  # line 187

    def testParseRevisionString(_):  # line 189
        m = sos.Metadata(os.getcwd())  # line 190
        m.branch = 1  # line 191
        m.commits = {0: 0, 1: 1, 2: 2}  # line 192
        _.assertEqual((1, 3), m.parseRevisionString("3"))  # line 193
        _.assertEqual((2, 3), m.parseRevisionString("2/3"))  # line 194
        _.assertEqual((1, -1), m.parseRevisionString(None))  # line 195
        _.assertEqual((2, -1), m.parseRevisionString("2/"))  # line 196
        _.assertEqual((1, -2), m.parseRevisionString("/-2"))  # line 197

    def testOfflineEmpty(_):  # line 199
        os.mkdir("." + os.sep + sos.metaFolder)  # line 200
        try:  # line 201
            sos.offline("trunk")  # line 201
            _.fail()  # line 201
        except SystemExit:  # line 202
            pass  # line 202
        os.rmdir("." + os.sep + sos.metaFolder)  # line 203
        sos.offline("test")  # line 204
        _.assertIn(sos.metaFolder, os.listdir("."))  # line 205
        _.assertAllIn(["b0", sos.metaFile], os.listdir("." + os.sep + sos.metaFolder))  # line 206
        _.assertAllIn(["r0", sos.metaFile], os.listdir("." + os.sep + sos.metaFolder + os.sep + "b0"))  # line 207
        _.assertEqual(2, len(os.listdir("." + os.sep + sos.metaFolder)))  # only branch folder and meta data file  # line 208
        _.assertEqual(2, len(os.listdir("." + os.sep + sos.metaFolder + os.sep + "b0")))  # only commit folder and meta data file  # line 209
        _.assertEqual(1, len(os.listdir(branchFolder(0, 0))))  # only meta data file  # line 210

    def testOfflineWithFiles(_):  # line 212
        _.createFile(1, "x" * 100)  # line 213
        _.createFile(2)  # line 214
        sos.offline("test")  # line 215
        _.assertAllIn(["file1", "file2", sos.metaFolder], os.listdir("."))  # line 216
        _.assertAllIn(["b0", sos.metaFile], os.listdir("." + os.sep + sos.metaFolder))  # line 217
        _.assertAllIn(["r0", sos.metaFile], os.listdir("." + os.sep + sos.metaFolder + os.sep + "b0"))  # line 218
        _.assertAllIn([sos.metaFile, "03b69bc801ae11f1ff2a71a50f165996d0ad681b4f822df13329a27e53f0fcd2", "b9ee10a87f612e299a6eb208210bc0898092a64c48091327cc2aaeee9b764ffa"], os.listdir("." + os.sep + sos.metaFolder + os.sep + "b0" + os.sep + "r0"))  # line 219
        _.assertEqual(2, len(os.listdir("." + os.sep + sos.metaFolder)))  # only branch folder and meta data file  # line 220
        _.assertEqual(2, len(os.listdir("." + os.sep + sos.metaFolder + os.sep + "b0")))  # only commit folder and meta data file  # line 221
        _.assertEqual(3, len(os.listdir(branchFolder(0, 0))))  # only meta data file plus branch base file copies  # line 222

    def testBranch(_):  # line 224
        _.createFile(1, "x" * 100)  # line 225
        _.createFile(2)  # line 226
        sos.offline("test")  # b0/r0  # line 227
        sos.branch("other")  # b1/r0  # line 228
        _.assertAllIn(["b0", "b1", sos.metaFile], os.listdir("." + os.sep + sos.metaFolder))  # line 229
        _.assertEqual(list(sorted(os.listdir("." + os.sep + sos.metaFolder + os.sep + "b0"))), list(sorted(os.listdir("." + os.sep + sos.metaFolder + os.sep + "b1"))))  # line 230
        _.assertEqual(list(sorted(os.listdir(branchFolder(0, 0)))), list(sorted(os.listdir(branchFolder(1, 0)))))  # line 232
        _.createFile(1, "z")  # modify file  # line 234
        sos.branch()  # b2/r0  branch to unnamed branch with modified file tree contents  # line 235
        _.assertNotEqual(os.stat("." + os.sep + sos.metaFolder + os.sep + "b1" + os.sep + "r0" + os.sep + "b9ee10a87f612e299a6eb208210bc0898092a64c48091327cc2aaeee9b764ffa").st_size, os.stat("." + os.sep + sos.metaFolder + os.sep + "b2" + os.sep + "r0" + os.sep + "b9ee10a87f612e299a6eb208210bc0898092a64c48091327cc2aaeee9b764ffa").st_size)  # line 236
        _.createFile(3, "z")  # line 238
        sos.branch("from_last_revision", ["--last", "--stay"])  # b3/r0 create copy of other file1,file2 and don't switch  # line 239
        _.assertEqual(list(sorted(os.listdir("." + os.sep + sos.metaFolder + os.sep + "b3" + os.sep + "r0"))), list(sorted(os.listdir("." + os.sep + sos.metaFolder + os.sep + "b2" + os.sep + "r0"))))  # line 240
# Check sos.status output which branch is marked


    def testComittingAndChanges(_):  # line 245
        _.createFile(1, "x" * 100)  # line 246
        _.createFile(2)  # line 247
        sos.offline("test")  # line 248
        changes = sos.changes()  # line 249
        _.assertEqual(0, len(changes.additions))  # line 250
        _.assertEqual(0, len(changes.deletions))  # line 251
        _.assertEqual(0, len(changes.modifications))  # line 252
        _.createFile(1, "z")  # line 253
        changes = sos.changes()  # line 254
        _.assertEqual(0, len(changes.additions))  # line 255
        _.assertEqual(0, len(changes.deletions))  # line 256
        _.assertEqual(1, len(changes.modifications))  # line 257
        sos.commit("message")  # line 258
        _.assertAllIn(["r0", "r1", sos.metaFile], os.listdir("." + os.sep + sos.metaFolder + os.sep + "b0"))  # line 259
        _.assertAllIn([sos.metaFile, "b9ee10a87f612e299a6eb208210bc0898092a64c48091327cc2aaeee9b764ffa"], os.listdir(branchFolder(0, 1)))  # line 260
        _.assertEqual(2, len(os.listdir(branchFolder(0, 1))))  # no further files, only the modified one  # line 261
        _.assertEqual(1, len(sos.changes("/0").modifications))  # vs. implicit (same) branch revision  # line 262
        _.assertEqual(1, len(sos.changes("0/0").modifications))  # vs. explicit branch revision  # line 263
        _.createFile(1, "")  # create empty file, mentioned in meta data, but not stored as own file  # line 264
        _.assertEqual(0, len(changes.additions))  # line 265
        _.assertEqual(0, len(changes.deletions))  # line 266
        _.assertEqual(1, len(changes.modifications))  # line 267
        sos.commit("modified")  # line 268
        _.assertEqual(1, len(os.listdir(branchFolder(0, 2))))  # no further files, only the modified one  # line 269
        try:  # expecting Exit due to no changes  # line 270
            sos.commit("nothing")  # expecting Exit due to no changes  # line 270
            _.fail()  # expecting Exit due to no changes  # line 270
        except:  # line 271
            pass  # line 271

    def testGetBranch(_):  # line 273
        m = sos.Metadata(os.getcwd())  # line 274
        m.branches = {0: sos.BranchInfo(0, 0, "trunk")}  # line 275
        _.assertEqual(27, m.getBranchByName(27))  # line 276
        _.assertEqual(0, m.getBranchByName("trunk"))  # line 277
        _.assertIsNone(m.getBranchByName("unknwon"))  # line 278

    def testSwitch(_):  # line 280
        _.createFile(1, "x" * 100)  # line 281
        _.createFile(2, "y")  # line 282
        sos.offline("test")  # file1-2  in initial branch commit  # line 283
        sos.branch("second")  # file1-2  switch, having same files  # line 284
        sos.switch("0")  # no change  switch back, no problem  # line 285
        sos.switch("second")  # no change  # switch back, no problem  # line 286
        _.createFile(3, "y")  # generate a file  # line 287
        try:  # uncommited changes detected  # line 288
            sos.switch("test")  # uncommited changes detected  # line 288
            _.fail()  # uncommited changes detected  # line 288
        except SystemExit:  # line 289
            pass  # line 289
        sos.commit("Finish")  # file1-3  commit third file into branch second  # line 290
        sos.changes()  # line 291
        sos.switch("test")  # file1-2, remove file3 from file tree  # line 292
        _.assertFalse(_.existsFile(3))  # removed when switching back to test  # line 293
        out = wrapChannels(lambda: sos.status()).replace("\r", "")  # line 294
        _.assertIn("  * b00   'test'", out)  # line 295
        _.assertIn("    b01 'second'", out)  # line 296
        _.assertIn("(dirty)", out)  # one branch has commits  # line 297
        _.assertIn("(in sync)", out)  # the other doesn't  # line 298
        _.createFile(4, "xy")  # generate a file  # line 299
        sos.switch("second", "--force")  # avoids warning on uncommited changes, but keeps file4  # line 300
        _.assertFalse(_.existsFile(4))  # removed when forcedly switching back to test  # line 301
        _.assertTrue(_.existsFile(3))  # was restored from branch's revision r1  # line 302
        os.unlink("." + os.sep + "file1")  # remove old file1  # line 303
        sos.switch("test", "--force")  # should restore file1 and remove file3  # line 304
        _.assertTrue(_.existsFile(1))  # was restored from branch's revision r1  # line 305
        _.assertFalse(_.existsFile(3))  # was restored from branch's revision r1  # line 306

    def testAutoDetectVCS(_):  # line 308
        os.mkdir(".git")  # line 309
        sos.offline(sos.vcsBranches[sos.findSosVcsBase()[2]])  # create initial branch  # line 310
        with open(sos.metaFolder + os.sep + sos.metaFile, "r") as fd:  # line 311
            meta = fd.read()  # line 311
        _.assertTrue("\"master\"" in meta)  # line 312
        os.rmdir(".git")  # line 313

    def testUpdate(_):  # line 315
        sos.offline("trunk")  # create initial branch b0/r0  # line 316
        _.createFile(1, "x" * 100)  # line 317
        sos.commit("second")  # create b0/r1  # line 318

        sos.switch("/0")  # go back to b0/r0 - deletes file1  # line 320
        _.assertFalse(_.existsFile(1))  # line 321

        sos.update("/1")  # recreate file1  # line 323
        _.assertTrue(_.existsFile(1))  # line 324

        sos.commit("third", ["--force"])  # force because nothing to commit. should create r2 with same contents as r1, but as differential from r1, not from r0 (= no changes in meta folder)  # line 326
        _.assertTrue(os.path.exists(branchFolder(0, 2)))  # line 327
        _.assertTrue(os.path.exists(branchFolder(0, 2) + os.sep + sos.metaFile))  # line 328
        _.assertEqual(1, len(os.listdir(branchFolder(0, 2))))  # only meta data file, no differential files  # line 329

        sos.update("/1")  # do nothing, as nothing has changed  # line 331
        _.assertTrue(_.existsFile(1))  # line 332

        _.createFile(2, "y" * 100)  # line 334
#    out = wrapChannels(() -> sos.branch("other"))  # won't comply as there are changes
#    _.assertIn("--force", out)
        sos.branch("other", ["--force"])  # automatically including file 2 (as we are in simple mode)  # line 337
        _.assertTrue(_.existsFile(2))  # line 338
        sos.update("trunk", ["--add"])  # only add stuff  # line 339
        _.assertTrue(_.existsFile(2))  # line 340
        sos.update("trunk")  # nothing to do  # line 341
        _.assertFalse(_.existsFile(2))  # removes file not present in original branch  # line 342

        theirs = b"a\nb\nc\nd\ne\nf\ng\nh\nx\nx\nj\nk"  # line 344
        _.createFile(10, theirs)  # line 345
        mine = b"a\nc\nd\ne\ng\nf\nx\nh\ny\ny\nj"  # missing "b", inserted g, modified g->x, replace x/x -> y/y, removed k  # line 346
        _.createFile(11, mine)  # line 347
        _.assertEqual(b"a\nb\nc\nd\ne\nf\ng\nh\nx\nx\nj\nk", sos.merge(filename="." + os.sep + "file10", intoname="." + os.sep + "file11", mergeOperation=sos.MergeOperation.BOTH, conflictResolution=sos.ConflictResolution.THEIRS))  # completely recreated other file  # line 348
        _.assertEqual(b"a\nb\nc\nd\ne\ng\nf\ng\nx\nh\nx\nx\ny\ny\nj\nk", sos.merge(filename="." + os.sep + "file10", intoname="." + os.sep + "file11", mergeOperation=sos.MergeOperation.INSERT, conflictResolution=sos.ConflictResolution.MINE))  # line 349

    def testUpdate2(_):  # line 351
        _.createFile("test.txt", "x" * 10)  # line 352
        sos.offline("trunk", ["--strict"])  # use strict mode, as timestamp differences are too small for testing  # line 353
        sos.branch("mod")  # line 354
        _.createFile("test.txt", "x" * 5 + "y" * 5)  # line 355
        time.sleep(1.1)  # line 356
        sos.commit("mod")  # create b0/r1  # line 357
        sos.switch("trunk", ["--force"])  # should replace contents, force in case some other files were modified (e.g. during working on the code) TODO investigate more  # line 358
        with open("test.txt", "rb") as fd:  # line 359
            _.assertEqual(b"x" * 10, fd.read())  # line 359
        sos.update("mod", ["--theirs"])  # integrate changes TODO same with ask -> theirs  # line 360
        with open("test.txt", "rb") as fd:  # line 361
            _.assertEqual(b"x" * 5 + b"y" * 5, fd.read())  # line 361
        _.createFile("test.txt", "x" * 10)  # line 362
        mockInput(["t"], lambda: sos.update("mod", ["--ask"]))  # same as above with interaction -> theirs  # line 363
        with open("test.txt", "rb") as fd:  # line 364
            _.assertEqual(b"x" * 5 + b"y" * 5, fd.read())  # line 364

    def testIsTextType(_):  # line 366
        m = sos.Metadata(".")  # line 367
        m.c.texttype = ["*.x", "*.md", "*.md.*"]  # line 368
        m.c.bintype = ["*.md.confluence"]  # line 369
        _.assertTrue(m.isTextType("ab.txt"))  # line 370
        _.assertTrue(m.isTextType("./ab.txt"))  # line 371
        _.assertTrue(m.isTextType("bc/ab.txt"))  # line 372
        _.assertFalse(m.isTextType("bc/ab."))  # line 373
        _.assertTrue(m.isTextType("23_3.x.x"))  # line 374
        _.assertTrue(m.isTextType("dfg/dfglkjdf7/test.md"))  # line 375
        _.assertTrue(m.isTextType("./test.md.pdf"))  # line 376
        _.assertFalse(m.isTextType("./test_a.md.confluence"))  # line 377

    def testEolDet(_):  # line 379
        _.assertEqual(b"\n", sos.eoldet(b"a\nb"))  # line 380
        _.assertEqual(b"\r\n", sos.eoldet(b"a\r\nb\r\n"))  # line 381
        _.assertEqual(b"\r", sos.eoldet(b"\ra\rb"))  # line 382
        _.assertAllIn(["Inconsistent", "with "], wrapChannels(lambda: _.assertEqual(b"\n", sos.eoldet(b"\r\na\r\nb\n"))))  # line 383
        _.assertAllIn(["Inconsistent", "without"], wrapChannels(lambda: _.assertEqual(b"\n", sos.eoldet(b"\ra\nnb\n"))))  # line 384
        _.assertIsNone(sos.eoldet(b""))  # line 385
        _.assertIsNone(sos.eoldet(b"sdf"))  # line 386

    def testMerge(_):  # line 388
        a = b"a\nb\ncc\nd"  # line 389
        b = b"a\nb\nee\nd"  # line 390
        _.assertEqual(b"a\nb\ncc\nee\nd", sos.merge(a, b, mergeOperation=sos.MergeOperation.INSERT))  # means insert changes from a into b, but don't replace  # line 391
        _.assertEqual(b"a\nb\nd", sos.merge(a, b, mergeOperation=sos.MergeOperation.REMOVE))  # line 392
        _.assertEqual(b"a\nb\ncc\nd", sos.merge(a, b, mergeOperation=sos.MergeOperation.BOTH))  # line 393
# Now test intra-line merging without conflicts
        _.assertEqual(b"a\nbc d\ne", sos.merge(b"a\nbc d\ne", b"a\nbcd\ne", mergeOperation=sos.MergeOperation.INSERT))  # because it's a deletion ['  a', '- bc d', '?   -\n', '+ bcd', '  e']  # line 395
        _.assertEqual(b"a\nbcd\ne", sos.merge(b"a\nbc d\ne", b"a\nbcd\ne", mergeOperation=sos.MergeOperation.REMOVE))  # ['  a', '- bc d', '?   -\n', '+ bcd', '  e']  # line 396
        _.assertEqual(b"a\nbc d\ne", sos.merge(b"a\nbcd\ne", b"a\nbc d\ne", mergeOperation=sos.MergeOperation.INSERT))  # nothing to insert  # line 397
        _.assertEqual(b"a\nbcd\ne", sos.merge(b"a\nbcd\ne", b"a\nbc d\ne", mergeOperation=sos.MergeOperation.REMOVE))  # remove space  # line 398
# Test with change + insert (conflict)
        _.assertEqual(b"a\nb fdd d\ne", sos.merge(b"a\nb cd d\ne", b"a\nb fdd d\ne", conflictResolution=sos.ConflictResolution.MINE))  # line 400
        _.assertEqual(b"a\nb cd d\ne", sos.merge(b"a\nb cd d\ne", b"a\nb fdd d\ne", conflictResolution=sos.ConflictResolution.THEIRS))  # ['  a', '- b cd d', '?   ^\n', '+ b fdd d', '?   ^^\n', '  e']  # line 401
        _.assertEqual(b"a\nb fdd d\ne", mockInput(["i"], lambda: sos.merge(b"a\nb cd d\ne", b"a\nb fdd d\ne", conflictResolution=sos.ConflictResolution.ASK)))  # ['  a', '- b cd d', '?   ^\n', '+ b fdd d', '?   ^^\n', '  e']  # line 402
        _.assertEqual(b"a\nb cd d\ne", mockInput(["t"], lambda: sos.merge(b"a\nb cd d\ne", b"a\nb fdd d\ne", conflictResolution=sos.ConflictResolution.ASK)))  # ['  a', '- b cd d', '?   ^\n', '+ b fdd d', '?   ^^\n', '  e']  # line 403
        _.assertEqual(b"abbc", sos.merge(b"abbc", b"addc", mergeOperation=sos.MergeOperation.BOTH, conflictResolution=sos.ConflictResolution.THEIRS))  # line 404
        _.assertEqual(b"a\nbb\nc", sos.merge(b"a\nbb\nc", b"a\ndd\nc", mergeOperation=sos.MergeOperation.BOTH, conflictResolution=sos.ConflictResolution.THEIRS))  # line 405
        _.assertIn("Differing EOL-styles", wrapChannels(lambda: sos.merge(b"a\nb", b"a\r\nb")))  # expect warning  # line 406
        _.assertIn(b"a\r\nb", sos.merge(b"a\nb", b"a\r\nb"))  # in doubt, use "mine" CR-LF  # line 407

    def testPickyMode(_):  # line 409
        sos.offline("trunk", ["--picky"])  # line 410
        sos.add(".", "file?", ["--force"])  # line 411
        _.createFile(1, "aa")  # line 412
        sos.commit("First")  # add one file  # line 413
        _.assertEqual(2, len(os.listdir(branchFolder(0, 1))))  # line 414
        _.createFile(2, "b")  # line 415
        sos.commit("Second", ["--force"])  # add nothing, because picky  # line 416
        _.assertEqual(1, len(os.listdir(branchFolder(0, 2))))  # line 417
        sos.add(".", "file?")  # line 418
        sos.commit("Third")  # add nothing, because picky  # line 419
        _.assertEqual(2, len(os.listdir(branchFolder(0, 3))))  # line 420
        out = wrapChannels(lambda: sos.log()).replace("\r", "")  # line 421
        _.assertIn("    r2", out)  # line 422
        _.assertIn("  * r3", out)  # line 423
        _.assertNotIn("  * r4", out)  # line 424

    def testTrackedSubfolder(_):  # line 426
        os.mkdir("." + os.sep + "sub")  # line 427
        sos.offline("trunk", ["--track"])  # line 428
        _.createFile(1, "x")  # line 429
        _.createFile(1, "x", prefix="sub")  # line 430
        sos.add(".", "file?")  # add glob pattern to track  # line 431
        sos.commit("First")  # line 432
        _.assertEqual(2, len(os.listdir(branchFolder(0, 1))))  # one new file + meta file  # line 433
        sos.add(".", "sub/file?")  # add glob pattern to track  # line 434
        sos.commit("Second")  # one new file + meta  # line 435
        _.assertEqual(2, len(os.listdir(branchFolder(0, 1))))  # one new file + meta file  # line 436
        os.unlink("file1")  # remove from basefolder  # line 437
        _.createFile(2, "y")  # line 438
        sos.rm(".", "sub/file?")  # line 439
        try:  # raises Exit. TODO test the "suggest a pattern" case  # line 440
            sos.rm(".", "sub/bla")  # raises Exit. TODO test the "suggest a pattern" case  # line 440
            _.fail()  # raises Exit. TODO test the "suggest a pattern" case  # line 440
        except:  # line 441
            pass  # line 441
        sos.commit("Third")  # line 442
        _.assertEqual(2, len(os.listdir(branchFolder(0, 2))))  # one new file + meta  # line 443
# TODO check if /file1 and sub/file1 were removed from index

    def testTrackedMode(_):  # line 446
        ''' Difference in semantics vs simple mode:
          - For remote/other branch we can only know and consider tracked files, thus ignoring all complexity stemming from handling addition of untracked files.
          - For current branch, we can take into account tracked and untracked ones, in theory, but it doesn't make sense.
        In conclusion, using the union of tracking patterns from both sides to find affected files makes sense, but disallow deleting files not present in remote branch.
    '''  # line 451
        sos.offline("test", options=["--track"])  # set up repo in tracking mode (SVN- or gitless-style)  # line 452
        _.createFile(1)  # line 453
        _.createFile("a123a")  # untracked file "a123a"  # line 454
        sos.add(".", "file?")  # add glob tracking pattern  # line 455
        sos.commit("second")  # versions "file1"  # line 456
        _.assertEqual(2, len(os.listdir(branchFolder(0, 1))))  # one new file + meta file  # line 457
        out = wrapChannels(lambda: sos.status()).replace("\r", "")  # line 458
        _.assertIn("  | ./file?", out)  # line 459

        _.createFile(2)  # untracked file "file2"  # line 461
        sos.commit("third")  # versions "file2"  # line 462
        _.assertEqual(2, len(os.listdir(branchFolder(0, 2))))  # one new file + meta file  # line 463

        os.mkdir("." + os.sep + "sub")  # line 465
        _.createFile(3, prefix="sub")  # untracked file "sub/file3"  # line 466
        sos.commit("fourth", ["--force"])  # no tracking pattern matches the subfolder  # line 467
        _.assertEqual(1, len(os.listdir(branchFolder(0, 3))))  # meta file only, no other tracked path/file  # line 468

        sos.branch("Other")  # second branch containing file1 and file2 tracked by "./file?"  # line 470
        sos.rm(".", "file?")  # remove tracking pattern, but don't touch previously created and versioned files  # line 471
        sos.add(".", "a*a")  # add tracking pattern  # line 472
        changes = sos.changes()  # should pick up addition  # line 473
        _.assertEqual(0, len(changes.modifications))  # line 474
        _.assertEqual(0, len(changes.deletions))  # not tracked anymore, but contained in version history and not removed  # line 475
        _.assertEqual(1, len(changes.additions))  # detected one addition "a123a", but won't recognize untracking files as deletion  # line 476

        sos.commit("Second_2")  # line 478
        _.assertEqual(2, len(os.listdir(branchFolder(1, 1))))  # "a123a" + meta file  # line 479
        _.assertTrue(os.path.exists("." + os.sep + "file1"))  # line 480
        _.assertTrue(os.path.exists("." + os.sep + "file2"))  # line 481

        sos.switch("test")  # go back to first branch - tracks only "file?", but not "a*a"  # line 483
        _.assertTrue(os.path.exists("." + os.sep + "file1"))  # line 484
        _.assertTrue(os.path.exists("." + os.sep + "a123a"))  # should not have been touched so far  # line 485

        sos.update("Other")  # integrate tracked files and tracking pattern from second branch into working state of master branch  # line 487
        _.assertTrue(os.path.exists("." + os.sep + "file1"))  # line 488
        _.assertTrue(os.path.exists("." + os.sep + "a123a"))  # line 489

        _.createFile("axxxa")  # new file that should be tracked on "test" now that we integrated "Other"  # line 491
        sos.commit("fifth")  # create new revision after integrating updates from second branch  # line 492
        _.assertEqual(3, len(os.listdir(branchFolder(0, 4))))  # one new file from other branch + one new in current folder + meta file  # line 493
        sos.switch("Other")  # switch back to just integrated branch that tracks only "a*a" - shouldn't do anything  # line 494
        _.assertTrue(os.path.exists("." + os.sep + "file1"))  # line 495
        _.assertTrue(os.path.exists("." + os.sep + "a123a"))  # line 496
        _.assertFalse(os.path.exists("." + os.sep + "axxxa"))  # because tracked in both branches, but not present in other -> delete in file tree TODO document  # line 497
# TODO test switch --meta

    def testLsTracked(_):  # line 500
        sos.offline("test", options=["--track"])  # set up repo in tracking mode (SVN- or gitless-style)  # line 501
        _.createFile(1)  # line 502
        _.createFile("foo")  # line 503
        sos.add(".", "file*")  # capture one file  # line 504
        out = sos.safeSplit(wrapChannels(lambda: sos.ls()).replace("\r", ""), "\n")  # line 505
        _.assertInAny('TRK file1 by "./file*"', out)  # line 506
        _.assertNotInAny('    file1 by "./file*"', out)  # line 507
        _.assertInAny("    foo", out)  # line 508

    def testCompression(_):  # line 510
        _.createFile(1)  # line 511
        sos.offline("master", options=["--plain", "--force"])  # line 512
        _.assertTrue(_.existsFile(branchFolder(0, 0) + os.sep + "b9ee10a87f612e299a6eb208210bc0898092a64c48091327cc2aaeee9b764ffa", b"x" * 10))  # line 513
        setRepoFlag("compress", True)  # was plain = uncompressed before  # line 514
        _.createFile(2)  # line 515
        sos.commit("Added file2")  # line 516
        _.assertTrue(_.existsFile(branchFolder(0, 1) + os.sep + "03b69bc801ae11f1ff2a71a50f165996d0ad681b4f822df13329a27e53f0fcd2"))  # exists  # line 517
        _.assertFalse(_.existsFile(branchFolder(0, 1) + os.sep + "03b69bc801ae11f1ff2a71a50f165996d0ad681b4f822df13329a27e53f0fcd2", b"x" * 10))  # but is compressed instead  # line 518

    def testConfigVariations(_):  # line 520
        def checkRepoState(flag: 'bool') -> 'bool':  # line 521
            with open(sos.metaFolder + os.sep + sos.metaFile, "rb") as fd:  # line 521
                contents = fd.read()  # type: bytes  # line 522
            return b'"strict": ' in contents and (b'"strict": ' + (b"true" if flag else b"false")) in contents  # line 523
        def makeRepo():  # line 524
            sos.offline("master", options=["--plain", "--force"])  # line 525
            _.createFile(1)  # line 526
            sos.commit("Added file1")  # line 527
        sos.config("set", ["strict", "on"])  # line 528
        makeRepo()  # line 529
        _.assertTrue(checkRepoState(True))  # line 530
        sos.config("set", ["strict", "off"])  # line 531
        makeRepo()  # line 532
        _.assertTrue(checkRepoState(False))  # line 533
        sos.config("set", ["strict", "yes"])  # line 534
        makeRepo()  # line 535
        _.assertTrue(checkRepoState(True))  # line 536
        sos.config("set", ["strict", "no"])  # line 537
        makeRepo()  # line 538
        _.assertTrue(checkRepoState(False))  # line 539
        sos.config("set", ["strict", "1"])  # line 540
        makeRepo()  # line 541
        _.assertTrue(checkRepoState(True))  # line 542
        sos.config("set", ["strict", "0"])  # line 543
        makeRepo()  # line 544
        _.assertTrue(checkRepoState(False))  # line 545
        sos.config("set", ["strict", "true"])  # line 546
        makeRepo()  # line 547
        _.assertTrue(checkRepoState(True))  # line 548
        sos.config("set", ["strict", "false"])  # line 549
        makeRepo()  # line 550
        _.assertTrue(checkRepoState(False))  # line 551
        sos.config("set", ["strict", "enable"])  # line 552
        makeRepo()  # line 553
        _.assertTrue(checkRepoState(True))  # line 554
        sos.config("set", ["strict", "disable"])  # line 555
        makeRepo()  # line 556
        _.assertTrue(checkRepoState(False))  # line 557
        sos.config("set", ["strict", "enabled"])  # line 558
        makeRepo()  # line 559
        _.assertTrue(checkRepoState(True))  # line 560
        sos.config("set", ["strict", "disabled"])  # line 561
        makeRepo()  # line 562
        _.assertTrue(checkRepoState(False))  # line 563
        try:  # line 564
            sos.config("set", ["strict", "nope"])  # line 564
            _.fail()  # line 564
        except:  # line 565
            pass  # line 565

    def testLsSimple(_):  # line 567
        _.createFile(1)  # line 568
        _.createFile("foo")  # line 569
        _.createFile("ign1")  # line 570
        _.createFile("ign2")  # line 571
        sos.offline("test")  # set up repo in tracking mode (SVN- or gitless-style)  # line 572
        sos.config("set", ["ignores", "ign1"])  # define an ignore pattern  # line 573
        sos.config("add", ["ignores", "ign2"])  # define an ignore pattern  # line 574
        sos.config("set", ["ignoresWhitelist", "ign1;ign2"])  # define a list of ignore patterns  # line 575
        out = wrapChannels(lambda: sos.config("show")).replace("\r", "")  # line 576
        _.assertIn("ignores => ['ign1', 'ign2']", out)  # line 577
        out = sos.safeSplit(wrapChannels(lambda: sos.ls()).replace("\r", ""), "\n")  # line 578
        _.assertInAny('    file1', out)  # line 579
        _.assertInAny('    ign1', out)  # line 580
        _.assertInAny('    ign2', out)  # line 581
        try:  # line 582
            sos.config("rm", ["foo", "bar"])  # line 582
            _.fail()  # line 582
        except:  # line 583
            pass  # line 583
        try:  # line 584
            sos.config("rm", ["ignores", "foo"])  # line 584
            _.fail()  # line 584
        except:  # line 585
            pass  # line 585
        sos.config("rm", ["ignores", "ign1"])  # line 586
        sos.config("unset", ["ignoresWhitelist"])  # remove ignore pattern  # line 587
        out = sos.safeSplit(wrapChannels(lambda: sos.ls()).replace("\r", ""), "\n")  # line 588
        _.assertInAny('    ign1', out)  # line 589
        _.assertInAny('IGN ign2', out)  # line 590
        _.assertNotInAny('    ign2', out)  # line 591

    def testWhitelist(_):  # line 593
# TODO test same for simple mode
        _.createFile(1)  # line 595
        sos.defaults.ignores[:] = ["file*"]  # replace in-place  # line 596
        sos.offline("xx", ["--track", "--strict"])  # because nothing to commit due to ignore pattern  # line 597
        sos.add(".", "file*")  # add tracking pattern for "file1"  # line 598
        sos.commit(options=["--force"])  # attempt to commit the file  # line 599
        _.assertEqual(1, len(os.listdir(branchFolder(0, 1))))  # only meta data, file1 was ignored  # line 600
        try:  # Exit because dirty  # line 601
            sos.online()  # Exit because dirty  # line 601
            _.fail()  # Exit because dirty  # line 601
        except:  # exception expected  # line 602
            pass  # exception expected  # line 602
        _.createFile("x2")  # add another change  # line 603
        sos.add(".", "x?")  # add tracking pattern for "file1"  # line 604
        try:  # force beyond dirty flag check  # line 605
            sos.online(["--force"])  # force beyond dirty flag check  # line 605
            _.fail()  # force beyond dirty flag check  # line 605
        except:  # line 606
            pass  # line 606
        sos.online(["--force", "--force"])  # force beyond file tree modifications check  # line 607
        _.assertFalse(os.path.exists(sos.metaFolder))  # line 608

        _.createFile(1)  # line 610
        sos.defaults.ignoresWhitelist[:] = ["file*"]  # line 611
        sos.offline("xx", ["--track"])  # line 612
        sos.add(".", "file*")  # line 613
        sos.commit()  # should NOT ask for force here  # line 614
        _.assertEqual(2, len(os.listdir(branchFolder(0, 1))))  # meta data and "file1", file1 was whitelisted  # line 615

    def testRemove(_):  # line 617
        _.createFile(1, "x" * 100)  # line 618
        sos.offline("trunk")  # line 619
        try:  # line 620
            sos.delete("trunk")  # line 620
            _fail()  # line 620
        except:  # line 621
            pass  # line 621
        _.createFile(2, "y" * 10)  # line 622
        sos.branch("added")  # line 623
        sos.delete("trunk")  # line 624
        _.assertEqual(2, len(os.listdir("." + os.sep + sos.metaFolder)))  # meta data file and "b1"  # line 625
        _.assertTrue(os.path.exists("." + os.sep + sos.metaFolder + os.sep + "b1"))  # line 626
        _.assertFalse(os.path.exists("." + os.sep + sos.metaFolder + os.sep + "b0"))  # line 627
        sos.branch("next")  # line 628
        _.createFile(3, "y" * 10)  # make a change  # line 629
        sos.delete("added", "--force")  # should succeed  # line 630

    def testUsage(_):  # line 632
        sos.usage()  # line 633

    def testDiff(_):  # line 635
        sos.offline(options=["--strict"])  # line 636
        _.createFile(1)  # line 637
        sos.commit()  # line 638
        _.createFile(1, "sdfsdgfsdf")  # line 639
        time.sleep(1.1)  # line 640
        sos.commit()  # TODO this sometimes fails "nothing to commit"  # line 641
        _.createFile(1, "foobar")  # line 642
        _.assertAllIn(["MOD ./file1", "DIF ./file1", "- | 0000 |xxxxxxxxxx|", "+ | 0000 |foobar|"], wrapChannels(lambda: sos.diff("/-2")))  # second last  # line 643

    def testFindBase(_):  # line 645
        old = os.getcwd()  # line 646
        try:  # line 647
            os.mkdir("." + os.sep + ".git")  # line 648
            os.makedirs("." + os.sep + "a" + os.sep + sos.metaFolder)  # line 649
            os.makedirs("." + os.sep + "a" + os.sep + "b")  # line 650
            os.chdir("a" + os.sep + "b")  # line 651
            s, vcs, cmd = sos.findSosVcsBase()  # line 652
            _.assertIsNotNone(s)  # line 653
            _.assertIsNotNone(vcs)  # line 654
            _.assertEqual("git", cmd)  # line 655
        finally:  # line 656
            os.chdir(old)  # line 656


if __name__ == '__main__':  # line 659
    logging.basicConfig(level=logging.DEBUG if '-v' in sys.argv or os.getenv("DEBUG", "false").strip().lower() == "true" or os.getenv("CI", "false").strip().lower() == "true" else logging.INFO, stream=sys.stderr, format="%(asctime)-23s %(levelname)-8s %(name)s:%(lineno)d | %(message)s" if '-v' in sys.argv or os.getenv("DEBUG", "false") == "true" else "%(message)s")  # line 660
    if configr:  # line 661
        c = configr.Configr("sos")  # line 662
        c.loadSettings()  # line 662
        if len(c.keys()) > 0:  # line 663
            sos.Exit("Cannot run test suite with existing local SOS user configuration (would affect results)")  # line 663
    unittest.main(testRunner=debugTestRunner() if '-v' in sys.argv and not os.getenv("BUILD", "false").lower() == "true" else None)  # warnings = "ignore")  # line 664
