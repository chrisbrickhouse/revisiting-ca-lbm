"""
This file is part of "Revisting California's low-back merger".

"Revisiting California's low-back merger" is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

Foobar is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with Foobar. If not, see <https://www.gnu.org/licenses/>.
"""
import csv
import math

from manim import *
from common import *


def plot_sine(ax,f):
    r = ax.plot(
            lambda x: math.sin(x*f),
            x_range=FULL_CYCLE
        )
    return r

class PlotScene(Scene):
    def construct(self):
        pass

    def setup_axes(self, xmin, xmax, xstep, ymin, ymax, ystep,yconf={}):
        ax = Axes(
            x_range=[xmin, xmax, xstep],
            y_range=[ymin, ymax, ystep],
            x_length=9,
            y_length=5,
            tips=False,
            axis_config={"include_numbers": True},
            x_axis_config={
                "decimal_number_config":{
                    "group_with_commas": False,
                    "num_decimal_places":0
                }
            },
            y_axis_config=yconf
        )
        return ax

    def linear_model(self,beta, x, y, intercept):
        z = beta[0] * x + beta[1] * y + beta[2] * x * y + intercept
        return z

    def get_canvas_point(self, ax, coord):
        return ax.coords_to_point(*coord)

    def make_legend(self):
        lot_square = Square(
                side_length=0.5,
                color = LOT_COLOR
            ).set_fill(
                    LOT_COLOR,
                    opacity=1
                )
        thought_square = Square(
                side_length=0.5,
                color = THOUGHT_COLOR
            ).set_fill(
                    THOUGHT_COLOR,
                    opacity=1
                ).next_to(
                        lot_square, 
                        DOWN
                    )
        lot_label = Tex("cot").next_to(lot_square, RIGHT)
        thought_label = Tex("caught").next_to(thought_square, RIGHT)

        lot_group = Group(lot_square, lot_label)
        thought_group = Group(thought_square, thought_label)
        legend_group = Group(lot_group, thought_group)
        return legend_group

    def get_color(self, token):
        if token == 'cot':
            return BLUE
        else:
            return ORANGE
