#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# __coconut_hash__ = 0xf30d3b65

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


class Tests(unittest.TestCase):  # line 51
    ''' Entire test suite. '''  # line 52

    def setUp(_):  # line 54
        for entry in os.listdir(testFolder):  # cannot remove testFolder on Windows when using TortoiseSVN as VCS  # line 55
            resource = os.path.join(testFolder, entry)  # line 56
            try:  # line 57
                os.unlink(resource)  # line 57
            except:  # line 58
                shutil.rmtree(resource)  # line 58
        os.chdir(testFolder)  # line 59

    def tearDown(_):  # line 61
        pass  # line 61

    def assertAllIn(_, what: '_coconut.typing.Sequence[str]', where: 'Union[str, List[str]]') -> 'None':  # line 63
        [_.assertIn(w, where) for w in what]  # line 63

    def assertInAll(_, what: 'str', where: '_coconut.typing.Sequence[str]') -> 'None':  # line 65
        [_.assertIn(what, w) for w in where]  # line 65

    def assertInAny(_, what: 'str', where: '_coconut.typing.Sequence[str]') -> 'None':  # line 67
        _.assertTrue(any((what in w for w in where)))  # line 67

    def assertNotInAny(_, what: 'str', where: '_coconut.typing.Sequence[str]') -> 'None':  # line 69
        _.assertFalse(any((what in w for w in where)))  # line 69

    def createFile(_, number: 'Union[int, str]', contents: 'str'="x" * 10, prefix: '_coconut.typing.Optional[str]'=None) -> 'None':  # line 71
        with open(("." if prefix is None else prefix) + os.sep + (("file%d" % number) if isinstance(number, int) else number), "wb") as fd:  # line 72
            fd.write(contents if isinstance(contents, bytes) else contents.encode("cp1252"))  # line 72

    def existsFile(_, number: 'int', expectedContents: 'str'=None) -> 'bool':  # line 74
        if not os.path.exists("." + os.sep + "file%d" % number):  # line 75
            return False  # line 75
        if expectedContents is None:  # line 76
            return True  # line 76
        with open("." + os.sep + "file%d" % number, "wb") as fd:  # line 77
            return fd.read() == expectedContents  # line 77

    def testAccessor(_):  # line 79
        a = sos.Accessor({"a": 1})  # line 80
        _.assertEqual((1, 1), (a["a"], a.a))  # line 81

    def testFirstofmap(_):  # line 83
        _.assertEqual(2, sos.firstOfMap({"a": 1, "b": 2}, ["x", "b"]))  # line 84
        _.assertIsNone(sos.firstOfMap({"a": 1, "b": 2}, []))  # line 85

    def testAjoin(_):  # line 87
        _.assertEqual("a1a2", sos.ajoin("a", ["1", "2"]))  # line 88
        _.assertEqual("* a\n* b", sos.ajoin("* ", ["a", "b"], "\n"))  # line 89

    def testFindChanges(_):  # line 91
        m = sos.Metadata(os.getcwd())  # line 92
        m.loadBranches()  # line 93
        _.createFile(1, "1")  # line 94
        m.createBranch(0)  # line 95
        _.assertEqual(1, len(m.paths))  # line 96
        time.sleep(1.1)  # time required by filesystem time resolution issues  # line 97
        _.createFile(1, "2")  # line 98
        _.createFile(2, "2")  # line 99
        changes = m.findChanges()  # detect time skew  # line 100
        _.assertEqual(1, len(changes.additions))  # line 101
        _.assertEqual(0, len(changes.deletions))  # line 102
        _.assertEqual(1, len(changes.modifications))  # line 103
        m.integrateChangeset(changes)  # line 104
        _.createFile(2, "12")  # modify file  # line 105
        changes = m.findChanges(0, 1)  # by size, creating new commit  # line 106
        _.assertEqual(0, len(changes.additions))  # line 107
        _.assertEqual(0, len(changes.deletions))  # line 108
        _.assertEqual(1, len(changes.modifications))  # line 109
        _.assertTrue(os.path.exists(branchFolder(0, 1)))  # line 110
        _.assertTrue(os.path.exists(branchFolder(0, 1) + os.sep + "03b69bc801ae11f1ff2a71a50f165996d0ad681b4f822df13329a27e53f0fcd2"))  # line 111

    def testDiffFunc(_):  # line 113
        a = {"./a": sos.PathInfo("", 0, 0, "")}  # line 114
        b = {"./a": sos.PathInfo("", 0, 0, "")}  # line 115
        changes = sos.diffPathSets(a, b)  # line 116
        _.assertEqual(0, len(changes.additions))  # line 117
        _.assertEqual(0, len(changes.deletions))  # line 118
        _.assertEqual(0, len(changes.modifications))  # line 119
        b = {"./a": sos.PathInfo("", 1, 0, "")}  # line 120
        changes = sos.diffPathSets(a, b)  # line 121
        _.assertEqual(0, len(changes.additions))  # line 122
        _.assertEqual(0, len(changes.deletions))  # line 123
        _.assertEqual(1, len(changes.modifications))  # line 124
        b = {}  # diff contains no entries -> no change  # line 125
        changes = sos.diffPathSets(a, b)  # line 126
        _.assertEqual(0, len(changes.additions))  # line 127
        _.assertEqual(0, len(changes.deletions))  # line 128
        _.assertEqual(0, len(changes.modifications))  # line 129
        b = {"./a": sos.PathInfo("", None, 1, "")}  # in diff marked as deleted  # line 130
        changes = sos.diffPathSets(a, b)  # line 131
        _.assertEqual(0, len(changes.additions))  # line 132
        _.assertEqual(1, len(changes.deletions))  # line 133
        _.assertEqual(0, len(changes.modifications))  # line 134
        b = {"./b": sos.PathInfo("", 1, 1, "")}  # line 135
        changes = sos.diffPathSets(a, b)  # line 136
        _.assertEqual(1, len(changes.additions))  # line 137
        _.assertEqual(0, len(changes.deletions))  # line 138
        _.assertEqual(0, len(changes.modifications))  # line 139
        a = {"./a": sos.PathInfo("", None, 0, "")}  # mark as deleted  # line 140
        b = {"./a": sos.PathInfo("", 1, 0, "")}  # re-added  # line 141
        changes = sos.diffPathSets(a, b)  # line 142
        _.assertEqual(1, len(changes.additions))  # line 143
        _.assertEqual(0, len(changes.deletions))  # line 144
        _.assertEqual(0, len(changes.modifications))  # line 145
        changes = sos.diffPathSets(b, a)  # line 146
        _.assertEqual(0, len(changes.additions))  # line 147
        _.assertEqual(1, len(changes.deletions))  # line 148
        _.assertEqual(0, len(changes.modifications))  # line 149

    def testPatternPaths(_):  # line 151
        sos.offline(options=["--track"])  # line 152
        os.mkdir("sub")  # line 153
        _.createFile("sub" + os.sep + "file1", "sdfsdf")  # line 154
        sos.add("./sub", "file?")  # this doesn't work as direct call won't invoke getRoot and therefore won't chdir virtually into that folder  # line 155
        sos.commit("test")  # line 156
        _.assertEqual(2, len(os.listdir(os.path.join(sos.metaFolder, "b0", "r1"))))  # sub/file1 was added  # line 157
        _.createFile(1)  # line 158
        try:  # should not commit anything, as the file in base folder doesn't match the path pattern  # line 159
            sos.commit("nothing")  # should not commit anything, as the file in base folder doesn't match the path pattern  # line 159
            _.fail()  # should not commit anything, as the file in base folder doesn't match the path pattern  # line 159
        except:  # line 160
            pass  # line 160

    def testComputeSequentialPathSet(_):  # line 162
        os.makedirs(branchFolder(0, 0))  # line 163
        os.makedirs(branchFolder(0, 1))  # line 164
        os.makedirs(branchFolder(0, 2))  # line 165
        os.makedirs(branchFolder(0, 3))  # line 166
        os.makedirs(branchFolder(0, 4))  # line 167
        m = sos.Metadata(os.getcwd())  # line 168
        m.branch = 0  # line 169
        m.commit = 2  # line 170
        m.saveBranches()  # line 171
        m.paths = {"./a": sos.PathInfo("", 0, 0, "")}  # line 172
        m.saveCommit(0, 0)  # initial  # line 173
        m.paths["./a"] = sos.PathInfo("", 1, 0, "")  # line 174
        m.saveCommit(0, 1)  # mod  # line 175
        m.paths["./b"] = sos.PathInfo("", 0, 0, "")  # line 176
        m.saveCommit(0, 2)  # add  # line 177
        m.paths["./a"] = sos.PathInfo("", None, 0, "")  # line 178
        m.saveCommit(0, 3)  # del  # line 179
        m.paths["./a"] = sos.PathInfo("", None, 0, "")  # line 180
        m.saveCommit(0, 4)  # readd  # line 181
        m.commits = {i: sos.CommitInfo(i, 0, None) for i in range(5)}  # line 182
        m.saveBranch(0)  # line 183
        m.computeSequentialPathSet(0, 4)  # line 184
        _.assertEqual(2, len(m.paths))  # line 185

    def testParseRevisionString(_):  # line 187
        m = sos.Metadata(os.getcwd())  # line 188
        m.branch = 1  # line 189
        m.commits = {0: 0, 1: 1, 2: 2}  # line 190
        _.assertEqual((1, 3), m.parseRevisionString("3"))  # line 191
        _.assertEqual((2, 3), m.parseRevisionString("2/3"))  # line 192
        _.assertEqual((1, -1), m.parseRevisionString(None))  # line 193
        _.assertEqual((2, -1), m.parseRevisionString("2/"))  # line 194
        _.assertEqual((1, -2), m.parseRevisionString("/-2"))  # line 195

    def testOfflineEmpty(_):  # line 197
        os.mkdir("." + os.sep + sos.metaFolder)  # line 198
        try:  # line 199
            sos.offline("trunk")  # line 199
            _.fail()  # line 199
        except SystemExit:  # line 200
            pass  # line 200
        os.rmdir("." + os.sep + sos.metaFolder)  # line 201
        sos.offline("test")  # line 202
        _.assertIn(sos.metaFolder, os.listdir("."))  # line 203
        _.assertAllIn(["b0", sos.metaFile], os.listdir("." + os.sep + sos.metaFolder))  # line 204
        _.assertAllIn(["r0", sos.metaFile], os.listdir("." + os.sep + sos.metaFolder + os.sep + "b0"))  # line 205
        _.assertEqual(2, len(os.listdir("." + os.sep + sos.metaFolder)))  # only branch folder and meta data file  # line 206
        _.assertEqual(2, len(os.listdir("." + os.sep + sos.metaFolder + os.sep + "b0")))  # only commit folder and meta data file  # line 207
        _.assertEqual(1, len(os.listdir(branchFolder(0, 0))))  # only meta data file  # line 208

    def testOfflineWithFiles(_):  # line 210
        _.createFile(1, "x" * 100)  # line 211
        _.createFile(2)  # line 212
        sos.offline("test")  # line 213
        _.assertAllIn(["file1", "file2", sos.metaFolder], os.listdir("."))  # line 214
        _.assertAllIn(["b0", sos.metaFile], os.listdir("." + os.sep + sos.metaFolder))  # line 215
        _.assertAllIn(["r0", sos.metaFile], os.listdir("." + os.sep + sos.metaFolder + os.sep + "b0"))  # line 216
        _.assertAllIn([sos.metaFile, "03b69bc801ae11f1ff2a71a50f165996d0ad681b4f822df13329a27e53f0fcd2", "b9ee10a87f612e299a6eb208210bc0898092a64c48091327cc2aaeee9b764ffa"], os.listdir("." + os.sep + sos.metaFolder + os.sep + "b0" + os.sep + "r0"))  # line 217
        _.assertEqual(2, len(os.listdir("." + os.sep + sos.metaFolder)))  # only branch folder and meta data file  # line 218
        _.assertEqual(2, len(os.listdir("." + os.sep + sos.metaFolder + os.sep + "b0")))  # only commit folder and meta data file  # line 219
        _.assertEqual(3, len(os.listdir(branchFolder(0, 0))))  # only meta data file plus branch base file copies  # line 220

    def testBranch(_):  # line 222
        _.createFile(1, "x" * 100)  # line 223
        _.createFile(2)  # line 224
        sos.offline("test")  # b0/r0  # line 225
        sos.branch("other")  # b1/r0  # line 226
        _.assertAllIn(["b0", "b1", sos.metaFile], os.listdir("." + os.sep + sos.metaFolder))  # line 227
        _.assertEqual(list(sorted(os.listdir("." + os.sep + sos.metaFolder + os.sep + "b0"))), list(sorted(os.listdir("." + os.sep + sos.metaFolder + os.sep + "b1"))))  # line 228
        _.assertEqual(list(sorted(os.listdir(branchFolder(0, 0)))), list(sorted(os.listdir(branchFolder(1, 0)))))  # line 230
        _.createFile(1, "z")  # modify file  # line 232
        sos.branch()  # b2/r0  branch to unnamed branch with modified file tree contents  # line 233
        _.assertNotEqual(os.stat("." + os.sep + sos.metaFolder + os.sep + "b1" + os.sep + "r0" + os.sep + "b9ee10a87f612e299a6eb208210bc0898092a64c48091327cc2aaeee9b764ffa").st_size, os.stat("." + os.sep + sos.metaFolder + os.sep + "b2" + os.sep + "r0" + os.sep + "b9ee10a87f612e299a6eb208210bc0898092a64c48091327cc2aaeee9b764ffa").st_size)  # line 234
        _.createFile(3, "z")  # line 236
        sos.branch("from_last_revision", ["--last", "--stay"])  # b3/r0 create copy of other file1,file2 and don't switch  # line 237
        _.assertEqual(list(sorted(os.listdir("." + os.sep + sos.metaFolder + os.sep + "b3" + os.sep + "r0"))), list(sorted(os.listdir("." + os.sep + sos.metaFolder + os.sep + "b2" + os.sep + "r0"))))  # line 238
