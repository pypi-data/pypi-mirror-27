# -*- coding: utf-8 -*-

__all__ = ['AbstractConnector']


class AbstractConnector(object):
    logout_limit = 5

    def login(self, prompt, login_prompt, password_prompt, username, password, timeout=None):
        pass

    def execute_command(self, command, prompt, timeout=None):
        pass

    def logout(self, logout_command="exit"):
        pass

    def execute(self, prompt=None, usernamePrompt=None, passwordPrompt=None,
                username=None, password=None, commands=None,
                exitPrompt=None, community=None):
        pass
