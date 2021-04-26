import hashlib
import operator
import os
import pathlib
import struct
import typing as tp

from pyvcs.objects import hash_object


class GitIndexEntry(tp.NamedTuple):
    # @see: https://github.com/git/git/blob/master/Documentation/technical/index-format.txt
    ctime_s: int
    ctime_n: int
    mtime_s: int
    mtime_n: int
    dev: int
    ino: int
    mode: int
    uid: int
    gid: int
    size: int
    sha1: bytes
    flags: int
    name: str

    def pack(self) -> bytes:
        values = (
        self.ctime_s,
        self.ctime_n,
        self.mtime_s,
        self.mtime_n,
        self.dev,
        self.ino,
        self.mode,
        self.uid,
        self.gid,
        self.size,
        self.sha1,
        self.flags,
        self.name.encode()
        )

        packed = struct.pack(f">10i20sh{len(self.name)}s3x", *values)
        return packed

    @staticmethod
    def unpack(data: bytes) -> "GitIndexEntry":
        format = f">10i20sh{len(data) - 62}s"
        unpacked = struct.unpack(format, data)
        unpacked_list = list(unpacked)
        unpacked_list[-1] = unpacked_list[-1][:-3].decode()
        return GitIndexEntry(*unpacked_list)



def read_index(gitdir: pathlib.Path) -> tp.List[GitIndexEntry]:
    """
    index = []

    path_index = gitdir / "index"

    try :
        f = path_index.open(mode = "rb")
        data = f.read()
    except:
        return index

    """
    ...

def write_index(gitdir: pathlib.Path, entries: tp.List[GitIndexEntry]) -> None:
    # PUT YOUR CODE HERE
    ...


def ls_files(gitdir: pathlib.Path, details: bool = False) -> None:
    # PUT YOUR CODE HERE
    ...


def update_index(gitdir: pathlib.Path, paths: tp.List[pathlib.Path], write: bool = True) -> None:
    # PUT YOUR CODE HERE
    ...
