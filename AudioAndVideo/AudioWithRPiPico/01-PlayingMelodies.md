# PLAYING MELODIES

One note on repeat is pretty boring: let's play a melody! We'll build on the code from the last example, but play through a list of notes.

***

### CONTENTS  

* [Playing melodies](#playing-melodies)  
* [Full code example](#full-code-example)  

***

### PLAYING MELODIES

Beeps and boops are fine, but what if we wanted to play a melody? No problem! We'll need a list of pitches in our melody, so here's the first line to *Happy Birthday*:

    D D E D G F#

We can look up the MIDI note numbers for these notes [using a chart like this](https://inspiredacoustics.com/en/MIDI_note_numbers_and_center_frequencies). You'll notice that each note also has a number next to it. That's the octave, or where on the scale that note is found. Using `4` will give us a nice middle-of-the-keyboard scale to work with:

```python
notes = [ 62, 62, 64, 62, 67, 66 ]
```

Put into a list, we can use a for-loop to play them!

```python
while True:
    for n in notes:
        synth.press(n)
        time.sleep(0.1)
        synth.release_all()
        time.sleep(0.1)
```

Not too shabby, but very robotic. That's because the duration of the notes was all exactly the same. Going back to our list of frequencies, let's group each note with a duration value:

```python
notes = [ 
  (62, 0.2),  # a "tuple"!
  (62, 0.1),  # stores the note at index 0
  (64, 0.4),  # and the duration at index 1
  (62, 0.4),
  (67, 0.4),
  (66, 0.8) 
]
```

We can then grab the note and duration in the for-loop, playing each note followed by a short pause:

```python
for note in notes:
    synth.press(note[0])
    time.sleep(note[1])
    synth.release_all()
    time.sleep(0.1)
```

***

### FULL CODE EXAMPLE  

```python
import board, time
import audiopwmio, audiomixer, synthio

# Set up our audio output
audio = audiopwmio.PWMAudioOut(board.GP10)
mixer = audiomixer.Mixer(
    channel_count = 1, 
    sample_rate = 44100, 
    buffer_size = 2048
)
synth = synthio.Synthesizer(sample_rate=44100)

# Connect to a mixer object and set overall volume
audio.play(mixer)
mixer.voice[0].play(synth)
mixer.voice[0].level = 1.0

# MIDI note names and note durations
notes = [ 
  (62, 0.2),  # A "tuple"!
  (62, 0.1),  # Stores the note at index 0
  (64, 0.4),  # And the duration at index 1
  (62, 0.4),
  (67, 0.4),
  (66, 0.8) 
]

while True:
  # Play the melody
  for note in notes:
      synth.press(note[0])
      time.sleep(note[1])
      synth.release_all()
      time.slee(0.1)

  # Then a short pause before starting again
  time.sleep(1)
```

***

### CHALLENGES  

1. Can you add the next line in *Happy Birthday*?  
2. Can you find the formula to convert notes into MIDI names? Try implementing it as a function!  

