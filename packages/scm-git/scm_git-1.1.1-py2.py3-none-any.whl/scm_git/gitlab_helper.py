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

    def __repr__(self):
        return ''''
            Current environment information
            url => "{url}"
            token => "{token}"'''.format(url=self.url, token=self.token)


