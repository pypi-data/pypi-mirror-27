#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu

from __future__ import (unicode_literals, absolute_import,
                        division, print_function)

from rapidpro_controller import COMPONENTS, SERVICE_COMMAND, run_command


def start_service(service):
    ''' returns boolean for success '''
    args = [SERVICE_COMMAND, 'start', service]
    return run_command(args) == 0


def stop_service(service):
    ''' returns boolean for success '''
    args = [SERVICE_COMMAND, 'stop', service]
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
