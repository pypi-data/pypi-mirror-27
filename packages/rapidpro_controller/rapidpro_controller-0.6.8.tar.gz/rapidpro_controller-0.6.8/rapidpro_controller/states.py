#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu

from __future__ import (unicode_literals, absolute_import,
                        division, print_function)
import os

from rapidpro_controller import (ROLES, STATUSES,
                                 ROLE_PATH, STATUS_PATH,
                                 WORKING, FAILURE,
                                 TRANSIANT,
                                 LSUCCESS, LINFO, LWARNING, LDANGER,
                                 get_remote_output, OTHER_SERVER,
                                 get_logger)

logger = get_logger(os.path.basename(__file__))


def get_local_role():
    with open(ROLE_PATH, 'r') as fp:
        return fp.read().strip()


def get_local_status():
    with open(STATUS_PATH, 'r') as fp:
        return fp.read().strip()


def get_remote_role():
    role = get_remote_output('cat {}'.format(ROLE_PATH), OTHER_SERVER)
    if role is None:
        return role
    return role.strip()


def get_remote_status():
    role = get_remote_output('cat {}'.format(STATUS_PATH), OTHER_SERVER)
    if role is None:
        return role
    return role.strip()


def get_role(role):
    if role not in ROLES:
        return "UNKNOWN ({})".format(role), LDANGER
    return role, LINFO


def get_status(status):
    if status not in STATUSES:
        return "UNKNOWN ({})".format(status), LDANGER
    level = LINFO
    if status == WORKING:
        level = LSUCCESS
    if status == FAILURE:
        level = LDANGER
    if status == TRANSIANT:
        level = LWARNING
    return status, level


def local_role():
    return get_role(get_local_role())


def remote_role():
    return get_role(get_remote_role())


def local_status():
    return get_status(get_local_status())


def remote_status():
    return get_status(get_remote_status())


def set_role(role):
    if role not in ROLES:
        logger.error("supplied role not allowed: `{}`".format(role))
        return 1

    with open(ROLE_PATH, 'w') as fp:
        fp.write(role)

    return 0


def set_status(status):
    if status not in STATUSES:
        logger.error("supplied status not allowed: `{}`".format(status))
        return 1

    with open(STATUS_PATH, 'w') as fp:
        fp.write(status)

    return 0