# Check sos.status output which branch is marked


    def testComittingAndChanges(_):  # line 243
        _.createFile(1, "x" * 100)  # line 244
        _.createFile(2)  # line 245
        sos.offline("test")  # line 246
        changes = sos.changes()  # line 247
        _.assertEqual(0, len(changes.additions))  # line 248
        _.assertEqual(0, len(changes.deletions))  # line 249
        _.assertEqual(0, len(changes.modifications))  # line 250
        _.createFile(1, "z")  # line 251
        changes = sos.changes()  # line 252
        _.assertEqual(0, len(changes.additions))  # line 253
        _.assertEqual(0, len(changes.deletions))  # line 254
        _.assertEqual(1, len(changes.modifications))  # line 255
        sos.commit("message")  # line 256
        _.assertAllIn(["r0", "r1", sos.metaFile], os.listdir("." + os.sep + sos.metaFolder + os.sep + "b0"))  # line 257
        _.assertAllIn([sos.metaFile, "b9ee10a87f612e299a6eb208210bc0898092a64c48091327cc2aaeee9b764ffa"], os.listdir(branchFolder(0, 1)))  # line 258
        _.assertEqual(2, len(os.listdir(branchFolder(0, 1))))  # no further files, only the modified one  # line 259
        _.assertEqual(1, len(sos.changes("/0").modifications))  # vs. implicit (same) branch revision  # line 260
        _.assertEqual(1, len(sos.changes("0/0").modifications))  # vs. explicit branch revision  # line 261
        _.createFile(1, "")  # create empty file, mentioned in meta data, but not stored as own file  # line 262
        _.assertEqual(0, len(changes.additions))  # line 263
        _.assertEqual(0, len(changes.deletions))  # line 264
        _.assertEqual(1, len(changes.modifications))  # line 265
        sos.commit("modified")  # line 266
        _.assertEqual(1, len(os.listdir(branchFolder(0, 2))))  # no further files, only the modified one  # line 267
        try:  # expecting Exit due to no changes  # line 268
            sos.commit("nothing")  # expecting Exit due to no changes  # line 268
            _.fail()  # expecting Exit due to no changes  # line 268
        except:  # line 269
            pass  # line 269

    def testSwitch(_):  # line 271
        _.createFile(1, "x" * 100)  # line 272
        _.createFile(2, "y")  # line 273
        sos.offline("test")  # file1-2  in initial branch commit  # line 274
        sos.branch("second")  # file1-2  switch, having same files  # line 275
        sos.switch("0")  # no change  switch back, no problem  # line 276
        sos.switch("second")  # no change  # switch back, no problem  # line 277
        _.createFile(3, "y")  # generate a file  # line 278
        try:  # uncommited changes detected  # line 279
            sos.switch("test")  # uncommited changes detected  # line 279
            _.fail()  # uncommited changes detected  # line 279
        except SystemExit:  # line 280
            pass  # line 280
        sos.commit("Finish")  # file1-3  commit third file into branch second  # line 281
        sos.changes()  # line 282
        sos.switch("test")  # file1-2, remove file3 from file tree  # line 283
        _.assertFalse(_.existsFile(3))  # removed when switching back to test  # line 284
        out = wrapChannels(lambda: sos.status()).replace("\r", "")  # line 285
        _.assertIn("  * b0   'test'", out)  # TODO dirty/insync  # line 286
        _.assertIn("    b1 'second'", out)  # TODO dirty/insync  # line 287
        _.createFile(4, "xy")  # generate a file  # line 288
        sos.switch("second", "--force")  # avoids warning on uncommited changes, but keeps file4  # line 289
        _.assertFalse(_.existsFile(4))  # removed when forcedly switching back to test  # line 290
        _.assertTrue(_.existsFile(3))  # was restored from branch's revision r1  # line 291
        os.unlink("." + os.sep + "file1")  # remove old file1  # line 292
        sos.switch("test", "--force")  # should restore file1 and remove file3  # line 293
        _.assertTrue(_.existsFile(1))  # was restored from branch's revision r1  # line 294
        _.assertFalse(_.existsFile(3))  # was restored from branch's revision r1  # line 295

    def testAutoDetectVCS(_):  # line 297
        os.mkdir(".git")  # line 298
        sos.offline(sos.vcsBranches[sos.findSosVcsBase()[2]])  # create initial branch  # line 299
        with open(sos.metaFolder + os.sep + sos.metaFile, "r") as fd:  # line 300
            meta = fd.read()  # line 300
        _.assertTrue("\"master\"" in meta)  # line 301
        os.rmdir(".git")  # line 302

    def testUpdate(_):  # line 304
        sos.offline("trunk")  # create initial branch b0/r0  # line 305
        _.createFile(1, "x" * 100)  # line 306
        sos.commit("second")  # create b0/r1  # line 307

        sos.switch("/0")  # go back to b0/r0 - deletes file1  # line 309
        _.assertFalse(_.existsFile(1))  # line 310

        sos.update("/1")  # recreate file1  # line 312
        _.assertTrue(_.existsFile(1))  # line 313

        sos.commit("third", ["--force"])  # force because nothing to commit. should create r2 with same contents as r1, but as differential from r1, not from r0 (= no changes in meta folder)  # line 315
        _.assertTrue(os.path.exists(branchFolder(0, 2)))  # line 316
        _.assertTrue(os.path.exists(branchFolder(0, 2) + os.sep + sos.metaFile))  # line 317
        _.assertEqual(1, len(os.listdir(branchFolder(0, 2))))  # only meta data file, no differential files  # line 318

        sos.update("/1")  # do nothing, as nothing has changed  # line 320
        _.assertTrue(_.existsFile(1))  # line 321

        _.createFile(2, "y" * 100)  # line 323
