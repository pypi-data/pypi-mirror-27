#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# __coconut_hash__ = 0x9f034905

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

# Standard modules
import codecs  # line 6
import collections  # line 6
import fnmatch  # line 6
import json  # line 6
import logging  # line 6
import mimetypes  # line 6
import os  # line 6
import shutil  # line 6
sys = _coconut_sys  # line 6
import time  # line 6
try:  # line 7
    from typing import Any  # only required for mypy  # line 8
    from typing import Dict  # only required for mypy  # line 8
    from typing import FrozenSet  # only required for mypy  # line 8
    from typing import IO  # only required for mypy  # line 8
    from typing import Iterator  # only required for mypy  # line 8
    from typing import List  # only required for mypy  # line 8
    from typing import Set  # only required for mypy  # line 8
    from typing import Tuple  # only required for mypy  # line 8
    from typing import Type  # only required for mypy  # line 8
    from typing import Union  # only required for mypy  # line 8
except:  # typing not available (e.g. Python 2)  # line 9
    pass  # typing not available (e.g. Python 2)  # line 9
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))  # line 10
try:  # line 11
    from sos import version  # line 12
    from sos.utility import *  # line 13
except:  # line 14
    import version  # line 15
    from utility import *  # line 16

# External dependencies
try:  # optional dependency  # line 19
    import configr  # optional dependency  # line 19
except:  # declare as undefined  # line 20
    configr = None  # declare as undefined  # line 20
#from enforce import runtime_validation  # https://github.com/RussBaz/enforce  TODO doesn't work for "data" types


# Constants
APPNAME = "Subversion Offline Solution  V%s  (C) Arne Bachmann" % version.__release_version__  # type: str  # line 25
defaults = Accessor({"strict": False, "track": False, "picky": False, "compress": True, "tags": [], "texttype": [], "bintype": [], "ignoreDirs": [".*", "__pycache__"], "ignoreDirsWhitelist": [], "ignores": ["__coconut__.py", "*.bak", "*.py[cdo]", "*.class", ".fslckout"], "ignoresWhitelist": []})  # line 26
termWidth = getTermWidth() - 1  # uses curses or returns conservative default of 80  # line 27


# Functions
def loadConfig() -> 'Union[configr.Configr, Accessor]':  # Simplifies loading config from file system or returning the defaults  # line 31
    config = None  # type: Union[configr.Configr, Accessor]  # line 32
    if not configr:  # this only applies for the case that configr is not available, thus no settings will be persisted anyway  # line 33
        return defaults  # this only applies for the case that configr is not available, thus no settings will be persisted anyway  # line 33
    config = configr.Configr("sos", defaults=defaults)  # defaults are used if key is not configured, but won't be saved  # line 34
    f, g = config.loadSettings(clientCodeLocation=os.path.abspath(__file__), location=os.environ.get("TEST", None))  # line 35
    if f is None:  # line 36
        debug("Encountered a problem while loading the user configuration: %r" % g)  # line 36
    return config  # line 37

@_coconut_tco  # line 39
def saveConfig(config: 'configr.Configr') -> 'Tuple[_coconut.typing.Optional[str], _coconut.typing.Optional[Exception]]':  # line 39
    return _coconut_tail_call(config.saveSettings, clientCodeLocation=os.path.abspath(__file__), location=os.environ.get("TEST", None))  # line 40

def usage(short: 'bool'=False) -> 'None':  # line 42
    print("//|\\\\ {appname} {version} //|\\\\".format(appname=APPNAME, version="" if not short else "(PyPI: %s)" % version.__version__))  # line 43
    if not short:  # line 44
        print("""

Usage: {cmd} <command> [<argument>] [<option1>, ...]        When operating in offline mode, or command is one of "help", "offline", "version"
       {cmd} --sos <sos command and arguments>              When operating in offline mode, forced passthrough to SOS
       {cmd} --vcs <underlying vcs command and arguments>   When operating in offline mode, forced passthrough to traditional VCS
       {cmd} <underlying vcs command and arguments>         When operating in online mode, automatic passthrough to traditional VCS

  Available commands:
    offline [<name>]                                      Start working offline, creating a branch (named <name>), default name depending on VCS
      --plain                                               Don't compress versioned files (same as `sos config set compress off`)
      --track                                               Setup SVN-style mode: users add/remove tracking patterns per branch
      --picky                                               Setup Git-style mode: users pick files for each operation
    online                                                Finish working offline

    branch  [<name>] [--last] [--stay]                    Create a new branch from current file tree and switch to it
      --last                                                Use last revision, not current file tree, but keep file tree unchanged
      --stay                                                Don't switch to new branch, continue on current one
    switch  [<branch>][/<revision>] [--meta]              Continue work on another branch
      --meta                                                Only switch file tracking patterns for current branch, don't update any files
    update  [<branch>][/<revision>]                       Integrate work from another branch  TODO add many merge and conflict resolution options
    destroy [<branch>]                                    Remove (current) branch entirely

    commit  [<message>] [--tag]                           Create a new revision from current state file tree, with an optional commit message
    changes [<branch>][/<revision>]                       List changed paths vs. last or specified revision
    diff    [<branch>][/<revision>] [--from=branch/rev.]  List changes in file tree (or `--from` specified revision) vs. last (or specified) revision
    add     [<file pattern>]                              Add a tracking pattern to current branch (file pattern)
    mv      [<oldpattern>] [<newPattern>]                 Rename, move, or move and rename tracked files according to tracked file patterns
      --soft                                              Don't move or rename files, only the tracking pattern
    rm      [<file pattern>]                              Remove a tracking pattern. Only useful after "offline --track" or "offline --picky"

    ls [<folder path>] [--patterns]                       List file tree and mark changes and tracking status
    status                                                List branches and display repository status
    log [--changes]                                       List commits of current branch
    config  [set/unset/show/add/rm] [<param> [<value>]]   Configure user-global defaults.
                                                          Flags (1/0, on/off, true/false, yes/no):
                                                            strict, track, picky, compress
                                                          Lists (semicolon-separated when set; single values for add/rm):
                                                            texttype, bintype, ignores, ignoreDirs, ignoresWhitelist, ignoreDirsWhitelist
                                                          Supported texts:
                                                            defaultbranch (has a dynamic default value, depending on VCS discovered)
    help, --help                                          Show this usage information

  Arguments:
    <branch/revision>            Revision string. Branch is optional and may be a label or index
                                 Revision is an optional integer and may be negative to reference from the latest commits (-1 is most recent revision)

  Common options:
    --force                      Executes potentially harmful operations
                                   for offline: ignore being already offline, start from scratch (same as 'sos online --force && sos offline')
                                   for online: ignore uncommitted branches
                                   for commit, switch, update, add: ignore uncommitted changes before executing command
    --strict                     Always perform full content comparison, don't rely only on file size and timestamp
                                   for offline command: memorize strict mode setting in repository
                                   for changes, diff, commit, switch, update, delete: perform operation in strict mode, regardless of repository setting
    --only   <tracked pattern>   Restrict operation to specified pattern(s). Available for "changes", "commit", "diff", "switch", and "update"
    --except <tracked pattern>   Avoid operation for specified pattern(s). Available for "changes", "commit", "diff", "switch", and "update"
    --{cmd}                      When executing {CMD} not being offline, pass arguments to {CMD} instead (e.g. {cmd} --{cmd} config set key value.)
    --log                        Enable logging details
    --verbose                    Enable verbose output""".format(appname=APPNAME, cmd="sos", CMD="SOS"))  # line 102

