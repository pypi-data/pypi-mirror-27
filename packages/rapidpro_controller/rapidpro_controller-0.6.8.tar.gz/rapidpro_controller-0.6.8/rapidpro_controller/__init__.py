#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu

from __future__ import (unicode_literals, absolute_import,
                        division, print_function)
import os
import sys
import json
import logging
import subprocess
from logging import handlers

from termcolor import colored
from path import Path

CONFIG_FILE = '/etc/rapidproctl.conf'
# CONFIG_FILE = './rapidproctl.conf'
try:
    with open(CONFIG_FILE, 'r') as fp:
        CONFIG = json.load(fp)
except:
    CONFIG = {}

# CONFIGURATION
LOG_FILE = CONFIG.get('LOG_FILE', '/var/log/rapidproctl/rapidproctl.log')
LOG_LEVEL = CONFIG.get('LOG_LEVEL', logging.INFO)
SSH_USER = CONFIG.get('SSH_USER', 'root')
SERVERA = CONFIG.get('SERVERA', 'sms1')
SERVERB = CONFIG.get('SERVERB', 'sms2')
ROLE_PATH = CONFIG.get('ROLE_PATH', '/etc/rapidpro.role')
STATUS_PATH = CONFIG.get('STATUS_PATH', '/etc/rapidpro.status')
CLUSTERIP_PATH = CONFIG.get('CLUSTERIP_PATH', '/etc/rapidpro.clusterip')
SERVICE_COMMAND = CONFIG.get('SERVICE_COMMAND', 'systemctl')
REDIS_CONFIG_PATH = CONFIG.get('REDIS_CONFIG_PATH', '/etc/redis/redis.conf')

POSTGRES_CONFIG_PATH = CONFIG.get('POSTGRES_CONFIG_PATH',
                                  '/var/lib/pgsql/data/postgresql.conf')
POSTGRES_HBACONF_PATH = CONFIG.get('POSTGRES_HBACONF_PATH',
                                   '/var/lib/pgsql/data/pg_hba.conf')
POSTGRES_DATA_DIR = CONFIG.get('POSTGRES_DATA_DIR',
                               '/var/lib/pgsql/data')
POSTGRES_DATABACKUP_DIR = CONFIG.get('POSTGRES_DATABACKUP_DIR',
                                     '/var/lib/pgsql/data_backup')

POSTGRES_TRIGGER_PATH = CONFIG.get('POSTGRES_TRIGGER_PATH',
                                   '/tmp/postgresql.trigger.5432')
POSTGRES_USER = CONFIG.get('POSTGRES_USER', 'postgres')
POSTGRES_GROUP = CONFIG.get('POSTGRES_GROUP', 'postgres')

WORKING_SLAVE_BACKUP_ON = CONFIG.get('WORKING_SLAVE_BACKUP_ON',
                                     'every-5-minutes')
SUPPORTED_MASTER_BACKUP_ON = CONFIG.get('SUPPORTED_MASTER_BACKUP_ON',
                                        ['0600', '2300'])
SINGLE_MASTER_BACKUP_ON = CONFIG.get('SINGLE_MASTER_BACKUP_ON',
                                     'every-30-minutes')
BACKUP_DIR = CONFIG.get('BACKUP_DIR', "/data/rapidpro-backups")
SUB_HOURLY_BACKUPS_TO_KEEP = CONFIG.get('SUB_HOURLY_BACKUPS_TO_KEEP', 10)
HOURLY_BACKUPS_TO_KEEP = CONFIG.get('HOURLY_BACKUPS_TO_KEEP', 10)
DAILY_BACKUPS_TO_KEEP = CONFIG.get('DAILY_BACKUPS_TO_KEEP', 10)
MONTHLY_BACKUPS_TO_KEEP = CONFIG.get('MONTHLY_BACKUPS_TO_KEEP', 3)
ENABLE_BACKUP = CONFIG.get('ENABLE_BACKUP', True)

SEND_EMAIL_ALERTS = CONFIG.get('SEND_EMAIL_ALERTS', True)
SEND_SMS_ALERTS = CONFIG.get('SEND_SMS_ALERTS', True)
EMAIL_ALERTS_TO = CONFIG.get('EMAIL_ALERTS_TO', [])
SMS_ALERTS_TO = CONFIG.get('SMS_ALERTS_TO', [])
ALERT_COMMAND = CONFIG.get('ALERT_COMMAND', "/usr/bin/rapidpro-alert")

SEND_SMS_URL = CONFIG.get('SEND_SMS_URL', "http://smsgateway:90/sendsmstt.php")
SEND_SMS_FROM = CONFIG.get('SEND_SMS_FROM', "85355")
HTTP_PROXY = CONFIG.get('HTTP_PROXY', None)
HTTPS_PROXY = CONFIG.get('HTTPS_PROXY', None)
CRM_IP_RESOURCE = CONFIG.get('CRM_IP_RESOURCE', 'admin_addr')

MONIT_AVAILABLE_CONF_DIR = CONFIG.get('MONIT_AVAILABLE_CONF_DIR',
                                      "/etc/monit/conf-available")
