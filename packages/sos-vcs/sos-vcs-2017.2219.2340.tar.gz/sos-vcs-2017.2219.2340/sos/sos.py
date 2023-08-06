#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# __coconut_hash__ = 0xe6fdd6b5

# Compiled with Coconut version 1.3.1-post_dev8 [Dead Parrot]

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


# Constants
APPNAME = "Subversion Offline Solution  V%s  (C) Arne Bachmann" % version.__release_version__  # type: str  # line 21
defaults = Accessor({"strict": False, "track": False, "picky": False, "compress": True, "tags": [], "texttype": [], "bintype": [], "ignoreDirs": [".*", "__pycache__"], "ignoreDirsWhitelist": [], "ignores": ["__coconut__.py", "*.bak", "*.py[cdo]", "*.class", ".fslckout"], "ignoresWhitelist": []})  # line 22
termWidth = getTermWidth() - 1  # uses curses or returns conservative default of 80  # line 23


# Functions
def loadConfig() -> 'Union[configr.Configr, Accessor]':  # Simplifies loading config from file system or returning the defaults  # line 27
    config = None  # type: Union[configr.Configr, Accessor]  # line 28
    if not configr:  # this only applies for the case that configr is not available, thus no settings will be persisted anyway  # line 29
        return defaults  # this only applies for the case that configr is not available, thus no settings will be persisted anyway  # line 29
    config = configr.Configr("sos", defaults=defaults)  # defaults are used if key is not configured, but won't be saved  # line 30
    f, g = config.loadSettings(clientCodeLocation=os.path.abspath(__file__), location=os.environ.get("TEST", None))  # line 31
    if f is None:  # line 32
        debug("Encountered a problem while loading the user configuration: %r" % g)  # line 32
    return config  # line 33

@_coconut_tco  # line 35
def saveConfig(c: 'configr.Configr') -> 'Tuple[_coconut.typing.Optional[str], _coconut.typing.Optional[Exception]]':  # line 35
    return _coconut_tail_call(c.saveSettings, clientCodeLocation=os.path.abspath(__file__), location=os.environ.get("TEST", None))  # line 36

