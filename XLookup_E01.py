import math

from manim import *
import random
import numpy as np
import re

import excel_character
from excel_helpers import *
from excel_tables import *
from excel_formula import *


class StylisedXExample(Scene):
    def construct(self):
        x_character: excel_character.XCharacter = excel_character.XCharacter()

        self.play(x_character.get_animation_draw_then_fill(), run_time=4)
        self.wait(4)

        self.play(x_character.get_animation_for_look(RIGHT * 9 + UP * 2), run_time=4)
        self.wait(4)
        self.play(x_character.get_animation_for_look(LEFT * 15 + UP * 4), run_time=4)
        self.play(x_character.animate.shift(UP * 2))


# Lookup table data
lookup_table_data = [
    ['Name', 'Age', 'Profession', 'Excel\n\rSkill', 'Hometown'],
    ['Rose', '23', 'Shop Assistant', '2', 'London'],
    ['Martha', '29', 'Doctor', '3', 'London'],
    ['Donna', '35', 'Temp', '4', 'London'],
    ['Amy', '27', 'Journalist', '2', 'Leadworth'],
    ['Rory', '30', 'Nurse', '1', 'Leadworth'],
    ['Clara', '28', 'Teacher', '5', 'Blackpool'],
    ['Bill', '24', 'Student', '2', 'Bristol'],
    ['Yasmin', '28', 'Police Officer', '3', 'Sheffield']
]


class LookupExample(Scene):
    def construct(self):
        # Initial wait
        self.wait(1)

        table = ExcelTable(lookup_table_data)
        table.scale(0.5)
        self.play(table.get_draw_animation())
        self.wait(3.5)

        self.play(table.get_passing_flash('A2:A9', flash_color=YELLOW_E).set_run_time(1.5),
                  Indicate(table.get_columns()[1][6], color=YELLOW_E))
        self.wait(0.3)
        self.play(table.get_passing_flash('A6:E6', flash_color=EP_GREEN).set_run_time(1.5))
        self.wait(0.3)
        result = table.highlight_table_range('D6', highlight_color=EP_EXCEL_GREEN)
        self.play(Create(result))
        self.wait(6)

        self.remove(result)
        self.wait(3)

        # Create a random selection of cells for highlighting
        number_random = 20
        random_cells = list((i + 3, j + 3) for i in range(8) for j in range(4))
        random.shuffle(random_cells)
        random_cells = random_cells[:number_random]

        # Highlight the first two random cells one at a time
        for i in range(2):
            i, j = random_cells.pop()
            self.play(Indicate(table.get_cell((i, j)).set_stroke(color=BLACK, width=2)), run_time=0.8, color=YELLOW_E)

        # Highlight the remaining random cells overlapping with each other
        anim = [Indicate(table.get_cell((i, j)).set_stroke(color=BLACK, width=2), color=YELLOW_E, run_time=0.5) for
                i, j in
                random_cells]
        self.play(LaggedStart(*anim, lag_ratio=0.1))
        self.wait(5)


class XLookup2DExample(Scene):
    def construct(self):
        # Create and add table to the scene
        table = ExcelTable(lookup_table_data)
        table.scale(0.4).to_edge(RIGHT).shift(DOWN * 0.3)
        self.play(table.get_draw_animation())
        self.wait(2)

        # Create and position formula components
        formula_str = '=XLOOKUP("Amy", A2:A9, C2:C9)'
        formula = ExcelFormula(formula=formula_str, start_location=LEFT * 4 + UP * 2, tables_list=[table])
        formula.write_to_scene(self)
        self.wait(2)

        # Perform the XLOOKUP
        result = table.highlight_table_range('C6', highlight_color=EP_EXCEL_GREEN)
        self.play(Create(result))
        self.wait(4)

        # Unwrite the formula and remove highlights 
        self.play(Unwrite(formula), Uncreate(formula.highlight_objs))
        self.wait(2)


class qt(Scene):
    def construct(self):
        f = ExcelFormula('=XLOOKUP("Test")')
        self.play(f.write_to_scene())
        self.wait(2)
        self.play(Indicate(f[0][2]))
        self.wait(2)
        self.play(FadeOut(f))
        self.wait(2)


