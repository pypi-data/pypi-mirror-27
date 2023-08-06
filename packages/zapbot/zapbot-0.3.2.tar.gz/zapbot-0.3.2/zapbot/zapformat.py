import discord
import re as regex
# import zapbot
from .exceptions import ZapFormatException

_sub = \
    {
        "data": r"{0}",
        "data+": r"{0\1}",
        "a:name": r"$author.name\1$",
        "a:!name": r"$author.display_name\1$",
        "c:name": r"$channel.name\1$"
    }

_regex = \
    {
        # The content of the message or whatever string is being worked on.
        "content": regex.compile(r"[$]content(.*?)[$]", flags=regex.IGNORECASE),
        # The mention for the caller of the current command.
        "author": regex.compile(r"[$]author(.*?)[$]", flags=regex.IGNORECASE),
        # The name of the server the current command was called in.
        "server": regex.compile(r"[$]server(.*?)[$]", flags=regex.IGNORECASE),
        # The mention for the channel the current command was called in.
        "channel": regex.compile(r"[$]channel(.*?)[$]", flags=regex.IGNORECASE),
        # The currently called command.
        "command": regex.compile(r"[$]command(.*?)[$]", flags=regex.IGNORECASE),
        # The name of the author of the command; $name$ defaults to the author name.
        "a:name": regex.compile(r"[$]a:name(.*?)[$]|[$]name(.*?)[$]", flags=regex.IGNORECASE),
        # The display name of the author of the command; can either use "displayname" or "!name" to denote it.
        # Can also shorten "displayname" to "dname"
        # If the author has a nickname, then that is returned instead of their username.
        "a:!name": regex.compile(
            r"[$]a:!name(.*?)[$]|[$]!name(.*?)[$]|[$]a:d(?:isplay)?name(.*?)[$]|[$]d(?:isplay)?name(.*?)[$]"),
        # The name of the channel the command is called in.
        "c:name": regex.compile(r"[$]c:name(.*?)[$]", flags=regex.IGNORECASE),
        # Variable data that the formatter will find itself during string assembly (via a given ID).
        # Allows for the use of members/users, channels, and roles that are not immediately
        # related to the called command. If a name is given (such as in "$<mod>m:id:ID$"), then any future uses
        # of the name (such as "$mod.name$") will use the same kind of data.
        # VARIABLE TYPES:
        # u (or user): User
        # m (or member): Member (no real difference from user, but can be used as a minor way to state what is expected)
        # c (or channel): Channel
        # r (or role): Role
        "var": regex.compile(
            r"[$](?:<(.+?)>:)?"                                                        # Variable name (optional)
            r"(u(?:ser)?|m(?:ember)?|c(?:hannel)?|r(?:ole)?|e(?:moji)?|e(?:mote)?):"  # Discord data type
            r"(i(?:d)?:|n(?:ame)?:)?"                                                  # Identification type (optional)
            r"(.+?)((?<!\\)[.].+)?[$]",                                                # Variable/Function call on data
            flags=regex.IGNORECASE)
    }


