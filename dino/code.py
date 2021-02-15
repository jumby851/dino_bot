"""
Prop-Maker based Master Sword
Adafruit invests time and resources providing this open source code.
Please support Adafruit and open source hardware by purchasing
products from Adafruit!
Written by Kattni Rembor & Limor Fried for Adafruit Industries
Copyright (c) 2019-2020 Adafruit Industries
Licensed under the MIT license.
All text above must be included in any redistribution.
"""

import random
import digitalio
import audioio
import audiocore
import board
import neopixel
import adafruit_lis3dh
import time
import dinomoves
import adafruit_rfm69
import busio

###### initialize radio:
spi = busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO)
cs = digitalio.DigitalInOut(board.RX)
reset = digitalio.DigitalInOut(board.TX)
rfm69 = adafruit_rfm69.RFM69(spi, cs, reset, 915.0)


###### initialize neopixels:
NUM_PIXELS = 15 # Number of pixels used in project
NEOPIXEL_PIN = board.D5
POWER_PIN = board.D10

enable = digitalio.DigitalInOut(POWER_PIN)
enable.direction = digitalio.Direction.OUTPUT
enable.value = True

strip = neopixel.NeoPixel(NEOPIXEL_PIN, NUM_PIXELS, brightness=0.1, auto_write=False)
strip.fill(0)  # NeoPixels off ASAP on startup
strip.show()

# CUSTOMISE COLORS HERE:
COLOR = (0, 120, 120)      # Default idle is light blue
COLOR_IDLE = COLOR # 'idle' color is the default

# CUSTOMISE IDLE PULSE SPEED HERE: 0 is fast, above 0 slows down
IDLE_PULSE_SPEED = 0.001
SWING_BLAST_SPEED = 0.007

# CUSTOMISE BRIGHTNESS HERE: must be a number between 0 and 1
IDLE_PULSE_BRIGHTNESS_MIN = 0.2  # Default minimum idle pulse brightness
IDLE_PULSE_BRIGHTNESS_MAX = 1  # Default maximum idle pulse brightness


###### initialize speaker:
audio = audioio.AudioOut(board.A0)  # Speaker
wave_file = None
wave_file_name = None


###### dino movement initialization
DINO_MOVE_DELAY=0.3 # wait time in seconds between motor moves


def play_wav(name, loop=False):
    """
    Play a WAV file in the 'sounds' directory.
    :param name: partial file name string, complete name will be built around
                 this, e.g. passing 'foo' will play file 'sounds/foo.wav'.
    :param loop: if True, sound will repeat indefinitely (until interrupted
                 by another sound).
    """
    global wave_file  # pylint: disable=global-statement
    global wave_file_name  # pylint: disable=global-statement

    if wave_file_name and wave_file_name == name and audio.playing:
        print("wav play pass audio.playing: %s" % audio.playing)
        pass
    print("playing", name)
    if wave_file:
        wave_file.close()
    try:
        wave_file = open('sounds/' + name + '.wav', 'rb')
        wave_file_name = name
        wave = audiocore.WaveFile(wave_file)
        audio.play(wave, loop=loop)
    except OSError:
        print("got an OSError")
        pass # we'll just skip playing then


def mix(color_1, color_2, weight_2):
    """
    Blend between two colors with a given ratio.
    :param color_1:  first color, as an (r,g,b) tuple
    :param color_2:  second color, as an (r,g,b) tuple
    :param weight_2: Blend weight (ratio) of second color, 0.0 to 1.0
    :return (r,g,b) tuple, blended color
    """
    if weight_2 < 0.0:
        weight_2 = 0.0
    elif weight_2 > 1.0:
        weight_2 = 1.0
    weight_1 = 1.0 - weight_2
    return (int(color_1[0] * weight_1 + color_2[0] * weight_2),
            int(color_1[1] * weight_1 + color_2[1] * weight_2),
            int(color_1[2] * weight_1 + color_2[2] * weight_2))


