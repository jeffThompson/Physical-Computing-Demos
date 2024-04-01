'''
MP3 PLAYBACK

Based on: https://learn.adafruit.com/mp3-playback-rp2040/pico-mp3
'''

import board, time
import audiopwmio, audiomp3

# Audio output on GP10
audio = audiopwmio.PWMAudioOut(board.GP10)

# Open and decode the MP3 file
mp3 = audiomp3.MP3Decoder(
    open('sounds/burp.mp3', 'rb')
)

while True:
    # Start playing the file
    audio.play(mp3)
    
    # While the audio is playing, just
    # hang out and wait
    while audio.playing:
        pass
    
    # Pause briefly then play again :)
    time.sleep(1)