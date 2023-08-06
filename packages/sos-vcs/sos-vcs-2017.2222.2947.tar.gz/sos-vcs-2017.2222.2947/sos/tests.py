#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# __coconut_hash__ = 0xcc1d10

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
        a = False  # type: bool  # line 180
        def b():  # line 181
            nonlocal a  # line 181
            a = True  # line 181
        co = sos.CallOnce(b)  # type: sos.CallOnce  # line 182
        co()  # line 183
        _.assertTrue(a)  # was modified  # line 184
        a = False  # line 185
        co()  # line 186
        _.assertFalse(a)  # was not modified again  # line 187
        sos.offline(options=["--track"])  # line 188
        os.mkdir("sub")  # line 189
        _.createFile("sub" + os.sep + "file1", "sdfsdf")  # line 190
        sos.add("./sub", "sub/file?")  # line 191
        sos.commit("test")  # should pick up sub/file1 pattern  # line 192
        _.assertEqual(2, len(os.listdir(os.path.join(sos.metaFolder, "b0", "r1"))))  # sub/file1 was added  # line 193
        _.createFile(1)  # line 194
        try:  # should not commit anything, as the file in base folder doesn't match the tracked pattern  # line 195
            sos.commit("nothing")  # should not commit anything, as the file in base folder doesn't match the tracked pattern  # line 195
            _.fail()  # should not commit anything, as the file in base folder doesn't match the tracked pattern  # line 195
        except:  # line 196
            pass  # line 196

    def testComputeSequentialPathSet(_):  # line 198
        os.makedirs(branchFolder(0, 0))  # line 199
        os.makedirs(branchFolder(0, 1))  # line 200
        os.makedirs(branchFolder(0, 2))  # line 201
        os.makedirs(branchFolder(0, 3))  # line 202
        os.makedirs(branchFolder(0, 4))  # line 203
        m = sos.Metadata(os.getcwd())  # line 204
        m.branch = 0  # line 205
        m.commit = 2  # line 206
        m.saveBranches()  # line 207
        m.paths = {"./a": sos.PathInfo("", 0, 0, "")}  # line 208
        m.saveCommit(0, 0)  # initial  # line 209
        m.paths["./a"] = sos.PathInfo("", 1, 0, "")  # line 210
        m.saveCommit(0, 1)  # mod  # line 211
        m.paths["./b"] = sos.PathInfo("", 0, 0, "")  # line 212
        m.saveCommit(0, 2)  # add  # line 213
        m.paths["./a"] = sos.PathInfo("", None, 0, "")  # line 214
        m.saveCommit(0, 3)  # del  # line 215
        m.paths["./a"] = sos.PathInfo("", None, 0, "")  # line 216
        m.saveCommit(0, 4)  # readd  # line 217
        m.commits = {i: sos.CommitInfo(i, 0, None) for i in range(5)}  # line 218
        m.saveBranch(0)  # line 219
        m.computeSequentialPathSet(0, 4)  # line 220
        _.assertEqual(2, len(m.paths))  # line 221

    def testParseRevisionString(_):  # line 223
        m = sos.Metadata(os.getcwd())  # line 224
        m.branch = 1  # line 225
        m.commits = {0: 0, 1: 1, 2: 2}  # line 226
        _.assertEqual((1, 3), m.parseRevisionString("3"))  # line 227
        _.assertEqual((2, 3), m.parseRevisionString("2/3"))  # line 228
        _.assertEqual((1, -1), m.parseRevisionString(None))  # line 229
        _.assertEqual((2, -1), m.parseRevisionString("2/"))  # line 230
        _.assertEqual((1, -2), m.parseRevisionString("/-2"))  # line 231
        _.assertEqual((1, -1), m.parseRevisionString("/"))  # line 232

    def testOfflineEmpty(_):  # line 234
        os.mkdir("." + os.sep + sos.metaFolder)  # line 235
        try:  # line 236
            sos.offline("trunk")  # line 236
            _.fail()  # line 236
        except SystemExit:  # line 237
            pass  # line 237
        os.rmdir("." + os.sep + sos.metaFolder)  # line 238
        sos.offline("test")  # line 239
        _.assertIn(sos.metaFolder, os.listdir("."))  # line 240
        _.assertAllIn(["b0", sos.metaFile], os.listdir("." + os.sep + sos.metaFolder))  # line 241
        _.assertAllIn(["r0", sos.metaFile], os.listdir("." + os.sep + sos.metaFolder + os.sep + "b0"))  # line 242
        _.assertEqual(2, len(os.listdir("." + os.sep + sos.metaFolder)))  # only branch folder and meta data file  # line 243
        _.assertEqual(2, len(os.listdir("." + os.sep + sos.metaFolder + os.sep + "b0")))  # only commit folder and meta data file  # line 244
        _.assertEqual(1, len(os.listdir(branchFolder(0, 0))))  # only meta data file  # line 245

    def testOfflineWithFiles(_):  # line 247
        _.createFile(1, "x" * 100)  # line 248
        _.createFile(2)  # line 249
        sos.offline("test")  # line 250
        _.assertAllIn(["file1", "file2", sos.metaFolder], os.listdir("."))  # line 251
        _.assertAllIn(["b0", sos.metaFile], os.listdir("." + os.sep + sos.metaFolder))  # line 252
        _.assertAllIn(["r0", sos.metaFile], os.listdir("." + os.sep + sos.metaFolder + os.sep + "b0"))  # line 253
        _.assertAllIn([sos.metaFile, "03b69bc801ae11f1ff2a71a50f165996d0ad681b4f822df13329a27e53f0fcd2", "b9ee10a87f612e299a6eb208210bc0898092a64c48091327cc2aaeee9b764ffa"], os.listdir("." + os.sep + sos.metaFolder + os.sep + "b0" + os.sep + "r0"))  # line 254
        _.assertEqual(2, len(os.listdir("." + os.sep + sos.metaFolder)))  # only branch folder and meta data file  # line 255
        _.assertEqual(2, len(os.listdir("." + os.sep + sos.metaFolder + os.sep + "b0")))  # only commit folder and meta data file  # line 256
        _.assertEqual(3, len(os.listdir(branchFolder(0, 0))))  # only meta data file plus branch base file copies  # line 257

    def testBranch(_):  # line 259
        _.createFile(1, "x" * 100)  # line 260
        _.createFile(2)  # line 261
        sos.offline("test")  # b0/r0  # line 262
        sos.branch("other")  # b1/r0  # line 263
        _.assertAllIn(["b0", "b1", sos.metaFile], os.listdir("." + os.sep + sos.metaFolder))  # line 264
        _.assertEqual(list(sorted(os.listdir("." + os.sep + sos.metaFolder + os.sep + "b0"))), list(sorted(os.listdir("." + os.sep + sos.metaFolder + os.sep + "b1"))))  # line 265
        _.assertEqual(list(sorted(os.listdir(branchFolder(0, 0)))), list(sorted(os.listdir(branchFolder(1, 0)))))  # line 267
        _.createFile(1, "z")  # modify file  # line 269
        sos.branch()  # b2/r0  branch to unnamed branch with modified file tree contents  # line 270
        _.assertNotEqual(os.stat("." + os.sep + sos.metaFolder + os.sep + "b1" + os.sep + "r0" + os.sep + "b9ee10a87f612e299a6eb208210bc0898092a64c48091327cc2aaeee9b764ffa").st_size, os.stat("." + os.sep + sos.metaFolder + os.sep + "b2" + os.sep + "r0" + os.sep + "b9ee10a87f612e299a6eb208210bc0898092a64c48091327cc2aaeee9b764ffa").st_size)  # line 271
        _.createFile(3, "z")  # line 273
        sos.branch("from_last_revision", ["--last", "--stay"])  # b3/r0 create copy of other file1,file2 and don't switch  # line 274
        _.assertEqual(list(sorted(os.listdir("." + os.sep + sos.metaFolder + os.sep + "b3" + os.sep + "r0"))), list(sorted(os.listdir("." + os.sep + sos.metaFolder + os.sep + "b2" + os.sep + "r0"))))  # line 275
