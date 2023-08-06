#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# __coconut_hash__ = 0x68621d6d

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
    --verbose                    Enable verbose output""".format(appname=APPNAME, cmd="sos", CMD="SOS"))  # line 105

# Main data class
#@runtime_validation
class Metadata:  # line 109
    ''' This class doesn't represent the entire repository state in memory,
      but serves as a container for different repo operations,
      using only parts of its attributes at any point in time. Use with care.
  '''  # line 113

    def __init__(_, path: 'str') -> 'None':  # line 115
        ''' Create empty container object for various repository operations. '''  # line 116
        _.c = loadConfig()  # line 117
        _.root = path  # type: str  # line 118
        _.branches = {}  # type: Dict[int, BranchInfo]  # branch number zero represents the initial state at branching  # line 119
        _.commits = {}  # type: Dict[int, CommitInfo]  # consecutive numbers per branch, starting at 0  # line 120
        _.paths = {}  # type: Dict[str, PathInfo]  # utf-8 encoded relative, normalized file system paths  # line 121
        _.tags = []  # type: List[str]  # line 122
        _.branch = None  # type: _coconut.typing.Optional[int]  # current branch number  # line 123
        _.commit = None  # type: _coconut.typing.Optional[int]  # current revision number  # line 124
        _.track = _.c.track  # type: bool  # track file name patterns in the repository (per branch)  # line 125
        _.picky = _.c.picky  # type: bool  # pick files to commit per operation  # line 126
        _.strict = _.c.strict  # type: bool  # be always strict (regarding file contents comparsion)  # line 127
        _.compress = _.c.compress  # type: bool  # these flags are stored in the repository  # line 128

    def isTextType(_, filename: 'str') -> 'bool':  # line 130
        return (((lambda _coconut_none_coalesce_item: "" if _coconut_none_coalesce_item is None else _coconut_none_coalesce_item)(mimetypes.guess_type(filename)[0])).startswith("text/") or any([fnmatch.fnmatch(filename, pattern) for pattern in _.c.texttype])) and not any([fnmatch.fnmatch(filename, pattern) for pattern in _.c.bintype])  # line 130

    def listChanges(_, changes: 'ChangeSet') -> 'None':  # line 132
        if len(changes.additions) > 0:  # line 133
            print(ajoin("ADD ", sorted(changes.additions.keys()), "\n"))  # line 133
        if len(changes.deletions) > 0:  # line 134
            print(ajoin("DEL ", sorted(changes.deletions.keys()), "\n"))  # line 134
        if len(changes.modifications) > 0:  # line 135
            print(ajoin("MOD ", sorted(changes.modifications.keys()), "\n"))  # line 135

    def loadBranches(_) -> 'None':  # line 137
        ''' Load list of branches and current branch info from metadata file. '''  # line 138
        try:  # fails if not yet created (on initial branch/commit)  # line 139
            branches = None  # type: List[Tuple]  # line 140
            with codecs.open(os.path.join(_.root, metaFolder, metaFile), "r", encoding=UTF8) as fd:  # line 141
                flags, branches = json.load(fd)  # line 142
            _.tags = flags["tags"]  # list of commit messages to treat as globally unique tags  # line 143
            _.branch = flags["branch"]  # current branch integer  # line 144
            _.track = flags["track"]  # line 145
            _.picky = flags["picky"]  # line 146
            _.strict = flags["strict"]  # line 147
            _.compress = flags["compress"]  # line 148
            _.branches = {i.number: i for i in (BranchInfo(*item) for item in branches)}  # re-create type info  # line 149
        except Exception as E:  # if not found, create metadata folder  # line 150
            _.branches = {}  # line 151
            warn("Couldn't read branches metadata: %r" % E)  # line 152

    def saveBranches(_) -> 'None':  # line 154
        ''' Save list of branches and current branch info to metadata file. '''  # line 155
        with codecs.open(os.path.join(_.root, metaFolder, metaFile), "w", encoding=UTF8) as fd:  # line 156
            json.dump(({"tags": _.tags, "branch": _.branch, "track": _.track, "picky": _.picky, "strict": _.strict, "compress": _.compress}, list(_.branches.values())), fd, ensure_ascii=False)  # line 157

    def getRevisionByName(_, name: 'str') -> '_coconut.typing.Optional[int]':  # line 159
        ''' Convenience accessor for named revisions (using commit message as name). '''  # line 160
        if name == "":  # line 161
            return -1  # line 161
        try:  # attempt to parse integer string  # line 162
            return longint(name)  # attempt to parse integer string  # line 162
        except ValueError:  # line 163
            pass  # line 163
        found = [number for number, commit in _.commits.items() if name == commit.message]  # line 164
        return found[0] if found else None  # line 165

    def getBranchByName(_, name: 'str') -> '_coconut.typing.Optional[int]':  # line 167
        ''' Convenience accessor for named branches. '''  # line 168
        if name == "":  # line 169
            return _.branch  # line 169
        try:  # attempt to parse integer string  # line 170
            return longint(name)  # attempt to parse integer string  # line 170
        except ValueError:  # line 171
            pass  # line 171
        found = [number for number, branch in _.branches.items() if name == branch.name]  # line 172
        return found[0] if found else None  # line 173

    def loadBranch(_, branch: 'int') -> 'None':  # line 175
        ''' Load all commit information from a branch meta data file. '''  # line 176
        with codecs.open(os.path.join(_.root, metaFolder, "b%d" % branch, metaFile), "r", encoding=UTF8) as fd:  # line 177
            commits = json.load(fd)  # type: List[List[Any]]  # list of CommitInfo that needs to be unmarshalled into value types  # line 178
        _.commits = {i.number: i for i in (CommitInfo(*item) for item in commits)}  # re-create type info  # line 179
        _.branch = branch  # line 180

    def saveBranch(_, branch: 'int') -> 'None':  # line 182
        ''' Save all commit information to a branch meta data file. '''  # line 183
        with codecs.open(os.path.join(_.root, metaFolder, "b%d" % branch, metaFile), "w", encoding=UTF8) as fd:  # line 184
            json.dump(list(_.commits.values()), fd, ensure_ascii=False)  # line 185

    def duplicateBranch(_, branch: 'int', name: '_coconut.typing.Optional[str]') -> 'None':  # line 187
        ''' Create branch from an existing branch/revision. WARN: Caller must have loaded branches information.
        branch: target branch (should not exist yet)
        name: optional name of new branch
        _.branch: current branch
    '''  # line 192
        debug("Duplicating branch '%s' to '%s'..." % ((lambda _coconut_none_coalesce_item: ("b%d" % _.branch) if _coconut_none_coalesce_item is None else _coconut_none_coalesce_item)(_.branches[_.branch].name), ("b%d" % branch if name is None else name)))  # line 193
        tracked = [t for t in _.branches[_.branch].tracked]  # copy  # line 194
        os.makedirs(os.path.join(_.root, metaFolder, "b%d" % branch, "r0"))  # line 195
        _.loadBranch(_.branch)  # line 196
        revision = max(_.commits)  # type: int  # line 197
        _.computeSequentialPathSet(_.branch, revision)  # full set of files in revision to _.paths  # line 198
        for path, pinfo in _.paths.items():  # line 199
            _.copyVersionedFile(_.branch, revision, branch, 0, pinfo)  # line 200
        _.commits = {0: CommitInfo(0, longint(time.time() * 1000), "Branched from '%s'" % ((lambda _coconut_none_coalesce_item: "b%d" % _.branch if _coconut_none_coalesce_item is None else _coconut_none_coalesce_item)(_.branches[_.branch].name)))}  # store initial commit  # line 201
        _.saveBranch(branch)  # save branch meta data to branch folder  # line 202
        _.saveCommit(branch, 0)  # save commit meta data to revision folder  # line 203
        _.branches[branch] = BranchInfo(branch, _.commits[0].ctime, name, _.branches[_.branch].inSync, tracked)  # save branch info, before storing repo state at caller  # line 204

    def createBranch(_, branch: 'int', name: '_coconut.typing.Optional[str]'=None, initialMessage: '_coconut.typing.Optional[str]'=None):  # line 206
        ''' Create a new branch from current file tree. This clears all known commits and modifies the file system.
        branch: target branch (should not exist yet)
        name: optional name of new branch
        _.branch: current branch, must exist already
    '''  # line 211
        simpleMode = not (_.track or _.picky)  # line 212
        tracked = [t for t in _.branches[_.branch].tracked] if _.track and len(_.branches) > 0 else []  # in case of initial branch creation  # line 213
        debug((lambda _coconut_none_coalesce_item: "b%d" % branch if _coconut_none_coalesce_item is None else _coconut_none_coalesce_item)("Creating branch '%s'..." % name))  # line 214
        _.paths = {}  # type: Dict[str, PathInfo]  # line 215
        if simpleMode:  # branches from file system state  # line 216
            changes = _.findChanges(branch, 0, progress=simpleMode)  # type: ChangeSet  # creates revision folder and versioned files  # line 217
            _.listChanges(changes)  # line 218
            _.paths.update(changes.additions.items())  # line 219
        else:  # tracking or picky mode: branch from lastest revision  # line 220
            os.makedirs(os.path.join(_.root, metaFolder, "b%d" % branch, "r0"))  # line 221
            if _.branch is not None:  # not immediately after "offline" - copy files from current branch  # line 222
                _.loadBranch(_.branch)  # line 223
                revision = max(_.commits)  # type: int  # TODO what if last switch was to an earlier revision? no persisting of last checkout  # line 224
                _.computeSequentialPathSet(_.branch, revision)  # full set of files in revision to _.paths  # line 225
                for path, pinfo in _.paths.items():  # line 226
                    _.copyVersionedFile(_.branch, revision, branch, 0, pinfo)  # line 227
        ts = longint(time.time() * 1000)  # line 228
        _.commits = {0: CommitInfo(0, ts, "Branched on %s" % strftime(ts) if initialMessage is None else initialMessage)}  # store initial commit for new branch  # line 229
        _.saveBranch(branch)  # save branch meta data (revisions) to branch folder  # line 230
        _.saveCommit(branch, 0)  # save commit meta data to revision folder  # line 231
        _.branches[branch] = BranchInfo(branch, _.commits[0].ctime, name, True if len(_.branches) == 0 else _.branches[_.branch].inSync, tracked)  # save branch info, in case it is needed  # line 232

    def removeBranch(_, branch: 'int') -> 'BranchInfo':  # line 234
        ''' Entirely remove a branch and all its revisions from the file system. '''  # line 235
        shutil.rmtree(os.path.join(_.root, metaFolder, "b%d" % branch))  # line 236
        binfo = _.branches[branch]  # line 237
        del _.branches[branch]  # line 238
        _.branch = max(_.branches)  # line 239
        _.saveBranches()  # line 240
        _.commits.clear()  # line 241
        return binfo  # line 242

    def loadCommit(_, branch: 'int', revision: 'int') -> 'None':  # line 244
        ''' Load all file information from a commit meta data. '''  # line 245
        with codecs.open(os.path.join(_.root, metaFolder, "b%d" % branch, "r%d" % revision, metaFile), "r", encoding=UTF8) as fd:  # line 246
            _.paths = json.load(fd)  # line 247
        _.paths = {path: PathInfo(*item) for path, item in _.paths.items()}  # re-create type info  # line 248
        _.branch = branch  # line 249

    def saveCommit(_, branch: 'int', revision: 'int'):  # line 251
        ''' Save all file information to a commit meta data file. '''  # line 252
        target = os.path.join(_.root, metaFolder, "b%d" % branch, "r%d" % revision)  # line 253
        try:  # line 254
            os.makedirs(target)  # line 254
        except:  # line 255
            pass  # line 255
        with codecs.open(os.path.join(target, metaFile), "w", encoding=UTF8) as fd:  # line 256
            json.dump(_.paths, fd, ensure_ascii=False)  # line 257

    def findChanges(_, branch: '_coconut.typing.Optional[int]'=None, revision: '_coconut.typing.Optional[int]'=None, checkContent: 'bool'=False, inverse: 'bool'=False, considerOnly: '_coconut.typing.Optional[FrozenSet[str]]'=None, dontConsider: '_coconut.typing.Optional[FrozenSet[str]]'=None, progress: 'bool'=False) -> 'ChangeSet':  # line 259
        ''' Find changes on the file system vs. in-memory paths (which should reflect the latest commit state).
        Only if both branch and revision are *not* None, write modified/added files to the specified revision folder (thus creating a new revision)
        The function returns the state of file tree *differences*, unless "inverse" is True -> then return original data
        checkContent: also computes file content hashes
        inverse: retain original state (size, mtime, hash) instead of updated one
        considerOnly: set of tracking patterns. None for simple mode. For update operation, consider union of other and current branch
        dontConsider: set of tracking patterns to not consider in changes
        progress: Show file names during processing
    '''  # line 268
        write = branch is not None and revision is not None  # line 269
        if write:  # line 270
            os.makedirs(os.path.join(_.root, metaFolder, "b%d" % branch, "r%d" % revision))  # line 270
        changes = ChangeSet({}, {}, {})  # type: ChangeSet  # line 271
        counter = Counter(-1)  # type: Counter  # line 272
        timer = time.time()  # line 272
        hashed = None  # type: _coconut.typing.Optional[str]  # line 273
        written = None  # type: longint  # line 273
        compressed = 0  # type: longint  # line 273
        original = 0  # type: longint  # line 273
        knownPaths = collections.defaultdict(list)  # type: Dict[str, List[str]]  # line 274
        for path, pinfo in _.paths.items():  # line 275
            if pinfo.size is not None and (considerOnly is None or any((path[:path.rindex(SLASH)] == pattern[:pattern.rindex(SLASH)] and fnmatch.fnmatch(path[path.rindex(SLASH) + 1:], pattern[pattern.rindex(SLASH) + 1:]) for pattern in considerOnly))) and (dontConsider is None or not any((path[:path.rindex(SLASH)] == pattern[:pattern.rindex(SLASH)] and fnmatch.fnmatch(path[path.rindex(SLASH) + 1:], pattern[pattern.rindex(SLASH) + 1:]) for pattern in dontConsider))):  # line 276
                knownPaths[os.path.dirname(path)].append(os.path.basename(path))  # TODO reimplement using fnmatch.filter and set operations for all files per path for speed  # line 279
        for path, dirnames, filenames in os.walk(_.root):  # line 280
            dirnames[:] = [f for f in dirnames if len([n for n in _.c.ignoreDirs if fnmatch.fnmatch(f, n)]) == 0 or len([p for p in _.c.ignoreDirsWhitelist if fnmatch.fnmatch(f, p)]) > 0]  # line 281
            filenames[:] = [f for f in filenames if len([n for n in _.c.ignores if fnmatch.fnmatch(f, n)]) == 0 or len([p for p in _.c.ignoresWhitelist if fnmatch.fnmatch(f, p)]) > 0]  # line 282
            dirnames.sort()  # line 283
            filenames.sort()  # line 283
            relPath = os.path.relpath(path, _.root).replace(os.sep, SLASH)  # line 284
            walk = filenames if considerOnly is None else list(reduce(lambda last, pattern: last | set(fnmatch.filter(filenames, os.path.basename(pattern))), (p for p in considerOnly if os.path.dirname(p).replace(os.sep, SLASH) == relPath), _coconut.set()))  # line 285
            if dontConsider:  # line 286
                walk[:] = [fn for fn in walk if not any((fnmatch.fnmatch(fn, os.path.basename(p)) for p in dontConsider if os.path.dirname(p).replace(os.sep, SLASH) == relPath))]  # line 287
            for file in walk:  # if m.track or m.picky: only files that match any path-relevant tracking patterns  # line 288
                filename = relPath + SLASH + file  # line 289
                filepath = os.path.join(path, file)  # line 290
                stat = os.stat(filepath)  # line 291
                size, mtime, newtime = stat.st_size, longint(stat.st_mtime * 1000), time.time()  # line 292
                if progress and newtime - timer > .1:  # line 293
                    outstring = "\rPreparing %s  %s" % (PROGRESS_MARKER[counter.inc() % 4], filename)  # line 294
                    sys.stdout.write(outstring + " " * max(0, termWidth - len(outstring)))  # TODO could write to new line instead of carriage return (still true?)  # line 295
                    sys.stdout.flush()  # TODO could write to new line instead of carriage return (still true?)  # line 295
                    timer = newtime  # TODO could write to new line instead of carriage return (still true?)  # line 295
                if filename not in _.paths:  # detected file not present (or untracked) in (other) branch  # line 296
                    nameHash = hashStr(filename)  # line 297
                    hashed, written = hashFile(filepath, _.compress, saveTo=os.path.join(_.root, metaFolder, "b%d" % branch, "r%d" % revision, nameHash) if write else None) if size > 0 else (None, 0)  # line 298
                    changes.additions[filename] = PathInfo(nameHash, size, mtime, hashed)  # line 299
                    compressed += written  # line 300
                    original += size  # line 300
                    continue  # line 301
                last = _.paths[filename]  # filename is known - check for modifications  # line 302
                if last.size is None:  # was removed before but is now added back - does not apply for tracking mode (which never marks files for removal in the history)  # line 303
                    hashed, written = hashFile(filepath, _.compress, saveTo=os.path.join(_.root, metaFolder, "b%d" % branch, "r%d" % revision, last.nameHash) if write else None) if size > 0 else (None, 0)  # line 304
                    changes.additions[filename] = PathInfo(last.nameHash, size, mtime, hashed)  # line 305
                    continue  # line 305
                elif size != last.size or mtime != last.mtime or (checkContent and hashFile(filepath, _.compress)[0] != last.hash):  # detected a modification  # line 306
                    hashed, written = hashFile(filepath, _.compress, saveTo=os.path.join(_.root, metaFolder, "b%d" % branch, "r%d" % revision, last.nameHash) if write else None) if (last.size if inverse else size) > 0 else (last.hash if inverse else None, 0)  # line 307
                    changes.modifications[filename] = PathInfo(last.nameHash, last.size if inverse else size, last.mtime if inverse else mtime, hashed)  # line 308
                else:  # line 309
                    continue  # line 309
                compressed += written  # line 310
                original += last.size if inverse else size  # line 310
            if relPath in knownPaths:  # at least one file is tracked  # line 311
                knownPaths[relPath][:] = list(set(knownPaths[relPath]) - set(walk))  # at least one file is tracked  # line 311
        for path, names in knownPaths.items():  # all paths that weren't walked by  # line 312
            for file in names:  # line 313
                changes.deletions[path + SLASH + file] = _.paths[path + SLASH + file]  # line 313
        if progress:  # force new line  # line 314
            print("\rPreparation finished. Compression factor %s" % ("is %.1f" % (original * 100. / compressed) if compressed > 0 else "cannot be computed").ljust(termWidth), file=sys.stdout)  # force new line  # line 314
        else:  # line 315
            debug("Finished detecting changes. Compression factor %s" % ("is %.1f" % (original * 100. / compressed) if compressed > 0 else "cannot be computed"))  # line 315
        return changes  # line 316

    def integrateChangeset(_, changes: 'ChangeSet', clear=False) -> 'None':  # line 318
        ''' In-memory update from a changeset, marking deleted files with size=None. Use clear = True to start on an empty path set. '''  # line 319
        if clear:  # line 320
            _.paths.clear()  # line 320
        else:  # line 321
            rm = [p for p, info in _.paths.items() if info.size is None]  # remove files deleted in earlier change sets (revisions)  # line 322
            for old in rm:  # remove previously removed entries completely  # line 323
                del _.paths[old]  # remove previously removed entries completely  # line 323
        for d, info in changes.deletions.items():  # mark now removed entries as deleted  # line 324
            _.paths[d] = PathInfo(info.nameHash, None, info.mtime, None)  # mark now removed entries as deleted  # line 324
        _.paths.update(changes.additions)  # line 325
        _.paths.update(changes.modifications)  # line 326

    def computeSequentialPathSet(_, branch: 'int', revision: 'int') -> 'None':  # line 328
        next(_.computeSequentialPathSetIterator(branch, revision, incrementally=False))  # simply invoke the generator once  # line 329

    def computeSequentialPathSetIterator(_, branch: 'int', revision: 'int', incrementally: 'bool'=True) -> '_coconut.typing.Optional[Iterator[ChangeSet]]':  # line 331
        ''' In-memory computation of current list of valid PathInfo entries for specified branch and until specified revision (inclusively) by traversing revision on the file system. '''  # line 332
        _.loadCommit(branch, 0)  # load initial paths  # line 333
        if incrementally:  # line 334
            yield diffPathSets({}, _.paths)  # line 334
        n = Metadata(_.root)  # type: Metadata  # next changes  # line 335
        for revision in range(1, revision + 1):  # line 336
            n.loadCommit(branch, revision)  # line 337
            changes = diffPathSets(_.paths, n.paths)  # type: ChangeSet  # line 338
            _.integrateChangeset(changes)  # line 339
            if incrementally:  # line 340
                yield changes  # line 340
        yield None  # for the default case - not incrementally  # line 341

    def parseRevisionString(_, argument: 'str') -> 'Tuple[_coconut.typing.Optional[int], _coconut.typing.Optional[int]]':  # line 343
        ''' Commit identifiers can be str or int for branch, and int for revision.
        Revision identifiers can be negative, with -1 being last commit.
    '''  # line 346
        if argument is None or argument == SLASH:  # no branch/revision specified  # line 347
            return (_.branch, -1)  # no branch/revision specified  # line 347
        argument = argument.strip()  # line 348
        if argument.startswith(SLASH):  # current branch  # line 349
            return (_.branch, _.getRevisionByName(argument[1:]))  # current branch  # line 349
        if argument.endswith(SLASH):  # line 350
            try:  # line 351
                return (_.getBranchByName(argument[:-1]), -1)  # line 351
            except ValueError:  # line 352
                Exit("Unknown branch label '%s'" % argument)  # line 352
        if SLASH in argument:  # line 353
            b, r = argument.split(SLASH)[:2]  # line 354
            try:  # line 355
                return (_.getBranchByName(b), _.getRevisionByName(r))  # line 355
            except ValueError:  # line 356
                Exit("Unknown branch label or wrong number format '%s/%s'" % (b, r))  # line 356
        branch = _.getBranchByName(argument)  # type: int  # returns number if given (revision) integer  # line 357
        if branch not in _.branches:  # line 358
            branch = None  # line 358
        try:  # either branch name/number or reverse/absolute revision number  # line 359
            return (_.branch if branch is None else branch, longint(argument if argument else "-1") if branch is None else -1)  # either branch name/number or reverse/absolute revision number  # line 359
        except:  # line 360
            Exit("Unknown branch label or wrong number format")  # line 360
        Exit("This should never happen")  # line 361
        return (None, None)  # line 361

    def findRevision(_, branch: 'int', revision: 'int', nameHash: 'str') -> 'Tuple[int, str]':  # line 363
        while True:  # find latest revision that contained the file physically  # line 364
            source = os.path.join(_.root, metaFolder, "b%d" % branch, "r%d" % revision, nameHash)  # type: str  # line 365
            if os.path.exists(source) and os.path.isfile(source):  # line 366
                break  # line 366
            revision -= 1  # line 367
            if revision < 0:  # line 368
                Exit("Cannot determine versioned file '%s' from specified branch '%d'" % (nameHash, branch))  # line 368
        return revision, source  # line 369

    def copyVersionedFile(_, branch: 'int', revision: 'int', toBranch: 'int', toRevision: 'int', pinfo: 'PathInfo') -> 'None':  # line 371
        ''' Copy versioned file to other branch/revision. '''  # line 372
        target = os.path.join(_.root, metaFolder, "b%d" % toBranch, "r%d" % toRevision, pinfo.nameHash)  # type: str  # line 373
        revision, source = _.findRevision(branch, revision, pinfo.nameHash)  # line 374
        shutil.copy2(source, target)  # line 375

    def readOrCopyVersionedFile(_, branch: 'int', revision: 'int', nameHash: 'str', toFile: '_coconut.typing.Optional[str]'=None) -> '_coconut.typing.Optional[bytes]':  # line 377
        ''' Return file contents, or copy contents into file path provided. '''  # line 378
        source = os.path.join(_.root, metaFolder, "b%d" % branch, "r%d" % revision, nameHash)  # type: str  # line 379
        try:  # line 380
            with openIt(source, "r", _.compress) as fd:  # line 381
                if toFile is None:  # read bytes into memory and return  # line 382
                    return fd.read()  # read bytes into memory and return  # line 382
                with open(toFile, "wb") as to:  # line 383
                    while True:  # line 384
                        buffer = fd.read(bufSize)  # line 385
                        to.write(buffer)  # line 386
                        if len(buffer) < bufSize:  # line 387
                            break  # line 387
                    return None  # line 388
        except Exception as E:  # line 389
            warn("Cannot read versioned file: %r (%d/%d/%s)" % (E, branch, revision, nameHash))  # line 389
        return None  # line 390

    def restoreFile(_, relPath: '_coconut.typing.Optional[str]', branch: 'int', revision: 'int', pinfo: 'PathInfo', ensurePath: 'bool'=False) -> '_coconut.typing.Optional[bytes]':  # line 392
        ''' Recreate file for given revision, or return contents if path is None. '''  # line 393
        if relPath is None:  # just return contents  # line 394
            return _.readOrCopyVersionedFile(branch, _.findRevision(branch, revision, pinfo.nameHash)[0], pinfo.nameHash) if pinfo.size > 0 else b''  # just return contents  # line 394
        target = os.path.join(_.root, relPath.replace(SLASH, os.sep))  # type: str  # line 395
        if ensurePath:  #  and not os.path.exists(os.path.dirname(target)):  # line 396
            try:  # line 397
                os.makedirs(os.path.dirname(target))  # line 397
            except:  # line 398
                pass  # line 398
        if pinfo.size == 0:  # line 399
            with open(target, "wb"):  # line 400
                pass  # line 400
            try:  # update access/modification timestamps on file system  # line 401
                os.utime(target, (pinfo.mtime / 1000., pinfo.mtime / 1000.))  # update access/modification timestamps on file system  # line 401
            except Exception as E:  # line 402
                error("Cannot update file's timestamp after restoration '%r'" % E)  # line 402
            return None  # line 403
        revision, source = _.findRevision(branch, revision, pinfo.nameHash)  # line 404
# Restore file by copying buffer-wise
        with openIt(source, "r", _.compress) as fd, open(target, "wb") as to:  # using Coconut's Enhanced Parenthetical Continuation  # line 406
            while True:  # line 407
                buffer = fd.read(bufSize)  # line 408
                to.write(buffer)  # line 409
                if len(buffer) < bufSize:  # line 410
                    break  # line 410
        try:  # update access/modification timestamps on file system  # line 411
            os.utime(target, (pinfo.mtime / 1000., pinfo.mtime / 1000.))  # update access/modification timestamps on file system  # line 411
        except Exception as E:  # line 412
            error("Cannot update file's timestamp after restoration '%r'" % E)  # line 412
        return None  # line 413

    def getTrackingPatterns(_, branch: '_coconut.typing.Optional[int]'=None) -> 'FrozenSet[str]':  # line 415
        ''' Returns list of tracking patterns for provided branch or current branch. '''  # line 416
        return _coconut.frozenset() if not _.track and not _.picky else frozenset(_.branches[_.branch if branch is None else branch].tracked)  # line 417


# Main client operations
def offline(argument: '_coconut.typing.Optional[str]'=None, options: '_coconut.typing.Sequence[str]'=[]) -> 'None':  # line 421
    ''' Initial command to start working offline. '''  # line 422
    if os.path.exists(metaFolder):  # line 423
        if '--force' not in options:  # line 424
            Exit("Repository folder is either already offline or older branches and commits were left over.\nUse 'sos online' to check for dirty branches, or\nWipe existing offline branches with 'sos offline --force'")  # line 424
        try:  # line 425
            for entry in os.listdir(metaFolder):  # line 426
                resource = metaFolder + os.sep + entry  # line 427
                if os.path.isdir(resource):  # line 428
                    shutil.rmtree(resource)  # line 428
                else:  # line 429
                    os.unlink(resource)  # line 429
        except:  # line 430
            Exit("Cannot reliably remove previous repository contents. Please remove .sos folder manually prior to going offline")  # line 430
    m = Metadata(os.getcwd())  # type: Metadata  # line 431
    if '--plain' in options or not m.c.compress:  # plain file copies instead of compressed ones  # line 432
        m.compress = False  # plain file copies instead of compressed ones  # line 432
    if '--picky' in options or m.c.picky:  # Git-like  # line 433
        m.picky = True  # Git-like  # line 433
    elif '--track' in options or m.c.track:  # Svn-like  # line 434
        m.track = True  # Svn-like  # line 434
    if '--strict' in options or m.c.strict:  # always hash contents  # line 435
        m.strict = True  # always hash contents  # line 435
    debug("Preparing offline repository...")  # line 436
    m.createBranch(0, str(defaults["defaultbranch"]) if argument is None else argument, initialMessage="Offline repository created on %s" % strftime())  # main branch's name may be None (e.g. for fossil)  # line 437
    m.branch = 0  # line 438
    m.saveBranches()  # no change immediately after going offline, going back online won't issue a warning  # line 439
    info("Offline repository prepared. Use 'sos online' to finish offline work")  # line 440

def online(options: '_coconut.typing.Sequence[str]'=[]) -> 'None':  # line 442
    ''' Finish working offline. '''  # line 443
    force = '--force' in options  # type: bool  # line 444
    m = Metadata(os.getcwd())  # line 445
    m.loadBranches()  # line 446
    if any([not b.inSync for b in m.branches.values()]) and not force:  # line 447
        Exit("There are still unsynchronized (dirty) branches.\nUse 'sos log' to list them.\nUse 'sos commit' and 'sos switch' to commit dirty branches to your VCS before leaving offline mode.\nUse 'sos online --force' to erase all aggregated offline revisions")  # line 447
    strict = '--strict' in options or m.strict  # type: bool  # line 448
    if options.count("--force") < 2:  # line 449
        changes = m.findChanges(checkContent=strict, considerOnly=None if not m.track and not m.picky else m.getTrackingPatterns())  # type: ChangeSet  # HINT no option for --only/--except here on purpose. No check for picky here, because online is not a command that considers staged files (but we could use --only here, alternatively)  # line 450
        if modified(changes):  # line 451
            Exit("File tree is modified vs. current branch.\nUse 'sos online --force --force' to continue with removing the offline repository")  # line 451
    try:  # line 452
        shutil.rmtree(metaFolder)  # line 452
        info("Exited offline mode. Continue working with your traditional VCS.")  # line 452
    except Exception as E:  # line 453
        Exit("Error removing offline repository: %r" % E)  # line 453

def branch(argument: '_coconut.typing.Optional[str]'=None, options: '_coconut.typing.Sequence[str]'=[]) -> 'None':  # line 455
    ''' Create a new branch (from file tree or last revision) and (by default) continue working on it. '''  # line 456
    last = '--last' in options  # type: bool  # use last revision for branching, not current file tree  # line 457
    stay = '--stay' in options  # type: bool  # continue on current branch after branching  # line 458
    force = '--force' in options  # type: bool  # branch even with local modifications  # line 459
    m = Metadata(os.getcwd())  # type: Metadata  # line 460
    m.loadBranches()  # line 461
    m.loadBranch(m.branch)  # line 462
    if argument and m.getBranchByName(argument) is not None:  # create a named branch  # line 463
        Exit("Branch '%s' already exists. Cannot proceed" % argument)  # create a named branch  # line 463
    branch = max(m.branches.keys()) + 1  # next branch's key - this isn't atomic but we assume single-user non-concurrent use here  # line 464
    debug("Branching to %sbranch b%02d%s%s..." % ("unnamed " if argument is None else "", branch, " '%s'" % argument if argument else "", " from last revision" if last else ""))  # line 465
    if last:  # line 466
        m.duplicateBranch(branch, "Branched from r%02d/b%02d" % (m.branch, max(m.commits.keys())) if argument is None else argument)  # branch from branch's last revision  # line 467
    else:  # from file tree state  # line 468
        m.createBranch(branch, "Branched from r%02d/b%02d" % (m.branch, max(m.commits.keys())) if argument is None else argument)  # branch from current file tree  # line 469
    if not stay:  # line 470
        m.branch = branch  # line 471
        m.saveBranches()  # line 472
    info("%s new %sbranch b%02d%s" % ("Continue work after branching" if stay else "Switched to", "unnamed " if argument is None else "", branch, " '%s'" % argument if argument else ""))  # line 473

def changes(argument: 'str'=None, options: '_coconut.typing.Sequence[str]'=[], onlys: '_coconut.typing.Optional[FrozenSet[str]]'=None, excps: '_coconut.typing.Optional[FrozenSet[str]]'=None) -> 'ChangeSet':  # line 475
    ''' Show changes of file tree vs. (last or specified) revision on current or specified branch. '''  # line 476
    m = Metadata(os.getcwd())  # type: Metadata  # line 477
    branch = None  # type: _coconut.typing.Optional[int]  # line 477
    revision = None  # type: _coconut.typing.Optional[int]  # line 477
    m.loadBranches()  # knows current branch  # line 478
    strict = '--strict' in options or m.strict  # type: bool  # line 479
    branch, revision = m.parseRevisionString(argument)  # line 480
    if branch not in m.branches:  # line 481
        Exit("Unknown branch")  # line 481
    m.loadBranch(branch)  # knows commits  # line 482
    revision = revision if revision >= 0 else len(m.commits) + revision  # negative indexing  # line 483
    if revision < 0 or revision > max(m.commits):  # line 484
        Exit("Unknown revision r%02d" % revision)  # line 484
    info("//|\\\\ Changes of file tree vs. revision '%s/r%02d'" % ((lambda _coconut_none_coalesce_item: "b%02d" % branch if _coconut_none_coalesce_item is None else _coconut_none_coalesce_item)(m.branches[branch].name), revision))  # line 485
    m.computeSequentialPathSet(branch, revision)  # load all commits up to specified revision  # line 486
    changes = m.findChanges(checkContent=strict, considerOnly=onlys if not m.track and not m.picky else conditionalIntersection(onlys, m.getTrackingPatterns() | m.getTrackingPatterns(branch)), dontConsider=excps)  # type: ChangeSet  # line 487
    m.listChanges(changes)  # line 488
    return changes  # for unit tests only  # line 489

def diff(argument: 'str'="", options: '_coconut.typing.Sequence[str]'=[], onlys: '_coconut.typing.Optional[FrozenSet[str]]'=None, excps: '_coconut.typing.Optional[FrozenSet[str]]'=None) -> 'None':  # line 491
    ''' Show text file differences of file tree vs. (last or specified) revision on current or specified branch. '''  # line 492
    m = Metadata(os.getcwd())  # type: Metadata  # line 493
    branch = None  # type: _coconut.typing.Optional[int]  # line 493
    revision = None  # type: _coconut.typing.Optional[int]  # line 493
    m.loadBranches()  # knows current branch  # line 494
    strict = '--strict' in options or m.strict  # type: bool  # line 495
    _from = {None: option.split("--from=")[1] for option in options if options.startswith("--from=")}.get(None, None)  # type: _coconut.typing.Optional[str]  # line 496
    branch, revision = m.parseRevisionString(argument)  # if nothing given, use last commit  # line 497
    if branch not in m.branches:  # line 498
        Exit("Unknown branch")  # line 498
    m.loadBranch(branch)  # knows commits  # line 499
    revision = revision if revision >= 0 else len(m.commits) + revision  # negative indexing  # line 500
    if revision < 0 or revision > max(m.commits):  # line 501
        Exit("Unknown revision r%02d" % revision)  # line 501
    info("//|\\\\ Differences of file tree vs. revision '%s/r%02d'" % ((lambda _coconut_none_coalesce_item: "b%02d" % branch if _coconut_none_coalesce_item is None else _coconut_none_coalesce_item)(m.branches[branch].name), revision))  # line 502
    m.computeSequentialPathSet(branch, revision)  # load all commits up to specified revision  # line 503
    changes = m.findChanges(checkContent=strict, inverse=True, considerOnly=onlys if not m.track and not m.picky else conditionalIntersection(onlys, m.getTrackingPatterns() | m.getTrackingPatterns(branch)), dontConsider=excps)  # type: ChangeSet  # line 504
    onlyBinaryModifications = dataCopy(ChangeSet, changes, modifications={k: v for k, v in changes.modifications.items() if not m.isTextType(os.path.basename(k))})  # type: ChangeSet  # line 505
    if modified(onlyBinaryModifications):  # line 506
        debug("//|\\\\ File changes")  # line 506
    m.listChanges(onlyBinaryModifications)  # only list modified binary files  # line 507

    if changes.modifications:  # line 509
        debug("%s//|\\\\ Textual modifications" % ("\n" if modified(onlyBinaryModifications) else ""))  # line 509
    for path, pinfo in (c for c in changes.modifications.items() if m.isTextType(os.path.basename(c[0]))):  # only consider modified text files  # line 510
        content = None  # type: _coconut.typing.Optional[bytes]  # ; othr:str[]; curr:str[]  # line 511
        if pinfo.size == 0:  # empty file contents  # line 512
            content = b""  # empty file contents  # line 512
        else:  # versioned file  # line 513
            content = m.restoreFile(None, branch, revision, pinfo)  # versioned file  # line 513
            assert content is not None  # versioned file  # line 513
        abspath = os.path.join(m.root, path.replace(SLASH, os.sep))  # current file  # line 514
        blocks = merge(file=content, intoname=abspath, diffOnly=True)  # type: List[MergeBlock]  # only determine change blocks  # line 515
        print("DIF %s%s" % (path, " <timestamp only>" if len(blocks) == 1 and blocks[0].tipe == MergeBlockType.KEEP else ""))  # line 516
        for block in blocks:  # line 517
            if block.tipe in [MergeBlockType.INSERT, MergeBlockType.REMOVE]:  # line 518
                pass  # TODO print some previous and following lines - which aren't accessible here anymore  # line 519
            if block.tipe == MergeBlockType.INSERT:  # TODO show color via (n)curses or other library?  # line 520
                for no, line in enumerate(block.lines):  # line 521
                    print("+++ %04d |%s|" % (no + block.line, line))  # line 522
            elif block.tipe == MergeBlockType.REMOVE:  # line 523
                for no, line in enumerate(block.lines):  # line 524
                    print("--- %04d |%s|" % (no + block.line, line))  # line 525
            elif block.tipe in [MergeBlockType.REPLACE, MergeBlockType.MODIFY]:  # TODO for MODIFY also show intra-line change ranges  # line 526
                for no, line in enumerate(block.replaces.lines):  # line 527
                    print("- | %04d |%s|" % (no + block.replaces.line, line))  # line 528
                for no, line in enumerate(block.lines):  # line 529
                    print("+ | %04d |%s|" % (no + block.line, line))  # line 530
#      elif block.tipe == MergeBlockType.KEEP: pass
#      elif block.tipe == MergeBlockType.MODIFY:  # intra-line modifications
#      elif block.tipe == MergeBlockType.MOVE:  # intra-line modifications

def commit(argument: '_coconut.typing.Optional[str]'=None, options: '_coconut.typing.Sequence[str]'=[], onlys: '_coconut.typing.Optional[FrozenSet[str]]'=None, excps: '_coconut.typing.Optional[FrozenSet[str]]'=None) -> 'None':  # line 535
    ''' Create new revision from file tree changes vs. last commit. '''  # line 536
    m = Metadata(os.getcwd())  # type: Metadata  # line 537
    m.loadBranches()  # knows current branch  # line 538
    if argument is not None and argument in m.tags:  # line 539
        Exit("Illegal commit message. It was already used as a tag name")  # line 539
    trackingPatterns = m.getTrackingPatterns()  # type: FrozenSet[str]  # SVN-like mode  # line 540
    if m.picky and not trackingPatterns:  # line 541
        Exit("No file patterns staged for commit in picky mode")  # line 541
    changes = None  # type: ChangeSet  # line 542
    m, branch, revision, changes, strict, force, trackingPatterns = exitOnChanges(None, options, commit=True, onlys=onlys, excps=excps)  # special flag creates new revision for detected changes, but abort if no changes  # line 543
    info((lambda _coconut_none_coalesce_item: "b%d" % m.branch if _coconut_none_coalesce_item is None else _coconut_none_coalesce_item)("Committing changes to branch '%s'..." % m.branches[m.branch].name))  # line 544
    m.integrateChangeset(changes, clear=True)  # update pathset to changeset only  # line 545
    m.saveCommit(m.branch, revision)  # revision has already been incremented  # line 546
    m.commits[revision] = CommitInfo(revision, longint(time.time() * 1000), argument)  # comment can be None  # line 547
    m.saveBranch(m.branch)  # line 548
    m.loadBranches()  # TODO is it necessary to load again?  # line 549
    if m.picky:  # line 550
        m.branches[m.branch] = dataCopy(BranchInfo, m.branches[m.branch], tracked=[], inSync=False)  # remove tracked patterns  # line 551
    else:  # track or simple mode  # line 552
        m.branches[m.branch] = dataCopy(BranchInfo, m.branches[m.branch], inSync=False)  # set branch dirty  # line 553
    if "--tag" in options and argument is not None:  # memorize unique tag  # line 554
        m.tags.append(argument)  # memorize unique tag  # line 554
    m.saveBranches()  # line 555
    info("Created new revision r%02d%s (+%02d/-%02d/*%02d)" % (revision, ((" '%s'" % argument) if argument is not None else ""), len(changes.additions), len(changes.deletions), len(changes.modifications)))  # line 556

def status() -> 'None':  # line 558
    ''' Show branches and current repository state. '''  # line 559
    m = Metadata(os.getcwd())  # type: Metadata  # line 560
    m.loadBranches()  # knows current branch  # line 561
    current = m.branch  # type: int  # line 562
    info("//|\\\\ Offline repository status")  # line 563
    print("Content checking %sactivated" % ("" if m.strict else "de"))  # line 564
    print("Data compression %sactivated" % ("" if m.compress else "de"))  # line 565
    print("Repository is in %s mode" % ("tracking" if m.track else ("picky" if m.picky else "simple")))  # line 566
    sl = max([len((lambda _coconut_none_coalesce_item: "" if _coconut_none_coalesce_item is None else _coconut_none_coalesce_item)(b.name)) for b in m.branches.values()])  # type: int  # line 567
    for branch in sorted(m.branches.values(), key=lambda b: b.number):  # line 568
        m.loadBranch(branch.number)  # knows commit history  # line 569
        print("  %s b%02d%s @%s (%s) with %d commits%s" % ("*" if current == branch.number else " ", branch.number, ((" %%%ds" % (sl + 2)) % ("'%s'" % branch.name)) if branch.name else "", strftime(branch.ctime), "in sync" if branch.inSync else "dirty", len(m.commits), ". Last comment: '%s'" % m.commits[max(m.commits)].message if m.commits[max(m.commits)].message else ""))  # line 570
    if m.track or m.picky and len(m.branches[m.branch].tracked) > 0:  # line 571
        info("\nTracked file patterns:")  # line 572
        print(ajoin("  | ", m.branches[m.branch].tracked, "\n"))  # line 573

def exitOnChanges(argument: '_coconut.typing.Optional[str]'=None, options: '_coconut.typing.Sequence[str]'=[], check: 'bool'=True, commit: 'bool'=False, onlys: '_coconut.typing.Optional[FrozenSet[str]]'=None, excps: '_coconut.typing.Optional[FrozenSet[str]]'=None) -> 'Tuple[Metadata, _coconut.typing.Optional[int], int, ChangeSet, bool, bool, FrozenSet[str]]':  # line 575
    ''' Common behavior for switch, update, delete, commit.
      Should not be called for picky mode, unless tracking patterns were added.
      check: stop program on detected change
      commit: don't stop on changes, because that's what we need in the operation
      Returns (Metadata, (current or target) branch, revision, set of changes vs. last commit on current branch, strict, force flags. '''  # line 580
    m = Metadata(os.getcwd())  # type: Metadata  # line 581
    m.loadBranches()  # knows current branch  # line 582
    force = '--force' in options  # type: bool  # line 583
    strict = '--strict' in options or m.strict  # type: bool  # line 584
    if argument is not None:  # line 585
        branch, revision = m.parseRevisionString(argument)  # for early abort  # line 586
        if branch is None:  # line 587
            Exit("Branch '%s' doesn't exist. Cannot proceed" % argument)  # line 587
    m.loadBranch(m.branch)  # knows last commits of *current* branch  # line 588

# Determine current changes
    trackingPatterns = m.getTrackingPatterns()  # type: FrozenSet[str]  # line 591
    m.computeSequentialPathSet(m.branch, max(m.commits))  # load all commits up to specified revision  # line 592
    changes = m.findChanges(m.branch if commit else None, max(m.commits) + 1 if commit else None, checkContent=strict, considerOnly=onlys if not (m.track or m.picky) else conditionalIntersection(onlys, trackingPatterns), dontConsider=excps)  # type: ChangeSet  # line 593
    if check and modified(changes) and not force:  # line 594
        m.listChanges(changes)  # line 595
        if not commit:  # line 596
            Exit("File tree contains changes. Use --force to proceed")  # line 596
    elif commit and not force:  #  and not check  # line 597
        Exit("Nothing to commit")  #  and not check  # line 597

    if argument is not None:  # branch/revision specified  # line 599
        m.loadBranch(branch)  # knows commits of target branch  # line 600
        revision = revision if revision >= 0 else len(m.commits) + revision  # negative indexing  # line 601
        if revision < 0 or revision > max(m.commits):  # line 602
            Exit("Unknown revision r%02d" % revision)  # line 602
        return (m, branch, revision, changes, strict, force, m.getTrackingPatterns(branch))  # line 603
    return (m, m.branch, max(m.commits) + (1 if commit else 0), changes, strict, force, trackingPatterns)  # line 604

def switch(argument: 'str', options: '_coconut.typing.Sequence[str]'=[], onlys: '_coconut.typing.Optional[FrozenSet[str]]'=None, excps: '_coconut.typing.Optional[FrozenSet[str]]'=None) -> 'None':  # line 606
    ''' Continue work on another branch, replacing file tree changes. '''  # line 607
    changes = None  # type: ChangeSet  # line 608
    m, branch, revision, changes, strict, force, trackingPatterns = exitOnChanges(argument, options)  # line 609
    info("//|\\\\ Switching to branch %sb%02d/r%02d" % ("'%s' " % m.branches[branch].name if m.branches[branch].name else "", branch, revision))  # line 610

# Determine file changes from other branch to current file tree
    if '--meta' in options:  # only switch meta data  # line 613
        m.branches[m.branch] = dataCopy(BranchInfo, m.branches[m.branch], tracked=m.branches[branch].tracked)  # line 614
    else:  # full file switch  # line 615
        m.computeSequentialPathSet(branch, revision)  # load all commits up to specified revision for target branch into memory  # line 616
        changes = m.findChanges(checkContent=strict, inverse=True, considerOnly=onlys if not m.track and not m.picky else conditionalIntersection(onlys, trackingPatterns | m.getTrackingPatterns(branch)), dontConsider=excps)  # determine difference of other branch vs. file tree (forced or in sync with current branch; "addition" means exists now and should be removed)  # line 617
        if not modified(changes):  # line 618
            info("No changes to current file tree")  # line 619
        else:  # integration required  # line 620
            for path, pinfo in changes.deletions.items():  # line 621
                m.restoreFile(path, branch, revision, pinfo, ensurePath=True)  # is deleted in current file tree: restore from branch to reach target  # line 622
                print("ADD " + path)  # line 623
            for path, pinfo in changes.additions.items():  # line 624
                os.unlink(os.path.join(m.root, path.replace(SLASH, os.sep)))  # is added in current file tree: remove from branch to reach target  # line 625
                print("DEL " + path)  # line 626
            for path, pinfo in changes.modifications.items():  # line 627
                m.restoreFile(path, branch, revision, pinfo)  # is modified in current file tree: restore from branch to reach target  # line 628
                print("MOD " + path)  # line 629
    m.branch = branch  # line 630
    m.saveBranches()  # store switched path info  # line 631
    info("Switched to branch %sb%02d/r%02d" % ("'%s' " % (m.branches[branch].name if m.branches[branch].name else ""), branch, revision))  # line 632

def update(argument: 'str', options: '_coconut.typing.Sequence[str]'=[], onlys: '_coconut.typing.Optional[FrozenSet[str]]'=None, excps: '_coconut.typing.Optional[FrozenSet[str]]'=None) -> 'None':  # line 634
    ''' Load and integrate a specified other branch/revision into current life file tree.
      In tracking mode, this also updates the set of tracked patterns.
      User options for merge operation: --add (don't remove), --rm (don't insert), --add-lines/--rm-lines (inside each file)
      User options for conflict resolution: --theirs/--mine/--ask
  '''  # line 639
    mrg = firstOfMap({"--add": MergeOperation.INSERT, "--rm": MergeOperation.REMOVE}, options, MergeOperation.BOTH)  # type: int  # default operation is replicate remove state for non-conflicting cases (insertions/deletions)  # line 640
    res = firstOfMap({'--theirs': ConflictResolution.THEIRS, '--mine': ConflictResolution.MINE}, options, ConflictResolution.NEXT)  # type: int  # NEXT means deeper level  # line 641
    mrgline = firstOfMap({'--add-lines': MergeOperation.INSERT, '--rm-lines': MergeOperation.REMOVE}, options, mrg)  # type: int  # default operation for modified files is same as for files  # line 642
    resline = firstOfMap({'--theirs-lines': ConflictResolution.THEIRS, '--mine-lines': ConflictResolution.MINE}, options, ConflictResolution.ASK)  # type: int  # line 643
    m = Metadata(os.getcwd())  # type: Metadata  # TODO same is called inside stop on changes - could return both current and designated branch instead  # line 644
    m.loadBranches()  # line 645
    changes = None  # type: ChangeSet  # line 645
    currentBranch = m.branch  # type: _coconut.typing.Optional[int]  # line 646
    m, branch, revision, changes, strict, force, trackingPatterns = exitOnChanges(argument, options, check=False, onlys=onlys, excps=excps)  # don't check for current changes, only parse arguments  # line 647
    debug("Integrating changes from '%s/r%02d' into file tree..." % ((lambda _coconut_none_coalesce_item: "b%02d" % branch if _coconut_none_coalesce_item is None else _coconut_none_coalesce_item)(m.branches[branch].name), revision))  # line 648

# Determine file changes from other branch over current file tree
    m.computeSequentialPathSet(branch, revision)  # load all commits up to specified revision for branch to integrate  # line 651
    trackingUnion = trackingPatterns | m.getTrackingPatterns(branch)  # type: FrozenSet[str]  # line 652
    changes = m.findChanges(checkContent=strict, inverse=True, considerOnly=onlys if not m.track and not m.picky else conditionalIntersection(onlys, trackingUnion), dontConsider=excps)  # determine difference of other branch vs. file tree. "addition" means exists now but not in other, and should be removed unless in tracking mode  # line 653
    if not (mrg & MergeOperation.INSERT and changes.additions or (mrg & MergeOperation.REMOVE and changes.deletions) or changes.modifications):  # no file ops  # line 654
        if trackingUnion != trackingPatterns:  # nothing added  # line 655
            info("No file changes detected, but tracking patterns were merged (run 'sos switch /-1 --meta' to undo)")  # TODO write test to see if this works  # line 656
        else:  # line 657
            info("Nothing to update")  # but write back updated branch info below  # line 658
    else:  # integration required  # line 659
        for path, pinfo in changes.deletions.items():  # deletions mark files not present in current file tree -> needs additon  # line 660
            if mrg & MergeOperation.INSERT:  # deleted in current file tree: restore from branch to reach target  # line 661
                m.restoreFile(path, branch, revision, pinfo, ensurePath=True)  # deleted in current file tree: restore from branch to reach target  # line 661
            print("ADD " + path if mrg & MergeOperation.INSERT else "(A) " + path)  # line 662
        for path, pinfo in changes.additions.items():  # line 663
            if m.track or m.picky:  # because untracked files of other branch cannot be detected (which is good)  # line 664
                Exit("This should never happen")  # because untracked files of other branch cannot be detected (which is good)  # line 664
            if mrg & MergeOperation.REMOVE:  # line 665
                os.unlink(m.root + os.sep + path.replace(SLASH, os.sep))  # line 665
            print("DEL " + path if mrg & MergeOperation.REMOVE else "(D) " + path)  # not contained in other branch, but maybe kept  # line 666
        for path, pinfo in changes.modifications.items():  # line 667
            into = os.path.join(m.root, path.replace(SLASH, os.sep))  # type: str  # line 668
            binary = not m.isTextType(path)  # line 669
            if res & ConflictResolution.ASK or (binary and res == ConflictResolution.NEXT):  # TODO this may ask user even if no interaction was asked for (check line level for interactivity fist)  # line 670
                print(("MOD " + path if not binary else "BIN ") + path)  # line 671
                reso = {"i": ConflictResolution.MINE, "t": ConflictResolution.THEIRS, "m": ConflictResolution.NEXT}.get(user_input(" Resolve: *M[I]ne, [T]heirs, [M]erge: (I)").strip().lower(), ConflictResolution.MINE)  # line 672
                debug("User selected %d" % reso)  # line 673
            else:  # line 674
                reso = res  # line 674
            if reso & ConflictResolution.THEIRS:  # line 675
                m.readOrCopyVersionedFile(branch, revision, pinfo.nameHash, toFile=into)  # blockwise copy of contents  # line 676
                print("THR " + path)  # line 677
            elif reso & ConflictResolution.MINE:  # line 678
                print("MNE " + path)  # nothing to do! same as skip  # line 679
            else:  # NEXT: line-based merge  # line 680
                file = m.readOrCopyVersionedFile(branch, revision, pinfo.nameHash) if pinfo.size > 0 else b''  # type: _coconut.typing.Optional[bytes]  # parse lines  # line 681
                if file is not None:  # if None, error message was already logged  # line 682
                    contents = merge(file=file, intoname=into, mergeOperation=mrgline, conflictResolution=resline)  # type: bytes  # line 683
                    with open(path, "wb") as fd:  # TODO write to temp file first, in case writing fails  # line 684
                        fd.write(contents)  # TODO write to temp file first, in case writing fails  # line 684
    info("Integrated changes from '%s/r%02d' into file tree" % ((lambda _coconut_none_coalesce_item: "b%02d" % branch if _coconut_none_coalesce_item is None else _coconut_none_coalesce_item)(m.branches[branch].name), revision))  # line 685
    m.branches[currentBranch] = dataCopy(BranchInfo, m.branches[currentBranch], inSync=False, tracked=list(trackingUnion))  # line 686
    m.branch = currentBranch  # need to restore setting before saving TODO operate on different objects instead  # line 687
    m.saveBranches()  # line 688

def delete(argument: 'str', options: '_coconut.typing.Sequence[str]'=[]) -> 'None':  # line 690
    ''' Remove a branch entirely. '''  # line 691
    m, branch, revision, changes, strict, force, trackingPatterns = exitOnChanges(None, options)  # line 692
    if len(m.branches) == 1:  # line 693
        Exit("Cannot remove the only remaining branch. Use 'sos online' to leave offline mode")  # line 693
    branch, revision = m.parseRevisionString(argument)  # not from exitOnChanges, because we have to set argument to None there  # line 694
    if branch is None or branch not in m.branches:  # line 695
        Exit("Unknown branch")  # line 695
    debug("Removing branch %d%s..." % (branch, " '%s'" % m.branches[branch].name if m.branches[branch].name else ""))  # line 696
    binfo = m.removeBranch(branch)  # need to keep a reference to removed entry for output below  # line 697
    info("Branch b%02d%s removed" % (branch, " '%s'" % binfo.name if binfo.name else ""))  # line 698

def add(relPath: 'str', pattern: 'str', options: '_coconut.typing.Sequence[str]'=[]) -> 'None':  # line 700
    ''' Add a tracked files pattern to current branch's tracked files. '''  # line 701
    force = '--force' in options  # type: bool  # line 702
    m = Metadata(os.getcwd())  # type: Metadata  # line 703
    m.loadBranches()  # line 704
    if not m.track and not m.picky:  # line 705
        Exit("Repository is in simple mode. Use 'offline --track' or 'offline --picky' instead")  # line 705
    if pattern in m.branches[m.branch].tracked:  # line 706
        Exit("Pattern '%s' already tracked" % pattern)  # line 706
    if not force and not os.path.exists(relPath.replace(SLASH, os.sep)):  # line 707
        Exit("The pattern folder doesn't exist. Use --force to add it anyway")  # line 707
    if not force and len(fnmatch.filter(os.listdir(os.path.abspath(relPath.replace(SLASH, os.sep))), os.path.basename(pattern.replace(SLASH, os.sep)))) == 0:  # doesn't match any current file  # line 708
        Exit("Pattern doesn't match any file in specified folder. Use --force to add it anyway")  # line 709
    m.branches[m.branch].tracked.append(pattern)  # line 710
    m.saveBranches()  # line 711
    info("Added tracking pattern '%s' for folder '%s'" % (os.path.basename(pattern.replace(SLASH, os.sep)), os.path.abspath(relPath)))  # line 712

def remove(relPath: 'str', pattern: 'str') -> 'None':  # line 714
    ''' Remove a tracked files pattern from current branch's tracked files. '''  # line 715
    m = Metadata(os.getcwd())  # type: Metadata  # line 716
    m.loadBranches()  # line 717
    if not m.track and not m.picky:  # line 718
        Exit("Repository is in simple mode. Needs 'offline --track' or 'offline --picky' instead")  # line 718
    if pattern not in m.branches[m.branch].tracked:  # line 719
        suggestion = _coconut.set()  # type: Set[str]  # line 720
        for pat in m.branches[m.branch].tracked:  # line 721
            if fnmatch.fnmatch(pattern, pat):  # line 722
                suggestion.add(pat)  # line 722
        if suggestion:  # TODO use same wording as in move  # line 723
            print("Do you mean any of the following tracked file patterns? '%s'" % (", ".join(sorted(suggestion))))  # TODO use same wording as in move  # line 723
        Exit("Tracked pattern '%s' not found" % pattern)  # line 724
    m.branches[m.branch].tracked.remove(pattern)  # line 725
    m.saveBranches()  # line 726
    info("Removed tracking pattern '%s' for folder '%s'" % (os.path.basename(pattern), os.path.abspath(relPath.replace(SLASH, os.sep))))  # line 727

def ls(argument: '_coconut.typing.Optional[str]'=None, options: '_coconut.typing.Sequence[str]'=[]) -> 'None':  # line 729
    ''' List specified directory, augmenting with repository metadata. '''  # line 730
    folder = "." if argument is None else argument  # type: str  # line 731
    m = Metadata(os.getcwd())  # type: Metadata  # line 732
    m.loadBranches()  # line 733
    info("Repository is in %s mode" % ("tracking" if m.track else ("picky" if m.picky else "simple")))  # line 734
    relPath = os.path.relpath(folder, m.root).replace(os.sep, SLASH)  # type: str  # line 735
    trackingPatterns = m.getTrackingPatterns() if m.track or m.picky else _coconut.frozenset()  # type: _coconut.typing.Optional[FrozenSet[str]]  # for current branch  # line 736
    if '--patterns' in options:  # line 737
        out = ajoin("TRK ", [os.path.basename(p) for p in trackingPatterns if os.path.dirname(p).replace(os.sep, SLASH) == relPath], nl="\n")  # type: str  # line 738
        if out:  # line 739
            print(out)  # line 739
        return  # line 740
    files = list(sorted((entry for entry in os.listdir(folder) if os.path.isfile(os.path.join(folder, entry)))))  # type: List[str]  # line 741
    for file in files:  # for each file list all tracking patterns that match, or none (e.g. in picky mode after commit)  # line 742
        ignore = None  # type: _coconut.typing.Optional[str]  # line 743
        for ig in m.c.ignores:  # line 744
            if fnmatch.fnmatch(file, ig):  # remember first match  # line 745
                ignore = ig  # remember first match  # line 745
                break  # remember first match  # line 745
        if ig:  # line 746
            for wl in m.c.ignoresWhitelist:  # line 747
                if fnmatch.fnmatch(file, wl):  # found a white list entry for ignored file, undo ignoring it  # line 748
                    ignore = None  # found a white list entry for ignored file, undo ignoring it  # line 748
                    break  # found a white list entry for ignored file, undo ignoring it  # line 748
        if not ignore:  # line 749
            matches = []  # type: List[str]  # line 750
            for pattern in (p for p in trackingPatterns if os.path.dirname(p).replace(os.sep, SLASH) == relPath):  # only patterns matching current folder  # line 751
                if fnmatch.fnmatch(file, os.path.basename(pattern)):  # line 752
                    matches.append(os.path.basename(pattern))  # line 752
        matches.sort(key=lambda element: len(element))  # line 753
        print("%s %s%s" % ("IGN" if ignore is not None else ("TRK" if len(matches) > 0 else "..."), file, "  (%s)" % ignore if ignore is not None else ("  (%s)" % ("; ".join(matches)) if len(matches) > 0 else "")))  # line 754

def log(options: '_coconut.typing.Sequence[str]') -> 'None':  # line 756
    ''' List previous commits on current branch. '''  # line 757
    m = Metadata(os.getcwd())  # type: Metadata  # line 758
    m.loadBranches()  # knows current branch  # line 759
    m.loadBranch(m.branch)  # knows commit history  # line 760
    info((lambda _coconut_none_coalesce_item: "r%02d" % m.branch if _coconut_none_coalesce_item is None else _coconut_none_coalesce_item)("//|\\\\ Offline commit history of branch '%s'" % m.branches[m.branch].name))  # TODO also retain "from branch/revision" on branching?  # line 761
    nl = len("%d" % max(m.commits))  # determine space needed for revision  # line 762
    changeset = m.computeSequentialPathSetIterator(m.branch, max(m.commits))  # line 763
    maxWidth = max([wcswidth((lambda _coconut_none_coalesce_item: "" if _coconut_none_coalesce_item is None else _coconut_none_coalesce_item)(commit.message)) for commit in m.commits.values()])  # type: int  # line 764
    for no in range(max(m.commits) + 1):  # line 765
        commit = m.commits[no]  # type: CommitInfo  # line 766
        changes = next(changeset)  # type: ChangeSet  # side-effect: updates m.paths  # line 767
        newTextFiles = len([file for file in changes.additions.keys() if m.isTextType(file)])  # type: int  # line 768
        print("  %s r%s @%s (+%02d/-%02d/*%02d +%02dT/%05.1f%%) |%s|" % ("*" if commit.number == max(m.commits) else " ", ("%%%ds" % nl) % commit.number, strftime(commit.ctime), len(changes.additions), len(changes.deletions), len(changes.modifications), newTextFiles, 0. if len(changes.additions) == 0 else newTextFiles * 100. / len(changes.additions), ((lambda _coconut_none_coalesce_item: "" if _coconut_none_coalesce_item is None else _coconut_none_coalesce_item)(commit.message)).ljust(maxWidth)))  # line 769
        if '--changes' in options:  # line 770
            m.listChanges(changes)  # line 770

def config(argument: 'str', options: 'List[str]'=[]) -> 'None':  # line 772
    if argument not in ["set", "unset", "show", "list", "add", "rm"]:  # line 773
        Exit("Unknown config command")  # line 773
    if not configr:  # line 774
        Exit("Cannot execute config command. 'configr' module not installed")  # line 774
    c = loadConfig()  # type: Union[configr.Configr, Accessor]  # line 775
    if argument == "set":  # line 776
        if len(options) < 2:  # line 777
            Exit("No key nor value specified")  # line 777
        if options[0] not in (["defaultbranch"] + CONFIGURABLE_FLAGS + CONFIGURABLE_LISTS):  # line 778
            Exit("Unsupported key %r" % options[0])  # line 778
        if options[0] in CONFIGURABLE_FLAGS and options[1].lower() not in TRUTH_VALUES + FALSE_VALUES:  # line 779
            Exit("Cannot set flag to '%s'. Try on/off instead" % options[1].lower())  # line 779
        c[options[0]] = options[1].lower() in TRUTH_VALUES if options[0] in CONFIGURABLE_FLAGS else (options[1].strip() if options[0] not in CONFIGURABLE_LISTS else safeSplit(options[1], ";"))  # TODO sanitize texts?  # line 780
    elif argument == "unset":  # line 781
        if len(options) < 1:  # line 782
            Exit("No key specified")  # line 782
        if options[0] not in c.keys():  # line 783
            Exit("Unknown key")  # line 783
        del c[options[0]]  # line 784
    elif argument == "add":  # line 785
        if len(options) < 2:  # line 786
            Exit("No key nor value specified")  # line 786
        if options[0] not in CONFIGURABLE_LISTS:  # line 787
            Exit("Unsupported key for add %r" % options[0])  # line 787
        if options[0] not in c.keys():  # add list  # line 788
            c[options[0]] = [options[1]]  # add list  # line 788
        elif options[1] in c[options[0]]:  # line 789
            Exit("Value already contained")  # line 789
        c[options[0]].append(options[1])  # line 790
    elif argument == "rm":  # line 791
        if len(options) < 2:  # line 792
            Exit("No key nor value specified")  # line 792
        if options[0] not in c.keys():  # line 793
            Exit("Unknown key specified: %r" % options[0])  # line 793
        if options[1] not in c[options[0]]:  # line 794
            Exit("Unknown value: %r" % options[1])  # line 794
        c[options[0]].remove(options[1])  # line 795
    else:  # Show  # line 796
        for k, v in sorted(c.items()):  # line 797
            print("%s => %r" % (k, v))  # line 797
        return  # line 798
    f, g = saveConfig(c)  # line 799
    if f is None:  # line 800
        error("Error saving user configuration: %r" % g)  # line 800

def move(relPath: 'str', pattern: 'str', newRelPath: 'str', newPattern: 'str', options: 'List[str]'=[]) -> 'None':  # line 802
    ''' Path differs: Move files, create folder if not existing. Pattern differs: Attempt to rename file, unless exists in target or not unique. '''  # line 803
    force = '--force' in options  # type: bool  # line 804
    soft = '--soft' in options  # type: bool  # line 805
    if not os.path.exists(relPath.replace(SLASH, os.sep)) and not force:  # line 806
        Exit("Source folder doesn't exist. Use --force to proceed anyway")  # line 806
    m = Metadata(os.getcwd())  # type: Metadata  # line 807
    matching = fnmatch.filter(os.listdir(relPath.replace(SLASH, os.sep)) if os.path.exists(relPath.replace(SLASH, os.sep)) else [], os.path.basename(pattern))  # type: List[str]  # find matching files in source  # line 808
    matching[:] = [f for f in matching if len([n for n in m.c.ignores if fnmatch.fnmatch(f, n)]) == 0 or len([p for p in m.c.ignoresWhitelist if fnmatch.fnmatch(f, p)]) > 0]  # line 809
    if not matching and not force:  # line 810
        Exit("No files match the specified file pattern. Use --force to proceed anyway")  # line 810
    m.loadBranches()  # knows current branch  # line 811
    if not m.track and not m.picky:  # line 812
        Exit("Repository is in simple mode. Simply use basic file operations to modify files, then execute 'sos commit' to version the changes")  # line 812
    if pattern not in m.branches[m.branch].tracked:  # line 813
        for tracked in (t for t in m.branches[m.branch].tracked if os.path.dirname(t) == relPath):  # for all patterns of the same source folder  # line 814
            alternative = fnmatch.filter(matching, os.path.basename(tracked))  # type: _coconut.typing.Sequence[str]  # find if it matches any of the files in the source folder, too  # line 815
            if alternative:  # line 816
                info("  '%s' matches %d files" % (tracked, len(alternative)))  # line 816
        if not (force or soft):  # line 817
            Exit("File pattern '%s' is not tracked on current branch. 'sos move' only works on tracked patterns" % pattern)  # line 817
    basePattern = os.path.basename(pattern)  # type: str  # pure glob without folder  # line 818
    newBasePattern = os.path.basename(newPattern)  # type: str  # line 819
    if basePattern.count("*") < newBasePattern.count("*") or (basePattern.count("?") - basePattern.count("[?]")) < (newBasePattern.count("?") - newBasePattern.count("[?]")) or (basePattern.count("[") - basePattern.count("\\[")) < (newBasePattern.count("[") - newBasePattern.count("\\[")) or (basePattern.count("]") - basePattern.count("\\]")) < (newBasePattern.count("]") - newBasePattern.count("\\]")):  # line 820
        Exit("Glob markers from '%s' to '%s' don't match, cannot move/rename tracked matching files" % (basePattern, newBasePattern))  # line 824
    oldTokens = None  # type: _coconut.typing.Sequence[GlobBlock]  # line 825
    newToken = None  # type: _coconut.typing.Sequence[GlobBlock]  # line 825
    oldTokens, newTokens = tokenizeGlobPatterns(os.path.basename(pattern), os.path.basename(newPattern))  # line 826
    matches = convertGlobFiles(matching, oldTokens, newTokens)  # type: _coconut.typing.Sequence[Tuple[str, str]]  # computes list of source - target filename pairs  # line 827
    if len({st[1] for st in matches}) != len(matches):  # line 828
        Exit("Some target filenames are not unique and different move/rename actions would point to the same target file")  # line 828
    matches = reorderRenameActions(matches, exitOnConflict=not soft)  # attempts to find conflict-free renaming order, or exits  # line 829
    if os.path.exists(newRelPath):  # line 830
        exists = [filename[1] for filename in matches if os.path.exists(os.path.join(newRelPath, filename[1]).replace(SLASH, os.sep))]  # type: _coconut.typing.Sequence[str]  # line 831
        if exists and not (force or soft):  # line 832
            Exit("%s files would write over existing files in %s cases. Use --force to execute it anyway" % ("Moving" if relPath != newRelPath else "Renaming", "all" if len(exists) == len(matches) else "some"))  # line 832
    else:  # line 833
        os.makedirs(os.path.abspath(newRelPath.replace(SLASH, os.sep)))  # line 833
    if not soft:  # perform actual renaming  # line 834
        for (source, target) in matches:  # line 835
            try:  # line 836
                shutil.move(os.path.abspath(os.path.join(relPath, source).replace(SLASH, os.sep)), os.path.abspath(os.path.join(newRelPath, target).replace(SLASH, os.sep)))  # line 836
            except Exception as E:  # one error can lead to another in case of delicate renaming order  # line 837
                error("Cannot move/rename file '%s' to '%s'" % (source, os.path.join(newRelPath, target)))  # one error can lead to another in case of delicate renaming order  # line 837
    m.branches[m.branch].tracked[m.branches[m.branch].tracked.index(pattern)] = newPattern  # line 838
    m.saveBranches()  # line 839

def parse(root: 'str', cwd: 'str'):  # line 841
    ''' Main operation. Main has already chdir into VCS root folder, cwd is original working directory for add, rm. '''  # line 842
    debug("Parsing command-line arguments...")  # line 843
    try:  # line 844
        command = sys.argv[1].strip() if len(sys.argv) > 1 else ""  # line 845
        argument = sys.argv[2].strip() if len(sys.argv) > 2 and not sys.argv[2].startswith("--") else None  # line 846
        options = sys.argv[3:] if command == "config" else [c for c in sys.argv[2:] if c.startswith("--")]  # consider second parameter for no-arg command, otherwise from third on  # line 847
        onlys, excps = parseOnlyOptions(cwd, options)  # extracts folder-relative information for changes, commit, diff, switch, update  # line 848
        debug("Processing command %r with argument '%s' and options %r." % ("" if command is None else command, "" if argument is None else argument, options))  # line 849
        if command[:1] in "amr":  # line 850
            relPath, pattern = relativize(root, os.path.join(cwd, "." if argument is None else argument))  # line 850
        if command[:1] == "m":  # line 851
            if not options:  # line 852
                Exit("Need a second file pattern argument as target for move/rename command")  # line 852
            newRelPath, newPattern = relativize(root, os.path.join(cwd, options[0]))  # line 853
        if command[:1] == "a":  # line 854
            add(relPath, pattern, options)  # line 854
        elif command[:1] == "b":  # line 855
            branch(argument, options)  # line 855
        elif command[:2] == "ch":  # line 856
            changes(argument, options, onlys, excps)  # line 856
        elif command[:3] == "com":  # line 857
            commit(argument, options, onlys, excps)  # line 857
        elif command[:2] == "ci":  # line 858
            commit(argument, options, onlys, excps)  # line 858
        elif command[:3] == 'con':  # line 859
            config(argument, options)  # line 859
        elif command[:2] == "de":  # line 860
            delete(argument, options)  # line 860
        elif command[:2] == "di":  # line 861
            diff(argument, options, onlys, excps)  # line 861
        elif command[:1] == "h":  # line 862
            usage()  # line 862
        elif command[:2] == "lo":  # line 863
            log(options)  # line 863
        elif command[:2] == "li":  # TODO handle absolute paths as well, also for Windows  # line 864
            ls(relativize(root, cwd if argument is None else os.path.join(cwd, argument))[1], options)  # TODO handle absolute paths as well, also for Windows  # line 864
        elif command[:2] == "ls":  # TODO avoid root super paths (..)  # line 865
            ls(relativize(root, cwd if argument is None else os.path.join(cwd, argument))[1], options)  # TODO avoid root super paths (..)  # line 865
        elif command[:1] == "m":  # line 866
            move(relPath, pattern, newRelPath, newPattern, options[1:])  # line 866
        elif command[:2] == "of":  # line 867
            offline(argument, options)  # line 867
        elif command[:2] == "on":  # line 868
            online(options)  # line 868
        elif command[:1] == "r":  # line 869
            remove(relPath, pattern)  # line 869
        elif command[:2] == "st":  # line 870
            status()  # line 870
        elif command[:2] == "sw":  # line 871
            switch(argument, options, onlys, excps)  # line 871
        elif command[:1] == "u":  # line 872
            update(argument, options, onlys, excps)  # line 872
        elif command[:1] == "v":  # line 873
            usage(short=True)  # line 873
        else:  # line 874
            Exit("Unknown command '%s'" % command)  # line 874
    except (Exception, RuntimeError) as E:  # line 875
        print(str(E))  # line 876
        import traceback  # line 877
        traceback.print_exc()  # line 878
        traceback.print_stack()  # line 879
        try:  # line 880
            traceback.print_last()  # line 880
        except:  # line 881
            pass  # line 881
        print("An internal error occurred in SOS. Please report above message to the project maintainer at  https://github.com/ArneBachmann/sos/issues  via 'New Issue'.\nPlease state your installed version via 'sos version', and what you were doing.")  # line 882
    sys.exit(0)  # line 883

def main() -> 'None':  # line 885
    global debug, info, warn, error  # line 886
    logging.basicConfig(level=level, stream=sys.stderr, format=("%(asctime)-23s %(levelname)-8s %(name)s:%(lineno)d | %(message)s" if '--log' in sys.argv else "%(message)s"))  # line 887
    _log = Logger(logging.getLogger(__name__))  # line 888
    debug, info, warn, error = _log.debug, _log.info, _log.warn, _log.error  # line 888
    for option in (o for o in ['--log', '--verbose', '-v', '--sos'] if o in sys.argv):  # clean up program arguments  # line 889
        sys.argv.remove(option)  # clean up program arguments  # line 889
    if '--help' in sys.argv or len(sys.argv) < 2:  # line 890
        usage()  # line 890
        Exit()  # line 890
    command = sys.argv[1] if len(sys.argv) > 1 else None  # type: _coconut.typing.Optional[str]  # line 891
    root, vcs, cmd = findSosVcsBase()  # root is None if no .sos folder exists up the folder tree (still working online); vcs is checkout/repo root folder; cmd is the VCS base command  # line 892
    debug("Found root folders for SOS|VCS: %s|%s" % ("" if root is None else root, "" if vcs is None else vcs))  # line 893
    defaults["defaultbranch"] = vcsBranches.get(cmd, "trunk")  # sets dynamic default with SVN fallback  # line 894
    if force_sos or root is not None or ("" if command is None else command)[:2] == "of" or ("" if command is None else command)[:1] in ["h", "v"]:  # in offline mode or just going offline TODO what about git config?  # line 895
        cwd = os.getcwd()  # line 896
        os.chdir(cwd if command[:2] == "of" else cwd if root is None else root)  # line 897
        parse(root, cwd)  # line 898
    elif force_vcs or cmd is not None:  # online mode - delegate to VCS  # line 899
        info("SOS: Running '%s %s'" % (cmd, " ".join(sys.argv[1:])))  # line 900
        import subprocess  # only required in this section  # line 901
        process = subprocess.Popen([cmd] + sys.argv[1:], shell=False, stdin=subprocess.PIPE, stdout=sys.stdout, stderr=sys.stderr)  # line 902
        inp = ""  # type: str  # line 903
        while True:  # line 904
            so, se = process.communicate(input=inp)  # line 905
            if process.returncode is not None:  # line 906
                break  # line 906
            inp = sys.stdin.read()  # line 907
        if sys.argv[1][:2] == "co" and process.returncode == 0:  # successful commit - assume now in sync again (but leave meta data folder with potential other feature branches behind until "online")  # line 908
            if root is None:  # line 909
                Exit("Cannot determine VCS root folder: Unable to mark repository as synchronized and will show a warning when leaving offline mode")  # line 909
            m = Metadata(root)  # line 910
            m.loadBranches()  # read repo  # line 911
            m.branches[m.branch] = dataCopy(BranchInfo, m.branches[m.branch], inSync=True)  # mark as committed  # line 912
            m.saveBranches()  # line 913
    else:  # line 914
        Exit("No offline repository present, and unable to detect VCS file tree")  # line 914


# Main part
level = logging.DEBUG if os.environ.get("DEBUG", "False").lower() == "true" or '--verbose' in sys.argv or '-v' in sys.argv else logging.INFO  # line 918
force_sos = '--sos' in sys.argv  # type: bool  # line 919
force_vcs = '--vcs' in sys.argv  # type: bool  # line 920
_log = Logger(logging.getLogger(__name__))  # type: logging.Logger  # line 921
debug, info, warn, error = _log.debug, _log.info, _log.warn, _log.error  # line 921
if __name__ == '__main__':  # line 922
    main()  # line 922
