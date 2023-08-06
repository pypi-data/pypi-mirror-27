#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# __coconut_hash__ = 0xa428f5e0

# Compiled with Coconut version 1.3.1 [Dead Parrot]

# Coconut Header: -------------------------------------------------------------

import sys as _coconut_sys, os.path as _coconut_os_path
_coconut_file_path = _coconut_os_path.dirname(_coconut_os_path.abspath(__file__))
_coconut_sys.path.insert(0, _coconut_file_path)
from __coconut__ import _coconut, _coconut_NamedTuple, _coconut_MatchError, _coconut_tail_call, _coconut_tco, _coconut_igetitem, _coconut_base_compose, _coconut_forward_compose, _coconut_back_compose, _coconut_forward_star_compose, _coconut_back_star_compose, _coconut_pipe, _coconut_star_pipe, _coconut_back_pipe, _coconut_back_star_pipe, _coconut_bool_and, _coconut_bool_or, _coconut_none_coalesce, _coconut_minus, _coconut_map, _coconut_partial
from __coconut__ import *
_coconut_sys.path.remove(_coconut_file_path)

# Compiled Coconut: -----------------------------------------------------------

# Standard modules
import codecs  # line 2
import fnmatch  # line 2
import json  # line 2
import logging  # line 2
import mimetypes  # line 2
import os  # line 2
import shutil  # line 2
sys = _coconut_sys  # line 2
import time  # line 2
try:  # line 3
    from typing import Any  # only required for mypy  # line 4
    from typing import Dict  # only required for mypy  # line 4
    from typing import FrozenSet  # only required for mypy  # line 4
    from typing import IO  # only required for mypy  # line 4
    from typing import Iterator  # only required for mypy  # line 4
    from typing import List  # only required for mypy  # line 4
    from typing import Set  # only required for mypy  # line 4
    from typing import Tuple  # only required for mypy  # line 4
    from typing import Union  # only required for mypy  # line 4
except:  # typing not available (e.g. Python 2)  # line 5
    pass  # typing not available (e.g. Python 2)  # line 5
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))  # line 6
try:  # line 7
    from sos import version  # line 8
    from sos.utility import *  # line 9
except:  # line 10
    import version  # line 11
    from utility import *  # line 12

# External dependencies
try:  # optional dependency  # line 15
    import configr  # optional dependency  # line 15
except:  # declare as undefined  # line 16
    configr = None  # declare as undefined  # line 16
#from enforce import runtime_validation  # https://github.com/RussBaz/enforce  TODO doesn't work for "data" types
if sys.version_info.major < 3:  # for Python 2 compatibility  # line 18
    int = long  # for Python 2 compatibility  # line 18


# Constants
APPNAME = "Subversion Offline Solution  V%s  (C) Arne Bachmann" % version.__release_version__  # type: str  # line 22
defaults = Accessor({"strict": False, "track": False, "picky": False, "compress": True, "texttype": [], "bintype": [], "ignoreDirs": [".*", "__pycache__"], "ignoreDirsWhitelist": [], "ignores": ["__coconut__.py", "*.bak", "*.py[cdo]", "*.class", ".fslckout"], "ignoresWhitelist": []})  # line 23
termWidth = getTermWidth() - 1  # uses curses or returns conservative default of 80  # line 24


# Functions
def loadConfig() -> 'Union[configr.Configr, Accessor]':  # Simplifies loading config from file system or returning the defaults  # line 28
    config = None  # type: Union[configr.Configr, Accessor]  # line 29
    if not configr:  # this only applies for the case that configr is not available, thus no settings will be persisted anyway  # line 30
        return defaults  # this only applies for the case that configr is not available, thus no settings will be persisted anyway  # line 30
    config = configr.Configr("sos", defaults=defaults)  # defaults are used if key is not configured, but won't be saved  # line 31
    f, g = config.loadSettings(clientCodeLocation=os.path.abspath(__file__), location=os.environ.get("TEST", None))  # line 32
    if f is None:  # line 33
        debug("Encountered a problem while loading the user configuration: %r" % g)  # line 33
    return config  # line 34

@_coconut_tco  # line 36
def saveConfig(c: 'configr.Configr') -> 'Tuple[_coconut.typing.Optional[str], _coconut.typing.Optional[Exception]]':  # line 36
    return _coconut_tail_call(c.saveSettings, clientCodeLocation=os.path.abspath(__file__), location=os.environ.get("TEST", None))  # line 37

def usage() -> 'None':  # line 39
    print("""/// {appname} ///

Usage: {cmd} <command> [<argument>] [<option1>, ...]        For command "offline" and when in offline mode
       {cmd} <underlying vcs command and arguments>         Unless working in offline mode

  Available commands:
    offline [<name>]                                      Start working offline, creating a branch (named <name>)
      --plain                                               Don't compress versioned files (same as `sos config set compress off`)
      --track                                               Setup SVN-style mode: users add/remove tracking patterns per branch
      --picky                                               Setup Git-style mode: users pick files for each operation
    online                                                Finish working offline

    branch  [<name>] [--last] [--stay]                    Create a new branch from current file tree and switch to it
      --last                                                Use last revision, not current file tree, but keep file tree unchanged
      --stay                                                Don't switch to new branch, continue on current one
    switch  [<branch>][/<revision>] [--meta]              Continue work on another branch
      --meta                                                Only switch file tracking patterns for current branch, don't update any files
    update  [<branch>][/<revision>]                       Integrate work from another branch TODO add many merge and conflict resolution options
    delete  [<branch>]                                    Remove (current) branch entirely

    commit  [<message>]                                   Create a new revision from current state file tree, with an optional commit message
    changes [<branch>][/<revision>]                       List changed paths vs. last or specified revision
    diff    [<branch>][/<revision>]                       List changes vs. last or specified revision
    add     [<filename or glob pattern>]                  Add a tracking pattern to current branch (path/filename or glob pattern)
    rm      [<filename or glob pattern>]                  Remove a tracking pattern. Only useful after "offline --track" or "offline --picky"

    ls                                                    List file tree and mark changes and tracking status
    status                                                List branches and display repository status
    log                                                   List commits of current branch
    config  [set/unset/show/add/rm] [<param> [<value>]]   Configure user-global defaults.
                                                          Flags (1/0, on/off, true/false, yes/no):
                                                            strict, track, picky, compress
                                                          Lists (semicolon-separated when set; single values for add/rm):
                                                            texttype, bintype, ignores, ignoreDirs, ignoresWhitelist, ignoreDirsWhitelist
                                                          Supported texts:
                                                            defaultbranch (has a dynamic default value, depending on VCS discovered)
    help, --help                                          Show this usage information

  Arguments:
    <branch/revision>           Revision string. Branch is optional and may be a label or index
                                Revision is an optional integer and may be negative to reference from the latest commits (-1 is most recent revision)

  Common options:
    --force                     Executes potentially harmful operations
                                  for offline: ignore being already offline, start from scratch (same as 'sos online --force && sos offline')
                                  for online: ignore uncommitted branches
                                  for commit, switch, update, add: ignore uncommitted changes before executing command
    --strict                    Perform full content comparison, don't rely only on file size and timestamp
                                  for offline: persist strict mode in repository
                                  for changes, diff, commit, switch, update, delete: perform operation in strict mode
    --{cmd}                       When executing {CMD} not being offline, pass arguments to {CMD} instead (e.g. {cmd} --{cmd} config set key value.)
    --log                       Enable internals logger
    --verbose                   Enable debugging output""".format(appname=APPNAME, cmd="sos", CMD="SOS"))  # line 92