# Main data class
#@runtime_validation
class Metadata:  # line 106
    ''' This class doesn't represent the entire repository state in memory,
      but serves as a container for different repo operations,
      using only parts of its attributes at any point in time. Use with care.
  '''  # line 110

    def __init__(_, path: 'str') -> 'None':  # line 112
        ''' Create empty container object for various repository operations. '''  # line 113
        _.c = loadConfig()  # line 114
        _.root = path  # type: str  # line 115
        _.branches = {}  # type: Dict[int, BranchInfo]  # branch number zero represents the initial state at branching  # line 116
        _.commits = {}  # type: Dict[int, CommitInfo]  # consecutive numbers per branch, starting at 0  # line 117
        _.paths = {}  # type: Dict[str, PathInfo]  # utf-8 encoded relative, normalized file system paths  # line 118
        _.tags = []  # type: List[str]  # line 119
        _.branch = None  # type: _coconut.typing.Optional[int]  # current branch number  # line 120
        _.commit = None  # type: _coconut.typing.Optional[int]  # current revision number  # line 121
        _.track = _.c.track  # type: bool  # track file name patterns in the repository (per branch)  # line 122
        _.picky = _.c.picky  # type: bool  # pick files to commit per operation  # line 123
        _.strict = _.c.strict  # type: bool  # be always strict (regarding file contents comparsion)  # line 124
        _.compress = _.c.compress  # type: bool  # these flags are stored in the repository  # line 125

    def isTextType(_, filename: 'str') -> 'bool':  # line 127
        return (((lambda _coconut_none_coalesce_item: "" if _coconut_none_coalesce_item is None else _coconut_none_coalesce_item)(mimetypes.guess_type(filename)[0])).startswith("text/") or any([fnmatch.fnmatch(filename, pattern) for pattern in _.c.texttype])) and not any([fnmatch.fnmatch(filename, pattern) for pattern in _.c.bintype])  # line 127

    def listChanges(_, changes: 'ChangeSet') -> 'None':  # line 129
        if len(changes.additions) > 0:  # line 130
            print(ajoin("ADD ", sorted(changes.additions.keys()), "\n"))  # line 130
        if len(changes.deletions) > 0:  # line 131
            print(ajoin("DEL ", sorted(changes.deletions.keys()), "\n"))  # line 131
        if len(changes.modifications) > 0:  # line 132
            print(ajoin("MOD ", sorted(changes.modifications.keys()), "\n"))  # line 132

    def loadBranches(_) -> 'None':  # line 134
        ''' Load list of branches and current branch info from metadata file. '''  # line 135
        try:  # fails if not yet created (on initial branch/commit)  # line 136
            branches = None  # type: List[Tuple]  # line 137
            with codecs.open(os.path.join(_.root, metaFolder, metaFile), "r", encoding=UTF8) as fd:  # line 138
                flags, branches = json.load(fd)  # line 139
            _.tags = flags["tags"]  # list of commit messages to treat as globally unique tags  # line 140
            _.branch = flags["branch"]  # current branch integer  # line 141
            _.track = flags["track"]  # line 142
            _.picky = flags["picky"]  # line 143
            _.strict = flags["strict"]  # line 144
            _.compress = flags["compress"]  # line 145
            _.branches = {i.number: i for i in (BranchInfo(*item) for item in branches)}  # re-create type info  # line 146
        except Exception as E:  # if not found, create metadata folder  # line 147
            _.branches = {}  # line 148
            warn("Couldn't read branches metadata: %r" % E)  # line 149

    def saveBranches(_) -> 'None':  # line 151
        ''' Save list of branches and current branch info to metadata file. '''  # line 152
        with codecs.open(os.path.join(_.root, metaFolder, metaFile), "w", encoding=UTF8) as fd:  # line 153
            json.dump(({"tags": _.tags, "branch": _.branch, "track": _.track, "picky": _.picky, "strict": _.strict, "compress": _.compress}, list(_.branches.values())), fd, ensure_ascii=False)  # line 154

    def getRevisionByName(_, name: 'str') -> '_coconut.typing.Optional[int]':  # line 156
        ''' Convenience accessor for named revisions (using commit message as name). '''  # line 157
        if name == "":  # line 158
            return -1  # line 158
        try:  # attempt to parse integer string  # line 159
            return longint(name)  # attempt to parse integer string  # line 159
        except ValueError:  # line 160
            pass  # line 160
        found = [number for number, commit in _.commits.items() if name == commit.message]  # line 161
        return found[0] if found else None  # line 162

    def getBranchByName(_, name: 'str') -> '_coconut.typing.Optional[int]':  # line 164
        ''' Convenience accessor for named branches. '''  # line 165
        if name == "":  # line 166
            return _.branch  # line 166
        try:  # attempt to parse integer string  # line 167
            return longint(name)  # attempt to parse integer string  # line 167
        except ValueError:  # line 168
            pass  # line 168
        found = [number for number, branch in _.branches.items() if name == branch.name]  # line 169
        return found[0] if found else None  # line 170

    def loadBranch(_, branch: 'int') -> 'None':  # line 172
        ''' Load all commit information from a branch meta data file. '''  # line 173
        with codecs.open(os.path.join(_.root, metaFolder, "b%d" % branch, metaFile), "r", encoding=UTF8) as fd:  # line 174
            commits = json.load(fd)  # type: List[List[Any]]  # list of CommitInfo that needs to be unmarshalled into value types  # line 175
        _.commits = {i.number: i for i in (CommitInfo(*item) for item in commits)}  # re-create type info  # line 176
        _.branch = branch  # line 177

    def saveBranch(_, branch: 'int') -> 'None':  # line 179
        ''' Save all commit information to a branch meta data file. '''  # line 180
        with codecs.open(os.path.join(_.root, metaFolder, "b%d" % branch, metaFile), "w", encoding=UTF8) as fd:  # line 181
            json.dump(list(_.commits.values()), fd, ensure_ascii=False)  # line 182

    def duplicateBranch(_, branch: 'int', name: '_coconut.typing.Optional[str]') -> 'None':  # line 184
        ''' Create branch from an existing branch/revision. WARN: Caller must have loaded branches information.
        branch: target branch (should not exist yet)
        name: optional name of new branch
        _.branch: current branch
    '''  # line 189
        debug("Duplicating branch '%s' to '%s'..." % ((lambda _coconut_none_coalesce_item: ("b%d" % _.branch) if _coconut_none_coalesce_item is None else _coconut_none_coalesce_item)(_.branches[_.branch].name), ("b%d" % branch if name is None else name)))  # line 190
        tracked = [t for t in _.branches[_.branch].tracked]  # copy  # line 191
        os.makedirs(os.path.join(_.root, metaFolder, "b%d" % branch, "r0"))  # line 192
        _.loadBranch(_.branch)  # line 193
        revision = max(_.commits)  # type: int  # line 194
        _.computeSequentialPathSet(_.branch, revision)  # full set of files in revision to _.paths  # line 195
        for path, pinfo in _.paths.items():  # line 196
            _.copyVersionedFile(_.branch, revision, branch, 0, pinfo)  # line 197
        _.commits = {0: CommitInfo(0, longint(time.time() * 1000), "Branched from '%s'" % ((lambda _coconut_none_coalesce_item: "b%d" % _.branch if _coconut_none_coalesce_item is None else _coconut_none_coalesce_item)(_.branches[_.branch].name)))}  # store initial commit  # line 198
        _.saveBranch(branch)  # save branch meta data to branch folder  # line 199
        _.saveCommit(branch, 0)  # save commit meta data to revision folder  # line 200
        _.branches[branch] = BranchInfo(branch, _.commits[0].ctime, name, _.branches[_.branch].inSync, tracked)  # save branch info, before storing repo state at caller  # line 201

    def createBranch(_, branch: 'int', name: '_coconut.typing.Optional[str]'=None, initialMessage: '_coconut.typing.Optional[str]'=None):  # line 203
        ''' Create a new branch from current file tree. This clears all known commits and modifies the file system.
        branch: target branch (should not exist yet)
        name: optional name of new branch
        _.branch: current branch, must exist already
    '''  # line 208
        simpleMode = not (_.track or _.picky)  # line 209
        tracked = [t for t in _.branches[_.branch].tracked] if _.track and len(_.branches) > 0 else []  # in case of initial branch creation  # line 210
        debug((lambda _coconut_none_coalesce_item: "b%d" % branch if _coconut_none_coalesce_item is None else _coconut_none_coalesce_item)("Creating branch '%s'..." % name))  # line 211
        _.paths = {}  # type: Dict[str, PathInfo]  # line 212
        if simpleMode:  # branches from file system state  # line 213
            changes = _.findChanges(branch, 0, progress=simpleMode)  # type: ChangeSet  # creates revision folder and versioned files  # line 214
            _.listChanges(changes)  # line 215
            _.paths.update(changes.additions.items())  # line 216
        else:  # tracking or picky mode: branch from lastest revision  # line 217
            os.makedirs(os.path.join(_.root, metaFolder, "b%d" % branch, "r0"))  # line 218
            if _.branch is not None:  # not immediately after "offline" - copy files from current branch  # line 219
                _.loadBranch(_.branch)  # line 220
                revision = max(_.commits)  # type: int  # TODO what if last switch was to an earlier revision? no persisting of last checkout  # line 221
                _.computeSequentialPathSet(_.branch, revision)  # full set of files in revision to _.paths  # line 222
                for path, pinfo in _.paths.items():  # line 223
                    _.copyVersionedFile(_.branch, revision, branch, 0, pinfo)  # line 224
        ts = longint(time.time() * 1000)  # line 225
        _.commits = {0: CommitInfo(0, ts, "Branched on %s" % strftime(ts) if initialMessage is None else initialMessage)}  # store initial commit for new branch  # line 226
        _.saveBranch(branch)  # save branch meta data (revisions) to branch folder  # line 227
        _.saveCommit(branch, 0)  # save commit meta data to revision folder  # line 228
        _.branches[branch] = BranchInfo(branch, _.commits[0].ctime, name, True if len(_.branches) == 0 else _.branches[_.branch].inSync, tracked)  # save branch info, in case it is needed  # line 229

    def removeBranch(_, branch: 'int') -> 'BranchInfo':  # line 231
        ''' Entirely remove a branch and all its revisions from the file system. '''  # line 232
        shutil.rmtree(os.path.join(_.root, metaFolder, "b%d" % branch))  # line 233
        binfo = _.branches[branch]  # line 234
        del _.branches[branch]  # line 235
        _.branch = max(_.branches)  # line 236
        _.saveBranches()  # line 237
        _.commits.clear()  # line 238
        return binfo  # line 239

    def loadCommit(_, branch: 'int', revision: 'int') -> 'None':  # line 241
        ''' Load all file information from a commit meta data. '''  # line 242
        with codecs.open(os.path.join(_.root, metaFolder, "b%d" % branch, "r%d" % revision, metaFile), "r", encoding=UTF8) as fd:  # line 243
            _.paths = json.load(fd)  # line 244
        _.paths = {path: PathInfo(*item) for path, item in _.paths.items()}  # re-create type info  # line 245
        _.branch = branch  # line 246

    def saveCommit(_, branch: 'int', revision: 'int'):  # line 248
        ''' Save all file information to a commit meta data file. '''  # line 249
        target = os.path.join(_.root, metaFolder, "b%d" % branch, "r%d" % revision)  # line 250
        try:  # line 251
            os.makedirs(target)  # line 251
        except:  # line 252
            pass  # line 252
        with codecs.open(os.path.join(target, metaFile), "w", encoding=UTF8) as fd:  # line 253
            json.dump(_.paths, fd, ensure_ascii=False)  # line 254

    def findChanges(_, branch: '_coconut.typing.Optional[int]'=None, revision: '_coconut.typing.Optional[int]'=None, checkContent: 'bool'=False, inverse: 'bool'=False, considerOnly: '_coconut.typing.Optional[FrozenSet[str]]'=None, dontConsider: '_coconut.typing.Optional[FrozenSet[str]]'=None, progress: 'bool'=False) -> 'ChangeSet':  # line 256
        ''' Find changes on the file system vs. in-memory paths (which should reflect the latest commit state).
        Only if both branch and revision are *not* None, write modified/added files to the specified revision folder (thus creating a new revision)
        The function returns the state of file tree *differences*, unless "inverse" is True -> then return original data
        checkContent: also computes file content hashes
        inverse: retain original state (size, mtime, hash) instead of updated one
        considerOnly: set of tracking patterns. None for simple mode. For update operation, consider union of other and current branch
        dontConsider: set of tracking patterns to not consider in changes
        progress: Show file names during processing
    '''  # line 265
        write = branch is not None and revision is not None  # line 266
        if write:  # line 267
            os.makedirs(os.path.join(_.root, metaFolder, "b%d" % branch, "r%d" % revision))  # line 267
        changes = ChangeSet({}, {}, {})  # type: ChangeSet  # line 268
        counter = Counter(-1)  # type: Counter  # line 269
        timer = time.time()  # line 269
        hashed = None  # type: _coconut.typing.Optional[str]  # line 270
        written = None  # type: longint  # line 270
        compressed = 0  # type: longint  # line 270
        original = 0  # type: longint  # line 270
        knownPaths = collections.defaultdict(list)  # type: Dict[str, List[str]]  # line 271
        for path, pinfo in _.paths.items():  # line 272
            if pinfo.size is not None and (considerOnly is None or any((path[:path.rindex(SLASH)] == pattern[:pattern.rindex(SLASH)] and fnmatch.fnmatch(path[path.rindex(SLASH) + 1:], pattern[pattern.rindex(SLASH) + 1:]) for pattern in considerOnly))) and (dontConsider is None or not any((path[:path.rindex(SLASH)] == pattern[:pattern.rindex(SLASH)] and fnmatch.fnmatch(path[path.rindex(SLASH) + 1:], pattern[pattern.rindex(SLASH) + 1:]) for pattern in dontConsider))):  # line 273
                knownPaths[os.path.dirname(path)].append(os.path.basename(path))  # TODO reimplement using fnmatch.filter and set operations for all files per path for speed  # line 276
        for path, dirnames, filenames in os.walk(_.root):  # line 277
            dirnames[:] = [f for f in dirnames if len([n for n in _.c.ignoreDirs if fnmatch.fnmatch(f, n)]) == 0 or len([p for p in _.c.ignoreDirsWhitelist if fnmatch.fnmatch(f, p)]) > 0]  # line 278
            filenames[:] = [f for f in filenames if len([n for n in _.c.ignores if fnmatch.fnmatch(f, n)]) == 0 or len([p for p in _.c.ignoresWhitelist if fnmatch.fnmatch(f, p)]) > 0]  # line 279
            dirnames.sort()  # line 280
            filenames.sort()  # line 280
            relPath = os.path.relpath(path, _.root).replace(os.sep, SLASH)  # line 281
            walk = filenames if considerOnly is None else list(reduce(lambda last, pattern: last | set(fnmatch.filter(filenames, os.path.basename(pattern))), (p for p in considerOnly if os.path.dirname(p).replace(os.sep, SLASH) == relPath), _coconut.set()))  # line 282
            if dontConsider:  # line 283
                walk[:] = [fn for fn in walk if not any((fnmatch.fnmatch(fn, os.path.basename(p)) for p in dontConsider if os.path.dirname(p).replace(os.sep, SLASH) == relPath))]  # line 284
            for file in walk:  # if m.track or m.picky: only files that match any path-relevant tracking patterns  # line 285
                filename = relPath + SLASH + file  # line 286
                filepath = os.path.join(path, file)  # line 287
                stat = os.stat(filepath)  # line 288
                size, mtime, newtime = stat.st_size, longint(stat.st_mtime * 1000), time.time()  # line 289
                if progress and newtime - timer > .1:  # line 290
                    outstring = "\rPreparing %s  %s" % (PROGRESS_MARKER[counter.inc() % 4], filename)  # line 291
                    sys.stdout.write(outstring + " " * max(0, termWidth - len(outstring)))  # TODO could write to new line instead of carriage return (still true?)  # line 292
                    sys.stdout.flush()  # TODO could write to new line instead of carriage return (still true?)  # line 292
                    timer = newtime  # TODO could write to new line instead of carriage return (still true?)  # line 292
                if filename not in _.paths:  # detected file not present (or untracked) in (other) branch  # line 293
                    nameHash = hashStr(filename)  # line 294
                    hashed, written = hashFile(filepath, _.compress, saveTo=os.path.join(_.root, metaFolder, "b%d" % branch, "r%d" % revision, nameHash) if write else None) if size > 0 else (None, 0)  # line 295
                    changes.additions[filename] = PathInfo(nameHash, size, mtime, hashed)  # line 296
                    compressed += written  # line 297
                    original += size  # line 297
                    continue  # line 298
                last = _.paths[filename]  # filename is known - check for modifications  # line 299
                if last.size is None:  # was removed before but is now added back - does not apply for tracking mode (which never marks files for removal in the history)  # line 300
                    hashed, written = hashFile(filepath, _.compress, saveTo=os.path.join(_.root, metaFolder, "b%d" % branch, "r%d" % revision, last.nameHash) if write else None) if size > 0 else (None, 0)  # line 301
                    changes.additions[filename] = PathInfo(last.nameHash, size, mtime, hashed)  # line 302
                    continue  # line 302
                elif size != last.size or mtime != last.mtime or (checkContent and hashFile(filepath, _.compress)[0] != last.hash):  # detected a modification  # line 303
                    hashed, written = hashFile(filepath, _.compress, saveTo=os.path.join(_.root, metaFolder, "b%d" % branch, "r%d" % revision, last.nameHash) if write else None) if (last.size if inverse else size) > 0 else (last.hash if inverse else None, 0)  # line 304
                    changes.modifications[filename] = PathInfo(last.nameHash, last.size if inverse else size, last.mtime if inverse else mtime, hashed)  # line 305
                else:  # line 306
                    continue  # line 306
                compressed += written  # line 307
                original += last.size if inverse else size  # line 307
            if relPath in knownPaths:  # at least one file is tracked  # line 308
                knownPaths[relPath][:] = list(set(knownPaths[relPath]) - set(walk))  # at least one file is tracked  # line 308
        for path, names in knownPaths.items():  # all paths that weren't walked by  # line 309
            for file in names:  # line 310
                changes.deletions[path + SLASH + file] = _.paths[path + SLASH + file]  # line 310
        if progress:  # force new line  # line 311
            print("\rPreparation finished. Compression factor %s" % ("is %.1f" % (original * 100. / compressed) if compressed > 0 else "cannot be computed").ljust(termWidth), file=sys.stdout)  # force new line  # line 311
        else:  # line 312
            debug("Finished detecting changes. Compression factor %s" % ("is %.1f" % (original * 100. / compressed) if compressed > 0 else "cannot be computed"))  # line 312
        return changes  # line 313

    def integrateChangeset(_, changes: 'ChangeSet', clear=False) -> 'None':  # line 315
        ''' In-memory update from a changeset, marking deleted files with size=None. Use clear = True to start on an empty path set. '''  # line 316
        if clear:  # line 317
            _.paths.clear()  # line 317
        else:  # line 318
            rm = [p for p, info in _.paths.items() if info.size is None]  # remove files deleted in earlier change sets (revisions)  # line 319
            for old in rm:  # remove previously removed entries completely  # line 320
                del _.paths[old]  # remove previously removed entries completely  # line 320
        for d, info in changes.deletions.items():  # mark now removed entries as deleted  # line 321
            _.paths[d] = PathInfo(info.nameHash, None, info.mtime, None)  # mark now removed entries as deleted  # line 321
        _.paths.update(changes.additions)  # line 322
        _.paths.update(changes.modifications)  # line 323

    def computeSequentialPathSet(_, branch: 'int', revision: 'int') -> 'None':  # line 325
        next(_.computeSequentialPathSetIterator(branch, revision, incrementally=False))  # simply invoke the generator once  # line 326

    def computeSequentialPathSetIterator(_, branch: 'int', revision: 'int', incrementally: 'bool'=True) -> '_coconut.typing.Optional[Iterator[ChangeSet]]':  # line 328
        ''' In-memory computation of current list of valid PathInfo entries for specified branch and until specified revision (inclusively) by traversing revision on the file system. '''  # line 329
        _.loadCommit(branch, 0)  # load initial paths  # line 330
        if incrementally:  # line 331
            yield diffPathSets({}, _.paths)  # line 331
        n = Metadata(_.root)  # type: Metadata  # next changes  # line 332
        for revision in range(1, revision + 1):  # line 333
            n.loadCommit(branch, revision)  # line 334
            changes = diffPathSets(_.paths, n.paths)  # type: ChangeSet  # line 335
            _.integrateChangeset(changes)  # line 336
            if incrementally:  # line 337
                yield changes  # line 337
        yield None  # for the default case - not incrementally  # line 338

    def parseRevisionString(_, argument: 'str') -> 'Tuple[_coconut.typing.Optional[int], _coconut.typing.Optional[int]]':  # line 340
        ''' Commit identifiers can be str or int for branch, and int for revision.
        Revision identifiers can be negative, with -1 being last commit.
    '''  # line 343
        if argument is None or argument == SLASH:  # no branch/revision specified  # line 344
            return (_.branch, -1)  # no branch/revision specified  # line 344
        argument = argument.strip()  # line 345
        if argument.startswith(SLASH):  # current branch  # line 346
            return (_.branch, _.getRevisionByName(argument[1:]))  # current branch  # line 346
        if argument.endswith(SLASH):  # line 347
            try:  # line 348
                return (_.getBranchByName(argument[:-1]), -1)  # line 348
            except ValueError:  # line 349
                Exit("Unknown branch label '%s'" % argument)  # line 349
        if SLASH in argument:  # line 350
            b, r = argument.split(SLASH)[:2]  # line 351
            try:  # line 352
                return (_.getBranchByName(b), _.getRevisionByName(r))  # line 352
            except ValueError:  # line 353
                Exit("Unknown branch label or wrong number format '%s/%s'" % (b, r))  # line 353
        branch = _.getBranchByName(argument)  # type: int  # returns number if given (revision) integer  # line 354
        if branch not in _.branches:  # line 355
            branch = None  # line 355
        try:  # either branch name/number or reverse/absolute revision number  # line 356
            return (_.branch if branch is None else branch, longint(argument if argument else "-1") if branch is None else -1)  # either branch name/number or reverse/absolute revision number  # line 356
        except:  # line 357
            Exit("Unknown branch label or wrong number format")  # line 357
        Exit("This should never happen")  # line 358
        return (None, None)  # line 358

    def findRevision(_, branch: 'int', revision: 'int', nameHash: 'str') -> 'Tuple[int, str]':  # line 360
        while True:  # find latest revision that contained the file physically  # line 361
            source = os.path.join(_.root, metaFolder, "b%d" % branch, "r%d" % revision, nameHash)  # type: str  # line 362
            if os.path.exists(source) and os.path.isfile(source):  # line 363
                break  # line 363
            revision -= 1  # line 364
            if revision < 0:  # line 365
                Exit("Cannot determine versioned file '%s' from specified branch '%d'" % (nameHash, branch))  # line 365
        return revision, source  # line 366

    def copyVersionedFile(_, branch: 'int', revision: 'int', toBranch: 'int', toRevision: 'int', pinfo: 'PathInfo') -> 'None':  # line 368
        ''' Copy versioned file to other branch/revision. '''  # line 369
        target = os.path.join(_.root, metaFolder, "b%d" % toBranch, "r%d" % toRevision, pinfo.nameHash)  # type: str  # line 370
        revision, source = _.findRevision(branch, revision, pinfo.nameHash)  # line 371
        shutil.copy2(source, target)  # line 372

    def readOrCopyVersionedFile(_, branch: 'int', revision: 'int', nameHash: 'str', toFile: '_coconut.typing.Optional[str]'=None) -> '_coconut.typing.Optional[bytes]':  # line 374
        ''' Return file contents, or copy contents into file path provided. '''  # line 375
        source = os.path.join(_.root, metaFolder, "b%d" % branch, "r%d" % revision, nameHash)  # type: str  # line 376
        try:  # line 377
            with openIt(source, "r", _.compress) as fd:  # line 378
                if toFile is None:  # read bytes into memory and return  # line 379
                    return fd.read()  # read bytes into memory and return  # line 379
                with open(toFile, "wb") as to:  # line 380
                    while True:  # line 381
                        buffer = fd.read(bufSize)  # line 382
                        to.write(buffer)  # line 383
                        if len(buffer) < bufSize:  # line 384
                            break  # line 384
                    return None  # line 385
        except Exception as E:  # line 386
            warn("Cannot read versioned file: %r (%d/%d/%s)" % (E, branch, revision, nameHash))  # line 386
        return None  # line 387

    def restoreFile(_, relPath: '_coconut.typing.Optional[str]', branch: 'int', revision: 'int', pinfo: 'PathInfo', ensurePath: 'bool'=False) -> '_coconut.typing.Optional[bytes]':  # line 389
        ''' Recreate file for given revision, or return contents if path is None. '''  # line 390
        if relPath is None:  # just return contents  # line 391
            return _.readOrCopyVersionedFile(branch, _.findRevision(branch, revision, pinfo.nameHash)[0], pinfo.nameHash) if pinfo.size > 0 else b''  # just return contents  # line 391
        target = os.path.join(_.root, relPath.replace(SLASH, os.sep))  # type: str  # line 392
        if ensurePath:  #  and not os.path.exists(os.path.dirname(target)):  # line 393
            try:  # line 394
                os.makedirs(os.path.dirname(target))  # line 394
            except:  # line 395
                pass  # line 395
        if pinfo.size == 0:  # line 396
            with open(target, "wb"):  # line 397
                pass  # line 397
            try:  # update access/modification timestamps on file system  # line 398
                os.utime(target, (-1, pinfo.mtime / 1000.))  # update access/modification timestamps on file system  # line 398
            except Exception as E:  # line 399
                error("Cannot update file's timestamp after restoration '%r'" % E)  # line 399
            return None  # line 400
        revision, source = _.findRevision(branch, revision, pinfo.nameHash)  # line 401
