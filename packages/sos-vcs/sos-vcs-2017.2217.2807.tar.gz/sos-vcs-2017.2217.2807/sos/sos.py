#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# __coconut_hash__ = 0xe17acc53

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
    from typing import Type  # only required for mypy  # line 4
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
_int = eval("long") if sys.version_info.major < 3 else int  # type: Union[Type]  # for Python 2 compatibility  # line 18


# Constants
APPNAME = "Subversion Offline Solution  V%s  (C) Arne Bachmann" % version.__release_version__  # type: str  # line 22
defaults = Accessor({"strict": False, "track": False, "picky": False, "compress": True, "tags": [], "texttype": [], "bintype": [], "ignoreDirs": [".*", "__pycache__"], "ignoreDirsWhitelist": [], "ignores": ["__coconut__.py", "*.bak", "*.py[cdo]", "*.class", ".fslckout"], "ignoresWhitelist": []})  # line 23
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
    print("""/|\\ {appname} /|\\

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
    update  [<branch>][/<revision>]                       Integrate work from another branch TODO add many merge and conflict resolution options
    delete  [<branch>]                                    Remove (current) branch entirely

    commit  [<message>] [--tag]                           Create a new revision from current state file tree, with an optional commit message
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
    --verbose                   Enable debugging output""".format(appname=APPNAME, cmd="sos", CMD="SOS"))  # line 93

