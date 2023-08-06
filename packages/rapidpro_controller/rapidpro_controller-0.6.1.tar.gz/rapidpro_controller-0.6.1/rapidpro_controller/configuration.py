#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu

from __future__ import (unicode_literals, absolute_import,
                        division, print_function)
import os
import shutil
import tempfile


def replace_between(content, start, stop, replacement, sep=""):
    before, rest = content.split(start)
    inside, after = rest.split(stop)
    return sep.join([before, start, replacement, stop, after])


def prefixed_replace(content, prefix, replacement):
    start = "### rapidpro-{}-start ###".format(prefix)
    stop = "### rapidpro-{}-stop ###".format(prefix)
    return replace_between(content, start, stop, replacement, "\n")


def config_replace(fpath, prefix, replacement):
    with open(fpath, 'r') as fp:
        content = fp.read()
    new_content = prefixed_replace(content, prefix, replacement)
    with open(fpath, 'w') as fp:
        fp.write(new_content)


def backup_conf(fpath):
    try:
        basename = os.path.basename(fpath)
        dest = tempfile.NamedTemporaryFile(prefix=basename+"-", delete=False)
        shutil.copyfile(fpath, dest.name)
        return dest.name
    except:
        return None


def restore_conf(backup_path, source_path):
    try:
        shutil.copyfile(backup_path, source_path)
        return True
    except:
        return False


def release_backup(backup_path):
    try:
        os.remove(backup_path)
        return True
    except:
        return False