# Check sos.status output which branch is marked


    def testComittingAndChanges(_):  # line 280
        _.createFile(1, "x" * 100)  # line 281
        _.createFile(2)  # line 282
        sos.offline("test")  # line 283
        changes = sos.changes()  # line 284
        _.assertEqual(0, len(changes.additions))  # line 285
        _.assertEqual(0, len(changes.deletions))  # line 286
        _.assertEqual(0, len(changes.modifications))  # line 287
        _.createFile(1, "z")  # size change  # line 288
        changes = sos.changes()  # line 289
        _.assertEqual(0, len(changes.additions))  # line 290
        _.assertEqual(0, len(changes.deletions))  # line 291
        _.assertEqual(1, len(changes.modifications))  # line 292
        sos.commit("message")  # line 293
        _.assertAllIn(["r0", "r1", sos.metaFile], os.listdir("." + os.sep + sos.metaFolder + os.sep + "b0"))  # line 294
        _.assertAllIn([sos.metaFile, "b9ee10a87f612e299a6eb208210bc0898092a64c48091327cc2aaeee9b764ffa"], os.listdir(branchFolder(0, 1)))  # line 295
        _.assertEqual(2, len(os.listdir(branchFolder(0, 1))))  # no further files, only the modified one  # line 296
        _.assertEqual(1, len(sos.changes("/0").modifications))  # vs. explicit revision on current branch  # line 297
        _.assertEqual(1, len(sos.changes("0/0").modifications))  # vs. explicit branch/revision  # line 298
        _.createFile(1, "")  # modify to empty file, mentioned in meta data, but not stored as own file  # line 299
        os.unlink("file2")  # line 300
        changes = sos.changes()  # line 301
        _.assertEqual(0, len(changes.additions))  # line 302
        _.assertEqual(1, len(changes.deletions))  # line 303
        _.assertEqual(1, len(changes.modifications))  # line 304
        sos.commit("modified")  # line 305
        _.assertEqual(1, len(os.listdir(branchFolder(0, 2))))  # no additional files, only mentions in metadata  # line 306
        try:  # expecting Exit due to no changes  # line 307
            sos.commit("nothing")  # expecting Exit due to no changes  # line 307
            _.fail()  # expecting Exit due to no changes  # line 307
        except:  # line 308
            pass  # line 308

    def testGetBranch(_):  # line 310
        m = sos.Metadata(os.getcwd())  # line 311
        m.branch = 1  # current branch  # line 312
        m.branches = {0: sos.BranchInfo(0, 0, "trunk")}  # line 313
        _.assertEqual(27, m.getBranchByName(27))  # line 314
        _.assertEqual(0, m.getBranchByName("trunk"))  # line 315
        _.assertEqual(1, m.getBranchByName(""))  # split from "/"  # line 316
        _.assertIsNone(m.getBranchByName("unknown"))  # line 317
        m.commits = {0: sos.CommitInfo(0, 0, "bla")}  # line 318
        _.assertEqual(13, m.getRevisionByName("13"))  # line 319
        _.assertEqual(0, m.getRevisionByName("bla"))  # line 320
        _.assertEqual(-1, m.getRevisionByName(""))  # split from "/"  # line 321

    def testTagging(_):  # line 323
        m = sos.Metadata(os.getcwd())  # line 324
        sos.offline()  # line 325
        _.createFile(111)  # line 326
        sos.commit("tag", ["--tag"])  # line 327
        _.createFile(2)  # line 328
        try:  # line 329
            sos.commit("tag")  # line 329
            _.fail()  # line 329
        except:  # line 330
            pass  # line 330
        sos.commit("tag-2", ["--tag"])  # line 331

    def testSwitch(_):  # line 333
        _.createFile(1, "x" * 100)  # line 334
        _.createFile(2, "y")  # line 335
        sos.offline("test")  # file1-2  in initial branch commit  # line 336
        sos.branch("second")  # file1-2  switch, having same files  # line 337
        sos.switch("0")  # no change  switch back, no problem  # line 338
        sos.switch("second")  # no change  # switch back, no problem  # line 339
        _.createFile(3, "y")  # generate a file  # line 340
        try:  # uncommited changes detected  # line 341
            sos.switch("test")  # uncommited changes detected  # line 341
            _.fail()  # uncommited changes detected  # line 341
        except SystemExit:  # line 342
            pass  # line 342
        sos.commit("Finish")  # file1-3  commit third file into branch second  # line 343
        sos.changes()  # line 344
        sos.switch("test")  # file1-2, remove file3 from file tree  # line 345
        _.assertFalse(_.existsFile(3))  # removed when switching back to test  # line 346
        out = wrapChannels(lambda: sos.status()).replace("\r", "")  # line 347
        _.assertIn("  * b00   'test'", out)  # line 348
        _.assertIn("    b01 'second'", out)  # line 349
        _.assertIn("(dirty)", out)  # one branch has commits  # line 350
        _.assertIn("(in sync)", out)  # the other doesn't  # line 351
        _.createFile(4, "xy")  # generate a file  # line 352
        sos.switch("second", "--force")  # avoids warning on uncommited changes, but keeps file4  # line 353
        _.assertFalse(_.existsFile(4))  # removed when forcedly switching back to test  # line 354
        _.assertTrue(_.existsFile(3))  # was restored from branch's revision r1  # line 355
        os.unlink("." + os.sep + "file1")  # remove old file1  # line 356
        sos.switch("test", "--force")  # should restore file1 and remove file3  # line 357
        _.assertTrue(_.existsFile(1))  # was restored from branch's revision r1  # line 358
        _.assertFalse(_.existsFile(3))  # was restored from branch's revision r1  # line 359

    def testAutoDetectVCS(_):  # line 361
        os.mkdir(".git")  # line 362
        sos.offline(sos.vcsBranches[sos.findSosVcsBase()[2]])  # create initial branch  # line 363
        with open(sos.metaFolder + os.sep + sos.metaFile, "r") as fd:  # line 364
            meta = fd.read()  # line 364
        _.assertTrue("\"master\"" in meta)  # line 365
        os.rmdir(".git")  # line 366

    def testUpdate(_):  # line 368
        sos.offline("trunk")  # create initial branch b0/r0  # line 369
        _.createFile(1, "x" * 100)  # line 370
        sos.commit("second")  # create b0/r1  # line 371

        sos.switch("/0")  # go back to b0/r0 - deletes file1  # line 373
        _.assertFalse(_.existsFile(1))  # line 374

        sos.update("/1")  # recreate file1  # line 376
        _.assertTrue(_.existsFile(1))  # line 377

        sos.commit("third", ["--force"])  # force because nothing to commit. should create r2 with same contents as r1, but as differential from r1, not from r0 (= no changes in meta folder)  # line 379
        _.assertTrue(os.path.exists(branchFolder(0, 2)))  # line 380
        _.assertTrue(os.path.exists(branchFolder(0, 2) + os.sep + sos.metaFile))  # line 381
        _.assertEqual(1, len(os.listdir(branchFolder(0, 2))))  # only meta data file, no differential files  # line 382

        sos.update("/1")  # do nothing, as nothing has changed  # line 384
        _.assertTrue(_.existsFile(1))  # line 385

        _.createFile(2, "y" * 100)  # line 387
