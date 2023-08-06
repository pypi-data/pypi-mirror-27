#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# __coconut_hash__ = 0xa9a0f024

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

    while os.stat(name)[8] == mt:  # wait until timestamp modified  # line 25
        with open(name, "w") as fd:  # line 26
            fd.write("x")  # line 26
    mt, start, count = os.stat(name)[8], time.time(), 0  # line 27
    while os.stat(name)[8] == mt:  # now cound and measure time until modified again  # line 28
        count += 1  # line 29
        with open(name, "w") as fd:  # line 30
            fd.write("x")  # line 30
    os.unlink(name)  # line 31
    fsprecision = round(time.time() - start, 2)  # line 32
    print("File system timestamp precision is %.2fs; wrote to the file %d times during that time" % (fsprecision, count))  # line 33
    return fsprecision  # line 34


FS_PRECISION = determineFilesystemTimeResolution() * 1.05  # line 37


@_coconut_tco  # line 40
def debugTestRunner(post_mortem=None):  # line 40
    ''' Unittest runner doing post mortem debugging on failing tests. '''  # line 41
    import pdb  # line 42
    if post_mortem is None:  # line 43
        post_mortem = pdb.post_mortem  # line 43
    class DebugTestResult(unittest.TextTestResult):  # line 44
        def addError(self, test, err):  # called before tearDown()  # line 45
            traceback.print_exception(*err)  # line 46
            post_mortem(err[2])  # line 47
            super(DebugTestResult, self).addError(test, err)  # line 48
        def addFailure(self, test, err):  # line 49
            traceback.print_exception(*err)  # line 50
            post_mortem(err[2])  # line 51
            super(DebugTestResult, self).addFailure(test, err)  # line 52
    return _coconut_tail_call(unittest.TextTestRunner, resultclass=DebugTestResult)  # line 53

def branchFolder(branch: 'int', revision: 'int') -> 'str':  # line 55
    return "." + os.sep + sos.metaFolder + os.sep + "b%d" % branch + os.sep + "r%d" % revision  # line 55

