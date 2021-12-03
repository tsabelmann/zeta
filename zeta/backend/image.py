""""""

import cairo
import mpmath
import numpy as np
import pathlib
import typing


class CriticalZeta:
    def __init__(self, file_path, background: int, foreground: int, width: int, height: int,
                 min_t: float = 0, max_t: float = 50):
        self._file_path = file_path
        self._background = background
        self._foreground = foreground
        self._width = width
        self._height = height
        self._min_t = min_t
        self._max_t = max_t

    @property
    def file_path(self) -> pathlib.Path:
        return self._file_path

    @property
    def width(self) -> int:
        return self._width

    @property
    def height(self) -> int:
        return self._height

    @property
    def background(self) -> int:
        return self._background

    def bg_rgb(self) -> typing.Tuple[int, int, int]:
        bg_r = (self.background >> 16) & 0xFF
        bg_g = (self.background >> 8) & 0xFF
        bg_b = (self.background >> 0) & 0xFF
        return bg_r, bg_g, bg_b

    @property
    def foreground(self) -> int:
        return self._foreground

    def fg_rgb(self) -> typing.Tuple[int, int, int]:
        fg_r = (self.foreground >> 16) & 0xFF
        fg_g = (self.foreground >> 8) & 0xFF
        fg_b = (self.foreground >> 0) & 0xFF
        return fg_r, fg_g, fg_b

    @property
    def min_t(self) -> float:
        return self._min_t

    @property
    def max_t(self) -> float:
        return self._max_t

    def generate(self):
        surface = cairo.SVGSurface(self.file_path, self.width, self.height)
        context = cairo.Context(surface)

        width = self.width / 120
        height = self.height / 120

        context.scale(120, 120)
        context.translate(width / 2, height / 2)

        bg_r, bg_g, bg_b = self.bg_rgb()
        context.set_source_rgb(bg_r, bg_g, bg_b)
        context.paint()

        t = np.arange(0, 50, 0.01)
        complex_map = map(lambda x: 0.5 + 1j * x, t)
        zeta_map = map(mpmath.zeta, complex_map)

        # Color Yellow
        # context.set_source_rgb(252 / 255, 254 / 255, 91 / 255)
        # Color ECAP Blue
        # context.set_source_rgb(0, 159 / 255, 227 / 255)

        # set foreground color
        fg_r, fg_g, fg_b = self.fg_rgb()
        context.set_source_rgb(fg_r / 255, fg_g / 255, fg_b / 255)

        # draw critical line
        context.set_line_width(0.03)
        for i, comp in enumerate(zeta_map):
            re = comp.real
            img = -comp.imag
            if i == 0:
                context.move_to(re, img)
            else:
                context.line_to(re, img)
        context.stroke()

