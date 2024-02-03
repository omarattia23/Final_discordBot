from discord.ext import commands
from discord import app_commands
from googleapiclient.errors import HttpError
from _log import _logger
from gsheet import gsheet


class feedback(commands.Cog):

  def __init__(self, client: commands.Bot):
    self.client = client
    self.logger = _logger()
    self.Mechanical_users = [
        'eslamsala7',
        'ibrahimeid.',
        'osamaasharaf',
        'mohameddawoud._37071',
        'mahmoud_ramdan',
        'abdallah.galal.',
        'mohammedwaly.162',
        'mohamed_fathy.',
        'youssefsalama0532_75933',
    ]

  @app_commands.command(name="feedback", description="Get Your Task Feedback")
  async def feedback(self, interaction, task_number: str):
    """Command: feedback

        Parameters:
        - task_number (str): The number of the task for which feedback is requested.

        Retrieves feedback for the specified task number and sends it as a response.
      """
    await interaction.response.defer(ephemeral=True)

    # user id
    id = interaction.user

    if str(id) in self.Mechanical_users:
      self.logger.info(
          f"user: {id} requested to get feedback Task_Number: {task_number} *Mechanical*"
      )
    else:
      self.logger.info(
          f"user: {id} requested to get feedback Task_Number: {task_number} *Electrical*"
      )
    try:
      f = self.feedback_gsheet(id, task_number)
      if str(f) == 'None':
        f = "__Feedback is not released yet__"
    except Exception as e:
      await interaction.followup.send(
          f"Failed to send feedback, please contact us to solve the problem")
      self.logger.error(f"Failed to send feedback: {e}")
      return
    await interaction.followup.send(
        f"Your Feedback Of **Task #{task_number}**\n{f}", ephemeral=True)
    self.logger.info(f"Seccussfully sent feedback")

  # -------------------------------------------------------------------------------------
  # -------------------------------feedback_sheet----------------------------------------
  # -------------------------------------------------------------------------------------

  def feedback_gsheet(self, id, task_number):
    """Retrieves feedback for a specified task number from a Google Sheet.

        Parameters:
        - id: The user ID.
        - task_number (str): The number of the task for which feedback is requested.

        Returns:
        - str: The feedback for the specified task number.
      """

    try:
      service = gsheet()
      # Call the Sheets API
      sheet = service.spreadsheets()
      # The ID and range of a sample spreadsheet.
      FeedBack_SPREADSHEET_ID = '1xtiuZf2pkdLDsQ6Rq9uGdFrMSVkVoZYEdF1GEpsYRak'

      if str(id) in self.Mechanical_users:
        FeedBack_RangeName = 'Mechanical Feedback!A1:Z100'
      else:
        FeedBack_RangeName = 'Electrical Feedback!A1:AL100'

      result = sheet.values().get(spreadsheetId=FeedBack_SPREADSHEET_ID,
                                  range=FeedBack_RangeName).execute()
      # print(result)
      values = result.get('values', [])

      if not values:
        print('No data found.')
        return
      # print(values)
      for row in values:
        # print(row)

        if str(row[0]) == str(id):

          try:
            Task = row[int(task_number) * 2]
            try:
              Notes = row[int(task_number) * 2 + 1]
              fd = f"**Grade**: {Task}\n__**Notes**__:\n{Notes}"
            except:
              fd = f"**Grade**: {Task}"

          # print(fd)
          except:
            fd = "__Feedback is not released yet__"
            # self.logger.error(e)

          return fd

    except HttpError as err:
      self.logger.error(err)


async def setup(client: commands.Bot) -> None:
  await client.add_cog(feedback(client))
