from manim import *

import XLookup_E01
from excel_tables import *
from excel_formula import *
from scenes import NarratedScene
import random


def categorise_book(pages: int, option2: bool = False) -> str:
    if pages < 100:
        return 'Short'
    elif pages < (300 if option2 else 400):
        return 'Medium'
    elif pages < 1000:
        return 'Long'
    else:
        return 'Epic'


class MatchMode(NarratedScene):
    def construct(self):
        books_data = [
            ['\\textbf{Name}', '\\textbf{Author}', '\\textbf{Pages}'],
            ['The Great Gatsby', 'F. Scott Fitzgerald', 180],
            ['The Hobbit', 'J.R.R. Tolkien', 310],
            ['The Catcher in the Rye', 'J.D. Salinger', 230],
            ['War and Peace', 'Leo Tolstoy', 1225],
            ['The Very Hungry Caterpillar', 'Eric Carle', 32],
            ['The Grapes of Wrath', 'John Steinbeck', 528],
            ['The Odyssey', 'Homer', 416],
            ['The Gruffalo', 'Julia Donaldson', 32],
            ['Les Misérables', 'Victor Hugo', 1463],
            ['The Cat in the Hat', 'Dr. Seuss', 61],
            ['The Picture of Dorian Gray', 'Oscar Wilde', 254],
            ['The Tale of Peter Rabbit', 'Beatrix Potter', 56],
            ['Next', 'Michael Crichton', 507]
        ]

        scoring_data = [
            ['\\textbf{Book Length}', '\\textbf{Min Pages}', '\\textbf{Max Pages}'],
            ['Short', 0, 99],
            ['Medium', 100, 499],
            ['Long', 400, 999],
            ['Epic', 1000, 5000]
        ]

        title = Text('XLookup: Match Mode').scale(0.85).to_edge(UP)
        self.play(Write(title))

        table_data = [books_data[i] + ['\\textbf{Book Length}' if i == 0 else categorise_book(books_data[i][-1])] + ['']
                      + scoring_data[i] if i < len(scoring_data)
                      else books_data[i] + [categorise_book(books_data[i][-1])]
                           + [''] * 4 for i in range(len(books_data))]

        table = ExcelTable(table_data)
        table.scale(0.3).to_edge(DOWN).shift(DOWN * 0.2)
        hidden_data = [(i, 4) for i in range(2, len(books_data) + 1)]
        self.play(table.get_draw_animation(hidden_data=hidden_data))
        self.wait(2)

        formula_str = '=XLOOKUP(C2, $G$2:$G$5, $F$2:$F$5, , -1)'
        formula = ExcelFormula(formula_str, tables_list=[table], split_lines=False, target_cell='D2',
                               start_location=table.get_top() + 0.5 * UP, start_align=ORIGIN)

        self.play(formula.write_to_scene())

        self.wait(1)

        hidden_data_mobs = [table.get_rows()[i][j] for i, j in hidden_data]
        result_1 = hidden_data_mobs.pop(0)
        self.play(Write(result_1))
        self.wait(2)
        write_results = LaggedStart(*[Write(mob) for mob in hidden_data_mobs], lag_ratio=0.1)
        self.play(table.animate_flash_fill('D2:D14', lagged_animations=[write_results]))
        self.wait(2)




