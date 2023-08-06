#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# __coconut_hash__ = 0x8fabb256

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
        _.assertEqual((1, -1), m.parseRevisionString("/"))  # line 225

    def testOfflineEmpty(_):  # line 227
        os.mkdir("." + os.sep + sos.metaFolder)  # line 228
        try:  # line 229
            sos.offline("trunk")  # line 229
            _.fail()  # line 229
        except SystemExit:  # line 230
            pass  # line 230
        os.rmdir("." + os.sep + sos.metaFolder)  # line 231
        sos.offline("test")  # line 232
        _.assertIn(sos.metaFolder, os.listdir("."))  # line 233
        _.assertAllIn(["b0", sos.metaFile], os.listdir("." + os.sep + sos.metaFolder))  # line 234
        _.assertAllIn(["r0", sos.metaFile], os.listdir("." + os.sep + sos.metaFolder + os.sep + "b0"))  # line 235
        _.assertEqual(2, len(os.listdir("." + os.sep + sos.metaFolder)))  # only branch folder and meta data file  # line 236
        _.assertEqual(2, len(os.listdir("." + os.sep + sos.metaFolder + os.sep + "b0")))  # only commit folder and meta data file  # line 237
        _.assertEqual(1, len(os.listdir(branchFolder(0, 0))))  # only meta data file  # line 238

    def testOfflineWithFiles(_):  # line 240
        _.createFile(1, "x" * 100)  # line 241
        _.createFile(2)  # line 242
        sos.offline("test")  # line 243
        _.assertAllIn(["file1", "file2", sos.metaFolder], os.listdir("."))  # line 244
        _.assertAllIn(["b0", sos.metaFile], os.listdir("." + os.sep + sos.metaFolder))  # line 245
        _.assertAllIn(["r0", sos.metaFile], os.listdir("." + os.sep + sos.metaFolder + os.sep + "b0"))  # line 246
        _.assertAllIn([sos.metaFile, "03b69bc801ae11f1ff2a71a50f165996d0ad681b4f822df13329a27e53f0fcd2", "b9ee10a87f612e299a6eb208210bc0898092a64c48091327cc2aaeee9b764ffa"], os.listdir("." + os.sep + sos.metaFolder + os.sep + "b0" + os.sep + "r0"))  # line 247
        _.assertEqual(2, len(os.listdir("." + os.sep + sos.metaFolder)))  # only branch folder and meta data file  # line 248
        _.assertEqual(2, len(os.listdir("." + os.sep + sos.metaFolder + os.sep + "b0")))  # only commit folder and meta data file  # line 249
        _.assertEqual(3, len(os.listdir(branchFolder(0, 0))))  # only meta data file plus branch base file copies  # line 250

    def testBranch(_):  # line 252
        _.createFile(1, "x" * 100)  # line 253
        _.createFile(2)  # line 254
        sos.offline("test")  # b0/r0  # line 255
        sos.branch("other")  # b1/r0  # line 256
        _.assertAllIn(["b0", "b1", sos.metaFile], os.listdir("." + os.sep + sos.metaFolder))  # line 257
        _.assertEqual(list(sorted(os.listdir("." + os.sep + sos.metaFolder + os.sep + "b0"))), list(sorted(os.listdir("." + os.sep + sos.metaFolder + os.sep + "b1"))))  # line 258
        _.assertEqual(list(sorted(os.listdir(branchFolder(0, 0)))), list(sorted(os.listdir(branchFolder(1, 0)))))  # line 260
        _.createFile(1, "z")  # modify file  # line 262
        sos.branch()  # b2/r0  branch to unnamed branch with modified file tree contents  # line 263
        _.assertNotEqual(os.stat("." + os.sep + sos.metaFolder + os.sep + "b1" + os.sep + "r0" + os.sep + "b9ee10a87f612e299a6eb208210bc0898092a64c48091327cc2aaeee9b764ffa").st_size, os.stat("." + os.sep + sos.metaFolder + os.sep + "b2" + os.sep + "r0" + os.sep + "b9ee10a87f612e299a6eb208210bc0898092a64c48091327cc2aaeee9b764ffa").st_size)  # line 264
        _.createFile(3, "z")  # line 266
        sos.branch("from_last_revision", ["--last", "--stay"])  # b3/r0 create copy of other file1,file2 and don't switch  # line 267
        _.assertEqual(list(sorted(os.listdir("." + os.sep + sos.metaFolder + os.sep + "b3" + os.sep + "r0"))), list(sorted(os.listdir("." + os.sep + sos.metaFolder + os.sep + "b2" + os.sep + "r0"))))  # line 268
