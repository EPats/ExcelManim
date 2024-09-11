import random

from manim import *

import excel_constants
import excel_tables
import excel_formula
import scenes

data = [
    ['\\textbf{Name}', '\\textbf{Year}', '\\textbf{Media}', '\\textbf{Tomato}\n\r\\textbf{Score}', '\\textbf{Main Hero}\n\r\\textbf{/Team}'],
    ['Iron Man', '2008', 'Movie', '94\\verb|%|', 'Iron Man'],
    ['The Incredible Hulk', '2008', 'Movie', '67\\verb|%|', 'Hulk'],
    ['Iron Man 2', '2010', 'Movie', '72\\verb|%|', 'Iron Man'],
    ['Thor', '2011', 'Movie', '77\\verb|%|', 'Thor'],
    ['Captain America: The First Avenger', '2011', 'Movie', '80\\verb|%|', 'Captain America'],
    ['The Avengers', '2012', 'Movie', '91\\verb|%|', 'The Avengers'],
    ['Iron Man 3', '2013', 'Movie', '79\\verb|%|', 'Iron Man'],
    ['Agents of S.H.I.E.L.D.', '2013', 'Tv', '95\\verb|%|', 'Agents of S.H.I.E.L.D'],
    ['Thor: The Dark World', '2013', 'Movie', '67\\verb|%|', 'Thor'],
    ['Captain America: The Winter Soldier', '2014', 'Movie', '90\\verb|%|', 'Captain America'],
    ['Guardians of the Galaxy', '2014', 'Movie', '92\\verb|%|', 'Guardians of the Galaxy'],
    ['Agent Carter', '2015', 'Tv', '86\\verb|%|', 'Agent Carter'],
    ['Daredevil', '2015', 'Tv', '92\\verb|%|', 'Daredevil'],
    ['Avengers: Age of Ultron', '2015', 'Movie', '76\\verb|%|', 'The Avengers'],
    ['Ant-Man', '2015', 'Movie', '83\\verb|%|', 'Ant-Man'],
    ['Jessica Jones', '2015', 'Tv', '83\\verb|%|', 'Jessica Jones'],
    ['Captain America: Civil War', '2016', 'Movie', '90\\verb|%|', 'The Avengers'],
    ['Ant-Man and The Wasp', '2018', 'Movie', '87\\verb|%|', 'Ant-Man and The Wasp'],
    ['Luke Cage', '2016', 'Tv', '87\\verb|%|', 'Luke Cage'],
    ['Doctor Strange', '2016', 'Movie', '89\\verb|%|', 'Doctor Strange'],
    ['Iron Fist', '2017', 'Tv', '37\\verb|%|', 'Iron Fist'],
    ['Guardians of the Galaxy Vol. 2', '2017', 'Movie', '85\\verb|%|', 'Guardians of the Galaxy'],
    ['Spider-Man: Homecoming', '2017', 'Movie', '92\\verb|%|', 'Spider-Man'],
    ['The Defenders', '2017', 'Tv', '78\\verb|%|', 'The Defenders'],
    ['Inhumans', '2017', 'Tv', '11\\verb|%|', 'The Inhumans'],
    ['Thor: Ragnarok', '2017', 'Movie', '93\\verb|%|', 'Thor'],
    ['The Punisher', '2017', 'Tv', '64\\verb|%|', 'The Punisher'],
    ['Runaways', '2017', 'Tv', '84\\verb|%|', 'The Runaways'],
    ['Black Panther', '2018', 'Movie', '96\\verb|%|', 'Black Panther'],
    ['Avengers: Infinity War', '2018', 'Movie', '85\\verb|%|', 'The Avengers'],
    ['Cloak and Dagger', '2018', 'Tv', '87\\verb|%|', 'Cloak and Dagger'],
    ['Captain Marvel', '2019', 'Movie', '79\\verb|%|', 'Captain Marvel'],
    ['Avengers: Endgame', '2019', 'Movie', '94\\verb|%|', 'The Avengers'],
    ['Spider-Man: Far From Home', '2019', 'Movie', '91\\verb|%|', 'Spider-Man'],
    ['WandaVision', '2021', 'Tv', '92\\verb|%|', 'Wanda/Vision'],
    ['The Falcon and the Winter Soldier', '2021', 'Tv', '85\\verb|%|', 'The Falcon/Winter Soldier'],
    ['Loki', '2021', 'Tv', '87\\verb|%|', 'Loki'],
    ['Black Widow', '2021', 'Movie', '79\\verb|%|', 'Black Widow'],
    ['What If...?', '2021', 'Tv', '89\\verb|%|', 'Various'],
    ['Shang-Chi and the Legend of the Ten Rings', '2021', 'Movie', '91\\verb|%|', 'Shang-Chi'],
    ['Eternals', '2021', 'Movie', '47\\verb|%|', 'The Eternals'],
    ['Hawkeye', '2021', 'Tv', '92\\verb|%|', 'Hawkeye'],
    ['Spider-Man: No Way Home', '2021', 'Movie', '93\\verb|%|', 'Spider-Man'],
    ['Moon Knight', '2022', 'Tv', '86\\verb|%|', 'Moon Knight'],
    ['Doctor Strange in the Multiverse of Madness', '2022', 'Movie', '74\\verb|%|', 'Doctor Strange'],
    ['Ms. Marvel', '2022', 'Tv', '98\\verb|%|', 'Ms. Marvel'],
    ['Thor: Love and Thunder', '2022', 'Movie', '63\\verb|%|', 'Thor'],
    ['I Am Groot', '2022', 'Tv', '88\\verb|%|', 'Groot'],
    ['She-Hulk: Attorney at Law', '2022', 'Tv', '79\\verb|%|', 'Jennifer Walters'],
    ['Werewolf by Night', '2022', 'Movie', '89\\verb|%|', 'Jack Russell'],
    ['Black Panther: Wakanda Forever', '2022', 'Movie', '84\\verb|%|', 'Shuri'],
    ['The Guardians of the Galaxy Holiday Special', '2022', 'Movie', '94\\verb|%|', 'Guardians of the Galaxy'],
    ['Ant-Man and The Wasp: Quantumania', '2023', 'Movie', '46\\verb|%|', 'Ant-Man and The Wasp'],
    ['Guardians of the Galaxy Vol. 3', '2023', 'Movie', '82\\verb|%|', 'Guardians of the Galaxy'],
    ['Secret Invasion', '2023', 'Tv', '52\\verb|%|', 'Nick Fury'],
    ['The Marvels', '2023', 'Movie', '62\\verb|%|', 'Captain Marvel/The Marvels'],
    ['Echo', '2024', 'Tv', '70\\verb|%|', 'Echo']
]
data = [[rw[0], rw[2], rw[1], *rw[3:]] for rw in data]