class DynamicArraysExample(NarratedScene):
    def construct(self):
        title = Text('Dynamic Arrays').scale(0.85).to_edge(UP)
        self.play(Write(title))

        n_values = [3, 1, 4, 1, 5, 9, 2, 6, 5, 3, 5, 8, 9, 7, 9, 3]
        sequence_str = f'=SEQUENCE({n_values[0]})'
        s = 0.8
        formula = ExcelFormula(sequence_str, scale=s).next_to(title, DOWN, buff=0.4)
        value_tracker = ValueTracker(n_values[0])
        tracked_tex = always_redraw(lambda: Integer().set_value(value_tracker.get_value())
                                    .scale(s).move_to(formula[0][-2]))
        result_tables: list[Table] = [results_table([[str(i)] for i in range(1, n + 1)], v_buff=0.6, h_buff=1.6,
                                                    results_title=False).scale(0.65) for n in n_values]

        for i, n in enumerate(n_values):
            result_table = result_tables[i]
            if i == 0:
                result_table.next_to(formula, DOWN)
                h1 = Line(result_table.get_cell((1, 1)).get_corner(DL), result_table.get_cell((1, 1)).get_corner(DR),
                          stroke_width=2, color=BLACK)
                h2 = Line(result_table.get_cell((2, 1)).get_corner(DL), result_table.get_cell((2, 1)).get_corner(DR),
                          stroke_width=2, color=BLACK)

                self.play(formula.write_to_scene().set_run_time(1.5),
                          AnimationGroup(result_table.create().set_run_time(1.6),
                                         Create(h1), Create(h2)))
                self.remove(formula[0][-2])
                self.add(tracked_tex)

            else:
                result_table.align_to(result_tables[0], UP)

                self.play(value_tracker.animate.set_value(n),
                          ReplacementTransform(result_tables[i - 1], result_table), run_time=0.8)
                self.remove(result_tables[i - 1])
            self.wait(0.4)

        self.wait(2)


base_table_data = [
    ['\\textbf{Name}', '\\textbf{Age}', '\\textbf{Profession}', '\\textbf{Excel}\n\r\\textbf{Skill}',
     '\\textbf{Hometown}'],
    ['Rose', '23', 'Shop Assistant', '2', 'London'],
    ['Martha', '29', 'Doctor', '3', 'London'],
    ['Donna', '35', 'Temp', '4', 'London'],
    ['Amy', '27', 'Journalist', '2', 'Leadworth'],
    ['Rory', '30', 'Nurse', '1', 'Leadworth'],
    ['Clara', '28', 'Teacher', '5', 'Blackpool'],
    ['Bill', '24', 'Student', '2', 'Bristol'],
    ['Yasmin', '28', 'Police Officer', '3', 'Sheffield']
]


