# MULTIPLE SERVOS

One servo is cool, but what if we want two? Or 10?!

***

### CONTENTS  

* [Using two servos](#using-two-servos)  
* [Timing issues](#timing-issues)  
* [More!](#more)  
* [Full code example](#full-code-example)  
* [Challenges](#challenges)

***

### USING TWO SERVOS  

Using two servos will be exactly like one! In order to make our code a bit cleaner and easier to modify, let's create a function that takes in a pin as the argument and returns a connected `Servo` object:  

```python
def connect_servo(pin, min_pulse=300, max_pulse=2700):
    pwm = pwmio.PWMOut(
        pin,
        duty_cycle = 2**15,
        frequency = 50
    )
    return servo.Servo(
        pwm,
        min_pulse = min_pulse,
        max_pulse = max_pulse
    )
```

Then we can connect two servos like this:  

```python
motor1 = connect_servo(board.D5)
motor2 = connect_servo(board.D6)
```

And make them move like we usually do!

```python
motor1.angle = 45
motor2.angle = 135
time.sleep(1)
```

To see how we do this in a for-loop, check out the full code below.

***

### TIMING ISSUES  

You will see however that the motors move one at a time, not together. That's because `time.sleep()` is *blocking*, meaning it stops our program entirely until the delay is finished. This means nothing else can happen during that period, like reading sensors. 

One approach to solving this is to create a timer in code, which records the start time and checks whether the delay is finished each time around the `while` loop. You can also check out [this more complex example from Adafruit](https://learn.adafruit.com/multi-tasking-with-circuitpython/servos).

***

### MORE!  

But what about MORE servos?! Luckily, we can add as many servos as we have PWM pins on our board. The only limitation is the amount of current that the Feather can provide. Current is how much electricity is being "sucked" from the power supply by the motor: since USB/our Feather can only provide 500mA, more than two small motors is definitely more than our power supply can handle.

To use more motors, you'll need an external 5VDC power supply. Just hook up all the 5V/ground connections to your supply. Be sure your Feather is also connected to the power supply's ground to avoid communication issues. Then hook up the control wires as normal!

***

### FULL CODE EXAMPLE  

```python
import board, time, pwmio
from adafruit_motor import servo

# A little function to make the creation of servos
# easier. Takes in a pin for the servo (and, optionally,
# the pulse values we figured out in the first example)
# and returns a Servo object
def connect_servo(pin, min_pulse=300, max_pulse=2700):
    pwm = pwmio.PWMOut(
        pin,
        duty_cycle = 2**15,
        frequency = 50
    )
    return servo.Servo(
        pwm,
        min_pulse = min_pulse,
        max_pulse = max_pulse
    )

# Connect our two motors
motor1 = connect_servo(board.D5)
motor2 = connect_servo(board.D6)

while True:
    # Set the motors to opposite angles!
    motor1.angle = 45
    motor2.angle = 135
    time.sleep(1)
    
    # Move motor 1 from 45 to 135º by 5º increments
    # And move motor 2 from 135–45º
    for angle in range(45,135, 5):
        motor1.angle = angle
        motor2.angle = 180-angle  # Converts the angle to 135–45º
        time.sleep(0.01)
    time.sleep(1)
```

Note: if you want your motors to move to/from completely different angles, you'll either need two separate for-loops (and one motor will move at a time) or the [`map_range()` function in the `adafruit_simplemath` library](https://docs.circuitpython.org/projects/simplemath/en/latest/api.html#adafruit_simplemath.map_range).

***

### CHALLENGES  

1. The ancient mode of communication called [*semaphore*](https://en.wikipedia.org/wiki/Semaphore) uses two flags, lights, or other signals to send messages. Can you create a two-motor semaphore machine that takes in a message and displays it?

