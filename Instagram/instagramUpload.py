import requests
import json
import pyrebase
from PIL import Image, ImageFont, ImageDraw
import textwrap
import time
import random

def make_image(
    text,
    author,
):
    font=r"Instagram\RobotoSlab.otf"
    font_autor=r"Instagram\TiltWrap.otf"
    font_color=(255, 255, 255)
    bg = Image.open(r"Instagram\Image\bg.png")

    def center_wrap(text, cwidth, **kw):
        lines = textwrap.wrap(text, **kw)
        return "\n".join(line.center(cwidth) for line in lines)
    
    width = 35

    centered_text = center_wrap(text, cwidth=40, width=width)
    text = centered_text
    W, H = bg.width, bg.height
    draw = ImageDraw.Draw(bg)


    font_size = int(35*W/720)
    font = ImageFont.truetype(font, font_size)


    box = draw.multiline_textbbox((0,0), text, font=font)

    x = (W - box[2]) / 2
    y = (H - box[3]) / 2

    draw.multiline_text(
        (x, y),
        text,
        font=font,
        align="center",
        fill=font_color,
    )   

    font_size_author = int(font_size / 1.28)
    fontAuthor = ImageFont.truetype(font_autor, font_size_author)

    author_box_width = draw.textbbox((0, 0), author, font=fontAuthor)[2]
    author_box_height = draw.textbbox((0, 0), author, font=fontAuthor)[3]

    author_x = (W - author_box_width) /2 - 20
    author_y = (H - author_box_height) /2 + 200


    bg.save(r"Instagram\Image\auxx.png")
    bg = Image.open(r"Instagram\Image\auxx.png")

    drawAuthor = ImageDraw.Draw(bg)

    drawAuthor.text(
        (author_x, author_y), 
        author.upper(), 
        font=fontAuthor,
        align="center",
        fill=font_color,
    )



    font_size_user = 20
    fontUser = ImageFont.truetype(font_autor, font_size_user)

    user = "The Quote Realm"

    user_box_width = draw.textbbox((0, 0), user, font=fontUser)[2]
    user_box_height = draw.textbbox((0, 0), user, font=fontUser)[3]

    user_x = 30
    user_y = H - 30 - user_box_height

    bg.save(r"Instagram\Image\auxx.png")
    bg = Image.open(r"Instagram\Image\auxx.png")

    drawUser = ImageDraw.Draw(bg)

    drawUser.text(
        (user_x, user_y), 
        user, 
        font=fontUser,
        align="center",
        fill=font_color,
    )

    bg.save(r"Instagram\Image\final.png")

def instagramUpload(quote, author):

    make_image(quote,author)

    config = {
    "apiKey": "AIzaSyD4tlVVzKXPXalFTIdpBAlNlW5tXOdbHn0",
    "authDomain": "thequoterealm-298ea.firebaseapp.com",
    "projectId": "thequoterealm-298ea",
    "storageBucket": "thequoterealm-298ea.appspot.com",
    "messagingSenderId": "596007939365",
    "appId": "1:596007939365:web:a7edc9b9dc02c2b95afecc",
    "measurementId": "G-TRJL3CTN77",
    "databaseURL": "gs://thequoterealm-298ea.appspot.com/",
    "serviceAccount": "C:/Users/GrecuAlexandru/Desktop/Autopost/Instagram/serviceAccountKey.json"
    }

    firebase = pyrebase.initialize_app(config)

    storage = firebase.storage()

    rand = random.randrange(0, 10000000000)

    storage.child("final.png"+str(rand)).put(r"Instagram\Image\final.png")



    ig_user_id = '17841458012795061'
    user_access_token = 'EAACWSRyVGjcBAEiuNKyCcWuF4pIv41ksDTfyZCKzvTGcqubpx754B7Cp8BOf9LD6OZCsPOWE3P4N90ZCXXuE39z24pFQZCXzkvn5oafHi0QSfShZBr2lKbYdywJrZCELPTANLPeTmNt4Qf5MqBCnEagjTHqTD6PZCk3IZB0zWIDg8jbudsGbhZAt7YSww1h8sJNIZD'

    time.sleep(20)
    # Post the Image
    image_location_1 = storage.child("final.png"+str(rand)).get_url(None)
    print(image_location_1)
    time.sleep(20)
    post_url = 'https://graph.facebook.com/v16.0/{}/media'.format(ig_user_id)


    with open('hashtags.txt', 'r') as f:
        hashtags = f.readlines()

    hashtags = [tag.strip() for tag in hashtags]
    hashtags_string = ' '.join(hashtags)

    caption = quote+'\n\n- '+ author + "\n\n@the.quote.realm\n@the.quote.realm\n@the.quote.realm\n\n"+hashtags_string
    print(caption)
    payload = {
        'image_url': image_location_1,
        'caption': caption,
        'access_token': user_access_token
        }
    r = requests.post(post_url, data=payload)
    print(r.text)
    result = json.loads(r.text)
    if 'id' in result:
        creation_id = result['id']
        second_url = 'https://graph.facebook.com/v16.0/{}/media_publish'.format(ig_user_id)
        second_payload = {
        'creation_id': creation_id,
        'access_token': user_access_token
        }
        r = requests.post(second_url, data=second_payload)
        print('--------Just posted to instagram--------')
        print(r.text)
    else:
        print('HOUSTON we have a problem')
    time.sleep(10)
    storage.delete("final.png"+str(rand),None)