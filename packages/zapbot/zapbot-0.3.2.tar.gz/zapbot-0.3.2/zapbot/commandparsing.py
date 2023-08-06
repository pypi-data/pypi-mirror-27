# from .zapbot import ZapBot
import inspect
from enum import Enum, unique

import discord

from .authorinfo import AuthorInfo
from .context import Context
from .queue import Queue
from .serverinfo import ServerInfo
from .command import Command


@unique
class _CommandParamType(Enum):
    VARIADIC_LIST = -1
    DEFAULT = 0
    BOT = 1
    CONTEXT = 2
    MESSAGE = 3
    AUTHOR = 4
    SERVER = 5

class CommandParser:

    def __init__(self, bot):

        self.bot = bot

        self.__param_keywords = \
            {
                "BOT": {"bot", "zapbot"},
                "CTX": {"context", "ctx", "contx"},
                "MESSAGE": {"message", "msg"},
                "AUTHOR": {"author", "author_info", "authorinfo"},
                "SERVER": {"server", "server_info", "serverinfo"}
            }

    def determine_prefix(self, content: str):

        return next((prefix for prefix in self.bot.prefixes if content.startswith(prefix)), None)

    def determine_command_structure(self, content: str, found_prefix: str):

        command_pieces = content.lstrip(found_prefix).split()
        command_queue = Queue()
        args = Queue()

        root_command = self.find_command(command_pieces[0], self.bot.commands)

        if root_command:

            command_queue.enqueue(root_command)
            index = 1
            subcommand_found = True
            able_to_search_command = lambda: subcommand_found and index < len(command_pieces)

            while able_to_search_command():

                piece = command_pieces[index]
                subcommand = self.find_command(piece, command_queue.last().children)

                subcommand_found = subcommand is not None

                if subcommand_found:
                    command_queue.enqueue(subcommand)
                    index += 1

            if index < len(command_pieces):
                args = command_pieces[index: ]

        return command_queue, args

    # Finds the command from the list of commands that match the given name, if any (includes aliases).
    # If there are multiple matches, for whatever reason, only the first is considered.
    def find_command(self, command_name: str, command_list):

        matched_commands = [command for command in command_list if
                            command_name == command.name or command_name in command.aliases]

        return matched_commands[0] if matched_commands else None

    def determine_param_lists(self, commands: Queue, args, message):

        command_queue_iter = commands.iter(0)
        command_param_lists = []

        context = Context(message)

        while not command_queue_iter.is_empty():

            command = command_queue_iter.dequeue()  # type: Command

            arg_spec = inspect.signature(command.func)

            param_queue = self.__determine_param_queue(arg_spec)  # type: Queue
            param_list = []

            while param_queue:

                param_type = param_queue.dequeue()

                if param_type is _CommandParamType.BOT:
                    param_list.append(self.bot)
                elif param_type is _CommandParamType.CONTEXT:
                    param_list.append(context)
                elif param_type is _CommandParamType.MESSAGE:
                    param_list.append(message)
                elif param_type is _CommandParamType.AUTHOR:
                    param_list.append(message.author)               # TODO: Append AuthorInfo object
                elif param_type is _CommandParamType.SERVER:
                    param_list.append(message.server)
                elif args and command_queue_iter.is_empty():

                    if param_type is _CommandParamType.VARIADIC_LIST:
                        arg = args
                        args = Queue()
                        param_list.extend(arg)
                    else:
                        arg = args.pop(0)
                        param_list.append(arg)

            command_param_lists.append(param_list)

        return command_param_lists

    def __is_special_param(self, name, param_spec, type_to_check: _CommandParamType):

        # print("name:{0}\tspec:{1}".format(name, param_spec))

        param_name = name.lower()
        param_type = param_spec.annotation

        # Determines parameter type via name or type annotation (allowing for any name, if wanted).
        if type_to_check is _CommandParamType.BOT:

            if param_name in self.__param_keywords["BOT"] or param_type is type(self.bot):
                return True

        elif type_to_check is _CommandParamType.CONTEXT:

            if param_name in self.__param_keywords["CTX"] or param_type is Context:
                return True

        elif type_to_check is _CommandParamType.MESSAGE:

            if param_name in self.__param_keywords["MESSAGE"] or param_type is discord.Message:
                return True

        elif type_to_check is _CommandParamType.AUTHOR:

            if param_name in self.__param_keywords["AUTHOR"] or param_type is AuthorInfo:
                return True

        elif type_to_check is _CommandParamType.SERVER:

            if param_name in self.__param_keywords["SERVER"] or param_type is ServerInfo:
                return True

        else:
            return False

    def __determine_param_queue(self, arg_spec: inspect.Signature):

        arg_names = arg_spec.parameters
        param_queue = Queue()

        # TODO: Potentially simplify parameter-typing process and/or make it more efficient.
        for (name, param) in arg_names.items():

            # Parameter is requesting access to the bot
            if self.__is_special_param(name, param, _CommandParamType.BOT) and \
                            _CommandParamType.BOT not in param_queue:
                param_queue.enqueue(_CommandParamType.BOT)

            # Parameter is requesting access to command context info
            elif self.__is_special_param(name, param, _CommandParamType.CONTEXT) and \
                            _CommandParamType.CONTEXT not in param_queue:
                param_queue.enqueue(_CommandParamType.CONTEXT)

            elif self.__is_special_param(name, param, _CommandParamType.MESSAGE) and \
                            _CommandParamType.MESSAGE not in param_queue:
                param_queue.enqueue(_CommandParamType.MESSAGE)

            # Parameter is requesting access to command author info
            elif self.__is_special_param(name, param, _CommandParamType.AUTHOR) and \
                            _CommandParamType.AUTHOR not in param_queue:
                param_queue.enqueue(_CommandParamType.AUTHOR)

            elif self.__is_special_param(name, param, _CommandParamType.SERVER) and \
                            _CommandParamType.SERVER not in param_queue:
                param_queue.enqueue(_CommandParamType.SERVER)

            # Parameter is variadic (corresponds to *args parameter)
            elif param.VAR_POSITIONAL:
                param_queue.enqueue(_CommandParamType.VARIADIC_LIST)

            # Parameter is a regular single parameter
            else:
                param_queue.enqueue(_CommandParamType.DEFAULT)

        return param_queue