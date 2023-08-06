#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# __coconut_hash__ = 0xb02ccd12

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
import time  # line 6
START_TIME = time.time()  # line 6
import codecs  # line 7
import collections  # line 7
import fnmatch  # line 7
import json  # line 7
import logging  # line 7
import mimetypes  # line 7
import os  # line 7
import shutil  # line 7
sys = _coconut_sys  # line 7
try:  # line 8
    from typing import Any  # only required for mypy  # line 9
    from typing import Dict  # only required for mypy  # line 9
    from typing import FrozenSet  # only required for mypy  # line 9
    from typing import IO  # only required for mypy  # line 9
    from typing import Iterator  # only required for mypy  # line 9
    from typing import List  # only required for mypy  # line 9
    from typing import Set  # only required for mypy  # line 9
    from typing import Tuple  # only required for mypy  # line 9
    from typing import Type  # only required for mypy  # line 9
    from typing import Union  # only required for mypy  # line 9
except:  # typing not available (e.g. Python 2)  # line 10
    pass  # typing not available (e.g. Python 2)  # line 10
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))  # line 11
try:  # line 12
    from sos import version  # line 13
    from sos.utility import *  # line 14
except:  # line 15
    import version  # line 16
    from utility import *  # line 17

# External dependencies
try:  # optional dependency  # line 20
    import configr  # optional dependency  # line 20
except:  # declare as undefined  # line 21
    configr = None  # declare as undefined  # line 21
#from enforce import runtime_validation  # https://github.com/RussBaz/enforce  TODO doesn't work for "data" types


# Constants
APPNAME = "Subversion Offline Solution  V%s  (C) Arne Bachmann" % version.__release_version__  # type: str  # line 26
defaults = Accessor({"strict": False, "track": False, "picky": False, "compress": False, "tags": [], "texttype": [], "bintype": [], "ignoreDirs": [".*", "__pycache__"], "ignoreDirsWhitelist": [], "ignores": ["__coconut__.py", "*.bak", "*.py[cdo]", "*.class", ".fslckout"], "ignoresWhitelist": []})  # line 27
termWidth = getTermWidth() - 1  # uses curses or returns conservative default of 80  # line 28


# Functions
def loadConfig() -> 'Union[configr.Configr, Accessor]':  # Simplifies loading config from file system or returning the defaults  # line 32
    config = None  # type: Union[configr.Configr, Accessor]  # line 33
    if not configr:  # this only applies for the case that configr is not available, thus no settings will be persisted anyway  # line 34
        return defaults  # this only applies for the case that configr is not available, thus no settings will be persisted anyway  # line 34
    config = configr.Configr("sos", defaults=defaults)  # defaults are used if key is not configured, but won't be saved  # line 35
    f, g = config.loadSettings(clientCodeLocation=os.path.abspath(__file__), location=os.environ.get("TEST", None))  # line 36
    if f is None:  # line 37
        debug("Encountered a problem while loading the user configuration: %r" % g)  # line 37
    return config  # line 38

@_coconut_tco  # line 40
def saveConfig(config: 'configr.Configr') -> 'Tuple[_coconut.typing.Optional[str], _coconut.typing.Optional[Exception]]':  # line 40
    return _coconut_tail_call(config.saveSettings, clientCodeLocation=os.path.abspath(__file__), location=os.environ.get("TEST", None))  # line 41

def usage(short: 'bool'=False) -> 'None':  # line 43
    print("//|\\\\ {appname} {version} //|\\\\".format(appname=APPNAME, version="" if not short else "(PyPI: %s)" % version.__version__))  # line 44
    if not short:  # line 45
        print("""

Usage: {cmd} <command> [<argument>] [<option1>, ...]        When operating in offline mode, or command is one of "help", "offline", "version"
       {cmd} --sos <sos command and arguments>              When operating in offline mode, forced passthrough to SOS
       {cmd} --vcs <underlying vcs command and arguments>   When operating in offline mode, forced passthrough to traditional VCS
       {cmd} <underlying vcs command and arguments>         When operating in online mode, automatic passthrough to traditional VCS

  Available commands:
    offline [<name>]                                      Start working offline, creating a branch (named <name>), default name depending on VCS
      --compress                                            Compress versioned files (same as `sos config set compress on && sos offline`)
      --track                                               Setup SVN-style mode: users add/remove tracking patterns per branch
      --picky                                               Setup Git-style mode: users pick files for each operation
    online                                                Finish working offline

    branch [<name>]                                       Create a new branch from current file tree and switch to it
      --last                                                Use last revision, not current file tree, but keep file tree unchanged
      --stay                                                Don't switch to new branch, continue on current one
    switch [<branch>][/<revision>]                        Continue work on another branch
      --meta                                                Only switch file tracking patterns for current branch, don't update any files
    update [<branch>][/<revision>]                        Integrate work from another branch  TODO add many merge and conflict resolution options
    destroy [<branch>]                                    Remove (current) branch entirely

    commit [<message>]                                    Create a new revision from current state file tree, with an optional commit message
      --tag                                               Converts commit message into a tag that can be used instead of numeric revisions
    changes [<branch>][/<revision>]                       List changed paths vs. last or specified revision
    diff [<branch>][/<revision>]                          List changes in file tree (or `--from` specified revision) vs. last (or specified) revision
      --from=branch/revision                                Take from revision as base to compare against (instead of current file tree)
    add <file pattern>                                    Add a tracking pattern to current branch (file pattern)
    mv <oldpattern> <newPattern>                          Rename, move, or move and rename tracked files according to tracked file patterns
      --soft                                                Don't move or rename files, only the tracking pattern
    rm <file pattern>                                     Remove a tracking pattern. Only useful after "offline --track" or "offline --picky"

    ls [<folder path>] [--patterns]                       List file tree and mark changes and tracking status
    status                                                List branches and display repository status
    log                                                   List commits of current branch
      --changes                                             Also list file differences
    config [set/unset/show/add/rm] [<param> [<value>]]    Configure user-global defaults.
                                                          Flags (1/0, on/off, true/false, yes/no):
                                                            strict, track, picky, compress
                                                          Lists (semicolon-separated when set; single values for add/rm):
                                                            texttype, bintype, ignores, ignoreDirs, ignoresWhitelist, ignoreDirsWhitelist
                                                          Supported texts:
                                                            defaultbranch (has a dynamic default value, depending on VCS discovered)
    help, --help                                          Show this usage information

  Arguments:
    <branch>/<revision>          Revision string. Branch is optional (defaulting to current branch) and may be label or number
                                 Revision is an optional integer and may be negative to reference from the latest commits (-1 is most recent revision), or a tag

  Common options:
    --force                      Executes potentially harmful operations. SOS will tell you, when it needs you to confirm an operation with "--force"
                                   for offline: ignore being already offline, start from scratch (same as 'sos online --force && sos offline')
                                   for online: ignore uncommitted branches, just go online and remove existing offline repository
                                   for commit, switch, update, add: ignore uncommitted changes before executing command
    --strict                     Always perform full content comparison, don't rely only on file size and timestamp
                                   for offline command: memorize strict mode setting in repository
                                   for changes, diff, commit, switch, update, delete: perform operation in strict mode, regardless of repository setting
    --only   <tracked pattern>   Restrict operation to specified pattern(s). Available for "changes", "commit", "diff", "switch", and "update"
    --except <tracked pattern>   Avoid operation for specified pattern(s). Available for "changes", "commit", "diff", "switch", and "update"
    --{cmd}                      When executing {CMD} not being offline, pass arguments to {CMD} instead (e.g. {cmd} --{cmd} config set key value.)
    --log                        Enable logging details
    --verbose                    Enable verbose output""".format(appname=APPNAME, cmd="sos", CMD="SOS"))  # line 106
    Exit(code=0)  # line 107

