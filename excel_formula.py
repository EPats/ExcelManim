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


class ExcelFormula(VGroup):
    def __init__(self, formula: str, start_location: Vector3D = DEFAULT_FORMULA_START_LOCATION, scale: float = 0.7,
                 color_offset: int = 0,
                 tables_list: list[tables.ExcelTable] = None, dynamic_ranges: dict[str, str] = None, **kwargs):
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
                'dynamic_range_argument': r'\${0,1}[A-Z]+\${0,1}[0-9]+#{0,1}',
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
                token_value = '\_'

            token_value = token_value.replace(',', ',\n')

            for k in FORMULA_REPLACEMENTS:
                token_value = token_value.replace(k, FORMULA_REPLACEMENTS[k])

            return token_type, token_value

        def combine_tokens_to_lines(tokens: list[tuple[str, str]]) -> list[list[tuple]]:
            result = []
            current_line = []

            for i, token in enumerate(tokens):
                if (token[0] in ['nested_function', 'force_new_line'] or
                        (token[0] == 'parentheses_close' and tokens[i - 1][0] == 'parentheses_close')):
                    if current_line:
                        result.append(current_line)
                    current_line = [] if token[0] == 'force_new_line' else [clean_string(token)]
                elif token[0] == 'comma':
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
        parentheses_open: list = []

        tex_mob_line: Tex
        for i, tex_mob_line in enumerate(tex_mob_lines):
            if i == 0:
                tex_mob_line.move_to(start_location, aligned_edge=LEFT)
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
                        range_color = RANGE_COLORS[(color_offset + len(highlights)) % len(RANGE_COLORS)]
                        tex_mob.set_color(range_color)
                        if self.tables:
                            token_value = line_tokens[i][j][1]
                            table = list(self.tables.values())[0] if len(self.tables) == 1 \
                                else self.tables[token_value.split('!')[0]]

                            range_highlight_address = token_value if token_type == 'range_argument' \
                                else dynamic_ranges[token_value]
                            range_highlight = table.highlight_table_range(range_str=range_highlight_address,
                                                                          highlight_color=range_color)
                            highlights[f'{i}:{j}'] = range_highlight
                    case 'parentheses_open':
                        parentheses_open.append((tex_mob, (i, j)))
                    case 'parentheses_close':
                        parentheses_open.pop()

        self.highlights: dict[str, Rectangle] = highlights
        self.highlight_objs = VGroup(*self.highlights.values())
        super().__init__(*tex_mob_lines, **kwargs)

    def get_all_objects(self):
        return self.submobjects + self.highlight_objs.submobjects

    def write_to_scene(self, run_time: float = 1.5, gap_between: float = 0.3) -> Animation:
        all_animations = []
        for i, tex_line in enumerate(self):
            tex: Tex
            for j, tex in enumerate(tex_line):
                t = min(0.2 + len(tex.tex_string) * 0.2, run_time)
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
            highlight_transformations += [Create(list(new_formula.highlights.values())[i]) for i in range(k, n)]

        return AnimationGroup(transform_text, *highlight_transformations)