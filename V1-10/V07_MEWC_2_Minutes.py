import math

from manim import *

import excel_constants


class MEWCAcronym(Scene):
    def construct(self):
        self.wait(2)
        title = Tex('\\textbf{M}icrosoft', '\\textbf{E}xcel', '\\textbf{W}orld', '\\textbf{C}hampionship')
        title.scale(1.5)
        title.arrange(DOWN)
        most_left = sorted([el for el in title], key=lambda el: el.get_left()[0])[0]
        el: SingleStringMathTex
        for el in title:
            el[0].set_color(excel_constants.EP_GREEN)
            el[0].scale(1.1)
            el.align_to(most_left, LEFT)
        self.play(LaggedStart(*[Write(el) for el in title], lag_ratio=0.5))
        self.wait(0.2)
        first_letters = VGroup(*[el[0].copy().set_x(0) for el in title])
        self.play(Transform(title, first_letters))
        self.wait(2)
class Andrews(Scene):
    def construct(self):
        self.wait(3)
        andrew_g = ImageMobject('../headshots/AndrewGrigolyunovichNoBG.png').scale(0.87)
        andrew_n = ImageMobject('../headshots/AndrewNgaiNoBG.png')
        andrews = [andrew_g, andrew_n]
        andrew_names = [*[Tex(name).scale(1.5) for name in ['Andrew\n\rGrigolyunovich', 'Andrew\n\rNgai']]]

        andrew_g.shift(LEFT * 2.2)
        andrew_n.shift(RIGHT * 2.6)

        def overshoot_function(t):
            if t < 0.7:  # Accelerating phase
                return 0.96 * (1 - math.cos(t * math.pi / 0.7)) / 2
            else:  # Overshoot and bounce phase
                return 0.96 + 0.08 * math.sin((t - 0.7) * 2 * math.pi / 0.3)

        for i, andrew in enumerate(andrews):
            andrew.to_edge(DOWN, buff=0)
            rot_pt = andrew.get_bottom()
            andrew_name = andrew_names[i]
            andrew_name.next_to(andrew, UP, buff=0)
            andrew_name.set_y(2.6)

            andrew.rotate(90 * DEGREES, axis=RIGHT, about_point=andrew.get_bottom())
            self.add(andrew)
            rotate_andrew = (andrew.animate(run_time=1.4, rate_func=overshoot_function)
                             .rotate(90 * DEGREES, axis=LEFT, about_point=rot_pt))
            self.play(LaggedStart(rotate_andrew, Write(andrew_name), lag_ratio=0.4))
            self.wait(1.5)