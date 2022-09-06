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

class DataCollection(MovingCameraScene):
    def construct(self):
        self.make_ca_map()

    def make_demo_table(self,site):
        if site == 'BAK':
            long_site = 'Bakersfield'
            dat = [
                    [98,57,21,3,17],
                    [107,61,23,3,20]
                ]
        elif site == 'SAC':
            long_site = 'Sacramento'
            dat = [
                    [131,87,10,9,25],
                    [136,89,10,11,26],
                ]
        elif site == 'SAL':
            long_site = 'Salinas'
            dat = [
                    [42,6,31,3,2],
                    [54,6,42,4,2]
                ]
        elif site == 'HUM':
            long_site = 'Humboldt'
            dat = [
                    [95,73,4,9,9],
                    [95,73,4,9,9]
                ]
        elif site == 'RDL':
            long_site = 'Redlands'
            dat = [
                    [70,46,11,7,6],
                    [79,51,13,9,6]
                ]
        else:
            raise ValueError
        labs = [
                Text("Dynamics"),
                Text("Duration"),
                Text("Total"),
                Text("White"),
                Text("Hispanic"),
                Text("Multiracial"),
                Text("Asian\nBlack\nIndigenous")
            ]
        labs = [x.scale(0.5) for x in labs]

        tab = MathTable(
                dat,
                row_labels = [labs[0],labs[1]],
                col_labels = [labs[2],labs[3],labs[4],labs[5],labs[6]],
                top_left_entry = Text(long_site).scale(0.5),
                include_outer_lines=True
            ).scale(0.5)
        return tab


    def make_ca_map(self):
        def make_site(coords,study):
            return Dot(coords,color=RED,radius=0.15)

        def play_dot(d):
            return FadeIn(d,shift=DOWN)

        ca_map = SVGMobject(
                'California_contour.svg',
                stroke_color=GREY,
                stroke_width=1,
                height=6
            )
        map_og_pos = ca_map.get_center()
        bak_dot = make_site([0,-1.3,0],'Brickhouse')
        bak_lab = Tex("Bakersfield").next_to(bak_dot,RIGHT)
        sal_dot = make_site([-1.3,-0.5,0],'Brickhouse')
        sal_lab = Tex("Salinas").next_to(sal_dot,LEFT)
        sac_dot = make_site([-1.1,0.8,0],'Brickhouse')
        sac_lab = Tex("Sacramento").next_to(sac_dot,RIGHT)
        hum_dot = make_site([-2.3,2.2,0],'Brickhouse')
        hum_lab = Tex("Humboldt").next_to(hum_dot,LEFT)
        rdl_dot = make_site([1,-2.1,0],'Brickhouse')
        rdl_lab = Tex("Redlands").next_to(rdl_dot,RIGHT)
        dots = VGroup(
                bak_dot,
                sal_dot,
                sac_dot,
                hum_dot,
                rdl_dot,
            )
        self.ca_map_group = VGroup(ca_map,dots)
        self.add(self.ca_map_group,bak_lab,sal_lab,sac_lab,hum_lab,rdl_lab)


class Results(Scene):
    def construct(self):
        pass

class FormantTrackExample(PlotScene):
    def construct(self):
        dtt = DiscreteTrigTransform()
        dtt.construct()
        self.make_axes()
        self.plot_tracks()

        self.add(dtt.vowel_label, dtt.vowel_vec)
        dtt.vowel_label.add_updater(
                lambda mobject: mobject.next_to(dtt.vowel_vec,LEFT)
            )

        v2_vec = Matrix([[3],[7],[5],[1],[9]]).next_to(
            self.plots[1], 
            DOWN,
            buff=0.5
        ).scale(0.7)
        v2_label = MathTex("\hat{V}_{T}=").next_to(v2_vec,LEFT)
        dot_anim = LaggedStart(
                *[FadeIn(x,shift=DOWN) for x in self.dots]
            )
        self.play(
                dtt.vowel_vec.animate.next_to(
                    self.plots[0], 
                    DOWN,
                    buff=0.5
                ).scale(0.7),
                FadeIn(v2_vec),
                FadeIn(v2_label),
                FadeIn(self.plots),
                dot_anim
            )
        self.wait(30)

    def add_dots(self):
        dot_anim = LaggedStart(
                *[FadeIn(x,shift=DOWN) for x in self.dots]
            )
        return dot_anim

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
        self.dots = dots



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
            ).scale(0.5).align_on_border(UL)
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
            ).scale(0.5).align_on_border(UR)
        ax1_labels = self.label(self.ax1)
        ax2_labels = self.label(self.ax2)
        self.plots = VGroup(self.ax1,self.ax2, ax1_labels, ax2_labels)

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