###### Setup idle pulse
idle_brightness = IDLE_PULSE_BRIGHTNESS_MIN  # current brightness of idle pulse
idle_increment = 0.01  # Initial idle pulse direction


###### Setup transform state
is_bowing = False
last_transformation=0


###### main loop
print("and here we go...")
while True:
    packet = rfm69.receive(timeout=0.01)  # Wait for a packet to be received (up to 0.5 seconds)
    if packet is not None:
        msg = str(packet, 'ascii')
        if msg == "forward":
            dinomoves.walk(DINO_MOVE_DELAY)
        elif msg == "left":
            dinomoves.walkRight(DINO_MOVE_DELAY)
        elif msg == "right":
            dinomoves.walkLeft(DINO_MOVE_DELAY)
        elif msg == "A":
            play_wav("happy_new_year_oliver_reformatted")
            if is_bowing:
                for i in range(0,3):
                    dinomoves.dinoChomp(0.2)
        elif msg == "B":
            play_wav("colette_noise")
            if is_bowing:
                dinomoves.dinoChomp(0.3)
        elif msg == "select":
            time_tmp = time.monotonic()
            if last_transformation + 1.5 < time_tmp:
                last_transformation = time_tmp
                print("trying to transform, is_bowing: %s"%is_bowing)
                if is_bowing:
                    dinomoves.robotTransform()
                else:
                    dinomoves.dinoTransform()
                is_bowing=not is_bowing
        elif msg == "special":
            dinomoves.stand()
            for i in range(0,3):
                time.sleep(0.3)
                dinomoves.shiftLeft()
                time.sleep(0.3)
                dinomoves.shiftRight()
            dinomoves.stand()

    # Idle pulse
    idle_brightness += idle_increment  # Pulse up
    if idle_brightness > IDLE_PULSE_BRIGHTNESS_MAX or \
        idle_brightness < IDLE_PULSE_BRIGHTNESS_MIN:  # Then...
        idle_increment *= -1  # Pulse direction flip
    strip.fill([int(c*idle_brightness) for c in COLOR_IDLE])
    strip.show()