class DataTest(Scene):
    def construct(self):
        tab = excel_tables.ExcelTable(data)
        tab.scale(0.3)
        self.play(tab.get_draw_animation())
        self.wait()


class NotFound(Scene):
    def construct(self):
        title = Title('FILTER', match_underline_width_to_text=True)
        self.add(title)
        self.wait(3)

        sub_data = data[:20] + [data[-1]]
        sub_data = [line + (['Wonder Woman'] if i == 1 else ['']) for i, line in enumerate(sub_data)]
        hidden_cells = [(2, 6)]
        tab = excel_tables.ExcelTable(sub_data, broken_row_groups=[['58']])
        tscale = 0.2
        tab.scale(tscale)
        tab.to_edge(LEFT, buff=0.4)
        tab.shift(DOWN * 0.4)
        # hidden_data = [tab.get_rows()[i][j] for i, j in hidden_cells]
        self.play(tab.get_draw_animation(hidden_data=hidden_cells))
        self.wait(5)

        hero_tex = Tex('Batman', color=BLACK).scale(0.22)
        hero_tex.move_to(tab.get_cell((3,7)).get_center())

        formula_text = '=FILTER(A2:A58, E2:E58=F2)'
        result = [['\\verb|#|CALC']]
        sl = tab.get_corner(UR) + RIGHT * 0.6 + DOWN * 0.35
        formula = excel_formula.ExcelFormula(formula_text, tables_list=[tab], scale=0.6,
                                             start_location=sl, start_align=UL)
        result_table = excel_tables.results_table(result, results_title=False).scale(0.6)
        result_table.next_to(formula, DOWN, buff=0.5)
        result_table.align_to(formula, LEFT)

        self.play(Write(hero_tex))
        self.wait()
        self.play(formula.write_line_by_line())
        self.wait()
        self.play(FadeIn(result_table))
        self.wait(5)
        self.play(*[FadeOut(mob) for mob in [formula, result_table, *formula.highlights.values()]])
        self.wait(2)

        formula_text = formula_text[:-1] + ', "Does not appear\nin the MCU")'
        result = [['Does not appear\n\rin the MCU']]
        sl = tab.get_corner(UR) + RIGHT * 1.4 + DOWN * 0.35
        formula_a = formula.copy()
        formula = excel_formula.ExcelFormula(formula_text, tables_list=[tab], scale=0.6,
                                             start_location=sl, start_align=UL)
        formula.align_to(formula_a, LEFT)
        result_table = excel_tables.results_table(result, results_title=False).scale(0.6)
        result_table.next_to(formula, DOWN, buff=0.5)
        result_table.align_to(formula, LEFT)

        self.play(formula.write_line_by_line())
        self.wait()
        self.play(FadeIn(result_table))
        self.wait(5)
        self.play(*[FadeOut(mob) for mob in [formula, result_table, *formula.highlights.values()]])
        self.wait(2)

        formula_text = '=FILTER(A2:A58, E2:E58=F2, F2 & " does not appear\nin the MCU")'
        result = [['Batman does not\n\rappear in the MCU']]
        sl = tab.get_corner(UR) + RIGHT * 1.4 + DOWN * 0.35
        formula = excel_formula.ExcelFormula(formula_text, tables_list=[tab], scale=0.6,
                                             start_location=sl, start_align=UL)
        formula.align_to(formula_a, LEFT)
        result_table = excel_tables.results_table(result, results_title=False).scale(0.6)
        result_table.next_to(formula, DOWN, buff=0.5)
        result_table.align_to(formula, LEFT)

        self.play(formula.write_line_by_line())
        self.wait()
        self.play(FadeIn(result_table))
        self.wait(5)
        # self.play(*[FadeOut(mob) for mob in [formula, result_table, *formula.highlights.values()]])
        # self.wait(2)


        for hero in ['Superman', 'Wonder Woman']:
            tex = Tex(hero, color=BLACK).scale(0.22)
            tex.move_to(tab.get_cell((3, 7)).get_center())
            new_results = excel_tables.results_table([[f'{hero} does not\n\rappear in the MCU']],
                                                     results_title=False).scale(0.6)
            new_results.next_to(formula, DOWN, buff=0.5)
            new_results.align_to(formula, LEFT)
            self.play(hero_tex.animate.become(tex), result_table.animate.become(new_results))
            self.wait(2)