class VLookup(Scene):
    def construct(self):
        v_lookup = Tex('VLOOKUP').to_edge(UP)
        h_lookup = Tex('and HLOOKUP').next_to(v_lookup, DOWN)
        self.wait(1)
        self.play(LaggedStart(Write(v_lookup).set_run_time(1.5), Write(h_lookup).set_run_time(1.5), lag_ratio=0.8))
        self.wait(0.2)

        table = ExcelTable(lookup_table_data)
        table.scale(0.4).to_edge(RIGHT).shift(DOWN * 0.3)
        self.play(dissolve_tex(scene=self, tex=h_lookup), table.get_draw_animation())
        self.wait(1)
        config.disable_caching = False

        formula_str = '=VLOOKUP("Rory", A2:E9,'
        formula = ExcelFormula(formula=formula_str, tables_list=[table])
        self.play(formula.write_to_scene())

        little_arrow = Arrow(stroke_width=8, tip_length=0.15, max_stroke_width_to_length_ratio=100,
                             max_tip_length_to_length_ratio=100, color=YELLOW,
                             start=table.get_cell((1, 2)).get_edge_center(UP) + [0, 0.3, 0],
                             end=table.get_cell((1, 2)).get_edge_center(UP))
        col_index = ValueTracker(1)
        col_index_counter = always_redraw(lambda: Integer().set_value(col_index.get_value()).scale(0.7)
                                          .next_to(little_arrow, RIGHT, buff=0.1))

        self.play(Create(little_arrow).set_run_time(1.2),
                              Write(col_index_counter).set_run_time(0.7),
                              lag_ratio=0.3)
        self.play(little_arrow.animate.next_to(table.get_cell((1, 5)), UP, buff=0),
                  col_index.animate.set_value(4), run_time=2)
        formula_str = '=VLOOKUP("Rory", A2:E9, 4)'

        # self.wait(3)
        formula2 = ExcelFormula(formula=formula_str, tables_list=[table])

        self.play(Write(formula2[-1]))
        self.wait(0.5)
        result = results_table([['1']], h_buff=2).scale(0.6).next_to(formula2[-1], DOWN, buff=0.9)
        tmp = formula2.copy()
        self.play(Transform(tmp, result))

        self.wait(1)

        # self.remove(formula[0][-2])
        self.play(FadeOut(formula), FadeIn(formula2[:-1]), run_time=0.01)
        self.play(Indicate(formula2[0][-2], color=YELLOW_E))
        self.play(table.get_passing_flash('A2:A9', flash_color=YELLOW_E))
        self.wait(0.5)
        self.play(table.get_passing_flash('B2:E9', flash_color=YELLOW_E))
        self.wait(1)
        self.play(Indicate(formula2[-1][0], color=YELLOW_E))
        self.wait(7)

        rary = 'Rary? Oh,\n\ryou mean Rory!'
        rary_text = Tex(rary).scale(0.7).next_to(result, DOWN)
        self.play(Write(rary_text), run_time=0.7)
        self.wait(2)
        self.play(dissolve_tex(self, rary_text))
        config.disable_caching = False
        self.wait(2)

        formula_str = '=VLOOKUP("Rory", A2:E9, 4, FALSE)'
        formula = ExcelFormula(formula=formula_str, tables_list=[table])
        formula[-2].move_to(formula2[-1].get_center()).align_to(formula2[-1], LEFT)
        self.play(FadeOut(formula2), run_time=0.01)
        self.add(formula[:-2])
        self.add(formula[-2][:-1])
        bracket = formula[-1][-1]
        bracket.next_to(formula[-2][-2], RIGHT, buff=0.1)
        self.play(Succession(Write(formula[-2][-1]).set_run_time(0.2), Write(formula[-1][0])),
                  bracket.animate.next_to(formula[-1][0], RIGHT, buff=0.1))
        self.wait(3)
        self.play(Indicate(formula[-1][0], color=YELLOW_E))
        self.wait(10)