class AvoidedMerger(ThreeDScene):
    def construct(self):
        ax = ThreeDAxes(
                x_range=[0,7,0.5],
                y_range=[0,5,0.5],
                z_range=[0,3,0.5],
                x_length=7,
                y_length=5,
                z_length=3
            )
        lot_line = Line3D(
                start = [-3,0,1],
                end = [3,-1.5,1],
                stroke_color=LOT_COLOR
            )
        thought_line = Line3D(
                start = [-3,1,1.5],
                end = [3,-1.5,3],
                stroke_color=THOUGHT_COLOR
            )
        z_lab = ax.get_z_axis_label(Tex("Duration"))
        x_lab = ax.get_x_axis_label(Tex("Birth year"))
        y_lab = ax.get_y_axis_label(Tex("Formant measure"))
        self.set_camera_orientation(0,-PI/2)
        self.add(ax,z_lab,y_lab,x_lab,lot_line,thought_line)
        self.wait(1)
        self.move_camera(PI/2,-PI/2,frame_center=[0,0,1.5],added_anims=[x_lab.animate.rotate(PI/2,[1,0,0]),ax.get_x_axis().get_tip().animate.rotate(PI/2,[1,0,0])])
        self.wait(1)

class MergerReview(Scene):
    def construct(self):
        opening_q = Tex("What"," is a ","merger","?")
        self.play(Write(opening_q))
        self.wait(1)
        self.play(FadeOut(opening_q))
        bloch_quote = Tex("\\textit{Contrast between sounds can be defined, I think,\\\\",
            "on the basis of distribution alone without\\\\",
            "the customary appeal to meaning.}\\\\---Bloch (1953)")
        martinet_quote = Tex("\\textit{the unit chosen is kept distinct from the ones that\\\\",
            "could have been used, in the very same context,\\\\ in order to make a different message.}\\\\",
                "---Martinet (1962)")
        self.play(Write(bloch_quote))
        self.wait(1)
        self.play(FadeOut(bloch_quote))
        self.play(Write(martinet_quote))
        self.wait(1)
        self.play(FadeOut(martinet_quote))
        ineq = Tex("contrastive $\\not =$ distinctive",)
        kip = Tex("See Kiparsky 2016 for a review",font_size=32).to_edge(DOWN)
        self.play(Write(ineq))
        self.wait(1)
        self.remove(kip)
        self.play(ineq.animate.to_edge(UP))
        merge_blist = BulletedList(
                "Speakers with overlapping vowel productions can still\\\\ distinguish the 'merged' vowels (Hay et al. 2013, i.a.)",
                "Speakers with distinct vowel productions may be unable \\\\to distinguish the 'distinct' vowel (Nunberg 1980, i.a.)"
            )
        self.play(
                LaggedStart(
                    *[Write(x) for x in merge_blist],
                    lag_ratio=1
                )
            )
        self.wait(1)
        self.play(*[FadeOut(x) for x in merge_blist],FadeOut(ineq))
        self.play(FadeIn(opening_q),shift=RIGHT)
        second_q = Tex("How"," is a ","merger"," identified","?")
        self.wait(1)
        self.play(FadeOut(opening_q,shift=DOWN),FadeIn(second_q,shift=DOWN))
        self.wait(1)
        self.play(FadeOut(second_q,shift=UP))
        m_percept = Tex("\\textsc{Merger in Perception}")
        m_product = Tex("\\textsc{Merger in Production}")
        m_per_bl = BulletedList(
                "non-distinctive",
                "independent acoustics"
            )
        m_prod_bl = BulletedList(
                "non-contrastive",
                "similar acoustics"
            )
        bl_group = Group(m_per_bl,m_prod_bl).arrange(buff=1)
        m_percept.next_to(m_per_bl,UP)
        m_product.next_to(m_prod_bl,UP)
        m_per_group = Group(m_per_bl,m_percept)
        m_prod_group = Group(m_prod_bl,m_product)
        m_group = Group(m_per_group,m_prod_group).arrange(buff=0.5)
        self.play(Write(m_percept),Write(m_product))
        self.wait(1)
        self.play(
                Write(m_per_bl[0]),
                Write(m_prod_bl[0])
            )
        self.wait(0.5)
        self.play(
                Write(m_per_bl[1]),
                Write(m_prod_bl[1])
            )
        self.wait(1)
        self.play(FadeOut(m_per_group),m_prod_group.animate.move_to(ORIGIN))
        self.wait(1)
        self.play(FadeOut(m_product),FadeOut(m_prod_bl[0]),FadeOut(m_prod_bl[1]))
        self.wait(0.5)

