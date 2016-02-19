# Ansible

Collection of ansible roles and playbooks I have found to be useful.

Roles are tested on Debian Jessie.

Requires python package on remote host.

## Credits
 - Antti Jaakkola (Annttu)
 - Joonas Järveläinen (jonttu)
 - Veli-Matti Leppänen (velzi)


Modules
===

Ferm
---

Combined with ferm_service module, ferm provides easy to use firewall.

#### Variables

|  name     |   description | example | default |
| --------- | ------------- | ------- | ------- |
| ferm_enabled | Should ferm be enabled | yes | yes |
| ferm_ipv6 | Enable ipv6 firewall | yes | yes |
| ferm_raw_table | Enable raw table filters | yes | yes |


Ferm_service
---

This module opens ports to ferm-firewall. Useful when service requires open ports.

#### Usage

Add to role's meta/main.yml

     dependencies:
      - { role: ferm_service, name: someservice, chain: input, saddr: "source-ip-here", dport: someport, proto: tcp }

#### Variables

|  name     |   description | example |
| --------- | ------------- | ------- |
| name      |	name for service | someservice |
| interface | Interface for incoming traffic | eth0 |
| daddr     | Destination address | 10.0.0.1 |
| saddr     | Source address | 10.0.0.0/24 |
| dport     | Destination port | 5555 |
| sport     | source port | 5555 |
| proto     | Protocol, tcp, udp, icmp | tcp |
| chain     | Firewall chain, input, output, forward, input6, output6, forward6 | input |
| action    | Firewall action: DROP, ACCEPT | ACCEPT |


virsh-console
----

Setup libvirt virtual to have getty on virtual serial console ttyS0.

ldap_users
----

Setup pam authentication against ldap and nscd and nslcd to use ldap.

#### Variables

| name | description | example |
| ---- | ----------- | ------- |
| ca_crt | Local path to ca file | /etc/ca.crt |
| ldap_ca | Remote path to ca file | /etc/ldap/ca.crt (default) |
| ldap_server | LDAP server(s) URI | ldaps://ldap.example.com |
| ldap_base | LDAP base dn | dc=example,dc=com |
| login_groups | List of groups allowed to login | sysadmin |

fail2ban
----

Install and setup fail2ban.

Currently only ssh service is supported.

#### Variables



Example config

    fail2ban:
      ignored_hosts:
         - 127.0.0.0/8
         - x.y.z.i/24
      bantime: 3600
      maxretry: 10
      destemail: root@localhost
      banaction: iptables-multiport
    
      services:
       - ssh:
         port: ssh
         logpath: /var/log/auth.log
         filter: sshd

nagios-nrpe
-----

Install and configure nagios-nrpe service.
Uses quite a dynamic plugin configuration via host_vars or group_vars. 

#### Variables

