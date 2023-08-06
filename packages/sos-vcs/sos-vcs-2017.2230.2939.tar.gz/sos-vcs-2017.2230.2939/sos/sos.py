#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# __coconut_hash__ = 0x6078ee96

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

def usage() -> 'None':  # line 42
    print("""//|\\\\ {appname} //|\\\\

Usage: {cmd} <command> [<argument>] [<option1>, ...]        When operating in offline mode, or command is "sos offline"
       {cmd} --sos <underlying vcs command and arguments>   When operating in offline mode, forced passthrough to traditional VCS
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
    --verbose                    Enable verbose output""".format(appname=APPNAME, cmd="sos", CMD="SOS"))  # line 100

# Main data class
#@runtime_validation
class Metadata:  # line 104
    ''' This class doesn't represent the entire repository state in memory,
      but serves as a container for different repo operations,
      using only parts of its attributes at any point in time. Use with care.
  '''  # line 108

    def __init__(_, path: 'str') -> 'None':  # line 110
        ''' Create empty container object for various repository operations. '''  # line 111
        _.c = loadConfig()  # line 112
        _.root = path  # type: str  # line 113
        _.branches = {}  # type: Dict[int, BranchInfo]  # branch number zero represents the initial state at branching  # line 114
        _.commits = {}  # type: Dict[int, CommitInfo]  # consecutive numbers per branch, starting at 0  # line 115
        _.paths = {}  # type: Dict[str, PathInfo]  # utf-8 encoded relative, normalized file system paths  # line 116
        _.tags = []  # type: List[str]  # line 117
        _.branch = None  # type: _coconut.typing.Optional[int]  # current branch number  # line 118
        _.commit = None  # type: _coconut.typing.Optional[int]  # current revision number  # line 119
        _.track = _.c.track  # type: bool  # track file name patterns in the repository (per branch)  # line 120
        _.picky = _.c.picky  # type: bool  # pick files to commit per operation  # line 121
        _.strict = _.c.strict  # type: bool  # be always strict (regarding file contents comparsion)  # line 122
        _.compress = _.c.compress  # type: bool  # these flags are stored in the repository  # line 123

    def isTextType(_, filename: 'str') -> 'bool':  # line 125
        return (((lambda _coconut_none_coalesce_item: "" if _coconut_none_coalesce_item is None else _coconut_none_coalesce_item)(mimetypes.guess_type(filename)[0])).startswith("text/") or any([fnmatch.fnmatch(filename, pattern) for pattern in _.c.texttype])) and not any([fnmatch.fnmatch(filename, pattern) for pattern in _.c.bintype])  # line 125

    def listChanges(_, changes: 'ChangeSet') -> 'None':  # line 127
        if len(changes.additions) > 0:  # line 128
            print(ajoin("ADD ", sorted(changes.additions.keys()), "\n"))  # line 128
        if len(changes.deletions) > 0:  # line 129
            print(ajoin("DEL ", sorted(changes.deletions.keys()), "\n"))  # line 129
        if len(changes.modifications) > 0:  # line 130
            print(ajoin("MOD ", sorted(changes.modifications.keys()), "\n"))  # line 130

    def loadBranches(_) -> 'None':  # line 132
        ''' Load list of branches and current branch info from metadata file. '''  # line 133
        try:  # fails if not yet created (on initial branch/commit)  # line 134
            branches = None  # type: List[Tuple]  # line 135
            with codecs.open(os.path.join(_.root, metaFolder, metaFile), "r", encoding=UTF8) as fd:  # line 136
                flags, branches = json.load(fd)  # line 137
            _.tags = flags["tags"]  # list of commit messages to treat as globally unique tags  # line 138
            _.branch = flags["branch"]  # current branch integer  # line 139
            _.track = flags["track"]  # line 140
            _.picky = flags["picky"]  # line 141
            _.strict = flags["strict"]  # line 142
            _.compress = flags["compress"]  # line 143
            _.branches = {i.number: i for i in (BranchInfo(*item) for item in branches)}  # re-create type info  # line 144
        except Exception as E:  # if not found, create metadata folder  # line 145
            _.branches = {}  # line 146
            warn("Couldn't read branches metadata: %r" % E)  # line 147

    def saveBranches(_) -> 'None':  # line 149
        ''' Save list of branches and current branch info to metadata file. '''  # line 150
        with codecs.open(os.path.join(_.root, metaFolder, metaFile), "w", encoding=UTF8) as fd:  # line 151
            json.dump(({"tags": _.tags, "branch": _.branch, "track": _.track, "picky": _.picky, "strict": _.strict, "compress": _.compress}, list(_.branches.values())), fd, ensure_ascii=False)  # line 152

    def getRevisionByName(_, name: 'str') -> '_coconut.typing.Optional[int]':  # line 154
        ''' Convenience accessor for named revisions (using commit message as name). '''  # line 155
        if name == "":  # line 156
            return -1  # line 156
        try:  # attempt to parse integer string  # line 157
            return longint(name)  # attempt to parse integer string  # line 157
        except ValueError:  # line 158
            pass  # line 158
        found = [number for number, commit in _.commits.items() if name == commit.message]  # line 159
        return found[0] if found else None  # line 160

    def getBranchByName(_, name: 'str') -> '_coconut.typing.Optional[int]':  # line 162
        ''' Convenience accessor for named branches. '''  # line 163
        if name == "":  # line 164
            return _.branch  # line 164
        try:  # attempt to parse integer string  # line 165
            return longint(name)  # attempt to parse integer string  # line 165
        except ValueError:  # line 166
            pass  # line 166
        found = [number for number, branch in _.branches.items() if name == branch.name]  # line 167
        return found[0] if found else None  # line 168

    def loadBranch(_, branch: 'int') -> 'None':  # line 170
        ''' Load all commit information from a branch meta data file. '''  # line 171
        with codecs.open(os.path.join(_.root, metaFolder, "b%d" % branch, metaFile), "r", encoding=UTF8) as fd:  # line 172
            commits = json.load(fd)  # type: List[List[Any]]  # list of CommitInfo that needs to be unmarshalled into value types  # line 173
        _.commits = {i.number: i for i in (CommitInfo(*item) for item in commits)}  # re-create type info  # line 174
        _.branch = branch  # line 175

    def saveBranch(_, branch: 'int') -> 'None':  # line 177
        ''' Save all commit information to a branch meta data file. '''  # line 178
        with codecs.open(os.path.join(_.root, metaFolder, "b%d" % branch, metaFile), "w", encoding=UTF8) as fd:  # line 179
            json.dump(list(_.commits.values()), fd, ensure_ascii=False)  # line 180

    def duplicateBranch(_, branch: 'int', name: '_coconut.typing.Optional[str]') -> 'None':  # line 182
        ''' Create branch from an existing branch/revision. WARN: Caller must have loaded branches information.
        branch: target branch (should not exist yet)
        name: optional name of new branch
        _.branch: current branch
    '''  # line 187
        debug("Duplicating branch '%s' to '%s'..." % ((lambda _coconut_none_coalesce_item: ("b%d" % _.branch) if _coconut_none_coalesce_item is None else _coconut_none_coalesce_item)(_.branches[_.branch].name), ("b%d" % branch if name is None else name)))  # line 188
        tracked = [t for t in _.branches[_.branch].tracked]  # copy  # line 189
        os.makedirs(os.path.join(_.root, metaFolder, "b%d" % branch, "r0"))  # line 190
        _.loadBranch(_.branch)  # line 191
        revision = max(_.commits)  # type: int  # line 192
        _.computeSequentialPathSet(_.branch, revision)  # full set of files in revision to _.paths  # line 193
        for path, pinfo in _.paths.items():  # line 194
            _.copyVersionedFile(_.branch, revision, branch, 0, pinfo)  # line 195
        _.commits = {0: CommitInfo(0, longint(time.time() * 1000), "Branched from '%s'" % ((lambda _coconut_none_coalesce_item: "b%d" % _.branch if _coconut_none_coalesce_item is None else _coconut_none_coalesce_item)(_.branches[_.branch].name)))}  # store initial commit  # line 196
        _.saveBranch(branch)  # save branch meta data to branch folder  # line 197
        _.saveCommit(branch, 0)  # save commit meta data to revision folder  # line 198
        _.branches[branch] = BranchInfo(branch, _.commits[0].ctime, name, _.branches[_.branch].inSync, tracked)  # save branch info, before storing repo state at caller  # line 199

    def createBranch(_, branch: 'int', name: '_coconut.typing.Optional[str]'=None, initialMessage: '_coconut.typing.Optional[str]'=None):  # line 201
        ''' Create a new branch from current file tree. This clears all known commits and modifies the file system.
        branch: target branch (should not exist yet)
        name: optional name of new branch
        _.branch: current branch, must exist already
    '''  # line 206
        simpleMode = not (_.track or _.picky)  # line 207
        tracked = [t for t in _.branches[_.branch].tracked] if _.track and len(_.branches) > 0 else []  # in case of initial branch creation  # line 208
        debug((lambda _coconut_none_coalesce_item: "b%d" % branch if _coconut_none_coalesce_item is None else _coconut_none_coalesce_item)("Creating branch '%s'..." % name))  # line 209
        _.paths = {}  # type: Dict[str, PathInfo]  # line 210
        if simpleMode:  # branches from file system state  # line 211
            changes = _.findChanges(branch, 0, progress=simpleMode)  # type: ChangeSet  # creates revision folder and versioned files  # line 212
            _.listChanges(changes)  # line 213
            _.paths.update(changes.additions.items())  # line 214
        else:  # tracking or picky mode: branch from lastest revision  # line 215
            os.makedirs(os.path.join(_.root, metaFolder, "b%d" % branch, "r0"))  # line 216
            if _.branch is not None:  # not immediately after "offline" - copy files from current branch  # line 217
                _.loadBranch(_.branch)  # line 218
                revision = max(_.commits)  # type: int  # TODO what if last switch was to an earlier revision? no persisting of last checkout  # line 219
                _.computeSequentialPathSet(_.branch, revision)  # full set of files in revision to _.paths  # line 220
                for path, pinfo in _.paths.items():  # line 221
                    _.copyVersionedFile(_.branch, revision, branch, 0, pinfo)  # line 222
        ts = longint(time.time() * 1000)  # line 223
        _.commits = {0: CommitInfo(0, ts, "Branched on %s" % strftime(ts) if initialMessage is None else initialMessage)}  # store initial commit for new branch  # line 224
        _.saveBranch(branch)  # save branch meta data (revisions) to branch folder  # line 225
        _.saveCommit(branch, 0)  # save commit meta data to revision folder  # line 226
        _.branches[branch] = BranchInfo(branch, _.commits[0].ctime, name, True if len(_.branches) == 0 else _.branches[_.branch].inSync, tracked)  # save branch info, in case it is needed  # line 227

    def removeBranch(_, branch: 'int') -> 'BranchInfo':  # line 229
        ''' Entirely remove a branch and all its revisions from the file system. '''  # line 230
        shutil.rmtree(os.path.join(_.root, metaFolder, "b%d" % branch))  # line 231
        binfo = _.branches[branch]  # line 232
        del _.branches[branch]  # line 233
        _.branch = max(_.branches)  # line 234
        _.saveBranches()  # line 235
        _.commits.clear()  # line 236
        return binfo  # line 237

    def loadCommit(_, branch: 'int', revision: 'int') -> 'None':  # line 239
        ''' Load all file information from a commit meta data. '''  # line 240
        with codecs.open(os.path.join(_.root, metaFolder, "b%d" % branch, "r%d" % revision, metaFile), "r", encoding=UTF8) as fd:  # line 241
            _.paths = json.load(fd)  # line 242
        _.paths = {path: PathInfo(*item) for path, item in _.paths.items()}  # re-create type info  # line 243
        _.branch = branch  # line 244

    def saveCommit(_, branch: 'int', revision: 'int'):  # line 246
        ''' Save all file information to a commit meta data file. '''  # line 247
        target = os.path.join(_.root, metaFolder, "b%d" % branch, "r%d" % revision)  # line 248
        try:  # line 249
            os.makedirs(target)  # line 249
        except:  # line 250
            pass  # line 250
        with codecs.open(os.path.join(target, metaFile), "w", encoding=UTF8) as fd:  # line 251
            json.dump(_.paths, fd, ensure_ascii=False)  # line 252

    def findChanges(_, branch: '_coconut.typing.Optional[int]'=None, revision: '_coconut.typing.Optional[int]'=None, checkContent: 'bool'=False, inverse: 'bool'=False, considerOnly: '_coconut.typing.Optional[FrozenSet[str]]'=None, dontConsider: '_coconut.typing.Optional[FrozenSet[str]]'=None, progress: 'bool'=False) -> 'ChangeSet':  # line 254
        ''' Find changes on the file system vs. in-memory paths (which should reflect the latest commit state).
        Only if both branch and revision are *not* None, write modified/added files to the specified revision folder (thus creating a new revision)
        The function returns the state of file tree *differences*, unless "inverse" is True -> then return original data
        checkContent: also computes file content hashes
        inverse: retain original state (size, mtime, hash) instead of updated one
        considerOnly: set of tracking patterns. None for simple mode. For update operation, consider union of other and current branch
        dontConsider: set of tracking patterns to not consider in changes
        progress: Show file names during processing
    '''  # line 263
        write = branch is not None and revision is not None  # line 264
        if write:  # line 265
            os.makedirs(os.path.join(_.root, metaFolder, "b%d" % branch, "r%d" % revision))  # line 265
        changes = ChangeSet({}, {}, {})  # type: ChangeSet  # line 266
        counter = Counter(-1)  # type: Counter  # line 267
        timer = time.time()  # line 267
        hashed = None  # type: _coconut.typing.Optional[str]  # line 268
        written = None  # type: longint  # line 268
        compressed = 0  # type: longint  # line 268
        original = 0  # type: longint  # line 268
        knownPaths = collections.defaultdict(list)  # type: Dict[str, List[str]]  # line 269
        for path, pinfo in _.paths.items():  # line 270
            if pinfo.size is not None and (considerOnly is None or any((path[:path.rindex(SLASH)] == pattern[:pattern.rindex(SLASH)] and fnmatch.fnmatch(path[path.rindex(SLASH) + 1:], pattern[pattern.rindex(SLASH) + 1:]) for pattern in considerOnly))) and (dontConsider is None or not any((path[:path.rindex(SLASH)] == pattern[:pattern.rindex(SLASH)] and fnmatch.fnmatch(path[path.rindex(SLASH) + 1:], pattern[pattern.rindex(SLASH) + 1:]) for pattern in dontConsider))):  # line 271
                knownPaths[os.path.dirname(path)].append(os.path.basename(path))  # TODO reimplement using fnmatch.filter and set operations for all files per path for speed  # line 274
        for path, dirnames, filenames in os.walk(_.root):  # line 275
            dirnames[:] = [f for f in dirnames if len([n for n in _.c.ignoreDirs if fnmatch.fnmatch(f, n)]) == 0 or len([p for p in _.c.ignoreDirsWhitelist if fnmatch.fnmatch(f, p)]) > 0]  # line 276
            filenames[:] = [f for f in filenames if len([n for n in _.c.ignores if fnmatch.fnmatch(f, n)]) == 0 or len([p for p in _.c.ignoresWhitelist if fnmatch.fnmatch(f, p)]) > 0]  # line 277
            dirnames.sort()  # line 278
            filenames.sort()  # line 278
            relPath = os.path.relpath(path, _.root).replace(os.sep, SLASH)  # line 279
            walk = filenames if considerOnly is None else list(reduce(lambda last, pattern: last | set(fnmatch.filter(filenames, os.path.basename(pattern))), (p for p in considerOnly if os.path.dirname(p).replace(os.sep, SLASH) == relPath), _coconut.set()))  # line 280
            if dontConsider:  # line 281
                walk[:] = [fn for fn in walk if not any((fnmatch.fnmatch(fn, os.path.basename(p)) for p in dontConsider if os.path.dirname(p).replace(os.sep, SLASH) == relPath))]  # line 282
            for file in walk:  # if m.track or m.picky: only files that match any path-relevant tracking patterns  # line 283
                filename = relPath + SLASH + file  # line 284
                filepath = os.path.join(path, file)  # line 285
                stat = os.stat(filepath)  # line 286
                size, mtime, newtime = stat.st_size, longint(stat.st_mtime * 1000), time.time()  # line 287
                if progress and newtime - timer > .1:  # line 288
                    outstring = "\rPreparing %s  %s" % (PROGRESS_MARKER[counter.inc() % 4], filename)  # line 289
                    sys.stdout.write(outstring + " " * max(0, termWidth - len(outstring)))  # TODO could write to new line instead of carriage return (still true?)  # line 290
                    sys.stdout.flush()  # TODO could write to new line instead of carriage return (still true?)  # line 290
                    timer = newtime  # TODO could write to new line instead of carriage return (still true?)  # line 290
                if filename not in _.paths:  # detected file not present (or untracked) in (other) branch  # line 291
                    nameHash = hashStr(filename)  # line 292
                    hashed, written = hashFile(filepath, _.compress, saveTo=os.path.join(_.root, metaFolder, "b%d" % branch, "r%d" % revision, nameHash) if write else None) if size > 0 else (None, 0)  # line 293
                    changes.additions[filename] = PathInfo(nameHash, size, mtime, hashed)  # line 294
                    compressed += written  # line 295
                    original += size  # line 295
                    continue  # line 296
                last = _.paths[filename]  # filename is known - check for modifications  # line 297
                if last.size is None:  # was removed before but is now added back - does not apply for tracking mode (which never marks files for removal in the history)  # line 298
                    hashed, written = hashFile(filepath, _.compress, saveTo=os.path.join(_.root, metaFolder, "b%d" % branch, "r%d" % revision, last.nameHash) if write else None) if size > 0 else (None, 0)  # line 299
                    changes.additions[filename] = PathInfo(last.nameHash, size, mtime, hashed)  # line 300
                    continue  # line 300
                elif size != last.size or mtime != last.mtime or (checkContent and hashFile(filepath, _.compress)[0] != last.hash):  # detected a modification  # line 301
                    hashed, written = hashFile(filepath, _.compress, saveTo=os.path.join(_.root, metaFolder, "b%d" % branch, "r%d" % revision, last.nameHash) if write else None) if (last.size if inverse else size) > 0 else (last.hash if inverse else None, 0)  # line 302
                    changes.modifications[filename] = PathInfo(last.nameHash, last.size if inverse else size, last.mtime if inverse else mtime, hashed)  # line 303
                else:  # line 304
                    continue  # line 304
                compressed += written  # line 305
                original += last.size if inverse else size  # line 305
            if relPath in knownPaths:  # at least one file is tracked  # line 306
                knownPaths[relPath][:] = list(set(knownPaths[relPath]) - set(walk))  # at least one file is tracked  # line 306
        for path, names in knownPaths.items():  # all paths that weren't walked by  # line 307
            for file in names:  # line 308
                changes.deletions[path + SLASH + file] = _.paths[path + SLASH + file]  # line 308
        if progress:  # force new line  # line 309
            print("\rPreparation finished. Compression factor %s" % ("is %.1f" % (original * 100. / compressed) if compressed > 0 else "cannot be computed").ljust(termWidth), file=sys.stdout)  # force new line  # line 309
        else:  # line 310
            debug("Finished detecting changes. Compression factor %s" % ("is %.1f" % (original * 100. / compressed) if compressed > 0 else "cannot be computed"))  # line 310
        return changes  # line 311

    def integrateChangeset(_, changes: 'ChangeSet', clear=False) -> 'None':  # line 313
        ''' In-memory update from a changeset, marking deleted files with size=None. Use clear = True to start on an empty path set. '''  # line 314
        if clear:  # line 315
            _.paths.clear()  # line 315
        else:  # line 316
            rm = [p for p, info in _.paths.items() if info.size is None]  # remove files deleted in earlier change sets (revisions)  # line 317
            for old in rm:  # remove previously removed entries completely  # line 318
                del _.paths[old]  # remove previously removed entries completely  # line 318
        for d, info in changes.deletions.items():  # mark now removed entries as deleted  # line 319
            _.paths[d] = PathInfo(info.nameHash, None, info.mtime, None)  # mark now removed entries as deleted  # line 319
        _.paths.update(changes.additions)  # line 320
        _.paths.update(changes.modifications)  # line 321

    def computeSequentialPathSet(_, branch: 'int', revision: 'int') -> 'None':  # line 323
        next(_.computeSequentialPathSetIterator(branch, revision, incrementally=False))  # simply invoke the generator once  # line 324

    def computeSequentialPathSetIterator(_, branch: 'int', revision: 'int', incrementally: 'bool'=True) -> '_coconut.typing.Optional[Iterator[ChangeSet]]':  # line 326
        ''' In-memory computation of current list of valid PathInfo entries for specified branch and until specified revision (inclusively) by traversing revision on the file system. '''  # line 327
        _.loadCommit(branch, 0)  # load initial paths  # line 328
        if incrementally:  # line 329
            yield diffPathSets({}, _.paths)  # line 329
        n = Metadata(_.root)  # type: Metadata  # next changes  # line 330
        for revision in range(1, revision + 1):  # line 331
            n.loadCommit(branch, revision)  # line 332
            changes = diffPathSets(_.paths, n.paths)  # type: ChangeSet  # line 333
            _.integrateChangeset(changes)  # line 334
            if incrementally:  # line 335
                yield changes  # line 335
        yield None  # for the default case - not incrementally  # line 336

    def parseRevisionString(_, argument: 'str') -> 'Tuple[_coconut.typing.Optional[int], _coconut.typing.Optional[int]]':  # line 338
        ''' Commit identifiers can be str or int for branch, and int for revision.
        Revision identifiers can be negative, with -1 being last commit.
    '''  # line 341
        if argument is None or argument == SLASH:  # no branch/revision specified  # line 342
            return (_.branch, -1)  # no branch/revision specified  # line 342
        argument = argument.strip()  # line 343
        if argument.startswith(SLASH):  # current branch  # line 344
            return (_.branch, _.getRevisionByName(argument[1:]))  # current branch  # line 344
        if argument.endswith(SLASH):  # line 345
            try:  # line 346
                return (_.getBranchByName(argument[:-1]), -1)  # line 346
            except ValueError:  # line 347
                Exit("Unknown branch label '%s'" % argument)  # line 347
        if SLASH in argument:  # line 348
            b, r = argument.split(SLASH)[:2]  # line 349
            try:  # line 350
                return (_.getBranchByName(b), _.getRevisionByName(r))  # line 350
            except ValueError:  # line 351
                Exit("Unknown branch label or wrong number format '%s/%s'" % (b, r))  # line 351
        branch = _.getBranchByName(argument)  # type: int  # returns number if given (revision) integer  # line 352
        if branch not in _.branches:  # line 353
            branch = None  # line 353
        try:  # either branch name/number or reverse/absolute revision number  # line 354
            return (_.branch if branch is None else branch, longint(argument if argument else "-1") if branch is None else -1)  # either branch name/number or reverse/absolute revision number  # line 354
        except:  # line 355
            Exit("Unknown branch label or wrong number format")  # line 355
        Exit("This should never happen")  # line 356
        return (None, None)  # line 356

    def findRevision(_, branch: 'int', revision: 'int', nameHash: 'str') -> 'Tuple[int, str]':  # line 358
        while True:  # find latest revision that contained the file physically  # line 359
            source = os.path.join(_.root, metaFolder, "b%d" % branch, "r%d" % revision, nameHash)  # type: str  # line 360
            if os.path.exists(source) and os.path.isfile(source):  # line 361
                break  # line 361
            revision -= 1  # line 362
            if revision < 0:  # line 363
                Exit("Cannot determine versioned file '%s' from specified branch '%d'" % (nameHash, branch))  # line 363
        return revision, source  # line 364

    def copyVersionedFile(_, branch: 'int', revision: 'int', toBranch: 'int', toRevision: 'int', pinfo: 'PathInfo') -> 'None':  # line 366
        ''' Copy versioned file to other branch/revision. '''  # line 367
        target = os.path.join(_.root, metaFolder, "b%d" % toBranch, "r%d" % toRevision, pinfo.nameHash)  # type: str  # line 368
        revision, source = _.findRevision(branch, revision, pinfo.nameHash)  # line 369
        shutil.copy2(source, target)  # line 370

    def readOrCopyVersionedFile(_, branch: 'int', revision: 'int', nameHash: 'str', toFile: '_coconut.typing.Optional[str]'=None) -> '_coconut.typing.Optional[bytes]':  # line 372
        ''' Return file contents, or copy contents into file path provided. '''  # line 373
        source = os.path.join(_.root, metaFolder, "b%d" % branch, "r%d" % revision, nameHash)  # type: str  # line 374
        try:  # line 375
            with openIt(source, "r", _.compress) as fd:  # line 376
                if toFile is None:  # read bytes into memory and return  # line 377
                    return fd.read()  # read bytes into memory and return  # line 377
                with open(toFile, "wb") as to:  # line 378
                    while True:  # line 379
                        buffer = fd.read(bufSize)  # line 380
                        to.write(buffer)  # line 381
                        if len(buffer) < bufSize:  # line 382
                            break  # line 382
                    return None  # line 383
        except Exception as E:  # line 384
            warn("Cannot read versioned file: %r (%d/%d/%s)" % (E, branch, revision, nameHash))  # line 384
        return None  # line 385

    def restoreFile(_, relPath: '_coconut.typing.Optional[str]', branch: 'int', revision: 'int', pinfo: 'PathInfo', ensurePath: 'bool'=False) -> '_coconut.typing.Optional[bytes]':  # line 387
        ''' Recreate file for given revision, or return contents if path is None. '''  # line 388
        if relPath is None:  # just return contents  # line 389
            return _.readOrCopyVersionedFile(branch, _.findRevision(branch, revision, pinfo.nameHash)[0], pinfo.nameHash) if pinfo.size > 0 else b''  # just return contents  # line 389
        target = os.path.join(_.root, relPath.replace(SLASH, os.sep))  # type: str  # line 390
        if ensurePath:  #  and not os.path.exists(os.path.dirname(target)):  # line 391
            try:  # line 392
                os.makedirs(os.path.dirname(target))  # line 392
            except:  # line 393
                pass  # line 393
        if pinfo.size == 0:  # line 394
            with open(target, "wb"):  # line 395
                pass  # line 395
            try:  # update access/modification timestamps on file system  # line 396
                os.utime(target, (-1, pinfo.mtime / 1000.))  # update access/modification timestamps on file system  # line 396
            except Exception as E:  # line 397
                error("Cannot update file's timestamp after restoration '%r'" % E)  # line 397
            return None  # line 398
        revision, source = _.findRevision(branch, revision, pinfo.nameHash)  # line 399
