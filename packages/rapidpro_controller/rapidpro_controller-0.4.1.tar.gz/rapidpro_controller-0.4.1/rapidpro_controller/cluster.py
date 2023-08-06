#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu

from __future__ import (unicode_literals, absolute_import,
                        division, print_function)
import json
import datetime

from rapidpro_controller import (get_output,
                                 THIS_SERVER, SERVERS, CLUSTER_MODES,
                                 ONLINE, STANDBY, READY, MAINTENANCE,
                                 run_command, CRM_IP_RESOURCE, CLUSTERIP_PATH)
from rapidpro_controller.xml2json import xml2json


class Xml2JsonOption:
    pretty = True


def get_crm_status(as_xml=True):
    return get_output(['crm_mon', '--as-xml', '-1'], False)


def xml_to_json(xml_string):
    return xml2json(xml_string, Xml2JsonOption, True, True)


def get_crm_json():
    status = get_crm_status()
    if status is None:
        return None
    return json.loads(xml_to_json(status))


def run_crm_status(quiet=True):
    command = ['crm', 'status']
    if quiet:
        command.append('-Q')
    return run_command(command, False)


def set_cluster_mode(mode, peer):
    if mode not in CLUSTER_MODES:
        return False
    return run_command(['crm', 'node', mode, peer], False) == 0


def get_ip_master():
    output = get_output(['crm', '-D', 'plain',
                         'resource', 'status', CRM_IP_RESOURCE], False)
    if output is None:
        return None
    return output.rsplit(":", 1)[-1].strip()


def get_cached_ip_master():
    try:
        with open(CLUSTERIP_PATH, 'r') as fp:
            cached_ip = json.load(fp)
    except:
        return None, None
    return cached_ip['peer'], cached_ip['on']


def cache_ip_master(peer, on=None):
    if on is None:
        on = datetime.datetime.now()
    data = {'peer': peer, on: on.isoformat()}
    try:
        with open(CLUSTERIP_PATH, 'w') as fp:
            json.dump(data, fp)
        return 0
    except:
        return 1


def is_ip_master():
    return get_ip_master() == THIS_SERVER


def was_ip_master():
    return get_cached_ip_master() == THIS_SERVER


def is_cluster_dc():
    crm = get_crm_json()
    summary = crm['crm_mon']['summary']
    is_master = summary['current_dc']['@name'] == THIS_SERVER

    return is_master


def crm_to_nodes(crm):
    if crm is None:
        return None
    try:
        nodes = {}
        for node in crm['crm_mon']['nodes']['node']:
            name = node['@name'].strip()
            if name in SERVERS:
                nodes[name] = node
        return nodes
    except:
        return None


def xbool(string):
    return string.lower() == "true"


def get_node_state(peer):
    crm = get_crm_json()
    nodes = crm_to_nodes(crm)
    if nodes is None:
        return None
    node = nodes.get(peer)
    if node is None:
        return None

    return {
        "shutdown": xbool(node['@shutdown']),
        "id": node['@id'],
        "standby": xbool(node['@standby']),
        "online": xbool(node['@online']),
        "expected_up": xbool(node['@expected_up']),
        "is_dc": xbool(node['@is_dc']),
        "maintenance": xbool(node['@maintenance']),
        "standby_onfail": xbool(node['@standby_onfail']),
        "pending": xbool(node['@pending']),
        "unclean": xbool(node['@unclean']),
    }


def put_online(peer):
    return set_cluster_mode(ONLINE, peer)


def put_standby(peer):
    return set_cluster_mode(STANDBY, peer)


def set_ready(peer):
    return set_cluster_mode(READY, peer)


def set_maintenance(peer):
    return set_cluster_mode(MAINTENANCE, peer)


def is_online(peer):
    ''' node is either online or standby '''
    try:
        return (get_node_state(peer)['online'] and
                not get_node_state(peer)['standby'])
    except:
        return False


def is_ready(peer):
    ''' node is either ready or maintenance '''
    try:
        return not get_node_state(peer)['maintenance']
    except:
        return False


def is_available(peer):
    return is_online(peer) and is_ready(peer)


def make_available(peer, force=False):
    success = True
    if not is_ready(peer) or force:
        if not set_ready(peer):
            success = False

    if not is_online(peer) or force:
        if not put_online(peer):
            success = False
    return success


def make_unavailable(peer, force=False):
    if is_online(peer) or force:
        return put_standby(peer)
    return True