#    out = wrapChannels(() -> sos.branch("other"))  # won't comply as there are changes
#    _.assertIn("--force", out)
        sos.branch("other", ["--force"])  # automatically including file 2 (as we are in simple mode)  # line 390
        _.assertTrue(_.existsFile(2))  # line 391
        sos.update("trunk", ["--add"])  # only add stuff  # line 392
        _.assertTrue(_.existsFile(2))  # line 393
        sos.update("trunk")  # nothing to do  # line 394
        _.assertFalse(_.existsFile(2))  # removes file not present in original branch  # line 395

        theirs = b"a\nb\nc\nd\ne\nf\ng\nh\nx\nx\nj\nk"  # line 397
        _.createFile(10, theirs)  # line 398
        mine = b"a\nc\nd\ne\ng\nf\nx\nh\ny\ny\nj"  # missing "b", inserted g, modified g->x, replace x/x -> y/y, removed k  # line 399
        _.createFile(11, mine)  # line 400
        _.assertEqual(b"a\nb\nc\nd\ne\nf\ng\nh\nx\nx\nj\nk", sos.merge(filename="." + os.sep + "file10", intoname="." + os.sep + "file11", mergeOperation=sos.MergeOperation.BOTH, conflictResolution=sos.ConflictResolution.THEIRS))  # completely recreated other file  # line 401
        _.assertEqual(b"a\nb\nc\nd\ne\ng\nf\ng\nx\nh\nx\nx\ny\ny\nj\nk", sos.merge(filename="." + os.sep + "file10", intoname="." + os.sep + "file11", mergeOperation=sos.MergeOperation.INSERT, conflictResolution=sos.ConflictResolution.MINE))  # line 402

    def testUpdate2(_):  # line 404
        _.createFile("test.txt", "x" * 10)  # line 405
        sos.offline("trunk", ["--strict"])  # use strict mode, as timestamp differences are too small for testing  # line 406
        sos.branch("mod")  # line 407
        _.createFile("test.txt", "x" * 5 + "y" * 5)  # line 408
        time.sleep(FS_PRECISION)  # line 409
        sos.commit("mod")  # create b0/r1  # line 410
        sos.switch("trunk", ["--force"])  # should replace contents, force in case some other files were modified (e.g. during working on the code) TODO investigate more  # line 411
        with open("test.txt", "rb") as fd:  # line 412
            _.assertEqual(b"x" * 10, fd.read())  # line 412
        sos.update("mod", ["--theirs"])  # integrate changes TODO same with ask -> theirs  # line 413
        with open("test.txt", "rb") as fd:  # line 414
            _.assertEqual(b"x" * 5 + b"y" * 5, fd.read())  # line 414
        _.createFile("test.txt", "x" * 10)  # line 415
        mockInput(["t"], lambda: sos.update("mod", ["--ask"]))  # same as above with interaction -> theirs  # line 416
        with open("test.txt", "rb") as fd:  # line 417
            _.assertEqual(b"x" * 5 + b"y" * 5, fd.read())  # line 417

    def testIsTextType(_):  # line 419
        m = sos.Metadata(".")  # line 420
        m.c.texttype = ["*.x", "*.md", "*.md.*"]  # line 421
        m.c.bintype = ["*.md.confluence"]  # line 422
        _.assertTrue(m.isTextType("ab.txt"))  # line 423
        _.assertTrue(m.isTextType("./ab.txt"))  # line 424
        _.assertTrue(m.isTextType("bc/ab.txt"))  # line 425
        _.assertFalse(m.isTextType("bc/ab."))  # line 426
        _.assertTrue(m.isTextType("23_3.x.x"))  # line 427
        _.assertTrue(m.isTextType("dfg/dfglkjdf7/test.md"))  # line 428
        _.assertTrue(m.isTextType("./test.md.pdf"))  # line 429
        _.assertFalse(m.isTextType("./test_a.md.confluence"))  # line 430

    def testEolDet(_):  # line 432
        ''' Check correct end-of-line detection. '''  # line 433
        _.assertEqual(b"\n", sos.eoldet(b"a\nb"))  # line 434
        _.assertEqual(b"\r\n", sos.eoldet(b"a\r\nb\r\n"))  # line 435
        _.assertEqual(b"\r", sos.eoldet(b"\ra\rb"))  # line 436
        _.assertAllIn(["Inconsistent", "with "], wrapChannels(lambda: _.assertEqual(b"\n", sos.eoldet(b"\r\na\r\nb\n"))))  # line 437
        _.assertAllIn(["Inconsistent", "without"], wrapChannels(lambda: _.assertEqual(b"\n", sos.eoldet(b"\ra\nnb\n"))))  # line 438
        _.assertIsNone(sos.eoldet(b""))  # line 439
        _.assertIsNone(sos.eoldet(b"sdf"))  # line 440

    def testMerge(_):  # line 442
        ''' Check merge results depending on conflict solution options. '''  # line 443
        a = b"a\nb\ncc\nd"  # line 444
        b = b"a\nb\nee\nd"  # line 445
        _.assertEqual(b"a\nb\ncc\nee\nd", sos.merge(a, b, mergeOperation=sos.MergeOperation.INSERT))  # means insert changes from a into b, but don't replace  # line 446
        _.assertEqual(b"a\nb\nd", sos.merge(a, b, mergeOperation=sos.MergeOperation.REMOVE))  # line 447
        _.assertEqual(b"a\nb\ncc\nd", sos.merge(a, b, mergeOperation=sos.MergeOperation.BOTH))  # line 448