def usage() -> 'None':  # line 38
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
        _.tags = []  # type: List[str]  # line 109
        _.branch = None  # type: _coconut.typing.Optional[int]  # current branch number  # line 110
        _.commit = None  # type: _coconut.typing.Optional[int]  # current revision number  # line 111
        _.track = _.c.track  # type: bool  # track file name patterns in the repository (per branch)  # line 112
        _.picky = _.c.picky  # type: bool  # pick files to commit per operation  # line 113
        _.strict = _.c.strict  # type: bool  # be always strict (regarding file contents comparsion)  # line 114
        _.compress = _.c.compress  # type: bool  # these flags are stored in the repository  # line 115

    def isTextType(_, filename: 'str') -> 'bool':  # line 117
        return (((lambda _coconut_none_coalesce_item: "" if _coconut_none_coalesce_item is None else _coconut_none_coalesce_item)(mimetypes.guess_type(filename)[0])).startswith("text/") or any([fnmatch.fnmatch(filename, pattern) for pattern in _.c.texttype])) and not any([fnmatch.fnmatch(filename, pattern) for pattern in _.c.bintype])  # line 117

    def listChanges(_, changes: 'ChangeSet') -> 'None':  # line 119
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
            _.tags = flags["tags"]  # list of commit messages to treat as globally unique tags  # line 130
            _.branch = flags["branch"]  # current branch integer  # line 131
            _.track = flags["track"]  # line 132
            _.picky = flags["picky"]  # line 133
            _.strict = flags["strict"]  # line 134
            _.compress = flags["compress"]  # line 135
            _.branches = {i.number: i for i in (BranchInfo(*item) for item in branches)}  # re-create type info  # line 136
        except Exception as E:  # if not found, create metadata folder  # line 137
            _.branches = {}  # line 138
            warn("Couldn't read branches metadata: %r" % E)  # line 139

    def saveBranches(_) -> 'None':  # line 141
        ''' Save list of branches and current branch info to metadata file. '''  # line 142
        with codecs.open(os.path.join(_.root, metaFolder, metaFile), "w", encoding=UTF8) as fd:  # line 143
            json.dump(({"tags": _.tags, "branch": _.branch, "track": _.track, "picky": _.picky, "strict": _.strict, "compress": _.compress}, list(_.branches.values())), fd, ensure_ascii=False)  # line 144

    def getRevisionByName(_, name: 'str') -> '_coconut.typing.Optional[int]':  # line 146
        ''' Convenience accessor for named revisions (using commit message as name). '''  # line 147
        if name == "":  # line 148
            return -1  # line 148
        try:  # attempt to parse integer string  # line 149
            return longint(name)  # attempt to parse integer string  # line 149
        except ValueError:  # line 150
            pass  # line 150
        found = [number for number, commit in _.commits.items() if name == commit.message]  # line 151
        return found[0] if found else None  # line 152

    def getBranchByName(_, name: 'str') -> '_coconut.typing.Optional[int]':  # line 154
        ''' Convenience accessor for named branches. '''  # line 155
        if name == "":  # line 156
            return _.branch  # line 156
        try:  # attempt to parse integer string  # line 157
            return longint(name)  # attempt to parse integer string  # line 157
        except ValueError:  # line 158
            pass  # line 158
        found = [number for number, branch in _.branches.items() if name == branch.name]  # line 159
        return found[0] if found else None  # line 160

    def loadBranch(_, branch: 'int') -> 'None':  # line 162
        ''' Load all commit information from a branch meta data file. '''  # line 163
        with codecs.open(os.path.join(_.root, metaFolder, "b%d" % branch, metaFile), "r", encoding=UTF8) as fd:  # line 164
            commits = json.load(fd)  # type: List[List[Any]]  # list of CommitInfo that needs to be unmarshalled into value types  # line 165
        _.commits = {i.number: i for i in (CommitInfo(*item) for item in commits)}  # re-create type info  # line 166
        _.branch = branch  # line 167

    def saveBranch(_, branch: 'int') -> 'None':  # line 169
        ''' Save all commit information to a branch meta data file. '''  # line 170
        with codecs.open(os.path.join(_.root, metaFolder, "b%d" % branch, metaFile), "w", encoding=UTF8) as fd:  # line 171
            json.dump(list(_.commits.values()), fd, ensure_ascii=False)  # line 172

    def duplicateBranch(_, branch: 'int', name: '_coconut.typing.Optional[str]') -> 'None':  # line 174
        ''' Create branch from an existing branch/revision. WARN: Caller must have loaded branches information.
        branch: target branch (should not exist yet)
        name: optional name of new branch
        _.branch: current branch
    '''  # line 179
        debug("Duplicating branch '%s' to '%d'..." % ((lambda _coconut_none_coalesce_item: "b%d" % _.branch if _coconut_none_coalesce_item is None else _coconut_none_coalesce_item)(_.branches[_.branch].name), branch))  # line 180
        tracked = [t for t in _.branches[_.branch].tracked]  # copy  # line 181
        os.makedirs(os.path.join(_.root, metaFolder, "b%d" % branch, "r0"))  # line 182
        _.loadBranch(_.branch)  # line 183
        revision = max(_.commits)  # type: int  # line 184
        _.computeSequentialPathSet(_.branch, revision)  # full set of files in revision to _.paths  # line 185
        for path, pinfo in _.paths.items():  # line 186
            _.copyVersionedFile(_.branch, revision, branch, 0, pinfo)  # line 187
        _.commits = {0: CommitInfo(0, longint(time.time() * 1000), "Branched from '%s'" % ((lambda _coconut_none_coalesce_item: "b%d" % _.branch if _coconut_none_coalesce_item is None else _coconut_none_coalesce_item)(_.branches[_.branch].name)))}  # store initial commit  # line 188
        _.saveBranch(branch)  # save branch meta data to branch folder  # line 189
        _.saveCommit(branch, 0)  # save commit meta data to revision folder  # line 190
        _.branches[branch] = BranchInfo(branch, _.commits[0].ctime, name, _.branches[_.branch].insync, tracked)  # save branch info, before storing repo state at caller  # line 191

    def createBranch(_, branch: 'int', name: '_coconut.typing.Optional[str]'=None, initialMessage: '_coconut.typing.Optional[str]'=None):  # line 193
        ''' Create a new branch from current file tree. This clears all known commits and modifies the file system.
        branch: target branch (should not exist yet)
        name: optional name of new branch
        _.branch: current branch, must exist already
    '''  # line 198
        simpleMode = not (_.track or _.picky)  # line 199
        tracked = [t for t in _.branches[_.branch].tracked] if _.track and len(_.branches) > 0 else []  # in case of initial branch creation  # line 200
        debug((lambda _coconut_none_coalesce_item: "b%d" % branch if _coconut_none_coalesce_item is None else _coconut_none_coalesce_item)("Creating branch '%s'..." % name))  # line 201
        _.paths = {}  # type: Dict[str, PathInfo]  # line 202
        if simpleMode:  # branches from file system state  # line 203
            changes = _.findChanges(branch, 0, progress=simpleMode)  # type: ChangeSet  # creates revision folder and versioned files  # line 204
            _.listChanges(changes)  # line 205
            _.paths.update(changes.additions.items())  # line 206
        else:  # tracking or picky mode: branch from lastest revision  # line 207
            os.makedirs(os.path.join(_.root, metaFolder, "b%d" % branch, "r0"))  # line 208
            if _.branch is not None:  # not immediately after "offline" - copy files from current branch  # line 209
                _.loadBranch(_.branch)  # line 210
                revision = max(_.commits)  # type: int  # TODO what if last switch was to an earlier revision? no persisting of last checkout  # line 211
                _.computeSequentialPathSet(_.branch, revision)  # full set of files in revision to _.paths  # line 212
                for path, pinfo in _.paths.items():  # line 213
                    _.copyVersionedFile(_.branch, revision, branch, 0, pinfo)  # line 214
        ts = longint(time.time() * 1000)  # line 215
        _.commits = {0: CommitInfo(0, ts, "Branched on %s" % strftime(ts) if initialMessage is None else initialMessage)}  # store initial commit for new branch  # line 216
        _.saveBranch(branch)  # save branch meta data (revisions) to branch folder  # line 217
        _.saveCommit(branch, 0)  # save commit meta data to revision folder  # line 218
        _.branches[branch] = BranchInfo(branch, _.commits[0].ctime, name, True if len(_.branches) == 0 else _.branches[_.branch].insync, tracked)  # save branch info, in case it is needed  # line 219

    def removeBranch(_, branch: 'int') -> 'BranchInfo':  # line 221
        ''' Entirely remove a branch and all its revisions from the file system. '''  # line 222
        shutil.rmtree(os.path.join(_.root, metaFolder, "b%d" % branch))  # line 223
        binfo = _.branches[branch]  # line 224
        del _.branches[branch]  # line 225
        _.branch = max(_.branches)  # line 226
        _.saveBranches()  # line 227
        _.commits.clear()  # line 228
        return binfo  # line 229

    def loadCommit(_, branch: 'int', revision: 'int') -> 'None':  # line 231
        ''' Load all file information from a commit meta data. '''  # line 232
        with codecs.open(os.path.join(_.root, metaFolder, "b%d" % branch, "r%d" % revision, metaFile), "r", encoding=UTF8) as fd:  # line 233
            _.paths = json.load(fd)  # line 234
        _.paths = {path: PathInfo(*item) for path, item in _.paths.items()}  # re-create type info  # line 235
        _.branch = branch  # line 236

    def saveCommit(_, branch: 'int', revision: 'int'):  # line 238
        ''' Save all file information to a commit meta data file. '''  # line 239
        target = os.path.join(_.root, metaFolder, "b%d" % branch, "r%d" % revision)  # line 240
        try:  # line 241
            os.makedirs(target)  # line 241
        except:  # line 242
            pass  # line 242
        with codecs.open(os.path.join(target, metaFile), "w", encoding=UTF8) as fd:  # line 243
            json.dump(_.paths, fd, ensure_ascii=False)  # line 244

    def findChanges(_, branch: '_coconut.typing.Optional[int]'=None, revision: '_coconut.typing.Optional[int]'=None, checkContent: 'bool'=False, inverse: 'bool'=False, considerOnly: '_coconut.typing.Optional[FrozenSet[str]]'=None, progress: 'bool'=False) -> 'ChangeSet':  # line 246
        ''' Find changes on the file system vs. in-memory paths (which should reflect the latest commit state).
        Only if both branch and revision are *not* None, write modified/added files to the specified revision folder (thus creating a new revision)
        The function returns the state of file tree *differences*, unless "inverse" is True -> then return original data
        checkContent: also computes file content hashes
        inverse: retain original state (size, mtime, hash) instead of updated one
        considerOnly: set of tracking patterns. For update operation, union of other and current branch
        progress: Show file names during processing
    '''  # line 254
        write = branch is not None and revision is not None  # line 255
        if write:  # line 256
            os.makedirs(os.path.join(_.root, metaFolder, "b%d" % branch, "r%d" % revision))  # line 256
        changes = ChangeSet({}, {}, {})  # type: ChangeSet  # line 257
        counter = Counter(-1)  # type: Counter  # line 258
        timer = time.time()  # line 258
        hashed = None  # type: _coconut.typing.Optional[str]  # line 259
        written = None  # type: longint  # line 259
        compressed = 0  # type: longint  # line 259
        original = 0  # type: longint  # line 259
        for path, dirnames, filenames in os.walk(_.root):  # line 260
            dirnames[:] = [f for f in dirnames if len([n for n in _.c.ignoreDirs if fnmatch.fnmatch(f, n)]) == 0 or len([p for p in _.c.ignoreDirsWhitelist if fnmatch.fnmatch(f, p)]) > 0]  # line 261
            filenames[:] = [f for f in filenames if len([n for n in _.c.ignores if fnmatch.fnmatch(f, n)]) == 0 or len([p for p in _.c.ignoresWhitelist if fnmatch.fnmatch(f, p)]) > 0]  # line 262
            dirnames.sort()  # line 263
            filenames.sort()  # line 263
            relpath = os.path.relpath(path, _.root).replace(os.sep, SLASH)  # line 264
            for file in (filenames if considerOnly is None else list(reduce(lambda last, pattern: last | set(fnmatch.filter(filenames, os.path.basename(pattern))), (p for p in considerOnly if os.path.dirname(p) == relpath), _coconut.set()))):  # if m.track or m.picky: only files that match any path-relevant tracking patterns  # line 265
                filename = relpath + SLASH + file  # line 266
                filepath = os.path.join(path, file)  # line 267
                stat = os.stat(filepath)  # line 268
                size, mtime, newtime = stat.st_size, longint(stat.st_mtime * 1000), time.time()  # line 269
                if progress and newtime - timer > .1:  # line 270
                    outstring = "\rPreparing %s  %s" % (PROGRESS_MARKER[counter.inc() % 4], filename)  # line 271
                    sys.stdout.write(outstring + " " * max(0, termWidth - len(outstring)))  # TODO could write to new line instead of carriage return, also needs terminal width  # line 272
                    sys.stdout.flush()  # TODO could write to new line instead of carriage return, also needs terminal width  # line 272
                    timer = newtime  # TODO could write to new line instead of carriage return, also needs terminal width  # line 272
                if filename not in _.paths:  # detected file not present (or untracked) in other branch  # line 273
                    namehash = hashStr(filename)  # line 274
                    hashed, written = hashFile(filepath, _.compress, saveTo=os.path.join(_.root, metaFolder, "b%d" % branch, "r%d" % revision, namehash) if write else None) if size > 0 else (None, 0)  # line 275
                    changes.additions[filename] = PathInfo(namehash, size, mtime, hashed)  # line 276
                    compressed += written  # line 277
                    original += size  # line 277
                    continue  # line 278
                last = _.paths[filename]  # filename is known - check for modifications  # line 279
                if last.size is None:  # was removed before but is now added back - does not apply for tracking mode (which never marks files for removal in the history)  # line 280
                    hashed, written = hashFile(filepath, _.compress, saveTo=os.path.join(_.root, metaFolder, "b%d" % branch, "r%d" % revision, last.namehash) if write else None) if size > 0 else (None, 0)  # line 281
                    changes.additions[filename] = PathInfo(last.namehash, size, mtime, hashed)  # line 282
                    continue  # line 282
                elif size != last.size or mtime != last.mtime or (checkContent and hashFile(filepath, _.compress) != last.hash):  # detected a modification  # line 283
                    hashed, written = hashFile(filepath, _.compress, saveTo=os.path.join(_.root, metaFolder, "b%d" % branch, "r%d" % revision, last.namehash) if write else None) if (last.size if inverse else size) > 0 else (last.hash if inverse else None, 0)  # line 284
                    changes.modifications[filename] = PathInfo(last.namehash, last.size if inverse else size, last.mtime if inverse else mtime, hashed)  # line 285
                else:  # line 286
                    continue  # line 286
                compressed += written  # line 287
                original += last.size if inverse else size  # line 287