# Main data class
#@runtime_validation
class Metadata:  # line 111
    ''' This class doesn't represent the entire repository state in memory,
      but serves as a container for different repo operations,
      using only parts of its attributes at any point in time. Use with care.
  '''  # line 115

    def __init__(_, path: 'str') -> 'None':  # line 117
        ''' Create empty container object for various repository operations. '''  # line 118
        _.c = loadConfig()  # line 119
        _.root = path  # type: str  # line 120
        _.branches = {}  # type: Dict[int, BranchInfo]  # branch number zero represents the initial state at branching  # line 121
        _.commits = {}  # type: Dict[int, CommitInfo]  # consecutive numbers per branch, starting at 0  # line 122
        _.paths = {}  # type: Dict[str, PathInfo]  # utf-8 encoded relative, normalized file system paths  # line 123
        _.tags = []  # type: List[str]  # line 124
        _.branch = None  # type: _coconut.typing.Optional[int]  # current branch number  # line 125
        _.commit = None  # type: _coconut.typing.Optional[int]  # current revision number  # line 126
        _.track = _.c.track  # type: bool  # track file name patterns in the repository (per branch)  # line 127
        _.picky = _.c.picky  # type: bool  # pick files to commit per operation  # line 128
        _.strict = _.c.strict  # type: bool  # be always strict (regarding file contents comparsion)  # line 129
        _.compress = _.c.compress  # type: bool  # these flags are stored in the repository  # line 130

    def isTextType(_, filename: 'str') -> 'bool':  # line 132
        return (((lambda _coconut_none_coalesce_item: "" if _coconut_none_coalesce_item is None else _coconut_none_coalesce_item)(mimetypes.guess_type(filename)[0])).startswith("text/") or any([fnmatch.fnmatch(filename, pattern) for pattern in _.c.texttype])) and not any([fnmatch.fnmatch(filename, pattern) for pattern in _.c.bintype])  # line 132

    def listChanges(_, changes: 'ChangeSet') -> 'None':  # line 134
        if len(changes.additions) > 0:  # line 135
            print(ajoin("ADD ", sorted(changes.additions.keys()), "\n"))  # line 135
        if len(changes.deletions) > 0:  # line 136
            print(ajoin("DEL ", sorted(changes.deletions.keys()), "\n"))  # line 136
        if len(changes.modifications) > 0:  # line 137
            print(ajoin("MOD ", sorted(changes.modifications.keys()), "\n"))  # line 137

    def loadBranches(_) -> 'None':  # line 139
        ''' Load list of branches and current branch info from metadata file. '''  # line 140
        try:  # fails if not yet created (on initial branch/commit)  # line 141
            branches = None  # type: List[Tuple]  # line 142
            with codecs.open(os.path.join(_.root, metaFolder, metaFile), "r", encoding=UTF8) as fd:  # line 143
                flags, branches = json.load(fd)  # line 144
            _.tags = flags["tags"]  # list of commit messages to treat as globally unique tags  # line 145
            _.branch = flags["branch"]  # current branch integer  # line 146
            _.track = flags["track"]  # line 147
            _.picky = flags["picky"]  # line 148
            _.strict = flags["strict"]  # line 149
            _.compress = flags["compress"]  # line 150
            _.branches = {i.number: i for i in (BranchInfo(*item) for item in branches)}  # re-create type info  # line 151
        except Exception as E:  # if not found, create metadata folder  # line 152
            _.branches = {}  # line 153
            warn("Couldn't read branches metadata: %r" % E)  # line 154

    def saveBranches(_) -> 'None':  # line 156
        ''' Save list of branches and current branch info to metadata file. '''  # line 157
        with codecs.open(os.path.join(_.root, metaFolder, metaFile), "w", encoding=UTF8) as fd:  # line 158
            json.dump(({"tags": _.tags, "branch": _.branch, "track": _.track, "picky": _.picky, "strict": _.strict, "compress": _.compress}, list(_.branches.values())), fd, ensure_ascii=False)  # line 159

    def getRevisionByName(_, name: 'str') -> '_coconut.typing.Optional[int]':  # line 161
        ''' Convenience accessor for named revisions (using commit message as name). '''  # line 162
        if name == "":  # line 163
            return -1  # line 163
        try:  # attempt to parse integer string  # line 164
            return longint(name)  # attempt to parse integer string  # line 164
        except ValueError:  # line 165
            pass  # line 165
        found = [number for number, commit in _.commits.items() if name == commit.message]  # line 166
        return found[0] if found else None  # line 167

    def getBranchByName(_, name: 'str') -> '_coconut.typing.Optional[int]':  # line 169
        ''' Convenience accessor for named branches. '''  # line 170
        if name == "":  # line 171
            return _.branch  # line 171
        try:  # attempt to parse integer string  # line 172
            return longint(name)  # attempt to parse integer string  # line 172
        except ValueError:  # line 173
            pass  # line 173
        found = [number for number, branch in _.branches.items() if name == branch.name]  # line 174
        return found[0] if found else None  # line 175

    def loadBranch(_, branch: 'int') -> 'None':  # line 177
        ''' Load all commit information from a branch meta data file. '''  # line 178
        with codecs.open(os.path.join(_.root, metaFolder, "b%d" % branch, metaFile), "r", encoding=UTF8) as fd:  # line 179
            commits = json.load(fd)  # type: List[List[Any]]  # list of CommitInfo that needs to be unmarshalled into value types  # line 180
        _.commits = {i.number: i for i in (CommitInfo(*item) for item in commits)}  # re-create type info  # line 181
        _.branch = branch  # line 182

    def saveBranch(_, branch: 'int') -> 'None':  # line 184
        ''' Save all commit information to a branch meta data file. '''  # line 185
        with codecs.open(os.path.join(_.root, metaFolder, "b%d" % branch, metaFile), "w", encoding=UTF8) as fd:  # line 186
            json.dump(list(_.commits.values()), fd, ensure_ascii=False)  # line 187

    def duplicateBranch(_, branch: 'int', name: '_coconut.typing.Optional[str]') -> 'None':  # line 189
        ''' Create branch from an existing branch/revision. WARN: Caller must have loaded branches information.
        branch: target branch (should not exist yet)
        name: optional name of new branch
        _.branch: current branch
    '''  # line 194
        debug("Duplicating branch '%s' to '%s'..." % ((lambda _coconut_none_coalesce_item: ("b%d" % _.branch) if _coconut_none_coalesce_item is None else _coconut_none_coalesce_item)(_.branches[_.branch].name), ("b%d" % branch if name is None else name)))  # line 195
        tracked = [t for t in _.branches[_.branch].tracked]  # copy  # line 196
        os.makedirs(os.path.join(_.root, metaFolder, "b%d" % branch, "r0"))  # line 197
        _.loadBranch(_.branch)  # line 198
        revision = max(_.commits)  # type: int  # line 199
        _.computeSequentialPathSet(_.branch, revision)  # full set of files in revision to _.paths  # line 200
        for path, pinfo in _.paths.items():  # line 201
            _.copyVersionedFile(_.branch, revision, branch, 0, pinfo)  # line 202
        _.commits = {0: CommitInfo(0, longint(time.time() * 1000), "Branched from '%s'" % ((lambda _coconut_none_coalesce_item: "b%d" % _.branch if _coconut_none_coalesce_item is None else _coconut_none_coalesce_item)(_.branches[_.branch].name)))}  # store initial commit  # line 203
        _.saveBranch(branch)  # save branch meta data to branch folder  # line 204
        _.saveCommit(branch, 0)  # save commit meta data to revision folder  # line 205
        _.branches[branch] = BranchInfo(branch, _.commits[0].ctime, name, _.branches[_.branch].inSync, tracked)  # save branch info, before storing repo state at caller  # line 206

    def createBranch(_, branch: 'int', name: '_coconut.typing.Optional[str]'=None, initialMessage: '_coconut.typing.Optional[str]'=None):  # line 208
        ''' Create a new branch from current file tree. This clears all known commits and modifies the file system.
        branch: target branch (should not exist yet)
        name: optional name of new branch
        _.branch: current branch, must exist already
    '''  # line 213
        simpleMode = not (_.track or _.picky)  # line 214
        tracked = [t for t in _.branches[_.branch].tracked] if _.track and len(_.branches) > 0 else []  # in case of initial branch creation  # line 215
        debug((lambda _coconut_none_coalesce_item: "b%d" % branch if _coconut_none_coalesce_item is None else _coconut_none_coalesce_item)("Creating branch '%s'..." % name))  # line 216
        _.paths = {}  # type: Dict[str, PathInfo]  # line 217
        if simpleMode:  # branches from file system state  # line 218
            changes = _.findChanges(branch, 0, progress=simpleMode)  # type: ChangeSet  # creates revision folder and versioned files  # line 219
            _.listChanges(changes)  # line 220
            _.paths.update(changes.additions.items())  # line 221
        else:  # tracking or picky mode: branch from lastest revision  # line 222
            os.makedirs(os.path.join(_.root, metaFolder, "b%d" % branch, "r0"))  # line 223
            if _.branch is not None:  # not immediately after "offline" - copy files from current branch  # line 224
                _.loadBranch(_.branch)  # line 225
                revision = max(_.commits)  # type: int  # TODO what if last switch was to an earlier revision? no persisting of last checkout  # line 226
                _.computeSequentialPathSet(_.branch, revision)  # full set of files in revision to _.paths  # line 227
                for path, pinfo in _.paths.items():  # line 228
                    _.copyVersionedFile(_.branch, revision, branch, 0, pinfo)  # line 229
        ts = longint(time.time() * 1000)  # line 230
        _.commits = {0: CommitInfo(0, ts, "Branched on %s" % strftime(ts) if initialMessage is None else initialMessage)}  # store initial commit for new branch  # line 231
        _.saveBranch(branch)  # save branch meta data (revisions) to branch folder  # line 232
        _.saveCommit(branch, 0)  # save commit meta data to revision folder  # line 233
        _.branches[branch] = BranchInfo(branch, _.commits[0].ctime, name, True if len(_.branches) == 0 else _.branches[_.branch].inSync, tracked)  # save branch info, in case it is needed  # line 234

    def removeBranch(_, branch: 'int') -> 'BranchInfo':  # line 236
        ''' Entirely remove a branch and all its revisions from the file system. '''  # line 237
        shutil.rmtree(os.path.join(_.root, metaFolder, "b%d" % branch))  # line 238
        binfo = _.branches[branch]  # line 239
        del _.branches[branch]  # line 240
        _.branch = max(_.branches)  # line 241
        _.saveBranches()  # line 242
        _.commits.clear()  # line 243
        return binfo  # line 244

    def loadCommit(_, branch: 'int', revision: 'int') -> 'None':  # line 246
        ''' Load all file information from a commit meta data. '''  # line 247
        with codecs.open(os.path.join(_.root, metaFolder, "b%d" % branch, "r%d" % revision, metaFile), "r", encoding=UTF8) as fd:  # line 248
            _.paths = json.load(fd)  # line 249
        _.paths = {path: PathInfo(*item) for path, item in _.paths.items()}  # re-create type info  # line 250
        _.branch = branch  # line 251

    def saveCommit(_, branch: 'int', revision: 'int'):  # line 253
        ''' Save all file information to a commit meta data file. '''  # line 254
        target = os.path.join(_.root, metaFolder, "b%d" % branch, "r%d" % revision)  # line 255
        try:  # line 256
            os.makedirs(target)  # line 256
        except:  # line 257
            pass  # line 257
        with codecs.open(os.path.join(target, metaFile), "w", encoding=UTF8) as fd:  # line 258
            json.dump(_.paths, fd, ensure_ascii=False)  # line 259

    def findChanges(_, branch: '_coconut.typing.Optional[int]'=None, revision: '_coconut.typing.Optional[int]'=None, checkContent: 'bool'=False, inverse: 'bool'=False, considerOnly: '_coconut.typing.Optional[FrozenSet[str]]'=None, dontConsider: '_coconut.typing.Optional[FrozenSet[str]]'=None, progress: 'bool'=False) -> 'ChangeSet':  # line 261
        ''' Find changes on the file system vs. in-memory paths (which should reflect the latest commit state).
        Only if both branch and revision are *not* None, write modified/added files to the specified revision folder (thus creating a new revision)
        The function returns the state of file tree *differences*, unless "inverse" is True -> then return original data
        checkContent: also computes file content hashes
        inverse: retain original state (size, mtime, hash) instead of updated one
        considerOnly: set of tracking patterns. None for simple mode. For update operation, consider union of other and current branch
        dontConsider: set of tracking patterns to not consider in changes
        progress: Show file names during processing
    '''  # line 270
        write = branch is not None and revision is not None  # line 271
        if write:  # line 272
            os.makedirs(os.path.join(_.root, metaFolder, "b%d" % branch, "r%d" % revision))  # line 272
        changes = ChangeSet({}, {}, {})  # type: ChangeSet  # line 273
        counter = Counter(-1)  # type: Counter  # line 274
        timer = time.time()  # line 274
        hashed = None  # type: _coconut.typing.Optional[str]  # line 275
        written = None  # type: longint  # line 275
        compressed = 0  # type: longint  # line 275
        original = 0  # type: longint  # line 275
        knownPaths = collections.defaultdict(list)  # type: Dict[str, List[str]]  # line 276
        for path, pinfo in _.paths.items():  # line 277
            if pinfo.size is not None and (considerOnly is None or any((path[:path.rindex(SLASH)] == pattern[:pattern.rindex(SLASH)] and fnmatch.fnmatch(path[path.rindex(SLASH) + 1:], pattern[pattern.rindex(SLASH) + 1:]) for pattern in considerOnly))) and (dontConsider is None or not any((path[:path.rindex(SLASH)] == pattern[:pattern.rindex(SLASH)] and fnmatch.fnmatch(path[path.rindex(SLASH) + 1:], pattern[pattern.rindex(SLASH) + 1:]) for pattern in dontConsider))):  # line 278
                knownPaths[os.path.dirname(path)].append(os.path.basename(path))  # TODO reimplement using fnmatch.filter and set operations for all files per path for speed  # line 281
        for path, dirnames, filenames in os.walk(_.root):  # line 282
            dirnames[:] = [f for f in dirnames if len([n for n in _.c.ignoreDirs if fnmatch.fnmatch(f, n)]) == 0 or len([p for p in _.c.ignoreDirsWhitelist if fnmatch.fnmatch(f, p)]) > 0]  # line 283
            filenames[:] = [f for f in filenames if len([n for n in _.c.ignores if fnmatch.fnmatch(f, n)]) == 0 or len([p for p in _.c.ignoresWhitelist if fnmatch.fnmatch(f, p)]) > 0]  # line 284
            dirnames.sort()  # line 285
            filenames.sort()  # line 285
            relPath = os.path.relpath(path, _.root).replace(os.sep, SLASH)  # line 286
            walk = filenames if considerOnly is None else list(reduce(lambda last, pattern: last | set(fnmatch.filter(filenames, os.path.basename(pattern))), (p for p in considerOnly if os.path.dirname(p).replace(os.sep, SLASH) == relPath), _coconut.set()))  # line 287
            if dontConsider:  # line 288
                walk[:] = [fn for fn in walk if not any((fnmatch.fnmatch(fn, os.path.basename(p)) for p in dontConsider if os.path.dirname(p).replace(os.sep, SLASH) == relPath))]  # line 289
            for file in walk:  # if m.track or m.picky: only files that match any path-relevant tracking patterns  # line 290
                filename = relPath + SLASH + file  # line 291
                filepath = os.path.join(path, file)  # line 292
                stat = os.stat(filepath)  # line 293
                size, mtime, newtime = stat.st_size, longint(stat.st_mtime * 1000), time.time()  # line 294
                if progress and newtime - timer > .1:  # line 295
                    outstring = "\rPreparing %s  %s" % (PROGRESS_MARKER[counter.inc() % 4], filename)  # line 296
                    sys.stdout.write(outstring + " " * max(0, termWidth - len(outstring)))  # TODO could write to new line instead of carriage return (still true?)  # line 297
                    sys.stdout.flush()  # TODO could write to new line instead of carriage return (still true?)  # line 297
                    timer = newtime  # TODO could write to new line instead of carriage return (still true?)  # line 297
                if filename not in _.paths:  # detected file not present (or untracked) in (other) branch  # line 298
                    nameHash = hashStr(filename)  # line 299
                    hashed, written = hashFile(filepath, _.compress, saveTo=os.path.join(_.root, metaFolder, "b%d" % branch, "r%d" % revision, nameHash) if write else None) if size > 0 else (None, 0)  # line 300
                    changes.additions[filename] = PathInfo(nameHash, size, mtime, hashed)  # line 301
                    compressed += written  # line 302
                    original += size  # line 302
                    continue  # line 303
                last = _.paths[filename]  # filename is known - check for modifications  # line 304
                if last.size is None:  # was removed before but is now added back - does not apply for tracking mode (which never marks files for removal in the history)  # line 305
                    hashed, written = hashFile(filepath, _.compress, saveTo=os.path.join(_.root, metaFolder, "b%d" % branch, "r%d" % revision, last.nameHash) if write else None) if size > 0 else (None, 0)  # line 306
                    changes.additions[filename] = PathInfo(last.nameHash, size, mtime, hashed)  # line 307
                    continue  # line 307
                elif size != last.size or mtime != last.mtime or (checkContent and hashFile(filepath, _.compress)[0] != last.hash):  # detected a modification  # line 308
                    hashed, written = hashFile(filepath, _.compress, saveTo=os.path.join(_.root, metaFolder, "b%d" % branch, "r%d" % revision, last.nameHash) if write else None) if (last.size if inverse else size) > 0 else (last.hash if inverse else None, 0)  # line 309
                    changes.modifications[filename] = PathInfo(last.nameHash, last.size if inverse else size, last.mtime if inverse else mtime, hashed)  # line 310
                else:  # line 311
                    continue  # line 311
                compressed += written  # line 312
                original += last.size if inverse else size  # line 312
            if relPath in knownPaths:  # at least one file is tracked  # line 313
                knownPaths[relPath][:] = list(set(knownPaths[relPath]) - set(walk))  # at least one file is tracked  # line 313
        for path, names in knownPaths.items():  # all paths that weren't walked by  # line 314
            for file in names:  # line 315
                changes.deletions[path + SLASH + file] = _.paths[path + SLASH + file]  # line 315
        if progress:  # force new line  # line 316
            print("\rPreparation finished. Compression factor %s" % ("is %.1f" % (original * 100. / compressed) if compressed > 0 else "cannot be computed").ljust(termWidth), file=sys.stdout)  # force new line  # line 316
        else:  # line 317
            debug("Finished detecting changes. Compression factor %s" % ("is %.1f" % (original * 100. / compressed) if compressed > 0 else "cannot be computed"))  # line 317
        return changes  # line 318

    def integrateChangeset(_, changes: 'ChangeSet', clear=False) -> 'None':  # line 320
        ''' In-memory update from a changeset, marking deleted files with size=None. Use clear = True to start on an empty path set. '''  # line 321
        if clear:  # line 322
            _.paths.clear()  # line 322
        else:  # line 323
            rm = [p for p, info in _.paths.items() if info.size is None]  # remove files deleted in earlier change sets (revisions)  # line 324
            for old in rm:  # remove previously removed entries completely  # line 325
                del _.paths[old]  # remove previously removed entries completely  # line 325
        for d, info in changes.deletions.items():  # mark now removed entries as deleted  # line 326
            _.paths[d] = PathInfo(info.nameHash, None, info.mtime, None)  # mark now removed entries as deleted  # line 326
        _.paths.update(changes.additions)  # line 327
        _.paths.update(changes.modifications)  # line 328

    def computeSequentialPathSet(_, branch: 'int', revision: 'int') -> 'None':  # line 330
        next(_.computeSequentialPathSetIterator(branch, revision, incrementally=False))  # simply invoke the generator once  # line 331

    def computeSequentialPathSetIterator(_, branch: 'int', revision: 'int', incrementally: 'bool'=True) -> '_coconut.typing.Optional[Iterator[ChangeSet]]':  # line 333
        ''' In-memory computation of current list of valid PathInfo entries for specified branch and until specified revision (inclusively) by traversing revision on the file system. '''  # line 334
        _.loadCommit(branch, 0)  # load initial paths  # line 335
        if incrementally:  # line 336
            yield diffPathSets({}, _.paths)  # line 336
        n = Metadata(_.root)  # type: Metadata  # next changes  # line 337
        for revision in range(1, revision + 1):  # line 338
            n.loadCommit(branch, revision)  # line 339
            changes = diffPathSets(_.paths, n.paths)  # type: ChangeSet  # line 340
            _.integrateChangeset(changes)  # line 341
            if incrementally:  # line 342
                yield changes  # line 342
        yield None  # for the default case - not incrementally  # line 343

    def parseRevisionString(_, argument: 'str') -> 'Tuple[_coconut.typing.Optional[int], _coconut.typing.Optional[int]]':  # line 345
        ''' Commit identifiers can be str or int for branch, and int for revision.
        Revision identifiers can be negative, with -1 being last commit.
    '''  # line 348
        if argument is None or argument == SLASH:  # no branch/revision specified  # line 349
            return (_.branch, -1)  # no branch/revision specified  # line 349
        argument = argument.strip()  # line 350
        if argument.startswith(SLASH):  # current branch  # line 351
            return (_.branch, _.getRevisionByName(argument[1:]))  # current branch  # line 351
        if argument.endswith(SLASH):  # line 352
            try:  # line 353
                return (_.getBranchByName(argument[:-1]), -1)  # line 353
            except ValueError:  # line 354
                Exit("Unknown branch label '%s'" % argument)  # line 354
        if SLASH in argument:  # line 355
            b, r = argument.split(SLASH)[:2]  # line 356
            try:  # line 357
                return (_.getBranchByName(b), _.getRevisionByName(r))  # line 357
            except ValueError:  # line 358
                Exit("Unknown branch label or wrong number format '%s/%s'" % (b, r))  # line 358
        branch = _.getBranchByName(argument)  # type: int  # returns number if given (revision) integer  # line 359
        if branch not in _.branches:  # line 360
            branch = None  # line 360
        try:  # either branch name/number or reverse/absolute revision number  # line 361
            return (_.branch if branch is None else branch, longint(argument if argument else "-1") if branch is None else -1)  # either branch name/number or reverse/absolute revision number  # line 361
        except:  # line 362
            Exit("Unknown branch label or wrong number format")  # line 362
        Exit("This should never happen")  # line 363
        return (None, None)  # line 363

    def findRevision(_, branch: 'int', revision: 'int', nameHash: 'str') -> 'Tuple[int, str]':  # line 365
        while True:  # find latest revision that contained the file physically  # line 366
            source = os.path.join(_.root, metaFolder, "b%d" % branch, "r%d" % revision, nameHash)  # type: str  # line 367
            if os.path.exists(source) and os.path.isfile(source):  # line 368
                break  # line 368
            revision -= 1  # line 369
            if revision < 0:  # line 370
                Exit("Cannot determine versioned file '%s' from specified branch '%d'" % (nameHash, branch))  # line 370
        return revision, source  # line 371

    def copyVersionedFile(_, branch: 'int', revision: 'int', toBranch: 'int', toRevision: 'int', pinfo: 'PathInfo') -> 'None':  # line 373
        ''' Copy versioned file to other branch/revision. '''  # line 374
        target = os.path.join(_.root, metaFolder, "b%d" % toBranch, "r%d" % toRevision, pinfo.nameHash)  # type: str  # line 375
        revision, source = _.findRevision(branch, revision, pinfo.nameHash)  # line 376
        shutil.copy2(source, target)  # line 377

    def readOrCopyVersionedFile(_, branch: 'int', revision: 'int', nameHash: 'str', toFile: '_coconut.typing.Optional[str]'=None) -> '_coconut.typing.Optional[bytes]':  # line 379
        ''' Return file contents, or copy contents into file path provided. '''  # line 380
        source = os.path.join(_.root, metaFolder, "b%d" % branch, "r%d" % revision, nameHash)  # type: str  # line 381
        try:  # line 382
            with openIt(source, "r", _.compress) as fd:  # line 383
                if toFile is None:  # read bytes into memory and return  # line 384
                    return fd.read()  # read bytes into memory and return  # line 384
                with open(toFile, "wb") as to:  # line 385
                    while True:  # line 386
                        buffer = fd.read(bufSize)  # line 387
                        to.write(buffer)  # line 388
                        if len(buffer) < bufSize:  # line 389
                            break  # line 389
                    return None  # line 390
        except Exception as E:  # line 391
            warn("Cannot read versioned file: %r (%d/%d/%s)" % (E, branch, revision, nameHash))  # line 391
        return None  # line 392

    def restoreFile(_, relPath: '_coconut.typing.Optional[str]', branch: 'int', revision: 'int', pinfo: 'PathInfo', ensurePath: 'bool'=False) -> '_coconut.typing.Optional[bytes]':  # line 394
        ''' Recreate file for given revision, or return contents if path is None. '''  # line 395
        if relPath is None:  # just return contents  # line 396
            return _.readOrCopyVersionedFile(branch, _.findRevision(branch, revision, pinfo.nameHash)[0], pinfo.nameHash) if pinfo.size > 0 else b''  # just return contents  # line 396
        target = os.path.join(_.root, relPath.replace(SLASH, os.sep))  # type: str  # line 397
        if ensurePath:  #  and not os.path.exists(os.path.dirname(target)):  # line 398
            try:  # line 399
                os.makedirs(os.path.dirname(target))  # line 399
            except:  # line 400
                pass  # line 400
        if pinfo.size == 0:  # line 401
            with open(target, "wb"):  # line 402
                pass  # line 402
            try:  # update access/modification timestamps on file system  # line 403
                os.utime(target, (pinfo.mtime / 1000., pinfo.mtime / 1000.))  # update access/modification timestamps on file system  # line 403
            except Exception as E:  # line 404
                error("Cannot update file's timestamp after restoration '%r'" % E)  # line 404
            return None  # line 405
        revision, source = _.findRevision(branch, revision, pinfo.nameHash)  # line 406
