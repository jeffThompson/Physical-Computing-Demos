# CONTROLLING SERVOS REMOTELY

Programming servos to repeat a set of moves can be super useful. You could also think about fun ways to having the motor move, such as totally random! But what if you want to control the servo manually? There are lots of ways we might think about doing this, but a simple example will be to use a potentiometer (a knob) to rotate the motor.

You might use this to create puppets or interactive sculptures. It also would be interesting to think about other kinds of inputs that could control your motor: analog sensors or even communication with your computer's mouse!

***

### CONTENTS  

* [Controlling a servo with a knob](#controlling-a-servo-with-a-knob)  
* [Smoothing the motion](#smoothing-the-motion)  
* [Full code example](#full-code-example)  

***

### CONTROLLING A SERVO WITH A KNOB  

To use a knob to control our servo, we'll need to set up both the servo and knob first:

```python
import board, time, pwmio
import analogio
from adafruit_motor import servo

knob = analogio.AnalogIn(board.A5)

pin = pwmio.PWMOut(board.D5, duty_cycle = 2**15, frequency = 50)
motor = servo.Servo(pin, min_pulse = 300, max_pulse = 2700)
```

We know that the knob gives us values from `0–65535` but our motor's position is measured in degrees. We'll want to scale the knob's input to match the motor, like this:

| KNOB VALUE   | SERVO ANGLE  |
|--------------|--------------|
| 0            | 45º          |
| 32767        | 90º          |
| 65535        | 135º         |

We could code this ourselves, but the `simplemath` library has a useful function that handles this for us! Drag the `adafruit_simplemath.mpy` file to your board, then import the function we need:  

```python
from adafruit_simplemath import map_range
```

The [`map_range()` function](https://docs.circuitpython.org/projects/simplemath/en/latest/api.html#adafruit_simplemath.map_range) takes in a value that in in one range and converts it to another:

```python
angle = map_range(
    knob.value,     # Input value
    0, 65535,       # Expected range of input
    45, 135         # Output range we want
)
```

Now we can read the knob in the main loop and use it to change the angle of the motor, with a small delay afterwards so it has time to move into position:

```python
while True:
    # Read the pot's value
    value = knob.value
    
    # This will be in the full analog range of 0–65535,
    # so we need to scale it to the servo's range
    angle = map_range(value, 0,65535, 45,135)
    
    # Let's print them both to make sure everything is working
    print(value, angle)
    
    # Then we can drive the servo to that location!
    motor.angle = angle
    time.sleep(0.1)
```

***

### SMOOTHING THE MOTION  

You'll notice that the motor's movement isn't very smooth. There are a few reasons for this: slow movements can often be jerky, but we're also not smoothing the values coming in from our messy, real-world sensor! To fix that, let's add the smoothing code we talked about with analog sensors ([see the tutorial](https://github.com/jeffThompson/Physical-Computing-Demos/blob/main/AnalogSensors/02-PlottingAndSmoothingValues.md) for more details on how this works).

First, we'll create a list of values and add a bunch of 0s:

```python
knob_values = []
for i in range(0, 10):
    knob_values.append(0)
```

Then in the loop we can add a new value, delete the oldest one, and average the list:

```python
# Add the new knob value
knob_values.append(value)

# Remove the first (oldest) value
knob_values.pop(0)

# And average the list
value = sum(knob_values) / len(knob_values)
```

Using the averaged value should smooth out the motion a lot!

***

### FULL CODE EXAMPLE  

```python
import board, time, pwmio
from adafruit_motor import servo

# A few extra imports are needed
import analogio
from adafruit_simplemath import map_range

# Create a potentiometer (knob) on A5
knob = analogio.AnalogIn(board.A5)

# Use smoothing to even out the knob's values
knob_values = []
for i in range(0, 10):
    knob_values.append(0)

# And a motor, as we've done before
pin = pwmio.PWMOut(
    board.D5,
    duty_cycle = 2**15,
    frequency = 50
)
motor = servo.Servo(
    pin,
    min_pulse = 300,
    max_pulse = 2700
)

# Start at the middle of travel
motor.angle = 90
time.sleep(1)

while True:
    # Read the pot's value
    value = knob.value
    
    # Smooth it out
    knob_values.append(value)                    # Add the new knob value
    knob_values.pop(0)                           # Remove the first (oldest) value
    value = sum(knob_values) / len(knob_values)  # And average the list
    
    # This will be in the full analog range of 0–65535,
    # so we need to scale it to the servo's range
    angle = map_range(value, 0,65535, 45,135)
    
    # Let's print them both to make sure everything is working
    print(value, angle)
    
    # Then we can drive the servo to that location!
    motor.angle = angle
    time.sleep(0.01)
```

