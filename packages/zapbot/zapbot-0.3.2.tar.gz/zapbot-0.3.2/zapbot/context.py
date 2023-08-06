import discord


class Context:

    def __init__(self, message: discord.Message):

        self.message = message