# Detect deletions. Files no longer being tracked should not be found here
            for folderPath in (p for p, pinfo in _.paths.items() if p[:p.rindex(SLASH)] == relpath and pinfo.size is not None):  # only versioned (and tracked) files that match currently visited folder. TODO don't check for removal just added entries  # line 289
                if folderPath[len(relpath) + 1:] not in filenames:  # filename no longer in file tree TODO use basename and dirname instead of slicing?  # line 290
                    changes.deletions[folderPath] = _.paths[folderPath]  # filename no longer in file tree TODO use basename and dirname instead of slicing?  # line 290
        if progress:  # force new line  # line 291
            print("\rPreparation finished. Compression factor %s" % ("is %.1f" % (original * 100. / compressed) if compressed > 0 else "cannot be computed").ljust(termWidth), file=sys.stdout)  # force new line  # line 291
        else:  # line 292
            debug("Finished detecting changes. Compression factor %s" % ("is %.1f" % (original * 100. / compressed) if compressed > 0 else "cannot be computed"))  # line 292
        return changes  # line 293

    def integrateChangeset(_, changes: 'ChangeSet', clear=False) -> 'None':  # line 295
        ''' In-memory update from a changeset, marking deleted files with size=None. Use clear = True to start on an empty path set. '''  # line 296
        if clear:  # line 297
            _.paths.clear()  # line 297
        else:  # line 298
            rm = [p for p, info in _.paths.items() if info.size is None]  # remove files deleted in earlier change sets (revisions)  # line 299
            for old in rm:  # remove previously removed entries completely  # line 300
                del _.paths[old]  # remove previously removed entries completely  # line 300
        for d, info in changes.deletions.items():  # mark now removed entries as deleted  # line 301
            _.paths[d] = PathInfo(info.namehash, None, info.mtime, None)  # mark now removed entries as deleted  # line 301
        _.paths.update(changes.additions)  # line 302
        _.paths.update(changes.modifications)  # line 303

    def computeSequentialPathSet(_, branch: 'int', revision: 'int') -> 'None':  # line 305
        next(_.computeSequentialPathSetIterator(branch, revision, incrementally=False))  # simply invoke the generator once  # line 306

    def computeSequentialPathSetIterator(_, branch: 'int', revision: 'int', incrementally: 'bool'=True) -> '_coconut.typing.Optional[Iterator[ChangeSet]]':  # line 308
        ''' In-memory computation of current list of valid PathInfo entries for specified branch and until specified revision (inclusively) by traversing revision on the file system. '''  # line 309
        _.loadCommit(branch, 0)  # load initial paths  # line 310
        if incrementally:  # line 311
            yield diffPathSets({}, _.paths)  # line 311
        n = Metadata(_.root)  # type: Metadata  # next changes  # line 312
        for revision in range(1, revision + 1):  # line 313
            n.loadCommit(branch, revision)  # line 314
            changes = diffPathSets(_.paths, n.paths)  # type: ChangeSet  # line 315
            _.integrateChangeset(changes)  # line 316
            if incrementally:  # line 317
                yield changes  # line 317
        yield None  # for the default case - not incrementally  # line 318

    def parseRevisionString(_, argument: 'str') -> 'Tuple[_coconut.typing.Optional[int], _coconut.typing.Optional[int]]':  # line 320
        ''' Commit identifiers can be str or int for branch, and int for revision.
        Revision identifiers can be negative, with -1 being last commit.
    '''  # line 323
        if argument is None or argument == SLASH:  # no branch/revision specified  # line 324
            return (_.branch, -1)  # no branch/revision specified  # line 324
        argument = argument.strip()  # line 325
        if argument.startswith(SLASH):  # current branch  # line 326
            return (_.branch, _.getRevisionByName(argument[1:]))  # current branch  # line 326
        if argument.endswith(SLASH):  # line 327
            try:  # line 328
                return (_.getBranchByName(argument[:-1]), -1)  # line 328
            except ValueError:  # line 329
                Exit("Unknown branch label")  # line 329
        if SLASH in argument:  # line 330
            b, r = argument.split(SLASH)[:2]  # line 331
            try:  # line 332
                return (_.getBranchByName(b), _.getRevisionByName(r))  # line 332
            except ValueError:  # line 333
                Exit("Unknown branch label or wrong number format")  # line 333
        branch = _.getBranchByName(argument)  # type: int  # returns number if given (revision) integer  # line 334
        if branch not in _.branches:  # line 335
            branch = None  # line 335
        try:  # either branch name/number or reverse/absolute revision number  # line 336
            return (_.branch if branch is None else branch, longint(argument) if branch is None else -1)  # either branch name/number or reverse/absolute revision number  # line 336
        except:  # line 337
            Exit("Unknown branch label or wrong number format")  # line 337
        return (None, None)  # should never be reached TODO raise exception instead?  # line 338

    def findRevision(_, branch: 'int', revision: 'int', namehash: 'str') -> 'Tuple[int, str]':  # line 340
        while True:  # find latest revision that contained the file physically  # line 341
            source = os.path.join(_.root, metaFolder, "b%d" % branch, "r%d" % revision, namehash)  # type: str  # line 342
            if os.path.exists(source) and os.path.isfile(source):  # line 343
                break  # line 343
            revision -= 1  # line 344
            if revision < 0:  # line 345
                Exit("Cannot determine versioned file '%s' from specified branch '%d'" % (namehash, branch))  # line 345
        return revision, source  # line 346

    def copyVersionedFile(_, branch: 'int', revision: 'int', tobranch: 'int', torevision: 'int', pinfo: 'PathInfo') -> 'None':  # line 348
        ''' Copy versioned file to other branch/revision. '''  # line 349
        target = os.path.join(_.root, metaFolder, "b%d" % tobranch, "r%d" % torevision, pinfo.namehash)  # type: str  # line 350
        revision, source = _.findRevision(branch, revision, pinfo.namehash)  # line 351
        shutil.copy2(source, target)  # line 352

    def readOrCopyVersionedFile(_, branch: 'int', revision: 'int', namehash: 'str', toFile: '_coconut.typing.Optional[str]'=None) -> '_coconut.typing.Optional[bytes]':  # line 354
        ''' Return file contents, or copy contents into file path provided. '''  # line 355
        source = os.path.join(_.root, metaFolder, "b%d" % branch, "r%d" % revision, namehash)  # type: str  # line 356
        try:  # line 357
            with openIt(source, "r", _.compress) as fd:  # line 358
                if toFile is None:  # read bytes into memory and return  # line 359
                    return fd.read()  # read bytes into memory and return  # line 359
                with open(toFile, "wb") as to:  # line 360
                    while True:  # line 361
                        buffer = fd.read(bufSize)  # line 362
                        to.write(buffer)  # line 363
                        if len(buffer) < bufSize:  # line 364
                            break  # line 364
                    return None  # line 365
        except Exception as E:  # line 366
            warn("Cannot read versioned file: %r (%d/%d/%s)" % (E, branch, revision, namehash))  # line 366
        return None  # line 367

    def restoreFile(_, relpath: '_coconut.typing.Optional[str]', branch: 'int', revision: 'int', pinfo: 'PathInfo') -> '_coconut.typing.Optional[bytes]':  # line 369
        ''' Recreate file for given revision, or return contents if path is None. '''  # line 370
        if relpath is None:  # just return contents  # line 371
            return _.readOrCopyVersionedFile(branch, _.findRevision(branch, revision, pinfo.namehash)[0], pinfo.namehash) if pinfo.size > 0 else b''  # just return contents  # line 371
        target = os.path.join(_.root, relpath.replace(SLASH, os.sep))  # type: str  # line 372
        if pinfo.size == 0:  # line 373
            with open(target, "wb"):  # line 374
                pass  # line 374
            try:  # update access/modification timestamps on file system  # line 375
                os.utime(target, (-1, pinfo.mtime / 1000.))  # update access/modification timestamps on file system  # line 375
            except Exception as E:  # line 376
                error("Cannot update file's timestamp after restoration '%r'" % E)  # line 376
            return None  # line 377
        revision, source = _.findRevision(branch, revision, pinfo.namehash)  # line 378
