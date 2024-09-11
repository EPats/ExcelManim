from manim import *

import custom_animations
import tex_objs


class ThreeTypesOfExcel(Scene):
    def construct(self):
        tex_1_pre: str = 'There are'
        tex_1: str = '3'
        tex_2: str = 'types of\nExcel\nEsport'
        tex_2_post: str = 'scenario'

        t1 = tex_objs.BlockTex(tex_1, pre_text=tex_1_pre)
        t1[0].next_to(t1[1], LEFT, buff=0.05)
        t1[1].set_color(XKCD.BOTTLEGREEN)
        t1.shift(RIGHT * 0.4)
        t2 = tex_objs.BlockTex(tex_2, post_text=tex_2_post).scale(2)

        t1.scale_to_fit_width(t2.height)
        rot_t1 = t1.copy().rotate(PI / 2, about_point=t1.get_corner(DL))
        t2.next_to(rot_t1, RIGHT, buff=0.7)

        self.play(t1.get_add_word_by_word_anim())
        self.play(t1.animate(run_time=0.5, rate_func=custom_animations.custom_ease)
                  .rotate(PI / 2, about_point=t1.get_corner(DL)),
                  t2.get_add_word_by_word_anim())
        self.wait(2)
        whole_group = VGroup(t1, t2)
        self.play(custom_animations.ZoomThrough(whole_group, [1, 1, 2]))

        headings: VGroup = VGroup(*[tex_objs.BlockTex(level).scale(2) for level in
                                    ['Level 1:\n\\textbf{Data}', 'Level 2:\n\\textbf{Games}', 'Level 3:\n\\textbf{Maps}']])
        headings.arrange(DOWN, buff=0)
        # headings.shift(UP)
        movement: float = 4.5
        headings[0].shift(LEFT * movement)
        headings[2].shift(RIGHT * movement)
        headings[0][1].set_color(XKCD.BOTTLEGREEN)
        headings[1][1].set_color(XKCD.BROWNORANGE)
        headings[2][1].set_color(XKCD.CHERRY)

        heading: tex_objs.BlockTex
        for heading in headings:
            self.play(heading.get_add_word_by_word_anim(custom_gaps={1: 0.25, 2: 0.6}))
            self.wait(1)