class CaliforniaMerger(Scene):
    def construct(self):
        self.CVS_polygon()
        self.california_studies()
        self.wait(8)

    def CVS_polygon(self):
        self.polygon = Polygon([4,3,0],[-4,3,0],[-1,-3,0],[4,-3,0],color=WHITE)
        self.play(FadeIn(self.polygon))
        self.LOT = Text('ɑ',color=BLUE).move_to([1.8,-2.5,0])
        self.THOUGHT = Text('ɔ',color=ORANGE).move_to([3.5,-1,0])
        merged_dot = Dot([3.1,-2.1,0],radius=0.5)
        arrow1 = Arrow(start=[2,-2.5,0],end=[3.1,-2.1,0],buff=0,max_stroke_width_to_length_ratio=3)
        arrow2 = Arrow(start=[3.5,-1.3,0],end=[3.1,-2.1,0],buff=0,max_stroke_width_to_length_ratio=3)
        bit = Text('ɪ').move_to([-2,2,0])
        bet = Text('ɛ').move_to([-1.5,0,0])
        bat = Text('æ').move_to([-1,-2,0])
        boot = Text('u').move_to([3.5,2.5,0])
        boat = Text('o').move_to([3.5,.5,0])
        book = Text('ʊ').move_to([2.5,1.5,0])
        vowels = VGroup(bit,bet,bat,boat,boot,book)
        arrow3 = Arrow(bit,bet)
        arrow4 = Arrow(bet,bat)
        arrow5 = Arrow(bat,[0.8,-2.5,0])
        arrow6 = Arrow(boot,[1.5,2.5,0])
        arrow7 = Arrow(boat,[1.5,0.5,0])
        arrow8 = Arrow(book,[0.5,1.5,0])
        arrows = VGroup(arrow3,arrow4,arrow5,arrow6,arrow7,arrow8)
        self.play(
                AnimationGroup(
                    *[FadeIn(x) for x in [self.LOT,self.THOUGHT]]
                )
            )
        self.wait(2)
        self.play(Create(arrow1),Create(arrow2))
        self.wait(20)
        self.play(
                AnimationGroup(*[FadeIn(x) for x in vowels])
            )
        self.wait(5)
        self.play(
                *[FadeIn(x) for x in arrows]
            )
        self.wait(27)
        # Move everything back to where it started
        self.vowels_arrows_polygon = VGroup(
                self.polygon,
                self.LOT,
                self.THOUGHT,
                arrow1,
                arrow2,
                vowels,
                arrows
            )
        self.play(
                self.vowels_arrows_polygon.animate.to_edge(RIGHT).scale(0.5)
            )

    def california_studies(self):
        COLORS = {
                'DeCamp': BLUE,
                'Hinton': BLUE,
                'Moonwomon': BLUE,
                'Hall-Lew': BLUE,
                'Hagiwara': BLUE,
                'Kennedy': BLUE,
                'Podesva': BLUE,
                'DOnofrio': YELLOW_B,
                'Brickhouse': RED,
                'OTHER': BLUE
            }
        def make_site(coords,study):
            return Dot(coords,color=COLORS[study],radius=0.15)

        def play_dot(d):
            return FadeIn(d,shift=DOWN)

        ca_map = SVGMobject(
                'California_contour.svg',
                stroke_color=WHITE,
                stroke_width=1,
                height=6
            )
        map_og_pos = ca_map.get_center()
        sf_dot1 = make_site([-1.65,0.3,0],'DeCamp')
        sf_dot2 = sf_dot1.copy()#make_site([-1.64,0.4,0],'Hinton')
        sf_dot3 = sf_dot1.copy()#make_site([-1.63,0.5,0],'Moonwomon')
        sf_dot4 = sf_dot1.copy()#make_site([-1.62,0.6,0],'Hall-Lew')
        bak_dot1 = make_site([0,-1.3,0],'DOnofrio')
        bak_dot2 = make_site([0,-1.3,0],'Brickhouse')
        mer_dot = make_site([-0.8,0.1,0],'DOnofrio')
        red_dot1 = make_site([-1.6,2.2,0],'Podesva')
        red_dot2 = make_site([-1.6,2.2,0],'DOnofrio')
        la_dot = make_site([0.4,-2.1,0],'Hagiwara')
        sb_dot = make_site([-0.3,-1.8,0],'Kennedy')
        sal_dot = make_site([-1.3,-0.5,0],'Brickhouse')
        sac_dot = make_site([-1.1,0.8,0],'Brickhouse')
        hum_dot = make_site([-2.3,2.2,0],'Brickhouse')
        rdl_dot = make_site([1,-2.1,0],'Brickhouse')
        dots = VGroup(
                sf_dot1,
                sf_dot2,
                sf_dot3,
                sf_dot4,
                bak_dot1,
                bak_dot2,
                mer_dot,
                red_dot1,
                red_dot2,
                la_dot,
                sb_dot,
                sal_dot,
                sac_dot,
                hum_dot,
                rdl_dot,
            )
        self.ca_map_group = VGroup(ca_map,dots)
        ca_map.to_edge(LEFT)

        self.play(Create(ca_map,run_time=1.5))
        self.wait(3)
        self.play(
                ca_map.animate.move_to(map_og_pos),
                FadeOut(self.vowels_arrows_polygon)
            )
        self.wait(1)
        study_list_temp = [ 
                "DeCamp (1953)",
                "Hinton, et al. (1987)",
                "Moonwomon (1991)",
                "Hagiwara (1997)",
                "Hall-Lew (2009)",
                "Kennedy and Grama (2012)",
                "Podesva, et al. (2015)",
                "D'Onofrio, et al. (2016)",
                "This study"
            ]
        study_list = []
        for study in study_list_temp:
            study_list.append(
                    Tex(study).move_to(ORIGIN).next_to(ORIGIN,RIGHT)
                )
        study_list[1].set_color(COLORS['Hinton']).next_to(sf_dot1,DL)
        study_list[0].set_color(COLORS['DeCamp']).next_to(study_list[1],UP,aligned_edge=LEFT)
        study_list[2].set_color(COLORS['Moonwomon']).next_to(study_list[1],DOWN,aligned_edge=LEFT)
        study_list[3].set_color(COLORS['Hagiwara']).next_to(la_dot,RIGHT)
        study_list[4].set_color(COLORS['Hall-Lew']).next_to(study_list[2],DOWN,aligned_edge=LEFT)
        study_list[5].set_color(COLORS['Kennedy']).next_to(sb_dot,LEFT,buff=0.1)
        study_list[7].set_color(COLORS['DOnofrio']).next_to(red_dot1,RIGHT)
        study_list[6].set_color(COLORS['Podesva']).next_to(study_list[7],UP,aligned_edge=LEFT)
        study_list[8].set_color(COLORS['Brickhouse']).next_to(hum_dot,LEFT)
        self.play(
                Write(study_list[0]),
                Write(study_list[1]),
                FadeIn(sf_dot1,shift=DOWN)
            )
        self.wait(16)
        self.play(
                *[FadeOut(x,shift=UP) for x in study_list[0:2]],
                FadeIn(study_list[2].next_to(sf_dot1,LEFT),shift=UP)
            )
        self.wait(6)
        self.play(
                FadeOut(study_list[2],shift=UP),
                Write(study_list[3]),
                FadeIn(la_dot,shift=DOWN)
            )
        self.wait(3.5)
        self.play(
                FadeOut(study_list[3],shift=UP),
                Write(study_list[4].next_to(sf_dot1,LEFT))
            )
        self.wait(9)
        self.play(
                FadeOut(study_list[4],shift=UP),
                Write(study_list[5]),
                FadeIn(sb_dot,shift=DOWN)
            )
        self.wait(16)
        self.play(
                FadeOut(study_list[5],shift=UP),
                Write(study_list[6].next_to(red_dot1,RIGHT)),
                FadeIn(red_dot1,shift=DOWN)
            )
        self.wait(10)
        self.play(
                FadeOut(study_list[6],shift=UP),
                Write(study_list[7].next_to(mer_dot,RIGHT)),
                *[FadeIn(x,shift=DOWN) for x in [red_dot2,mer_dot,bak_dot1]]
            )
        self.wait(18)
        self.play(
                FadeOut(study_list[7],shift=UP),
                *[x.animate.set_color(COLORS['OTHER']) for x in [red_dot2,mer_dot,bak_dot1]],
                Write(study_list[8]),
                *[FadeIn(x,shift=DOWN) for x in [sal_dot,sac_dot,hum_dot,rdl_dot,bak_dot2]]
            )
        self.wait(12)
        self.play(
                FadeOut(study_list[8],shift=UP),
                *[x.animate.set_color(COLORS['OTHER']) for x in [sal_dot,sac_dot,hum_dot,rdl_dot,bak_dot2]],
            )
        self.wait(21)
        self.play(
                self.ca_map_group.animate.to_edge(LEFT),
            )
        percept_bl = BulletedList(
                "Evidence of vowel overlap since early 90s",
                "Perceptual evidence much weaker",
                "11 of 22 CA speakers could distinguish\\\\(Labov, Ash, Boberg 2006)",
                "What acoustic dimension are we missing?"
            ).next_to(self.ca_map_group,RIGHT).scale(0.8)
        self.wait(4)
        self.play(LaggedStart(*[Write(x) for x in percept_bl],lag_ratio=4))


