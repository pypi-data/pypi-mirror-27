#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# __coconut_hash__ = 0x1a3e53e3

# Compiled with Coconut version 1.3.1-post_dev8 [Dead Parrot]

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
    return "." + os.sep + sos.utility.metaFolder + os.sep + "b%d" % branch + os.sep + "r%d" % revision  # line 54

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
    with open(sos.utility.metaFolder + os.sep + sos.utility.metaFile, "r") as fd:  # line 73
        flags, branches = json.loads(fd.read())  # line 73
    flags[name] = value  # line 74
    with open(sos.utility.metaFolder + os.sep + sos.utility.metaFile, "w") as fd:  # line 75
        fd.write(json.dumps((flags, branches)))  # line 75

def checkRepoFlag(name: 'str', flag: 'bool') -> 'bool':  # line 77
    with open(sos.utility.metaFolder + os.sep + sos.utility.metaFile, "r") as fd:  # line 78
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
        sos.add("./sub", "file?")  # this doesn't work as direct call won't invoke getRoot and therefore won't chdir virtually into that folder  # line 183
        sos.commit("test")  # line 184
        _.assertEqual(2, len(os.listdir(os.path.join(sos.utility.metaFolder, "b0", "r1"))))  # sub/file1 was added  # line 185
        _.createFile(1)  # line 186
        try:  # should not commit anything, as the file in base folder doesn't match the path pattern  # line 187
            sos.commit("nothing")  # should not commit anything, as the file in base folder doesn't match the path pattern  # line 187
            _.fail()  # should not commit anything, as the file in base folder doesn't match the path pattern  # line 187
        except:  # line 188
            pass  # line 188

    def testComputeSequentialPathSet(_):  # line 190
        os.makedirs(branchFolder(0, 0))  # line 191
        os.makedirs(branchFolder(0, 1))  # line 192
        os.makedirs(branchFolder(0, 2))  # line 193
        os.makedirs(branchFolder(0, 3))  # line 194
        os.makedirs(branchFolder(0, 4))  # line 195
        m = sos.Metadata(os.getcwd())  # line 196
        m.branch = 0  # line 197
        m.commit = 2  # line 198
        m.saveBranches()  # line 199
        m.paths = {"./a": sos.PathInfo("", 0, 0, "")}  # line 200
        m.saveCommit(0, 0)  # initial  # line 201
        m.paths["./a"] = sos.PathInfo("", 1, 0, "")  # line 202
        m.saveCommit(0, 1)  # mod  # line 203
        m.paths["./b"] = sos.PathInfo("", 0, 0, "")  # line 204
        m.saveCommit(0, 2)  # add  # line 205
        m.paths["./a"] = sos.PathInfo("", None, 0, "")  # line 206
        m.saveCommit(0, 3)  # del  # line 207
        m.paths["./a"] = sos.PathInfo("", None, 0, "")  # line 208
        m.saveCommit(0, 4)  # readd  # line 209
        m.commits = {i: sos.CommitInfo(i, 0, None) for i in range(5)}  # line 210
        m.saveBranch(0)  # line 211
        m.computeSequentialPathSet(0, 4)  # line 212
        _.assertEqual(2, len(m.paths))  # line 213

    def testParseRevisionString(_):  # line 215
        m = sos.Metadata(os.getcwd())  # line 216
        m.branch = 1  # line 217
        m.commits = {0: 0, 1: 1, 2: 2}  # line 218
        _.assertEqual((1, 3), m.parseRevisionString("3"))  # line 219
        _.assertEqual((2, 3), m.parseRevisionString("2/3"))  # line 220
        _.assertEqual((1, -1), m.parseRevisionString(None))  # line 221
        _.assertEqual((2, -1), m.parseRevisionString("2/"))  # line 222
        _.assertEqual((1, -2), m.parseRevisionString("/-2"))  # line 223
        _.assertEqual((1, -1), m.parseRevisionString("/"))  # line 224

    def testOfflineEmpty(_):  # line 226
        os.mkdir("." + os.sep + sos.utility.metaFolder)  # line 227
        try:  # line 228
            sos.offline("trunk")  # line 228
            _.fail()  # line 228
        except SystemExit:  # line 229
            pass  # line 229
        os.rmdir("." + os.sep + sos.utility.metaFolder)  # line 230
        sos.offline("test")  # line 231
        _.assertIn(sos.utility.metaFolder, os.listdir("."))  # line 232
        _.assertAllIn(["b0", sos.utility.metaFile], os.listdir("." + os.sep + sos.utility.metaFolder))  # line 233
        _.assertAllIn(["r0", sos.utility.metaFile], os.listdir("." + os.sep + sos.utility.metaFolder + os.sep + "b0"))  # line 234
        _.assertEqual(2, len(os.listdir("." + os.sep + sos.utility.metaFolder)))  # only branch folder and meta data file  # line 235
        _.assertEqual(2, len(os.listdir("." + os.sep + sos.utility.metaFolder + os.sep + "b0")))  # only commit folder and meta data file  # line 236
        _.assertEqual(1, len(os.listdir(branchFolder(0, 0))))  # only meta data file  # line 237

    def testOfflineWithFiles(_):  # line 239
        _.createFile(1, "x" * 100)  # line 240
        _.createFile(2)  # line 241
        sos.offline("test")  # line 242
        _.assertAllIn(["file1", "file2", sos.utility.metaFolder], os.listdir("."))  # line 243
        _.assertAllIn(["b0", sos.utility.metaFile], os.listdir("." + os.sep + sos.utility.metaFolder))  # line 244
        _.assertAllIn(["r0", sos.utility.metaFile], os.listdir("." + os.sep + sos.utility.metaFolder + os.sep + "b0"))  # line 245
        _.assertAllIn([sos.utility.metaFile, "03b69bc801ae11f1ff2a71a50f165996d0ad681b4f822df13329a27e53f0fcd2", "b9ee10a87f612e299a6eb208210bc0898092a64c48091327cc2aaeee9b764ffa"], os.listdir("." + os.sep + sos.utility.metaFolder + os.sep + "b0" + os.sep + "r0"))  # line 246
        _.assertEqual(2, len(os.listdir("." + os.sep + sos.utility.metaFolder)))  # only branch folder and meta data file  # line 247
        _.assertEqual(2, len(os.listdir("." + os.sep + sos.utility.metaFolder + os.sep + "b0")))  # only commit folder and meta data file  # line 248
        _.assertEqual(3, len(os.listdir(branchFolder(0, 0))))  # only meta data file plus branch base file copies  # line 249

    def testBranch(_):  # line 251
        _.createFile(1, "x" * 100)  # line 252
        _.createFile(2)  # line 253
        sos.offline("test")  # b0/r0  # line 254
        sos.branch("other")  # b1/r0  # line 255
        _.assertAllIn(["b0", "b1", sos.utility.metaFile], os.listdir("." + os.sep + sos.utility.metaFolder))  # line 256
        _.assertEqual(list(sorted(os.listdir("." + os.sep + sos.utility.metaFolder + os.sep + "b0"))), list(sorted(os.listdir("." + os.sep + sos.utility.metaFolder + os.sep + "b1"))))  # line 257
        _.assertEqual(list(sorted(os.listdir(branchFolder(0, 0)))), list(sorted(os.listdir(branchFolder(1, 0)))))  # line 259
        _.createFile(1, "z")  # modify file  # line 261
        sos.branch()  # b2/r0  branch to unnamed branch with modified file tree contents  # line 262
        _.assertNotEqual(os.stat("." + os.sep + sos.utility.metaFolder + os.sep + "b1" + os.sep + "r0" + os.sep + "b9ee10a87f612e299a6eb208210bc0898092a64c48091327cc2aaeee9b764ffa").st_size, os.stat("." + os.sep + sos.utility.metaFolder + os.sep + "b2" + os.sep + "r0" + os.sep + "b9ee10a87f612e299a6eb208210bc0898092a64c48091327cc2aaeee9b764ffa").st_size)  # line 263
        _.createFile(3, "z")  # line 265
        sos.branch("from_last_revision", ["--last", "--stay"])  # b3/r0 create copy of other file1,file2 and don't switch  # line 266
        _.assertEqual(list(sorted(os.listdir("." + os.sep + sos.utility.metaFolder + os.sep + "b3" + os.sep + "r0"))), list(sorted(os.listdir("." + os.sep + sos.utility.metaFolder + os.sep + "b2" + os.sep + "r0"))))  # line 267
