
# Wow, lots of imports!
import board, time
import analogio, pwmio
from simpleio import map_range
import json
from random import random, randint
import audiopwmio, audiomixer, synthio

# Read settings from a JSON file (stored on
# your board)
with open('settings.json') as f:
    data = json.load(f)
    min_bpm =           data['min_bpm']
    max_bpm =           data['max_bpm']
    blink_on_duration = data['blink_on_duration']
    led_brightness =    int(data['led_brightness'] * 65535)
    audio_level =       data['audio_level']
    sample_rate =       data['sample_rate']
    attack_time =       data['attack_time']
    release_time =      data['release_time']
    sustain_level =     data['sustain_level']

# Audio setup, just like in the previous examples
audio = audiopwmio.PWMAudioOut(board.GP10)
mixer = audiomixer.Mixer(channel_count=1, sample_rate=sample_rate, buffer_size=2048)
synth = synthio.Synthesizer(sample_rate=sample_rate)

audio.play(mixer)
mixer.voice[0].play(synth)
mixer.voice[0].level = audio_level

envelope = synthio.Envelope(
    attack_time=    attack_time,
    release_time =  release_time,
    sustain_level = sustain_level
)
synth.envelope = envelope

# A simple knob class!
# This lets us set up pins, read and smooth values,
# etc without getting our code super messy
class Knob:
    def __init__(self, pin, smooth=10):
        self.pin = analogio.AnalogIn(pin)
        self.smooth = smooth
        if self.smooth > 0:
            self.values = [ 0 for i in range(0, smooth) ]

    def read(self):
        if self.smooth > 0:
            self.values.append(self.pin.value)
            self.values.pop(0)
            self.mean = sum(self.values) / len(self.values)
            return self.mean
        return self.pin.value

# This LED class is similar, but a bit more complex!
# It uses PWM and can blink without pausing our program,
# a perfect use for a class which can hide the messy
# timing bits behind the scenes
class LED:
    def __init__(self, pin):
        self.pin = pwmio.PWMOut(
            pin, frequency=5000, duty_cycle=0
        )
        self.prev_time = time.monotonic()
        self.on = True

    def set_blink_duration(self, value):
        self.bpm = map_range(
            value,
            0, 65535,
            min_bpm, max_bpm
        )
        delay = (60000 / int(self.bpm)) / 1000  # in seconds
        # print(self.bpm, delay)
        self.blink_off_duration = delay - blink_on_duration

    def update(self):
        now = time.monotonic()
        if self.on:
            if now >= self.prev_time + blink_on_duration:
                self.pin.duty_cycle = 0
                self.prev_time = now
                self.on = False
        else:
            if now >= self.prev_time + self.blink_off_duration:
                self.pin.duty_cycle = led_brightness
                self.prev_time = now
                self.on = True
                return True
        return False

# Create an instance of the Knob and LED classes!
knob = Knob(board.A0, 10)
led =  LED(board.GP2)

# Random MIDI note number
note = randint(0, 127)

while True:
    # Read the knob and use to set the LED's
    # blink rate (aka 'tempo' for audio)
    led.set_blink_duration(knob.read())
    
    # If we're on the start of a beat, play
    # a new random note
    new_beat = led.update()
    if new_beat:
        note += randint(-12, 12)
        if note < 0:
            note = 0
        elif note > 127:
            note = 127
        print(note)

        mixer.voice[0].level = random() * audio_level
        synth.release_all()
        synth.press(note)
    time.sleep(0.001)

