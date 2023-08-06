#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu

from __future__ import (unicode_literals, absolute_import,
                        division, print_function)

import requests

from rapidpro_controller import (EMAIL_ALERTS_TO, SMS_ALERTS_TO, SEND_SMS_URL,
                                 SEND_EMAIL_ALERTS, SEND_SMS_ALERTS,
                                 run_command, get_proxies)


def alert_via_email(message):
    dest = ",".join(EMAIL_ALERTS_TO)
    command = 'echo "{msg}" | mail -s "rapidpro-alert" {dest}'.format(
        msg=message, dest=dest)
    success = run_command(command, shell=True) == 0
    return success, EMAIL_ALERTS_TO


def alert_via_sms(message):
    succeeded = []
    failed = []
    for number in SMS_ALERTS_TO:
        payload = {
            'from': '85855',
            'to': number,
            'text': message,
        }
        try:
            req = requests.post(SEND_SMS_URL,
                                data=payload,
                                proxies=get_proxies())
            assert req.status_code in (200, 201)
        except:
            failed.append(number)
        else:
            succeeded.append(number)

    return len(failed) == 0, succeeded, failed


def alert(message):
    email_success = None
    email_recipients = []

    if SEND_EMAIL_ALERTS:
        email_success, email_recipients = alert_via_email(message)

    if SEND_SMS_ALERTS:
        sms_success, sms_sent, sms_failed = alert_via_sms(message)

    success = email_success and sms_success
    return (success, email_success, email_recipients,
            sms_success, sms_sent, sms_failed)
