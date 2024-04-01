# GENERATING TONES

So far, the only output device we've looked as has been LEDs and motors. But audio isn't too hard, especially using the Raspberry Pi Pico board! While you can create audio with the Feather (see the `AudioWithAdafruitFeather` section) the Pi Pico can run some very helpful audio libraries that our Feather can't :(

To get us started, we'll look at how to create basic tones (aka notes of varying frequencies). The nice thing is that this makes a super loud signal so we don't need any kind of amplification. Later, we'll add some additional controls such as an envelope to change the sound!

***

### CONTENTS  

* [Setting up audio output](#setting-up-audio-output)  
* [Playing notes](#playing-notes)  
* [Full code example](#full-code-example)  
* [Challenges](#challenges)

### STUFF YOU'LL NEED  

* Breadboard-friendly speaker  
* Jumper wires  
* Feather board  
* USB cable  

***

### BASIC SETUP  

The circuit for this example is super simple! All we'll need is a speaker, with one leg connected to `GP10` and the other to ground. These speakers aren't polarized, so you can wire them up in either orientation.

> ⚠️ You'll notice that the pins on the Pi Pico have a different naming convention. This can be confusing! Generally, you can use the name listed on the bottom of the board next to each pin.  

We'll also need to a few libraries to our board:

```python
import board, time

import audiopwmio
import audiomixer
import synthio
```

***

### SETTING UP AUDIO OUTPUT  

With everything wired up, let's set up the audio output:

```python
audio = audiopwmio.PWMAudioOut(board.GP10)
```

Then we create a `mixer` that can output the audio:

```python
mixer = audiomixer.Mixer(
    channel_count = 1, 
    sample_rate = 44100, 
    buffer_size = 2048
)
```

One channel means mono audio. The sample rate is set to `44100` which is a good high quality; we shouldn't need to change the buffer size.

And then we create the synth itself:

```python
synth = synthio.Synthesizer(sample_rate=44100)
```

Whew! With that done, let's set up the audio output and we're ready to play some tones!

```python
audio.play(mixer)
mixer.voice[0].play(synth)
mixer.voice[0].level = 1.0
```

Later, we can change the audio level (`0–1`) as we play notes.

***

### PLAYING NOTES

With everything set up, let's make some notes! The synth library let's us play notes defined in MIDI format. Each note has three values:

1. Note: a note value from `0–127`  
2. Velocity: the volume of the note, also `0–127` but sadly not really supported by `synthio`  
3. Duration: how long the note should last, in seconds  

Let's play the same note over and over :)

```python
while True:
    note =     60
    duration = 1

    # Play the note
    synth.press(note)
    time.sleep(duration)
    synth.release_all()

    # Then 1/2-second silence
    time.sleep(0.5)
```

Bonus! If you want to play chords, you can combine multiple MIDI note numbers into a *tuple* like this: `synth.press((60, 64, 68))`!

***

### ADDING AN ENVELOPE  

If we want to modify how our instrument sounds, we can add an envelope. This adjust the way the synth starts, holds, and ends a note.

Just add this code right after we create the mixer:  

```python
envelope = synthio.Envelope(
    attack_time=    0.2,
    release_time =  0.4,
    sustain_level = 0.8
)
synth.envelope = envelope
```

This will automatically be applied whenever we play a note! Try adjusting the values (all measured in seconds) and see how the synth changes.

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

# Add an envelope to transform the sound
envelope = synthio.Envelope(
    attack_time =   0.2,
    release_time =  0.4,
    sustain_level = 0.8
)
synth.envelope = envelope

# Then play a note over and over!
while True:
    note =     60   # MIDI note value (0–127)
    duration = 1    # Length to play note (sec)

    # Play the note
    synth.press(note)

    # Or multiple notes!
    # synth.press((60, 64, 68))

    time.sleep(duration)
    synth.release_all()

    # Then 1/2-second silence
    time.sleep(0.5)
```

***

### CHALLENGES  

1. Can you use Python's `random` library to create random tones? Hint: use `randint` to generate notes in the MIDI range  

