import uasyncio as asyncio
from neopixel import NeoPixel
from machine import Pin
import random


# Define a simple Queue class
class Queue:
    def __init__(self):
        self._queue = []

    def put(self, item):
        self._queue.append(item)

    def get(self) -> any:
        if self._queue:
            return self._queue.pop(0)
        else:
            return None


# Define a queue for communication between UI and backend
backend_to_ui_queue = Queue()


async def ui_task():
    while True:
        # Check if there's any message from backend
        msg = backend_to_ui_queue.get()
        if msg is None:
            await asyncio.sleep(0.1)
            continue

        old_val, new_val = msg
        print(f"Setting visible LEDs from {old_val} to {new_val}")
        if new_val - old_val > 0:
            for j in range(old_val, new_val):
                if j >= 0:
                    print(f"a) Turning on LED with index {j}")
                    brightness = 0
                    while brightness <= 100:
                        np[j] = (0, brightness, 0)
                        brightness += 1
                        np.write()
                    await asyncio.sleep(0.01)
                else:
                    print(f"b) Turning off LED with index {j - 1}")
                    brightness = 100
                    while brightness >= 0:
                        np[j*(-1) - 1] = (brightness, 0, 0)
                        brightness -= 1
                        np.write()
                    await asyncio.sleep(0.01)

        else:
            for j in reversed(range(new_val, old_val)):
                if j >= 0:
                    brightness = 100
                    print(f"c) Turning off LED with index {j}")
                    while brightness >= 0:
                        np[j] = (0, brightness, 0)
                        brightness -= 1
                        np.write()
                    await asyncio.sleep(0.01)
                else:
                    print(f"d) Turning on LED with index {j - 1}")
                    brightness = 0
                    while brightness <= 100:
                        np[j*(-1) - 1] = (brightness, 0, 0)
                        brightness += 1
                        np.write()
                    await asyncio.sleep(0.01)
        await asyncio.sleep(1)


async def backend_task():
    old_val = 0
    new_val = 0

    # backend_to_ui_queue.put((0, 5))
    # await asyncio.sleep(3)
    # backend_to_ui_queue.put((5, 7))
    # await asyncio.sleep(3)
    # backend_to_ui_queue.put((7, 3))
    # await asyncio.sleep(3)
    # backend_to_ui_queue.put((3, 0))
    # await asyncio.sleep(3)
    # backend_to_ui_queue.put((0, -3))
    # await asyncio.sleep(3)
    # backend_to_ui_queue.put((-3, 3))
    # await asyncio.sleep(3)
    # exit()

    while True:
        while new_val == old_val:
            new_val = random.randint(((-1) * test_range), test_range)
            # new_val = random.randint(1, num_leds + 1)

        print(f"New LED count: {new_val}")
        backend_to_ui_queue.put((old_val, new_val))
        old_val = new_val
        await asyncio.sleep(5)

# Initialisierung Neopixel
num_leds = 64
test_range = 64
np = NeoPixel(Pin(28, Pin.OUT), num_leds)


# Clear LEDs
for j in range(num_leds):
    np[j] = (0, 0, 0)
np.write()
print("Cleared LEDs")

# Start asyncio event loop
loop = asyncio.get_event_loop()
loop.create_task(ui_task())
loop.create_task(backend_task())

# Example of sending messages between UI and backend
# ui_to_backend_queue.put("Hello from UI!")
# backend_to_ui_queue.put("Hello from backend!")

# Run event loop indefinitely
loop.run_forever()