class FilterIntro(scenes.IntroScene):
    def __init__(self):
        super().__init__('=FILTER')

class percenttest(Scene):
    def construct(self):
        t = Tex("This is a 50% tex")
        self.play(Write(t))
        self.wait(4)
class Examples(Scene):
    def construct(self):
        def tv_logic(row):
            return row[1] == 'Tv'

        def avengers_logic(row):
            return row[4] == 'The Avengers'

        title = Title('FILTER', match_underline_width_to_text=True)
        self.add(title)
        self.wait(3)

        sub_data = data[:20] + [data[-1]]
        sub_data = [line + (['\\textbf{Helper}'] if i == 0 else [str(line[1] == 'Tv')]) for i, line in enumerate(sub_data)]
        hidden_cells = [(i, 6) for i in list(range(1, len(sub_data))) + [len(sub_data) + 1]]
        tab = excel_tables.ExcelTable(sub_data, broken_row_groups=[['58']])
        tscale = 0.2
        tab.scale(tscale)
        hidden_data = [tab.get_rows()[i][j] for i, j in hidden_cells]

        for d in hidden_data:
            d.set_opacity(0)

        self.play(tab.get_draw_animation(hidden_data=hidden_cells))
        self.wait(8)
        tmp = tab.copy()
        tmp.to_edge(LEFT, buff=0.4)
        tmp.shift(DOWN * 0.4)
        self.play(tab.animate.move_to(tmp.get_center()))
        self.wait(2)

        sl = tab.get_corner(UR) + RIGHT * 1.2 + DOWN * 0.35
        example = '=FILTER(A2:E58, B2:B58="Tv")'
        example_logic = tv_logic
        formula = excel_formula.ExcelFormula(example, tables_list=[tab], scale=0.6,
                                             start_location=sl)
        f1 = formula.copy()
        result_data = [row for row in data if example_logic(row)]
        result_table = excel_tables.results_table(result_data, results_title=False).scale(0.18)
        result_table.next_to(formula, DOWN, buff=0.2)
        result_table.align_to(formula, LEFT)
        # result_table.shift(RIGHT * 0.5)
        # result_table.align_to(formula, UP)

        self.play(formula.write_line_by_line())
        self.wait()
        self.play(FadeIn(result_table))
        self.wait(5)

        filter_logic = [['True' if example_logic(row) else '...' if row[2] == '...' else 'False'] for row in
                        sub_data[1:]]
        filter_logic_table = excel_tables.results_table(filter_logic, results_title=False).scale(0.2)
        filter_logic_table.next_to(tab.get_cell((13, 7)), RIGHT, buff=0.1)
        filter_logic_table.scale_to_fit_height(formula.highlight_objs[0].height)
        self.play(FadeIn(filter_logic_table), Indicate(formula[1][:-1]))
        self.wait(5)

        self.play(*[FadeOut(mob) for mob in [filter_logic_table, formula, result_table, *formula.highlights.values()]])
        self.wait(2)

        helper_formula_text = '=B2="Tv"'
        helper_formula = excel_formula.ExcelFormula(helper_formula_text, tables_list=[tab], scale=0.6, target_cell='F2', start_location=sl)
        helper_formula.shift(LEFT * 0.3)
        hidden_data = [d.copy().set_opacity(1) for d in hidden_data]
        self.play(Write(hidden_data.pop(0)))
        self.wait()
        self.play(helper_formula.write_line_by_line())
        self.play(Write(hidden_data[0]))
        self.wait()
        self.play(tab.animate_flash_fill(range_str='F2:F2', lagged_animations=[Write(d) for d in hidden_data[1:]], lag_ratio=0.075))
        self.wait(3)

        self.play(*[FadeOut(mob) for mob in [helper_formula, *helper_formula.highlights.values()]])
        self.wait()
        example = '=FILTER(A2:E58, F2:F58)'
        formula = excel_formula.ExcelFormula(example, tables_list=[tab], scale=0.6,
                                             start_location=sl)
        formula.align_to(f1, LEFT)
        self.play(formula.write_line_by_line())
        self.wait()
        self.play(FadeIn(result_table))
        self.wait(5)

        self.play(*[FadeOut(mob) for mob in [formula, result_table, *formula.highlights.values()] + hidden_data])

        #############################

        example = '=FILTER(A2:A58, E2:E58="The Avengers")'
        example_logic = avengers_logic
        formula = excel_formula.ExcelFormula(example, tables_list=[tab], scale=0.6,
                                             start_location=sl)
        formula.align_to(f1, LEFT)
        result_data = [[row[0]] for row in data if example_logic(row)]
        result_table = excel_tables.results_table(result_data, results_title=False).scale(0.3)
        result_table.next_to(formula, DOWN, buff=0.2)
        result_table.align_to(formula, LEFT)
        # result_table.shift(RIGHT * 0.5)

        self.play(formula.write_line_by_line())
        self.wait()
        self.play(FadeIn(result_table))
        self.wait(2)

        filter_logic = [['True' if example_logic(row) else '...' if row[2] == '...' else 'False'] for row in
                        sub_data[1:]]
        filter_logic_table = excel_tables.results_table(filter_logic, results_title=False).scale(0.2)
        filter_logic_table.next_to(tab.get_cell((13, 7)), RIGHT, buff=0.1)
        filter_logic_table.scale_to_fit_height(formula.highlight_objs[0].height)
        self.play(FadeIn(filter_logic_table), Indicate(formula[1][:-1]))
        self.wait(5)

        self.play(*[FadeOut(mob) for mob in [filter_logic_table, formula, result_table, *formula.highlights.values()]])
        self.wait(2)

        #############################

        def complex_and_logic(row):
            return row[1] == 'Movie' and '{' not in row[2] and '{' not in row[3] and int(row[2]) > 2015 and int(
                row[3][:-8]) >= 90

        example = '=AND(B2="Movie",\nC2>2015,\nD2>=0.9)'
        example_logic = complex_and_logic
        filter_logic = [['True' if example_logic(row) else '...' if row[2] == '...' else 'False'] for row in
                        sub_data[1:]]
        tmp_data = [line if i < 0 else line[:-1] + filter_logic[i] for i, line in enumerate(sub_data, start=-1)]
        # tmp_data[-1][-1] = 'False'
        tmp_data = [line for line in tmp_data if not line[0] == '...']
        tmp_table = excel_tables.ExcelTable(tmp_data, broken_row_groups=[['58']])
        tmp_table.scale(tscale)
        tmp_table.move_to(tab)

        helper_formula_text = example
        helper_formula = excel_formula.ExcelFormula(helper_formula_text, tables_list=[tab], scale=0.6, target_cell='F2',
                                             start_location=sl)
        helper_formula.align_to(f1, LEFT)
        hidden_data = [tmp_table.get_rows()[i][j] for i, j in hidden_cells]
        hidden_data.pop(0)
        # self.play(Write(hidden_data.pop(0)))
        # self.wait()
        self.play(helper_formula.write_line_by_line())
        self.play(Write(hidden_data[0]))
        self.wait()
        self.play(tab.animate_flash_fill(range_str='F2', lagged_animations=[Write(d) for d in hidden_data[1:]], lag_ratio=0.075))
        self.wait(3)

        self.play(*[FadeOut(mob) for mob in [helper_formula, *helper_formula.highlights.values()]])
        self.wait()
        example = '=FILTER(A2:E58, F2:F58)'
        formula = excel_formula.ExcelFormula(example, tables_list=[tab], scale=0.6,
                                             start_location=sl)
        formula.align_to(f1, LEFT)
        result_data = [[row[0]] for row in data if example_logic(row)]
        result_table = excel_tables.results_table(result_data, results_title=False).scale(0.3)
        result_table.next_to(formula, DOWN, buff=0.2)
        result_table.align_to(formula, LEFT)
        # result_table.shift(RIGHT * 0.5)

        self.play(formula.write_line_by_line())
        self.wait()
        self.play(FadeIn(result_table))
        self.wait(5)

        self.play(*[FadeOut(mob) for mob in [formula, result_table, *formula.highlights.values()] + hidden_data])

        self.wait(5)

        example = '=FILTER(A2:A58,\n(B2:B58="Movie") *\n(C2:C58>2015) *\n(D2:D58>=0.9))'
        example_logic = complex_and_logic
        formula = excel_formula.ExcelFormula(example, tables_list=[tab], scale=0.6,
                                             start_location=sl)
        formula.align_to(f1, LEFT)
        result_data = [[row[0]] for row in data if example_logic(row)]
        result_table = excel_tables.results_table(result_data, results_title=False).scale(0.3)
        result_table.next_to(formula, DOWN, buff=0.2)
        result_table.align_to(formula, LEFT)
        # result_table.shift(RIGHT * 0.5)
        # result_table.align_to(formula, UP)

        self.play(formula.write_line_by_line())
        self.wait()
        self.play(FadeIn(result_table))
        self.wait(2)

        filter_logic = [['True' if example_logic(row) else '...' if row[2] == '...' else 'False'] for row in
                        sub_data[1:]]
        filter_logic_table = excel_tables.results_table(filter_logic, results_title=False).scale(0.2)
        filter_logic_table.next_to(tab.get_cell((13, 7)), RIGHT, buff=0.1)
        filter_logic_table.scale_to_fit_height(formula.highlight_objs[0].height)
        self.play(FadeIn(filter_logic_table))
        self.wait(5)

        self.play(*[FadeOut(mob) for mob in [filter_logic_table, formula, result_table, *formula.highlights.values()]])
        self.wait(2)

        #############################

        def complex_or_logic(row):
            return '{' not in row[2] and '.' not in row[2] and int(row[2]) > 2015 and row[4] in ['The Avengers', 'Spider-Man']

        helper_formula_text = '=OR(E2="The Avengers",E2="Spider-Man")'
        helper_formula = excel_formula.ExcelFormula(helper_formula_text, tables_list=[tab], scale=0.6,
                                             start_location=sl)
        helper_formula.align_to(f1, LEFT)

        tmp_data = [line if i < 0 else line[:-1] + filter_logic[i] for i, line in enumerate(sub_data, start=-1)]
        # tmp_data[-1][-1] = 'False'
        tmp_data = [line for line in tmp_data if not line[0] == '...']
        tmp_table = excel_tables.ExcelTable(tmp_data, broken_row_groups=[['58']])
        tmp_table.scale(tscale)
        tmp_table.move_to(tab)
        hidden_data = [tmp_table.get_rows()[i][j] for i, j in hidden_cells]
        hidden_data.pop(0)

        example = '=FILTER(A2:A58, F2:F58)'
        formula = excel_formula.ExcelFormula(example, tables_list=[tab], scale=0.6,
                                             start_location=sl)
        formula.align_to(f1, LEFT)
        example_logic = complex_or_logic

        result_data = [[row[0]] for row in data if example_logic(row)]
        result_table = excel_tables.results_table(result_data, results_title=False).scale(0.3)
        result_table.next_to(formula, DOWN, buff=0.2)
        result_table.align_to(formula, LEFT)
        # result_table.shift(RIGHT * 0.5)
        # result_table.align_to(formula, UP)
        # self.play(Write(hidden_data.pop(0)))
        # self.wait()
        self.play(helper_formula.write_line_by_line())
        self.play(Write(hidden_data[0]))
        self.wait()
        self.play(tab.animate_flash_fill(range_str='F2', lagged_animations=[Write(d) for d in hidden_data[1:]], lag_ratio=0.075))
        self.wait(3)

        self.play(*[FadeOut(mob) for mob in [helper_formula, *helper_formula.highlights.values()]])
        self.wait(2)

        self.play(formula.write_line_by_line())
        self.wait()
        self.play(FadeIn(result_table))
        self.wait(5)

        self.play(*[FadeOut(mob) for mob in [formula, result_table, *formula.highlights.values()] + hidden_data])

        self.wait(2)

        example = '=FILTER(A2:A58, (E2:E58="The Avengers") +\n(E2:E58="Spider-Man"))'
        formula = excel_formula.ExcelFormula(example, tables_list=[tab], scale=0.6,
                                             start_location=sl)
        formula.align_to(f1, LEFT)
        self.play(formula.write_line_by_line())
        result_table.next_to(formula, DOWN, buff=0.2)
        result_table.align_to(formula, LEFT)
        # self.wait()
        self.play(FadeIn(result_table))
        self.wait(2)

        filter_logic = [['True' if example_logic(row) else '...' if row[2] == '...' else 'False'] for row in
                        sub_data[1:]]
        filter_logic_table = excel_tables.results_table(filter_logic, results_title=False).scale(0.2)
        filter_logic_table.next_to(tab.get_cell((13, 7)), RIGHT, buff=0.1)
        filter_logic_table.scale_to_fit_height(formula.highlight_objs[0].height)
        self.wait(5)

        self.play(*[FadeOut(mob) for mob in [formula, result_table, *formula.highlights.values()]])
        self.wait(2)

