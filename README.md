# Ansible Nextcloud Collection

Ansible Nextcloud Collection - is not meant to install nor to maintain your nextcloud itself.  
It's meant to bring up your nextcloud usage to the next level 🚀  
No ssh required.

### Features

[![Build Status](https://drone.osuv.de/api/badges/m/nextcloud_collection/status.svg)](https://drone.osuv.de/m/nextcloud_collection)

* 💾 `file` module - download, upload and delete files
* 🗨 `talk` module - post messages in conversations
* 👥 `user` module - maintain nextcloud users
* 🔑 passwords
  * `lookup` plugin for [passwords app](https://apps.nextcloud.com/apps/passwords)
  * `password` module - create, update and delete [passwords](https://apps.nextcloud.com/apps/passwords)

### Support


| **host** | **category** |
| --- | --- |
| https://git.osuv.de/m/nextcloud_collection | origin |
| https://gitlab.com/markuman/nextcloud_collection | pull mirror, merge-requests and Issues |
| https://github.com/markuman/nextcloud_collection | push mirror, pull-requests and Issues |

# Usage

## Install

https://galaxy.ansible.com/markuman/nextcloud

`ansible-galaxy collection install markuman.nextcloud`

## Auth

You can authenticate either with your user password or with an App-Token (_Settings -> Security -> "Create new app password_).  
When you've setup MFA/2FA/TOTP, you must authenticate with an App-Token.

The collection modules and plugins require the following parameter. Alternatively the parameter can also be set as an ENV variable.

| **Ansible Parameter** | **ENV Variable** |
| --- | --- |
| `host` | `NEXTCLOUD_HOST` |
| `user` | `NEXTCLOUD_USER` |
| `api_token` | `NEXTCLOUD_TOKEN` |

## ssl_mode

`ssl_mode` parameter, default value (`https`).  
* ability to use http:// for integration tests
* ability to skip ssl verification
* Possible values `https`, `http`, `skip`

## lookup passwords

When `details=False`, only the password is returned.  
When `details=True`, the entire object is returned.

```yml
- name: Retrieve Password with label "Stackoverflow"
  debug:
    var: lookup('markuman.nextcloud.passwords', 'Stackoverflow' , host='nextcloud.tld', user='ansible', api_token='some-token', details=False)
```

## file module

The `file` module supports also `access_token` as an alias for `api_token`, to be closer on ansible S3 module.

**mode: get**
```yml
- name: fetch file from nextcloud
  markuman.nextcloud.file:
    mode: get
    src: anythingeverything.jpg
    dest: /tmp/anythingeverything.jpg
    overwritten: different # 'always' is the default. 'never' is an option too.
    host: nextcloud.tld
    user: myuser
    api_token: xxx
```

**mode: delete**

CAUTION ⚠ removes files and folders - recursive!

```yml
- name: delete file on nextcloud
  markuman.nextcloud.file:
    mode: delete
    src: bla.docx
```

**mode: put**

```yml
- name: upload file on nextcloud
  markuman.nextcloud.file:
    mode: put
    src: /tmp/testtt.jpg
    dest: testtt.jpg
```

## talk module

```yml
- name: send hello
  markuman.nextcloud.talk:
    msg: Ho Hi from Ansible.
    channel: 8fyrb4ec
```

## password_info module

| parameter | notes |
| --- | --- |
| `name` | the name of the password |

```yml
- name: look for one password
  markuman.nextcloud.password_info:
    name: ansible-test-01
  register: out

- name: fetch all passwords
  markuman.nextcloud.password_info:
  register: out
```

## password module

| parameter | notes |
| --- | --- |
| `password` | when no password it given, ansible will request an auto-generated password from the nextcloud server |
| `name` | the name of the password |
| `username` | username that belongs to the password |
| `url` | url of the password |
| `notes` | notes to the password |
| `favorite` | whether the password should be marked as favourite or not |
| `state` | `present` or `absent` |
| `update_password` | When to update a password. `on_create` (default) will write the password only if the password record is created. `always` will also update the password if it's exist and the requested password differs from existing. |
| `folder` | Name of the folder where the password must be saved (_works currently only on createion_) |



```yml
- name: sample create
  markuman.nextcloud.password:
    name: ansible-test-05
    password: something
    username: markus
    url: https://nureintest.de
    notes: made with ansible

- name: >
    when no password is requestes
    nextcloud password apps will auto-generate it
  markuman.nextcloud.password:
    name: some super password
```

## user_info

List all nextcloud users.

```yml
- name: get nc users
  markuman.nextcloud.user_info:
  register: out

- debug: msg="{{ out.users }}"
```