# Main data class
#@runtime_validation
class Metadata:  # line 97
    ''' This class doesn't represent the entire repository state in memory,
      but serves as a container for different repo operations,
      using only parts of its attributes at any point in time. Use with care.
  '''  # line 101

    def __init__(_, path: 'str') -> 'None':  # line 103
        ''' Create empty container object for various repository operations. '''  # line 104
        _.c = loadConfig()  # line 105
        _.root = path  # type: str  # line 106
        _.branches = {}  # type: Dict[int, BranchInfo]  # branch number zero represents the initial state at branching  # line 107
        _.commits = {}  # type: Dict[int, CommitInfo]  # consecutive numbers per branch, starting at 0  # line 108
        _.paths = {}  # type: Dict[str, PathInfo]  # utf-8 encoded relative, normalized file system paths  # line 109
        _.tags = []  # type: List[str]  # line 110
        _.branch = None  # type: _coconut.typing.Optional[int]  # current branch number  # line 111
        _.commit = None  # type: _coconut.typing.Optional[int]  # current revision number  # line 112
        _.track = _.c.track  # type: bool  # track file name patterns in the repository (per branch)  # line 113
        _.picky = _.c.picky  # type: bool  # pick files to commit per operation  # line 114
        _.strict = _.c.strict  # type: bool  # be always strict (regarding file contents comparsion)  # line 115
        _.compress = _.c.compress  # type: bool  # these flags are stored in the repository  # line 116

    def isTextType(_, filename: 'str') -> 'bool':  # line 118
        return (((lambda _coconut_none_coalesce_item: "" if _coconut_none_coalesce_item is None else _coconut_none_coalesce_item)(mimetypes.guess_type(filename)[0])).startswith("text/") or any([fnmatch.fnmatch(filename, pattern) for pattern in _.c.texttype])) and not any([fnmatch.fnmatch(filename, pattern) for pattern in _.c.bintype])  # line 118

    def listChanges(_, changes: 'ChangeSet') -> 'None':  # line 120
        ''' In diffmode, don't list modified files, because the diff is displayed elsewhere. '''  # line 121
        if len(changes.additions) > 0:  # line 122
            print(ajoin("ADD ", sorted(changes.additions.keys()), "\n"))  # line 122
        if len(changes.deletions) > 0:  # line 123
            print(ajoin("DEL ", sorted(changes.deletions.keys()), "\n"))  # line 123
        if len(changes.modifications) > 0:  # line 124
            print(ajoin("MOD ", sorted(changes.modifications.keys()), "\n"))  # line 124

    def loadBranches(_) -> 'None':  # line 126
        ''' Load list of branches and current branch info from metadata file. '''  # line 127
        try:  # fails if not yet created (on initial branch/commit)  # line 128
            branches = None  # type: List[Tuple]  # line 129
            with codecs.open(os.path.join(_.root, metaFolder, metaFile), "r", encoding=UTF8) as fd:  # line 130
                flags, branches = json.load(fd)  # line 131
            _.tags = flags["tags"]  # list of commit messages to treat as globally unique tags  # line 132
            _.branch = flags["branch"]  # current branch integer  # line 133
            _.track = flags["track"]  # line 134
            _.picky = flags["picky"]  # line 135
            _.strict = flags["strict"]  # line 136
            _.compress = flags["compress"]  # line 137
            _.branches = {i.number: i for i in (BranchInfo(*item) for item in branches)}  # re-create type info  # line 138
        except Exception as E:  # if not found, create metadata folder  # line 139
            _.branches = {}  # line 140
            warn("Couldn't read branches metadata: %r" % E)  # line 141

    def saveBranches(_) -> 'None':  # line 143
        ''' Save list of branches and current branch info to metadata file. '''  # line 144
        with codecs.open(os.path.join(_.root, metaFolder, metaFile), "w", encoding=UTF8) as fd:  # line 145
            json.dump(({"tags": _.tags, "branch": _.branch, "track": _.track, "picky": _.picky, "strict": _.strict, "compress": _.compress}, list(_.branches.values())), fd, ensure_ascii=False)  # line 146

    def getRevisionByName(_, name: 'str') -> '_coconut.typing.Optional[int]':  # line 148
        ''' Convenience accessor for named revisions (using commit message as name). '''  # line 149
        if name == "":  # line 150
            return -1  # line 150
        try:  # attempt to parse integer string  # line 151
            return _int(name)  # attempt to parse integer string  # line 151
        except ValueError:  # line 152
            pass  # line 152
        found = [number for number, commit in _.commits.items() if name == commit.message]  # line 153
        return found[0] if found else None  # line 154

    def getBranchByName(_, name: 'str') -> '_coconut.typing.Optional[int]':  # line 156
        ''' Convenience accessor for named branches. '''  # line 157
        if name == "":  # line 158
            return _.branch  # line 158
        try:  # attempt to parse integer string  # line 159
            return _int(name)  # attempt to parse integer string  # line 159
        except ValueError:  # line 160
            pass  # line 160
        found = [number for number, branch in _.branches.items() if name == branch.name]  # line 161
        return found[0] if found else None  # line 162

    def loadBranch(_, branch: 'int') -> 'None':  # line 164
        ''' Load all commit information from a branch meta data file. '''  # line 165
        with codecs.open(os.path.join(_.root, metaFolder, "b%d" % branch, metaFile), "r", encoding=UTF8) as fd:  # line 166
            commits = json.load(fd)  # type: List[List[Any]]  # list of CommitInfo that needs to be unmarshalled into value types  # line 167
        _.commits = {i.number: i for i in (CommitInfo(*item) for item in commits)}  # re-create type info  # line 168
        _.branch = branch  # line 169

    def saveBranch(_, branch: 'int') -> 'None':  # line 171
        ''' Save all commit information to a branch meta data file. '''  # line 172
        with codecs.open(os.path.join(_.root, metaFolder, "b%d" % branch, metaFile), "w", encoding=UTF8) as fd:  # line 173
            json.dump(list(_.commits.values()), fd, ensure_ascii=False)  # line 174

    def duplicateBranch(_, branch: 'int', name: '_coconut.typing.Optional[str]') -> 'None':  # line 176
        ''' Create branch from an existing branch/revision. WARN: Caller must have loaded branches information.
        branch: target branch (should not exist yet)
        name: optional name of new branch
        _.branch: current branch
    '''  # line 181
        debug("Duplicating branch '%s' to '%d'..." % ((lambda _coconut_none_coalesce_item: "b%d" % _.branch if _coconut_none_coalesce_item is None else _coconut_none_coalesce_item)(_.branches[_.branch].name), branch))  # line 182
        tracked = [t for t in _.branches[_.branch].tracked]  # copy  # line 183
        os.makedirs(os.path.join(_.root, metaFolder, "b%d" % branch, "r0"))  # line 184
        _.loadBranch(_.branch)  # line 185
        revision = max(_.commits)  # type: int  # line 186
        _.computeSequentialPathSet(_.branch, revision)  # full set of files in revision to _.paths  # line 187
        for path, pinfo in _.paths.items():  # line 188
            _.copyVersionedFile(_.branch, revision, branch, 0, pinfo)  # line 189
        _.commits = {0: CommitInfo(0, _int(time.time() * 1000), "Branched from '%s'" % ((lambda _coconut_none_coalesce_item: "b%d" % _.branch if _coconut_none_coalesce_item is None else _coconut_none_coalesce_item)(_.branches[_.branch].name)))}  # store initial commit  # line 190
        _.saveBranch(branch)  # save branch meta data to branch folder  # line 191
        _.saveCommit(branch, 0)  # save commit meta data to revision folder  # line 192
        _.branches[branch] = BranchInfo(branch, _.commits[0].ctime, name, _.branches[_.branch].insync, tracked)  # save branch info, before storing repo state at caller  # line 193

    def createBranch(_, branch: 'int', name: '_coconut.typing.Optional[str]'=None, initialMessage: '_coconut.typing.Optional[str]'=None):  # line 195
        ''' Create a new branch from current file tree. This clears all known commits and modifies the file system.
        branch: target branch (should not exist yet)
        name: optional name of new branch
        _.branch: current branch, must exist already
    '''  # line 200
        simpleMode = not (_.track or _.picky)  # line 201
        tracked = [t for t in _.branches[_.branch].tracked] if _.track and len(_.branches) > 0 else []  # in case of initial branch creation  # line 202
        debug((lambda _coconut_none_coalesce_item: "b%d" % branch if _coconut_none_coalesce_item is None else _coconut_none_coalesce_item)("Creating branch '%s'..." % name))  # line 203
        _.paths = {}  # type: Dict[str, PathInfo]  # line 204
        if simpleMode:  # branches from file system state  # line 205
            changes = _.findChanges(branch, 0, progress=simpleMode)  # type: ChangeSet  # creates revision folder and versioned files  # line 206
            _.listChanges(changes)  # line 207
            _.paths.update(changes.additions.items())  # line 208
        else:  # tracking or picky mode: branch from lastest revision  # line 209
            os.makedirs(os.path.join(_.root, metaFolder, "b%d" % branch, "r0"))  # line 210
            if _.branch is not None:  # not immediately after "offline" - copy files from current branch  # line 211
                _.loadBranch(_.branch)  # line 212
                revision = max(_.commits)  # type: int  # TODO what if last switch was to an earlier revision? no persisting of last checkout  # line 213
                _.computeSequentialPathSet(_.branch, revision)  # full set of files in revision to _.paths  # line 214
                for path, pinfo in _.paths.items():  # line 215
                    _.copyVersionedFile(_.branch, revision, branch, 0, pinfo)  # line 216
        ts = _int(time.time() * 1000)  # line 217
        _.commits = {0: CommitInfo(0, ts, "Branched on %s" % strftime(ts) if initialMessage is None else initialMessage)}  # store initial commit for new branch  # line 218
        _.saveBranch(branch)  # save branch meta data (revisions) to branch folder  # line 219
        _.saveCommit(branch, 0)  # save commit meta data to revision folder  # line 220
        _.branches[branch] = BranchInfo(branch, _.commits[0].ctime, name, True if len(_.branches) == 0 else _.branches[_.branch].insync, tracked)  # save branch info, in case it is needed  # line 221

    def removeBranch(_, branch: 'int') -> 'BranchInfo':  # line 223
        ''' Entirely remove a branch and all its revisions from the file system. '''  # line 224
        shutil.rmtree(os.path.join(_.root, metaFolder, "b%d" % branch))  # line 225
        binfo = _.branches[branch]  # line 226
        del _.branches[branch]  # line 227
        _.branch = max(_.branches)  # line 228
        _.saveBranches()  # line 229
        _.commits.clear()  # line 230
        return binfo  # line 231

    def loadCommit(_, branch: 'int', revision: 'int') -> 'None':  # line 233
        ''' Load all file information from a commit meta data. '''  # line 234
        with codecs.open(os.path.join(_.root, metaFolder, "b%d" % branch, "r%d" % revision, metaFile), "r", encoding=UTF8) as fd:  # line 235
            _.paths = json.load(fd)  # line 236
        _.paths = {path: PathInfo(*item) for path, item in _.paths.items()}  # re-create type info  # line 237
        _.branch = branch  # line 238

    def saveCommit(_, branch: 'int', revision: 'int'):  # line 240
        ''' Save all file information to a commit meta data file. '''  # line 241
        target = os.path.join(_.root, metaFolder, "b%d" % branch, "r%d" % revision)  # line 242
        try:  # line 243
            os.makedirs(target)  # line 243
        except:  # line 244
            pass  # line 244
        with codecs.open(os.path.join(target, metaFile), "w", encoding=UTF8) as fd:  # line 245
            json.dump(_.paths, fd, ensure_ascii=False)  # line 246

    def findChanges(_, branch: '_coconut.typing.Optional[int]'=None, revision: '_coconut.typing.Optional[int]'=None, checkContent: 'bool'=False, inverse: 'bool'=False, considerOnly: '_coconut.typing.Optional[FrozenSet[str]]'=None, progress: 'bool'=False) -> 'ChangeSet':  # line 248
        ''' Find changes on the file system vs. in-memory paths (which should reflect the latest commit state).
        Only if both branch and revision are *not* None, write modified/added files to the specified revision folder (thus creating a new revision)
        The function returns the state of file tree *differences*, unless "inverse" is True -> then return original data
        checkContent: also computes file content hashes
        inverse: retain original state (size, mtime, hash) instead of updated one
        considerOnly: set of tracking patterns. For update operation, union of other and current branch
        progress: Show file names during processing
    '''  # line 256
        write = branch is not None and revision is not None  # line 257
        if write:  # line 258
            os.makedirs(os.path.join(_.root, metaFolder, "b%d" % branch, "r%d" % revision))  # line 258
        changes = ChangeSet({}, {}, {})  # type: ChangeSet  # line 259
        counter = Counter(-1)  # type: Counter  # line 260
        timer = time.time()  # line 260
        for path, dirnames, filenames in os.walk(_.root):  # line 261
            dirnames[:] = [f for f in dirnames if len([n for n in _.c.ignoreDirs if fnmatch.fnmatch(f, n)]) == 0 or len([p for p in _.c.ignoreDirsWhitelist if fnmatch.fnmatch(f, p)]) > 0]  # line 262
            filenames[:] = [f for f in filenames if len([n for n in _.c.ignores if fnmatch.fnmatch(f, n)]) == 0 or len([p for p in _.c.ignoresWhitelist if fnmatch.fnmatch(f, p)]) > 0]  # line 263
            dirnames.sort()  # line 264
            filenames.sort()  # line 264
            relpath = os.path.relpath(path, _.root).replace(os.sep, SLASH)  # line 265
            for file in (filenames if considerOnly is None else list(reduce(lambda last, pattern: last | set(fnmatch.filter(filenames, os.path.basename(pattern))), (p for p in considerOnly if os.path.dirname(p) == relpath), _coconut.set()))):  # if m.track or m.picky: only files that match any path-relevant tracking patterns  # line 266
                filename = relpath + SLASH + file  # line 267
                filepath = os.path.join(path, file)  # line 268
                stat = os.stat(filepath)  # line 269
                size, mtime, newtime = stat.st_size, _int(stat.st_mtime * 1000), time.time()  # line 270
                if progress and newtime - timer > .1:  # line 271
                    outstring = "\rPreparing %s  %s" % (PROGRESS_MARKER[counter.inc() % 4], filename)  # line 272
                    sys.stdout.write(outstring + " " * max(0, termWidth - len(outstring)))  # TODO could write to new line instead of carriage return, also needs terminal width  # line 273
                    sys.stdout.flush()  # TODO could write to new line instead of carriage return, also needs terminal width  # line 273
                    timer = newtime  # TODO could write to new line instead of carriage return, also needs terminal width  # line 273
                if filename not in _.paths:  # detected file not present (or untracked) in other branch  # line 274
                    namehash = hashStr(filename)  # line 275
                    changes.additions[filename] = PathInfo(namehash, size, mtime, hashFile(filepath, _.compress, saveTo=os.path.join(_.root, metaFolder, "b%d" % branch, "r%d" % revision, namehash) if write else None) if size > 0 else None)  # line 276
                    continue  # line 277
                last = _.paths[filename]  # filename is known - check for modifications  # line 278
                if last.size is None:  # was removed before but is now added back - does not apply for tracking mode (which never marks files for removal in the history)  # line 279
                    changes.additions[filename] = PathInfo(last.namehash, size, mtime, hashFile(filepath, _.compress, saveTo=os.path.join(_.root, metaFolder, "b%d" % branch, "r%d" % revision, last.namehash) if write else None) if size > 0 else None)  # line 280
                    continue  # line 280
                elif size != last.size or mtime != last.mtime or (checkContent and hashFile(filepath, _.compress) != last.hash):  # detected a modification  # line 281
                    changes.modifications[filename] = PathInfo(last.namehash, last.size if inverse else size, last.mtime if inverse else mtime, last.hash if inverse else hashFile(filepath, _.compress, saveTo=os.path.join(_.root, metaFolder, "b%d" % branch, "r%d" % revision, last.namehash) if write else None) if (last.size if inverse else size) > 0 else None)  # line 282
