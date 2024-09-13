from manim import *

import custom_animations
import excel_formula
import tex_objs


class TreasureHuntOpening(Scene):
    def construct(self):
        texts: list[str] = [
            'I got\n100\\verb|%|\nin Battle \\verb|#|8',
            'Excel World\nChampionships\nRoad To\nLas Vegas',
            'and still\ncame\n15th'
        ]
        self.wait()
        tex_mobs: list[tex_objs.BlockTex] = [tex_objs.BlockTex(text, buff=0.05).scale(1.45).set_opacity(0)
                                             for text in texts]

        max_width = max(tex_mobs[2].height, tex_mobs[1].height, tex_mobs[0].height)
        tex_mobs[2][-1].set_color(XKCD.AMBER)

        tex_mobs[0].scale_to_fit_width(max_width).move_to(ORIGIN)
        tex_mobs[1].scale_to_fit_width(max_width).move_to(ORIGIN)
        tex_mobs[2].scale_to_fit_height(max_width).move_to(ORIGIN)

        tmp_0 = tex_mobs[0].copy().set_color(XKCD.SLATE).set_opacity(1)
        tmp_1 = tex_mobs[1].copy().set_color(XKCD.SLATE).set_opacity(1)

        tmp_0.rotate(PI/2, about_point=tmp_0.get_corner(DL))
        tmp_0.to_edge(LEFT)

        tmp_1.set_color(XKCD.SLATE).set_opacity(1).rotate(-PI/2, about_point=tmp_1.get_corner(DR))
        tmp_1.to_edge(RIGHT).set_y(-0.2)
        tex_mobs[1].scale_to_fit_height(tex_mobs[0].width).next_to(tmp_0).shift(DOWN * 0.1)

        tex_mobs[2].next_to(tmp_0, RIGHT)

        self.play(tex_mobs[0].animate_add_word_by_word(custom_gaps={1: 0, 2: 0, 4: 0, 7: 0}))
        self.play(Transform(tex_mobs[0], tmp_0),
                  tex_mobs[1].animate_add_word_by_word(custom_gaps={7: 0}))
        self.play(Transform(tex_mobs[1], tmp_1),
                  tex_mobs[2].animate_add_word_by_word())

        self.wait()
        whole_group = VGroup(*tex_mobs)
        self.play(custom_animations.ZoomThrough(whole_group, indexes=[2, 1, 1]))


class ComplexNumbers(Scene):
    def construct(self):
        ax = Axes()
        labels = ax.get_axis_labels(Text('Im', font='Comfortaa').scale(0.8), Text('Re', font='Comfortaa').scale(0.8))
        self.wait()
        self.play(LaggedStart(FadeIn(ax), Write(labels), lag_ratio=0.4))
        self.wait(4)
        p0 = labels[0].get_center()
        p1 = labels[1].get_center()
        self.play(labels[0].animate.move_to(p1), labels[1].animate.move_to(p0))
        self.wait(2)


class ComplexLookup(Scene):
    def construct(self):
        a = Arrow().scale(0.6).rotate(PI / 4)
        arrow_name_tex = '\\textbf{Direction}'
        reference_name_tex = '\\textbf{Cell}'
        reference_tex = 'F5'
        reference_pos_tex = '5 + 6i'
        arrow_pos_tex = '-1 + i'
        result_tex = '-4 + 7i'
        lookup_text = '=XLOOKUP(-4 + 7i, Map[C], Map[Cell])'
        final_cell_text = 'G4'
        s = 1.2
        formula = excel_formula.ExcelFormula(lookup_text, split_lines=False, tex_template=tex_objs.GENTLE_SANS_SERIF, scale=s)
        arrow_name = Tex(arrow_name_tex, tex_template=tex_objs.GENTLE_SANS_SERIF).scale(s)
        reference_name = Tex(reference_name_tex, tex_template=tex_objs.GENTLE_SANS_SERIF).scale(s)
        reference = Tex(reference_tex, tex_template=tex_objs.GENTLE_SANS_SERIF).scale(s)
        reference_pos = Tex(reference_pos_tex, tex_template=tex_objs.GENTLE_SANS_SERIF).scale(s)
        arrow_pos = Tex(arrow_pos_tex, tex_template=tex_objs.GENTLE_SANS_SERIF).scale(s)
        result = Tex(result_tex, tex_template=tex_objs.GENTLE_SANS_SERIF).scale(s)
        final_cell = Tex(final_cell_text, tex_template=tex_objs.GENTLE_SANS_SERIF).scale(s)

        reference_name.to_corner(UL).shift(DOWN + RIGHT * 3.5)
        arrow_name.to_corner(UR).shift(DOWN + LEFT * 3.5)
        a.next_to(arrow_name, DOWN)
        arrow_pos.next_to(a, DOWN)
        reference.next_to(reference_name, DOWN)
        reference.set_y(a.get_y())
        reference_pos.next_to(reference, DOWN)
        reference_pos.set_y(arrow_pos.get_y())

        plus = Tex('+', tex_template=tex_objs.GENTLE_SANS_SERIF).scale(s)
        plus.move_to(reference_pos.get_center() + (arrow_pos.get_center() - reference_pos.get_center()) / 2)

        result.next_to(plus, DOWN, buff=0.8)
        combine_copy = VGroup(reference_pos.copy(), arrow_pos.copy())
        formula.next_to(result, DOWN, buff=1)
        final_cell.next_to(formula, DOWN)
        formula[0][10].set_color(RED)

        self.play(LaggedStart(Write(reference_name), Write(arrow_name), lag_ratio=0.4))
        self.play(LaggedStart(Write(reference), DrawBorderThenFill(a).set_run_time(0.8), lag_ratio=0.4))
        self.play(LaggedStart(Write(reference_pos), Write(arrow_pos), lag_ratio=0.4))
        self.play(Write(plus))
        self.play(Transform(combine_copy, result))
        self.play(formula.write_line_by_line())
        self.play(Transform(formula.copy(), final_cell))
        self.wait(4)