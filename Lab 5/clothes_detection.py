
#This example is directly copied from the Tensorflow examples provided from the Teachable Machine.

import tensorflow.keras
from PIL import Image, ImageOps
import numpy as np
import cv2
import sys

# weather API: https://pypi.org/project/python-weather/
import python_weather
import asyncio
import gtts
from io import BytesIO
from pydub.playback import play
from pydub import AudioSegment
import pyaudio

def playAudio(text):
    tts = gtts.gTTS(text, lang='en')
    mp3 = BytesIO()
    tts.write_to_fp(mp3)
    mp3.seek(0)
    audio = AudioSegment.from_file(mp3, format='mp3')
    play(audio)

# Disable scientific notation for clarity
np.set_printoptions(suppress=True)

img = None
webCam = False
if(len(sys.argv)>1 and not sys.argv[-1]== "noWindow"):
   try:
      print("I'll try to read your image");
      img = cv2.imread(sys.argv[1])
      if img is None:
         print("Failed to load image file:", sys.argv[1])
   except:
      print("Failed to load the image are you sure that:", sys.argv[1],"is a path to an image?")
else:
   try:
      print("Trying to open the Webcam.")
      cap = cv2.VideoCapture(0)
      if cap is None or not cap.isOpened():
         raise("No camera")
      webCam = True
   except:
      print("Unable to access webcam.")


# Load the model
model = tensorflow.keras.models.load_model('clothing_model.h5')
# Load Labels:
labels=[]
f = open("clothes_labels.txt", "r")
for line in f.readlines():
    if(len(line)<1):
        continue
    labels.append(line.split(' ')[1].strip())

playAudio("Today's temperature is 57 degrees.")

global what_to_wear
what_to_wear = 0
global rain
rain = False
global temp
temp = -99999

while(True):

    if webCam:
        ret, img = cap.read()

    rows, cols, channels = img.shape
    data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)

    size = (224, 224)
    img =  cv2.resize(img, size, interpolation = cv2.INTER_AREA)
    #turn the image into a numpy array
    image_array = np.asarray(img)

    # Normalize the image
    normalized_image_array = (image_array.astype(np.float32) / 127.0) - 1
    # Load the image into the array
    data[0] = normalized_image_array

    # run the inference
    prediction = model.predict(data)
    print("I think its a:",labels[np.argmax(prediction)])

    if np.argmax(prediction) == 3:
        playAudio("Background detected")

    else:
        playAudio("I think you are wearing a " + labels[np.argmax(prediction)])

        if np.argmax(prediction) == what_to_wear:
            print("Outfit matches")
            playAudio("You are good to go. Goodbye.")
            break
        elif np.argmax(prediction) == 0:
            if what_to_wear == 1:
                playAudio("You should wear more clothes. Do not forget your coat.")
            elif what_to_wear == 2:
                playAudio("You should wear less clothes. Here is a t shirt.")
        elif np.argmax(prediction) == 1:
            if what_to_wear == 0:
                playAudio("You should wear less clothes. Here is your jacket.")
            elif what_to_wear == 2:
                playAudio("You should wear less clothes. Here is a t shirt.")
        elif np.argmax(prediction) == 2:
            if what_to_wear == 0:
                playAudio("You should wear more clothes. Do not forget your jacket.")
            elif what_to_wear == 1:
                playAudio("You should wear more clothes. Do not forget your coat.")

    if webCam:
        if sys.argv[-1] == "noWindow":
           cv2.imwrite('detected_out.jpg',img)
           continue
        cv2.imshow('detected (press q to quit)',img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            cap.release()
            break
    else:
        break

cv2.imwrite('detected_out.jpg',img)
cv2.destroyAllWindows()