@_coconut_tco  # line 57
def wrapChannels(func: '_coconut.typing.Callable[..., Any]'):  # line 57
    ''' Wrap function call to capture and return strings emitted on stdout and stderr. '''  # line 58
    oldv, oldo, olde = sys.argv, sys.stdout, sys.stderr  # line 59
    buf = StringIO()  # line 60
    sys.stdout = sys.stderr = buf  # line 61
    handler = logging.StreamHandler(buf)  # line 62
    logging.getLogger().addHandler(handler)  # line 63
    try:  # capture output into buf  # line 64
        func()  # capture output into buf  # line 64
    except Exception as E:  # line 65
        buf.write(str(E) + "\n")  # line 65
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
        with open(("." if prefix is None else prefix) + os.sep + (("file%d" % number) if isinstance(number, int) else number), "wb") as fd:  # line 101
            fd.write(contents if isinstance(contents, bytes) else contents.encode("cp1252"))  # line 101

    def existsFile(_, number: 'Union[int, str]', expectedContents: 'bytes'=None) -> 'bool':  # line 103
        if not os.path.exists(("." + os.sep + "file%d" % number) if isinstance(number, int) else number):  # line 104
            return False  # line 104
        if expectedContents is None:  # line 105
            return True  # line 105
        with open(("." + os.sep + "file%d" % number) if isinstance(number, int) else number, "rb") as fd:  # line 106
            return fd.read() == expectedContents  # line 106

    def testAccessor(_):  # line 108
        a = sos.Accessor({"a": 1})  # line 109
        _.assertEqual((1, 1), (a["a"], a.a))  # line 110

    def testFirstofmap(_):  # line 112
        _.assertEqual(2, sos.firstOfMap({"a": 1, "b": 2}, ["x", "b"]))  # line 113
        _.assertIsNone(sos.firstOfMap({"a": 1, "b": 2}, []))  # line 114

    def testAjoin(_):  # line 116
        _.assertEqual("a1a2", sos.ajoin("a", ["1", "2"]))  # line 117
        _.assertEqual("* a\n* b", sos.ajoin("* ", ["a", "b"], "\n"))  # line 118

    def testFindChanges(_):  # line 120
        m = sos.Metadata(os.getcwd())  # line 121
        m.loadBranches()  # line 122
        _.createFile(1, "1")  # line 123
        m.createBranch(0)  # line 124
        _.assertEqual(1, len(m.paths))  # line 125
        time.sleep(FS_PRECISION)  # time required by filesystem time resolution issues  # line 126
        _.createFile(1, "2")  # line 127
        _.createFile(2, "2")  # line 128
        changes = m.findChanges()  # detect time skew  # line 129
        _.assertEqual(1, len(changes.additions))  # line 130
        _.assertEqual(0, len(changes.deletions))  # line 131
        _.assertEqual(1, len(changes.modifications))  # line 132
        m.integrateChangeset(changes)  # line 133
        _.createFile(2, "12")  # modify file  # line 134
        changes = m.findChanges(0, 1)  # by size, creating new commit  # line 135
        _.assertEqual(0, len(changes.additions))  # line 136
        _.assertEqual(0, len(changes.deletions))  # line 137
        _.assertEqual(1, len(changes.modifications))  # line 138
        _.assertTrue(os.path.exists(branchFolder(0, 1)))  # line 139
        _.assertTrue(os.path.exists(branchFolder(0, 1) + os.sep + "03b69bc801ae11f1ff2a71a50f165996d0ad681b4f822df13329a27e53f0fcd2"))  # line 140

    def testDiffFunc(_):  # line 142
        a = {"./a": sos.PathInfo("", 0, 0, "")}  # line 143
        b = {"./a": sos.PathInfo("", 0, 0, "")}  # line 144
        changes = sos.diffPathSets(a, b)  # line 145
        _.assertEqual(0, len(changes.additions))  # line 146
        _.assertEqual(0, len(changes.deletions))  # line 147
        _.assertEqual(0, len(changes.modifications))  # line 148
        b = {"./a": sos.PathInfo("", 1, 0, "")}  # line 149
        changes = sos.diffPathSets(a, b)  # line 150
        _.assertEqual(0, len(changes.additions))  # line 151
        _.assertEqual(0, len(changes.deletions))  # line 152
        _.assertEqual(1, len(changes.modifications))  # line 153
        b = {}  # diff contains no entries -> no change  # line 154
        changes = sos.diffPathSets(a, b)  # line 155
        _.assertEqual(0, len(changes.additions))  # line 156
        _.assertEqual(0, len(changes.deletions))  # line 157
        _.assertEqual(0, len(changes.modifications))  # line 158
        b = {"./a": sos.PathInfo("", None, 1, "")}  # in diff marked as deleted  # line 159
        changes = sos.diffPathSets(a, b)  # line 160
        _.assertEqual(0, len(changes.additions))  # line 161
        _.assertEqual(1, len(changes.deletions))  # line 162
        _.assertEqual(0, len(changes.modifications))  # line 163
        b = {"./b": sos.PathInfo("", 1, 1, "")}  # line 164
        changes = sos.diffPathSets(a, b)  # line 165
        _.assertEqual(1, len(changes.additions))  # line 166
        _.assertEqual(0, len(changes.deletions))  # line 167
        _.assertEqual(0, len(changes.modifications))  # line 168
        a = {"./a": sos.PathInfo("", None, 0, "")}  # mark as deleted  # line 169
        b = {"./a": sos.PathInfo("", 1, 0, "")}  # re-added  # line 170
        changes = sos.diffPathSets(a, b)  # line 171
        _.assertEqual(1, len(changes.additions))  # line 172
        _.assertEqual(0, len(changes.deletions))  # line 173
        _.assertEqual(0, len(changes.modifications))  # line 174
        changes = sos.diffPathSets(b, a)  # line 175
        _.assertEqual(0, len(changes.additions))  # line 176
        _.assertEqual(1, len(changes.deletions))  # line 177
        _.assertEqual(0, len(changes.modifications))  # line 178

    def testPatternPaths(_):  # line 180
        sos.offline(options=["--track"])  # line 181
        os.mkdir("sub")  # line 182
        _.createFile("sub" + os.sep + "file1", "sdfsdf")  # line 183
        sos.add("./sub", "file?")  # this doesn't work as direct call won't invoke getRoot and therefore won't chdir virtually into that folder  # line 184
        sos.commit("test")  # line 185
        _.assertEqual(2, len(os.listdir(os.path.join(sos.metaFolder, "b0", "r1"))))  # sub/file1 was added  # line 186
        _.createFile(1)  # line 187
        try:  # should not commit anything, as the file in base folder doesn't match the path pattern  # line 188
            sos.commit("nothing")  # should not commit anything, as the file in base folder doesn't match the path pattern  # line 188
            _.fail()  # should not commit anything, as the file in base folder doesn't match the path pattern  # line 188
        except:  # line 189
            pass  # line 189

    def testComputeSequentialPathSet(_):  # line 191
        os.makedirs(branchFolder(0, 0))  # line 192
        os.makedirs(branchFolder(0, 1))  # line 193
        os.makedirs(branchFolder(0, 2))  # line 194
        os.makedirs(branchFolder(0, 3))  # line 195
        os.makedirs(branchFolder(0, 4))  # line 196
        m = sos.Metadata(os.getcwd())  # line 197
        m.branch = 0  # line 198
        m.commit = 2  # line 199
        m.saveBranches()  # line 200
        m.paths = {"./a": sos.PathInfo("", 0, 0, "")}  # line 201
        m.saveCommit(0, 0)  # initial  # line 202
        m.paths["./a"] = sos.PathInfo("", 1, 0, "")  # line 203
        m.saveCommit(0, 1)  # mod  # line 204
        m.paths["./b"] = sos.PathInfo("", 0, 0, "")  # line 205
        m.saveCommit(0, 2)  # add  # line 206
        m.paths["./a"] = sos.PathInfo("", None, 0, "")  # line 207
        m.saveCommit(0, 3)  # del  # line 208
        m.paths["./a"] = sos.PathInfo("", None, 0, "")  # line 209
        m.saveCommit(0, 4)  # readd  # line 210
        m.commits = {i: sos.CommitInfo(i, 0, None) for i in range(5)}  # line 211
        m.saveBranch(0)  # line 212
        m.computeSequentialPathSet(0, 4)  # line 213
        _.assertEqual(2, len(m.paths))  # line 214

    def testParseRevisionString(_):  # line 216
        m = sos.Metadata(os.getcwd())  # line 217
        m.branch = 1  # line 218
        m.commits = {0: 0, 1: 1, 2: 2}  # line 219
        _.assertEqual((1, 3), m.parseRevisionString("3"))  # line 220
        _.assertEqual((2, 3), m.parseRevisionString("2/3"))  # line 221
        _.assertEqual((1, -1), m.parseRevisionString(None))  # line 222
        _.assertEqual((2, -1), m.parseRevisionString("2/"))  # line 223
        _.assertEqual((1, -2), m.parseRevisionString("/-2"))  # line 224

    def testOfflineEmpty(_):  # line 226
        os.mkdir("." + os.sep + sos.metaFolder)  # line 227
        try:  # line 228
            sos.offline("trunk")  # line 228
            _.fail()  # line 228
        except SystemExit:  # line 229
            pass  # line 229
        os.rmdir("." + os.sep + sos.metaFolder)  # line 230
        sos.offline("test")  # line 231
        _.assertIn(sos.metaFolder, os.listdir("."))  # line 232
        _.assertAllIn(["b0", sos.metaFile], os.listdir("." + os.sep + sos.metaFolder))  # line 233
        _.assertAllIn(["r0", sos.metaFile], os.listdir("." + os.sep + sos.metaFolder + os.sep + "b0"))  # line 234
        _.assertEqual(2, len(os.listdir("." + os.sep + sos.metaFolder)))  # only branch folder and meta data file  # line 235
        _.assertEqual(2, len(os.listdir("." + os.sep + sos.metaFolder + os.sep + "b0")))  # only commit folder and meta data file  # line 236
        _.assertEqual(1, len(os.listdir(branchFolder(0, 0))))  # only meta data file  # line 237

    def testOfflineWithFiles(_):  # line 239
        _.createFile(1, "x" * 100)  # line 240
        _.createFile(2)  # line 241
        sos.offline("test")  # line 242
        _.assertAllIn(["file1", "file2", sos.metaFolder], os.listdir("."))  # line 243
        _.assertAllIn(["b0", sos.metaFile], os.listdir("." + os.sep + sos.metaFolder))  # line 244
        _.assertAllIn(["r0", sos.metaFile], os.listdir("." + os.sep + sos.metaFolder + os.sep + "b0"))  # line 245
        _.assertAllIn([sos.metaFile, "03b69bc801ae11f1ff2a71a50f165996d0ad681b4f822df13329a27e53f0fcd2", "b9ee10a87f612e299a6eb208210bc0898092a64c48091327cc2aaeee9b764ffa"], os.listdir("." + os.sep + sos.metaFolder + os.sep + "b0" + os.sep + "r0"))  # line 246
        _.assertEqual(2, len(os.listdir("." + os.sep + sos.metaFolder)))  # only branch folder and meta data file  # line 247
        _.assertEqual(2, len(os.listdir("." + os.sep + sos.metaFolder + os.sep + "b0")))  # only commit folder and meta data file  # line 248
        _.assertEqual(3, len(os.listdir(branchFolder(0, 0))))  # only meta data file plus branch base file copies  # line 249

    def testBranch(_):  # line 251
        _.createFile(1, "x" * 100)  # line 252
        _.createFile(2)  # line 253
        sos.offline("test")  # b0/r0  # line 254
        sos.branch("other")  # b1/r0  # line 255
        _.assertAllIn(["b0", "b1", sos.metaFile], os.listdir("." + os.sep + sos.metaFolder))  # line 256
        _.assertEqual(list(sorted(os.listdir("." + os.sep + sos.metaFolder + os.sep + "b0"))), list(sorted(os.listdir("." + os.sep + sos.metaFolder + os.sep + "b1"))))  # line 257
        _.assertEqual(list(sorted(os.listdir(branchFolder(0, 0)))), list(sorted(os.listdir(branchFolder(1, 0)))))  # line 259
        _.createFile(1, "z")  # modify file  # line 261
        sos.branch()  # b2/r0  branch to unnamed branch with modified file tree contents  # line 262
        _.assertNotEqual(os.stat("." + os.sep + sos.metaFolder + os.sep + "b1" + os.sep + "r0" + os.sep + "b9ee10a87f612e299a6eb208210bc0898092a64c48091327cc2aaeee9b764ffa").st_size, os.stat("." + os.sep + sos.metaFolder + os.sep + "b2" + os.sep + "r0" + os.sep + "b9ee10a87f612e299a6eb208210bc0898092a64c48091327cc2aaeee9b764ffa").st_size)  # line 263
        _.createFile(3, "z")  # line 265
        sos.branch("from_last_revision", ["--last", "--stay"])  # b3/r0 create copy of other file1,file2 and don't switch  # line 266
        _.assertEqual(list(sorted(os.listdir("." + os.sep + sos.metaFolder + os.sep + "b3" + os.sep + "r0"))), list(sorted(os.listdir("." + os.sep + sos.metaFolder + os.sep + "b2" + os.sep + "r0"))))  # line 267
