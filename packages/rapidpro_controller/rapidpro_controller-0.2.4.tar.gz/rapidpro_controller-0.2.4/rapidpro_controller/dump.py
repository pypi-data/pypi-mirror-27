#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu

from __future__ import (unicode_literals, absolute_import,
                        division, print_function)
import os
import datetime

from path import Path

from rapidpro_controller import (get_logger, SLAVE, WORKING,
                                 WORKING_SLAVE_BACKUP_ON,
                                 SINGLE_MASTER_BACKUP_ON,
                                 SUPPORTED_MASTER_BACKUP_ON,
                                 BACKUP_DIR,
                                 run_command,
                                 MONTHLY_BACKUPS_TO_KEEP,
                                 DAILY_BACKUPS_TO_KEEP,
                                 HOURLY_BACKUPS_TO_KEEP,
                                 SUB_HOURLY_BACKUPS_TO_KEEP)
from rapidpro_controller.states import (get_local_role, get_local_status,
                                        get_remote_status)

logger = get_logger(os.path.basename(__file__))

# ensure backup dir exists
Path(BACKUP_DIR).makedirs_p()


def get_timecodes(shortcut):
    if shortcut == 'every-5-minutes':
        return [str(h).zfill(2) + str(m).zfill(2)
                for h in range(0, 24)
                for m in range(0, 60, 5)]
    elif shortcut == 'every-30-minutes':
        return [str(h).zfill(2) + str(m).zfill(2)
                for h in range(0, 24)
                for m in range(0, 60, 30)]
    return []


def timecode_for(adate):
    return adate.strftime('%Y%m%d'), adate.strftime('%H%M')


def get_closest_code(codes, code):
    if code not in codes:
        codes.append(code)
        codes.sort()
        nindex = codes.index(code)
        index = nindex - 1 if nindex > 0 else 0
        return codes[index]

    return code


def get_backup_name(kind, day, code):
    return "rapidpro-{day}_{code}.sql".format(
        kind=kind, day=day, code=code)


def date_from_name(fname):
    name = fname.split('.')[0]
    _, date_part = name.split('rapidpro_', 1)
    day, code = date_part.split('_')
    return day, code, datetime.datetime(year=int(day[0:4]),
                                        month=int(day[4:6]),
                                        day=int(day[6:8]),
                                        hour=int(code[0:2]),
                                        minute=int(code[2:4]))


def cleanup_backups():
    backup_files = [fn for fn in os.listdir(BACKUP_DIR) if fn.endswith('.sql')]

    # sort by date (latest first)
    backup_files.sort(reverse=True)

    subhourly = []
    hourly = []
    daily = []
    monthly = []

    for fname in backup_files:
        fday, fcode, fdate = date_from_name(fname)
        entry = (fname, fday, fcode, fdate)

        # 0000 codes are used for montly and daily
        if fcode == '0000':
            # only first of month for monthly
            if fdate.day == 0:
                monthly.append(entry)

            # all days are OK for daily
            daily.append(entry)

        # xx00 codes are used for hourly
        if fcode.endswith('00'):
            hourly.append(entry)

        # any are OK for subhourly
        subhourly.append(entry)

    monthly = monthly[:MONTHLY_BACKUPS_TO_KEEP]
    daily = daily[:DAILY_BACKUPS_TO_KEEP]
    hourly = hourly[:HOURLY_BACKUPS_TO_KEEP]
    subhourly = subhourly[:SUB_HOURLY_BACKUPS_TO_KEEP]

    to_keep = monthly + daily + hourly + subhourly
    to_keep_fnames = [e[0] for e in to_keep]

    to_remove = [fname for fname in backup_files
                 if fname not in to_keep_fnames]

    success = True
    for fname in to_remove:
        fpath = os.path.join(BACKUP_DIR, fname)
        try:
            os.remove(fpath)
        except:
            success = False

    return success, to_remove, to_keep_fnames


def backup_supported_master(on):
    # accept supported master backup request from time to time
    codes = get_timecodes(SUPPORTED_MASTER_BACKUP_ON)
    day, code = timecode_for(on)
    target = get_closest_code(codes, code)
    target_fname = get_backup_name('single-master', day, target)
    target_fpath = os.path.join(BACKUP_DIR, target_fname)

    return backup_to(target_fpath)


def backup_single_master(on):
    # frequently accept single master request
    # but don't stress master server too much
    codes = get_timecodes(SINGLE_MASTER_BACKUP_ON)
    day, code = timecode_for(on)
    target = get_closest_code(codes, code)
    target_fname = get_backup_name('single-master', day, target)
    target_fpath = os.path.join(BACKUP_DIR, target_fname)

    return backup_to(target_fpath)


def backup_working_slave(on):
    # always accept a working slave backup request
    codes = get_timecodes(WORKING_SLAVE_BACKUP_ON)
    day, code = timecode_for(on)
    target = get_closest_code(codes, code)
    target_fname = get_backup_name('working-slave', day, target)
    target_fpath = os.path.join(BACKUP_DIR, target_fname)

    return backup_to(target_fpath)


def database_cold_backup():

    now = datetime.datetime.now()
    # are we a working slave?
    is_slave = get_local_role() == SLAVE
    is_working = get_local_status() == WORKING
    is_working_slave = is_slave and is_working
    peer_is_working = get_remote_status() == WORKING

    if not is_working:
        # don't backup non-working server
        return False

    if is_working_slave and peer_is_working:
        # backup on working slave with working master
        return backup_working_slave(now)

    is_master = not is_slave
    is_working_master = is_master and is_working
    is_single_master = is_working_master and not peer_is_working
    is_supported_master = is_working_master and peer_is_working

    if is_single_master:
        return backup_single_master(now)

    if is_supported_master:
        return backup_supported_master(now)


def backup_to(path, force=False):
    if os.path.exists(path) and not force:
        return False

    return run_command(['rapidpro-pgdump-to', path])
