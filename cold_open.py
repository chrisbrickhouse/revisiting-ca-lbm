"""
This file is part of "Revisting California's low-back merger".

"Revisiting California's low-back merger" is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

Foobar is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with Foobar. If not, see <https://www.gnu.org/licenses/>.
"""
from manim import *

class CircleIntro(Scene):
    def construct(self):
        c_lot = Circle(radius=2).set_fill(YELLOW, opacity=0.5)
        c_thought = Circle(radius=2).set_fill(BLUE, opacity=0.5)

        circs = Group(c_lot, c_thought).arrange(buff=2)

        c_lot_og_center = c_lot.get_center()
        c_thought_og_center = c_thought.get_center()

        t_lot = Tex(LOT).next_to(c_lot, DOWN)
        t_thought = Tex(THOUGHT).next_to(c_thought,DOWN)

        self.play(Create(c_lot),Create(c_thought))

        self.wait(1)

        self.play(Write(t_lot), Write(t_thought))

        self.play(Wait(run_time=3))

        self.play(FadeOut(t_lot), FadeOut(t_thought))

        self.play(c_lot.animate.move_to(ORIGIN), c_thought.animate.move_to(ORIGIN))

        self.play(Wait(run_time=3))
        c_lot.generate_target()
        c_lot.target.shift([-1.,0.,0.]).stretch_to_fit_width(0)
        c_thought.generate_target()
        c_thought.target.shift([1.,0.,0.]).stretch_to_fit_width(0)

        self.play(MoveToTarget(c_lot),MoveToTarget(c_thought))
        self.wait(1)
        self.play(FadeOut(c_lot),FadeOut(c_thought))

        self.wait(0.5)


class TitleSlide(Scene):
    def construct(self):
        title = Tex(r"Revisting California's low-back merger:", font_size=64)
        subtitle = Tex(
                r'A lot of thoughts about \textsc{lot} and \textsc{thought}',
                font_size=48
            ).next_to(title, DOWN)
        author = Tex(r"Christian Brickhouse",font_size=32).next_to(subtitle, DOWN+[0,-2.,0])
        email = Tex(r"\texttt{brickhouse@stanford.edu}",font_size=32).next_to(author, DOWN)
        date = Tex(r"2 Sept 2022",font_size=32).next_to(email, DOWN)


        self.play(Write(title))
        self.play(Write(subtitle))
        #self.play(Wait(run_time=1))
        self.play(Write(author), Write(email), Write(date))
        #self.play(Wait(run_time=10))
        #self.play(FadeOut(title, subtitle, author, email, date))