# Now test intra-line merging without conflicts
        _.assertEqual(b"a\nbc d\ne", sos.merge(b"a\nbc d\ne", b"a\nbcd\ne", mergeOperation=sos.MergeOperation.INSERT))  # because it's a deletion ['  a', '- bc d', '?   -\n', '+ bcd', '  e']  # line 450
        _.assertEqual(b"a\nbcd\ne", sos.merge(b"a\nbc d\ne", b"a\nbcd\ne", mergeOperation=sos.MergeOperation.REMOVE))  # ['  a', '- bc d', '?   -\n', '+ bcd', '  e']  # line 451
        _.assertEqual(b"a\nbc d\ne", sos.merge(b"a\nbcd\ne", b"a\nbc d\ne", mergeOperation=sos.MergeOperation.INSERT))  # nothing to insert  # line 452
        _.assertEqual(b"a\nbcd\ne", sos.merge(b"a\nbcd\ne", b"a\nbc d\ne", mergeOperation=sos.MergeOperation.REMOVE))  # remove space  # line 453
# Test with change + insert (conflict)
        _.assertEqual(b"a\nb fdd d\ne", sos.merge(b"a\nb cd d\ne", b"a\nb fdd d\ne", conflictResolution=sos.ConflictResolution.MINE))  # line 455
        _.assertEqual(b"a\nb cd d\ne", sos.merge(b"a\nb cd d\ne", b"a\nb fdd d\ne", conflictResolution=sos.ConflictResolution.THEIRS))  # ['  a', '- b cd d', '?   ^\n', '+ b fdd d', '?   ^^\n', '  e']  # line 456
        _.assertEqual(b"a\nb fdd d\ne", mockInput(["i"], lambda: sos.merge(b"a\nb cd d\ne", b"a\nb fdd d\ne", conflictResolution=sos.ConflictResolution.ASK)))  # ['  a', '- b cd d', '?   ^\n', '+ b fdd d', '?   ^^\n', '  e']  # line 457
        _.assertEqual(b"a\nb cd d\ne", mockInput(["t"], lambda: sos.merge(b"a\nb cd d\ne", b"a\nb fdd d\ne", conflictResolution=sos.ConflictResolution.ASK)))  # ['  a', '- b cd d', '?   ^\n', '+ b fdd d', '?   ^^\n', '  e']  # line 458
        _.assertEqual(b"abbc", sos.merge(b"abbc", b"addc", mergeOperation=sos.MergeOperation.BOTH, conflictResolution=sos.ConflictResolution.THEIRS))  # line 459
        _.assertEqual(b"a\nbb\nc", sos.merge(b"a\nbb\nc", b"a\ndd\nc", mergeOperation=sos.MergeOperation.BOTH, conflictResolution=sos.ConflictResolution.THEIRS))  # line 460
        _.assertIn("Differing EOL-styles", wrapChannels(lambda: sos.merge(b"a\nb", b"a\r\nb")))  # expect warning  # line 461
        _.assertIn(b"a\r\nb", sos.merge(b"a\nb", b"a\r\nb"))  # in doubt, use "mine" CR-LF  # line 462

    def testPickyMode(_):  # line 464
        ''' Confirm that picky mode reset tracked patterns after commits. '''  # line 465
        sos.offline("trunk", ["--picky"])  # line 466
        sos.add(".", "./file?", ["--force"])  # line 467
        _.createFile(1, "aa")  # line 468
        sos.commit("First")  # add one file  # line 469
        _.assertEqual(2, len(os.listdir(branchFolder(0, 1))))  # line 470
        _.createFile(2, "b")  # line 471
        try:  # add nothing, because picky  # line 472
            sos.commit("Second")  # add nothing, because picky  # line 472
        except:  # line 473
            pass  # line 473
        sos.add(".", "./file?")  # line 474
        sos.commit("Third")  # line 475
        _.assertEqual(2, len(os.listdir(branchFolder(0, 2))))  # line 476
        out = wrapChannels(lambda: sos.log([])).replace("\r", "")  # line 477
        _.assertIn("  * r2", out)  # line 478

    def testTrackedSubfolder(_):  # line 480
        ''' See if patterns for files in sub folders are picked up correctly. '''  # line 481
        os.mkdir("." + os.sep + "sub")  # line 482
        sos.offline("trunk", ["--track"])  # line 483
        _.createFile(1, "x")  # line 484
        _.createFile(1, "x", prefix="sub")  # line 485
        sos.add(".", "./file?")  # add glob pattern to track  # line 486
        sos.commit("First")  # line 487
        _.assertEqual(2, len(os.listdir(branchFolder(0, 1))))  # one new file + meta file  # line 488
        sos.add(".", "sub/file?")  # add glob pattern to track  # line 489
        sos.commit("Second")  # one new file + meta  # line 490
        _.assertEqual(2, len(os.listdir(branchFolder(0, 1))))  # one new file + meta file  # line 491
        os.unlink("file1")  # remove from basefolder  # line 492
        _.createFile(2, "y")  # line 493
        sos.rm(".", "sub/file?")  # line 494
        try:  # raises Exit. TODO test the "suggest a pattern" case  # line 495
            sos.rm(".", "sub/bla")  # raises Exit. TODO test the "suggest a pattern" case  # line 495
            _.fail()  # raises Exit. TODO test the "suggest a pattern" case  # line 495
        except:  # line 496
            pass  # line 496
        sos.commit("Third")  # line 497
        _.assertEqual(2, len(os.listdir(branchFolder(0, 2))))  # one new file + meta  # line 498
