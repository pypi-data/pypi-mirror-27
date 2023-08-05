# -*- coding: utf-8 -*-
import gitlab


class GitlabWrapper:
    API_VERSION = '4'

    def __init__(self, url, token):
        self.url = url
        self.token = token
        self.gl = gitlab.Gitlab(url=self.url, private_token=self.token, api_version=self.API_VERSION)

    def get_or_create_user(self, email, name):
        exists_users = self.gl.users.list(search=email)
        if exists_users:
            return exists_users[0]
        username = email[:email.find('@')].replace('.', '_')
        exists_users = self.gl.users.list(username=username)
        if len(exists_users):
            username = username + '_{}'.format(len(exists_users) + 1)
        user_data = dict(
            email=email,
            username=username,
            name=name,
            reset_password=True,
        )
        new_user = self.gl.users.create(user_data)
        return new_user

    def get_or_create_user_project(self, user, repository_name):
        try:
            exists_project = self.gl.projects.get('{}/{}'.format(user.username, repository_name))
            return exists_project
        except gitlab.GitlabGetError:
            pass
        user.projects.create(data={'name': repository_name})
        # делаем еще запрос, для получения проекта со всеми аттрибутами
        exists_project = self.gl.projects.get('{}/{}'.format(user.username, repository_name))
        return exists_project

    def make_user_project_master(self, user, project):
        try:
            project.members.create(data=dict(
                user_id=user.id,
                access_level=40,
            ))
        except gitlab.GitlabCreateError:
            pass

    def copy_files_to_repository(self, base_project, files_path, target_project, autor):
        commit_actions = []
        items = base_project.repository_tree(path=files_path, recursive=True)
        for item in items:
            # item = {'name': '__init__.py', 'path': 'module_01/lesson_01/__init__.py', 'type': 'blob',
            #  'id': '633f866158ac742cf754a2c43edcb07e3a094f3c', 'mode': '100644'}
            if item['type'] == 'blob':
                file_sha = item['id']
                file_info = base_project.repository_blob(sha=file_sha)
                # file_info = {'content': 'IyAtKi0gY29kaW5nOiB1dGYtOCAtKi0KCg==', 'size': 25,
                #  'sha': '633f866158ac742cf754a2c43edcb07e3a094f3c', 'encoding': 'base64'}
                action = dict(
                    action='create',
                    file_path=item['path'],
                    content=file_info['content'],
                    encoding='base64',
                )
                commit_actions.append(action)
        commit_data = {
            'branch': 'master',
            'commit_message': 'Add {}'.format(files_path),
            'actions': commit_actions
        }
        commit = target_project.commits.create(commit_data, sudo=autor)
        return commit