class ExamplesOld(Scene):
    def construct(self):
        def tv_logic(row):
            return row[1] == 'Tv'

        def avengers_logic(row):
            return row[4] == 'The Avengers'


        title = Title('FILTER', match_underline_width_to_text=True)
        self.add(title)
        self.wait(3)

        sub_data = data[:20] + [data[-1]]
        tab = excel_tables.ExcelTable(sub_data, broken_row_groups=[['58']])
        tab.scale(0.2).to_edge(LEFT, buff=0.25)
        tab.shift(DOWN * 0.2)
        self.play(tab.get_draw_animation())
        self.wait()

        sl = tab.get_corner(UR) + RIGHT * 0.8 + DOWN * 0.5
        example = '=FILTER(A2:E58, B2:B58="Tv")'
        example_logic = tv_logic
        formula = excel_formula.ExcelFormula(example, tables_list=[tab], scale=0.6,
                                                   start_location=sl)
        result_data = [row for row in data if example_logic(row)]
        result_table = excel_tables.results_table(result_data, results_title=False).scale(0.18)
        result_table.next_to(formula, RIGHT, buff=0.2)
        result_table.align_to(formula, UP)

        self.play(formula.write_line_by_line())
        self.wait()
        self.play(FadeIn(result_table))
        self.wait(2)

        filter_logic = [['True' if example_logic(row) else '...' if row[2] == '...' else 'False'] for row in sub_data[1:]]
        filter_logic_table = excel_tables.results_table(filter_logic, results_title=False).scale(0.2)
        filter_logic_table.next_to(tab.get_cell((13, 6)), RIGHT, buff=0.1)
        filter_logic_table.scale_to_fit_height(formula.highlight_objs[0].height)
        self.play(FadeIn(filter_logic_table), Indicate(formula[1][:-1]))
        self.wait(5)

        self.play(*[FadeOut(mob) for mob in [filter_logic_table, formula, result_table, *formula.highlights.values()]])
        self.wait(2)

        #############################

        example = '=FILTER(A2:A58, E2:E58="The Avengers")'
        example_logic = avengers_logic
        formula = excel_formula.ExcelFormula(example, tables_list=[tab], scale=0.6,
                                             start_location=sl)
        result_data = [[row[0]] for row in data if example_logic(row)]
        result_table = excel_tables.results_table(result_data, results_title=False).scale(0.3)
        result_table.next_to(formula, RIGHT, buff=0.2)
        result_table.align_to(formula, UP)

        self.play(formula.write_line_by_line())
        self.wait()
        self.play(FadeIn(result_table))
        self.wait(2)

        filter_logic = [['True' if example_logic(row) else '...' if row[2] == '...' else 'False'] for row in
                        sub_data[1:]]
        filter_logic_table = excel_tables.results_table(filter_logic, results_title=False).scale(0.2)
        filter_logic_table.next_to(tab.get_cell((13, 6)), RIGHT, buff=0.1)
        filter_logic_table.scale_to_fit_height(formula.highlight_objs[0].height)
        self.play(FadeIn(filter_logic_table), Indicate(formula[1][:-1]))
        self.wait(5)

        self.play(*[FadeOut(mob) for mob in [filter_logic_table, formula, result_table, *formula.highlights.values()]])
        self.wait(2)

        #############################

        def complex_and_logic(row):
            return row[1] == 'Movie' and '{' not in row[2] and '{' not in row[3] and int(row[2]) > 2015 and int(row[3][:-8]) >= 90

        example = '=FILTER(A2:A58, (B2:B58="Movie") *\n(C2:C58>2015) *\n(D2:D58>=90%))'
        example_logic = complex_and_logic
        formula = excel_formula.ExcelFormula(example, tables_list=[tab], scale=0.6,
                                             start_location=sl)
        result_data = [[row[0]] for row in data if example_logic(row)]
        result_table = excel_tables.results_table(result_data, results_title=False).scale(0.3)
        result_table.next_to(formula, RIGHT, buff=0.2)
        result_table.align_to(formula, UP)

        self.play(formula.write_line_by_line())
        self.wait()
        self.play(FadeIn(result_table))
        self.wait(2)

        filter_logic = [['True' if example_logic(row) else '...' if row[2] == '...' else 'False'] for row in
                        sub_data[1:]]
        filter_logic_table = excel_tables.results_table(filter_logic, results_title=False).scale(0.2)
        filter_logic_table.next_to(tab.get_cell((13, 6)), RIGHT, buff=0.1)
        filter_logic_table.scale_to_fit_height(formula.highlight_objs[0].height)
        self.play(FadeIn(filter_logic_table), Indicate(formula[1][:-1]))
        self.wait(5)

        self.play(*[FadeOut(mob) for mob in [filter_logic_table, formula, *formula.highlights.values()]])
        example = ('=FILTER(A2:A58,\nBYROW(B2:D58,\nLAMBDA(rw,\n'
                   'AND(\nINDEX(rw, 1)="Movie",\nINDEX(rw, 2)>2015,\nINDEX(rw, 3)>=90%\n))))')
        formula = excel_formula.ExcelFormula(example, tables_list=[tab], split_lines=False, scale=0.6,
                                             start_location=sl)
        self.play(formula.write_line_by_line())#, result_table.animate.next_to(formula, DOWN, buff=0.1))

        self.play(*[FadeOut(mob) for mob in [filter_logic_table, formula, result_table, *formula.highlights.values()]])
        self.wait(2)

        #############################

        def complex_or_logic(row):
            return row[1] == 'Movie' and '{' not in row[2] and int(row[2]) > 2015 and row[4] in ['The Avengers',
                                                                                                 'Spider-Man']

        example = '=FILTER(A2:A58, (B2:B58="Movie") *\n(E2:E58="The Avengers" +\nE2:E58="Spider-Man"))'
        example_logic = complex_or_logic
        formula = excel_formula.ExcelFormula(example, tables_list=[tab], scale=0.6,
                                             start_location=sl)
        result_data = [[row[0]] for row in data if example_logic(row)]
        result_table = excel_tables.results_table(result_data, results_title=False).scale(0.3)
        result_table.next_to(formula, RIGHT, buff=0.2)
        result_table.align_to(formula, UP)

        self.play(formula.write_line_by_line())
        self.wait()
        self.play(FadeIn(result_table))
        self.wait(2)

        filter_logic = [['True' if example_logic(row) else '...' if row[2] == '...' else 'False'] for row in
                        sub_data[1:]]
        filter_logic_table = excel_tables.results_table(filter_logic, results_title=False).scale(0.2)
        filter_logic_table.next_to(tab.get_cell((13, 6)), RIGHT, buff=0.1)
        filter_logic_table.scale_to_fit_height(formula.highlight_objs[0].height)
        self.play(FadeIn(filter_logic_table), Indicate(formula[1][:-1]))
        self.wait(5)

        self.play(*[FadeOut(mob) for mob in [filter_logic_table, formula, *formula.highlights.values()]])
        example = ('=FILTER(A2:A58,\nBYROW(B2:E58,\nLAMBDA(rw,\n'
                   'AND(\nINDEX(rw, 1)="Movie",\nOR(\nINDEX(rw, 4)="The Avengers",'
                   '\nINDEX(rw, 4)="Spider-Man"\n)))))')

        formula = excel_formula.ExcelFormula(example, tables_list=[tab], split_lines=False, scale=0.6,
                                             start_location=sl)
        self.play(formula.write_line_by_line())#, result_table.animate.next_to(formula, DOWN, buff=0.1))

        self.play(*[FadeOut(mob) for mob in [filter_logic_table, formula, result_table, *formula.highlights.values()]])
        self.wait(2)