# Main data class
#@runtime_validation
class Metadata:  # line 96
    ''' This class doesn't represent the entire repository state in memory,
      but serves as a container for different repo operations,
      using only parts of its attributes at any point in time. Use with care.
  '''  # line 100

    def __init__(_, path: 'str') -> 'None':  # line 102
        ''' Create empty container object for various repository operations. '''  # line 103
        _.c = loadConfig()  # line 104
        _.root = path  # type: str  # line 105
        _.branches = {}  # type: Dict[int, BranchInfo]  # branch number zero represents the initial state at branching  # line 106
        _.commits = {}  # type: Dict[int, CommitInfo]  # consecutive numbers per branch, starting at 0  # line 107
        _.paths = {}  # type: Dict[str, PathInfo]  # utf-8 encoded relative, normalized file system paths  # line 108
        _.branch = None  # type: _coconut.typing.Optional[int]  # current branch number  # line 109
        _.commit = None  # type: _coconut.typing.Optional[int]  # current revision number  # line 110
        _.track = _.c.track  # type: bool  # track file name patterns in the repository (per branch)  # line 111
        _.picky = _.c.picky  # type: bool  # pick files to commit per operation  # line 112
        _.strict = _.c.strict  # type: bool  # be always strict (regarding file contents comparsion)  # line 113
        _.compress = _.c.compress  # type: bool  # these flags are stored in the repository  # line 114

    def isTextType(_, filename: 'str') -> 'bool':  # line 116
        return (((lambda _coconut_none_coalesce_item: "" if _coconut_none_coalesce_item is None else _coconut_none_coalesce_item)(mimetypes.guess_type(filename)[0])).startswith("text/") or any([fnmatch.fnmatch(filename, pattern) for pattern in _.c.texttype])) and not any([fnmatch.fnmatch(filename, pattern) for pattern in _.c.bintype])  # line 116

    def listChanges(_, changes: 'ChangeSet') -> 'None':  # line 118
        ''' In diffmode, don't list modified files, because the diff is displayed elsewhere. '''  # line 119
        if len(changes.additions) > 0:  # line 120
            print(ajoin("ADD ", sorted(changes.additions.keys()), "\n"))  # line 120
        if len(changes.deletions) > 0:  # line 121
            print(ajoin("DEL ", sorted(changes.deletions.keys()), "\n"))  # line 121
        if len(changes.modifications) > 0:  # line 122
            print(ajoin("MOD ", sorted(changes.modifications.keys()), "\n"))  # line 122

    def loadBranches(_) -> 'None':  # line 124
        ''' Load list of branches and current branch info from metadata file. '''  # line 125
        try:  # fails if not yet created (on initial branch/commit)  # line 126
            branches = None  # type: List[Tuple]  # line 127
            with codecs.open(os.path.join(_.root, metaFolder, metaFile), "r", encoding=UTF8) as fd:  # line 128
                flags, branches = json.load(fd)  # line 129
            _.branch = flags["branch"]  # current branch integer  # line 130
            _.track = flags["track"]  # line 131
            _.picky = flags["picky"]  # line 132
            _.strict = flags["strict"]  # line 133
            _.compress = flags["compress"]  # line 134
            _.branches = {i.number: i for i in (BranchInfo(*item) for item in branches)}  # re-create type info  # line 135
        except Exception as E:  # if not found, create metadata folder  # line 136
            _.branches = {}  # line 137
            warn("Couldn't read branches metadata: %r" % E)  # line 138

    def saveBranches(_) -> 'None':  # line 140
        ''' Save list of branches and current branch info to metadata file. '''  # line 141
        with codecs.open(os.path.join(_.root, metaFolder, metaFile), "w", encoding=UTF8) as fd:  # line 142
            json.dump(({"branch": _.branch, "track": _.track, "picky": _.picky, "strict": _.strict, "compress": _.compress}, list(_.branches.values())), fd, ensure_ascii=False)  # line 143

    def getBranchByName(_, name: 'Union[str, int]') -> '_coconut.typing.Optional[int]':  # line 145
        ''' Convenience accessor for named branches. '''  # line 146
        if isinstance(name, int):  # line 147
            return name  # line 147
        try:  # attempt to parse integer string  # line 148
            return int(name)  # attempt to parse integer string  # line 148
        except ValueError:  # line 149
            pass  # line 149
        found = [number for number, branch in _.branches.items() if name == branch.name]  # line 150
        return found[0] if found else None  # line 151

    def loadBranch(_, branch: 'int') -> 'None':  # line 153
        ''' Load all commit information from a branch meta data file. '''  # line 154
        with codecs.open(os.path.join(_.root, metaFolder, "b%d" % branch, metaFile), "r", encoding=UTF8) as fd:  # line 155
            commits = json.load(fd)  # type: List[List[Any]]  # list of CommitInfo that needs to be unmarshalled into value types  # line 156
        _.commits = {i.number: i for i in (CommitInfo(*item) for item in commits)}  # re-create type info  # line 157
        _.branch = branch  # line 158

    def saveBranch(_, branch: 'int') -> 'None':  # line 160
        ''' Save all commit information to a branch meta data file. '''  # line 161
        with codecs.open(os.path.join(_.root, metaFolder, "b%d" % branch, metaFile), "w", encoding=UTF8) as fd:  # line 162
            json.dump(list(_.commits.values()), fd, ensure_ascii=False)  # line 163

    def duplicateBranch(_, branch: 'int', name: '_coconut.typing.Optional[str]') -> 'None':  # line 165
        ''' Create branch from an existing branch/revision. WARN: Caller must have loaded branches information.
        branch: target branch (should not exist yet)
        name: optional name of new branch
        _.branch: current branch
    '''  # line 170
        debug("Duplicating branch '%s' to '%d'..." % ((lambda _coconut_none_coalesce_item: "b%d" % _.branch if _coconut_none_coalesce_item is None else _coconut_none_coalesce_item)(_.branches[_.branch].name), branch))  # line 171
        tracked = [t for t in _.branches[_.branch].tracked]  # copy  # line 172
        os.makedirs(os.path.join(_.root, metaFolder, "b%d" % branch, "r0"))  # line 173
        _.loadBranch(_.branch)  # line 174
        revision = max(_.commits)  # type: int  # line 175
        _.computeSequentialPathSet(_.branch, revision)  # full set of files in revision to _.paths  # line 176
        for path, pinfo in _.paths.items():  # line 177
            _.copyVersionedFile(_.branch, revision, branch, 0, pinfo)  # line 178
        _.commits = {0: CommitInfo(0, int(time.time() * 1000), "Branched from '%s'" % ((lambda _coconut_none_coalesce_item: "b%d" % _.branch if _coconut_none_coalesce_item is None else _coconut_none_coalesce_item)(_.branches[_.branch].name)))}  # store initial commit  # line 179
        _.saveBranch(branch)  # save branch meta data to branch folder  # line 180
        _.saveCommit(branch, 0)  # save commit meta data to revision folder  # line 181
        _.branches[branch] = BranchInfo(branch, _.commits[0].ctime, name, _.branches[_.branch].insync, tracked)  # save branch info, before storing repo state at caller  # line 182

    def createBranch(_, branch: 'int', name: '_coconut.typing.Optional[str]'=None, initialMessage: '_coconut.typing.Optional[str]'=None):  # line 184
        ''' Create a new branch from current file tree. This clears all known commits and modifies the file system.
        branch: target branch (should not exist yet)
        name: optional name of new branch
        _.branch: current branch, must exist already
    '''  # line 189
        simpleMode = not (_.track or _.picky)  # line 190
        tracked = [t for t in _.branches[_.branch].tracked] if _.track and len(_.branches) > 0 else []  # in case of initial branch creation  # line 191
        debug((lambda _coconut_none_coalesce_item: "b%d" % branch if _coconut_none_coalesce_item is None else _coconut_none_coalesce_item)("Creating branch '%s'..." % name))  # line 192
        _.paths = {}  # type: Dict[str, PathInfo]  # line 193
        if simpleMode:  # branches from file system state  # line 194
            changes = _.findChanges(branch, 0, progress=simpleMode)  # type: ChangeSet  # creates revision folder and versioned files  # line 195
            _.listChanges(changes)  # line 196
            _.paths.update(changes.additions.items())  # line 197
        else:  # tracking or picky mode: branch from lastest revision  # line 198
            os.makedirs(os.path.join(_.root, metaFolder, "b%d" % branch, "r0"))  # line 199
            if _.branch is not None:  # not immediately after "offline" - copy files from current branch  # line 200
                _.loadBranch(_.branch)  # line 201
                revision = max(_.commits)  # type: int  # TODO what if last switch was to an earlier revision? no persisting of last checkout  # line 202
                _.computeSequentialPathSet(_.branch, revision)  # full set of files in revision to _.paths  # line 203
                for path, pinfo in _.paths.items():  # line 204
                    _.copyVersionedFile(_.branch, revision, branch, 0, pinfo)  # line 205
        ts = int(time.time() * 1000)  # line 206
        _.commits = {0: CommitInfo(0, ts, "Branched on %s" % strftime(ts) if initialMessage is None else initialMessage)}  # store initial commit for new branch  # line 207
        _.saveBranch(branch)  # save branch meta data (revisions) to branch folder  # line 208
        _.saveCommit(branch, 0)  # save commit meta data to revision folder  # line 209
        _.branches[branch] = BranchInfo(branch, _.commits[0].ctime, name, True if len(_.branches) == 0 else _.branches[_.branch].insync, tracked)  # save branch info, in case it is needed  # line 210

    def removeBranch(_, branch: 'int') -> 'BranchInfo':  # line 212
        ''' Entirely remove a branch and all its revisions from the file system. '''  # line 213
        shutil.rmtree(os.path.join(_.root, metaFolder, "b%d" % branch))  # line 214
        binfo = _.branches[branch]  # line 215
        del _.branches[branch]  # line 216
        _.branch = max(_.branches)  # line 217
        _.saveBranches()  # line 218
        _.commits.clear()  # line 219
        return binfo  # line 220

    def loadCommit(_, branch: 'int', revision: 'int') -> 'None':  # line 222
        ''' Load all file information from a commit meta data. '''  # line 223
        with codecs.open(os.path.join(_.root, metaFolder, "b%d" % branch, "r%d" % revision, metaFile), "r", encoding=UTF8) as fd:  # line 224
            _.paths = json.load(fd)  # line 225
        _.paths = {path: PathInfo(*item) for path, item in _.paths.items()}  # re-create type info  # line 226
        _.branch = branch  # line 227

    def saveCommit(_, branch: 'int', revision: 'int'):  # line 229
        ''' Save all file information to a commit meta data file. '''  # line 230
        target = os.path.join(_.root, metaFolder, "b%d" % branch, "r%d" % revision)  # line 231
        try:  # line 232
            os.makedirs(target)  # line 232
        except:  # line 233
            pass  # line 233
        with codecs.open(os.path.join(target, metaFile), "w", encoding=UTF8) as fd:  # line 234
            json.dump(_.paths, fd, ensure_ascii=False)  # line 235

    def findChanges(_, branch: '_coconut.typing.Optional[int]'=None, revision: '_coconut.typing.Optional[int]'=None, checkContent: 'bool'=False, inverse: 'bool'=False, considerOnly: '_coconut.typing.Optional[FrozenSet[str]]'=None, progress: 'bool'=False) -> 'ChangeSet':  # line 237
        ''' Find changes on the file system vs. in-memory paths (which should reflect the latest commit state).
        Only if both branch and revision are *not* None, write modified/added files to the specified revision folder (thus creating a new revision)
        The function returns the state of file tree *differences*, unless "inverse" is True -> then return original data
        checkContent: also computes file content hashes
        inverse: retain original state (size, mtime, hash) instead of updated one
        considerOnly: set of tracking patterns. For update operation, union of other and current branch
        progress: Show file names during processing
    '''  # line 245
        write = branch is not None and revision is not None  # line 246
        if write:  # line 247
            os.makedirs(os.path.join(_.root, metaFolder, "b%d" % branch, "r%d" % revision))  # line 247
        changes = ChangeSet({}, {}, {})  # type: ChangeSet  # line 248
        counter = Counter(-1)  # type: Counter  # line 249
        timer = time.time()  # line 249
        for path, dirnames, filenames in os.walk(_.root):  # line 250
            dirnames[:] = [f for f in dirnames if len([n for n in _.c.ignoreDirs if fnmatch.fnmatch(f, n)]) == 0 or len([p for p in _.c.ignoreDirsWhitelist if fnmatch.fnmatch(f, p)]) > 0]  # line 251
            filenames[:] = [f for f in filenames if len([n for n in _.c.ignores if fnmatch.fnmatch(f, n)]) == 0 or len([p for p in _.c.ignoresWhitelist if fnmatch.fnmatch(f, p)]) > 0]  # line 252
            dirnames.sort()  # line 253
            filenames.sort()  # line 253
            relpath = os.path.relpath(path, _.root).replace(os.sep, SLASH)  # line 254
            for file in (filenames if considerOnly is None else list(reduce(lambda last, pattern: last | set(fnmatch.filter(filenames, os.path.basename(pattern))), (p for p in considerOnly if os.path.dirname(p) == relpath), _coconut.set()))):  # if m.track or m.picky: only files that match any path-relevant tracking patterns  # line 255
                filename = relpath + SLASH + file  # line 256
                filepath = os.path.join(path, file)  # line 257
                stat = os.stat(filepath)  # line 258
                size, mtime, newtime = stat.st_size, int(stat.st_mtime * 1000), time.time()  # line 259
                if progress and newtime - timer > .1:  # line 260
                    outstring = "\rPreparing %s  %s" % (PROGRESS_MARKER[counter.inc() % 4], filename)  # line 261
                    sys.stdout.write(outstring + " " * max(0, termWidth - len(outstring)))  # TODO could write to new line instead of carriage return, also needs terminal width  # line 262
                    sys.stdout.flush()  # TODO could write to new line instead of carriage return, also needs terminal width  # line 262
                    timer = newtime  # TODO could write to new line instead of carriage return, also needs terminal width  # line 262
                if filename not in _.paths:  # detected file not present (or untracked) in other branch  # line 263
                    namehash = hashStr(filename)  # line 264
                    changes.additions[filename] = PathInfo(namehash, size, mtime, hashFile(filepath, _.compress, saveTo=os.path.join(_.root, metaFolder, "b%d" % branch, "r%d" % revision, namehash) if write else None) if size > 0 else None)  # line 265
                    continue  # line 266
                last = _.paths[filename]  # filename is known  # line 267
                if last.size is None:  # was removed before but is now added back - does not apply for tracking mode (which never marks files for removal in the history)  # line 268
                    changes.additions[filename] = PathInfo(last.namehash, size, mtime, hashFile(filepath, _.compress, saveTo=os.path.join(_.root, metaFolder, "b%d" % branch, "r%d" % revision, last.namehash) if write else None) if size > 0 else None)  # line 269
                    continue  # line 269
                elif size != last.size or mtime != last.mtime or (checkContent and hashFile(filepath, _.compress) == last.hash):  # detected a modification  # line 270
                    changes.modifications[filename] = PathInfo(last.namehash, last.size if inverse else size, last.mtime if inverse else mtime, last.hash if inverse else hashFile(filepath, _.compress, saveTo=os.path.join(_.root, metaFolder, "b%d" % branch, "r%d" % revision, last.namehash) if write else None) if (last.size if inverse else size) > 0 else None)  # line 271