# Restore file by copying buffer-wise
        with openIt(source, "r", _.compress) as fd, open(target, "wb") as to:  # using Coconut's Enhanced Parenthetical Continuation  # line 403
            while True:  # line 404
                buffer = fd.read(bufSize)  # line 405
                to.write(buffer)  # line 406
                if len(buffer) < bufSize:  # line 407
                    break  # line 407
        try:  # update access/modification timestamps on file system  # line 408
            os.utime(target, (-1, pinfo.mtime / 1000.))  # update access/modification timestamps on file system  # line 408
        except Exception as E:  # line 409
            error("Cannot update file's timestamp after restoration '%r'" % E)  # line 409
        return None  # line 410

    def getTrackingPatterns(_, branch: '_coconut.typing.Optional[int]'=None) -> 'FrozenSet[str]':  # line 412
        ''' Returns list of tracking patterns for provided branch or current branch. '''  # line 413
        return _coconut.frozenset() if not _.track and not _.picky else frozenset(_.branches[_.branch if branch is None else branch].tracked)  # line 414


# Main client operations
def offline(argument: '_coconut.typing.Optional[str]'=None, options: '_coconut.typing.Sequence[str]'=[]) -> 'None':  # line 418
    ''' Initial command to start working offline. '''  # line 419
    if os.path.exists(metaFolder):  # line 420
        if '--force' not in options:  # line 421
            Exit("Repository folder is either already offline or older branches and commits were left over.\nUse 'sos online' to check for dirty branches, or\nWipe existing offline branches with 'sos offline --force'")  # line 421
        try:  # line 422
            for entry in os.listdir(metaFolder):  # line 423
                resource = metaFolder + os.sep + entry  # line 424
                if os.path.isdir(resource):  # line 425
                    shutil.rmtree(resource)  # line 425
                else:  # line 426
                    os.unlink(resource)  # line 426
        except:  # line 427
            Exit("Cannot reliably remove previous repository contents. Please remove .sos folder manually prior to going offline")  # line 427
    m = Metadata(os.getcwd())  # type: Metadata  # line 428
    if '--plain' in options or not m.c.compress:  # plain file copies instead of compressed ones  # line 429
        m.compress = False  # plain file copies instead of compressed ones  # line 429
    if '--picky' in options or m.c.picky:  # Git-like  # line 430
        m.picky = True  # Git-like  # line 430
    elif '--track' in options or m.c.track:  # Svn-like  # line 431
        m.track = True  # Svn-like  # line 431
    if '--strict' in options or m.c.strict:  # always hash contents  # line 432
        m.strict = True  # always hash contents  # line 432
    debug("Preparing offline repository...")  # line 433
    m.createBranch(0, str(defaults["defaultbranch"]) if argument is None else argument, initialMessage="Offline repository created on %s" % strftime())  # main branch's name may be None (e.g. for fossil)  # line 434
    m.branch = 0  # line 435
    m.saveBranches()  # no change immediately after going offline, going back online won't issue a warning  # line 436
    info("Offline repository prepared. Use 'sos online' to finish offline work")  # line 437

