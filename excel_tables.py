from typing import Callable

from manim import *
import re
import excel_helpers as helpers
from excel_constants import *


class ExcelTable(MobjectTable):
    def __init__(self, table_data_strings: list[list[str]], sheet_name: str = '',
                 broken_column_groups: list[list[str]] = None,
                 broken_row_groups: list[list[str]] = None, tex_color: ManimColor = BLACK,
                 element_to_mobject: Callable[[VMobject], VMobject] = lambda m: m, **kwargs):

        def create_tex_cells(data: list[list[str]]) -> list[list[Tex]]:
            return [[Tex(cell).set_color(tex_color) for cell in row] for row in data]

        def create_labels(size: int, start: int, is_column: bool = True) -> list[Text]:
            return [Text(chr(64 + i), weight='BOLD') if is_column else Text(str(i), weight='BOLD')
                    for i in range(start, size + start)]

        def insert_blank_rows(data: list[list[str]], broken_rows: list[list[str]] = None) -> tuple:
            broken_row_count = sum(len(group) for group in broken_row_groups) if broken_row_groups else 0
            start_rows = len(data) - broken_row_count
            row_labels = create_labels(size=start_rows, start=1, is_column=False)
            blank_rows = []

            if not broken_rows:
                return data, row_labels, blank_rows

            blank_row = ['...'] * len(data[0])
            insert_row_index = len(row_labels)
            for broken_row_group in broken_rows:
                data.insert(insert_row_index, blank_row)
                blank_rows.append(insert_row_index + 2)
                row_labels.append(Text('...'))
                row_labels.extend(Text(str(num)) for num in broken_row_group)
                insert_row_index = len(row_labels)

            return data, row_labels, blank_rows

        def process_broken_columns(data: list[list[str]], broken_columns: list[list[str]] = None) -> tuple:
            broken_col_count = sum(len(group) for group in broken_column_groups) if broken_column_groups else 0
            start_columns = len(data[0]) - broken_col_count
            column_labels = create_labels(size=start_columns, start=1, is_column=True)
            blank_columns = []

            if not broken_columns:
                return data, column_labels, blank_columns

            new_data = [row[:-broken_col_count] for row in data]
            leftover_data = [row[-broken_col_count:] for row in data]
            for broken_col_group in broken_columns:
                blank_columns.append(len(column_labels) + 2)
                column_labels.append(Text('...'))
                column_labels.extend(Text(letter) for letter in broken_col_group)

                broken_col_data = [row[:len(broken_col_group)] for row in leftover_data]
                leftover_data = [row[len(broken_col_group):] for row in leftover_data] \
                    if len(broken_col_group) < len(leftover_data[0]) else []

                new_data = [new_data[i] + ['...'] + broken_col_data[i] for i in range(len(new_data))]
                if not any(leftover_data):
                    break

            return new_data, column_labels, blank_columns

        new_data, col_labels, blank_col_indices = process_broken_columns(
            table_data_strings, broken_column_groups)
        new_data, row_labels, blank_row_indices = insert_blank_rows(
            new_data, broken_row_groups)

        table_data = create_tex_cells(new_data)

        additional_arguments = {'col_labels': col_labels, 'row_labels': row_labels, 'include_outer_lines': True,
                                'line_config': {'stroke_width': 2, 'color': BLACK},
                                'element_to_mobject': element_to_mobject}
        self.sheet_name = sheet_name

        if sheet_name:
            additional_arguments['top_left_entry'] = Text(sheet_name, slant=ITALIC, color=WHITE)

        super().__init__(table_data, **additional_arguments, **kwargs)

        self.highlight_cells(blank_row_indices, blank_col_indices)

    def highlight_cells(self, blank_row_indices: list[int], blank_col_indices: list[int]) -> None:
        for i in range(1, len(self.get_columns()) + 1):
            self.add_highlighted_cell((1, i), EP_EXCEL_GREEN, fill_opacity=1)
        for i in range(2, len(self.get_rows()) + 1):
            self.add_highlighted_cell((i, 1), EP_EXCEL_GREEN, fill_opacity=1)
        for i in range(2, len(self.get_rows()) + 1):
            for j in range(2, len(self.get_columns()) + 1):
                opacity = 0.4 if i in blank_row_indices or j in blank_col_indices else 0.8
                self.add_highlighted_cell((i, j), WHITE, fill_opacity=opacity)

    def add_named_table(self, table_range: str, color1: ManimColor = BLUE, color2: ManimColor = BLUE_A,
                        title_color: ManimColor = BLUE_E) -> None:
        start_cell_indices, end_cell_indices = self.get_start_cell_end_cell_indices(table_range)
        for i in range(start_cell_indices[0], end_cell_indices[0] + 1):
            for j in range(start_cell_indices[1], end_cell_indices[1] + 1):
                opacity = 0.8
                color = title_color if i == start_cell_indices[0] \
                    else color2 if i % 2 == start_cell_indices[0] % 2 else color1
                self.add_highlighted_cell((i, j), color, fill_opacity=opacity)

    def get_draw_animation(self, hidden_data: list[tuple[int, int]] = None) -> Animation:
        background_rectangles = VGroup(
            *[mob for mob in self.submobjects if mob.name == "BackgroundRectangle"][::-1])

        top_left = self.top_left_entry
        headers_col = self.get_col_labels()
        headers_row = self.get_row_labels()
        lines = self.get_vertical_lines()
        lines.add(self.get_horizontal_lines())

        if hidden_data:
            rows = []
            for i, row in enumerate(self.get_rows()[1:], start=1):
                current_row = VGroup()
                for j, el in enumerate(row[1:], start=1):
                    if (i, j) not in hidden_data:
                        current_row.add(row[j])
                rows.append(current_row)
        else:
            rows = [row[1:] for row in self.get_rows()[1:]]

        anims = []
        if top_left:
            headers_anim = AnimationGroup(Write(top_left), Write(headers_col), Write(headers_row))
        else:
            headers_anim = AnimationGroup(Write(headers_col), Write(headers_row))
        headers_anim.set_run_time(1.5)

        return Succession(
            LaggedStart(
                AnimationGroup(
                    Create(background_rectangles).set_run_time(1.5),
                    LaggedStart(Create(lines), run_time=2.5, lag_ratio=0.15)),
                headers_anim,
                lag_ratio=0.5),
            LaggedStart(*[Write(el) for el in rows], run_time=2.5, lag_ratio=0.2)
        )
        # anims.play()
        # scene.add(top_left)

    def get_start_cell_end_cell_indices(self, range_str: str) -> tuple:
        if '!' in range_str:
            range_str = range_str.split('!')[1]

        rows = list(map(str, re.findall(r'\d+', range_str)))
        cols = list(map(str, re.findall(r'[A-Z]+', range_str)))
        # [sum((ord(c) - 64) * 26 ** i for i, c in enumerate(reversed(col))) for col in
        #         re.findall(r'[A-Z]+', range_str)]

        row_labels = [tex.text for tex in self.get_row_labels()]
        col_labels = [tex.text for tex in self.get_col_labels()]

        start_row = row_labels.index(rows[0]) + 2
        end_row = row_labels.index(rows[-1]) + 2
        start_col = col_labels.index(cols[0]) + 2
        end_col = col_labels.index(cols[-1]) + 2

        return (start_row, start_col), (end_row, end_col)

    def get_start_end_cells_for_range(self, range_str: str) -> (Polygon, Polygon):
        start_cell_indices, end_cel_indicesl = self.get_start_cell_end_cell_indices(range_str)

        # Get the top-left and bottom-right corners of the specified cell range
        start_cell = self.get_cell((start_cell_indices[0], start_cell_indices[1]))
        end_cell = self.get_cell((end_cel_indicesl[0], end_cel_indicesl[1]))

        return start_cell, end_cell

    def highlight_table_range(self, range_str: str, highlight_color: ManimColor = BLUE,
                              stroke_width: float = DEFAULT_STROKE_WIDTH) -> Polygon:
        """
           Highlights a range of cells in an excel table in specified color.

           Parameters:
           table: The table in which the cells are to be highlighted.
           range_str: A string representing the range of cells to be highlighted (e.g., 'A1:C3').
           color: The color to use for highlighting.

           Returns:
           A rectangle highlighting the specified cell range, positioned on top of the range.
       """
        start_cell, end_cell = self.get_start_end_cells_for_range(range_str)

        # Determine the coordinates of the corners
        start_corner = start_cell.get_corner(UL)
        end_corner = end_cell.get_corner(DR)

        # Calculate width and height of the rectangle
        width = end_corner[0] - start_corner[0]
        height = end_corner[1] - start_corner[1]

        highlight_rectangle = Rectangle(fill_color=highlight_color, color=highlight_color, fill_opacity=0.4,
                                        width=width,
                                        height=height, stroke_width=stroke_width)

        # Position the rectangle to cover the specified cell range
        highlight_rectangle.move_to((end_corner + start_corner) / 2)
        highlight_rectangle = helpers.change_path_to_top_left_clockwise(highlight_rectangle)

        return highlight_rectangle

    def get_formula_range(self, range_str: str, color: ManimColor, with_comma: bool = True) -> (Tex, Rectangle):
        tex_mob = Tex(range_str, ',', color=color)
        tex_mob.set_color_by_tex(',', WHITE) if with_comma else Tex(range_str, color=color)
        return tex_mob, self.highlight_table_range(range_str, color)

    def get_passing_flash(self, range_str: str, run_time: float = 2.5, time_width: float = 1.2,
                          flash_color: ManimColor = EP_BLUE, stroke_width: float = DEFAULT_STROKE_WIDTH) \
            -> ShowPassingFlash:
        rectangle = self.highlight_table_range(range_str, highlight_color=flash_color, stroke_width=stroke_width)
        rectangle.set_fill(opacity=0)
        rectangle = helpers.change_path_to_top_left_clockwise(rectangle)

        return ShowPassingFlash(rectangle, time_width=time_width, run_time=run_time)

    def animate_flash_fill(self, range_str: str, lagged_animations: list[Animation] = None, n_squares: int = 3) -> LaggedStart:
        start_cell, end_cell = self.get_start_end_cells_for_range(range_str)
        start_dr = start_cell.get_corner(DR)
        sq = Square(side_length=0.3, color=EP_EXCEL_GREEN, stroke_width=2).move_to(start_dr)

        square_anims = [sq.copy().animate.scale(0.001).set_stroke(opacity=0) for _ in range(n_squares)]
        square_anim = LaggedStart(*square_anims, lag_ratio=0.2)
        if lagged_animations:
            return LaggedStart(square_anim, *lagged_animations, lag_ratio=0.2)
        return square_anim