# Restore file by copying buffer-wise
        with openIt(source, "r", _.compress) as fd, open(target, "wb") as to:  # using Coconut's Enhanced Parenthetical Continuation  # line 408
            while True:  # line 409
                buffer = fd.read(bufSize)  # line 410
                to.write(buffer)  # line 411
                if len(buffer) < bufSize:  # line 412
                    break  # line 412
        try:  # update access/modification timestamps on file system  # line 413
            os.utime(target, (pinfo.mtime / 1000., pinfo.mtime / 1000.))  # update access/modification timestamps on file system  # line 413
        except Exception as E:  # line 414
            error("Cannot update file's timestamp after restoration '%r'" % E)  # line 414
        return None  # line 415

    def getTrackingPatterns(_, branch: '_coconut.typing.Optional[int]'=None) -> 'FrozenSet[str]':  # line 417
        ''' Returns list of tracking patterns for provided branch or current branch. '''  # line 418
        return _coconut.frozenset() if not _.track and not _.picky else frozenset(_.branches[_.branch if branch is None else branch].tracked)  # line 419


# Main client operations
def offline(argument: '_coconut.typing.Optional[str]'=None, options: '_coconut.typing.Sequence[str]'=[]) -> 'None':  # line 423
    ''' Initial command to start working offline. '''  # line 424
    if os.path.exists(metaFolder):  # line 425
        if '--force' not in options:  # line 426
            Exit("Repository folder is either already offline or older branches and commits were left over.\nUse 'sos online' to check for dirty branches, or\nWipe existing offline branches with 'sos offline --force'")  # line 426
        try:  # line 427
            for entry in os.listdir(metaFolder):  # line 428
                resource = metaFolder + os.sep + entry  # line 429
                if os.path.isdir(resource):  # line 430
                    shutil.rmtree(resource)  # line 430
                else:  # line 431
                    os.unlink(resource)  # line 431
        except:  # line 432
            Exit("Cannot reliably remove previous repository contents. Please remove .sos folder manually prior to going offline")  # line 432
    m = Metadata(os.getcwd())  # type: Metadata  # line 433
    if '--compress' in options or m.c.compress:  # plain file copies instead of compressed ones  # line 434
        m.compress = True  # plain file copies instead of compressed ones  # line 434
    if '--picky' in options or m.c.picky:  # Git-like  # line 435
        m.picky = True  # Git-like  # line 435
    elif '--track' in options or m.c.track:  # Svn-like  # line 436
        m.track = True  # Svn-like  # line 436
    if '--strict' in options or m.c.strict:  # always hash contents  # line 437
        m.strict = True  # always hash contents  # line 437
    debug("Preparing offline repository...")  # line 438
    m.createBranch(0, str(defaults["defaultbranch"]) if argument is None else argument, initialMessage="Offline repository created on %s" % strftime())  # main branch's name may be None (e.g. for fossil)  # line 439
    m.branch = 0  # line 440
    m.saveBranches()  # no change immediately after going offline, going back online won't issue a warning  # line 441
    info("Offline repository prepared. Use 'sos online' to finish offline work")  # line 442

