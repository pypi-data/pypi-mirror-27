#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# __coconut_hash__ = 0x35a367f4

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
import collections  # line 2
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
def saveConfig(config: 'configr.Configr') -> 'Tuple[_coconut.typing.Optional[str], _coconut.typing.Optional[Exception]]':  # line 35
    return _coconut_tail_call(config.saveSettings, clientCodeLocation=os.path.abspath(__file__), location=os.environ.get("TEST", None))  # line 36

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
    mv      [<oldpattern>] [<newPattern>]                 Rename, move, or move and rename tracked files according to glob patterns
      --soft                                              Don't move or rename files, only the tracking pattern
    rm      [<filename or glob pattern>]                  Remove a tracking pattern. Only useful after "offline --track" or "offline --picky"

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
    --only <tracked pattern>     Restrict operation to specified pattern(s). Available for "changes", "commit", "diff", "switch", and "update"
    --except <tracked pattern >  Avoid operation for specified pattern(s). Available for "changes", "commit", "diff", "switch", and "update"
    --{cmd}                      When executing {CMD} not being offline, pass arguments to {CMD} instead (e.g. {cmd} --{cmd} config set key value.)
    --log                        Enable logging details
    --verbose                    Enable verbose output""".format(appname=APPNAME, cmd="sos", CMD="SOS"))  # line 96

# Main data class
#@runtime_validation
class Metadata:  # line 100
    ''' This class doesn't represent the entire repository state in memory,
      but serves as a container for different repo operations,
      using only parts of its attributes at any point in time. Use with care.
  '''  # line 104

    def __init__(_, path: 'str') -> 'None':  # line 106
        ''' Create empty container object for various repository operations. '''  # line 107
        _.c = loadConfig()  # line 108
        _.root = path  # type: str  # line 109
        _.branches = {}  # type: Dict[int, BranchInfo]  # branch number zero represents the initial state at branching  # line 110
        _.commits = {}  # type: Dict[int, CommitInfo]  # consecutive numbers per branch, starting at 0  # line 111
        _.paths = {}  # type: Dict[str, PathInfo]  # utf-8 encoded relative, normalized file system paths  # line 112
        _.tags = []  # type: List[str]  # line 113
        _.branch = None  # type: _coconut.typing.Optional[int]  # current branch number  # line 114
        _.commit = None  # type: _coconut.typing.Optional[int]  # current revision number  # line 115
        _.track = _.c.track  # type: bool  # track file name patterns in the repository (per branch)  # line 116
        _.picky = _.c.picky  # type: bool  # pick files to commit per operation  # line 117
        _.strict = _.c.strict  # type: bool  # be always strict (regarding file contents comparsion)  # line 118
        _.compress = _.c.compress  # type: bool  # these flags are stored in the repository  # line 119

    def isTextType(_, filename: 'str') -> 'bool':  # line 121
        return (((lambda _coconut_none_coalesce_item: "" if _coconut_none_coalesce_item is None else _coconut_none_coalesce_item)(mimetypes.guess_type(filename)[0])).startswith("text/") or any([fnmatch.fnmatch(filename, pattern) for pattern in _.c.texttype])) and not any([fnmatch.fnmatch(filename, pattern) for pattern in _.c.bintype])  # line 121

    def listChanges(_, changes: 'ChangeSet') -> 'None':  # line 123
        if len(changes.additions) > 0:  # line 124
            print(ajoin("ADD ", sorted(changes.additions.keys()), "\n"))  # line 124
        if len(changes.deletions) > 0:  # line 125
            print(ajoin("DEL ", sorted(changes.deletions.keys()), "\n"))  # line 125
        if len(changes.modifications) > 0:  # line 126
            print(ajoin("MOD ", sorted(changes.modifications.keys()), "\n"))  # line 126

    def loadBranches(_) -> 'None':  # line 128
        ''' Load list of branches and current branch info from metadata file. '''  # line 129
        try:  # fails if not yet created (on initial branch/commit)  # line 130
            branches = None  # type: List[Tuple]  # line 131
            with codecs.open(os.path.join(_.root, metaFolder, metaFile), "r", encoding=UTF8) as fd:  # line 132
                flags, branches = json.load(fd)  # line 133
            _.tags = flags["tags"]  # list of commit messages to treat as globally unique tags  # line 134
            _.branch = flags["branch"]  # current branch integer  # line 135
            _.track = flags["track"]  # line 136
            _.picky = flags["picky"]  # line 137
            _.strict = flags["strict"]  # line 138
            _.compress = flags["compress"]  # line 139
            _.branches = {i.number: i for i in (BranchInfo(*item) for item in branches)}  # re-create type info  # line 140
        except Exception as E:  # if not found, create metadata folder  # line 141
            _.branches = {}  # line 142
            warn("Couldn't read branches metadata: %r" % E)  # line 143

    def saveBranches(_) -> 'None':  # line 145
        ''' Save list of branches and current branch info to metadata file. '''  # line 146
        with codecs.open(os.path.join(_.root, metaFolder, metaFile), "w", encoding=UTF8) as fd:  # line 147
            json.dump(({"tags": _.tags, "branch": _.branch, "track": _.track, "picky": _.picky, "strict": _.strict, "compress": _.compress}, list(_.branches.values())), fd, ensure_ascii=False)  # line 148

    def getRevisionByName(_, name: 'str') -> '_coconut.typing.Optional[int]':  # line 150
        ''' Convenience accessor for named revisions (using commit message as name). '''  # line 151
        if name == "":  # line 152
            return -1  # line 152
        try:  # attempt to parse integer string  # line 153
            return longint(name)  # attempt to parse integer string  # line 153
        except ValueError:  # line 154
            pass  # line 154
        found = [number for number, commit in _.commits.items() if name == commit.message]  # line 155
        return found[0] if found else None  # line 156

    def getBranchByName(_, name: 'str') -> '_coconut.typing.Optional[int]':  # line 158
        ''' Convenience accessor for named branches. '''  # line 159
        if name == "":  # line 160
            return _.branch  # line 160
        try:  # attempt to parse integer string  # line 161
            return longint(name)  # attempt to parse integer string  # line 161
        except ValueError:  # line 162
            pass  # line 162
        found = [number for number, branch in _.branches.items() if name == branch.name]  # line 163
        return found[0] if found else None  # line 164

    def loadBranch(_, branch: 'int') -> 'None':  # line 166
        ''' Load all commit information from a branch meta data file. '''  # line 167
        with codecs.open(os.path.join(_.root, metaFolder, "b%d" % branch, metaFile), "r", encoding=UTF8) as fd:  # line 168
            commits = json.load(fd)  # type: List[List[Any]]  # list of CommitInfo that needs to be unmarshalled into value types  # line 169
        _.commits = {i.number: i for i in (CommitInfo(*item) for item in commits)}  # re-create type info  # line 170
        _.branch = branch  # line 171

    def saveBranch(_, branch: 'int') -> 'None':  # line 173
        ''' Save all commit information to a branch meta data file. '''  # line 174
        with codecs.open(os.path.join(_.root, metaFolder, "b%d" % branch, metaFile), "w", encoding=UTF8) as fd:  # line 175
            json.dump(list(_.commits.values()), fd, ensure_ascii=False)  # line 176

    def duplicateBranch(_, branch: 'int', name: '_coconut.typing.Optional[str]') -> 'None':  # line 178
        ''' Create branch from an existing branch/revision. WARN: Caller must have loaded branches information.
        branch: target branch (should not exist yet)
        name: optional name of new branch
        _.branch: current branch
    '''  # line 183
        debug("Duplicating branch '%s' to '%d'..." % ((lambda _coconut_none_coalesce_item: "b%d" % _.branch if _coconut_none_coalesce_item is None else _coconut_none_coalesce_item)(_.branches[_.branch].name), branch))  # line 184
        tracked = [t for t in _.branches[_.branch].tracked]  # copy  # line 185
        os.makedirs(os.path.join(_.root, metaFolder, "b%d" % branch, "r0"))  # line 186
        _.loadBranch(_.branch)  # line 187
        revision = max(_.commits)  # type: int  # line 188
        _.computeSequentialPathSet(_.branch, revision)  # full set of files in revision to _.paths  # line 189
        for path, pinfo in _.paths.items():  # line 190
            _.copyVersionedFile(_.branch, revision, branch, 0, pinfo)  # line 191
        _.commits = {0: CommitInfo(0, longint(time.time() * 1000), "Branched from '%s'" % ((lambda _coconut_none_coalesce_item: "b%d" % _.branch if _coconut_none_coalesce_item is None else _coconut_none_coalesce_item)(_.branches[_.branch].name)))}  # store initial commit  # line 192
        _.saveBranch(branch)  # save branch meta data to branch folder  # line 193
        _.saveCommit(branch, 0)  # save commit meta data to revision folder  # line 194
        _.branches[branch] = BranchInfo(branch, _.commits[0].ctime, name, _.branches[_.branch].inSync, tracked)  # save branch info, before storing repo state at caller  # line 195

    def createBranch(_, branch: 'int', name: '_coconut.typing.Optional[str]'=None, initialMessage: '_coconut.typing.Optional[str]'=None):  # line 197
        ''' Create a new branch from current file tree. This clears all known commits and modifies the file system.
        branch: target branch (should not exist yet)
        name: optional name of new branch
        _.branch: current branch, must exist already
    '''  # line 202
        simpleMode = not (_.track or _.picky)  # line 203
        tracked = [t for t in _.branches[_.branch].tracked] if _.track and len(_.branches) > 0 else []  # in case of initial branch creation  # line 204
        debug((lambda _coconut_none_coalesce_item: "b%d" % branch if _coconut_none_coalesce_item is None else _coconut_none_coalesce_item)("Creating branch '%s'..." % name))  # line 205
        _.paths = {}  # type: Dict[str, PathInfo]  # line 206
        if simpleMode:  # branches from file system state  # line 207
            changes = _.findChanges(branch, 0, progress=simpleMode)  # type: ChangeSet  # creates revision folder and versioned files  # line 208
            _.listChanges(changes)  # line 209
            _.paths.update(changes.additions.items())  # line 210
        else:  # tracking or picky mode: branch from lastest revision  # line 211
            os.makedirs(os.path.join(_.root, metaFolder, "b%d" % branch, "r0"))  # line 212
            if _.branch is not None:  # not immediately after "offline" - copy files from current branch  # line 213
                _.loadBranch(_.branch)  # line 214
                revision = max(_.commits)  # type: int  # TODO what if last switch was to an earlier revision? no persisting of last checkout  # line 215
                _.computeSequentialPathSet(_.branch, revision)  # full set of files in revision to _.paths  # line 216
                for path, pinfo in _.paths.items():  # line 217
                    _.copyVersionedFile(_.branch, revision, branch, 0, pinfo)  # line 218
        ts = longint(time.time() * 1000)  # line 219
        _.commits = {0: CommitInfo(0, ts, "Branched on %s" % strftime(ts) if initialMessage is None else initialMessage)}  # store initial commit for new branch  # line 220
        _.saveBranch(branch)  # save branch meta data (revisions) to branch folder  # line 221
        _.saveCommit(branch, 0)  # save commit meta data to revision folder  # line 222
        _.branches[branch] = BranchInfo(branch, _.commits[0].ctime, name, True if len(_.branches) == 0 else _.branches[_.branch].inSync, tracked)  # save branch info, in case it is needed  # line 223

    def removeBranch(_, branch: 'int') -> 'BranchInfo':  # line 225
        ''' Entirely remove a branch and all its revisions from the file system. '''  # line 226
        shutil.rmtree(os.path.join(_.root, metaFolder, "b%d" % branch))  # line 227
        binfo = _.branches[branch]  # line 228
        del _.branches[branch]  # line 229
        _.branch = max(_.branches)  # line 230
        _.saveBranches()  # line 231
        _.commits.clear()  # line 232
        return binfo  # line 233

    def loadCommit(_, branch: 'int', revision: 'int') -> 'None':  # line 235
        ''' Load all file information from a commit meta data. '''  # line 236
        with codecs.open(os.path.join(_.root, metaFolder, "b%d" % branch, "r%d" % revision, metaFile), "r", encoding=UTF8) as fd:  # line 237
            _.paths = json.load(fd)  # line 238
        _.paths = {path: PathInfo(*item) for path, item in _.paths.items()}  # re-create type info  # line 239
        _.branch = branch  # line 240

    def saveCommit(_, branch: 'int', revision: 'int'):  # line 242
        ''' Save all file information to a commit meta data file. '''  # line 243
        target = os.path.join(_.root, metaFolder, "b%d" % branch, "r%d" % revision)  # line 244
        try:  # line 245
            os.makedirs(target)  # line 245
        except:  # line 246
            pass  # line 246
        with codecs.open(os.path.join(target, metaFile), "w", encoding=UTF8) as fd:  # line 247
            json.dump(_.paths, fd, ensure_ascii=False)  # line 248

    def findChanges(_, branch: '_coconut.typing.Optional[int]'=None, revision: '_coconut.typing.Optional[int]'=None, checkContent: 'bool'=False, inverse: 'bool'=False, considerOnly: '_coconut.typing.Optional[FrozenSet[str]]'=None, dontConsider: '_coconut.typing.Optional[FrozenSet[str]]'=None, progress: 'bool'=False) -> 'ChangeSet':  # line 250
        ''' Find changes on the file system vs. in-memory paths (which should reflect the latest commit state).
        Only if both branch and revision are *not* None, write modified/added files to the specified revision folder (thus creating a new revision)
        The function returns the state of file tree *differences*, unless "inverse" is True -> then return original data
        checkContent: also computes file content hashes
        inverse: retain original state (size, mtime, hash) instead of updated one
        considerOnly: set of tracking patterns. None for simple mode. For update operation, consider union of other and current branch
        dontConsider: set of tracking patterns to not consider in changes
        progress: Show file names during processing
    '''  # line 259
        write = branch is not None and revision is not None  # line 260
        if write:  # line 261
            os.makedirs(os.path.join(_.root, metaFolder, "b%d" % branch, "r%d" % revision))  # line 261
        changes = ChangeSet({}, {}, {})  # type: ChangeSet  # line 262
        counter = Counter(-1)  # type: Counter  # line 263
        timer = time.time()  # line 263
        hashed = None  # type: _coconut.typing.Optional[str]  # line 264
        written = None  # type: longint  # line 264
        compressed = 0  # type: longint  # line 264
        original = 0  # type: longint  # line 264
        knownPaths = collections.defaultdict(list)  # type: Dict[str, List[str]]  # line 265
        for path, pinfo in _.paths.items():  # TODO check dontConsider below  # line 266
            if pinfo.size is not None and (considerOnly is None or any((path[:path.rindex(SLASH)] == pattern[:pattern.rindex(SLASH)] and fnmatch.fnmatch(path[path.rindex(SLASH) + 1:], pattern[pattern.rindex(SLASH) + 1:]) for pattern in considerOnly))) and (dontConsider is None or not any((path[:path.rindex(SLASH)] == pattern[:pattern.rindex(SLASH)] and fnmatch.fnmatch(path[path.rindex(SLASH) + 1:], pattern[pattern.rindex(SLASH) + 1:]) for pattern in dontConsider))):  # line 267
                knownPaths[os.path.dirname(path)].append(os.path.basename(path))  # TODO reimplement using fnmatch.filter for all files per path for speed  # line 270
        for path, dirnames, filenames in os.walk(_.root):  # line 271
            dirnames[:] = [f for f in dirnames if len([n for n in _.c.ignoreDirs if fnmatch.fnmatch(f, n)]) == 0 or len([p for p in _.c.ignoreDirsWhitelist if fnmatch.fnmatch(f, p)]) > 0]  # line 272
            filenames[:] = [f for f in filenames if len([n for n in _.c.ignores if fnmatch.fnmatch(f, n)]) == 0 or len([p for p in _.c.ignoresWhitelist if fnmatch.fnmatch(f, p)]) > 0]  # line 273
            dirnames.sort()  # line 274
            filenames.sort()  # line 274
            relPath = os.path.relpath(path, _.root).replace(os.sep, SLASH)  # TODO removes ./ ??  # line 275
            walk = filenames if considerOnly is None else list(reduce(lambda last, pattern: last | set(fnmatch.filter(filenames, os.path.basename(pattern))), (p for p in considerOnly if os.path.dirname(p).replace(os.sep, SLASH) == relPath), _coconut.set()))  # line 276
            if dontConsider:  # line 277
                walk[:] = [fn for fn in walk if not any((fnmatch.fnmatch(fn, os.path.basename(p)) for p in dontConsider if os.path.dirname(p).replace(os.sep, SLASH) == relPath))]  # TODO dirname is correct noramalized? same above?  # line 278
            for file in walk:  # if m.track or m.picky: only files that match any path-relevant tracking patterns  # line 279
                filename = relPath + SLASH + file  # line 280
                filepath = os.path.join(path, file)  # line 281
                stat = os.stat(filepath)  # line 282
                size, mtime, newtime = stat.st_size, longint(stat.st_mtime * 1000), time.time()  # line 283
                if progress and newtime - timer > .1:  # line 284
                    outstring = "\rPreparing %s  %s" % (PROGRESS_MARKER[counter.inc() % 4], filename)  # line 285
                    sys.stdout.write(outstring + " " * max(0, termWidth - len(outstring)))  # TODO could write to new line instead of carriage return, also needs terminal width  # line 286
                    sys.stdout.flush()  # TODO could write to new line instead of carriage return, also needs terminal width  # line 286
                    timer = newtime  # TODO could write to new line instead of carriage return, also needs terminal width  # line 286
                if filename not in _.paths:  # detected file not present (or untracked) in (other) branch  # line 287
                    nameHash = hashStr(filename)  # line 288
                    hashed, written = hashFile(filepath, _.compress, saveTo=os.path.join(_.root, metaFolder, "b%d" % branch, "r%d" % revision, nameHash) if write else None) if size > 0 else (None, 0)  # line 289
                    changes.additions[filename] = PathInfo(nameHash, size, mtime, hashed)  # line 290
                    compressed += written  # line 291
                    original += size  # line 291
                    continue  # line 292
                last = _.paths[filename]  # filename is known - check for modifications  # line 293
                if last.size is None:  # was removed before but is now added back - does not apply for tracking mode (which never marks files for removal in the history)  # line 294
                    hashed, written = hashFile(filepath, _.compress, saveTo=os.path.join(_.root, metaFolder, "b%d" % branch, "r%d" % revision, last.nameHash) if write else None) if size > 0 else (None, 0)  # line 295
                    changes.additions[filename] = PathInfo(last.nameHash, size, mtime, hashed)  # line 296
                    continue  # line 296
                elif size != last.size or mtime != last.mtime or (checkContent and hashFile(filepath, _.compress)[0] != last.hash):  # detected a modification  # line 297
                    hashed, written = hashFile(filepath, _.compress, saveTo=os.path.join(_.root, metaFolder, "b%d" % branch, "r%d" % revision, last.nameHash) if write else None) if (last.size if inverse else size) > 0 else (last.hash if inverse else None, 0)  # line 298
                    changes.modifications[filename] = PathInfo(last.nameHash, last.size if inverse else size, last.mtime if inverse else mtime, hashed)  # line 299
                else:  # line 300
                    continue  # line 300
                compressed += written  # line 301
                original += last.size if inverse else size  # line 301
            if relPath in knownPaths:  # at least one file is tracked  # line 302
                knownPaths[relPath][:] = list(set(knownPaths[relPath]) - set(walk))  # at least one file is tracked  # line 302
        for path, names in knownPaths.items():  # all paths that weren't walked by  # line 303
            for file in names:  # line 304
                changes.deletions[path + SLASH + file] = _.paths[path + SLASH + file]  # line 304
        if progress:  # force new line  # line 305
            print("\rPreparation finished. Compression factor %s" % ("is %.1f" % (original * 100. / compressed) if compressed > 0 else "cannot be computed").ljust(termWidth), file=sys.stdout)  # force new line  # line 305
        else:  # line 306
            debug("Finished detecting changes. Compression factor %s" % ("is %.1f" % (original * 100. / compressed) if compressed > 0 else "cannot be computed"))  # line 306
        return changes  # line 307

    def integrateChangeset(_, changes: 'ChangeSet', clear=False) -> 'None':  # line 309
        ''' In-memory update from a changeset, marking deleted files with size=None. Use clear = True to start on an empty path set. '''  # line 310
        if clear:  # line 311
            _.paths.clear()  # line 311
        else:  # line 312
            rm = [p for p, info in _.paths.items() if info.size is None]  # remove files deleted in earlier change sets (revisions)  # line 313
            for old in rm:  # remove previously removed entries completely  # line 314
                del _.paths[old]  # remove previously removed entries completely  # line 314
        for d, info in changes.deletions.items():  # mark now removed entries as deleted  # line 315
            _.paths[d] = PathInfo(info.nameHash, None, info.mtime, None)  # mark now removed entries as deleted  # line 315
        _.paths.update(changes.additions)  # line 316
        _.paths.update(changes.modifications)  # line 317

    def computeSequentialPathSet(_, branch: 'int', revision: 'int') -> 'None':  # line 319
        next(_.computeSequentialPathSetIterator(branch, revision, incrementally=False))  # simply invoke the generator once  # line 320

    def computeSequentialPathSetIterator(_, branch: 'int', revision: 'int', incrementally: 'bool'=True) -> '_coconut.typing.Optional[Iterator[ChangeSet]]':  # line 322
        ''' In-memory computation of current list of valid PathInfo entries for specified branch and until specified revision (inclusively) by traversing revision on the file system. '''  # line 323
        _.loadCommit(branch, 0)  # load initial paths  # line 324
        if incrementally:  # line 325
            yield diffPathSets({}, _.paths)  # line 325
        n = Metadata(_.root)  # type: Metadata  # next changes  # line 326
        for revision in range(1, revision + 1):  # line 327
            n.loadCommit(branch, revision)  # line 328
            changes = diffPathSets(_.paths, n.paths)  # type: ChangeSet  # line 329
            _.integrateChangeset(changes)  # line 330
            if incrementally:  # line 331
                yield changes  # line 331
        yield None  # for the default case - not incrementally  # line 332

    def parseRevisionString(_, argument: 'str') -> 'Tuple[_coconut.typing.Optional[int], _coconut.typing.Optional[int]]':  # line 334
        ''' Commit identifiers can be str or int for branch, and int for revision.
        Revision identifiers can be negative, with -1 being last commit.
    '''  # line 337
        if argument is None or argument == SLASH:  # no branch/revision specified  # line 338
            return (_.branch, -1)  # no branch/revision specified  # line 338
        argument = argument.strip()  # line 339
        if argument.startswith(SLASH):  # current branch  # line 340
            return (_.branch, _.getRevisionByName(argument[1:]))  # current branch  # line 340
        if argument.endswith(SLASH):  # line 341
            try:  # line 342
                return (_.getBranchByName(argument[:-1]), -1)  # line 342
            except ValueError:  # line 343
                Exit("Unknown branch label")  # line 343
        if SLASH in argument:  # line 344
            b, r = argument.split(SLASH)[:2]  # line 345
            try:  # line 346
                return (_.getBranchByName(b), _.getRevisionByName(r))  # line 346
            except ValueError:  # line 347
                Exit("Unknown branch label or wrong number format")  # line 347
        branch = _.getBranchByName(argument)  # type: int  # returns number if given (revision) integer  # line 348
        if branch not in _.branches:  # line 349
            branch = None  # line 349
        try:  # either branch name/number or reverse/absolute revision number  # line 350
            return (_.branch if branch is None else branch, longint(argument if argument else "-1") if branch is None else -1)  # either branch name/number or reverse/absolute revision number  # line 350
        except:  # line 351
            Exit("Unknown branch label or wrong number format")  # line 351
        Exit("This should never happen")  # line 352
        return (None, None)  # line 352

    def findRevision(_, branch: 'int', revision: 'int', nameHash: 'str') -> 'Tuple[int, str]':  # line 354
        while True:  # find latest revision that contained the file physically  # line 355
            source = os.path.join(_.root, metaFolder, "b%d" % branch, "r%d" % revision, nameHash)  # type: str  # line 356
            if os.path.exists(source) and os.path.isfile(source):  # line 357
                break  # line 357
            revision -= 1  # line 358
            if revision < 0:  # line 359
                Exit("Cannot determine versioned file '%s' from specified branch '%d'" % (nameHash, branch))  # line 359
        return revision, source  # line 360

    def copyVersionedFile(_, branch: 'int', revision: 'int', toBranch: 'int', toRevision: 'int', pinfo: 'PathInfo') -> 'None':  # line 362
        ''' Copy versioned file to other branch/revision. '''  # line 363
        target = os.path.join(_.root, metaFolder, "b%d" % toBranch, "r%d" % toRevision, pinfo.nameHash)  # type: str  # line 364
        revision, source = _.findRevision(branch, revision, pinfo.nameHash)  # line 365
        shutil.copy2(source, target)  # line 366

    def readOrCopyVersionedFile(_, branch: 'int', revision: 'int', nameHash: 'str', toFile: '_coconut.typing.Optional[str]'=None) -> '_coconut.typing.Optional[bytes]':  # line 368
        ''' Return file contents, or copy contents into file path provided. '''  # line 369
        source = os.path.join(_.root, metaFolder, "b%d" % branch, "r%d" % revision, nameHash)  # type: str  # line 370
        try:  # line 371
            with openIt(source, "r", _.compress) as fd:  # line 372
                if toFile is None:  # read bytes into memory and return  # line 373
                    return fd.read()  # read bytes into memory and return  # line 373
                with open(toFile, "wb") as to:  # line 374
                    while True:  # line 375
                        buffer = fd.read(bufSize)  # line 376
                        to.write(buffer)  # line 377
                        if len(buffer) < bufSize:  # line 378
                            break  # line 378
                    return None  # line 379
        except Exception as E:  # line 380
            warn("Cannot read versioned file: %r (%d/%d/%s)" % (E, branch, revision, nameHash))  # line 380
        return None  # line 381

    def restoreFile(_, relPath: '_coconut.typing.Optional[str]', branch: 'int', revision: 'int', pinfo: 'PathInfo', ensurePath: 'bool'=False) -> '_coconut.typing.Optional[bytes]':  # line 383
        ''' Recreate file for given revision, or return contents if path is None. '''  # line 384
        if relPath is None:  # just return contents  # line 385
            return _.readOrCopyVersionedFile(branch, _.findRevision(branch, revision, pinfo.nameHash)[0], pinfo.nameHash) if pinfo.size > 0 else b''  # just return contents  # line 385
        target = os.path.join(_.root, relPath.replace(SLASH, os.sep))  # type: str  # line 386
        if ensurePath:  #  and not os.path.exists(os.path.dirname(target)):  # line 387
            try:  # line 388
                os.makedirs(os.path.dirname(target))  # line 388
            except:  # line 389
                pass  # line 389
        if pinfo.size == 0:  # line 390
            with open(target, "wb"):  # line 391
                pass  # line 391
            try:  # update access/modification timestamps on file system  # line 392
                os.utime(target, (-1, pinfo.mtime / 1000.))  # update access/modification timestamps on file system  # line 392
            except Exception as E:  # line 393
                error("Cannot update file's timestamp after restoration '%r'" % E)  # line 393
            return None  # line 394
        revision, source = _.findRevision(branch, revision, pinfo.nameHash)  # line 395
# Restore file by copying buffer-wise
        with openIt(source, "r", _.compress) as fd, open(target, "wb") as to:  # using Coconut's Enhanced Parenthetical Continuation  # line 397
            while True:  # line 398
                buffer = fd.read(bufSize)  # line 399
                to.write(buffer)  # line 400
                if len(buffer) < bufSize:  # line 401
                    break  # line 401
        try:  # update access/modification timestamps on file system  # line 402
            os.utime(target, (-1, pinfo.mtime / 1000.))  # update access/modification timestamps on file system  # line 402
        except Exception as E:  # line 403
            error("Cannot update file's timestamp after restoration '%r'" % E)  # line 403
        return None  # line 404

    def getTrackingPatterns(_, branch: '_coconut.typing.Optional[int]'=None) -> 'FrozenSet[str]':  # line 406
        ''' Returns list of tracking patterns for provided branch or current branch. '''  # line 407
        return _coconut.frozenset() if not _.track and not _.picky else frozenset(_.branches[_.branch if branch is None else branch].tracked)  # line 408


# Main client operations
def offline(argument: '_coconut.typing.Optional[str]'=None, options: '_coconut.typing.Sequence[str]'=[]) -> 'None':  # line 412
    ''' Initial command to start working offline. '''  # line 413
    if os.path.exists(metaFolder):  # line 414
        if '--force' not in options:  # line 415
            Exit("Repository folder is either already offline or older branches and commits were left over.\nUse 'sos online' to check for dirty branches, or\nWipe existing offline branches with 'sos offline --force'")  # line 415
        try:  # line 416
            for entry in os.listdir(metaFolder):  # line 417
                resource = metaFolder + os.sep + entry  # line 418
                if os.path.isdir(resource):  # line 419
                    shutil.rmtree(resource)  # line 419
                else:  # line 420
                    os.unlink(resource)  # line 420
        except:  # line 421
            Exit("Cannot reliably remove previous repository contents. Please remove .sos folder manually prior to going offline")  # line 421
    m = Metadata(os.getcwd())  # type: Metadata  # line 422
    if '--plain' in options or not m.c.compress:  # plain file copies instead of compressed ones  # line 423
        m.compress = False  # plain file copies instead of compressed ones  # line 423
    if '--picky' in options or m.c.picky:  # Git-like  # line 424
        m.picky = True  # Git-like  # line 424
    elif '--track' in options or m.c.track:  # Svn-like  # line 425
        m.track = True  # Svn-like  # line 425
    if '--strict' in options or m.c.strict:  # always hash contents  # line 426
        m.strict = True  # always hash contents  # line 426
    debug("Preparing offline repository...")  # line 427
    m.createBranch(0, str(defaults["defaultbranch"]) if argument is None else argument, initialMessage="Offline repository created on %s" % strftime())  # main branch's name may be None (e.g. for fossil)  # line 428
    m.branch = 0  # line 429
    m.saveBranches()  # no change immediately after going offline, going back online won't issue a warning  # line 430
    info("Offline repository prepared. Use 'sos online' to finish offline work")  # line 431

def online(options: '_coconut.typing.Sequence[str]'=[]) -> 'None':  # line 433
    ''' Finish working offline. '''  # line 434
    force = '--force' in options  # type: bool  # line 435
    m = Metadata(os.getcwd())  # line 436
    m.loadBranches()  # line 437
    if any([not b.inSync for b in m.branches.values()]) and not force:  # line 438
        Exit("There are still unsynchronized (dirty) branches.\nUse 'sos log' to list them.\nUse 'sos commit' and 'sos switch' to commit dirty branches to your VCS before leaving offline mode.\nUse 'sos online --force' to erase all aggregated offline revisions")  # line 438
    strict = '--strict' in options or m.strict  # type: bool  # line 439
    if options.count("--force") < 2:  # line 440
        changes = m.findChanges(checkContent=strict, considerOnly=None if not m.track and not m.picky else m.getTrackingPatterns())  # type: ChangeSet  # HINT no option for --only/--except here on purpose. No check for picky here, because online is not a command that considers staged files (but we could use --only here, alternatively)  # line 441
        if modified(changes):  # line 442
            Exit("File tree is modified vs. current branch.\nUse 'sos online --force --force' to continue with removing the offline repository")  # line 442
    try:  # line 443
        shutil.rmtree(metaFolder)  # line 443
        info("Exited offline mode. Continue working with your traditional VCS.")  # line 443
    except Exception as E:  # line 444
        Exit("Error removing offline repository: %r" % E)  # line 444

def branch(argument: '_coconut.typing.Optional[str]'=None, options: '_coconut.typing.Sequence[str]'=[]) -> 'None':  # line 446
    ''' Create a new branch (from file tree or last revision) and (by default) continue working on it. '''  # line 447
    last = '--last' in options  # type: bool  # use last revision for branching, not current file tree  # line 448
    stay = '--stay' in options  # type: bool  # continue on current branch after branching  # line 449
    force = '--force' in options  # type: bool  # branch even with local modifications  # line 450
    m = Metadata(os.getcwd())  # type: Metadata  # line 451
    m.loadBranches()  # line 452
    if argument and m.getBranchByName(argument) is not None:  # create a named branch  # line 453
        Exit("Branch '%s' already exists. Cannot proceed" % argument)  # create a named branch  # line 453
    branch = max(m.branches.keys()) + 1  # next branch's key - this isn't atomic but we assume single-user non-concurrent use here  # line 454
    debug("Branching to %sbranch b%02d%s%s..." % ("unnamed " if argument is None else "", branch, " '%s'" % argument if argument else "", " from last revision" if last else ""))  # line 455
    if last:  # line 456
        m.duplicateBranch(branch, argument)  # branch from branch's last revision  # line 457
    else:  # from file tree state  # line 458
        m.createBranch(branch, argument)  # branch from current file tree  # line 459
    if not stay:  # line 460
        m.branch = branch  # line 461
        m.saveBranches()  # line 462
    info("%s new %sbranch b%02d%s" % ("Continue work after branching" if stay else "Switched to", "unnamed " if argument is None else "", branch, " '%s'" % argument if argument else ""))  # line 463

def changes(argument: 'str'=None, options: '_coconut.typing.Sequence[str]'=[], onlys: '_coconut.typing.Optional[FrozenSet[str]]'=None, excps: '_coconut.typing.Optional[FrozenSet[str]]'=None) -> 'ChangeSet':  # line 465
    ''' Show changes of file tree vs. (last or specified) revision on current or specified branch. '''  # line 466
    m = Metadata(os.getcwd())  # type: Metadata  # line 467
    branch = None  # type: _coconut.typing.Optional[int]  # line 467
    revision = None  # type: _coconut.typing.Optional[int]  # line 467
    m.loadBranches()  # knows current branch  # line 468
    strict = '--strict' in options or m.strict  # type: bool  # line 469
    branch, revision = m.parseRevisionString(argument)  # line 470
    if branch not in m.branches:  # line 471
        Exit("Unknown branch")  # line 471
    m.loadBranch(branch)  # knows commits  # line 472
    revision = revision if revision >= 0 else len(m.commits) + revision  # negative indexing  # line 473
    if revision < 0 or revision > max(m.commits):  # line 474
        Exit("Unknown revision r%02d" % revision)  # line 474
    info("//|\\\\ Changes of file tree vs. revision '%s/r%02d'" % ((lambda _coconut_none_coalesce_item: "b%02d" % branch if _coconut_none_coalesce_item is None else _coconut_none_coalesce_item)(m.branches[branch].name), revision))  # line 475
    m.computeSequentialPathSet(branch, revision)  # load all commits up to specified revision  # line 476
    changes = m.findChanges(checkContent=strict, considerOnly=onlys if not m.track and not m.picky else conditionalIntersection(onlys, m.getTrackingPatterns() | m.getTrackingPatterns(branch)), dontConsider=excps)  # type: ChangeSet  # line 477
    m.listChanges(changes)  # line 478
    return changes  # for unit tests only  # line 479

def diff(argument: 'str'="", options: '_coconut.typing.Sequence[str]'=[], onlys: '_coconut.typing.Optional[FrozenSet[str]]'=None, excps: '_coconut.typing.Optional[FrozenSet[str]]'=None) -> 'None':  # line 481
    ''' Show text file differences of file tree vs. (last or specified) revision on current or specified branch. '''  # line 482
    m = Metadata(os.getcwd())  # type: Metadata  # line 483
    branch = None  # type: _coconut.typing.Optional[int]  # line 483
    revision = None  # type: _coconut.typing.Optional[int]  # line 483
    m.loadBranches()  # knows current branch  # line 484
    strict = '--strict' in options or m.strict  # type: bool  # line 485
    branch, revision = m.parseRevisionString(argument)  # line 486
    if branch not in m.branches:  # line 487
        Exit("Unknown branch")  # line 487
    m.loadBranch(branch)  # knows commits  # line 488
    revision = revision if revision >= 0 else len(m.commits) + revision  # negative indexing  # line 489
    if revision < 0 or revision > max(m.commits):  # line 490
        Exit("Unknown revision r%02d" % revision)  # line 490
    info("//|\\\\ Differences of file tree vs. revision '%s/r%02d'" % ((lambda _coconut_none_coalesce_item: "b%02d" % branch if _coconut_none_coalesce_item is None else _coconut_none_coalesce_item)(m.branches[branch].name), revision))  # line 491
    m.computeSequentialPathSet(branch, revision)  # load all commits up to specified revision  # line 492
    changes = m.findChanges(checkContent=strict, inverse=True, considerOnly=onlys if not m.track and not m.picky else conditionalIntersection(onlys, m.getTrackingPatterns() | m.getTrackingPatterns(branch)), dontConsider=excps)  # type: ChangeSet  # line 493
    onlyBinaryModifications = dataCopy(ChangeSet, changes, modifications={k: v for k, v in changes.modifications.items() if not m.isTextType(k)})  # type: ChangeSet  # line 494
    if modified(onlyBinaryModifications):  # line 495
        debug("//|\\\\ File changes")  # line 495
    m.listChanges(onlyBinaryModifications)  # only list modified binary files  # line 496

    if changes.modifications:  # TODO only text files, not binary  # line 498
        debug("%s//|\\\\ Textual modifications" % ("\n" if modified(onlyBinaryModifications) else ""))  # TODO only text files, not binary  # line 498
    for path, pinfo in changes.modifications.items():  # only consider modified files TODO also show A/D here? or replace listing above?  # line 499
        content = None  # type: _coconut.typing.Optional[bytes]  # ; othr:str[]; curr:str[]  # line 500
        if pinfo.size == 0:  # empty file contents  # line 501
            content = b""  # empty file contents  # line 501
        else:  # versioned file  # line 502
            content = m.restoreFile(None, branch, revision, pinfo)  # versioned file  # line 502
            assert content is not None  # versioned file  # line 502
        abspath = os.path.join(m.root, path.replace(SLASH, os.sep))  # current file  # line 503
        blocks = merge(file=content, intoname=abspath, diffOnly=True)  # type: List[MergeBlock]  # only determine change blocks  # line 504
        print("DIF %s%s" % (path, " <timestamp only>" if len(blocks) == 1 and blocks[0].tipe == MergeBlockType.KEEP else ""))  # line 505
        for block in blocks:  # line 506
            if block.tipe in [MergeBlockType.INSERT, MergeBlockType.REMOVE]:  # line 507
                pass  # TODO print some previous and following lines - which aren't accessible here anymore  # line 508
            if block.tipe == MergeBlockType.INSERT:  # TODO show color via curses?  # line 509
                for no, line in enumerate(block.lines):  # line 510
                    print("+++ %04d |%s|" % (no + block.line, line))  # line 511
            elif block.tipe == MergeBlockType.REMOVE:  # line 512
                for no, line in enumerate(block.lines):  # line 513
                    print("--- %04d |%s|" % (no + block.line, line))  # line 514
            elif block.tipe in [MergeBlockType.REPLACE, MergeBlockType.MODIFY]:  # TODO for MODIFY also show intra-line change ranges  # line 515
                for no, line in enumerate(block.replaces.lines):  # line 516
                    print("- | %04d |%s|" % (no + block.replaces.line, line))  # line 517
                for no, line in enumerate(block.lines):  # line 518
                    print("+ | %04d |%s|" % (no + block.line, line))  # line 519
#      elif block.tipe == MergeBlockType.KEEP: pass
#      elif block.tipe == MergeBlockType.MODIFY:  # intra-line modifications
#      elif block.tipe == MergeBlockType.MOVE:  # intra-line modifications

def commit(argument: '_coconut.typing.Optional[str]'=None, options: '_coconut.typing.Sequence[str]'=[], onlys: '_coconut.typing.Optional[FrozenSet[str]]'=None, excps: '_coconut.typing.Optional[FrozenSet[str]]'=None) -> 'None':  # line 524
    ''' Create new revision from file tree changes vs. last commit. '''  # line 525
    m = Metadata(os.getcwd())  # type: Metadata  # line 526
    m.loadBranches()  # knows current branch  # line 527
    if argument is not None and argument in m.tags:  # line 528
        Exit("Illegal commit message. It was already used as a tag name")  # line 528
    trackingPatterns = m.getTrackingPatterns()  # type: FrozenSet[str]  # SVN-like mode  # line 529
    if m.picky and not trackingPatterns:  # line 530
        Exit("No file patterns staged for commit in picky mode")  # line 530
    changes = None  # type: ChangeSet  # line 531
    m, branch, revision, changes, strict, force, trackingPatterns = exitOnChanges(None, options, commit=True, onlys=onlys, excps=excps)  # special flag creates new revision for detected changes, but abort if no changes  # line 532
    info((lambda _coconut_none_coalesce_item: "b%d" % m.branch if _coconut_none_coalesce_item is None else _coconut_none_coalesce_item)("Committing changes to branch '%s'..." % m.branches[m.branch].name))  # line 533
    m.integrateChangeset(changes, clear=True)  # update pathset to changeset only  # line 534
    m.saveCommit(m.branch, revision)  # revision has already been incremented  # line 535
    m.commits[revision] = CommitInfo(revision, longint(time.time() * 1000), argument)  # comment can be None  # line 536
    m.saveBranch(m.branch)  # line 537
    m.loadBranches()  # TODO is it necessary to load again?  # line 538
    if m.picky:  # line 539
        m.branches[m.branch] = dataCopy(BranchInfo, m.branches[m.branch], tracked=[], inSync=False)  # remove tracked patterns  # line 540
    else:  # track or simple mode  # line 541
        m.branches[m.branch] = dataCopy(BranchInfo, m.branches[m.branch], inSync=False)  # set branch dirty  # line 542
    if "--tag" in options and argument is not None:  # memorize unique tag  # line 543
        m.tags.append(argument)  # memorize unique tag  # line 543
    m.saveBranches()  # line 544
    info("Created new revision r%02d%s (+%02d/-%02d/*%02d)" % (revision, ((" '%s'" % argument) if argument is not None else ""), len(changes.additions), len(changes.deletions), len(changes.modifications)))  # line 545

def status() -> 'None':  # line 547
    ''' Show branches and current repository state. '''  # line 548
    m = Metadata(os.getcwd())  # type: Metadata  # line 549
    m.loadBranches()  # knows current branch  # line 550
    current = m.branch  # type: int  # line 551
    info("//|\\\\ Offline repository status")  # line 552
    print("Content checking %sactivated" % ("" if m.strict else "de"))  # line 553
    print("Data compression %sactivated" % ("" if m.compress else "de"))  # line 554
    print("Repository is in %s mode" % ("tracking" if m.track else ("picky" if m.picky else "simple")))  # line 555
    sl = max([len((lambda _coconut_none_coalesce_item: "" if _coconut_none_coalesce_item is None else _coconut_none_coalesce_item)(b.name)) for b in m.branches.values()])  # type: int  # line 556
    for branch in sorted(m.branches.values(), key=lambda b: b.number):  # line 557
        m.loadBranch(branch.number)  # knows commit history  # line 558
        print("  %s b%02d%s @%s (%s) with %d commits%s" % ("*" if current == branch.number else " ", branch.number, ((" %%%ds" % (sl + 2)) % ("'%s'" % branch.name)) if branch.name else "", strftime(branch.ctime), "in sync" if branch.inSync else "dirty", len(m.commits), ". Last comment: '%s'" % m.commits[max(m.commits)].message if m.commits[max(m.commits)].message else ""))  # line 559
    if m.track or m.picky and len(m.branches[m.branch].tracked) > 0:  # line 560
        info("\nTracked file patterns:")  # line 561
        print(ajoin("  | ", m.branches[m.branch].tracked, "\n"))  # line 562

def exitOnChanges(argument: '_coconut.typing.Optional[str]'=None, options: '_coconut.typing.Sequence[str]'=[], check: 'bool'=True, commit: 'bool'=False, onlys: '_coconut.typing.Optional[FrozenSet[str]]'=None, excps: '_coconut.typing.Optional[FrozenSet[str]]'=None) -> 'Tuple[Metadata, _coconut.typing.Optional[int], int, ChangeSet, bool, bool, FrozenSet[str]]':  # line 564
    ''' Common behavior for switch, update, delete, commit.
      Should not be called for picky mode, unless tracking patterns were added.
      check: stop program on detected change
      commit: don't stop on changes, because that's what we need in the operation
      Returns (Metadata, (current or target) branch, revision, set of changes vs. last commit on current branch, strict, force flags. '''  # line 569
    m = Metadata(os.getcwd())  # type: Metadata  # line 570
    m.loadBranches()  # knows current branch  # line 571
    force = '--force' in options  # type: bool  # line 572
    strict = '--strict' in options or m.strict  # type: bool  # line 573
    if argument is not None:  # line 574
        branch, revision = m.parseRevisionString(argument)  # for early abort  # line 575
        if branch is None:  # line 576
            Exit("Branch '%s' doesn't exist. Cannot proceed" % argument)  # line 576
    m.loadBranch(m.branch)  # knows last commits of *current* branch  # line 577

# Determine current changes
    trackingPatterns = m.getTrackingPatterns()  # type: FrozenSet[str]  # line 580
    m.computeSequentialPathSet(m.branch, max(m.commits))  # load all commits up to specified revision  # line 581
    changes = m.findChanges(m.branch if commit else None, max(m.commits) + 1 if commit else None, checkContent=strict, considerOnly=onlys if not (m.track or m.picky) else conditionalIntersection(onlys, trackingPatterns), dontConsider=excps)  # type: ChangeSet  # line 582
    if check and modified(changes) and not force:  # line 583
        m.listChanges(changes)  # line 584
        if not commit:  # line 585
            Exit("File tree contains changes. Use --force to proceed")  # line 585
    elif commit and not force:  #  and not check  # line 586
        Exit("Nothing to commit")  #  and not check  # line 586

    if argument is not None:  # branch/revision specified  # line 588
        m.loadBranch(branch)  # knows commits of target branch  # line 589
        revision = revision if revision >= 0 else len(m.commits) + revision  # negative indexing  # line 590
        if revision < 0 or revision > max(m.commits):  # line 591
            Exit("Unknown revision r%02d" % revision)  # line 591
        return (m, branch, revision, changes, strict, force, m.getTrackingPatterns(branch))  # line 592
    return (m, m.branch, max(m.commits) + (1 if commit else 0), changes, strict, force, trackingPatterns)  # line 593

def switch(argument: 'str', options: '_coconut.typing.Sequence[str]'=[], onlys: '_coconut.typing.Optional[FrozenSet[str]]'=None, excps: '_coconut.typing.Optional[FrozenSet[str]]'=None) -> 'None':  # line 595
    ''' Continue work on another branch, replacing file tree changes. '''  # line 596
    changes = None  # type: ChangeSet  # line 597
    m, branch, revision, changes, strict, force, trackingPatterns = exitOnChanges(argument, options)  # line 598
    info("//|\\\\ Switching to branch %sb%02d/r%02d" % ("'%s' " % m.branches[branch].name if m.branches[branch].name else "", branch, revision))  # line 599

# Determine file changes from other branch to current file tree
    if '--meta' in options:  # only switch meta data  # line 602
        m.branches[m.branch] = dataCopy(BranchInfo, m.branches[m.branch], tracked=m.branches[branch].tracked)  # line 603
    else:  # full file switch  # line 604
        m.computeSequentialPathSet(branch, revision)  # load all commits up to specified revision for target branch into memory  # line 605
        changes = m.findChanges(checkContent=strict, inverse=True, considerOnly=onlys if not m.track and not m.picky else conditionalIntersection(onlys, trackingPatterns | m.getTrackingPatterns(branch)), dontConsider=excps)  # determine difference of other branch vs. file tree (forced or in sync with current branch; "addition" means exists now and should be removed)  # line 606
        if not modified(changes):  # line 607
            info("No changes to current file tree")  # line 608
        else:  # integration required  # line 609
            for path, pinfo in changes.deletions.items():  # line 610
                m.restoreFile(path, branch, revision, pinfo, ensurePath=True)  # is deleted in current file tree: restore from branch to reach target  # line 611
                print("ADD " + path)  # line 612
            for path, pinfo in changes.additions.items():  # line 613
                os.unlink(os.path.join(m.root, path.replace(SLASH, os.sep)))  # is added in current file tree: remove from branch to reach target  # line 614
                print("DEL " + path)  # line 615
            for path, pinfo in changes.modifications.items():  # line 616
                m.restoreFile(path, branch, revision, pinfo)  # is modified in current file tree: restore from branch to reach target  # line 617
                print("MOD " + path)  # line 618
    m.branch = branch  # line 619
    m.saveBranches()  # store switched path info  # line 620
    info("Switched to branch %sb%02d/r%02d" % ("'%s' " % (m.branches[branch].name if m.branches[branch].name else ""), branch, revision))  # line 621

def update(argument: 'str', options: '_coconut.typing.Sequence[str]'=[], onlys: '_coconut.typing.Optional[FrozenSet[str]]'=None, excps: '_coconut.typing.Optional[FrozenSet[str]]'=None) -> 'None':  # line 623
    ''' Load and integrate a specified other branch/revision into current life file tree.
      In tracking mode, this also updates the set of tracked patterns.
      User options for merge operation: --add (don't remove), --rm (don't insert), --add-lines/--rm-lines (inside each file)
      User options for conflict resolution: --theirs/--mine/--ask
  '''  # line 628
    mrg = firstOfMap({"--add": MergeOperation.INSERT, "--rm": MergeOperation.REMOVE}, options, MergeOperation.BOTH)  # type: int  # default operation is replicate remove state for non-conflicting cases (insertions/deletions)  # line 629
    res = firstOfMap({'--theirs': ConflictResolution.THEIRS, '--mine': ConflictResolution.MINE}, options, ConflictResolution.NEXT)  # type: int  # NEXT means deeper level  # line 630
    mrgline = firstOfMap({'--add-lines': MergeOperation.INSERT, '--rm-lines': MergeOperation.REMOVE}, options, mrg)  # type: int  # default operation for modified files is same as for files  # line 631
    resline = firstOfMap({'--theirs-lines': ConflictResolution.THEIRS, '--mine-lines': ConflictResolution.MINE}, options, ConflictResolution.ASK)  # type: int  # line 632
    m = Metadata(os.getcwd())  # type: Metadata  # TODO same is called inside stop on changes - could return both current and designated branch instead  # line 633
    m.loadBranches()  # line 634
    changes = None  # type: ChangeSet  # line 634
    currentBranch = m.branch  # type: _coconut.typing.Optional[int]  # line 635
    m, branch, revision, changes, strict, force, trackingPatterns = exitOnChanges(argument, options, check=False, onlys=onlys, excps=excps)  # don't check for current changes, only parse arguments  # line 636
    debug("Integrating changes from '%s/r%02d' into file tree..." % ((lambda _coconut_none_coalesce_item: "b%02d" % branch if _coconut_none_coalesce_item is None else _coconut_none_coalesce_item)(m.branches[branch].name), revision))  # line 637

# Determine file changes from other branch over current file tree
    m.computeSequentialPathSet(branch, revision)  # load all commits up to specified revision for branch to integrate  # line 640
    trackingUnion = trackingPatterns | m.getTrackingPatterns(branch)  # type: FrozenSet[str]  # line 641
    changes = m.findChanges(checkContent=strict, inverse=True, considerOnly=onlys if not m.track and not m.picky else conditionalIntersection(onlys, trackingUnion), dontConsider=excps)  # determine difference of other branch vs. file tree. "addition" means exists now but not in other, and should be removed unless in tracking mode  # line 642
    if not (mrg & MergeOperation.INSERT and changes.additions or (mrg & MergeOperation.REMOVE and changes.deletions) or changes.modifications):  # no file ops  # line 643
        if trackingUnion != trackingPatterns:  # nothing added  # line 644
            info("No file changes detected, but tracking patterns were merged (run 'sos switch /-1 --meta' to undo)")  # TODO write test to see if this works  # line 645
        else:  # line 646
            info("Nothing to update")  # but write back updated branch info below  # line 647
    else:  # integration required  # line 648
        for path, pinfo in changes.deletions.items():  # deletions mark files not present in current file tree -> needs additon  # line 649
            if mrg & MergeOperation.INSERT:  # deleted in current file tree: restore from branch to reach target  # line 650
                m.restoreFile(path, branch, revision, pinfo, ensurePath=True)  # deleted in current file tree: restore from branch to reach target  # line 650
            print("ADD " + path if mrg & MergeOperation.INSERT else "(A) " + path)  # line 651
        for path, pinfo in changes.additions.items():  # line 652
            if m.track or m.picky:  # because untracked files of other branch cannot be detected (which is good)  # line 653
                Exit("This should never happen")  # because untracked files of other branch cannot be detected (which is good)  # line 653
            if mrg & MergeOperation.REMOVE:  # line 654
                os.unlink(m.root + os.sep + path.replace(SLASH, os.sep))  # line 654
            print("DEL " + path if mrg & MergeOperation.REMOVE else "(D) " + path)  # not contained in other branch, but maybe kept  # line 655
        for path, pinfo in changes.modifications.items():  # line 656
            into = os.path.join(m.root, path.replace(SLASH, os.sep))  # type: str  # line 657
            binary = not m.isTextType(path)  # line 658
            if res & ConflictResolution.ASK or (binary and res == ConflictResolution.NEXT):  # TODO this may ask user even if no interaction was asked for (check line level for interactivity fist)  # line 659
                print(("MOD " + path if not binary else "BIN ") + path)  # line 660
                reso = {"i": ConflictResolution.MINE, "t": ConflictResolution.THEIRS, "m": ConflictResolution.NEXT}.get(user_input(" Resolve: *M[I]ne, [T]heirs, [M]erge: (I)").strip().lower(), ConflictResolution.MINE)  # line 661
                debug("User selected %d" % reso)  # line 662
            else:  # line 663
                reso = res  # line 663
            if reso & ConflictResolution.THEIRS:  # line 664
                m.readOrCopyVersionedFile(branch, revision, pinfo.nameHash, toFile=into)  # blockwise copy of contents  # line 665
                print("THR " + path)  # line 666
            elif reso & ConflictResolution.MINE:  # line 667
                print("MNE " + path)  # nothing to do! same as skip  # line 668
            else:  # NEXT: line-based merge  # line 669
                file = m.readOrCopyVersionedFile(branch, revision, pinfo.nameHash) if pinfo.size > 0 else b''  # type: _coconut.typing.Optional[bytes]  # parse lines TODO decode etc.  # line 670
                if file is not None:  # if None, error message was already logged  # line 671
                    contents = merge(file=file, intoname=into, mergeOperation=mrgline, conflictResolution=resline)  # type: bytes  # line 672
                    with open(path, "wb") as fd:  # TODO write to temp file first  # line 673
                        fd.write(contents)  # TODO write to temp file first  # line 673
    info("Integrated changes from '%s/r%02d' into file tree" % ((lambda _coconut_none_coalesce_item: "b%02d" % branch if _coconut_none_coalesce_item is None else _coconut_none_coalesce_item)(m.branches[branch].name), revision))  # line 674
    m.branches[currentBranch] = dataCopy(BranchInfo, m.branches[currentBranch], inSync=False, tracked=list(trackingUnion))  # TODO really? it's a change that cannot be undone easily by the user  # line 675
    m.branch = currentBranch  # need to restore setting before saving TODO operate on different objects instead  # line 676
    m.saveBranches()  # line 677

def delete(argument: 'str', options: '_coconut.typing.Sequence[str]'=[]) -> 'None':  # line 679
    ''' Remove a branch entirely. '''  # line 680
    m, branch, revision, changes, strict, force, trackingPatterns = exitOnChanges(None, options)  # line 681
    if len(m.branches) == 1:  # line 682
        Exit("Cannot remove the only remaining branch. Use 'sos online' to leave offline mode")  # line 682
    branch, revision = m.parseRevisionString(argument)  # not from exitOnChanges, because we have to set argument to None there  # line 683
    if branch is None or branch not in m.branches:  # line 684
        Exit("Unknown branch")  # line 684
    debug("Removing branch %d%s..." % (branch, " '%s'" % m.branches[branch].name if m.branches[branch].name else ""))  # line 685
    binfo = m.removeBranch(branch)  # need to keep a reference to removed entry for output below  # line 686
    info("Branch b%02d%s removed" % (branch, " '%s'" % binfo.name if binfo.name else ""))  # line 687

def add(relPath: 'str', pattern: 'str', options: '_coconut.typing.Sequence[str]'=[]) -> 'None':  # line 689
    ''' Add a tracked files pattern to current branch's tracked files. '''  # line 690
    force = '--force' in options  # type: bool  # line 691
    m = Metadata(os.getcwd())  # type: Metadata  # line 692
    m.loadBranches()  # line 693
    if not m.track and not m.picky:  # line 694
        Exit("Repository is in simple mode. Use 'offline --track' or 'offline --picky' instead")  # line 694
    if pattern in m.branches[m.branch].tracked:  # line 695
        Exit("Pattern '%s' already tracked" % pattern)  # line 695
    if not force and not os.path.exists(relPath.replace(SLASH, os.sep)):  # line 696
        Exit("The pattern folder doesn't exist. Use --force to add it anyway")  # line 696
    if not force and len(fnmatch.filter(os.listdir(os.path.abspath(relPath.replace(SLASH, os.sep))), os.path.basename(pattern.replace(SLASH, os.sep)))) == 0:  # doesn't match any current file  # line 697
        Exit("Pattern doesn't match any file in specified folder. Use --force to add it anyway")  # line 698
    m.branches[m.branch].tracked.append(pattern)  # TODO set inSync flag to False? same for rm  # line 699
    m.saveBranches()  # line 700
    info("Added tracking pattern '%s' for folder '%s'" % (os.path.basename(pattern.replace(SLASH, os.sep)), os.path.abspath(relPath)))  # line 701

def remove(relPath: 'str', pattern: 'str') -> 'None':  # line 703
    ''' Remove a tracked files pattern from current branch's tracked files. '''  # line 704
    m = Metadata(os.getcwd())  # type: Metadata  # line 705
    m.loadBranches()  # line 706
    if not m.track and not m.picky:  # line 707
        Exit("Repository is in simple mode. Needs 'offline --track' or 'offline --picky' instead")  # line 707
    if pattern not in m.branches[m.branch].tracked:  # line 708
        suggestion = _coconut.set()  # type: Set[str]  # line 709
        for pat in m.branches[m.branch].tracked:  # line 710
            if fnmatch.fnmatch(pattern, pat):  # line 711
                suggestion.add(pat)  # line 711
        if suggestion:  # TODO use same wording as in move  # line 712
            print("Do you mean any of the following tracked globs? '%s'" % (", ".join(sorted(suggestion))))  # TODO use same wording as in move  # line 712
        Exit("Tracked pattern '%s' not found" % pattern)  # line 713
    m.branches[m.branch].tracked.remove(pattern)  # line 714
    m.saveBranches()  # line 715
    info("Removed tracking pattern '%s' for folder '%s'" % (os.path.basename(pattern), os.path.abspath(relPath.replace(SLASH, os.sep))))  # line 716

def ls(argument: '_coconut.typing.Optional[str]'=None, options: '_coconut.typing.Sequence[str]'=[]) -> 'None':  # line 718
    ''' List specified directory, augmenting with repository metadata. '''  # line 719
    cwd = os.getcwd() if argument is None else argument  # type: str  # line 720
    m = Metadata(cwd)  # type: Metadata  # line 721
    m.loadBranches()  # line 722
    info("Repository is in %s mode" % ("tracking" if m.track else ("picky" if m.picky else "simple")))  # line 723
    relPath = os.path.relpath(cwd, m.root).replace(os.sep, SLASH)  # type: str  # line 724
    trackingPatterns = m.getTrackingPatterns() if m.track or m.picky else _coconut.frozenset()  # type: _coconut.typing.Optional[FrozenSet[str]]  # for current branch  # line 725
    if '--patterns' in options:  # line 726
        out = ajoin("TRK ", [p for p in trackingPatterns if os.path.dirname(p).replace(os.sep, SLASH) == relPath], nl="\n")  # type: str  # line 727
        if out:  # line 728
            print(out)  # line 728
        return  # line 729
    files = list(sorted((entry for entry in os.listdir(cwd) if os.path.isfile(entry))))  # type: List[str]  # line 730
    for file in files:  # for each file list all tracking patterns that match, or none (e.g. in picky mode after commit)  # line 731
        ignore = None  # type: _coconut.typing.Optional[str]  # line 732
        for ig in m.c.ignores:  # line 733
            if fnmatch.fnmatch(file, ig):  # remember first match TODO document this  # line 734
                ignore = ig  # remember first match TODO document this  # line 734
                break  # remember first match TODO document this  # line 734
        if ig:  # line 735
            for wl in m.c.ignoresWhitelist:  # line 736
                if fnmatch.fnmatch(file, wl):  # found a white list entry for ignored file, undo ignoring it  # line 737
                    ignore = None  # found a white list entry for ignored file, undo ignoring it  # line 737
                    break  # found a white list entry for ignored file, undo ignoring it  # line 737
        if not ignore:  # line 738
            matches = []  # type: List[str]  # line 739
            for pattern in (p for p in trackingPatterns if os.path.dirname(p).replace(os.sep, SLASH) == relPath):  # only patterns matching current folder  # line 740
                if fnmatch.fnmatch(file, os.path.basename(pattern)):  # line 741
                    matches.append(pattern)  # line 741
        print("%s %s%s" % ("IGN" if ignore is not None else ("TRK" if len(matches) > 0 else "..."), file, ' by "%s"' % ignore if ignore is not None else (" by " + ";".join(['"%s"' % match for match in matches]) if len(matches) > 0 else "")))  # line 742

def log(options: '_coconut.typing.Sequence[str]') -> 'None':  # line 744
    ''' List previous commits on current branch. '''  # line 745
    m = Metadata(os.getcwd())  # type: Metadata  # line 746
    m.loadBranches()  # knows current branch  # line 747
    m.loadBranch(m.branch)  # knows commit history  # line 748
    info((lambda _coconut_none_coalesce_item: "r%02d" % m.branch if _coconut_none_coalesce_item is None else _coconut_none_coalesce_item)("//|\\\\ Offline commit history of branch '%s'" % m.branches[m.branch].name))  # TODO also retain "from branch/revision" on branching?  # line 749
    nl = len("%d" % max(m.commits))  # determine space needed for revision  # line 750
    changeset = m.computeSequentialPathSetIterator(m.branch, max(m.commits))  # line 751
    maxWidth = max([wcswidth((lambda _coconut_none_coalesce_item: "" if _coconut_none_coalesce_item is None else _coconut_none_coalesce_item)(commit.message)) for commit in m.commits.values()])  # type: int  # line 752
    for no in range(max(m.commits) + 1):  # line 753
        commit = m.commits[no]  # type: CommitInfo  # line 754
        changes = next(changeset)  # type: ChangeSet  # side-effect: updates m.paths  # line 755
        newTextFiles = len([file for file in changes.additions.keys() if m.isTextType(file)])  # type: int  # line 756
        print("  %s r%s @%s (+%02d/-%02d/*%02d +%02dT/%05.1f%%) |%s|" % ("*" if commit.number == max(m.commits) else " ", ("%%%ds" % nl) % commit.number, strftime(commit.ctime), len(changes.additions), len(changes.deletions), len(changes.modifications), newTextFiles, 0. if len(changes.additions) == 0 else newTextFiles * 100. / len(changes.additions), ((lambda _coconut_none_coalesce_item: "" if _coconut_none_coalesce_item is None else _coconut_none_coalesce_item)(commit.message)).ljust(maxWidth)))  # line 757
        if '--changes' in options:  # line 758
            m.listChanges(changes)  # line 758

def config(argument: 'str', options: 'List[str]'=[]) -> 'None':  # line 760
    if argument not in ["set", "unset", "show", "list", "add", "rm"]:  # line 761
        Exit("Unknown config command")  # line 761
    if not configr:  # line 762
        Exit("Cannot execute config command. 'configr' module not installed")  # line 762
    c = loadConfig()  # type: Union[configr.Configr, Accessor]  # line 763
    if argument == "set":  # line 764
        if len(options) < 2:  # line 765
            Exit("No key nor value specified")  # line 765
        if options[0] not in (["defaultbranch"] + CONFIGURABLE_FLAGS + CONFIGURABLE_LISTS):  # line 766
            Exit("Unsupported key %r" % options[0])  # line 766
        if options[0] in CONFIGURABLE_FLAGS and options[1].lower() not in TRUTH_VALUES + FALSE_VALUES:  # line 767
            Exit("Cannot set flag to '%s'. Try on/off instead" % options[1].lower())  # line 767
        c[options[0]] = options[1].lower() in TRUTH_VALUES if options[0] in CONFIGURABLE_FLAGS else (options[1].strip() if options[0] not in CONFIGURABLE_LISTS else safeSplit(options[1], ";"))  # TODO sanitize texts?  # line 768
    elif argument == "unset":  # line 769
        if len(options) < 1:  # line 770
            Exit("No key specified")  # line 770
        if options[0] not in c.keys():  # line 771
            Exit("Unknown key")  # line 771
        del c[options[0]]  # line 772
    elif argument == "add":  # line 773
        if len(options) < 2:  # line 774
            Exit("No key nor value specified")  # line 774
        if options[0] not in CONFIGURABLE_LISTS:  # line 775
            Exit("Unsupported key for add %r" % options[0])  # line 775
        if options[0] not in c.keys():  # add list  # line 776
            c[options[0]] = [options[1]]  # add list  # line 776
        elif options[1] in c[options[0]]:  # line 777
            Exit("Value already contained")  # line 777
        c[options[0]].append(options[1])  # line 778
    elif argument == "rm":  # line 779
        if len(options) < 2:  # line 780
            Exit("No key nor value specified")  # line 780
        if options[0] not in c.keys():  # line 781
            Exit("Unknown key specified: %r" % options[0])  # line 781
        if options[1] not in c[options[0]]:  # line 782
            Exit("Unknown value: %r" % options[1])  # line 782
        c[options[0]].remove(options[1])  # line 783
    else:  # Show  # line 784
        for k, v in sorted(c.items()):  # line 785
            print("%s => %r" % (k, v))  # line 785
        return  # line 786
    f, g = saveConfig(c)  # line 787
    if f is None:  # line 788
        error("Error saving user configuration: %r" % g)  # line 788

def move(relPath: 'str', pattern: 'str', newRelPath: 'str', newPattern: 'str', options: 'List[str]'=[]) -> 'None':  # line 790
    ''' Path differs: Move files, create folder if not existing. Pattern differs: Attempt to rename file, unless exists in target or not unique. '''  # line 791
    force = '--force' in options  # type: bool  # line 792
    soft = '--soft' in options  # type: bool  # line 793
    if not os.path.exists(relPath.replace(SLASH, os.sep)) and not force:  # line 794
        Exit("Source folder doesn't exist. Use --force to proceed anyway")  # line 794
    matching = fnmatch.filter(os.listdir(relPath.replace(SLASH, os.sep)) if os.path.exists(relPath.replace(SLASH, os.sep)) else [], os.path.basename(pattern))  # type: _coconut.typing.Sequence[str]  # find matching files in source  # line 795
    if not matching and not force:  # line 796
        Exit("No files match the specified file or glob pattern. Use --force to proceed anyway")  # line 796
    m = Metadata(os.getcwd())  # type: Metadata  # line 797
    m.loadBranches()  # knows current branch  # line 798
    if not m.track and not m.picky:  # line 799
        Exit("Repository is in simple mode. Simply use basic file operations to modify files, then execute 'sos commit' to version the changes")  # line 799
    if pattern not in m.branches[m.branch].tracked:  # line 800
        for tracked in (t for t in m.branches[m.branch].tracked if os.path.dirname(t) == relPath):  # for all patterns of the same source folder  # line 801
            alternative = fnmatch.filter(matching, os.path.basename(tracked))  # type: _coconut.typing.Sequence[str]  # find if it matches any of the files in the source folder, too  # line 802
            if alternative:  # line 803
                info("  '%s' matches %d files" % (tracked, len(alternative)))  # line 803
        if not (force or soft):  # line 804
            Exit("File or glob pattern '%s' is not tracked on current branch. 'sos move' only works on tracked patterns" % pattern)  # line 804
    basePattern = os.path.basename(pattern)  # type: str  # pure glob without folder  # line 805
    newBasePattern = os.path.basename(newPattern)  # type: str  # line 806
    if basePattern.count("*") < newBasePattern.count("*") or (basePattern.count("?") - basePattern.count("[?]")) < (newBasePattern.count("?") - newBasePattern.count("[?]")) or (basePattern.count("[") - basePattern.count("\\[")) < (newBasePattern.count("[") - newBasePattern.count("\\[")) or (basePattern.count("]") - basePattern.count("\\]")) < (newBasePattern.count("]") - newBasePattern.count("\\]")):  # line 807
        Exit("Glob markers from '%s' to '%s' don't match, cannot move/rename tracked matching files" % (basePattern, newBasePattern))  # line 811
    oldTokens = None  # type: _coconut.typing.Sequence[GlobBlock]  # line 812
    newToken = None  # type: _coconut.typing.Sequence[GlobBlock]  # line 812
    oldTokens, newTokens = tokenizeGlobPatterns(os.path.basename(pattern), os.path.basename(newPattern))  # line 813
    matches = convertGlobFiles(matching, oldTokens, newTokens)  # type: _coconut.typing.Sequence[Tuple[str, str]]  # computes list of source - target filename pairs  # line 814
    if len({st[1] for st in matches}) != len(matches):  # line 815
        Exit("Some target filenames are not unique and different move/rename actions would point to the same target file")  # line 815
    matches = reorderRenameActions(matches, exitOnConflict=not soft)  # attempts to find conflict-free renaming order, or exits  # line 816
    if os.path.exists(newRelPath):  # line 817
        exists = [filename[1] for filename in matches if os.path.exists(os.path.join(newRelPath, filename[1]).replace(SLASH, os.sep))]  # type: _coconut.typing.Sequence[str]  # line 818
        if exists and not (force or soft):  # line 819
            Exit("%s files would write over existing files in %s cases. Use --force to execute it anyway" % ("Moving" if relPath != newRelPath else "Renaming", "all" if len(exists) == len(matches) else "some"))  # line 819
    else:  # line 820
        os.makedirs(os.path.abspath(newRelPath.replace(SLASH, os.sep)))  # line 820
    if not soft:  # perform actual renaming  # line 821
        for (source, target) in matches:  # line 822
            try:  # line 823
                shutil.move(os.path.abspath(os.path.join(relPath, source).replace(SLASH, os.sep)), os.path.abspath(os.path.join(newRelPath, target).replace(SLASH, os.sep)))  # line 823
            except Exception as E:  # one error can lead to another in case of delicate renaming order  # line 824
                error("Cannot move/rename file '%s' to '%s'" % (source, os.path.join(newRelPath, target)))  # one error can lead to another in case of delicate renaming order  # line 824
    m.branches[m.branch].tracked[m.branches[m.branch].tracked.index(pattern)] = newPattern  # line 825
    m.saveBranches()  # line 826

def parse(root: 'str', cwd: 'str'):  # line 828
    ''' Main operation. Main has already chdir into VCS root folder, cwd is original working directory for add, rm. '''  # line 829
    debug("Parsing command-line arguments...")  # line 830
    command = sys.argv[1].strip() if len(sys.argv) > 1 else ""  # line 831
    argument = sys.argv[2].strip() if len(sys.argv) > 2 and not sys.argv[2].startswith("--") else None  # line 832
    options = sys.argv[3:] if command == "config" else [c for c in sys.argv[2:] if c.startswith("--")]  # consider second parameter for no-arg command, otherwise from third on  # line 833
    onlys, excps = parseOnlyOptions(cwd, options)  # extracts folder-relative information for changes, commit, diff, switch, update  # line 834
    debug("Processing command %r with argument '%s' and options %r." % ("" if command is None else command, "" if argument is None else argument, options))  # line 835
    if command[:1] in "amr":  # line 836
        relPath, pattern = relativize(root, os.path.join(cwd, argument))  # line 836
    if command[:1] == "m":  # line 837
        if not options:  # line 838
            Exit("Need a second file pattern argument as target for move/rename command")  # line 838
        newRelPath, newPattern = relativize(root, os.path.join(cwd, options[0]))  # TODO add error message if target pattern is missing (???)  # line 839
    if command[:1] == "a":  # line 840
        add(relPath, pattern, options)  # line 840
    elif command[:1] == "b":  # line 841
        branch(argument, options)  # line 841
    elif command[:2] == "ch":  # line 842
        changes(argument, options, onlys, excps)  # line 842
    elif command[:3] == "com":  # line 843
        commit(argument, options, onlys, excps)  # line 843
    elif command[:2] == "ci":  # line 844
        commit(argument, options, onlys, excps)  # line 844
    elif command[:3] == 'con':  # line 845
        config(argument, options)  # line 845
    elif command[:2] == "de":  # line 846
        delete(argument, options)  # line 846
    elif command[:2] == "di":  # line 847
        diff(argument, options, onlys, excps)  # line 847
    elif command[:1] == "h":  # line 848
        usage()  # line 848
    elif command[:2] == "lo":  # line 849
        log(options)  # line 849
    elif command[:2] == "li":  # line 850
        ls(argument, options)  # line 850
    elif command[:2] == "ls":  # line 851
        ls(argument, options)  # line 851
    elif command[:1] == "m":  # line 852
        move(relPath, pattern, newRelPath, newPattern, options[1:])  # line 852
    elif command[:2] == "of":  # line 853
        offline(argument, options)  # line 853
    elif command[:2] == "on":  # line 854
        online(options)  # line 854
    elif command[:1] == "r":  # line 855
        remove(relPath, pattern)  # line 855
    elif command[:2] == "st":  # line 856
        status()  # line 856
    elif command[:2] == "sw":  # line 857
        switch(argument, options, onlys, excps)  # line 857
    elif command[:1] == "u":  # line 858
        update(argument, options, onlys, excps)  # line 858
    else:  # line 859
        Exit("Unknown command '%s'" % command)  # line 859
    sys.exit(0)  # line 860

def main() -> 'None':  # line 862
    global debug, info, warn, error  # line 863
    logging.basicConfig(level=level, stream=sys.stderr, format=("%(asctime)-23s %(levelname)-8s %(name)s:%(lineno)d | %(message)s" if '--log' in sys.argv else "%(message)s"))  # line 864
    _log = Logger(logging.getLogger(__name__))  # line 865
    debug, info, warn, error = _log.debug, _log.info, _log.warn, _log.error  # line 865
    for option in (o for o in ['--log', '--verbose', '-v', '--sos'] if o in sys.argv):  # clean up program arguments  # line 866
        sys.argv.remove(option)  # clean up program arguments  # line 866
    if '--help' in sys.argv or len(sys.argv) < 2:  # line 867
        usage()  # line 867
        Exit()  # line 867
    command = sys.argv[1] if len(sys.argv) > 1 else None  # type: _coconut.typing.Optional[str]  # line 868
    root, vcs, cmd = findSosVcsBase()  # root is None if no .sos folder exists up the folder tree (still working online); vcs is checkout/repo root folder; cmd is the VCS base command  # line 869
    debug("Found root folders for SOS|VCS: %s|%s" % ("" if root is None else root, "" if vcs is None else vcs))  # line 870
    defaults["defaultbranch"] = vcsBranches.get(cmd, "trunk")  # sets dynamic default with SVN fallback  # line 871
    if force_sos or root is not None or ("" if command is None else command)[:2] == "of" or ("" if command is None else command)[:1] == "h":  # in offline mode or just going offline TODO what about git config?  # line 872
        cwd = os.getcwd()  # line 873
        os.chdir(cwd if command[:2] == "of" else cwd if root is None else root)  # line 874
        parse(root, cwd)  # line 875
    elif cmd is not None:  # online mode - delegate to VCS  # line 876
        info("SOS: Running '%s %s'" % (cmd, " ".join(sys.argv[1:])))  # line 877
        import subprocess  # only required in this section  # line 878
        process = subprocess.Popen([cmd] + sys.argv[1:], shell=False, stdin=subprocess.PIPE, stdout=sys.stdout, stderr=sys.stderr)  # line 879
        inp = ""  # type: str  # line 880
        while True:  # line 881
            so, se = process.communicate(input=inp)  # line 882
            if process.returncode is not None:  # line 883
                break  # line 883
            inp = sys.stdin.read()  # line 884
        if sys.argv[1][:2] == "co" and process.returncode == 0:  # successful commit - assume now in sync again (but leave meta data folder with potential other feature branches behind until "online")  # line 885
            if root is None:  # line 886
                Exit("Cannot determine VCS root folder: Unable to mark repository as synchronized and will show a warning when leaving offline mode")  # line 886
            m = Metadata(root)  # line 887
            m.loadBranches()  # read repo  # line 888
            m.branches[m.branch] = dataCopy(BranchInfo, m.branches[m.branch], inSync=True)  # mark as committed  # line 889
            m.saveBranches()  # line 890
    else:  # line 891
        Exit("No offline repository present, and unable to detect VCS file tree")  # line 891


# Main part
level = logging.DEBUG if os.environ.get("DEBUG", "False").lower() == "true" or '--verbose' in sys.argv or '-v' in sys.argv else logging.INFO  # line 895
force_sos = '--sos' in sys.argv  # line 896
_log = Logger(logging.getLogger(__name__))  # line 897
debug, info, warn, error = _log.debug, _log.info, _log.warn, _log.error  # line 897
if __name__ == '__main__':  # line 898
    main()  # line 898