# TODO check if /file1 and sub/file1 were removed from index

    def testTrackedMode(_):  # line 501
        ''' Difference in semantics vs simple mode:
          - For remote/other branch we can only know and consider tracked files, thus ignoring all complexity stemming from handling addition of untracked files.
          - For current branch, we can take into account tracked and untracked ones, in theory, but it doesn't make sense.
        In conclusion, using the union of tracking patterns from both sides to find affected files makes sense, but disallow deleting files not present in remote branch.
    '''  # line 506
        sos.offline("test", options=["--track"])  # set up repo in tracking mode (SVN- or gitless-style)  # line 507
        _.createFile(1)  # line 508
        _.createFile("a123a")  # untracked file "a123a"  # line 509
        sos.add(".", "./file?")  # add glob tracking pattern  # line 510
        sos.commit("second")  # versions "file1"  # line 511
        _.assertEqual(2, len(os.listdir(branchFolder(0, 1))))  # one new file + meta file  # line 512
        out = wrapChannels(lambda: sos.status()).replace("\r", "")  # line 513
        _.assertIn("  | ./file?", out)  # line 514

        _.createFile(2)  # untracked file "file2"  # line 516
        sos.commit("third")  # versions "file2"  # line 517
        _.assertEqual(2, len(os.listdir(branchFolder(0, 2))))  # one new file + meta file  # line 518

        os.mkdir("." + os.sep + "sub")  # line 520
        _.createFile(3, prefix="sub")  # untracked file "sub/file3"  # line 521
        sos.commit("fourth", ["--force"])  # no tracking pattern matches the subfolder  # line 522
        _.assertEqual(1, len(os.listdir(branchFolder(0, 3))))  # meta file only, no other tracked path/file  # line 523

        sos.branch("Other")  # second branch containing file1 and file2 tracked by "./file?"  # line 525
        sos.rm(".", "./file?")  # remove tracking pattern, but don't touch previously created and versioned files  # line 526
        sos.add(".", "./a*a")  # add tracking pattern  # line 527
        changes = sos.changes()  # should pick up addition only, because tracked, but not the deletion, as not tracked anymore  # line 528
        _.assertEqual(0, len(changes.modifications))  # line 529
        _.assertEqual(0, len(changes.deletions))  # not tracked anymore, but contained in version history and not removed  # line 530
        _.assertEqual(1, len(changes.additions))  # detected one addition "a123a", but won't recognize untracking files as deletion  # line 531

        sos.commit("Second_2")  # line 533
        _.assertEqual(2, len(os.listdir(branchFolder(1, 1))))  # "a123a" + meta file  # line 534
        _.assertTrue(os.path.exists("." + os.sep + "file1"))  # line 535
        _.assertTrue(os.path.exists("." + os.sep + "file2"))  # line 536

        sos.switch("test")  # go back to first branch - tracks only "file?", but not "a*a"  # line 538
        _.assertTrue(os.path.exists("." + os.sep + "file1"))  # line 539
        _.assertTrue(os.path.exists("." + os.sep + "a123a"))  # should not have been touched so far  # line 540

        sos.update("Other")  # integrate tracked files and tracking pattern from second branch into working state of master branch  # line 542
        _.assertTrue(os.path.exists("." + os.sep + "file1"))  # line 543
        _.assertTrue(os.path.exists("." + os.sep + "a123a"))  # line 544

        _.createFile("axxxa")  # new file that should be tracked on "test" now that we integrated "Other"  # line 546
        sos.commit("fifth")  # create new revision after integrating updates from second branch  # line 547
        _.assertEqual(3, len(os.listdir(branchFolder(0, 4))))  # one new file from other branch + one new in current folder + meta file  # line 548
        sos.switch("Other")  # switch back to just integrated branch that tracks only "a*a" - shouldn't do anything  # line 549
        _.assertTrue(os.path.exists("." + os.sep + "file1"))  # line 550
        _.assertTrue(os.path.exists("." + os.sep + "a123a"))  # line 551
        _.assertFalse(os.path.exists("." + os.sep + "axxxa"))  # because tracked in both branches, but not present in other -> delete in file tree TODO document  # line 552