# Check sos.status output which branch is marked


    def testComittingAndChanges(_):  # line 273
        _.createFile(1, "x" * 100)  # line 274
        _.createFile(2)  # line 275
        sos.offline("test")  # line 276
        changes = sos.changes()  # line 277
        _.assertEqual(0, len(changes.additions))  # line 278
        _.assertEqual(0, len(changes.deletions))  # line 279
        _.assertEqual(0, len(changes.modifications))  # line 280
        _.createFile(1, "z")  # line 281
        changes = sos.changes()  # line 282
        _.assertEqual(0, len(changes.additions))  # line 283
        _.assertEqual(0, len(changes.deletions))  # line 284
        _.assertEqual(1, len(changes.modifications))  # line 285
        sos.commit("message")  # line 286
        _.assertAllIn(["r0", "r1", sos.metaFile], os.listdir("." + os.sep + sos.metaFolder + os.sep + "b0"))  # line 287
        _.assertAllIn([sos.metaFile, "b9ee10a87f612e299a6eb208210bc0898092a64c48091327cc2aaeee9b764ffa"], os.listdir(branchFolder(0, 1)))  # line 288
        _.assertEqual(2, len(os.listdir(branchFolder(0, 1))))  # no further files, only the modified one  # line 289
        _.assertEqual(1, len(sos.changes("/0").modifications))  # vs. implicit (same) branch revision  # line 290
        _.assertEqual(1, len(sos.changes("0/0").modifications))  # vs. explicit branch revision  # line 291
        _.createFile(1, "")  # create empty file, mentioned in meta data, but not stored as own file  # line 292
        _.assertEqual(0, len(changes.additions))  # line 293
        _.assertEqual(0, len(changes.deletions))  # line 294
        _.assertEqual(1, len(changes.modifications))  # line 295
        sos.commit("modified")  # line 296
        _.assertEqual(1, len(os.listdir(branchFolder(0, 2))))  # no further files, only the modified one  # line 297
        try:  # expecting Exit due to no changes  # line 298
            sos.commit("nothing")  # expecting Exit due to no changes  # line 298
            _.fail()  # expecting Exit due to no changes  # line 298
        except:  # line 299
            pass  # line 299

    def testGetBranch(_):  # line 301
        m = sos.Metadata(os.getcwd())  # line 302
        m.branch = 1  # current branch  # line 303
        m.branches = {0: sos.BranchInfo(0, 0, "trunk")}  # line 304
        _.assertEqual(27, m.getBranchByName(27))  # line 305
        _.assertEqual(0, m.getBranchByName("trunk"))  # line 306
        _.assertEqual(1, m.getBranchByName(""))  # split from "/"  # line 307
        _.assertIsNone(m.getBranchByName("unknown"))  # line 308
        m.commits = {0: sos.CommitInfo(0, 0, "bla")}  # line 309
        _.assertEqual(13, m.getRevisionByName("13"))  # line 310
        _.assertEqual(0, m.getRevisionByName("bla"))  # line 311
        _.assertEqual(-1, m.getRevisionByName(""))  # split from "/"  # line 312

    def testTagging(_):  # line 314
        m = sos.Metadata(os.getcwd())  # line 315
        sos.offline()  # line 316
        _.createFile(111)  # line 317
        sos.commit("tag", ["--tag"])  # line 318
        _.createFile(2)  # line 319
        try:  # line 320
            sos.commit("tag")  # line 320
            _.fail()  # line 320
        except:  # line 321
            pass  # line 321
        sos.commit("tag-2", ["--tag"])  # line 322

    def testSwitch(_):  # line 324
        _.createFile(1, "x" * 100)  # line 325
        _.createFile(2, "y")  # line 326
        sos.offline("test")  # file1-2  in initial branch commit  # line 327
        sos.branch("second")  # file1-2  switch, having same files  # line 328
        sos.switch("0")  # no change  switch back, no problem  # line 329
        sos.switch("second")  # no change  # switch back, no problem  # line 330
        _.createFile(3, "y")  # generate a file  # line 331
        try:  # uncommited changes detected  # line 332
            sos.switch("test")  # uncommited changes detected  # line 332
            _.fail()  # uncommited changes detected  # line 332
        except SystemExit:  # line 333
            pass  # line 333
        sos.commit("Finish")  # file1-3  commit third file into branch second  # line 334
        sos.changes()  # line 335
        sos.switch("test")  # file1-2, remove file3 from file tree  # line 336
        _.assertFalse(_.existsFile(3))  # removed when switching back to test  # line 337
        out = wrapChannels(lambda: sos.status()).replace("\r", "")  # line 338
        _.assertIn("  * b00   'test'", out)  # line 339
        _.assertIn("    b01 'second'", out)  # line 340
        _.assertIn("(dirty)", out)  # one branch has commits  # line 341
        _.assertIn("(in sync)", out)  # the other doesn't  # line 342
        _.createFile(4, "xy")  # generate a file  # line 343
        sos.switch("second", "--force")  # avoids warning on uncommited changes, but keeps file4  # line 344
        _.assertFalse(_.existsFile(4))  # removed when forcedly switching back to test  # line 345
        _.assertTrue(_.existsFile(3))  # was restored from branch's revision r1  # line 346
        os.unlink("." + os.sep + "file1")  # remove old file1  # line 347
        sos.switch("test", "--force")  # should restore file1 and remove file3  # line 348
        _.assertTrue(_.existsFile(1))  # was restored from branch's revision r1  # line 349
        _.assertFalse(_.existsFile(3))  # was restored from branch's revision r1  # line 350

    def testAutoDetectVCS(_):  # line 352
        os.mkdir(".git")  # line 353
        sos.offline(sos.vcsBranches[sos.findSosVcsBase()[2]])  # create initial branch  # line 354
        with open(sos.metaFolder + os.sep + sos.metaFile, "r") as fd:  # line 355
            meta = fd.read()  # line 355
        _.assertTrue("\"master\"" in meta)  # line 356
        os.rmdir(".git")  # line 357

    def testUpdate(_):  # line 359
        sos.offline("trunk")  # create initial branch b0/r0  # line 360
        _.createFile(1, "x" * 100)  # line 361
        sos.commit("second")  # create b0/r1  # line 362

        sos.switch("/0")  # go back to b0/r0 - deletes file1  # line 364
        _.assertFalse(_.existsFile(1))  # line 365

        sos.update("/1")  # recreate file1  # line 367
        _.assertTrue(_.existsFile(1))  # line 368

        sos.commit("third", ["--force"])  # force because nothing to commit. should create r2 with same contents as r1, but as differential from r1, not from r0 (= no changes in meta folder)  # line 370
        _.assertTrue(os.path.exists(branchFolder(0, 2)))  # line 371
        _.assertTrue(os.path.exists(branchFolder(0, 2) + os.sep + sos.metaFile))  # line 372
        _.assertEqual(1, len(os.listdir(branchFolder(0, 2))))  # only meta data file, no differential files  # line 373

        sos.update("/1")  # do nothing, as nothing has changed  # line 375
        _.assertTrue(_.existsFile(1))  # line 376

        _.createFile(2, "y" * 100)  # line 378