# Detect deletions. Files no longer being tracked should not be found here
            for folderPath in (p for p, pinfo in _.paths.items() if p[:p.rindex(SLASH)] == relpath and pinfo.size is not None):  # only versioned (and tracked) files that match currently visited folder. TODO don't check for removal just added entries  # line 273
                if folderPath[len(relpath) + 1:] not in filenames:  # filename no longer in file tree TODO use basename and dirname instead of slicing?  # line 274
                    changes.deletions[folderPath] = _.paths[folderPath]  # filename no longer in file tree TODO use basename and dirname instead of slicing?  # line 274
        if progress:  # force new line  # line 275
            print("Preparation finished." + " " * (termWidth - 21), file=sys.stdout)  # force new line  # line 275
        return changes  # line 276

    def integrateChangeset(_, changes: 'ChangeSet', clear=False) -> 'None':  # line 278
        ''' In-memory update from a changeset, marking deleted files with size=None. Use clear = True to start on an empty path set. '''  # line 279
        if clear:  # line 280
            _.paths.clear()  # line 280
        else:  # line 281
            rm = [p for p, info in _.paths.items() if info.size is None]  # remove files deleted in earlier change sets (revisions)  # line 282
            for old in rm:  # remove previously removed entries completely  # line 283
                del _.paths[old]  # remove previously removed entries completely  # line 283
        for d, info in changes.deletions.items():  # mark now removed entries as deleted  # line 284
            _.paths[d] = PathInfo(info.namehash, None, info.mtime, None)  # mark now removed entries as deleted  # line 284
        _.paths.update(changes.additions)  # line 285
        _.paths.update(changes.modifications)  # line 286

    def computeSequentialPathSet(_, branch: 'int', revision: 'int') -> 'None':  # line 288
        next(_.computeSequentialPathSetIterator(branch, revision, incrementally=False))  # simply invoke the generator once  # line 289

    def computeSequentialPathSetIterator(_, branch: 'int', revision: 'int', incrementally: 'bool'=True) -> 'Optional[Iterator[ChangeSet]]':  # line 291
        ''' In-memory computation of current list of valid PathInfo entries for specified branch and until specified revision (inclusively) by traversing revision on the file system. '''  # line 292
        _.loadCommit(branch, 0)  # load initial paths  # line 293
        if incrementally:  # line 294
            yield diffPathSets({}, _.paths)  # line 294
        n = Metadata(_.root)  # type: Metadata  # next changes  # line 295
        for revision in range(1, revision + 1):  # line 296
            n.loadCommit(branch, revision)  # line 297
            changes = diffPathSets(_.paths, n.paths)  # type: ChangeSet  # line 298
            _.integrateChangeset(changes)  # line 299
            if incrementally:  # line 300
                yield changes  # line 300
        yield None  # for the default case - not incrementally  # line 301

    def parseRevisionString(_, argument: 'str') -> 'Tuple[_coconut.typing.Optional[int], _coconut.typing.Optional[int]]':  # line 303
        ''' Commit identifiers can be str or int for branch, and int for revision.
        Revision identifiers can be negative, with -1 being last commit.
    '''  # line 306
        if argument is None:  # no branch/revision specified  # line 307
            return (_.branch, -1)  # no branch/revision specified  # line 307
        argument = argument.strip()  # line 308
        if argument.startswith(SLASH):  # current branch  # line 309
            return (_.branch, int(argument[1:]))  # current branch  # line 309
        if argument.endswith(SLASH):  # line 310
            try:  # line 311
                return (_.getBranchByName(argument[:-1]), -1)  # line 311
            except ValueError:  # line 312
                Exit("Unknown branch label")  # line 312
        if SLASH in argument:  # line 313
            b, r = argument.split(SLASH)[:2]  # line 314
            try:  # line 315
                return (_.getBranchByName(b), int(r))  # line 315
            except ValueError:  # line 316
                Exit("Unknown branch label or wrong number format")  # line 316
        branch = _.getBranchByName(argument)  # type: int  # returns number if given (revision) integer  # line 317
        if branch not in _.branches:  # line 318
            branch = None  # line 318
        try:  # either branch name/number or reverse/absolute revision number  # line 319
            return (_.branch if branch is None else branch, int(argument) if branch is None else -1)  # either branch name/number or reverse/absolute revision number  # line 319
        except:  # line 320
            Exit("Unknown branch label or wrong number format")  # line 320
        return (None, None)  # should never be reached TODO raise exception instead?  # line 321

    def findRevision(_, branch: 'int', revision: 'int', namehash: 'str') -> 'Tuple[int, str]':  # line 323
        while True:  # find latest revision that contained the file physically  # line 324
            source = os.path.join(_.root, metaFolder, "b%d" % branch, "r%d" % revision, namehash)  # type: str  # line 325
            if os.path.exists(source) and os.path.isfile(source):  # line 326
                break  # line 326
            revision -= 1  # line 327
            if revision < 0:  # line 328
                Exit("Cannot determine versioned file '%s' from specified branch '%d'" % (namehash, branch))  # line 328
        return revision, source  # line 329

    def copyVersionedFile(_, branch: 'int', revision: 'int', tobranch: 'int', torevision: 'int', pinfo: 'PathInfo') -> 'None':  # line 331
        ''' Copy versioned file to other branch/revision. '''  # line 332
        target = os.path.join(_.root, metaFolder, "b%d" % tobranch, "r%d" % torevision, pinfo.namehash)  # type: str  # line 333
        revision, source = _.findRevision(branch, revision, pinfo.namehash)  # line 334
        shutil.copy2(source, target)  # line 335

    def readOrCopyVersionedFile(_, branch: 'int', revision: 'int', namehash: 'str', toFile: '_coconut.typing.Optional[str]'=None) -> '_coconut.typing.Optional[bytes]':  # line 337
        ''' Return file contents, or copy contents into file path provided. '''  # line 338
        source = os.path.join(_.root, metaFolder, "b%d" % branch, "r%d" % revision, namehash)  # type: str  # line 339
        try:  # line 340
            with openIt(source, "r", _.compress) as fd:  # line 341
                if toFile is None:  # read bytes into memory and return  # line 342
                    return fd.read()  # read bytes into memory and return  # line 342
                with open(toFile, "wb") as to:  # line 343
                    while True:  # line 344
                        buffer = fd.read(bufSize)  # line 345
                        to.write(buffer)  # line 346
                        if len(buffer) < bufSize:  # line 347
                            break  # line 347
                    return None  # line 348
        except Exception as E:  # line 349
            warn("Cannot read versioned file: %r (%d/%d/%s)" % (E, branch, revision, namehash))  # line 349
        return None  # line 350

    def restoreFile(_, relpath: '_coconut.typing.Optional[str]', branch: 'int', revision: 'int', pinfo: 'PathInfo') -> '_coconut.typing.Optional[bytes]':  # line 352
        ''' Recreate file for given revision, or return contents if path is None. '''  # line 353
        if relpath is None:  # just return contents  # line 354
            return _.readOrCopyVersionedFile(branch, _.findRevision(branch, revision, pinfo.namehash)[0], pinfo.namehash) if pinfo.size > 0 else b''  # just return contents  # line 354
        target = os.path.join(_.root, relpath.replace(SLASH, os.sep))  # type: str  # line 355
        if pinfo.size == 0:  # line 356
            with open(target, "wb"):  # line 357
                pass  # line 357
            try:  # update access/modification timestamps on file system  # line 358
                os.utime(target, (-1, pinfo.mtime / 1000.))  # update access/modification timestamps on file system  # line 358
            except Exception as E:  # line 359
                error("Cannot update file's timestamp after restoration '%r'" % E)  # line 359
            return None  # line 360
        revision, source = _.findRevision(branch, revision, pinfo.namehash)  # line 361