# TODO test switch --meta

    def testLsTracked(_):  # line 555
        sos.offline("test", options=["--track"])  # set up repo in tracking mode (SVN- or gitless-style)  # line 556
        _.createFile(1)  # line 557
        _.createFile("foo")  # line 558
        sos.add(".", "./file*")  # capture one file  # line 559
        out = sos.safeSplit(wrapChannels(lambda: sos.ls()).replace("\r", ""), "\n")  # line 560
        _.assertInAny('TRK file1 by "./file*"', out)  # line 561
        _.assertNotInAny('    file1 by "./file*"', out)  # line 562
        _.assertInAny("    foo", out)  # line 563

    def testCompression(_):  # line 565
        _.createFile(1)  # line 566
        sos.offline("master", options=["--plain", "--force"])  # line 567
        _.assertTrue(_.existsFile(branchFolder(0, 0) + os.sep + "b9ee10a87f612e299a6eb208210bc0898092a64c48091327cc2aaeee9b764ffa", b"x" * 10))  # line 568
        setRepoFlag("compress", True)  # was plain = uncompressed before  # line 569
        _.createFile(2)  # line 570
        sos.commit("Added file2")  # line 571
        _.assertTrue(_.existsFile(branchFolder(0, 1) + os.sep + "03b69bc801ae11f1ff2a71a50f165996d0ad681b4f822df13329a27e53f0fcd2"))  # exists  # line 572
        _.assertFalse(_.existsFile(branchFolder(0, 1) + os.sep + "03b69bc801ae11f1ff2a71a50f165996d0ad681b4f822df13329a27e53f0fcd2", b"x" * 10))  # but is compressed instead  # line 573

    def testConfigVariations(_):  # line 575
        def makeRepo():  # line 576
            try:  # line 577
                os.unlink("file1")  # line 577
            except:  # line 578
                pass  # line 578
            sos.offline("master", options=["--plain", "--force"])  # line 579
            _.createFile(1)  # line 580
            sos.commit("Added file1")  # line 581
        sos.config("set", ["strict", "on"])  # line 582
        makeRepo()  # line 583
        _.assertTrue(checkRepoFlag("strict", True))  # line 584
        sos.config("set", ["strict", "off"])  # line 585
        makeRepo()  # line 586
        _.assertTrue(checkRepoFlag("strict", False))  # line 587
        sos.config("set", ["strict", "yes"])  # line 588
        makeRepo()  # line 589
        _.assertTrue(checkRepoFlag("strict", True))  # line 590
        sos.config("set", ["strict", "no"])  # line 591
        makeRepo()  # line 592
        _.assertTrue(checkRepoFlag("strict", False))  # line 593
        sos.config("set", ["strict", "1"])  # line 594
        makeRepo()  # line 595
        _.assertTrue(checkRepoFlag("strict", True))  # line 596
        sos.config("set", ["strict", "0"])  # line 597
        makeRepo()  # line 598
        _.assertTrue(checkRepoFlag("strict", False))  # line 599
        sos.config("set", ["strict", "true"])  # line 600
        makeRepo()  # line 601
        _.assertTrue(checkRepoFlag("strict", True))  # line 602
        sos.config("set", ["strict", "false"])  # line 603
        makeRepo()  # line 604
        _.assertTrue(checkRepoFlag("strict", False))  # line 605
        sos.config("set", ["strict", "enable"])  # line 606
        makeRepo()  # line 607
        _.assertTrue(checkRepoFlag("strict", True))  # line 608
        sos.config("set", ["strict", "disable"])  # line 609
        makeRepo()  # line 610
        _.assertTrue(checkRepoFlag("strict", False))  # line 611
        sos.config("set", ["strict", "enabled"])  # line 612
        makeRepo()  # line 613
        _.assertTrue(checkRepoFlag("strict", True))  # line 614
        sos.config("set", ["strict", "disabled"])  # line 615
        makeRepo()  # line 616
        _.assertTrue(checkRepoFlag("strict", False))  # line 617
        try:  # line 618
            sos.config("set", ["strict", "nope"])  # line 618
            _.fail()  # line 618
        except:  # line 619
            pass  # line 619

    def testLsSimple(_):  # line 621
        _.createFile(1)  # line 622
        _.createFile("foo")  # line 623
        _.createFile("ign1")  # line 624
        _.createFile("ign2")  # line 625
        sos.offline("test")  # set up repo in tracking mode (SVN- or gitless-style)  # line 626
        sos.config("set", ["ignores", "ign1"])  # define an ignore pattern  # line 627
        sos.config("add", ["ignores", "ign2"])  # define an ignore pattern  # line 628
        sos.config("set", ["ignoresWhitelist", "ign1;ign2"])  # define a list of ignore patterns  # line 629
        out = wrapChannels(lambda: sos.config("show")).replace("\r", "")  # line 630
        _.assertIn("ignores => ['ign1', 'ign2']", out)  # line 631
        out = sos.safeSplit(wrapChannels(lambda: sos.ls()).replace("\r", ""), "\n")  # line 632
        _.assertInAny('    file1', out)  # line 633
        _.assertInAny('    ign1', out)  # line 634
        _.assertInAny('    ign2', out)  # line 635
        try:  # line 636
            sos.config("rm", ["foo", "bar"])  # line 636
            _.fail()  # line 636
        except:  # line 637
            pass  # line 637
        try:  # line 638
            sos.config("rm", ["ignores", "foo"])  # line 638
            _.fail()  # line 638
        except:  # line 639
            pass  # line 639
        sos.config("rm", ["ignores", "ign1"])  # line 640
        sos.config("unset", ["ignoresWhitelist"])  # remove ignore pattern  # line 641
        out = sos.safeSplit(wrapChannels(lambda: sos.ls()).replace("\r", ""), "\n")  # line 642
        _.assertInAny('    ign1', out)  # line 643
        _.assertInAny('IGN ign2', out)  # line 644
        _.assertNotInAny('    ign2', out)  # line 645

    def testWhitelist(_):  # line 647
