#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This is a prototype of a simple state machine that remotely executes a list of
commands via SSH on network devices (expecting the prompt_pattern to match) and
returns the results to you.
"""

import logging
import re
import select
import socket
import os

import paramiko

from . import AbstractConnector

__author__ = 'ege'

PROMPT_PATTERN = r'\S+(>|#|-|:)'
logger = logging.getLogger(__name__)


class Channel(object):
    def __init__(self, host, username, password, prompt_pattern=PROMPT_PATTERN, init_commands=[], port=22
                 , allow_agent=False, look_for_keys=False, eol='\n', delay_after_command=None, debug=False,
                 debug_prompt=None, debug_data=None):
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.prompt = re.compile(prompt_pattern)
        self.init_commands = init_commands
        self.allow_agent = allow_agent
        self.look_for_keys = look_for_keys
        self.results = []
        self.eol = eol
        self.delay_after_command = delay_after_command
        self.debug = debug

        if self.debug:
            self.debug_prompt = debug_prompt
            self.debug_data = debug_data
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        self.ssh = ssh
        self.initialized = False
        self.has_prompt = False
        self.promt_node = None
        self.shell = None
        logger.debug("EOL character is %s" % self.eol)

    def run(self, commands):
        """
        This is what we call do actually connect and start the event loop
        """

        if not self.debug:
            # Establish the SSH connection
            self.ssh.connect(self.host, port=self.port, username=self.username, password=self.password
                             , allow_agent=self.allow_agent, look_for_keys=self.look_for_keys)
            # Create an SSH shell descriptor. This is how we're going to interact
            # with the remote device.
            shell = self.ssh.invoke_shell()
            shell.settimeout(0.0)
            self.shell = shell

        self.commands = commands
        # Turn the list of commands into an iterator, so we know when we've run
        # out of commands
        self.cmditer = iter(self.commands)

        # Establish the data buffer we'll use to store output between commands
        self.data = ''

        # And start the event loop to store the results of the commands and
        # return them when we're done.

        results = self.interact()
        return results

    def interact(self):
        import time
        import uuid
        """Interact with the device using the SSH shell."""
        shell = self.shell
        file_name = 'discovery_data_%s.txt' % uuid.uuid4().hex

        with open(file_name , 'w+') as data_file:

            # Start an infinite while loop, and use the select.select async I/O
            # handler to detect when data has been received by the SSH shell.
            while True:
                if not self.debug:
                    # The ``r`` variable names the object that has received data. See:
                    # http://docs.python.org/2/library/select.html#select.select
                    r, w, e = select.select([shell], [], [])
                    # If 'shell' has received data, try to retreive it:
                    if shell in r:
                        # log.debug("HEY LET'S DO SOMETHING WITH SHELL")
                        try:
                            # Fetch 1K off the socket.
                            bytes = shell.recv(8192)

                            # If it's no data, we're done.
                            if len(bytes) == 0:
                                logger.info("len(bytes) = 0, breaked!")
                                break
                        # If we timeout or get an error, log it and carry on.
                        except (socket.timeout, socket.error) as err:
                            logger.error(str(err))

                    # If the socket has not received any data after we sent somethign,
                    # disconnect.
                    else:
                        break
                else:
                    if not self.has_prompt:
                        bytes = self.debug_prompt.read(8192)
                    else:
                        bytes = self.debug_data.read(8192)
                    # Try to process the data we received.
                self.data_received(bytes, data_file)
                if self.delay_after_command:
                    time.sleep(float(self.delay_after_command))

        # The explicit call to disconnect
        data_file.close()
        os.remove(data_file.name)
        shell.close()
        if self.debug:
            self.debug_prompt.close()
            self.debug_data.close()
        # And finally return the output of the results.
        return self.results


    def data_received(self, bytes, data_file):
        """
        This is what we do when data is received from the socket.

        :param bytes:
            Bytes that are received.
        """
        # This is our buffer. Until we get a result we want, we keep appending
        # bytes to the file.

        # Check if the prompt pattern matches. Return None if it doesn't so the
        # event loop continues to try to receive data.
        #
        # Basicaly this means:
        # - Loop until the prompt matches
        # - Trim off the prompt
        # - Store the buffer as the result of the last command sent"
        # - Zero out the buffer
        # - Rinse/repeat til all commands are sent and results stored

        # Promt detection
        if not self.has_prompt:
            m = self.prompt.search(bytes)

            if m:
                self.promt_node = m.group(0)  # '[local]cankiri-ttnet-1>'
                self.has_prompt = True
        # The prompt matched! Strip the prompt from the match result so we get
        # the data received withtout the prompt. This is our result.
        # Only keep results once we've started sending commands
        if self.initialized:
            if bytes:
                if not self.promt_node:
                    logger.exception("Disappeared promt of node")
                data_file.write(bytes)
                if not bytes.endswith(self.promt_node[-1:]):
                    return None
            data = data_file.seek(0)
            data = data_file.read()
            self.results = data[data.find('\n') + 1:data.rfind('\n') - 1]

        # And send the next command in the stack.
        self.send_next()


    def send_next(self):
        """
        Send the next command in the command stack.
        """
        # We're sending a new command, so we zero out the data buffer.
        # Check if we can safely initialize. This is a chance to do setup, such
        # as turning off console paging, or changing up CLI settings.
        if not self.initialized:
            if self.init_commands:
                for command in self.init_commands:
                    logger.info('Running initial command: %s%s' % (command, self.eol))
                    if not self.debug:
                        self.shell.send(command + self.eol)  # Send this command

                self.init_commands = []
                return None
            else:
                logger.debug('Successfully initialized for command execution')
                self.initialized = True

        # Try to fetch the next command in the stack. If we're out of commands,
        # close the channel and disconnect.
        try:
            next_command = self.cmditer.next()  # Get the next command
        except StopIteration:
            self.close()  # Or disconnect
            return None

        # Try to send the next command
        if next_command is None:
            self.results.append(None)  # Store a null command w/ null result
            self.send_next()  # Fetch the next command
        else:
            logger.info('sending %r' % next_command)
            if not self.debug:
                self.shell.send(next_command + self.eol)  # Send this command


    def close(self):
        """Close the SSH connection."""
        if not self.debug:
                self.ssh.close()


class SshParamiko(AbstractConnector):
    host = None
    port = None
    username = None
    password = None
    timeout = None
    channel = None
    init_commands = []
    delay_after_command = None

    def __init__(self, host, port=22, init_commands=['terminal length 0'], eol='\n',
                 delay_after_command=None, debug=False):
        self.host = host.split('/')[0] if '/' in host else host
        self.port = port
        self.init_commands = init_commands
        self.eol = eol

        self.delay_after_command = delay_after_command
        self.has_prompt = False
        self.debug = debug

    def login(self, prompt, login_prompt, password_prompt, username, password, timeout=None):
        self.timeout = timeout

        self.channel = Channel(self.host, username, password, prompt_pattern=prompt, init_commands=self.init_commands
                               , port=self.port, eol=self.eol, delay_after_command=self.delay_after_command,
                               debug=self.debug)

        return True

    def logout(self, logout_command=list(['exit'])):
        if logout_command:
            self.channel.run(logout_command)
        self.channel.close()
        if not self.channel.shell.closed:
            logger.exception("SSH session/channel still active! host: %s" % self.host)

    def execute_command(self, command, prompt, timeout=None):
        if isinstance(command, basestring):
            command = [command, ]

        results = self.channel.run(command)
        return results

    def execute(self, prompt=None, usernamePrompt=None, passwordPrompt=None, username=None, password=None,
                commands=None, exitPrompt=None, community=None):

        result = None
        try:
            self.login(prompt, usernamePrompt, passwordPrompt, username=username,
                       password=password, timeout=120)

            result = self.execute_command(commands, prompt, timeout=30)

        except Exception as e:
            logger.error('Unable to execute command correctly!\nEXCEPTION: %s' % e)
        finally:
            self.logout()

        return result