# Detect deletions. Files no longer being tracked should not be found here
            for folderPath in (p for p, pinfo in _.paths.items() if p[:p.rindex(SLASH)] == relpath and pinfo.size is not None):  # only versioned (and tracked) files that match currently visited folder. TODO don't check for removal just added entries  # line 284
                if folderPath[len(relpath) + 1:] not in filenames:  # filename no longer in file tree TODO use basename and dirname instead of slicing?  # line 285
                    changes.deletions[folderPath] = _.paths[folderPath]  # filename no longer in file tree TODO use basename and dirname instead of slicing?  # line 285
        if progress:  # force new line  # line 286
            print("Preparation finished." + " " * (termWidth - 21), file=sys.stdout)  # force new line  # line 286
        return changes  # line 287

    def integrateChangeset(_, changes: 'ChangeSet', clear=False) -> 'None':  # line 289
        ''' In-memory update from a changeset, marking deleted files with size=None. Use clear = True to start on an empty path set. '''  # line 290
        if clear:  # line 291
            _.paths.clear()  # line 291
        else:  # line 292
            rm = [p for p, info in _.paths.items() if info.size is None]  # remove files deleted in earlier change sets (revisions)  # line 293
            for old in rm:  # remove previously removed entries completely  # line 294
                del _.paths[old]  # remove previously removed entries completely  # line 294
        for d, info in changes.deletions.items():  # mark now removed entries as deleted  # line 295
            _.paths[d] = PathInfo(info.namehash, None, info.mtime, None)  # mark now removed entries as deleted  # line 295
        _.paths.update(changes.additions)  # line 296
        _.paths.update(changes.modifications)  # line 297

    def computeSequentialPathSet(_, branch: 'int', revision: 'int') -> 'None':  # line 299
        next(_.computeSequentialPathSetIterator(branch, revision, incrementally=False))  # simply invoke the generator once  # line 300

    def computeSequentialPathSetIterator(_, branch: 'int', revision: 'int', incrementally: 'bool'=True) -> '_coconut.typing.Optional[Iterator[ChangeSet]]':  # line 302
        ''' In-memory computation of current list of valid PathInfo entries for specified branch and until specified revision (inclusively) by traversing revision on the file system. '''  # line 303
        _.loadCommit(branch, 0)  # load initial paths  # line 304
        if incrementally:  # line 305
            yield diffPathSets({}, _.paths)  # line 305
        n = Metadata(_.root)  # type: Metadata  # next changes  # line 306
        for revision in range(1, revision + 1):  # line 307
            n.loadCommit(branch, revision)  # line 308
            changes = diffPathSets(_.paths, n.paths)  # type: ChangeSet  # line 309
            _.integrateChangeset(changes)  # line 310
            if incrementally:  # line 311
                yield changes  # line 311
        yield None  # for the default case - not incrementally  # line 312

    def parseRevisionString(_, argument: 'str') -> 'Tuple[_coconut.typing.Optional[int], _coconut.typing.Optional[int]]':  # line 314
        ''' Commit identifiers can be str or int for branch, and int for revision.
        Revision identifiers can be negative, with -1 being last commit.
    '''  # line 317
        if argument is None or argument == SLASH:  # no branch/revision specified  # line 318
            return (_.branch, -1)  # no branch/revision specified  # line 318
        argument = argument.strip()  # line 319
        if argument.startswith(SLASH):  # current branch  # line 320
            return (_.branch, _.getRevisionByName(argument[1:]))  # current branch  # line 320
        if argument.endswith(SLASH):  # line 321
            try:  # line 322
                return (_.getBranchByName(argument[:-1]), -1)  # line 322
            except ValueError:  # line 323
                Exit("Unknown branch label")  # line 323
        if SLASH in argument:  # line 324
            b, r = argument.split(SLASH)[:2]  # line 325
            try:  # line 326
                return (_.getBranchByName(b), _.getRevisionByName(r))  # line 326
            except ValueError:  # line 327
                Exit("Unknown branch label or wrong number format")  # line 327
        branch = _.getBranchByName(argument)  # type: int  # returns number if given (revision) integer  # line 328
        if branch not in _.branches:  # line 329
            branch = None  # line 329
        try:  # either branch name/number or reverse/absolute revision number  # line 330
            return (_.branch if branch is None else branch, _int(argument) if branch is None else -1)  # either branch name/number or reverse/absolute revision number  # line 330
        except:  # line 331
            Exit("Unknown branch label or wrong number format")  # line 331
        return (None, None)  # should never be reached TODO raise exception instead?  # line 332

    def findRevision(_, branch: 'int', revision: 'int', namehash: 'str') -> 'Tuple[int, str]':  # line 334
        while True:  # find latest revision that contained the file physically  # line 335
            source = os.path.join(_.root, metaFolder, "b%d" % branch, "r%d" % revision, namehash)  # type: str  # line 336
            if os.path.exists(source) and os.path.isfile(source):  # line 337
                break  # line 337
            revision -= 1  # line 338
            if revision < 0:  # line 339
                Exit("Cannot determine versioned file '%s' from specified branch '%d'" % (namehash, branch))  # line 339
        return revision, source  # line 340

    def copyVersionedFile(_, branch: 'int', revision: 'int', tobranch: 'int', torevision: 'int', pinfo: 'PathInfo') -> 'None':  # line 342
        ''' Copy versioned file to other branch/revision. '''  # line 343
        target = os.path.join(_.root, metaFolder, "b%d" % tobranch, "r%d" % torevision, pinfo.namehash)  # type: str  # line 344
        revision, source = _.findRevision(branch, revision, pinfo.namehash)  # line 345
        shutil.copy2(source, target)  # line 346

    def readOrCopyVersionedFile(_, branch: 'int', revision: 'int', namehash: 'str', toFile: '_coconut.typing.Optional[str]'=None) -> '_coconut.typing.Optional[bytes]':  # line 348
        ''' Return file contents, or copy contents into file path provided. '''  # line 349
        source = os.path.join(_.root, metaFolder, "b%d" % branch, "r%d" % revision, namehash)  # type: str  # line 350
        try:  # line 351
            with openIt(source, "r", _.compress) as fd:  # line 352
                if toFile is None:  # read bytes into memory and return  # line 353
                    return fd.read()  # read bytes into memory and return  # line 353
                with open(toFile, "wb") as to:  # line 354
                    while True:  # line 355
                        buffer = fd.read(bufSize)  # line 356
                        to.write(buffer)  # line 357
                        if len(buffer) < bufSize:  # line 358
                            break  # line 358
                    return None  # line 359
        except Exception as E:  # line 360
            warn("Cannot read versioned file: %r (%d/%d/%s)" % (E, branch, revision, namehash))  # line 360
        return None  # line 361

    def restoreFile(_, relpath: '_coconut.typing.Optional[str]', branch: 'int', revision: 'int', pinfo: 'PathInfo') -> '_coconut.typing.Optional[bytes]':  # line 363
        ''' Recreate file for given revision, or return contents if path is None. '''  # line 364
        if relpath is None:  # just return contents  # line 365
            return _.readOrCopyVersionedFile(branch, _.findRevision(branch, revision, pinfo.namehash)[0], pinfo.namehash) if pinfo.size > 0 else b''  # just return contents  # line 365
        target = os.path.join(_.root, relpath.replace(SLASH, os.sep))  # type: str  # line 366
        if pinfo.size == 0:  # line 367
            with open(target, "wb"):  # line 368
                pass  # line 368
            try:  # update access/modification timestamps on file system  # line 369
                os.utime(target, (-1, pinfo.mtime / 1000.))  # update access/modification timestamps on file system  # line 369
            except Exception as E:  # line 370
                error("Cannot update file's timestamp after restoration '%r'" % E)  # line 370
            return None  # line 371
        revision, source = _.findRevision(branch, revision, pinfo.namehash)  # line 372