def results_table(table_data_strings: list[list[str]], h_buff: float = 1.3, v_buff: float = 0.8,
                  results_title: bool = True) -> Mobject:
    """
       Creates a table with Excel-like formatting.

       Parameters:
       table_data_strings (list of list of str): A list of lists containing the strings for each cell.

       Returns:
       A table object with formatted cells.
   """

    # Convert table data strings to Tex objects with black color
    table_data: list[list[Tex]] = [[Tex(data).set_color(BLACK) for data in row] for row in table_data_strings]

    # Determine the number of columns and rows
    cols: int = len(table_data_strings[0])
    rows: int = len(table_data_strings)

    # Create column and row labels
    # Create the table with outer lines and specified line configuration
    table: Table = MobjectTable(
        table_data,
        include_outer_lines=True,
        line_config={'stroke_width': 2, 'color': BLACK},
        h_buff=h_buff,
        v_buff=v_buff
    )

    # Highlight the rest of the cells with white
    # Not full opacity as the white hurts my eyes!
    for i in range(1, rows + 1):
        for j in range(1, cols + 1):
            table.add_highlighted_cell((i, j), WHITE, fill_opacity=0.8)

    if results_title:
        title = Tex('Results').next_to(table, UP, buff=0.1)
        return VGroup(title, table)
    else:
        return table