# Restore file by copying buffer-wise
        with openIt(source, "r", _.compress) as fd, open(target, "wb") as to:  # using Coconut's Enhanced Parenthetical Continuation  # line 380
            while True:  # line 381
                buffer = fd.read(bufSize)  # line 382
                to.write(buffer)  # line 383
                if len(buffer) < bufSize:  # line 384
                    break  # line 384
        try:  # update access/modification timestamps on file system  # line 385
            os.utime(target, (-1, pinfo.mtime / 1000.))  # update access/modification timestamps on file system  # line 385
        except Exception as E:  # line 386
            error("Cannot update file's timestamp after restoration '%r'" % E)  # line 386
        return None  # line 387

    def getTrackingPatterns(_, branch: '_coconut.typing.Optional[int]'=None) -> 'FrozenSet[str]':  # line 389
        ''' Returns list of tracking patterns for provided branch or current branch. '''  # line 390
        return _coconut.frozenset() if not _.track and not _.picky else frozenset(_.branches[_.branch if branch is None else branch].tracked)  # line 391


# Main client operations
def offline(argument: '_coconut.typing.Optional[str]'=None, options: '_coconut.typing.Sequence[str]'=[]) -> 'None':  # line 395
    ''' Initial command to start working offline. '''  # line 396
    if os.path.exists(metaFolder):  # line 397
        if '--force' not in options:  # line 398
            Exit("Repository folder is either already offline or older branches and commits were left over.\nUse 'sos online' to check for dirty branches, or\nWipe existing offline branches with 'sos offline --force'")  # line 398
        try:  # line 399
            for entry in os.listdir(metaFolder):  # line 400
                resource = metaFolder + os.sep + entry  # line 401
                if os.path.isdir(resource):  # line 402
                    shutil.rmtree(resource)  # line 402
                else:  # line 403
                    os.unlink(resource)  # line 403
        except:  # line 404
            Exit("Cannot reliably remove previous repository contents. Please remove .sos folder manually prior to going offline")  # line 404
    m = Metadata(os.getcwd())  # type: Metadata  # line 405
    if '--plain' in options or not m.c.compress:  # plain file copies instead of compressed ones  # line 406
        m.compress = False  # plain file copies instead of compressed ones  # line 406
    if '--picky' in options or m.c.picky:  # Git-like  # line 407
        m.picky = True  # Git-like  # line 407
    elif '--track' in options or m.c.track:  # Svn-like  # line 408
        m.track = True  # Svn-like  # line 408
    if '--strict' in options or m.c.strict:  # always hash contents  # line 409
        m.strict = True  # always hash contents  # line 409
    debug("Preparing offline repository...")  # line 410
    m.createBranch(0, str(defaults["defaultbranch"]) if argument is None else argument, initialMessage="Offline repository created on %s" % strftime())  # main branch's name may be None (e.g. for fossil)  # line 411
    m.branch = 0  # line 412
    m.saveBranches()  # no change immediately after going offline, going back online won't issue a warning  # line 413
    info("Offline repository prepared. Use 'sos online' to finish offline work")  # line 414

def online(options: '_coconut.typing.Sequence[str]'=[]) -> 'None':  # line 416
    ''' Finish working offline. '''  # line 417
    force = '--force' in options  # type: bool  # line 418
    m = Metadata(os.getcwd())  # line 419
    m.loadBranches()  # line 420
    if any([not b.insync for b in m.branches.values()]) and not force:  # line 421
        Exit("There are still unsynchronized (dirty) branches.\nUse 'sos log' to list them.\nUse 'sos commit' and 'sos switch' to commit dirty branches to your VCS before leaving offline mode.\nUse 'sos online --force' to erase all aggregated offline revisions.")  # line 421
    strict = '--strict' in options or m.strict  # type: bool  # line 422
    if options.count("--force") < 2:  # line 423
        changes = m.findChanges(checkContent=strict, considerOnly=None if not m.track else m.getTrackingPatterns())  # type: ChangeSet  # line 424
        if modified(changes):  # line 425
            Exit("File tree is modified vs. current branch.\nUse 'sos online --force --force' to continue with removing the offline repository.")  # line 425
    try:  # line 426
        shutil.rmtree(metaFolder)  # line 426
        info("Exited offline mode. Continue working with your traditional VCS.")  # line 426
    except Exception as E:  # line 427
        Exit("Error removing offline repository: %r" % E)  # line 427

def branch(argument: '_coconut.typing.Optional[str]'=None, options: '_coconut.typing.Sequence[str]'=[]) -> 'None':  # line 429
    ''' Create a new branch (from file tree or last revision) and (by default) continue working on it. '''  # line 430
    last = '--last' in options  # type: bool  # use last revision for branching, not current file tree  # line 431
    stay = '--stay' in options  # type: bool  # continue on current branch after branching  # line 432
    force = '--force' in options  # type: bool  # branch even with local modifications  # line 433
    m = Metadata(os.getcwd())  # type: Metadata  # line 434
    m.loadBranches()  # line 435
    if argument and m.getBranchByName(argument) is not None:  # create a named branch  # line 436
        Exit("Branch '%s' already exists. Cannot proceed" % argument)  # create a named branch  # line 436
    branch = max(m.branches.keys()) + 1  # next branch's key - this isn't atomic but we assume single-user non-concurrent use here  # line 437
    debug("Branching to %sbranch b%02d%s%s..." % ("unnamed " if argument is None else "", branch, " '%s'" % argument if argument else "", " from last revision" if last else ""))  # line 438
    if last:  # line 439
        m.duplicateBranch(branch, argument)  # branch from branch's last revision  # line 440
    else:  # from file tree state  # line 441
        m.createBranch(branch, argument)  # branch from current file tree  # line 442
    if not stay:  # line 443
        m.branch = branch  # line 444
        m.saveBranches()  # line 445
    info("%s new %sbranch b%02d%s" % ("Continue work after branching" if stay else "Switched to", "unnamed " if argument is None else "", branch, " '%s'" % argument if argument else ""))  # line 446

def changes(argument: 'str'=None, options: '_coconut.typing.Sequence[str]'=[]) -> 'ChangeSet':  # line 448
    ''' Show changes of file tree vs. (last or specified) revision on current or specified branch. '''  # line 449
    m = Metadata(os.getcwd())  # type: Metadata  # line 450
    branch = None  # type: _coconut.typing.Optional[int]  # line 450
    revision = None  # type: _coconut.typing.Optional[int]  # line 450
    m.loadBranches()  # knows current branch  # line 451
    strict = '--strict' in options or m.strict  # type: bool  # line 452
    branch, revision = m.parseRevisionString(argument)  # line 453
    if branch not in m.branches:  # line 454
        Exit("Unknown branch")  # line 454
    m.loadBranch(branch)  # knows commits  # line 455
    revision = revision if revision >= 0 else len(m.commits) + revision  # negative indexing  # line 456
    if revision < 0 or revision > max(m.commits):  # line 457
        Exit("Unknown revision r%02d" % revision)  # line 457
    info("/|\\ Changes of file tree vs. revision '%s/r%02d'" % ((lambda _coconut_none_coalesce_item: "b%02d" % branch if _coconut_none_coalesce_item is None else _coconut_none_coalesce_item)(m.branches[branch].name), revision))  # line 458
    m.computeSequentialPathSet(branch, revision)  # load all commits up to specified revision  # line 459
    changes = m.findChanges(checkContent=strict, considerOnly=None if not m.track else m.getTrackingPatterns() | m.getTrackingPatterns(branch))  # type: ChangeSet  # line 460
    m.listChanges(changes)  # line 461
    return changes  # line 462