class FilterIntro(scenes.IntroScene):
    def __init__(self):
        super().__init__('FILTER Function')


class BooleanLogic(Scene):
    def construct(self):
        lines = [
            [False, False, False],
            [True, False, False],
            [False, True, False],
            [False, False, True],
            [True, True, False],
            [True, False, True],
            [False, True, True],
            [True, True, True]
        ]

        str_lines = [[f'{" * ".join(str(line_el) for line_el in line)}', ' = ',
                      f'{" * ".join(str(1 if line_el else 0) for line_el in line)}', ' = ',
                      f'{str(1 if all(line) else 0)}', '\n\r'] for line in lines]
        tex_mob = Tex(*[tex_el for line in str_lines for tex_el in line])

        true_col = excel_constants.EP_EXCEL_GREEN
        false_col = XKCD.INDIANRED
        for i, sub_mob in enumerate(tex_mob):
            if i < 6:
                sub_mob.shift(LEFT * (5 - i) * 0.2)
            else:
                sub_mob.next_to(tex_mob[i % 6], DOWN, coor_mask=np.array([1, 0, 0]))
            if i % 6 == 4:
                sub_mob.set_color(true_col if i > 45 else false_col)
        self.play(LaggedStart(*[Write(tex_mob[i:i + 6]) for i in range(0, 48, 6)], lag_ratio=0.35))
        self.wait(2)