# Check sos.status output which branch is marked


    def testComittingAndChanges(_):  # line 272
        _.createFile(1, "x" * 100)  # line 273
        _.createFile(2)  # line 274
        sos.offline("test")  # line 275
        changes = sos.changes()  # line 276
        _.assertEqual(0, len(changes.additions))  # line 277
        _.assertEqual(0, len(changes.deletions))  # line 278
        _.assertEqual(0, len(changes.modifications))  # line 279
        _.createFile(1, "z")  # size change  # line 280
        changes = sos.changes()  # line 281
        _.assertEqual(0, len(changes.additions))  # line 282
        _.assertEqual(0, len(changes.deletions))  # line 283
        _.assertEqual(1, len(changes.modifications))  # line 284
        sos.commit("message")  # line 285
        _.assertAllIn(["r0", "r1", sos.utility.metaFile], os.listdir("." + os.sep + sos.utility.metaFolder + os.sep + "b0"))  # line 286
        _.assertAllIn([sos.utility.metaFile, "b9ee10a87f612e299a6eb208210bc0898092a64c48091327cc2aaeee9b764ffa"], os.listdir(branchFolder(0, 1)))  # line 287
        _.assertEqual(2, len(os.listdir(branchFolder(0, 1))))  # no further files, only the modified one  # line 288
        _.assertEqual(1, len(sos.changes("/0").modifications))  # vs. explicit revision on current branch  # line 289
        _.assertEqual(1, len(sos.changes("0/0").modifications))  # vs. explicit branch/revision  # line 290
        _.createFile(1, "")  # modify to empty file, mentioned in meta data, but not stored as own file  # line 291
        os.unlink("file2")  # line 292
        changes = sos.changes()  # line 293
        _.assertEqual(0, len(changes.additions))  # line 294
        _.assertEqual(1, len(changes.deletions))  # line 295
        _.assertEqual(1, len(changes.modifications))  # line 296
        sos.commit("modified")  # line 297
        _.assertEqual(1, len(os.listdir(branchFolder(0, 2))))  # no additional files, only mentions in metadata  # line 298
        try:  # expecting Exit due to no changes  # line 299
            sos.commit("nothing")  # expecting Exit due to no changes  # line 299
            _.fail()  # expecting Exit due to no changes  # line 299
        except:  # line 300
            pass  # line 300

    def testGetBranch(_):  # line 302
        m = sos.Metadata(os.getcwd())  # line 303
        m.branch = 1  # current branch  # line 304
        m.branches = {0: sos.BranchInfo(0, 0, "trunk")}  # line 305
        _.assertEqual(27, m.getBranchByName(27))  # line 306
        _.assertEqual(0, m.getBranchByName("trunk"))  # line 307
        _.assertEqual(1, m.getBranchByName(""))  # split from "/"  # line 308
        _.assertIsNone(m.getBranchByName("unknown"))  # line 309
        m.commits = {0: sos.CommitInfo(0, 0, "bla")}  # line 310
        _.assertEqual(13, m.getRevisionByName("13"))  # line 311
        _.assertEqual(0, m.getRevisionByName("bla"))  # line 312
        _.assertEqual(-1, m.getRevisionByName(""))  # split from "/"  # line 313

    def testTagging(_):  # line 315
        m = sos.Metadata(os.getcwd())  # line 316
        sos.offline()  # line 317
        _.createFile(111)  # line 318
        sos.commit("tag", ["--tag"])  # line 319
        _.createFile(2)  # line 320
        try:  # line 321
            sos.commit("tag")  # line 321
            _.fail()  # line 321
        except:  # line 322
            pass  # line 322
        sos.commit("tag-2", ["--tag"])  # line 323

    def testSwitch(_):  # line 325
        _.createFile(1, "x" * 100)  # line 326
        _.createFile(2, "y")  # line 327
        sos.offline("test")  # file1-2  in initial branch commit  # line 328
        sos.branch("second")  # file1-2  switch, having same files  # line 329
        sos.switch("0")  # no change  switch back, no problem  # line 330
        sos.switch("second")  # no change  # switch back, no problem  # line 331
        _.createFile(3, "y")  # generate a file  # line 332
        try:  # uncommited changes detected  # line 333
            sos.switch("test")  # uncommited changes detected  # line 333
            _.fail()  # uncommited changes detected  # line 333
        except SystemExit:  # line 334
            pass  # line 334
        sos.commit("Finish")  # file1-3  commit third file into branch second  # line 335
        sos.changes()  # line 336
        sos.switch("test")  # file1-2, remove file3 from file tree  # line 337
        _.assertFalse(_.existsFile(3))  # removed when switching back to test  # line 338
        out = wrapChannels(lambda: sos.status()).replace("\r", "")  # line 339
        _.assertIn("  * b00   'test'", out)  # line 340
        _.assertIn("    b01 'second'", out)  # line 341
        _.assertIn("(dirty)", out)  # one branch has commits  # line 342
        _.assertIn("(in sync)", out)  # the other doesn't  # line 343
        _.createFile(4, "xy")  # generate a file  # line 344
        sos.switch("second", "--force")  # avoids warning on uncommited changes, but keeps file4  # line 345
        _.assertFalse(_.existsFile(4))  # removed when forcedly switching back to test  # line 346
        _.assertTrue(_.existsFile(3))  # was restored from branch's revision r1  # line 347
        os.unlink("." + os.sep + "file1")  # remove old file1  # line 348
        sos.switch("test", "--force")  # should restore file1 and remove file3  # line 349
        _.assertTrue(_.existsFile(1))  # was restored from branch's revision r1  # line 350
        _.assertFalse(_.existsFile(3))  # was restored from branch's revision r1  # line 351

    def testAutoDetectVCS(_):  # line 353
        os.mkdir(".git")  # line 354
        sos.offline(sos.vcsBranches[sos.findSosVcsBase()[2]])  # create initial branch  # line 355
        with open(sos.utility.metaFolder + os.sep + sos.utility.metaFile, "r") as fd:  # line 356
            meta = fd.read()  # line 356
        _.assertTrue("\"master\"" in meta)  # line 357
        os.rmdir(".git")  # line 358

    def testUpdate(_):  # line 360
        sos.offline("trunk")  # create initial branch b0/r0  # line 361
        _.createFile(1, "x" * 100)  # line 362
        sos.commit("second")  # create b0/r1  # line 363

        sos.switch("/0")  # go back to b0/r0 - deletes file1  # line 365
        _.assertFalse(_.existsFile(1))  # line 366

        sos.update("/1")  # recreate file1  # line 368
        _.assertTrue(_.existsFile(1))  # line 369

        sos.commit("third", ["--force"])  # force because nothing to commit. should create r2 with same contents as r1, but as differential from r1, not from r0 (= no changes in meta folder)  # line 371
        _.assertTrue(os.path.exists(branchFolder(0, 2)))  # line 372
        _.assertTrue(os.path.exists(branchFolder(0, 2) + os.sep + sos.utility.metaFile))  # line 373
        _.assertEqual(1, len(os.listdir(branchFolder(0, 2))))  # only meta data file, no differential files  # line 374

        sos.update("/1")  # do nothing, as nothing has changed  # line 376
        _.assertTrue(_.existsFile(1))  # line 377

        _.createFile(2, "y" * 100)  # line 379