# Restore file by copying buffer-wise
        with openIt(source, "r", _.compress) as fd, open(target, "wb") as to:  # using Coconut's Enhanced Parenthetical Continuation  # line 363
            while True:  # line 364
                buffer = fd.read(bufSize)  # line 365
                to.write(buffer)  # line 366
                if len(buffer) < bufSize:  # line 367
                    break  # line 367
        try:  # update access/modification timestamps on file system  # line 368
            os.utime(target, (-1, pinfo.mtime / 1000.))  # update access/modification timestamps on file system  # line 368
        except Exception as E:  # line 369
            error("Cannot update file's timestamp after restoration '%r'" % E)  # line 369
        return None  # line 370

    def getTrackingPatterns(_, branch: '_coconut.typing.Optional[int]'=None) -> 'FrozenSet[str]':  # line 372
        ''' Returns list of tracking patterns for provided branch or current branch. '''  # line 373
        return _coconut.frozenset() if not _.track and not _.picky else frozenset(_.branches[_.branch if branch is None else branch].tracked)  # line 374


# Main client operations
def offline(argument: '_coconut.typing.Optional[str]'=None, options: '_coconut.typing.Sequence[str]'=[]) -> 'None':  # line 378
    ''' Initial command to start working offline. '''  # line 379
    if os.path.exists(metaFolder):  # line 380
        if '--force' not in options:  # line 381
            Exit("Repository folder is either already offline or older branches and commits were left over. Use 'sos online' or continue working offline")  # line 381
        try:  # line 382
            for entry in os.listdir(metaFolder):  # line 383
                resource = metaFolder + os.sep + entry  # line 384
                if os.path.isdir(resource):  # line 385
                    shutil.rmtree(resource)  # line 385
                else:  # line 386
                    os.unlink(resource)  # line 386
        except:  # line 387
            Exit("Cannot reliably remove previous repository contents. Please remove .sos folder manually prior to going offline")  # line 387
    m = Metadata(os.getcwd())  # type: Metadata  # line 388
    if '--plain' in options or not m.c.compress:  # plain file copies instead of compressed ones  # line 389
        m.compress = False  # plain file copies instead of compressed ones  # line 389
    if '--picky' in options or m.c.picky:  # Git-like  # line 390
        m.picky = True  # Git-like  # line 390
    elif '--track' in options or m.c.track:  # Svn-like  # line 391
        m.track = True  # Svn-like  # line 391
    if '--strict' in options or m.c.strict:  # always hash contents  # line 392
        m.strict = True  # always hash contents  # line 392
    debug("Preparing offline repository...")  # line 393
    m.createBranch(0, str(defaults["defaultbranch"]) if argument is None else argument, initialMessage="Offline repository created on %s" % strftime())  # main branch's name may be None (e.g. for fossil)  # line 394
    m.branch = 0  # line 395
    m.saveBranches()  # no change immediately after going offline, going back online won't issue a warning  # line 396
    info("Offline repository prepared. Use 'sos online' to finish offline work")  # line 397

def online(options: '_coconut.typing.Sequence[str]'=[]) -> 'None':  # line 399
    ''' Finish working offline. '''  # line 400
    force = '--force' in options  # type: bool  # line 401
    m = Metadata(os.getcwd())  # line 402
    m.loadBranches()  # line 403
    if any([not b.insync for b in m.branches.values()]) and not force:  # line 404
        Exit("There are still unsynchronized (dirty) branches.\nUse 'sos log' to list them.\nUse 'sos commit' and 'sos switch' to commit dirty branches to your VCS before leaving offline mode.\nUse 'sos online --force' to erase all aggregated offline revisions.")  # line 404
    strict = '--strict' in options or m.strict  # type: bool  # line 405
    if options.count("--force") < 2:  # line 406
        changes = m.findChanges(checkContent=strict, considerOnly=None if not m.track else m.getTrackingPatterns())  # type: ChangeSet  # line 407
        if modified(changes):  # line 408
            Exit("File tree is modified vs. current branch.\nUse 'sos online --force --force' to continue with removing the offline repository.")  # line 408
    try:  # line 409
        shutil.rmtree(metaFolder)  # line 409
        info("Exited offline mode. Continue working with your traditional VCS.")  # line 409
    except Exception as E:  # line 410
        Exit("Error removing offline repository: %r" % E)  # line 410

def branch(argument: '_coconut.typing.Optional[str]'=None, options: '_coconut.typing.Sequence[str]'=[]) -> 'None':  # line 412
    ''' Create a new branch (from file tree or last revision) and (by default) continue working on it. '''  # line 413
    last = '--last' in options  # type: bool  # use last revision for branching, not current file tree  # line 414
    stay = '--stay' in options  # type: bool  # continue on current branch after branching  # line 415
    force = '--force' in options  # type: bool  # branch even with local modifications  # line 416
    m = Metadata(os.getcwd())  # type: Metadata  # line 417
    m.loadBranches()  # line 418
    if argument and m.getBranchByName(argument) is not None:  # create a named branch  # line 419
        Exit("Branch '%s' already exists. Cannot proceed" % argument)  # create a named branch  # line 419
    branch = max(m.branches.keys()) + 1  # next branch's key - this isn't atomic but we assume single-user non-concurrent use here  # line 420
    debug("Branching to %sbranch b%02d%s%s..." % ("unnamed " if argument is None else "", branch, " '%s'" % argument if argument else "", " from last revision" if last else ""))  # line 421
    if last:  # line 422
        m.duplicateBranch(branch, argument)  # branch from branch's last revision  # line 423
    else:  # from file tree state  # line 424
        m.createBranch(branch, argument)  # branch from current file tree  # line 425
    if not stay:  # line 426
        m.branch = branch  # line 427
        m.saveBranches()  # line 428
    info("%s new %sbranch b%02d%s" % ("Continue work after branching" if stay else "Switched to", "unnamed " if argument is None else "", branch, " '%s'" % argument if argument else ""))  # line 429