def online(options: '_coconut.typing.Sequence[str]'=[]) -> 'None':  # line 439
    ''' Finish working offline. '''  # line 440
    force = '--force' in options  # type: bool  # line 441
    m = Metadata(os.getcwd())  # line 442
    m.loadBranches()  # line 443
    if any([not b.inSync for b in m.branches.values()]) and not force:  # line 444
        Exit("There are still unsynchronized (dirty) branches.\nUse 'sos log' to list them.\nUse 'sos commit' and 'sos switch' to commit dirty branches to your VCS before leaving offline mode.\nUse 'sos online --force' to erase all aggregated offline revisions")  # line 444
    strict = '--strict' in options or m.strict  # type: bool  # line 445
    if options.count("--force") < 2:  # line 446
        changes = m.findChanges(checkContent=strict, considerOnly=None if not m.track and not m.picky else m.getTrackingPatterns())  # type: ChangeSet  # HINT no option for --only/--except here on purpose. No check for picky here, because online is not a command that considers staged files (but we could use --only here, alternatively)  # line 447
        if modified(changes):  # line 448
            Exit("File tree is modified vs. current branch.\nUse 'sos online --force --force' to continue with removing the offline repository")  # line 448
    try:  # line 449
        shutil.rmtree(metaFolder)  # line 449
        info("Exited offline mode. Continue working with your traditional VCS.")  # line 449
    except Exception as E:  # line 450
        Exit("Error removing offline repository: %r" % E)  # line 450

def branch(argument: '_coconut.typing.Optional[str]'=None, options: '_coconut.typing.Sequence[str]'=[]) -> 'None':  # line 452
    ''' Create a new branch (from file tree or last revision) and (by default) continue working on it. '''  # line 453
    last = '--last' in options  # type: bool  # use last revision for branching, not current file tree  # line 454
    stay = '--stay' in options  # type: bool  # continue on current branch after branching  # line 455
    force = '--force' in options  # type: bool  # branch even with local modifications  # line 456
    m = Metadata(os.getcwd())  # type: Metadata  # line 457
    m.loadBranches()  # line 458
    m.loadBranch(m.branch)  # line 459
    if argument and m.getBranchByName(argument) is not None:  # create a named branch  # line 460
        Exit("Branch '%s' already exists. Cannot proceed" % argument)  # create a named branch  # line 460
    branch = max(m.branches.keys()) + 1  # next branch's key - this isn't atomic but we assume single-user non-concurrent use here  # line 461
    debug("Branching to %sbranch b%02d%s%s..." % ("unnamed " if argument is None else "", branch, " '%s'" % argument if argument else "", " from last revision" if last else ""))  # line 462
    if last:  # line 463
        m.duplicateBranch(branch, "Branched from r%02d/b%02d" % (m.branch, max(m.commits.keys())) if argument is None else argument)  # branch from branch's last revision  # line 464
    else:  # from file tree state  # line 465
        m.createBranch(branch, "Branched from r%02d/b%02d" % (m.branch, max(m.commits.keys())) if argument is None else argument)  # branch from current file tree  # line 466
    if not stay:  # line 467
        m.branch = branch  # line 468
        m.saveBranches()  # line 469
    info("%s new %sbranch b%02d%s" % ("Continue work after branching" if stay else "Switched to", "unnamed " if argument is None else "", branch, " '%s'" % argument if argument else ""))  # line 470

def changes(argument: 'str'=None, options: '_coconut.typing.Sequence[str]'=[], onlys: '_coconut.typing.Optional[FrozenSet[str]]'=None, excps: '_coconut.typing.Optional[FrozenSet[str]]'=None) -> 'ChangeSet':  # line 472
    ''' Show changes of file tree vs. (last or specified) revision on current or specified branch. '''  # line 473
    m = Metadata(os.getcwd())  # type: Metadata  # line 474
    branch = None  # type: _coconut.typing.Optional[int]  # line 474
    revision = None  # type: _coconut.typing.Optional[int]  # line 474
    m.loadBranches()  # knows current branch  # line 475
    strict = '--strict' in options or m.strict  # type: bool  # line 476
    branch, revision = m.parseRevisionString(argument)  # line 477
    if branch not in m.branches:  # line 478
        Exit("Unknown branch")  # line 478
    m.loadBranch(branch)  # knows commits  # line 479
    revision = revision if revision >= 0 else len(m.commits) + revision  # negative indexing  # line 480
    if revision < 0 or revision > max(m.commits):  # line 481
        Exit("Unknown revision r%02d" % revision)  # line 481
    info("//|\\\\ Changes of file tree vs. revision '%s/r%02d'" % ((lambda _coconut_none_coalesce_item: "b%02d" % branch if _coconut_none_coalesce_item is None else _coconut_none_coalesce_item)(m.branches[branch].name), revision))  # line 482
    m.computeSequentialPathSet(branch, revision)  # load all commits up to specified revision  # line 483
    changes = m.findChanges(checkContent=strict, considerOnly=onlys if not m.track and not m.picky else conditionalIntersection(onlys, m.getTrackingPatterns() | m.getTrackingPatterns(branch)), dontConsider=excps)  # type: ChangeSet  # line 484
    m.listChanges(changes)  # line 485
    return changes  # for unit tests only  # line 486