class VowelWhatNow(FormantTrackExample):
    def construct(self):
        opening_q = Tex("What is a vowel?")
        ax = self.setup_axes( 0., 20., 1.,-5., 5., 1.,)
        self.play(FadeIn(opening_q))
        self.wait(7)
        vowel_wave = ax.plot(lambda x: self.waveform(x),x_range=[0,20,.01])
        self.play(FadeOut(opening_q,shift=RIGHT),Create(vowel_wave))
        self.wait(6)
        dt_arrow = Arrow(start=ax.c2p(*[5,-2,0]),end=ax.c2p(*[15,-2,0]))
        dt_text = Tex("Time dependent").next_to(dt_arrow,DOWN)
        dy_arrow = CurvedArrow(ax.c2p(*[5,1,0]),ax.c2p(*[15,1,0]),radius=-5)
        dy_text = Tex("Changes over time").next_to(dy_arrow,UP)
        arrow_wave_text = VGroup(vowel_wave,dt_arrow,dt_text,dy_arrow,dy_text)
        self.play(
                LaggedStart(
                    *[
                        Create(dt_arrow),
                        Create(dt_text),
                        Wait(1),
                        Create(dy_arrow),
                        Create(dy_text),
                    ],
                    lag_ratio=1
                )
            )
        self.wait(1)
        self.play(AnimationGroup(*[FadeOut(x) for x in arrow_wave_text]))
        self.wait(3)
        self.make_axes()
        self.plot_tracks()
        self.play(FadeIn(self.plots),self.add_dots())
        bl_comp = BulletedList(
                "Point measurements",
                "Euclidean distances (Becker 2019, i.a.)",
                "Pillai scores (Hay, Warren, and Drager 2006)",
                "Spectral overlap assessment metric (Wassink 2006)",
                "Discrete Cosine Transform (Kleber, Harrington, and Reubold 2011)",
                buff=0.4
            ).scale(0.7).to_edge(DOWN)
        self.wait(3)
        self.play(Write(bl_comp[0]))
        self.wait(6)
        self.play(Write(bl_comp[1]))
        self.wait(5)
        self.play(Write(bl_comp[2]))
        self.wait(0.5)
        self.play(Write(bl_comp[3]))
        self.wait(11)
        self.play(Write(bl_comp[4]))
        self.wait(19)


    def waveform(self,x,sd=10.):
        x = x - 10.
        out = np.sin(10. * x) * math.exp(-x**2/20.)
        return out


