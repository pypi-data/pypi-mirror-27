import discord


# Class containing relevant data about the message author.
# Subclass of discord.User, as the author being discord.Member is not guaranteed.
# NOTE: might just do away with AuthorInfo, since it doesn't do much meaningful stuff compared
# NOTE: to a normal discord.Member object.
class AuthorInfo(discord.Member):

    def __init__(self, message: discord.Message):

        self.info = message.author

        super().__init__(username=self.info.name,
                         id=self.info.id,
                         discriminator=self.info.discriminator,
                         avatar=self.info.avatar,
                         bot=self.info.bot)

        self.is_member = isinstance(self.info, discord.Member)