#    out = wrapChannels(() -> sos.branch("other"))  # won't comply as there are changes
#    _.assertIn("--force", out)
        sos.branch("other", ["--force"])  # automatically including file 2 (as we are in simple mode)  # line 326
        _.assertTrue(_.existsFile(2))  # line 327
        sos.update("trunk", ["--add"])  # only add stuff  # line 328
        _.assertTrue(_.existsFile(2))  # line 329
        sos.update("trunk")  # nothing to do  # line 330
        _.assertFalse(_.existsFile(2))  # removes file not present in original branch  # line 331

        theirs = b"a\nb\nc\nd\ne\nf\ng\nh\nx\nx\nj\nk"  # line 333
        _.createFile(10, theirs)  # line 334
        mine = b"a\nc\nd\ne\ng\nf\nx\nh\ny\ny\nj"  # missing "b", inserted g, modified g->x, replace x/x -> y/y, removed k  # line 335
        _.createFile(11, mine)  # line 336
        _.assertEqual(b"a\nb\nc\nd\ne\nf\ng\nh\nx\nx\nj\nk", sos.merge(filename="." + os.sep + "file10", intoname="." + os.sep + "file11", mergeOperation=sos.MergeOperation.BOTH, conflictResolution=sos.ConflictResolution.THEIRS))  # completely recreated other file  # line 337
        _.assertEqual(b"a\nb\nc\nd\ne\ng\nf\ng\nx\nh\nx\nx\ny\ny\nj\nk", sos.merge(filename="." + os.sep + "file10", intoname="." + os.sep + "file11", mergeOperation=sos.MergeOperation.INSERT, conflictResolution=sos.ConflictResolution.MINE))  # line 338

    def testUpdate2(_):  # line 340
        _.createFile("test.txt", "x" * 10)  # line 341
        sos.offline("trunk", ["--strict"])  # use strict mode, as timestamp differences are too small for testing  # line 342
        sos.branch("mod")  # line 343
        _.createFile("test.txt", "x" * 5 + "y" * 5)  # line 344
        time.sleep(1.1)  # line 345
        sos.commit("mod")  # create b0/r1  # line 346
        sos.switch("trunk", ["--force"])  # should replace contents, force in case some other files were modified (e.g. during working on the code) TODO investigate more  # line 347
        with open("test.txt", "rb") as fd:  # line 348
            _.assertEqual(b"x" * 10, fd.read())  # line 348
        sos.update("mod", ["--theirs"])  # integrate changes TODO same with ask -> theirs  # line 349
        with open("test.txt", "rb") as fd:  # line 350
            _.assertEqual(b"x" * 5 + b"y" * 5, fd.read())  # line 350
        _.createFile("test.txt", "x" * 10)  # line 351
        mockInput(["t"], lambda: sos.update("mod", ["--ask"]))  # same as above with interaction -> theirs  # line 352
        with open("test.txt", "rb") as fd:  # line 353
            _.assertEqual(b"x" * 5 + b"y" * 5, fd.read())  # line 353

    def testEolDet(_):  # line 355
        _.assertEqual(b"\n", sos.eoldet(b"a\nb"))  # line 356
        _.assertEqual(b"\r\n", sos.eoldet(b"a\r\nb\r\n"))  # line 357
        _.assertEqual(b"\r", sos.eoldet(b"\ra\rb"))  # line 358
        _.assertAllIn(["Inconsistent", "with "], wrapChannels(lambda: _.assertEqual(b"\n", sos.eoldet(b"\r\na\r\nb\n"))))  # line 359
        _.assertAllIn(["Inconsistent", "without"], wrapChannels(lambda: _.assertEqual(b"\n", sos.eoldet(b"\ra\nnb\n"))))  # line 360
        _.assertIsNone(sos.eoldet(b""))  # line 361
        _.assertIsNone(sos.eoldet(b"sdf"))  # line 362

    def testMerge(_):  # line 364
        a = b"a\nb\ncc\nd"  # line 365
        b = b"a\nb\nee\nd"  # line 366
        _.assertEqual(b"a\nb\ncc\nee\nd", sos.merge(a, b, mergeOperation=sos.MergeOperation.INSERT))  # means insert changes from a into b, but don't replace  # line 367
        _.assertEqual(b"a\nb\nd", sos.merge(a, b, mergeOperation=sos.MergeOperation.REMOVE))  # line 368
        _.assertEqual(b"a\nb\ncc\nd", sos.merge(a, b, mergeOperation=sos.MergeOperation.BOTH))  # line 369