class DynamicArraysXLookup(NarratedScene):
    def construct(self):
        title = Text('XLookup: Dynamic Arrays').scale(0.85).to_edge(UP)
        self.play(Write(title))

        lookup_data = [
            ['\\textbf{Name}', '\\textbf{Hometown}', ''],
            ['Donna', 'London', ''],
            ['Yasmin', 'Sheffield', ''],
            ['Martha', 'London', ''],
            ['Clara', 'Blackpool', ''],
            ['', '', 'Shop Assistant'],
            ['', '', ''],
            ['\\textbf{Name}', '\\textbf{Profession}', '\\textbf{Excel Skill}'],
            ['Rory', 'Nurse', '1']
        ]

        table_data = [base_table_data[i] + [''] + lookup_data[i] for i in range(len(base_table_data))]
        table = ExcelTable(table_data)
        table.scale(0.37).to_edge(DOWN).shift(DOWN * 0.2)
        hidden_data = [(2, 8), (3, 8), (4, 8), (5, 8), (9, 8), (9, 9), (6, 9)]
        self.play(table.get_draw_animation(hidden_data=hidden_data))
        self.wait(2)

        formula_str = '=XLOOKUP(G2:G5, A2:A9, E2:E9)'
        formula = ExcelFormula(formula_str, tables_list=[table], split_lines=False, target_cell='H2',
                               start_location=table.get_top() + 0.5 * UP, start_align=ORIGIN)
        hidden_data_mobs = [table.get_rows()[i][j] for i, j in hidden_data[:-3]]
        self.play(formula.write_to_scene(gap_between=0))
        self.wait(0.3)
        self.play(LaggedStart(*[Write(mob) for mob in hidden_data_mobs], lag_ratio=0.25))
        self.wait(2)
        self.play(formula.fade_out())
        self.wait(1)

        formula_str = '=XLOOKUP(G9, A2:A9, C2:D9)'
        formula = ExcelFormula(formula_str, tables_list=[table], split_lines=False, target_cell='H9',
                               start_location=table.get_top() + 0.5 * UP, start_align=ORIGIN)
        hidden_data_mobs = [table.get_rows()[i][j] for i, j in hidden_data[-3:-1]]
        self.play(formula.write_to_scene(gap_between=0))
        self.wait(0.3)
        self.play(LaggedStart(*[Write(mob) for mob in hidden_data_mobs], lag_ratio=0.25))
        self.wait(2)
        self.play(formula.fade_out())

        self.wait(3)

        lookup_data = [
            ['\\textbf{Name}', '\\textbf{Attribute}', '\\textbf{Value}'],
            ['Bill', 'Age', '24'],
            ['Rose', 'Profession', 'Shop Assistant'],
            ['Rory', 'Hometown', 'Leadworth'],
            ['Clara', 'Excel Skill', '5'],
            ['Martha', 'Profession', 'Doctor'],
        ]
        tex_data = [[Tex(data, color=BLACK) for data in row] for row in lookup_data]

        for i, row in enumerate(tex_data, start=2):
            for j, data in enumerate(row, start=8):
                data.scale(0.4)
                data.move_to(table.get_cell((i, j)).get_center())
                if j < 10 or i == 2:
                    self.add(data)

        for row in table.get_rows()[1:]:
            for i, cell in enumerate(row):
                if i < 7:
                    continue
                self.remove(cell)

        self.wait(2)
        hidden_data = [row[-1] for row in tex_data[1:]]

        formula_str = '=XLOOKUP(H2, $B$1:$E$1, \nXLOOKUP(G2, $A$2:$A$9, $B$2:$E$9))'
        formula = ExcelFormula(formula_str, tables_list=[table], split_lines=False, target_cell='I2')
        formula.next_to(table, UP, buff=0.3)
        formula.formula_box[1].move_to(formula).shift(UP * 0.02)
        # formula.formula_box[0].next_to(formula, DOWN).next_to(formula, RIGHT, coor_mask=np.array([0, 1, 0]))

        highlight_anim = table.get_passing_flash(range_str=formula.target_cell, flash_color=BLACK, stroke_width=2.5)
        type_anims = LaggedStart(highlight_anim, Transform(formula.formula_box[0], formula.formula_box[1]),
                                 lag_ratio=0.2)
        self.play(type_anims)

        all_animations = []
        i = 1
        tex_line = formula[1][:-1]
        tex: Tex
        for j, tex in enumerate(tex_line):
            t = min(len(tex.tex_string) * 0.2, 1.5)
            animations = [Write(tex).set_run_time(t)]
            if f'{i}:{j}' in formula.highlights:
                animations.append(Create(formula.highlights[f'{i}:{j}']).set_run_time(t))
            all_animations.append(AnimationGroup(*animations))
        self.play(Succession(*all_animations))

        self.wait(4)
        all_animations.clear()
        i = 0
        tex_line = formula[0]
        for j, tex in enumerate(tex_line):
            t = min(len(tex.tex_string) * 0.2, 1.5)
            animations = [Write(tex).set_run_time(t)]
            if f'{i}:{j}' in formula.highlights:
                animations.append(Create(formula.highlights[f'{i}:{j}']).set_run_time(t))
            all_animations.append(AnimationGroup(*animations))
        self.play(Succession(*all_animations))

        self.wait(0.7)
        self.play(Write(formula[1][-1]))
        self.wait(0.5)
        first_result = hidden_data.pop(0)
        self.play(Write(first_result))
        self.wait(0.5)
        write_results = LaggedStart(*[Write(mob) for mob in hidden_data], lag_ratio=0.25)
        self.play(table.animate_flash_fill(formula.target_cell, lagged_animations=[write_results]))
        self.wait(4)