# Restore file by copying buffer-wise
        with openIt(source, "r", _.compress) as fd, open(target, "wb") as to:  # using Coconut's Enhanced Parenthetical Continuation  # line 401
            while True:  # line 402
                buffer = fd.read(bufSize)  # line 403
                to.write(buffer)  # line 404
                if len(buffer) < bufSize:  # line 405
                    break  # line 405
        try:  # update access/modification timestamps on file system  # line 406
            os.utime(target, (-1, pinfo.mtime / 1000.))  # update access/modification timestamps on file system  # line 406
        except Exception as E:  # line 407
            error("Cannot update file's timestamp after restoration '%r'" % E)  # line 407
        return None  # line 408

    def getTrackingPatterns(_, branch: '_coconut.typing.Optional[int]'=None) -> 'FrozenSet[str]':  # line 410
        ''' Returns list of tracking patterns for provided branch or current branch. '''  # line 411
        return _coconut.frozenset() if not _.track and not _.picky else frozenset(_.branches[_.branch if branch is None else branch].tracked)  # line 412


# Main client operations
def offline(argument: '_coconut.typing.Optional[str]'=None, options: '_coconut.typing.Sequence[str]'=[]) -> 'None':  # line 416
    ''' Initial command to start working offline. '''  # line 417
    if os.path.exists(metaFolder):  # line 418
        if '--force' not in options:  # line 419
            Exit("Repository folder is either already offline or older branches and commits were left over.\nUse 'sos online' to check for dirty branches, or\nWipe existing offline branches with 'sos offline --force'")  # line 419
        try:  # line 420
            for entry in os.listdir(metaFolder):  # line 421
                resource = metaFolder + os.sep + entry  # line 422
                if os.path.isdir(resource):  # line 423
                    shutil.rmtree(resource)  # line 423
                else:  # line 424
                    os.unlink(resource)  # line 424
        except:  # line 425
            Exit("Cannot reliably remove previous repository contents. Please remove .sos folder manually prior to going offline")  # line 425
    m = Metadata(os.getcwd())  # type: Metadata  # line 426
    if '--plain' in options or not m.c.compress:  # plain file copies instead of compressed ones  # line 427
        m.compress = False  # plain file copies instead of compressed ones  # line 427
    if '--picky' in options or m.c.picky:  # Git-like  # line 428
        m.picky = True  # Git-like  # line 428
    elif '--track' in options or m.c.track:  # Svn-like  # line 429
        m.track = True  # Svn-like  # line 429
    if '--strict' in options or m.c.strict:  # always hash contents  # line 430
        m.strict = True  # always hash contents  # line 430
    debug("Preparing offline repository...")  # line 431
    m.createBranch(0, str(defaults["defaultbranch"]) if argument is None else argument, initialMessage="Offline repository created on %s" % strftime())  # main branch's name may be None (e.g. for fossil)  # line 432
    m.branch = 0  # line 433
    m.saveBranches()  # no change immediately after going offline, going back online won't issue a warning  # line 434
    info("Offline repository prepared. Use 'sos online' to finish offline work")  # line 435

