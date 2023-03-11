import os
from PIL import Image, ImageFont, ImageDraw
import requests
import cv2
import textwrap
import random
import string
from moviepy.editor import VideoFileClip, AudioFileClip
from getShortestLength import get_shortest_length
from cutVideo import cut_video
import time

def deleteFile(filename):
    if os.path.exists(filename):
        os.remove(filename)
    
def add_subtitle(
    bg,
    text="nice",
    author="author",
    xy=("center", 20),
    font="ProximaNovaSemibold.otf",
    font_size=35,
    font_color=(255, 255, 255),
    stroke=3,
    stroke_color=(0, 0, 0),
):
    def center_wrap(text, cwidth=80, **kw):
        lines = textwrap.wrap(text, **kw)
        return "\n".join(line.center(cwidth) for line in lines)

    def random_string(x):
        return ''.join(
            random.choice(
                string.ascii_letters +
                string.digits) for _ in range(x))
    width = 40
    centered_text = center_wrap(text, cwidth=40, width=width)
    text = centered_text
    stroke_width = stroke
    W, H = bg.width, bg.height
    draw = ImageDraw.Draw(bg)


    font_size = int(35*W/720)
    stroke_width = int(3*W/720)
    font = ImageFont.truetype(font, font_size)

    xy = (0, 0)
    box = draw.multiline_textbbox(xy, text, font=font)

    x = (W - box[2]) / 2
    y = ((H - box[3]) / 2) - (H*700/3840)

    draw.multiline_text(
        (x, y),
        text,
        font=font,
        align="center",
        fill=font_color,
        stroke_width=stroke_width,
        stroke_fill=stroke_color,
    )   

    author_box_width = draw.textbbox((0, 0), author, font=font)[2]
    author_box_height = draw.textbbox((0, 0), author, font=font)[3]

    author_x = x + box[2] - author_box_width - 30
    author_y = y + box[3] + author_box_height + 30

    bg.save("auxx.jpg")
    bg = Image.open("auxx.jpg")

    drawAuthor = ImageDraw.Draw(bg)



    drawAuthor.text(
        (author_x, author_y), 
        "- "+author, 
        font=font,
        align="center",
        fill=font_color,
        stroke_width=stroke_width,
        stroke_fill=(15,15,15)
    )

    return bg



def make_video(text, author):
    # GET RANDOM SOUND

    sound_folder_path = "./Sounds"

    # Get a list of all the files in the folder
    sound_files = [f for f in os.listdir(sound_folder_path) if os.path.isfile(os.path.join(sound_folder_path, f))]

    # Choose a random file from the list
    random_sound_file = random.choice(sound_files)


    sound_file = os.path.join(sound_folder_path, random_sound_file)
    # Print the path to the random file


    # GET RANDOM VIDEO

    video_folder_path = "./videos"

    # Get a list of all the files in the folder
    video_files = [f for f in os.listdir(video_folder_path) if os.path.isfile(os.path.join(video_folder_path, f))]

    # Choose a random file from the list
    random_video_file = random.choice(video_files)


    video_file = os.path.join(video_folder_path, random_video_file)
    # Print the path to the random file

    shortest_length = get_shortest_length(video_file, sound_file)

    # Load the video
    cap = cv2.VideoCapture(video_file)
    fps = cap.get(cv2.CAP_PROP_FPS)
    # Define the codec and create VideoWriter object
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter('output.mp4', fourcc, fps,
                        (int(cap.get(3)), int(cap.get(4))))

    # Read frames from video and add text
    while (cap.isOpened()):
        ret, frame = cap.read()
        if ret:
            cv2.imwrite("frame.jpg", frame)
            time.sleep(0.25)
            frame = Image.open("frame.jpg")
            frame = add_subtitle(frame, text, author)
            frame.save("frame.jpg")
            frame = cv2.imread("frame.jpg")
            out.write(frame)
        else:
            break

    # Release the objects
    cap.release()
    out.release()



    # Load the video clip
    video = VideoFileClip("output.mp4")

    # Load the audio clip
    audio = AudioFileClip(sound_file)

    # Overlay the audio on the video
    final_video = video.set_audio(audio)

    # Write the final video to disk
    final_video.write_videofile("video_with_music.mp4")


    cut_video("C:/Users/GrecuAlexandru/Desktop/Autopost/video_with_music.mp4", shortest_length, "C:/Users/GrecuAlexandru/Desktop/Autopost/Output/final_video.mp4")

    cv2.destroyAllWindows()

    # deleteFile("frame.jpg")
    # deleteFile("auxxx.jpg")
    # deleteFile("output.mp4")
    # deleteFile("video_with_music.mp4")