class HLookup(Scene):
    def construct(self):
        v_lookup = Tex('VLOOKUP').to_edge(UP)
        table = ExcelTable(lookup_table_data)
        table.scale(0.4).to_edge(RIGHT).shift(DOWN * 0.3)
        formula_str = '=VLOOKUP("Rory", A2:E9, 4, FALSE)'
        formula = ExcelFormula(formula=formula_str, tables_list=[table])
        results = results_table([['1']], h_buff=2).scale(0.6).next_to(formula[-1], DOWN)
        self.add(v_lookup, table, formula, formula.highlight_objs, results)
        self.wait(2)

        transposed_table_data = [[row[i] for row in lookup_table_data] for i in range(len(lookup_table_data[0]))]
        transposed_table = ExcelTable(transposed_table_data).scale(0.37).to_edge(DOWN).shift(UP * 0.6)
        h_lookup = Tex('HLOOKUP').to_edge(UP)
        formula_str = '=HLOOKUP("Rory", B1:I5, 4, FALSE)'
        h_formula = ExcelFormula(formula=formula_str, tables_list=[transposed_table], start_location=LEFT * 3.5 + UP * 2.3)
        formula.highlight_objs.z_index = 1
        h_formula.highlight_objs.z_index = 1
        self.play(TransformMatchingTex(v_lookup, h_lookup), TransformMatchingShapes(table, transposed_table),
                  Transform(formula, h_formula),
                  Transform(formula.highlight_objs, h_formula.highlight_objs),
                  results.animate.next_to(h_formula[1], RIGHT, buff=1.5).shift(DOWN*0.2))
        h_formula.highlight_objs.z_index = 1

        self.wait(10)


class AlignmentTest(Scene):
    def construct(self):
        table = ExcelTable(lookup_table_data).scale(0.4).to_edge(RIGHT).shift(DOWN * 0.3)
        self.play(table.get_draw_animation())
        formula_str = '=VLOOKUP("Rory",A2:E9,4)'
        formula_1 = ExcelFormula(formula=formula_str)
        formula_1.write_to_scene(self)
        self.wait(1)
        formula_str = '=VLOOKUPFUNCTIONBUTLONGER("Rory",A2:E9,4)'
        formula_2 = ExcelFormula(formula=formula_str)
        formula_2.write_to_scene(self)
        self.wait(2)


class XLookupTitle(Scene):
    def construct(self):
        title = Tex('XLookup').scale(2)
        self.wait(2)
        self.play(FadeIn(title), run_time=1.5)
        self.wait(3)