class NotFoundExample(NarratedScene):
    def construct(self):
        title = Text('XLookup: Not Found').scale(0.85).to_edge(UP)
        self.play(Write(title))

        lookup_data = [
            ['\\textbf{Name}', '\\textbf{Excel Skill}'],
            ['Rory', '1'],
            ['Clara', '5'],
            ['Mickey', '\\verb|#|N\\verb|/|A'],
            ['Martha', '3'],
            ['Yasmin', '3']
        ]
        table_data = [base_table_data[i] + ([''] + lookup_data[i] if i < len(lookup_data)
                                            else [''] * (len(lookup_data[0]) + 1)) for i in range(len(base_table_data))]
        table = ExcelTable(table_data)
        table.scale(0.38).to_edge(DOWN).shift(DOWN * 0.2)
        self.wait(1)
        self.play(table.get_draw_animation())
        formula_str = '=XLOOKUP(G4, $A$2:$A$9, $D$2:$D$9)'
        formula = ExcelFormula(formula_str, tables_list=[table], split_lines=False, target_cell='H4')
        formula.next_to(table, UP, buff=0.35)
        formula.formula_box[1].move_to(formula).shift(UP * 0.02)
        self.wait(3)
        self.play(formula.write_to_scene())
        self.wait(4)

        mickey_score = table.get_rows()[4][8]
        formula_orig = formula.copy()
        formula_ifna = ExcelFormula(f'=IFNA({formula_str[1:]}, "")', tables_list=[table], split_lines=False,
                                    target_cell='H4', start_location=formula.get_center(), start_align=ORIGIN)
        self.play(TransformMatchingTex(formula, formula_ifna),
                  Transform(formula.formula_box[0], formula_ifna.formula_box[1]),
                  FadeOut(mickey_score))

        self.wait(3)
        formula_iferr = ExcelFormula(f'=IFERROR({formula_str[1:]}, "")', tables_list=[table], split_lines=False,
                                     target_cell='H4', start_location=formula.get_center(), start_align=ORIGIN)
        self.remove(formula.formula_box[0], formula_ifna.formula_box[1])
        self.play(TransformMatchingTex(formula_ifna, formula_iferr),
                  Transform(formula_ifna.formula_box[1], formula_iferr.formula_box[1]))
        self.wait(3)

        self.remove(formula_iferr.formula_box[1], formula_ifna.formula_box[1])
        self.play(TransformMatchingTex(formula_iferr, formula_orig),
                  Transform(formula.formula_box[1], formula_orig.formula_box[1]),
                  FadeIn(mickey_score))
        # self.remove(formula.formula_box[1])
        self.wait(4)

        not_founds = ['""', '"Unscored"', '0', 'AVERAGE($D$2:$D$9)']
        prev_formula = formula
        old_score = mickey_score
        for not_found in not_founds:
            if not_found == '""':
                new_score_tex = ''
            elif not_found == 'AVERAGE($D$2:$D$9)':
                new_score_tex = '2.75'
            elif not_found == '"Unscored"':
                new_score_tex = '``Unscored"'
            else:
                new_score_tex = not_found
            new_score = Tex(new_score_tex, color=BLACK).scale(0.4)
            new_score.move_to(table.get_cell((5, 9)).get_center())
            new_formula = ExcelFormula(f'{formula_str[:-1]}, {not_found})', tables_list=[table],
                                       split_lines=False, target_cell='H4', start_location=formula.get_center(),
                                       start_align=ORIGIN)
            self.remove(mickey_score, prev_formula, formula.formula_box[1], formula, formula_orig)
            anims = [TransformMatchingTex(prev_formula, new_formula),
                     Transform(formula.formula_box[1], new_formula.formula_box[1]),
                     FadeOut(old_score), FadeIn(new_score)]
            if not_found == not_founds[-1]:
                anims.append(Create(new_formula.highlight_objs[-1]))
            self.play(*anims)
            self.wait(1)
            old_score = new_score
            prev_formula = new_formula

        self.wait(3)