# Restore file by copying buffer-wise
        with openIt(source, "r", _.compress) as fd, open(target, "wb") as to:  # using Coconut's Enhanced Parenthetical Continuation  # line 374
            while True:  # line 375
                buffer = fd.read(bufSize)  # line 376
                to.write(buffer)  # line 377
                if len(buffer) < bufSize:  # line 378
                    break  # line 378
        try:  # update access/modification timestamps on file system  # line 379
            os.utime(target, (-1, pinfo.mtime / 1000.))  # update access/modification timestamps on file system  # line 379
        except Exception as E:  # line 380
            error("Cannot update file's timestamp after restoration '%r'" % E)  # line 380
        return None  # line 381

    def getTrackingPatterns(_, branch: '_coconut.typing.Optional[int]'=None) -> 'FrozenSet[str]':  # line 383
        ''' Returns list of tracking patterns for provided branch or current branch. '''  # line 384
        return _coconut.frozenset() if not _.track and not _.picky else frozenset(_.branches[_.branch if branch is None else branch].tracked)  # line 385


# Main client operations
def offline(argument: '_coconut.typing.Optional[str]'=None, options: '_coconut.typing.Sequence[str]'=[]) -> 'None':  # line 389
    ''' Initial command to start working offline. '''  # line 390
    if os.path.exists(metaFolder):  # line 391
        if '--force' not in options:  # line 392
            Exit("Repository folder is either already offline or older branches and commits were left over. Use 'sos online' or continue working offline")  # line 392
        try:  # line 393
            for entry in os.listdir(metaFolder):  # line 394
                resource = metaFolder + os.sep + entry  # line 395
                if os.path.isdir(resource):  # line 396
                    shutil.rmtree(resource)  # line 396
                else:  # line 397
                    os.unlink(resource)  # line 397
        except:  # line 398
            Exit("Cannot reliably remove previous repository contents. Please remove .sos folder manually prior to going offline")  # line 398
    m = Metadata(os.getcwd())  # type: Metadata  # line 399
    if '--plain' in options or not m.c.compress:  # plain file copies instead of compressed ones  # line 400
        m.compress = False  # plain file copies instead of compressed ones  # line 400
    if '--picky' in options or m.c.picky:  # Git-like  # line 401
        m.picky = True  # Git-like  # line 401
    elif '--track' in options or m.c.track:  # Svn-like  # line 402
        m.track = True  # Svn-like  # line 402
    if '--strict' in options or m.c.strict:  # always hash contents  # line 403
        m.strict = True  # always hash contents  # line 403
    debug("Preparing offline repository...")  # line 404
    m.createBranch(0, str(defaults["defaultbranch"]) if argument is None else argument, initialMessage="Offline repository created on %s" % strftime())  # main branch's name may be None (e.g. for fossil)  # line 405
    m.branch = 0  # line 406
    m.saveBranches()  # no change immediately after going offline, going back online won't issue a warning  # line 407
    info("Offline repository prepared. Use 'sos online' to finish offline work")  # line 408

def online(options: '_coconut.typing.Sequence[str]'=[]) -> 'None':  # line 410
    ''' Finish working offline. '''  # line 411
    force = '--force' in options  # type: bool  # line 412
    m = Metadata(os.getcwd())  # line 413
    m.loadBranches()  # line 414
    if any([not b.insync for b in m.branches.values()]) and not force:  # line 415
        Exit("There are still unsynchronized (dirty) branches.\nUse 'sos log' to list them.\nUse 'sos commit' and 'sos switch' to commit dirty branches to your VCS before leaving offline mode.\nUse 'sos online --force' to erase all aggregated offline revisions.")  # line 415
    strict = '--strict' in options or m.strict  # type: bool  # line 416
    if options.count("--force") < 2:  # line 417
        changes = m.findChanges(checkContent=strict, considerOnly=None if not m.track else m.getTrackingPatterns())  # type: ChangeSet  # line 418
        if modified(changes):  # line 419
            Exit("File tree is modified vs. current branch.\nUse 'sos online --force --force' to continue with removing the offline repository.")  # line 419
    try:  # line 420
        shutil.rmtree(metaFolder)  # line 420
        info("Exited offline mode. Continue working with your traditional VCS.")  # line 420
    except Exception as E:  # line 421
        Exit("Error removing offline repository: %r" % E)  # line 421

def branch(argument: '_coconut.typing.Optional[str]'=None, options: '_coconut.typing.Sequence[str]'=[]) -> 'None':  # line 423
    ''' Create a new branch (from file tree or last revision) and (by default) continue working on it. '''  # line 424
    last = '--last' in options  # type: bool  # use last revision for branching, not current file tree  # line 425
    stay = '--stay' in options  # type: bool  # continue on current branch after branching  # line 426
    force = '--force' in options  # type: bool  # branch even with local modifications  # line 427
    m = Metadata(os.getcwd())  # type: Metadata  # line 428
    m.loadBranches()  # line 429
    if argument and m.getBranchByName(argument) is not None:  # create a named branch  # line 430
        Exit("Branch '%s' already exists. Cannot proceed" % argument)  # create a named branch  # line 430
    branch = max(m.branches.keys()) + 1  # next branch's key - this isn't atomic but we assume single-user non-concurrent use here  # line 431
    debug("Branching to %sbranch b%02d%s%s..." % ("unnamed " if argument is None else "", branch, " '%s'" % argument if argument else "", " from last revision" if last else ""))  # line 432
    if last:  # line 433
        m.duplicateBranch(branch, argument)  # branch from branch's last revision  # line 434
    else:  # from file tree state  # line 435
        m.createBranch(branch, argument)  # branch from current file tree  # line 436
    if not stay:  # line 437
        m.branch = branch  # line 438
        m.saveBranches()  # line 439
    info("%s new %sbranch b%02d%s" % ("Continue work after branching" if stay else "Switched to", "unnamed " if argument is None else "", branch, " '%s'" % argument if argument else ""))  # line 440

def changes(argument: 'str'=None, options: '_coconut.typing.Sequence[str]'=[]) -> 'ChangeSet':  # line 442
    ''' Show changes of file tree vs. (last or specified) revision on current or specified branch. '''  # line 443
    m = Metadata(os.getcwd())  # type: Metadata  # line 444
    branch = None  # type: _coconut.typing.Optional[int]  # line 444
    revision = None  # type: _coconut.typing.Optional[int]  # line 444
    m.loadBranches()  # knows current branch  # line 445
    strict = '--strict' in options or m.strict  # type: bool  # line 446
    branch, revision = m.parseRevisionString(argument)  # line 447
    if branch not in m.branches:  # line 448
        Exit("Unknown branch")  # line 448
    m.loadBranch(branch)  # knows commits  # line 449
    revision = revision if revision >= 0 else len(m.commits) + revision  # negative indexing  # line 450
    if revision < 0 or revision > max(m.commits):  # line 451
        Exit("Unknown revision r%02d" % revision)  # line 451
    info("/|\\ Changes of file tree vs. revision '%s/r%02d'" % ((lambda _coconut_none_coalesce_item: "b%02d" % branch if _coconut_none_coalesce_item is None else _coconut_none_coalesce_item)(m.branches[branch].name), revision))  # line 452
    m.computeSequentialPathSet(branch, revision)  # load all commits up to specified revision  # line 453
    changes = m.findChanges(checkContent=strict, considerOnly=None if not m.track else m.getTrackingPatterns() | m.getTrackingPatterns(branch))  # type: ChangeSet  # line 454
    m.listChanges(changes)  # line 455
    return changes  # line 456