def online(options: '_coconut.typing.Sequence[str]'=[]) -> 'None':  # line 444
    ''' Finish working offline. '''  # line 445
    force = '--force' in options  # type: bool  # line 446
    m = Metadata(os.getcwd())  # line 447
    m.loadBranches()  # line 448
    if any([not b.inSync for b in m.branches.values()]) and not force:  # line 449
        Exit("There are still unsynchronized (dirty) branches.\nUse 'sos log' to list them.\nUse 'sos commit' and 'sos switch' to commit dirty branches to your VCS before leaving offline mode.\nUse 'sos online --force' to erase all aggregated offline revisions")  # line 449
    strict = '--strict' in options or m.strict  # type: bool  # line 450
    if options.count("--force") < 2:  # line 451
        changes = m.findChanges(checkContent=strict, considerOnly=None if not m.track and not m.picky else m.getTrackingPatterns())  # type: ChangeSet  # HINT no option for --only/--except here on purpose. No check for picky here, because online is not a command that considers staged files (but we could use --only here, alternatively)  # line 452
        if modified(changes):  # line 453
            Exit("File tree is modified vs. current branch.\nUse 'sos online --force --force' to continue with removing the offline repository")  # line 453
    try:  # line 454
        shutil.rmtree(metaFolder)  # line 454
        info("Exited offline mode. Continue working with your traditional VCS.")  # line 454
    except Exception as E:  # line 455
        Exit("Error removing offline repository: %r" % E)  # line 455

def branch(argument: '_coconut.typing.Optional[str]'=None, options: '_coconut.typing.Sequence[str]'=[]) -> 'None':  # line 457
    ''' Create a new branch (from file tree or last revision) and (by default) continue working on it. '''  # line 458
    last = '--last' in options  # type: bool  # use last revision for branching, not current file tree  # line 459
    stay = '--stay' in options  # type: bool  # continue on current branch after branching  # line 460
    force = '--force' in options  # type: bool  # branch even with local modifications  # line 461
    m = Metadata(os.getcwd())  # type: Metadata  # line 462
    m.loadBranches()  # line 463
    m.loadBranch(m.branch)  # line 464
    if argument and m.getBranchByName(argument) is not None:  # create a named branch  # line 465
        Exit("Branch '%s' already exists. Cannot proceed" % argument)  # create a named branch  # line 465
    branch = max(m.branches.keys()) + 1  # next branch's key - this isn't atomic but we assume single-user non-concurrent use here  # line 466
    debug("Branching to %sbranch b%02d%s%s..." % ("unnamed " if argument is None else "", branch, " '%s'" % argument if argument else "", " from last revision" if last else ""))  # line 467
    if last:  # line 468
        m.duplicateBranch(branch, "Branched from r%02d/b%02d" % (m.branch, max(m.commits.keys())) if argument is None else argument)  # branch from branch's last revision  # line 469
    else:  # from file tree state  # line 470
        m.createBranch(branch, "Branched from r%02d/b%02d" % (m.branch, max(m.commits.keys())) if argument is None else argument)  # branch from current file tree  # line 471
    if not stay:  # line 472
        m.branch = branch  # line 473
        m.saveBranches()  # line 474
    info("%s new %sbranch b%02d%s" % ("Continue work after branching" if stay else "Switched to", "unnamed " if argument is None else "", branch, " '%s'" % argument if argument else ""))  # line 475

def changes(argument: 'str'=None, options: '_coconut.typing.Sequence[str]'=[], onlys: '_coconut.typing.Optional[FrozenSet[str]]'=None, excps: '_coconut.typing.Optional[FrozenSet[str]]'=None) -> 'ChangeSet':  # line 477
    ''' Show changes of file tree vs. (last or specified) revision on current or specified branch. '''  # line 478
    m = Metadata(os.getcwd())  # type: Metadata  # line 479
    branch = None  # type: _coconut.typing.Optional[int]  # line 479
    revision = None  # type: _coconut.typing.Optional[int]  # line 479
    m.loadBranches()  # knows current branch  # line 480
    strict = '--strict' in options or m.strict  # type: bool  # line 481
    branch, revision = m.parseRevisionString(argument)  # line 482
    if branch not in m.branches:  # line 483
        Exit("Unknown branch")  # line 483
    m.loadBranch(branch)  # knows commits  # line 484
    revision = revision if revision >= 0 else len(m.commits) + revision  # negative indexing  # line 485
    if revision < 0 or revision > max(m.commits):  # line 486
        Exit("Unknown revision r%02d" % revision)  # line 486
    info("//|\\\\ Changes of file tree vs. revision '%s/r%02d'" % ((lambda _coconut_none_coalesce_item: "b%02d" % branch if _coconut_none_coalesce_item is None else _coconut_none_coalesce_item)(m.branches[branch].name), revision))  # line 487
    m.computeSequentialPathSet(branch, revision)  # load all commits up to specified revision  # line 488
    changes = m.findChanges(checkContent=strict, considerOnly=onlys if not m.track and not m.picky else conditionalIntersection(onlys, m.getTrackingPatterns() | m.getTrackingPatterns(branch)), dontConsider=excps)  # type: ChangeSet  # line 489
    m.listChanges(changes)  # line 490
    return changes  # for unit tests only  # line 491