#    out = wrapChannels(() -> sos.branch("other"))  # won't comply as there are changes
#    _.assertIn("--force", out)
        sos.branch("other", ["--force"])  # automatically including file 2 (as we are in simple mode)  # line 382
        _.assertTrue(_.existsFile(2))  # line 383
        sos.update("trunk", ["--add"])  # only add stuff  # line 384
        _.assertTrue(_.existsFile(2))  # line 385
        sos.update("trunk")  # nothing to do  # line 386
        _.assertFalse(_.existsFile(2))  # removes file not present in original branch  # line 387

        theirs = b"a\nb\nc\nd\ne\nf\ng\nh\nx\nx\nj\nk"  # line 389
        _.createFile(10, theirs)  # line 390
        mine = b"a\nc\nd\ne\ng\nf\nx\nh\ny\ny\nj"  # missing "b", inserted g, modified g->x, replace x/x -> y/y, removed k  # line 391
        _.createFile(11, mine)  # line 392
        _.assertEqual(b"a\nb\nc\nd\ne\nf\ng\nh\nx\nx\nj\nk", sos.merge(filename="." + os.sep + "file10", intoname="." + os.sep + "file11", mergeOperation=sos.MergeOperation.BOTH, conflictResolution=sos.ConflictResolution.THEIRS))  # completely recreated other file  # line 393
        _.assertEqual(b"a\nb\nc\nd\ne\ng\nf\ng\nx\nh\nx\nx\ny\ny\nj\nk", sos.merge(filename="." + os.sep + "file10", intoname="." + os.sep + "file11", mergeOperation=sos.MergeOperation.INSERT, conflictResolution=sos.ConflictResolution.MINE))  # line 394

    def testUpdate2(_):  # line 396
        _.createFile("test.txt", "x" * 10)  # line 397
        sos.offline("trunk", ["--strict"])  # use strict mode, as timestamp differences are too small for testing  # line 398
        sos.branch("mod")  # line 399
        _.createFile("test.txt", "x" * 5 + "y" * 5)  # line 400
        time.sleep(FS_PRECISION)  # line 401
        sos.commit("mod")  # create b0/r1  # line 402
        sos.switch("trunk", ["--force"])  # should replace contents, force in case some other files were modified (e.g. during working on the code) TODO investigate more  # line 403
        with open("test.txt", "rb") as fd:  # line 404
            _.assertEqual(b"x" * 10, fd.read())  # line 404
        sos.update("mod", ["--theirs"])  # integrate changes TODO same with ask -> theirs  # line 405
        with open("test.txt", "rb") as fd:  # line 406
            _.assertEqual(b"x" * 5 + b"y" * 5, fd.read())  # line 406
        _.createFile("test.txt", "x" * 10)  # line 407
        mockInput(["t"], lambda: sos.update("mod", ["--ask"]))  # same as above with interaction -> theirs  # line 408
        with open("test.txt", "rb") as fd:  # line 409
            _.assertEqual(b"x" * 5 + b"y" * 5, fd.read())  # line 409

    def testIsTextType(_):  # line 411
        m = sos.Metadata(".")  # line 412
        m.c.texttype = ["*.x", "*.md", "*.md.*"]  # line 413
        m.c.bintype = ["*.md.confluence"]  # line 414
        _.assertTrue(m.isTextType("ab.txt"))  # line 415
        _.assertTrue(m.isTextType("./ab.txt"))  # line 416
        _.assertTrue(m.isTextType("bc/ab.txt"))  # line 417
        _.assertFalse(m.isTextType("bc/ab."))  # line 418
        _.assertTrue(m.isTextType("23_3.x.x"))  # line 419
        _.assertTrue(m.isTextType("dfg/dfglkjdf7/test.md"))  # line 420
        _.assertTrue(m.isTextType("./test.md.pdf"))  # line 421
        _.assertFalse(m.isTextType("./test_a.md.confluence"))  # line 422

    def testEolDet(_):  # line 424
        _.assertEqual(b"\n", sos.eoldet(b"a\nb"))  # line 425
        _.assertEqual(b"\r\n", sos.eoldet(b"a\r\nb\r\n"))  # line 426
        _.assertEqual(b"\r", sos.eoldet(b"\ra\rb"))  # line 427
        _.assertAllIn(["Inconsistent", "with "], wrapChannels(lambda: _.assertEqual(b"\n", sos.eoldet(b"\r\na\r\nb\n"))))  # line 428
        _.assertAllIn(["Inconsistent", "without"], wrapChannels(lambda: _.assertEqual(b"\n", sos.eoldet(b"\ra\nnb\n"))))  # line 429
        _.assertIsNone(sos.eoldet(b""))  # line 430
        _.assertIsNone(sos.eoldet(b"sdf"))  # line 431

    def testMerge(_):  # line 433
        a = b"a\nb\ncc\nd"  # line 434
        b = b"a\nb\nee\nd"  # line 435
        _.assertEqual(b"a\nb\ncc\nee\nd", sos.merge(a, b, mergeOperation=sos.MergeOperation.INSERT))  # means insert changes from a into b, but don't replace  # line 436
        _.assertEqual(b"a\nb\nd", sos.merge(a, b, mergeOperation=sos.MergeOperation.REMOVE))  # line 437
        _.assertEqual(b"a\nb\ncc\nd", sos.merge(a, b, mergeOperation=sos.MergeOperation.BOTH))  # line 438
