"""
This file is part of "Revisting California's low-back merger".

"Revisiting California's low-back merger" is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

Foobar is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with Foobar. If not, see <https://www.gnu.org/licenses/>.
"""
import csv
import math

from manim import *
from PlotScene import *
from common import *

class FormantTrackExample(PlotScene):
    def construct(self):
        self.make_axes()
        self.plot_tracks()

    def plot_tracks(self):
        def plot_loop(ax, d, color):
            def make_dot(point, col, r=0.04):
                return Dot(
                        point,
                        color = col,
                        radius = r
                    )
            p_f1 = self.get_canvas_point(ax,[d[1],d[2],0.])
            p_f2 = self.get_canvas_point(ax,[d[1],d[3],0.])
            return [make_dot(p_f1,color),make_dot(p_f2,color)]


        data = self.load_data()
        cot_data = [x for x in data if x[0] == 'cot']
        caught_data = [x for x in data if x[0] == 'caught']
        dots = []
        for d in cot_data:
            dots.extend(plot_loop(self.ax1,d,LOT_COLOR))
        for d in caught_data:
            dots.extend(plot_loop(self.ax2,d,THOUGHT_COLOR))
        self.add(*dots)



    def load_data(self):
        import csv
        ret = []
        with open('formant_track_data_clean.csv') as f:
            reader = csv.reader(f)
            for row in reader:
                token = str(row[1])
                index = float(row[3])
                f1 = float(row[4])
                f2 = float(row[5])
                ret.append([token,index,f1,f2])
        return ret

    def make_axes(self):
        self.ax1 = self.setup_axes(
                0., 
                10., 
                1., 
                0., 
                2000., 
                500.,
                yconf={
                    "decimal_number_config":{
                        "group_with_commas": False,
                        "num_decimal_places":0
                    }
                }
            ).scale(0.5)
        self.ax2 = self.setup_axes(
                0., 
                10., 
                1., 
                0., 
                2000., 
                500.,
                yconf={
                    "decimal_number_config":{
                        "group_with_commas": False,
                        "num_decimal_places":0
                    }
                }
            ).scale(0.5)
        self.plots = Group(self.ax1,self.ax2).arrange(buff=1)
        ax1_labels = self.label(self.ax1)
        ax2_labels = self.label(self.ax2)
        self.add(self.plots,ax1_labels,ax2_labels)

    def label(self, ax):
        x_label = ax.get_x_axis_label(
                Tex("Index").scale(0.5), 
                edge=DOWN, 
                direction=DOWN, 
                buff=0.3
            )
        y_label = ax.get_y_axis_label(
                Tex("Frequency (Hz)").scale(0.5).rotate(90 * DEGREES),
                edge=LEFT,
                direction=LEFT,
                buff=0.3
            )
        labels = VGroup(x_label, y_label)
        return labels

