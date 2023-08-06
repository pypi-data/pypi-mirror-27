#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu

from __future__ import (unicode_literals, absolute_import,
                        division, print_function)
import os

from rapidpro_controller import (MASTER, get_logger,
                                 FAILURE, TRANSIANT, DISABLED, WORKING)
from rapidpro_controller.states import (get_local_role, get_local_status)


logger = get_logger(os.path.basename(__file__))


MASTER_TO_SLAVE = [
    ['rapidpro-set-status', 'transiant'],
    ['rapidpro-stop'],
    ['rapidpro-disable'],
    ['rapidpro-configure-slave'],
    ['rapidpro-set-role', 'slave'],
    ['rapidpro-start'],
    ['rapidpro-enable'],
    ['rapidpro-set-status', 'working'],
]

SLAVE_TO_MASTER = [
    ['rapidpro-set-status', 'transiant'],
    ['rapidpro-stop'],
    ['rapidpro-disable'],
    ['rapidpro-configure-master'],
    ['rapidpro-set-role', 'master'],
    ['rapidpro-start'],
    ['rapidpro-enable'],
    ['rapidpro-set-status', 'working'],
]


def change_role(new_role):
    role = get_local_role()
    if role == new_role:
        return False, []

    return True, SLAVE_TO_MASTER if new_role == MASTER else MASTER_TO_SLAVE


def change_status(new_status):
    role = get_local_role()
    status = get_local_status()

    if status == new_status:
        logger.error("already at `{}` status".format(new_status))
        return False, []

    if new_status == TRANSIANT:
        logger.error("`{}` is not a status to target but a ~transiant~ state "
                     "used when changing to an actual status.\n"
                     "check `rapidpro-set-status` if that's what you want."
                     .format(TRANSIANT))
        return False, []

    if new_status == FAILURE:
        return True, [
            ['rapidpro-record-failure'],
        ]

    if new_status == DISABLED:
        return True, [
            ['rapidpro-set-status', TRANSIANT],
            ['rapidpro-stop'],
            ['rapidpro-disable'],
            ['rapidpro-set-status', DISABLED],
        ]

    if new_status == WORKING:

        if status == FAILURE:
            logger.error("you are marked in failure. "
                         "please change to disabled first.")
            return False, []

        return True, [
            ['rapidpro-set-status', TRANSIANT],
            ['rapidpro-stop'],
            ['rapidpro-configure-{}'.format(role)],
            ['rapidpro-start'],
            ['rapidpro-enable'],
            ['rapidpro-set-status', WORKING],
        ]

    return False, []
