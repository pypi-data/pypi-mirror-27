#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu

from __future__ import (unicode_literals, absolute_import,
                        division, print_function)

import requests

from rapidpro_controller import (SEND_SMS_URL, get_proxies, SEND_SMS_FROM)


def send_sms_to(message, recipient):
    payload = {
        'from': SEND_SMS_FROM,
        'to': recipient,
        'text': message,
    }
    try:
        req = requests.post(SEND_SMS_URL,
                            params=payload,
                            proxies=get_proxies())
        return req.status_code == 200
    except:
        return False
