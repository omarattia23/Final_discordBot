import discord
from discord.ext import commands
from discord import app_commands
from gdrive import gdrive
from _log import _logger
from logTask import logTask
import requests
from io import BytesIO
import os
from dotenv import load_dotenv


class send_task(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client
        self.logger = _logger()
        load_dotenv('.env')


    @app_commands.command(
        name="send_task", description="All tasks should be submitted here"
    )
    async def send_task(
        self,
        interaction: discord.Interaction,
        task_number: str,
        file: discord.Attachment,
    ):
        """Command: send_task

        Parameters:
        - task_number (str): The number of the task to be submitted.
        - file (discord.Attachment): The file attachment to be submitted.

        Submits a task with the specified number and a file attachment to the designated Google Drive folder.
        """
        try:
            await interaction.response.defer(ephemeral=False)
        except:
            print("Error")
        try:
            task_number = int(task_number)
        except:
            await interaction.followup.send("Invalid task number.", ephemeral=True)
            self.logger.error(
                f"{interaction.user} entered invalid task number: '{task_number}'"
            )
            return
        try:
            # user name
            user_name = interaction.user.global_name
            user_id = interaction.user
            print("username:" + user_name)
            # self.Mechanical_users = [
            #     "eslamsala7",
            #     "ibrahimeid.",
            #     "osamaasharaf",
            #     "mohameddawoud._37071",
            #     "mahmoud_ramdan",
            #     "abdallah.galal.",
            #     "mohammedwaly.162",
            #     "mohamed_fathy.",
            #     "youssefsalama0532_75933",
            #     "knockknock4652",
            #     "ahmed.moshtak",
            #     "ahmed.ibrahim_mechanical",
            #     "mohamedhamdy_mechanical",
            #     "mohamedtarek0492_21782",
            #     "ibrahim_221",
            #     "mohamed_goda_",
            #     "ahmed_abdelnaser",
            # ]
            # if str(user_id) not in self.Mechanical_users:
            #     # Create a GoogleDriveFile instance
            #     folder_id = [
            #         "1kTQ8aS09SzJehyre0CdXANy8DccjkgT3",
            #         "10WBerw-jxyH078S6WOb9rswsYZ6NDf_1",
            #         "13P3fshEVTnZfdI9QYtsXKCaYIzyfam3z",
            #         "1UFJxDmcgJRAEtOX101p7-9fWXR8iTUqT",
            #         "1IkQ0UGr1-yu2XGaya_dh8-0p0YJPjxf4",
            #         "15B7YJ1OTHMKSyf76l07lCKA4CC7MB8BG",
            #         "1qmsEs2KTJtX1E8-0ZJaqUaayV8Ydnb8X",
            #         "1z2KPos5dBunJx8Xk1MLoQd4C4_tYFsZW",
            #         "1E0N-wDhYUWP85WnwY3hbArrk0pj7Ctwd",
            #         "1dKYgbpNyYGQXiFePaLKFPQ-eIuqdjMBc",
            #         "1SOTuhqB7idIDtFCBiUmBS_QlhVSTkEn6",
            #         "1PXZJaN8XKVjL0hJvz7L4U9CEgHWWC1Jd",
            #         "1g4whM-sINoq7YRZL4BGamrAbYh9qUxLa",
            #     ]
            # else:
            #     folder_id = [
            #         "1XkuxgvWI6XaLH2T6ACQksgWysMJkC_V4",
            #         "1N_poXbRxdEyaXjnoOnHmrgNPRhimGROO",
            #         "1rLcF4gssJHWDjlUoHfdd8iRoM9VMIFwN",
            #         "1b4WmvpSAkwuiPjhHW7SfQqPxMRZeLtl8",
            #         "1nIAFjzR0e9ZB1YF4JsESeYjV0wUQSStY",
            #         "1bTEUeqNPU3fA-vcTrnz9gGUcYcw-oemq",
            #         "1X_L_PIdMlRMWm4moG3-W2rCMrMjBXPqY",
            #         "1rsh82U9SaQ1Yds-Wf-52uzVCe47sttTB",
            #         "10GHDMlW3eKOVAyPwRlCkxjW8cD9gBS8t",
            #         "1IWXWHx31fDXpP_dLi6IEo4n-Zc8JtuDI",
            #     ]

            folder_ids = os.getenv("task_folder_ids")
            folder_ids = folder_ids.split(",")
            # print(folder_ids)
            gfile = gdrive().CreateFile(
                {
                    "title": file.filename,
                    "parents": [{"id": folder_ids[int(task_number) - 1]}],
                    "content-length": file.size,  # Set the content length explicitly
                }
            )
            print(type(folder_ids))
            print(folder_ids[int(task_number) - 1])
            response = requests.get(file.url)
            file_data = BytesIO(response.content)
            
            # Save the file data to a temporary file
            temp_file_path = f"temp/{file.filename}"
            with open(temp_file_path, "wb") as temp_file:
                temp_file.write(file_data.getvalue())
            # Set the content file from the temporary file
            
            gfile.SetContentFile(temp_file_path)
            
            # Upload the file to Google Drive directly
            gfile.Upload()
            
            os.remove(temp_file_path)
            
            
            # Get the link to the uploaded file
            # file_url = gfile['alternateLink']

            # Send the file link as a response in Discord
            # await interaction.response.send_message(f'Uploaded file to Google Drive. You can access it [here]({file_url}).', ephemeral=True)
            logTask(user_name, str(user_id), task_number, "---", str(file.filename))
            await interaction.followup.send(
                f"**{user_name}** successfully submitted **Task #{task_number}**"
            )
            # if str(user_id) not in self.Mechanical_users:
            #     self.logger.info(
            #         f"**{user_name}** successfully submitted **Task #{task_number}** Electronics"
            #     )
            # else:
            #     self.logger.info(
            #         f"**{user_name}** successfully submitted **Task #{task_number}** Mechanical"
            #     )
            
        except Exception as e:
            self.logger.error(
                f"**{user_name}** coundn't submitted **Task #{task_number}**"
            )
            self.logger.error(e)
            print(e)


async def setup(client: commands.Bot) -> None:
    await client.add_cog(send_task(client))