def changes(argument: 'str'=None, options: '_coconut.typing.Sequence[str]'=[]) -> 'ChangeSet':  # line 431
    ''' Show changes of file tree vs. (last or specified) revision on current or specified branch. '''  # line 432
    m = Metadata(os.getcwd())  # type: Metadata  # line 433
    branch = None  # type: _coconut.typing.Optional[int]  # line 433
    revision = None  # type: _coconut.typing.Optional[int]  # line 433
    m.loadBranches()  # knows current branch  # line 434
    strict = '--strict' in options or m.strict  # type: bool  # line 435
    branch, revision = m.parseRevisionString(argument)  # line 436
    if branch not in m.branches:  # line 437
        Exit("Unknown branch")  # line 437
    m.loadBranch(branch)  # knows commits  # line 438
    revision = revision if revision >= 0 else len(m.commits) + revision  # negative indexing  # line 439
    if revision < 0 or revision > max(m.commits):  # line 440
        Exit("Unknown revision r%02d" % revision)  # line 440
    info("/// Changes of file tree vs. revision '%s/r%02d'" % ((lambda _coconut_none_coalesce_item: "b%02d" % branch if _coconut_none_coalesce_item is None else _coconut_none_coalesce_item)(m.branches[branch].name), revision))  # line 441
    m.computeSequentialPathSet(branch, revision)  # load all commits up to specified revision  # line 442
    changes = m.findChanges(checkContent=strict, considerOnly=None if not m.track else m.getTrackingPatterns() | m.getTrackingPatterns(branch))  # type: ChangeSet  # line 443
    m.listChanges(changes)  # line 444
    return changes  # line 445

def diff(argument: 'str', options: '_coconut.typing.Sequence[str]'=[]) -> 'None':  # line 447
    ''' Show text file differences of file tree vs. (last or specified) revision on current or specified branch. '''  # line 448
    m = Metadata(os.getcwd())  # type: Metadata  # line 449
    branch = None  # type: _coconut.typing.Optional[int]  # line 449
    revision = None  # type: _coconut.typing.Optional[int]  # line 449
    m.loadBranches()  # knows current branch  # line 450
    strict = '--strict' in options or m.strict  # type: bool  # line 451
    branch, revision = m.parseRevisionString(argument)  # line 452
    if branch not in m.branches:  # line 453
        Exit("Unknown branch")  # line 453
    m.loadBranch(branch)  # knows commits  # line 454
    revision = revision if revision >= 0 else len(m.commits) + revision  # negative indexing  # line 455
    if revision < 0 or revision > max(m.commits):  # line 456
        Exit("Unknown revision r%02d" % revision)  # line 456
    info("/// Differences of file tree vs. revision '%s/r%02d'" % ((lambda _coconut_none_coalesce_item: "b%02d" % branch if _coconut_none_coalesce_item is None else _coconut_none_coalesce_item)(m.branches[branch].name), revision))  # line 457
    m.computeSequentialPathSet(branch, revision)  # load all commits up to specified revision  # line 458
    changes = m.findChanges(checkContent=strict, inverse=True, considerOnly=None if not m.track else m.getTrackingPatterns() | m.getTrackingPatterns(branch))  # type: ChangeSet  # line 459
    onlyBinaryModifications = dataCopy(ChangeSet, changes, modifications={k: v for k, v in changes.modifications.items() if not m.isTextType(k)})  # type: ChangeSet  # line 460
    if modified(onlyBinaryModifications):  # line 461
        debug("/// File changes")  # line 461
    m.listChanges(onlyBinaryModifications)  # only list modified binary files  # line 462

    if changes.modifications:  # TODO only text files, not binary  # line 464
        debug("%s/// Textual modifications" % ("\n" if modified(onlyBinaryModifications) else ""))  # TODO only text files, not binary  # line 464
    for path, pinfo in changes.modifications.items():  # only consider modified files TODO also show A/D here? or replace listing above?  # line 465
        content = None  # type: _coconut.typing.Optional[bytes]  # ; othr:str[]; curr:str[]  # line 466
        if pinfo.size == 0:  # empty file contents  # line 467
            content = b""  # empty file contents  # line 467
        else:  # versioned file  # line 468
            content = m.restoreFile(None, branch, revision, pinfo)  # versioned file  # line 468
            assert content is not None  # versioned file  # line 468
        abspath = os.path.join(m.root, path.replace(SLASH, os.sep))  # current file  # line 469
        blocks = merge(file=content, intoname=abspath, diffOnly=True)  # type: List[MergeBlock]  # only determine change blocks  # line 470
        print("DIF %s%s" % (path, " <timestamp only>" if len(blocks) == 1 and blocks[0].tipe == MergeBlockType.KEEP else ""))  # line 471
        for block in blocks:  # line 472
            if block.tipe in [MergeBlockType.INSERT, MergeBlockType.REMOVE]:  # line 473
                pass  # TODO print some previous and following lines - which aren't accessible here anymore  # line 474
            if block.tipe == MergeBlockType.INSERT:  # TODO show color via curses?  # line 475
                for no, line in enumerate(block.lines):  # line 476
                    print("+++ %04d |%s|" % (no + block.line, line))  # line 477
            elif block.tipe == MergeBlockType.REMOVE:  # line 478
                for no, line in enumerate(block.lines):  # line 479
                    print("--- %04d |%s|" % (no + block.line, line))  # line 480
            elif block.tipe in [MergeBlockType.REPLACE, MergeBlockType.MODIFY]:  # TODO for MODIFY also show intra-line change ranges  # line 481
                for no, line in enumerate(block.replaces.lines):  # line 482
                    print("- | %04d |%s|" % (no + block.replaces.line, line))  # line 483
                for no, line in enumerate(block.lines):  # line 484
                    print("+ | %04d |%s|" % (no + block.line, line))  # line 485
#      elif block.tipe == MergeBlockType.KEEP: pass
#      elif block.tipe == MergeBlockType.MODIFY:  # intra-line modifications
#      elif block.tipe == MergeBlockType.MOVE:  # intra-line modifications

def commit(argument: '_coconut.typing.Optional[str]'=None, options: '_coconut.typing.Sequence[str]'=[]) -> 'None':  # line 490
    ''' Create new revision from file tree changes vs. last commit. '''  # line 491
    changes = None  # type: ChangeSet  # line 492
    m, branch, revision, changes, strict, force, trackingPatterns = exitOnChanges(None, options, commit=True)  # special flag creates new revision for detected changes, but abort if no changes  # line 493
    info((lambda _coconut_none_coalesce_item: "b%d" % m.branch if _coconut_none_coalesce_item is None else _coconut_none_coalesce_item)("Committing changes to branch '%s'..." % m.branches[m.branch].name))  # line 494
    m.integrateChangeset(changes, clear=True)  # update pathset to changeset only  # line 495
    m.saveCommit(m.branch, revision)  # revision has already been incremented  # line 496
    m.commits[revision] = CommitInfo(revision, int(time.time() * 1000), argument)  # comment can be None  # line 497
    m.saveBranch(m.branch)  # line 498
    m.loadBranches()  # TODO is it necessary to load again?  # line 499
    if m.picky:  # HINT was changed from only picky to include track as well  # line 500
        m.branches[m.branch] = dataCopy(BranchInfo, m.branches[m.branch], tracked=[], insync=False)  # remove tracked patterns  # line 501
    else:  # track or simple mode  # line 502
        m.branches[m.branch] = dataCopy(BranchInfo, m.branches[m.branch], insync=False)  # set branch dirty  # line 503
    m.saveBranches()  # line 504
    info("Created new revision r%02d%s (+%02d/-%02d/*%02d)" % (revision, ((" '%s'" % argument) if argument is not None else ""), len(changes.additions), len(changes.deletions), len(changes.modifications)))  # line 505

def status() -> 'None':  # line 507
    ''' Show branches and current repository state. '''  # line 508
    m = Metadata(os.getcwd())  # type: Metadata  # line 509
    m.loadBranches()  # knows current branch  # line 510
    current = m.branch  # type: int  # line 511
    info("/// Offline repository status")  # line 512
    sl = max([len((lambda _coconut_none_coalesce_item: "" if _coconut_none_coalesce_item is None else _coconut_none_coalesce_item)(b.name)) for b in m.branches.values()])  # type: int  # line 513
    for branch in sorted(m.branches.values(), key=lambda b: b.number):  # line 514
        m.loadBranch(branch.number)  # knows commit history  # line 515
        print("  %s b%02d%s @%s (%s) with %d commits%s" % ("*" if current == branch.number else " ", branch.number, ((" %%%ds" % (sl + 2)) % ("'%s'" % branch.name)) if branch.name else "", strftime(branch.ctime), "in sync" if branch.insync else "dirty", len(m.commits), ". Last comment: '%s'" % m.commits[max(m.commits)].message if m.commits[max(m.commits)].message else ""))  # line 516
    if m.track or m.picky and len(m.branches[m.branch].tracked) > 0:  # line 517
        info("\nTracked file patterns:")  # line 518
        print(ajoin("  | ", m.branches[m.branch].tracked, "\n"))  # line 519