class NotFoundExample2(NarratedScene):
    def construct(self):
        title = Text('XLookup: Not Found').scale(0.85).to_edge(UP)
        self.play(Write(title))

        lookup_data = [
            ['\\textbf{Name}', '\\textbf{Excel Skill}'],
            ['Rory', '1'],
            ['Clara', '5'],
            ['Mickey', '\\verb|#|N\\verb|/|A'],
            ['Martha', '3'],
            ['Yasmin', '3']
        ]
        table_data = [base_table_data[i] + ([''] + lookup_data[i] if i < len(lookup_data)
                                            else [''] * (len(lookup_data[0]) + 1)) for i in range(len(base_table_data))]
        table = ExcelTable(table_data)
        table.scale(0.38).to_edge(DOWN).shift(DOWN * 0.2)
        self.wait(1)
        self.play(table.get_draw_animation())
        formula_str = '=XLOOKUP(G4, $A$2:$A$9, $D$2:$D$9)'
        formula = ExcelFormula(formula_str, tables_list=[table], split_lines=False, target_cell='H4')
        formula.next_to(table, UP, buff=0.35)
        formula.formula_box[1].move_to(formula).shift(UP * 0.02)
        self.wait(3)
        self.play(formula.write_to_scene())
        self.wait(4)

        mickey_score = table.get_rows()[4][8]
        formula_orig = formula.copy()
        formula_ifna = ExcelFormula(f'=IFNA({formula_str[1:]}, "")', tables_list=[table], split_lines=False,
                                    target_cell='H4', start_location=formula.get_center(), start_align=ORIGIN)
        self.play(TransformMatchingTex(formula, formula_ifna),
                  Transform(formula.formula_box[0], formula_ifna.formula_box[1]),
                  FadeOut(mickey_score))

        self.wait(3)
        formula_iferr = ExcelFormula(f'=IFERROR({formula_str[1:]}, "")', tables_list=[table], split_lines=False,
                                     target_cell='H4', start_location=formula.get_center(), start_align=ORIGIN)
        self.remove(formula.formula_box[0], formula_ifna.formula_box[1])
        self.play(TransformMatchingTex(formula_ifna, formula_iferr),
                  Transform(formula_ifna.formula_box[1], formula_iferr.formula_box[1]))
        self.wait(3)

        self.remove(formula_iferr.formula_box[1], formula_ifna.formula_box[1])
        self.play(TransformMatchingTex(formula_iferr, formula_orig),
                  Transform(formula.formula_box[1], formula_orig.formula_box[1]),
                  FadeIn(mickey_score))
        # self.remove(formula.formula_box[1])
        self.wait(4)

        not_founds = ['""', '"Unscored"', '0', 'AVERAGE($D$2:$D$9)']
        prev_formula = formula
        old_score = mickey_score
        for not_found in not_founds:
            if not_found == '""':
                new_score_tex = ''
            elif not_found == 'AVERAGE($D$2:$D$9)':
                new_score_tex = '2.75'
            elif not_found == '"Unscored"':
                new_score_tex = '``Unscored"'
            else:
                new_score_tex = not_found
            new_score = Tex(new_score_tex, color=BLACK).scale(0.4)
            new_score.move_to(table.get_cell((5, 9)).get_center())
            new_formula = ExcelFormula(f'{formula_str[:-1]}, {not_found})', tables_list=[table],
                                       split_lines=False, target_cell='H4', start_location=formula.get_center(),
                                       start_align=ORIGIN)
            self.remove(mickey_score, prev_formula, formula.formula_box[1], formula, formula_orig)
            anims = [TransformMatchingTex(prev_formula, new_formula),
                     Transform(formula.formula_box[1], new_formula.formula_box[1]),
                     FadeOut(old_score), FadeIn(new_score)]
            self.play(*anims)
            self.wait(1)
            old_score = new_score
            prev_formula = new_formula

        self.wait(3)


class XLookupReview(Scene):
    def construct(self):
        # Create and add table to the scene
        table = ExcelTable(XLookup_E01.lookup_table_data)
        table.scale(0.4).to_edge(RIGHT).shift(DOWN * 0.3)
        self.wait(1)

        # Create text objects for function names
        title = Tex('XLOOKUP').to_edge(UP)
        self.play(Write(title))
        self.wait(0.5)
        self.play(table.get_draw_animation())
        self.wait(2)


        formula_str = '=XLOOKUP("Rory", A2:A9, D2:D9)'
        formula = ExcelFormula(formula=formula_str, tables_list=[table])
        result = results_table([['1']], h_buff=2).scale(0.6).next_to(formula[-1], DOWN, buff=0.5)
        self.wait(1.5)
        self.play(formula.write_to_scene(gap_between=0))
        self.wait(0.5)
        self.play(Transform(formula.copy(), result))
        self.wait(10)
        # self.play(Unwrite(formula), Uncreate(formula.highlight_objs))



