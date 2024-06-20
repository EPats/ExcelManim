from manim import *
from excel_formula import *
from excel_tables import *
from scenes import NarratedScene


class HelperLookups(NarratedScene):
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

        table_data = [table_data[i] + ([''] + extra_data[i] if i < len(extra_data) else [''] * 4)
                      for i in range(len(table_data))]


        table = ExcelTable(table_data).scale(0.25).to_corner(DL).shift(RIGHT*0.5)
        hidden_cells = [(6,7)]
        self.play(table.get_draw_animation(hidden_data=hidden_cells), run_time=2.5)

        wrong_result = [row for row in table_data if row[0] == 'Clara'][0][2]
        wrong_result_tex = (Tex(wrong_result, color=BLACK).scale(0.25)
                            .move_to(table.get_rows()[hidden_cells[0][0]][hidden_cells[0][1]].get_center()))
        hidden_data = [table.get_rows()[i][j] for i, j in hidden_cells]
        formula_str = '=XLOOKUP(E6, A2:A19, C2:C19)'
        formula = ExcelFormula(formula_str, tables_list=[table], target_cell='G6', start_align=LEFT + UP,
                               start_location=UP+RIGHT*1)
        formula_str_2 = '=XLOOKUP(E6&F6, A2:A19&B2:B19, C2:C19)'
        formula_2 = ExcelFormula(formula_str_2, tables_list=[table], target_cell='G6', start_align=LEFT + UP,
                                 start_location=UP+RIGHT*1)

        self.play(formula.write_to_scene())
        self.play(Write(wrong_result_tex))
        self.wait(2)
        self.play(Unwrite(wrong_result_tex), Unwrite(formula), Uncreate(formula.highlight_objs), Uncreate(formula.formula_box))
        self.wait(2)

        self.play(formula_2.write_to_scene())
        self.play(Write(hidden_data[0]))
        self.wait(2)

class ExactExplainer(NarratedScene):
    def construct(self):
        title = Text("Case-Sensitive Lookups").scale(0.85).to_edge(UP)
        title.z_index = 1
        self.play(Write(title))

        tardis_data = [
            ['\\textbf{TARDIS ID}', '\\textbf{Name}'],
            ['gJ2iS', 'Rose'],
            ['j2LM4', 'Martha'],
            ['qi9CI', 'Donna'],
            ['oFrJ5', 'Amy'],
            ['pFrV4', 'Rory'],
            ['J2lm4', 'Clara'],
            ['ZIYJr', 'Bill'],
            ['ngrXu', 'Yasmin'],
            ['wxbOW', 'Ryan'],
            ['J2lm4', 'Graham']
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
        table = ExcelTable(table_data).scale(s).to_corner(DL)

        hidden_cells = [(4,5), *[(i, 3) for i in range(1, len(table_data) + 1)]]
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
        self.wait(2)


class NamedRangeTableExample(NarratedScene):
    def construct(self):
        title = Text("Named Ranges and Tables").scale(0.85).to_edge(UP)
        title.z_index = 1
        self.play(Write(title))

        table_data = [
            ['\\textbf{Month}', '\\textbf{Sales}'],
            ['January', '1000'],
            ['February', '2000'],
            ['March', '3000'],
            ['April', '4000'],
            ['May', '5000'],
            ['June', '6000'],
            ['July', '7000'],
            ['August', '8000'],
            ['September', '9000'],
            ['October', '10000'],
            ['November', '11000'],
            ['December', '12000']
        ]

        extra_data = [table_data[0], table_data[6]]
        table_data = [table_data[i] + ([''] + extra_data[i] if i < len(extra_data) else [''] * 3)
                      for i in range(len(table_data))]

        table = ExcelTable(table_data).scale(0.4).to_corner(DL)
        table.add_named_table('A3:B8')
        self.play(table.get_draw_animation())
        self.wait(2)
        formula_str = '=TEST(Table1[Sales], !MyNamedRange!)'
        dynamic_ranges = {'Table1[Sales]': 'A2:A13',
                          'MyNamedRange': 'B2:B13'}
        formula = ExcelFormula(formula_str, tables_list=[table], target_cell='D3', start_align=LEFT + UP,
                               start_location=UP+RIGHT*1, dynamic_ranges=dynamic_ranges)
        self.play(formula.write_to_scene())
        self.wait(4)