class BooleanLogicAdd(Scene):
    def construct(self):
        lines = [
            [False, False],
            [True, False],
            [False, True],
            [True, True]
        ]

        str_lines = [[f'{" + ".join(str(line_el) for line_el in line)}', ' = ',
                      f'{" + ".join(str(1 if line_el else 0) for line_el in line)}', ' = ',
                      f'{str(2 if all(line) else 1 if any(line) else 0)}', '\n\r'] for line in lines]
        tex_mob = Tex(*[tex_el for line in str_lines for tex_el in line])

        true_col = excel_constants.EP_EXCEL_GREEN
        false_col = XKCD.INDIANRED
        for i, sub_mob in enumerate(tex_mob):
            if i < 6:
                sub_mob.shift(LEFT * (5 - i) * 0.2)
            else:
                sub_mob.next_to(tex_mob[i % 6], DOWN, coor_mask=np.array([1, 0, 0]))
            if i % 6 == 4:
                sub_mob.set_color(true_col if i > 6 else false_col)
        self.play(LaggedStart(*[Write(tex_mob[i:i + 6]) for i in range(0, 48, 6)], lag_ratio=0.35))
        self.wait(2)


class FilterErrors(Scene):
    def construct(self):
        title = Title('FILTER', match_underline_width_to_text=True).scale(1.2)
        self.play(Write(title))
        self.wait(2)

        filter_formula = excel_formula.ExcelFormula('=FILTER(array, include, [if_empty])', scale=1)
        filter_formula.to_edge(LEFT).shift(DOWN * 0.3 + RIGHT * 0.4)
        self.play(filter_formula.write_anim_with_required_arguments_only())
        self.wait(10)

        colours = [
            XKCD.LIGHTBLUEGREY,
            XKCD.STEELBLUE,
            XKCD.LIGHTBLUE,
            XKCD.SLATE,
            XKCD.LIGHTPERIWINKLE,
            XKCD.DARKGREYBLUE,
            XKCD.DARK
        ]

        data_n = 30
        r = 6
        c = data_n // r
        data = VGroup(*[Square(fill_color=colours[i % len(colours)],
                               color=BLACK,
                               fill_opacity=1) for i in range(data_n)])
        data.arrange_in_grid(rows=r, cols=c, buff=0)
        s = 0.225
        data.scale(s)
        data.align_to(filter_formula, UP)
        data.shift(RIGHT * 0.1 + UP * 0.2)
        self.play(LaggedStart(*[DrawBorderThenFill(s, run_time=0.5) for s in data], lag_ratio=0.05))

        vertical_filter = [True, False, False, True, False, True, False, True, True]
        true_col = excel_constants.EP_EXCEL_GREEN
        false_col = XKCD.INDIANRED

        v_f = VGroup(*[Square(fill_color=true_col if val else false_col,
                              color=BLACK,
                              fill_opacity=1) for val in vertical_filter])
        v_f.arrange(DOWN, buff=0).scale(s)

        plus = Tex('+')
        eq = Tex('=')

        plus.next_to(data, RIGHT)

        self.wait()
        self.play(Write(plus))
        self.wait()
        v_f.next_to(plus, RIGHT)
        v_f.align_to(data, UP)
        eq.next_to(plus, RIGHT, buff=1)
        self.play(Create(v_f))
        self.wait()
        self.play(Write(eq))
        self.wait()
        result_tex = Tex('\\verb|#|VALUE')
        result_tex.next_to(eq)
        self.play(Write(result_tex))
        self.wait(2)

        self.play(*[FadeOut(mob) for mob in [plus, eq, v_f, result_tex]])

        vertical_filter = [True, False, False, "e", False, True]
        true_col = excel_constants.EP_EXCEL_GREEN
        false_col = XKCD.INDIANRED

        v_f = VGroup(*[Square(fill_color=ORANGE if val == "e" else true_col if val else false_col,
                              color=BLACK,
                              fill_opacity=1) for val in vertical_filter])
        v_f.arrange(DOWN, buff=0).scale(s)
        self.wait()
        self.play(Write(plus))
        self.wait()
        v_f.next_to(plus, RIGHT)
        eq.next_to(v_f, RIGHT)
        self.play(Create(v_f))
        self.wait()
        self.play(Write(eq))
        self.wait()
        result_tex = Tex('\\verb|#|DIV/0')
        result_tex.next_to(eq)
        self.play(Write(result_tex))
        self.wait(2)

        self.play(*[FadeOut(mob) for mob in [plus, eq, v_f, result_tex]])

        vertical_filter = [False, False, False, False, False, False]
        true_col = excel_constants.EP_EXCEL_GREEN
        false_col = XKCD.INDIANRED

        v_f = VGroup(*[Square(fill_color=false_col,
                              color=BLACK,
                              fill_opacity=1) for _ in vertical_filter])
        v_f.arrange(DOWN, buff=0).scale(s)
        self.wait()
        self.play(Write(plus))
        self.wait()
        v_f.next_to(plus, RIGHT)
        eq.next_to(v_f, RIGHT)
        self.play(Create(v_f))
        self.wait()
        self.play(Write(eq))
        self.wait()
        result_tex = Tex('\\verb|#|CALC')
        result_tex.next_to(eq)
        self.play(Write(result_tex))
        self.wait(2)

        self.wait(2)

        self.play(filter_formula.reveal_anim_optional_args())
        self.wait(2)