# Check sos.status output which branch is marked


    def testComittingAndChanges(_):  # line 272
        _.createFile(1, "x" * 100)  # line 273
        _.createFile(2)  # line 274
        sos.offline("test")  # line 275
        changes = sos.changes()  # line 276
        _.assertEqual(0, len(changes.additions))  # line 277
        _.assertEqual(0, len(changes.deletions))  # line 278
        _.assertEqual(0, len(changes.modifications))  # line 279
        _.createFile(1, "z")  # line 280
        changes = sos.changes()  # line 281
        _.assertEqual(0, len(changes.additions))  # line 282
        _.assertEqual(0, len(changes.deletions))  # line 283
        _.assertEqual(1, len(changes.modifications))  # line 284
        sos.commit("message")  # line 285
        _.assertAllIn(["r0", "r1", sos.metaFile], os.listdir("." + os.sep + sos.metaFolder + os.sep + "b0"))  # line 286
        _.assertAllIn([sos.metaFile, "b9ee10a87f612e299a6eb208210bc0898092a64c48091327cc2aaeee9b764ffa"], os.listdir(branchFolder(0, 1)))  # line 287
        _.assertEqual(2, len(os.listdir(branchFolder(0, 1))))  # no further files, only the modified one  # line 288
        _.assertEqual(1, len(sos.changes("/0").modifications))  # vs. implicit (same) branch revision  # line 289
        _.assertEqual(1, len(sos.changes("0/0").modifications))  # vs. explicit branch revision  # line 290
        _.createFile(1, "")  # create empty file, mentioned in meta data, but not stored as own file  # line 291
        _.assertEqual(0, len(changes.additions))  # line 292
        _.assertEqual(0, len(changes.deletions))  # line 293
        _.assertEqual(1, len(changes.modifications))  # line 294
        sos.commit("modified")  # line 295
        _.assertEqual(1, len(os.listdir(branchFolder(0, 2))))  # no further files, only the modified one  # line 296
        try:  # expecting Exit due to no changes  # line 297
            sos.commit("nothing")  # expecting Exit due to no changes  # line 297
            _.fail()  # expecting Exit due to no changes  # line 297
        except:  # line 298
            pass  # line 298

    def testGetBranch(_):  # line 300
        m = sos.Metadata(os.getcwd())  # line 301
        m.branches = {0: sos.BranchInfo(0, 0, "trunk")}  # line 302
        _.assertEqual(27, m.getBranchByName(27))  # line 303
        _.assertEqual(0, m.getBranchByName("trunk"))  # line 304
        _.assertIsNone(m.getBranchByName("unknwon"))  # line 305

    def testSwitch(_):  # line 307
        _.createFile(1, "x" * 100)  # line 308
        _.createFile(2, "y")  # line 309
        sos.offline("test")  # file1-2  in initial branch commit  # line 310
        sos.branch("second")  # file1-2  switch, having same files  # line 311
        sos.switch("0")  # no change  switch back, no problem  # line 312
        sos.switch("second")  # no change  # switch back, no problem  # line 313
        _.createFile(3, "y")  # generate a file  # line 314
        try:  # uncommited changes detected  # line 315
            sos.switch("test")  # uncommited changes detected  # line 315
            _.fail()  # uncommited changes detected  # line 315
        except SystemExit:  # line 316
            pass  # line 316
        sos.commit("Finish")  # file1-3  commit third file into branch second  # line 317
        sos.changes()  # line 318
        sos.switch("test")  # file1-2, remove file3 from file tree  # line 319
        _.assertFalse(_.existsFile(3))  # removed when switching back to test  # line 320
        out = wrapChannels(lambda: sos.status()).replace("\r", "")  # line 321
        _.assertIn("  * b00   'test'", out)  # line 322
        _.assertIn("    b01 'second'", out)  # line 323
        _.assertIn("(dirty)", out)  # one branch has commits  # line 324
        _.assertIn("(in sync)", out)  # the other doesn't  # line 325
        _.createFile(4, "xy")  # generate a file  # line 326
        sos.switch("second", "--force")  # avoids warning on uncommited changes, but keeps file4  # line 327
        _.assertFalse(_.existsFile(4))  # removed when forcedly switching back to test  # line 328
        _.assertTrue(_.existsFile(3))  # was restored from branch's revision r1  # line 329
        os.unlink("." + os.sep + "file1")  # remove old file1  # line 330
        sos.switch("test", "--force")  # should restore file1 and remove file3  # line 331
        _.assertTrue(_.existsFile(1))  # was restored from branch's revision r1  # line 332
        _.assertFalse(_.existsFile(3))  # was restored from branch's revision r1  # line 333

    def testAutoDetectVCS(_):  # line 335
        os.mkdir(".git")  # line 336
        sos.offline(sos.vcsBranches[sos.findSosVcsBase()[2]])  # create initial branch  # line 337
        with open(sos.metaFolder + os.sep + sos.metaFile, "r") as fd:  # line 338
            meta = fd.read()  # line 338
        _.assertTrue("\"master\"" in meta)  # line 339
        os.rmdir(".git")  # line 340

    def testUpdate(_):  # line 342
        sos.offline("trunk")  # create initial branch b0/r0  # line 343
        _.createFile(1, "x" * 100)  # line 344
        sos.commit("second")  # create b0/r1  # line 345

        sos.switch("/0")  # go back to b0/r0 - deletes file1  # line 347
        _.assertFalse(_.existsFile(1))  # line 348

        sos.update("/1")  # recreate file1  # line 350
        _.assertTrue(_.existsFile(1))  # line 351

        sos.commit("third", ["--force"])  # force because nothing to commit. should create r2 with same contents as r1, but as differential from r1, not from r0 (= no changes in meta folder)  # line 353
        _.assertTrue(os.path.exists(branchFolder(0, 2)))  # line 354
        _.assertTrue(os.path.exists(branchFolder(0, 2) + os.sep + sos.metaFile))  # line 355
        _.assertEqual(1, len(os.listdir(branchFolder(0, 2))))  # only meta data file, no differential files  # line 356

        sos.update("/1")  # do nothing, as nothing has changed  # line 358
        _.assertTrue(_.existsFile(1))  # line 359

        _.createFile(2, "y" * 100)  # line 361
