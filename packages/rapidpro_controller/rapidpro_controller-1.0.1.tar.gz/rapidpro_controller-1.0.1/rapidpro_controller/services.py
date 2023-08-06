#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu

from __future__ import (unicode_literals, absolute_import,
                        division, print_function)
import os

from path import Path

from rapidpro_controller import (COMPONENTS, SERVICE_COMMAND, run_command,
                                 MONIT_COMMAND,
                                 MONIT_FILES,
                                 MONIT_ENABLED_CONF_DIR,
                                 MONIT_AVAILABLE_CONF_DIR,
                                 SLAVE)
from rapidpro_controller.states import get_local_role


def start_service(service):
    ''' returns boolean for success '''
    args = [SERVICE_COMMAND, 'start', service]
    return run_command(args) == 0


def stop_service(service):
    ''' returns boolean for success '''
    args = [SERVICE_COMMAND, 'stop', service]
    return run_command(args) == 0


def restart_service(service):
    ''' returns boolean for success '''
    args = [SERVICE_COMMAND, 'restart', service]
    return run_command(args) == 0


def enable_service(service):
    ''' returns boolean for success '''
    args = [SERVICE_COMMAND, 'enable', service]
    return run_command(args) == 0


def disable_service(service):
    ''' returns boolean for success '''
    args = [SERVICE_COMMAND, 'disable', service]
    return run_command(args) == 0


def stop_all_services():
    failed_to_stop = []
    for component in COMPONENTS:
        if not stop_service(component):
            failed_to_stop.append(component)

    return len(failed_to_stop) == 0, failed_to_stop


def restart_all_services():
    failed_to_restart = []
    for component in COMPONENTS:
        if not restart_service(component):
            failed_to_restart.append(component)

    return len(failed_to_restart) == 0, failed_to_restart


def start_all_services(cancel_on_failure=True, stop_all_on_failure=True):
    ''' start all services

        returns:
            all_started, failed_to_start, failed_to_stop '''
    started = []
    failed_to_start = []
    for component in COMPONENTS:
        if not start_service(component):
            failed_to_start.append(component)
            if cancel_on_failure:
                break
        else:
            started.append(component)

    failed_to_stop = []
    if stop_all_on_failure and failed_to_start:
        for component in started:
            if not stop_service(component):
                failed_to_stop.append(component)

    return len(started) == len(COMPONENTS), failed_to_start, failed_to_stop


def show_service_status(service):
    run_command([SERVICE_COMMAND, 'status', service])


def enable_all_services():
    failed_to_enable = []
    for component in COMPONENTS:
        if not enable_service(component):
            failed_to_enable.append(component)

    return len(failed_to_enable) == 0, failed_to_enable


def disable_all_services():
    failed_to_disable = []
    for component in COMPONENTS:
        if not disable_service(component):
            failed_to_disable.append(component)

    return len(failed_to_disable) == 0, failed_to_disable


def reconfigure_monit(enable, auto_reload=True):
    is_slave = get_local_role() == SLAVE

    for fname in MONIT_FILES:
        src = Path(os.path.join(MONIT_AVAILABLE_CONF_DIR, fname))
        src_slave = Path(os.path.join(MONIT_AVAILABLE_CONF_DIR,
                                      "{fn}.slave".format(fn=fname)))
        if is_slave and src_slave.exists():
            src = src_slave
        dst = Path(os.path.join(MONIT_ENABLED_CONF_DIR, fname))

        # delete symlink
        dst.remove_p()

        if enable:
            # create symlink
            src.symlink(dst)

    if auto_reload:
        return reload_monit()
    return True


def reload_monit():
    return run_command([MONIT_COMMAND, 'reload']) == 0