class SearchModesExample(NarratedScene):
    def construct(self):
        title = Text('XLookup: Search Mode').scale(0.85).to_edge(UP)
        self.play(Write(title))
        headers = ['\\textbf{Name}', '\\textbf{Year}', '\\textbf{Location}']
        visit_data = [
                ['Yasmin', '1903', 'New York, USA'],
                ['Rory', '2020', 'London, England'],
                ['Clara', '2020', 'London, England'],
                ['Martha', '1599', 'London, England'],
                ['Amy', '1890', 'Paris, France'],
                ['Rose', '1869', 'Cardiff, Wales'],
                ['Clara', '1207', 'Cumbria, England'],
                ['Martha', '1913', 'England'],
                ['Amy', '102', 'Roman Britain'],
                ['Rose', '1941', 'London, England'],
                ['Rory', '102', 'Roman Britain'],
                ['Amy', '2020', 'London, England'],
                ['Martha', '4100', 'Sanctuary Base 6'],
                ['Bill', '2017', 'Bristol, England'],
                ['Rory', '1890', 'Paris, France'],
                ['Bill', '1814', 'London, England'],
                ['Clara', '1893', 'Yorkshire, England'],
                ['Yasmin', '1300', 'Mongolia']
            ]
        visit_data = sorted(visit_data, key=lambda x: int(x[1]))
        table_data = [headers] + visit_data
        extra_data = [[''] * 3,
                      [''] * 3,
                      [''] * 3,
                      ['\\textbf{Most Recent}\n\r\\textbf{Visit}'] + [''] * 2,
                      ['\\textbf{Name}', '\\textbf{Year}', '\\textbf{Location}'],
                      ['Clara', '2020', 'London, England']
                      ]

        table_data = [table_data[i] + ([''] + extra_data[i] if i < len(extra_data) else [''] * 4)
                      for i in range(len(table_data))]


        table = ExcelTable(table_data).scale(0.25).to_corner(DL).shift(RIGHT*0.5+DOWN*0.3)
        hidden_cells = [(6,6),(6,7)]
        self.wait(5)
        self.play(table.get_draw_animation(hidden_data=hidden_cells), run_time=2.5)

        hidden_data = [table.get_rows()[i][j] for i, j in hidden_cells]
        formula_str = '=XLOOKUP(E6, A2:A19, C2:C19, , , -1)'
        formula = ExcelFormula(formula_str, tables_list=[table], target_cell='G6', start_align=LEFT + UP,
                               start_location=UP+RIGHT*1)

        self.play(formula.write_to_scene())
        self.play(LaggedStart(*[Write(mob) for mob in hidden_data], lag_ratio=0.2))
        self.wait(10)

class SearchModesBlank(NarratedScene):
    def construct(self):
        title = Text('XLookup: Search Mode').scale(0.85).to_edge(UP)
        self.add(title)
        self.wait(5)


