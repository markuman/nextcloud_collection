#!/usr/bin/python
# -*- coding: utf-8 -*-

DOCUMENTATION = '''
module: markuman.nextcloud.user_info
short_description: administrate nextcloud users
description:
  - Add, remove, enable or disable users
version_added: "4.0.0"
author:
  - "Markus Bergholz"
requirements:
  - requests python module
'''

EXAMPLES = '''
    - name: install and enable impersonate app
      markuman.nextcloud.user_info:
'''

from ansible.module_utils.basic import *
from ansible_collections.markuman.nextcloud.plugins.module_utils.nextcloud import NextcloudHandler


def main():
    module = AnsibleModule(
        argument_spec = dict(
            host = dict(required=False, type='str'),
            api_token = dict(required=False, type='str', no_log=True, aliases=['access_token']),
            ssl_mode = dict(required=False, type='str', default='https')
        )
    )

    nc = NextcloudHandler(module.params)

    retval = nc.get('/ocs/v1.php/cloud/users').json()

    module.exit_json(users=retval.get('ocs', {}).get('data', {}).get('users', []))
    

if __name__ == '__main__':
    main()