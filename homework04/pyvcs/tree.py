import os
import pathlib
import stat
import time
import typing as tp

from pyvcs.index import GitIndexEntry, read_index
from pyvcs.objects import hash_object
from pyvcs.refs import get_ref, is_detached, resolve_head, update_ref


def write_tree(gitdir: pathlib.Path, index: tp.List[GitIndexEntry], dirname: str = "") -> str:
    records = b""
    for el in index:
        if "/" in el.name:
            records += b"40000 "
            subdir_files = b""
            dir_name = el.name[: el.name.find("/")]
            records += dir_name.encode() + b"\0"
            subdir_files += oct(el.mode)[2:].encode() + b" "
            subdir_files += el.name[el.name.find("/") + 1:].encode() + b"\0"
            subdir_files += el.sha1
            blob_hash = hash_object(subdir_files, fmt="tree", write=True)
            records += bytes.fromhex(blob_hash)
        else:
            records += oct(el.mode)[2:].encode() + b" "
            records += el.name.encode() + b"\0"
            records += el.sha1
    tree_name = hash_object(records, fmt="tree", write=True)
    return tree_name


def commit_tree(
        gitdir: pathlib.Path,
        tree: str,
        message: str,
        parent: tp.Optional[str] = None,
        author: tp.Optional[str] = None,
) -> str:
    if "GIT_DIR" not in os.environ:
        os.environ["GIT_DIR"] = ".git"
    if author is None:
        author = f"{os.environ['GIT_AUTHOR_NAME']} <{os.environ['GIT_AUTHOR_EMAIL']}>"
    timestamp = int(time.mktime(time.localtime()))
    utc_offset = -time.timezone
    author_time = "{} {}{:02}{:02}".format(
        timestamp,
        "+" if utc_offset > 0 else "-",
        abs(utc_offset) // 3600,
        (abs(utc_offset) // 60) % 60,
    )
    content = f"tree {tree}\n"
    if parent:
        content += f"parent {parent}\n"
    content += f"author {author} {author_time}\ncommitter {author} {author_time}\n\n{message}\n"
    sha = hash_object(content.encode("ascii"), "commit", True)
    return sha
