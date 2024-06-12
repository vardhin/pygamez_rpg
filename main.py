import pygame
import sys
import random
import json
from settings import *
from level import Level
from collections import deque

key_action = func_null
class FixedSizeQueue:
    def __init__(self, max_size):
        self.queue = deque(maxlen=max_size)

    def append(self, item):
        self.queue.append(item)

    def display(self):
        print(list(self.queue))
    
    def get_string(self):
        return ''.join(map(str, self.queue))
spells = FixedSizeQueue(MAX_SPELL_SIZE)


with open("window_titles.json", "r") as file:
    data = json.load(file)
    titles = data["titles"]


def handle_keys(event):
    if event.type == pygame.QUIT:
        return False
    elif event.type == pygame.KEYDOWN:
        if event.key == pygame.K_ESCAPE:  # Quit if ESC key is pressed
            return False
        else:
            # Check if the pressed key is a printable character
            if event.key <= 127 and event.unicode.isprintable():
                # Convert the pressed key to its corresponding ASCII value
                ascii_value = event.key
                print("ASCII value:", ascii_value, "Pressed key:", chr(ascii_value))
                KEY_ASCII_LISTENER = str(chr(ascii_value))
                spells.append(chr(ascii_value))

            else:
                # Print a message indicating which modifier key was pressed
                mods = pygame.key.get_mods()
                if mods & pygame.KMOD_SHIFT:
                    print("Shift key is pressed")
                elif mods & pygame.KMOD_CTRL:
                    print("Ctrl key is pressed")
                elif mods & pygame.KMOD_ALT:
                    print("Alt key is pressed")
                elif mods & pygame.KMOD_META:
                    print("Meta key (Windows key on Windows, Command key on macOS) is pressed")
                elif mods & pygame.KMOD_CAPS:
                    print("Caps Lock is ON")

                if event.key == pygame.K_BACKSPACE:
                    print("Backspace key is pressed")
                elif event.key == pygame.K_TAB:
                    print("Tab key is pressed")
                elif event.key == pygame.K_PAGEUP:
                    print("Page Up key is pressed")
                elif event.key == pygame.K_PAGEDOWN:
                    print("Page Down key is pressed")
                elif event.key == pygame.K_HOME:
                    print("Home key is pressed")
                elif event.key == pygame.K_END:
                    print("End key is pressed")
                elif event.key in (pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT):
                    print("Arrow key is pressed")
                elif event.key == pygame.K_RETURN:
                    print("Return key is pressed")

    return True


class Game:
    def __init__(self):
        # general setup
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption(random.choice(titles))
        self.clock = pygame.time.Clock()

        self.level = Level()
    
    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                running = handle_keys(event)
            self.screen.fill('black')
            self.level.run()
            pygame.display.update()
            self.clock.tick(FPS)

if __name__ == '__main__':
    game = Game()
    game.run()
