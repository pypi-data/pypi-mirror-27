import inspect

import discord
import asyncio
import importlib
import re as regex
from functools import wraps
from enum import Enum, unique
from collections import OrderedDict

from .commandparsing import CommandParser
from .command import Command
from .exceptions import ZapBotCommandRunException

@unique
class _CommandParamType(Enum):

    DEFAULT = 0
    BOT = 1
    CONTEXT = 2
    AUTHOR = 3
    SERVER = 4


_param_keywords = \
    {
        "BOT": {"bot", "bot_info", "botinfo"},
        "CTX": {"ctx", "context", "contx"},
        "AUTHOR": {"author", "author_info", "authorinfo"},
        "SERVER": {"server", "server_info", "serverinfo"}
    }


def _get_variable(name):
    stack = inspect.stack()
    try:
        for frames in stack:
            try:
                frame = frames[0]
                current_locals = frame.f_locals
                if name in current_locals:
                    return current_locals[name]
            finally:
                del frame
    finally:
        del stack


# Special signals to call from the bot that can allow for specific behavior.
@unique
class BotSignals(Enum):

    # Intended for commands with subcommands, and forces the bot to stop running any commands
    # loaded into the command queue; i.e. it won't run any further subcommands after the current
    # command that returns this.
    HALT_COMMAND = 0


class ZapBot(discord.Client):

    def __init__(self, *, token=None, prefixes=None, help_format=None, pm_help=False, owner=None, **options):

        super().__init__(**options)

        # TODO: load in bot data from config file.

        self.owner = ""

        # NOTE: Change this when updating bot to read from config
        self.token = token

        # Make prefixes a dict of sets
        # Base sets:
        # { ALL: {} }
        # { USER: {} }
        # { ADMIN: {} }
        self.prefixes = set()
        # NOTE: Change this when updating bot to read from config
        self.prefixes.update(prefixes if isinstance(prefixes, list) else [prefixes])

        self.modules = OrderedDict()

        self.commands = set()

        self.command_parser = CommandParser(self)

        # Special bot codes
        self.signals = BotSignals

        # Add help command
        help_command = Command(name="help", func=self.__help_cmd)
        self.commands.add(help_command)

    async def __help_cmd(self, message: discord.Message, *args):

        help_content = ""

        for cmd in self.commands:
            help_content += "`{0}`:\n\t{1}\n".format(cmd.name, cmd.desc) if cmd.desc else "`{0}`\n\n".format(cmd.name)

        await self.say(help_content)

    async def say(self, destination, content=None, *, tts=False, embed=None):

        await self.send_message(destination=destination, content=content, tts=tts, embed=None)

    def add_module(self, cogs):

        def get_module_data(cogs):

            name = None
            cog_list = []

            if isinstance(cogs, dict):

                name = list(cogs.keys())[0]
                cog_list = []

                first_value = list(cogs.values())[0]

                if not isinstance(first_value, list):
                    cog_list.append(first_value)
                else:
                    cog_list.extend(first_value)

            elif isinstance(cogs, list):

                # Get name of the file for the first cog in the list.
                name = cogs[0].rsplit('.', 1)[-1]
                cog_list = cogs

            elif isinstance(cogs, str):

                name = cogs.rsplit('.', 1)[-1]
                cog_list = [cogs]

            return name, cog_list

        module_name, cog_list = get_module_data(cogs)

        self.modules[module_name] = cog_list

        for cog in cog_list:
            self.__add_cog(cog)

    # CRITICAL: Fix adding cogs
    def __add_cog(self, cog: str):

        mod = importlib.import_module(cog, package=None)  # type: module
        # print(mod)
        members = inspect.getmembers(cog)

        commands = []

        for attr in dir(mod):

            attribute = getattr(mod, attr)

            if type(attribute) is Command:
                self.commands.add(attribute)

        for name, member in members:

            if type(member) is Command:

                if member.parent is None:
                    self.commands.add(member)

    @staticmethod
    def get_message_author() -> discord.User:
        return _get_variable("_internal_author")

    @staticmethod
    def get_message_channel() -> discord.Channel:
        return _get_variable("_internal_channel")

    @staticmethod
    def get_current_command() -> Command:
        return _get_variable("_internal_current_command")

    @staticmethod
    def get_current_message() -> discord.Message:
        return _get_variable("_internal_message")

    @staticmethod
    def get_message_content() -> str:
        return ZapBot.get_current_message().content

    async def process_commands(self, message: discord.Message):

        _internal_channel = message.channel
        _internal_author = message.author
        _internal_current_command = None
        _internal_message = message

        print(message.content)

        prefix = self.command_parser.determine_prefix(message.content)

        if prefix == message.content:
            print("Prefix is the only portion of the command")
            return

        if prefix:

            command_queue, command_args = self.command_parser.determine_command_structure(message.content, prefix)

            # print("CMD QUEUE:\n", command_queue)
            # print("CMD ARGS: ", command_args)
            command_arg_lists = self.command_parser.determine_param_lists(command_queue, command_args, message)

            current_command_result = None
            running_command = lambda: not command_queue.is_empty() and \
                                       current_command_result is not self.signals.HALT_COMMAND

            # print("ARG LISTS:\n", command_arg_lists)

            try:

                while running_command():

                    current_run_command = command_queue.dequeue()  # type: Command
                    current_command_args = command_arg_lists.pop(0)

                    _internal_current_command = current_run_command

                    current_command_result = await current_run_command.func(*current_command_args)

            except ZapBotCommandRunException:
                pass
            finally:
                pass

    async def process_command(self, command, args):

        # TODO: Method that runs a single given command.
        # USE:  Allow user to potentially make custom message parsing and running process.
        pass

    # Override of the original Client.run() method that can accept a token or no arguments.
    # If there are no arguments, then the bot will use the token given upon being built, if any.
    def run(self, token: str = None, *args, **kwargs):

        if not token:
            super().run(self.token, *args, **kwargs)
        else:
            super().run(token, *args, **kwargs)

    # BELOW: Utility methods for users

    # Sends a message into the channel the command was given in.
    # Gives the option to automatically delete the message after a specified amount of seconds.
    async def say(self, content: str = None, *, tts: bool = False, embed: discord.Embed = None,
                  lifetime: float = None, format: str = None):

        # TODO: Fix the formatting; it breaks the ability to send messages
        # format = "$CONTENT$" if not format else self.__message_content_format_convert(format)
        # content = self.__message_content_format_finalize(format, content)

        destination = self.get_message_channel()
        sent_message = await self.send_message(content=content, destination=destination, tts=tts, embed=embed)

        if lifetime is not None:

            await asyncio.sleep(lifetime)
            await self.delete_message(sent_message)

        return sent_message

    # Sends a message into the channel the command was given in, with
    # Gives the option to automatically delete the message after a specified amount of seconds.
    async def reply(self, content: str = None, *, tts: bool = False, embed: discord.Embed = None,
                    lifetime: float = None, reply_format: str = None):

        destination = _get_variable("_internal_channel")
        author = _get_variable("_internal_author")

        # reply_format = "$MENTION$, $CONTENT$" if not reply_format else \
        #    self.__message_content_format_convert(reply_format)
        content = "{0}, {1}".format(author.mention, content)

        sent_message = await self.send_message(content=content, destination=destination, tts=tts, embed=embed)

        if lifetime is not None:

            await asyncio.sleep(lifetime)
            await self.delete_message(sent_message)

        return sent_message