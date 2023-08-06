#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu

from __future__ import (unicode_literals, absolute_import,
                        division, print_function)
import os

from path import Path

from rapidpro_controller.configuration import (backup_conf, config_replace,
                                               restore_conf, release_backup)
from rapidpro_controller import (OTHER_SERVER,
                                 POSTGRES_CONFIG_PATH,
                                 POSTGRES_DATA_DIR,
                                 POSTGRES_MAIN_DATA_DIR,
                                 POSTGRES_ARCHIVE_DIR,
                                 POSTGRES_RECOVERYCONF_PATH,
                                 POSTGRES_TRIGGER_PATH,
                                 POSTGRES_USER, POSTGRES_GROUP,
                                 run_command)


def configure_postgres_slave():
    ''' postgres slave needs

        - to enable hot_standby and remove archiving
        - to backup `main` postgres folder
        - to download a fresh copy of the db
        - to setup recovery.conf file
    '''

    def switch_conf():
        role_conf = "# enable hot_standby for slave\n" \
                    "hot_standby = on\n"
        backup_path = backup_conf(POSTGRES_CONFIG_PATH)
        backup_restored = False
        try:
            config_replace(POSTGRES_CONFIG_PATH, 'postgres', role_conf)
            success = True
        except:
            success = False
            backup_restored = restore_conf(backup_path, POSTGRES_CONFIG_PATH)
        else:
            release_backup(backup_path)

        return success, backup_path, backup_restored

    def backup_main_folder():
        src = Path(POSTGRES_MAIN_DATA_DIR)
        dst = Path(os.path.join(POSTGRES_DATA_DIR, 'main_backup'))
        try:
            if dst.exists():
                dst.rmtree()
            src.move(dst)
            return True
        except:
            return False

    def retrieve_backup():
        p = Path(POSTGRES_MAIN_DATA_DIR)
        p.makedirs_p(0700)
        p.chmod(0700)
        p.chown(POSTGRES_USER, POSTGRES_GROUP)
        os.environ['PGPASSWORD'] = 'replicapass'
        success = run_command(['pg_basebackup',
                               '-h', OTHER_SERVER,
                               '-U', 'replica',
                               '-D', POSTGRES_MAIN_DATA_DIR,
                               '-P', '--xlog']) == 0
        del(os.environ['PGPASSWORD'])
        return success

    def create_recovery():
        content = "standby_mode = 'on'\n" \
                  "primary_conninfo = 'host={master} port=5432 " \
                  "user=replica password=replicapass'\n" \
                  "restore_command = 'cp {dir}/archive/%f %p'\n" \
                  "trigger_file = '{trigger_path}'\n" \
                  .format(master=OTHER_SERVER, dir=POSTGRES_MAIN_DATA_DIR,
                          trigger_path=POSTGRES_TRIGGER_PATH)
        with open(POSTGRES_RECOVERYCONF_PATH, 'w') as fp:
            fp.write(content)
        p = Path(POSTGRES_RECOVERYCONF_PATH)
        p.chmod(0600)
        p.chown(POSTGRES_USER, POSTGRES_GROUP)

    # rewrite main config file
    conf_switched, backup_path, backup_restored = switch_conf()

    # backup main directory
    try:
        assert conf_switched
        dir_backedup = backup_main_folder()
    except:
        dir_backedup = False

    try:
        assert dir_backedup
        backup_retrieved = retrieve_backup()
    except:
        backup_retrieved = False

    # create recovery config file
    try:
        assert backup_retrieved
        create_recovery()
        recovery_confed = True
    except:
        recovery_confed = False

    success = conf_switched and dir_backedup \
        and backup_retrieved and recovery_confed

    return success, conf_switched, dir_backedup, \
        backup_retrieved, recovery_confed


def configure_postgres_master():
    ''' postgres master needs

        - to enable archiving in conf and remove hot_standby
        - to create the archive folder
        - to remove recovery file if it exists
    '''

    def switch_conf():
        role_conf = "# enable archiving for master\n" \
                    "archive_mode = on\n" \
                    "archive_command = 'cp %p {dir}/archive/%f'\n" \
                    .format(dir=POSTGRES_MAIN_DATA_DIR)
        backup_path = backup_conf(POSTGRES_CONFIG_PATH)
        backup_restored = False
        try:
            config_replace(POSTGRES_CONFIG_PATH, 'postgres', role_conf)
            success = True
        except:
            success = False
            backup_restored = restore_conf(backup_path, POSTGRES_CONFIG_PATH)
        else:
            release_backup(backup_path)

        return success, backup_path, backup_restored

    def create_archive_folder():
        p = Path(POSTGRES_ARCHIVE_DIR)
        p.makedirs_p(0700)
        p.chmod(0700)
        p.chown(POSTGRES_USER, POSTGRES_GROUP)

    def remove_recovery():
        Path(POSTGRES_RECOVERYCONF_PATH).remove_p()

    # rewrite main config file
    conf_switched, backup_path, backup_restored = switch_conf()

    # backup main directory
    try:
        assert conf_switched
        create_archive_folder()
        dir_created = True
    except:
        dir_created = False

    try:
        assert dir_created
        remove_recovery()
        recovery_rmed = True
    except:
        recovery_rmed = False

    success = conf_switched and dir_created and recovery_rmed

    return success, conf_switched, dir_created, recovery_rmed
