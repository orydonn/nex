import discord
from discord.ext import commands
import random
from discord.utils import get
import asyncio

database = {}
TOKEN = 'ODU0OTc4NzcyMDcwNjk0OTEz.YMrzBw.YYYiiYEnUkp0H38DZUaqmn0s4L4'

bot = commands.Bot(command_prefix='!')

maincategory = 865318947499016192

channels = {}


class temporary_channel:
    def __init__(self, category, creator):
        self.created_channel = None
        self.creator = creator
        self.channel_category = bot.get_channel(category)

    def checking_data(self):
        if self.creator not in database:
            database.setdefault(self.creator, [str(self.creator.name), self.channel_category, {'bitrate': None, 'user_limit': 5, 'rtc_region': None}])

    async def creating_channel(self):
        for guild in bot.guilds:
            self.created_channel = await guild.create_voice_channel(name=database[self.creator][0], category=database[self.creator][1], **database[self.creator][2])
        await self.creator.move_to(self.created_channel)

    def updating_data(self):
        new_setting = bot.get_channel(self.created_channel.id)
        database[self.creator] = [new_setting.name, self.channel_category,
                            {'bitrate': new_setting.bitrate, 'user_limit': new_setting.user_limit, 'rtc_region': None}]

    async def checking_void(self, channel):
        await channel.delete()
        print(channels_for_delete, '--------------------------')
        return [self.creator]


@bot.event
async def on_voice_state_update(member, before, after):
    if after.channel is not None:
        if after.channel.id == 861291318612590632:
            if member not in channels:
                channels.setdefault(member, temporary_channel(maincategory, member))
            channels[member].checking_data()
            await channels[member].creating_channel()

            # global maincategory
            # maincategory = bot.get_channel(864122028306071583)
            # if member not in database:
            #     database.setdefault(member, [str(member.name), maincategory, {'bitrate': None, 'user_limit': 5, 'rtc_region': None}])
            # print(*database[member])
            # for guild in bot.guilds:
            #     global created_channel
            #     created_channel = await guild.create_voice_channel(name=database[member][0], category=database[member][1], **database[member][2])
            # await member.move_to(created_channel)


    else:
        for created_channel in channels.items():
            if before.channel.id == created_channel[1].created_channel.id:
                created_channel[1].updating_data()
            # new_setting = bot.get_channel(created_channel.id)
            # print('Ливнул')
            # database[member] = [new_setting.name, maincategory, {'bitrate': new_setting.bitrate, 'user_limit': new_setting.user_limit, 'rtc_region': None}]
            # print(*database[member])
            # await created_channel.delete()
            # print(created_channel)
    global channels_for_delete
    channels_for_delete = []
    for created_channel in channels.items():
        if created_channel[1].created_channel.members == []:
            channels_for_delete.append(await created_channel[1].checking_void(created_channel[1].created_channel))
    for deleting_channel in channels_for_delete:
        print(deleting_channel[0])
        channels.pop(deleting_channel[0])


bot.run(TOKEN)