def diff(argument: 'str', options: '_coconut.typing.Sequence[str]'=[]) -> 'None':  # line 458
    ''' Show text file differences of file tree vs. (last or specified) revision on current or specified branch. '''  # line 459
    m = Metadata(os.getcwd())  # type: Metadata  # line 460
    branch = None  # type: _coconut.typing.Optional[int]  # line 460
    revision = None  # type: _coconut.typing.Optional[int]  # line 460
    m.loadBranches()  # knows current branch  # line 461
    strict = '--strict' in options or m.strict  # type: bool  # line 462
    branch, revision = m.parseRevisionString(argument)  # line 463
    if branch not in m.branches:  # line 464
        Exit("Unknown branch")  # line 464
    m.loadBranch(branch)  # knows commits  # line 465
    revision = revision if revision >= 0 else len(m.commits) + revision  # negative indexing  # line 466
    if revision < 0 or revision > max(m.commits):  # line 467
        Exit("Unknown revision r%02d" % revision)  # line 467
    info("/|\\ Differences of file tree vs. revision '%s/r%02d'" % ((lambda _coconut_none_coalesce_item: "b%02d" % branch if _coconut_none_coalesce_item is None else _coconut_none_coalesce_item)(m.branches[branch].name), revision))  # line 468
    m.computeSequentialPathSet(branch, revision)  # load all commits up to specified revision  # line 469
    changes = m.findChanges(checkContent=strict, inverse=True, considerOnly=None if not m.track else m.getTrackingPatterns() | m.getTrackingPatterns(branch))  # type: ChangeSet  # line 470
    onlyBinaryModifications = dataCopy(ChangeSet, changes, modifications={k: v for k, v in changes.modifications.items() if not m.isTextType(k)})  # type: ChangeSet  # line 471
    if modified(onlyBinaryModifications):  # line 472
        debug("/|\\ File changes")  # line 472
    m.listChanges(onlyBinaryModifications)  # only list modified binary files  # line 473

    if changes.modifications:  # TODO only text files, not binary  # line 475
        debug("%s/|\\ Textual modifications" % ("\n" if modified(onlyBinaryModifications) else ""))  # TODO only text files, not binary  # line 475
    for path, pinfo in changes.modifications.items():  # only consider modified files TODO also show A/D here? or replace listing above?  # line 476
        content = None  # type: _coconut.typing.Optional[bytes]  # ; othr:str[]; curr:str[]  # line 477
        if pinfo.size == 0:  # empty file contents  # line 478
            content = b""  # empty file contents  # line 478
        else:  # versioned file  # line 479
            content = m.restoreFile(None, branch, revision, pinfo)  # versioned file  # line 479
            assert content is not None  # versioned file  # line 479
        abspath = os.path.join(m.root, path.replace(SLASH, os.sep))  # current file  # line 480
        blocks = merge(file=content, intoname=abspath, diffOnly=True)  # type: List[MergeBlock]  # only determine change blocks  # line 481
        print("DIF %s%s" % (path, " <timestamp only>" if len(blocks) == 1 and blocks[0].tipe == MergeBlockType.KEEP else ""))  # line 482
        for block in blocks:  # line 483
            if block.tipe in [MergeBlockType.INSERT, MergeBlockType.REMOVE]:  # line 484
                pass  # TODO print some previous and following lines - which aren't accessible here anymore  # line 485
            if block.tipe == MergeBlockType.INSERT:  # TODO show color via curses?  # line 486
                for no, line in enumerate(block.lines):  # line 487
                    print("+++ %04d |%s|" % (no + block.line, line))  # line 488
            elif block.tipe == MergeBlockType.REMOVE:  # line 489
                for no, line in enumerate(block.lines):  # line 490
                    print("--- %04d |%s|" % (no + block.line, line))  # line 491
            elif block.tipe in [MergeBlockType.REPLACE, MergeBlockType.MODIFY]:  # TODO for MODIFY also show intra-line change ranges  # line 492
                for no, line in enumerate(block.replaces.lines):  # line 493
                    print("- | %04d |%s|" % (no + block.replaces.line, line))  # line 494
                for no, line in enumerate(block.lines):  # line 495
                    print("+ | %04d |%s|" % (no + block.line, line))  # line 496
#      elif block.tipe == MergeBlockType.KEEP: pass
#      elif block.tipe == MergeBlockType.MODIFY:  # intra-line modifications
#      elif block.tipe == MergeBlockType.MOVE:  # intra-line modifications

def commit(argument: '_coconut.typing.Optional[str]'=None, options: '_coconut.typing.Sequence[str]'=[]) -> 'None':  # line 501
    ''' Create new revision from file tree changes vs. last commit. '''  # line 502
    m = Metadata(os.getcwd())  # type: Metadata  # line 503
    m.loadBranches()  # knows current branch  # line 504
    if argument is not None and argument in m.tags:  # line 505
        Exit("Illegal commit message. It was already used as a tag name")  # line 505
    changes = None  # type: ChangeSet  # line 506
    m, branch, revision, changes, strict, force, trackingPatterns = exitOnChanges(None, options, commit=True)  # special flag creates new revision for detected changes, but abort if no changes  # line 507
    info((lambda _coconut_none_coalesce_item: "b%d" % m.branch if _coconut_none_coalesce_item is None else _coconut_none_coalesce_item)("Committing changes to branch '%s'..." % m.branches[m.branch].name))  # line 508
    m.integrateChangeset(changes, clear=True)  # update pathset to changeset only  # line 509
    m.saveCommit(m.branch, revision)  # revision has already been incremented  # line 510
    m.commits[revision] = CommitInfo(revision, _int(time.time() * 1000), argument)  # comment can be None  # line 511
    m.saveBranch(m.branch)  # line 512
    m.loadBranches()  # TODO is it necessary to load again?  # line 513
    if m.picky:  # HINT was changed from only picky to include track as well  # line 514
        m.branches[m.branch] = dataCopy(BranchInfo, m.branches[m.branch], tracked=[], insync=False)  # remove tracked patterns  # line 515
    else:  # track or simple mode  # line 516
        m.branches[m.branch] = dataCopy(BranchInfo, m.branches[m.branch], insync=False)  # set branch dirty  # line 517
    if "--tag" in options and argument is not None:  # memorize unique tag  # line 518
        m.tags.append(argument)  # memorize unique tag  # line 518
    m.saveBranches()  # line 519
    info("Created new revision r%02d%s (+%02d/-%02d/*%02d)" % (revision, ((" '%s'" % argument) if argument is not None else ""), len(changes.additions), len(changes.deletions), len(changes.modifications)))  # line 520

def status() -> 'None':  # line 522
    ''' Show branches and current repository state. '''  # line 523
    m = Metadata(os.getcwd())  # type: Metadata  # line 524
    m.loadBranches()  # knows current branch  # line 525
    current = m.branch  # type: int  # line 526
    info("/|\\ Offline repository status")  # line 527
    sl = max([len((lambda _coconut_none_coalesce_item: "" if _coconut_none_coalesce_item is None else _coconut_none_coalesce_item)(b.name)) for b in m.branches.values()])  # type: int  # line 528
    for branch in sorted(m.branches.values(), key=lambda b: b.number):  # line 529
        m.loadBranch(branch.number)  # knows commit history  # line 530
        print("  %s b%02d%s @%s (%s) with %d commits%s" % ("*" if current == branch.number else " ", branch.number, ((" %%%ds" % (sl + 2)) % ("'%s'" % branch.name)) if branch.name else "", strftime(branch.ctime), "in sync" if branch.insync else "dirty", len(m.commits), ". Last comment: '%s'" % m.commits[max(m.commits)].message if m.commits[max(m.commits)].message else ""))  # line 531
    if m.track or m.picky and len(m.branches[m.branch].tracked) > 0:  # line 532
        info("\nTracked file patterns:")  # line 533
        print(ajoin("  | ", m.branches[m.branch].tracked, "\n"))  # line 534

def exitOnChanges(argument: '_coconut.typing.Optional[str]'=None, options: '_coconut.typing.Sequence[str]'=[], check: 'bool'=True, commit: 'bool'=False) -> 'Tuple[Metadata, _coconut.typing.Optional[int], int, ChangeSet, bool, bool, FrozenSet[str]]':  # line 536
    ''' Common behavior for switch, update, delete, commit.
      check: stop program on detected change
      commit: don't stop on changes, because that's what we need in the operation
      Returns (Metadata, (current or target) branch, revision, set of changes vs. last commit on current branch, strict, force flags. '''  # line 540
    m = Metadata(os.getcwd())  # type: Metadata  # line 541
    m.loadBranches()  # knows current branch  # line 542
    trackingPatterns = m.getTrackingPatterns()  # type: FrozenSet[str]  # SVN-like mode  # line 543
    force = '--force' in options  # type: bool  # line 544
    strict = '--strict' in options or m.strict  # type: bool  # line 545
    if argument is not None:  # line 546
        branch, revision = m.parseRevisionString(argument)  # for early abort  # line 547
        if branch is None:  # line 548
            Exit("Branch '%s' doesn't exist. Cannot proceed" % argument)  # line 548
    m.loadBranch(m.branch)  # knows last commits of *current* branch  # line 549