| name  | type | description | example | required |
| ----- | ---- | ----------- | ------- | ------- |
| server_port | int | Port where nrpe server listens | 5666 ( default ) | no |
| user_groups | list | Groups which nagios user should have | Debian-exim | no |
| plugins | list | a list of plugin entries | see [below](#plugin-variables) | yes |
| sudo_plugins | list | a list of plugin entries which requires sudo | see [below](#plugin-variables) | no |


#### Plugin variables
| name     | type   | description | default | example | required |
| -------- | ------ | ----------- | ------- | ------- | -------- |
| name     | string | Name of plugin, automatically prefixed with "check\_" | | disk | yes |
| path     | string | partial or full path to plugin | /usr/lib/nagios/plugins/check_{{ name }} | /usr/lib/nagios/plugins/check_disk or disk |  no |
| warning  | string | warning limit |  | 10% | no |
| critical | string | critical limit | | 20% | no |
| args     | string | plugin arguments | | -p /dev/sda1 | no |

#### Example config

    nagios_nrpe:
     server_port: 5555
     allowed_hosts:
      - 10.0.0.1
     user_groups:
      - Debian-exim
     plugins:
      - name: users
        critical: 30
        warning: 10
      - name: mailq
        args: -M exim
        critical: 100
        warning: 10
     sudo_plugins:
      - name: apt
        args: -u -t 60

munin-node
----------

Install and configure munin-node

#### variables

In munin block

| name     | type   | description   | default | example | required | 
| -------- | ------ | ------------- | ------- | ------- | -------- |
| master_address | ip-address | master ip-address without netmask | | 10.0.0.2 | yes |

#### Example usage

    munin_node:
     master_address: 10.0.0.2

munin-master
----------

Install and configure munin-node

#### variables

In munin block

| name      | type    | description   | default | example | required | 
| --------- | ------- | ------------- | ------- | ------- | -------- |
| rrdcached | boolean | Use rrdcached | true    | true    | false    |

#### Example usage

    munin_master:
     rrdcached: false


NTP
----

Install and configure a ntp server for host.

#### Variables

| name     | type   | description   | default | example | required | 
| -------- | ------ | ------------- | ------- | ------- | -------- |
| servers | list of servers | list of servers, see [server variables](#ntp_server_variables) | 4 pool.ntp.org servers |  | no |
| peers | list of peers | list of peers, see [server variables](#ntp_server_variables) | | no |
| restrict | list of restrictons | see [restrict variables](#ntp_restrict_variables) | allow local, deny others | | no |

#### ntp server variables ####

| name     | type   | description   | default | example | required | 
| -------- | ------ | ------------- | ------- | ------- | -------- |
| address | ip or hostname | peer or server address | | 10.0.0.1 | yes | 
| iburst | boolean | use iburst | false | false | no | 
| burst | boolean | use iburst | false | false | no |
| true | boolean | Force  the  association to assume truechimer status | false | false | no | 
| xleave | boolean | Operate in interleaved mode | false | false | no | 
| key | string | key string | no |  | no | 
| autokey | boolean | use autokey option | false | false | no | 
| minpoll | int | minimum polling interval, in seconds as a power of two | | 10 | no | 
| maxpoll | int | maximum polling interval, in seconds as a power of two | | 20 | no | 
| mode | string | Pass option to a reference clock driver | | | no | 
| noselect | boolean | only display peer/server but don't use | false | false | no | 
| preempt | boolean | Preempt server/peer | false | false | no | 
| ttl | int | ttl used in broadcast and anycast mode | | | no | 
| version | string | specify allowed version | | | no | 

More information on:

    man 5 ntp.conf

#### ntp restrict variables ####

| name     | type   | description   | default | example | required | 
| -------- | ------ | ------------- | ------- | ------- | -------- |
| address | ip or hostname | Client ip or hostname.  | | 10.0.0.1  | yes |
| mask | hostmask | Optional hostmask if ip is a network.  | | 255.255.255.0 | no |
| kod | boolean | send kiss of death packet to denied host. | false | true | no |
| noquery | boolean | Don't allow queries. | false | false | no |
| nomodify | boolean | Don't allow modifications. |false | false | no |
| notrap | boolean | Don't allow control message traps. | false | false | no |
| noserve | boolean | Don't provide time service. | false | false | no |
| nopeer | boolean | Provide stateless service but don't accept as peer. | false | false | no |
| notrust | boolean | Don't allow unauthenticated packages. | false | false | no |
| limited | boolean | see doc | false | false | no |
| ntpport | boolean | Accept only queries from port NTP port (123) | false | false | no |
| version | boolean | Ignore these hosts if not the current NTP version. | false | false | no |
| ignore | boolean | Ignore all packets from hosts. | false | false | no |
| lowpriotrap | boolean | | false | false | no |

More information in [doc.ntp.org](http://doc.ntp.org/4.1.1/accopt.htm)

Sudo
-----

Install sudo package and provide per user or per app sudo permissions using dependencies.

##### example usage

Add to your role's meta/main.yml

    dependencies:
     - { role: sudo, name: somename, user: someuser, command: "somecommand", nopasswd: true }

#### Variables

| name     | type   | description   | default | example | required | 
| -------- | ------ | ------------- | ------- | ------- | -------- |
| name | string | name for file | | apt-dater-sudo | yes |
| user | string | username for sudo permission | | someuser | yes |
| command | string | allow sudo only for this command | | /usr/bin/apt-get | no |
| nopasswd | boolean | enable sudo without password | false | true | no |


apt-dater-host 
-------

Install and configure remote for apt-dater. Uses separate apt-dater user for ssh.

#### Variables

Variables are prefixed with apt_dater_host.

| name     | type   | description   | default | example | required | 
| -------- | ------ | ------------- | ------- | ------- | -------- |
| username | string | name of the user in remote system | apt-dater | apt-dater | no |
| home     | string | home dir path of the user | /var/lib/apt-dater | /home/apt-dater | no |
| ssh_key  | string | public key for apt-dater | | ssh-rsa AAA... | yes |
| forbid_install | bool | Forbid installing new packaged | false | true | no |
| forbid_upgrade | bool | Forbid upgrading system using apt-dater | false | true | no |

##### example usage

In site.yml

    - role apt-dater-host
    
in host_vars or group_vars

    apt_dater_host:
     ssh_key: ssh-rsa AAAA...


network
-----

Configure /etc/networking/interfaces etc.

#### Variables

| name     | type   | description   | default | example | required | 
| -------- | ------ | ------------- | ------- | ------- | -------- |
| network_interfaces | list | list of interfaces |  | see [interface variables](#interface-variables) | yes |
| network_dns_servers | list | list of dns-server addresses | | | no |
| network_domain | string | Domain name | | | no |


#### interface variables

| name     | type   | description   | default | example | required | 
| -------- | ------ | ------------- | ------- | ------- | -------- |
| interface | string | Interface name |  | eth0 | yes |
| ip | ipv4 address | Interface IPv4 address |  | 10.0.0.2 | yes |  
| mask | integer or hostmask | IPv4 address mask |  | 24 or 255.255.255.0 | yes |
| gateway | IPv4 address | gateway address | | 10.0.0.1 | no |
| dhcp | boolean | Use dhcp to acquire address, if true ip, netmask and gateway are ignored | false | true | no |
| dns_servers | list of strings | List of dns-nameservers | | | no |
| dns_search | string | dns-search value | | | no |
| mtu | integer | Interface mtu | | | no |
| boardcast | ipv4 address | IPv4 broadcast address | | 10.0.0.255 | no |
| boardcast | ipv4 address | IPv4 network address | | 10.0.0.0 | no |
| parent | Interface | Parent interface for vlan-interface | | eth0 | no |
| auto6 | ipv6 autoconf | 
| ip6 | ipv6 address | Interface IPv6 address | | 2001:DB8::10:2 | no |
| mask6 | integer | Interface IPv6 address mask | 64 | 64 | no |
| gateway6 | ipv6 address | gateway IPv6 address | 2001:DB8::1 | no |
| accept_ra | boolean, integer |  accept router advertisements | true, false, 0, 1 2 | no |
| autoconf | boolean | IPv6 autoconf | true, false | no |
| privext | boolean, integer | Use IPv6 privacy extension (RFC3041) | true, false, 0, 1, 2 | no |

packages
-------

Install configured packages.

#### Variables


| name     | type   | description   | default | example | required | 
| -------- | ------ | ------------- | ------- | ------- | -------- |
| install_packages | list | List of packages to install | ... | ... | no |

##### example usage

In site.yml

    roles:
      - packages

in host_vars or group_vars

    install_packages:
      - vim
      - screen


ssh
---

Install Openssh-server

#### Variables


| name     | type   | description   | default | example | required |
| -------- | ------ | ------------- | ------- | ------- | -------- |
| ssh_usedns | bool | set to no to disable UseDNS | no | yes | no |
| ssh_all_password_login | bool | enable password logins |  yes | yes | no |
| ssh_x11forwarding | bool | enable password logins | no | yes | no |

##### example usage

In site.yml

    roles:
     - ssh

hostname
--- 

Set system hostname.

### Variables

| name     | type   | description   | default | example | required |
| -------- | ------ | ------------- | ------- | ------- | -------- |
| hostname | string | System hostname fqdn | none | testing.localdomain | yes |

### example usage

In site.yml

    roles:
     - hostname


etckeeper
--- 

Install etckeeper with git.

### example usage

In site.yml

    roles:
     - etckeeper

nginx
--- 

Install nginx web-server. Currently does not support configuration.

### example usage

In site.yml

    roles:
     - nginx

there
--- 

There is a simple multiuser commandline password manager. [There in github](https://github.com/cybercom-finland/there/). This role installs newest there from github.

### Variables

| name     | type   | description   | default | example | required |
| -------- | ------ | ------------- | ------- | ------- | -------- |
| there_path | string | Path to where there stores passwords | /opt/there | /opt/there | no |
| there_group | string | An Unix group which members have access to password directory | there | there | no |

### example usage

In site.yml

    roles:
     - there

apt
---

Set various configuration parameters for apt-get


### Variables

| name     | type   | description   | default | example | required |
| -------- | ------ | ------------- | ------- | ------- | -------- |
| apt_install_suggested | boolean | Setup if apt should install suggested packages by default | false | false | no |
| apt_install_recommends | boolean | Setup if apt should install recommend packages by default | false | false | no |


### example usage

In site.yml

    roles:
     - apt


timezone
---

Set system timezone.

### Variables

| name     | type   | description   | default | example | required |
| -------- | ------ | ------------- | ------- | ------- | -------- |
| timezone | string | Timezone name | UTC | Europe/Helsinki | no |

### example usage

In site.yml

    timezone: Europe/Helsinki


pam_mkhomedir
---

Enable pam_mkhomedir

### Variables

No variables.

### example usage

In site.yml

    roles:
     - pam_mkhomedir

TODO
===

* lldpd
* munin master
* icinga ( master )
* icinga2

vars plugins
============

keychain_sudo.py
------

Plugin that fetches sudo passwords from OS X keychain.

#### Usage

Add path to vars_plugins to your ansible.conf file.

[defaults]
vars_plugins = path/to/vars_plugins

And configure usage for hosts on hosts file.

[all:vars]
ansible_ask_sudo_pass=true
use_keychain=true

Also remove ask_sudo_pass from defaults if defined.

License
===

The MIT License (MIT)

Copyright (c) 2015 Antti Jaakkola

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