#    out = wrapChannels(() -> sos.branch("other"))  # won't comply as there are changes
#    _.assertIn("--force", out)
        sos.branch("other", ["--force"])  # automatically including file 2 (as we are in simple mode)  # line 381
        _.assertTrue(_.existsFile(2))  # line 382
        sos.update("trunk", ["--add"])  # only add stuff  # line 383
        _.assertTrue(_.existsFile(2))  # line 384
        sos.update("trunk")  # nothing to do  # line 385
        _.assertFalse(_.existsFile(2))  # removes file not present in original branch  # line 386

        theirs = b"a\nb\nc\nd\ne\nf\ng\nh\nx\nx\nj\nk"  # line 388
        _.createFile(10, theirs)  # line 389
        mine = b"a\nc\nd\ne\ng\nf\nx\nh\ny\ny\nj"  # missing "b", inserted g, modified g->x, replace x/x -> y/y, removed k  # line 390
        _.createFile(11, mine)  # line 391
        _.assertEqual(b"a\nb\nc\nd\ne\nf\ng\nh\nx\nx\nj\nk", sos.merge(filename="." + os.sep + "file10", intoname="." + os.sep + "file11", mergeOperation=sos.MergeOperation.BOTH, conflictResolution=sos.ConflictResolution.THEIRS))  # completely recreated other file  # line 392
        _.assertEqual(b"a\nb\nc\nd\ne\ng\nf\ng\nx\nh\nx\nx\ny\ny\nj\nk", sos.merge(filename="." + os.sep + "file10", intoname="." + os.sep + "file11", mergeOperation=sos.MergeOperation.INSERT, conflictResolution=sos.ConflictResolution.MINE))  # line 393

    def testUpdate2(_):  # line 395
        _.createFile("test.txt", "x" * 10)  # line 396
        sos.offline("trunk", ["--strict"])  # use strict mode, as timestamp differences are too small for testing  # line 397
        sos.branch("mod")  # line 398
        _.createFile("test.txt", "x" * 5 + "y" * 5)  # line 399
        time.sleep(FS_PRECISION)  # line 400
        sos.commit("mod")  # create b0/r1  # line 401
        sos.switch("trunk", ["--force"])  # should replace contents, force in case some other files were modified (e.g. during working on the code) TODO investigate more  # line 402
        with open("test.txt", "rb") as fd:  # line 403
            _.assertEqual(b"x" * 10, fd.read())  # line 403
        sos.update("mod", ["--theirs"])  # integrate changes TODO same with ask -> theirs  # line 404
        with open("test.txt", "rb") as fd:  # line 405
            _.assertEqual(b"x" * 5 + b"y" * 5, fd.read())  # line 405
        _.createFile("test.txt", "x" * 10)  # line 406
        mockInput(["t"], lambda: sos.update("mod", ["--ask"]))  # same as above with interaction -> theirs  # line 407
        with open("test.txt", "rb") as fd:  # line 408
            _.assertEqual(b"x" * 5 + b"y" * 5, fd.read())  # line 408

    def testIsTextType(_):  # line 410
        m = sos.Metadata(".")  # line 411
        m.c.texttype = ["*.x", "*.md", "*.md.*"]  # line 412
        m.c.bintype = ["*.md.confluence"]  # line 413
        _.assertTrue(m.isTextType("ab.txt"))  # line 414
        _.assertTrue(m.isTextType("./ab.txt"))  # line 415
        _.assertTrue(m.isTextType("bc/ab.txt"))  # line 416
        _.assertFalse(m.isTextType("bc/ab."))  # line 417
        _.assertTrue(m.isTextType("23_3.x.x"))  # line 418
        _.assertTrue(m.isTextType("dfg/dfglkjdf7/test.md"))  # line 419
        _.assertTrue(m.isTextType("./test.md.pdf"))  # line 420
        _.assertFalse(m.isTextType("./test_a.md.confluence"))  # line 421

    def testEolDet(_):  # line 423
        _.assertEqual(b"\n", sos.eoldet(b"a\nb"))  # line 424
        _.assertEqual(b"\r\n", sos.eoldet(b"a\r\nb\r\n"))  # line 425
        _.assertEqual(b"\r", sos.eoldet(b"\ra\rb"))  # line 426
        _.assertAllIn(["Inconsistent", "with "], wrapChannels(lambda: _.assertEqual(b"\n", sos.eoldet(b"\r\na\r\nb\n"))))  # line 427
        _.assertAllIn(["Inconsistent", "without"], wrapChannels(lambda: _.assertEqual(b"\n", sos.eoldet(b"\ra\nnb\n"))))  # line 428
        _.assertIsNone(sos.eoldet(b""))  # line 429
        _.assertIsNone(sos.eoldet(b"sdf"))  # line 430

    def testMerge(_):  # line 432
        a = b"a\nb\ncc\nd"  # line 433
        b = b"a\nb\nee\nd"  # line 434
        _.assertEqual(b"a\nb\ncc\nee\nd", sos.merge(a, b, mergeOperation=sos.MergeOperation.INSERT))  # means insert changes from a into b, but don't replace  # line 435
        _.assertEqual(b"a\nb\nd", sos.merge(a, b, mergeOperation=sos.MergeOperation.REMOVE))  # line 436
        _.assertEqual(b"a\nb\ncc\nd", sos.merge(a, b, mergeOperation=sos.MergeOperation.BOTH))  # line 437