def diff(argument: 'str', options: '_coconut.typing.Sequence[str]'=[]) -> 'None':  # line 464
    ''' Show text file differences of file tree vs. (last or specified) revision on current or specified branch. '''  # line 465
    m = Metadata(os.getcwd())  # type: Metadata  # line 466
    branch = None  # type: _coconut.typing.Optional[int]  # line 466
    revision = None  # type: _coconut.typing.Optional[int]  # line 466
    m.loadBranches()  # knows current branch  # line 467
    strict = '--strict' in options or m.strict  # type: bool  # line 468
    branch, revision = m.parseRevisionString(argument)  # line 469
    if branch not in m.branches:  # line 470
        Exit("Unknown branch")  # line 470
    m.loadBranch(branch)  # knows commits  # line 471
    revision = revision if revision >= 0 else len(m.commits) + revision  # negative indexing  # line 472
    if revision < 0 or revision > max(m.commits):  # line 473
        Exit("Unknown revision r%02d" % revision)  # line 473
    info("/|\\ Differences of file tree vs. revision '%s/r%02d'" % ((lambda _coconut_none_coalesce_item: "b%02d" % branch if _coconut_none_coalesce_item is None else _coconut_none_coalesce_item)(m.branches[branch].name), revision))  # line 474
    m.computeSequentialPathSet(branch, revision)  # load all commits up to specified revision  # line 475
    changes = m.findChanges(checkContent=strict, inverse=True, considerOnly=None if not m.track else m.getTrackingPatterns() | m.getTrackingPatterns(branch))  # type: ChangeSet  # line 476
    onlyBinaryModifications = dataCopy(ChangeSet, changes, modifications={k: v for k, v in changes.modifications.items() if not m.isTextType(k)})  # type: ChangeSet  # line 477
    if modified(onlyBinaryModifications):  # line 478
        debug("/|\\ File changes")  # line 478
    m.listChanges(onlyBinaryModifications)  # only list modified binary files  # line 479

    if changes.modifications:  # TODO only text files, not binary  # line 481
        debug("%s/|\\ Textual modifications" % ("\n" if modified(onlyBinaryModifications) else ""))  # TODO only text files, not binary  # line 481
    for path, pinfo in changes.modifications.items():  # only consider modified files TODO also show A/D here? or replace listing above?  # line 482
        content = None  # type: _coconut.typing.Optional[bytes]  # ; othr:str[]; curr:str[]  # line 483
        if pinfo.size == 0:  # empty file contents  # line 484
            content = b""  # empty file contents  # line 484
        else:  # versioned file  # line 485
            content = m.restoreFile(None, branch, revision, pinfo)  # versioned file  # line 485
            assert content is not None  # versioned file  # line 485
        abspath = os.path.join(m.root, path.replace(SLASH, os.sep))  # current file  # line 486
        blocks = merge(file=content, intoname=abspath, diffOnly=True)  # type: List[MergeBlock]  # only determine change blocks  # line 487
        print("DIF %s%s" % (path, " <timestamp only>" if len(blocks) == 1 and blocks[0].tipe == MergeBlockType.KEEP else ""))  # line 488
        for block in blocks:  # line 489
            if block.tipe in [MergeBlockType.INSERT, MergeBlockType.REMOVE]:  # line 490
                pass  # TODO print some previous and following lines - which aren't accessible here anymore  # line 491
            if block.tipe == MergeBlockType.INSERT:  # TODO show color via curses?  # line 492
                for no, line in enumerate(block.lines):  # line 493
                    print("+++ %04d |%s|" % (no + block.line, line))  # line 494
            elif block.tipe == MergeBlockType.REMOVE:  # line 495
                for no, line in enumerate(block.lines):  # line 496
                    print("--- %04d |%s|" % (no + block.line, line))  # line 497
            elif block.tipe in [MergeBlockType.REPLACE, MergeBlockType.MODIFY]:  # TODO for MODIFY also show intra-line change ranges  # line 498
                for no, line in enumerate(block.replaces.lines):  # line 499
                    print("- | %04d |%s|" % (no + block.replaces.line, line))  # line 500
                for no, line in enumerate(block.lines):  # line 501
                    print("+ | %04d |%s|" % (no + block.line, line))  # line 502
#      elif block.tipe == MergeBlockType.KEEP: pass
#      elif block.tipe == MergeBlockType.MODIFY:  # intra-line modifications
#      elif block.tipe == MergeBlockType.MOVE:  # intra-line modifications

def commit(argument: '_coconut.typing.Optional[str]'=None, options: '_coconut.typing.Sequence[str]'=[]) -> 'None':  # line 507
    ''' Create new revision from file tree changes vs. last commit. '''  # line 508
    m = Metadata(os.getcwd())  # type: Metadata  # line 509
    m.loadBranches()  # knows current branch  # line 510
    if argument is not None and argument in m.tags:  # line 511
        Exit("Illegal commit message. It was already used as a tag name")  # line 511
    changes = None  # type: ChangeSet  # line 512
    m, branch, revision, changes, strict, force, trackingPatterns = exitOnChanges(None, options, commit=True)  # special flag creates new revision for detected changes, but abort if no changes  # line 513
    info((lambda _coconut_none_coalesce_item: "b%d" % m.branch if _coconut_none_coalesce_item is None else _coconut_none_coalesce_item)("Committing changes to branch '%s'..." % m.branches[m.branch].name))  # line 514
    m.integrateChangeset(changes, clear=True)  # update pathset to changeset only  # line 515
    m.saveCommit(m.branch, revision)  # revision has already been incremented  # line 516
    m.commits[revision] = CommitInfo(revision, longint(time.time() * 1000), argument)  # comment can be None  # line 517
    m.saveBranch(m.branch)  # line 518
    m.loadBranches()  # TODO is it necessary to load again?  # line 519
    if m.picky:  # HINT was changed from only picky to include track as well  # line 520
        m.branches[m.branch] = dataCopy(BranchInfo, m.branches[m.branch], tracked=[], insync=False)  # remove tracked patterns  # line 521
    else:  # track or simple mode  # line 522
        m.branches[m.branch] = dataCopy(BranchInfo, m.branches[m.branch], insync=False)  # set branch dirty  # line 523
    if "--tag" in options and argument is not None:  # memorize unique tag  # line 524
        m.tags.append(argument)  # memorize unique tag  # line 524
    m.saveBranches()  # line 525
    info("Created new revision r%02d%s (+%02d/-%02d/*%02d)" % (revision, ((" '%s'" % argument) if argument is not None else ""), len(changes.additions), len(changes.deletions), len(changes.modifications)))  # line 526

def status() -> 'None':  # line 528
    ''' Show branches and current repository state. '''  # line 529
    m = Metadata(os.getcwd())  # type: Metadata  # line 530
    m.loadBranches()  # knows current branch  # line 531
    current = m.branch  # type: int  # line 532
    info("/|\\ Offline repository status")  # line 533
    sl = max([len((lambda _coconut_none_coalesce_item: "" if _coconut_none_coalesce_item is None else _coconut_none_coalesce_item)(b.name)) for b in m.branches.values()])  # type: int  # line 534
    for branch in sorted(m.branches.values(), key=lambda b: b.number):  # line 535
        m.loadBranch(branch.number)  # knows commit history  # line 536
        print("  %s b%02d%s @%s (%s) with %d commits%s" % ("*" if current == branch.number else " ", branch.number, ((" %%%ds" % (sl + 2)) % ("'%s'" % branch.name)) if branch.name else "", strftime(branch.ctime), "in sync" if branch.insync else "dirty", len(m.commits), ". Last comment: '%s'" % m.commits[max(m.commits)].message if m.commits[max(m.commits)].message else ""))  # line 537
    if m.track or m.picky and len(m.branches[m.branch].tracked) > 0:  # line 538
        info("\nTracked file patterns:")  # line 539
        print(ajoin("  | ", m.branches[m.branch].tracked, "\n"))  # line 540

def exitOnChanges(argument: '_coconut.typing.Optional[str]'=None, options: '_coconut.typing.Sequence[str]'=[], check: 'bool'=True, commit: 'bool'=False) -> 'Tuple[Metadata, _coconut.typing.Optional[int], int, ChangeSet, bool, bool, FrozenSet[str]]':  # line 542
    ''' Common behavior for switch, update, delete, commit.
      check: stop program on detected change
      commit: don't stop on changes, because that's what we need in the operation
      Returns (Metadata, (current or target) branch, revision, set of changes vs. last commit on current branch, strict, force flags. '''  # line 546
    m = Metadata(os.getcwd())  # type: Metadata  # line 547
    m.loadBranches()  # knows current branch  # line 548
    trackingPatterns = m.getTrackingPatterns()  # type: FrozenSet[str]  # SVN-like mode  # line 549
    force = '--force' in options  # type: bool  # line 550
    strict = '--strict' in options or m.strict  # type: bool  # line 551
    if argument is not None:  # line 552
        branch, revision = m.parseRevisionString(argument)  # for early abort  # line 553
        if branch is None:  # line 554
            Exit("Branch '%s' doesn't exist. Cannot proceed" % argument)  # line 554
    m.loadBranch(m.branch)  # knows last commits of *current* branch  # line 555

# Determine current changes
    m.computeSequentialPathSet(m.branch, max(m.commits))  # load all commits up to specified revision  # line 558
    changes = m.findChanges(m.branch if commit else None, max(m.commits) + 1 if commit else None, checkContent=strict, considerOnly=None if not m.track and not m.picky else trackingPatterns)  # type: ChangeSet  # line 559
    if modified(changes) and not force:  # and check?  # line 560
        m.listChanges(changes)  # line 561
        if check and not commit:  # line 562
            Exit("File tree contains changes. Use --force to proceed")  # line 562
    elif commit and not force:  #  and not check  # line 563
        Exit("Nothing to commit. Aborting")  #  and not check  # line 563

    if argument is not None:  # branch/revision specified  # line 565
        m.loadBranch(branch)  # knows commits of target branch  # line 566
        revision = revision if revision >= 0 else len(m.commits) + revision  # negative indexing  # line 567
        if revision < 0 or revision > max(m.commits):  # line 568
            Exit("Unknown revision r%02d" % revision)  # line 568
        return (m, branch, revision, changes, strict, force, m.getTrackingPatterns(branch))  # line 569
    return (m, m.branch, max(m.commits) + (1 if commit else 0), changes, strict, force, trackingPatterns)  # line 570

