[![tests](https://github.com/boutetnico/ansible-role-percona-pmm-server/workflows/Test%20ansible%20role/badge.svg)](https://github.com/boutetnico/ansible-role-percona-pmm-server/actions?query=workflow%3A%22Test+ansible+role%22)
[![Ansible Galaxy](https://img.shields.io/badge/galaxy-boutetnico.percona_pmm_server-blue.svg)](https://galaxy.ansible.com/boutetnico/percona_pmm_server)

ansible-role-percona-pmm-server
===============================

This role installs [PMM server](https://docs.percona.com/percona-monitoring-and-management/3/) using the [official Docker image](https://hub.docker.com/r/percona/pmm-server).

It is part of a family of Ansible roles allowing to setup and configure PMM:

- [ansible-role-percona-pmm-server](https://github.com/boutetnico/ansible-role-percona-pmm-server)
- [ansible-role-pmm-client](https://github.com/boutetnico/ansible-role-pmm-client)

Requirements
------------

Ansible 2.10 or newer.

Supported Platforms
-------------------

- [Debian - 12 (Bookworm)](https://wiki.debian.org/DebianBookworm)
- [Debian - 13 (Trixie)](https://wiki.debian.org/DebianTrixie)
- [Ubuntu - 22.04 (Jammy Jellyfish)](http://releases.ubuntu.com/22.04/)
- [Ubuntu - 24.04 (Noble Numbat)](http://releases.ubuntu.com/24.04/)

Role Variables
--------------

| Variable                        | Required | Default              | Choices | Comments                                           |
|---------------------------------|----------|----------------------|---------|----------------------------------------------------|
| pmm_server_docker_image_name    | true     | `percona/pmm-server` | string  |                                                    |
| pmm_server_docker_image_version | true     | `3`                  | string  |                                                    |
| pmm_server_docker_pull          | true     | `false`              | boolean | Set `true` to force pulling a newer Docker image.  |
| pmm_server_docker_env           | true     | `{}`                 | dict    |                                                    |
| pmm_server_network_mode         | true     | `bridge`             | string  | `bridge`, `host`, `none` or `container:<name|id>`. |
| pmm_server_ports                | true     |                      | list    | See `defaults/main.yml`.                           |
| pmm_server_container_state      | true     | `started`            | string  | `absent`, `present`, `stopped` or `started`.       |
| pmm_server_restart_policy       | true     | `unless-stopped`     | string  |                                                    |
| pmm_server_anonymous_access     | true     | `false`              | bool    | Enable or disable anonymous dashboard access.      |

Dependencies
------------

Docker

Example Playbook
----------------

    - hosts: all
      roles:
        - role: ansible-role-percona-pmm-server

Testing
-------

## Debian

    molecule --base-config molecule/shared/base.yml test --scenario-name debian-12
    molecule --base-config molecule/shared/base.yml test --scenario-name debian-13

## Ubuntu

    molecule --base-config molecule/shared/base.yml test --scenario-name ubuntu-2204
    molecule --base-config molecule/shared/base.yml test --scenario-name ubuntu-2404

License
-------

MIT

Author Information
------------------

[@boutetnico](https://github.com/boutetnico)
