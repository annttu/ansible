# encoding: utf-8

"""
This plugin allows to fetch username and sudo password from OS X keychain

Add this plugin to ./vars_plugins/keychain_sudo.py and append ./vars_plugins to vars_plugins variable in defaults context on ansible.conf

[defaults]
vars_plugins = ./vars_plugins

And configure usage for hosts on hosts file.

[all:vars]
ansible_ask_sudo_pass=true
use_keychain=true

"""

import getpass
import os
import sys
import  subprocess
from sys import platform
import re

class KeyChain(object):
    find_passwd = re.compile('password: "([^"]+)"').search
    find_user = re.compile('"acct"<blob>="([^"]+)"').search

    @classmethod
    def find_key(cls, fn, out):
        match = fn(out)
        return match and match.group(1)

    @classmethod
    def get_credentials(cls, domain, keychain=None):

        if platform != 'darwin':
            print("Plugin works only on OS X")
            return (None, None)

        cmd = [
            'security',
            'find-generic-password',
            '-g',
            '-s', domain,
        ]
        try:
            out = subprocess.check_output(cmd, stderr=subprocess.STDOUT)
        except subprocess.CalledProcessError:
            return (None, None)
        user = cls.find_key(cls.find_user, out)
        passwd = cls.find_key(cls.find_passwd, out)
        return (user, passwd)

class VarsModule(object):

    sudo_password_cache = {}
    remote_username_cache = {}

    def __init__(self, inventory):
        self.inventory = inventory
        self.inventory_basedir = inventory.basedir()

    def get_host_vars(self, host, vault_password=None):
        """ Get host specific variables. """
        use_keychain = host.get_variables().get("use_keychain")
        hostname = host.get_variables().get('inventory_hostname')
        if '-l' in sys.argv:
            # Check if only limited set of hosts is required for this run and get password only for them
            # quite a dirty way to accomplish that...
            found = False
            for limit in sys.argv[sys.argv.index('-l')+1].split(","):
                m = re.match(limit.replace("*", ".*"), hostname)
                if m is not None:
                    found = True
                    break
            if not found:
                return
        if use_keychain and use_keychain.lower() in ['true', 'yes']:
            if VarsModule.sudo_password_cache.get(hostname) is None:
                user, passwd = KeyChain.get_credentials(host.get_variables()['inventory_hostname'])
                if not user:
                    # Maybe short hostname then?
                    user, passwd = KeyChain.get_credentials(host.get_variables()['inventory_hostname_short'])

                if not passwd:
                    print("Cannot get password for host %s from keychain" % hostname)
                    passwd = getpass.getpass("Password for host %s: "% hostname)
                VarsModule.remote_username_cache[hostname] = user
                VarsModule.sudo_password_cache[hostname] = passwd
            if VarsModule.remote_username_cache[hostname]:
                host.set_variable('ansible_ssh_user', VarsModule.remote_username_cache[hostname])
            host.set_variable('ansible_sudo_pass', VarsModule.sudo_password_cache[hostname])