def diff(argument: 'str'="", options: '_coconut.typing.Sequence[str]'=[], onlys: '_coconut.typing.Optional[FrozenSet[str]]'=None, excps: '_coconut.typing.Optional[FrozenSet[str]]'=None) -> 'None':  # line 493
    ''' Show text file differences of file tree vs. (last or specified) revision on current or specified branch. '''  # line 494
    m = Metadata(os.getcwd())  # type: Metadata  # line 495
    branch = None  # type: _coconut.typing.Optional[int]  # line 495
    revision = None  # type: _coconut.typing.Optional[int]  # line 495
    m.loadBranches()  # knows current branch  # line 496
    strict = '--strict' in options or m.strict  # type: bool  # line 497
    _from = {None: option.split("--from=")[1] for option in options if options.startswith("--from=")}.get(None, None)  # type: _coconut.typing.Optional[str]  # line 498
    branch, revision = m.parseRevisionString(argument)  # if nothing given, use last commit  # line 499
    if branch not in m.branches:  # line 500
        Exit("Unknown branch")  # line 500
    m.loadBranch(branch)  # knows commits  # line 501
    revision = revision if revision >= 0 else len(m.commits) + revision  # negative indexing  # line 502
    if revision < 0 or revision > max(m.commits):  # line 503
        Exit("Unknown revision r%02d" % revision)  # line 503
    info("//|\\\\ Differences of file tree vs. revision '%s/r%02d'" % ((lambda _coconut_none_coalesce_item: "b%02d" % branch if _coconut_none_coalesce_item is None else _coconut_none_coalesce_item)(m.branches[branch].name), revision))  # line 504
    m.computeSequentialPathSet(branch, revision)  # load all commits up to specified revision  # line 505
    changes = m.findChanges(checkContent=strict, inverse=True, considerOnly=onlys if not m.track and not m.picky else conditionalIntersection(onlys, m.getTrackingPatterns() | m.getTrackingPatterns(branch)), dontConsider=excps)  # type: ChangeSet  # line 506
    onlyBinaryModifications = dataCopy(ChangeSet, changes, modifications={k: v for k, v in changes.modifications.items() if not m.isTextType(os.path.basename(k))})  # type: ChangeSet  # line 507
    if modified(onlyBinaryModifications):  # line 508
        debug("//|\\\\ File changes")  # line 508
    m.listChanges(onlyBinaryModifications)  # only list modified binary files  # line 509

    if changes.modifications:  # line 511
        debug("%s//|\\\\ Textual modifications" % ("\n" if modified(onlyBinaryModifications) else ""))  # line 511
    for path, pinfo in (c for c in changes.modifications.items() if m.isTextType(os.path.basename(c[0]))):  # only consider modified text files  # line 512
        content = None  # type: _coconut.typing.Optional[bytes]  # ; othr:str[]; curr:str[]  # line 513
        if pinfo.size == 0:  # empty file contents  # line 514
            content = b""  # empty file contents  # line 514
        else:  # versioned file  # line 515
            content = m.restoreFile(None, branch, revision, pinfo)  # versioned file  # line 515
            assert content is not None  # versioned file  # line 515
        abspath = os.path.join(m.root, path.replace(SLASH, os.sep))  # current file  # line 516
        blocks = merge(file=content, intoname=abspath, diffOnly=True)  # type: List[MergeBlock]  # only determine change blocks  # line 517
        print("DIF %s%s" % (path, " <timestamp only>" if len(blocks) == 1 and blocks[0].tipe == MergeBlockType.KEEP else ""))  # line 518
        for block in blocks:  # line 519
            if block.tipe in [MergeBlockType.INSERT, MergeBlockType.REMOVE]:  # line 520
                pass  # TODO print some previous and following lines - which aren't accessible here anymore  # line 521
            if block.tipe == MergeBlockType.INSERT:  # TODO show color via (n)curses or other library?  # line 522
                for no, line in enumerate(block.lines):  # line 523
                    print("+++ %04d |%s|" % (no + block.line, line))  # line 524
            elif block.tipe == MergeBlockType.REMOVE:  # line 525
                for no, line in enumerate(block.lines):  # line 526
                    print("--- %04d |%s|" % (no + block.line, line))  # line 527
            elif block.tipe in [MergeBlockType.REPLACE, MergeBlockType.MODIFY]:  # TODO for MODIFY also show intra-line change ranges  # line 528
                for no, line in enumerate(block.replaces.lines):  # line 529
                    print("- | %04d |%s|" % (no + block.replaces.line, line))  # line 530
                for no, line in enumerate(block.lines):  # line 531
                    print("+ | %04d |%s|" % (no + block.line, line))  # line 532
#      elif block.tipe == MergeBlockType.KEEP: pass
#      elif block.tipe == MergeBlockType.MODIFY:  # intra-line modifications
#      elif block.tipe == MergeBlockType.MOVE:  # intra-line modifications

def commit(argument: '_coconut.typing.Optional[str]'=None, options: '_coconut.typing.Sequence[str]'=[], onlys: '_coconut.typing.Optional[FrozenSet[str]]'=None, excps: '_coconut.typing.Optional[FrozenSet[str]]'=None) -> 'None':  # line 537
    ''' Create new revision from file tree changes vs. last commit. '''  # line 538
    m = Metadata(os.getcwd())  # type: Metadata  # line 539
    m.loadBranches()  # knows current branch  # line 540
    if argument is not None and argument in m.tags:  # line 541
        Exit("Illegal commit message. It was already used as a tag name")  # line 541
    trackingPatterns = m.getTrackingPatterns()  # type: FrozenSet[str]  # SVN-like mode  # line 542
    if m.picky and not trackingPatterns:  # line 543
        Exit("No file patterns staged for commit in picky mode")  # line 543
    changes = None  # type: ChangeSet  # line 544
    m, branch, revision, changes, strict, force, trackingPatterns = exitOnChanges(None, options, commit=True, onlys=onlys, excps=excps)  # special flag creates new revision for detected changes, but abort if no changes  # line 545
    info((lambda _coconut_none_coalesce_item: "b%d" % m.branch if _coconut_none_coalesce_item is None else _coconut_none_coalesce_item)("Committing changes to branch '%s'..." % m.branches[m.branch].name))  # line 546
    m.integrateChangeset(changes, clear=True)  # update pathset to changeset only  # line 547
    m.saveCommit(m.branch, revision)  # revision has already been incremented  # line 548
    m.commits[revision] = CommitInfo(revision, longint(time.time() * 1000), argument)  # comment can be None  # line 549
    m.saveBranch(m.branch)  # line 550
    m.loadBranches()  # TODO is it necessary to load again?  # line 551
    if m.picky:  # line 552
        m.branches[m.branch] = dataCopy(BranchInfo, m.branches[m.branch], tracked=[], inSync=False)  # remove tracked patterns  # line 553
    else:  # track or simple mode  # line 554
        m.branches[m.branch] = dataCopy(BranchInfo, m.branches[m.branch], inSync=False)  # set branch dirty  # line 555
    if "--tag" in options and argument is not None:  # memorize unique tag  # line 556
        m.tags.append(argument)  # memorize unique tag  # line 556
    m.saveBranches()  # line 557
    info("Created new revision r%02d%s (+%02d/-%02d/*%02d)" % (revision, ((" '%s'" % argument) if argument is not None else ""), len(changes.additions), len(changes.deletions), len(changes.modifications)))  # line 558

def status() -> 'None':  # line 560
    ''' Show branches and current repository state. '''  # line 561
    m = Metadata(os.getcwd())  # type: Metadata  # line 562
    m.loadBranches()  # knows current branch  # line 563
    current = m.branch  # type: int  # line 564
    info("//|\\\\ Offline repository status")  # line 565
    print("Content checking %sactivated" % ("" if m.strict else "de"))  # line 566
    print("Data compression %sactivated" % ("" if m.compress else "de"))  # line 567
    print("Repository is in %s mode" % ("tracking" if m.track else ("picky" if m.picky else "simple")))  # line 568
    sl = max([len((lambda _coconut_none_coalesce_item: "" if _coconut_none_coalesce_item is None else _coconut_none_coalesce_item)(b.name)) for b in m.branches.values()])  # type: int  # line 569
    for branch in sorted(m.branches.values(), key=lambda b: b.number):  # line 570
        m.loadBranch(branch.number)  # knows commit history  # line 571
        print("  %s b%02d%s @%s (%s) with %d commits%s" % ("*" if current == branch.number else " ", branch.number, ((" %%%ds" % (sl + 2)) % ("'%s'" % branch.name)) if branch.name else "", strftime(branch.ctime), "in sync" if branch.inSync else "dirty", len(m.commits), ". Last comment: '%s'" % m.commits[max(m.commits)].message if m.commits[max(m.commits)].message else ""))  # line 572
    if m.track or m.picky and len(m.branches[m.branch].tracked) > 0:  # line 573
        info("\nTracked file patterns:")  # line 574
        print(ajoin("  | ", m.branches[m.branch].tracked, "\n"))  # line 575

def exitOnChanges(argument: '_coconut.typing.Optional[str]'=None, options: '_coconut.typing.Sequence[str]'=[], check: 'bool'=True, commit: 'bool'=False, onlys: '_coconut.typing.Optional[FrozenSet[str]]'=None, excps: '_coconut.typing.Optional[FrozenSet[str]]'=None) -> 'Tuple[Metadata, _coconut.typing.Optional[int], int, ChangeSet, bool, bool, FrozenSet[str]]':  # line 577
    ''' Common behavior for switch, update, delete, commit.
      Should not be called for picky mode, unless tracking patterns were added.
      check: stop program on detected change
      commit: don't stop on changes, because that's what we need in the operation
      Returns (Metadata, (current or target) branch, revision, set of changes vs. last commit on current branch, strict, force flags. '''  # line 582
    m = Metadata(os.getcwd())  # type: Metadata  # line 583
    m.loadBranches()  # knows current branch  # line 584
    force = '--force' in options  # type: bool  # line 585
    strict = '--strict' in options or m.strict  # type: bool  # line 586
    if argument is not None:  # line 587
        branch, revision = m.parseRevisionString(argument)  # for early abort  # line 588
        if branch is None:  # line 589
            Exit("Branch '%s' doesn't exist. Cannot proceed" % argument)  # line 589
    m.loadBranch(m.branch)  # knows last commits of *current* branch  # line 590

# Determine current changes
    trackingPatterns = m.getTrackingPatterns()  # type: FrozenSet[str]  # line 593
    m.computeSequentialPathSet(m.branch, max(m.commits))  # load all commits up to specified revision  # line 594
    changes = m.findChanges(m.branch if commit else None, max(m.commits) + 1 if commit else None, checkContent=strict, considerOnly=onlys if not (m.track or m.picky) else conditionalIntersection(onlys, trackingPatterns), dontConsider=excps)  # type: ChangeSet  # line 595
    if check and modified(changes) and not force:  # line 596
        m.listChanges(changes)  # line 597
        if not commit:  # line 598
            Exit("File tree contains changes. Use --force to proceed")  # line 598
    elif commit and not force:  #  and not check  # line 599
        Exit("Nothing to commit")  #  and not check  # line 599

    if argument is not None:  # branch/revision specified  # line 601
        m.loadBranch(branch)  # knows commits of target branch  # line 602
        revision = revision if revision >= 0 else len(m.commits) + revision  # negative indexing  # line 603
        if revision < 0 or revision > max(m.commits):  # line 604
            Exit("Unknown revision r%02d" % revision)  # line 604
        return (m, branch, revision, changes, strict, force, m.getTrackingPatterns(branch))  # line 605
    return (m, m.branch, max(m.commits) + (1 if commit else 0), changes, strict, force, trackingPatterns)  # line 606

def switch(argument: 'str', options: '_coconut.typing.Sequence[str]'=[], onlys: '_coconut.typing.Optional[FrozenSet[str]]'=None, excps: '_coconut.typing.Optional[FrozenSet[str]]'=None) -> 'None':  # line 608
    ''' Continue work on another branch, replacing file tree changes. '''  # line 609
    changes = None  # type: ChangeSet  # line 610
    m, branch, revision, changes, strict, force, trackingPatterns = exitOnChanges(argument, options)  # line 611
    info("//|\\\\ Switching to branch %sb%02d/r%02d" % ("'%s' " % m.branches[branch].name if m.branches[branch].name else "", branch, revision))  # line 612

