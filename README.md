# PICOREOS

This repository provides a set of ansible roles to provision a coreos rpi4 server, on a raspberry pi 4b, and, to some extent, harden it a little.

The firmware is provided by https://github.com/pftf/RPi4/releases and coreos-installer installs coreos.

To get started you will need to create a playbook that calls the roles.  An example playbook is included as picoreos_pb.yml

## roles
The following roles are run for a complete install:
&nbsp;&nbsp;
- rpi4_coreos&emsp;&emsp;&emsp;&emsp;&emsp;uses latest https://github.com/pftf/RPi4/release to install the latest firmware and coreos-installer to install the coreos fedora version that you define as 'fedora_version'
- req_install&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;installs the packages that are required for ansible to work on coreos
- devsec_os_hardening&emsp;a modified fork of [devsec_os_hardening](#devsec_hardening)
- devsec_ssh_hardening&emsp;a modified fork of [devsec_ssh_hardening](#devsec_hardening)
- nordvpn&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;openvpn install of nordvpn configured to connect to random uk vpn server on boot
- server_hardening&emsp;&emsp;to come... fail2ban and some other bits and pieces

## caveat!
<b>MAKE CERTAIN</b> that the disk name is correct in the [variables](#variables) for the rpi4_coreos role.

The rpi4_coreos role is a <b>destructive operation</b> and will overwrite anything that is on the target disk.

You will need to put the microssd card into a slot on your machine, and then define which disk name it is in the playbook as the variable to the rpi4_coreos role.  The rpi4_coreos role will run to install the latest coreos and firmware and will then prompt you to remove the ssd card and place it in your raspberry pi, and boot up.

As soon as the pi has finished booting, which you can confirm with ```ssh core@picoreos.lan```, you can press enter to continue.  All roles/tasks from then on will run automatically, unless the script detects that you need to adjust sudo settings on the remote.

There are a few reboots during the process of installation and these take some time, as coreos on the pi4b takes about 4 minutes to reboot.

## if interrupted
If the ansible script is interrupted for some reason and you then rerun, be aware that the previous run may have installed something that then gets picked up earlier in the script as a reboot.

## tested against
This repo has only been tested against a rpi4b with 8Gb of ram.

## dependencies
  create a new python virtual environment and install ansible, python3-rpm on the host and pip install rpm in the prefix.
  Tested using Fedora Silverblue as a control node.

  It is necessary to create an ssh key file using ssh-keygen.  The following command will work:
  ```
  ssh-keygen -t ed25519 -C your_comment_here
  ```
  Make sure to use a secure password.  The files id_ed25519 and id_ed25519.pub will be created unless you
  specify different filenames.  You will need to tell the rpi4_coreos role where to find the public keyfile.
  See the rpi4_coreos section of [variables](#variables).  This is used in the butane file so that the
  ssh key is provisioned into the microssd image.

## optional
  You can layer/install coreos-installer and ansible will use it.  If it doesn't find it, it uses a version inside a container instead.

## configuration

### butane
You can find the butane template in roles/rpi4_coreos/templates/.  Coreos has an immutable file system and so currently /var is mounted within a luks encrypted partition.  If you want to unlock this partition on another machine you will need to define an encryption key in the butane configuration.

### variables
  You will need to add some variables to call the roles
  - rpi4_cores
  ```
    rpi4_coreos_provision_disk: "sdb"
    rpi4_coreos_ssh_path: '~/.ssh/id_ed25519.pub'
  ```
  - req_install
  ```
    fedora_version: 41
  ```
  - os_hardening:
  ```
    os_immutable_fs: true
    os_auditd_enabled: false
  ```
  -ssh_hardening
  ```
    os_immutable_fs: true
    ssh_authorized_keys_file: '.ssh/authorized_keys.d/ignition'
  ```
  - nordvpn
    NordVPN uses an auth.txt file with two lines of a password for accessing
    the nordvpn service via openvpn.  The following variables are vault encrypted
    lines to that file.  See https://support.nordvpn.com/hc/en-us/articles/20285620014353-Linux-start-on-boot-manual-connection for more information
  ```
  nordvpn_openvpn_auth_txt_upper: !vault |
    $ANSIBLE_VAULT;1.1;AES256
    30356239336663323737323661613237336131643664306231316263323439396330393861386366
    6166333065336561353035393633626538666630616263350a303066313866333534343863636133
    37613130353761383062363264376535386337663666326563633263336134393530396463616462
    3730646130656437370a653434323037656365633564383232353837313265313039653730346465
    39353338366334336639306438663164
  nordvpn_openvpn_auth_txt_lower: !vault |
    $ANSIBLE_VAULT;1.1;AES256
    37343364336161333235343133396130306663363363613938613732376139373165393539323535
    3039646539303162316663643338353764356530656161360a656136383038303566346430616331
    36656432646638313565333132633239353130653838306165356237623666373838386564636532
    3264383162393332310a343731393334306630353932643330363261316465356636613263616437
    63333964333832356364663165663163
  ```

### inventory
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
picoreos_hosts
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
```

## encryption
  You can encrypt the become passwords, nordvpn auth.txt lines etc  using the following command:
```
ansible-vault encrypt_string --ask-vault-pass 'password_here'
```
  The vault password that you are prompted for will be entered on the command line.  You will need
to use the same vault password for all the encrypted details.

## command line
```
ansible-playbook -i inventory --ask-vault-password picoreos_pb.yml
```

## ansible tags
As far as possible, the roles are idempotent, so if you interrupt the process you can start again.
If you are restarting, then some of the earlier play tasks that use the raw module with sudo will
moan about lack of sudo access.  This is because the remote_user is removed from the sudo group as
early as possible.  You may get prompted to ssh in to the remote and add the user to the ssh group.
You can skip the removal of the user from the sudo group to prevent this using the following:
```
ansible-playbook -i inventory --ask-vault-password --skip-tags sudo_removal ./picoreos_pb.yml
```
Each of the secondary roles has a tag which allows you to skip those roles if you want.  Available
role tags are:
```
devsec                allows you to skip both os_hardening and ssh_hardening
devsec_os_hardening   allows you to skip devsec.os_hardening
devsec_ssh_hardening  allows you to skip devsec.ssh_hardening
nordvpn               allows you to skip the nordvpn role
```

## devsec_hardening
Picoreos ansible scripts use a modified version of [devsec/ansible-collection-hardening](https://github.com/dev-sec/ansible-collection-hardening) - os_hardening and ssh_hardening.
These have been modified to allow them to work with systems that have an immutable filesystem.
In order to install the collection you will need the following command, inside your virtual environment...
```
ansible-galaxy collection install git+https://github.com/millerthegorilla/ansible-collection-hardening.git,os_immutable_fs
```

## ssh known_hosts

Ansible connects via hostname to the remote.  If the host already exists in the known_hosts file on
the control node, then ssh will complain.  You can either remove the host from known_hosts manually,
or delete the file, or add the following to your command line:
```
ansible-playbook -i inventory --ask-vault-pass --ssh-common-args='-o StrictHostKeyChecking=no' ./picoreos_pb.yml
```
although it is not recommended to do so, as the stricthostkeychecking guards against man in the middle attacks.

## ssh hardening
It is probably sensible to define the following in your control node's .ssh/config file...
```
Host picoreos
  Hostname picoreos
  User core
  PubKeyAuthentication yes
  PubkeyAcceptedKeyTypes=ssh-ed25519
  PreferredAuthentications publickey
  IdentityFile /home/your_username_home_directory_here/.ssh/id_ed25519
  IdentitiesOnly yes
```

## raspberry pi 4b memory limit
If you are using a raspberry pi4b with 4Gb or more, then you will want to attach a keyboard and go to the settings of the pi firmware when it boots, and then go to rapberry pi -> advanced -> remove 3Gb limit.

<b>*Do not*</b> do this until after the first successful boot to completion or the ignition configuration will not have set up coreos and the boot and subsequent boots will fail.

## disclaimer

This repo and the code within are provided as is.  I am not responsible for any problems that arise as
a consequence of using it.  If you have a problem then consider opening an issue.

## license
  mit license