class IndexMatch(Scene):
    def construct(self):
        self.wait(3)

        # Create and add table to the scene
        table = ExcelTable(lookup_table_data)
        table.scale(0.4).to_edge(RIGHT).shift(DOWN * 0.3)
        title = Tex('INDEX/MATCH').to_edge(UP)
        self.play(Write(title), table.get_draw_animation())
        self.wait(3)


        formula_str = '=MATCH("Rory",A2:A9,0)'
        match_formula = ExcelFormula(formula=formula_str, tables_list=[table], color_offset=1)
        match_result = (results_table([['5']], h_buff=2).scale(0.6)
                        .next_to(match_formula[-1], DOWN, buff=0.5)
                        .next_to(match_formula[0], DOWN, coor_mask=np.array([1, 0, 0])))

        text = '*Note this is Rory\'s position\n\rwithin the red range.'
        comment_1 = Tex(text).scale(0.35).next_to(match_result, LEFT, buff=0.1).shift(DOWN * 0.1)
        t_match_lines = VGroup(*[mob.copy() for mob in match_formula])

        self.play(match_formula.write_to_scene())
        self.wait(0.5 )
        self.play(Transform(t_match_lines, match_result))
        self.wait(0.5)
        self.play(FadeIn(comment_1))
        self.wait(1)

        ###

        formula_str = '=INDEX(D2:D9, 5)'
        index_formula = ExcelFormula(formula=formula_str, tables_list=[table],
                                     start_location=DEFAULT_FORMULA_START_LOCATION +
                                                    DOWN * (match_formula.height + match_result.height + 1))
        index_result = (results_table([['1']], h_buff=2).scale(0.6)
                        .next_to(index_formula[-1], DOWN, buff=0.5)
                        .next_to(match_result, DOWN, coor_mask=np.array([1, 0, 0])))
        text = '*Note this is the skill level\n\rat the 5th position in the\n\rblue range, aka Rory!'
        comment_2 = Tex(text).scale(0.35).next_to(index_result, LEFT, buff=0.1).shift(DOWN * 0.15)
        t_index_lines = VGroup(*[mob.copy() for mob in index_formula])

        self.play(index_formula.write_to_scene())
        self.wait(1)
        self.play(Transform(t_index_lines, index_result))
        self.wait(0.5)
        self.play(FadeIn(comment_2))
        self.wait(4)

        formula_str = '=INDEX(D2:D9, MATCH("Rory", A2:A9, 0))'
        formula = ExcelFormula(formula=formula_str, tables_list=[table])
        index_partial, match_partial = VGroup(*(formula[:2]), formula[-1]), VGroup(*formula[2:-1])
        index_old, match_old = VGroup(*index_formula), VGroup(*match_formula)

        self.remove(t_match_lines, t_index_lines)
        self.add(index_result)
        self.play(Transform(index_old, index_partial), Transform(match_old, match_partial), FadeOut(comment_1),
                  FadeOut(comment_2), FadeOut(match_result),
                  index_result.animate.next_to(formula[-1], DOWN, buff=0.5,
                                               coor_mask=np.array([0, 1, 0])))

        self.wait(7)

        formula_str = '=INDEX(A6:E6, MATCH("Excel Skill", A1:E1, 0))'
        horizontal_formula = ExcelFormula(formula=formula_str, tables_list=[table])
        formula_lines_group, horizontal_group = VGroup(*formula), VGroup(*horizontal_formula)
        formula_highlights_group = VGroup(*formula.highlights.values())
        horizontal_highlights_group = VGroup(*horizontal_formula.highlights.values())
        self.remove(formula_lines_group, formula_highlights_group, index_old, match_old, index_partial,
                    match_partial, *match_formula.highlights.values(),
                    *index_formula.highlights.values())
        self.play(Transform(formula_lines_group, horizontal_group),
                  Transform(formula_highlights_group, horizontal_highlights_group),
                  run_time=2)

        self.wait(5)
        fade_all_mobs = [FadeOut(mob) for mob in self.mobjects]
        self.add(table.copy(), title.copy())
        self.play(*fade_all_mobs)

        self.wait(4)

        formula_str = '=INDEX(B2:E9, MATCH("Rory", A2:A9, 0), MATCH("Excel Skill", B1:E1, 0))'
        twod_formula = ExcelFormula(formula=formula_str, tables_list=[table])
        self.play(twod_formula.write_to_scene())
        self.wait(10)

        self.play(Indicate(twod_formula[3][0], color=YELLOW_E), Indicate(twod_formula[6][0], color=YELLOW_E))
        self.wait(5)


class XLookup(Scene):
    def construct(self):
        # Create and add table to the scene
        table = ExcelTable(lookup_table_data)
        table.scale(0.4).to_edge(RIGHT).shift(DOWN * 0.3)
        self.add(table)
        self.wait(1)

        # Create text objects for function names
        title = Tex('XLOOKUP').to_edge(UP)
        self.play(Write(title))
        self.wait(5)



        # Create and position formula components
        formula_str = '=XLOOKUP(lookup_value, lookup_array, return_array)'
        formula = ExcelFormula(formula=formula_str)
        # bracket = Tex(')').scale(0.7).next_to(formula[-1], RIGHT, buff=0.1)
        self.play(formula.write_to_scene(gap_between=0, run_time=0.8))
        # self.play(Write(bracket), run_time=0.3)
        self.wait(0.2)
        formula_str = '=XLOOKUP(lookup_value, lookup_array, return_array, [if_not_found], [match_mode], [search_mode])'
        formula2 = ExcelFormula(formula=formula_str)
        self.play(formula.transform_into(formula2))
        self.wait(0.5)
        self.play(FadeOut(formula), run_time=0.001)
        self.play(dissolve_tex(self, formula2[2][-1]), dissolve_tex(self, formula2[3]), dissolve_tex(self, formula2[4]),
                  dissolve_tex(self, formula2[5][:-1][0]), formula2[5][-1].animate.next_to(formula2[2][-2], RIGHT, buff=0.1))
        self.wait(5)
        self.play(FadeOut(formula2), run_time=0.001)

        formula_str = '=XLOOKUP("Rory", A2:A9, D2:D9)'
        formula = ExcelFormula(formula=formula_str, tables_list=[table])
        result = results_table([['1']], h_buff=2).scale(0.6).next_to(formula[-1], DOWN, buff=0.5)
        self.wait(1.5)
        self.play(formula.write_to_scene(gap_between=0))
        self.wait(0.5)
        self.play(Transform(formula.copy(), result))
        self.wait(10)
        # self.play(Unwrite(formula), Uncreate(formula.highlight_objs))

        formula_horizontal = ExcelFormula(formula='=XLOOKUP("Excel Skill", A1:E1, A6:E6')
        self.wait(1.5)
        self.play(formula.transform_into(formula_horizontal))
        self.wait(3)