# Determine current changes
    m.computeSequentialPathSet(m.branch, max(m.commits))  # load all commits up to specified revision  # line 552
    changes = m.findChanges(m.branch if commit else None, max(m.commits) + 1 if commit else None, checkContent=strict, considerOnly=None if not m.track and not m.picky else trackingPatterns)  # type: ChangeSet  # line 553
    if modified(changes) and not force:  # and check?  # line 554
        m.listChanges(changes)  # line 555
        if check and not commit:  # line 556
            Exit("File tree contains changes. Use --force to proceed")  # line 556
    elif commit and not force:  #  and not check  # line 557
        Exit("Nothing to commit. Aborting")  #  and not check  # line 557

    if argument is not None:  # branch/revision specified  # line 559
        m.loadBranch(branch)  # knows commits of target branch  # line 560
        revision = revision if revision >= 0 else len(m.commits) + revision  # negative indexing  # line 561
        if revision < 0 or revision > max(m.commits):  # line 562
            Exit("Unknown revision r%02d" % revision)  # line 562
        return (m, branch, revision, changes, strict, force, m.getTrackingPatterns(branch))  # line 563
    return (m, m.branch, max(m.commits) + (1 if commit else 0), changes, strict, force, trackingPatterns)  # line 564

def switch(argument: 'str', options: '_coconut.typing.Sequence[str]'=[]) -> 'None':  # line 566
    ''' Continue work on another branch, replacing file tree changes. '''  # line 567
    changes = None  # type: ChangeSet  # line 568
    m, branch, revision, changes, strict, force, trackingPatterns = exitOnChanges(argument, options)  # line 569
    info("/|\\ Switching to branch %sb%02d/r%02d" % ("'%s' " % m.branches[branch].name if m.branches[branch].name else "", branch, revision))  # line 570

# Determine file changes from other branch to current file tree
    if '--meta' in options:  # only switch meta data  # line 573
        m.branches[m.branch] = dataCopy(BranchInfo, m.branches[m.branch], tracked=m.branches[branch].tracked)  # line 574
    else:  # full file switch  # line 575
        m.computeSequentialPathSet(branch, revision)  # load all commits up to specified revision for target branch into memory  # line 576
        changes = m.findChanges(checkContent=strict, inverse=True, considerOnly=None if not m.track else trackingPatterns | m.getTrackingPatterns(branch))  # determine difference of other branch vs. file tree (forced or in sync with current branch; "addition" means exists now and should be removed)  # line 577
        if not modified(changes):  # line 578
            info("No changes to current file tree")  # line 579
        else:  # integration required  # line 580
            for path, pinfo in changes.deletions.items():  # line 581
                m.restoreFile(path, branch, revision, pinfo)  # is deleted in current file tree: restore from branch to reach target  # line 582
                debug("ADD " + path)  # line 583
            for path, pinfo in changes.additions.items():  # line 584
                os.unlink(os.path.join(m.root, path.replace(SLASH, os.sep)))  # is added in current file tree: remove from branch to reach target  # line 585
                debug("DEL " + path)  # line 586
            for path, pinfo in changes.modifications.items():  # line 587
                m.restoreFile(path, branch, revision, pinfo)  # is modified in current file tree: restore from branch to reach target  # line 588
                debug("MOD " + path)  # line 589
    m.branch = branch  # line 590
    m.saveBranches()  # store switched path info  # line 591
    info("Switched to branch %sb%02d/r%02d" % ("'%s' " % (m.branches[branch].name if m.branches[branch].name else ""), branch, revision))  # line 592

def update(argument: 'str', options: '_coconut.typing.Sequence[str]'=[]) -> 'None':  # line 594
    ''' Load and integrate a specified other branch/revision into current life file tree.
      In tracking mode, this also updates the set of tracked patterns.
      User options for merge operation: --add (don't remove), --rm (don't insert), --add-lines/--rm-lines (inside each file)
      User options for conflict resolution: --theirs/--mine/--ask
  '''  # line 599
    mrg = firstOfMap({"--add": MergeOperation.INSERT, "--rm": MergeOperation.REMOVE}, options, MergeOperation.BOTH)  # type: int  # default operation is replicate remove state for non-conflicting cases (insertions/deletions)  # line 600
    res = firstOfMap({'--theirs': ConflictResolution.THEIRS, '--mine': ConflictResolution.MINE}, options, ConflictResolution.NEXT)  # type: int  # NEXT means deeper level  # line 601
    mrgline = firstOfMap({'--add-lines': MergeOperation.INSERT, '--rm-lines': MergeOperation.REMOVE}, options, mrg)  # type: int  # default operation for modified files is same as for files  # line 602
    resline = firstOfMap({'--theirs-lines': ConflictResolution.THEIRS, '--mine-lines': ConflictResolution.MINE}, options, ConflictResolution.ASK)  # type: int  # line 603
    m = Metadata(os.getcwd())  # type: Metadata  # TODO same is called inside stop on changes - could return both current and designated branch instead  # line 604
    m.loadBranches()  # line 605
    changes = None  # type: ChangeSet  # line 605
    currentBranch = m.branch  # type: _coconut.typing.Optional[int]  # line 606
    m, branch, revision, changes, strict, force, trackingPatterns = exitOnChanges(argument, options, check=False)  # don't check for current changes, only parse arguments  # line 607
    debug("Integrating changes from '%s/r%02d' into file tree..." % ((lambda _coconut_none_coalesce_item: "b%02d" % branch if _coconut_none_coalesce_item is None else _coconut_none_coalesce_item)(m.branches[branch].name), revision))  # line 608

# Determine file changes from other branch over current file tree
    m.computeSequentialPathSet(branch, revision)  # load all commits up to specified revision for branch to integrate  # line 611
    trackingUnion = trackingPatterns | m.getTrackingPatterns(branch)  # type: FrozenSet[str]  # line 612
    changes = m.findChanges(checkContent=strict, inverse=True, considerOnly=None if not m.track else trackingUnion)  # determine difference of other branch vs. file tree. "addition" means exists now but not in other, and should be removed unless in tracking mode  # line 613
    if not (mrg & MergeOperation.INSERT and changes.additions or (mrg & MergeOperation.REMOVE and changes.deletions) or changes.modifications):  # line 614
        if trackingUnion == trackingPatterns:  # nothing added  # line 615
            info("No file changes detected, but tracking patterns were merged (run 'sos switch /-1 --meta' to undo)")  # TODO write test to see if this works  # line 616
        else:  # line 617
            info("Nothing to update")  # but write back updated branch info below  # line 618
    else:  # integration required  # line 619
        for path, pinfo in changes.deletions.items():  # deletions mark files not present in current file tree -> needs additon  # line 620
            if mrg & MergeOperation.INSERT:  # deleted in current file tree: restore from branch to reach target  # line 621
                m.restoreFile(path, branch, revision, pinfo)  # deleted in current file tree: restore from branch to reach target  # line 621
            print("ADD " + path if mrg & MergeOperation.INSERT else "(A) " + path)  # line 622
        for path, pinfo in changes.additions.items():  # line 623
            if m.track or m.picky:  # because untracked files of other branch cannot be detected (which is good)  # line 624
                Exit("This should never happen")  # because untracked files of other branch cannot be detected (which is good)  # line 624
            if mrg & MergeOperation.REMOVE:  # line 625
                os.unlink(m.root + os.sep + path.replace(SLASH, os.sep))  # line 625
            print("DEL " if mrg & MergeOperation.REMOVE else "(D) " + path)  # not contained in other branch, but maybe kept  # line 626
        for path, pinfo in changes.modifications.items():  # line 627
            into = os.path.join(m.root, path.replace(SLASH, os.sep))  # type: str  # line 628
            binary = not m.isTextType(path)  # line 629
            if res & ConflictResolution.ASK or (binary and res == ConflictResolution.NEXT):  # TODO this may ask user even if no interaction was asked for (check line level for interactivity fist)  # line 630
                print(("MOD " if not binary else "BIN ") + path)  # line 631
                reso = {"i": ConflictResolution.MINE, "t": ConflictResolution.THEIRS, "m": ConflictResolution.NEXT}.get(user_input(" Resolve: *M[I]ne, [T]heirs, [M]erge: (I)").strip().lower(), ConflictResolution.MINE)  # line 632
                debug("User selected %d" % reso)  # line 633
            else:  # line 634
                reso = res  # line 634
            if reso & ConflictResolution.THEIRS:  # line 635
                m.readOrCopyVersionedFile(branch, revision, pinfo.namehash, toFile=into)  # blockwise copy of contents  # line 636
                print("THR " + path)  # line 637
            elif reso & ConflictResolution.MINE:  # line 638
                print("MNE " + path)  # nothing to do! same as skip  # line 639
            else:  # NEXT: line-based merge  # line 640
                file = m.readOrCopyVersionedFile(branch, revision, pinfo.namehash) if pinfo.size > 0 else b''  # type: _coconut.typing.Optional[bytes]  # parse lines TODO decode etc.  # line 641
                if file is not None:  # if None, error message was already logged  # line 642
                    contents = merge(file=file, intoname=into, mergeOperation=mrgline, conflictResolution=resline)  # type: bytes  # line 643
                    with open(path, "wb") as fd:  # TODO write to temp file first  # line 644
                        fd.write(contents)  # TODO write to temp file first  # line 644
    info("Integrated changes from '%s/r%02d' into file tree" % ((lambda _coconut_none_coalesce_item: "b%02d" % branch if _coconut_none_coalesce_item is None else _coconut_none_coalesce_item)(m.branches[branch].name), revision))  # line 645
    m.branches[currentBranch] = dataCopy(BranchInfo, m.branches[currentBranch], insync=False, tracked=list(trackingUnion))  # TODO really? it's a change that cannot be undone easily by the user  # line 646
    m.branch = currentBranch  # need to restore setting before saving TODO operate on different objects instead  # line 647
    m.saveBranches()  # line 648

