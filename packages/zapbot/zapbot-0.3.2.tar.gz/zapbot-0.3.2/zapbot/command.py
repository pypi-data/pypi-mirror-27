import discord
from typing import Callable
import asyncio
import inspect
from functools import wraps

class Command:

    def __init__(self, *, name: str, func: Callable, aliases=None, desc: str = None, parent=None,
                 static_typing: bool = True):

        self.name = name
        self.aliases = [] if not aliases else aliases
        self.func = func
        self.desc = desc
        self.parent = parent
        self.children = set()
        self.static_typing = static_typing

    def __str__(self):

        result = "COMMAND NAME: {0}\n" \
                 "NAME ALIASES: {1}\n" \
                 "CMD FUNC NAME: {2}\n" \
                 "DESC: {3}\n" \
                 "TYPING: {4}\n" \
                 "PARENT: {5}\n" \
                 "CHILDREN:\n{6}"

        children_names = "||".join([child.name for child in self.children])
        parent_name = self.parent.name if self.parent else None

        return result.format(self.name, self.aliases, self.func.__name__, self.desc,
                             "STATIC" if self.static_typing else "DYNAMIC", parent_name, children_names)

    def __subcommand_decorator(self, func):

        if isinstance(func, Command):
            raise TypeError(''
                            '\nYou used the @subcommand() decorator on what is already a Command.\n'
                            'If you want to make a subcommand, just use only one @subcommand() decorator.\n'
                            "You don't need to use the @command() decorator.")

        if not asyncio.iscoroutinefunction(func) and not isinstance(func, CommandSettings):
            raise TypeError(""
                            "\nThe function you want to make a subcommand must be a coroutine.\n"
                            "If you don't know what a coroutine is, try putting the word "
                            '"async" before "def" in your function.\n'
                            "Here's a quick StackOverflow link about it that may help:\n"
                            "https://stackoverflow.com/questions/41283091/how-to-use-async-await-in-python-3-5\n"
                            "Here's the Python docs on it:\n"
                            "https://docs.python.org/3/library/asyncio-task.html\n"
                            "It's pretty cool, I know.")

        if not isinstance(func, CommandSettings):

            desc = inspect.getdoc(func)

            if isinstance(desc, bytes):
                desc = desc.decode("utf-8")

            name = func.__name__

            subcommand = Subcommand(name=name, func=func, desc=desc, parent=self)
            self.children.add(subcommand)

        else:

            func  # type: CommandSettings

            if not func.desc:
                func.desc = inspect.getdoc(func)

                if isinstance(func.desc, bytes):
                    func.desc = func.desc.decode("utf-8")

            if not func.name:
                func.name = func.__name__

            if not func.func:
                func.func = func

            subcommand = Subcommand(name=func.name, func=func.func, desc=func.desc, parent=self,
                                    static_typing=func.static_typing)
            self.children.add(subcommand)

        return subcommand

    def subcommand(self):

        def decorator(func):

            if isinstance(func, Command):
                raise TypeError(''
                                '\nYou used the @subcommand() decorator on what is already a Command.\n'
                                'If you want to make a subcommand, just use only one @subcommand() decorator.\n'
                                "You don't need to use the @command() decorator.")

            if not asyncio.iscoroutinefunction(func) and not isinstance(func, CommandSettings):
                raise TypeError(""
                                "\nThe function you want to make a subcommand must be a coroutine.\n"
                                "If you don't know what a coroutine is, try putting the word "
                                '"async" before "def" in your function.\n'
                                "Here's a quick StackOverflow link about it that may help:\n"
                                "https://stackoverflow.com/questions/41283091/how-to-use-async-await-in-python-3-5\n"
                                "Here's the Python docs on it:\n"
                                "https://docs.python.org/3/library/asyncio-task.html\n"
                                "It's pretty cool, I know.")

            if not isinstance(func, CommandSettings):

                desc = inspect.getdoc(func)

                if isinstance(desc, bytes):
                    desc = desc.decode("utf-8")

                name = func.__name__

                subcommand = Subcommand(name=name, func=func, desc=desc, parent=self)
                self.children.add(subcommand)

            else:

                func  # type: CommandSettings

                if not func.desc:
                    func.desc = inspect.getdoc(func)

                    if isinstance(func.desc, bytes):
                        func.desc = func.desc.decode("utf-8")

                if not func.name:
                    func.name = func.__name__

                if not func.func:
                    func.func = func

                subcommand = Subcommand(name=func.name, func=func.func, desc=func.desc, parent=self,
                                        static_typing=func.static_typing)
                self.children.add(subcommand)

            return subcommand

        return decorator


class Subcommand(Command):

    def __init__(self, *, name: str, func: Callable, aliases=None, desc: str = None, parent=None,
                 static_typing: bool = True):

        super().__init__(name=name, func=func, aliases=aliases, desc=desc, parent=parent, static_typing=static_typing)


class CommandSettings:

    def __init__(self, *, name: str = None, func: Callable = None, desc: str = None, static_typing: bool = True):

        self.name = name
        self.func = func
        self.desc = desc
        self.static_typing = static_typing


def command(name=None, **attrs):

    def decorator(func):

        if isinstance(func, Command):
            raise TypeError(''
                            '\nYou used the @command() decorator on what is already a Command.\n'
                            'Sadly, a "CommandCommand" object does not exist. Subcommands are a thing, though.\n'
                            'You might want one of those; if so, "@<main command>.subcommand()" should '
                            'be what you need.')

        if not asyncio.iscoroutinefunction(func) and not isinstance(func, CommandSettings):
            raise TypeError(""
                            "\nThe function you want to make a command must be a coroutine.\n"
                            "If you don't know what a coroutine is, try putting the word "
                            '"async" before "def" in your function.\n'
                            "Here's a quick StackOverflow link about it that may help:\n"
                            "https://stackoverflow.com/questions/41283091/how-to-use-async-await-in-python-3-5\n"
                            "Here's the Python docs on it:\n"
                            "https://docs.python.org/3/library/asyncio-task.html\n"
                            "It's pretty cool, I know.")

        if not isinstance(func, CommandSettings):

            desc = inspect.getdoc(func)

            if isinstance(desc, bytes):
                desc = desc.decode("utf-8")

            name = func.__name__

            return Command(name=name, func=func, desc=desc)

        else:

            func  # type: CommandSettings

            if not func.desc:
                func.desc = inspect.getdoc()

                if isinstance(func.desc, bytes):
                    func.desc = func.desc.decode("utf-8")

            if not func.name:
                func.name = func.name

            if not func.func:
                func.func = func

            return Command(name=func.name, func=func.func, desc=func.desc, static_typing=func.static_typing)

    return decorator


def settings(name: str = None, aliases = None, func=None, desc: str = None, static_typing: bool = True):

    def decorator(cmd_func):

        if isinstance(cmd_func, Command):

            cmd_func  # type: Command
            cmd_func.name = name if name else cmd_func.name
            cmd_func.aliases = aliases if aliases else cmd_func.aliases
            cmd_func.func = func if func else cmd_func.func
            cmd_func.desc = desc if desc else cmd_func.desc
            cmd_func.static_typing = static_typing if \
                static_typing != cmd_func.static_typing else cmd_func.static_typing

            return cmd_func

        else:

            return CommandSettings \
            (
                name=name if name else cmd_func.__name__,
                func=func if func else cmd_func,
                desc=desc,
                static_typing=static_typing
            )

    return decorator