def switch(argument: 'str', options: '_coconut.typing.Sequence[str]'=[]) -> 'None':  # line 572
    ''' Continue work on another branch, replacing file tree changes. '''  # line 573
    changes = None  # type: ChangeSet  # line 574
    m, branch, revision, changes, strict, force, trackingPatterns = exitOnChanges(argument, options)  # line 575
    info("/|\\ Switching to branch %sb%02d/r%02d" % ("'%s' " % m.branches[branch].name if m.branches[branch].name else "", branch, revision))  # line 576

# Determine file changes from other branch to current file tree
    if '--meta' in options:  # only switch meta data  # line 579
        m.branches[m.branch] = dataCopy(BranchInfo, m.branches[m.branch], tracked=m.branches[branch].tracked)  # line 580
    else:  # full file switch  # line 581
        m.computeSequentialPathSet(branch, revision)  # load all commits up to specified revision for target branch into memory  # line 582
        changes = m.findChanges(checkContent=strict, inverse=True, considerOnly=None if not m.track else trackingPatterns | m.getTrackingPatterns(branch))  # determine difference of other branch vs. file tree (forced or in sync with current branch; "addition" means exists now and should be removed)  # line 583
        if not modified(changes):  # line 584
            info("No changes to current file tree")  # line 585
        else:  # integration required  # line 586
            for path, pinfo in changes.deletions.items():  # line 587
                m.restoreFile(path, branch, revision, pinfo)  # is deleted in current file tree: restore from branch to reach target  # line 588
                debug("ADD " + path)  # line 589
            for path, pinfo in changes.additions.items():  # line 590
                os.unlink(os.path.join(m.root, path.replace(SLASH, os.sep)))  # is added in current file tree: remove from branch to reach target  # line 591
                debug("DEL " + path)  # line 592
            for path, pinfo in changes.modifications.items():  # line 593
                m.restoreFile(path, branch, revision, pinfo)  # is modified in current file tree: restore from branch to reach target  # line 594
                debug("MOD " + path)  # line 595
    m.branch = branch  # line 596
    m.saveBranches()  # store switched path info  # line 597
    info("Switched to branch %sb%02d/r%02d" % ("'%s' " % (m.branches[branch].name if m.branches[branch].name else ""), branch, revision))  # line 598

def update(argument: 'str', options: '_coconut.typing.Sequence[str]'=[]) -> 'None':  # line 600
    ''' Load and integrate a specified other branch/revision into current life file tree.
      In tracking mode, this also updates the set of tracked patterns.
      User options for merge operation: --add (don't remove), --rm (don't insert), --add-lines/--rm-lines (inside each file)
      User options for conflict resolution: --theirs/--mine/--ask
  '''  # line 605
    mrg = firstOfMap({"--add": MergeOperation.INSERT, "--rm": MergeOperation.REMOVE}, options, MergeOperation.BOTH)  # type: int  # default operation is replicate remove state for non-conflicting cases (insertions/deletions)  # line 606
    res = firstOfMap({'--theirs': ConflictResolution.THEIRS, '--mine': ConflictResolution.MINE}, options, ConflictResolution.NEXT)  # type: int  # NEXT means deeper level  # line 607
    mrgline = firstOfMap({'--add-lines': MergeOperation.INSERT, '--rm-lines': MergeOperation.REMOVE}, options, mrg)  # type: int  # default operation for modified files is same as for files  # line 608
    resline = firstOfMap({'--theirs-lines': ConflictResolution.THEIRS, '--mine-lines': ConflictResolution.MINE}, options, ConflictResolution.ASK)  # type: int  # line 609
    m = Metadata(os.getcwd())  # type: Metadata  # TODO same is called inside stop on changes - could return both current and designated branch instead  # line 610
    m.loadBranches()  # line 611
    changes = None  # type: ChangeSet  # line 611
    currentBranch = m.branch  # type: _coconut.typing.Optional[int]  # line 612
    m, branch, revision, changes, strict, force, trackingPatterns = exitOnChanges(argument, options, check=False)  # don't check for current changes, only parse arguments  # line 613
    debug("Integrating changes from '%s/r%02d' into file tree..." % ((lambda _coconut_none_coalesce_item: "b%02d" % branch if _coconut_none_coalesce_item is None else _coconut_none_coalesce_item)(m.branches[branch].name), revision))  # line 614

# Determine file changes from other branch over current file tree
    m.computeSequentialPathSet(branch, revision)  # load all commits up to specified revision for branch to integrate  # line 617
    trackingUnion = trackingPatterns | m.getTrackingPatterns(branch)  # type: FrozenSet[str]  # line 618
    changes = m.findChanges(checkContent=strict, inverse=True, considerOnly=None if not m.track else trackingUnion)  # determine difference of other branch vs. file tree. "addition" means exists now but not in other, and should be removed unless in tracking mode  # line 619
    if not (mrg & MergeOperation.INSERT and changes.additions or (mrg & MergeOperation.REMOVE and changes.deletions) or changes.modifications):  # line 620
        if trackingUnion == trackingPatterns:  # nothing added  # line 621
            info("No file changes detected, but tracking patterns were merged (run 'sos switch /-1 --meta' to undo)")  # TODO write test to see if this works  # line 622
        else:  # line 623
            info("Nothing to update")  # but write back updated branch info below  # line 624
    else:  # integration required  # line 625
        for path, pinfo in changes.deletions.items():  # deletions mark files not present in current file tree -> needs additon  # line 626
            if mrg & MergeOperation.INSERT:  # deleted in current file tree: restore from branch to reach target  # line 627
                m.restoreFile(path, branch, revision, pinfo)  # deleted in current file tree: restore from branch to reach target  # line 627
            print("ADD " + path if mrg & MergeOperation.INSERT else "(A) " + path)  # line 628
        for path, pinfo in changes.additions.items():  # line 629
            if m.track or m.picky:  # because untracked files of other branch cannot be detected (which is good)  # line 630
                Exit("This should never happen")  # because untracked files of other branch cannot be detected (which is good)  # line 630
            if mrg & MergeOperation.REMOVE:  # line 631
                os.unlink(m.root + os.sep + path.replace(SLASH, os.sep))  # line 631
            print("DEL " if mrg & MergeOperation.REMOVE else "(D) " + path)  # not contained in other branch, but maybe kept  # line 632
        for path, pinfo in changes.modifications.items():  # line 633
            into = os.path.join(m.root, path.replace(SLASH, os.sep))  # type: str  # line 634
            binary = not m.isTextType(path)  # line 635
            if res & ConflictResolution.ASK or (binary and res == ConflictResolution.NEXT):  # TODO this may ask user even if no interaction was asked for (check line level for interactivity fist)  # line 636
                print(("MOD " if not binary else "BIN ") + path)  # line 637
                reso = {"i": ConflictResolution.MINE, "t": ConflictResolution.THEIRS, "m": ConflictResolution.NEXT}.get(user_input(" Resolve: *M[I]ne, [T]heirs, [M]erge: (I)").strip().lower(), ConflictResolution.MINE)  # line 638
                debug("User selected %d" % reso)  # line 639
            else:  # line 640
                reso = res  # line 640
            if reso & ConflictResolution.THEIRS:  # line 641
                m.readOrCopyVersionedFile(branch, revision, pinfo.namehash, toFile=into)  # blockwise copy of contents  # line 642
                print("THR " + path)  # line 643
            elif reso & ConflictResolution.MINE:  # line 644
                print("MNE " + path)  # nothing to do! same as skip  # line 645
            else:  # NEXT: line-based merge  # line 646
                file = m.readOrCopyVersionedFile(branch, revision, pinfo.namehash) if pinfo.size > 0 else b''  # type: _coconut.typing.Optional[bytes]  # parse lines TODO decode etc.  # line 647
                if file is not None:  # if None, error message was already logged  # line 648
                    contents = merge(file=file, intoname=into, mergeOperation=mrgline, conflictResolution=resline)  # type: bytes  # line 649
                    with open(path, "wb") as fd:  # TODO write to temp file first  # line 650
                        fd.write(contents)  # TODO write to temp file first  # line 650
    info("Integrated changes from '%s/r%02d' into file tree" % ((lambda _coconut_none_coalesce_item: "b%02d" % branch if _coconut_none_coalesce_item is None else _coconut_none_coalesce_item)(m.branches[branch].name), revision))  # line 651
    m.branches[currentBranch] = dataCopy(BranchInfo, m.branches[currentBranch], insync=False, tracked=list(trackingUnion))  # TODO really? it's a change that cannot be undone easily by the user  # line 652
    m.branch = currentBranch  # need to restore setting before saving TODO operate on different objects instead  # line 653
    m.saveBranches()  # line 654

