import requests

class GITLABHelper(object):
    def __init__(self, url, token):
        self.url = url
        self.token = token
        self.headers = {"PRIVATE-TOKEN": token}

    @property
    def groups(self):
        url = self.url + '/groups/'
        return requests.get(url, headers=self.headers).json()

    def _get_item_from_list_by_name(self, items, name, type_str):
        for _item in items:
            if _item['name'] == name:
                return _item
        else:
            raise ValueError('%s %s not found' % (type_str, name))

    def get_group_by_name(self, name):
        return self._get_item_from_list_by_name(self.groups, name, 'Group')

    def get_project_by_name(self, name):
        return self._get_item_from_list_by_name(self.projects, name, 'Project')

    @property
    def projects(self):
        url = self.url + '/projects/'
        return requests.get(url, headers=self.headers).json()

    def _create_sub_group_by_parent_group_id(self, parent_id, group_name):
        url = self.url + '/groups'
        params = {
            "name": group_name,
            "path": group_name,
            "description": "SCM create seb sub group automatically",
            "request_access_enabled": True,
            "visibility": "internal",
            "parent_id": parent_id,
        }

        return requests.post(url, params, headers=self.headers).json()

    def create_sub_group_by_parent_group_name(self, parent_group_name, group_name):
        _group = self.get_group_by_name(parent_group_name)
        return self._create_sub_group_by_parent_group_id(_group['id'], group_name)

    def _create_project_under_group_by_group_id(self, group_id, project_name):
        url = self.url + '/projects'
        params = {
            "namespace_id": group_id,
            "name": project_name,
            'visibility': "internal"
        }

        return requests.post(url, params, headers=self.headers).json()

    def create_project_under_group_by_group_name(self, group_name, project_name):
        _group = self.get_group_by_name(group_name)
        return self._create_project_under_group_by_group_id(_group['id'], project_name)

    def _set_protected_branch_by_project_id(self, project_id, branch_name):
        url = self.url + '/projects/' + str(project_id) + '/protected_branches'
        params = {
            "name": branch_name,
            "push_access_levels": [
                {
                    "access_level": 40,
                    "access_level_description": "Masters"
                }
            ],
            "merge_access_levels": [
                {
                    "access_level": 30,
                    "access_level_description": "Developers + Masters"
                }
            ]
        }

        return requests.post(url, params, headers=self.headers).json()

    def set_protected_branch_by_project_name(self, project_name, branch_name):
        _project = self.get_project_by_name(project_name)
        return self._set_protected_branch_by_project_id(_project['id'], branch_name)

    def _get_user_id_by_username(self, username):
            url = self.url + '/users?username=%s' % username
            res = requests.get(url, headers=self.headers).json()
            return res[0]['id']

    def add_user_to_project(self, username, project_name):
        project = self.get_project_by_name(project_name)
        url = self.url + '/projects/%s/members' % project['id']

        params = {
            "user_id": self._get_user_id_by_username(username),
            "access_level": 30
        }

        return requests.post(url, params, headers=self.headers).json()

    def add_user_to_group(self, username, group_name):
        group = self.get_group_by_name(group_name)
        url = self.url + '/groups/%s/members' % group['id']

        params = {
            "user_id": self._get_user_id_by_username(username),
            "access_level": 30
        }

        return requests.post(url, params, headers=self.headers).json()


    def __repr__(self):
        return ''''
            Current environment information
            url => "{url}"
            token => "{token}"'''.format(url=self.url, token=self.token)


if __name__ == '__main__':
    TOKEN = '_yCUXgMgrPxLqqy5CZtT'
    URL = 'https://gitlabe1.ext.net.nokia.com/api/v4'
    g = GITLABHelper(URL, TOKEN)
    from pprint import pprint

    # username = 'kevinwan'
    # project = 'p2'
    # id = g._get_user_id_by_username(username)
    # pprint(id)
    # res = g.get_project_by_name(project)
    # pprint(res['id'])
    # res = g.add_user_to_project(username, project)
    # pprint(res)

    # username = 'kevinwan'
    # group = 'wxj1'
    # id = g._get_user_id_by_username(username)
    # pprint(id)
    # res = g.get_group_by_name(group)
    # pprint(res['id'])
    # res = g.add_user_to_group(username, group)
    # pprint(res)