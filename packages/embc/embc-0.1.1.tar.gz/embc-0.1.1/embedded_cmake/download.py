import tarfile
import zipfile
import gitutils
import requests
import tempfile
try:
    from urlparse import urlparse
except ImportError:
    from urllib.parse import urlparse
from os.path import splitext, basename, dirname, join, exists
from os import makedirs


def download_name(url):
    disassembled = urlparse(url)
    filename = basename(disassembled.path)
    if filename == "":
        filename = basename(dirname(disassembled.path))
    if filename == "":
        filename = disassembled.netloc

    barename, file_ext = splitext(filename)
    if file_ext == ".git":
        return barename
    else:
        return filename


def download(url, dest=None, unpack=True, root=None):
    if dest is None:
        dest = download_name(url)
    if root is not None:
        dest = join(root, dest)

    if url.startswith("git://") or url.endswith(".git"):
        return download_git(url, dest), "git"
    else:
        return download_http(url, dest, unpack)


def download_http(url, dest, unpack=True):
    r = requests.get(url)
    if r.status_code == requests.codes.ok:
        if unpack and r.headers['content-type'] in ("application/x-gzip", "application/x-gtar", "application/x-tgz", "application/tar", "application/tar+gzip", "application/tar+bzip2"):
            return unpack_tar_response(r, dest), "tgz"
        elif unpack and r.headers['content-type'] in ("application/zip",):
            return unpack_zip_response(r, dest), "zip"
        else:
            return unpack_file_response(r, dest), "raw"


def download_git(url, dest):
    if not exists(dest):
        gitutils.clone(url, dest)
    return dest


def unpack_tar_response(r, dest):
    with tempfile.TemporaryFile() as tarfd:
        tarfd.write(r.content)
        tarfd.seek(0)

        makedirs(dest)
        with tarfile.open(fileobj = tarfd) as tar:
            for member in tar:
                if member.name.startswith("..") or member.name.startswith("/"):
                    continue
                tar.extract(member, dest)
    return dest


def unpack_zip_response(r, dest):
    with tempfile.TemporaryFile() as tmpfd:
        tmpfd.write(r.content)
        tmpfd.seek(0)

        makedirs(dest)
        with zipfile.ZipFile(tmpfd, "r") as zipfd:
            zipfd.extractall(dest)
    return dest


def unpack_file_response(r, dest):
    makedirs(dirname(dest))
    with open(dest, "wb") as filefd:
        filefd.write(r.content)
    return dest
