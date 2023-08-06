#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu

from __future__ import (unicode_literals, absolute_import,
                        division, print_function)

import requests

from rapidpro_controller import (SEND_SMS_URL, get_proxies)


def send_sms_to(message, recipient):
    payload = {
        'from': '85855',
        'to': recipient,
        'text': message,
    }
    try:
        req = requests.post(SEND_SMS_URL,
                            data=payload,
                            proxies=get_proxies())
        return req.status_code in (200, 201)
    except:
        return False