# Now test intra-line merging without conflicts
        _.assertEqual(b"a\nbc d\ne", sos.merge(b"a\nbc d\ne", b"a\nbcd\ne", mergeOperation=sos.MergeOperation.INSERT))  # because it's a deletion ['  a', '- bc d', '?   -\n', '+ bcd', '  e']  # line 440
        _.assertEqual(b"a\nbcd\ne", sos.merge(b"a\nbc d\ne", b"a\nbcd\ne", mergeOperation=sos.MergeOperation.REMOVE))  # ['  a', '- bc d', '?   -\n', '+ bcd', '  e']  # line 441
        _.assertEqual(b"a\nbc d\ne", sos.merge(b"a\nbcd\ne", b"a\nbc d\ne", mergeOperation=sos.MergeOperation.INSERT))  # nothing to insert  # line 442
        _.assertEqual(b"a\nbcd\ne", sos.merge(b"a\nbcd\ne", b"a\nbc d\ne", mergeOperation=sos.MergeOperation.REMOVE))  # remove space  # line 443
# Test with change + insert (conflict)
        _.assertEqual(b"a\nb fdd d\ne", sos.merge(b"a\nb cd d\ne", b"a\nb fdd d\ne", conflictResolution=sos.ConflictResolution.MINE))  # line 445
        _.assertEqual(b"a\nb cd d\ne", sos.merge(b"a\nb cd d\ne", b"a\nb fdd d\ne", conflictResolution=sos.ConflictResolution.THEIRS))  # ['  a', '- b cd d', '?   ^\n', '+ b fdd d', '?   ^^\n', '  e']  # line 446
        _.assertEqual(b"a\nb fdd d\ne", mockInput(["i"], lambda: sos.merge(b"a\nb cd d\ne", b"a\nb fdd d\ne", conflictResolution=sos.ConflictResolution.ASK)))  # ['  a', '- b cd d', '?   ^\n', '+ b fdd d', '?   ^^\n', '  e']  # line 447
        _.assertEqual(b"a\nb cd d\ne", mockInput(["t"], lambda: sos.merge(b"a\nb cd d\ne", b"a\nb fdd d\ne", conflictResolution=sos.ConflictResolution.ASK)))  # ['  a', '- b cd d', '?   ^\n', '+ b fdd d', '?   ^^\n', '  e']  # line 448
        _.assertEqual(b"abbc", sos.merge(b"abbc", b"addc", mergeOperation=sos.MergeOperation.BOTH, conflictResolution=sos.ConflictResolution.THEIRS))  # line 449
        _.assertEqual(b"a\nbb\nc", sos.merge(b"a\nbb\nc", b"a\ndd\nc", mergeOperation=sos.MergeOperation.BOTH, conflictResolution=sos.ConflictResolution.THEIRS))  # line 450
        _.assertIn("Differing EOL-styles", wrapChannels(lambda: sos.merge(b"a\nb", b"a\r\nb")))  # expect warning  # line 451
        _.assertIn(b"a\r\nb", sos.merge(b"a\nb", b"a\r\nb"))  # in doubt, use "mine" CR-LF  # line 452

    def testPickyMode(_):  # line 454
        sos.offline("trunk", ["--picky"])  # line 455
        sos.add(".", "file?", ["--force"])  # line 456
        _.createFile(1, "aa")  # line 457
        sos.commit("First")  # add one file  # line 458
        _.assertEqual(2, len(os.listdir(branchFolder(0, 1))))  # line 459
        _.createFile(2, "b")  # line 460
        sos.commit("Second", ["--force"])  # add nothing, because picky  # line 461
        _.assertEqual(1, len(os.listdir(branchFolder(0, 2))))  # line 462
        sos.add(".", "file?")  # line 463
        sos.commit("Third")  # add nothing, because picky  # line 464
        _.assertEqual(2, len(os.listdir(branchFolder(0, 3))))  # line 465
        out = wrapChannels(lambda: sos.log([])).replace("\r", "")  # line 466
        _.assertIn("    r2", out)  # line 467
        _.assertIn("  * r3", out)  # line 468
        _.assertNotIn("  * r4", out)  # line 469

    def testTrackedSubfolder(_):  # line 471
        os.mkdir("." + os.sep + "sub")  # line 472
        sos.offline("trunk", ["--track"])  # line 473
        _.createFile(1, "x")  # line 474
        _.createFile(1, "x", prefix="sub")  # line 475
        sos.add(".", "file?")  # add glob pattern to track  # line 476
        sos.commit("First")  # line 477
        _.assertEqual(2, len(os.listdir(branchFolder(0, 1))))  # one new file + meta file  # line 478
        sos.add(".", "sub/file?")  # add glob pattern to track  # line 479
        sos.commit("Second")  # one new file + meta  # line 480
        _.assertEqual(2, len(os.listdir(branchFolder(0, 1))))  # one new file + meta file  # line 481
        os.unlink("file1")  # remove from basefolder  # line 482
        _.createFile(2, "y")  # line 483
        sos.rm(".", "sub/file?")  # line 484
        try:  # raises Exit. TODO test the "suggest a pattern" case  # line 485
            sos.rm(".", "sub/bla")  # raises Exit. TODO test the "suggest a pattern" case  # line 485
            _.fail()  # raises Exit. TODO test the "suggest a pattern" case  # line 485
        except:  # line 486
            pass  # line 486
        sos.commit("Third")  # line 487
        _.assertEqual(2, len(os.listdir(branchFolder(0, 2))))  # one new file + meta  # line 488