class SearchModesExplained(NarratedScene):
    def construct(self):
        title = Text('XLookup: Search Mode').scale(0.85).to_edge(UP)
        self.add(title)

        def reset_rects(rects: VGroup, last_search: int = -1) -> None:
            rects.set_color(XKCD.COBALT)
            if last_search > 0:
                rects[last_search - 1].scale(1 / 1.2)

        def check_rect(rects: list[RoundedRectangle], is_match_list: list[bool], run_time_1: float, run_time_2: float) \
                -> list[Animation]:
            self.play(*[rect.animate.scale(1.2).set_color(YELLOW_E) for rect in rects], run_time=run_time_1 * 1.4)
            self.wait(run_time_2)
            new_colors = [EP_GREEN if is_match else RED for is_match in is_match_list]
            self.play(*[rect.animate.set_color(new_color) for rect, new_color in zip(rects, new_colors)], run_time=run_time_1)
            # self.wait(run_time_2)
            if any([not is_match for is_match in is_match_list]):
                return [rect.animate.scale(1 / 1.2) for rect, is_match in zip(rects, is_match_list) if not is_match]
            return []

        n_objs = 50
        r = RoundedRectangle(width=1, height=0.036, corner_radius=0.018, fill_color=XKCD.COBALT, fill_opacity=1,
                             color=XKCD.COBALT)

        linear_title = Tex('Linear Search').scale(0.8).shift(LEFT*2+UP*2.5)
        binary_title = Tex('Binary Search').scale(0.8).shift(RIGHT*2+UP*2.5)

        linear_rects = VGroup(*[r.copy() for _ in range(n_objs)]).arrange(DOWN, buff=0.08).next_to(linear_title, DOWN)
        binary_rects = linear_rects.copy().shift(RIGHT * 5).next_to(binary_title, DOWN)
        self.play(Write(linear_title), Write(binary_title))
        self.play(Create(linear_rects), Create(binary_rects), run_time=2.5)
        self.wait(3)

        targets = list(range(1, n_objs + 1))
        random.shuffle(targets)
        number_targets = 5
        lin_searches: Mobject
        bin_searches: Mobject
        searching_for = ValueTracker(0)

        # for i, search_target in enumerate(targets[:number_targets]):
        for i, search_target in enumerate([37, 5, 13, 2, 21]):
            search_title = always_redraw(lambda: VGroup(Text(f'Searching for').scale(0.6),
                                                        Integer().set_value(searching_for.get_value()).scale(0.7))
                                         .arrange(DOWN, buff=0.1))
            if i == 0 :
                self.play(Write(search_title))
            left = 0
            right = n_objs - 1
            binary_matched = False
            mid: int
            run_time_1 = 0.2
            run_time_2 = 0.05
            lin_checks = ValueTracker(0)
            bin_checks = ValueTracker(0)

            p1 = linear_rects.get_center() + LEFT * 1.3
            p2 = binary_rects.get_center() + RIGHT * 1.3

            lin_searches = always_redraw(lambda: VGroup(Integer().set_value(lin_checks.get_value()).scale(0.7),
                                                        Tex(' searches').scale(0.6)).arrange(DOWN, buff=0.1).move_to(p1))
            bin_searches = always_redraw(lambda: VGroup(Integer().set_value(bin_checks.get_value()).scale(0.7),
                                                        Tex(' searches').scale(0.6)).arrange(DOWN, buff=0.1).move_to(p2))

            self.play(searching_for.animate.set_value(search_target))
            self.play(Write(lin_searches), Write(bin_searches))
            for linear_n in range(search_target):
                lin_checks.increment_value(1)
                if not binary_matched:
                    bin_checks.increment_value(1)
                mid = (left + right) // 2
                linear_matched = linear_n == (search_target - 1)
                rectangles = [linear_rects[linear_n]] if binary_matched else [linear_rects[linear_n], binary_rects[mid]]
                matching = [linear_matched] if binary_matched else [linear_matched, mid == (search_target - 1)]

                final_anims = check_rect(rectangles, matching, run_time_1, run_time_2)
                binary_matched = mid == (search_target - 1)
                if not binary_matched:
                    # bin_checks.increment_value(1)
                    final_anims.append(AnimationGroup(*[rect.animate.set_color(GREY) for rect
                                                         in (binary_rects[:mid] if mid < search_target
                                                             else binary_rects[mid + 1:])
                                                        if rect.color == XKCD.COBALT]))
                    if mid < search_target:
                        left = mid + 1
                    else:
                        right = mid - 1

                if final_anims:
                    self.play(*final_anims, run_time=run_time_1)

            while not mid == (search_target - 1):
                bin_checks.increment_value(1)
                mid = (left + right) // 2
                rectangles = [binary_rects[mid]]
                matching = [mid == (search_target - 1)]
                final_anims = check_rect(rectangles, matching, run_time_1, run_time_2)
                if final_anims:
                    self.play(*final_anims, run_time=run_time_1)
                if mid < search_target:
                    left = mid + 1
                else:
                    right = mid - 1

            self.wait(0.8)
            self.remove(lin_searches, bin_searches)
            reset_rects(linear_rects, search_target)
            reset_rects(binary_rects, search_target)
            self.wait(0.5)