def exitOnChanges(argument: '_coconut.typing.Optional[str]'=None, options: '_coconut.typing.Sequence[str]'=[], check: 'bool'=True, commit: 'bool'=False) -> 'Tuple[Metadata, _coconut.typing.Optional[int], int, ChangeSet, bool, bool, FrozenSet[str]]':  # line 521
    ''' Common behavior for switch, update, delete, commit.
      check: stop program on detected change
      commit: don't stop on changes, because that's what we need in the operation
      Returns (Metadata, (current or target) branch, revision, set of changes vs. last commit on current branch, strict, force flags. '''  # line 525
    m = Metadata(os.getcwd())  # type: Metadata  # line 526
    m.loadBranches()  # knows current branch  # line 527
    trackingPatterns = m.getTrackingPatterns()  # type: FrozenSet[str]  # SVN-like mode  # line 528
    force = '--force' in options  # type: bool  # line 529
    strict = '--strict' in options or m.strict  # type: bool  # line 530
    if argument is not None:  # line 531
        branch, revision = m.parseRevisionString(argument)  # for early abort  # line 532
        if branch is None:  # line 533
            Exit("Branch '%s' doesn't exist. Cannot proceed" % argument)  # line 533
    m.loadBranch(m.branch)  # knows last commits of *current* branch  # line 534

# Determine current changes
    m.computeSequentialPathSet(m.branch, max(m.commits))  # load all commits up to specified revision  # line 537
    changes = m.findChanges(m.branch if commit else None, max(m.commits) + 1 if commit else None, checkContent=strict, considerOnly=None if not m.track and not m.picky else trackingPatterns)  # type: ChangeSet  # line 538
    if modified(changes) and not force:  # and check?  # line 539
        m.listChanges(changes)  # line 540
        if check and not commit:  # line 541
            Exit("File tree contains changes. Use --force to proceed")  # line 541
    elif commit and not force:  #  and not check  # line 542
        Exit("Nothing to commit. Aborting")  #  and not check  # line 542

    if argument is not None:  # branch/revision specified  # line 544
        m.loadBranch(branch)  # knows commits of target branch  # line 545
        revision = revision if revision >= 0 else len(m.commits) + revision  # negative indexing  # line 546
        if revision < 0 or revision > max(m.commits):  # line 547
            Exit("Unknown revision r%02d" % revision)  # line 547
        return (m, branch, revision, changes, strict, force, m.getTrackingPatterns(branch))  # line 548
    return (m, m.branch, max(m.commits) + (1 if commit else 0), changes, strict, force, trackingPatterns)  # line 549

def switch(argument: 'str', options: '_coconut.typing.Sequence[str]'=[]) -> 'None':  # line 551
    ''' Continue work on another branch, replacing file tree changes. '''  # line 552
    changes = None  # type: ChangeSet  # line 553
    m, branch, revision, changes, strict, force, trackingPatterns = exitOnChanges(argument, options)  # line 554
    info("/// Switching to branch %sb%02d/r%02d" % ("'%s' " % m.branches[branch].name if m.branches[branch].name else "", branch, revision))  # line 555

# Determine file changes from other branch to current file tree
    if '--meta' in options:  # only switch meta data  # line 558
        m.branches[m.branch] = dataCopy(BranchInfo, m.branches[m.branch], tracked=m.branches[branch].tracked)  # line 559
    else:  # full file switch  # line 560
        m.computeSequentialPathSet(branch, revision)  # load all commits up to specified revision for target branch into memory  # line 561
        changes = m.findChanges(checkContent=strict, inverse=True, considerOnly=None if not m.track else trackingPatterns | m.getTrackingPatterns(branch))  # determine difference of other branch vs. file tree (forced or in sync with current branch; "addition" means exists now and should be removed)  # line 562
        if not modified(changes):  # line 563
            info("No changes to current file tree")  # line 564
        else:  # integration required  # line 565
            for path, pinfo in changes.deletions.items():  # line 566
                m.restoreFile(path, branch, revision, pinfo)  # is deleted in current file tree: restore from branch to reach target  # line 567
                debug("ADD " + path)  # line 568
            for path, pinfo in changes.additions.items():  # line 569
                os.unlink(os.path.join(m.root, path.replace(SLASH, os.sep)))  # is added in current file tree: remove from branch to reach target  # line 570
                debug("DEL " + path)  # line 571
            for path, pinfo in changes.modifications.items():  # line 572
                m.restoreFile(path, branch, revision, pinfo)  # is modified in current file tree: restore from branch to reach target  # line 573
                debug("MOD " + path)  # line 574
    m.branch = branch  # line 575
    m.saveBranches()  # store switched path info  # line 576
    info("Switched to branch %sb%02d/r%02d" % ("'%s' " % (m.branches[branch].name if m.branches[branch].name else ""), branch, revision))  # line 577

def update(argument: 'str', options: '_coconut.typing.Sequence[str]'=[]) -> 'None':  # line 579
    ''' Load and integrate a specified other branch/revision into current life file tree.
      In tracking mode, this also updates the set of tracked patterns.
      User options for merge operation: --add (don't remove), --rm (don't insert), --add-lines/--rm-lines (inside each file)
      User options for conflict resolution: --theirs/--mine/--ask
  '''  # line 584
    mrg = firstOfMap({"--add": MergeOperation.INSERT, "--rm": MergeOperation.REMOVE}, options, MergeOperation.BOTH)  # type: int  # default operation is replicate remove state for non-conflicting cases (insertions/deletions)  # line 585
    res = firstOfMap({'--theirs': ConflictResolution.THEIRS, '--mine': ConflictResolution.MINE}, options, ConflictResolution.NEXT)  # type: int  # NEXT means deeper level  # line 586
    mrgline = firstOfMap({'--add-lines': MergeOperation.INSERT, '--rm-lines': MergeOperation.REMOVE}, options, mrg)  # type: int  # default operation for modified files is same as for files  # line 587
    resline = firstOfMap({'--theirs-lines': ConflictResolution.THEIRS, '--mine-lines': ConflictResolution.MINE}, options, ConflictResolution.ASK)  # type: int  # line 588
    m = Metadata(os.getcwd())  # type: Metadata  # TODO same is called inside stop on changes - could return both current and designated branch instead  # line 589
    m.loadBranches()  # line 590
    changes = None  # type: ChangeSet  # line 590
    currentBranch = m.branch  # type: _coconut.typing.Optional[int]  # line 591
    m, branch, revision, changes, strict, force, trackingPatterns = exitOnChanges(argument, options, check=False)  # don't check for current changes, only parse arguments  # line 592
    debug("Integrating changes from '%s/r%02d' into file tree..." % ((lambda _coconut_none_coalesce_item: "b%02d" % branch if _coconut_none_coalesce_item is None else _coconut_none_coalesce_item)(m.branches[branch].name), revision))  # line 593

