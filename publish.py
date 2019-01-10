#!/usr/bin/env python

from contextlib import contextmanager
from os import chdir, getcwd
from os.path import join
from shutil import copytree, rmtree
from subprocess import check_call as run
from tempfile import mkdtemp
import subprocess


REPO = subprocess.run('git ls-remote --get-url'.split(), stdout=subprocess.PIPE).stdout.decode().strip()

@contextmanager
def tmpdir():
    try:
        path = mkdtemp()
        yield path
    finally:
        rmtree(path)


@contextmanager
def cwd(path):
    old_path = getcwd()
    try:
        chdir(path)
        yield
    finally:
        chdir(old_path)


def publish():
    with tmpdir() as root:
        path = join(root, 'dist')
        copytree('dist', path)

        with cwd(path):
            run(['touch', '.nojekyll'])
            run(['git', 'init'])
            run(['git', 'add', '.'])
            run(['git', 'commit', '-m', 'up'])
            run(['git', 'push', '--force', REPO, 'master:gh-pages'])


if __name__ == '__main__':
    publish()
