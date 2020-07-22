import discord
import asyncio
import time
import datetime
from DiscordMessenger import Messenger
from PokeMeowLogic import PokeMeowBotLogic

class MyClient(discord.Client):
    pokeMeow = 'PokéMeow#6691'
    logicBot = 0
    messageSender = 0
    timeOfLastSend = 0
    timeOfLastGet = 0

    async def on_ready(self):
        print("logged on as {0}!".format(self.user))
        self.messageSender = Messenger()
        self.logicBot = PokeMeowBotLogic()
        response = self.logicBot.StartUp()
        self.messageSender.send(response)
        self.timeOfLastGet = time.time()
        self.timeOfLastSend = time.time()
        self.bg_task = self.loop.create_task(self.check_no_response())



    async def on_message(self, message):
        if str(message.author) == str(self.pokeMeow):
            self.timeOfLastGet = time.time()

            embedded = [str(embed.to_dict()) for embed in message.embeds]

            if len(embedded) != 0:
                response = self.logicBot.GetResponse(embedded[0])
            else:
                response = self.logicBot.GetResponse(str(message.content))

            await asyncio.sleep(15.0)
            self.messageSender.send(response)
            self.timeOfLastSend = time.time()

    async def check_no_response(self):
        await self.wait_until_ready()
        while not self.is_closed():
            if time.time() - self.timeOfLastGet > 30 and time.time() - self.timeOfLastSend > 30:
                print("Nothing for 10 seconds, sending ;p")
                self.messageSender.send(";p")

            await asyncio.sleep(5) # task runs every 5 seconds

try:
    f = open("token.txt", "r")
    token = f.readline()
    f.close()
    bot = MyClient()
    bot.run(token)
except:
    print("Couldn't get the token from \'token.txt\'!")