# Now test intra-line merging without conflicts
        _.assertEqual(b"a\nbc d\ne", sos.merge(b"a\nbc d\ne", b"a\nbcd\ne", mergeOperation=sos.MergeOperation.INSERT))  # because it's a deletion ['  a', '- bc d', '?   -\n', '+ bcd', '  e']  # line 439
        _.assertEqual(b"a\nbcd\ne", sos.merge(b"a\nbc d\ne", b"a\nbcd\ne", mergeOperation=sos.MergeOperation.REMOVE))  # ['  a', '- bc d', '?   -\n', '+ bcd', '  e']  # line 440
        _.assertEqual(b"a\nbc d\ne", sos.merge(b"a\nbcd\ne", b"a\nbc d\ne", mergeOperation=sos.MergeOperation.INSERT))  # nothing to insert  # line 441
        _.assertEqual(b"a\nbcd\ne", sos.merge(b"a\nbcd\ne", b"a\nbc d\ne", mergeOperation=sos.MergeOperation.REMOVE))  # remove space  # line 442
# Test with change + insert (conflict)
        _.assertEqual(b"a\nb fdd d\ne", sos.merge(b"a\nb cd d\ne", b"a\nb fdd d\ne", conflictResolution=sos.ConflictResolution.MINE))  # line 444
        _.assertEqual(b"a\nb cd d\ne", sos.merge(b"a\nb cd d\ne", b"a\nb fdd d\ne", conflictResolution=sos.ConflictResolution.THEIRS))  # ['  a', '- b cd d', '?   ^\n', '+ b fdd d', '?   ^^\n', '  e']  # line 445
        _.assertEqual(b"a\nb fdd d\ne", mockInput(["i"], lambda: sos.merge(b"a\nb cd d\ne", b"a\nb fdd d\ne", conflictResolution=sos.ConflictResolution.ASK)))  # ['  a', '- b cd d', '?   ^\n', '+ b fdd d', '?   ^^\n', '  e']  # line 446
        _.assertEqual(b"a\nb cd d\ne", mockInput(["t"], lambda: sos.merge(b"a\nb cd d\ne", b"a\nb fdd d\ne", conflictResolution=sos.ConflictResolution.ASK)))  # ['  a', '- b cd d', '?   ^\n', '+ b fdd d', '?   ^^\n', '  e']  # line 447
        _.assertEqual(b"abbc", sos.merge(b"abbc", b"addc", mergeOperation=sos.MergeOperation.BOTH, conflictResolution=sos.ConflictResolution.THEIRS))  # line 448
        _.assertEqual(b"a\nbb\nc", sos.merge(b"a\nbb\nc", b"a\ndd\nc", mergeOperation=sos.MergeOperation.BOTH, conflictResolution=sos.ConflictResolution.THEIRS))  # line 449
        _.assertIn("Differing EOL-styles", wrapChannels(lambda: sos.merge(b"a\nb", b"a\r\nb")))  # expect warning  # line 450
        _.assertIn(b"a\r\nb", sos.merge(b"a\nb", b"a\r\nb"))  # in doubt, use "mine" CR-LF  # line 451

    def testPickyMode(_):  # line 453
        sos.offline("trunk", ["--picky"])  # line 454
        sos.add(".", "file?", ["--force"])  # line 455
        _.createFile(1, "aa")  # line 456
        sos.commit("First")  # add one file  # line 457
        _.assertEqual(2, len(os.listdir(branchFolder(0, 1))))  # line 458
        _.createFile(2, "b")  # line 459
        sos.commit("Second", ["--force"])  # add nothing, because picky  # line 460
        _.assertEqual(1, len(os.listdir(branchFolder(0, 2))))  # line 461
        sos.add(".", "file?")  # line 462
        sos.commit("Third")  # add nothing, because picky  # line 463
        _.assertEqual(2, len(os.listdir(branchFolder(0, 3))))  # line 464
        out = wrapChannels(lambda: sos.log()).replace("\r", "")  # line 465
        _.assertIn("    r2", out)  # line 466
        _.assertIn("  * r3", out)  # line 467
        _.assertNotIn("  * r4", out)  # line 468

    def testTrackedSubfolder(_):  # line 470
        os.mkdir("." + os.sep + "sub")  # line 471
        sos.offline("trunk", ["--track"])  # line 472
        _.createFile(1, "x")  # line 473
        _.createFile(1, "x", prefix="sub")  # line 474
        sos.add(".", "file?")  # add glob pattern to track  # line 475
        sos.commit("First")  # line 476
        _.assertEqual(2, len(os.listdir(branchFolder(0, 1))))  # one new file + meta file  # line 477
        sos.add(".", "sub/file?")  # add glob pattern to track  # line 478
        sos.commit("Second")  # one new file + meta  # line 479
        _.assertEqual(2, len(os.listdir(branchFolder(0, 1))))  # one new file + meta file  # line 480
        os.unlink("file1")  # remove from basefolder  # line 481
        _.createFile(2, "y")  # line 482
        sos.rm(".", "sub/file?")  # line 483
        try:  # raises Exit. TODO test the "suggest a pattern" case  # line 484
            sos.rm(".", "sub/bla")  # raises Exit. TODO test the "suggest a pattern" case  # line 484
            _.fail()  # raises Exit. TODO test the "suggest a pattern" case  # line 484
        except:  # line 485
            pass  # line 485
        sos.commit("Third")  # line 486
        _.assertEqual(2, len(os.listdir(branchFolder(0, 2))))  # one new file + meta  # line 487
