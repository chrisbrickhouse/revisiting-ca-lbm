"""
This file is part of "Revisting California's low-back merger".

"Revisiting California's low-back merger" is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

Foobar is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with Foobar. If not, see <https://www.gnu.org/licenses/>.
"""
from manim import *

LOT = r'\textsc{lot}'
THOUGHT = r'\textsc{thought}'

LOT_COLOR = BLUE
THOUGHT_COLOR = ORANGE

FULL_CYCLE = [0., 2*PI, PI/16]


def make_coeff(n, ax):
    return Tex(str(n)).next_to(ax, UP)