class EuclideanDistanceDemo(Scene):
    def construct(self):
        v1 = Matrix([['a'],['b']])
        v2 = Matrix([['c'],['d']])
        vecs = Group(v1,v2).arrange()
        self.wait(9)
        self.play(FadeIn(vecs))
        self.wait(7)

        v3 = MathTex('(a,b)').move_to(v1)
        v4 = MathTex('(c,d)').move_to(v2)
        vecs = Group(v3,v4).arrange()
        self.play(
                FadeOut(v1,shift=UP),
                FadeIn(v3,shift=UP),
                FadeOut(v2,shift=UP),
                FadeIn(v4,shift=UP)
            )
        self.wait(8)

        dot = Dot([-2, -1, 0]).set_color(LOT_COLOR).set_z_index(1)
        dot2 = Dot([2, 2, 0]).set_color(THOUGHT_COLOR).set_z_index(1)
        line = Line(dot.get_center(), dot2.get_center())
        self.play(
                Create(dot),
                Create(dot2),
                v3.animate.next_to(dot,LEFT),
                v4.animate.next_to(dot2,RIGHT,buff=0.5)
            )
        self.wait(5)
        self.play(Create(line))
        self.wait(3)
        v3.add_updater(
                lambda mobj: mobj.next_to(dot,LEFT)
            )
        v4.add_updater(
                lambda mobj: mobj.next_to(dot2,RIGHT,buff=0.5)
            )
        invisible_dot = Dot([2,-1,0], fill_opacity=0)
        w = DashedLine(dot.get_center(),[2,-1,0])
        h = DashedLine(dot2.get_center(),[2,-1,0])
        self.play(Create(h),Create(w))
        v5 = MathTex('(c,b)').next_to([2,-1,0],DR)
        self.play(FadeIn(v5))
        self.wait(0.5)
        b1 = Brace(w)
        b1_lab = b1.get_tex('c-a')
        b2 = BraceBetweenPoints(
                dot2.get_center(),
                [2,-1,0],
                direction=RIGHT
            )
        b2_lab = b2.get_tex('d-b').add_updater(
                lambda mobj: mobj.next_to(b2.get_tip(),RIGHT)
            )

        self.play(
                FadeIn(b1),
                FadeIn(b2),
                Write(b1_lab),
                Write(b2_lab)
            )
        self.wait(1)
        triangle = VGroup(line,h,w,dot,dot2,invisible_dot)
        braces = VGroup(b1,b2)
        tri_and_brace = VGroup(triangle,braces)
        self.play(
                tri_and_brace.animate.rotate(-36.9*DEGREES),
                v5.animate.next_to([0.85,-1.8,0],DOWN,buff=0.5),
                b1_lab.animate.next_to([-1,-1,0],LEFT)
            )
        self.wait(1)
        top_brace = BraceBetweenPoints(dot.get_center(),dot2.get_center(),direction=UP)
        hyp_eq = top_brace.get_tex(
                "dist = \sqrt{(",
                "c - a",
                ")^2 + (",
                "d - b",
                ")^2}"
            )
        self.play(FadeIn(top_brace),Write(hyp_eq))
        self.wait(2)
        v3.clear_updaters()
        v4.clear_updaters()
        b2_lab.clear_updaters()
        braces.add(top_brace)
        labels = VGroup(v3,v4,v5,b1_lab,b2_lab)
        to_rm = VGroup(triangle,braces,labels)
        vecs = VGroup(v1,v2)
        self.play(
                LaggedStart(
                    FadeOut(to_rm, shift=RIGHT),
                    FadeIn(vecs,shift=RIGHT),
                    lag_ratio=3
                )
            )
        self.wait(3)
        v1_hat = MathTex("\hat{v}").move_to(v1)
        v2_hat = MathTex("\hat{u}").move_to(v2)
        self.play(ReplacementTransform(v1,v1_hat),ReplacementTransform(v2,v2_hat))
        self.wait(6)
        eq1 = MathTex("(","\hat{u}","-","\hat{v}",")^2")
        eq2 = MathTex(
                "dist = \sqrt{(",
                "\hat{u}_1 - \hat{v}_1",
                ")^2 + (",
                "\hat{u}_2 - \hat{v}_2",
                ")^2}"
            ).move_to(hyp_eq)
        v_hats = VGroup(v1_hat,v2_hat)
        self.play(Swap(*v_hats))
        self.play(TransformMatchingTex(v_hats,eq1),TransformMatchingTex(hyp_eq,eq2))
        self.wait(11)
        eq3 = MathTex(
                "dist = \sqrt{\sum_{i=1}^{k}",
                "(","\hat{u}","_i","-","\hat{v}","_i",")^2","}"
            ).move_to(eq1)
        eq4 = MathTex(
                "dist = \sqrt{(",
                "\hat{u}_1 - \hat{v}_1",
                ")^2 + (",
                "\hat{u}_2 - \hat{v}_2",
                ")^2 + ... + (\hat{u}_k - \hat{v}_k)^2}"
            ).move_to(hyp_eq)
        self.play(
                TransformMatchingTex(eq1,eq3),
                TransformMatchingTex(eq2,eq4)
            )
        self.wait(7)
        self.play(FadeOut(eq4,shift=UP),eq3.animate.move_to(ORIGIN))
        self.wait(3)
        self.euclidean_dist_eq = eq3


