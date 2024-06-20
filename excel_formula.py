import typing

from manim import *
from manim.typing import Vector3D

from excel_constants import *
import excel_tables as tables
import re

DEFAULT_FORMULA_START_LOCATION: Vector3D = LEFT * 5 + UP * 2

FORMULA_REPLACEMENTS: dict[str, str] = {
    '[': '\\verb|[|',
    ']': '\\verb|]|',
    '&': '\&',
    '_': '\\verb|_|',
    '<': '\\verb|<|',
    '>': '\\verb|>|',
    '--': '\\verb|--|',
    ',': ',\n',
    '$': '\\verb|$|'
}

REVERSED_FORMULA_REPLACEMENTS: dict[str, str] = {v: k for k, v in FORMULA_REPLACEMENTS.items()}


class ExcelFormula(VGroup):
    def __init__(self, formula: str, start_location: Vector3D = DEFAULT_FORMULA_START_LOCATION, scale: float = 0.7,
                 color_offset: int = 0, tables_list: list = None, split_lines: bool = True, target_cell: str = '',
                 dynamic_ranges: dict[str, str] = None, tex_color: ManimColor = WHITE, start_align: Vector3D = LEFT,
                 **kwargs):

        self.tables = {table.sheet_name: table for table in tables_list} if tables_list else {}

        def parse_excel_formula(formula: str) -> list[tuple[str, str]]:
            # Regular expressions to capture different parts of the formula
            regex_patterns = {
                'force_new_line': '\n',
                'main_function': r'^={0,1}([A-Z][A-Z\d]*+(?=\())',
                'nested_function': r'([A-Z]+[A-Z\d]*(?=\())',
                'string_argument': r'"([^"]*)"',
                'number_argument': r'(\d+(?:\.\d+)?)',
                'boolean_argument': r'\b(TRUE|FALSE)\b',
                'blank_argument': r'(?<=\()\s*(?=,)|(?<=,)\s*(?=,)|(?<=,)\s*(?=\))',
                'parentheses_open': r'\(',
                'parentheses_close': r'\)',
                'range_argument': r'(([A-Za-z0-9_]+!){0,1}\${0,1}[A-Z]+\${0,1}[0-9]+:\${0,1}[A-Z]+\${0,1}[0-9]+)'
                                  r'|'
                                  r'(([A-Za-z0-9_]+!){0,1}\${0,1}[A-Z]+\${0,1}[0-9]+)',
                'dynamic_range_argument': r'\${0,1}[A-Z]+\${0,1}[0-9]+#{0,1}'
                                          r'|'
                                          r'([A-Za-z0-9_]+\[[A-Za-z0-9_]+\])'
                                          r'|'
                                          r'![A-Za-z0-9_]+!',
                'named_argument': r'\[{0,1}[A-Za-z0-9_]+\]{0,1}',
                'comma': r',',
                'unary_operator': r'--',
                'comparison_operator': r'<=|>=|<>|<|>|=',
                'operator': r'[\+\*\-/&]'
            }

            tokens = []
            pos = 0
            formula = re.sub(r',(?=\S)', ', ', formula.strip())
            formula = re.sub(r' +', r' ', formula)

            def get_next_token(formula, pos):
                for token_type, pattern in regex_patterns.items():
                    regex = re.compile(pattern)
                    match = regex.match(formula, pos)
                    if match:
                        return (token_type, match.group(), match.end() + (0 if match.group() else 1))
                return (None, None, pos + 1)

            # Search through the formula for matches with any of the patterns
            while pos < len(formula):
                token_type, token_value, new_pos = get_next_token(formula, pos)
                if token_type:
                    tokens.append((token_type, token_value))
                pos = new_pos

            return tokens

        def clean_string(token_pair: tuple[str, str]) -> tuple[str, str]:
            token_type, token_value = token_pair
            if token_type == 'string_argument':
                token_value = f'``{token_value[1:]}'
            elif token_type == 'blank_argument':
                token_value = '  '
            elif token_type == 'dynamic_range_argument' and token_value[0] == '!':
                token_value = token_value[1:-1]
            if split_lines:
                token_value = token_value.replace(',', ',\n')

            for k in FORMULA_REPLACEMENTS:
                token_value = token_value.replace(k, FORMULA_REPLACEMENTS[k])

            return token_type, token_value

        def combine_tokens_to_lines(tokens: list[tuple[str, str]]) -> list[list[tuple]]:
            result = []
            current_line = []

            new_line_list = ['nested_function', 'force_new_line'] if split_lines else ['force_new_line']
            for i, token in enumerate(tokens):
                if (token[0] in new_line_list or
                        (token[0] == 'parentheses_close' and tokens[i - 1][0] == 'parentheses_close' and split_lines)):
                    if current_line:
                        result.append(current_line)
                    current_line = [] if token[0] == 'force_new_line' else [clean_string(token)]
                elif token[0] == 'comma' and split_lines:
                    if current_line:
                        current_line.append(clean_string(token))
                        result.append(current_line)
                    current_line = []
                else:
                    current_line.append(clean_string(token))

            if current_line:
                result.append(current_line)

            return result

        tokens: list[tuple[str, str]] = parse_excel_formula(formula)
        line_tokens: list[list[tuple]] = combine_tokens_to_lines(tokens)
        tex_mob_lines: list[Tex] = [Tex(*[token[1] for token in line]).scale(scale) for line in line_tokens]

        highlights: dict = {}
        highlight_names_to_colors = {}
        parentheses_open: list = []

        tex_mob_line: Tex
        for i, tex_mob_line in enumerate(tex_mob_lines):
            tex_mob_line.set_color(tex_color)
            if i == 0:
                tex_mob_line.move_to(start_location, aligned_edge=start_align)
            else:
                tex_mob_line.next_to(tex_mob_lines[i - 1], DOWN)

            if line_tokens[i][0][0] == 'nested_function':
                tex_mob_line.align_to(tex_mob_lines[0], LEFT).shift(RIGHT * 0.5 * len(parentheses_open))
            elif line_tokens[i][0][0] == 'parentheses_close':
                tex_mob_line.align_to(parentheses_open[-1][0], LEFT)
            elif line_tokens[i][0][0] != 'main_function':
                align_mob_index = parentheses_open[-1][1]
                align_mob = tex_mob_lines[align_mob_index[0]][align_mob_index[1] + 1]
                tex_mob_line.align_to(align_mob, LEFT)

            tex_mob: Tex
            for j, tex_mob in enumerate(tex_mob_line):
                match token_type := line_tokens[i][j][0]:
                    case 'range_argument' | 'dynamic_range_argument':
                        token_value = line_tokens[i][j][1]
                        if token_value in highlight_names_to_colors:
                            range_color = highlight_names_to_colors[token_value]
                            tex_mob.set_color(range_color)
                            continue

                        range_color = RANGE_COLORS[(color_offset + len(highlights)) % len(RANGE_COLORS)]
                        tex_mob.set_color(range_color)
                        if self.tables:
                            table = list(self.tables.values())[0] if len(self.tables) == 1 \
                                else self.tables[token_value.split('!')[0]]

                            dynamic_key = token_value
                            for k in REVERSED_FORMULA_REPLACEMENTS:
                                dynamic_key = dynamic_key.replace(k, REVERSED_FORMULA_REPLACEMENTS[k])
                            range_highlight_address = token_value if token_type == 'range_argument' \
                                else dynamic_ranges[dynamic_key]
                            range_highlight = table.highlight_table_range(range_str=range_highlight_address,
                                                                          highlight_color=range_color)
                            highlights[f'{i}:{j}'] = range_highlight
                            highlight_names_to_colors[token_value] = range_color
                    case 'parentheses_open':
                        parentheses_open.append((tex_mob, (i, j)))
                    case 'parentheses_close':
                        parentheses_open.pop()

        self.highlights: dict[str, Rectangle] = highlights
        print(len(self.highlights))
        self.highlight_objs = VGroup(*self.highlights.values())
        self.target_cell = target_cell
        self.formula_box = VGroup()

        super().__init__(*tex_mob_lines, **kwargs)

        if self.target_cell:
            table = list(self.tables.values())[0] if len(self.tables) == 1 \
                else self.tables[self.target_cell.split('!')[0]]

            start_cell, end_cell = table.get_start_end_cells_for_range(self.target_cell)
            formula_box = SurroundingRectangle(start_cell, color=BLACK, stroke_opacity=0, buff=0)
            formula_box_2 = Rectangle(width=self.get_true_width() + 0.2 * 2,
                                                   height=self.get_true_height() + 0.2 * 2,
                                                   color=WHITE).move_to(self).shift(UP * 0.02)

            self.z_index = 1
            self.formula_box.add(formula_box, formula_box_2)

    def get_all_objects(self):
        return self.submobjects + self.highlight_objs.submobjects + self.formula_box.submobjects

    def fade_out(self):
        return AnimationGroup(*[FadeOut(mob) for mob in self.get_all_objects()])

    def write_to_scene(self, run_time: float = 1.5, gap_between: float = 0.3) -> Animation:
        all_animations = []

        if self.target_cell:
            table = list(self.tables.values())[0] if len(self.tables) == 1 \
                else self.tables[self.target_cell.split('!')[0]]
            highlight_anim = table.get_passing_flash(range_str=self.target_cell, flash_color=BLACK, stroke_width=2.5)
            type_anims = LaggedStart(highlight_anim, Transform(self.formula_box[0], self.formula_box[1]),
                                lag_ratio=0.2)
            all_animations.append(type_anims)

        for i, tex_line in enumerate(self):
            tex: Tex
            for j, tex in enumerate(tex_line):
                t = min(len(tex.tex_string) * 0.2, run_time)
                animations = [Write(tex).set_run_time(t)]
                if self.highlights and f'{i}:{j}' in self.highlights:
                    animations.append(Create(self.highlights[f'{i}:{j}']).set_run_time(t))
                all_animations.append(AnimationGroup(*animations))
                if gap_between:
                    all_animations.append(Wait(gap_between))
        return Succession(*all_animations)

    def transform_into(self, new_formula: 'ExcelFormula'):
        transform_text = TransformMatchingTex(self, new_formula)

        n = len(self.highlights)
        m = len(new_formula.highlights)
        k = min(n, m)

        highlight_transformations: list[Animation] = [Transform(list(self.highlights.values())[i],
                                                                list(new_formula.highlights.values())[i])
                                                      for i in range(k)]
        if k == 0:
            return transform_text

        if n > m:
            highlight_transformations += [FadeOut(list(self.highlights.values())[i]) for i in range(k, n)]
        elif m > n:
            highlight_transformations += [Create(list(new_formula.highlights.values())[i]) for i in range(k, m)]

        return AnimationGroup(transform_text, *highlight_transformations)

    def get_true_width(self):
        return max([line.get_right()[0] for line in self]) - self[0].get_left()[0]

    def get_true_height(self):
        return self[0].get_top()[1] - self[-1].get_bottom()[1]