# TODO check if /file1 and sub/file1 were removed from index

    def testTrackedMode(_):  # line 491
        ''' Difference in semantics vs simple mode:
          - For remote/other branch we can only know and consider tracked files, thus ignoring all complexity stemming from handling addition of untracked files.
          - For current branch, we can take into account tracked and untracked ones, in theory, but it doesn't make sense.
        In conclusion, using the union of tracking patterns from both sides to find affected files makes sense, but disallow deleting files not present in remote branch.
    '''  # line 496
        sos.offline("test", options=["--track"])  # set up repo in tracking mode (SVN- or gitless-style)  # line 497
        _.createFile(1)  # line 498
        _.createFile("a123a")  # untracked file "a123a"  # line 499
        sos.add(".", "file?")  # add glob tracking pattern  # line 500
        sos.commit("second")  # versions "file1"  # line 501
        _.assertEqual(2, len(os.listdir(branchFolder(0, 1))))  # one new file + meta file  # line 502
        out = wrapChannels(lambda: sos.status()).replace("\r", "")  # line 503
        _.assertIn("  | ./file?", out)  # line 504

        _.createFile(2)  # untracked file "file2"  # line 506
        sos.commit("third")  # versions "file2"  # line 507
        _.assertEqual(2, len(os.listdir(branchFolder(0, 2))))  # one new file + meta file  # line 508

        os.mkdir("." + os.sep + "sub")  # line 510
        _.createFile(3, prefix="sub")  # untracked file "sub/file3"  # line 511
        sos.commit("fourth", ["--force"])  # no tracking pattern matches the subfolder  # line 512
        _.assertEqual(1, len(os.listdir(branchFolder(0, 3))))  # meta file only, no other tracked path/file  # line 513

        sos.branch("Other")  # second branch containing file1 and file2 tracked by "./file?"  # line 515
        sos.rm(".", "file?")  # remove tracking pattern, but don't touch previously created and versioned files  # line 516
        sos.add(".", "a*a")  # add tracking pattern  # line 517
        changes = sos.changes()  # should pick up addition  # line 518
        _.assertEqual(0, len(changes.modifications))  # line 519
        _.assertEqual(0, len(changes.deletions))  # not tracked anymore, but contained in version history and not removed  # line 520
        _.assertEqual(1, len(changes.additions))  # detected one addition "a123a", but won't recognize untracking files as deletion  # line 521

        sos.commit("Second_2")  # line 523
        _.assertEqual(2, len(os.listdir(branchFolder(1, 1))))  # "a123a" + meta file  # line 524
        _.assertTrue(os.path.exists("." + os.sep + "file1"))  # line 525
        _.assertTrue(os.path.exists("." + os.sep + "file2"))  # line 526

        sos.switch("test")  # go back to first branch - tracks only "file?", but not "a*a"  # line 528
        _.assertTrue(os.path.exists("." + os.sep + "file1"))  # line 529
        _.assertTrue(os.path.exists("." + os.sep + "a123a"))  # should not have been touched so far  # line 530

        sos.update("Other")  # integrate tracked files and tracking pattern from second branch into working state of master branch  # line 532
        _.assertTrue(os.path.exists("." + os.sep + "file1"))  # line 533
        _.assertTrue(os.path.exists("." + os.sep + "a123a"))  # line 534

        _.createFile("axxxa")  # new file that should be tracked on "test" now that we integrated "Other"  # line 536
        sos.commit("fifth")  # create new revision after integrating updates from second branch  # line 537
        _.assertEqual(3, len(os.listdir(branchFolder(0, 4))))  # one new file from other branch + one new in current folder + meta file  # line 538
        sos.switch("Other")  # switch back to just integrated branch that tracks only "a*a" - shouldn't do anything  # line 539
        _.assertTrue(os.path.exists("." + os.sep + "file1"))  # line 540
        _.assertTrue(os.path.exists("." + os.sep + "a123a"))  # line 541
        _.assertFalse(os.path.exists("." + os.sep + "axxxa"))  # because tracked in both branches, but not present in other -> delete in file tree TODO document  # line 542