class ComparisonTable(MobjectTable):
    def __init__(self, table_data, **kwargs):
        self.raw_data = table_data
        object_data = [
            [TICK.copy().scale(0.35) if text == 'Yes' else CROSS.copy().scale(0.35) if text == 'No' else Paragraph(text)
             for text in line]
            for line in table_data]

        for line in object_data:
            for el in line:
                if el.name == 'Paragraph':
                    text = el.lines_text.text
                    if text in ['High', 'Easy']:
                        el.set_color(EP_GREEN)
                    elif text == 'Med':
                        el.set_color(YELLOW)
                    elif text in ['Hard', 'Low']:
                        el.set_color(RED)
                    elif text == 'Both':
                        el.set_sheen_direction(DOWN)
                        el.set_color([XKCD.BARBIEPINK, XKCD.BARBIEPINK, XKCD.AMETHYST, XKCD.COBALT, XKCD.COBALT])

        super().__init__(object_data, **kwargs)

    def create_and_write_headers(self):
        lines = self.get_vertical_lines()
        lines.add(self.get_horizontal_lines())
        return LaggedStart(LaggedStart(Create(lines), run_time=3, lag_ratio=0.15),
                           LaggedStart(*[Write(mob).set_run_time(1.5) for mob in self.get_rows()[0]],
                                       lag_ratio=0.4))

    def fill_in_rows(self, gap_between_rows: float = 1, animations_length: float = 1, gap_between: float = 0.3):
        rows = self.get_rows()[1:]
        animations = []
        for i, row in enumerate(self.raw_data[1:]):
            animations.append(Wait(gap_between_rows))
            animations.append(Write(rows[i][0]).set_run_time(animations_length))
            animations.append(Wait(gap_between))

            current_animations = []
            for j, text in enumerate(row):
                if j == 0:
                    continue

                el = rows[i][j]
                animation: Animation

                if el.name == 'Paragraph':
                    animation = Write(el)
                else:
                    animation = DrawBorderThenFill(el)

                if not current_animations or text == row[j - 1]:
                    current_animations.append(animation)
                else:
                    animations.append(AnimationGroup(*current_animations).set_run_time(animations_length))
                    current_animations = [animation]

                if j == len(row) - 1:
                    animations.append(AnimationGroup(*current_animations).set_run_time(animations_length))
                animations.append(Wait(gap_between))

        return Succession(*animations)
