from gtts import gTTS
import os

# define variables
s = "hello world"
file = "file.mp3"

# initialize tts, create mp3 and play
tts = gTTS(s, lang='en')
tts.save(file)
os.system("mpg123 " + file)