class FilterDefine(Scene):
    def construct(self):
        title = Title('FILTER', match_underline_width_to_text=True).scale(1.2)
        self.play(Write(title))
        self.wait(2)

        filter_formula = excel_formula.ExcelFormula('=FILTER(array, include, [if_empty])', scale=1)
        filter_formula.to_edge(LEFT).shift(DOWN * 0.3 + RIGHT * 0.4)
        self.play(filter_formula.write_anim_with_required_arguments_only())
        self.wait(10)

        colours = [
            XKCD.LIGHTBLUEGREY,
            XKCD.STEELBLUE,
            XKCD.LIGHTBLUE,
            XKCD.SLATE,
            XKCD.LIGHTPERIWINKLE,
            XKCD.DARKGREYBLUE,
            XKCD.DARK
        ]

        data_n = 30
        r = 6
        c = data_n // r
        data = VGroup(*[Square(fill_color=colours[i % len(colours)],
                               color=BLACK,
                               fill_opacity=1) for i in range(data_n)])
        data.arrange_in_grid(rows=r, cols=c, buff=0)
        s = 0.225
        data.scale(s)
        data.align_to(filter_formula, UP)
        data.shift(RIGHT * 0.1 + UP * 0.2)
        self.play(LaggedStart(*[DrawBorderThenFill(s, run_time=0.5) for s in data], lag_ratio=0.05))

        vertical_filter = [True, False, False, True, False, True]
        horizontal_filter = [False, True, False, True, True]
        true_col = excel_constants.EP_EXCEL_GREEN
        false_col = XKCD.INDIANRED

        v_f = VGroup(*[Square(fill_color=true_col if val else false_col,
                               color=BLACK,
                               fill_opacity=1) for val in vertical_filter])
        h_f = VGroup(*[Square(fill_color=true_col if val else false_col,
                               color=BLACK,
                               fill_opacity=1) for val in horizontal_filter])
        v_f.arrange(DOWN, buff=0).scale(s)
        h_f.arrange(RIGHT, buff=0).scale(s)

        v_result = VGroup()
        h_result = VGroup()
        print(f'{vertical_filter=}, {horizontal_filter=}')
        for i, s in enumerate(data):
            if vertical_filter[i // c]:
                v_result.add(s.copy())

            if horizontal_filter[i % c]:
                h_result.add(s.copy())

        plus = Tex('+')
        plus_copy = plus.copy()
        eq = Tex('=')
        eq_copy = eq.copy()

        plus.next_to(data, RIGHT)
        plus_copy.next_to(data, DOWN)
        plus_copy.shift(DOWN * 1 + LEFT * 0.25)

        self.wait()
        self.play(Write(plus))
        self.wait()
        v_f.next_to(plus, RIGHT)
        eq.next_to(v_f, RIGHT)
        self.play(Create(v_f))
        self.wait()
        self.play(Write(eq))
        self.wait()
        self.play(v_result.animate(rate_func=there_and_back).set_fill(true_col))
        self.wait()
        v_result_copy = v_result.copy()
        v_result_copy.arrange_in_grid(cols=c, buff=0)
        v_result_copy.next_to(eq, RIGHT)
        self.play(Transform(v_result, v_result_copy))
        self.wait()

        self.wait(2)

        self.play(Write(plus_copy))
        self.wait()
        h_f.next_to(plus_copy, RIGHT)
        eq_copy.next_to(h_f, RIGHT)
        self.play(Create(h_f))
        self.wait()
        self.play(Write(eq_copy))
        self.wait()
        self.play(h_result.animate(rate_func=there_and_back).set_fill(true_col))
        self.wait()
        h_result_copy = h_result.copy()
        h_result_copy.arrange_in_grid(rows=r, buff=0)
        h_result_copy.next_to(eq_copy, RIGHT)
        self.play(Transform(h_result, h_result_copy))
        self.wait()

        self.wait(2)

        self.play(filter_formula.reveal_anim_optional_args())
        self.wait(2)