def online(options: '_coconut.typing.Sequence[str]'=[]) -> 'None':  # line 437
    ''' Finish working offline. '''  # line 438
    force = '--force' in options  # type: bool  # line 439
    m = Metadata(os.getcwd())  # line 440
    m.loadBranches()  # line 441
    if any([not b.inSync for b in m.branches.values()]) and not force:  # line 442
        Exit("There are still unsynchronized (dirty) branches.\nUse 'sos log' to list them.\nUse 'sos commit' and 'sos switch' to commit dirty branches to your VCS before leaving offline mode.\nUse 'sos online --force' to erase all aggregated offline revisions")  # line 442
    strict = '--strict' in options or m.strict  # type: bool  # line 443
    if options.count("--force") < 2:  # line 444
        changes = m.findChanges(checkContent=strict, considerOnly=None if not m.track and not m.picky else m.getTrackingPatterns())  # type: ChangeSet  # HINT no option for --only/--except here on purpose. No check for picky here, because online is not a command that considers staged files (but we could use --only here, alternatively)  # line 445
        if modified(changes):  # line 446
            Exit("File tree is modified vs. current branch.\nUse 'sos online --force --force' to continue with removing the offline repository")  # line 446
    try:  # line 447
        shutil.rmtree(metaFolder)  # line 447
        info("Exited offline mode. Continue working with your traditional VCS.")  # line 447
    except Exception as E:  # line 448
        Exit("Error removing offline repository: %r" % E)  # line 448