def delete(argument: 'str', options: '_coconut.typing.Sequence[str]'=[]) -> 'None':  # line 656
    ''' Remove a branch entirely. '''  # line 657
    m, branch, revision, changes, strict, force, trackingPatterns = exitOnChanges(None, options)  # line 658
    if len(m.branches) == 1:  # line 659
        Exit("Cannot remove the only remaining branch. Use 'sos online' to leave offline mode")  # line 659
    branch, revision = m.parseRevisionString(argument)  # not from exitOnChanges, because we have to set argument to None there  # line 660
    if branch is None or branch not in m.branches:  # line 661
        Exit("Unknown branch")  # line 661
    debug("Removing branch %d%s..." % (branch, " '%s'" % m.branches[branch].name if m.branches[branch].name else ""))  # line 662
    binfo = m.removeBranch(branch)  # need to keep a reference to removed entry for output below  # line 663
    info("Branch b%02d%s removed" % (branch, " '%s'" % binfo.name if binfo.name else ""))  # line 664

def add(folder: 'str', argument: 'str', options: '_coconut.typing.Sequence[str]'=[]) -> 'None':  # line 666
    ''' Add a tracked files pattern to current branch's tracked files. '''  # line 667
    force = '--force' in options  # type: bool  # line 668
    m = Metadata(os.getcwd())  # type: Metadata  # line 669
    m.loadBranches()  # line 670
    if not m.track and not m.picky:  # line 671
        Exit("Repository is in simple mode. Needs 'offline --track' or 'offline --picky' instead")  # line 671
    relpath = os.path.relpath(os.path.dirname(os.path.abspath(os.path.join(folder, argument))), m.root)  # for tracking list  # line 672
    pattern = os.path.join(relpath, os.path.basename(argument)).replace(os.sep, SLASH)  # line 673
    if pattern in m.branches[m.branch].tracked:  # line 674
        Exit("Pattern '%s' already tracked")  # line 675
    if not force and len(fnmatch.filter(os.listdir(os.path.abspath(relpath)), os.path.basename(pattern.replace(SLASH, os.sep)))) == 0:  # doesn't match any current file  # line 676
        Exit("Pattern doesn't match any file in specified folder. Use --force to add it anyway")  # line 677
    m.branches[m.branch].tracked.append(pattern)  # TODO set insync flag to False? same for rm  # line 678
    m.saveBranches()  # line 679
    info("Added tracking pattern '%s' for folder '%s'" % (os.path.basename(pattern.replace(SLASH, os.sep)), os.path.abspath(relpath)))  # line 680

def rm(folder: 'str', argument: 'str') -> 'None':  # line 682
    ''' Remove a tracked files pattern from current branch's tracked files. '''  # line 683
    m = Metadata(os.getcwd())  # type: Metadata  # line 684
    m.loadBranches()  # line 685
    if not m.track and not m.picky:  # line 686
        Exit("Repository is in simple mode. Needs 'offline --track' or 'offline --picky' instead")  # line 686
    relpath = os.path.relpath(os.path.dirname(os.path.abspath(os.path.join(folder, argument))), m.root)  # type: str  # line 687
    pattern = os.path.join(relpath, os.path.basename(argument)).replace(os.sep, SLASH)  # type: str  # line 688
    if pattern not in m.branches[m.branch].tracked:  # line 689
        suggestion = _coconut.set()  # type: Set[str]  # line 690
        for pat in m.branches[m.branch].tracked:  # line 691
            if fnmatch.fnmatch(pattern, pat):  # line 692
                suggestion.add(pat)  # line 692
        if suggestion:  # line 693
            print("Do you mean any of the following tracked globs? '%s'" % (", ".join(sorted(suggestion))))  # line 693
        Exit("Tracked pattern '%s' not found" % pattern)  # line 694
    m.branches[m.branch].tracked.remove(pattern)  # line 695
    m.saveBranches()  # line 696
    info("Removed tracking pattern '%s' for folder '%s'" % (os.path.basename(pattern.replace(SLASH, os.sep)), os.path.abspath(relpath)))  # line 697

def ls(argument: '_coconut.typing.Optional[str]'=None) -> 'None':  # line 699
    ''' List specified directory, augmenting with repository metadata. '''  # line 700
    cwd = os.getcwd() if argument is None else argument  # type: str  # line 701
    m = Metadata(cwd)  # type: Metadata  # line 702
    m.loadBranches()  # line 703
    relpath = os.path.relpath(cwd, m.root).replace(os.sep, SLASH)  # type: str  # line 704
    files = list(sorted((entry for entry in os.listdir(cwd) if os.path.isfile(entry))))  # type: List[str]  # line 705
    trackingPatterns = m.getTrackingPatterns() if m.track or m.picky else _coconut.frozenset()  # type: FrozenSet[str]  # for current branch  # line 706
    for file in files:  # line 707
        ignore = None  # type: _coconut.typing.Optional[str]  # line 708
        for ig in m.c.ignores:  # line 709
            if fnmatch.fnmatch(file, ig):  # remember first match TODO document this  # line 710
                ignore = ig  # remember first match TODO document this  # line 710
                break  # remember first match TODO document this  # line 710
        if ig:  # line 711
            for wl in m.c.ignoresWhitelist:  # line 712
                if fnmatch.fnmatch(file, wl):  # found a white list entry for ignored file, undo ignoring it  # line 713
                    ignore = None  # found a white list entry for ignored file, undo ignoring it  # line 713
                    break  # found a white list entry for ignored file, undo ignoring it  # line 713
        if ignore is None:  # line 714
            matches = []  # type: List[str]  # line 715
            for pattern in (p for p in trackingPatterns if os.path.dirname(p) == relpath):  # only patterns matching current folder  # line 716
                if fnmatch.fnmatch(file, os.path.basename(pattern)):  # TODO or only file basename?  # line 717
                    matches.append(pattern)  # TODO or only file basename?  # line 717
        print("%s %s%s" % ("IGN" if ignore is not None else ("TRK" if len(matches) > 0 else "   "), file, ' by "%s"' % ignore if ignore is not None else (" by " + ";".join(['"%s"' % match for match in matches]) if len(matches) > 0 else "")))  # line 718

def log(options: '_coconut.typing.Sequence[str]') -> 'None':  # line 720
    ''' List previous commits on current branch. '''  # line 721
    m = Metadata(os.getcwd())  # type: Metadata  # line 722
    m.loadBranches()  # knows current branch  # line 723
    m.loadBranch(m.branch)  # knows commit history  # line 724
    info((lambda _coconut_none_coalesce_item: "r%02d" % m.branch if _coconut_none_coalesce_item is None else _coconut_none_coalesce_item)("/|\\ Offline commit history of branch '%s'" % m.branches[m.branch].name))  # TODO also retain "from branch/revision" on branching?  # line 725
    nl = len("%d" % max(m.commits))  # determine space needed for revision  # line 726
    changeset = m.computeSequentialPathSetIterator(m.branch, max(m.commits))  # line 727
    maxWidth = max([wcswidth(commit.message) for commit in m.commits.values()])  # type: int  # line 728
    for no in range(max(m.commits) + 1):  # line 729
        commit = m.commits[no]  # type: CommitInfo  # line 730
        changes = next(changeset)  # type: ChangeSet  # side-effect: updates m.paths  # line 731
        newTextFiles = len([file for file in changes.additions.keys() if m.isTextType(file)])  # type: int  # line 732
        print("  %s r%s @%s (+%02d/-%02d/*%02d +%02dT/%05.1f%%) |%s|" % ("*" if commit.number == max(m.commits) else " ", ("%%%ds" % nl) % commit.number, strftime(commit.ctime), len(changes.additions), len(changes.deletions), len(changes.modifications), newTextFiles, 0. if len(changes.additions) == 0 else newTextFiles * 100. / len(changes.additions), ((lambda _coconut_none_coalesce_item: "" if _coconut_none_coalesce_item is None else _coconut_none_coalesce_item)(commit.message)).ljust(maxWidth)))  # line 733
        if '--changes' in options:  # line 734
            m.listChanges(changes)  # line 734

