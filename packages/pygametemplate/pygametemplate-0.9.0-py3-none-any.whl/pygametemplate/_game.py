import os
from contextlib import suppress
import time
from importlib import import_module

import pygame
with suppress(ImportError):
    import pygame._view     # sometimes necessary. If it isn't this will cause an error
    #! UPDATE: this might only be necessary for py2exe to work, so if you can
    # compile without it, then there's no need to import pygame_view whatsoever
import psutil

from pygametemplate import load_image
from pygametemplate.system import System
from pygametemplate.console import Console
from pygametemplate.userinput import Input
from pygametemplate.hotkey import Hotkey
from pygametemplate.text_input import TextInput


pygame.init()


class Game:

    VIEW_MODULE = "lib.views"

    def __init__(self, StartingView, resolution=(1280, 720), mode="windowed",
                 *, caption="Insert name here v0.1.0", icon=None,
                 max_allowed_ram=1**30):
        """Create a new Game object.

        `icon` should be the name of an image file.
        """
        self.pygame = pygame
        self.system = System(self)
        self.width, self.height = resolution
        self.mode = mode
        self.initialise_screen()
        pygame.display.set_caption(caption)
        if icon is not None:
            pygame.display.set_icon(load_image(icon))

        self.max_allowed_ram = max_allowed_ram
        self.previous_views = []
        self.current_view = StartingView(self)

        self.fps = 60
        self.frame = 0  # The current frame the game is on (since the game was opened)

        self.input = Input(self)
        self.console = Console(self)

        self.quit_condition = Hotkey(self, "f4", alt=True).pressed

    def set_view(self, view_name: str):
        """Set the current view to the View class with the given name."""
        self.previous_views.append(self.current_view)
        View = self.get_view_class(view_name)   # pylint: disable=invalid-name
        for view in reversed(self.previous_views):
            if isinstance(view, View):
                self.current_view = view
                self.previous_views.remove(view)
                break
        else:
            self.current_view = View(self)

        while get_memory_use() > self.max_allowed_ram:
            oldest_view = self.previous_views.pop(0)
            oldest_view.unload()


    def get_view_class(self, view_name: str):
        """Return the View class with the given view_name."""
        return getattr(import_module(self.VIEW_MODULE), view_name)

    def logic(self):
        raise NotImplementedError

    def draw(self):
        raise NotImplementedError

    def on_quit(self):
        pass

    def quit(self):
        """Signal the game to quit."""
        self.running = False

    def _logic(self):
        self._check_quit()
        self.console.logic()
        self.current_view.logic()
        self.logic()

    def _draw(self):
        self.screen.fill((0, 0, 0))
        self.current_view.draw()
        self.draw()
        self.console.draw()

    def _quit(self):
        self.on_quit()
        pygame.quit()

    @staticmethod
    def get_memory_use():
        """Return the current memory usage of the game (RSS) in bytes."""
        return psutil.Process(os.getpid()).memory_info()[0]

    def initialise_screen(self, resolution=None, mode=None):
        """(Re)initialise the screen using the given resolution and mode."""
        if resolution is None:
            resolution = (self.width, self.height)
        if mode is None:
            mode = self.mode
        flags = pygame.HWSURFACE | pygame.DOUBLEBUF
        if mode == "fullscreen":
            flags |= pygame.FULLSCREEN
        elif mode == "windowed":
            os.environ["SDL_VIDEO_CENTERED"] = "1"
        elif mode == "borderless":
            os.environ["SDL_VIDEO_WINDOW_POS"] = "0,0"
            flags |= pygame.NOFRAME
        else:
            raise ValueError("Unknown mode for reinitialise_screen(): '{}'".format(mode))

        self.screen = pygame.display.set_mode(resolution, flags)
        self.width, self.height = resolution
        self.mode = mode

    def display(self, image, coordinates, area=None, special_flags=0):
        """Display the given image at the given coordinates.

        Coordinates and area should be givenas if they were for a 1920x1080 window.
        """
        x_scale = self.width/1920.0
        y_scale = self.height/1080.0
        coordinates = (coordinates[0]*x_scale, coordinates[1]*y_scale)
        if area is not None:
            area = (area[0]*x_scale, area[1]*y_scale,
                    area[2]*x_scale, area[3]*y_scale)
        self.screen.blit(image, coordinates, area, special_flags)

    def _inputs(self):
        self.input.reset()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit()
            elif event.type == pygame.MOUSEMOTION:
                self.input.mouse_pos = event.pos
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.input.buttondown(event)
            elif event.type == pygame.MOUSEBUTTONUP:
                self.input.buttonup(event.button)
            elif event.type == pygame.KEYDOWN:
                self.input.buttondown(event)
                TextInput.receive_single_characters(event)
            elif event.type == pygame.KEYUP:
                self.input.buttonup(event.key)
        TextInput.receive_multiple_characters()

    def _update(self):
        self.frame += 1
        pygame.display.flip()   # Updating the screen
        self.clock.tick(self.fps)    # [fps] times per second

    def runtime(self) -> float:
        """Return the amount of time the game has been running for in seconds."""
        return time.time() - self.start_time

    def _check_quit(self):
        if self.quit_condition():
            self.quit()

    def run(self):
        """Run the game."""
        self.running = True
        self.clock = pygame.time.Clock()
        self.start_time = time.time()

        while self.running:
            self._inputs()
            self._logic()
            self._draw()
            self._update()

        self._quit()
