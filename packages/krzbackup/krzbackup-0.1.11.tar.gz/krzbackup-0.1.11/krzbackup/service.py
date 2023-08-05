#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import print_function

import os
import time

import dbus
import psutil


class Service(object):
    """
    Dummy class to better contain methods
    """

    def __init__(self):
        self.log = self.log.getLogger('backup.service')

    def stop_service(self, service):
        SYSTEMD_BUSNAME = 'org.freedesktop.systemd1'
        SYSTEMD_PATH = '/org/freedesktop/systemd1'
        SYSTEMD_MANAGER_INTERFACE = 'org.freedesktop.systemd1.Manager'
        SYSTEMD_UNIT_INTERFACE = 'org.freedesktop.systemd1.Unit'

        bus = dbus.SystemBus()

        proxy = bus.get_object('org.freedesktop.PolicyKit1', '/org/freedesktop/PolicyKit1/Authority')
        authority = dbus.Interface(proxy, dbus_interface='org.freedesktop.PolicyKit1.Authority')
        system_bus_name = bus.get_unique_name()

        subject = ('system-bus-name', {'name': system_bus_name})
        action_id = 'org.freedesktop.systemd1.manage-units'
        details = {}
        flags = 1  # AllowUserInteraction flag
        cancellation_id = ''  # No cancellation id

        result = authority.CheckAuthorization(subject, action_id, details, flags, cancellation_id)

        if result[1] != 0:
            self.log.error("Need administrative privilege")

        systemd_object = bus.get_object(SYSTEMD_BUSNAME, SYSTEMD_PATH)
        systemd_manager = dbus.Interface(systemd_object, SYSTEMD_MANAGER_INTERFACE)

        unit = systemd_manager.GetUnit('{}'.format(service))
        unit_object = bus.get_object(SYSTEMD_BUSNAME, unit)
        systemd_manager.StopUnit('{}'.format(service), 'replace')

        while list(systemd_manager.ListJobs()):
            time.sleep(2)
            self.log.info('there are pending jobs, lets wait for them to finish.')

        prop_unit = dbus.Interface(unit_object, 'org.freedesktop.DBus.Properties')

        active_state = prop_unit.Get('org.freedesktop.systemd1.Unit', 'ActiveState')

        sub_state = prop_unit.Get('org.freedesktop.systemd1.Unit', 'SubState')

        self.log.debug(print(active_state, sub_state))

    def start_service(self, service):
        SYSTEMD_BUSNAME = 'org.freedesktop.systemd1'
        SYSTEMD_PATH = '/org/freedesktop/systemd1'
        SYSTEMD_MANAGER_INTERFACE = 'org.freedesktop.systemd1.Manager'
        SYSTEMD_UNIT_INTERFACE = 'org.freedesktop.systemd1.Unit'

        bus = dbus.SystemBus()

        proxy = bus.get_object('org.freedesktop.PolicyKit1', '/org/freedesktop/PolicyKit1/Authority')
        authority = dbus.Interface(proxy, dbus_interface='org.freedesktop.PolicyKit1.Authority')
        system_bus_name = bus.get_unique_name()

        subject = ('system-bus-name', {'name': system_bus_name})
        action_id = 'org.freedesktop.systemd1.manage-units'
        details = {}
        flags = 1  # AllowUserInteraction flag
        cancellation_id = ''  # No cancellation id

        result = authority.CheckAuthorization(subject, action_id, details, flags, cancellation_id)

        if result[1] != 0:
            self.log.error("Need administrative privilege")

        systemd_object = bus.get_object(SYSTEMD_BUSNAME, SYSTEMD_PATH)
        systemd_manager = dbus.Interface(systemd_object, SYSTEMD_MANAGER_INTERFACE)

        unit = systemd_manager.GetUnit(service)
        unit_object = bus.get_object(SYSTEMD_BUSNAME, unit)
        systemd_manager.StartUnit('{}'.format(service), 'replace')

        while list(systemd_manager.ListJobs()):
            time.sleep(2)
            self.log.info('there are pending jobs, lets wait for them to finish.')

        prop_unit = dbus.Interface(unit_object, 'org.freedesktop.DBus.Properties')

        active_state = prop_unit.Get('org.freedesktop.systemd1.Unit', 'ActiveState')

        sub_state = prop_unit.Get('org.freedesktop.systemd1.Unit', 'SubState')

        self.log.debug(print(active_state, sub_state))

    def restart_service(self, service):
        self.stop_service(service)
        time.sleep(2)
        processlist = self.find_procs_by_name(service)
        if not processlist:
            self.start_service(service)
        else:
            for pid in processlist:
                os.kill(pid, signal.SIGTERM)

            self.start_service(service)

    def find_procs_by_name(self, name):
        "Return a list of processes matching 'name'."
        assert name, name
        ls = []
        for p in psutil.process_iter():
            name_, exe, cmdline = "", "", []
            try:
                name_ = p.name()
                cmdline = p.cmdline()
                exe = p.exe()
            except (psutil.AccessDenied, psutil.ZombieProcess):
                pass
            except psutil.NoSuchProcess:
                continue
            try:
                if name in name_ or name in cmdline[0] or name in os.path.basename(exe):
                    ls.append(p.pids)
            except Exception as e:
                pass
        return ls