# TODO test same for simple mode
        _.createFile(1)  # line 649
        sos.defaults.ignores[:] = ["file*"]  # replace in-place  # line 650
        sos.offline("xx", ["--track", "--strict"])  # because nothing to commit due to ignore pattern  # line 651
        sos.add(".", "./file*")  # add tracking pattern for "file1"  # line 652
        sos.commit(options=["--force"])  # attempt to commit the file  # line 653
        _.assertEqual(1, len(os.listdir(branchFolder(0, 1))))  # only meta data, file1 was ignored  # line 654
        try:  # Exit because dirty  # line 655
            sos.online()  # Exit because dirty  # line 655
            _.fail()  # Exit because dirty  # line 655
        except:  # exception expected  # line 656
            pass  # exception expected  # line 656
        _.createFile("x2")  # add another change  # line 657
        sos.add(".", "./x?")  # add tracking pattern for "file1"  # line 658
        try:  # force beyond dirty flag check  # line 659
            sos.online(["--force"])  # force beyond dirty flag check  # line 659
            _.fail()  # force beyond dirty flag check  # line 659
        except:  # line 660
            pass  # line 660
        sos.online(["--force", "--force"])  # force beyond file tree modifications check  # line 661
        _.assertFalse(os.path.exists(sos.metaFolder))  # line 662

        _.createFile(1)  # line 664
        sos.defaults.ignoresWhitelist[:] = ["file*"]  # line 665
        sos.offline("xx", ["--track"])  # line 666
        sos.add(".", "./file*")  # line 667
        sos.commit()  # should NOT ask for force here  # line 668
        _.assertEqual(2, len(os.listdir(branchFolder(0, 1))))  # meta data and "file1", file1 was whitelisted  # line 669

    def testRemove(_):  # line 671
        _.createFile(1, "x" * 100)  # line 672
        sos.offline("trunk")  # line 673
        try:  # line 674
            sos.delete("trunk")  # line 674
            _fail()  # line 674
        except:  # line 675
            pass  # line 675
        _.createFile(2, "y" * 10)  # line 676
        sos.branch("added")  # line 677
        sos.delete("trunk")  # line 678
        _.assertEqual(2, len(os.listdir("." + os.sep + sos.metaFolder)))  # meta data file and "b1"  # line 679
        _.assertTrue(os.path.exists("." + os.sep + sos.metaFolder + os.sep + "b1"))  # line 680
        _.assertFalse(os.path.exists("." + os.sep + sos.metaFolder + os.sep + "b0"))  # line 681
        sos.branch("next")  # line 682
        _.createFile(3, "y" * 10)  # make a change  # line 683
        sos.delete("added", "--force")  # should succeed  # line 684

    def testUsage(_):  # line 686
        sos.usage()  # line 687

    def testOnly(_):  # line 689
        _.assertEqual((_coconut.frozenset(((".", "./A"), ("x", "x/B"))), _coconut.frozenset(((".", "./C"),))), sos.parseOnlyOptions(".", ["abc", "def", "--only", "A", "--x", "--only", "x/B", "--except", "C", "--only"]))  # line 690
        _.assertEqual(_coconut.frozenset(("B",)), sos.conditionalIntersection(_coconut.frozenset(("A", "B", "C")), _coconut.frozenset(("B", "D"))))  # line 691
        _.assertEqual(_coconut.frozenset(("B", "D")), sos.conditionalIntersection(_coconut.frozenset(), _coconut.frozenset(("B", "D"))))  # line 692
        _.assertEqual(_coconut.frozenset(("B", "D")), sos.conditionalIntersection(None, _coconut.frozenset(("B", "D"))))  # line 693

    def testDiff(_):  # line 695
        sos.offline(options=["--strict"])  # line 696
        _.createFile(1)  # line 697
        _.createFile(2)  # line 698
        sos.commit()  # line 699
        _.createFile(1, "sdfsdgfsdf")  # line 700
        _.createFile(2, "12343")  # line 701
        sos.commit()  # line 702
        _.createFile(1, "foobar")  # line 703
        _.assertAllIn(["MOD ./file1", "MOD ./file2", "DIF ./file1", "- | 0000 |xxxxxxxxxx|", "+ | 0000 |foobar|"], wrapChannels(lambda: sos.diff("/-2")))  # vs. second last  # line 704
        _.assertNotIn("MOD ./file1", wrapChannels(lambda: sos.diff("/-2", onlys=_coconut.frozenset(("./file2",)))))  # line 705

    def testFindBase(_):  # line 707
        old = os.getcwd()  # line 708
        try:  # line 709
            os.mkdir("." + os.sep + ".git")  # line 710
            os.makedirs("." + os.sep + "a" + os.sep + sos.metaFolder)  # line 711
            os.makedirs("." + os.sep + "a" + os.sep + "b")  # line 712
            os.chdir("a" + os.sep + "b")  # line 713
            s, vcs, cmd = sos.findSosVcsBase()  # line 714
            _.assertIsNotNone(s)  # line 715
            _.assertIsNotNone(vcs)  # line 716
            _.assertEqual("git", cmd)  # line 717
        finally:  # line 718
            os.chdir(old)  # line 718


if __name__ == '__main__':  # line 721
    logging.basicConfig(level=logging.DEBUG if '-v' in sys.argv or os.getenv("DEBUG", "false").strip().lower() == "true" or os.getenv("CI", "false").strip().lower() == "true" else logging.INFO, stream=sys.stderr, format="%(asctime)-23s %(levelname)-8s %(name)s:%(lineno)d | %(message)s" if '-v' in sys.argv or os.getenv("DEBUG", "false") == "true" else "%(message)s")  # line 722
    if configr:  # line 723
        c = configr.Configr("sos")  # line 724
        c.loadSettings()  # line 724
        if len(c.keys()) > 0:  # line 725
            sos.Exit("Cannot run test suite with existing local SOS user configuration (would affect results)")  # line 725
    unittest.main(testRunner=debugTestRunner() if '-v' in sys.argv and not os.getenv("CI", "false").lower() == "true" else None)  # warnings = "ignore")  # line 726