#    out = wrapChannels(() -> sos.branch("other"))  # won't comply as there are changes
#    _.assertIn("--force", out)
        sos.branch("other", ["--force"])  # automatically including file 2 (as we are in simple mode)  # line 364
        _.assertTrue(_.existsFile(2))  # line 365
        sos.update("trunk", ["--add"])  # only add stuff  # line 366
        _.assertTrue(_.existsFile(2))  # line 367
        sos.update("trunk")  # nothing to do  # line 368
        _.assertFalse(_.existsFile(2))  # removes file not present in original branch  # line 369

        theirs = b"a\nb\nc\nd\ne\nf\ng\nh\nx\nx\nj\nk"  # line 371
        _.createFile(10, theirs)  # line 372
        mine = b"a\nc\nd\ne\ng\nf\nx\nh\ny\ny\nj"  # missing "b", inserted g, modified g->x, replace x/x -> y/y, removed k  # line 373
        _.createFile(11, mine)  # line 374
        _.assertEqual(b"a\nb\nc\nd\ne\nf\ng\nh\nx\nx\nj\nk", sos.merge(filename="." + os.sep + "file10", intoname="." + os.sep + "file11", mergeOperation=sos.MergeOperation.BOTH, conflictResolution=sos.ConflictResolution.THEIRS))  # completely recreated other file  # line 375
        _.assertEqual(b"a\nb\nc\nd\ne\ng\nf\ng\nx\nh\nx\nx\ny\ny\nj\nk", sos.merge(filename="." + os.sep + "file10", intoname="." + os.sep + "file11", mergeOperation=sos.MergeOperation.INSERT, conflictResolution=sos.ConflictResolution.MINE))  # line 376

    def testUpdate2(_):  # line 378
        _.createFile("test.txt", "x" * 10)  # line 379
        sos.offline("trunk", ["--strict"])  # use strict mode, as timestamp differences are too small for testing  # line 380
        sos.branch("mod")  # line 381
        _.createFile("test.txt", "x" * 5 + "y" * 5)  # line 382
        time.sleep(FS_PRECISION)  # line 383
        sos.commit("mod")  # create b0/r1  # line 384
        sos.switch("trunk", ["--force"])  # should replace contents, force in case some other files were modified (e.g. during working on the code) TODO investigate more  # line 385
        with open("test.txt", "rb") as fd:  # line 386
            _.assertEqual(b"x" * 10, fd.read())  # line 386
        sos.update("mod", ["--theirs"])  # integrate changes TODO same with ask -> theirs  # line 387
        with open("test.txt", "rb") as fd:  # line 388
            _.assertEqual(b"x" * 5 + b"y" * 5, fd.read())  # line 388
        _.createFile("test.txt", "x" * 10)  # line 389
        mockInput(["t"], lambda: sos.update("mod", ["--ask"]))  # same as above with interaction -> theirs  # line 390
        with open("test.txt", "rb") as fd:  # line 391
            _.assertEqual(b"x" * 5 + b"y" * 5, fd.read())  # line 391

    def testIsTextType(_):  # line 393
        m = sos.Metadata(".")  # line 394
        m.c.texttype = ["*.x", "*.md", "*.md.*"]  # line 395
        m.c.bintype = ["*.md.confluence"]  # line 396
        _.assertTrue(m.isTextType("ab.txt"))  # line 397
        _.assertTrue(m.isTextType("./ab.txt"))  # line 398
        _.assertTrue(m.isTextType("bc/ab.txt"))  # line 399
        _.assertFalse(m.isTextType("bc/ab."))  # line 400
        _.assertTrue(m.isTextType("23_3.x.x"))  # line 401
        _.assertTrue(m.isTextType("dfg/dfglkjdf7/test.md"))  # line 402
        _.assertTrue(m.isTextType("./test.md.pdf"))  # line 403
        _.assertFalse(m.isTextType("./test_a.md.confluence"))  # line 404

    def testEolDet(_):  # line 406
        _.assertEqual(b"\n", sos.eoldet(b"a\nb"))  # line 407
        _.assertEqual(b"\r\n", sos.eoldet(b"a\r\nb\r\n"))  # line 408
        _.assertEqual(b"\r", sos.eoldet(b"\ra\rb"))  # line 409
        _.assertAllIn(["Inconsistent", "with "], wrapChannels(lambda: _.assertEqual(b"\n", sos.eoldet(b"\r\na\r\nb\n"))))  # line 410
        _.assertAllIn(["Inconsistent", "without"], wrapChannels(lambda: _.assertEqual(b"\n", sos.eoldet(b"\ra\nnb\n"))))  # line 411
        _.assertIsNone(sos.eoldet(b""))  # line 412
        _.assertIsNone(sos.eoldet(b"sdf"))  # line 413

    def testMerge(_):  # line 415
        a = b"a\nb\ncc\nd"  # line 416
        b = b"a\nb\nee\nd"  # line 417
        _.assertEqual(b"a\nb\ncc\nee\nd", sos.merge(a, b, mergeOperation=sos.MergeOperation.INSERT))  # means insert changes from a into b, but don't replace  # line 418
        _.assertEqual(b"a\nb\nd", sos.merge(a, b, mergeOperation=sos.MergeOperation.REMOVE))  # line 419
        _.assertEqual(b"a\nb\ncc\nd", sos.merge(a, b, mergeOperation=sos.MergeOperation.BOTH))  # line 420