def branch(argument: '_coconut.typing.Optional[str]'=None, options: '_coconut.typing.Sequence[str]'=[]) -> 'None':  # line 450
    ''' Create a new branch (from file tree or last revision) and (by default) continue working on it. '''  # line 451
    last = '--last' in options  # type: bool  # use last revision for branching, not current file tree  # line 452
    stay = '--stay' in options  # type: bool  # continue on current branch after branching  # line 453
    force = '--force' in options  # type: bool  # branch even with local modifications  # line 454
    m = Metadata(os.getcwd())  # type: Metadata  # line 455
    m.loadBranches()  # line 456
    m.loadBranch(m.branch)  # line 457
    if argument and m.getBranchByName(argument) is not None:  # create a named branch  # line 458
        Exit("Branch '%s' already exists. Cannot proceed" % argument)  # create a named branch  # line 458
    branch = max(m.branches.keys()) + 1  # next branch's key - this isn't atomic but we assume single-user non-concurrent use here  # line 459
    debug("Branching to %sbranch b%02d%s%s..." % ("unnamed " if argument is None else "", branch, " '%s'" % argument if argument else "", " from last revision" if last else ""))  # line 460
    if last:  # line 461
        m.duplicateBranch(branch, "Branched from r%02d/b%02d" % (m.branch, max(m.commits.keys())) if argument is None else argument)  # branch from branch's last revision  # line 462
    else:  # from file tree state  # line 463
        m.createBranch(branch, "Branched from r%02d/b%02d" % (m.branch, max(m.commits.keys())) if argument is None else argument)  # branch from current file tree  # line 464
    if not stay:  # line 465
        m.branch = branch  # line 466
        m.saveBranches()  # line 467
    info("%s new %sbranch b%02d%s" % ("Continue work after branching" if stay else "Switched to", "unnamed " if argument is None else "", branch, " '%s'" % argument if argument else ""))  # line 468

def changes(argument: 'str'=None, options: '_coconut.typing.Sequence[str]'=[], onlys: '_coconut.typing.Optional[FrozenSet[str]]'=None, excps: '_coconut.typing.Optional[FrozenSet[str]]'=None) -> 'ChangeSet':  # line 470
    ''' Show changes of file tree vs. (last or specified) revision on current or specified branch. '''  # line 471
    m = Metadata(os.getcwd())  # type: Metadata  # line 472
    branch = None  # type: _coconut.typing.Optional[int]  # line 472
    revision = None  # type: _coconut.typing.Optional[int]  # line 472
    m.loadBranches()  # knows current branch  # line 473
    strict = '--strict' in options or m.strict  # type: bool  # line 474
    branch, revision = m.parseRevisionString(argument)  # line 475
    if branch not in m.branches:  # line 476
        Exit("Unknown branch")  # line 476
    m.loadBranch(branch)  # knows commits  # line 477
    revision = revision if revision >= 0 else len(m.commits) + revision  # negative indexing  # line 478
    if revision < 0 or revision > max(m.commits):  # line 479
        Exit("Unknown revision r%02d" % revision)  # line 479
    info("//|\\\\ Changes of file tree vs. revision '%s/r%02d'" % ((lambda _coconut_none_coalesce_item: "b%02d" % branch if _coconut_none_coalesce_item is None else _coconut_none_coalesce_item)(m.branches[branch].name), revision))  # line 480
    m.computeSequentialPathSet(branch, revision)  # load all commits up to specified revision  # line 481
    changes = m.findChanges(checkContent=strict, considerOnly=onlys if not m.track and not m.picky else conditionalIntersection(onlys, m.getTrackingPatterns() | m.getTrackingPatterns(branch)), dontConsider=excps)  # type: ChangeSet  # line 482
    m.listChanges(changes)  # line 483
    return changes  # for unit tests only  # line 484

def diff(argument: 'str'="", options: '_coconut.typing.Sequence[str]'=[], onlys: '_coconut.typing.Optional[FrozenSet[str]]'=None, excps: '_coconut.typing.Optional[FrozenSet[str]]'=None) -> 'None':  # line 486
    ''' Show text file differences of file tree vs. (last or specified) revision on current or specified branch. '''  # line 487
    m = Metadata(os.getcwd())  # type: Metadata  # line 488
    branch = None  # type: _coconut.typing.Optional[int]  # line 488
    revision = None  # type: _coconut.typing.Optional[int]  # line 488
    m.loadBranches()  # knows current branch  # line 489
    strict = '--strict' in options or m.strict  # type: bool  # line 490
    _from = {None: option.split("--from=")[1] for option in options if options.startswith("--from=")}.get(None, None)  # type: _coconut.typing.Optional[str]  # line 491
    branch, revision = m.parseRevisionString(argument)  # if nothing given, use last commit  # line 492
    if branch not in m.branches:  # line 493
        Exit("Unknown branch")  # line 493
    m.loadBranch(branch)  # knows commits  # line 494
    revision = revision if revision >= 0 else len(m.commits) + revision  # negative indexing  # line 495
    if revision < 0 or revision > max(m.commits):  # line 496
        Exit("Unknown revision r%02d" % revision)  # line 496
    info("//|\\\\ Differences of file tree vs. revision '%s/r%02d'" % ((lambda _coconut_none_coalesce_item: "b%02d" % branch if _coconut_none_coalesce_item is None else _coconut_none_coalesce_item)(m.branches[branch].name), revision))  # line 497
    m.computeSequentialPathSet(branch, revision)  # load all commits up to specified revision  # line 498
    changes = m.findChanges(checkContent=strict, inverse=True, considerOnly=onlys if not m.track and not m.picky else conditionalIntersection(onlys, m.getTrackingPatterns() | m.getTrackingPatterns(branch)), dontConsider=excps)  # type: ChangeSet  # line 499
    onlyBinaryModifications = dataCopy(ChangeSet, changes, modifications={k: v for k, v in changes.modifications.items() if not m.isTextType(os.path.basename(k))})  # type: ChangeSet  # line 500
    if modified(onlyBinaryModifications):  # line 501
        debug("//|\\\\ File changes")  # line 501
    m.listChanges(onlyBinaryModifications)  # only list modified binary files  # line 502

    if changes.modifications:  # line 504
        debug("%s//|\\\\ Textual modifications" % ("\n" if modified(onlyBinaryModifications) else ""))  # line 504
    for path, pinfo in (c for c in changes.modifications.items() if m.isTextType(os.path.basename(c[0]))):  # only consider modified text files  # line 505
        content = None  # type: _coconut.typing.Optional[bytes]  # ; othr:str[]; curr:str[]  # line 506
        if pinfo.size == 0:  # empty file contents  # line 507
            content = b""  # empty file contents  # line 507
        else:  # versioned file  # line 508
            content = m.restoreFile(None, branch, revision, pinfo)  # versioned file  # line 508
            assert content is not None  # versioned file  # line 508
        abspath = os.path.join(m.root, path.replace(SLASH, os.sep))  # current file  # line 509
        blocks = merge(file=content, intoname=abspath, diffOnly=True)  # type: List[MergeBlock]  # only determine change blocks  # line 510
        print("DIF %s%s" % (path, " <timestamp only>" if len(blocks) == 1 and blocks[0].tipe == MergeBlockType.KEEP else ""))  # line 511
        for block in blocks:  # line 512
            if block.tipe in [MergeBlockType.INSERT, MergeBlockType.REMOVE]:  # line 513
                pass  # TODO print some previous and following lines - which aren't accessible here anymore  # line 514
            if block.tipe == MergeBlockType.INSERT:  # TODO show color via (n)curses or other library?  # line 515
                for no, line in enumerate(block.lines):  # line 516
                    print("+++ %04d |%s|" % (no + block.line, line))  # line 517
            elif block.tipe == MergeBlockType.REMOVE:  # line 518
                for no, line in enumerate(block.lines):  # line 519
                    print("--- %04d |%s|" % (no + block.line, line))  # line 520
            elif block.tipe in [MergeBlockType.REPLACE, MergeBlockType.MODIFY]:  # TODO for MODIFY also show intra-line change ranges  # line 521
                for no, line in enumerate(block.replaces.lines):  # line 522
                    print("- | %04d |%s|" % (no + block.replaces.line, line))  # line 523
                for no, line in enumerate(block.lines):  # line 524
                    print("+ | %04d |%s|" % (no + block.line, line))  # line 525