# TODO check if /file1 and sub/file1 were removed from index

    def testTrackedMode(_):  # line 490
        ''' Difference in semantics vs simple mode:
          - For remote/other branch we can only know and consider tracked files, thus ignoring all complexity stemming from handling addition of untracked files.
          - For current branch, we can take into account tracked and untracked ones, in theory, but it doesn't make sense.
        In conclusion, using the union of tracking patterns from both sides to find affected files makes sense, but disallow deleting files not present in remote branch.
    '''  # line 495
        sos.offline("test", options=["--track"])  # set up repo in tracking mode (SVN- or gitless-style)  # line 496
        _.createFile(1)  # line 497
        _.createFile("a123a")  # untracked file "a123a"  # line 498
        sos.add(".", "file?")  # add glob tracking pattern  # line 499
        sos.commit("second")  # versions "file1"  # line 500
        _.assertEqual(2, len(os.listdir(branchFolder(0, 1))))  # one new file + meta file  # line 501
        out = wrapChannels(lambda: sos.status()).replace("\r", "")  # line 502
        _.assertIn("  | ./file?", out)  # line 503

        _.createFile(2)  # untracked file "file2"  # line 505
        sos.commit("third")  # versions "file2"  # line 506
        _.assertEqual(2, len(os.listdir(branchFolder(0, 2))))  # one new file + meta file  # line 507

        os.mkdir("." + os.sep + "sub")  # line 509
        _.createFile(3, prefix="sub")  # untracked file "sub/file3"  # line 510
        sos.commit("fourth", ["--force"])  # no tracking pattern matches the subfolder  # line 511
        _.assertEqual(1, len(os.listdir(branchFolder(0, 3))))  # meta file only, no other tracked path/file  # line 512

        sos.branch("Other")  # second branch containing file1 and file2 tracked by "./file?"  # line 514
        sos.rm(".", "file?")  # remove tracking pattern, but don't touch previously created and versioned files  # line 515
        sos.add(".", "a*a")  # add tracking pattern  # line 516
        changes = sos.changes()  # should pick up addition  # line 517
        _.assertEqual(0, len(changes.modifications))  # line 518
        _.assertEqual(0, len(changes.deletions))  # not tracked anymore, but contained in version history and not removed  # line 519
        _.assertEqual(1, len(changes.additions))  # detected one addition "a123a", but won't recognize untracking files as deletion  # line 520

        sos.commit("Second_2")  # line 522
        _.assertEqual(2, len(os.listdir(branchFolder(1, 1))))  # "a123a" + meta file  # line 523
        _.assertTrue(os.path.exists("." + os.sep + "file1"))  # line 524
        _.assertTrue(os.path.exists("." + os.sep + "file2"))  # line 525

        sos.switch("test")  # go back to first branch - tracks only "file?", but not "a*a"  # line 527
        _.assertTrue(os.path.exists("." + os.sep + "file1"))  # line 528
        _.assertTrue(os.path.exists("." + os.sep + "a123a"))  # should not have been touched so far  # line 529

        sos.update("Other")  # integrate tracked files and tracking pattern from second branch into working state of master branch  # line 531
        _.assertTrue(os.path.exists("." + os.sep + "file1"))  # line 532
        _.assertTrue(os.path.exists("." + os.sep + "a123a"))  # line 533

        _.createFile("axxxa")  # new file that should be tracked on "test" now that we integrated "Other"  # line 535
        sos.commit("fifth")  # create new revision after integrating updates from second branch  # line 536
        _.assertEqual(3, len(os.listdir(branchFolder(0, 4))))  # one new file from other branch + one new in current folder + meta file  # line 537
        sos.switch("Other")  # switch back to just integrated branch that tracks only "a*a" - shouldn't do anything  # line 538
        _.assertTrue(os.path.exists("." + os.sep + "file1"))  # line 539
        _.assertTrue(os.path.exists("." + os.sep + "a123a"))  # line 540
        _.assertFalse(os.path.exists("." + os.sep + "axxxa"))  # because tracked in both branches, but not present in other -> delete in file tree TODO document  # line 541