def diff(argument: 'str'="", options: '_coconut.typing.Sequence[str]'=[], onlys: '_coconut.typing.Optional[FrozenSet[str]]'=None, excps: '_coconut.typing.Optional[FrozenSet[str]]'=None) -> 'None':  # line 488
    ''' Show text file differences of file tree vs. (last or specified) revision on current or specified branch. '''  # line 489
    m = Metadata(os.getcwd())  # type: Metadata  # line 490
    branch = None  # type: _coconut.typing.Optional[int]  # line 490
    revision = None  # type: _coconut.typing.Optional[int]  # line 490
    m.loadBranches()  # knows current branch  # line 491
    strict = '--strict' in options or m.strict  # type: bool  # line 492
    _from = {None: option.split("--from=")[1] for option in options if options.startswith("--from=")}.get(None, None)  # type: _coconut.typing.Optional[str]  # line 493
    branch, revision = m.parseRevisionString(argument)  # if nothing given, use last commit  # line 494
    if branch not in m.branches:  # line 495
        Exit("Unknown branch")  # line 495
    m.loadBranch(branch)  # knows commits  # line 496
    revision = revision if revision >= 0 else len(m.commits) + revision  # negative indexing  # line 497
    if revision < 0 or revision > max(m.commits):  # line 498
        Exit("Unknown revision r%02d" % revision)  # line 498
    info("//|\\\\ Differences of file tree vs. revision '%s/r%02d'" % ((lambda _coconut_none_coalesce_item: "b%02d" % branch if _coconut_none_coalesce_item is None else _coconut_none_coalesce_item)(m.branches[branch].name), revision))  # line 499
    m.computeSequentialPathSet(branch, revision)  # load all commits up to specified revision  # line 500
    changes = m.findChanges(checkContent=strict, inverse=True, considerOnly=onlys if not m.track and not m.picky else conditionalIntersection(onlys, m.getTrackingPatterns() | m.getTrackingPatterns(branch)), dontConsider=excps)  # type: ChangeSet  # line 501
    onlyBinaryModifications = dataCopy(ChangeSet, changes, modifications={k: v for k, v in changes.modifications.items() if not m.isTextType(os.path.basename(k))})  # type: ChangeSet  # line 502
    if modified(onlyBinaryModifications):  # line 503
        debug("//|\\\\ File changes")  # line 503
    m.listChanges(onlyBinaryModifications)  # only list modified binary files  # line 504

    if changes.modifications:  # line 506
        debug("%s//|\\\\ Textual modifications" % ("\n" if modified(onlyBinaryModifications) else ""))  # line 506
    for path, pinfo in (c for c in changes.modifications.items() if m.isTextType(os.path.basename(c[0]))):  # only consider modified text files  # line 507
        content = None  # type: _coconut.typing.Optional[bytes]  # ; othr:str[]; curr:str[]  # line 508
        if pinfo.size == 0:  # empty file contents  # line 509
            content = b""  # empty file contents  # line 509
        else:  # versioned file  # line 510
            content = m.restoreFile(None, branch, revision, pinfo)  # versioned file  # line 510
            assert content is not None  # versioned file  # line 510
        abspath = os.path.join(m.root, path.replace(SLASH, os.sep))  # current file  # line 511
        blocks = merge(file=content, intoname=abspath, diffOnly=True)  # type: List[MergeBlock]  # only determine change blocks  # line 512
        print("DIF %s%s" % (path, " <timestamp only>" if len(blocks) == 1 and blocks[0].tipe == MergeBlockType.KEEP else ""))  # line 513
        for block in blocks:  # line 514
            if block.tipe in [MergeBlockType.INSERT, MergeBlockType.REMOVE]:  # line 515
                pass  # TODO print some previous and following lines - which aren't accessible here anymore  # line 516
            if block.tipe == MergeBlockType.INSERT:  # TODO show color via (n)curses or other library?  # line 517
                for no, line in enumerate(block.lines):  # line 518
                    print("+++ %04d |%s|" % (no + block.line, line))  # line 519
            elif block.tipe == MergeBlockType.REMOVE:  # line 520
                for no, line in enumerate(block.lines):  # line 521
                    print("--- %04d |%s|" % (no + block.line, line))  # line 522
            elif block.tipe in [MergeBlockType.REPLACE, MergeBlockType.MODIFY]:  # TODO for MODIFY also show intra-line change ranges  # line 523
                for no, line in enumerate(block.replaces.lines):  # line 524
                    print("- | %04d |%s|" % (no + block.replaces.line, line))  # line 525
                for no, line in enumerate(block.lines):  # line 526
                    print("+ | %04d |%s|" % (no + block.line, line))  # line 527
#      elif block.tipe == MergeBlockType.KEEP: pass
#      elif block.tipe == MergeBlockType.MODIFY:  # intra-line modifications
#      elif block.tipe == MergeBlockType.MOVE:  # intra-line modifications

def commit(argument: '_coconut.typing.Optional[str]'=None, options: '_coconut.typing.Sequence[str]'=[], onlys: '_coconut.typing.Optional[FrozenSet[str]]'=None, excps: '_coconut.typing.Optional[FrozenSet[str]]'=None) -> 'None':  # line 532
    ''' Create new revision from file tree changes vs. last commit. '''  # line 533
    m = Metadata(os.getcwd())  # type: Metadata  # line 534
    m.loadBranches()  # knows current branch  # line 535
    if argument is not None and argument in m.tags:  # line 536
        Exit("Illegal commit message. It was already used as a tag name")  # line 536
    trackingPatterns = m.getTrackingPatterns()  # type: FrozenSet[str]  # SVN-like mode  # line 537
    if m.picky and not trackingPatterns:  # line 538
        Exit("No file patterns staged for commit in picky mode")  # line 538
    changes = None  # type: ChangeSet  # line 539
    m, branch, revision, changes, strict, force, trackingPatterns = exitOnChanges(None, options, commit=True, onlys=onlys, excps=excps)  # special flag creates new revision for detected changes, but abort if no changes  # line 540
    info((lambda _coconut_none_coalesce_item: "b%d" % m.branch if _coconut_none_coalesce_item is None else _coconut_none_coalesce_item)("Committing changes to branch '%s'..." % m.branches[m.branch].name))  # line 541
    m.integrateChangeset(changes, clear=True)  # update pathset to changeset only  # line 542
    m.saveCommit(m.branch, revision)  # revision has already been incremented  # line 543
    m.commits[revision] = CommitInfo(revision, longint(time.time() * 1000), argument)  # comment can be None  # line 544
    m.saveBranch(m.branch)  # line 545
    m.loadBranches()  # TODO is it necessary to load again?  # line 546
    if m.picky:  # line 547
        m.branches[m.branch] = dataCopy(BranchInfo, m.branches[m.branch], tracked=[], inSync=False)  # remove tracked patterns  # line 548
    else:  # track or simple mode  # line 549
        m.branches[m.branch] = dataCopy(BranchInfo, m.branches[m.branch], inSync=False)  # set branch dirty  # line 550
    if "--tag" in options and argument is not None:  # memorize unique tag  # line 551
        m.tags.append(argument)  # memorize unique tag  # line 551
    m.saveBranches()  # line 552
    info("Created new revision r%02d%s (+%02d/-%02d/*%02d)" % (revision, ((" '%s'" % argument) if argument is not None else ""), len(changes.additions), len(changes.deletions), len(changes.modifications)))  # line 553

def status() -> 'None':  # line 555
    ''' Show branches and current repository state. '''  # line 556
    m = Metadata(os.getcwd())  # type: Metadata  # line 557
    m.loadBranches()  # knows current branch  # line 558
    current = m.branch  # type: int  # line 559
    info("//|\\\\ Offline repository status")  # line 560
    print("Content checking %sactivated" % ("" if m.strict else "de"))  # line 561
    print("Data compression %sactivated" % ("" if m.compress else "de"))  # line 562
    print("Repository is in %s mode" % ("tracking" if m.track else ("picky" if m.picky else "simple")))  # line 563
    sl = max([len((lambda _coconut_none_coalesce_item: "" if _coconut_none_coalesce_item is None else _coconut_none_coalesce_item)(b.name)) for b in m.branches.values()])  # type: int  # line 564
    for branch in sorted(m.branches.values(), key=lambda b: b.number):  # line 565
        m.loadBranch(branch.number)  # knows commit history  # line 566
        print("  %s b%02d%s @%s (%s) with %d commits%s" % ("*" if current == branch.number else " ", branch.number, ((" %%%ds" % (sl + 2)) % ("'%s'" % branch.name)) if branch.name else "", strftime(branch.ctime), "in sync" if branch.inSync else "dirty", len(m.commits), ". Last comment: '%s'" % m.commits[max(m.commits)].message if m.commits[max(m.commits)].message else ""))  # line 567
    if m.track or m.picky and len(m.branches[m.branch].tracked) > 0:  # line 568
        info("\nTracked file patterns:")  # line 569
        print(ajoin("  | ", m.branches[m.branch].tracked, "\n"))  # line 570

def exitOnChanges(argument: '_coconut.typing.Optional[str]'=None, options: '_coconut.typing.Sequence[str]'=[], check: 'bool'=True, commit: 'bool'=False, onlys: '_coconut.typing.Optional[FrozenSet[str]]'=None, excps: '_coconut.typing.Optional[FrozenSet[str]]'=None) -> 'Tuple[Metadata, _coconut.typing.Optional[int], int, ChangeSet, bool, bool, FrozenSet[str]]':  # line 572
    ''' Common behavior for switch, update, delete, commit.
      Should not be called for picky mode, unless tracking patterns were added.
      check: stop program on detected change
      commit: don't stop on changes, because that's what we need in the operation
      Returns (Metadata, (current or target) branch, revision, set of changes vs. last commit on current branch, strict, force flags. '''  # line 577
    m = Metadata(os.getcwd())  # type: Metadata  # line 578
    m.loadBranches()  # knows current branch  # line 579
    force = '--force' in options  # type: bool  # line 580
    strict = '--strict' in options or m.strict  # type: bool  # line 581
    if argument is not None:  # line 582
        branch, revision = m.parseRevisionString(argument)  # for early abort  # line 583
        if branch is None:  # line 584
            Exit("Branch '%s' doesn't exist. Cannot proceed" % argument)  # line 584
    m.loadBranch(m.branch)  # knows last commits of *current* branch  # line 585

# Determine current changes
    trackingPatterns = m.getTrackingPatterns()  # type: FrozenSet[str]  # line 588
    m.computeSequentialPathSet(m.branch, max(m.commits))  # load all commits up to specified revision  # line 589
    changes = m.findChanges(m.branch if commit else None, max(m.commits) + 1 if commit else None, checkContent=strict, considerOnly=onlys if not (m.track or m.picky) else conditionalIntersection(onlys, trackingPatterns), dontConsider=excps)  # type: ChangeSet  # line 590
    if check and modified(changes) and not force:  # line 591
        m.listChanges(changes)  # line 592
        if not commit:  # line 593
            Exit("File tree contains changes. Use --force to proceed")  # line 593
    elif commit and not force:  #  and not check  # line 594
        Exit("Nothing to commit")  #  and not check  # line 594

    if argument is not None:  # branch/revision specified  # line 596
        m.loadBranch(branch)  # knows commits of target branch  # line 597
        revision = revision if revision >= 0 else len(m.commits) + revision  # negative indexing  # line 598
        if revision < 0 or revision > max(m.commits):  # line 599
            Exit("Unknown revision r%02d" % revision)  # line 599
        return (m, branch, revision, changes, strict, force, m.getTrackingPatterns(branch))  # line 600
    return (m, m.branch, max(m.commits) + (1 if commit else 0), changes, strict, force, trackingPatterns)  # line 601

def switch(argument: 'str', options: '_coconut.typing.Sequence[str]'=[], onlys: '_coconut.typing.Optional[FrozenSet[str]]'=None, excps: '_coconut.typing.Optional[FrozenSet[str]]'=None) -> 'None':  # line 603
    ''' Continue work on another branch, replacing file tree changes. '''  # line 604
    changes = None  # type: ChangeSet  # line 605
    m, branch, revision, changes, strict, force, trackingPatterns = exitOnChanges(argument, options)  # line 606
    info("//|\\\\ Switching to branch %sb%02d/r%02d" % ("'%s' " % m.branches[branch].name if m.branches[branch].name else "", branch, revision))  # line 607

