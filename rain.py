import time
import sys
import shutil
import random

frame_length = 0.1
raindrop_per_second = 6
use_color = True
color = {
    'trail_color': "\033[0;32m", # Haxor green. 
    'tip_color': "\033[1;37m", # White.
    'reset': "\033[0m"
}

def generate_charset():
    charset = []

    for i in range(0x30A0, 0x30FF + 1): # Katakana block.
        charset.append(chr(i))

    return charset

charset = generate_charset()

def run(charset, frame_length, raindrop_per_second, use_color, color):

    sys.stdout.write('\033[?1049h') # Switch to the alternate screen in terminal.
    sys.stdout.flush()

    raindrops = {}

    while True:
        try:
            cols, rows = shutil.get_terminal_size() # Get terminal size every frame to handle terminal resize.
            sys.stdout.write("\033[2J") # Clear terminal.

            for i in range(raindrop_per_second - 1): # Determine amount of new raindrops per second.
                raindrop_col = random.randrange(1, rows + 1)

                if raindrop_col not in raindrops: # Get a random column and check if there's not already a raindrop there.
                    raindrops[raindrop_col] = Raindrop(random.randrange(1, cols + 1, 2), raindrop_col, random.randrange(cols // 2, cols))

            delete_flags = [] # Collect raindrops that have ended.

            for key, raindrop in raindrops.items():
                raindrop.draw(use_color, color)
                raindrop.update()

                if raindrop.frame >= raindrop.length * 2 + 1:
                    delete_flags.append(key)

            for key in delete_flags:
                del raindrops[key]
            
            sys.stdout.flush()
            time.sleep(frame_length)

        except KeyboardInterrupt:
            sys.stdout.write("\033[?1049l") # Revert to main screen in terminal.
            sys.stdout.flush()
            sys.exit()

class Raindrop:
    def __init__(self, x, y, length):
        self.x = x
        self.y = y
        self.length = length
        self.frame = 1

        if self.length >= self.y: # Trim raindrop that is over the top.
            self.length = self.y - 1

        self.chars = []
        for i in range(self.length):
            self.chars.append(random.choice(charset))

    def draw(self, use_color, color):
        sys.stdout.write("\033[{};{}f".format(self.y, self.x)) # Position cursor to raindrop's end.

        for i in range(self.length): # Draw the characters upwards.
            sys.stdout.write("\033[1A\033[2D") # Move the cursor upwards and compensate for character length (2 for kana).

            if self.frame >= self.length - i and self.frame <= self.length * 2 - i: # Draw only chars in frames where it should appear.
                if use_color:
                    if self.frame == self.length - i or i == 0: # Check if the character is the tip.
                        sys.stdout.write(color['tip_color'] + self.chars[i] + color['reset'])
                    else:
                        sys.stdout.write(color['trail_color'] + self.chars[i] + color['reset'])
                else:
                    sys.stdout.write(self.chars[i])
            else:
                sys.stdout.write("\033[2C") # Compensate for right shift.

    def update(self):
        self.frame += 1

run(charset, frame_length, raindrop_per_second, use_color, color)