# Now test intra-line merging without conflicts
        _.assertEqual(b"a\nbc d\ne", sos.merge(b"a\nbc d\ne", b"a\nbcd\ne", mergeOperation=sos.MergeOperation.INSERT))  # because it's a deletion ['  a', '- bc d', '?   -\n', '+ bcd', '  e']  # line 371
        _.assertEqual(b"a\nbcd\ne", sos.merge(b"a\nbc d\ne", b"a\nbcd\ne", mergeOperation=sos.MergeOperation.REMOVE))  # ['  a', '- bc d', '?   -\n', '+ bcd', '  e']  # line 372
        _.assertEqual(b"a\nbc d\ne", sos.merge(b"a\nbcd\ne", b"a\nbc d\ne", mergeOperation=sos.MergeOperation.INSERT))  # nothing to insert  # line 373
        _.assertEqual(b"a\nbcd\ne", sos.merge(b"a\nbcd\ne", b"a\nbc d\ne", mergeOperation=sos.MergeOperation.REMOVE))  # remove space  # line 374
# Test with change + insert (conflict)
        _.assertEqual(b"a\nb fdd d\ne", sos.merge(b"a\nb cd d\ne", b"a\nb fdd d\ne", conflictResolution=sos.ConflictResolution.MINE))  # line 376
        _.assertEqual(b"a\nb cd d\ne", sos.merge(b"a\nb cd d\ne", b"a\nb fdd d\ne", conflictResolution=sos.ConflictResolution.THEIRS))  # ['  a', '- b cd d', '?   ^\n', '+ b fdd d', '?   ^^\n', '  e']  # line 377
        _.assertEqual(b"a\nb fdd d\ne", mockInput(["i"], lambda: sos.merge(b"a\nb cd d\ne", b"a\nb fdd d\ne", conflictResolution=sos.ConflictResolution.ASK)))  # ['  a', '- b cd d', '?   ^\n', '+ b fdd d', '?   ^^\n', '  e']  # line 378
        _.assertEqual(b"a\nb cd d\ne", mockInput(["t"], lambda: sos.merge(b"a\nb cd d\ne", b"a\nb fdd d\ne", conflictResolution=sos.ConflictResolution.ASK)))  # ['  a', '- b cd d', '?   ^\n', '+ b fdd d', '?   ^^\n', '  e']  # line 379
        _.assertEqual(b"abbc", sos.merge(b"abbc", b"addc", mergeOperation=sos.MergeOperation.BOTH, conflictResolution=sos.ConflictResolution.THEIRS))  # line 380
        _.assertEqual(b"a\nbb\nc", sos.merge(b"a\nbb\nc", b"a\ndd\nc", mergeOperation=sos.MergeOperation.BOTH, conflictResolution=sos.ConflictResolution.THEIRS))  # line 381
        _.assertIn("Differing EOL-styles", wrapChannels(lambda: sos.merge(b"a\nb", b"a\r\nb")))  # expect warning  # line 382
        _.assertIn(b"a\r\nb", sos.merge(b"a\nb", b"a\r\nb"))  # in doubt, use "mine" CR-LF  # line 383

    def testPickyMode(_):  # line 385
        sos.offline("trunk", ["--picky"])  # line 386
        sos.add(".", "file?", ["--force"])  # line 387
        _.createFile(1, "aa")  # line 388
        sos.commit("First")  # add one file  # line 389
        _.assertEqual(2, len(os.listdir(branchFolder(0, 1))))  # line 390
        _.createFile(2, "b")  # line 391
        sos.commit("Second", ["--force"])  # add nothing, because picky  # line 392
        _.assertEqual(1, len(os.listdir(branchFolder(0, 2))))  # line 393
        sos.add(".", "file?")  # line 394
        sos.commit("Third")  # add nothing, because picky  # line 395
        _.assertEqual(2, len(os.listdir(branchFolder(0, 3))))  # line 396
        out = wrapChannels(lambda: sos.log()).replace("\r", "")  # line 397
        _.assertIn("    r2", out)  # line 398
        _.assertIn("  * r3", out)  # line 399
        _.assertNotIn("  * r4", out)  # line 400

    def testTrackedSubfolder(_):  # line 402
        os.mkdir("." + os.sep + "sub")  # line 403
        sos.offline("trunk", ["--track"])  # line 404
        _.createFile(1, "x")  # line 405
        _.createFile(1, "x", prefix="sub")  # line 406
        sos.add(".", "file?")  # add glob pattern to track  # line 407
        sos.commit("First")  # line 408
        _.assertEqual(2, len(os.listdir(branchFolder(0, 1))))  # one new file + meta file  # line 409
        sos.add(".", "sub/file?")  # add glob pattern to track  # line 410
        sos.commit("Second")  # one new file + meta  # line 411
        _.assertEqual(2, len(os.listdir(branchFolder(0, 1))))  # one new file + meta file  # line 412
        os.unlink("file1")  # remove from basefolder  # line 413
        _.createFile(2, "y")  # line 414
        sos.rm(".", "sub/file?")  # line 415
        try:  # raises Exit. TODO test the "suggest a pattern" case  # line 416
            sos.rm(".", "sub/bla")  # raises Exit. TODO test the "suggest a pattern" case  # line 416
            _.fail()  # raises Exit. TODO test the "suggest a pattern" case  # line 416
        except:  # line 417
            pass  # line 417
        sos.commit("Third")  # line 418
        _.assertEqual(2, len(os.listdir(branchFolder(0, 2))))  # one new file + meta  # line 419