# TODO test switch --meta

    def testLsTracked(_):  # line 544
        sos.offline("test", options=["--track"])  # set up repo in tracking mode (SVN- or gitless-style)  # line 545
        _.createFile(1)  # line 546
        _.createFile("foo")  # line 547
        sos.add(".", "file*")  # capture one file  # line 548
        out = sos.safeSplit(wrapChannels(lambda: sos.ls()).replace("\r", ""), "\n")  # line 549
        _.assertInAny('TRK file1 by "./file*"', out)  # line 550
        _.assertNotInAny('    file1 by "./file*"', out)  # line 551
        _.assertInAny("    foo", out)  # line 552

    def testCompression(_):  # line 554
        _.createFile(1)  # line 555
        sos.offline("master", options=["--plain", "--force"])  # line 556
        _.assertTrue(_.existsFile(branchFolder(0, 0) + os.sep + "b9ee10a87f612e299a6eb208210bc0898092a64c48091327cc2aaeee9b764ffa", b"x" * 10))  # line 557
        setRepoFlag("compress", True)  # was plain = uncompressed before  # line 558
        _.createFile(2)  # line 559
        sos.commit("Added file2")  # line 560
        _.assertTrue(_.existsFile(branchFolder(0, 1) + os.sep + "03b69bc801ae11f1ff2a71a50f165996d0ad681b4f822df13329a27e53f0fcd2"))  # exists  # line 561
        _.assertFalse(_.existsFile(branchFolder(0, 1) + os.sep + "03b69bc801ae11f1ff2a71a50f165996d0ad681b4f822df13329a27e53f0fcd2", b"x" * 10))  # but is compressed instead  # line 562

    def testConfigVariations(_):  # line 564
        def makeRepo():  # line 565
            try:  # line 566
                os.unlink("file1")  # line 566
            except:  # line 567
                pass  # line 567
            sos.offline("master", options=["--plain", "--force"])  # line 568
            _.createFile(1)  # line 569
            sos.commit("Added file1")  # line 570
        sos.config("set", ["strict", "on"])  # line 571
        makeRepo()  # line 572
        _.assertTrue(checkRepoFlag("strict", True))  # line 573
        sos.config("set", ["strict", "off"])  # line 574
        makeRepo()  # line 575
        _.assertTrue(checkRepoFlag("strict", False))  # line 576
        sos.config("set", ["strict", "yes"])  # line 577
        makeRepo()  # line 578
        _.assertTrue(checkRepoFlag("strict", True))  # line 579
        sos.config("set", ["strict", "no"])  # line 580
        makeRepo()  # line 581
        _.assertTrue(checkRepoFlag("strict", False))  # line 582
        sos.config("set", ["strict", "1"])  # line 583
        makeRepo()  # line 584
        _.assertTrue(checkRepoFlag("strict", True))  # line 585
        sos.config("set", ["strict", "0"])  # line 586
        makeRepo()  # line 587
        _.assertTrue(checkRepoFlag("strict", False))  # line 588
        sos.config("set", ["strict", "true"])  # line 589
        makeRepo()  # line 590
        _.assertTrue(checkRepoFlag("strict", True))  # line 591
        sos.config("set", ["strict", "false"])  # line 592
        makeRepo()  # line 593
        _.assertTrue(checkRepoFlag("strict", False))  # line 594
        sos.config("set", ["strict", "enable"])  # line 595
        makeRepo()  # line 596
        _.assertTrue(checkRepoFlag("strict", True))  # line 597
        sos.config("set", ["strict", "disable"])  # line 598
        makeRepo()  # line 599
        _.assertTrue(checkRepoFlag("strict", False))  # line 600
        sos.config("set", ["strict", "enabled"])  # line 601
        makeRepo()  # line 602
        _.assertTrue(checkRepoFlag("strict", True))  # line 603
        sos.config("set", ["strict", "disabled"])  # line 604
        makeRepo()  # line 605
        _.assertTrue(checkRepoFlag("strict", False))  # line 606
        try:  # line 607
            sos.config("set", ["strict", "nope"])  # line 607
            _.fail()  # line 607
        except:  # line 608
            pass  # line 608

    def testLsSimple(_):  # line 610
        _.createFile(1)  # line 611
        _.createFile("foo")  # line 612
        _.createFile("ign1")  # line 613
        _.createFile("ign2")  # line 614
        sos.offline("test")  # set up repo in tracking mode (SVN- or gitless-style)  # line 615
        sos.config("set", ["ignores", "ign1"])  # define an ignore pattern  # line 616
        sos.config("add", ["ignores", "ign2"])  # define an ignore pattern  # line 617
        sos.config("set", ["ignoresWhitelist", "ign1;ign2"])  # define a list of ignore patterns  # line 618
        out = wrapChannels(lambda: sos.config("show")).replace("\r", "")  # line 619
        _.assertIn("ignores => ['ign1', 'ign2']", out)  # line 620
        out = sos.safeSplit(wrapChannels(lambda: sos.ls()).replace("\r", ""), "\n")  # line 621
        _.assertInAny('    file1', out)  # line 622
        _.assertInAny('    ign1', out)  # line 623
        _.assertInAny('    ign2', out)  # line 624
        try:  # line 625
            sos.config("rm", ["foo", "bar"])  # line 625
            _.fail()  # line 625
        except:  # line 626
            pass  # line 626
        try:  # line 627
            sos.config("rm", ["ignores", "foo"])  # line 627
            _.fail()  # line 627
        except:  # line 628
            pass  # line 628
        sos.config("rm", ["ignores", "ign1"])  # line 629
        sos.config("unset", ["ignoresWhitelist"])  # remove ignore pattern  # line 630
        out = sos.safeSplit(wrapChannels(lambda: sos.ls()).replace("\r", ""), "\n")  # line 631
        _.assertInAny('    ign1', out)  # line 632
        _.assertInAny('IGN ign2', out)  # line 633
        _.assertNotInAny('    ign2', out)  # line 634

    def testWhitelist(_):  # line 636