# Determine file changes from other branch to current file tree
    if '--meta' in options:  # only switch meta data  # line 610
        m.branches[m.branch] = dataCopy(BranchInfo, m.branches[m.branch], tracked=m.branches[branch].tracked)  # line 611
    else:  # full file switch  # line 612
        m.computeSequentialPathSet(branch, revision)  # load all commits up to specified revision for target branch into memory  # line 613
        changes = m.findChanges(checkContent=strict, inverse=True, considerOnly=onlys if not m.track and not m.picky else conditionalIntersection(onlys, trackingPatterns | m.getTrackingPatterns(branch)), dontConsider=excps)  # determine difference of other branch vs. file tree (forced or in sync with current branch; "addition" means exists now and should be removed)  # line 614
        if not modified(changes):  # line 615
            info("No changes to current file tree")  # line 616
        else:  # integration required  # line 617
            for path, pinfo in changes.deletions.items():  # line 618
                m.restoreFile(path, branch, revision, pinfo, ensurePath=True)  # is deleted in current file tree: restore from branch to reach target  # line 619
                print("ADD " + path)  # line 620
            for path, pinfo in changes.additions.items():  # line 621
                os.unlink(os.path.join(m.root, path.replace(SLASH, os.sep)))  # is added in current file tree: remove from branch to reach target  # line 622
                print("DEL " + path)  # line 623
            for path, pinfo in changes.modifications.items():  # line 624
                m.restoreFile(path, branch, revision, pinfo)  # is modified in current file tree: restore from branch to reach target  # line 625
                print("MOD " + path)  # line 626
    m.branch = branch  # line 627
    m.saveBranches()  # store switched path info  # line 628
    info("Switched to branch %sb%02d/r%02d" % ("'%s' " % (m.branches[branch].name if m.branches[branch].name else ""), branch, revision))  # line 629

def update(argument: 'str', options: '_coconut.typing.Sequence[str]'=[], onlys: '_coconut.typing.Optional[FrozenSet[str]]'=None, excps: '_coconut.typing.Optional[FrozenSet[str]]'=None) -> 'None':  # line 631
    ''' Load and integrate a specified other branch/revision into current life file tree.
      In tracking mode, this also updates the set of tracked patterns.
      User options for merge operation: --add (don't remove), --rm (don't insert), --add-lines/--rm-lines (inside each file)
      User options for conflict resolution: --theirs/--mine/--ask
  '''  # line 636
    mrg = firstOfMap({"--add": MergeOperation.INSERT, "--rm": MergeOperation.REMOVE}, options, MergeOperation.BOTH)  # type: int  # default operation is replicate remove state for non-conflicting cases (insertions/deletions)  # line 637
    res = firstOfMap({'--theirs': ConflictResolution.THEIRS, '--mine': ConflictResolution.MINE}, options, ConflictResolution.NEXT)  # type: int  # NEXT means deeper level  # line 638
    mrgline = firstOfMap({'--add-lines': MergeOperation.INSERT, '--rm-lines': MergeOperation.REMOVE}, options, mrg)  # type: int  # default operation for modified files is same as for files  # line 639
    resline = firstOfMap({'--theirs-lines': ConflictResolution.THEIRS, '--mine-lines': ConflictResolution.MINE}, options, ConflictResolution.ASK)  # type: int  # line 640
    m = Metadata(os.getcwd())  # type: Metadata  # TODO same is called inside stop on changes - could return both current and designated branch instead  # line 641
    m.loadBranches()  # line 642
    changes = None  # type: ChangeSet  # line 642
    currentBranch = m.branch  # type: _coconut.typing.Optional[int]  # line 643
    m, branch, revision, changes, strict, force, trackingPatterns = exitOnChanges(argument, options, check=False, onlys=onlys, excps=excps)  # don't check for current changes, only parse arguments  # line 644
    debug("Integrating changes from '%s/r%02d' into file tree..." % ((lambda _coconut_none_coalesce_item: "b%02d" % branch if _coconut_none_coalesce_item is None else _coconut_none_coalesce_item)(m.branches[branch].name), revision))  # line 645

# Determine file changes from other branch over current file tree
    m.computeSequentialPathSet(branch, revision)  # load all commits up to specified revision for branch to integrate  # line 648
    trackingUnion = trackingPatterns | m.getTrackingPatterns(branch)  # type: FrozenSet[str]  # line 649
    changes = m.findChanges(checkContent=strict, inverse=True, considerOnly=onlys if not m.track and not m.picky else conditionalIntersection(onlys, trackingUnion), dontConsider=excps)  # determine difference of other branch vs. file tree. "addition" means exists now but not in other, and should be removed unless in tracking mode  # line 650
    if not (mrg & MergeOperation.INSERT and changes.additions or (mrg & MergeOperation.REMOVE and changes.deletions) or changes.modifications):  # no file ops  # line 651
        if trackingUnion != trackingPatterns:  # nothing added  # line 652
            info("No file changes detected, but tracking patterns were merged (run 'sos switch /-1 --meta' to undo)")  # TODO write test to see if this works  # line 653
        else:  # line 654
            info("Nothing to update")  # but write back updated branch info below  # line 655
    else:  # integration required  # line 656
        for path, pinfo in changes.deletions.items():  # deletions mark files not present in current file tree -> needs additon  # line 657
            if mrg & MergeOperation.INSERT:  # deleted in current file tree: restore from branch to reach target  # line 658
                m.restoreFile(path, branch, revision, pinfo, ensurePath=True)  # deleted in current file tree: restore from branch to reach target  # line 658
            print("ADD " + path if mrg & MergeOperation.INSERT else "(A) " + path)  # line 659
        for path, pinfo in changes.additions.items():  # line 660
            if m.track or m.picky:  # because untracked files of other branch cannot be detected (which is good)  # line 661
                Exit("This should never happen")  # because untracked files of other branch cannot be detected (which is good)  # line 661
            if mrg & MergeOperation.REMOVE:  # line 662
                os.unlink(m.root + os.sep + path.replace(SLASH, os.sep))  # line 662
            print("DEL " + path if mrg & MergeOperation.REMOVE else "(D) " + path)  # not contained in other branch, but maybe kept  # line 663
        for path, pinfo in changes.modifications.items():  # line 664
            into = os.path.join(m.root, path.replace(SLASH, os.sep))  # type: str  # line 665
            binary = not m.isTextType(path)  # line 666
            if res & ConflictResolution.ASK or (binary and res == ConflictResolution.NEXT):  # TODO this may ask user even if no interaction was asked for (check line level for interactivity fist)  # line 667
                print(("MOD " + path if not binary else "BIN ") + path)  # line 668
                reso = {"i": ConflictResolution.MINE, "t": ConflictResolution.THEIRS, "m": ConflictResolution.NEXT}.get(user_input(" Resolve: *M[I]ne, [T]heirs, [M]erge: (I)").strip().lower(), ConflictResolution.MINE)  # line 669
                debug("User selected %d" % reso)  # line 670
            else:  # line 671
                reso = res  # line 671
            if reso & ConflictResolution.THEIRS:  # line 672
                m.readOrCopyVersionedFile(branch, revision, pinfo.nameHash, toFile=into)  # blockwise copy of contents  # line 673
                print("THR " + path)  # line 674
            elif reso & ConflictResolution.MINE:  # line 675
                print("MNE " + path)  # nothing to do! same as skip  # line 676
            else:  # NEXT: line-based merge  # line 677
                file = m.readOrCopyVersionedFile(branch, revision, pinfo.nameHash) if pinfo.size > 0 else b''  # type: _coconut.typing.Optional[bytes]  # parse lines  # line 678
                if file is not None:  # if None, error message was already logged  # line 679
                    contents = merge(file=file, intoname=into, mergeOperation=mrgline, conflictResolution=resline)  # type: bytes  # line 680
                    with open(path, "wb") as fd:  # TODO write to temp file first, in case writing fails  # line 681
                        fd.write(contents)  # TODO write to temp file first, in case writing fails  # line 681
    info("Integrated changes from '%s/r%02d' into file tree" % ((lambda _coconut_none_coalesce_item: "b%02d" % branch if _coconut_none_coalesce_item is None else _coconut_none_coalesce_item)(m.branches[branch].name), revision))  # line 682
    m.branches[currentBranch] = dataCopy(BranchInfo, m.branches[currentBranch], inSync=False, tracked=list(trackingUnion))  # line 683
    m.branch = currentBranch  # need to restore setting before saving TODO operate on different objects instead  # line 684
    m.saveBranches()  # line 685

def delete(argument: 'str', options: '_coconut.typing.Sequence[str]'=[]) -> 'None':  # line 687
    ''' Remove a branch entirely. '''  # line 688
    m, branch, revision, changes, strict, force, trackingPatterns = exitOnChanges(None, options)  # line 689
    if len(m.branches) == 1:  # line 690
        Exit("Cannot remove the only remaining branch. Use 'sos online' to leave offline mode")  # line 690
    branch, revision = m.parseRevisionString(argument)  # not from exitOnChanges, because we have to set argument to None there  # line 691
    if branch is None or branch not in m.branches:  # line 692
        Exit("Unknown branch")  # line 692
    debug("Removing branch %d%s..." % (branch, " '%s'" % m.branches[branch].name if m.branches[branch].name else ""))  # line 693
    binfo = m.removeBranch(branch)  # need to keep a reference to removed entry for output below  # line 694
    info("Branch b%02d%s removed" % (branch, " '%s'" % binfo.name if binfo.name else ""))  # line 695

def add(relPath: 'str', pattern: 'str', options: '_coconut.typing.Sequence[str]'=[]) -> 'None':  # line 697
    ''' Add a tracked files pattern to current branch's tracked files. '''  # line 698
    force = '--force' in options  # type: bool  # line 699
    m = Metadata(os.getcwd())  # type: Metadata  # line 700
    m.loadBranches()  # line 701
    if not m.track and not m.picky:  # line 702
        Exit("Repository is in simple mode. Use 'offline --track' or 'offline --picky' instead")  # line 702
    if pattern in m.branches[m.branch].tracked:  # line 703
        Exit("Pattern '%s' already tracked" % pattern)  # line 703
    if not force and not os.path.exists(relPath.replace(SLASH, os.sep)):  # line 704
        Exit("The pattern folder doesn't exist. Use --force to add it anyway")  # line 704
    if not force and len(fnmatch.filter(os.listdir(os.path.abspath(relPath.replace(SLASH, os.sep))), os.path.basename(pattern.replace(SLASH, os.sep)))) == 0:  # doesn't match any current file  # line 705
        Exit("Pattern doesn't match any file in specified folder. Use --force to add it anyway")  # line 706
    m.branches[m.branch].tracked.append(pattern)  # line 707
    m.saveBranches()  # line 708
    info("Added tracking pattern '%s' for folder '%s'" % (os.path.basename(pattern.replace(SLASH, os.sep)), os.path.abspath(relPath)))  # line 709