class DiscreteTrigTransform(PlotScene):
    def construct(self):
        self.make_axes()
        self.show_sine_addition()
        self.show_coeffs()
        self.coeffs_to_vector()
        self.wait(10)

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
        vowel_label = MathTex("\hat{V}_{L}=").next_to(vowel_vec,LEFT)

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
        self.wait(3)
        self.play(FadeIn(f2_formula, shift=UP))
        self.wait(3)
        self.play(
                FadeIn(f1_matrix),
                formula[0].animate.next_to(f1_matrix,LEFT),
                self.coeffs[0].animate.move_to(f1_matrix[0][0]),
                self.coeffs[1].animate.move_to(f1_matrix[0][1]),
                self.coeffs[2].animate.move_to(f1_matrix[0][2]),
                FadeOut(formula[1:])
            )
        self.wait(1)
        self.play(
                FadeIn(f2_matrix),
                f2_formula[0].animate.next_to(f2_matrix,LEFT),
                self.coeffs[3].animate.move_to(f2_matrix[0][0]),
                self.coeffs[4].animate.move_to(f2_matrix[0][1]),
                FadeOut(f2_formula[1:])
            )
        self.wait(3)
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
        self.vowel_vec = vowel_vec
        self.vowel_label = vowel_label

    def show_coeffs(self):
        c1 = make_coeff(1,self.ax1)
        c2 = make_coeff(1,self.ax2)
        c3 = make_coeff(1,self.ax3)
        self.play(Write(c1),Write(c2),Write(c3))
        self.wait(4)
        new_coeffs = self.change_coeffs(c1,c2,c3,2.0,3.0,5.0)
        self.wait(5)
        new_coeffs = self.change_coeffs(*new_coeffs,-2.0, 3., 5.)
        self.wait(5)
        new_coeffs = self.change_coeffs(*new_coeffs,-2.0, 3., 10.)
        self.wait(5)
        new_coeffs = self.change_coeffs(*new_coeffs,-2.0,3.,0.)
        self.wait(5)
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

        self.wait(5)

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


