# Copyright (C) 2017 Allen Li
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Working with hashed archives."""

import filecmp
import hashlib
import logging
import os
from pathlib import Path
from pathlib import PurePath

_BUFSIZE = 2 ** 20
_HASHDIR = 'hash'

logger = logging.getLogger(__name__)


def find_hashdir(start: 'PathLike') -> Path:
    """Find hash archive directory."""
    path = Path(start).resolve()
    if path.is_file():
        path = path.parent
    while True:
        if _HASHDIR in os.listdir(path):
            return path / _HASHDIR
        if path.parent == path:
            raise Error('rootdir not found')
        path = path.parent


def add_all(hashdir: 'PathLike', paths: 'Iterable[PathLike]', merge=False):
    """Add files and directories to a hash archive."""
    for path in paths:
        if os.path.isdir(path):
            add_dir(hashdir, path, merge=merge)
        else:
            add_file(hashdir, path, merge=merge)


def add_dir(hashdir: 'PathLike', directory: 'PathLike', merge=False):
    """Add a directory's files to a hash archive."""
    for root, dirs, files in os.walk(directory):
        for filename in files:
            path = os.path.join(root, filename)
            add_file(hashdir, path, merge=merge)


def add_file(hashdir: 'PathLike', path: 'PathLike', merge=False):
    """Add a file to a hash archive.

    If the file is already in the hash archive and is the same file,
    return without doing anything else.  If it is not the same file,
    behavior is determined by merge.  If merge is False, raise
    FileExistsError.  If merge is True, replace the file with a hard
    link to the file in the hash archive if the content is the same.
    """
    logger.info('Adding file %s', path)
    hashed_path = Path(hashdir, _hashed_path(path))
    if not hashed_path.exists():
        logger.info('Storing %s to %s', path, hashed_path)
        hashed_path.parent.mkdir(exist_ok=True)
        os.link(path, hashed_path)
        return
    if hashed_path.samefile(os.fspath(path)):
        logger.info('%s already stored to %s', path, hashed_path)
        return
    if not (merge and filecmp.cmp(path, hashed_path, shallow=False)):
        raise FileExistsError(f'{hashed_path} exists but different from {path}')
    os.unlink(path)
    os.link(hashed_path, path)


def _hashed_path(path: 'PathLike') -> PurePath:
    """Return hashed path for a file."""
    with open(path, 'rb') as f:
        digest = _hexdigest(f)
    ext = os.path.splitext(path)[1]
    return PurePath(digest[:2], f'{digest[2:]}{ext}')


def _hexdigest(file):
    """Return hex digest for file."""
    h = hashlib.sha256()
    _feed(h, file)
    return h.hexdigest()


def _feed(hasher, file):
    """Feed bytes in a file to a hasher."""
    while True:
        b = file.read(_BUFSIZE)
        if not b:
            break
        hasher.update(b)


class Error(Exception):
    pass


class FileExistsError(Exception):
    pass
