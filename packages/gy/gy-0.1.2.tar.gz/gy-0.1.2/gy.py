# coding: utf8

"""
    gy generates .gitignore files from the command line for you.
"""

import os
import shutil
import zipfile

import click
import requests

IGNORE_ZIP_URL = 'https://codeload.github.com/github/gitignore/zip/master'
IGNORE_ZIP_NAME = 'ignore-master.zip'
HERE = os.path.abspath(os.path.dirname(__file__))
ARCHIVE_DIR = 'archive'
SUFFIX = '.gitignore'


def _unzip(archive, target):
    """
    :param archive:
    :param target:
    :return:
    """
    with zipfile.ZipFile(archive, 'r') as z:
        z.extractall(target)


def _download_zip(url):
    """
    :param url:
    :return:
    """
    r = requests.get(url)
    if r.status_code == 200:
        parent = os.path.join(HERE, ARCHIVE_DIR)
        if not os.path.exists(parent):
            os.mkdir(parent)
        path = os.path.join(parent, IGNORE_ZIP_NAME)
        with open(path, 'w') as f:
            f.write(r.content)
        _unzip(path, parent)
        os.remove(path)


def _remove_files(target):
    """
    :param target:
    :return:
    """
    path = os.path.join(HERE, target)
    if os.path.exists(path):
        shutil.rmtree(path)


def wrap_files():
    """
    :return:
    """
    gd = dict()
    path = os.path.join(HERE, ARCHIVE_DIR)
    for root, _, files in os.walk(path):
        for f in files:
            if f.endswith(SUFFIX):
                gd[f.replace(SUFFIX, '', 1).lower()] = os.path.join(root, f)

    return gd


def ls_ignores():
    """
    :return:
    """
    return [k for k in wrap_files()]


def gr_ignores(names):
    """
    :param names:
    :return:
    """
    names.strip()
    ignores_map = wrap_files()
    unknown_list = list()
    output_list = list()
    for l in names.split(','):
        if l.lower() not in ignores_map:
            unknown_list.append(l)
        else:
            with open(ignores_map[l.lower()], 'r') as f:
                output_list.append(f.read())

    if unknown_list:
        print('unsupported files: {0}'.format(', '.join(unknown_list)))
        print('run `gy ls` to see all supported languages.')
    print('\n'.join(output_list))


@click.group()
def cli():
    """Yet another .gitignore magician in your command line."""
    pass


@cli.command()
def update():
    """update .gitignore zip"""
    _remove_files(ARCHIVE_DIR)
    _download_zip(IGNORE_ZIP_URL)


@cli.command()
def ls():
    """list all supported languages"""
    ignores_list = ls_ignores()
    print('{0} supported .gitignore files:'.format(len(ignores_list)))
    ignores_list.sort()
    print(', '.join(ignores_list))


@cli.command()
@click.argument('languages', required=False)
def generate(languages):
    """generate .gitignore file"""
    languages = languages or 'python'
    gr_ignores(languages)


def main():
    """
    :return:
    """
    cli()


if __name__ == '__main__':
    main()