# Determine file changes from other branch over current file tree
    m.computeSequentialPathSet(branch, revision)  # load all commits up to specified revision for branch to integrate  # line 596
    trackingUnion = trackingPatterns | m.getTrackingPatterns(branch)  # type: FrozenSet[str]  # line 597
    changes = m.findChanges(checkContent=strict, inverse=True, considerOnly=None if not m.track else trackingUnion)  # determine difference of other branch vs. file tree. "addition" means exists now but not in other, and should be removed unless in tracking mode  # line 598
    if not (mrg & MergeOperation.INSERT and changes.additions or (mrg & MergeOperation.REMOVE and changes.deletions) or changes.modifications):  # line 599
        if trackingUnion == trackingPatterns:  # nothing added  # line 600
            info("No file changes detected, but tracking patterns were merged (run 'sos switch /-1 --meta' to undo)")  # TODO write test to see if this works  # line 601
        else:  # line 602
            info("Nothing to update")  # but write back updated branch info below  # line 603
    else:  # integration required  # line 604
        for path, pinfo in changes.deletions.items():  # deletions mark files not present in current file tree -> needs additon  # line 605
            if mrg & MergeOperation.INSERT:  # deleted in current file tree: restore from branch to reach target  # line 606
                m.restoreFile(path, branch, revision, pinfo)  # deleted in current file tree: restore from branch to reach target  # line 606
            print("ADD " + path if mrg & MergeOperation.INSERT else "(A) " + path)  # line 607
        for path, pinfo in changes.additions.items():  # line 608
            if m.track or m.picky:  # because untracked files of other branch cannot be detected (which is good)  # line 609
                Exit("This should never happen")  # because untracked files of other branch cannot be detected (which is good)  # line 609
            if mrg & MergeOperation.REMOVE:  # line 610
                os.unlink(m.root + os.sep + path.replace(SLASH, os.sep))  # line 610
            print("DEL " if mrg & MergeOperation.REMOVE else "(D) " + path)  # not contained in other branch, but maybe kept  # line 611
        for path, pinfo in changes.modifications.items():  # line 612
            into = os.path.join(m.root, path.replace(SLASH, os.sep))  # type: str  # line 613
            binary = not m.isTextType(path)  # line 614
            if res & ConflictResolution.ASK or (binary and res == ConflictResolution.NEXT):  # TODO this may ask user even if no interaction was asked for (check line level for interactivity fist)  # line 615
                print(("MOD " if not binary else "BIN ") + path)  # line 616
                reso = {"i": ConflictResolution.MINE, "t": ConflictResolution.THEIRS, "m": ConflictResolution.NEXT}.get(user_input(" Resolve: *M[I]ne, [T]heirs, [M]erge: (I)").strip().lower(), ConflictResolution.MINE)  # line 617
                debug("User selected %d" % reso)  # line 618
            else:  # line 619
                reso = res  # line 619
            if reso & ConflictResolution.THEIRS:  # line 620
                m.readOrCopyVersionedFile(branch, revision, pinfo.namehash, toFile=into)  # blockwise copy of contents  # line 621
                print("THR " + path)  # line 622
            elif reso & ConflictResolution.MINE:  # line 623
                print("MNE " + path)  # nothing to do! same as skip  # line 624
            else:  # NEXT: line-based merge  # line 625
                file = m.readOrCopyVersionedFile(branch, revision, pinfo.namehash) if pinfo.size > 0 else b''  # type: _coconut.typing.Optional[bytes]  # parse lines TODO decode etc.  # line 626
                if file is not None:  # if None, error message was already logged  # line 627
                    contents = merge(file=file, intoname=into, mergeOperation=mrgline, conflictResolution=resline)  # type: bytes  # line 628
                    with open(path, "wb") as fd:  # TODO write to temp file first  # line 629
                        fd.write(contents)  # TODO write to temp file first  # line 629
    info("Integrated changes from '%s/r%02d' into file tree" % ((lambda _coconut_none_coalesce_item: "b%02d" % branch if _coconut_none_coalesce_item is None else _coconut_none_coalesce_item)(m.branches[branch].name), revision))  # line 630
    m.branches[currentBranch] = dataCopy(BranchInfo, m.branches[currentBranch], insync=False, tracked=list(trackingUnion))  # TODO really? it's a change that cannot be undone easily by the user  # line 631
    m.branch = currentBranch  # need to restore setting before saving TODO operate on different objects instead  # line 632
    m.saveBranches()  # line 633

def delete(argument: 'str', options: '_coconut.typing.Sequence[str]'=[]) -> 'None':  # line 635
    ''' Remove a branch entirely. '''  # line 636
    m, branch, revision, changes, strict, force, trackingPatterns = exitOnChanges(None, options)  # line 637
    if len(m.branches) == 1:  # line 638
        Exit("Cannot remove the only remaining branch. Use 'sos online' to leave offline mode")  # line 638
    branch, revision = m.parseRevisionString(argument)  # not from exitOnChanges, because we have to set argument to None there  # line 639
    if branch is None or branch not in m.branches:  # line 640
        Exit("Unknown branch")  # line 640
    debug("Removing branch %d%s..." % (branch, " '%s'" % m.branches[branch].name if m.branches[branch].name else ""))  # line 641
    binfo = m.removeBranch(branch)  # need to keep a reference to removed entry for output below  # line 642
    info("Branch b%02d%s removed" % (branch, " '%s'" % binfo.name if binfo.name else ""))  # line 643

def add(folder: 'str', argument: 'str', options: '_coconut.typing.Sequence[str]'=[]) -> 'None':  # line 645
    ''' Add a tracked files pattern to current branch's tracked files. '''  # line 646
    force = '--force' in options  # type: bool  # line 647
    m = Metadata(os.getcwd())  # type: Metadata  # line 648
    m.loadBranches()  # line 649
    if not m.track and not m.picky:  # line 650
        Exit("Repository is in simple mode. Needs 'offline --track' or 'offline --picky' instead")  # line 650
    relpath = os.path.relpath(os.path.dirname(os.path.abspath(os.path.join(folder, argument))), m.root)  # for tracking list  # line 651
    pattern = os.path.join(relpath, os.path.basename(argument)).replace(os.sep, SLASH)  # line 652
    if pattern in m.branches[m.branch].tracked:  # line 653
        Exit("Pattern '%s' already tracked")  # line 654
    if not force and len(fnmatch.filter(os.listdir(os.path.abspath(relpath)), os.path.basename(pattern.replace(SLASH, os.sep)))) == 0:  # doesn't match any current file  # line 655
        Exit("Pattern doesn't match any file in specified folder. Use --force to add it anyway")  # line 656
    m.branches[m.branch].tracked.append(pattern)  # TODO set insync flag to False? same for rm  # line 657
    m.saveBranches()  # line 658
    info("Added tracking pattern '%s' for folder '%s'" % (os.path.basename(pattern.replace(SLASH, os.sep)), os.path.abspath(relpath)))  # line 659

def rm(folder: 'str', argument: 'str') -> 'None':  # line 661
    ''' Remove a tracked files pattern from current branch's tracked files. '''  # line 662
    m = Metadata(os.getcwd())  # type: Metadata  # line 663
    m.loadBranches()  # line 664
    if not m.track and not m.picky:  # line 665
        Exit("Repository is in simple mode. Needs 'offline --track' or 'offline --picky' instead")  # line 665
    relpath = os.path.relpath(os.path.dirname(os.path.abspath(os.path.join(folder, argument))), m.root)  # type: str  # line 666
    pattern = os.path.join(relpath, os.path.basename(argument)).replace(os.sep, SLASH)  # type: str  # line 667
    if pattern not in m.branches[m.branch].tracked:  # line 668
        suggestion = _coconut.set()  # type: Set[str]  # line 669
        for pat in m.branches[m.branch].tracked:  # line 670
            if fnmatch.fnmatch(pattern, pat):  # line 671
                suggestion.add(pat)  # line 671
        if suggestion:  # line 672
            print("Do you mean any of the following tracked globs? '%s'" % (", ".join(sorted(suggestion))))  # line 672
        Exit("Tracked pattern '%s' not found" % pattern)  # line 673
    m.branches[m.branch].tracked.remove(pattern)  # line 674
    m.saveBranches()  # line 675
    info("Removed tracking pattern '%s' for folder '%s'" % (os.path.basename(pattern.replace(SLASH, os.sep)), os.path.abspath(relpath)))  # line 676

def ls(argument: '_coconut.typing.Optional[str]'=None) -> 'None':  # line 678
    ''' List specified directory, augmenting with repository metadata. '''  # line 679
    cwd = os.getcwd() if argument is None else argument  # type: str  # line 680
    m = Metadata(cwd)  # type: Metadata  # line 681
    m.loadBranches()  # line 682
    relpath = os.path.relpath(cwd, m.root).replace(os.sep, SLASH)  # type: str  # line 683
    files = list(sorted((entry for entry in os.listdir(cwd) if os.path.isfile(entry))))  # type: List[str]  # line 684
    trackingPatterns = m.getTrackingPatterns() if m.track or m.picky else _coconut.frozenset()  # type: FrozenSet[str]  # for current branch  # line 685
    for file in files:  # line 686
        ignore = None  # type: _coconut.typing.Optional[str]  # line 687
        for ig in m.c.ignores:  # line 688
            if fnmatch.fnmatch(file, ig):  # remember first match TODO document this  # line 689
                ignore = ig  # remember first match TODO document this  # line 689
                break  # remember first match TODO document this  # line 689
        if ig:  # line 690
            for wl in m.c.ignoresWhitelist:  # line 691
                if fnmatch.fnmatch(file, wl):  # found a white list entry for ignored file, undo ignoring it  # line 692
                    ignore = None  # found a white list entry for ignored file, undo ignoring it  # line 692
                    break  # found a white list entry for ignored file, undo ignoring it  # line 692
        if ignore is None:  # line 693
            matches = []  # type: List[str]  # line 694
            for pattern in (p for p in trackingPatterns if os.path.dirname(p) == relpath):  # only patterns matching current folder  # line 695
                if fnmatch.fnmatch(file, os.path.basename(pattern)):  # TODO or only file basename?  # line 696
                    matches.append(pattern)  # TODO or only file basename?  # line 696
        print("%s %s%s" % ("IGN" if ignore is not None else ("TRK" if len(matches) > 0 else "   "), file, ' by "%s"' % ignore if ignore is not None else (" by " + ";".join(['"%s"' % match for match in matches]) if len(matches) > 0 else "")))  # line 697