MONIT_ENABLED_CONF_DIR = CONFIG.get('MONIT_ENABLED_CONF_DIR',
                                    "/etc/monit/conf-enabled")
MONIT_FILES = CONFIG.get('MONIT_FILES',
                         ["nginx", "postgressql", "redis-server",
                          "rapidpro", "celery"])
MONIT_COMMAND = CONFIG.get('MONIT_COMMAND', "/usr/bin/monit")
BIN_PREFIX = CONFIG.get('BIN_PREFIX', "/usr/bin")
# END

POSTGRES_ARCHIVE_DIR = os.path.join(POSTGRES_DATA_DIR, 'archive')
POSTGRES_RECOVERYCONF_PATH = os.path.join(POSTGRES_DATA_DIR,
                                          'recovery.conf')

SERVERS = [SERVERA, SERVERB]

MASTER = 'master'
SLAVE = 'slave'
ROLES = [MASTER, SLAVE]

ONLINE = 'online'
STANDBY = 'standby'  # opposite of ONLINE
READY = 'ready'
MAINTENANCE = 'maintenance'  # opposite of READY
CLUSTER_MODES = [ONLINE, STANDBY, READY, MAINTENANCE]

WORKING = 'working'
FAILURE = 'failure'
DISABLED = 'disabled'
TRANSIANT = 'transiant'
STATUSES = [WORKING, FAILURE, DISABLED, TRANSIANT]

LSUCCESS = 'success'
LINFO = 'info'
LWARNING = 'warning'
LDANGER = 'danger'
LNOTICE = 'notice'
COLORS = {
    LSUCCESS: 'green',
    LWARNING: 'yellow',
    LDANGER: 'red',
    LNOTICE: 'blue',

    WORKING: 'green',
    FAILURE: 'red',
    DISABLED: 'red',
    TRANSIANT: 'red',

    MAINTENANCE: 'red',
    READY: 'green',
}

COMPONENTS = ['postgresql', 'redis-server',
              'nginx', 'rapidpro',
              'celerybeat', 'celery']


def is_root():
    return os.geteuid() == 0


def get_logger(name):
    logger = logging.getLogger(name)
    logger.setLevel(LOG_LEVEL)
    sh_format = logging.Formatter("%(message)s")
    lsh = logging.StreamHandler(sys.stdout)
    lsh.setFormatter(sh_format)
    logger.addHandler(lsh)
    lfh = handlers.RotatingFileHandler(LOG_FILE,
                                       maxBytes=(1048576 * 5),
                                       backupCount=7)
    fh_format = logging.Formatter(
        "%(asctime)s [%(name)s:%(levelname)s] %(message)s")
    lfh.setFormatter(fh_format)
    logger.addHandler(lfh)
    return logger


def get_color(status):
    return COLORS.get(status)


def log_success(logger, text='success', msg=None):
    message = "... {}".format(colored(text, get_color(LSUCCESS)))
    if msg is not None:
        message += ". {}".format(msg)
    logger.info(message)


def log_failure(logger, text='failure', msg=None):
    message = "... {}".format(colored(text, get_color(LDANGER)))
    if msg is not None:
        message += ". {}".format(msg)
    logger.info(message)


def get_proxies():
    return {
        'http': HTTP_PROXY,
        'https': HTTPS_PROXY,
    }


Path(os.path.dirname(LOG_FILE)).makedirs_p()
logger = get_logger(__file__)


def run_command(command, shell=False, auto_prefix=True):
    args = [command] if isinstance(command, basestring) else command
    if auto_prefix and not args[0].startswith("/"):
        args[0] = os.path.join(BIN_PREFIX, args[0])
    try:
        return subprocess.call(args, shell=shell)
    except Exception as exp:
        logger.debug(exp)
        return 1


def get_output(command, shell=True):
    args = [command] if isinstance(command, basestring) else command
    try:
        return subprocess.check_output(args, shell=shell)
    except Exception as exp:
        logger.debug(exp)
        return None


def get_remote_output(command, peer, shell=True):
    args = [command] if isinstance(command, basestring) else command
    ssh_cmd = ["ssh", "{u}@{s}".format(u=SSH_USER, s=peer),
               '"{}"'.format(" ".join(args))]
    try:
        return subprocess.check_output(" ".join(ssh_cmd), shell=shell)
    except Exception as exp:
        logger.debug(exp)
        return None


def whoami():
    return get_output('/bin/hostname').strip()


def get_other_server(check_self=False):
    global THIS_SERVER
    if check_self:
        THIS_SERVER = whoami()
    return SERVERB if whoami() == SERVERA else SERVERA


THIS_SERVER = whoami()
OTHER_SERVER = get_other_server()
if THIS_SERVER not in SERVERS or OTHER_SERVER not in SERVERS:
    logger.critical("{warning} Unable to guess which server this is. "
                    "Please check hostname."
                    .format(warning=colored("!! WARNING !!",
                                            get_color(LDANGER))))
    logger.critical("hostname: `{host}`. servers: `{servers}`"
                    .format(host=THIS_SERVER, servers=SERVERS))
    sys.exit(1)