# Determine file changes from other branch to current file tree
    if '--meta' in options:  # only switch meta data  # line 615
        m.branches[m.branch] = dataCopy(BranchInfo, m.branches[m.branch], tracked=m.branches[branch].tracked)  # line 616
    else:  # full file switch  # line 617
        m.computeSequentialPathSet(branch, revision)  # load all commits up to specified revision for target branch into memory  # line 618
        changes = m.findChanges(checkContent=strict, inverse=True, considerOnly=onlys if not m.track and not m.picky else conditionalIntersection(onlys, trackingPatterns | m.getTrackingPatterns(branch)), dontConsider=excps)  # determine difference of other branch vs. file tree (forced or in sync with current branch; "addition" means exists now and should be removed)  # line 619
        if not modified(changes):  # line 620
            info("No changes to current file tree")  # line 621
        else:  # integration required  # line 622
            for path, pinfo in changes.deletions.items():  # line 623
                m.restoreFile(path, branch, revision, pinfo, ensurePath=True)  # is deleted in current file tree: restore from branch to reach target  # line 624
                print("ADD " + path)  # line 625
            for path, pinfo in changes.additions.items():  # line 626
                os.unlink(os.path.join(m.root, path.replace(SLASH, os.sep)))  # is added in current file tree: remove from branch to reach target  # line 627
                print("DEL " + path)  # line 628
            for path, pinfo in changes.modifications.items():  # line 629
                m.restoreFile(path, branch, revision, pinfo)  # is modified in current file tree: restore from branch to reach target  # line 630
                print("MOD " + path)  # line 631
    m.branch = branch  # line 632
    m.saveBranches()  # store switched path info  # line 633
    info("Switched to branch %sb%02d/r%02d" % ("'%s' " % (m.branches[branch].name if m.branches[branch].name else ""), branch, revision))  # line 634

def update(argument: 'str', options: '_coconut.typing.Sequence[str]'=[], onlys: '_coconut.typing.Optional[FrozenSet[str]]'=None, excps: '_coconut.typing.Optional[FrozenSet[str]]'=None) -> 'None':  # line 636
    ''' Load and integrate a specified other branch/revision into current life file tree.
      In tracking mode, this also updates the set of tracked patterns.
      User options for merge operation: --add (don't remove), --rm (don't insert), --add-lines/--rm-lines (inside each file)
      User options for conflict resolution: --theirs/--mine/--ask
  '''  # line 641
    mrg = firstOfMap({"--add": MergeOperation.INSERT, "--rm": MergeOperation.REMOVE}, options, MergeOperation.BOTH)  # type: int  # default operation is replicate remove state for non-conflicting cases (insertions/deletions)  # line 642
    res = firstOfMap({'--theirs': ConflictResolution.THEIRS, '--mine': ConflictResolution.MINE}, options, ConflictResolution.NEXT)  # type: int  # NEXT means deeper level  # line 643
    mrgline = firstOfMap({'--add-lines': MergeOperation.INSERT, '--rm-lines': MergeOperation.REMOVE}, options, mrg)  # type: int  # default operation for modified files is same as for files  # line 644
    resline = firstOfMap({'--theirs-lines': ConflictResolution.THEIRS, '--mine-lines': ConflictResolution.MINE}, options, ConflictResolution.ASK)  # type: int  # line 645
    m = Metadata(os.getcwd())  # type: Metadata  # TODO same is called inside stop on changes - could return both current and designated branch instead  # line 646
    m.loadBranches()  # line 647
    changes = None  # type: ChangeSet  # line 647
    currentBranch = m.branch  # type: _coconut.typing.Optional[int]  # line 648
    m, branch, revision, changes, strict, force, trackingPatterns = exitOnChanges(argument, options, check=False, onlys=onlys, excps=excps)  # don't check for current changes, only parse arguments  # line 649
    debug("Integrating changes from '%s/r%02d' into file tree..." % ((lambda _coconut_none_coalesce_item: "b%02d" % branch if _coconut_none_coalesce_item is None else _coconut_none_coalesce_item)(m.branches[branch].name), revision))  # line 650

# Determine file changes from other branch over current file tree
    m.computeSequentialPathSet(branch, revision)  # load all commits up to specified revision for branch to integrate  # line 653
    trackingUnion = trackingPatterns | m.getTrackingPatterns(branch)  # type: FrozenSet[str]  # line 654
    changes = m.findChanges(checkContent=strict, inverse=True, considerOnly=onlys if not m.track and not m.picky else conditionalIntersection(onlys, trackingUnion), dontConsider=excps)  # determine difference of other branch vs. file tree. "addition" means exists now but not in other, and should be removed unless in tracking mode  # line 655
    if not (mrg & MergeOperation.INSERT and changes.additions or (mrg & MergeOperation.REMOVE and changes.deletions) or changes.modifications):  # no file ops  # line 656
        if trackingUnion != trackingPatterns:  # nothing added  # line 657
            info("No file changes detected, but tracking patterns were merged (run 'sos switch /-1 --meta' to undo)")  # TODO write test to see if this works  # line 658
        else:  # line 659
            info("Nothing to update")  # but write back updated branch info below  # line 660
    else:  # integration required  # line 661
        for path, pinfo in changes.deletions.items():  # deletions mark files not present in current file tree -> needs additon  # line 662
            if mrg & MergeOperation.INSERT:  # deleted in current file tree: restore from branch to reach target  # line 663
                m.restoreFile(path, branch, revision, pinfo, ensurePath=True)  # deleted in current file tree: restore from branch to reach target  # line 663
            print("ADD " + path if mrg & MergeOperation.INSERT else "(A) " + path)  # line 664
        for path, pinfo in changes.additions.items():  # line 665
            if m.track or m.picky:  # because untracked files of other branch cannot be detected (which is good)  # line 666
                Exit("This should never happen")  # because untracked files of other branch cannot be detected (which is good)  # line 666
            if mrg & MergeOperation.REMOVE:  # line 667
                os.unlink(m.root + os.sep + path.replace(SLASH, os.sep))  # line 667
            print("DEL " + path if mrg & MergeOperation.REMOVE else "(D) " + path)  # not contained in other branch, but maybe kept  # line 668
        for path, pinfo in changes.modifications.items():  # line 669
            into = os.path.join(m.root, path.replace(SLASH, os.sep))  # type: str  # line 670
            binary = not m.isTextType(path)  # line 671
            if res & ConflictResolution.ASK or (binary and res == ConflictResolution.NEXT):  # TODO this may ask user even if no interaction was asked for (check line level for interactivity fist)  # line 672
                print(("MOD " + path if not binary else "BIN ") + path)  # line 673
                reso = {"i": ConflictResolution.MINE, "t": ConflictResolution.THEIRS, "m": ConflictResolution.NEXT}.get(user_input(" Resolve: *M[I]ne, [T]heirs, [M]erge: (I)").strip().lower(), ConflictResolution.MINE)  # line 674
                debug("User selected %d" % reso)  # line 675
            else:  # line 676
                reso = res  # line 676
            if reso & ConflictResolution.THEIRS:  # line 677
                m.readOrCopyVersionedFile(branch, revision, pinfo.nameHash, toFile=into)  # blockwise copy of contents  # line 678
                print("THR " + path)  # line 679
            elif reso & ConflictResolution.MINE:  # line 680
                print("MNE " + path)  # nothing to do! same as skip  # line 681
            else:  # NEXT: line-based merge  # line 682
                file = m.readOrCopyVersionedFile(branch, revision, pinfo.nameHash) if pinfo.size > 0 else b''  # type: _coconut.typing.Optional[bytes]  # parse lines  # line 683
                if file is not None:  # if None, error message was already logged  # line 684
                    contents = merge(file=file, intoname=into, mergeOperation=mrgline, conflictResolution=resline)  # type: bytes  # line 685
                    with open(path, "wb") as fd:  # TODO write to temp file first, in case writing fails  # line 686
                        fd.write(contents)  # TODO write to temp file first, in case writing fails  # line 686
    info("Integrated changes from '%s/r%02d' into file tree" % ((lambda _coconut_none_coalesce_item: "b%02d" % branch if _coconut_none_coalesce_item is None else _coconut_none_coalesce_item)(m.branches[branch].name), revision))  # line 687
    m.branches[currentBranch] = dataCopy(BranchInfo, m.branches[currentBranch], inSync=False, tracked=list(trackingUnion))  # line 688
    m.branch = currentBranch  # need to restore setting before saving TODO operate on different objects instead  # line 689
    m.saveBranches()  # line 690

def delete(argument: 'str', options: '_coconut.typing.Sequence[str]'=[]) -> 'None':  # line 692
    ''' Remove a branch entirely. '''  # line 693
    m, branch, revision, changes, strict, force, trackingPatterns = exitOnChanges(None, options)  # line 694
    if len(m.branches) == 1:  # line 695
        Exit("Cannot remove the only remaining branch. Use 'sos online' to leave offline mode")  # line 695
    branch, revision = m.parseRevisionString(argument)  # not from exitOnChanges, because we have to set argument to None there  # line 696
    if branch is None or branch not in m.branches:  # line 697
        Exit("Unknown branch")  # line 697
    debug("Removing branch %d%s..." % (branch, " '%s'" % m.branches[branch].name if m.branches[branch].name else ""))  # line 698
    binfo = m.removeBranch(branch)  # need to keep a reference to removed entry for output below  # line 699
    info("Branch b%02d%s removed" % (branch, " '%s'" % binfo.name if binfo.name else ""))  # line 700

def add(relPath: 'str', pattern: 'str', options: '_coconut.typing.Sequence[str]'=[]) -> 'None':  # line 702
    ''' Add a tracked files pattern to current branch's tracked files. '''  # line 703
    force = '--force' in options  # type: bool  # line 704
    m = Metadata(os.getcwd())  # type: Metadata  # line 705
    m.loadBranches()  # line 706
    if not m.track and not m.picky:  # line 707
        Exit("Repository is in simple mode. Use 'offline --track' or 'offline --picky' instead")  # line 707
    if pattern in m.branches[m.branch].tracked:  # line 708
        Exit("Pattern '%s' already tracked" % pattern)  # line 708
    if not force and not os.path.exists(relPath.replace(SLASH, os.sep)):  # line 709
        Exit("The pattern folder doesn't exist. Use --force to add it anyway")  # line 709
    if not force and len(fnmatch.filter(os.listdir(os.path.abspath(relPath.replace(SLASH, os.sep))), os.path.basename(pattern.replace(SLASH, os.sep)))) == 0:  # doesn't match any current file  # line 710
        Exit("Pattern doesn't match any file in specified folder. Use --force to add it anyway")  # line 711
    m.branches[m.branch].tracked.append(pattern)  # line 712
    m.saveBranches()  # line 713
    info("Added tracking pattern '%s' for folder '%s'" % (os.path.basename(pattern.replace(SLASH, os.sep)), os.path.abspath(relPath)))  # line 714