'''
is_angle_toggle = True

# CUSTOMISE SENSITIVITY HERE: smaller numbers = more sensitive to motion
HIT_THRESHOLD = 250
SWING_THRESHOLD = 150

# Set to the length in seconds of the "on.wav" file
POWER_ON_SOUND_DURATION = 1.7

# Set up accelerometer on I2C bus, 4G range:
i2c = board.I2C()
accel = adafruit_lis3dh.LIS3DH_I2C(i2c)
accel.range = adafruit_lis3dh.RANGE_4_G

COLOR_IDLE = COLOR # 'idle' color is the default
COLOR_HIT = ALT_COLOR  # "hit" color is ALT_COLOR set above
COLOR_SWING = ALT_COLOR  # "swing" color is ALT_COLOR set above


def power_on(sound, duration):
    """
    Animate NeoPixels with accompanying sound effect for power on.
    :param sound: sound name (similar format to play_wav() above)
    :param duration: estimated duration of sound, in seconds (>0.0)
    """
    prev = 0
    start_time = time.monotonic()  # Save audio start time
    play_wav(sound)
    while True:
        elapsed = time.monotonic() - start_time  # Time spent playing sound
        if elapsed > duration:  # Past sound duration?
            break  # Stop animating
        animation_time = elapsed / duration  # Animation time, 0.0 to 1.0
        threshold = int(NUM_PIXELS * animation_time + 0.5)
        num = threshold - prev  # Number of pixels to light on this pass
        if num != 0:
            strip[prev:threshold] = [ALT_COLOR] * num
            strip.show()
            prev = threshold


# List of swing wav files without the .wav in the name for use with play_wav()
swing_sounds = [
    'colette_noise'
    #'swing1',
    #'swing2',
    #'swing3',
    #'swing4',
]

# List of hit wav files without the .wav in the name for use with play_wav()
hit_sounds = [
    'happy_new_year_oliver_reformatted'
    #'hit1',
    #'hit2',
    #'hit3',
    #'hit4',
]


mode = 0  # Initial mode = OFF

# Main loop
while True:
    if mode == 0:  # If currently off...
        enable.value = True
        power_on('on', POWER_ON_SOUND_DURATION)  # Power up!
        play_wav('idle', loop=True)  # Play idle sound now
        mode = 1  # Idle mode

        # Setup for idle pulse
        idle_brightness = IDLE_PULSE_BRIGHTNESS_MIN
        idle_increment = 0.01
        strip.fill([int(c*idle_brightness) for c in COLOR])
        strip.show()

    elif mode >= 1:  # If not OFF mode...
        x, y, z = accel.acceleration  # Read accelerometer
        accel_total = x * x + z * z
        # (Y axis isn't needed, due to the orientation that the Prop-Maker
        # Wing is mounted.  Also, square root isn't needed, since we're
        # comparing thresholds...use squared values instead.)
        if accel_total > HIT_THRESHOLD:  # Large acceleration = HIT
            TRIGGER_TIME = time.monotonic()  # Save initial time of hit
            play_wav(random.choice(hit_sounds))  # Start playing 'hit' sound
            COLOR_ACTIVE = COLOR_HIT  # Set color to fade from
            mode = 3  # HIT mode
            print('trying to walk')
            for servoNum in range(0,8):
                kit.servo[servoNum].angle= 90 if is_angle_toggle else 0
            is_angle_toggle = not is_angle_toggle
            #time.sleep(0.1)

        elif mode == 1 and accel_total > SWING_THRESHOLD:  # Mild = SWING
            TRIGGER_TIME = time.monotonic()  # Save initial time of swing
            play_wav(random.choice(swing_sounds))  # Randomly choose from available swing sounds
            # make a larson scanner animation_time
            strip_backup = strip[0:-1]
            for p in range(-1, len(strip)):
                for i in range (p-1, p+2): # shoot a 'ray' of 3 pixels
                    if 0 <= i < len(strip):
                        strip[i] = COLOR_SWING
                strip.show()
                time.sleep(SWING_BLAST_SPEED)
                if 0 <= (p-1) < len(strip):
                    strip[p-1] = strip_backup[p-1]  # restore previous color at the tail
                strip.show()
            for servoNum in range(0,8):
                kit.servo[servoNum].angle=90 if is_angle_toggle else 0
            is_angle_toggle = not is_angle_toggle
            #time.sleep(0.1)
            while audio.playing:
                pass # wait till we're done
            mode = 2  # we'll go back to idle mode

        elif mode == 1:
            # Idle pulse
            idle_brightness += idle_increment  # Pulse up
            if idle_brightness > IDLE_PULSE_BRIGHTNESS_MAX or \
               idle_brightness < IDLE_PULSE_BRIGHTNESS_MIN:  # Then...
                idle_increment *= -1  # Pulse direction flip
            strip.fill([int(c*idle_brightness) for c in COLOR_IDLE])
            strip.show()
            time.sleep(IDLE_PULSE_SPEED)  # Idle pulse speed set above
        elif mode > 1:  # If in SWING or HIT mode...
            if audio.playing:  # And sound currently playing...
                blend = time.monotonic() - TRIGGER_TIME  # Time since triggered
                if mode == 2:  # If SWING,
                    blend = abs(0.5 - blend) * 2.0  # ramp up, down
                strip.fill(mix(COLOR_ACTIVE, COLOR, blend))  # Fade from hit/swing to base color
                strip.show()
            else:  # No sound now, but still SWING or HIT modes
                play_wav('idle', loop=True)  # Resume idle sound
                mode = 1  # Return to idle mode
'''