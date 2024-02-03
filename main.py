import discord
from discord.ext import commands
from datetime import datetime
from keep_alive import keep_alive
from _log import _logger
from discord import app_commands

# # Discord bot setup
# intents = discord.Intents.default()
# intents.typing = False
# intents.presences = False
# intents.message_content = True
# intents.reactions = True  # Make sure to enable the reactions intent
# bot = commands.Bot(command_prefix='!', intents=intents) # Set the command prefix to an empty string


class MyBot(commands.Bot):

  def __init__(self):
    super().__init__(command_prefix=commands.when_mentioned_or('!'),
                     intents=discord.Intents.all())
    # Set up logging
    self.logger = _logger()
    # # Log script start
    self.logger.info("-----------------------")
    self.logger.info("Script started...")
    self.logger.debug(datetime.now().strftime("%d-%b-%Y %H_%M_%S"))

  async def setup_hook(self):
    self.cogslist = [
        "slash_commands.feedback", "slash_commands.send_task",
        "slash_commands.send_project", "slash_commands.send_msg"
    ]
    for ext in self.cogslist:
      await self.load_extension(ext)

  async def on_ready(self):
    try:
      self.logger.info(f'Logged in as {self.user.name}')
      await self.tree.sync()
    except Exception as e:
      self.logger.error(f'Error in on_ready: {e}')


# -------------------------------------------------------------------------------------

if __name__ == "__main__":
  keep_alive()

  # Instantiate the bot and run it
  bot = MyBot()

  @bot.tree.command(name="reload", description="reload slash_commands")
  async def reload(interaction: discord.Interaction):
    await interaction.response.defer(ephemeral=True)
    cogslist = [
        "slash_commands.feedback", "slash_commands.send_task",
        "slash_commands.send_project", "slash_commands.send_msg"
    ]
    try:
      for s in cogslist:
        await bot.reload_extension(s)
      await interaction.followup.send("Successfully reloaded commands")
    except Exception as e:
      await interaction.followup.send(
          f"Failed! Couldn't reload the command.See error below:\n```{e}```")

  bot.run(
      'MTE2NjQwMjg1NDg0NDY0OTQ5Mw.Gmsco-.-VpZ1LUoKj7LOj8e9hceUXlqIaeRSGAMmVkb9Y'
  )
