# SWEEP

In the [last example](00-ServoMotorBasics.md), we moved the servo to various angles but the movement was basically at top speed. But what if we want our servo to move more slowly? Luckily, this is really easy using a for-loop and some short delay.

This takes a cue from animation and the PWM LED code we learned about earlier: by moving the motor a little bit, then pausing for a really short period before moving again, it creates the illusion of smooth, slow motion. Pretty neat!

***

### CONTENTS  

* [Changing the speed of motion](#changing-the-speed-of-motion)  
* [Why is the motion jerky?](#why-is-the-motion-jerky)  
* [Full code example](#full-code-example)  

***

### CHANGING THE SPEED OF MOTION 

Start by creating your motor in code, using the `min/max_pulse` values you figured out in the last example:

```python
import board, time, pwmio
from adafruit_motor import servo

pin = pwmio.PWMOut(
    board.D5,
    duty_cycle = 2**15,
    frequency = 50
)

motor = servo.Servo(
    pin,
    min_pulse = 300,  # Use the values from
    max_pulse = 2700  # the last example
)
```

Let's start our motor at 45º to start, before our main loop:

```python
motor.angle = 45
time.sleep(1)
```

Now we can sweep it nice and slowly to 135º!

```python
while True:
    for angle in range(45, 135, 5):
      motor.angle = angle
      time.sleep(0.01)
```

This will rotate the motor from 45–135º in increments of 5º. It will wait 1/100th of a second before moving the next 5º, which should provide a slow, even motion. Let's have our motor go back to 45º again at a slower speed:

```python
for angle in range(135, 45, -2):
    motor.angle = angle
    time.sleep(0.01)
```

Try changing the increment and delay values! How do they change the way the motor moves?

***

### WHY IS THE MOTION JERKY?  

This example show you can get *relatively* smooth motion. You'll notice some jerkiness, especially at really slow speeds. Unfortunately, there's no easy way to get around this. You can try experimenting with the angle step and delay times, but that will only get you so far.

Unfortunately, CircuitPython doesn't include acceleration (smooth start/end of motion) or other extra functionality that might help here. You could try implementing this yourself, but a stepper motor is really the best solution when you want really smooth, accurate motion.

***

### FULL CODE EXAMPLE  

```python
import board, time, pwmio
from adafruit_motor import servo

pin = pwmio.PWMOut(
    board.D5,
    duty_cycle = 2**15,
    frequency = 50
)
motor = servo.Servo(
    pin,
    min_pulse = 300,  # Use the values from
    max_pulse = 2700  # the last example
)

# Start at initial position
motor.angle = 45
time.sleep(1)

while True:
    # Clockwise
    for angle in range(45, 135, 5):
        motor.angle = angle
        time.sleep(0.01)
    time.sleep(1)
    
    # Counter-clockwise
    for angle in range(135, 45, -2):
        motor.angle = angle
        time.sleep(0.01)
    time.sleep(1)
```