#      elif block.tipe == MergeBlockType.KEEP: pass
#      elif block.tipe == MergeBlockType.MODIFY:  # intra-line modifications
#      elif block.tipe == MergeBlockType.MOVE:  # intra-line modifications

def commit(argument: '_coconut.typing.Optional[str]'=None, options: '_coconut.typing.Sequence[str]'=[], onlys: '_coconut.typing.Optional[FrozenSet[str]]'=None, excps: '_coconut.typing.Optional[FrozenSet[str]]'=None) -> 'None':  # line 530
    ''' Create new revision from file tree changes vs. last commit. '''  # line 531
    m = Metadata(os.getcwd())  # type: Metadata  # line 532
    m.loadBranches()  # knows current branch  # line 533
    if argument is not None and argument in m.tags:  # line 534
        Exit("Illegal commit message. It was already used as a tag name")  # line 534
    trackingPatterns = m.getTrackingPatterns()  # type: FrozenSet[str]  # SVN-like mode  # line 535
    if m.picky and not trackingPatterns:  # line 536
        Exit("No file patterns staged for commit in picky mode")  # line 536
    changes = None  # type: ChangeSet  # line 537
    m, branch, revision, changes, strict, force, trackingPatterns = exitOnChanges(None, options, commit=True, onlys=onlys, excps=excps)  # special flag creates new revision for detected changes, but abort if no changes  # line 538
    info((lambda _coconut_none_coalesce_item: "b%d" % m.branch if _coconut_none_coalesce_item is None else _coconut_none_coalesce_item)("Committing changes to branch '%s'..." % m.branches[m.branch].name))  # line 539
    m.integrateChangeset(changes, clear=True)  # update pathset to changeset only  # line 540
    m.saveCommit(m.branch, revision)  # revision has already been incremented  # line 541
    m.commits[revision] = CommitInfo(revision, longint(time.time() * 1000), argument)  # comment can be None  # line 542
    m.saveBranch(m.branch)  # line 543
    m.loadBranches()  # TODO is it necessary to load again?  # line 544
    if m.picky:  # line 545
        m.branches[m.branch] = dataCopy(BranchInfo, m.branches[m.branch], tracked=[], inSync=False)  # remove tracked patterns  # line 546
    else:  # track or simple mode  # line 547
        m.branches[m.branch] = dataCopy(BranchInfo, m.branches[m.branch], inSync=False)  # set branch dirty  # line 548
    if "--tag" in options and argument is not None:  # memorize unique tag  # line 549
        m.tags.append(argument)  # memorize unique tag  # line 549
    m.saveBranches()  # line 550
    info("Created new revision r%02d%s (+%02d/-%02d/*%02d)" % (revision, ((" '%s'" % argument) if argument is not None else ""), len(changes.additions), len(changes.deletions), len(changes.modifications)))  # line 551

def status() -> 'None':  # line 553
    ''' Show branches and current repository state. '''  # line 554
    m = Metadata(os.getcwd())  # type: Metadata  # line 555
    m.loadBranches()  # knows current branch  # line 556
    current = m.branch  # type: int  # line 557
    info("//|\\\\ Offline repository status")  # line 558
    print("Content checking %sactivated" % ("" if m.strict else "de"))  # line 559
    print("Data compression %sactivated" % ("" if m.compress else "de"))  # line 560
    print("Repository is in %s mode" % ("tracking" if m.track else ("picky" if m.picky else "simple")))  # line 561
    sl = max([len((lambda _coconut_none_coalesce_item: "" if _coconut_none_coalesce_item is None else _coconut_none_coalesce_item)(b.name)) for b in m.branches.values()])  # type: int  # line 562
    for branch in sorted(m.branches.values(), key=lambda b: b.number):  # line 563
        m.loadBranch(branch.number)  # knows commit history  # line 564
        print("  %s b%02d%s @%s (%s) with %d commits%s" % ("*" if current == branch.number else " ", branch.number, ((" %%%ds" % (sl + 2)) % ("'%s'" % branch.name)) if branch.name else "", strftime(branch.ctime), "in sync" if branch.inSync else "dirty", len(m.commits), ". Last comment: '%s'" % m.commits[max(m.commits)].message if m.commits[max(m.commits)].message else ""))  # line 565
    if m.track or m.picky and len(m.branches[m.branch].tracked) > 0:  # line 566
        info("\nTracked file patterns:")  # line 567
        print(ajoin("  | ", m.branches[m.branch].tracked, "\n"))  # line 568

def exitOnChanges(argument: '_coconut.typing.Optional[str]'=None, options: '_coconut.typing.Sequence[str]'=[], check: 'bool'=True, commit: 'bool'=False, onlys: '_coconut.typing.Optional[FrozenSet[str]]'=None, excps: '_coconut.typing.Optional[FrozenSet[str]]'=None) -> 'Tuple[Metadata, _coconut.typing.Optional[int], int, ChangeSet, bool, bool, FrozenSet[str]]':  # line 570
    ''' Common behavior for switch, update, delete, commit.
      Should not be called for picky mode, unless tracking patterns were added.
      check: stop program on detected change
      commit: don't stop on changes, because that's what we need in the operation
      Returns (Metadata, (current or target) branch, revision, set of changes vs. last commit on current branch, strict, force flags. '''  # line 575
    m = Metadata(os.getcwd())  # type: Metadata  # line 576
    m.loadBranches()  # knows current branch  # line 577
    force = '--force' in options  # type: bool  # line 578
    strict = '--strict' in options or m.strict  # type: bool  # line 579
    if argument is not None:  # line 580
        branch, revision = m.parseRevisionString(argument)  # for early abort  # line 581
        if branch is None:  # line 582
            Exit("Branch '%s' doesn't exist. Cannot proceed" % argument)  # line 582
    m.loadBranch(m.branch)  # knows last commits of *current* branch  # line 583

# Determine current changes
    trackingPatterns = m.getTrackingPatterns()  # type: FrozenSet[str]  # line 586
    m.computeSequentialPathSet(m.branch, max(m.commits))  # load all commits up to specified revision  # line 587
    changes = m.findChanges(m.branch if commit else None, max(m.commits) + 1 if commit else None, checkContent=strict, considerOnly=onlys if not (m.track or m.picky) else conditionalIntersection(onlys, trackingPatterns), dontConsider=excps)  # type: ChangeSet  # line 588
    if check and modified(changes) and not force:  # line 589
        m.listChanges(changes)  # line 590
        if not commit:  # line 591
            Exit("File tree contains changes. Use --force to proceed")  # line 591
    elif commit and not force:  #  and not check  # line 592
        Exit("Nothing to commit")  #  and not check  # line 592

    if argument is not None:  # branch/revision specified  # line 594
        m.loadBranch(branch)  # knows commits of target branch  # line 595
        revision = revision if revision >= 0 else len(m.commits) + revision  # negative indexing  # line 596
        if revision < 0 or revision > max(m.commits):  # line 597
            Exit("Unknown revision r%02d" % revision)  # line 597
        return (m, branch, revision, changes, strict, force, m.getTrackingPatterns(branch))  # line 598
    return (m, m.branch, max(m.commits) + (1 if commit else 0), changes, strict, force, trackingPatterns)  # line 599

def switch(argument: 'str', options: '_coconut.typing.Sequence[str]'=[], onlys: '_coconut.typing.Optional[FrozenSet[str]]'=None, excps: '_coconut.typing.Optional[FrozenSet[str]]'=None) -> 'None':  # line 601
    ''' Continue work on another branch, replacing file tree changes. '''  # line 602
    changes = None  # type: ChangeSet  # line 603
    m, branch, revision, changes, strict, force, trackingPatterns = exitOnChanges(argument, options)  # line 604
    info("//|\\\\ Switching to branch %sb%02d/r%02d" % ("'%s' " % m.branches[branch].name if m.branches[branch].name else "", branch, revision))  # line 605

# Determine file changes from other branch to current file tree
    if '--meta' in options:  # only switch meta data  # line 608
        m.branches[m.branch] = dataCopy(BranchInfo, m.branches[m.branch], tracked=m.branches[branch].tracked)  # line 609
    else:  # full file switch  # line 610
        m.computeSequentialPathSet(branch, revision)  # load all commits up to specified revision for target branch into memory  # line 611
        changes = m.findChanges(checkContent=strict, inverse=True, considerOnly=onlys if not m.track and not m.picky else conditionalIntersection(onlys, trackingPatterns | m.getTrackingPatterns(branch)), dontConsider=excps)  # determine difference of other branch vs. file tree (forced or in sync with current branch; "addition" means exists now and should be removed)  # line 612
        if not modified(changes):  # line 613
            info("No changes to current file tree")  # line 614
        else:  # integration required  # line 615
            for path, pinfo in changes.deletions.items():  # line 616
                m.restoreFile(path, branch, revision, pinfo, ensurePath=True)  # is deleted in current file tree: restore from branch to reach target  # line 617
                print("ADD " + path)  # line 618
            for path, pinfo in changes.additions.items():  # line 619
                os.unlink(os.path.join(m.root, path.replace(SLASH, os.sep)))  # is added in current file tree: remove from branch to reach target  # line 620
                print("DEL " + path)  # line 621
            for path, pinfo in changes.modifications.items():  # line 622
                m.restoreFile(path, branch, revision, pinfo)  # is modified in current file tree: restore from branch to reach target  # line 623
                print("MOD " + path)  # line 624
    m.branch = branch  # line 625
    m.saveBranches()  # store switched path info  # line 626
    info("Switched to branch %sb%02d/r%02d" % ("'%s' " % (m.branches[branch].name if m.branches[branch].name else ""), branch, revision))  # line 627