# TODO test switch --meta

    def testLsTracked(_):  # line 545
        sos.offline("test", options=["--track"])  # set up repo in tracking mode (SVN- or gitless-style)  # line 546
        _.createFile(1)  # line 547
        _.createFile("foo")  # line 548
        sos.add(".", "file*")  # capture one file  # line 549
        out = sos.safeSplit(wrapChannels(lambda: sos.ls()).replace("\r", ""), "\n")  # line 550
        _.assertInAny('TRK file1 by "./file*"', out)  # line 551
        _.assertNotInAny('    file1 by "./file*"', out)  # line 552
        _.assertInAny("    foo", out)  # line 553

    def testCompression(_):  # line 555
        _.createFile(1)  # line 556
        sos.offline("master", options=["--plain", "--force"])  # line 557
        _.assertTrue(_.existsFile(branchFolder(0, 0) + os.sep + "b9ee10a87f612e299a6eb208210bc0898092a64c48091327cc2aaeee9b764ffa", b"x" * 10))  # line 558
        setRepoFlag("compress", True)  # was plain = uncompressed before  # line 559
        _.createFile(2)  # line 560
        sos.commit("Added file2")  # line 561
        _.assertTrue(_.existsFile(branchFolder(0, 1) + os.sep + "03b69bc801ae11f1ff2a71a50f165996d0ad681b4f822df13329a27e53f0fcd2"))  # exists  # line 562
        _.assertFalse(_.existsFile(branchFolder(0, 1) + os.sep + "03b69bc801ae11f1ff2a71a50f165996d0ad681b4f822df13329a27e53f0fcd2", b"x" * 10))  # but is compressed instead  # line 563

    def testConfigVariations(_):  # line 565
        def makeRepo():  # line 566
            try:  # line 567
                os.unlink("file1")  # line 567
            except:  # line 568
                pass  # line 568
            sos.offline("master", options=["--plain", "--force"])  # line 569
            _.createFile(1)  # line 570
            sos.commit("Added file1")  # line 571
        sos.config("set", ["strict", "on"])  # line 572
        makeRepo()  # line 573
        _.assertTrue(checkRepoFlag("strict", True))  # line 574
        sos.config("set", ["strict", "off"])  # line 575
        makeRepo()  # line 576
        _.assertTrue(checkRepoFlag("strict", False))  # line 577
        sos.config("set", ["strict", "yes"])  # line 578
        makeRepo()  # line 579
        _.assertTrue(checkRepoFlag("strict", True))  # line 580
        sos.config("set", ["strict", "no"])  # line 581
        makeRepo()  # line 582
        _.assertTrue(checkRepoFlag("strict", False))  # line 583
        sos.config("set", ["strict", "1"])  # line 584
        makeRepo()  # line 585
        _.assertTrue(checkRepoFlag("strict", True))  # line 586
        sos.config("set", ["strict", "0"])  # line 587
        makeRepo()  # line 588
        _.assertTrue(checkRepoFlag("strict", False))  # line 589
        sos.config("set", ["strict", "true"])  # line 590
        makeRepo()  # line 591
        _.assertTrue(checkRepoFlag("strict", True))  # line 592
        sos.config("set", ["strict", "false"])  # line 593
        makeRepo()  # line 594
        _.assertTrue(checkRepoFlag("strict", False))  # line 595
        sos.config("set", ["strict", "enable"])  # line 596
        makeRepo()  # line 597
        _.assertTrue(checkRepoFlag("strict", True))  # line 598
        sos.config("set", ["strict", "disable"])  # line 599
        makeRepo()  # line 600
        _.assertTrue(checkRepoFlag("strict", False))  # line 601
        sos.config("set", ["strict", "enabled"])  # line 602
        makeRepo()  # line 603
        _.assertTrue(checkRepoFlag("strict", True))  # line 604
        sos.config("set", ["strict", "disabled"])  # line 605
        makeRepo()  # line 606
        _.assertTrue(checkRepoFlag("strict", False))  # line 607
        try:  # line 608
            sos.config("set", ["strict", "nope"])  # line 608
            _.fail()  # line 608
        except:  # line 609
            pass  # line 609

    def testLsSimple(_):  # line 611
        _.createFile(1)  # line 612
        _.createFile("foo")  # line 613
        _.createFile("ign1")  # line 614
        _.createFile("ign2")  # line 615
        sos.offline("test")  # set up repo in tracking mode (SVN- or gitless-style)  # line 616
        sos.config("set", ["ignores", "ign1"])  # define an ignore pattern  # line 617
        sos.config("add", ["ignores", "ign2"])  # define an ignore pattern  # line 618
        sos.config("set", ["ignoresWhitelist", "ign1;ign2"])  # define a list of ignore patterns  # line 619
        out = wrapChannels(lambda: sos.config("show")).replace("\r", "")  # line 620
        _.assertIn("ignores => ['ign1', 'ign2']", out)  # line 621
        out = sos.safeSplit(wrapChannels(lambda: sos.ls()).replace("\r", ""), "\n")  # line 622
        _.assertInAny('    file1', out)  # line 623
        _.assertInAny('    ign1', out)  # line 624
        _.assertInAny('    ign2', out)  # line 625
        try:  # line 626
            sos.config("rm", ["foo", "bar"])  # line 626
            _.fail()  # line 626
        except:  # line 627
            pass  # line 627
        try:  # line 628
            sos.config("rm", ["ignores", "foo"])  # line 628
            _.fail()  # line 628
        except:  # line 629
            pass  # line 629
        sos.config("rm", ["ignores", "ign1"])  # line 630
        sos.config("unset", ["ignoresWhitelist"])  # remove ignore pattern  # line 631
        out = sos.safeSplit(wrapChannels(lambda: sos.ls()).replace("\r", ""), "\n")  # line 632
        _.assertInAny('    ign1', out)  # line 633
        _.assertInAny('IGN ign2', out)  # line 634
        _.assertNotInAny('    ign2', out)  # line 635

    def testWhitelist(_):  # line 637