# TODO test same for simple mode
        _.createFile(1)  # line 638
        sos.defaults.ignores[:] = ["file*"]  # replace in-place  # line 639
        sos.offline("xx", ["--track", "--strict"])  # because nothing to commit due to ignore pattern  # line 640
        sos.add(".", "file*")  # add tracking pattern for "file1"  # line 641
        sos.commit(options=["--force"])  # attempt to commit the file  # line 642
        _.assertEqual(1, len(os.listdir(branchFolder(0, 1))))  # only meta data, file1 was ignored  # line 643
        try:  # Exit because dirty  # line 644
            sos.online()  # Exit because dirty  # line 644
            _.fail()  # Exit because dirty  # line 644
        except:  # exception expected  # line 645
            pass  # exception expected  # line 645
        _.createFile("x2")  # add another change  # line 646
        sos.add(".", "x?")  # add tracking pattern for "file1"  # line 647
        try:  # force beyond dirty flag check  # line 648
            sos.online(["--force"])  # force beyond dirty flag check  # line 648
            _.fail()  # force beyond dirty flag check  # line 648
        except:  # line 649
            pass  # line 649
        sos.online(["--force", "--force"])  # force beyond file tree modifications check  # line 650
        _.assertFalse(os.path.exists(sos.metaFolder))  # line 651

        _.createFile(1)  # line 653
        sos.defaults.ignoresWhitelist[:] = ["file*"]  # line 654
        sos.offline("xx", ["--track"])  # line 655
        sos.add(".", "file*")  # line 656
        sos.commit()  # should NOT ask for force here  # line 657
        _.assertEqual(2, len(os.listdir(branchFolder(0, 1))))  # meta data and "file1", file1 was whitelisted  # line 658

    def testRemove(_):  # line 660
        _.createFile(1, "x" * 100)  # line 661
        sos.offline("trunk")  # line 662
        try:  # line 663
            sos.delete("trunk")  # line 663
            _fail()  # line 663
        except:  # line 664
            pass  # line 664
        _.createFile(2, "y" * 10)  # line 665
        sos.branch("added")  # line 666
        sos.delete("trunk")  # line 667
        _.assertEqual(2, len(os.listdir("." + os.sep + sos.metaFolder)))  # meta data file and "b1"  # line 668
        _.assertTrue(os.path.exists("." + os.sep + sos.metaFolder + os.sep + "b1"))  # line 669
        _.assertFalse(os.path.exists("." + os.sep + sos.metaFolder + os.sep + "b0"))  # line 670
        sos.branch("next")  # line 671
        _.createFile(3, "y" * 10)  # make a change  # line 672
        sos.delete("added", "--force")  # should succeed  # line 673

    def testUsage(_):  # line 675
        sos.usage()  # line 676

    def testDiff(_):  # line 678
        sos.offline(options=["--strict"])  # line 679
        _.createFile(1)  # line 680
        sos.commit()  # line 681
        _.createFile(1, "sdfsdgfsdf")  # line 682
        time.sleep(FS_PRECISION)  # line 683
        sos.commit()  # TODO this sometimes fails "nothing to commit"  # line 684
        _.createFile(1, "foobar")  # line 685
        _.assertAllIn(["MOD ./file1", "DIF ./file1", "- | 0000 |xxxxxxxxxx|", "+ | 0000 |foobar|"], wrapChannels(lambda: sos.diff("/-2")))  # second last  # line 686

    def testFindBase(_):  # line 688
        old = os.getcwd()  # line 689
        try:  # line 690
            os.mkdir("." + os.sep + ".git")  # line 691
            os.makedirs("." + os.sep + "a" + os.sep + sos.metaFolder)  # line 692
            os.makedirs("." + os.sep + "a" + os.sep + "b")  # line 693
            os.chdir("a" + os.sep + "b")  # line 694
            s, vcs, cmd = sos.findSosVcsBase()  # line 695
            _.assertIsNotNone(s)  # line 696
            _.assertIsNotNone(vcs)  # line 697
            _.assertEqual("git", cmd)  # line 698
        finally:  # line 699
            os.chdir(old)  # line 699


if __name__ == '__main__':  # line 702
    logging.basicConfig(level=logging.DEBUG if '-v' in sys.argv or os.getenv("DEBUG", "false").strip().lower() == "true" or os.getenv("CI", "false").strip().lower() == "true" else logging.INFO, stream=sys.stderr, format="%(asctime)-23s %(levelname)-8s %(name)s:%(lineno)d | %(message)s" if '-v' in sys.argv or os.getenv("DEBUG", "false") == "true" else "%(message)s")  # line 703
    if configr:  # line 704
        c = configr.Configr("sos")  # line 705
        c.loadSettings()  # line 705
        if len(c.keys()) > 0:  # line 706
            sos.Exit("Cannot run test suite with existing local SOS user configuration (would affect results)")  # line 706
    unittest.main(testRunner=debugTestRunner() if '-v' in sys.argv and not os.getenv("CI", "false").lower() == "true" else None)  # warnings = "ignore")  # line 707
