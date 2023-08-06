#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu

from __future__ import (unicode_literals, absolute_import,
                        division, print_function)

from rapidpro_controller.configuration import (backup_conf, config_replace,
                                               restore_conf, release_backup)
from rapidpro_controller import (OTHER_SERVER,
                                 REDIS_CONFIG_PATH)


def configure_redis_slave():
    ''' redis slave has a slaveof statement referencing master '''

    role_conf = "slaveof {other} 6379".format(other=OTHER_SERVER)
    backup_path = backup_conf(REDIS_CONFIG_PATH)
    backup_restored = False
    try:
        config_replace(REDIS_CONFIG_PATH, 'redis', role_conf)
        success = True
    except:
        success = False
        backup_restored = restore_conf(backup_path, REDIS_CONFIG_PATH)
    else:
        release_backup(backup_path)

    return success, backup_path, backup_restored


def configure_redis_master():
    ''' redis master has no particular configuration '''

    role_conf = ""
    backup_path = backup_conf(REDIS_CONFIG_PATH)
    backup_restored = False
    try:
        config_replace(REDIS_CONFIG_PATH, 'redis', role_conf)
        success = True
    except:
        success = False
        backup_restored = restore_conf(backup_path, REDIS_CONFIG_PATH)
    else:
        release_backup(backup_path)

    return success, backup_path, backup_restored