def remove(relPath: 'str', pattern: 'str') -> 'None':  # line 711
    ''' Remove a tracked files pattern from current branch's tracked files. '''  # line 712
    m = Metadata(os.getcwd())  # type: Metadata  # line 713
    m.loadBranches()  # line 714
    if not m.track and not m.picky:  # line 715
        Exit("Repository is in simple mode. Needs 'offline --track' or 'offline --picky' instead")  # line 715
    if pattern not in m.branches[m.branch].tracked:  # line 716
        suggestion = _coconut.set()  # type: Set[str]  # line 717
        for pat in m.branches[m.branch].tracked:  # line 718
            if fnmatch.fnmatch(pattern, pat):  # line 719
                suggestion.add(pat)  # line 719
        if suggestion:  # TODO use same wording as in move  # line 720
            print("Do you mean any of the following tracked file patterns? '%s'" % (", ".join(sorted(suggestion))))  # TODO use same wording as in move  # line 720
        Exit("Tracked pattern '%s' not found" % pattern)  # line 721
    m.branches[m.branch].tracked.remove(pattern)  # line 722
    m.saveBranches()  # line 723
    info("Removed tracking pattern '%s' for folder '%s'" % (os.path.basename(pattern), os.path.abspath(relPath.replace(SLASH, os.sep))))  # line 724

def ls(argument: '_coconut.typing.Optional[str]'=None, options: '_coconut.typing.Sequence[str]'=[]) -> 'None':  # line 726
    ''' List specified directory, augmenting with repository metadata. '''  # line 727
    folder = "." if argument is None else argument  # type: str  # line 728
    m = Metadata(os.getcwd())  # type: Metadata  # line 729
    m.loadBranches()  # line 730
    info("Repository is in %s mode" % ("tracking" if m.track else ("picky" if m.picky else "simple")))  # line 731
    relPath = os.path.relpath(folder, m.root).replace(os.sep, SLASH)  # type: str  # line 732
    trackingPatterns = m.getTrackingPatterns() if m.track or m.picky else _coconut.frozenset()  # type: _coconut.typing.Optional[FrozenSet[str]]  # for current branch  # line 733
    if '--patterns' in options:  # line 734
        out = ajoin("TRK ", [os.path.basename(p) for p in trackingPatterns if os.path.dirname(p).replace(os.sep, SLASH) == relPath], nl="\n")  # type: str  # line 735
        if out:  # line 736
            print(out)  # line 736
        return  # line 737
    files = list(sorted((entry for entry in os.listdir(folder) if os.path.isfile(os.path.join(folder, entry)))))  # type: List[str]  # line 738
    for file in files:  # for each file list all tracking patterns that match, or none (e.g. in picky mode after commit)  # line 739
        ignore = None  # type: _coconut.typing.Optional[str]  # line 740
        for ig in m.c.ignores:  # line 741
            if fnmatch.fnmatch(file, ig):  # remember first match  # line 742
                ignore = ig  # remember first match  # line 742
                break  # remember first match  # line 742
        if ig:  # line 743
            for wl in m.c.ignoresWhitelist:  # line 744
                if fnmatch.fnmatch(file, wl):  # found a white list entry for ignored file, undo ignoring it  # line 745
                    ignore = None  # found a white list entry for ignored file, undo ignoring it  # line 745
                    break  # found a white list entry for ignored file, undo ignoring it  # line 745
        if not ignore:  # line 746
            matches = []  # type: List[str]  # line 747
            for pattern in (p for p in trackingPatterns if os.path.dirname(p).replace(os.sep, SLASH) == relPath):  # only patterns matching current folder  # line 748
                if fnmatch.fnmatch(file, os.path.basename(pattern)):  # line 749
                    matches.append(os.path.basename(pattern))  # line 749
        matches.sort(key=lambda element: len(element))  # line 750
        print("%s %s%s" % ("IGN" if ignore is not None else ("TRK" if len(matches) > 0 else "..."), file, "  (%s)" % ignore if ignore is not None else ("  (%s)" % ("; ".join(matches)) if len(matches) > 0 else "")))  # line 751

def log(options: '_coconut.typing.Sequence[str]') -> 'None':  # line 753
    ''' List previous commits on current branch. '''  # line 754
    m = Metadata(os.getcwd())  # type: Metadata  # line 755
    m.loadBranches()  # knows current branch  # line 756
    m.loadBranch(m.branch)  # knows commit history  # line 757
    info((lambda _coconut_none_coalesce_item: "r%02d" % m.branch if _coconut_none_coalesce_item is None else _coconut_none_coalesce_item)("//|\\\\ Offline commit history of branch '%s'" % m.branches[m.branch].name))  # TODO also retain "from branch/revision" on branching?  # line 758
    nl = len("%d" % max(m.commits))  # determine space needed for revision  # line 759
    changeset = m.computeSequentialPathSetIterator(m.branch, max(m.commits))  # line 760
    maxWidth = max([wcswidth((lambda _coconut_none_coalesce_item: "" if _coconut_none_coalesce_item is None else _coconut_none_coalesce_item)(commit.message)) for commit in m.commits.values()])  # type: int  # line 761
    for no in range(max(m.commits) + 1):  # line 762
        commit = m.commits[no]  # type: CommitInfo  # line 763
        changes = next(changeset)  # type: ChangeSet  # side-effect: updates m.paths  # line 764
        newTextFiles = len([file for file in changes.additions.keys() if m.isTextType(file)])  # type: int  # line 765
        print("  %s r%s @%s (+%02d/-%02d/*%02d +%02dT/%05.1f%%) |%s|" % ("*" if commit.number == max(m.commits) else " ", ("%%%ds" % nl) % commit.number, strftime(commit.ctime), len(changes.additions), len(changes.deletions), len(changes.modifications), newTextFiles, 0. if len(changes.additions) == 0 else newTextFiles * 100. / len(changes.additions), ((lambda _coconut_none_coalesce_item: "" if _coconut_none_coalesce_item is None else _coconut_none_coalesce_item)(commit.message)).ljust(maxWidth)))  # line 766
        if '--changes' in options:  # line 767
            m.listChanges(changes)  # line 767

def config(argument: 'str', options: 'List[str]'=[]) -> 'None':  # line 769
    if argument not in ["set", "unset", "show", "list", "add", "rm"]:  # line 770
        Exit("Unknown config command")  # line 770
    if not configr:  # line 771
        Exit("Cannot execute config command. 'configr' module not installed")  # line 771
    c = loadConfig()  # type: Union[configr.Configr, Accessor]  # line 772
    if argument == "set":  # line 773
        if len(options) < 2:  # line 774
            Exit("No key nor value specified")  # line 774
        if options[0] not in (["defaultbranch"] + CONFIGURABLE_FLAGS + CONFIGURABLE_LISTS):  # line 775
            Exit("Unsupported key %r" % options[0])  # line 775
        if options[0] in CONFIGURABLE_FLAGS and options[1].lower() not in TRUTH_VALUES + FALSE_VALUES:  # line 776
            Exit("Cannot set flag to '%s'. Try on/off instead" % options[1].lower())  # line 776
        c[options[0]] = options[1].lower() in TRUTH_VALUES if options[0] in CONFIGURABLE_FLAGS else (options[1].strip() if options[0] not in CONFIGURABLE_LISTS else safeSplit(options[1], ";"))  # TODO sanitize texts?  # line 777
    elif argument == "unset":  # line 778
        if len(options) < 1:  # line 779
            Exit("No key specified")  # line 779
        if options[0] not in c.keys():  # line 780
            Exit("Unknown key")  # line 780
        del c[options[0]]  # line 781
    elif argument == "add":  # line 782
        if len(options) < 2:  # line 783
            Exit("No key nor value specified")  # line 783
        if options[0] not in CONFIGURABLE_LISTS:  # line 784
            Exit("Unsupported key for add %r" % options[0])  # line 784
        if options[0] not in c.keys():  # add list  # line 785
            c[options[0]] = [options[1]]  # add list  # line 785
        elif options[1] in c[options[0]]:  # line 786
            Exit("Value already contained")  # line 786
        c[options[0]].append(options[1])  # line 787
    elif argument == "rm":  # line 788
        if len(options) < 2:  # line 789
            Exit("No key nor value specified")  # line 789
        if options[0] not in c.keys():  # line 790
            Exit("Unknown key specified: %r" % options[0])  # line 790
        if options[1] not in c[options[0]]:  # line 791
            Exit("Unknown value: %r" % options[1])  # line 791
        c[options[0]].remove(options[1])  # line 792
    else:  # Show  # line 793
        for k, v in sorted(c.items()):  # line 794
            print("%s => %r" % (k, v))  # line 794
        return  # line 795
    f, g = saveConfig(c)  # line 796
    if f is None:  # line 797
        error("Error saving user configuration: %r" % g)  # line 797

