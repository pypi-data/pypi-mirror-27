#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# __coconut_hash__ = 0x9b104799

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
    update  [<branch>][/<revision>]                       Integrate work from another branch TODO add many merge and conflict resolution options
    destroy [<branch>]                                    Remove (current) branch entirely

    commit  [<message>] [--tag]                           Create a new revision from current state file tree, with an optional commit message
    changes [<branch>][/<revision>]                       List changed paths vs. last or specified revision
    diff    [<branch>][/<revision>]                       List changes vs. last or specified revision
    add     [<filename or glob pattern>]                  Add a tracking pattern to current branch (path/filename or glob pattern)
    mv      [<oldpattern>] [<newpattern>]                 Rename, move or move and rename tracked files according to glob patterns
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
    <branch/revision>            Revision string. Branch is optional and may be a label or index
                                 Revision is an optional integer and may be negative to reference from the latest commits (-1 is most recent revision)

  Common options:
    --force                      Executes potentially harmful operations
                                   for offline: ignore being already offline, start from scratch (same as 'sos online --force && sos offline')
                                   for online: ignore uncommitted branches
                                   for commit, switch, update, add: ignore uncommitted changes before executing command
    --strict                     Perform full content comparison, don't rely only on file size and timestamp
                                   for offline: persist strict mode in repository
                                   for changes, diff, commit, switch, update, delete: perform operation in strict mode
    --only <filename or glob>    Restrict operation to specified pattern(s). Available for "changes", "commit", "diff", "switch", and "update"
    --except <filename or glob>  Avoid operation for specified pattern(s). Available for "changes", "commit", "diff", "switch", and "update"
    --{cmd}                      When executing {CMD} not being offline, pass arguments to {CMD} instead (e.g. {cmd} --{cmd} config set key value.)
    --log                        Enable internals logger
    --verbose                    Enable debugging output""".format(appname=APPNAME, cmd="sos", CMD="SOS"))  # line 95

# Main data class
#@runtime_validation
class Metadata:  # line 99
    ''' This class doesn't represent the entire repository state in memory,
      but serves as a container for different repo operations,
      using only parts of its attributes at any point in time. Use with care.
  '''  # line 103

    def __init__(_, path: 'str') -> 'None':  # line 105
        ''' Create empty container object for various repository operations. '''  # line 106
        _.c = loadConfig()  # line 107
        _.root = path  # type: str  # line 108
        _.branches = {}  # type: Dict[int, BranchInfo]  # branch number zero represents the initial state at branching  # line 109
        _.commits = {}  # type: Dict[int, CommitInfo]  # consecutive numbers per branch, starting at 0  # line 110
        _.paths = {}  # type: Dict[str, PathInfo]  # utf-8 encoded relative, normalized file system paths  # line 111
        _.tags = []  # type: List[str]  # line 112
        _.branch = None  # type: _coconut.typing.Optional[int]  # current branch number  # line 113
        _.commit = None  # type: _coconut.typing.Optional[int]  # current revision number  # line 114
        _.track = _.c.track  # type: bool  # track file name patterns in the repository (per branch)  # line 115
        _.picky = _.c.picky  # type: bool  # pick files to commit per operation  # line 116
        _.strict = _.c.strict  # type: bool  # be always strict (regarding file contents comparsion)  # line 117
        _.compress = _.c.compress  # type: bool  # these flags are stored in the repository  # line 118

    def isTextType(_, filename: 'str') -> 'bool':  # line 120
        return (((lambda _coconut_none_coalesce_item: "" if _coconut_none_coalesce_item is None else _coconut_none_coalesce_item)(mimetypes.guess_type(filename)[0])).startswith("text/") or any([fnmatch.fnmatch(filename, pattern) for pattern in _.c.texttype])) and not any([fnmatch.fnmatch(filename, pattern) for pattern in _.c.bintype])  # line 120

    def listChanges(_, changes: 'ChangeSet') -> 'None':  # line 122
        if len(changes.additions) > 0:  # line 123
            print(ajoin("ADD ", sorted(changes.additions.keys()), "\n"))  # line 123
        if len(changes.deletions) > 0:  # line 124
            print(ajoin("DEL ", sorted(changes.deletions.keys()), "\n"))  # line 124
        if len(changes.modifications) > 0:  # line 125
            print(ajoin("MOD ", sorted(changes.modifications.keys()), "\n"))  # line 125

    def loadBranches(_) -> 'None':  # line 127
        ''' Load list of branches and current branch info from metadata file. '''  # line 128
        try:  # fails if not yet created (on initial branch/commit)  # line 129
            branches = None  # type: List[Tuple]  # line 130
            with codecs.open(os.path.join(_.root, metaFolder, metaFile), "r", encoding=UTF8) as fd:  # line 131
                flags, branches = json.load(fd)  # line 132
            _.tags = flags["tags"]  # list of commit messages to treat as globally unique tags  # line 133
            _.branch = flags["branch"]  # current branch integer  # line 134
            _.track = flags["track"]  # line 135
            _.picky = flags["picky"]  # line 136
            _.strict = flags["strict"]  # line 137
            _.compress = flags["compress"]  # line 138
            _.branches = {i.number: i for i in (BranchInfo(*item) for item in branches)}  # re-create type info  # line 139
        except Exception as E:  # if not found, create metadata folder  # line 140
            _.branches = {}  # line 141
            warn("Couldn't read branches metadata: %r" % E)  # line 142

    def saveBranches(_) -> 'None':  # line 144
        ''' Save list of branches and current branch info to metadata file. '''  # line 145
        with codecs.open(os.path.join(_.root, metaFolder, metaFile), "w", encoding=UTF8) as fd:  # line 146
            json.dump(({"tags": _.tags, "branch": _.branch, "track": _.track, "picky": _.picky, "strict": _.strict, "compress": _.compress}, list(_.branches.values())), fd, ensure_ascii=False)  # line 147

    def getRevisionByName(_, name: 'str') -> '_coconut.typing.Optional[int]':  # line 149
        ''' Convenience accessor for named revisions (using commit message as name). '''  # line 150
        if name == "":  # line 151
            return -1  # line 151
        try:  # attempt to parse integer string  # line 152
            return longint(name)  # attempt to parse integer string  # line 152
        except ValueError:  # line 153
            pass  # line 153
        found = [number for number, commit in _.commits.items() if name == commit.message]  # line 154
        return found[0] if found else None  # line 155

    def getBranchByName(_, name: 'str') -> '_coconut.typing.Optional[int]':  # line 157
        ''' Convenience accessor for named branches. '''  # line 158
        if name == "":  # line 159
            return _.branch  # line 159
        try:  # attempt to parse integer string  # line 160
            return longint(name)  # attempt to parse integer string  # line 160
        except ValueError:  # line 161
            pass  # line 161
        found = [number for number, branch in _.branches.items() if name == branch.name]  # line 162
        return found[0] if found else None  # line 163

    def loadBranch(_, branch: 'int') -> 'None':  # line 165
        ''' Load all commit information from a branch meta data file. '''  # line 166
        with codecs.open(os.path.join(_.root, metaFolder, "b%d" % branch, metaFile), "r", encoding=UTF8) as fd:  # line 167
            commits = json.load(fd)  # type: List[List[Any]]  # list of CommitInfo that needs to be unmarshalled into value types  # line 168
        _.commits = {i.number: i for i in (CommitInfo(*item) for item in commits)}  # re-create type info  # line 169
        _.branch = branch  # line 170

    def saveBranch(_, branch: 'int') -> 'None':  # line 172
        ''' Save all commit information to a branch meta data file. '''  # line 173
        with codecs.open(os.path.join(_.root, metaFolder, "b%d" % branch, metaFile), "w", encoding=UTF8) as fd:  # line 174
            json.dump(list(_.commits.values()), fd, ensure_ascii=False)  # line 175

    def duplicateBranch(_, branch: 'int', name: '_coconut.typing.Optional[str]') -> 'None':  # line 177
        ''' Create branch from an existing branch/revision. WARN: Caller must have loaded branches information.
        branch: target branch (should not exist yet)
        name: optional name of new branch
        _.branch: current branch
    '''  # line 182
        debug("Duplicating branch '%s' to '%d'..." % ((lambda _coconut_none_coalesce_item: "b%d" % _.branch if _coconut_none_coalesce_item is None else _coconut_none_coalesce_item)(_.branches[_.branch].name), branch))  # line 183
        tracked = [t for t in _.branches[_.branch].tracked]  # copy  # line 184
        os.makedirs(os.path.join(_.root, metaFolder, "b%d" % branch, "r0"))  # line 185
        _.loadBranch(_.branch)  # line 186
        revision = max(_.commits)  # type: int  # line 187
        _.computeSequentialPathSet(_.branch, revision)  # full set of files in revision to _.paths  # line 188
        for path, pinfo in _.paths.items():  # line 189
            _.copyVersionedFile(_.branch, revision, branch, 0, pinfo)  # line 190
        _.commits = {0: CommitInfo(0, longint(time.time() * 1000), "Branched from '%s'" % ((lambda _coconut_none_coalesce_item: "b%d" % _.branch if _coconut_none_coalesce_item is None else _coconut_none_coalesce_item)(_.branches[_.branch].name)))}  # store initial commit  # line 191
        _.saveBranch(branch)  # save branch meta data to branch folder  # line 192
        _.saveCommit(branch, 0)  # save commit meta data to revision folder  # line 193
        _.branches[branch] = BranchInfo(branch, _.commits[0].ctime, name, _.branches[_.branch].insync, tracked)  # save branch info, before storing repo state at caller  # line 194

    def createBranch(_, branch: 'int', name: '_coconut.typing.Optional[str]'=None, initialMessage: '_coconut.typing.Optional[str]'=None):  # line 196
        ''' Create a new branch from current file tree. This clears all known commits and modifies the file system.
        branch: target branch (should not exist yet)
        name: optional name of new branch
        _.branch: current branch, must exist already
    '''  # line 201
        simpleMode = not (_.track or _.picky)  # line 202
        tracked = [t for t in _.branches[_.branch].tracked] if _.track and len(_.branches) > 0 else []  # in case of initial branch creation  # line 203
        debug((lambda _coconut_none_coalesce_item: "b%d" % branch if _coconut_none_coalesce_item is None else _coconut_none_coalesce_item)("Creating branch '%s'..." % name))  # line 204
        _.paths = {}  # type: Dict[str, PathInfo]  # line 205
        if simpleMode:  # branches from file system state  # line 206
            changes = _.findChanges(branch, 0, progress=simpleMode)  # type: ChangeSet  # creates revision folder and versioned files  # line 207
            _.listChanges(changes)  # line 208
            _.paths.update(changes.additions.items())  # line 209
        else:  # tracking or picky mode: branch from lastest revision  # line 210
            os.makedirs(os.path.join(_.root, metaFolder, "b%d" % branch, "r0"))  # line 211
            if _.branch is not None:  # not immediately after "offline" - copy files from current branch  # line 212
                _.loadBranch(_.branch)  # line 213
                revision = max(_.commits)  # type: int  # TODO what if last switch was to an earlier revision? no persisting of last checkout  # line 214
                _.computeSequentialPathSet(_.branch, revision)  # full set of files in revision to _.paths  # line 215
                for path, pinfo in _.paths.items():  # line 216
                    _.copyVersionedFile(_.branch, revision, branch, 0, pinfo)  # line 217
        ts = longint(time.time() * 1000)  # line 218
        _.commits = {0: CommitInfo(0, ts, "Branched on %s" % strftime(ts) if initialMessage is None else initialMessage)}  # store initial commit for new branch  # line 219
        _.saveBranch(branch)  # save branch meta data (revisions) to branch folder  # line 220
        _.saveCommit(branch, 0)  # save commit meta data to revision folder  # line 221
        _.branches[branch] = BranchInfo(branch, _.commits[0].ctime, name, True if len(_.branches) == 0 else _.branches[_.branch].insync, tracked)  # save branch info, in case it is needed  # line 222

    def removeBranch(_, branch: 'int') -> 'BranchInfo':  # line 224
        ''' Entirely remove a branch and all its revisions from the file system. '''  # line 225
        shutil.rmtree(os.path.join(_.root, metaFolder, "b%d" % branch))  # line 226
        binfo = _.branches[branch]  # line 227
        del _.branches[branch]  # line 228
        _.branch = max(_.branches)  # line 229
        _.saveBranches()  # line 230
        _.commits.clear()  # line 231
        return binfo  # line 232

    def loadCommit(_, branch: 'int', revision: 'int') -> 'None':  # line 234
        ''' Load all file information from a commit meta data. '''  # line 235
        with codecs.open(os.path.join(_.root, metaFolder, "b%d" % branch, "r%d" % revision, metaFile), "r", encoding=UTF8) as fd:  # line 236
            _.paths = json.load(fd)  # line 237
        _.paths = {path: PathInfo(*item) for path, item in _.paths.items()}  # re-create type info  # line 238
        _.branch = branch  # line 239

    def saveCommit(_, branch: 'int', revision: 'int'):  # line 241
        ''' Save all file information to a commit meta data file. '''  # line 242
        target = os.path.join(_.root, metaFolder, "b%d" % branch, "r%d" % revision)  # line 243
        try:  # line 244
            os.makedirs(target)  # line 244
        except:  # line 245
            pass  # line 245
        with codecs.open(os.path.join(target, metaFile), "w", encoding=UTF8) as fd:  # line 246
            json.dump(_.paths, fd, ensure_ascii=False)  # line 247

    def findChanges(_, branch: '_coconut.typing.Optional[int]'=None, revision: '_coconut.typing.Optional[int]'=None, checkContent: 'bool'=False, inverse: 'bool'=False, considerOnly: '_coconut.typing.Optional[FrozenSet[str]]'=None, dontConsider: '_coconut.typing.Optional[FrozenSet[str]]'=None, progress: 'bool'=False) -> 'ChangeSet':  # line 249
        ''' Find changes on the file system vs. in-memory paths (which should reflect the latest commit state).
        Only if both branch and revision are *not* None, write modified/added files to the specified revision folder (thus creating a new revision)
        The function returns the state of file tree *differences*, unless "inverse" is True -> then return original data
        checkContent: also computes file content hashes
        inverse: retain original state (size, mtime, hash) instead of updated one
        considerOnly: set of tracking patterns. For update operation, consider union of other and current branch
        dontConsider: set of tracking patterns to not consider in changes
        progress: Show file names during processing
    '''  # line 258
        write = branch is not None and revision is not None  # line 259
        if write:  # line 260
            os.makedirs(os.path.join(_.root, metaFolder, "b%d" % branch, "r%d" % revision))  # line 260
        changes = ChangeSet({}, {}, {})  # type: ChangeSet  # line 261
        counter = Counter(-1)  # type: Counter  # line 262
        timer = time.time()  # line 262
        hashed = None  # type: _coconut.typing.Optional[str]  # line 263
        written = None  # type: longint  # line 263
        compressed = 0  # type: longint  # line 263
        original = 0  # type: longint  # line 263
        for path, dirnames, filenames in os.walk(_.root):  # line 264
            dirnames[:] = [f for f in dirnames if len([n for n in _.c.ignoreDirs if fnmatch.fnmatch(f, n)]) == 0 or len([p for p in _.c.ignoreDirsWhitelist if fnmatch.fnmatch(f, p)]) > 0]  # line 265
            filenames[:] = [f for f in filenames if len([n for n in _.c.ignores if fnmatch.fnmatch(f, n)]) == 0 or len([p for p in _.c.ignoresWhitelist if fnmatch.fnmatch(f, p)]) > 0]  # line 266
            dirnames.sort()  # line 267
            filenames.sort()  # line 267
            relpath = os.path.relpath(path, _.root).replace(os.sep, SLASH)  # line 268
            walk = filenames if considerOnly is None else list(reduce(lambda last, pattern: last | set(fnmatch.filter(filenames, os.path.basename(pattern))), (p for p in considerOnly if os.path.dirname(p) == relpath), _coconut.set()))  # line 269
            if dontConsider:  # line 270
                walk[:] = [fn for fn in walk if not any((fnmatch.fnmatch(fn, os.path.basename(p)) for p in dontConsider if os.path.dirname(p) == relpath))]  # TODO dirname is correct noramalized? same above?  # line 271
            for file in walk:  # if m.track or m.picky: only files that match any path-relevant tracking patterns  # line 272
                filename = relpath + SLASH + file  # line 273
                filepath = os.path.join(path, file)  # line 274
                stat = os.stat(filepath)  # line 275
                size, mtime, newtime = stat.st_size, longint(stat.st_mtime * 1000), time.time()  # line 276
                if progress and newtime - timer > .1:  # line 277
                    outstring = "\rPreparing %s  %s" % (PROGRESS_MARKER[counter.inc() % 4], filename)  # line 278
                    sys.stdout.write(outstring + " " * max(0, termWidth - len(outstring)))  # TODO could write to new line instead of carriage return, also needs terminal width  # line 279
                    sys.stdout.flush()  # TODO could write to new line instead of carriage return, also needs terminal width  # line 279
                    timer = newtime  # TODO could write to new line instead of carriage return, also needs terminal width  # line 279
                if filename not in _.paths:  # detected file not present (or untracked) in other branch  # line 280
                    namehash = hashStr(filename)  # line 281
                    hashed, written = hashFile(filepath, _.compress, saveTo=os.path.join(_.root, metaFolder, "b%d" % branch, "r%d" % revision, namehash) if write else None) if size > 0 else (None, 0)  # line 282
                    changes.additions[filename] = PathInfo(namehash, size, mtime, hashed)  # line 283
                    compressed += written  # line 284
                    original += size  # line 284
                    continue  # line 285
                last = _.paths[filename]  # filename is known - check for modifications  # line 286
                if last.size is None:  # was removed before but is now added back - does not apply for tracking mode (which never marks files for removal in the history)  # line 287
                    hashed, written = hashFile(filepath, _.compress, saveTo=os.path.join(_.root, metaFolder, "b%d" % branch, "r%d" % revision, last.namehash) if write else None) if size > 0 else (None, 0)  # line 288
                    changes.additions[filename] = PathInfo(last.namehash, size, mtime, hashed)  # line 289
                    continue  # line 289
                elif size != last.size or mtime != last.mtime or (checkContent and hashFile(filepath, _.compress) != last.hash):  # detected a modification  # line 290
                    hashed, written = hashFile(filepath, _.compress, saveTo=os.path.join(_.root, metaFolder, "b%d" % branch, "r%d" % revision, last.namehash) if write else None) if (last.size if inverse else size) > 0 else (last.hash if inverse else None, 0)  # line 291
                    changes.modifications[filename] = PathInfo(last.namehash, last.size if inverse else size, last.mtime if inverse else mtime, hashed)  # line 292
                else:  # line 293
                    continue  # line 293
                compressed += written  # line 294
                original += last.size if inverse else size  # line 294
# Detect deletions. Files no longer being tracked should not be found here
            for folderPath in (p for p, pinfo in _.paths.items() if p[:p.rindex(SLASH)] == relpath and pinfo.size is not None):  # only versioned (and tracked) files that match currently visited folder. TODO don't check for removal just added entries  # line 296
                if folderPath[len(relpath) + 1:] not in filenames:  # filename no longer in file tree TODO use basename and dirname instead of slicing?  # line 297
                    changes.deletions[folderPath] = _.paths[folderPath]  # filename no longer in file tree TODO use basename and dirname instead of slicing?  # line 297
        if progress:  # force new line  # line 298
            print("\rPreparation finished. Compression factor %s" % ("is %.1f" % (original * 100. / compressed) if compressed > 0 else "cannot be computed").ljust(termWidth), file=sys.stdout)  # force new line  # line 298
        else:  # line 299
            debug("Finished detecting changes. Compression factor %s" % ("is %.1f" % (original * 100. / compressed) if compressed > 0 else "cannot be computed"))  # line 299
        return changes  # line 300

    def integrateChangeset(_, changes: 'ChangeSet', clear=False) -> 'None':  # line 302
        ''' In-memory update from a changeset, marking deleted files with size=None. Use clear = True to start on an empty path set. '''  # line 303
        if clear:  # line 304
            _.paths.clear()  # line 304
        else:  # line 305
            rm = [p for p, info in _.paths.items() if info.size is None]  # remove files deleted in earlier change sets (revisions)  # line 306
            for old in rm:  # remove previously removed entries completely  # line 307
                del _.paths[old]  # remove previously removed entries completely  # line 307
        for d, info in changes.deletions.items():  # mark now removed entries as deleted  # line 308
            _.paths[d] = PathInfo(info.namehash, None, info.mtime, None)  # mark now removed entries as deleted  # line 308
        _.paths.update(changes.additions)  # line 309
        _.paths.update(changes.modifications)  # line 310

    def computeSequentialPathSet(_, branch: 'int', revision: 'int') -> 'None':  # line 312
        next(_.computeSequentialPathSetIterator(branch, revision, incrementally=False))  # simply invoke the generator once  # line 313

    def computeSequentialPathSetIterator(_, branch: 'int', revision: 'int', incrementally: 'bool'=True) -> '_coconut.typing.Optional[Iterator[ChangeSet]]':  # line 315
        ''' In-memory computation of current list of valid PathInfo entries for specified branch and until specified revision (inclusively) by traversing revision on the file system. '''  # line 316
        _.loadCommit(branch, 0)  # load initial paths  # line 317
        if incrementally:  # line 318
            yield diffPathSets({}, _.paths)  # line 318
        n = Metadata(_.root)  # type: Metadata  # next changes  # line 319
        for revision in range(1, revision + 1):  # line 320
            n.loadCommit(branch, revision)  # line 321
            changes = diffPathSets(_.paths, n.paths)  # type: ChangeSet  # line 322
            _.integrateChangeset(changes)  # line 323
            if incrementally:  # line 324
                yield changes  # line 324
        yield None  # for the default case - not incrementally  # line 325

    def parseRevisionString(_, argument: 'str') -> 'Tuple[_coconut.typing.Optional[int], _coconut.typing.Optional[int]]':  # line 327
        ''' Commit identifiers can be str or int for branch, and int for revision.
        Revision identifiers can be negative, with -1 being last commit.
    '''  # line 330
        if argument is None or argument == SLASH:  # no branch/revision specified  # line 331
            return (_.branch, -1)  # no branch/revision specified  # line 331
        argument = argument.strip()  # line 332
        if argument.startswith(SLASH):  # current branch  # line 333
            return (_.branch, _.getRevisionByName(argument[1:]))  # current branch  # line 333
        if argument.endswith(SLASH):  # line 334
            try:  # line 335
                return (_.getBranchByName(argument[:-1]), -1)  # line 335
            except ValueError:  # line 336
                Exit("Unknown branch label")  # line 336
        if SLASH in argument:  # line 337
            b, r = argument.split(SLASH)[:2]  # line 338
            try:  # line 339
                return (_.getBranchByName(b), _.getRevisionByName(r))  # line 339
            except ValueError:  # line 340
                Exit("Unknown branch label or wrong number format")  # line 340
        branch = _.getBranchByName(argument)  # type: int  # returns number if given (revision) integer  # line 341
        if branch not in _.branches:  # line 342
            branch = None  # line 342
        try:  # either branch name/number or reverse/absolute revision number  # line 343
            return (_.branch if branch is None else branch, longint(argument) if branch is None else -1)  # either branch name/number or reverse/absolute revision number  # line 343
        except:  # line 344
            Exit("Unknown branch label or wrong number format")  # line 344
        Exit("This should never happen")  # return (None, None)  # line 345

    def findRevision(_, branch: 'int', revision: 'int', namehash: 'str') -> 'Tuple[int, str]':  # line 347
        while True:  # find latest revision that contained the file physically  # line 348
            source = os.path.join(_.root, metaFolder, "b%d" % branch, "r%d" % revision, namehash)  # type: str  # line 349
            if os.path.exists(source) and os.path.isfile(source):  # line 350
                break  # line 350
            revision -= 1  # line 351
            if revision < 0:  # line 352
                Exit("Cannot determine versioned file '%s' from specified branch '%d'" % (namehash, branch))  # line 352
        return revision, source  # line 353

    def copyVersionedFile(_, branch: 'int', revision: 'int', tobranch: 'int', torevision: 'int', pinfo: 'PathInfo') -> 'None':  # line 355
        ''' Copy versioned file to other branch/revision. '''  # line 356
        target = os.path.join(_.root, metaFolder, "b%d" % tobranch, "r%d" % torevision, pinfo.namehash)  # type: str  # line 357
        revision, source = _.findRevision(branch, revision, pinfo.namehash)  # line 358
        shutil.copy2(source, target)  # line 359

    def readOrCopyVersionedFile(_, branch: 'int', revision: 'int', namehash: 'str', toFile: '_coconut.typing.Optional[str]'=None) -> '_coconut.typing.Optional[bytes]':  # line 361
        ''' Return file contents, or copy contents into file path provided. '''  # line 362
        source = os.path.join(_.root, metaFolder, "b%d" % branch, "r%d" % revision, namehash)  # type: str  # line 363
        try:  # line 364
            with openIt(source, "r", _.compress) as fd:  # line 365
                if toFile is None:  # read bytes into memory and return  # line 366
                    return fd.read()  # read bytes into memory and return  # line 366
                with open(toFile, "wb") as to:  # line 367
                    while True:  # line 368
                        buffer = fd.read(bufSize)  # line 369
                        to.write(buffer)  # line 370
                        if len(buffer) < bufSize:  # line 371
                            break  # line 371
                    return None  # line 372
        except Exception as E:  # line 373
            warn("Cannot read versioned file: %r (%d/%d/%s)" % (E, branch, revision, namehash))  # line 373
        return None  # line 374

    def restoreFile(_, relpath: '_coconut.typing.Optional[str]', branch: 'int', revision: 'int', pinfo: 'PathInfo') -> '_coconut.typing.Optional[bytes]':  # line 376
        ''' Recreate file for given revision, or return contents if path is None. '''  # line 377
        if relpath is None:  # just return contents  # line 378
            return _.readOrCopyVersionedFile(branch, _.findRevision(branch, revision, pinfo.namehash)[0], pinfo.namehash) if pinfo.size > 0 else b''  # just return contents  # line 378
        target = os.path.join(_.root, relpath.replace(SLASH, os.sep))  # type: str  # line 379
        if pinfo.size == 0:  # line 380
            with open(target, "wb"):  # line 381
                pass  # line 381
            try:  # update access/modification timestamps on file system  # line 382
                os.utime(target, (-1, pinfo.mtime / 1000.))  # update access/modification timestamps on file system  # line 382
            except Exception as E:  # line 383
                error("Cannot update file's timestamp after restoration '%r'" % E)  # line 383
            return None  # line 384
        revision, source = _.findRevision(branch, revision, pinfo.namehash)  # line 385
# Restore file by copying buffer-wise
        with openIt(source, "r", _.compress) as fd, open(target, "wb") as to:  # using Coconut's Enhanced Parenthetical Continuation  # line 387
            while True:  # line 388
                buffer = fd.read(bufSize)  # line 389
                to.write(buffer)  # line 390
                if len(buffer) < bufSize:  # line 391
                    break  # line 391
        try:  # update access/modification timestamps on file system  # line 392
            os.utime(target, (-1, pinfo.mtime / 1000.))  # update access/modification timestamps on file system  # line 392
        except Exception as E:  # line 393
            error("Cannot update file's timestamp after restoration '%r'" % E)  # line 393
        return None  # line 394

    def getTrackingPatterns(_, branch: '_coconut.typing.Optional[int]'=None) -> 'FrozenSet[str]':  # line 396
        ''' Returns list of tracking patterns for provided branch or current branch. '''  # line 397
        return _coconut.frozenset() if not _.track and not _.picky else frozenset(_.branches[_.branch if branch is None else branch].tracked)  # line 398


# Main client operations
def offline(argument: '_coconut.typing.Optional[str]'=None, options: '_coconut.typing.Sequence[str]'=[]) -> 'None':  # line 402
    ''' Initial command to start working offline. '''  # line 403
    if os.path.exists(metaFolder):  # line 404
        if '--force' not in options:  # line 405
            Exit("Repository folder is either already offline or older branches and commits were left over.\nUse 'sos online' to check for dirty branches, or\nWipe existing offline branches with 'sos offline --force'")  # line 405
        try:  # line 406
            for entry in os.listdir(metaFolder):  # line 407
                resource = metaFolder + os.sep + entry  # line 408
                if os.path.isdir(resource):  # line 409
                    shutil.rmtree(resource)  # line 409
                else:  # line 410
                    os.unlink(resource)  # line 410
        except:  # line 411
            Exit("Cannot reliably remove previous repository contents. Please remove .sos folder manually prior to going offline")  # line 411
    m = Metadata(os.getcwd())  # type: Metadata  # line 412
    if '--plain' in options or not m.c.compress:  # plain file copies instead of compressed ones  # line 413
        m.compress = False  # plain file copies instead of compressed ones  # line 413
    if '--picky' in options or m.c.picky:  # Git-like  # line 414
        m.picky = True  # Git-like  # line 414
    elif '--track' in options or m.c.track:  # Svn-like  # line 415
        m.track = True  # Svn-like  # line 415
    if '--strict' in options or m.c.strict:  # always hash contents  # line 416
        m.strict = True  # always hash contents  # line 416
    debug("Preparing offline repository...")  # line 417
    m.createBranch(0, str(defaults["defaultbranch"]) if argument is None else argument, initialMessage="Offline repository created on %s" % strftime())  # main branch's name may be None (e.g. for fossil)  # line 418
    m.branch = 0  # line 419
    m.saveBranches()  # no change immediately after going offline, going back online won't issue a warning  # line 420
    info("Offline repository prepared. Use 'sos online' to finish offline work")  # line 421

def online(options: '_coconut.typing.Sequence[str]'=[]) -> 'None':  # line 423
    ''' Finish working offline. '''  # line 424
    force = '--force' in options  # type: bool  # line 425
    m = Metadata(os.getcwd())  # line 426
    m.loadBranches()  # line 427
    if any([not b.insync for b in m.branches.values()]) and not force:  # line 428
        Exit("There are still unsynchronized (dirty) branches.\nUse 'sos log' to list them.\nUse 'sos commit' and 'sos switch' to commit dirty branches to your VCS before leaving offline mode.\nUse 'sos online --force' to erase all aggregated offline revisions.")  # line 428
    strict = '--strict' in options or m.strict  # type: bool  # line 429
    if options.count("--force") < 2:  # line 430
        changes = m.findChanges(checkContent=strict, considerOnly=None if not m.track else m.getTrackingPatterns())  # type: ChangeSet  # HINT no option for --only/--except here on purpose. No check for picky here, because online is not a command that considers staged files (but we could use --only here, alternatively)  # line 431
        if modified(changes):  # line 432
            Exit("File tree is modified vs. current branch.\nUse 'sos online --force --force' to continue with removing the offline repository.")  # line 432
    try:  # line 433
        shutil.rmtree(metaFolder)  # line 433
        info("Exited offline mode. Continue working with your traditional VCS.")  # line 433
    except Exception as E:  # line 434
        Exit("Error removing offline repository: %r" % E)  # line 434

def branch(argument: '_coconut.typing.Optional[str]'=None, options: '_coconut.typing.Sequence[str]'=[]) -> 'None':  # line 436
    ''' Create a new branch (from file tree or last revision) and (by default) continue working on it. '''  # line 437
    last = '--last' in options  # type: bool  # use last revision for branching, not current file tree  # line 438
    stay = '--stay' in options  # type: bool  # continue on current branch after branching  # line 439
    force = '--force' in options  # type: bool  # branch even with local modifications  # line 440
    m = Metadata(os.getcwd())  # type: Metadata  # line 441
    m.loadBranches()  # line 442
    if argument and m.getBranchByName(argument) is not None:  # create a named branch  # line 443
        Exit("Branch '%s' already exists. Cannot proceed" % argument)  # create a named branch  # line 443
    branch = max(m.branches.keys()) + 1  # next branch's key - this isn't atomic but we assume single-user non-concurrent use here  # line 444
    debug("Branching to %sbranch b%02d%s%s..." % ("unnamed " if argument is None else "", branch, " '%s'" % argument if argument else "", " from last revision" if last else ""))  # line 445
    if last:  # line 446
        m.duplicateBranch(branch, argument)  # branch from branch's last revision  # line 447
    else:  # from file tree state  # line 448
        m.createBranch(branch, argument)  # branch from current file tree  # line 449
    if not stay:  # line 450
        m.branch = branch  # line 451
        m.saveBranches()  # line 452
    info("%s new %sbranch b%02d%s" % ("Continue work after branching" if stay else "Switched to", "unnamed " if argument is None else "", branch, " '%s'" % argument if argument else ""))  # line 453

def changes(argument: 'str'=None, options: '_coconut.typing.Sequence[str]'=[], onlys: '_coconut.typing.Optional[FrozenSet[str]]'=None, excps: '_coconut.typing.Optional[FrozenSet[str]]'=None) -> 'ChangeSet':  # line 455
    ''' Show changes of file tree vs. (last or specified) revision on current or specified branch. '''  # line 456
    m = Metadata(os.getcwd())  # type: Metadata  # line 457
    branch = None  # type: _coconut.typing.Optional[int]  # line 457
    revision = None  # type: _coconut.typing.Optional[int]  # line 457
    m.loadBranches()  # knows current branch  # line 458
    strict = '--strict' in options or m.strict  # type: bool  # line 459
    branch, revision = m.parseRevisionString(argument)  # line 460
    if branch not in m.branches:  # line 461
        Exit("Unknown branch")  # line 461
    m.loadBranch(branch)  # knows commits  # line 462
    revision = revision if revision >= 0 else len(m.commits) + revision  # negative indexing  # line 463
    if revision < 0 or revision > max(m.commits):  # line 464
        Exit("Unknown revision r%02d" % revision)  # line 464
    info("//|\\\\ Changes of file tree vs. revision '%s/r%02d'" % ((lambda _coconut_none_coalesce_item: "b%02d" % branch if _coconut_none_coalesce_item is None else _coconut_none_coalesce_item)(m.branches[branch].name), revision))  # line 465
    m.computeSequentialPathSet(branch, revision)  # load all commits up to specified revision  # line 466
    changes = m.findChanges(checkContent=strict, considerOnly=onlys if not m.track else conditionalIntersection(onlys, m.getTrackingPatterns() | m.getTrackingPatterns(branch)), dontConsider=excps)  # type: ChangeSet  # line 467
    m.listChanges(changes)  # line 468
    return changes  # line 469

def diff(argument: 'str', options: '_coconut.typing.Sequence[str]'=[], onlys: '_coconut.typing.Optional[FrozenSet[str]]'=None, excps: '_coconut.typing.Optional[FrozenSet[str]]'=None) -> 'None':  # line 471
    ''' Show text file differences of file tree vs. (last or specified) revision on current or specified branch. '''  # line 472
    m = Metadata(os.getcwd())  # type: Metadata  # line 473
    branch = None  # type: _coconut.typing.Optional[int]  # line 473
    revision = None  # type: _coconut.typing.Optional[int]  # line 473
    m.loadBranches()  # knows current branch  # line 474
    strict = '--strict' in options or m.strict  # type: bool  # line 475
    branch, revision = m.parseRevisionString(argument)  # line 476
    if branch not in m.branches:  # line 477
        Exit("Unknown branch")  # line 477
    m.loadBranch(branch)  # knows commits  # line 478
    revision = revision if revision >= 0 else len(m.commits) + revision  # negative indexing  # line 479
    if revision < 0 or revision > max(m.commits):  # line 480
        Exit("Unknown revision r%02d" % revision)  # line 480
    info("//|\\\\ Differences of file tree vs. revision '%s/r%02d'" % ((lambda _coconut_none_coalesce_item: "b%02d" % branch if _coconut_none_coalesce_item is None else _coconut_none_coalesce_item)(m.branches[branch].name), revision))  # line 481
    m.computeSequentialPathSet(branch, revision)  # load all commits up to specified revision  # line 482
    changes = m.findChanges(checkContent=strict, inverse=True, considerOnly=onlys if not m.track else conditionalIntersection(onlys, m.getTrackingPatterns() | m.getTrackingPatterns(branch)), dontConsider=excps)  # type: ChangeSet  # line 483
    onlyBinaryModifications = dataCopy(ChangeSet, changes, modifications={k: v for k, v in changes.modifications.items() if not m.isTextType(k)})  # type: ChangeSet  # line 484
    if modified(onlyBinaryModifications):  # line 485
        debug("//|\\\\ File changes")  # line 485
    m.listChanges(onlyBinaryModifications)  # only list modified binary files  # line 486

    if changes.modifications:  # TODO only text files, not binary  # line 488
        debug("%s//|\\\\ Textual modifications" % ("\n" if modified(onlyBinaryModifications) else ""))  # TODO only text files, not binary  # line 488
    for path, pinfo in changes.modifications.items():  # only consider modified files TODO also show A/D here? or replace listing above?  # line 489
        content = None  # type: _coconut.typing.Optional[bytes]  # ; othr:str[]; curr:str[]  # line 490
        if pinfo.size == 0:  # empty file contents  # line 491
            content = b""  # empty file contents  # line 491
        else:  # versioned file  # line 492
            content = m.restoreFile(None, branch, revision, pinfo)  # versioned file  # line 492
            assert content is not None  # versioned file  # line 492
        abspath = os.path.join(m.root, path.replace(SLASH, os.sep))  # current file  # line 493
        blocks = merge(file=content, intoname=abspath, diffOnly=True)  # type: List[MergeBlock]  # only determine change blocks  # line 494
        print("DIF %s%s" % (path, " <timestamp only>" if len(blocks) == 1 and blocks[0].tipe == MergeBlockType.KEEP else ""))  # line 495
        for block in blocks:  # line 496
            if block.tipe in [MergeBlockType.INSERT, MergeBlockType.REMOVE]:  # line 497
                pass  # TODO print some previous and following lines - which aren't accessible here anymore  # line 498
            if block.tipe == MergeBlockType.INSERT:  # TODO show color via curses?  # line 499
                for no, line in enumerate(block.lines):  # line 500
                    print("+++ %04d |%s|" % (no + block.line, line))  # line 501
            elif block.tipe == MergeBlockType.REMOVE:  # line 502
                for no, line in enumerate(block.lines):  # line 503
                    print("--- %04d |%s|" % (no + block.line, line))  # line 504
            elif block.tipe in [MergeBlockType.REPLACE, MergeBlockType.MODIFY]:  # TODO for MODIFY also show intra-line change ranges  # line 505
                for no, line in enumerate(block.replaces.lines):  # line 506
                    print("- | %04d |%s|" % (no + block.replaces.line, line))  # line 507
                for no, line in enumerate(block.lines):  # line 508
                    print("+ | %04d |%s|" % (no + block.line, line))  # line 509
#      elif block.tipe == MergeBlockType.KEEP: pass
#      elif block.tipe == MergeBlockType.MODIFY:  # intra-line modifications
#      elif block.tipe == MergeBlockType.MOVE:  # intra-line modifications

def commit(argument: '_coconut.typing.Optional[str]'=None, options: '_coconut.typing.Sequence[str]'=[], onlys: '_coconut.typing.Optional[FrozenSet[str]]'=None, excps: '_coconut.typing.Optional[FrozenSet[str]]'=None) -> 'None':  # line 514
    ''' Create new revision from file tree changes vs. last commit. '''  # line 515
    m = Metadata(os.getcwd())  # type: Metadata  # line 516
    m.loadBranches()  # knows current branch  # line 517
    if argument is not None and argument in m.tags:  # line 518
        Exit("Illegal commit message. It was already used as a tag name")  # line 518
    trackingPatterns = m.getTrackingPatterns()  # type: FrozenSet[str]  # SVN-like mode  # line 519
    if m.picky and not trackingPatterns:  # line 520
        Exit("No file patterns staged for commit in picky mode")  # line 520
    changes = None  # type: ChangeSet  # line 521
    m, branch, revision, changes, strict, force, trackingPatterns = exitOnChanges(None, options, commit=True, onlys=onlys, excps=excps)  # special flag creates new revision for detected changes, but abort if no changes  # line 522
    info((lambda _coconut_none_coalesce_item: "b%d" % m.branch if _coconut_none_coalesce_item is None else _coconut_none_coalesce_item)("Committing changes to branch '%s'..." % m.branches[m.branch].name))  # line 523
    m.integrateChangeset(changes, clear=True)  # update pathset to changeset only  # line 524
    m.saveCommit(m.branch, revision)  # revision has already been incremented  # line 525
    m.commits[revision] = CommitInfo(revision, longint(time.time() * 1000), argument)  # comment can be None  # line 526
    m.saveBranch(m.branch)  # line 527
    m.loadBranches()  # TODO is it necessary to load again?  # line 528
    if m.picky:  # HINT was changed from only picky to include track as well  # line 529
        m.branches[m.branch] = dataCopy(BranchInfo, m.branches[m.branch], tracked=[], insync=False)  # remove tracked patterns  # line 530
    else:  # track or simple mode  # line 531
        m.branches[m.branch] = dataCopy(BranchInfo, m.branches[m.branch], insync=False)  # set branch dirty  # line 532
    if "--tag" in options and argument is not None:  # memorize unique tag  # line 533
        m.tags.append(argument)  # memorize unique tag  # line 533
    m.saveBranches()  # line 534
    info("Created new revision r%02d%s (+%02d/-%02d/*%02d)" % (revision, ((" '%s'" % argument) if argument is not None else ""), len(changes.additions), len(changes.deletions), len(changes.modifications)))  # line 535

def status() -> 'None':  # line 537
    ''' Show branches and current repository state. '''  # line 538
    m = Metadata(os.getcwd())  # type: Metadata  # line 539
    m.loadBranches()  # knows current branch  # line 540
    current = m.branch  # type: int  # line 541
    info("//|\\\\ Offline repository status")  # line 542
    sl = max([len((lambda _coconut_none_coalesce_item: "" if _coconut_none_coalesce_item is None else _coconut_none_coalesce_item)(b.name)) for b in m.branches.values()])  # type: int  # line 543
    for branch in sorted(m.branches.values(), key=lambda b: b.number):  # line 544
        m.loadBranch(branch.number)  # knows commit history  # line 545
        print("  %s b%02d%s @%s (%s) with %d commits%s" % ("*" if current == branch.number else " ", branch.number, ((" %%%ds" % (sl + 2)) % ("'%s'" % branch.name)) if branch.name else "", strftime(branch.ctime), "in sync" if branch.insync else "dirty", len(m.commits), ". Last comment: '%s'" % m.commits[max(m.commits)].message if m.commits[max(m.commits)].message else ""))  # line 546
    if m.track or m.picky and len(m.branches[m.branch].tracked) > 0:  # line 547
        info("\nTracked file patterns:")  # line 548
        print(ajoin("  | ", m.branches[m.branch].tracked, "\n"))  # line 549

def exitOnChanges(argument: '_coconut.typing.Optional[str]'=None, options: '_coconut.typing.Sequence[str]'=[], check: 'bool'=True, commit: 'bool'=False, onlys: '_coconut.typing.Optional[FrozenSet[str]]'=None, excps: '_coconut.typing.Optional[FrozenSet[str]]'=None) -> 'Tuple[Metadata, _coconut.typing.Optional[int], int, ChangeSet, bool, bool, FrozenSet[str]]':  # line 551
    ''' Common behavior for switch, update, delete, commit.
      Should not be called for picky mode, unless tracking patterns were added.
      check: stop program on detected change
      commit: don't stop on changes, because that's what we need in the operation
      Returns (Metadata, (current or target) branch, revision, set of changes vs. last commit on current branch, strict, force flags. '''  # line 556
    m = Metadata(os.getcwd())  # type: Metadata  # line 557
    m.loadBranches()  # knows current branch  # line 558
    force = '--force' in options  # type: bool  # line 559
    strict = '--strict' in options or m.strict  # type: bool  # line 560
    if argument is not None:  # line 561
        branch, revision = m.parseRevisionString(argument)  # for early abort  # line 562
        if branch is None:  # line 563
            Exit("Branch '%s' doesn't exist. Cannot proceed" % argument)  # line 563
    m.loadBranch(m.branch)  # knows last commits of *current* branch  # line 564

# Determine current changes
    trackingPatterns = m.getTrackingPatterns()  # type: FrozenSet[str]  # line 567
    m.computeSequentialPathSet(m.branch, max(m.commits))  # load all commits up to specified revision  # line 568
    changes = m.findChanges(m.branch if commit else None, max(m.commits) + 1 if commit else None, checkContent=strict, considerOnly=onlys if not m.track and not m.picky else conditionalIntersection(onlys, trackingPatterns), dontConsider=excps)  # type: ChangeSet  # line 569
    if modified(changes) and not force:  # and check?  # line 570
        m.listChanges(changes)  # line 571
        if check and not commit:  # line 572
            Exit("File tree contains changes. Use --force to proceed")  # line 572
    elif commit and not force:  #  and not check  # line 573
        Exit("Nothing to commit")  #  and not check  # line 573

    if argument is not None:  # branch/revision specified  # line 575
        m.loadBranch(branch)  # knows commits of target branch  # line 576
        revision = revision if revision >= 0 else len(m.commits) + revision  # negative indexing  # line 577
        if revision < 0 or revision > max(m.commits):  # line 578
            Exit("Unknown revision r%02d" % revision)  # line 578
        return (m, branch, revision, changes, strict, force, m.getTrackingPatterns(branch))  # line 579
    return (m, m.branch, max(m.commits) + (1 if commit else 0), changes, strict, force, trackingPatterns)  # line 580

def switch(argument: 'str', options: '_coconut.typing.Sequence[str]'=[], onlys: '_coconut.typing.Optional[FrozenSet[str]]'=None, excps: '_coconut.typing.Optional[FrozenSet[str]]'=None) -> 'None':  # line 582
    ''' Continue work on another branch, replacing file tree changes. '''  # line 583
    changes = None  # type: ChangeSet  # line 584
    m, branch, revision, changes, strict, force, trackingPatterns = exitOnChanges(argument, options)  # line 585
    info("//|\\\\ Switching to branch %sb%02d/r%02d" % ("'%s' " % m.branches[branch].name if m.branches[branch].name else "", branch, revision))  # line 586

# Determine file changes from other branch to current file tree
    if '--meta' in options:  # only switch meta data  # line 589
        m.branches[m.branch] = dataCopy(BranchInfo, m.branches[m.branch], tracked=m.branches[branch].tracked)  # line 590
    else:  # full file switch  # line 591
        m.computeSequentialPathSet(branch, revision)  # load all commits up to specified revision for target branch into memory  # line 592
        changes = m.findChanges(checkContent=strict, inverse=True, considerOnly=onlys if not m.track else conditionalIntersection(onlys, trackingPatterns | m.getTrackingPatterns(branch)), dontConsider=excps)  # determine difference of other branch vs. file tree (forced or in sync with current branch; "addition" means exists now and should be removed)  # line 593
        if not modified(changes):  # line 594
            info("No changes to current file tree")  # line 595
        else:  # integration required  # line 596
            for path, pinfo in changes.deletions.items():  # line 597
                m.restoreFile(path, branch, revision, pinfo)  # is deleted in current file tree: restore from branch to reach target  # line 598
                print("ADD " + path)  # line 599
            for path, pinfo in changes.additions.items():  # line 600
                os.unlink(os.path.join(m.root, path.replace(SLASH, os.sep)))  # is added in current file tree: remove from branch to reach target  # line 601
                print("DEL " + path)  # line 602
            for path, pinfo in changes.modifications.items():  # line 603
                m.restoreFile(path, branch, revision, pinfo)  # is modified in current file tree: restore from branch to reach target  # line 604
                print("MOD " + path)  # line 605
    m.branch = branch  # line 606
    m.saveBranches()  # store switched path info  # line 607
    info("Switched to branch %sb%02d/r%02d" % ("'%s' " % (m.branches[branch].name if m.branches[branch].name else ""), branch, revision))  # line 608

def update(argument: 'str', options: '_coconut.typing.Sequence[str]'=[], onlys: '_coconut.typing.Optional[FrozenSet[str]]'=None, excps: '_coconut.typing.Optional[FrozenSet[str]]'=None) -> 'None':  # line 610
    ''' Load and integrate a specified other branch/revision into current life file tree.
      In tracking mode, this also updates the set of tracked patterns.
      User options for merge operation: --add (don't remove), --rm (don't insert), --add-lines/--rm-lines (inside each file)
      User options for conflict resolution: --theirs/--mine/--ask
  '''  # line 615
    mrg = firstOfMap({"--add": MergeOperation.INSERT, "--rm": MergeOperation.REMOVE}, options, MergeOperation.BOTH)  # type: int  # default operation is replicate remove state for non-conflicting cases (insertions/deletions)  # line 616
    res = firstOfMap({'--theirs': ConflictResolution.THEIRS, '--mine': ConflictResolution.MINE}, options, ConflictResolution.NEXT)  # type: int  # NEXT means deeper level  # line 617
    mrgline = firstOfMap({'--add-lines': MergeOperation.INSERT, '--rm-lines': MergeOperation.REMOVE}, options, mrg)  # type: int  # default operation for modified files is same as for files  # line 618
    resline = firstOfMap({'--theirs-lines': ConflictResolution.THEIRS, '--mine-lines': ConflictResolution.MINE}, options, ConflictResolution.ASK)  # type: int  # line 619
    m = Metadata(os.getcwd())  # type: Metadata  # TODO same is called inside stop on changes - could return both current and designated branch instead  # line 620
    m.loadBranches()  # line 621
    changes = None  # type: ChangeSet  # line 621
    currentBranch = m.branch  # type: _coconut.typing.Optional[int]  # line 622
    m, branch, revision, changes, strict, force, trackingPatterns = exitOnChanges(argument, options, check=False, onlys=onlys, excps=excps)  # don't check for current changes, only parse arguments  # line 623
    debug("Integrating changes from '%s/r%02d' into file tree..." % ((lambda _coconut_none_coalesce_item: "b%02d" % branch if _coconut_none_coalesce_item is None else _coconut_none_coalesce_item)(m.branches[branch].name), revision))  # line 624

# Determine file changes from other branch over current file tree
    m.computeSequentialPathSet(branch, revision)  # load all commits up to specified revision for branch to integrate  # line 627
    trackingUnion = trackingPatterns | m.getTrackingPatterns(branch)  # type: FrozenSet[str]  # line 628
    changes = m.findChanges(checkContent=strict, inverse=True, considerOnly=onlys if not m.track else conditionalIntersection(onlys, trackingUnion), dontConsider=excps)  # determine difference of other branch vs. file tree. "addition" means exists now but not in other, and should be removed unless in tracking mode  # line 629
    if not (mrg & MergeOperation.INSERT and changes.additions or (mrg & MergeOperation.REMOVE and changes.deletions) or changes.modifications):  # line 630
        if trackingUnion == trackingPatterns:  # nothing added  # line 631
            info("No file changes detected, but tracking patterns were merged (run 'sos switch /-1 --meta' to undo)")  # TODO write test to see if this works  # line 632
        else:  # line 633
            info("Nothing to update")  # but write back updated branch info below  # line 634
    else:  # integration required  # line 635
        for path, pinfo in changes.deletions.items():  # deletions mark files not present in current file tree -> needs additon  # line 636
            if mrg & MergeOperation.INSERT:  # deleted in current file tree: restore from branch to reach target  # line 637
                m.restoreFile(path, branch, revision, pinfo)  # deleted in current file tree: restore from branch to reach target  # line 637
            print("ADD " + path if mrg & MergeOperation.INSERT else "(A) " + path)  # line 638
        for path, pinfo in changes.additions.items():  # line 639
            if m.track or m.picky:  # because untracked files of other branch cannot be detected (which is good)  # line 640
                Exit("This should never happen")  # because untracked files of other branch cannot be detected (which is good)  # line 640
            if mrg & MergeOperation.REMOVE:  # line 641
                os.unlink(m.root + os.sep + path.replace(SLASH, os.sep))  # line 641
            print("DEL " + path if mrg & MergeOperation.REMOVE else "(D) " + path)  # not contained in other branch, but maybe kept  # line 642
        for path, pinfo in changes.modifications.items():  # line 643
            into = os.path.join(m.root, path.replace(SLASH, os.sep))  # type: str  # line 644
            binary = not m.isTextType(path)  # line 645
            if res & ConflictResolution.ASK or (binary and res == ConflictResolution.NEXT):  # TODO this may ask user even if no interaction was asked for (check line level for interactivity fist)  # line 646
                print(("MOD " + path if not binary else "BIN ") + path)  # line 647
                reso = {"i": ConflictResolution.MINE, "t": ConflictResolution.THEIRS, "m": ConflictResolution.NEXT}.get(user_input(" Resolve: *M[I]ne, [T]heirs, [M]erge: (I)").strip().lower(), ConflictResolution.MINE)  # line 648
                debug("User selected %d" % reso)  # line 649
            else:  # line 650
                reso = res  # line 650
            if reso & ConflictResolution.THEIRS:  # line 651
                m.readOrCopyVersionedFile(branch, revision, pinfo.namehash, toFile=into)  # blockwise copy of contents  # line 652
                print("THR " + path)  # line 653
            elif reso & ConflictResolution.MINE:  # line 654
                print("MNE " + path)  # nothing to do! same as skip  # line 655
            else:  # NEXT: line-based merge  # line 656
                file = m.readOrCopyVersionedFile(branch, revision, pinfo.namehash) if pinfo.size > 0 else b''  # type: _coconut.typing.Optional[bytes]  # parse lines TODO decode etc.  # line 657
                if file is not None:  # if None, error message was already logged  # line 658
                    contents = merge(file=file, intoname=into, mergeOperation=mrgline, conflictResolution=resline)  # type: bytes  # line 659
                    with open(path, "wb") as fd:  # TODO write to temp file first  # line 660
                        fd.write(contents)  # TODO write to temp file first  # line 660
    info("Integrated changes from '%s/r%02d' into file tree" % ((lambda _coconut_none_coalesce_item: "b%02d" % branch if _coconut_none_coalesce_item is None else _coconut_none_coalesce_item)(m.branches[branch].name), revision))  # line 661
    m.branches[currentBranch] = dataCopy(BranchInfo, m.branches[currentBranch], insync=False, tracked=list(trackingUnion))  # TODO really? it's a change that cannot be undone easily by the user  # line 662
    m.branch = currentBranch  # need to restore setting before saving TODO operate on different objects instead  # line 663
    m.saveBranches()  # line 664

def delete(argument: 'str', options: '_coconut.typing.Sequence[str]'=[]) -> 'None':  # line 666
    ''' Remove a branch entirely. '''  # line 667
    m, branch, revision, changes, strict, force, trackingPatterns = exitOnChanges(None, options)  # line 668
    if len(m.branches) == 1:  # line 669
        Exit("Cannot remove the only remaining branch. Use 'sos online' to leave offline mode")  # line 669
    branch, revision = m.parseRevisionString(argument)  # not from exitOnChanges, because we have to set argument to None there  # line 670
    if branch is None or branch not in m.branches:  # line 671
        Exit("Unknown branch")  # line 671
    debug("Removing branch %d%s..." % (branch, " '%s'" % m.branches[branch].name if m.branches[branch].name else ""))  # line 672
    binfo = m.removeBranch(branch)  # need to keep a reference to removed entry for output below  # line 673
    info("Branch b%02d%s removed" % (branch, " '%s'" % binfo.name if binfo.name else ""))  # line 674

def add(relpath: 'str', pattern: 'str', options: '_coconut.typing.Sequence[str]'=[]) -> 'None':  # line 676
    ''' Add a tracked files pattern to current branch's tracked files. '''  # line 677
    force = '--force' in options  # type: bool  # line 678
    m = Metadata(os.getcwd())  # type: Metadata  # line 679
    m.loadBranches()  # line 680
    if not m.track and not m.picky:  # line 681
        Exit("Repository is in simple mode. Use 'offline --track' or 'offline --picky' instead")  # line 681
    if pattern in m.branches[m.branch].tracked:  # line 682
        Exit("Pattern '%s' already tracked" % pattern)  # line 682
    if not force and len(fnmatch.filter(os.listdir(os.path.abspath(relpath)), os.path.basename(pattern.replace(SLASH, os.sep)))) == 0:  # doesn't match any current file  # line 683
        Exit("Pattern doesn't match any file in specified folder. Use --force to add it anyway")  # line 684
    m.branches[m.branch].tracked.append(pattern)  # TODO set insync flag to False? same for rm  # line 685
    m.saveBranches()  # line 686
    info("Added tracking pattern '%s' for folder '%s'" % (os.path.basename(pattern.replace(SLASH, os.sep)), os.path.abspath(relpath)))  # line 687

def rm(relpath: 'str', pattern: 'str') -> 'None':  # line 689
    ''' Remove a tracked files pattern from current branch's tracked files. '''  # line 690
    m = Metadata(os.getcwd())  # type: Metadata  # line 691
    m.loadBranches()  # line 692
    if not m.track and not m.picky:  # line 693
        Exit("Repository is in simple mode. Needs 'offline --track' or 'offline --picky' instead")  # line 693
    if pattern not in m.branches[m.branch].tracked:  # line 694
        suggestion = _coconut.set()  # type: Set[str]  # line 695
        for pat in m.branches[m.branch].tracked:  # line 696
            if fnmatch.fnmatch(pattern, pat):  # line 697
                suggestion.add(pat)  # line 697
        if suggestion:  # line 698
            print("Do you mean any of the following tracked globs? '%s'" % (", ".join(sorted(suggestion))))  # line 698
        Exit("Tracked pattern '%s' not found" % pattern)  # line 699
    m.branches[m.branch].tracked.remove(pattern)  # line 700
    m.saveBranches()  # line 701
    info("Removed tracking pattern '%s' for folder '%s'" % (os.path.basename(pattern.replace(SLASH, os.sep)), os.path.abspath(relpath)))  # line 702

def ls(argument: '_coconut.typing.Optional[str]'=None) -> 'None':  # line 704
    ''' List specified directory, augmenting with repository metadata. '''  # line 705
    cwd = os.getcwd() if argument is None else argument  # type: str  # line 706
    m = Metadata(cwd)  # type: Metadata  # line 707
    m.loadBranches()  # line 708
    relpath = os.path.relpath(cwd, m.root).replace(os.sep, SLASH)  # type: str  # line 709
    files = list(sorted((entry for entry in os.listdir(cwd) if os.path.isfile(entry))))  # type: List[str]  # line 710
    trackingPatterns = m.getTrackingPatterns() if m.track or m.picky else _coconut.frozenset()  # type: FrozenSet[str]  # for current branch  # line 711
    for file in files:  # line 712
        ignore = None  # type: _coconut.typing.Optional[str]  # line 713
        for ig in m.c.ignores:  # line 714
            if fnmatch.fnmatch(file, ig):  # remember first match TODO document this  # line 715
                ignore = ig  # remember first match TODO document this  # line 715
                break  # remember first match TODO document this  # line 715
        if ig:  # line 716
            for wl in m.c.ignoresWhitelist:  # line 717
                if fnmatch.fnmatch(file, wl):  # found a white list entry for ignored file, undo ignoring it  # line 718
                    ignore = None  # found a white list entry for ignored file, undo ignoring it  # line 718
                    break  # found a white list entry for ignored file, undo ignoring it  # line 718
        if ignore is None:  # line 719
            matches = []  # type: List[str]  # line 720
            for pattern in (p for p in trackingPatterns if os.path.dirname(p) == relpath):  # only patterns matching current folder  # line 721
                if fnmatch.fnmatch(file, os.path.basename(pattern)):  # TODO or only file basename?  # line 722
                    matches.append(pattern)  # TODO or only file basename?  # line 722
        print("%s %s%s" % ("IGN" if ignore is not None else ("TRK" if len(matches) > 0 else "   "), file, ' by "%s"' % ignore if ignore is not None else (" by " + ";".join(['"%s"' % match for match in matches]) if len(matches) > 0 else "")))  # line 723

def log(options: '_coconut.typing.Sequence[str]') -> 'None':  # line 725
    ''' List previous commits on current branch. '''  # line 726
    m = Metadata(os.getcwd())  # type: Metadata  # line 727
    m.loadBranches()  # knows current branch  # line 728
    m.loadBranch(m.branch)  # knows commit history  # line 729
    info((lambda _coconut_none_coalesce_item: "r%02d" % m.branch if _coconut_none_coalesce_item is None else _coconut_none_coalesce_item)("//|\\\\ Offline commit history of branch '%s'" % m.branches[m.branch].name))  # TODO also retain "from branch/revision" on branching?  # line 730
    nl = len("%d" % max(m.commits))  # determine space needed for revision  # line 731
    changeset = m.computeSequentialPathSetIterator(m.branch, max(m.commits))  # line 732
    maxWidth = max([wcswidth((lambda _coconut_none_coalesce_item: "" if _coconut_none_coalesce_item is None else _coconut_none_coalesce_item)(commit.message)) for commit in m.commits.values()])  # type: int  # line 733
    for no in range(max(m.commits) + 1):  # line 734
        commit = m.commits[no]  # type: CommitInfo  # line 735
        changes = next(changeset)  # type: ChangeSet  # side-effect: updates m.paths  # line 736
        newTextFiles = len([file for file in changes.additions.keys() if m.isTextType(file)])  # type: int  # line 737
        print("  %s r%s @%s (+%02d/-%02d/*%02d +%02dT/%05.1f%%) |%s|" % ("*" if commit.number == max(m.commits) else " ", ("%%%ds" % nl) % commit.number, strftime(commit.ctime), len(changes.additions), len(changes.deletions), len(changes.modifications), newTextFiles, 0. if len(changes.additions) == 0 else newTextFiles * 100. / len(changes.additions), ((lambda _coconut_none_coalesce_item: "" if _coconut_none_coalesce_item is None else _coconut_none_coalesce_item)(commit.message)).ljust(maxWidth)))  # line 738
        if '--changes' in options:  # line 739
            m.listChanges(changes)  # line 739

def config(argument: 'str', options: 'List[str]'=[]) -> 'None':  # line 741
    if argument not in ["set", "unset", "show", "list", "add", "rm"]:  # line 742
        Exit("Unknown config command")  # line 742
    if not configr:  # line 743
        Exit("Cannot execute config command. 'configr' module not installed")  # line 743
    c = loadConfig()  # type: Union[configr.Configr, Accessor]  # line 744
    if argument == "set":  # line 745
        if len(options) < 2:  # line 746
            Exit("No key nor value specified")  # line 746
        if options[0] not in (["defaultbranch"] + CONFIGURABLE_FLAGS + CONFIGURABLE_LISTS):  # line 747
            Exit("Unsupported key %r" % options[0])  # line 747
        if options[0] in CONFIGURABLE_FLAGS and options[1].lower() not in TRUTH_VALUES + FALSE_VALUES:  # line 748
            Exit("Cannot set flag to '%s'. Try on/off instead" % options[1].lower())  # line 748
        c[options[0]] = options[1].lower() in TRUTH_VALUES if options[0] in CONFIGURABLE_FLAGS else (options[1].strip() if options[0] not in CONFIGURABLE_LISTS else safeSplit(options[1], ";"))  # TODO sanitize texts?  # line 749
    elif argument == "unset":  # line 750
        if len(options) < 1:  # line 751
            Exit("No key specified")  # line 751
        if options[0] not in c.keys():  # line 752
            Exit("Unknown key")  # line 752
        del c[options[0]]  # line 753
    elif argument == "add":  # line 754
        if len(options) < 2:  # line 755
            Exit("No key nor value specified")  # line 755
        if options[0] not in CONFIGURABLE_LISTS:  # line 756
            Exit("Unsupported key for add %r" % options[0])  # line 756
        if options[0] not in c.keys():  # add list  # line 757
            c[options[0]] = [options[1]]  # add list  # line 757
        elif options[1] in c[options[0]]:  # line 758
            Exit("Value already contained")  # line 758
        c[options[0]].append(options[1])  # line 759
    elif argument == "rm":  # line 760
        if len(options) < 2:  # line 761
            Exit("No key nor value specified")  # line 761
        if options[0] not in c.keys():  # line 762
            Exit("Unknown key specified: %r" % options[0])  # line 762
        if options[1] not in c[options[0]]:  # line 763
            Exit("Unknown value: %r" % options[1])  # line 763
        c[options[0]].remove(options[1])  # line 764
    else:  # Show  # line 765
        for k, v in sorted(c.items()):  # line 766
            print("%s => %r" % (k, v))  # line 766
        return  # line 767
    f, g = saveConfig(c)  # line 768
    if f is None:  # line 769
        error("Error saving user configuration: %r" % g)  # line 769

def move(relpath: 'str', pattern: 'str', newrelpath: 'str', newpattern: 'str', options: 'List[str]'=[]) -> 'None':  # line 771
    pass  # line 772

def parse(root: 'str', cwd: 'str'):  # line 774
    ''' Main operation. Main has already chdir into VCS root folder, cwd is original working directory for add, rm. '''  # line 775
    debug("Parsing command-line arguments...")  # line 776
    command = sys.argv[1].strip() if len(sys.argv) > 1 else ""  # line 777
    argument = sys.argv[2].strip() if len(sys.argv) > 2 and not sys.argv[2].startswith("--") else None  # line 778
    options = sys.argv[3:] if command == "config" else [c for c in sys.argv[2:] if c.startswith("--")]  # consider second parameter for no-arg command, otherwise from third on  # line 779
    onlys, excps = parseOnlyOptions(cwd, options)  # extracts folder-relative information for changes, commit, diff, switch, update  # line 780
    debug("Processing command %r with argument '%s' and options %r." % ("" if command is None else command, "" if argument is None else argument, options))  # line 781
    if command[:1] in "amr":  # line 782
        relpath, pattern = relativize(root, os.path.join(cwd, argument))  # line 782
    if command[:1] == "m":  # TODO add error message if target pattern is missing  # line 783
        newrelpath, newpattern = relativize(root, os.path.join(cwd, options[0]))  # TODO add error message if target pattern is missing  # line 783
    if command[:1] == "a":  # line 784
        add(relpath, pattern, options)  # line 784
    elif command[:1] == "b":  # line 785
        branch(argument, options)  # line 785
    elif command[:2] == "ch":  # line 786
        changes(argument, options, onlys, excps)  # line 786
    elif command[:3] == "com":  # line 787
        commit(argument, options, onlys, excps)  # line 787
    elif command[:2] == "ci":  # line 788
        commit(argument, options, onlys, excps)  # line 788
    elif command[:3] == 'con':  # line 789
        config(argument, options)  # line 789
    elif command[:2] == "de":  # line 790
        delete(argument, options)  # line 790
    elif command[:2] == "di":  # line 791
        diff(argument, options, onlys, excps)  # line 791
    elif command[:1] == "h":  # line 792
        usage()  # line 792
    elif command[:2] == "lo":  # line 793
        log(options)  # line 793
    elif command[:2] == "li":  # line 794
        ls(argument)  # line 794
    elif command[:2] == "ls":  # line 795
        ls(argument)  # line 795
    elif command[:1] == "m":  # line 796
        move(relpath, pattern, newrelpath, newpattern, options[1:])  # line 796
    elif command[:2] == "of":  # line 797
        offline(argument, options)  # line 797
    elif command[:2] == "on":  # line 798
        online(options)  # line 798
    elif command[:1] == "r":  # line 799
        rm(relpath, pattern)  # line 799
    elif command[:2] == "st":  # line 800
        status()  # line 800
    elif command[:2] == "sw":  # line 801
        switch(argument, options, onlys, excps)  # line 801
    elif command[:1] == "u":  # line 802
        update(argument, options, onlys, excps)  # line 802
    else:  # line 803
        Exit("Unknown command '%s'" % command)  # line 803
    sys.exit(0)  # line 804

def main() -> 'None':  # line 806
    global debug, info, warn, error  # line 807
    logging.basicConfig(level=level, stream=sys.stderr, format=("%(asctime)-23s %(levelname)-8s %(name)s:%(lineno)d | %(message)s" if '--log' in sys.argv else "%(message)s"))  # line 808
    _log = Logger(logging.getLogger(__name__))  # line 809
    debug, info, warn, error = _log.debug, _log.info, _log.warn, _log.error  # line 809
    for option in (o for o in ['--log', '--verbose', '-v', '--sos'] if o in sys.argv):  # clean up program arguments  # line 810
        sys.argv.remove(option)  # clean up program arguments  # line 810
    if '--help' in sys.argv or len(sys.argv) < 2:  # line 811
        usage()  # line 811
        Exit()  # line 811
    command = sys.argv[1] if len(sys.argv) > 1 else None  # type: _coconut.typing.Optional[str]  # line 812
    root, vcs, cmd = findSosVcsBase()  # root is None if no .sos folder exists up the folder tree (still working online); vcs is checkout/repo root folder; cmd is the VCS base command  # line 813
    debug("Found root folders for SOS|VCS: %s|%s" % ("" if root is None else root, "" if vcs is None else vcs))  # line 814
    defaults["defaultbranch"] = vcsBranches.get(cmd, "trunk")  # sets dynamic default with SVN fallback  # line 815
    if force_sos or root is not None or ("" if command is None else command)[:2] == "of" or ("" if command is None else command)[:1] == "h":  # in offline mode or just going offline TODO what about git config?  # line 816
        cwd = os.getcwd()  # line 817
        os.chdir(cwd if command[:2] == "of" else cwd if root is None else root)  # line 818
        parse(root, cwd)  # line 819
    elif cmd is not None:  # online mode - delegate to VCS  # line 820
        info("SOS: Running '%s %s'" % (cmd, " ".join(sys.argv[1:])))  # line 821
        import subprocess  # only required in this section  # line 822
        process = subprocess.Popen([cmd] + sys.argv[1:], shell=False, stdin=subprocess.PIPE, stdout=sys.stdout, stderr=sys.stderr)  # line 823
        inp = ""  # type: str  # line 824
        while True:  # line 825
            so, se = process.communicate(input=inp)  # line 826
            if process.returncode is not None:  # line 827
                break  # line 827
            inp = sys.stdin.read()  # line 828
        if sys.argv[1][:2] == "co" and process.returncode == 0:  # successful commit - assume now in sync again (but leave meta data folder with potential other feature branches behind until "online")  # line 829
            if root is None:  # line 830
                Exit("Cannot determine VCS root folder: Unable to mark repository as synchronized and will show a warning when leaving offline mode")  # line 830
            m = Metadata(root)  # line 831
            m.loadBranches()  # read repo  # line 832
            m.branches[m.branch] = dataCopy(BranchInfo, m.branches[m.branch], insync=True)  # mark as committed  # line 833
            m.saveBranches()  # line 834
    else:  # line 835
        Exit("No offline repository present, and unable to detect VCS file tree")  # line 835


# Main part
level = logging.DEBUG if os.environ.get("DEBUG", "False").lower() == "true" or '--verbose' in sys.argv or '-v' in sys.argv else logging.INFO  # line 839
force_sos = '--sos' in sys.argv  # line 840
_log = Logger(logging.getLogger(__name__))  # line 841
debug, info, warn, error = _log.debug, _log.info, _log.warn, _log.error  # line 841
if __name__ == '__main__':  # line 842
    main()  # line 842