def update(argument: 'str', options: '_coconut.typing.Sequence[str]'=[], onlys: '_coconut.typing.Optional[FrozenSet[str]]'=None, excps: '_coconut.typing.Optional[FrozenSet[str]]'=None) -> 'None':  # line 629
    ''' Load and integrate a specified other branch/revision into current life file tree.
      In tracking mode, this also updates the set of tracked patterns.
      User options for merge operation: --add (don't remove), --rm (don't insert), --add-lines/--rm-lines (inside each file)
      User options for conflict resolution: --theirs/--mine/--ask
  '''  # line 634
    mrg = firstOfMap({"--add": MergeOperation.INSERT, "--rm": MergeOperation.REMOVE}, options, MergeOperation.BOTH)  # type: int  # default operation is replicate remove state for non-conflicting cases (insertions/deletions)  # line 635
    res = firstOfMap({'--theirs': ConflictResolution.THEIRS, '--mine': ConflictResolution.MINE}, options, ConflictResolution.NEXT)  # type: int  # NEXT means deeper level  # line 636
    mrgline = firstOfMap({'--add-lines': MergeOperation.INSERT, '--rm-lines': MergeOperation.REMOVE}, options, mrg)  # type: int  # default operation for modified files is same as for files  # line 637
    resline = firstOfMap({'--theirs-lines': ConflictResolution.THEIRS, '--mine-lines': ConflictResolution.MINE}, options, ConflictResolution.ASK)  # type: int  # line 638
    m = Metadata(os.getcwd())  # type: Metadata  # TODO same is called inside stop on changes - could return both current and designated branch instead  # line 639
    m.loadBranches()  # line 640
    changes = None  # type: ChangeSet  # line 640
    currentBranch = m.branch  # type: _coconut.typing.Optional[int]  # line 641
    m, branch, revision, changes, strict, force, trackingPatterns = exitOnChanges(argument, options, check=False, onlys=onlys, excps=excps)  # don't check for current changes, only parse arguments  # line 642
    debug("Integrating changes from '%s/r%02d' into file tree..." % ((lambda _coconut_none_coalesce_item: "b%02d" % branch if _coconut_none_coalesce_item is None else _coconut_none_coalesce_item)(m.branches[branch].name), revision))  # line 643

# Determine file changes from other branch over current file tree
    m.computeSequentialPathSet(branch, revision)  # load all commits up to specified revision for branch to integrate  # line 646
    trackingUnion = trackingPatterns | m.getTrackingPatterns(branch)  # type: FrozenSet[str]  # line 647
    changes = m.findChanges(checkContent=strict, inverse=True, considerOnly=onlys if not m.track and not m.picky else conditionalIntersection(onlys, trackingUnion), dontConsider=excps)  # determine difference of other branch vs. file tree. "addition" means exists now but not in other, and should be removed unless in tracking mode  # line 648
    if not (mrg & MergeOperation.INSERT and changes.additions or (mrg & MergeOperation.REMOVE and changes.deletions) or changes.modifications):  # no file ops  # line 649
        if trackingUnion != trackingPatterns:  # nothing added  # line 650
            info("No file changes detected, but tracking patterns were merged (run 'sos switch /-1 --meta' to undo)")  # TODO write test to see if this works  # line 651
        else:  # line 652
            info("Nothing to update")  # but write back updated branch info below  # line 653
    else:  # integration required  # line 654
        for path, pinfo in changes.deletions.items():  # deletions mark files not present in current file tree -> needs additon  # line 655
            if mrg & MergeOperation.INSERT:  # deleted in current file tree: restore from branch to reach target  # line 656
                m.restoreFile(path, branch, revision, pinfo, ensurePath=True)  # deleted in current file tree: restore from branch to reach target  # line 656
            print("ADD " + path if mrg & MergeOperation.INSERT else "(A) " + path)  # line 657
        for path, pinfo in changes.additions.items():  # line 658
            if m.track or m.picky:  # because untracked files of other branch cannot be detected (which is good)  # line 659
                Exit("This should never happen")  # because untracked files of other branch cannot be detected (which is good)  # line 659
            if mrg & MergeOperation.REMOVE:  # line 660
                os.unlink(m.root + os.sep + path.replace(SLASH, os.sep))  # line 660
            print("DEL " + path if mrg & MergeOperation.REMOVE else "(D) " + path)  # not contained in other branch, but maybe kept  # line 661
        for path, pinfo in changes.modifications.items():  # line 662
            into = os.path.join(m.root, path.replace(SLASH, os.sep))  # type: str  # line 663
            binary = not m.isTextType(path)  # line 664
            if res & ConflictResolution.ASK or (binary and res == ConflictResolution.NEXT):  # TODO this may ask user even if no interaction was asked for (check line level for interactivity fist)  # line 665
                print(("MOD " + path if not binary else "BIN ") + path)  # line 666
                reso = {"i": ConflictResolution.MINE, "t": ConflictResolution.THEIRS, "m": ConflictResolution.NEXT}.get(user_input(" Resolve: *M[I]ne, [T]heirs, [M]erge: (I)").strip().lower(), ConflictResolution.MINE)  # line 667
                debug("User selected %d" % reso)  # line 668
            else:  # line 669
                reso = res  # line 669
            if reso & ConflictResolution.THEIRS:  # line 670
                m.readOrCopyVersionedFile(branch, revision, pinfo.nameHash, toFile=into)  # blockwise copy of contents  # line 671
                print("THR " + path)  # line 672
            elif reso & ConflictResolution.MINE:  # line 673
                print("MNE " + path)  # nothing to do! same as skip  # line 674
            else:  # NEXT: line-based merge  # line 675
                file = m.readOrCopyVersionedFile(branch, revision, pinfo.nameHash) if pinfo.size > 0 else b''  # type: _coconut.typing.Optional[bytes]  # parse lines  # line 676
                if file is not None:  # if None, error message was already logged  # line 677
                    contents = merge(file=file, intoname=into, mergeOperation=mrgline, conflictResolution=resline)  # type: bytes  # line 678
                    with open(path, "wb") as fd:  # TODO write to temp file first, in case writing fails  # line 679
                        fd.write(contents)  # TODO write to temp file first, in case writing fails  # line 679
    info("Integrated changes from '%s/r%02d' into file tree" % ((lambda _coconut_none_coalesce_item: "b%02d" % branch if _coconut_none_coalesce_item is None else _coconut_none_coalesce_item)(m.branches[branch].name), revision))  # line 680
    m.branches[currentBranch] = dataCopy(BranchInfo, m.branches[currentBranch], inSync=False, tracked=list(trackingUnion))  # line 681
    m.branch = currentBranch  # need to restore setting before saving TODO operate on different objects instead  # line 682
    m.saveBranches()  # line 683

def delete(argument: 'str', options: '_coconut.typing.Sequence[str]'=[]) -> 'None':  # line 685
    ''' Remove a branch entirely. '''  # line 686
    m, branch, revision, changes, strict, force, trackingPatterns = exitOnChanges(None, options)  # line 687
    if len(m.branches) == 1:  # line 688
        Exit("Cannot remove the only remaining branch. Use 'sos online' to leave offline mode")  # line 688
    branch, revision = m.parseRevisionString(argument)  # not from exitOnChanges, because we have to set argument to None there  # line 689
    if branch is None or branch not in m.branches:  # line 690
        Exit("Unknown branch")  # line 690
    debug("Removing branch %d%s..." % (branch, " '%s'" % m.branches[branch].name if m.branches[branch].name else ""))  # line 691
    binfo = m.removeBranch(branch)  # need to keep a reference to removed entry for output below  # line 692
    info("Branch b%02d%s removed" % (branch, " '%s'" % binfo.name if binfo.name else ""))  # line 693

def add(relPath: 'str', pattern: 'str', options: '_coconut.typing.Sequence[str]'=[]) -> 'None':  # line 695
    ''' Add a tracked files pattern to current branch's tracked files. '''  # line 696
    force = '--force' in options  # type: bool  # line 697
    m = Metadata(os.getcwd())  # type: Metadata  # line 698
    m.loadBranches()  # line 699
    if not m.track and not m.picky:  # line 700
        Exit("Repository is in simple mode. Use 'offline --track' or 'offline --picky' instead")  # line 700
    if pattern in m.branches[m.branch].tracked:  # line 701
        Exit("Pattern '%s' already tracked" % pattern)  # line 701
    if not force and not os.path.exists(relPath.replace(SLASH, os.sep)):  # line 702
        Exit("The pattern folder doesn't exist. Use --force to add it anyway")  # line 702
    if not force and len(fnmatch.filter(os.listdir(os.path.abspath(relPath.replace(SLASH, os.sep))), os.path.basename(pattern.replace(SLASH, os.sep)))) == 0:  # doesn't match any current file  # line 703
        Exit("Pattern doesn't match any file in specified folder. Use --force to add it anyway")  # line 704
    m.branches[m.branch].tracked.append(pattern)  # line 705
    m.saveBranches()  # line 706
    info("Added tracking pattern '%s' for folder '%s'" % (os.path.basename(pattern.replace(SLASH, os.sep)), os.path.abspath(relPath)))  # line 707

def remove(relPath: 'str', pattern: 'str') -> 'None':  # line 709
    ''' Remove a tracked files pattern from current branch's tracked files. '''  # line 710
    m = Metadata(os.getcwd())  # type: Metadata  # line 711
    m.loadBranches()  # line 712
    if not m.track and not m.picky:  # line 713
        Exit("Repository is in simple mode. Needs 'offline --track' or 'offline --picky' instead")  # line 713
    if pattern not in m.branches[m.branch].tracked:  # line 714
        suggestion = _coconut.set()  # type: Set[str]  # line 715
        for pat in m.branches[m.branch].tracked:  # line 716
            if fnmatch.fnmatch(pattern, pat):  # line 717
                suggestion.add(pat)  # line 717
        if suggestion:  # TODO use same wording as in move  # line 718
            print("Do you mean any of the following tracked file patterns? '%s'" % (", ".join(sorted(suggestion))))  # TODO use same wording as in move  # line 718
        Exit("Tracked pattern '%s' not found" % pattern)  # line 719
    m.branches[m.branch].tracked.remove(pattern)  # line 720
    m.saveBranches()  # line 721
    info("Removed tracking pattern '%s' for folder '%s'" % (os.path.basename(pattern), os.path.abspath(relPath.replace(SLASH, os.sep))))  # line 722