class MatchModeAlt(Scene):
    def construct(self):
        books_data = [
            ['\\textbf{Name}', '\\textbf{Author}', '\\textbf{Pages}'],
            ['The Great Gatsby', 'F. Scott Fitzgerald', 180],
            ['The Hobbit', 'J.R.R. Tolkien', 310],
            ['The Catcher in the Rye', 'J.D. Salinger', 230],
            ['War and Peace', 'Leo Tolstoy', 1225],
            ['The Very Hungry Caterpillar', 'Eric Carle', 32],
            ['The Grapes of Wrath', 'John Steinbeck', 528],
            ['The Odyssey', 'Homer', 416],
            ['The Gruffalo', 'Julia Donaldson', 32],
            ['Les Misérables', 'Victor Hugo', 1463],
            ['The Cat in the Hat', 'Dr. Seuss', 61],
            ['The Picture of Dorian Gray', 'Oscar Wilde', 254],
            ['The Tale of Peter Rabbit', 'Beatrix Potter', 56],
            ['Next', 'Michael Crichton', 507]
        ]

        scoring_data = [
            ['\\textbf{Book Length}', '\\textbf{Min Pages}', '\\textbf{Max Pages}'],
            ['Short', 0, 99],
            ['Medium', 100, 499],
            ['Long', 400, 999],
            ['Epic', 1000, 5000]
        ]

        title = Text('XLookup: Match Mode').scale(0.85).to_edge(UP)
        self.add(title)

        table_data = [
            books_data[i] + ['\\textbf{Book Length}' if i == 0 else categorise_book(books_data[i][-1])] + ['']
            + scoring_data[i] if i < len(scoring_data)
            else books_data[i] + [categorise_book(books_data[i][-1])]
                 + [''] * 4 for i in range(len(books_data))]

        table = ExcelTable(table_data)
        table.scale(0.3).to_edge(DOWN).shift(DOWN * 0.2)
        hidden_data = [(i, 4) for i in range(2, len(books_data) + 1)]
        self.add(table)
        self.remove(*[table.get_rows()[i][j] for i, j in hidden_data])
        self.wait(2)

        formula_str = '=IF(C2<$G$3, $F$2, IF(C2<$G$4, $F$3, IF(C2<$G$5, $F$4, $F$5)))'
        formula = ExcelFormula(formula_str, tables_list=[table], split_lines=False, target_cell='D2',
                               start_location=table.get_top() + 0.5 * UP, start_align=ORIGIN)
        self.wait(2)
        self.play(FadeIn(formula), FadeIn(formula.highlight_objs), FadeIn(formula.formula_box))
        formula_str = '=IFS(C2<$G$3, $F$2, C2<$G$4, $F$3, C2<$G$5, $F$4, TRUE, $F$5)'
        formula2 = ExcelFormula(formula_str, tables_list=[table], split_lines=False, target_cell='D2',
                               start_location=table.get_top() + 0.5 * UP, start_align=ORIGIN)
        self.wait(2)

        self.play(formula.transform_into(formula2))

        self.wait(2)
        self.remove(formula, *formula.highlights.values(), formula.formula_box,
                    formula2, *formula.highlights.values(), formula2.formula_box)

        tmp_form = formula2.copy()
        tmp = formula.highlight_objs
        tmp_box = formula.formula_box
        formula_str = '=INDEX($F$2:$F$5, SUM(--(C2>=$G$2:$G$5)))'
        formula = ExcelFormula(formula_str, tables_list=[table], split_lines=False, target_cell='D2',
                               start_location=table.get_top() + 0.5 * UP, start_align=ORIGIN)
        self.add(tmp_form)
        # anims = [TransformMatchingShapes(tmp[0], formula.highlight_objs[0]),
        #          TransformMatchingShapes(tmp[1], formula.highlight_objs[1]),
        #          *[FadeOut(mob) for mob in tmp[2:]],
        #          Transform(tmp_box, formula.formula_box)]
        self.play(tmp_form.transform_into(formula), Transform(tmp_box, formula.formula_box))
        self.wait(2)

        self.wait(2)