def log() -> 'None':  # line 699
    ''' List previous commits on current branch. '''  # TODO --verbose for changesets  # line 700
    m = Metadata(os.getcwd())  # type: Metadata  # line 701
    m.loadBranches()  # knows current branch  # line 702
    m.loadBranch(m.branch)  # knows commit history  # line 703
    info((lambda _coconut_none_coalesce_item: "r%02d" % m.branch if _coconut_none_coalesce_item is None else _coconut_none_coalesce_item)("/// Offline commit history of branch '%s'" % m.branches[m.branch].name))  # TODO also retain "from branch/revision" on branching?  # line 704
    nl = len("%d" % max(m.commits))  # determine space needed for revision  # line 705
    changeset = m.computeSequentialPathSetIterator(m.branch, max(m.commits))  # line 706
    for no in range(max(m.commits) + 1):  # line 707
        commit = m.commits[no]  # type: CommitInfo  # line 708
        changes = next(changeset)  # type: ChangeSet  # side-effect: updates m.paths  # line 709
        print("  %s r%s @%s (+%02d/-%02d/*%02d): %s" % ("*" if commit.number == max(m.commits) else " ", ("%%%ds" % nl) % commit.number, strftime(commit.ctime), len(changes.additions), len(changes.deletions), len(changes.modifications), (lambda _coconut_none_coalesce_item: "" if _coconut_none_coalesce_item is None else _coconut_none_coalesce_item)(commit.message)))  # line 710
# TODO list number of files and if binary/text

def config(argument: 'str', options: 'List[str]'=[]) -> 'None':  # line 713
    if argument not in ["set", "unset", "show", "list", "add", "rm"]:  # line 714
        Exit("Unknown config command")  # line 714
    if not configr:  # line 715
        Exit("Cannot execute config command. 'configr' module not installed")  # line 715
    c = loadConfig()  # type: Union[configr.Configr, Accessor]  # line 716
    if argument == "set":  # line 717
        if len(options) < 2:  # line 718
            Exit("No key nor value specified")  # line 718
        if options[0] not in (["defaultbranch"] + CONFIGURABLE_FLAGS + CONFIGURABLE_LISTS):  # line 719
            Exit("Unsupported key %r" % options[0])  # line 719
        if options[0] in CONFIGURABLE_FLAGS and options[1].lower() not in TRUTH_VALUES + FALSE_VALUES:  # line 720
            Exit("Cannot set flag to '%s'. Try on/off instead" % options[1].lower())  # line 720
        c[options[0]] = options[1].lower() in TRUTH_VALUES if options[0] in CONFIGURABLE_FLAGS else (options[1].strip() if options[0] not in CONFIGURABLE_LISTS else safeSplit(options[1], ";"))  # TODO sanitize texts?  # line 721
    elif argument == "unset":  # line 722
        if len(options) < 1:  # line 723
            Exit("No key specified")  # line 723
        if options[0] not in c.keys():  # line 724
            Exit("Unknown key")  # line 724
        del c[options[0]]  # line 725
    elif argument == "add":  # line 726
        if len(options) < 2:  # line 727
            Exit("No key nor value specified")  # line 727
        if options[0] not in CONFIGURABLE_LISTS:  # line 728
            Exit("Unsupported key for add %r" % options[0])  # line 728
        if options[0] not in c.keys():  # add list  # line 729
            c[options[0]] = [options[1]]  # add list  # line 729
        elif options[1] in c[options[0]]:  # line 730
            Exit("Value already contained")  # line 730
        c[options[0]].append(options[1])  # line 731
    elif argument == "rm":  # line 732
        if len(options) < 2:  # line 733
            Exit("No key nor value specified")  # line 733
        if options[0] not in c.keys():  # line 734
            Exit("Unknown key specified: %r" % options[0])  # line 734
        if options[1] not in c[options[0]]:  # line 735
            Exit("Unknown value: %r" % options[1])  # line 735
        c[options[0]].remove(options[1])  # line 736
    else:  # Show  # line 737
        for k, v in sorted(c.items()):  # line 738
            print("%s => %r" % (k, v))  # line 738
        return  # line 739
    f, g = saveConfig(c)  # line 740
    if f is None:  # line 741
        error("Error saving user configuration: %r" % g)  # line 741

def parse(root: 'str', inFolder: 'str'):  # line 743
    ''' Main operation. '''  # line 744
    debug("Parsing command-line arguments...")  # line 745
    command = sys.argv[1].strip() if len(sys.argv) > 1 else ""  # line 746
    argument = sys.argv[2].strip() if len(sys.argv) > 2 else None  # line 747
    options = sys.argv[3:] if command == "config" else [c for c in sys.argv[2:] if c.startswith("--")]  # consider second parameter for no-arg command, otherwise from third on  # line 748
    debug("Processing command %r with argument '%s' and options %r." % ("" if command is None else command, "" if argument is None else argument, options))  # line 749
    if command[:1] == "a":  # line 750
        add(inFolder, argument, options)  # line 750
    elif command[:1] == "b":  # line 751
        branch(argument, options)  # line 751
    elif command[:2] == "ch":  # line 752
        changes(argument, options)  # line 752
    elif command[:3] == "com" or command[:2] == "ci":  # line 753
        commit(argument, options)  # line 753
    elif command[:3] == 'con':  # line 754
        config(argument, options)  # line 754
    elif command[:2] == "de":  # line 755
        delete(argument, options)  # line 755
    elif command[:2] == "di":  # line 756
        diff(argument, options)  # line 756
    elif command[:1] == "h":  # line 757
        usage()  # line 757
    elif command[:2] == "lo":  # line 758
        log()  # line 758
    elif command[:2] in ["li", "ls"]:  # line 759
        ls(argument)  # line 759
    elif command[:2] == "of":  # line 760
        offline(argument, options)  # line 760
    elif command[:2] == "on":  # line 761
        online(options)  # line 761
    elif command[:1] == "r":  # line 762
        rm(inFolder, argument)  # line 762
    elif command[:2] == "st":  # line 763
        status()  # line 763
    elif command[:2] == "sw":  # line 764
        switch(argument, options)  # line 764
    elif command[:2] == "u":  # line 765
        update(argument, options)  # line 765
    else:  # line 766
        Exit("Unknown command '%s'" % command)  # line 766
    sys.exit(0)  # line 767

def main() -> 'None':  # line 769
    global debug, info, warn, error  # line 770
    logging.basicConfig(level=level, stream=sys.stderr, format=("%(asctime)-23s %(levelname)-8s %(name)s:%(lineno)d | %(message)s" if '--log' in sys.argv else "%(message)s"))  # line 771
    _log = Logger(logging.getLogger(__name__))  # line 772
    debug, info, warn, error = _log.debug, _log.info, _log.warn, _log.error  # line 772
    for option in (o for o in ['--log', '--verbose', '-v', '--sos'] if o in sys.argv):  # clean up program arguments  # line 773
        sys.argv.remove(option)  # clean up program arguments  # line 773
    if '--help' in sys.argv or len(sys.argv) < 2:  # line 774
        usage()  # line 774
        Exit()  # line 774
    command = sys.argv[1] if len(sys.argv) > 1 else None  # type: _coconut.typing.Optional[str]  # line 775
    root, vcs, cmd = findSosVcsBase()  # root is None if no .sos folder exists up the folder tree (still working online); vcs is checkout/repo root folder; cmd is the VCS base command  # line 776
    debug("Found root folders for SOS|VCS: %s|%s" % ("" if root is None else root, "" if vcs is None else vcs))  # line 777
    defaults["defaultbranch"] = vcsBranches.get(cmd, "trunk")  # sets dynamic default with SVN fallback  # line 778
    if force_sos or root is not None or ("" if command is None else command)[:2] == "of" or ("" if command is None else command)[:1] == "h":  # in offline mode or just going offline TODO what about git config?  # line 779
        cwd = os.getcwd()  # line 780
        os.chdir(cwd if command[:2] == "of" else cwd if root is None else root)  # line 781
        parse(root, cwd)  # line 782
    elif cmd is not None:  # online mode - delegate to VCS  # line 783
        info("SOS: Running '%s %s'" % (cmd, " ".join(sys.argv[1:])))  # line 784
        import subprocess  # only requuired in this section  # line 785
        process = subprocess.Popen([cmd] + sys.argv[1:], shell=False, stdin=subprocess.PIPE, stdout=sys.stdout, stderr=sys.stderr)  # line 786
        inp = ""  # type: str  # line 787
        while True:  # line 788
            so, se = process.communicate(input=inp)  # line 789
            if process.returncode is not None:  # line 790
                break  # line 790
            inp = sys.stdin.read()  # line 791
        if sys.argv[1][:2] == "co" and process.returncode == 0:  # successful commit - assume now in sync again (but leave meta data folder with potential other feature branches behind until "online")  # line 792
            if root is None:  # line 793
                Exit("Cannot determine VCS root folder: Unable to mark repository as synchronized and will show a warning when leaving offline mode")  # line 793
            m = Metadata(root)  # line 794
            m.loadBranches()  # read repo  # line 795
            m.branches[m.branch] = dataCopy(BranchInfo, m.branches[m.branch], insync=True)  # mark as committed  # line 796
            m.saveBranches()  # line 797
    else:  # line 798
        Exit("No offline repository present, and unable to detect VCS file tree")  # line 798


# Main part
level = logging.DEBUG if os.environ.get("DEBUG", "False").lower() == "true" or '--verbose' in sys.argv or '-v' in sys.argv else logging.INFO  # line 802
force_sos = '--sos' in sys.argv  # line 803
_log = Logger(logging.getLogger(__name__))  # line 804
debug, info, warn, error = _log.debug, _log.info, _log.warn, _log.error  # line 804
if __name__ == '__main__':  # line 805
    main()  # line 805