# TODO test same for simple mode
        _.createFile(1)  # line 639
        sos.defaults.ignores[:] = ["file*"]  # replace in-place  # line 640
        sos.offline("xx", ["--track", "--strict"])  # because nothing to commit due to ignore pattern  # line 641
        sos.add(".", "file*")  # add tracking pattern for "file1"  # line 642
        sos.commit(options=["--force"])  # attempt to commit the file  # line 643
        _.assertEqual(1, len(os.listdir(branchFolder(0, 1))))  # only meta data, file1 was ignored  # line 644
        try:  # Exit because dirty  # line 645
            sos.online()  # Exit because dirty  # line 645
            _.fail()  # Exit because dirty  # line 645
        except:  # exception expected  # line 646
            pass  # exception expected  # line 646
        _.createFile("x2")  # add another change  # line 647
        sos.add(".", "x?")  # add tracking pattern for "file1"  # line 648
        try:  # force beyond dirty flag check  # line 649
            sos.online(["--force"])  # force beyond dirty flag check  # line 649
            _.fail()  # force beyond dirty flag check  # line 649
        except:  # line 650
            pass  # line 650
        sos.online(["--force", "--force"])  # force beyond file tree modifications check  # line 651
        _.assertFalse(os.path.exists(sos.utility.metaFolder))  # line 652

        _.createFile(1)  # line 654
        sos.defaults.ignoresWhitelist[:] = ["file*"]  # line 655
        sos.offline("xx", ["--track"])  # line 656
        sos.add(".", "file*")  # line 657
        sos.commit()  # should NOT ask for force here  # line 658
        _.assertEqual(2, len(os.listdir(branchFolder(0, 1))))  # meta data and "file1", file1 was whitelisted  # line 659

    def testRemove(_):  # line 661
        _.createFile(1, "x" * 100)  # line 662
        sos.offline("trunk")  # line 663
        try:  # line 664
            sos.delete("trunk")  # line 664
            _fail()  # line 664
        except:  # line 665
            pass  # line 665
        _.createFile(2, "y" * 10)  # line 666
        sos.branch("added")  # line 667
        sos.delete("trunk")  # line 668
        _.assertEqual(2, len(os.listdir("." + os.sep + sos.utility.metaFolder)))  # meta data file and "b1"  # line 669
        _.assertTrue(os.path.exists("." + os.sep + sos.utility.metaFolder + os.sep + "b1"))  # line 670
        _.assertFalse(os.path.exists("." + os.sep + sos.utility.metaFolder + os.sep + "b0"))  # line 671
        sos.branch("next")  # line 672
        _.createFile(3, "y" * 10)  # make a change  # line 673
        sos.delete("added", "--force")  # should succeed  # line 674

    def testUsage(_):  # line 676
        sos.usage()  # line 677

    def testDiff(_):  # line 679
        sos.offline(options=["--strict"])  # line 680
        _.createFile(1)  # line 681
        sos.commit()  # line 682
        _.createFile(1, "sdfsdgfsdf")  # line 683
        time.sleep(FS_PRECISION)  # line 684
        sos.commit()  # TODO this sometimes fails "nothing to commit"  # line 685
        _.createFile(1, "foobar")  # line 686
        _.assertAllIn(["MOD ./file1", "DIF ./file1", "- | 0000 |xxxxxxxxxx|", "+ | 0000 |foobar|"], wrapChannels(lambda: sos.diff("/-2")))  # second last  # line 687

    def testFindBase(_):  # line 689
        old = os.getcwd()  # line 690
        try:  # line 691
            os.mkdir("." + os.sep + ".git")  # line 692
            os.makedirs("." + os.sep + "a" + os.sep + sos.utility.metaFolder)  # line 693
            os.makedirs("." + os.sep + "a" + os.sep + "b")  # line 694
            os.chdir("a" + os.sep + "b")  # line 695
            s, vcs, cmd = sos.findSosVcsBase()  # line 696
            _.assertIsNotNone(s)  # line 697
            _.assertIsNotNone(vcs)  # line 698
            _.assertEqual("git", cmd)  # line 699
        finally:  # line 700
            os.chdir(old)  # line 700


if __name__ == '__main__':  # line 703
    logging.basicConfig(level=logging.DEBUG if '-v' in sys.argv or os.getenv("DEBUG", "false").strip().lower() == "true" or os.getenv("CI", "false").strip().lower() == "true" else logging.INFO, stream=sys.stderr, format="%(asctime)-23s %(levelname)-8s %(name)s:%(lineno)d | %(message)s" if '-v' in sys.argv or os.getenv("DEBUG", "false") == "true" else "%(message)s")  # line 704
    if configr:  # line 705
        c = configr.Configr("sos")  # line 706
        c.loadSettings()  # line 706
        if len(c.keys()) > 0:  # line 707
            sos.utility.Exit("Cannot run test suite with existing local SOS user configuration (would affect results)")  # line 707
    unittest.main(testRunner=debugTestRunner() if '-v' in sys.argv and not os.getenv("CI", "false").lower() == "true" else None)  # warnings = "ignore")  # line 708