def delete(argument: 'str', options: '_coconut.typing.Sequence[str]'=[]) -> 'None':  # line 650
    ''' Remove a branch entirely. '''  # line 651
    m, branch, revision, changes, strict, force, trackingPatterns = exitOnChanges(None, options)  # line 652
    if len(m.branches) == 1:  # line 653
        Exit("Cannot remove the only remaining branch. Use 'sos online' to leave offline mode")  # line 653
    branch, revision = m.parseRevisionString(argument)  # not from exitOnChanges, because we have to set argument to None there  # line 654
    if branch is None or branch not in m.branches:  # line 655
        Exit("Unknown branch")  # line 655
    debug("Removing branch %d%s..." % (branch, " '%s'" % m.branches[branch].name if m.branches[branch].name else ""))  # line 656
    binfo = m.removeBranch(branch)  # need to keep a reference to removed entry for output below  # line 657
    info("Branch b%02d%s removed" % (branch, " '%s'" % binfo.name if binfo.name else ""))  # line 658

def add(folder: 'str', argument: 'str', options: '_coconut.typing.Sequence[str]'=[]) -> 'None':  # line 660
    ''' Add a tracked files pattern to current branch's tracked files. '''  # line 661
    force = '--force' in options  # type: bool  # line 662
    m = Metadata(os.getcwd())  # type: Metadata  # line 663
    m.loadBranches()  # line 664
    if not m.track and not m.picky:  # line 665
        Exit("Repository is in simple mode. Needs 'offline --track' or 'offline --picky' instead")  # line 665
    relpath = os.path.relpath(os.path.dirname(os.path.abspath(os.path.join(folder, argument))), m.root)  # for tracking list  # line 666
    pattern = os.path.join(relpath, os.path.basename(argument)).replace(os.sep, SLASH)  # line 667
    if pattern in m.branches[m.branch].tracked:  # line 668
        Exit("Pattern '%s' already tracked")  # line 669
    if not force and len(fnmatch.filter(os.listdir(os.path.abspath(relpath)), os.path.basename(pattern.replace(SLASH, os.sep)))) == 0:  # doesn't match any current file  # line 670
        Exit("Pattern doesn't match any file in specified folder. Use --force to add it anyway")  # line 671
    m.branches[m.branch].tracked.append(pattern)  # TODO set insync flag to False? same for rm  # line 672
    m.saveBranches()  # line 673
    info("Added tracking pattern '%s' for folder '%s'" % (os.path.basename(pattern.replace(SLASH, os.sep)), os.path.abspath(relpath)))  # line 674

def rm(folder: 'str', argument: 'str') -> 'None':  # line 676
    ''' Remove a tracked files pattern from current branch's tracked files. '''  # line 677
    m = Metadata(os.getcwd())  # type: Metadata  # line 678
    m.loadBranches()  # line 679
    if not m.track and not m.picky:  # line 680
        Exit("Repository is in simple mode. Needs 'offline --track' or 'offline --picky' instead")  # line 680
    relpath = os.path.relpath(os.path.dirname(os.path.abspath(os.path.join(folder, argument))), m.root)  # type: str  # line 681
    pattern = os.path.join(relpath, os.path.basename(argument)).replace(os.sep, SLASH)  # type: str  # line 682
    if pattern not in m.branches[m.branch].tracked:  # line 683
        suggestion = _coconut.set()  # type: Set[str]  # line 684
        for pat in m.branches[m.branch].tracked:  # line 685
            if fnmatch.fnmatch(pattern, pat):  # line 686
                suggestion.add(pat)  # line 686
        if suggestion:  # line 687
            print("Do you mean any of the following tracked globs? '%s'" % (", ".join(sorted(suggestion))))  # line 687
        Exit("Tracked pattern '%s' not found" % pattern)  # line 688
    m.branches[m.branch].tracked.remove(pattern)  # line 689
    m.saveBranches()  # line 690
    info("Removed tracking pattern '%s' for folder '%s'" % (os.path.basename(pattern.replace(SLASH, os.sep)), os.path.abspath(relpath)))  # line 691

def ls(argument: '_coconut.typing.Optional[str]'=None) -> 'None':  # line 693
    ''' List specified directory, augmenting with repository metadata. '''  # line 694
    cwd = os.getcwd() if argument is None else argument  # type: str  # line 695
    m = Metadata(cwd)  # type: Metadata  # line 696
    m.loadBranches()  # line 697
    relpath = os.path.relpath(cwd, m.root).replace(os.sep, SLASH)  # type: str  # line 698
    files = list(sorted((entry for entry in os.listdir(cwd) if os.path.isfile(entry))))  # type: List[str]  # line 699
    trackingPatterns = m.getTrackingPatterns() if m.track or m.picky else _coconut.frozenset()  # type: FrozenSet[str]  # for current branch  # line 700
    for file in files:  # line 701
        ignore = None  # type: _coconut.typing.Optional[str]  # line 702
        for ig in m.c.ignores:  # line 703
            if fnmatch.fnmatch(file, ig):  # remember first match TODO document this  # line 704
                ignore = ig  # remember first match TODO document this  # line 704
                break  # remember first match TODO document this  # line 704
        if ig:  # line 705
            for wl in m.c.ignoresWhitelist:  # line 706
                if fnmatch.fnmatch(file, wl):  # found a white list entry for ignored file, undo ignoring it  # line 707
                    ignore = None  # found a white list entry for ignored file, undo ignoring it  # line 707
                    break  # found a white list entry for ignored file, undo ignoring it  # line 707
        if ignore is None:  # line 708
            matches = []  # type: List[str]  # line 709
            for pattern in (p for p in trackingPatterns if os.path.dirname(p) == relpath):  # only patterns matching current folder  # line 710
                if fnmatch.fnmatch(file, os.path.basename(pattern)):  # TODO or only file basename?  # line 711
                    matches.append(pattern)  # TODO or only file basename?  # line 711
        print("%s %s%s" % ("IGN" if ignore is not None else ("TRK" if len(matches) > 0 else "   "), file, ' by "%s"' % ignore if ignore is not None else (" by " + ";".join(['"%s"' % match for match in matches]) if len(matches) > 0 else "")))  # line 712

def log() -> 'None':  # line 714
    ''' List previous commits on current branch. '''  # TODO --verbose for changesets  # line 715
    m = Metadata(os.getcwd())  # type: Metadata  # line 716
    m.loadBranches()  # knows current branch  # line 717
    m.loadBranch(m.branch)  # knows commit history  # line 718
    info((lambda _coconut_none_coalesce_item: "r%02d" % m.branch if _coconut_none_coalesce_item is None else _coconut_none_coalesce_item)("/|\\ Offline commit history of branch '%s'" % m.branches[m.branch].name))  # TODO also retain "from branch/revision" on branching?  # line 719
    nl = len("%d" % max(m.commits))  # determine space needed for revision  # line 720
    changeset = m.computeSequentialPathSetIterator(m.branch, max(m.commits))  # line 721
    for no in range(max(m.commits) + 1):  # line 722
        commit = m.commits[no]  # type: CommitInfo  # line 723
        changes = next(changeset)  # type: ChangeSet  # side-effect: updates m.paths  # line 724
        print("  %s r%s @%s (+%02d/-%02d/*%02d): %s" % ("*" if commit.number == max(m.commits) else " ", ("%%%ds" % nl) % commit.number, strftime(commit.ctime), len(changes.additions), len(changes.deletions), len(changes.modifications), (lambda _coconut_none_coalesce_item: "" if _coconut_none_coalesce_item is None else _coconut_none_coalesce_item)(commit.message)))  # line 725