class XLookup2(Scene):
    def construct(self):
        # Create and add table to the scene
        table = ExcelTable(lookup_table_data)
        table.scale(0.4).to_edge(RIGHT).shift(DOWN * 0.3)
        self.add(table)
        self.wait(1)

        # Create text objects for function names
        title = Tex('XLOOKUP').to_edge(UP)
        self.play(Write(title))
        self.wait(5)



        # Create and position formula components
        formula_str = '=XLOOKUP(lookup_value, lookup_array, return_array)'
        formula = ExcelFormula(formula=formula_str)
        # bracket = Tex(')').scale(0.7).next_to(formula[-1], RIGHT, buff=0.1)
        self.play(formula.write_to_scene(gap_between=0, run_time=0.8))
        # self.play(Write(bracket), run_time=0.3)
        self.wait(0.2)
        formula_str = '=XLOOKUP(lookup_value, lookup_array, return_array, [if_not_found], [match_mode], [search_mode])'
        formula2 = ExcelFormula(formula=formula_str)
        self.play(formula.transform_into(formula2))
        self.wait(0.5)
        self.play(FadeOut(formula), run_time=0.001)
        self.play(dissolve_tex(self, formula2[2][-1]), dissolve_tex(self, formula2[3]), dissolve_tex(self, formula2[4]),
                  dissolve_tex(self, formula2[5][:-1][0]), formula2[5][-1].animate.next_to(formula2[2][-2], RIGHT, buff=0.1))
        self.wait(5)
        self.play(FadeOut(formula2), run_time=0.001)

        formula_str = '=XLOOKUP("Rory", A2:A9, D2:D9)'
        formula = ExcelFormula(formula=formula_str, tables_list=[table])
        result = results_table([['1']], h_buff=2).scale(0.6).next_to(formula[-1], DOWN, buff=0.5)
        self.wait(1.5)
        self.play(formula.write_to_scene(gap_between=0))
        self.wait(0.5)
        self.play(Transform(formula.copy(), result))
        self.wait(10)
        # self.play(Unwrite(formula), Uncreate(formula.highlight_objs))

        formula_horizontal = ExcelFormula(formula='=XLOOKUP("Excel Skill", A1:E1, A6:E6)', tables_list=[table])
        self.wait(1.5)
        self.play(formula.transform_into(formula_horizontal))
        self.wait(3)


