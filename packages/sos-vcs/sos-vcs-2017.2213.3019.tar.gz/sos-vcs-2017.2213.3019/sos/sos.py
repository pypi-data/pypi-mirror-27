#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# __coconut_hash__ = 0x91135e36

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
    --verbose                   Enable debugging output""".format(appname=APPNAME, cmd="sos", CMD="SOS"))  # line 91

# Main data class
#@runtime_validation
class Metadata:  # line 95
    ''' This class doesn't represent the entire repository state in memory,
      but serves as a container for different repo operations,
      using only parts of its attributes at any point in time. Use with care.
  '''  # line 99

    def __init__(_, path: 'str') -> 'None':  # line 101
        ''' Create empty container object for various repository operations. '''  # line 102
        _.c = loadConfig()  # line 103
        _.root = path  # type: str  # line 104
        _.branches = {}  # type: Dict[int, BranchInfo]  # branch number zero represents the initial state at branching  # line 105
        _.commits = {}  # type: Dict[int, CommitInfo]  # consecutive numbers per branch, starting at 0  # line 106
        _.paths = {}  # type: Dict[str, PathInfo]  # utf-8 encoded relative, normalized file system paths  # line 107
        _.track = _.c.track  # type: bool  # track files in the repository (tracked patterns are stored for each branch separately)  # line 108
        _.picky = _.c.picky  # type: bool  # pick files on each operation  # line 109
        _.strict = _.c.strict  # type: bool  # be always strict (regarding file contents comparsion)  # line 110
        _.compress = _.c.compress  # type: bool  # these flags are stored per branch, therefore not part of the (default) configuration  # line 111
        _.branch = None  # type: _coconut.typing.Optional[int]  # current branch number  # line 112
        _.commit = None  # type: _coconut.typing.Optional[int]  # current revision number  # line 113

    def isTextType(_, filename: 'str') -> 'bool':  # line 115
        return (((lambda _coconut_none_coalesce_item: "" if _coconut_none_coalesce_item is None else _coconut_none_coalesce_item)(mimetypes.guess_type(filename)[0])).startswith("text/") or any([fnmatch.fnmatch(filename, pattern) for pattern in _.c.texttype])) and not any([fnmatch.fnmatch(filename, pattern) for pattern in _.c.bintype])  # line 115

    def listChanges(_, changes: 'ChangeSet') -> 'None':  # line 117
        ''' In diffmode, don't list modified files, because the diff is displayed elsewhere. '''  # line 118
        if len(changes.additions) > 0:  # line 119
            print(ajoin("ADD ", sorted(changes.additions.keys()), "\n"))  # line 119
        if len(changes.deletions) > 0:  # line 120
            print(ajoin("DEL ", sorted(changes.deletions.keys()), "\n"))  # line 120
        if len(changes.modifications) > 0:  # line 121
            print(ajoin("MOD ", sorted(changes.modifications.keys()), "\n"))  # line 121

    def loadBranches(_) -> 'None':  # line 123
        ''' Load list of branches and current branch info from metadata file. '''  # line 124
        try:  # fails if not yet created (on initial branch/commit)  # line 125
            branches = None  # type: List[Tuple]  # line 126
            with codecs.open(os.path.join(_.root, metaFolder, metaFile), "r", encoding=UTF8) as fd:  # line 127
                flags, branches = json.load(fd)  # line 128
            _.branch = flags["branch"]  # line 129
            _.track = flags["track"]  # line 130
            _.picky = flags["picky"]  # line 131
            _.strict = flags["strict"]  # line 132
            _.compress = flags["compress"]  # line 133
            _.branches = {i.number: i for i in (BranchInfo(*item) for item in branches)}  # re-create type info  # line 134
        except Exception as E:  # if not found, create metadata folder  # line 135
            _.branches = {}  # line 136
            warn("Couldn't read branches metadata: %r" % E)  # line 137

    def saveBranches(_) -> 'None':  # line 139
        ''' Save list of branches and current branch info to metadata file. '''  # line 140
        with codecs.open(os.path.join(_.root, metaFolder, metaFile), "w", encoding=UTF8) as fd:  # line 141
            json.dump(({"branch": _.branch, "track": _.track, "picky": _.picky, "strict": _.strict, "compress": _.compress}, list(_.branches.values())), fd, ensure_ascii=False)  # line 142

    def getBranchByName(_, name: 'Union[str, int]') -> '_coconut.typing.Optional[int]':  # line 144
        ''' Convenience accessor for named branches. '''  # line 145
        if isinstance(name, int):  # if type(name) is int: return name  # line 146
            return name  # if type(name) is int: return name  # line 146
        try:  # attempt to parse integer string  # line 147
            return int(name)  # attempt to parse integer string  # line 147
        except ValueError:  # line 148
            pass  # line 148
        found = [number for number, branch in _.branches.items() if name == branch.name]  # line 149
        return found[0] if found else None  # line 150

    def loadBranch(_, branch: 'int') -> 'None':  # line 152
        ''' Load all commit information from a branch meta data file. '''  # line 153
        with codecs.open(os.path.join(_.root, metaFolder, "b%d" % branch, metaFile), "r", encoding=UTF8) as fd:  # line 154
            commits = json.load(fd)  # type: List[List[Any]]  # list of CommitInfo that needs to be unmarshalled into value types  # line 155
        _.commits = {i.number: i for i in (CommitInfo(*item) for item in commits)}  # re-create type info  # line 156
        _.branch = branch  # line 157

    def saveBranch(_, branch: 'int') -> 'None':  # line 159
        ''' Save all commit information to a branch meta data file. '''  # line 160
        with codecs.open(os.path.join(_.root, metaFolder, "b%d" % branch, metaFile), "w", encoding=UTF8) as fd:  # line 161
            json.dump(list(_.commits.values()), fd, ensure_ascii=False)  # line 162

    def duplicateBranch(_, branch: 'int', name: '_coconut.typing.Optional[str]') -> 'None':  # line 164
        ''' Create branch from an existing branch/revision. WARN: Caller must have loaded branches information.
        branch: target branch (should not exist yet)
        name: optional name of new branch
        _.branch: current branch
    '''  # line 169
        debug("Duplicating branch '%s' to '%d'..." % ((lambda _coconut_none_coalesce_item: "b%d" % _.branch if _coconut_none_coalesce_item is None else _coconut_none_coalesce_item)(_.branches[_.branch].name), branch))  # line 170
        tracked = [t for t in _.branches[_.branch].tracked]  # copy  # line 171
        os.makedirs(os.path.join(_.root, metaFolder, "b%d" % branch, "r0"))  # line 172
        _.loadBranch(_.branch)  # line 173
        revision = max(_.commits)  # type: int  # line 174
        _.computeSequentialPathSet(_.branch, revision)  # full set of files in revision to _.paths  # line 175
        for path, pinfo in _.paths.items():  # line 176
            _.copyVersionedFile(_.branch, revision, branch, 0, pinfo)  # line 177
        _.commits = {0: CommitInfo(0, int(time.time() * 1000), "Branched from '%s'" % ((lambda _coconut_none_coalesce_item: "b%d" % _.branch if _coconut_none_coalesce_item is None else _coconut_none_coalesce_item)(_.branches[_.branch].name)))}  # store initial commit  # line 178
        _.saveBranch(branch)  # save branch meta data to branch folder  # line 179
        _.saveCommit(branch, 0)  # save commit meta data to revision folder  # line 180
        _.branches[branch] = BranchInfo(branch, _.commits[0].ctime, name, _.branches[_.branch].insync, tracked)  # save branch info, before storing repo state at caller  # line 181

    def createBranch(_, branch: 'int', name: '_coconut.typing.Optional[str]'=None, initialMessage: '_coconut.typing.Optional[str]'=None):  # line 183
        ''' Create a new branch from current file tree. This clears all known commits and modifies the file system.
        branch: target branch (should not exist yet)
        name: optional name of new branch
        _.branch: current branch, must exist already
    '''  # line 188
        simpleMode = not (_.track or _.picky)  # line 189
        tracked = [t for t in _.branches[_.branch].tracked] if _.track and len(_.branches) > 0 else []  # in case of initial branch creation  # line 190
        debug((lambda _coconut_none_coalesce_item: "b%d" % branch if _coconut_none_coalesce_item is None else _coconut_none_coalesce_item)("Creating branch '%s'..." % name))  # line 191
        _.paths = {}  # type: Dict[str, PathInfo]  # line 192
        if simpleMode:  # branches from file system state  # line 193
            changes = _.findChanges(branch, 0, progress=simpleMode)  # type: ChangeSet  # creates revision folder and versioned files  # line 194
            _.listChanges(changes)  # line 195
            _.paths.update(changes.additions.items())  # line 196
        else:  # tracking or picky mode: branch from lastest revision  # line 197
            os.makedirs(os.path.join(_.root, metaFolder, "b%d" % branch, "r0"))  # line 198
            if _.branch is not None:  # not immediately after "offline" - copy files from current branch  # line 199
                _.loadBranch(_.branch)  # line 200
                revision = max(_.commits)  # type: int  # TODO what if last switch was to an earlier revision? no persisting of last checkout  # line 201
                _.computeSequentialPathSet(_.branch, revision)  # full set of files in revision to _.paths  # line 202
                for path, pinfo in _.paths.items():  # line 203
                    _.copyVersionedFile(_.branch, revision, branch, 0, pinfo)  # line 204
        ts = int(time.time() * 1000)  # line 205
        _.commits = {0: CommitInfo(0, ts, "Branched on %s" % strftime(ts) if initialMessage is None else initialMessage)}  # store initial commit for new branch  # line 206
        _.saveBranch(branch)  # save branch meta data (revisions) to branch folder  # line 207
        _.saveCommit(branch, 0)  # save commit meta data to revision folder  # line 208
        _.branches[branch] = BranchInfo(branch, _.commits[0].ctime, name, True if len(_.branches) == 0 else _.branches[_.branch].insync, tracked)  # save branch info, in case it is needed  # line 209

    def removeBranch(_, branch: 'int') -> 'BranchInfo':  # line 211
        ''' Entirely remove a branch and all its revisions from the file system. '''  # line 212
        shutil.rmtree(os.path.join(_.root, metaFolder, "b%d" % branch))  # line 213
        binfo = _.branches[branch]  # line 214
        del _.branches[branch]  # line 215
        _.branch = max(_.branches)  # line 216
        _.saveBranches()  # line 217
        _.commits.clear()  # line 218
        return binfo  # line 219

    def loadCommit(_, branch: 'int', revision: 'int') -> 'None':  # line 221
        ''' Load all file information from a commit meta data. '''  # line 222
        with codecs.open(os.path.join(_.root, metaFolder, "b%d" % branch, "r%d" % revision, metaFile), "r", encoding=UTF8) as fd:  # line 223
            _.paths = json.load(fd)  # line 224
        _.paths = {path: PathInfo(*item) for path, item in _.paths.items()}  # re-create type info  # line 225
        _.branch = branch  # line 226

    def saveCommit(_, branch: 'int', revision: 'int'):  # line 228
        ''' Save all file information to a commit meta data file. '''  # line 229
        target = os.path.join(_.root, metaFolder, "b%d" % branch, "r%d" % revision)  # line 230
        try:  # line 231
            os.makedirs(target)  # line 231
        except:  # line 232
            pass  # line 232
        with codecs.open(os.path.join(target, metaFile), "w", encoding=UTF8) as fd:  # line 233
            json.dump(_.paths, fd, ensure_ascii=False)  # line 234

    def findChanges(_, branch: '_coconut.typing.Optional[int]'=None, revision: '_coconut.typing.Optional[int]'=None, checkContent: 'bool'=False, inverse: 'bool'=False, considerOnly: '_coconut.typing.Optional[FrozenSet[str]]'=None, progress: 'bool'=False) -> 'ChangeSet':  # line 236
        ''' Find changes on the file system vs. in-memory paths (which should reflect the latest commit state).
        Only if both branch and revision are *not* None, write modified/added files to the specified revision folder (thus creating a new revision)
        The function returns the state of file tree *differences*, unless "inverse" is True -> then return original data
        checkContent: also computes file content hashes
        inverse: retain original state (size, mtime, hash) instead of updated one
        considerOnly: set of tracking patterns. For update operation, union of other and current branch
        progress: Show file names during processing
    '''  # line 244
        write = branch is not None and revision is not None  # line 245
        if write:  # line 246
            os.makedirs(os.path.join(_.root, metaFolder, "b%d" % branch, "r%d" % revision))  # line 246
        changes = ChangeSet({}, {}, {})  # type: ChangeSet  # line 247
        counter = Counter(-1)  # type: Counter  # line 248
        timer = time.time()  # line 248
        for path, dirnames, filenames in os.walk(_.root):  # line 249
            dirnames[:] = [f for f in dirnames if len([n for n in _.c.ignoreDirs if fnmatch.fnmatch(f, n)]) == 0 or len([p for p in _.c.ignoreDirsWhitelist if fnmatch.fnmatch(f, p)]) > 0]  # line 250
            filenames[:] = [f for f in filenames if len([n for n in _.c.ignores if fnmatch.fnmatch(f, n)]) == 0 or len([p for p in _.c.ignoresWhitelist if fnmatch.fnmatch(f, p)]) > 0]  # line 251
            dirnames.sort()  # line 252
            filenames.sort()  # line 252
            relpath = os.path.relpath(path, _.root).replace(os.sep, SLASH)  # line 253
            for file in (filenames if considerOnly is None else list(reduce(lambda last, pattern: last | set(fnmatch.filter(filenames, os.path.basename(pattern))), (p for p in considerOnly if os.path.dirname(p) == relpath), _coconut.set()))):  # if m.track or m.picky: only files that match any path-relevant tracking patterns  # line 254
                filename = relpath + SLASH + file  # line 255
                filepath = os.path.join(path, file)  # line 256
                stat = os.stat(filepath)  # line 257
                size, mtime, newtime = stat.st_size, int(stat.st_mtime * 1000), time.time()  # line 258
                if progress and newtime - timer > .1:  # line 259
                    outstring = "\rPreparing %s  %s" % (PROGRESS_MARKER[counter.inc() % 4], filename)  # line 260
                    sys.stdout.write(outstring + " " * max(0, termWidth - len(outstring)))  # TODO could write to new line instead of carriage return, also needs terminal width  # line 261
                    sys.stdout.flush()  # TODO could write to new line instead of carriage return, also needs terminal width  # line 261
                    timer = newtime  # TODO could write to new line instead of carriage return, also needs terminal width  # line 261
                if filename not in _.paths:  # detected file not present (or untracked) in other branch  # line 262
                    namehash = hashStr(filename)  # line 263
                    changes.additions[filename] = PathInfo(namehash, size, mtime, hashFile(filepath, _.compress, saveTo=os.path.join(_.root, metaFolder, "b%d" % branch, "r%d" % revision, namehash) if write else None) if size > 0 else None)  # line 264
                    continue  # line 265
                last = _.paths[filename]  # filename is known  # line 266
                if last.size is None:  # was removed before but is now added back - does not apply for tracking mode (which never marks files for removal in the history)  # line 267
                    changes.additions[filename] = PathInfo(last.namehash, size, mtime, hashFile(filepath, _.compress, saveTo=os.path.join(_.root, metaFolder, "b%d" % branch, "r%d" % revision, last.namehash) if write else None) if size > 0 else None)  # line 268
                    continue  # line 268
                elif size != last.size or mtime != last.mtime or (checkContent and hashFile(filepath, _.compress) == last.hash):  # detected a modification  # line 269
                    changes.modifications[filename] = PathInfo(last.namehash, last.size if inverse else size, last.mtime if inverse else mtime, last.hash if inverse else hashFile(filepath, _.compress, saveTo=os.path.join(_.root, metaFolder, "b%d" % branch, "r%d" % revision, last.namehash) if write else None) if (last.size if inverse else size) > 0 else None)  # line 270
# Detect deletions. Files no longer being tracked should not be found here
            for folderPath in (p for p, pinfo in _.paths.items() if p[:p.rindex(SLASH)] == relpath and pinfo.size is not None):  # only versioned (and tracked) files that match currently visited folder. TODO don't check for removal just added entries  # line 272
                if folderPath[len(relpath) + 1:] not in filenames:  # filename no longer in file tree TODO use basename and dirname instead of slicing?  # line 273
                    changes.deletions[folderPath] = _.paths[folderPath]  # filename no longer in file tree TODO use basename and dirname instead of slicing?  # line 273
        if progress:  # force new line  # line 274
            print("Preparation finished." + " " * (termWidth - 21), file=sys.stdout)  # force new line  # line 274
        return changes  # line 275

    def integrateChangeset(_, changes: 'ChangeSet', clear=False) -> 'None':  # line 277
        ''' In-memory update from a changeset, marking deleted files with size=None. Use clear = True to start on an empty path set. '''  # line 278
        if clear:  # line 279
            _.paths.clear()  # line 279
        else:  # line 280
            rm = [p for p, info in _.paths.items() if info.size is None]  # remove files deleted in earlier change sets (revisions)  # line 281
            for old in rm:  # remove previously removed entries completely  # line 282
                del _.paths[old]  # remove previously removed entries completely  # line 282
        for d, info in changes.deletions.items():  # mark now removed entries as deleted  # line 283
            _.paths[d] = PathInfo(info.namehash, None, info.mtime, None)  # mark now removed entries as deleted  # line 283
        _.paths.update(changes.additions)  # line 284
        _.paths.update(changes.modifications)  # line 285

    def computeSequentialPathSet(_, branch: 'int', revision: 'int') -> 'None':  # line 287
        next(_.computeSequentialPathSetIterator(branch, revision, incrementally=False))  # simply invoke the generator once  # line 288

    def computeSequentialPathSetIterator(_, branch: 'int', revision: 'int', incrementally: 'bool'=True) -> 'Optional[Iterator[ChangeSet]]':  # line 290
        ''' In-memory computation of current list of valid PathInfo entries for specified branch and until specified revision (inclusively) by traversing revision on the file system. '''  # line 291
        _.loadCommit(branch, 0)  # load initial paths  # line 292
        if incrementally:  # line 293
            yield diffPathSets({}, _.paths)  # line 293
        n = Metadata(_.root)  # type: Metadata  # next changes  # line 294
        for revision in range(1, revision + 1):  # line 295
            n.loadCommit(branch, revision)  # line 296
            changes = diffPathSets(_.paths, n.paths)  # type: ChangeSet  # line 297
            _.integrateChangeset(changes)  # line 298
            if incrementally:  # line 299
                yield changes  # line 299
        yield None  # for the default case - not incrementally  # line 300

    def parseRevisionString(_, argument: 'str') -> 'Tuple[_coconut.typing.Optional[int], _coconut.typing.Optional[int]]':  # line 302
        ''' Commit identifiers can be str or int for branch, and int for revision.
        Revision identifiers can be negative, with -1 being last commit.
    '''  # line 305
        if argument is None:  # no branch/revision specified  # line 306
            return (_.branch, -1)  # no branch/revision specified  # line 306
        argument = argument.strip()  # line 307
        if argument.startswith(SLASH):  # current branch  # line 308
            return (_.branch, int(argument[1:]))  # current branch  # line 308
        if argument.endswith(SLASH):  # line 309
            try:  # line 310
                return (_.getBranchByName(argument[:-1]), -1)  # line 310
            except ValueError:  # line 311
                Exit("Unknown branch label")  # line 311
        if SLASH in argument:  # line 312
            b, r = argument.split(SLASH)[:2]  # line 313
            try:  # line 314
                return (_.getBranchByName(b), int(r))  # line 314
            except ValueError:  # line 315
                Exit("Unknown branch label or wrong number format")  # line 315
        branch = _.getBranchByName(argument)  # type: int  # returns number if given (revision) integer  # line 316
        if branch not in _.branches:  # line 317
            branch = None  # line 317
        try:  # either branch name/number or reverse/absolute revision number  # line 318
            return (_.branch if branch is None else branch, int(argument) if branch is None else -1)  # either branch name/number or reverse/absolute revision number  # line 318
        except:  # line 319
            Exit("Unknown branch label or wrong number format")  # line 319
        return (None, None)  # should never be reached TODO raise exception instead?  # line 320

    def findRevision(_, branch: 'int', revision: 'int', namehash: 'str') -> 'Tuple[int, str]':  # line 322
        while True:  # find latest revision that contained the file physically  # line 323
            source = os.path.join(_.root, metaFolder, "b%d" % branch, "r%d" % revision, namehash)  # type: str  # line 324
            if os.path.exists(source) and os.path.isfile(source):  # line 325
                break  # line 325
            revision -= 1  # line 326
            if revision < 0:  # line 327
                Exit("Cannot determine versioned file '%s' from specified branch '%d'" % (namehash, branch))  # line 327
        return revision, source  # line 328

    def copyVersionedFile(_, branch: 'int', revision: 'int', tobranch: 'int', torevision: 'int', pinfo: 'PathInfo') -> 'None':  # line 330
        ''' Copy versioned file to other branch/revision. '''  # line 331
        target = os.path.join(_.root, metaFolder, "b%d" % tobranch, "r%d" % torevision, pinfo.namehash)  # type: str  # line 332
        revision, source = _.findRevision(branch, revision, pinfo.namehash)  # line 333
        shutil.copy2(source, target)  # line 334

    def readOrCopyVersionedFile(_, branch: 'int', revision: 'int', namehash: 'str', toFile: '_coconut.typing.Optional[str]'=None) -> '_coconut.typing.Optional[bytes]':  # line 336
        ''' Return file contents, or copy contents into file path provided. '''  # line 337
        source = os.path.join(_.root, metaFolder, "b%d" % branch, "r%d" % revision, namehash)  # type: str  # line 338
        try:  # line 339
            with openIt(source, "r", _.compress) as fd:  # line 340
                if toFile is None:  # read bytes into memory and return  # line 341
                    return fd.read()  # read bytes into memory and return  # line 341
                with open(toFile, "wb") as to:  # line 342
                    while True:  # line 343
                        buffer = fd.read(bufSize)  # line 344
                        to.write(buffer)  # line 345
                        if len(buffer) < bufSize:  # line 346
                            break  # line 346
                    return None  # line 347
        except Exception as E:  # line 348
            warn("Cannot read versioned file: %r (%d/%d/%s)" % (E, branch, revision, namehash))  # line 348
        return None  # line 349

    def restoreFile(_, relpath: '_coconut.typing.Optional[str]', branch: 'int', revision: 'int', pinfo: 'PathInfo') -> '_coconut.typing.Optional[bytes]':  # line 351
        ''' Recreate file for given revision, or return contents if path is None. '''  # line 352
        if relpath is None:  # just return contents  # line 353
            return _.readOrCopyVersionedFile(branch, _.findRevision(branch, revision, pinfo.namehash)[0], pinfo.namehash) if pinfo.size > 0 else b''  # just return contents  # line 353
        target = os.path.join(_.root, relpath.replace(SLASH, os.sep))  # type: str  # line 354
        if pinfo.size == 0:  # line 355
            with open(target, "wb"):  # line 356
                pass  # line 356
            try:  # update access/modification timestamps on file system  # line 357
                os.utime(target, (-1, pinfo.mtime / 1000.))  # update access/modification timestamps on file system  # line 357
            except Exception as E:  # line 358
                error("Cannot update file's timestamp after restoration '%r'" % E)  # line 358
            return None  # line 359
        revision, source = _.findRevision(branch, revision, pinfo.namehash)  # line 360
# Restore file by copying buffer-wise
        with openIt(source, "r", _.compress) as fd, open(target, "wb") as to:  # using Coconut's Enhanced Parenthetical Continuation  # line 362
            while True:  # line 363
                buffer = fd.read(bufSize)  # line 364
                to.write(buffer)  # line 365
                if len(buffer) < bufSize:  # line 366
                    break  # line 366
        try:  # update access/modification timestamps on file system  # line 367
            os.utime(target, (-1, pinfo.mtime / 1000.))  # update access/modification timestamps on file system  # line 367
        except Exception as E:  # line 368
            error("Cannot update file's timestamp after restoration '%r'" % E)  # line 368
        return None  # line 369

    def getTrackingPatterns(_, branch: '_coconut.typing.Optional[int]'=None) -> 'FrozenSet[str]':  # line 371
        ''' Returns list of tracking patterns for provided branch or current branch. '''  # line 372
        return _coconut.frozenset() if not _.track and not _.picky else frozenset(_.branches[_.branch if branch is None else branch].tracked)  # line 373


# Main client operations
def offline(argument: '_coconut.typing.Optional[str]'=None, options: '_coconut.typing.Sequence[str]'=[]) -> 'None':  # line 377
    ''' Initial command to start working offline. '''  # line 378
    if '--force' not in options and os.path.exists(metaFolder):  # line 379
        Exit("Repository folder is either already offline or older branches and commits were left over. Use 'sos online' or continue working offline")  # line 380
    m = Metadata(os.getcwd())  # type: Metadata  # line 381
    if '--picky' in options or m.c.picky:  # Git-like  # line 382
        m.picky = True  # Git-like  # line 382
    elif '--track' in options or m.c.track:  # Svn-like  # line 383
        m.track = True  # Svn-like  # line 383
    if '--strict' in options or m.c.strict:  # always hash contents  # line 384
        m.strict = True  # always hash contents  # line 384
    debug("Preparing offline repository...")  # line 385
    m.createBranch(0, str(defaults["defaultbranch"]) if argument is None else argument, initialMessage="Offline repository created on %s" % strftime())  # main branch's name may be None (e.g. for fossil)  # line 386
    m.branch = 0  # line 387
    m.saveBranches()  # no change immediately after going offline, going back online won't issue a warning  # line 388
    info("Offline repository prepared. Use 'sos online' to finish offline work")  # line 389

def online(options: '_coconut.typing.Sequence[str]'=[]) -> 'None':  # line 391
    ''' Finish working offline. '''  # line 392
    force = '--force' in options  # type: bool  # line 393
    m = Metadata(os.getcwd())  # line 394
    m.loadBranches()  # line 395
    if any([not b.insync for b in m.branches.values()]) and not force:  # line 396
        Exit("There are still unsynchronized (dirty) branches.\nUse 'sos log' to list them.\nUse 'sos commit' and 'sos switch' to commit dirty branches to your VCS before leaving offline mode.\nUse 'sos online --force' to erase all aggregated offline revisions.")  # line 396
    strict = '--strict' in options or m.strict  # type: bool  # line 397
    if options.count("--force") < 2:  # line 398
        changes = m.findChanges(checkContent=strict, considerOnly=None if not m.track else m.getTrackingPatterns())  # type: ChangeSet  # line 399
        if modified(changes):  # line 400
            Exit("File tree is modified vs. current branch.\nUse 'sos online --force --force' to continue with removing the offline repository.")  # line 400
    try:  # line 401
        shutil.rmtree(metaFolder)  # line 401
        info("Exited offline mode. Continue working with your traditional VCS.")  # line 401
    except Exception as E:  # line 402
        Exit("Error removing offline repository: %r" % E)  # line 402

def branch(argument: '_coconut.typing.Optional[str]'=None, options: '_coconut.typing.Sequence[str]'=[]) -> 'None':  # line 404
    ''' Create a new branch (from file tree or last revision) and (by default) continue working on it. '''  # line 405
    last = '--last' in options  # type: bool  # use last revision for branching, not current file tree  # line 406
    stay = '--stay' in options  # type: bool  # continue on current branch after branching  # line 407
    force = '--force' in options  # type: bool  # branch even with local modifications  # line 408
    m = Metadata(os.getcwd())  # type: Metadata  # line 409
    m.loadBranches()  # line 410
    if argument and m.getBranchByName(argument) is not None:  # create a named branch  # line 411
        Exit("Branch '%s' already exists. Cannot proceed" % argument)  # create a named branch  # line 411
    branch = max(m.branches.keys()) + 1  # next branch's key - this isn't atomic but we assume single-user non-concurrent use here  # line 412
    debug("Branching to %sbranch b%d%s%s..." % ("unnamed " if argument is None else "", branch, " '%s'" % argument if argument else "", " from last revision" if last else ""))  # line 413
    if last:  # line 414
        m.duplicateBranch(branch, argument)  # branch from branch's last revision  # line 415
    else:  # from file tree state  # line 416
        m.createBranch(branch, argument)  # branch from current file tree  # line 417
    if not stay:  # line 418
        m.branch = branch  # line 419
        m.saveBranches()  # line 420
    info("%s new %sbranch b%d%s" % ("Continue work after branching" if stay else "Switched to", "unnamed " if argument is None else "", branch, " '%s'" % argument if argument else ""))  # line 421

def changes(argument: 'str'=None, options: '_coconut.typing.Sequence[str]'=[]) -> 'ChangeSet':  # line 423
    ''' Show changes of file tree vs. (last or specified) revision on current or specified branch. '''  # line 424
    m = Metadata(os.getcwd())  # type: Metadata  # line 425
    branch = None  # type: _coconut.typing.Optional[int]  # line 425
    revision = None  # type: _coconut.typing.Optional[int]  # line 425
    m.loadBranches()  # knows current branch  # line 426
    strict = '--strict' in options or m.strict  # type: bool  # line 427
    branch, revision = m.parseRevisionString(argument)  # line 428
    if branch not in m.branches:  # line 429
        Exit("Unknown branch")  # line 429
    m.loadBranch(branch)  # knows commits  # line 430
    revision = revision if revision >= 0 else len(m.commits) + revision  # negative indexing  # line 431
    if revision < 0 or revision > max(m.commits):  # line 432
        Exit("Unknown revision r%d" % revision)  # line 432
    info("/// Changes of file tree vs. revision '%s/r%d'" % ((lambda _coconut_none_coalesce_item: "b%d" % branch if _coconut_none_coalesce_item is None else _coconut_none_coalesce_item)(m.branches[branch].name), revision))  # line 433
    m.computeSequentialPathSet(branch, revision)  # load all commits up to specified revision  # line 434
    changes = m.findChanges(checkContent=strict, considerOnly=None if not m.track else m.getTrackingPatterns() | m.getTrackingPatterns(branch))  # type: ChangeSet  # line 435
    m.listChanges(changes)  # line 436
    return changes  # line 437

def diff(argument: 'str', options: '_coconut.typing.Sequence[str]'=[]) -> 'None':  # line 439
    ''' Show text file differences of file tree vs. (last or specified) revision on current or specified branch. '''  # line 440
    m = Metadata(os.getcwd())  # type: Metadata  # line 441
    branch = None  # type: _coconut.typing.Optional[int]  # line 441
    revision = None  # type: _coconut.typing.Optional[int]  # line 441
    m.loadBranches()  # knows current branch  # line 442
    strict = '--strict' in options or m.strict  # type: bool  # line 443
    branch, revision = m.parseRevisionString(argument)  # line 444
    if branch not in m.branches:  # line 445
        Exit("Unknown branch")  # line 445
    m.loadBranch(branch)  # knows commits  # line 446
    revision = revision if revision >= 0 else len(m.commits) + revision  # negative indexing  # line 447
    if revision < 0 or revision > max(m.commits):  # line 448
        Exit("Unknown revision r%d" % revision)  # line 448
    info("/// Differences of file tree vs. revision '%s/r%d'" % ((lambda _coconut_none_coalesce_item: "b%d" % branch if _coconut_none_coalesce_item is None else _coconut_none_coalesce_item)(m.branches[branch].name), revision))  # line 449
    m.computeSequentialPathSet(branch, revision)  # load all commits up to specified revision  # line 450
    changes = m.findChanges(checkContent=strict, inverse=True, considerOnly=None if not m.track else m.getTrackingPatterns() | m.getTrackingPatterns(branch))  # type: ChangeSet  # line 451
    onlyBinaryModifications = dataCopy(ChangeSet, changes, modifications={k: v for k, v in changes.modifications.items() if not m.isTextType(k)})  # type: ChangeSet  # line 452
    if modified(onlyBinaryModifications):  # line 453
        debug("/// File changes")  # line 453
    m.listChanges(onlyBinaryModifications)  # only list modified binary files  # line 454

    if changes.modifications:  # TODO only text files, not binary  # line 456
        debug("%s/// Textual modifications" % ("\n" if modified(onlyBinaryModifications) else ""))  # TODO only text files, not binary  # line 456
    for path, pinfo in changes.modifications.items():  # only consider modified files TODO also show A/D here? or replace listing above?  # line 457
        content = None  # type: _coconut.typing.Optional[bytes]  # ; othr:str[]; curr:str[]  # line 458
        if pinfo.size == 0:  # empty file contents  # line 459
            content = b""  # empty file contents  # line 459
        else:  # versioned file  # line 460
            content = m.restoreFile(None, branch, revision, pinfo)  # versioned file  # line 460
            assert content is not None  # versioned file  # line 460
        abspath = os.path.join(m.root, path.replace(SLASH, os.sep))  # current file  # line 461
        blocks = merge(file=content, intoname=abspath, diffOnly=True)  # type: List[MergeBlock]  # only determine change blocks  # line 462
        print("DIF %s%s" % (path, " <timestamp only>" if len(blocks) == 1 and blocks[0].tipe == MergeBlockType.KEEP else ""))  # line 463
        for block in blocks:  # line 464
            if block.tipe in [MergeBlockType.INSERT, MergeBlockType.REMOVE]:  # line 465
                pass  # TODO print some previous and following lines - which aren't accessible here anymore  # line 466
            if block.tipe == MergeBlockType.INSERT:  # TODO show color via curses?  # line 467
                for no, line in enumerate(block.lines):  # line 468
                    print("+++ %04d |%s|" % (no + block.line, line))  # line 469
            elif block.tipe == MergeBlockType.REMOVE:  # line 470
                for no, line in enumerate(block.lines):  # line 471
                    print("--- %04d |%s|" % (no + block.line, line))  # line 472
            elif block.tipe in [MergeBlockType.REPLACE, MergeBlockType.MODIFY]:  # TODO for MODIFY also show intra-line change ranges  # line 473
                for no, line in enumerate(block.replaces.lines):  # line 474
                    print("- | %04d |%s|" % (no + block.replaces.line, line))  # line 475
                for no, line in enumerate(block.lines):  # line 476
                    print("+ | %04d |%s|" % (no + block.line, line))  # line 477
#      elif block.tipe == MergeBlockType.KEEP: pass
#      elif block.tipe == MergeBlockType.MODIFY:  # intra-line modifications
#      elif block.tipe == MergeBlockType.MOVE:  # intra-line modifications

def commit(argument: '_coconut.typing.Optional[str]'=None, options: '_coconut.typing.Sequence[str]'=[]) -> 'None':  # line 482
    ''' Create new revision from file tree changes vs. last commit. '''  # line 483
    changes = None  # type: ChangeSet  # line 484
    m, branch, revision, changes, strict, force, trackingPatterns = exitOnChanges(None, options, commit=True)  # special flag creates new revision for detected changes, but abort if no changes  # line 485
    info((lambda _coconut_none_coalesce_item: "b%d" % m.branch if _coconut_none_coalesce_item is None else _coconut_none_coalesce_item)("Committing changes to branch '%s'..." % m.branches[m.branch].name))  # line 486
    m.integrateChangeset(changes, clear=True)  # update pathset to changeset only  # line 487
    m.saveCommit(m.branch, revision)  # revision has already been incremented  # line 488
    m.commits[revision] = CommitInfo(revision, int(time.time() * 1000), argument)  # comment can be None  # line 489
    m.saveBranch(m.branch)  # line 490
    if m.picky or m.track:  # TODO is it necessary to load again  # line 491
        m.loadBranches()  # TODO is it necessary to load again  # line 491
    if m.picky:  # HINT was changed from only picky to include track as well  # line 492
        m.branches[m.branch] = dataCopy(BranchInfo, m.branches[m.branch], tracked=[], insync=False)  # remove tracked patterns  # line 493
    elif m.track:  # line 494
        m.branches[m.branch] = dataCopy(BranchInfo, m.branches[m.branch], insync=False)  # set branch dirty  # line 495
    if m.picky or m.track:  # line 496
        m.saveBranches()  # line 496
    info("Created new revision r%02d%s (+%02d/-%02d/*%02d)" % (revision, ((" '%s'" % argument) if argument is not None else ""), len(changes.additions), len(changes.deletions), len(changes.modifications)))  # line 497

def status() -> 'None':  # line 499
    ''' Show branches and current repository state. '''  # line 500
    m = Metadata(os.getcwd())  # type: Metadata  # line 501
    m.loadBranches()  # knows current branch  # line 502
    current = m.branch  # type: int  # line 503
    info("/// Offline repository status")  # line 504
    sl = max([len((lambda _coconut_none_coalesce_item: "" if _coconut_none_coalesce_item is None else _coconut_none_coalesce_item)(b.name)) for b in m.branches.values()])  # type: int  # line 505
    for branch in sorted(m.branches.values(), key=lambda b: b.number):  # line 506
        m.loadBranch(branch.number)  # knows commit history  # line 507
        print("  %s b%d%s @%s (%s) with %d commits%s" % ("*" if current == branch.number else " ", branch.number, ((" %%%ds" % (sl + 2)) % ("'%s'" % branch.name)) if branch.name else "", strftime(branch.ctime), "in sync" if branch.insync else "dirty", len(m.commits), ". Last comment: '%s'" % m.commits[max(m.commits)].message if m.commits[max(m.commits)].message else ""))  # line 508
    if m.track or m.picky and len(m.branches[m.branch].tracked) > 0:  # line 509
        info("\nTracked file patterns:")  # line 510
        print(ajoin("  | ", m.branches[m.branch].tracked, "\n"))  # line 511

def exitOnChanges(argument: '_coconut.typing.Optional[str]'=None, options: '_coconut.typing.Sequence[str]'=[], check: 'bool'=True, commit: 'bool'=False) -> 'Tuple[Metadata, _coconut.typing.Optional[int], int, ChangeSet, bool, bool, FrozenSet[str]]':  # line 513
    ''' Common behavior for switch, update, delete, commit.
      check: stop program on detected change
      commit: don't stop on changes, because that's what we need in the operation
      Returns (Metadata, (current or target) branch, revision, set of changes vs. last commit on current branch, strict, force flags. '''  # line 517
    m = Metadata(os.getcwd())  # type: Metadata  # line 518
    m.loadBranches()  # knows current branch  # line 519
    trackingPatterns = m.getTrackingPatterns()  # type: FrozenSet[str]  # SVN-like mode  # line 520
    force = '--force' in options  # type: bool  # line 521
    strict = '--strict' in options or m.strict  # type: bool  # line 522
    if argument is not None:  # line 523
        branch, revision = m.parseRevisionString(argument)  # for early abort  # line 524
        if branch is None:  # line 525
            Exit("Branch '%s' doesn't exist. Cannot proceed" % argument)  # line 525
    m.loadBranch(m.branch)  # knows last commits of *current* branch  # line 526

# Determine current changes
    m.computeSequentialPathSet(m.branch, max(m.commits))  # load all commits up to specified revision  # line 529
    changes = m.findChanges(m.branch if commit else None, max(m.commits) + 1 if commit else None, checkContent=strict, considerOnly=None if not m.track and not m.picky else trackingPatterns)  # type: ChangeSet  # line 530
    if modified(changes) and not force:  # and check?  # line 531
        m.listChanges(changes)  # line 532
        if check and not commit:  # line 533
            Exit("File tree contains changes. Use --force to proceed")  # line 533
    elif commit and not force:  #  and not check  # line 534
        Exit("Nothing to commit. Aborting")  #  and not check  # line 534

    if argument is not None:  # branch/revision specified  # line 536
        m.loadBranch(branch)  # knows commits of target branch  # line 537
        revision = revision if revision >= 0 else len(m.commits) + revision  # negative indexing  # line 538
        if revision < 0 or revision > max(m.commits):  # line 539
            Exit("Unknown revision r%02d" % revision)  # line 539
        return (m, branch, revision, changes, strict, force, m.getTrackingPatterns(branch))  # line 540
    return (m, m.branch, max(m.commits) + (1 if commit else 0), changes, strict, force, trackingPatterns)  # line 541

def switch(argument: 'str', options: '_coconut.typing.Sequence[str]'=[]) -> 'None':  # line 543
    ''' Continue work on another branch, replacing file tree changes. '''  # line 544
    changes = None  # type: ChangeSet  # line 545
    m, branch, revision, changes, strict, force, trackingPatterns = exitOnChanges(argument, options)  # line 546
    info("/// Switching to branch %sb%d/r%d" % ("'%s' " % m.branches[branch].name if m.branches[branch].name else "", branch, revision))  # line 547

# Determine file changes from other branch to current file tree
    if '--meta' in options:  # only switch meta data  # line 550
        m.branches[m.branch] = dataCopy(BranchInfo, m.branches[m.branch], tracked=m.branches[branch].tracked)  # line 551
    else:  # full file switch  # line 552
        m.computeSequentialPathSet(branch, revision)  # load all commits up to specified revision for target branch into memory  # line 553
        changes = m.findChanges(checkContent=strict, inverse=True, considerOnly=None if not m.track else trackingPatterns | m.getTrackingPatterns(branch))  # determine difference of other branch vs. file tree (forced or in sync with current branch; "addition" means exists now and should be removed)  # line 554
        if not modified(changes):  # line 555
            info("No changes to current file tree")  # line 556
        else:  # integration required  # line 557
            for path, pinfo in changes.deletions.items():  # line 558
                m.restoreFile(path, branch, revision, pinfo)  # is deleted in current file tree: restore from branch to reach target  # line 559
                debug("ADD " + path)  # line 560
            for path, pinfo in changes.additions.items():  # line 561
                os.unlink(os.path.join(m.root, path.replace(SLASH, os.sep)))  # is added in current file tree: remove from branch to reach target  # line 562
                debug("DEL " + path)  # line 563
            for path, pinfo in changes.modifications.items():  # line 564
                m.restoreFile(path, branch, revision, pinfo)  # is modified in current file tree: restore from branch to reach target  # line 565
                debug("MOD " + path)  # line 566
    m.branch = branch  # line 567
    m.saveBranches()  # store switched path info  # line 568
    info("Switched to branch %sb%d/r%d" % ("'%s' " % (m.branches[branch].name if m.branches[branch].name else ""), branch, revision))  # line 569

def update(argument: 'str', options: '_coconut.typing.Sequence[str]'=[]) -> 'None':  # line 571
    ''' Load and integrate a specified other branch/revision into current life file tree.
      In tracking mode, this also updates the set of tracked patterns.
      User options for merge operation: --add (don't remove), --rm (don't insert), --add-lines/--rm-lines (inside each file)
      User options for conflict resolution: --theirs/--mine/--ask
  '''  # line 576
    mrg = firstOfMap({"--add": MergeOperation.INSERT, "--rm": MergeOperation.REMOVE}, options, MergeOperation.BOTH)  # type: int  # default operation is replicate remove state for non-conflicting cases (insertions/deletions)  # line 577
    res = firstOfMap({'--theirs': ConflictResolution.THEIRS, '--mine': ConflictResolution.MINE}, options, ConflictResolution.NEXT)  # type: int  # NEXT means deeper level  # line 578
    mrgline = firstOfMap({'--add-lines': MergeOperation.INSERT, '--rm-lines': MergeOperation.REMOVE}, options, mrg)  # type: int  # default operation for modified files is same as for files  # line 579
    resline = firstOfMap({'--theirs-lines': ConflictResolution.THEIRS, '--mine-lines': ConflictResolution.MINE}, options, ConflictResolution.ASK)  # type: int  # line 580
    m = Metadata(os.getcwd())  # type: Metadata  # TODO same is called inside stop on changes - could return both current and designated branch instead  # line 581
    m.loadBranches()  # line 582
    changes = None  # type: ChangeSet  # line 582
    currentBranch = m.branch  # type: _coconut.typing.Optional[int]  # line 583
    m, branch, revision, changes, strict, force, trackingPatterns = exitOnChanges(argument, options, check=False)  # don't check for current changes, only parse arguments  # line 584
    debug("Integrating changes from '%s/r%d' into file tree..." % ((lambda _coconut_none_coalesce_item: "b%d" % branch if _coconut_none_coalesce_item is None else _coconut_none_coalesce_item)(m.branches[branch].name), revision))  # line 585

# Determine file changes from other branch over current file tree
    m.computeSequentialPathSet(branch, revision)  # load all commits up to specified revision for branch to integrate  # line 588
    trackingUnion = trackingPatterns | m.getTrackingPatterns(branch)  # type: FrozenSet[str]  # line 589
    changes = m.findChanges(checkContent=strict, inverse=True, considerOnly=None if not m.track else trackingUnion)  # determine difference of other branch vs. file tree. "addition" means exists now but not in other, and should be removed unless in tracking mode  # line 590
    if not (mrg & MergeOperation.INSERT and changes.additions or (mrg & MergeOperation.REMOVE and changes.deletions) or changes.modifications):  # line 591
        if trackingUnion == trackingPatterns:  # nothing added  # line 592
            info("No file changes detected, but tracking patterns were merged (run 'sos switch /-1 --meta' to undo)")  # TODO write test to see if this works  # line 593
        else:  # line 594
            info("Nothing to update")  # but write back updated branch info below  # line 595
    else:  # integration required  # line 596
        for path, pinfo in changes.deletions.items():  # deletions mark files not present in current file tree -> needs additon  # line 597
            if mrg & MergeOperation.INSERT:  # deleted in current file tree: restore from branch to reach target  # line 598
                m.restoreFile(path, branch, revision, pinfo)  # deleted in current file tree: restore from branch to reach target  # line 598
            print("ADD " + path if mrg & MergeOperation.INSERT else "(A) " + path)  # line 599
        for path, pinfo in changes.additions.items():  # line 600
            if m.track or m.picky:  # because untracked files of other branch cannot be detected (which is good)  # line 601
                Exit("This should never happen")  # because untracked files of other branch cannot be detected (which is good)  # line 601
            if mrg & MergeOperation.REMOVE:  # line 602
                os.unlink(m.root + os.sep + path.replace(SLASH, os.sep))  # line 602
            print("DEL " if mrg & MergeOperation.REMOVE else "(D) " + path)  # not contained in other branch, but maybe kept  # line 603
        for path, pinfo in changes.modifications.items():  # line 604
            into = os.path.join(m.root, path.replace(SLASH, os.sep))  # type: str  # line 605
            binary = not m.isTextType(path)  # line 606
            if res & ConflictResolution.ASK or (binary and res == ConflictResolution.NEXT):  # TODO this may ask user even if no interaction was asked for (check line level for interactivity fist)  # line 607
                print(("MOD " if not binary else "BIN ") + path)  # line 608
                reso = {"i": ConflictResolution.MINE, "t": ConflictResolution.THEIRS, "m": ConflictResolution.NEXT}.get(user_input(" Resolve: *M[I]ne, [T]heirs, [M]erge: (I)").strip().lower(), ConflictResolution.MINE)  # line 609
                debug("User selected %d" % reso)  # line 610
            else:  # line 611
                reso = res  # line 611
            if reso & ConflictResolution.THEIRS:  # line 612
                m.readOrCopyVersionedFile(branch, revision, pinfo.namehash, toFile=into)  # blockwise copy of contents  # line 613
                print("THR " + path)  # line 614
            elif reso & ConflictResolution.MINE:  # line 615
                print("MNE " + path)  # nothing to do! same as skip  # line 616
            else:  # NEXT: line-based merge  # line 617
                file = m.readOrCopyVersionedFile(branch, revision, pinfo.namehash) if pinfo.size > 0 else b''  # type: _coconut.typing.Optional[bytes]  # parse lines TODO decode etc.  # line 618
                if file is not None:  # if None, error message was already logged  # line 619
                    contents = merge(file=file, intoname=into, mergeOperation=mrgline, conflictResolution=resline)  # type: bytes  # line 620
                    with open(path, "wb") as fd:  # TODO write to temp file first  # line 621
                        fd.write(contents)  # TODO write to temp file first  # line 621
    info("Integrated changes from '%s/r%d' into file tree" % ((lambda _coconut_none_coalesce_item: "b%d" % branch if _coconut_none_coalesce_item is None else _coconut_none_coalesce_item)(m.branches[branch].name), revision))  # line 622
    m.branches[currentBranch] = dataCopy(BranchInfo, m.branches[currentBranch], insync=False, tracked=list(trackingUnion))  # TODO really? it's a change that cannot be undone easily by the user  # line 623
    m.branch = currentBranch  # need to restore setting before saving TODO operate on different objects instead  # line 624
    m.saveBranches()  # line 625

def delete(argument: 'str', options: '_coconut.typing.Sequence[str]'=[]) -> 'None':  # line 627
    ''' Remove a branch entirely. '''  # line 628
    m, branch, revision, changes, strict, force, trackingPatterns = exitOnChanges(None, options)  # line 629
    if len(m.branches) == 1:  # line 630
        Exit("Cannot remove the only remaining branch. Use 'sos online' to leave offline mode")  # line 630
    branch, revision = m.parseRevisionString(argument)  # not from exitOnChanges, because we have to set argument to None there  # line 631
    if branch is None or branch not in m.branches:  # line 632
        Exit("Unknown branch")  # line 632
    debug("Removing branch %d%s..." % (branch, " '%s'" % m.branches[branch].name if m.branches[branch].name else ""))  # line 633
    binfo = m.removeBranch(branch)  # need to keep a reference to removed entry for output below  # line 634
    info("Branch b%d%s removed" % (branch, " '%s'" % binfo.name if binfo.name else ""))  # line 635

def add(folder: 'str', argument: 'str', options: '_coconut.typing.Sequence[str]'=[]) -> 'None':  # line 637
    ''' Add a tracked files pattern to current branch's tracked files. '''  # line 638
    force = '--force' in options  # type: bool  # line 639
    m = Metadata(os.getcwd())  # type: Metadata  # line 640
    m.loadBranches()  # line 641
    if not m.track and not m.picky:  # line 642
        Exit("Repository is in simple mode. Needs 'offline --track' or 'offline --picky' instead")  # line 642
    relpath = os.path.relpath(os.path.dirname(os.path.abspath(os.path.join(folder, argument))), m.root)  # for tracking list  # line 643
    pattern = os.path.join(relpath, os.path.basename(argument)).replace(os.sep, SLASH)  # line 644
    if pattern in m.branches[m.branch].tracked:  # line 645
        Exit("Pattern '%s' already tracked")  # line 646
    if not force and len(fnmatch.filter(os.listdir(os.path.abspath(relpath)), os.path.basename(pattern.replace(SLASH, os.sep)))) == 0:  # doesn't match any current file  # line 647
        Exit("Pattern doesn't match any file in specified folder. Use --force to add it anyway")  # line 648
    m.branches[m.branch].tracked.append(pattern)  # TODO set insync flag to False? same for rm  # line 649
    m.saveBranches()  # line 650
    info("Added tracking pattern '%s' for folder '%s'" % (os.path.basename(pattern.replace(SLASH, os.sep)), os.path.abspath(relpath)))  # line 651

def rm(folder: 'str', argument: 'str') -> 'None':  # line 653
    ''' Remove a tracked files pattern from current branch's tracked files. '''  # line 654
    m = Metadata(os.getcwd())  # type: Metadata  # line 655
    m.loadBranches()  # line 656
    if not m.track and not m.picky:  # line 657
        Exit("Repository is in simple mode. Needs 'offline --track' or 'offline --picky' instead")  # line 657
    relpath = os.path.relpath(os.path.dirname(os.path.abspath(os.path.join(folder, argument))), m.root)  # type: str  # line 658
    pattern = os.path.join(relpath, os.path.basename(argument)).replace(os.sep, SLASH)  # type: str  # line 659
    if pattern not in m.branches[m.branch].tracked:  # line 660
        suggestion = _coconut.set()  # type: Set[str]  # line 661
        for pat in m.branches[m.branch].tracked:  # line 662
            if fnmatch.fnmatch(pattern, pat):  # line 663
                suggestion.add(pat)  # line 663
        if suggestion:  # line 664
            print("Do you mean any of the following tracked globs? '%s'" % (", ".join(sorted(suggestion))))  # line 664
        Exit("Tracked pattern '%s' not found" % pattern)  # line 665
    m.branches[m.branch].tracked.remove(pattern)  # line 666
    m.saveBranches()  # line 667
    info("Removed tracking pattern '%s' for folder '%s'" % (os.path.basename(pattern.replace(SLASH, os.sep)), os.path.abspath(relpath)))  # line 668

def ls(argument: '_coconut.typing.Optional[str]'=None) -> 'None':  # line 670
    ''' List specified directory, augmenting with repository metadata. '''  # line 671
    cwd = os.getcwd() if argument is None else argument  # type: str  # line 672
    m = Metadata(cwd)  # type: Metadata  # line 673
    m.loadBranches()  # line 674
    relpath = os.path.relpath(cwd, m.root).replace(os.sep, SLASH)  # type: str  # line 675
    files = list(sorted((entry for entry in os.listdir(cwd) if os.path.isfile(entry))))  # type: List[str]  # line 676
    trackingPatterns = m.getTrackingPatterns() if m.track or m.picky else _coconut.frozenset()  # type: FrozenSet[str]  # for current branch  # line 677
    for file in files:  # line 678
        ignore = None  # type: _coconut.typing.Optional[str]  # line 679
        for ig in m.c.ignores:  # line 680
            if fnmatch.fnmatch(file, ig):  # remember first match TODO document this  # line 681
                ignore = ig  # remember first match TODO document this  # line 681
                break  # remember first match TODO document this  # line 681
        if ig:  # line 682
            for wl in m.c.ignoresWhitelist:  # line 683
                if fnmatch.fnmatch(file, wl):  # found a white list entry for ignored file, undo ignoring it  # line 684
                    ignore = None  # found a white list entry for ignored file, undo ignoring it  # line 684
                    break  # found a white list entry for ignored file, undo ignoring it  # line 684
        if ignore is None:  # line 685
            matches = []  # type: List[str]  # line 686
            for pattern in (p for p in trackingPatterns if os.path.dirname(p) == relpath):  # only patterns matching current folder  # line 687
                if fnmatch.fnmatch(file, os.path.basename(pattern)):  # TODO or only file basename?  # line 688
                    matches.append(pattern)  # TODO or only file basename?  # line 688
        print("%s %s%s" % ("IGN" if ignore is not None else ("TRK" if len(matches) > 0 else "   "), file, ' by "%s"' % ignore if ignore is not None else (" by " + ";".join(['"%s"' % match for match in matches]) if len(matches) > 0 else "")))  # line 689

def log() -> 'None':  # line 691
    ''' List previous commits on current branch. '''  # TODO --verbose for changesets  # line 692
    m = Metadata(os.getcwd())  # type: Metadata  # line 693
    m.loadBranches()  # knows current branch  # line 694
    m.loadBranch(m.branch)  # knows commit history  # line 695
    info((lambda _coconut_none_coalesce_item: "r%02d" % m.branch if _coconut_none_coalesce_item is None else _coconut_none_coalesce_item)("/// Offline commit history of branch '%s'" % m.branches[m.branch].name))  # TODO also retain "from branch/revision" on branching?  # line 696
    nl = len("%d" % max(m.commits))  # determine space needed for revision  # line 697
    changeset = m.computeSequentialPathSetIterator(m.branch, max(m.commits))  # line 698
    for no in range(max(m.commits) + 1):  # line 699
        commit = m.commits[no]  # type: CommitInfo  # line 700
        changes = next(changeset)  # type: ChangeSet  # side-effect: updates m.paths  # line 701
        print("  %s r%s @%s (+%02d/-%02d/*%02d): %s" % ("*" if commit.number == max(m.commits) else " ", ("%%%ds" % nl) % commit.number, strftime(commit.ctime), len(changes.additions), len(changes.deletions), len(changes.modifications), (lambda _coconut_none_coalesce_item: "" if _coconut_none_coalesce_item is None else _coconut_none_coalesce_item)(commit.message)))  # line 702
# TODO list number of files and if binary/text

def config(argument: 'str', options: 'List[str]'=[]) -> 'None':  # line 705
    if argument not in ["set", "unset", "show", "list", "add", "rm"]:  # line 706
        Exit("Unknown config command")  # line 706
    if not configr:  # line 707
        Exit("Cannot execute config command. 'configr' module not installed")  # line 707
    c = loadConfig()  # type: Union[configr.Configr, Accessor]  # line 708
    if argument == "set":  # line 709
        if len(options) < 2:  # line 710
            Exit("No key nor value specified")  # line 710
        if options[0] not in (["defaultbranch"] + CONFIGURABLE_FLAGS + CONFIGURABLE_LISTS):  # line 711
            Exit("Unsupported key %r" % options[0])  # line 711
        c[options[0]] = options[1].lower() in TRUTH_VALUES if options[0] in CONFIGURABLE_FLAGS else (options[1].strip() if options[0] not in CONFIGURABLE_LISTS else safeSplit(options[1], ";"))  # TODO sanitize texts?  # line 712
    elif argument == "unset":  # line 713
        if len(options) < 1:  # line 714
            Exit("No key specified")  # line 714
        if options[0] not in c.keys():  # line 715
            Exit("Unknown key")  # line 715
        del c[options[0]]  # line 716
    elif argument == "add":  # line 717
        if len(options) < 2:  # line 718
            Exit("No key nor value specified")  # line 718
        if options[0] not in CONFIGURABLE_LISTS:  # line 719
            Exit("Unsupported key for add %r" % options[0])  # line 719
        if options[0] not in c.keys():  # add list  # line 720
            c[options[0]] = [options[1]]  # add list  # line 720
        elif options[1] in c[options[0]]:  # line 721
            Exit("Value already contained")  # line 721
        c[options[0]].append(options[1])  # line 722
    elif argument == "rm":  # line 723
        if len(options) < 2:  # line 724
            Exit("No key nor value specified")  # line 724
        if options[0] not in c.keys():  # line 725
            Exit("Unknown key specified: %r" % options[0])  # line 725
        if options[1] not in c[options[0]]:  # line 726
            Exit("Unknown value: %r" % options[1])  # line 726
        c[options[0]].remove(options[1])  # line 727
    else:  # Show  # line 728
        for k, v in sorted(c.items()):  # line 729
            print("%s => %r" % (k, v))  # line 729
        return  # line 730
    f, g = saveConfig(c)  # line 731
    if f is None:  # line 732
        error("Error saving user configuration: %r" % g)  # line 732

def parse(root: 'str', inFolder: 'str'):  # line 734
    ''' Main operation. '''  # line 735
    debug("Parsing command-line arguments...")  # line 736
    command = sys.argv[1].strip() if len(sys.argv) > 1 else ""  # line 737
    argument = sys.argv[2].strip() if len(sys.argv) > 2 else None  # line 738
    options = sys.argv[3:] if command == "config" else [c for c in sys.argv[2:] if c.startswith("--")]  # consider second parameter for no-arg command, otherwise from third on  # line 739
    debug("Processing command %r with argument '%s' and options %r." % ("" if command is None else command, "" if argument is None else argument, options))  # line 740
    if command[:1] == "a":  # line 741
        add(inFolder, argument, options)  # line 741
    elif command[:1] == "b":  # line 742
        branch(argument, options)  # line 742
    elif command[:2] == "ch":  # line 743
        changes(argument, options)  # line 743
    elif command[:3] == "com" or command[:2] == "ci":  # line 744
        commit(argument, options)  # line 744
    elif command[:3] == 'con':  # line 745
        config(argument, options)  # line 745
    elif command[:2] == "de":  # line 746
        delete(argument, options)  # line 746
    elif command[:2] == "di":  # line 747
        diff(argument, options)  # line 747
    elif command[:1] == "h":  # line 748
        usage()  # line 748
    elif command[:2] == "lo":  # line 749
        log()  # line 749
    elif command[:2] in ["li", "ls"]:  # line 750
        ls(argument)  # line 750
    elif command[:2] == "of":  # line 751
        offline(argument, options)  # line 751
    elif command[:2] == "on":  # line 752
        online(options)  # line 752
    elif command[:1] == "r":  # line 753
        rm(inFolder, argument)  # line 753
    elif command[:2] == "st":  # line 754
        status()  # line 754
    elif command[:2] == "sw":  # line 755
        switch(argument, options)  # line 755
    elif command[:2] == "u":  # line 756
        update(argument, options)  # line 756
    else:  # line 757
        Exit("Unknown command '%s'" % command)  # line 757
    sys.exit(0)  # line 758

def main() -> 'None':  # line 760
    global debug, info, warn, error  # line 761
    logging.basicConfig(level=level, stream=sys.stderr, format=("%(asctime)-23s %(levelname)-8s %(name)s:%(lineno)d | %(message)s" if '--log' in sys.argv else "%(message)s"))  # line 762
    _log = Logger(logging.getLogger(__name__))  # line 763
    debug, info, warn, error = _log.debug, _log.info, _log.warn, _log.error  # line 763
    for option in (o for o in ['--log', '--verbose', '-v', '--sos'] if o in sys.argv):  # clean up program arguments  # line 764
        sys.argv.remove(option)  # clean up program arguments  # line 764
    if '--help' in sys.argv or len(sys.argv) < 2:  # line 765
        usage()  # line 765
        Exit()  # line 765
    command = sys.argv[1] if len(sys.argv) > 1 else None  # type: _coconut.typing.Optional[str]  # line 766
    root, vcs, cmd = findSosVcsBase()  # root is None if no .sos folder exists up the folder tree (still working online); vcs is checkout/repo root folder; cmd is the VCS base command  # line 767
    debug("Found root folders for SOS|VCS: %s|%s" % ("" if root is None else root, "" if vcs is None else vcs))  # line 768
    defaults["defaultbranch"] = vcsBranches.get(cmd, "trunk")  # sets dynamic default with SVN fallback  # line 769
    if force_sos or root is not None or ("" if command is None else command)[:2] == "of" or ("" if command is None else command)[:1] == "h":  # in offline mode or just going offline TODO what about git config?  # line 770
        cwd = os.getcwd()  # line 771
        os.chdir(cwd if command[:2] == "of" else cwd if root is None else root)  # line 772
        parse(root, cwd)  # line 773
    elif cmd is not None:  # online mode - delegate to VCS  # line 774
        info("SOS: Running '%s %s'" % (cmd, " ".join(sys.argv[1:])))  # line 775
        import subprocess  # only requuired in this section  # line 776
        process = subprocess.Popen([cmd] + sys.argv[1:], shell=False, stdin=subprocess.PIPE, stdout=sys.stdout, stderr=sys.stderr)  # line 777
        inp = ""  # type: str  # line 778
        while True:  # line 779
            so, se = process.communicate(input=inp)  # line 780
            if process.returncode is not None:  # line 781
                break  # line 781
            inp = sys.stdin.read()  # line 782
        if sys.argv[1][:2] == "co" and process.returncode == 0:  # successful commit - assume now in sync again (but leave meta data folder with potential other feature branches behind until "online")  # line 783
            if root is None:  # line 784
                Exit("Cannot determine VCS root folder: Unable to mark repository as synchronized and will show a warning when leaving offline mode")  # line 784
            m = Metadata(root)  # line 785
            m.loadBranches()  # read repo  # line 786
            m.branches[m.branch] = dataCopy(BranchInfo, m.branches[m.branch], insync=True)  # mark as committed  # line 787
            m.saveBranches()  # line 788
    else:  # line 789
        Exit("No offline repository present, and unable to detect VCS file tree")  # line 789


# Main part
level = logging.DEBUG if os.environ.get("DEBUG", "False").lower() == "true" or '--verbose' in sys.argv or '-v' in sys.argv else logging.INFO  # line 793
force_sos = '--sos' in sys.argv  # line 794
_log = Logger(logging.getLogger(__name__))  # line 795
debug, info, warn, error = _log.debug, _log.info, _log.warn, _log.error  # line 795
if __name__ == '__main__':  # line 796
    main()  # line 796