class ZapFormatter:

    def __init__(self, bot):

        self.bot = bot

        # NOTE: FORMAT PROCESS
        # 1) Sub and format data known ahead of time (author, server, etc)
        # 2) For any unknown data (such as a channel denoted with "$<intro channel>c:ID.name$"),

    # Format any Discord data that can be easily gathered and known Ahead Of Time, due to the data being
    # common data that is relevant to the currently called command.
    def __format_aot_data(self, format_string: str):

        formatted_string = format_string

        # Preprocessing
        formatted_string = _regex["a:name"].sub(_sub["a:name"], formatted_string)
        formatted_string = _regex["a:!name"].sub(_sub["a:!name"], formatted_string)
        formatted_string = _regex["c:name"].sub(_sub["c:name"], formatted_string)

        # Processing ahead of time found data
        formatted_string = _regex["content"].sub(_sub["data+"], formatted_string).format(self.bot.get_message_content())
        formatted_string = _regex["author"].sub(_sub["data+"], formatted_string).format(self.bot.get_message_author())
        current_channel = self.bot.get_message_channel()
        formatted_string = _regex["channel"].sub(_sub["data+"], formatted_string).format(current_channel)
        formatted_string = _regex["server"].sub(_sub["data+"], formatted_string).format(current_channel.server)
        formatted_string = _regex["command"].sub(_sub["data+"], formatted_string).format(self.bot.get_current_command())

        return formatted_string

    # Format any Discord data that can be only be known Just In Time, due to the data just being more like
    # some kind of arbitrary Discord data that is not directly relevant to the currently called command, such
    # as a specific chat channel, server role, server member, server emoji, etc.
    def __format_jit_data(self, format_string: str):

        formatted_string = format_string

        # Get iterator for bot format variables.
        format_var_matches = _regex["var"].finditer(formatted_string)

        for var_match in format_var_matches:

            # Extract data from variable signatures.
            var_name = var_match.group(1)
            var_type_full = var_match.group(2)
            var_type = var_type_full.lower()[0]
            var_id_type = var_match.group(3).lower()[0] if var_match.group(3) else None
            var_id = var_match.group(4)
            var_extra = var_match.group(5)
            var_data = None

            # If no type for the identification for the data is provided, default behavior is to try to assume the
            # type; if the identification given is a number, assume it is an ID- otherwise, assume it is a name.
            if var_id_type is None:
                var_id_type = "i" if var_id.isdigit() else "n"

            check_with_id = var_id_type == "i"

            # Variable is a Discord user/member.
            if var_type in {"u", "m"}:
                var_data = \
                    discord.utils.get(self.bot.get_message_channel().server.members, id=var_id) if \
                    check_with_id else discord.utils.get(self.bot.get_message_channel().server.members, name=var_id)

            # Variable is a Discord channel.
            elif var_type == "c":
                var_data = \
                    discord.utils.get(self.bot.get_message_channel().server.channels, id=var_id) if \
                    check_with_id else discord.utils.get(self.bot.get_message_channel().server.channels, name=var_id)

            # Variable is a Discord role.
            elif var_type == "r":
                var_data = \
                    discord.utils.get(self.bot.get_message_channel().server.roles, id=var_id) if \
                    check_with_id else discord.utils.get(self.bot.get_message_channel().server.roles, name=var_id)

            # Variable is a Discord emote/emoji.
            elif var_type == "e":
                var_data = \
                    discord.utils.get(self.bot.get_message_channel().server.emojis, id=var_id) if \
                    check_with_id else discord.utils.get(self.bot.get_message_channel().server.emojis, name=var_id)

            # The requested data was found.
            if var_data:

                # Format out the initial instance of the ZapFormat variable.
                # If access to a class variable or method is wanted, then get the value by evaluation.
                escaped_match = regex.escape(var_match.group(0))

                if var_extra:
                    var_data_value = eval("var_data" + var_extra)
                    formatted_string = regex.sub(escaped_match, "{0}", formatted_string).format(var_data_value)

                else:
                    formatted_string = regex.sub(escaped_match, "{0}", formatted_string).format(var_data)

                # If the variable is named, find any future instances of the same variable and format them out.
                if var_name:

                    # Compile regex to find any other JIT data based on the same variable.
                    future_variable_regex = regex.compile(
                        r"[$]({0})((?<!\\)[.].+)?[$]".format(regex.escape(var_name)), flags=regex.IGNORECASE)

                    future_variable_instances = future_variable_regex.finditer(formatted_string)

                    # For every instance of the current format variable, apply the same kind of process used to
                    # format the first instance of the variable.
                    for future_variable in future_variable_instances:

                        future_extra = future_variable.group(2)

                        escaped_match = regex.escape(future_variable.group(0))

                        if future_extra:
                            future_data_value = eval("var_data" + future_extra)
                            formatted_string = regex.sub(escaped_match, "{0}", formatted_string)\
                                .format(future_data_value)

                        else:
                            formatted_string = regex.sub(escaped_match, "{0}", formatted_string).format(var_data)

            else:
                raise ZapFormatException(
                    message="The data for a ZapFormat variable was not found with the given information:\n"
                    "VARIABLE STRING: {0}\n"
                    "VARIABLE NAME: {1}\n"
                    "VARIABLE TYPE: {2}\n"
                    "IDENTIFICATION TYPE: {3}\n"
                    "GIVEN IDENTIFICATION {4}".format(var_match.group(0), var_name, var_type_full, var_id_type, var_id))

        return formatted_string

    def format(self, content: str, format_string: str):

        formatted_string = self.__format_aot_data(format_string)
        formatted_string = self.__format_jit_data(formatted_string)

        return formatted_string