# TODO check if /file1 and sub/file1 were removed from index

    def testTrackedMode(_):  # line 422
        ''' Difference in semantics vs simple mode:
          - For remote/other branch we can only know and consider tracked files, thus ignoring all complexity stemming from handling addition of untracked files.
          - For current branch, we can take into account tracked and untracked ones, in theory, but it doesn't make sense.
        In conclusion, using the union of tracking patterns from both sides to find affected files makes sense, but disallow deleting files not present in remote branch.
    '''  # line 427
        sos.offline("test", options=["--track"])  # set up repo in tracking mode (SVN- or gitless-style)  # line 428
        _.createFile(1)  # line 429
        _.createFile("a123a")  # untracked file "a123a"  # line 430
        sos.add(".", "file?")  # add glob tracking pattern  # line 431
        sos.commit("second")  # versions "file1"  # line 432
        _.assertEqual(2, len(os.listdir(branchFolder(0, 1))))  # one new file + meta file  # line 433
        out = wrapChannels(lambda: sos.status()).replace("\r", "")  # line 434
        _.assertIn("  | ./file?", out)  # line 435

        _.createFile(2)  # untracked file "file2"  # line 437
        sos.commit("third")  # versions "file2"  # line 438
        _.assertEqual(2, len(os.listdir(branchFolder(0, 2))))  # one new file + meta file  # line 439

        os.mkdir("." + os.sep + "sub")  # line 441
        _.createFile(3, prefix="sub")  # untracked file "sub/file3"  # line 442
        sos.commit("fourth", ["--force"])  # no tracking pattern matches the subfolder  # line 443
        _.assertEqual(1, len(os.listdir(branchFolder(0, 3))))  # meta file only, no other tracked path/file  # line 444

        sos.branch("Other")  # second branch containing file1 and file2 tracked by "./file?"  # line 446
        sos.rm(".", "file?")  # remove tracking pattern, but don't touch previously created and versioned files  # line 447
        sos.add(".", "a*a")  # add tracking pattern  # line 448
        changes = sos.changes()  # should pick up addition  # line 449
        _.assertEqual(0, len(changes.modifications))  # line 450
        _.assertEqual(0, len(changes.deletions))  # not tracked anymore, but contained in version history and not removed  # line 451
        _.assertEqual(1, len(changes.additions))  # detected one addition "a123a", but won't recognize untracking files as deletion  # line 452

        sos.commit("Second_2")  # line 454
        _.assertEqual(2, len(os.listdir(branchFolder(1, 1))))  # "a123a" + meta file  # line 455
        _.assertTrue(os.path.exists("." + os.sep + "file1"))  # line 456
        _.assertTrue(os.path.exists("." + os.sep + "file2"))  # line 457

        sos.switch("test")  # go back to first branch - tracks only "file?", but not "a*a"  # line 459
        _.assertTrue(os.path.exists("." + os.sep + "file1"))  # line 460
        _.assertTrue(os.path.exists("." + os.sep + "a123a"))  # should not have been touched so far  # line 461

        sos.update("Other")  # integrate tracked files and tracking pattern from second branch into working state of master branch  # line 463
        _.assertTrue(os.path.exists("." + os.sep + "file1"))  # line 464
        _.assertTrue(os.path.exists("." + os.sep + "a123a"))  # line 465

        _.createFile("axxxa")  # new file that should be tracked on "test" now that we integrated "Other"  # line 467
        sos.commit("fifth")  # create new revision after integrating updates from second branch  # line 468
        _.assertEqual(3, len(os.listdir(branchFolder(0, 4))))  # one new file from other branch + one new in current folder + meta file  # line 469
        sos.switch("Other")  # switch back to just integrated branch that tracks only "a*a" - shouldn't do anything  # line 470
        _.assertTrue(os.path.exists("." + os.sep + "file1"))  # line 471
        _.assertTrue(os.path.exists("." + os.sep + "a123a"))  # line 472
        _.assertFalse(os.path.exists("." + os.sep + "axxxa"))  # because tracked in both branches, but not present in other -> delete in file tree TODO document  # line 473
