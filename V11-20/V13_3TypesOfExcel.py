import random
from functools import partial

from manim import *

import custom_animations
import excel_character
import tex_objs


class IntroScene(Scene):
    def construct(self):
        data_cases = [
            ('Speed\nlandia', '', ''),
            ('Biathlon', '', ''),
            ('Flight to\nNowhere', '', ''),
            ('Elections\nare Coming', '', ''),
            ('Social\nNetwork', '', ''),
            ('Sommelier', '', ''),
            ('I\'m Left\nHanded', '', 'Right?')
        ]

        game_cases = [
            ('Euchre', '', ''),
            ('Othello', '', ''),
            ('A Story\nAbout the\nReels', '', ''),
            ('Collect\nEm All', '', ''),
            ('Passing\nNotes', '', ''),
            ('Bingo', '', '')
        ]

        map_cases = [
            ('Bear\nIsland', '', ''),
            ('Doggie\nDaycare', '', ''),
            ('Lana\nBanana', '', ''),
            ('Deep Sea\nDiving', '', ''),
            ('VLookie\nthe Gold\nMiner', '', ''),
            ('Treasure\nHunt', '', ''),
            ('Maze', '', '')
        ]

        blues = [
            XKCD.LIGHTBLUEGREY,
            XKCD.STEELBLUE,
            XKCD.LIGHTBLUE,
            XKCD.SLATE,
            XKCD.LIGHTPERIWINKLE,
            XKCD.BLUISHGREY,
            XKCD.BLUEYGREY
        ]

        data_mobs = VGroup(*[tex_objs.BlockTex(*case) for case in data_cases])
        game_mobs = VGroup(*[tex_objs.BlockTex(*case) for case in game_cases])
        map_mobs = VGroup(*[tex_objs.BlockTex(*case) for case in map_cases])

        all_mobs = VGroup(*data_mobs, *game_mobs, *map_mobs)
        max_width = max([mob.width for mob in all_mobs])
        for mob in all_mobs:
            mob.scale_to_fit_width(max_width)
            mob.set_color(random.choice(blues))

        all_mobs.shuffle()
        b = 0.6
        all_mobs.arrange_in_grid(buff=b).scale(0.55)
        sh = 0.2
        sv = 0.2
        for mob in all_mobs:
            random_offset = np.array([
                random.uniform(-sh, sh),
                random.uniform(-sv, sv),
                0
            ])
            mob.shift(random_offset)

        tl = all_mobs[0]
        tr = all_mobs[4]
        ls = all_mobs[5:16:5]
        rs = all_mobs[9:20:5]
        ls.set_y(all_mobs.get_y()),
        rs.set_y(all_mobs.get_y())
        tl.next_to(ls[1], LEFT).shift(UP * 0.1),
        tr.next_to(rs[1], RIGHT).shift(DOWN * 0.1)
        all_mobs.move_to(ORIGIN).shuffle()

        self.play(LaggedStart(*[Write(mob) for mob in all_mobs], lag_ratio=0.1))

        self.wait(4)

        level_1 = tex_objs.BlockTex('Level 1', color=XKCD.BOTTLEGREEN).scale(3)
        level_2 = tex_objs.BlockTex('Level 2', color=XKCD.BROWNORANGE).scale(3)
        level_3 = tex_objs.BlockTex('Level 3', color=XKCD.CHERRY).scale(3)

        level_1.shift(LEFT * 4 + UP * 2)
        level_3.shift(RIGHT * 4 + DOWN * 2)

        self.play(LaggedStart(
                Transform(data_mobs, level_1),
                Transform(game_mobs, level_2),
                Transform(map_mobs, level_3),
                lag_ratio=0.2
            )
        )

        self.wait(2)



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

        self.play(t1.animate_add_word_by_word())
        self.play(t1.animate(run_time=0.5, rate_func=custom_animations.custom_ease)
                  .rotate(PI / 2, about_point=t1.get_corner(DL)),
                  t2.animate_add_word_by_word())
        self.wait(2)
        whole_group = VGroup(t1, t2)
        self.play(custom_animations.ZoomThrough(whole_group, [1, 1, 2]))

        headings: VGroup = VGroup(*[tex_objs.BlockTex(level).scale(2) for level in
                                    ['Level 1:\n\\textbf{Data}', 'Level 2:\n\\textbf{Games}',
                                     'Level 3:\n\\textbf{Maps}']])
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
            self.play(heading.animate_add_word_by_word(custom_gaps={1: 0.25, 2: 0.6}))
            self.wait(1)


