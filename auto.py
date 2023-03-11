from TiktokBot import TiktokBot
from MakeVideo import make_video
from Instagram.instagramUpload import instagramUpload
import time
import datetime
import random
import subprocess
import requests


def tiktokupload(text, author):
    # make_video(text,author)

    tiktok_bot = TiktokBot()

    tiktok_bot.upload.uploadVideo("./Output/final_video.mp4",text,author)

    return random.randint(0, 60)


def youtubeshortsupload():

    # Define the command you want to run
    command = 'python ./YoutubeShorts/upload_video.py --file="./Output/final_video.mp4" --title="The Quote Realm | Quotes #quotes #shorts" --description="Quotes | The Quote Realm #quotes #shorts" --privacyStatus="public" --noauth_local_webserver'

    # Run the command and capture the output 
    output = subprocess.check_output(command, shell=True)

    # Print the output
    print(output.decode())


response = requests.get("https://zenquotes.io/api/random")
text = '"' + response.json()[0]['q'] + '"'
author = response.json()[0]['a']

tiktokupload(text,author)

# make_video(text,author)

# random_minute = random.randint(0, 30)
# print("RANDOM MINUTE : " + str(random_minute))
# print("STARTED MACHINE")
# while True:
#     # Get the current time
#     now = datetime.datetime.now()

#     # Check if it's 3pm or 6pm
#     if now.hour == 9 or now.hour == 13 or now.hour == 18:
#         if now.minute == random_minute:
#             # Execute the function
#             print("START")
#             print("Getting Quote : "+str(datetime.datetime.now()))
#             response = requests.get("https://zenquotes.io/api/random")
#             text = '"' + response.json()[0]['q'] + '"'
#             author = response.json()[0]['a']
#             print("Got Quote : "+str(datetime.datetime.now()))
#             print("Uploading to Instagram : "+str(datetime.datetime.now()))
#             instagramUpload(text,author)
#             print("Uploaded to Instagram : "+str(datetime.datetime.now()))
#             time.sleep(60)
#             print("Uploading to Tiktok : "+str(datetime.datetime.now()))
#             random_minute = tiktokupload(text,author)
#             print("RANDOM MINUTE : " + str(random_minute))
#             print("Uploaded to Tiktok : "+str(datetime.datetime.now()))
#             time.sleep(60)
#             print("Uploading to Youtube Shorts : "+str(datetime.datetime.now()))
#             youtubeshortsupload()
#             print("Uploaded to Youtube Shorts : "+str(datetime.datetime.now()))
#             print("END")


#     # Wait for 1 minute before checking again
#     time.sleep(30)