class PlotDCT(PlotScene):
    def construct(self):
        ax = self.setup_axes( 1920., 2000., 10.,4., math.log(4500.), 1,)
        labels = self.label(ax)
        legend = self.make_legend().next_to(ax,RIGHT*0.1).scale(0.8)
        title = Title(
            "Distance in DCT-space by birth year\\\\",
            include_underline=False,
            font_size=40,
        )
        title2 = Title(
            "{{Distance in DCT-space by birth year}}\\\\{{(White speakers)}}",
            include_underline=False,
            font_size=40,
        )
        title3 = Title(
            "Distance in DCT-space by birth year\\\\(Asian, Black, and Native American speakers)",
            include_underline=False,
            font_size=40,
        )
        dots = []
        white =[]
        abi = []
        for coord,race in self.load_data():
            if coord[1] > 3500:
                continue
            logged = coord
            logged[1] = math.log(coord[1])
            p = self.get_canvas_point(ax,logged)
            point = Dot(
                    p,
                    color=MAROON_B,
                    fill_opacity=0.5,
                    radius=0.04
                )
            dots.append(point)
            if race == 'aawhite':
                white.append(point)
            elif race == 'abi':
                abi.append(point)
        dots.sort(key = lambda x: x.get_x())
        dot_anim = [FadeIn(d, shift=DOWN) for d in dots]
        rm_dots = [FadeOut(d, shift=DOWN) for d in dots if d not in white]
        rm_white = [FadeOut(w, shift=UP) for w in white]
        return_abi = [FadeIn(a, shift=UP) for a in abi]
        plot = LaggedStart(*dot_anim, lag_ratio=0.001)
        self.add(ax,labels,title)
        self.play(plot)
        self.wait(10)
        fit_line = ax.plot(
                lambda x: math.log(self.lm(x)), 
                x_range=[1920,2000,1]
            ).set_color(MAROON)
        white_line = ax.plot(
                lambda x: math.log(self.lm_white(x)),
                x_range=[1920,2000,1]
            ).set_color(MAROON)
        abi_line = ax.plot(
                lambda x: math.log(self.lm_abi(x)),
                x_range=[1920,2000,1]
            ).set_color(MAROON)
        self.play(Create(fit_line))
        self.wait(36)
        self.play(*rm_dots,Transform(fit_line,white_line),FadeIn(title2))
        self.wait(13)
        self.remove(title2)
        self.play(*rm_white,*return_abi,Transform(fit_line,abi_line),FadeIn(title3))
        self.wait(22)
        self.play(
                *[FadeOut(x,shift=UP) for x in abi],
                FadeOut(labels),
                FadeOut(fit_line),
                FadeOut(title),
                FadeOut(title3)
            )
        self.wait(1)
        self.ax = ax

    def lm_abi(self,x):
        intercept = 6.53
        beta_birth = -0.006
        x_offset = 1968.076

        y = beta_birth * (x-x_offset) + intercept
        return math.exp(y)

    def lm_white(self,x):
        intercept = 6.53
        beta_birth = -0.003
        x_offset = 1968.076

        y = beta_birth * (x-x_offset) + intercept
        return math.exp(y)

    def lm(self,x):
        intercept = 706.368
        beta_birth = -2.2507
        x_offset = 1968.076

        y = beta_birth * (x-x_offset) + intercept
        return y

    def load_data(self):
        out = []
        with open('DCT_data_clean.csv') as f:
            reader = csv.reader(f)
            next(reader)
            for row in reader:
                out.append(([float(row[1]),float(row[2]),0.0],row[3]))
        return out

    def label(self, ax):
        x_label = ax.get_x_axis_label(
                Tex("Birth year").scale(1), 
                edge=DOWN, 
                direction=DOWN, 
                buff=3
            )
        y_label = ax.get_y_axis_label(
                Tex("Log DCT distance").scale(1).rotate(90 * DEGREES),
                edge=LEFT,
                direction=LEFT,
                buff=0.5
            )
        labels = VGroup(x_label, y_label)
        return labels