class DiscreteTrigTransform(PlotScene):
    def construct(self):
        self.make_axes()
        self.show_sine_addition()
        self.show_coeffs()
        self.coeffs_to_vector()
        self.wait(1)

    def coeffs_to_vector(self):
        # List of objects to remove from self.show_coeffs
        old_mobjects = [
                self.first_sine,
                self.second_sine,
                self.third_sine,
                self.live_sine
            ]
        # Tex formulae for GAM formant trajectories
        formula = MathTex("F_1=","-2","sin(x) + ","3","sin(2x) + ","0","sin(3x)")
        f2_formula = MathTex("F_2=","4","sin(x) + ","2","sin(2x)").next_to(formula,DOWN)
        # Add the F2 coeffs to self.coeffs
        self.coeffs.append(MathTex("4").move_to(f2_formula[1]))
        self.coeffs.append(MathTex("2").move_to(f2_formula[3]))
        # Column vectors for F1 and F2 coeffs
        f1_matrix = Matrix([[-2],[3],[0]]).next_to(formula,UP)
        f2_matrix = Matrix([[4],[2]]).next_to(f2_formula,DOWN)
        # Final vowel vector viz
        vowel_vec = Matrix([[-2],[3],[0],[4],[2]]).move_to(ORIGIN)
        vowel_label = MathTex("\hat{V}=").next_to(vowel_vec,LEFT)

        rm = AnimationGroup(*[FadeOut(x) for x in old_mobjects],*[FadeOut(x) for x in self.plots])
        coeff_anim = []
        for i in [0,1,2]:
            self.coeffs[i].generate_target()
            self.coeffs[i].animate.move_to(formula[i*2+1])
            coeff_anim.append(Transform(self.coeffs[i],formula[i*2+1]))
        formula_anim = []
        for i in range(len(formula)):
            if i in [1,3,5]:
                continue
            formula_anim.append(Write(formula[i]))
        self.wait(1)
        self.play(LaggedStart(rm,AnimationGroup(*coeff_anim,*formula_anim)))
        self.wait(0.5)
        self.play(FadeIn(f2_formula, shift=UP))
        self.wait(1)
        self.play(
                FadeIn(f1_matrix),
                formula[0].animate.next_to(f1_matrix,LEFT),
                self.coeffs[0].animate.move_to(f1_matrix[0][0]),
                self.coeffs[1].animate.move_to(f1_matrix[0][1]),
                self.coeffs[2].animate.move_to(f1_matrix[0][2]),
                FadeOut(formula[1:])
            )
        self.play(
                FadeIn(f2_matrix),
                f2_formula[0].animate.next_to(f2_matrix,LEFT),
                self.coeffs[3].animate.move_to(f2_matrix[0][0]),
                self.coeffs[4].animate.move_to(f2_matrix[0][1]),
                FadeOut(f2_formula[1:])
            )
        self.wait(1)
        self.play(
                *[FadeOut(x, shift=DOWN) for x in self.coeffs[0:3]],
                *[FadeOut(x, shift=UP) for x in self.coeffs[3:]],
                FadeOut(f1_matrix),
                FadeOut(f2_matrix),
                FadeIn(vowel_vec),
                FadeOut(formula[0],shift=DOWN),
                FadeOut(f2_formula[0],shift=DOWN),
                FadeIn(vowel_label)
            )

    def show_coeffs(self):
        c1 = make_coeff(1,self.ax1)
        c2 = make_coeff(1,self.ax2)
        c3 = make_coeff(1,self.ax3)
        self.play(Write(c1),Write(c2),Write(c3))
        self.wait(1)
        new_coeffs = self.change_coeffs(c1,c2,c3,2.0,3.0,5.0)
        self.wait(1)
        new_coeffs = self.change_coeffs(*new_coeffs,-2.0, 3., 5.)
        self.wait(1)
        new_coeffs = self.change_coeffs(*new_coeffs,-2.0, 3., 10.)
        self.wait(1)
        new_coeffs = self.change_coeffs(*new_coeffs,-2.0,3.,0.)
        self.wait(1)
        self.coeffs = new_coeffs

    def change_coeffs(self,c1,c2,c3,w1,w2,w3):
        alt1 = make_coeff(int(w1), self.ax1)
        alt2 = make_coeff(int(w2), self.ax2)
        alt3 = make_coeff(int(w3), self.ax3)

        new_sine = self.reweight(w1,w2,w3)

        self.play(
            FadeOut(c1,shift=UP),
            FadeOut(c2,shift=UP),
            FadeOut(c3,shift=UP),
            FadeIn(alt1,shift=UP),
            FadeIn(alt2,shift=UP),
            FadeIn(alt3,shift=UP),
            Transform(
                self.live_sine,
                new_sine,
                replace_mobject_with_target_in_scene=True
            )
        )
        self.live_sine = new_sine
        return [alt1,alt2,alt3]

    def reweight(self,a,b,c):
        s = sum([abs(x) for x in [a,b,c]])
        return self.com_ax.plot(
                lambda x: (math.sin(x*1.)*a + math.sin(x*2.)*b + math.sin(x*3.)*c)/s,
                x_range=FULL_CYCLE
            )

    def make_axes(self):
        self.com_ax = self.setup_axes(0., 2*PI, 1., -1., 1., 1.).scale(0.5)
        self.ax1 = self.setup_axes(0., 2*PI, 1., -1., 1., 1.).scale(0.3)
        self.ax2 = self.setup_axes(0., 2*PI, 1., -1., 1., 1.).scale(0.3)
        self.ax3 = self.setup_axes(0., 2*PI, 1., -1., 1., 1.).scale(0.3)

        self.lower_plots = Group(self.ax1,self.ax2,self.ax3).arrange(buff=1).next_to(self.com_ax,DOWN)
        self.plots = Group(self.com_ax,self.lower_plots).arrange([0.,-1.,0.],buff=1)
        self.add(self.plots)


    def show_sine_addition(self):
        self.first_sine = plot_sine(self.ax1, 1.)
        self.second_sine = plot_sine(self.ax2, 2.)
        self.third_sine = plot_sine(self.ax3, 3.)
        self.add(self.first_sine,self.second_sine,self.third_sine)

        com_ax_first_sine = self.com_ax.plot(
                lambda x: math.sin(x*1.),
                x_range=FULL_CYCLE
            )
        com_ax_second_sine = self.com_ax.plot(
                lambda x: math.sin(x*1.)/2 + math.sin(x*2.)/2,
                x_range=FULL_CYCLE
            )
        com_ax_third_sine = self.com_ax.plot(
                lambda x: math.sin(x*1.)/3 + math.sin(x*2.)/3 + math.sin(x*3.)/3,
                x_range=FULL_CYCLE
            )

        f1_move = self.copy_and_move(self.first_sine, com_ax_first_sine)
        self.play(Transform(
            f1_move,
            com_ax_first_sine,
            replace_mobject_with_target_in_scene=True
        ))

        f2_move = self.copy_and_move(self.second_sine, com_ax_second_sine)
        self.play(
                Transform(
                    f2_move,
                    com_ax_second_sine,
                    replace_mobject_with_target_in_scene=True
                ),
                Transform(
                    com_ax_first_sine,
                    com_ax_second_sine,
                    replace_mobject_with_target_in_scene=True
                )
            )

        f3_move = self.copy_and_move(self.third_sine, com_ax_third_sine)
        self.play(
                Transform(
                    f3_move,
                    com_ax_third_sine,
                    replace_mobject_with_target_in_scene=True
                ),
                Transform(
                    com_ax_second_sine,
                    com_ax_third_sine,
                    replace_mobject_with_target_in_scene=True
                )
            )
        self.live_sine = com_ax_third_sine


    def copy_and_move(self,curve,target):
        curve_copy = curve.copy()
        curve_copy.generate_target()
        curve_copy.animate.move_to(target)
        return curve_copy

    def sine(self,x,f=1.):
        return math.sin(x*f)