# Now test intra-line merging without conflicts
        _.assertEqual(b"a\nbc d\ne", sos.merge(b"a\nbc d\ne", b"a\nbcd\ne", mergeOperation=sos.MergeOperation.INSERT))  # because it's a deletion ['  a', '- bc d', '?   -\n', '+ bcd', '  e']  # line 422
        _.assertEqual(b"a\nbcd\ne", sos.merge(b"a\nbc d\ne", b"a\nbcd\ne", mergeOperation=sos.MergeOperation.REMOVE))  # ['  a', '- bc d', '?   -\n', '+ bcd', '  e']  # line 423
        _.assertEqual(b"a\nbc d\ne", sos.merge(b"a\nbcd\ne", b"a\nbc d\ne", mergeOperation=sos.MergeOperation.INSERT))  # nothing to insert  # line 424
        _.assertEqual(b"a\nbcd\ne", sos.merge(b"a\nbcd\ne", b"a\nbc d\ne", mergeOperation=sos.MergeOperation.REMOVE))  # remove space  # line 425
# Test with change + insert (conflict)
        _.assertEqual(b"a\nb fdd d\ne", sos.merge(b"a\nb cd d\ne", b"a\nb fdd d\ne", conflictResolution=sos.ConflictResolution.MINE))  # line 427
        _.assertEqual(b"a\nb cd d\ne", sos.merge(b"a\nb cd d\ne", b"a\nb fdd d\ne", conflictResolution=sos.ConflictResolution.THEIRS))  # ['  a', '- b cd d', '?   ^\n', '+ b fdd d', '?   ^^\n', '  e']  # line 428
        _.assertEqual(b"a\nb fdd d\ne", mockInput(["i"], lambda: sos.merge(b"a\nb cd d\ne", b"a\nb fdd d\ne", conflictResolution=sos.ConflictResolution.ASK)))  # ['  a', '- b cd d', '?   ^\n', '+ b fdd d', '?   ^^\n', '  e']  # line 429
        _.assertEqual(b"a\nb cd d\ne", mockInput(["t"], lambda: sos.merge(b"a\nb cd d\ne", b"a\nb fdd d\ne", conflictResolution=sos.ConflictResolution.ASK)))  # ['  a', '- b cd d', '?   ^\n', '+ b fdd d', '?   ^^\n', '  e']  # line 430
        _.assertEqual(b"abbc", sos.merge(b"abbc", b"addc", mergeOperation=sos.MergeOperation.BOTH, conflictResolution=sos.ConflictResolution.THEIRS))  # line 431
        _.assertEqual(b"a\nbb\nc", sos.merge(b"a\nbb\nc", b"a\ndd\nc", mergeOperation=sos.MergeOperation.BOTH, conflictResolution=sos.ConflictResolution.THEIRS))  # line 432
        _.assertIn("Differing EOL-styles", wrapChannels(lambda: sos.merge(b"a\nb", b"a\r\nb")))  # expect warning  # line 433
        _.assertIn(b"a\r\nb", sos.merge(b"a\nb", b"a\r\nb"))  # in doubt, use "mine" CR-LF  # line 434

    def testPickyMode(_):  # line 436
        sos.offline("trunk", ["--picky"])  # line 437
        sos.add(".", "file?", ["--force"])  # line 438
        _.createFile(1, "aa")  # line 439
        sos.commit("First")  # add one file  # line 440
        _.assertEqual(2, len(os.listdir(branchFolder(0, 1))))  # line 441
        _.createFile(2, "b")  # line 442
        sos.commit("Second", ["--force"])  # add nothing, because picky  # line 443
        _.assertEqual(1, len(os.listdir(branchFolder(0, 2))))  # line 444
        sos.add(".", "file?")  # line 445
        sos.commit("Third")  # add nothing, because picky  # line 446
        _.assertEqual(2, len(os.listdir(branchFolder(0, 3))))  # line 447
        out = wrapChannels(lambda: sos.log()).replace("\r", "")  # line 448
        _.assertIn("    r2", out)  # line 449
        _.assertIn("  * r3", out)  # line 450
        _.assertNotIn("  * r4", out)  # line 451

    def testTrackedSubfolder(_):  # line 453
        os.mkdir("." + os.sep + "sub")  # line 454
        sos.offline("trunk", ["--track"])  # line 455
        _.createFile(1, "x")  # line 456
        _.createFile(1, "x", prefix="sub")  # line 457
        sos.add(".", "file?")  # add glob pattern to track  # line 458
        sos.commit("First")  # line 459
        _.assertEqual(2, len(os.listdir(branchFolder(0, 1))))  # one new file + meta file  # line 460
        sos.add(".", "sub/file?")  # add glob pattern to track  # line 461
        sos.commit("Second")  # one new file + meta  # line 462
        _.assertEqual(2, len(os.listdir(branchFolder(0, 1))))  # one new file + meta file  # line 463
        os.unlink("file1")  # remove from basefolder  # line 464
        _.createFile(2, "y")  # line 465
        sos.rm(".", "sub/file?")  # line 466
        try:  # raises Exit. TODO test the "suggest a pattern" case  # line 467
            sos.rm(".", "sub/bla")  # raises Exit. TODO test the "suggest a pattern" case  # line 467
            _.fail()  # raises Exit. TODO test the "suggest a pattern" case  # line 467
        except:  # line 468
            pass  # line 468
        sos.commit("Third")  # line 469
        _.assertEqual(2, len(os.listdir(branchFolder(0, 2))))  # one new file + meta  # line 470