# TODO list number of files and if binary/text

def config(argument: 'str', options: 'List[str]'=[]) -> 'None':  # line 728
    if argument not in ["set", "unset", "show", "list", "add", "rm"]:  # line 729
        Exit("Unknown config command")  # line 729
    if not configr:  # line 730
        Exit("Cannot execute config command. 'configr' module not installed")  # line 730
    c = loadConfig()  # type: Union[configr.Configr, Accessor]  # line 731
    if argument == "set":  # line 732
        if len(options) < 2:  # line 733
            Exit("No key nor value specified")  # line 733
        if options[0] not in (["defaultbranch"] + CONFIGURABLE_FLAGS + CONFIGURABLE_LISTS):  # line 734
            Exit("Unsupported key %r" % options[0])  # line 734
        if options[0] in CONFIGURABLE_FLAGS and options[1].lower() not in TRUTH_VALUES + FALSE_VALUES:  # line 735
            Exit("Cannot set flag to '%s'. Try on/off instead" % options[1].lower())  # line 735
        c[options[0]] = options[1].lower() in TRUTH_VALUES if options[0] in CONFIGURABLE_FLAGS else (options[1].strip() if options[0] not in CONFIGURABLE_LISTS else safeSplit(options[1], ";"))  # TODO sanitize texts?  # line 736
    elif argument == "unset":  # line 737
        if len(options) < 1:  # line 738
            Exit("No key specified")  # line 738
        if options[0] not in c.keys():  # line 739
            Exit("Unknown key")  # line 739
        del c[options[0]]  # line 740
    elif argument == "add":  # line 741
        if len(options) < 2:  # line 742
            Exit("No key nor value specified")  # line 742
        if options[0] not in CONFIGURABLE_LISTS:  # line 743
            Exit("Unsupported key for add %r" % options[0])  # line 743
        if options[0] not in c.keys():  # add list  # line 744
            c[options[0]] = [options[1]]  # add list  # line 744
        elif options[1] in c[options[0]]:  # line 745
            Exit("Value already contained")  # line 745
        c[options[0]].append(options[1])  # line 746
    elif argument == "rm":  # line 747
        if len(options) < 2:  # line 748
            Exit("No key nor value specified")  # line 748
        if options[0] not in c.keys():  # line 749
            Exit("Unknown key specified: %r" % options[0])  # line 749
        if options[1] not in c[options[0]]:  # line 750
            Exit("Unknown value: %r" % options[1])  # line 750
        c[options[0]].remove(options[1])  # line 751
    else:  # Show  # line 752
        for k, v in sorted(c.items()):  # line 753
            print("%s => %r" % (k, v))  # line 753
        return  # line 754
    f, g = saveConfig(c)  # line 755
    if f is None:  # line 756
        error("Error saving user configuration: %r" % g)  # line 756

def parse(root: 'str', inFolder: 'str'):  # line 758
    ''' Main operation. '''  # line 759
    debug("Parsing command-line arguments...")  # line 760
    command = sys.argv[1].strip() if len(sys.argv) > 1 else ""  # line 761
    argument = sys.argv[2].strip() if len(sys.argv) > 2 else None  # line 762
    options = sys.argv[3:] if command == "config" else [c for c in sys.argv[2:] if c.startswith("--")]  # consider second parameter for no-arg command, otherwise from third on  # line 763
    debug("Processing command %r with argument '%s' and options %r." % ("" if command is None else command, "" if argument is None else argument, options))  # line 764
    if command[:1] == "a":  # line 765
        add(inFolder, argument, options)  # line 765
    elif command[:1] == "b":  # line 766
        branch(argument, options)  # line 766
    elif command[:2] == "ch":  # line 767
        changes(argument, options)  # line 767
    elif command[:3] == "com" or command[:2] == "ci":  # line 768
        commit(argument, options)  # line 768
    elif command[:3] == 'con':  # line 769
        config(argument, options)  # line 769
    elif command[:2] == "de":  # line 770
        delete(argument, options)  # line 770
    elif command[:2] == "di":  # line 771
        diff(argument, options)  # line 771
    elif command[:1] == "h":  # line 772
        usage()  # line 772
    elif command[:2] == "lo":  # line 773
        log()  # line 773
    elif command[:2] in ["li", "ls"]:  # line 774
        ls(argument)  # line 774
    elif command[:2] == "of":  # line 775
        offline(argument, options)  # line 775
    elif command[:2] == "on":  # line 776
        online(options)  # line 776
    elif command[:1] == "r":  # line 777
        rm(inFolder, argument)  # line 777
    elif command[:2] == "st":  # line 778
        status()  # line 778
    elif command[:2] == "sw":  # line 779
        switch(argument, options)  # line 779
    elif command[:2] == "u":  # line 780
        update(argument, options)  # line 780
    else:  # line 781
        Exit("Unknown command '%s'" % command)  # line 781
    sys.exit(0)  # line 782

def main() -> 'None':  # line 784
    global debug, info, warn, error  # line 785
    logging.basicConfig(level=level, stream=sys.stderr, format=("%(asctime)-23s %(levelname)-8s %(name)s:%(lineno)d | %(message)s" if '--log' in sys.argv else "%(message)s"))  # line 786
    _log = Logger(logging.getLogger(__name__))  # line 787
    debug, info, warn, error = _log.debug, _log.info, _log.warn, _log.error  # line 787
    for option in (o for o in ['--log', '--verbose', '-v', '--sos'] if o in sys.argv):  # clean up program arguments  # line 788
        sys.argv.remove(option)  # clean up program arguments  # line 788
    if '--help' in sys.argv or len(sys.argv) < 2:  # line 789
        usage()  # line 789
        Exit()  # line 789
    command = sys.argv[1] if len(sys.argv) > 1 else None  # type: _coconut.typing.Optional[str]  # line 790
    root, vcs, cmd = findSosVcsBase()  # root is None if no .sos folder exists up the folder tree (still working online); vcs is checkout/repo root folder; cmd is the VCS base command  # line 791
    debug("Found root folders for SOS|VCS: %s|%s" % ("" if root is None else root, "" if vcs is None else vcs))  # line 792
    defaults["defaultbranch"] = vcsBranches.get(cmd, "trunk")  # sets dynamic default with SVN fallback  # line 793
    if force_sos or root is not None or ("" if command is None else command)[:2] == "of" or ("" if command is None else command)[:1] == "h":  # in offline mode or just going offline TODO what about git config?  # line 794
        cwd = os.getcwd()  # line 795
        os.chdir(cwd if command[:2] == "of" else cwd if root is None else root)  # line 796
        parse(root, cwd)  # line 797
    elif cmd is not None:  # online mode - delegate to VCS  # line 798
        info("SOS: Running '%s %s'" % (cmd, " ".join(sys.argv[1:])))  # line 799
        import subprocess  # only requuired in this section  # line 800
        process = subprocess.Popen([cmd] + sys.argv[1:], shell=False, stdin=subprocess.PIPE, stdout=sys.stdout, stderr=sys.stderr)  # line 801
        inp = ""  # type: str  # line 802
        while True:  # line 803
            so, se = process.communicate(input=inp)  # line 804
            if process.returncode is not None:  # line 805
                break  # line 805
            inp = sys.stdin.read()  # line 806
        if sys.argv[1][:2] == "co" and process.returncode == 0:  # successful commit - assume now in sync again (but leave meta data folder with potential other feature branches behind until "online")  # line 807
            if root is None:  # line 808
                Exit("Cannot determine VCS root folder: Unable to mark repository as synchronized and will show a warning when leaving offline mode")  # line 808
            m = Metadata(root)  # line 809
            m.loadBranches()  # read repo  # line 810
            m.branches[m.branch] = dataCopy(BranchInfo, m.branches[m.branch], insync=True)  # mark as committed  # line 811
            m.saveBranches()  # line 812
    else:  # line 813
        Exit("No offline repository present, and unable to detect VCS file tree")  # line 813


# Main part
level = logging.DEBUG if os.environ.get("DEBUG", "False").lower() == "true" or '--verbose' in sys.argv or '-v' in sys.argv else logging.INFO  # line 817
force_sos = '--sos' in sys.argv  # line 818
_log = Logger(logging.getLogger(__name__))  # line 819
debug, info, warn, error = _log.debug, _log.info, _log.warn, _log.error  # line 819
if __name__ == '__main__':  # line 820
    main()  # line 820
