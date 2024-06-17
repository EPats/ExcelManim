from manim import *
from excel_tables import *
from excel_formula import *
from scenes import NarratedScene


class MatchMode(NarratedScene):
    def construct(self):
        books_data = [
            ['Name', 'Author', 'Pages'],
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
            ['Book Length', 'Min Pages', 'Max Pages'],
            ['Short', 0, 99],
            ['Medium', 100, 499],
            ['Long', 400, 999],
            ['Epic', 1000, 5000]
        ]

        table_data = [books_data[i] + ['Book Length' if i == 0 else self.categorise_book(books_data[i][-1])] + ['']
                      + scoring_data[i] if i < len(scoring_data)
                      else books_data[i] + [self.categorise_book(books_data[i][-1])]
                      + [''] * 4 for i in range(len(books_data))]

        table = ExcelTable(table_data)
        table.scale(0.3).to_edge(DOWN).shift(DOWN*0.2)
        hidden_data = [(i, 4) for i in range(2, len(books_data) + 1)]
        self.play(table.get_draw_animation(hidden_data=hidden_data))
        self.wait(2)

        formula_str = '=XLOOKUP(C2, $G$2:$G$5, $F$2:$F$5, , -1)'
        formula = ExcelFormula(formula_str, tables_list=[table], split_lines=False, target_cell='D2',
                               start_location=table.get_top() + 0.5 * UP, start_align=ORIGIN)
        hidden_data_mobs = [table.get_rows()[i][j] for i, j in hidden_data]

        self.play(formula.write_to_scene())
        self.wait(1)
        result_1 = hidden_data_mobs.pop(0)
        self.play(Write(result_1))
        self.wait(2)
        write_results = LaggedStart(*[Write(mob) for mob in hidden_data_mobs], lag_ratio=0.1)
        self.play(table.animate_flash_fill('D2:D14', lagged_animations=[write_results]))
        self.wait(2)
        self.play(FadeOut(formula.formula_box[0]))
        self.wait(2)


    def categorise_book(self, pages: int, option2: bool = False) -> str:
        if pages < 100:
            return 'Short'
        elif pages < (300 if option2 else 400):
            return 'Medium'
        elif pages < 1000:
            return 'Long'
        else:
            return 'Epic'
