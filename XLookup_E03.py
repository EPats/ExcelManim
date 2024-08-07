from manim import *

import excel_formula
from excel_formula import *
from excel_tables import *
from scenes import NarratedScene


class HelperLookups(Scene):
    def construct(self):
        title = Text("Helper Lookups").scale(0.85).to_edge(UP)
        title.z_index = 1
        self.play(Write(title))

        table_data = [
            ['\\textbf{Name}', '\\textbf{Year}', '\\textbf{Location}'],
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

        extra_data = [[''] * 3,
                      [''] * 3,
                      [''] * 3,
                      [''] * 3,
                      ['\\textbf{Name}', '\\textbf{Year}', '\\textbf{Location}'],
                      ['Clara', '1893', 'Yorkshire, England']
                      ]

        table_data = [table_data[i] + ([''] if i == 0 else [table_data[i][0] + table_data[i][1]])
                      + (extra_data[i] if i < len(extra_data) else [''] * 3)
                      for i in range(len(table_data))]

        table = ExcelTable(table_data).scale(0.25).to_corner(DL).shift(RIGHT * 0.5)
        hidden_cells = [(6, 7)] + [(i, 4) for i in range(1, len(table_data) + 1)]
        hidden_data = [table.get_rows()[i][j] for i, j in hidden_cells]
        self.play(table.get_draw_animation(hidden_data=hidden_cells), run_time=2.5)

        result_cells = hidden_cells.pop(0)
        result = hidden_data.pop(0)

        wrong_result = [row for row in table_data if row[0] == 'Clara'][0][2]
        wrong_result_tex = (Tex(wrong_result, color=BLACK).scale(0.25)
                            .move_to(table.get_rows()[result_cells[0]][result_cells[1]].get_center()))

        formula_str = '=XLOOKUP(E6, A2:A19, C2:C19)'
        formula = ExcelFormula(formula_str, tables_list=[table], target_cell='G6', start_align=LEFT + UP,
                               start_location=UP + RIGHT * 1.5)
        formula_str_2 = '=XLOOKUP(E6&F6, A2:A19&B2:B19, C2:C19)'
        formula_2 = ExcelFormula(formula_str_2, tables_list=[table], target_cell='G6', start_align=LEFT + UP,
                                 start_location=UP + RIGHT * 1.5)

        tmp_formula_str = '=A2:A19 & B2:B19'
        tmp_formula = ExcelFormula(tmp_formula_str, tables_list=[table], target_cell='D2', start_align=LEFT + UP,
                                   start_location=UP + RIGHT * 0.5)
        tmp_formula.align_to(formula, LEFT)
        tmp_formula.formula_box[1].move_to(tmp_formula).shift(UP * 0.02)

        write_helper = LaggedStart(*[Write(data) for data in hidden_data], lag_ratio=0.05)
        unwrite_helper = LaggedStart(*[Unwrite(data) for data in hidden_data], lag_ratio=0.05)

        self.play(formula.write_to_scene())
        self.wait(0.2)
        self.play(Write(wrong_result_tex))
        self.wait(2)
        self.play(Unwrite(wrong_result_tex), Unwrite(formula), Uncreate(formula.highlight_objs),
                  Uncreate(formula.formula_box))
        self.wait(2)

        self.play(tmp_formula.write_to_scene())
        self.wait(0.2)
        self.play(write_helper)
        self.wait(3)
        self.play(unwrite_helper, Unwrite(tmp_formula), Uncreate(tmp_formula.highlight_objs),
                  Uncreate(tmp_formula.formula_box))
        self.wait(2)

        self.play(formula_2.write_to_scene())
        self.wait(0.2)
        self.play(Write(result))
        self.wait(2)


class ExactExplainer(NarratedScene):
    def construct(self):
        title = Text("Case-Sensitive Lookups").scale(0.85).to_edge(UP)
        title.z_index = 1
        self.play(Write(title))

        tardis_data = [
            ['\\textbf{TARDIS Id}', '\\textbf{Name}'],
            ['gJ2iS', 'Rose'],
            ['j2LM4', 'Martha'],
            ['qi9CI', 'Donna'],
            ['oFrJ5', 'Amy'],
            ['pFrV4', 'Rory'],
            ['J2lm4', 'Clara'],
            ['ZIYJr', 'Bill'],
            ['ngrXu', 'Yasmin'],
            ['wxbOW', 'Ryan'],
            ['J2Lm4', 'Graham']
        ]

        extra_data = [
            [''] * 2,
            [''] * 2,
            tardis_data[0],
            tardis_data[6]
        ]

        table_data = [tardis_data[i] + ([''] + extra_data[i] if i < len(extra_data) else [''] * 3)
                      for i in range(len(tardis_data))]
        match = extra_data[3][0]
        results_txt = ['TRUE' if row[0] == match else 'FALSE' for row in table_data[1:]]
        for i, result in enumerate(results_txt, start=1):
            table_data[i][2] = result

        s = 0.37
        table = ExcelTable(table_data).scale(s).to_edge(LEFT).shift(DOWN*0.4)

        hidden_cells = [(4, 5), *[(i, 3) for i in range(1, len(table_data) + 1)]]
        self.play(table.get_draw_animation(hidden_data=hidden_cells), run_time=2.5)

        wrong_result = [row for row in table_data if row[0].lower() == match.lower()][0][1]
        wrong_result_tex = (Tex(wrong_result, color=BLACK).scale(s)
                            .move_to(table.get_rows()[hidden_cells[0][0]][hidden_cells[0][1]].get_center()))
        hidden_data = [table.get_rows()[i][j] for i, j in hidden_cells]

        formula_str = '=XLOOKUP(D4, A2:A11, B2:B11)'

        start_loc = UP * 1 + RIGHT * 1.5

        formula = ExcelFormula(formula_str, tables_list=[table], target_cell='E4', start_align=LEFT + UP,
                               start_location=start_loc)

        formula_exact_str = '=EXACT(D4, A2:A11)'
        formula_exact = ExcelFormula(formula_exact_str, tables_list=[table], target_cell='C2', start_align=LEFT + UP,
                                     start_location=start_loc)

        formula_str_2 = '=XLOOKUP(TRUE, EXACT(D4, A2:A11), B2:B11)'
        formula_2 = ExcelFormula(formula_str_2, tables_list=[table], target_cell='E4', start_align=LEFT + UP,
                                 start_location=start_loc)

        self.play(formula.write_to_scene())
        self.play(Write(wrong_result_tex))
        self.wait(2)
        self.play(Unwrite(wrong_result_tex), Unwrite(formula), Uncreate(formula.highlight_objs),
                  Uncreate(formula.formula_box))
        self.wait(2)

        self.play(formula_exact.write_to_scene())
        self.play(LaggedStart(*[Write(data) for data in hidden_data[1:]], lag_ratio=0.2))
        self.wait(2)
        self.play(Unwrite(formula_exact), Uncreate(formula_exact.highlight_objs),
                  Uncreate(formula_exact.formula_box), *[Unwrite(data) for data in hidden_data[1:]])
        self.wait(2)

        self.play(formula_2.write_to_scene())
        self.play(Write(hidden_data[0]))
        self.wait(3)


class ComplexExplainer(NarratedScene):
    def construct(self):
        title = Text("Complex Criteria Lookups").scale(0.85).to_edge(UP)
        title.z_index = 1

        table_data = [
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

        def calculate_extra(row):
            c1 = int(row[1]) < 30
            c2 = int(row[3]) >= 3
            c3 = row[4][0] == 'S'

            return '1' if c1 and c2 and c3 else '0'

        table_extra = [['\\verb|<|30'], ['Excel\\verb|>|=3'], ['``S" Town'], ['Yasmin']]
        table_data = [table_data[i] + ([''] if i == 0 else [calculate_extra(table_data[i])])
                      + (table_extra[i] if i < len(table_extra) else [''])
                      for i in range(len(table_data))]
        table = ExcelTable(table_data).scale(0.35).to_edge(LEFT).shift(LEFT*0.25)
        hidden_cells = [(4, 7), *[(i, 6) for i in range(1, len(table_data) + 1)]]
        hidden_data = [table.get_rows()[i][j] for i, j in hidden_cells]

        self.wait(2)
        self.play(Write(title), table.get_draw_animation(hidden_data=hidden_cells))
        self.wait(4)

        result_cells = hidden_cells.pop(0)
        result = hidden_data.pop(0)

        partial_str = '=(B2:B9 < 30) *\n(D2:D9 >= 3) * \n (LEFT(E2:E9) = "S")'
        formula_str = f'=XLOOKUP(1,\n{partial_str[1:]},\nA2:A9)'
        formula = ExcelFormula(formula_str, tables_list=[table], target_cell='G4', start_align=LEFT + UP,
                               start_location=UP * 1.25 + RIGHT * 1.5, split_lines=False, scale=0.65)


        partial_formula = ExcelFormula(partial_str, tables_list=[table], target_cell='F2', start_align=LEFT + UP,
                                       start_location=UP * 1.25 + RIGHT * 1.5, split_lines=False, scale=0.65)
        self.play(partial_formula.write_to_scene())
        self.wait(0.5)
        self.play(LaggedStart(*[Write(data) for data in hidden_data], lag_ratio=0.05))
        self.wait(2)
        self.play(LaggedStart(*[Unwrite(data) for data in hidden_data], lag_ratio=0.05),
                  Unwrite(partial_formula), Uncreate(partial_formula.formula_box),
                  Uncreate(partial_formula.highlight_objs))
        self.wait(3)

        self.play(formula.write_to_scene())
        self.wait(0.5)
        self.play(Write(result))
        self.wait(3)


class NamedRangeTableExample(NarratedScene):
    def construct(self):
        title = Text("Named Ranges and Tables").scale(0.85).to_edge(UP)
        title.z_index = 1
        self.play(Write(title))

        tardis_data = [
            ['\\textbf{TARDIS\_Id}', '\\textbf{Name}'],
            ['gJ2iS', 'Rose'],
            ['j2LM4', 'Martha'],
            ['qi9CI', 'Donna'],
            ['oFrJ5', 'Amy'],
            ['pFrV4', 'Rory'],
            ['J2lm4', 'Clara'],
            ['ZIYJr', 'Bill'],
            ['ngrXu', 'Yasmin'],
            ['wxbOW', 'Ryan'],
            ['J2Lm4', 'Graham']
        ]

        extra_data = [
            [''] * 2,
            [''] * 2,
            tardis_data[0],
            tardis_data[6]
        ]

        table_data = [tardis_data[i] + ([''] + extra_data[i] if i < len(extra_data) else [''] * 3)
                      for i in range(len(tardis_data))]

        table = ExcelTable(table_data).scale(0.35).to_edge(LEFT).shift(DOWN*0.4)
        table.add_named_table('A1:B11')

        formula_str = '=XLOOKUP(TRUE, EXACT(!Tardis_Id!, Codes[TARDIS_Id]), Codes[Name])'
        dynamic_ranges = {'Codes[TARDIS_Id]': 'A2:A11',
                          'Codes[Name]': 'B2:B11',
                          'Tardis_Id': 'D4'}
        formula = ExcelFormula(formula_str, tables_list=[table], target_cell='E4', start_align=LEFT + UP,
                               start_location=UP + RIGHT * 1, dynamic_ranges=dynamic_ranges)
        hidden_data = [(4, 5)]

        self.play(table.get_draw_animation(hidden_data=hidden_data))
        self.wait(2)
        self.play(formula.write_to_scene())
        self.wait(0.5)
        self.play(Write(table.get_rows()[hidden_data[0][0]][hidden_data[0][1]]))
        self.wait(4)


class WildCardSearch(NarratedScene):
    def construct(self):
        title = Text('Wildcard Searches').scale(0.85).to_edge(UP)
        title.z_index = 1
        self.play(Write(title))
        self.wait(1)

        wildcards = [Tex(excel_formula.FORMULA_REPLACEMENTS[wc]
                         if wc in excel_formula.FORMULA_REPLACEMENTS
                         else wc) for wc in ['?', '*', '~']]
        wildcard_examples = VGroup(*wildcards).scale(2.5).arrange(RIGHT, buff=2.5).shift(UP * 1)
        self.play(LaggedStart(*[Write(wct) for wct in wildcard_examples], lag_ratio=0.4))
        self.wait(2)

        wildcard_explainers = [Tex(explainer).scale(0.7) for explainer in
                               ['Any one\n\rcharacter', 'Any number\n\rof characters', 'Escape\n\rcharacter']]
        for i, wildcard_explainer in enumerate(wildcard_explainers):
            wildcard_explainer.next_to(wildcards[i], DOWN)
            if i > 0:
                wildcard_explainer.align_to(wildcard_explainers[i - 1], UP)
            self.play(Write(wildcard_explainer))
            self.wait(1)

        self.wait(2)
        self.play(Unwrite(wildcard_examples), *[Unwrite(wce).set_run_time(1) for wce in wildcard_explainers])
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

        extra_data = [
            ['\\textbf{Pattern}', '\\textbf{Name}', '\\textbf{Profession}'],
            ['M*', 'Martha', 'Doctor'],
            ['R?s?', 'Rose', 'Shop Assistant'],
            ['C*a', 'Clara', 'Teacher'],
            ['*s*', 'Rose', 'Shop Assistant'],
            ['*s???', 'Yasmin', 'Police Officer']
        ]

        table_data = [base_table_data[i] + [''] + (extra_data[i] if i < len(extra_data) else [''] * len(extra_data[0]))
                      for i in range(len(base_table_data))]
        table = ExcelTable(table_data).scale(0.35).to_edge(DOWN)

        formula_str = '=XLOOKUP(G2, $A$2:$A$9, \nHSTACK($A$2:A$9, $C$2:$C$9), , 2)'
        formula = ExcelFormula(formula_str, tables_list=[table], target_cell='H2', split_lines=False)
        formula.next_to(title, DOWN, buff=0.6)
        formula.formula_box[1].move_to(formula).shift(UP * 0.02)
        j_vals = [8, 9]
        hidden_data = [(i, j) for i in range(2, len(extra_data) + 1) for j in j_vals]
        i_vals = {i for i, j in hidden_data}

        hidden_data_rows = [[table.get_rows()[i][j_vals[0]], table.get_rows()[i][j_vals[1]]] for i in i_vals]

        self.play(table.get_draw_animation(hidden_data=hidden_data))
        self.wait(2)
        self.play(formula.write_to_scene())
        self.wait(2)

        self.play(LaggedStart(*[Write(el) for el in hidden_data_rows[0]], lag_ratio=0.4))
        self.wait(2)
        self.play(table.animate_flash_fill(range_str='H2', lagged_animations=[LaggedStart(*[Write(el) for el in row])
                                                                              for row in hidden_data_rows[1:]]))
        self.wait(2)