def move(relPath: 'str', pattern: 'str', newRelPath: 'str', newPattern: 'str', options: 'List[str]'=[]) -> 'None':  # line 799
    ''' Path differs: Move files, create folder if not existing. Pattern differs: Attempt to rename file, unless exists in target or not unique. '''  # line 800
    force = '--force' in options  # type: bool  # line 801
    soft = '--soft' in options  # type: bool  # line 802
    if not os.path.exists(relPath.replace(SLASH, os.sep)) and not force:  # line 803
        Exit("Source folder doesn't exist. Use --force to proceed anyway")  # line 803
    m = Metadata(os.getcwd())  # type: Metadata  # line 804
    matching = fnmatch.filter(os.listdir(relPath.replace(SLASH, os.sep)) if os.path.exists(relPath.replace(SLASH, os.sep)) else [], os.path.basename(pattern))  # type: List[str]  # find matching files in source  # line 805
    matching[:] = [f for f in matching if len([n for n in m.c.ignores if fnmatch.fnmatch(f, n)]) == 0 or len([p for p in m.c.ignoresWhitelist if fnmatch.fnmatch(f, p)]) > 0]  # line 806
    if not matching and not force:  # line 807
        Exit("No files match the specified file pattern. Use --force to proceed anyway")  # line 807
    m.loadBranches()  # knows current branch  # line 808
    if not m.track and not m.picky:  # line 809
        Exit("Repository is in simple mode. Simply use basic file operations to modify files, then execute 'sos commit' to version the changes")  # line 809
    if pattern not in m.branches[m.branch].tracked:  # line 810
        for tracked in (t for t in m.branches[m.branch].tracked if os.path.dirname(t) == relPath):  # for all patterns of the same source folder  # line 811
            alternative = fnmatch.filter(matching, os.path.basename(tracked))  # type: _coconut.typing.Sequence[str]  # find if it matches any of the files in the source folder, too  # line 812
            if alternative:  # line 813
                info("  '%s' matches %d files" % (tracked, len(alternative)))  # line 813
        if not (force or soft):  # line 814
            Exit("File pattern '%s' is not tracked on current branch. 'sos move' only works on tracked patterns" % pattern)  # line 814
    basePattern = os.path.basename(pattern)  # type: str  # pure glob without folder  # line 815
    newBasePattern = os.path.basename(newPattern)  # type: str  # line 816
    if basePattern.count("*") < newBasePattern.count("*") or (basePattern.count("?") - basePattern.count("[?]")) < (newBasePattern.count("?") - newBasePattern.count("[?]")) or (basePattern.count("[") - basePattern.count("\\[")) < (newBasePattern.count("[") - newBasePattern.count("\\[")) or (basePattern.count("]") - basePattern.count("\\]")) < (newBasePattern.count("]") - newBasePattern.count("\\]")):  # line 817
        Exit("Glob markers from '%s' to '%s' don't match, cannot move/rename tracked matching files" % (basePattern, newBasePattern))  # line 821
    oldTokens = None  # type: _coconut.typing.Sequence[GlobBlock]  # line 822
    newToken = None  # type: _coconut.typing.Sequence[GlobBlock]  # line 822
    oldTokens, newTokens = tokenizeGlobPatterns(os.path.basename(pattern), os.path.basename(newPattern))  # line 823
    matches = convertGlobFiles(matching, oldTokens, newTokens)  # type: _coconut.typing.Sequence[Tuple[str, str]]  # computes list of source - target filename pairs  # line 824
    if len({st[1] for st in matches}) != len(matches):  # line 825
        Exit("Some target filenames are not unique and different move/rename actions would point to the same target file")  # line 825
    matches = reorderRenameActions(matches, exitOnConflict=not soft)  # attempts to find conflict-free renaming order, or exits  # line 826
    if os.path.exists(newRelPath):  # line 827
        exists = [filename[1] for filename in matches if os.path.exists(os.path.join(newRelPath, filename[1]).replace(SLASH, os.sep))]  # type: _coconut.typing.Sequence[str]  # line 828
        if exists and not (force or soft):  # line 829
            Exit("%s files would write over existing files in %s cases. Use --force to execute it anyway" % ("Moving" if relPath != newRelPath else "Renaming", "all" if len(exists) == len(matches) else "some"))  # line 829
    else:  # line 830
        os.makedirs(os.path.abspath(newRelPath.replace(SLASH, os.sep)))  # line 830
    if not soft:  # perform actual renaming  # line 831
        for (source, target) in matches:  # line 832
            try:  # line 833
                shutil.move(os.path.abspath(os.path.join(relPath, source).replace(SLASH, os.sep)), os.path.abspath(os.path.join(newRelPath, target).replace(SLASH, os.sep)))  # line 833
            except Exception as E:  # one error can lead to another in case of delicate renaming order  # line 834
                error("Cannot move/rename file '%s' to '%s'" % (source, os.path.join(newRelPath, target)))  # one error can lead to another in case of delicate renaming order  # line 834
    m.branches[m.branch].tracked[m.branches[m.branch].tracked.index(pattern)] = newPattern  # line 835
    m.saveBranches()  # line 836

def parse(root: 'str', cwd: 'str'):  # line 838
    ''' Main operation. Main has already chdir into VCS root folder, cwd is original working directory for add, rm. '''  # line 839
    debug("Parsing command-line arguments...")  # line 840
    try:  # line 841
        command = sys.argv[1].strip() if len(sys.argv) > 1 else ""  # line 842
        argument = sys.argv[2].strip() if len(sys.argv) > 2 and not sys.argv[2].startswith("--") else None  # line 843
        options = sys.argv[3:] if command == "config" else [c for c in sys.argv[2:] if c.startswith("--")]  # consider second parameter for no-arg command, otherwise from third on  # line 844
        onlys, excps = parseOnlyOptions(cwd, options)  # extracts folder-relative information for changes, commit, diff, switch, update  # line 845
        debug("Processing command %r with argument '%s' and options %r." % ("" if command is None else command, "" if argument is None else argument, options))  # line 846
        if command[:1] in "amr":  # line 847
            relPath, pattern = relativize(root, os.path.join(cwd, "." if argument is None else argument))  # line 847
        if command[:1] == "m":  # line 848
            if not options:  # line 849
                Exit("Need a second file pattern argument as target for move/rename command")  # line 849
            newRelPath, newPattern = relativize(root, os.path.join(cwd, options[0]))  # line 850
        if command[:1] == "a":  # line 851
            add(relPath, pattern, options)  # line 851
        elif command[:1] == "b":  # line 852
            branch(argument, options)  # line 852
        elif command[:2] == "ch":  # line 853
            changes(argument, options, onlys, excps)  # line 853
        elif command[:3] == "com":  # line 854
            commit(argument, options, onlys, excps)  # line 854
        elif command[:2] == "ci":  # line 855
            commit(argument, options, onlys, excps)  # line 855
        elif command[:3] == 'con':  # line 856
            config(argument, options)  # line 856
        elif command[:2] == "de":  # line 857
            delete(argument, options)  # line 857
        elif command[:2] == "di":  # line 858
            diff(argument, options, onlys, excps)  # line 858
        elif command[:1] == "h":  # line 859
            usage()  # line 859
        elif command[:2] == "lo":  # line 860
            log(options)  # line 860
        elif command[:2] == "li":  # TODO handle absolute paths as well, also for Windows  # line 861
            ls(relativize(root, cwd if argument is None else os.path.join(cwd, argument))[1], options)  # TODO handle absolute paths as well, also for Windows  # line 861
        elif command[:2] == "ls":  # TODO avoid root super paths (..)  # line 862
            ls(relativize(root, cwd if argument is None else os.path.join(cwd, argument))[1], options)  # TODO avoid root super paths (..)  # line 862
        elif command[:1] == "m":  # line 863
            move(relPath, pattern, newRelPath, newPattern, options[1:])  # line 863
        elif command[:2] == "of":  # line 864
            offline(argument, options)  # line 864
        elif command[:2] == "on":  # line 865
            online(options)  # line 865
        elif command[:1] == "r":  # line 866
            remove(relPath, pattern)  # line 866
        elif command[:2] == "st":  # line 867
            status()  # line 867
        elif command[:2] == "sw":  # line 868
            switch(argument, options, onlys, excps)  # line 868
        elif command[:1] == "u":  # line 869
            update(argument, options, onlys, excps)  # line 869
        elif command[:1] == "v":  # line 870
            usage(short=True)  # line 870
        else:  # line 871
            Exit("Unknown command '%s'" % command)  # line 871
    except (Exception, RuntimeError) as E:  # line 872
        print(str(E))  # line 873
        import traceback  # line 874
        traceback.print_exc()  # line 875
        traceback.print_stack()  # line 876
        try:  # line 877
            traceback.print_last()  # line 877
        except:  # line 878
            pass  # line 878
        print("An internal error occurred in SOS. Please report above message to the project maintainer at  https://github.com/ArneBachmann/sos/issues  via 'New Issue'.\nPlease state your installed version via 'sos version', and what you were doing.")  # line 879
    sys.exit(0)  # line 880

def main() -> 'None':  # line 882
    global debug, info, warn, error  # line 883
    logging.basicConfig(level=level, stream=sys.stderr, format=("%(asctime)-23s %(levelname)-8s %(name)s:%(lineno)d | %(message)s" if '--log' in sys.argv else "%(message)s"))  # line 884
    _log = Logger(logging.getLogger(__name__))  # line 885
    debug, info, warn, error = _log.debug, _log.info, _log.warn, _log.error  # line 885
    for option in (o for o in ['--log', '--verbose', '-v', '--sos'] if o in sys.argv):  # clean up program arguments  # line 886
        sys.argv.remove(option)  # clean up program arguments  # line 886
    if '--help' in sys.argv or len(sys.argv) < 2:  # line 887
        usage()  # line 887
        Exit()  # line 887
    command = sys.argv[1] if len(sys.argv) > 1 else None  # type: _coconut.typing.Optional[str]  # line 888
    root, vcs, cmd = findSosVcsBase()  # root is None if no .sos folder exists up the folder tree (still working online); vcs is checkout/repo root folder; cmd is the VCS base command  # line 889
    debug("Found root folders for SOS|VCS: %s|%s" % ("" if root is None else root, "" if vcs is None else vcs))  # line 890
    defaults["defaultbranch"] = vcsBranches.get(cmd, "trunk")  # sets dynamic default with SVN fallback  # line 891
    if force_sos or root is not None or ("" if command is None else command)[:2] == "of" or ("" if command is None else command)[:1] in ["h", "v"]:  # in offline mode or just going offline TODO what about git config?  # line 892
        cwd = os.getcwd()  # line 893
        os.chdir(cwd if command[:2] == "of" else cwd if root is None else root)  # line 894
        parse(root, cwd)  # line 895
    elif force_vcs or cmd is not None:  # online mode - delegate to VCS  # line 896
        info("SOS: Running '%s %s'" % (cmd, " ".join(sys.argv[1:])))  # line 897
        import subprocess  # only required in this section  # line 898
        process = subprocess.Popen([cmd] + sys.argv[1:], shell=False, stdin=subprocess.PIPE, stdout=sys.stdout, stderr=sys.stderr)  # line 899
        inp = ""  # type: str  # line 900
        while True:  # line 901
            so, se = process.communicate(input=inp)  # line 902
            if process.returncode is not None:  # line 903
                break  # line 903
            inp = sys.stdin.read()  # line 904
        if sys.argv[1][:2] == "co" and process.returncode == 0:  # successful commit - assume now in sync again (but leave meta data folder with potential other feature branches behind until "online")  # line 905
            if root is None:  # line 906
                Exit("Cannot determine VCS root folder: Unable to mark repository as synchronized and will show a warning when leaving offline mode")  # line 906
            m = Metadata(root)  # line 907
            m.loadBranches()  # read repo  # line 908
            m.branches[m.branch] = dataCopy(BranchInfo, m.branches[m.branch], inSync=True)  # mark as committed  # line 909
            m.saveBranches()  # line 910
    else:  # line 911
        Exit("No offline repository present, and unable to detect VCS file tree")  # line 911


# Main part
level = logging.DEBUG if os.environ.get("DEBUG", "False").lower() == "true" or '--verbose' in sys.argv or '-v' in sys.argv else logging.INFO  # line 915
force_sos = '--sos' in sys.argv  # type: bool  # line 916
force_vcs = '--vcs' in sys.argv  # type: bool  # line 917
_log = Logger(logging.getLogger(__name__))  # type: logging.Logger  # line 918
debug, info, warn, error = _log.debug, _log.info, _log.warn, _log.error  # line 918
if __name__ == '__main__':  # line 919
    main()  # line 919