def ls(argument: '_coconut.typing.Optional[str]'=None, options: '_coconut.typing.Sequence[str]'=[]) -> 'None':  # line 724
    ''' List specified directory, augmenting with repository metadata. '''  # line 725
    folder = "." if argument is None else argument  # type: str  # line 726
    m = Metadata(os.getcwd())  # type: Metadata  # line 727
    m.loadBranches()  # line 728
    info("Repository is in %s mode" % ("tracking" if m.track else ("picky" if m.picky else "simple")))  # line 729
    relPath = os.path.relpath(folder, m.root).replace(os.sep, SLASH)  # type: str  # line 730
    trackingPatterns = m.getTrackingPatterns() if m.track or m.picky else _coconut.frozenset()  # type: _coconut.typing.Optional[FrozenSet[str]]  # for current branch  # line 731
    if '--patterns' in options:  # line 732
        out = ajoin("TRK ", [os.path.basename(p) for p in trackingPatterns if os.path.dirname(p).replace(os.sep, SLASH) == relPath], nl="\n")  # type: str  # line 733
        if out:  # line 734
            print(out)  # line 734
        return  # line 735
    files = list(sorted((entry for entry in os.listdir(folder) if os.path.isfile(os.path.join(folder, entry)))))  # type: List[str]  # line 736
    for file in files:  # for each file list all tracking patterns that match, or none (e.g. in picky mode after commit)  # line 737
        ignore = None  # type: _coconut.typing.Optional[str]  # line 738
        for ig in m.c.ignores:  # line 739
            if fnmatch.fnmatch(file, ig):  # remember first match  # line 740
                ignore = ig  # remember first match  # line 740
                break  # remember first match  # line 740
        if ig:  # line 741
            for wl in m.c.ignoresWhitelist:  # line 742
                if fnmatch.fnmatch(file, wl):  # found a white list entry for ignored file, undo ignoring it  # line 743
                    ignore = None  # found a white list entry for ignored file, undo ignoring it  # line 743
                    break  # found a white list entry for ignored file, undo ignoring it  # line 743
        if not ignore:  # line 744
            matches = []  # type: List[str]  # line 745
            for pattern in (p for p in trackingPatterns if os.path.dirname(p).replace(os.sep, SLASH) == relPath):  # only patterns matching current folder  # line 746
                if fnmatch.fnmatch(file, os.path.basename(pattern)):  # line 747
                    matches.append(os.path.basename(pattern))  # line 747
        matches.sort(key=lambda element: len(element))  # line 748
        print("%s %s%s" % ("IGN" if ignore is not None else ("TRK" if len(matches) > 0 else "..."), file, "  (%s)" % ignore if ignore is not None else ("  (%s)" % ("; ".join(matches)) if len(matches) > 0 else "")))  # line 749

def log(options: '_coconut.typing.Sequence[str]') -> 'None':  # line 751
    ''' List previous commits on current branch. '''  # line 752
    m = Metadata(os.getcwd())  # type: Metadata  # line 753
    m.loadBranches()  # knows current branch  # line 754
    m.loadBranch(m.branch)  # knows commit history  # line 755
    info((lambda _coconut_none_coalesce_item: "r%02d" % m.branch if _coconut_none_coalesce_item is None else _coconut_none_coalesce_item)("//|\\\\ Offline commit history of branch '%s'" % m.branches[m.branch].name))  # TODO also retain "from branch/revision" on branching?  # line 756
    nl = len("%d" % max(m.commits))  # determine space needed for revision  # line 757
    changeset = m.computeSequentialPathSetIterator(m.branch, max(m.commits))  # line 758
    maxWidth = max([wcswidth((lambda _coconut_none_coalesce_item: "" if _coconut_none_coalesce_item is None else _coconut_none_coalesce_item)(commit.message)) for commit in m.commits.values()])  # type: int  # line 759
    for no in range(max(m.commits) + 1):  # line 760
        commit = m.commits[no]  # type: CommitInfo  # line 761
        changes = next(changeset)  # type: ChangeSet  # side-effect: updates m.paths  # line 762
        newTextFiles = len([file for file in changes.additions.keys() if m.isTextType(file)])  # type: int  # line 763
        print("  %s r%s @%s (+%02d/-%02d/*%02d +%02dT/%05.1f%%) |%s|" % ("*" if commit.number == max(m.commits) else " ", ("%%%ds" % nl) % commit.number, strftime(commit.ctime), len(changes.additions), len(changes.deletions), len(changes.modifications), newTextFiles, 0. if len(changes.additions) == 0 else newTextFiles * 100. / len(changes.additions), ((lambda _coconut_none_coalesce_item: "" if _coconut_none_coalesce_item is None else _coconut_none_coalesce_item)(commit.message)).ljust(maxWidth)))  # line 764
        if '--changes' in options:  # line 765
            m.listChanges(changes)  # line 765

def config(argument: 'str', options: 'List[str]'=[]) -> 'None':  # line 767
    if argument not in ["set", "unset", "show", "list", "add", "rm"]:  # line 768
        Exit("Unknown config command")  # line 768
    if not configr:  # line 769
        Exit("Cannot execute config command. 'configr' module not installed")  # line 769
    c = loadConfig()  # type: Union[configr.Configr, Accessor]  # line 770
    if argument == "set":  # line 771
        if len(options) < 2:  # line 772
            Exit("No key nor value specified")  # line 772
        if options[0] not in (["defaultbranch"] + CONFIGURABLE_FLAGS + CONFIGURABLE_LISTS):  # line 773
            Exit("Unsupported key %r" % options[0])  # line 773
        if options[0] in CONFIGURABLE_FLAGS and options[1].lower() not in TRUTH_VALUES + FALSE_VALUES:  # line 774
            Exit("Cannot set flag to '%s'. Try on/off instead" % options[1].lower())  # line 774
        c[options[0]] = options[1].lower() in TRUTH_VALUES if options[0] in CONFIGURABLE_FLAGS else (options[1].strip() if options[0] not in CONFIGURABLE_LISTS else safeSplit(options[1], ";"))  # TODO sanitize texts?  # line 775
    elif argument == "unset":  # line 776
        if len(options) < 1:  # line 777
            Exit("No key specified")  # line 777
        if options[0] not in c.keys():  # line 778
            Exit("Unknown key")  # line 778
        del c[options[0]]  # line 779
    elif argument == "add":  # line 780
        if len(options) < 2:  # line 781
            Exit("No key nor value specified")  # line 781
        if options[0] not in CONFIGURABLE_LISTS:  # line 782
            Exit("Unsupported key for add %r" % options[0])  # line 782
        if options[0] not in c.keys():  # add list  # line 783
            c[options[0]] = [options[1]]  # add list  # line 783
        elif options[1] in c[options[0]]:  # line 784
            Exit("Value already contained")  # line 784
        c[options[0]].append(options[1])  # line 785
    elif argument == "rm":  # line 786
        if len(options) < 2:  # line 787
            Exit("No key nor value specified")  # line 787
        if options[0] not in c.keys():  # line 788
            Exit("Unknown key specified: %r" % options[0])  # line 788
        if options[1] not in c[options[0]]:  # line 789
            Exit("Unknown value: %r" % options[1])  # line 789
        c[options[0]].remove(options[1])  # line 790
    else:  # Show  # line 791
        for k, v in sorted(c.items()):  # line 792
            print("%s => %r" % (k, v))  # line 792
        return  # line 793
    f, g = saveConfig(c)  # line 794
    if f is None:  # line 795
        error("Error saving user configuration: %r" % g)  # line 795