# TODO check if /file1 and sub/file1 were removed from index

    def testTrackedMode(_):  # line 473
        ''' Difference in semantics vs simple mode:
          - For remote/other branch we can only know and consider tracked files, thus ignoring all complexity stemming from handling addition of untracked files.
          - For current branch, we can take into account tracked and untracked ones, in theory, but it doesn't make sense.
        In conclusion, using the union of tracking patterns from both sides to find affected files makes sense, but disallow deleting files not present in remote branch.
    '''  # line 478
        sos.offline("test", options=["--track"])  # set up repo in tracking mode (SVN- or gitless-style)  # line 479
        _.createFile(1)  # line 480
        _.createFile("a123a")  # untracked file "a123a"  # line 481
        sos.add(".", "file?")  # add glob tracking pattern  # line 482
        sos.commit("second")  # versions "file1"  # line 483
        _.assertEqual(2, len(os.listdir(branchFolder(0, 1))))  # one new file + meta file  # line 484
        out = wrapChannels(lambda: sos.status()).replace("\r", "")  # line 485
        _.assertIn("  | ./file?", out)  # line 486

        _.createFile(2)  # untracked file "file2"  # line 488
        sos.commit("third")  # versions "file2"  # line 489
        _.assertEqual(2, len(os.listdir(branchFolder(0, 2))))  # one new file + meta file  # line 490

        os.mkdir("." + os.sep + "sub")  # line 492
        _.createFile(3, prefix="sub")  # untracked file "sub/file3"  # line 493
        sos.commit("fourth", ["--force"])  # no tracking pattern matches the subfolder  # line 494
        _.assertEqual(1, len(os.listdir(branchFolder(0, 3))))  # meta file only, no other tracked path/file  # line 495

        sos.branch("Other")  # second branch containing file1 and file2 tracked by "./file?"  # line 497
        sos.rm(".", "file?")  # remove tracking pattern, but don't touch previously created and versioned files  # line 498
        sos.add(".", "a*a")  # add tracking pattern  # line 499
        changes = sos.changes()  # should pick up addition  # line 500
        _.assertEqual(0, len(changes.modifications))  # line 501
        _.assertEqual(0, len(changes.deletions))  # not tracked anymore, but contained in version history and not removed  # line 502
        _.assertEqual(1, len(changes.additions))  # detected one addition "a123a", but won't recognize untracking files as deletion  # line 503

        sos.commit("Second_2")  # line 505
        _.assertEqual(2, len(os.listdir(branchFolder(1, 1))))  # "a123a" + meta file  # line 506
        _.assertTrue(os.path.exists("." + os.sep + "file1"))  # line 507
        _.assertTrue(os.path.exists("." + os.sep + "file2"))  # line 508

        sos.switch("test")  # go back to first branch - tracks only "file?", but not "a*a"  # line 510
        _.assertTrue(os.path.exists("." + os.sep + "file1"))  # line 511
        _.assertTrue(os.path.exists("." + os.sep + "a123a"))  # should not have been touched so far  # line 512

        sos.update("Other")  # integrate tracked files and tracking pattern from second branch into working state of master branch  # line 514
        _.assertTrue(os.path.exists("." + os.sep + "file1"))  # line 515
        _.assertTrue(os.path.exists("." + os.sep + "a123a"))  # line 516

        _.createFile("axxxa")  # new file that should be tracked on "test" now that we integrated "Other"  # line 518
        sos.commit("fifth")  # create new revision after integrating updates from second branch  # line 519
        _.assertEqual(3, len(os.listdir(branchFolder(0, 4))))  # one new file from other branch + one new in current folder + meta file  # line 520
        sos.switch("Other")  # switch back to just integrated branch that tracks only "a*a" - shouldn't do anything  # line 521
        _.assertTrue(os.path.exists("." + os.sep + "file1"))  # line 522
        _.assertTrue(os.path.exists("." + os.sep + "a123a"))  # line 523
        _.assertFalse(os.path.exists("." + os.sep + "axxxa"))  # because tracked in both branches, but not present in other -> delete in file tree TODO document  # line 524