class PlotDuration(PlotScene):
    B_BIRTH = -0.0003022
    B_TOKEN = 0.02609
    B_INTERACTION = 0.0003105
    INTERCEPT = 0.2289
    X_OFFSET = 1968.038
    def construct(self):
        dctp = PlotDCT()
        dctp.construct()
        old_ax = dctp.ax
        ax = self.setup_axes( 1920., 2000., 10.,0.06, 0.4, 0.03,)
        labels = self.label(ax)
        legend = self.make_legend().next_to(ax,RIGHT*0.1).scale(0.8)
        title = Title(
            "Token duration by birth year\\\\",
            include_underline=False,
            font_size=40,
        )
        title2 = Title(
            "{{Token duration by birth year}}\\\\{{(White speakers)}}",
            include_underline=False,
            font_size=40,
        )
        title3 = Title(
            "Token duration by birth year\\\\(Asian, Black, and Native American speakers)",
            include_underline=False,
            font_size=40,
        )
        self.add(old_ax)
        self.play(
                Transform(old_ax,ax),
                Create(labels),
                Create(title),
                FadeIn(legend)
            )
        #self.add(ax, labels,title,legend)

        dots = []
        white = []
        abi = []
        for coord, token,race in self.load_data():
            p = self.get_canvas_point(ax,coord)
            point = Dot(
                    p,color=self.get_color(token),
                    fill_opacity=0.5,
                    radius=0.04
                )
            dots.append(point)
            if race == 'aawhite':
                white.append(point)
            elif race in ['abi','black','native','asian']:
                abi.append(point)
        # Sorting by x coord means they animate in left-to-right
        dots.sort(key = lambda x: x.get_x())
        dot_anim = [FadeIn(d, shift=DOWN) for d in dots]
        dot_rm = [FadeOut(d,shift=DOWN) for d in dots if d not in white]
        white_anim = [FadeOut(d,shift=UP) for d in white]
        abi_anim = [FadeIn(d,shift=DOWN) for d in abi]
        plot = LaggedStart(*dot_anim, lag_ratio=0.001)
        plot_abi= LaggedStart(*abi_anim, lag_ratio=0.001)

        thought_line = ax.plot(
                lambda x: self.lm(x,'caught'), 
                x_range=[1920,2000,1]
            ).set_color(THOUGHT_COLOR)
        lot_line = ax.plot(
                lambda x: self.lm(x, 'cot'), 
                x_range=[1920,2000,1]
            ).set_color(LOT_COLOR)
        tl2 = ax.plot(
                lambda x:self.lm_white(x,'caught'),
                x_range=[1920,2000,1]
            ).set_color(THOUGHT_COLOR)
        ll2 = ax.plot(
                lambda x:self.lm_white(x,'cot'),
                x_range=[1920,2000,1]
            ).set_color(LOT_COLOR)
        tl3 = ax.plot(
                lambda x:self.lm_abi(x,'caught'),
                x_range=[1920,2000,1]
            ).set_color(THOUGHT_COLOR)
        ll3 = ax.plot(
                lambda x:self.lm_abi(x,'cot'),
                x_range=[1920,2000,1]
            ).set_color(LOT_COLOR)
        self.play(plot)
        self.wait(5)
        self.play(Create(thought_line), Create(lot_line))
        self.wait(23)
        self.play(*dot_rm,Transform(thought_line,tl2),Transform(lot_line,ll2),FadeIn(title2),FadeOut(title))
        self.wait(12)
        self.add(title)
        self.remove(title2)
        self.play(plot_abi,*white_anim,Transform(thought_line,tl3),Transform(lot_line,ll3),FadeOut(title2[1]),FadeIn(title3))
        self.wait(10)
        self.play(*[FadeOut(x,shift=UP) for x in abi])
        self.wait(1)

    def lm_abi(self,x,token):
        if token == 'cot':
            y = 1
        else:
            y = 0
        betas = [
                -0.003,
                0.,
                -0.003
            ]
        return math.exp(
                self.linear_model(
                    betas,
                    x - self.X_OFFSET,
                    y,
                    -1.49
                )
            )

    def lm_white(self,x,token):
        if token == 'cot':
            y = 0.5
        else:
            y = -0.5
        betas = [
                0.,
                0.116,
                0.002
            ]
        return math.exp(
                self.linear_model(
                    betas,
                    x - self.X_OFFSET,
                    y,
                    -1.49
                )
            )


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
                if row[1] == 'SAL':
                    continue
                try:
                    birthyear = float(row[8])
                except ValueError:
                    continue
                token = str(row[4])
                dur = float(row[6])
                race = row[9]
                out.append(([birthyear,dur,0.],token,race))
        return out