# TODO test switch --meta

    def testLsTracked(_):  # line 476
        sos.offline("test", options=["--track"])  # set up repo in tracking mode (SVN- or gitless-style)  # line 477
        _.createFile(1)  # line 478
        _.createFile("foo")  # line 479
        sos.add(".", "file*")  # capture one file  # line 480
        out = sos.safeSplit(wrapChannels(lambda: sos.ls()).replace("\r", ""), "\n")  # line 481
        _.assertInAny('TRK file1 by "./file*"', out)  # line 482
        _.assertNotInAny('    file1 by "./file*"', out)  # line 483
        _.assertInAny("    foo", out)  # line 484

    def testLsSimple(_):  # line 486
        _.createFile(1)  # line 487
        _.createFile("foo")  # line 488
        _.createFile("ign1")  # line 489
        _.createFile("ign2")  # line 490
        sos.offline("test")  # set up repo in tracking mode (SVN- or gitless-style)  # line 491
        sos.config("set", ["ignores", "ign1"])  # define an ignore pattern  # line 492
        sos.config("add", ["ignores", "ign2"])  # define an ignore pattern  # line 493
        sos.config("set", ["ignoresWhitelist", "ign1;ign2"])  # define a list of ignore patterns  # line 494
        out = wrapChannels(lambda: sos.config("show")).replace("\r", "")  # line 495
        _.assertIn("ignores => ['ign1', 'ign2']", out)  # line 496
        out = sos.safeSplit(wrapChannels(lambda: sos.ls()).replace("\r", ""), "\n")  # line 497
        _.assertInAny('    file1', out)  # line 498
        _.assertInAny('    ign1', out)  # line 499
        _.assertInAny('    ign2', out)  # line 500
        try:  # line 501
            sos.config("rm", ["foo", "bar"])  # line 501
            _.fail()  # line 501
        except:  # line 502
            pass  # line 502
        try:  # line 503
            sos.config("rm", ["ignores", "foo"])  # line 503
            _.fail()  # line 503
        except:  # line 504
            pass  # line 504
        sos.config("rm", ["ignores", "ign1"])  # line 505
        sos.config("unset", ["ignoresWhitelist"])  # remove ignore pattern  # line 506
        out = sos.safeSplit(wrapChannels(lambda: sos.ls()).replace("\r", ""), "\n")  # line 507
        _.assertInAny('    ign1', out)  # line 508
        _.assertInAny('IGN ign2', out)  # line 509
        _.assertNotInAny('    ign2', out)  # line 510

    def testWhitelist(_):  # line 512
