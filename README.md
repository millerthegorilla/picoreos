# PICOREOS

This repository provides a set of ansible roles to provision a coreos rpi4 server, on a raspberry pi 4b, and, to some extent, harden it a little.

To get started you will need to create a playbook that calls the roles.  An example playbook is included as picoreos_pb.yaml

## license
  mit license

## dependencies
  create a new python virtual environment and install ansible, python3-rpm on the host and pip install rpm in the prefix.
  Tested using Fedora Silverblue as a control node.

## optional
  you can layer/install coreos-installer and ansible will use it.  If it doesn't find it, it uses a version inside a container instead.

## configuration
  You will need to configure an inventory with the following groups and variables:
```
ungrouped:
  hosts:
    localhost:
      ansible_connection: local
      ansible_python_interpreter: /usr/bin/python3
      ansible_become_method: sudo
      ansible_become_password: !vault |
          $ANSIBLE_VAULT;1.1;AES256
          3861636662303632383530373966306165616464343463393636313032366662373638613330
          646261373333326464633738663462313437373462650a636166653161656266363736656334
          3366643730373135356633303332633335646633663930313866313031643665373462366162
          3065613132643437630a30316135323265663361366237633633356138356365636333373661
          37643938313162346534646539653866314663537393335616533346664383366
picoreos_hosts:
  hosts:
    picoreos:
      ansible_become_user: root
      ansible_become_method: sudo
      ansible_become_password: !vault |
          $ANSIBLE_VAULT;1.1;AES256
          3365316661623234361613064353065313573465333262373866643666613065326264306662
          366361313461303856532333861353032633238430650a393164383264333962393266376235
          3965366133356633862663238373738663234383163937393432613561383231363430313930
          64656465311640a6466616136643562626634343083130396164343733366133313232656437
dynamically_created_hosts:
```
You can encrypt the become passwords using the following command:
```
ansible-vault encrypt_string --ask-vault-pass 'password_here'
```
The vault password that you are prompted for will be entered on the command line.

## command line
```
ansible-playbook -i inventory --ask-vault-password picoreos_pb.yml
```

## devsec_hardening
Picoreos ansible scripts use a modified version of devsec_hardening - os_hardening and ssh_hardening.  These have been modified to allow them to work with systems that have an immutable filesystem
In order to install the collection you will need the following command, inside your virtual environment...
```
ansible-galaxy collection install git+https://github.com/millerthegorilla/ansible-collection-hardening.git,os_immutable_fs
```