class PlotDuration(PlotScene):
    B_BIRTH = -0.0003022
    B_TOKEN = 0.02609
    B_INTERACTION = 0.0003105
    INTERCEPT = 0.2289
    X_OFFSET = 1968.038
    def construct(self):
        ax = self.setup_axes( 1920., 2000., 10.,0.06, 0.4, 0.03,)
        labels = self.label(ax)
        legend = self.make_legend().next_to(ax,RIGHT*0.1).scale(0.8)
        title = Title(
            r"Token duration by birth year",
            include_underline=False,
            font_size=40,
        )
        self.add(ax, labels,title,legend)

        dots = []
        for coord, token in self.load_data():
            p = self.get_canvas_point(ax,coord)
            point = Dot(
                    p,color=self.get_color(token),
                    fill_opacity=0.5,
                    radius=0.04
                )
            dots.append(point)
        # Sorting by x coord means they animate in left-to-right
        dots.sort(key = lambda x: x.get_x())
        dot_anim = [FadeIn(d, shift=DOWN) for d in dots]
        plot = LaggedStart(*dot_anim, lag_ratio=0.001)

        thought_line = ax.plot(
                lambda x: self.lm(x,'caught'), 
                x_range=[1920,2000,1]
            ).set_color(THOUGHT_COLOR)
        lot_line = ax.plot(
                lambda x: self.lm(x, 'cot'), 
                x_range=[1920,2000,1]
            ).set_color(LOT_COLOR)

        self.play(plot)
        self.play(Create(thought_line), Create(lot_line))
        self.wait(2)

    def lm(self, x, token):
        if token == 'cot':
            y = 1
        else:
            y = 0
        betas = [
                self.B_BIRTH,
                self.B_TOKEN,
                self.B_INTERACTION
            ]
        return self.linear_model(
                betas, 
                x - self.X_OFFSET,
                y, 
                self.INTERCEPT
            )

    def label(self, ax):
        x_label = ax.get_x_axis_label(
                Tex("Birth year").scale(1), 
                edge=DOWN, 
                direction=DOWN, 
                buff=3
            )
        y_label = ax.get_y_axis_label(
                Tex("Duration (s)").scale(1).rotate(90 * DEGREES),
                edge=LEFT,
                direction=LEFT,
                buff=0.5
            )
        labels = VGroup(x_label, y_label)
        return labels

    def load_data(self):
        import csv
        out = []
        with open('duration_plotting_data_clean.csv') as f:
            reader = csv.reader(f)
            next(reader)
            for row in reader:
                try:
                    birthyear = float(row[19])
                except ValueError:
                    continue
                token = str(row[4])
                dur = float(row[6])
                out.append(([birthyear,dur,0.],token))
        return out