def move(relPath: 'str', pattern: 'str', newRelPath: 'str', newPattern: 'str', options: 'List[str]'=[]) -> 'None':  # line 797
    ''' Path differs: Move files, create folder if not existing. Pattern differs: Attempt to rename file, unless exists in target or not unique. '''  # line 798
    force = '--force' in options  # type: bool  # line 799
    soft = '--soft' in options  # type: bool  # line 800
    if not os.path.exists(relPath.replace(SLASH, os.sep)) and not force:  # line 801
        Exit("Source folder doesn't exist. Use --force to proceed anyway")  # line 801
    m = Metadata(os.getcwd())  # type: Metadata  # line 802
    matching = fnmatch.filter(os.listdir(relPath.replace(SLASH, os.sep)) if os.path.exists(relPath.replace(SLASH, os.sep)) else [], os.path.basename(pattern))  # type: List[str]  # find matching files in source  # line 803
    matching[:] = [f for f in matching if len([n for n in m.c.ignores if fnmatch.fnmatch(f, n)]) == 0 or len([p for p in m.c.ignoresWhitelist if fnmatch.fnmatch(f, p)]) > 0]  # line 804
    if not matching and not force:  # line 805
        Exit("No files match the specified file pattern. Use --force to proceed anyway")  # line 805
    m.loadBranches()  # knows current branch  # line 806
    if not m.track and not m.picky:  # line 807
        Exit("Repository is in simple mode. Simply use basic file operations to modify files, then execute 'sos commit' to version the changes")  # line 807
    if pattern not in m.branches[m.branch].tracked:  # line 808
        for tracked in (t for t in m.branches[m.branch].tracked if os.path.dirname(t) == relPath):  # for all patterns of the same source folder  # line 809
            alternative = fnmatch.filter(matching, os.path.basename(tracked))  # type: _coconut.typing.Sequence[str]  # find if it matches any of the files in the source folder, too  # line 810
            if alternative:  # line 811
                info("  '%s' matches %d files" % (tracked, len(alternative)))  # line 811
        if not (force or soft):  # line 812
            Exit("File pattern '%s' is not tracked on current branch. 'sos move' only works on tracked patterns" % pattern)  # line 812
    basePattern = os.path.basename(pattern)  # type: str  # pure glob without folder  # line 813
    newBasePattern = os.path.basename(newPattern)  # type: str  # line 814
    if basePattern.count("*") < newBasePattern.count("*") or (basePattern.count("?") - basePattern.count("[?]")) < (newBasePattern.count("?") - newBasePattern.count("[?]")) or (basePattern.count("[") - basePattern.count("\\[")) < (newBasePattern.count("[") - newBasePattern.count("\\[")) or (basePattern.count("]") - basePattern.count("\\]")) < (newBasePattern.count("]") - newBasePattern.count("\\]")):  # line 815
        Exit("Glob markers from '%s' to '%s' don't match, cannot move/rename tracked matching files" % (basePattern, newBasePattern))  # line 819
    oldTokens = None  # type: _coconut.typing.Sequence[GlobBlock]  # line 820
    newToken = None  # type: _coconut.typing.Sequence[GlobBlock]  # line 820
    oldTokens, newTokens = tokenizeGlobPatterns(os.path.basename(pattern), os.path.basename(newPattern))  # line 821
    matches = convertGlobFiles(matching, oldTokens, newTokens)  # type: _coconut.typing.Sequence[Tuple[str, str]]  # computes list of source - target filename pairs  # line 822
    if len({st[1] for st in matches}) != len(matches):  # line 823
        Exit("Some target filenames are not unique and different move/rename actions would point to the same target file")  # line 823
    matches = reorderRenameActions(matches, exitOnConflict=not soft)  # attempts to find conflict-free renaming order, or exits  # line 824
    if os.path.exists(newRelPath):  # line 825
        exists = [filename[1] for filename in matches if os.path.exists(os.path.join(newRelPath, filename[1]).replace(SLASH, os.sep))]  # type: _coconut.typing.Sequence[str]  # line 826
        if exists and not (force or soft):  # line 827
            Exit("%s files would write over existing files in %s cases. Use --force to execute it anyway" % ("Moving" if relPath != newRelPath else "Renaming", "all" if len(exists) == len(matches) else "some"))  # line 827
    else:  # line 828
        os.makedirs(os.path.abspath(newRelPath.replace(SLASH, os.sep)))  # line 828
    if not soft:  # perform actual renaming  # line 829
        for (source, target) in matches:  # line 830
            try:  # line 831
                shutil.move(os.path.abspath(os.path.join(relPath, source).replace(SLASH, os.sep)), os.path.abspath(os.path.join(newRelPath, target).replace(SLASH, os.sep)))  # line 831
            except Exception as E:  # one error can lead to another in case of delicate renaming order  # line 832
                error("Cannot move/rename file '%s' to '%s'" % (source, os.path.join(newRelPath, target)))  # one error can lead to another in case of delicate renaming order  # line 832
    m.branches[m.branch].tracked[m.branches[m.branch].tracked.index(pattern)] = newPattern  # line 833
    m.saveBranches()  # line 834

def parse(root: 'str', cwd: 'str'):  # line 836
    ''' Main operation. Main has already chdir into VCS root folder, cwd is original working directory for add, rm. '''  # line 837
    debug("Parsing command-line arguments...")  # line 838
    try:  # line 839
        raise Exception()  # line 840
        command = sys.argv[1].strip() if len(sys.argv) > 1 else ""  # line 841
        argument = sys.argv[2].strip() if len(sys.argv) > 2 and not sys.argv[2].startswith("--") else None  # line 842
        options = sys.argv[3:] if command == "config" else [c for c in sys.argv[2:] if c.startswith("--")]  # consider second parameter for no-arg command, otherwise from third on  # line 843
        onlys, excps = parseOnlyOptions(cwd, options)  # extracts folder-relative information for changes, commit, diff, switch, update  # line 844
        debug("Processing command %r with argument '%s' and options %r." % ("" if command is None else command, "" if argument is None else argument, options))  # line 845
        if command[:1] in "amr":  # line 846
            relPath, pattern = relativize(root, os.path.join(cwd, "." if argument is None else argument))  # line 846
        if command[:1] == "m":  # line 847
            if not options:  # line 848
                Exit("Need a second file pattern argument as target for move/rename command")  # line 848
            newRelPath, newPattern = relativize(root, os.path.join(cwd, options[0]))  # line 849
        if command[:1] == "a":  # line 850
            add(relPath, pattern, options)  # line 850
        elif command[:1] == "b":  # line 851
            branch(argument, options)  # line 851
        elif command[:2] == "ch":  # line 852
            changes(argument, options, onlys, excps)  # line 852
        elif command[:3] == "com":  # line 853
            commit(argument, options, onlys, excps)  # line 853
        elif command[:2] == "ci":  # line 854
            commit(argument, options, onlys, excps)  # line 854
        elif command[:3] == 'con':  # line 855
            config(argument, options)  # line 855
        elif command[:2] == "de":  # line 856
            delete(argument, options)  # line 856
        elif command[:2] == "di":  # line 857
            diff(argument, options, onlys, excps)  # line 857
        elif command[:1] == "h":  # line 858
            usage()  # line 858
        elif command[:2] == "lo":  # line 859
            log(options)  # line 859
        elif command[:2] == "li":  # TODO handle absolute paths as well, also for Windows  # line 860
            ls(relativize(root, cwd if argument is None else os.path.join(cwd, argument))[1], options)  # TODO handle absolute paths as well, also for Windows  # line 860
        elif command[:2] == "ls":  # TODO avoid root super paths (..)  # line 861
            ls(relativize(root, cwd if argument is None else os.path.join(cwd, argument))[1], options)  # TODO avoid root super paths (..)  # line 861
        elif command[:1] == "m":  # line 862
            move(relPath, pattern, newRelPath, newPattern, options[1:])  # line 862
        elif command[:2] == "of":  # line 863
            offline(argument, options)  # line 863
        elif command[:2] == "on":  # line 864
            online(options)  # line 864
        elif command[:1] == "r":  # line 865
            remove(relPath, pattern)  # line 865
        elif command[:2] == "st":  # line 866
            status()  # line 866
        elif command[:2] == "sw":  # line 867
            switch(argument, options, onlys, excps)  # line 867
        elif command[:1] == "u":  # line 868
            update(argument, options, onlys, excps)  # line 868
        else:  # line 869
            Exit("Unknown command '%s'" % command)  # line 869
    except (Exception, RuntimeError) as E:  # line 870
        import traceback  # line 871
        traceback.print_stack()  # line 872
        print("An internal error occurred in SOS. Please report above message to the project maintainer at  https://github.com/ArneBachmann/sos/issues  via 'New Issue'.\nPlease state your installed version ('sos version'), and what you were doing.")  # line 873
    sys.exit(0)  # line 874

def main() -> 'None':  # line 876
    global debug, info, warn, error  # line 877
    logging.basicConfig(level=level, stream=sys.stderr, format=("%(asctime)-23s %(levelname)-8s %(name)s:%(lineno)d | %(message)s" if '--log' in sys.argv else "%(message)s"))  # line 878
    _log = Logger(logging.getLogger(__name__))  # line 879
    debug, info, warn, error = _log.debug, _log.info, _log.warn, _log.error  # line 879
    for option in (o for o in ['--log', '--verbose', '-v', '--sos'] if o in sys.argv):  # clean up program arguments  # line 880
        sys.argv.remove(option)  # clean up program arguments  # line 880
    if '--help' in sys.argv or len(sys.argv) < 2:  # line 881
        usage()  # line 881
        Exit()  # line 881
    command = sys.argv[1] if len(sys.argv) > 1 else None  # type: _coconut.typing.Optional[str]  # line 882
    root, vcs, cmd = findSosVcsBase()  # root is None if no .sos folder exists up the folder tree (still working online); vcs is checkout/repo root folder; cmd is the VCS base command  # line 883
    debug("Found root folders for SOS|VCS: %s|%s" % ("" if root is None else root, "" if vcs is None else vcs))  # line 884
    defaults["defaultbranch"] = vcsBranches.get(cmd, "trunk")  # sets dynamic default with SVN fallback  # line 885
    if force_sos or root is not None or ("" if command is None else command)[:2] == "of" or ("" if command is None else command)[:1] == "h":  # in offline mode or just going offline TODO what about git config?  # line 886
        cwd = os.getcwd()  # line 887
        os.chdir(cwd if command[:2] == "of" else cwd if root is None else root)  # line 888
        parse(root, cwd)  # line 889
    elif cmd is not None:  # online mode - delegate to VCS  # line 890
        info("SOS: Running '%s %s'" % (cmd, " ".join(sys.argv[1:])))  # line 891
        import subprocess  # only required in this section  # line 892
        process = subprocess.Popen([cmd] + sys.argv[1:], shell=False, stdin=subprocess.PIPE, stdout=sys.stdout, stderr=sys.stderr)  # line 893
        inp = ""  # type: str  # line 894
        while True:  # line 895
            so, se = process.communicate(input=inp)  # line 896
            if process.returncode is not None:  # line 897
                break  # line 897
            inp = sys.stdin.read()  # line 898
        if sys.argv[1][:2] == "co" and process.returncode == 0:  # successful commit - assume now in sync again (but leave meta data folder with potential other feature branches behind until "online")  # line 899
            if root is None:  # line 900
                Exit("Cannot determine VCS root folder: Unable to mark repository as synchronized and will show a warning when leaving offline mode")  # line 900
            m = Metadata(root)  # line 901
            m.loadBranches()  # read repo  # line 902
            m.branches[m.branch] = dataCopy(BranchInfo, m.branches[m.branch], inSync=True)  # mark as committed  # line 903
            m.saveBranches()  # line 904
    else:  # line 905
        Exit("No offline repository present, and unable to detect VCS file tree")  # line 905


# Main part
level = logging.DEBUG if os.environ.get("DEBUG", "False").lower() == "true" or '--verbose' in sys.argv or '-v' in sys.argv else logging.INFO  # line 909
force_sos = '--sos' in sys.argv  # line 910
_log = Logger(logging.getLogger(__name__))  # line 911
debug, info, warn, error = _log.debug, _log.info, _log.warn, _log.error  # line 911
if __name__ == '__main__':  # line 912
    main()  # line 912