class ComparisonTableLookups(Scene):
    def construct(self):
        table_data = [['Feature', 'VLOOKUP', 'HLOOKUP', 'INDEX/\nMATCH', 'XLOOKUP'],
                      ['Lookup Direction', 'Right only', 'Down only', 'Both', 'Both'],
                      ['Robust to Changes', 'No', 'No', 'Yes', 'Yes'],
                      ['Exact Match Default', 'No', 'No', 'No', 'Yes'],
                      ['Ease of Use', 'Med', 'Med', 'Hard', 'Easy'],
                      ['Flexibility', 'Low', 'Low', 'High', 'High'],
                      ['Match Mode', 'Lim', 'Lim', 'Full', 'Full'],
                      ['Custom Not Found', 'No', 'No', 'No', 'Yes'],
                      ['Wildcard Match', 'Always', 'Always', 'Always', 'When Req'],
                      ['Dynamic Arrays', 'No', 'No', 'No', 'Yes'],
                      ['Implicit Helpers', 'No', 'No', 'Yes', 'Yes'],
                      ['EXACT & Complex Matches', 'No', 'No', 'Yes', 'Yes']]
        table = ComparisonTable(table_data)
        table.scale(0.4).to_edge(UP)
        self.play(table.create_and_write_headers(), lag_ratio=0.6)
        self.wait(3)
        self.play(table.fill_in_rows())
        self.wait(10)


class ComparisonTableLookupsSimple(Scene):
    def construct(self):
        table_data = [['Feature', 'VLOOKUP', 'HLOOKUP', 'INDEX/\nMATCH', 'XLOOKUP'],
                      ['Lookup Direction', 'Right only', 'Down only', 'Both', 'Both'],
                      ['Robust to Changes', 'No', 'No', 'Yes', 'Yes'],
                      ['Exact Match Default', 'No', 'No', 'No', 'Yes'],
                      ['Ease of Use', 'Med', 'Med', 'Hard', 'Easy'],
                      ['Flexibility', 'Low', 'Low', 'High', 'High']]
        table = ComparisonTable(table_data)
        table.scale(0.5)
        self.wait(3)
        self.play(table.create_and_write_headers(), lag_ratio=0.6)
        self.wait(3)
        self.play(table.fill_in_rows())
        self.wait(10)


class Thumbnail(Scene):
    def construct(self):
        v = Tex('VLOOKUP')
        i = Tex('INDEX/MATCH')
        h = Tex('HLOOKUP')
        x = Tex('X')

        l = Tex('LOOKUP')

        # g1 = VGroup(v, i, h)
        g1 = VGroup(v)
        g1 = g1.scale(1.1).arrange(DOWN, buff=1.3).shift(LEFT * 2).next_to(ORIGIN, LEFT, coor_mask=np.array([1, 0, 0]))
        mob: Tex
        for mob in g1:
            cross = CROSS.copy().scale(0.3).move_to(mob.get_center())
            cross.z_index = 1
            cross.set_stroke(XKCD.DARKRED)
            mob.set_color(GRAY)
            self.add(cross)

        x.scale(2.5).shift(RIGHT * 2)
        l.scale(1.5).next_to(x, RIGHT, buff=0.1)
        xg = VGroup(x, l)
        self.add(g1, xg)
        # self.play(LaggedStart(AnimationGroup(Unwrite(v), Unwrite(h)), Unwrite(i), lag_ratio=0.1))
        # *[Unwrite(mob) for mob in g1])
        self.play(Unwrite(g1))