def config(argument: 'str', options: 'List[str]'=[]) -> 'None':  # line 736
    if argument not in ["set", "unset", "show", "list", "add", "rm"]:  # line 737
        Exit("Unknown config command")  # line 737
    if not configr:  # line 738
        Exit("Cannot execute config command. 'configr' module not installed")  # line 738
    c = loadConfig()  # type: Union[configr.Configr, Accessor]  # line 739
    if argument == "set":  # line 740
        if len(options) < 2:  # line 741
            Exit("No key nor value specified")  # line 741
        if options[0] not in (["defaultbranch"] + CONFIGURABLE_FLAGS + CONFIGURABLE_LISTS):  # line 742
            Exit("Unsupported key %r" % options[0])  # line 742
        if options[0] in CONFIGURABLE_FLAGS and options[1].lower() not in TRUTH_VALUES + FALSE_VALUES:  # line 743
            Exit("Cannot set flag to '%s'. Try on/off instead" % options[1].lower())  # line 743
        c[options[0]] = options[1].lower() in TRUTH_VALUES if options[0] in CONFIGURABLE_FLAGS else (options[1].strip() if options[0] not in CONFIGURABLE_LISTS else safeSplit(options[1], ";"))  # TODO sanitize texts?  # line 744
    elif argument == "unset":  # line 745
        if len(options) < 1:  # line 746
            Exit("No key specified")  # line 746
        if options[0] not in c.keys():  # line 747
            Exit("Unknown key")  # line 747
        del c[options[0]]  # line 748
    elif argument == "add":  # line 749
        if len(options) < 2:  # line 750
            Exit("No key nor value specified")  # line 750
        if options[0] not in CONFIGURABLE_LISTS:  # line 751
            Exit("Unsupported key for add %r" % options[0])  # line 751
        if options[0] not in c.keys():  # add list  # line 752
            c[options[0]] = [options[1]]  # add list  # line 752
        elif options[1] in c[options[0]]:  # line 753
            Exit("Value already contained")  # line 753
        c[options[0]].append(options[1])  # line 754
    elif argument == "rm":  # line 755
        if len(options) < 2:  # line 756
            Exit("No key nor value specified")  # line 756
        if options[0] not in c.keys():  # line 757
            Exit("Unknown key specified: %r" % options[0])  # line 757
        if options[1] not in c[options[0]]:  # line 758
            Exit("Unknown value: %r" % options[1])  # line 758
        c[options[0]].remove(options[1])  # line 759
    else:  # Show  # line 760
        for k, v in sorted(c.items()):  # line 761
            print("%s => %r" % (k, v))  # line 761
        return  # line 762
    f, g = saveConfig(c)  # line 763
    if f is None:  # line 764
        error("Error saving user configuration: %r" % g)  # line 764

def parse(root: 'str', inFolder: 'str'):  # line 766
    ''' Main operation. '''  # line 767
    debug("Parsing command-line arguments...")  # line 768
    command = sys.argv[1].strip() if len(sys.argv) > 1 else ""  # line 769
    argument = sys.argv[2].strip() if len(sys.argv) > 2 and not sys.argv[2].startswith("--") else None  # line 770
    options = sys.argv[3:] if command == "config" else [c for c in sys.argv[2:] if c.startswith("--")]  # consider second parameter for no-arg command, otherwise from third on  # line 771
    debug("Processing command %r with argument '%s' and options %r." % ("" if command is None else command, "" if argument is None else argument, options))  # line 772
    if command[:1] == "a":  # line 773
        add(inFolder, argument, options)  # line 773
    elif command[:1] == "b":  # line 774
        branch(argument, options)  # line 774
    elif command[:2] == "ch":  # line 775
        changes(argument, options)  # line 775
    elif command[:3] == "com" or command[:2] == "ci":  # line 776
        commit(argument, options)  # line 776
    elif command[:3] == 'con':  # line 777
        config(argument, options)  # line 777
    elif command[:2] == "de":  # line 778
        delete(argument, options)  # line 778
    elif command[:2] == "di":  # line 779
        diff(argument, options)  # line 779
    elif command[:1] == "h":  # line 780
        usage()  # line 780
    elif command[:2] == "lo":  # line 781
        log(options)  # line 781
    elif command[:2] in ["li", "ls"]:  # line 782
        ls(argument)  # line 782
    elif command[:2] == "of":  # line 783
        offline(argument, options)  # line 783
    elif command[:2] == "on":  # line 784
        online(options)  # line 784
    elif command[:1] == "r":  # line 785
        rm(inFolder, argument)  # line 785
    elif command[:2] == "st":  # line 786
        status()  # line 786
    elif command[:2] == "sw":  # line 787
        switch(argument, options)  # line 787
    elif command[:2] == "u":  # line 788
        update(argument, options)  # line 788
    else:  # line 789
        Exit("Unknown command '%s'" % command)  # line 789
    sys.exit(0)  # line 790

def main() -> 'None':  # line 792
    global debug, info, warn, error  # line 793
    logging.basicConfig(level=level, stream=sys.stderr, format=("%(asctime)-23s %(levelname)-8s %(name)s:%(lineno)d | %(message)s" if '--log' in sys.argv else "%(message)s"))  # line 794
    _log = Logger(logging.getLogger(__name__))  # line 795
    debug, info, warn, error = _log.debug, _log.info, _log.warn, _log.error  # line 795
    for option in (o for o in ['--log', '--verbose', '-v', '--sos'] if o in sys.argv):  # clean up program arguments  # line 796
        sys.argv.remove(option)  # clean up program arguments  # line 796
    if '--help' in sys.argv or len(sys.argv) < 2:  # line 797
        usage()  # line 797
        Exit()  # line 797
    command = sys.argv[1] if len(sys.argv) > 1 else None  # type: _coconut.typing.Optional[str]  # line 798
    root, vcs, cmd = findSosVcsBase()  # root is None if no .sos folder exists up the folder tree (still working online); vcs is checkout/repo root folder; cmd is the VCS base command  # line 799
    debug("Found root folders for SOS|VCS: %s|%s" % ("" if root is None else root, "" if vcs is None else vcs))  # line 800
    defaults["defaultbranch"] = vcsBranches.get(cmd, "trunk")  # sets dynamic default with SVN fallback  # line 801
    if force_sos or root is not None or ("" if command is None else command)[:2] == "of" or ("" if command is None else command)[:1] == "h":  # in offline mode or just going offline TODO what about git config?  # line 802
        cwd = os.getcwd()  # line 803
        os.chdir(cwd if command[:2] == "of" else cwd if root is None else root)  # line 804
        parse(root, cwd)  # line 805
    elif cmd is not None:  # online mode - delegate to VCS  # line 806
        info("SOS: Running '%s %s'" % (cmd, " ".join(sys.argv[1:])))  # line 807
        import subprocess  # only required in this section  # line 808
        process = subprocess.Popen([cmd] + sys.argv[1:], shell=False, stdin=subprocess.PIPE, stdout=sys.stdout, stderr=sys.stderr)  # line 809
        inp = ""  # type: str  # line 810
        while True:  # line 811
            so, se = process.communicate(input=inp)  # line 812
            if process.returncode is not None:  # line 813
                break  # line 813
            inp = sys.stdin.read()  # line 814
        if sys.argv[1][:2] == "co" and process.returncode == 0:  # successful commit - assume now in sync again (but leave meta data folder with potential other feature branches behind until "online")  # line 815
            if root is None:  # line 816
                Exit("Cannot determine VCS root folder: Unable to mark repository as synchronized and will show a warning when leaving offline mode")  # line 816
            m = Metadata(root)  # line 817
            m.loadBranches()  # read repo  # line 818
            m.branches[m.branch] = dataCopy(BranchInfo, m.branches[m.branch], insync=True)  # mark as committed  # line 819
            m.saveBranches()  # line 820
    else:  # line 821
        Exit("No offline repository present, and unable to detect VCS file tree")  # line 821


# Main part
level = logging.DEBUG if os.environ.get("DEBUG", "False").lower() == "true" or '--verbose' in sys.argv or '-v' in sys.argv else logging.INFO  # line 825
force_sos = '--sos' in sys.argv  # line 826
_log = Logger(logging.getLogger(__name__))  # line 827
debug, info, warn, error = _log.debug, _log.info, _log.warn, _log.error  # line 827
if __name__ == '__main__':  # line 828
    main()  # line 828
