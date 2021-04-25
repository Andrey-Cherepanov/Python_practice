import hashlib
import os
import pathlib
import re
import stat
import typing as tp
import zlib

from pyvcs.refs import update_ref
from pyvcs.repo import repo_find


def hash_object(data: bytes, fmt: str, write: bool = False) -> str:
    header = f"{fmt} {len(data)}\0"
    store = header.encode() + data
    result = hashlib.sha1(store).hexdigest()
    content = zlib.compress(store)

    if write:
        workdir = pathlib.Path(".").absolute()
        gitdir = repo_find(workdir)

        if not pathlib.Path.exists(gitdir / "objects" / result[0:2]):
            (gitdir / "objects" / result[0:2]).mkdir()
        if not pathlib.Path.exists(gitdir / "objects" / result[0:2] / result[:2]):
            (gitdir / "objects" / result[0:2] / result[2:]).write_bytes(content)

    return result


def resolve_object(obj_name: str, gitdir: pathlib.Path) -> tp.List[str]:
    objs = []
    if len(obj_name) > 40 or len(obj_name) < 4:
        raise Exception(f"Not a valid object name {obj_name}")

    obj_dir = gitdir / "objects" / obj_name[:2]

    for obj in obj_dir.iterdir():
        if obj_name[2:] in obj.parts[-1]:
            objs.append(
            str(obj.parts[-2]) + str(obj.parts[-1])
            )

    if not objs :
        raise Exception(f"Not a valid object name {obj_name}")

    return objs


def find_object(obj_name: str, gitdir: pathlib.Path) -> str:
    # PUT YOUR CODE HERE
    ...


def read_object(sha: str, gitdir: pathlib.Path) -> tp.Tuple[str, bytes]:
    path = gitdir / "objects" / sha[:2] / sha[2:]
    with path.open(mode = "rb") as f:
        obj_data = zlib.decompress(f.read())
        header = obj_data[: obj_data.find(b"\x00")]
        fmt = header[:header.find(b" ")]
        content = obj_data[obj_data.find(b"\x00")+1 : ]
        return fmt.decode(), content


def read_tree(data: bytes) -> tp.List[tp.Tuple[int, str, str]]:
    # PUT YOUR CODE HERE
    ...


def cat_file(obj_name: str, pretty: bool = True) -> None:
    gitdir = repo_find(pathlib.Path("."))

    if len(resolve_object(obj_name, gitdir)):
        header, content = read_object(obj_name, gitdir)
        print(content.decode())


def find_tree_files(tree_sha: str, gitdir: pathlib.Path) -> tp.List[tp.Tuple[str, str]]:
    # PUT YOUR CODE HERE
    ...


def commit_parse(raw: bytes, start: int = 0, dct=None):
    # PUT YOUR CODE HERE
    ...
