import board
import busio
import digitalio
import adafruit_sharpmemorydisplay
import time
import numpy as np
import mmap

# Framebuffer parameters
BUFFER_PATH = "/dev/fb0"
BUFFER_WIDTH = 720
BUFFER_HEIGHT = 480
BUFFER_BIT_DEPTH = 16
RESIZE = False

# Adafrui sharp memory display parameters
WIDTH = 400
HEIGHT = 240

# Calculated Parameters 
BYTES_PER_PIXEL = BUFFER_BIT_DEPTH // 8
BUFFER_SIZE = BUFFER_WIDTH * BUFFER_HEIGHT * BYTES_PER_PIXEL
ys = np.linspace(0, BUFFER_HEIGHT - 1, HEIGHT, dtype=np.uint16)
xs = np.linspace(0, BUFFER_WIDTH - 1, WIDTH, dtype=np.uint16)
grid_y, grid_x = np.meshgrid(ys, xs, indexing='ij')

# Board pin mapping
spi = busio.SPI(board.SCK, MOSI=board.MOSI)
scs = digitalio.DigitalInOut(board.D23)  # inverted chip select

display = adafruit_sharpmemorydisplay.SharpMemoryDisplay(spi, scs, WIDTH, HEIGHT)


def clear():
    display.fill(1)
    display.show()

def refresh():
    # Read framebuffer from path
    with open(BUFFER_PATH, "rb") as fb:
        fb_mem = mmap.mmap(fb.fileno(), BUFFER_SIZE, access=mmap.ACCESS_READ)
        arr = np.frombuffer(fb_mem, dtype=np.uint16).reshape((BUFFER_HEIGHT, BUFFER_WIDTH))

        # Downscaling
        if RESIZE:
            downscaled = arr[grid_y, grid_x]
        else:
            downscaled = arr[:WIDTH, :HEIGHT]

        # Pack bits row-by-row (axis=1 preserves alignment)
        packed = np.packbits(downscaled, axis=1, bitorder='big')
        byte_array = packed.flatten().tobytes()

        # Assign framebuffer byte array to display buffer
        display.buffer = byte_array

    fb.close()

    # Display image
    display.show()

# Main program loop
clear()
try:
    while True:
        refresh()
        time.sleep(1/30)
except Exception as e:
    print(e) 
except KeyboardInterrupt:
    print("program was interrupted by user.")
finally:
    clear()