# TODO test switch --meta

    def testLsTracked(_):  # line 527
        sos.offline("test", options=["--track"])  # set up repo in tracking mode (SVN- or gitless-style)  # line 528
        _.createFile(1)  # line 529
        _.createFile("foo")  # line 530
        sos.add(".", "file*")  # capture one file  # line 531
        out = sos.safeSplit(wrapChannels(lambda: sos.ls()).replace("\r", ""), "\n")  # line 532
        _.assertInAny('TRK file1 by "./file*"', out)  # line 533
        _.assertNotInAny('    file1 by "./file*"', out)  # line 534
        _.assertInAny("    foo", out)  # line 535

    def testCompression(_):  # line 537
        _.createFile(1)  # line 538
        sos.offline("master", options=["--plain", "--force"])  # line 539
        _.assertTrue(_.existsFile(branchFolder(0, 0) + os.sep + "b9ee10a87f612e299a6eb208210bc0898092a64c48091327cc2aaeee9b764ffa", b"x" * 10))  # line 540
        setRepoFlag("compress", True)  # was plain = uncompressed before  # line 541
        _.createFile(2)  # line 542
        sos.commit("Added file2")  # line 543
        _.assertTrue(_.existsFile(branchFolder(0, 1) + os.sep + "03b69bc801ae11f1ff2a71a50f165996d0ad681b4f822df13329a27e53f0fcd2"))  # exists  # line 544
        _.assertFalse(_.existsFile(branchFolder(0, 1) + os.sep + "03b69bc801ae11f1ff2a71a50f165996d0ad681b4f822df13329a27e53f0fcd2", b"x" * 10))  # but is compressed instead  # line 545

    def testConfigVariations(_):  # line 547
        def makeRepo():  # line 548
            try:  # line 549
                os.unlink("file1")  # line 549
            except:  # line 550
                pass  # line 550
            sos.offline("master", options=["--plain", "--force"])  # line 551
            _.createFile(1)  # line 552
            sos.commit("Added file1")  # line 553
        sos.config("set", ["strict", "on"])  # line 554
        makeRepo()  # line 555
        _.assertTrue(checkRepoFlag("strict", True))  # line 556
        sos.config("set", ["strict", "off"])  # line 557
        makeRepo()  # line 558
        _.assertTrue(checkRepoFlag("strict", False))  # line 559
        sos.config("set", ["strict", "yes"])  # line 560
        makeRepo()  # line 561
        _.assertTrue(checkRepoFlag("strict", True))  # line 562
        sos.config("set", ["strict", "no"])  # line 563
        makeRepo()  # line 564
        _.assertTrue(checkRepoFlag("strict", False))  # line 565
        sos.config("set", ["strict", "1"])  # line 566
        makeRepo()  # line 567
        _.assertTrue(checkRepoFlag("strict", True))  # line 568
        sos.config("set", ["strict", "0"])  # line 569
        makeRepo()  # line 570
        _.assertTrue(checkRepoFlag("strict", False))  # line 571
        sos.config("set", ["strict", "true"])  # line 572
        makeRepo()  # line 573
        _.assertTrue(checkRepoFlag("strict", True))  # line 574
        sos.config("set", ["strict", "false"])  # line 575
        makeRepo()  # line 576
        _.assertTrue(checkRepoFlag("strict", False))  # line 577
        sos.config("set", ["strict", "enable"])  # line 578
        makeRepo()  # line 579
        _.assertTrue(checkRepoFlag("strict", True))  # line 580
        sos.config("set", ["strict", "disable"])  # line 581
        makeRepo()  # line 582
        _.assertTrue(checkRepoFlag("strict", False))  # line 583
        sos.config("set", ["strict", "enabled"])  # line 584
        makeRepo()  # line 585
        _.assertTrue(checkRepoFlag("strict", True))  # line 586
        sos.config("set", ["strict", "disabled"])  # line 587
        makeRepo()  # line 588
        _.assertTrue(checkRepoFlag("strict", False))  # line 589
        try:  # line 590
            sos.config("set", ["strict", "nope"])  # line 590
            _.fail()  # line 590
        except:  # line 591
            pass  # line 591

    def testLsSimple(_):  # line 593
        _.createFile(1)  # line 594
        _.createFile("foo")  # line 595
        _.createFile("ign1")  # line 596
        _.createFile("ign2")  # line 597
        sos.offline("test")  # set up repo in tracking mode (SVN- or gitless-style)  # line 598
        sos.config("set", ["ignores", "ign1"])  # define an ignore pattern  # line 599
        sos.config("add", ["ignores", "ign2"])  # define an ignore pattern  # line 600
        sos.config("set", ["ignoresWhitelist", "ign1;ign2"])  # define a list of ignore patterns  # line 601
        out = wrapChannels(lambda: sos.config("show")).replace("\r", "")  # line 602
        _.assertIn("ignores => ['ign1', 'ign2']", out)  # line 603
        out = sos.safeSplit(wrapChannels(lambda: sos.ls()).replace("\r", ""), "\n")  # line 604
        _.assertInAny('    file1', out)  # line 605
        _.assertInAny('    ign1', out)  # line 606
        _.assertInAny('    ign2', out)  # line 607
        try:  # line 608
            sos.config("rm", ["foo", "bar"])  # line 608
            _.fail()  # line 608
        except:  # line 609
            pass  # line 609
        try:  # line 610
            sos.config("rm", ["ignores", "foo"])  # line 610
            _.fail()  # line 610
        except:  # line 611
            pass  # line 611
        sos.config("rm", ["ignores", "ign1"])  # line 612
        sos.config("unset", ["ignoresWhitelist"])  # remove ignore pattern  # line 613
        out = sos.safeSplit(wrapChannels(lambda: sos.ls()).replace("\r", ""), "\n")  # line 614
        _.assertInAny('    ign1', out)  # line 615
        _.assertInAny('IGN ign2', out)  # line 616
        _.assertNotInAny('    ign2', out)  # line 617

    def testWhitelist(_):  # line 619