# TODO test same for simple mode
        _.createFile(1)  # line 514
        sos.defaults.ignores[:] = ["file*"]  # replace in-place  # line 515
        sos.offline("xx", ["--track", "--strict"])  # because nothing to commit due to ignore pattern  # line 516
        sos.add(".", "file*")  # add tracking pattern for "file1"  # line 517
        sos.commit(options=["--force"])  # attempt to commit the file  # line 518
        _.assertEqual(1, len(os.listdir(branchFolder(0, 1))))  # only meta data, file1 was ignored  # line 519
        try:  # Exit because dirty  # line 520
            sos.online()  # Exit because dirty  # line 520
            _.fail()  # Exit because dirty  # line 520
        except:  # exception expected  # line 521
            pass  # exception expected  # line 521
        _.createFile("x2")  # add another change  # line 522
        sos.add(".", "x?")  # add tracking pattern for "file1"  # line 523
        try:  # force beyond dirty flag check  # line 524
            sos.online(["--force"])  # force beyond dirty flag check  # line 524
            _.fail()  # force beyond dirty flag check  # line 524
        except:  # line 525
            pass  # line 525
        sos.online(["--force", "--force"])  # force beyond file tree modifications check  # line 526
        _.assertFalse(os.path.exists(sos.metaFolder))  # line 527

        _.createFile(1)  # line 529
        sos.defaults.ignoresWhitelist[:] = ["file*"]  # line 530
        sos.offline("xx", ["--track"])  # line 531
        sos.add(".", "file*")  # line 532
        sos.commit()  # should NOT ask for force here  # line 533
        _.assertEqual(2, len(os.listdir(branchFolder(0, 1))))  # meta data and "file1", file1 was whitelisted  # line 534

    def testRemove(_):  # line 536
        _.createFile(1, "x" * 100)  # line 537
        sos.offline("trunk")  # line 538
        try:  # line 539
            sos.delete("trunk")  # line 539
            _fail()  # line 539
        except:  # line 540
            pass  # line 540
        _.createFile(2, "y" * 10)  # line 541
        sos.branch("added")  # line 542
        sos.delete("trunk")  # line 543
        _.assertEqual(2, len(os.listdir("." + os.sep + sos.metaFolder)))  # meta data file and "b1"  # line 544
        _.assertTrue(os.path.exists("." + os.sep + sos.metaFolder + os.sep + "b1"))  # line 545
        _.assertFalse(os.path.exists("." + os.sep + sos.metaFolder + os.sep + "b0"))  # line 546
        sos.branch("next")  # line 547
        _.createFile(3, "y" * 10)  # make a change  # line 548
        sos.delete("added", "--force")  # should succeed  # line 549

    def testUsage(_):  # line 551
        sos.usage()  # line 552

    def testDiff(_):  # line 554
        sos.offline(options=["--strict"])  # line 555
        _.createFile(1)  # line 556
        sos.commit()  # line 557
        _.createFile(1, "sdfsdgfsdf")  # line 558
        time.sleep(1.1)  # line 559
        sos.commit()  # TODO this sometimes fails "nothing to commit"  # line 560
        _.createFile(1, "foobar")  # line 561
        _.assertAllIn(["MOD ./file1", "DIF ./file1", "- | 0000 |xxxxxxxxxx|", "+ | 0000 |foobar|"], wrapChannels(lambda: sos.diff("/-2")))  # second last  # line 562

    def testFindBase(_):  # line 564
        old = os.getcwd()  # line 565
        try:  # line 566
            os.mkdir("." + os.sep + ".git")  # line 567
            os.makedirs("." + os.sep + "a" + os.sep + sos.metaFolder)  # line 568
            os.makedirs("." + os.sep + "a" + os.sep + "b")  # line 569
            os.chdir("a" + os.sep + "b")  # line 570
            s, vcs, cmd = sos.findSosVcsBase()  # line 571
            _.assertIsNotNone(s)  # line 572
            _.assertIsNotNone(vcs)  # line 573
            _.assertEqual("git", cmd)  # line 574
        finally:  # line 575
            os.chdir(old)  # line 575


if __name__ == '__main__':  # line 578
    logging.basicConfig(level=logging.DEBUG if '-v' in sys.argv or os.getenv("DEBUG", "false").strip().lower() == "true" or os.getenv("CI", "false").strip().lower() == "true" else logging.INFO, stream=sys.stderr, format="%(asctime)-23s %(levelname)-8s %(name)s:%(lineno)d | %(message)s" if '-v' in sys.argv or os.getenv("DEBUG", "false") == "true" else "%(message)s")  # line 579
    if configr:  # line 580
        c = configr.Configr("sos")  # line 581
        c.loadSettings()  # line 581
        if len(c.keys()) > 0:  # line 582
            sos.Exit("Cannot run test suite with existing local SOS user configuration (would affect results)")  # line 582
    unittest.main(testRunner=debugTestRunner() if '-v' in sys.argv and not os.getenv("BUILD", "false").lower() == "true" else None)  # warnings = "ignore")  # line 583