class ExcelSheetHappens(Scene):
    def construct(self):
        tb = tex_objs.BlockTex('Excel\nSheet\nHappens').scale(3.2).move_to(ORIGIN)
        char = excel_character.XCharacter().scale(1.5)
        char.to_corner(DL)
        char.true_hide_all_eyebrows()
        self.wait()
        self.play(FadeIn(char))
        self.wait()
        self.play(LaggedStart(
            tb.animate_add_word_by_word(),
            char.animate_roll_eyes(),
            lag_ratio=0.3
        ))
        self.play(char.animate_twist_and_shout(run_time=0.8))
        self.play(char.animate_eyes_centre(run_time=0.4))
        self.wait(3)


class ConfusedX(Scene):
    def construct(self):
        char = excel_character.XCharacter().scale(2.5)
        char.to_edge(DOWN)
        self.play(char.animate_create())
        question_marks = VGroup(*[tex_objs.BlockTex('?') for _ in range(3)])
        question_marks.arrange(RIGHT).scale(5)
        question_marks.next_to(char, UP)
        angle = PI/5
        question_marks[0].rotate(angle=angle)
        question_marks[2].rotate(angle=-angle)

        elastic = partial(custom_animations.custom_ease_out_elastic, oscillations=10, frequency=5, amplitude=1)
        # self.wait(2)
        self.play(char.animate_intrigued_eyes())
        self.play(
            LaggedStart(
                Write(question_marks[1]),
                Write(question_marks[0]),
                Write(question_marks[2]),
                lag_ratio=0.3
            ),
            char.animate_think_eye(rate_func=elastic, run_time=2),
        )
        self.wait(2)


class AlphabetCode(Scene):
    def construct(self):
        alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        alphabet_mobs = VGroup(*[Tex(alphabet[i], tex_template=tex_objs.GENTLE_SANS_SERIF)
                                 for i in range(len(alphabet))]).scale(1.8)
        alphabet_mobs.arrange_in_grid(cols=13, buff=(0.4, 0.8))
        self.play(LaggedStart(
            *[Write(letter) for letter in alphabet_mobs],
            lag_ratio=0.1
        ))
        self.wait()

        pointer = Triangle(fill_opacity=1, fill_color=YELLOW, color=YELLOW_E).scale(0.2)
        pointer.next_to(alphabet_mobs[6], DOWN, buff=0.1)
        self.play(DrawBorderThenFill(pointer))
        self.wait()

        path = (Line(pointer.get_center(),
                    alphabet_mobs[12].get_bottom() + DOWN * 0.2)
                .append_points(Line(alphabet_mobs[12].get_bottom() + DOWN * 0.2,
                                    alphabet_mobs[13].get_bottom() + DOWN * 0.2).points)
                .append_points(Line(alphabet_mobs[13].get_bottom() + DOWN * 0.2,
                                    alphabet_mobs[25].get_bottom() + DOWN * 0.2).points))
        self.play(MoveAlongPath(pointer, path, run_time=2, rate_func=rate_functions.ease_out_bounce))

class ThreeTypesOfExcel2(Scene):
    def construct(self):
        text_1 = tex_objs.BlockTex('Most cases\nfall into\none of').scale(2).move_to(ORIGIN)
        text_2 = tex_objs.BlockTex('these 3\ncategories').scale(3)
        text_2[0][-1].set_color(XKCD.BOTTLEGREEN)
        text_1_copy = text_1.copy().scale_to_fit_width(text_2.height).rotate(PI/2).to_edge(LEFT).set_color(XKCD.SLATE)
        text_2.next_to(text_1_copy, RIGHT)

        self.play(text_1.animate_add_word_by_word(custom_gaps={4: 0, 5: 0, 6: 0, 7: 0}))
        self.play(
            Transform(text_1, text_1_copy),
            text_2.animate_add_word_by_word()
        )
        self.wait(2)
        self.play(custom_animations.ZoomThrough(VGroup(text_1, text_2), [1, -1, 4]))

        headings: VGroup = VGroup(*[tex_objs.BlockTex(level).scale(2) for level in
                                    ['Level 1:\n\\textbf{Data}', 'Level 2:\n\\textbf{Games}',
                                     'Level 3:\n\\textbf{Maps}']])
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
            self.play(heading.animate_add_word_by_word(custom_gaps={1: 1, 2: 3}))
            self.wait(1)