def remove(relPath: 'str', pattern: 'str') -> 'None':  # line 716
    ''' Remove a tracked files pattern from current branch's tracked files. '''  # line 717
    m = Metadata(os.getcwd())  # type: Metadata  # line 718
    m.loadBranches()  # line 719
    if not m.track and not m.picky:  # line 720
        Exit("Repository is in simple mode. Needs 'offline --track' or 'offline --picky' instead")  # line 720
    if pattern not in m.branches[m.branch].tracked:  # line 721
        suggestion = _coconut.set()  # type: Set[str]  # line 722
        for pat in m.branches[m.branch].tracked:  # line 723
            if fnmatch.fnmatch(pattern, pat):  # line 724
                suggestion.add(pat)  # line 724
        if suggestion:  # TODO use same wording as in move  # line 725
            print("Do you mean any of the following tracked file patterns? '%s'" % (", ".join(sorted(suggestion))))  # TODO use same wording as in move  # line 725
        Exit("Tracked pattern '%s' not found" % pattern)  # line 726
    m.branches[m.branch].tracked.remove(pattern)  # line 727
    m.saveBranches()  # line 728
    info("Removed tracking pattern '%s' for folder '%s'" % (os.path.basename(pattern), os.path.abspath(relPath.replace(SLASH, os.sep))))  # line 729

def ls(argument: '_coconut.typing.Optional[str]'=None, options: '_coconut.typing.Sequence[str]'=[]) -> 'None':  # line 731
    ''' List specified directory, augmenting with repository metadata. '''  # line 732
    folder = "." if argument is None else argument  # type: str  # line 733
    m = Metadata(os.getcwd())  # type: Metadata  # line 734
    m.loadBranches()  # line 735
    info("Repository is in %s mode" % ("tracking" if m.track else ("picky" if m.picky else "simple")))  # line 736
    relPath = os.path.relpath(folder, m.root).replace(os.sep, SLASH)  # type: str  # line 737
    trackingPatterns = m.getTrackingPatterns() if m.track or m.picky else _coconut.frozenset()  # type: _coconut.typing.Optional[FrozenSet[str]]  # for current branch  # line 738
    if '--patterns' in options:  # line 739
        out = ajoin("TRK ", [os.path.basename(p) for p in trackingPatterns if os.path.dirname(p).replace(os.sep, SLASH) == relPath], nl="\n")  # type: str  # line 740
        if out:  # line 741
            print(out)  # line 741
        return  # line 742
    files = list(sorted((entry for entry in os.listdir(folder) if os.path.isfile(os.path.join(folder, entry)))))  # type: List[str]  # line 743
    for file in files:  # for each file list all tracking patterns that match, or none (e.g. in picky mode after commit)  # line 744
        ignore = None  # type: _coconut.typing.Optional[str]  # line 745
        for ig in m.c.ignores:  # line 746
            if fnmatch.fnmatch(file, ig):  # remember first match  # line 747
                ignore = ig  # remember first match  # line 747
                break  # remember first match  # line 747
        if ig:  # line 748
            for wl in m.c.ignoresWhitelist:  # line 749
                if fnmatch.fnmatch(file, wl):  # found a white list entry for ignored file, undo ignoring it  # line 750
                    ignore = None  # found a white list entry for ignored file, undo ignoring it  # line 750
                    break  # found a white list entry for ignored file, undo ignoring it  # line 750
        if not ignore:  # line 751
            matches = []  # type: List[str]  # line 752
            for pattern in (p for p in trackingPatterns if os.path.dirname(p).replace(os.sep, SLASH) == relPath):  # only patterns matching current folder  # line 753
                if fnmatch.fnmatch(file, os.path.basename(pattern)):  # line 754
                    matches.append(os.path.basename(pattern))  # line 754
        matches.sort(key=lambda element: len(element))  # line 755
        print("%s %s%s" % ("IGN" if ignore is not None else ("TRK" if len(matches) > 0 else "..."), file, "  (%s)" % ignore if ignore is not None else ("  (%s)" % ("; ".join(matches)) if len(matches) > 0 else "")))  # line 756

def log(options: '_coconut.typing.Sequence[str]') -> 'None':  # line 758
    ''' List previous commits on current branch. '''  # line 759
    m = Metadata(os.getcwd())  # type: Metadata  # line 760
    m.loadBranches()  # knows current branch  # line 761
    m.loadBranch(m.branch)  # knows commit history  # line 762
    info((lambda _coconut_none_coalesce_item: "r%02d" % m.branch if _coconut_none_coalesce_item is None else _coconut_none_coalesce_item)("//|\\\\ Offline commit history of branch '%s'" % m.branches[m.branch].name))  # TODO also retain "from branch/revision" on branching?  # line 763
    nl = len("%d" % max(m.commits))  # determine space needed for revision  # line 764
    changeset = m.computeSequentialPathSetIterator(m.branch, max(m.commits))  # line 765
    maxWidth = max([wcswidth((lambda _coconut_none_coalesce_item: "" if _coconut_none_coalesce_item is None else _coconut_none_coalesce_item)(commit.message)) for commit in m.commits.values()])  # type: int  # line 766
    for no in range(max(m.commits) + 1):  # line 767
        commit = m.commits[no]  # type: CommitInfo  # line 768
        changes = next(changeset)  # type: ChangeSet  # side-effect: updates m.paths  # line 769
        newTextFiles = len([file for file in changes.additions.keys() if m.isTextType(file)])  # type: int  # line 770
        print("  %s r%s @%s (+%02d/-%02d/*%02d +%02dT/%05.1f%%) |%s|" % ("*" if commit.number == max(m.commits) else " ", ("%%%ds" % nl) % commit.number, strftime(commit.ctime), len(changes.additions), len(changes.deletions), len(changes.modifications), newTextFiles, 0. if len(changes.additions) == 0 else newTextFiles * 100. / len(changes.additions), ((lambda _coconut_none_coalesce_item: "" if _coconut_none_coalesce_item is None else _coconut_none_coalesce_item)(commit.message)).ljust(maxWidth)))  # line 771
        if '--changes' in options:  # line 772
            m.listChanges(changes)  # line 772

def config(argument: 'str', options: 'List[str]'=[]) -> 'None':  # line 774
    if argument not in ["set", "unset", "show", "list", "add", "rm"]:  # line 775
        Exit("Unknown config command")  # line 775
    if not configr:  # line 776
        Exit("Cannot execute config command. 'configr' module not installed")  # line 776
    c = loadConfig()  # type: Union[configr.Configr, Accessor]  # line 777
    if argument == "set":  # line 778
        if len(options) < 2:  # line 779
            Exit("No key nor value specified")  # line 779
        if options[0] not in (["defaultbranch"] + CONFIGURABLE_FLAGS + CONFIGURABLE_LISTS):  # line 780
            Exit("Unsupported key %r" % options[0])  # line 780
        if options[0] in CONFIGURABLE_FLAGS and options[1].lower() not in TRUTH_VALUES + FALSE_VALUES:  # line 781
            Exit("Cannot set flag to '%s'. Try on/off instead" % options[1].lower())  # line 781
        c[options[0]] = options[1].lower() in TRUTH_VALUES if options[0] in CONFIGURABLE_FLAGS else (options[1].strip() if options[0] not in CONFIGURABLE_LISTS else safeSplit(options[1], ";"))  # TODO sanitize texts?  # line 782
    elif argument == "unset":  # line 783
        if len(options) < 1:  # line 784
            Exit("No key specified")  # line 784
        if options[0] not in c.keys():  # line 785
            Exit("Unknown key")  # line 785
        del c[options[0]]  # line 786
    elif argument == "add":  # line 787
        if len(options) < 2:  # line 788
            Exit("No key nor value specified")  # line 788
        if options[0] not in CONFIGURABLE_LISTS:  # line 789
            Exit("Unsupported key for add %r" % options[0])  # line 789
        if options[0] not in c.keys():  # add list  # line 790
            c[options[0]] = [options[1]]  # add list  # line 790
        elif options[1] in c[options[0]]:  # line 791
            Exit("Value already contained")  # line 791
        c[options[0]].append(options[1])  # line 792
    elif argument == "rm":  # line 793
        if len(options) < 2:  # line 794
            Exit("No key nor value specified")  # line 794
        if options[0] not in c.keys():  # line 795
            Exit("Unknown key specified: %r" % options[0])  # line 795
        if options[1] not in c[options[0]]:  # line 796
            Exit("Unknown value: %r" % options[1])  # line 796
        c[options[0]].remove(options[1])  # line 797
    else:  # Show or list  # line 798
        for k, v in sorted(c.items()):  # line 799
            print("%s: %r" % (k.rjust(20), v))  # line 799
        if len(c.keys()) == 0:  # TODO list defaults instead? Or display [DEFAULT] for each item above if unmodified  # line 800
            info("No configuration stored, using only defaults.")  # TODO list defaults instead? Or display [DEFAULT] for each item above if unmodified  # line 800
        return  # line 801
    f, g = saveConfig(c)  # line 802
    if f is None:  # line 803
        error("Error saving user configuration: %r" % g)  # line 803