class Searches(Scene):
    def construct(self):
        blue_to_use = XKCD.COBALT
        n = 50
        r = RoundedRectangle(color=XKCD.COBALTBLUE, fill_color=blue_to_use, fill_opacity=1, height=0.08, width=1,
                             corner_radius=0.04, stroke_width=0.2)
        path = r.get_all_points()
        i = 12
        new_path = np.concatenate((path[i:], path[:i]), axis=0)
        r.set_points(new_path[::-1])
        rectangles = VGroup(*[r.copy() for _ in range(n)])
        rectangles.arrange(DOWN, buff=0.06)
        # rectangles.shift(LEFT*3)
        self.play(
            LaggedStart(*[DrawBorderThenFill(rectangle).set_run_time(1.5) for rectangle in rectangles], lag_ratio=0.05))
        self.wait(4)

        find_m = 50
        find_m -= 1

        rt_1 = 0.3
        rt_2 = 0.05
        # Linear
        for i in range(find_m):
            self.play(rectangles[i].animate.scale(1.2).set_color(YELLOW), run_time=rt_1)
            self.play(rectangles[i].animate.set_color(RED), run_time=rt_2)
            self.play(rectangles[i].animate.scale(1 / 1.2), run_time=rt_1)

        self.play(rectangles[find_m].animate.scale(1.2).set_color(YELLOW), run_time=rt_1)
        self.play(rectangles[find_m].animate.set_color(GREEN), run_time=rt_2)
        self.wait(3)

        rectangles.set_color(blue_to_use)
        rectangles[find_m].scale(1 / 1.2)
        # Binary
        left = 0
        right = n - 1

        while True:
            i = (left + right) // 2

            if i == find_m:
                self.play(rectangles[find_m].animate.scale(1.2).set_color(YELLOW), run_time=rt_1)
                self.play(rectangles[find_m].animate.set_color(GREEN), run_time=rt_2)
                break

            self.play(rectangles[i].animate.scale(1.2).set_color(YELLOW), run_time=rt_1)
            self.play(rectangles[i].animate.set_color(RED), run_time=rt_2)
            if i < find_m:
                left = i + 1
                j = i
                fade_group = [rectangle for rectangle in rectangles[:i] if rectangle.color == blue_to_use]
            else:
                right = i - 1
                j = i
                fade_group = [rectangle for rectangle in rectangles[i:] if rectangle.color == blue_to_use]

            if fade_group:
                self.play(rectangles[j].animate.scale(1 / 1.2),
                          AnimationGroup(*[rectangle.animate.set_color(GREY) for rectangle in fade_group]),
                          run_time=rt_1)
            else:
                self.play(rectangles[j].animate.scale(1 / 1.2), run_time=rt_1)

        self.wait(3)
        rectangles[find_m].scale(1 / 1.2)
        rectangles.set_color(blue_to_use)
        self.wait(4)

        self.play(rectangles.animate.scale(0.9))
        title = None
        for find_m in range(n):
            if title:
                title.become(Title(f'n={find_m + 1}'))
            else:
                title = Title(f'n={find_m + 1}')
                self.play(Create(title))

            self.wait()

            left = 0
            right = n - 1
            bs = 0
            while True:
                i = (left + right) // 2
                bs += 1
                if i == find_m:
                    break
                if i < find_m:
                    left = i + 1
                    j = i
                else:
                    right = i - 1
                    j = i

            n_bin = n // 2
            width = n_bin
            while n_bin != find_m:
                width = max(width // 2, 1)
                n_bin = n_bin + width if find_m > n_bin else n_bin - width

            label_linear = Text(f'{find_m + 1} search(es)\nfor linear search').next_to(rectangles, LEFT)
            label_binary = Text(f'{bs} search(es)\nfor binary search').next_to(rectangles, RIGHT)
            self.play(FadeIn(label_linear), FadeIn(label_binary))

            left = 0
            right = n - 1

            while True:
                i = (left + right) // 2

                if i == find_m:
                    self.play(rectangles[find_m].animate.scale(1.2).set_color(YELLOW), run_time=rt_1)
                    self.play(rectangles[find_m].animate.set_color(GREEN), run_time=rt_2)
                    break

                self.play(rectangles[i].animate.scale(1.2).set_color(YELLOW), run_time=rt_1)
                self.play(rectangles[i].animate.set_color(RED), run_time=rt_2)
                if i < find_m:
                    left = i + 1
                    j = i
                    fade_group = [rectangle for rectangle in rectangles[:i] if rectangle.color == blue_to_use]
                else:
                    right = i - 1
                    j = i
                    fade_group = [rectangle for rectangle in rectangles[i:] if rectangle.color == blue_to_use]

                if fade_group:
                    self.play(rectangles[j].animate.scale(1 / 1.2),
                              AnimationGroup(*[rectangle.animate.set_color(GREY) for rectangle in fade_group]),
                              run_time=rt_1)
                else:
                    self.play(rectangles[j].animate.scale(1 / 1.2), run_time=rt_1)

            self.wait(3)
            self.remove(label_linear, label_binary)
            rectangles[find_m].scale(1 / 1.2)
            rectangles.set_color(blue_to_use)
            self.wait(2)


if __name__ == '__main__':
    print('Running debug')
    with tempconfig({"quality": "medium_quality", "disable_caching": True, '--preview': True}):
        scene = XLookup()
        scene.render()