# TODO test same for simple mode
        _.createFile(1)  # line 621
        sos.defaults.ignores[:] = ["file*"]  # replace in-place  # line 622
        sos.offline("xx", ["--track", "--strict"])  # because nothing to commit due to ignore pattern  # line 623
        sos.add(".", "file*")  # add tracking pattern for "file1"  # line 624
        sos.commit(options=["--force"])  # attempt to commit the file  # line 625
        _.assertEqual(1, len(os.listdir(branchFolder(0, 1))))  # only meta data, file1 was ignored  # line 626
        try:  # Exit because dirty  # line 627
            sos.online()  # Exit because dirty  # line 627
            _.fail()  # Exit because dirty  # line 627
        except:  # exception expected  # line 628
            pass  # exception expected  # line 628
        _.createFile("x2")  # add another change  # line 629
        sos.add(".", "x?")  # add tracking pattern for "file1"  # line 630
        try:  # force beyond dirty flag check  # line 631
            sos.online(["--force"])  # force beyond dirty flag check  # line 631
            _.fail()  # force beyond dirty flag check  # line 631
        except:  # line 632
            pass  # line 632
        sos.online(["--force", "--force"])  # force beyond file tree modifications check  # line 633
        _.assertFalse(os.path.exists(sos.metaFolder))  # line 634

        _.createFile(1)  # line 636
        sos.defaults.ignoresWhitelist[:] = ["file*"]  # line 637
        sos.offline("xx", ["--track"])  # line 638
        sos.add(".", "file*")  # line 639
        sos.commit()  # should NOT ask for force here  # line 640
        _.assertEqual(2, len(os.listdir(branchFolder(0, 1))))  # meta data and "file1", file1 was whitelisted  # line 641

    def testRemove(_):  # line 643
        _.createFile(1, "x" * 100)  # line 644
        sos.offline("trunk")  # line 645
        try:  # line 646
            sos.delete("trunk")  # line 646
            _fail()  # line 646
        except:  # line 647
            pass  # line 647
        _.createFile(2, "y" * 10)  # line 648
        sos.branch("added")  # line 649
        sos.delete("trunk")  # line 650
        _.assertEqual(2, len(os.listdir("." + os.sep + sos.metaFolder)))  # meta data file and "b1"  # line 651
        _.assertTrue(os.path.exists("." + os.sep + sos.metaFolder + os.sep + "b1"))  # line 652
        _.assertFalse(os.path.exists("." + os.sep + sos.metaFolder + os.sep + "b0"))  # line 653
        sos.branch("next")  # line 654
        _.createFile(3, "y" * 10)  # make a change  # line 655
        sos.delete("added", "--force")  # should succeed  # line 656

    def testUsage(_):  # line 658
        sos.usage()  # line 659

    def testDiff(_):  # line 661
        sos.offline(options=["--strict"])  # line 662
        _.createFile(1)  # line 663
        sos.commit()  # line 664
        _.createFile(1, "sdfsdgfsdf")  # line 665
        time.sleep(FS_PRECISION)  # line 666
        sos.commit()  # TODO this sometimes fails "nothing to commit"  # line 667
        _.createFile(1, "foobar")  # line 668
        _.assertAllIn(["MOD ./file1", "DIF ./file1", "- | 0000 |xxxxxxxxxx|", "+ | 0000 |foobar|"], wrapChannels(lambda: sos.diff("/-2")))  # second last  # line 669

    def testFindBase(_):  # line 671
        old = os.getcwd()  # line 672
        try:  # line 673
            os.mkdir("." + os.sep + ".git")  # line 674
            os.makedirs("." + os.sep + "a" + os.sep + sos.metaFolder)  # line 675
            os.makedirs("." + os.sep + "a" + os.sep + "b")  # line 676
            os.chdir("a" + os.sep + "b")  # line 677
            s, vcs, cmd = sos.findSosVcsBase()  # line 678
            _.assertIsNotNone(s)  # line 679
            _.assertIsNotNone(vcs)  # line 680
            _.assertEqual("git", cmd)  # line 681
        finally:  # line 682
            os.chdir(old)  # line 682


if __name__ == '__main__':  # line 685
    logging.basicConfig(level=logging.DEBUG if '-v' in sys.argv or os.getenv("DEBUG", "false").strip().lower() == "true" or os.getenv("CI", "false").strip().lower() == "true" else logging.INFO, stream=sys.stderr, format="%(asctime)-23s %(levelname)-8s %(name)s:%(lineno)d | %(message)s" if '-v' in sys.argv or os.getenv("DEBUG", "false") == "true" else "%(message)s")  # line 686
    if configr:  # line 687
        c = configr.Configr("sos")  # line 688
        c.loadSettings()  # line 688
        if len(c.keys()) > 0:  # line 689
            sos.Exit("Cannot run test suite with existing local SOS user configuration (would affect results)")  # line 689
    unittest.main(testRunner=debugTestRunner() if '-v' in sys.argv and not os.getenv("CI", "false").lower() == "true" else None)  # warnings = "ignore")  # line 690