def move(relPath: 'str', pattern: 'str', newRelPath: 'str', newPattern: 'str', options: 'List[str]'=[]) -> 'None':  # line 805
    ''' Path differs: Move files, create folder if not existing. Pattern differs: Attempt to rename file, unless exists in target or not unique. '''  # line 806
    force = '--force' in options  # type: bool  # line 807
    soft = '--soft' in options  # type: bool  # line 808
    if not os.path.exists(relPath.replace(SLASH, os.sep)) and not force:  # line 809
        Exit("Source folder doesn't exist. Use --force to proceed anyway")  # line 809
    m = Metadata(os.getcwd())  # type: Metadata  # line 810
    matching = fnmatch.filter(os.listdir(relPath.replace(SLASH, os.sep)) if os.path.exists(relPath.replace(SLASH, os.sep)) else [], os.path.basename(pattern))  # type: List[str]  # find matching files in source  # line 811
    matching[:] = [f for f in matching if len([n for n in m.c.ignores if fnmatch.fnmatch(f, n)]) == 0 or len([p for p in m.c.ignoresWhitelist if fnmatch.fnmatch(f, p)]) > 0]  # line 812
    if not matching and not force:  # line 813
        Exit("No files match the specified file pattern. Use --force to proceed anyway")  # line 813
    m.loadBranches()  # knows current branch  # line 814
    if not m.track and not m.picky:  # line 815
        Exit("Repository is in simple mode. Simply use basic file operations to modify files, then execute 'sos commit' to version the changes")  # line 815
    if pattern not in m.branches[m.branch].tracked:  # line 816
        for tracked in (t for t in m.branches[m.branch].tracked if os.path.dirname(t) == relPath):  # for all patterns of the same source folder  # line 817
            alternative = fnmatch.filter(matching, os.path.basename(tracked))  # type: _coconut.typing.Sequence[str]  # find if it matches any of the files in the source folder, too  # line 818
            if alternative:  # line 819
                info("  '%s' matches %d files" % (tracked, len(alternative)))  # line 819
        if not (force or soft):  # line 820
            Exit("File pattern '%s' is not tracked on current branch. 'sos move' only works on tracked patterns" % pattern)  # line 820
    basePattern = os.path.basename(pattern)  # type: str  # pure glob without folder  # line 821
    newBasePattern = os.path.basename(newPattern)  # type: str  # line 822
    if basePattern.count("*") < newBasePattern.count("*") or (basePattern.count("?") - basePattern.count("[?]")) < (newBasePattern.count("?") - newBasePattern.count("[?]")) or (basePattern.count("[") - basePattern.count("\\[")) < (newBasePattern.count("[") - newBasePattern.count("\\[")) or (basePattern.count("]") - basePattern.count("\\]")) < (newBasePattern.count("]") - newBasePattern.count("\\]")):  # line 823
        Exit("Glob markers from '%s' to '%s' don't match, cannot move/rename tracked matching files" % (basePattern, newBasePattern))  # line 827
    oldTokens = None  # type: _coconut.typing.Sequence[GlobBlock]  # line 828
    newToken = None  # type: _coconut.typing.Sequence[GlobBlock]  # line 828
    oldTokens, newTokens = tokenizeGlobPatterns(os.path.basename(pattern), os.path.basename(newPattern))  # line 829
    matches = convertGlobFiles(matching, oldTokens, newTokens)  # type: _coconut.typing.Sequence[Tuple[str, str]]  # computes list of source - target filename pairs  # line 830
    if len({st[1] for st in matches}) != len(matches):  # line 831
        Exit("Some target filenames are not unique and different move/rename actions would point to the same target file")  # line 831
    matches = reorderRenameActions(matches, exitOnConflict=not soft)  # attempts to find conflict-free renaming order, or exits  # line 832
    if os.path.exists(newRelPath):  # line 833
        exists = [filename[1] for filename in matches if os.path.exists(os.path.join(newRelPath, filename[1]).replace(SLASH, os.sep))]  # type: _coconut.typing.Sequence[str]  # line 834
        if exists and not (force or soft):  # line 835
            Exit("%s files would write over existing files in %s cases. Use --force to execute it anyway" % ("Moving" if relPath != newRelPath else "Renaming", "all" if len(exists) == len(matches) else "some"))  # line 835
    else:  # line 836
        os.makedirs(os.path.abspath(newRelPath.replace(SLASH, os.sep)))  # line 836
    if not soft:  # perform actual renaming  # line 837
        for (source, target) in matches:  # line 838
            try:  # line 839
                shutil.move(os.path.abspath(os.path.join(relPath, source).replace(SLASH, os.sep)), os.path.abspath(os.path.join(newRelPath, target).replace(SLASH, os.sep)))  # line 839
            except Exception as E:  # one error can lead to another in case of delicate renaming order  # line 840
                error("Cannot move/rename file '%s' to '%s'" % (source, os.path.join(newRelPath, target)))  # one error can lead to another in case of delicate renaming order  # line 840
    m.branches[m.branch].tracked[m.branches[m.branch].tracked.index(pattern)] = newPattern  # line 841
    m.saveBranches()  # line 842

def parse(root: 'str', cwd: 'str'):  # line 844
    ''' Main operation. Main has already chdir into VCS root folder, cwd is original working directory for add, rm. '''  # line 845
    debug("Parsing command-line arguments...")  # line 846
    try:  # line 847
        command = sys.argv[1].strip() if len(sys.argv) > 1 else ""  # line 848
        argument = sys.argv[2].strip() if len(sys.argv) > 2 and not sys.argv[2].startswith("--") else None  # line 849
        options = sys.argv[3:] if command == "config" else [c for c in sys.argv[2:] if c.startswith("--")]  # consider second parameter for no-arg command, otherwise from third on  # line 850
        onlys, excps = parseOnlyOptions(cwd, options)  # extracts folder-relative information for changes, commit, diff, switch, update  # line 851
        debug("Processing command %r with argument '%s' and options %r." % ("" if command is None else command, "" if argument is None else argument, options))  # line 852
        if command[:1] in "amr":  # line 853
            relPath, pattern = relativize(root, os.path.join(cwd, "." if argument is None else argument))  # line 853
        if command[:1] == "m":  # line 854
            if not options:  # line 855
                Exit("Need a second file pattern argument as target for move/rename command")  # line 855
            newRelPath, newPattern = relativize(root, os.path.join(cwd, options[0]))  # line 856
        if command[:1] == "a":  # line 857
            add(relPath, pattern, options)  # line 857
        elif command[:1] == "b":  # line 858
            branch(argument, options)  # line 858
        elif command[:2] == "ch":  # line 859
            changes(argument, options, onlys, excps)  # line 859
        elif command[:3] == "com":  # line 860
            commit(argument, options, onlys, excps)  # line 860
        elif command[:2] == "ci":  # line 861
            commit(argument, options, onlys, excps)  # line 861
        elif command[:3] == 'con':  # line 862
            config(argument, options)  # line 862
        elif command[:2] == "de":  # line 863
            delete(argument, options)  # line 863
        elif command[:2] == "di":  # line 864
            diff(argument, options, onlys, excps)  # line 864
        elif command[:1] == "h":  # line 865
            usage()  # line 865
        elif command[:2] == "lo":  # line 866
            log(options)  # line 866
        elif command[:2] == "li":  # TODO handle absolute paths as well, also for Windows  # line 867
            ls(relativize(root, cwd if argument is None else os.path.join(cwd, argument))[1], options)  # TODO handle absolute paths as well, also for Windows  # line 867
        elif command[:2] == "ls":  # TODO avoid root super paths (..)  # line 868
            ls(relativize(root, cwd if argument is None else os.path.join(cwd, argument))[1], options)  # TODO avoid root super paths (..)  # line 868
        elif command[:1] == "m":  # line 869
            move(relPath, pattern, newRelPath, newPattern, options[1:])  # line 869
        elif command[:2] == "of":  # line 870
            offline(argument, options)  # line 870
        elif command[:2] == "on":  # line 871
            online(options)  # line 871
        elif command[:1] == "r":  # line 872
            remove(relPath, pattern)  # line 872
        elif command[:2] == "st":  # line 873
            status()  # line 873
        elif command[:2] == "sw":  # line 874
            switch(argument, options, onlys, excps)  # line 874
        elif command[:1] == "u":  # line 875
            update(argument, options, onlys, excps)  # line 875
        elif command[:1] == "v":  # line 876
            usage(short=True)  # line 876
        else:  # line 877
            Exit("Unknown command '%s'" % command)  # line 877
        Exit(code=0)  # line 878
    except (Exception, RuntimeError) as E:  # line 879
        print(str(E))  # line 880
        import traceback  # line 881
        traceback.print_exc()  # line 882
        traceback.print_stack()  # line 883
        try:  # line 884
            traceback.print_last()  # line 884
        except:  # line 885
            pass  # line 885
        Exit("An internal error occurred in SOS. Please report above message to the project maintainer at  https://github.com/ArneBachmann/sos/issues  via 'New Issue'.\nPlease state your installed version via 'sos version', and what you were doing.")  # line 886

def main() -> 'None':  # line 888
    global debug, info, warn, error  # line 889
    logging.basicConfig(level=level, stream=sys.stderr, format=("%(asctime)-23s %(levelname)-8s %(name)s:%(lineno)d | %(message)s" if '--log' in sys.argv else "%(message)s"))  # line 890
    _log = Logger(logging.getLogger(__name__))  # line 891
    debug, info, warn, error = _log.debug, _log.info, _log.warn, _log.error  # line 891
    for option in (o for o in ['--log', '--verbose', '-v', '--sos'] if o in sys.argv):  # clean up program arguments  # line 892
        sys.argv.remove(option)  # clean up program arguments  # line 892
    if '--help' in sys.argv or len(sys.argv) < 2:  # line 893
        usage()  # line 893
    command = sys.argv[1] if len(sys.argv) > 1 else None  # type: _coconut.typing.Optional[str]  # line 894
    root, vcs, cmd = findSosVcsBase()  # root is None if no .sos folder exists up the folder tree (still working online); vcs is checkout/repo root folder; cmd is the VCS base command  # line 895
    debug("Found root folders for SOS|VCS: %s|%s" % ("" if root is None else root, "" if vcs is None else vcs))  # line 896
    defaults["defaultbranch"] = vcsBranches.get(cmd, "trunk")  # sets dynamic default with SVN fallback  # line 897
    if force_sos or root is not None or ("" if command is None else command)[:2] == "of" or ("" if command is None else command)[:1] in ["h", "v"]:  # in offline mode or just going offline TODO what about git config?  # line 898
        cwd = os.getcwd()  # line 899
        os.chdir(cwd if command[:2] == "of" else cwd if root is None else root)  # line 900
        parse(root, cwd)  # line 901
    elif force_vcs or cmd is not None:  # online mode - delegate to VCS  # line 902
        info("SOS: Running '%s %s'" % (cmd, " ".join(sys.argv[1:])))  # line 903
        import subprocess  # only required in this section  # line 904
        process = subprocess.Popen([cmd] + sys.argv[1:], shell=False, stdin=subprocess.PIPE, stdout=sys.stdout, stderr=sys.stderr)  # line 905
        inp = ""  # type: str  # line 906
        while True:  # line 907
            so, se = process.communicate(input=inp)  # line 908
            if process.returncode is not None:  # line 909
                break  # line 909
            inp = sys.stdin.read()  # line 910
        if sys.argv[1][:2] == "co" and process.returncode == 0:  # successful commit - assume now in sync again (but leave meta data folder with potential other feature branches behind until "online")  # line 911
            if root is None:  # line 912
                Exit("Cannot determine VCS root folder: Unable to mark repository as synchronized and will show a warning when leaving offline mode")  # line 912
            m = Metadata(root)  # line 913
            m.loadBranches()  # read repo  # line 914
            m.branches[m.branch] = dataCopy(BranchInfo, m.branches[m.branch], inSync=True)  # mark as committed  # line 915
            m.saveBranches()  # line 916
    else:  # line 917
        Exit("No offline repository present, and unable to detect VCS file tree")  # line 917


# Main part
verbose = lateBinding["verbose"] = os.environ.get("DEBUG", "False").lower() == "true" or '--verbose' in sys.argv or '-v' in sys.argv  # imported from utility, and only modified here  # line 921
lateBinding["start"] = START_TIME  # line 922
level = logging.DEBUG if verbose else logging.INFO  # line 923
force_sos = '--sos' in sys.argv  # type: bool  # line 924
force_vcs = '--vcs' in sys.argv  # type: bool  # line 925
_log = Logger(logging.getLogger(__name__))  # type: logging.Logger  # line 926
debug, info, warn, error = _log.debug, _log.info, _log.warn, _log.error  # line 926
if __name__ == '__main__':  # line 927
    main()  # line 927
